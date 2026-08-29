"""#1651 AC — PM's transcript pinned e2e against REAL Postgres.

PM live 2026-08-18: standup → "Want me to … mark that overdue todo done?" →
"Yes mark the overdue todo done." → "I couldn't find a todo matching
'overdue'". The fix binds the overdue todo's id into the #846 pending-offer
carrier at offer time; this file proves the whole loop against the real todo
store (POSTGRES_PORT=5433, docker compose up -d) — mocked-interface
persistence tests are how #1548/#1603 shipped broken, so the mock stays out
of the persistence layer here.

Layer honesty (m-43): what is REAL here is the layer that failed live — the
todo rows (seeded via ``TodoManagementService``, the same service the chat
path writes through), the owner-scoped overdue resolution, the #846 carrier
through ``IntentService.process_intent``, and the completion write asserted
by re-reading the ROW BY ID. What is mocked: the LLM boundary (explosive —
both turns must resolve deterministically) and the standup assembler
boundary (a deterministic non-empty summary — the radar sources are not this
issue's layer; the empty-report branch deliberately doesn't arm this offer).
"""

import uuid
from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy import text as _text

from services.database.session_factory import AsyncSessionFactory
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.standup_todo_offer import (
    STANDUP_COMPLETE_TODO_WORKFLOW,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.todo.todo_management_service import TodoManagementService

PROSE = "Here's your derived standup."


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Both turns in
    the transcript must resolve deterministically (the standup claim, then
    the pending-offer seam)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1651 turns must resolve " "deterministically"
        )


@pytest.fixture
async def repro_user():
    """A scratch user, removed with its todos afterwards (the #1544 idiom)."""
    username = f"todo-1651-{uuid.uuid4().hex[:8]}"
    async with AsyncSessionFactory.session_scope() as s:
        r = await s.execute(
            _text(
                "INSERT INTO users (username, email, is_active) "
                "VALUES (:u, :e, true) RETURNING id"
            ),
            {"u": username, "e": f"{username}@example.com"},
        )
        uid = r.scalar()
        await s.commit()
    yield uid
    async with AsyncSessionFactory.session_scope() as s:
        await s.execute(_text("DELETE FROM todo_items WHERE owner_id = :u"), {"u": str(uid)})
        await s.execute(
            _text(
                "DELETE FROM items WHERE id NOT IN (SELECT id FROM todo_items) "
                "AND text LIKE 'repro-1651%'"
            )
        )
        # process_intent seeds a personalization row for the principal — it
        # references users and must go first (the #1472 teardown idiom).
        await s.execute(
            _text("DELETE FROM personalization_contexts " "WHERE owner_id = CAST(:u AS uuid)"),
            {"u": str(uid)},
        )
        await s.execute(_text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


@pytest.fixture
def live_service():
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _summary():
    summary = MagicMock()
    summary.is_empty.return_value = False
    summary.to_prose.return_value = PROSE
    summary.to_dict.return_value = {"sections": []}
    return summary


async def _standup_turn(service, sid, user_id):
    with patch(
        "services.standup.assembler.build_user_standup_summary",
        new=AsyncMock(return_value=_summary()),
    ):
        return await service.process_intent(
            message="give me my standup", session_id=sid, user_id=str(user_id)
        )


async def _row_completed(todo_id: str) -> bool:
    async with AsyncSessionFactory.session_scope_fresh() as s:
        r = await s.execute(
            _text("SELECT completed FROM todo_items WHERE id = :i"),
            {"i": str(todo_id)},
        )
        return r.scalar_one()


@pytest.mark.asyncio
async def test_pm_transcript_end_to_end_real_todo_completes(repro_user, live_service):
    """The transcript, turn for turn, against the real store. The todo's
    title deliberately shares no word with 'overdue' — a title-matching
    acceptance (the #1651 bug) cannot find it; only the BOUND id can."""
    svc = TodoManagementService()
    overdue = await svc.create_todo(
        user_id=repro_user,
        text="repro-1651 send the beta invite batch",
        due_date=datetime.now(timezone.utc) - timedelta(days=3),
    )
    assert overdue is not None
    sid = f"int-1651-{uuid.uuid4().hex[:8]}"

    # Turn 1 — the report renders complete; the closing offer names its
    # referent and the #846 store binds the REAL row id.
    result = await _standup_turn(live_service, sid, repro_user)
    assert result.message.startswith(f"Good morning! {PROSE}")
    assert '"repro-1651 send the beta invite batch"' in result.message
    assert "(yes/no)" in result.message
    stored = live_service.workflow_offer_service._pending_offers.get(sid)
    assert stored is not None
    assert stored["workflow_type"] == STANDUP_COMPLETE_TODO_WORKFLOW
    assert stored["pending_action"]["todo_id"] == str(overdue.id)  # bound id

    # Turn 2 — PM's verbatim acceptance. The REAL row flips to completed.
    result2 = await live_service.process_intent(
        message="Yes mark the overdue todo done.",
        session_id=sid,
        user_id=str(repro_user),
    )
    assert "repro-1651 send the beta invite batch" in result2.message
    assert "couldn't find a todo matching" not in result2.message  # the bug's copy
    assert await _row_completed(overdue.id) is True


@pytest.mark.asyncio
async def test_crisp_yes_completes_and_decline_leaves_row(repro_user, live_service):
    svc = TodoManagementService()
    overdue = await svc.create_todo(
        user_id=repro_user,
        text="repro-1651 pay the invoice",
        due_date=datetime.now(timezone.utc) - timedelta(days=5),
    )
    sid = f"int-1651-{uuid.uuid4().hex[:8]}"

    # Decline first: the row stays pending, the offer is consumed.
    await _standup_turn(live_service, sid, repro_user)
    declined = await live_service.process_intent(
        message="no", session_id=sid, user_id=str(repro_user)
    )
    assert '"repro-1651 pay the invoice" stays on your list' in declined.message
    assert await _row_completed(overdue.id) is False
    assert live_service.workflow_offer_service._pending_offers.get(sid) is None

    # A fresh report re-offers (declining an action is not the #1591 mode
    # decline — the referent is still overdue); crisp "yes" completes it.
    await _standup_turn(live_service, sid, repro_user)
    accepted = await live_service.process_intent(
        message="yes", session_id=sid, user_id=str(repro_user)
    )
    assert "repro-1651 pay the invoice" in accepted.message
    assert await _row_completed(overdue.id) is True


@pytest.mark.asyncio
async def test_no_actionable_referent_arms_no_bound_offer(repro_user, live_service):
    """AC: a user whose todos are all future-dated (or absent) gets the
    ordinary #1591 trailing — never the bound completion workflow."""
    svc = TodoManagementService()
    await svc.create_todo(
        user_id=repro_user,
        text="repro-1651 plan next sprint",
        due_date=datetime.now(timezone.utc) + timedelta(days=30),
    )
    sid = f"int-1651-{uuid.uuid4().hex[:8]}"
    result = await _standup_turn(live_service, sid, repro_user)
    assert result.intent_data.get("standup_todo_offer_pending") is None
    stored = live_service.workflow_offer_service._pending_offers.get(sid)
    if stored is not None:  # the #1591 invitation may legitimately arm
        assert stored["workflow_type"] != STANDUP_COMPLETE_TODO_WORKFLOW
    assert "overdue" not in result.message
