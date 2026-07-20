"""B3 (#1394 / ADR-078 D2/OQ-3) — pre-classifier referent resolution.

"change the title" after creating issue #107 → emit `update_issue` resolved to #107
(NOT the document/Notion misroute, NOT create_issue). Deterministic detection (OQ-2),
emit-directly (OQ-3), owner-scoped ledger read (D1a). The guards are load-bearing:
N1 (no-referent → no emit), N2 (fresh topic → no emit), N3 (resolved → update_issue,
never create_issue).
"""

import contextlib

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import SessionActivityDB  # noqa: E402
from services.database.repositories import SessionActivityRepository  # noqa: E402
from services.intent_service.classifier import (  # noqa: E402
    IntentClassifier,
    _detect_issue_referent,
)

_CONV = "conv-b3-1"
_USER = "owner-b3"


class TestDetection:
    """Pure deterministic detection — the N2 guard lives here (field-word requirement)."""

    @pytest.mark.parametrize("msg", [
        "change the title to Foo",
        "add a label to it",
        "update the body",
        "rename the title",
        "set the description",
    ])
    def test_positive_referents_detected(self, msg):
        assert _detect_issue_referent(msg) is True

    @pytest.mark.parametrize("msg", [
        "the roadmap needs restructuring",   # N2: fresh topic, no field word
        "change it to red",                  # pronoun but no field word → N2 safe
        "what did we create this session",   # not an update
        "create an issue about testing",     # creation, not update
        "change the title of issue #107 to Foo",  # explicit # → nothing to resolve
        "",
    ])
    def test_non_referents_pass_through(self, msg):
        assert _detect_issue_referent(msg) is False


@pytest_asyncio.fixture
async def sm(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: SessionActivityDB.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    import services.database.session_factory as sf

    monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


async def _seed_issue(maker, owner, conv, ref="mediajunkie/test-piper-morgan#107", title="Fix login"):
    async with maker() as s:
        await SessionActivityRepository(s).record(
            owner_id=owner, conversation_id=conv,
            action_type="issue_created", target_ref=ref, target_title=title,
        )


class TestResolveEmit:
    pytestmark = pytest.mark.asyncio

    async def test_p1_resolves_to_update_issue(self, sm):
        await _seed_issue(sm, _USER, _CONV)
        intent = await IntentClassifier._resolve_issue_referent(
            "change the title to Foo", _USER, _CONV
        )
        assert intent is not None
        assert intent.action == "update_issue"                     # NOT create_issue (N3)
        assert intent.context["repository"] == "mediajunkie/test-piper-morgan"
        assert intent.context["issue_number"] == 107
        assert intent.original_message == "change the title to Foo"  # raw preserved (#1332)

    async def test_p2_pronoun_resolves(self, sm):
        await _seed_issue(sm, _USER, _CONV)
        intent = await IntentClassifier._resolve_issue_referent(
            "add a label to it", _USER, _CONV
        )
        assert intent is not None
        assert intent.action == "update_issue"
        assert intent.context["issue_number"] == 107


class TestGuards:
    pytestmark = pytest.mark.asyncio

    async def test_n1_empty_ledger_no_emit(self, sm):
        """No creation this session → pass through unchanged (no fabricated target)."""
        intent = await IntentClassifier._resolve_issue_referent(
            "change the title to Foo", _USER, _CONV
        )
        assert intent is None

    async def test_n2_fresh_topic_no_emit(self, sm):
        """Fresh definite-article topic after a creation → NOT hijacked."""
        await _seed_issue(sm, _USER, _CONV)
        intent = await IntentClassifier._resolve_issue_referent(
            "the roadmap needs restructuring", _USER, _CONV
        )
        assert intent is None

    async def test_n3_never_create_issue(self, sm):
        """The resolved path emits update_issue, never create_issue — by construction."""
        await _seed_issue(sm, _USER, _CONV)
        intent = await IntentClassifier._resolve_issue_referent(
            "change the title to Foo", _USER, _CONV
        )
        assert intent.action != "create_issue"
        assert intent.action == "update_issue"

    async def test_d1a_no_principal_no_read(self, sm):
        """No user_id/session_id → no ledger read, no resolution."""
        assert await IntentClassifier._resolve_issue_referent(
            "change the title to Foo", None, _CONV
        ) is None
        assert await IntentClassifier._resolve_issue_referent(
            "change the title to Foo", _USER, None
        ) is None

    async def test_d1a_owner_scoped(self, sm):
        """Another user's creation in the same conversation is not resolved."""
        await _seed_issue(sm, "other-user", _CONV, ref="o/r#999")
        intent = await IntentClassifier._resolve_issue_referent(
            "change the title to Foo", _USER, _CONV
        )
        assert intent is None  # _USER has no creation → no fabrication


class TestLiveWiring:
    """The 2026-07-19 live-scenario gap: B3 was built and green here, but the
    chat path never delivered session_id to classify() — Stage-0 read a null
    session, found nothing, and fell through on EVERY live turn. These tests
    exercise the real call-path wiring so the gap can't silently reopen.
    """

    pytestmark = pytest.mark.asyncio

    async def test_classify_threads_session_id_to_stage0(self, sm):
        """classify(session_id=...) must reach the ledger read and emit the
        resolved intent — no LLM, no cache, no context dict involved."""
        await _seed_issue(sm, _USER, _CONV)
        clf = IntentClassifier()
        intent = await clf.classify(
            "change the title to Foo", user_id=_USER, session_id=_CONV
        )
        assert intent.action == "update_issue"
        assert intent.context["issue_number"] == 107

    async def test_referent_never_served_from_cache(self, sm):
        """Stage-0 runs ABOVE the cache: a referent-shaped message must resolve
        against THIS session's ledger even when a (cross-session) cache entry
        exists for the identical message text."""
        await _seed_issue(sm, _USER, _CONV)
        clf = IntentClassifier()
        clf.cache.set(
            "change the title to Foo",
            {"category": "EXECUTION", "action": "update_document", "confidence": 0.99},
        )
        intent = await clf.classify(
            "change the title to Foo", user_id=_USER, session_id=_CONV
        )
        assert intent.action == "update_issue"  # B3 won; the stale cache did not

    async def test_classify_multiple_passes_session_id_through(self, sm):
        await _seed_issue(sm, _USER, _CONV)
        clf = IntentClassifier()
        result = await clf.classify_multiple(
            "change the title to Foo", user_id=_USER, session_id=_CONV
        )
        assert result.intents and result.intents[0].action == "update_issue"

    async def test_process_intent_call_site_wires_session_id(self):
        """The intent_service call site (the one that was missing it) must pass
        session_id as its own kwarg — not inside context (context would inject
        into the LLM prompt and disable the classifier cache)."""
        from unittest.mock import AsyncMock, MagicMock

        from services.intent.intent_service import IntentService
        from services.intent_service.pre_classifier import MultiIntentResult

        svc = IntentService()
        mock_clf = MagicMock()
        mock_clf.classify_multiple = AsyncMock(
            return_value=MultiIntentResult(
                intents=[], original_message="change the title to Foo", is_multi_intent=False
            )
        )
        mock_clf.classify = AsyncMock(side_effect=RuntimeError("fallback reached"))
        svc.intent_classifier = mock_clf
        with contextlib.suppress(Exception):
            await svc.process_intent(
                "change the title to Foo", session_id="sess-wire-1", user_id=_USER
            )
        assert mock_clf.classify_multiple.await_count >= 1
        kwargs = mock_clf.classify_multiple.await_args.kwargs
        assert kwargs.get("session_id") == "sess-wire-1"
        ctx = kwargs.get("context") or {}
        assert "session_id" not in ctx  # the kwarg channel, never the prompt/cache channel
