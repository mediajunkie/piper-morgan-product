"""#1591 AC: REAL-DB round-trip for the standup-mode preference capture.

The unit suite (tests/unit/services/intent_service/
test_standup_preference_capture_1591.py) proves the flow against an in-memory
persistence double; this file drives the REAL store — users.preferences JSONB
via collaboration_gate's seam, the same row the #1510 rail writes — against
dev Postgres (POSTGRES_PORT=5433, docker compose up -d). Mocked-interface
persistence tests are how #1548/#1603 shipped broken; the mock stays out of
the persistence layer here.

Covers, against the real store:
- the capture loop end-to-end: repeated report choice → the rail's read-back
  armed → acceptance writes the real row (source=user_verified) → the NEXT
  handler run reads the store and asks nothing (honored, not re-inferred)
- a stored standup_mode=interview redirects a generic ask without ever
  running the assembler (stored — not re-inferred each time)
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy import text as _text

from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service import standup_preferences as sp
from services.intent_service import verified_inference as vi
from services.intent_service.workflow_entries import (
    register_default_workflows,
    run_verify_inference_workflow,
)
from services.shared_types import IntentCategory

PROSE = "Here's your derived standup."


async def _seed_user(prefix: str = "su1591") -> str:
    """Seed a real users row (the #1472 idiom, mirrored from the 1510 file)."""
    uid = str(uuid4())
    now = datetime.now(timezone.utc)
    async with AsyncSessionFactory.session_scope_fresh() as s:
        await s.execute(
            _text(
                "INSERT INTO users (id, username, email, is_active, is_verified, "
                "created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
            ),
            {
                "id": uid,
                "u": f"{prefix}_{uid[:8]}",
                "e": f"{prefix}_{uid[:8]}@test.example.com",
                "now": now,
            },
        )
        await s.commit()
    return uid


async def _delete_user(uid: str) -> None:
    async with AsyncSessionFactory.session_scope_fresh() as s:
        await s.execute(_text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


async def _raw_preferences(uid: str) -> dict:
    """Read the JSONB straight off the row (m-43: name the layer — this is
    the store as it actually is, not as any wrapper reports it)."""
    async with AsyncSessionFactory.session_scope_fresh() as s:
        row = await s.execute(
            _text("SELECT preferences FROM users WHERE id = :u"), {"u": uid}
        )
        return row.scalar_one() or {}


@pytest.fixture
async def seeded_user_id():
    uid = await _seed_user()
    yield uid
    await _delete_user(uid)


@pytest.fixture(autouse=True)
def _clean_transient_state():
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()
    yield
    sp._MODE_CHOICES.clear()
    vi._SESSION_DECLINES.clear()


@pytest.fixture
def service():
    register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _standup_intent(message: str = "give me my standup") -> Intent:
    return Intent(
        category=IntentCategory.STATUS,
        action="get_standup",
        original_message=message,
        confidence=1.0,
    )


def _summary():
    summary = MagicMock()
    summary.is_empty.return_value = False
    summary.to_prose.return_value = PROSE
    summary.to_dict.return_value = {"sections": []}
    return summary


async def _report_turn(service, sid, user_id, message="give me my standup"):
    with patch(
        "services.standup.assembler.build_user_standup_summary",
        new=AsyncMock(return_value=_summary()),
    ):
        return await service._handle_standup_query(
            _standup_intent(message), "wf-1591-int", session_id=sid, user_id=user_id
        )


async def test_capture_loop_persists_and_second_run_reads_the_real_store(
    service, seeded_user_id
):
    """The whole #1591 capture loop against the real row: two report choices
    → the rail's read-back armed → acceptance persists standup_mode with
    user_verified provenance → the next run reads the STORE (no re-inference,
    no ask)."""
    sid = f"int-1591-{seeded_user_id[:8]}"

    await _report_turn(service, sid, seeded_user_id)
    service.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=seeded_user_id)
    await _report_turn(service, sid, seeded_user_id)

    offer = service.workflow_offer_service.get_and_clear_pending_offer(
        sid, user_id=seeded_user_id
    )
    assert offer is not None
    assert offer["workflow_type"] == vi.VERIFY_INFERENCE_WORKFLOW
    assert offer["pending_action"]["inference_key"] == sp.STANDUP_MODE_KEY

    result = await run_verify_inference_workflow(
        session_id=sid,
        user_id=seeded_user_id,
        context={"pending_action": offer["pending_action"]},
    )
    assert result["intent_data"]["persisted"] is True

    raw = await _raw_preferences(seeded_user_id)
    stored = raw[vi.VERIFIED_INFERENCES_PREF_KEY][sp.STANDUP_MODE_KEY]
    assert stored["value"] == sp.MODE_REPORT
    assert stored["source"] == vi.SOURCE_USER_VERIFIED

    # Second run: honored from the real store — no ask of any kind is armed,
    # and the report renders with the plain discoverability line.
    after = await _report_turn(service, sid, seeded_user_id)
    assert after.message.startswith(f"Good morning! {PROSE}")
    assert service.workflow_offer_service._pending_offers.get(sid) is None
    assert "Say 'my standup interview'" in after.message


async def test_stored_interview_preference_redirects_without_running_the_assembler(
    service, seeded_user_id
):
    """standup_mode=interview in the real store: a generic standup ask
    dispatches the interview and the assembler never runs — 'stored, not
    re-inferred each time' at the real persistence layer."""
    ok = await vi.store_verified_inference(
        seeded_user_id, sp.STANDUP_MODE_KEY, sp.MODE_INTERVIEW, confidence=0.55
    )
    assert ok is True

    sentinel = IntentProcessingResult(
        success=True, message="interview started", intent_data={"action": "standup_started"}
    )
    service._start_standup_conversation = AsyncMock(return_value=sentinel)
    with patch("services.standup.assembler.build_user_standup_summary") as assembler:
        result = await service._handle_standup_query(
            _standup_intent("give me my standup"),
            "wf-1591-int-2",
            session_id=f"int-1591-red-{seeded_user_id[:8]}",
            user_id=seeded_user_id,
        )
    assert result is sentinel
    assembler.assert_not_called()
    service._start_standup_conversation.assert_awaited_once()
