"""#1735 — the auto-apply joint of the personalization learning loop.

BEFORE (the defect these pins were written red against, 2026-09-24):
``PreferenceDetectionHandler.apply_auto_preferences`` built a pattern dict with
keys ``dimension``/``new_value``/``hint_id``/``source`` and handed it to
``UserPreferenceManager.apply_preference_pattern``, whose gate reads
``pattern["confidence"]`` (absent → 0.0 < 0.7) and ``pattern["pattern_data"]``
(absent → no ``preference_key``). The gate returned ``False`` before writing
anything — and the caller **discarded that return value**, appended the hint to
its ``applied`` list anyway and logged ``"Auto-applied preference for …"``. A
silent total no-op that reported success: m-44 ("clear" is not a measurement)
inside the learning loop itself.

AFTER: the pattern carries the hint's own confidence and a real
``pattern_data`` (``personality_{dimension}`` → value, the SAME key
``confirm_preference`` writes on the user-accepted path), the write goes to
USER scope so it lands in ``users.preferences["upm"]`` (DB-backed since #1574 —
session scope is in-memory by design and would evaporate), and a rejected write
is reported LOUD: a warning naming the reason plus an ``errors`` entry, never a
fabricated ``applied`` row.

LAYER (m-43): these pins measure **the store**, not the return dict — a fresh
``UserPreferenceManager`` (= a restart) reads back what the handler wrote, which
is the only layer on which "the loop is connected" can be true. Two of them use
the REAL local Postgres through the real session factory with a per-run UUID
user deleted by exact id in ``finally`` (#1813 shape, mirroring
``test_preference_persistence_1574``); the loud-failure pins are pure in-process.

DENOMINATOR: the auto-apply joint only (joint 3 of #1735's four). Joints 1
(PersonalizationContext.upsert writer-less), 2 (nothing reads personality_*) and
4 (users.preferences has no learning writer) are NOT addressed here — they are
the design decision #1735 reserves for Arch/PM. See
``dev/2026/09/24/1735-learning-loop-census-and-decision-2026-09-24.md``.
"""

from __future__ import annotations

import logging
import uuid

import pytest
import pytest_asyncio
from sqlalchemy import delete

from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.domain.user_preference_manager import UserPreferenceManager
from services.intent_service.preference_handler import PreferenceDetectionHandler
from services.personality.preference_detection import (
    DetectionMethod,
    PreferenceDimension,
    PreferenceHint,
)

pytestmark = pytest.mark.asyncio


def _auto_apply_hint(user_id: str, **overrides) -> PreferenceHint:
    """A REAL learned hint that passes ``is_ready_for_auto_apply`` — confidence
    at/above AUTO_APPLY_THRESHOLD (0.9) from an explicit-feedback detection.
    This is the exact object ``IntentProcessingHooks._run_preference_detection``
    forwards from ``ConversationAnalyzer.analyze_message``."""
    kwargs = dict(
        id=f"hint_{uuid.uuid4().hex[:8]}",
        user_id=user_id,
        dimension=PreferenceDimension.TECHNICAL,
        current_value="BALANCED",
        detected_value="DETAILED",
        confidence_score=0.95,
        detection_method=DetectionMethod.EXPLICIT_FEEDBACK,
        source_text="I prefer technical detail",
    )
    kwargs.update(overrides)
    return PreferenceHint(**kwargs)


@pytest_asyncio.fixture
async def db_user():
    uid = uuid.uuid4()
    tag = uid.hex[:12]
    async with AsyncSessionFactory.session_scope_fresh() as s:
        s.add(
            User(
                id=uid,
                username=f"autoapply-1735-{tag}",
                email=f"autoapply-1735-{tag}@test.local",
                is_active=True,
                is_verified=True,
                preferences={"existing_key": "untouched"},
            )
        )
        await s.commit()
    try:
        yield uid
    finally:
        async with AsyncSessionFactory.session_scope_fresh() as s:
            await s.execute(delete(User).where(User.id == uid))
            await s.commit()


class TestAutoApplyActuallyWrites:
    """THE #1735 pin: auto-apply must land in the store the learning writes to."""

    async def test_auto_apply_lands_in_the_upm_store_a_fresh_manager_can_read(self, db_user):
        """RED before the fix: the gate rejected the malformed pattern and
        nothing was ever written, so the fresh manager read ``None``."""
        handler = PreferenceDetectionHandler()
        hint = _auto_apply_hint(str(db_user))

        result = await handler.apply_auto_preferences(str(db_user), "session_1735", [hint])

        assert result["success"] is True, result
        assert result["errors"] == []

        fresh = UserPreferenceManager()
        assert (
            await fresh.get_preference("personality_technical_depth", user_id=db_user) == "DETAILED"
        )

    async def test_auto_apply_uses_the_same_key_as_the_user_accepted_path(self, db_user):
        """``confirm_preference`` writes ``personality_{dimension}``; auto-apply
        must not invent a second namespace or the two halves of one loop
        disagree about where a learned preference lives."""
        handler = PreferenceDetectionHandler()
        await handler.apply_auto_preferences(
            str(db_user),
            None,
            [
                _auto_apply_hint(
                    str(db_user), dimension=PreferenceDimension.WARMTH, detected_value=0.8
                )
            ],
        )

        fresh = UserPreferenceManager()
        stored = await fresh.get_all_preferences(user_id=db_user)
        assert "personality_warmth_level" in stored, stored
        # ...and the write is namespaced: unrelated keys in the same JSONB column survive (#1574).
        async with AsyncSessionFactory.session_scope_fresh() as s:
            row = await s.get(User, db_user)
            assert row.preferences["existing_key"] == "untouched"

    async def test_report_agrees_with_the_store(self, db_user):
        """The report must not be able to say ``applied`` while the store is
        empty — that fabricated agreement is what made the no-op invisible for
        16 days."""
        handler = PreferenceDetectionHandler()
        result = await handler.apply_auto_preferences(
            str(db_user), None, [_auto_apply_hint(str(db_user))]
        )

        fresh = UserPreferenceManager()
        stored = await fresh.get_preference("personality_technical_depth", user_id=db_user)
        assert bool(result["applied"]) == (stored is not None)


class TestAutoApplyFailsLoud:
    """When the write genuinely cannot happen, it is reported — never silent."""

    async def test_unusable_hint_is_reported_loud_not_silently_skipped(self, caplog):
        """A hint whose detected value is absent cannot supply
        ``pattern_data.preference_value``. The requirement is not that this
        succeed — it is that it NEVER returns a clean success."""
        handler = PreferenceDetectionHandler()
        hint = _auto_apply_hint("user123", detected_value=None)

        with caplog.at_level(logging.WARNING, logger="services.intent_service.preference_handler"):
            result = await handler.apply_auto_preferences("user123", None, [hint])

        assert result["success"] is False, result
        assert result["applied"] == []
        assert len(result["errors"]) == 1
        assert result["errors"][0]["reason"]
        assert any("auto_apply" in r.getMessage() for r in caplog.records), caplog.text

    async def test_gate_rejection_is_reported_loud_with_the_missing_keys(self, caplog, monkeypatch):
        """If ``apply_preference_pattern``'s gate ever rejects the pattern
        again (threshold change, shape drift), the caller must name it rather
        than fabricate an ``applied`` row. Drives the real gate by forcing a
        False return."""
        handler = PreferenceDetectionHandler()

        async def _reject(*_args, **_kwargs):
            return False

        monkeypatch.setattr(handler.preference_manager, "apply_preference_pattern", _reject)

        with caplog.at_level(logging.WARNING, logger="services.intent_service.preference_handler"):
            result = await handler.apply_auto_preferences(
                "user123", None, [_auto_apply_hint("user123")]
            )

        assert result["success"] is False, result
        assert result["applied"] == []
        assert result["errors"] and "reject" in result["errors"][0]["reason"].lower()
        assert any("auto_apply" in r.getMessage() for r in caplog.records), caplog.text

    async def test_hints_below_the_auto_apply_bar_are_skipped_without_an_error(self):
        """Not every skip is a failure: a hint that is not ready for auto-apply
        is correctly ignored, and that must not be reported as an error (or the
        loud channel becomes noise nobody reads — the m-44 inverse)."""
        handler = PreferenceDetectionHandler()
        low = _auto_apply_hint("user123", confidence_score=0.5)
        result = await handler.apply_auto_preferences("user123", None, [low])
        assert result == {"success": True, "applied": [], "errors": []}


class TestNamedResidualReadersAreDbBacked:
    """#1735 named three readers that "silently reset on restart" because they
    treated a per-instance dict as persistent: ``calendar_setup_offered``
    (#790), ``slack_default_channel`` and ``notion_database`` (#693).

    #1574 fixed the MECHANISM under all three — every one is
    ``get_preference(key, user_id=...)``, which is read-through/write-through to
    ``users.preferences["upm"]``. But #1574's own pins exercise the generic
    ``set_preference``/``get_preference`` with the key ``"timezone"``; nothing
    pinned these three by name, so "already fixed" was a code-reading claim
    rather than a measured one. These pin it at the TYPED-ACCESSOR layer
    (m-43), across a fresh-manager boundary (= a restart), so the claim is
    checkable and a future refactor of any accessor cannot silently re-strand it.
    """

    async def test_calendar_setup_offer_state_survives_a_restart(self, db_user):
        await UserPreferenceManager().set_calendar_setup_offer_state(db_user, "declined")
        assert await UserPreferenceManager().get_calendar_setup_offer_state(db_user) == "declined"

    async def test_slack_default_channel_survives_a_restart(self, db_user):
        await UserPreferenceManager().set_slack_default_channel(db_user, "#standups")
        assert await UserPreferenceManager().get_slack_default_channel(db_user) == "#standups"

    async def test_notion_database_survives_a_restart(self, db_user):
        await UserPreferenceManager().set_notion_database(db_user, "db-1735")
        assert await UserPreferenceManager().get_notion_database(db_user) == "db-1735"
