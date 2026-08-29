"""#1666: chat-path todo deletion against the REAL repository, #1190-gated.

Drives the REAL ``IntentService.process_intent`` (explosive LLM boundary,
classification stubbed per turn — the #1605/#1650 idiom) with NO mock at the
todo boundary: handler → service → real repository → real Postgres (the
#1603 lesson — the mocked tests stayed green through a real chat-path
failure).

What this pins that the unit e2e can't: the row itself.
- confirm turn: the ask renders the REAL stored todo text; the row survives;
- crisp "yes": the row is GONE from the database;
- "no": the row is still there.
"""

import uuid
from types import SimpleNamespace

import pytest
from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1666 turns must resolve " "deterministically"
        )


@pytest.fixture
async def repro_user():
    """A scratch user, removed with its todos afterwards (#1603 idiom)."""
    username = f"todo-1666-{uuid.uuid4().hex[:8]}"
    async with AsyncSessionFactory.session_scope() as s:
        r = await s.execute(
            text(
                "INSERT INTO users (username, email, is_active) "
                "VALUES (:u, :e, true) RETURNING id"
            ),
            {"u": username, "e": f"{username}@example.com"},
        )
        uid = r.scalar()
        await s.commit()
    yield uid
    async with AsyncSessionFactory.session_scope() as s:
        await s.execute(text("DELETE FROM todo_items WHERE owner_id = :u"), {"u": str(uid)})
        # process_intent seeds an ADR-075 personalization row for a new user:
        await s.execute(
            text("DELETE FROM personalization_contexts WHERE owner_id = :u"),
            {"u": uid},
        )
        await s.execute(
            text(
                "DELETE FROM items WHERE id NOT IN (SELECT id FROM todo_items) "
                "AND text LIKE 'repro-1666%'"
            )
        )
        await s.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


@pytest.fixture
def live_service():
    # The app registers the rail at startup (container/initialization.py) —
    # mirror it here; idempotent.
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _stub_classification(monkeypatch, service, message, action):
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)


async def _active_texts(service, user_id):
    todos = await service.todo_handlers.todo_service.list_todos(
        user_id=user_id, include_completed=False
    )
    return [t.text for t in todos]


@pytest.mark.asyncio
async def test_confirmed_yes_deletes_the_real_row(repro_user, live_service, monkeypatch):
    """confirm ask (real title bound, row untouched) → crisp yes → row GONE."""
    created = await live_service.todo_handlers.todo_service.create_todo(
        text="repro-1666 delete me", user_id=repro_user
    )
    assert created is not None
    sid = "s-1666-yes"

    _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
    asked = await live_service.process_intent(
        message="delete todo 1", session_id=sid, user_id=str(repro_user)
    )
    # startswith: a first-response personalization notice (ADR-075 OQ-3) may
    # be appended once for a brand-new user — orthogonal to the confirm ask.
    assert asked.message.startswith('Delete todo 1: "repro-1666 delete me"? (yes/no)')
    assert asked.intent_data.get("destructive_confirmation_pending") is True
    # The ask turn deleted nothing — the row is still in Postgres:
    assert await _active_texts(live_service, repro_user) == ["repro-1666 delete me"]

    confirmed = await live_service.process_intent(
        message="yes", session_id=sid, user_id=str(repro_user)
    )
    assert "had trouble" not in confirmed.message, confirmed.message
    assert "repro-1666 delete me" in confirmed.message
    # The positive claim must be true in the DB, not just the prose (#1603):
    assert await _active_texts(live_service, repro_user) == []
    async with AsyncSessionFactory.session_scope() as s:
        r = await s.execute(
            text("SELECT count(*) FROM todo_items WHERE owner_id = :u"),
            {"u": str(repro_user)},
        )
        assert r.scalar() == 0, "row still present after a claimed deletion"


@pytest.mark.asyncio
async def test_decline_keeps_the_real_row(repro_user, live_service, monkeypatch):
    """confirm ask → 'no' → honest cancel copy, row still present."""
    created = await live_service.todo_handlers.todo_service.create_todo(
        text="repro-1666 keep me", user_id=repro_user
    )
    assert created is not None
    sid = "s-1666-no"

    _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
    asked = await live_service.process_intent(
        message="delete todo 1", session_id=sid, user_id=str(repro_user)
    )
    assert asked.message.startswith('Delete todo 1: "repro-1666 keep me"? (yes/no)')

    declined = await live_service.process_intent(
        message="no", session_id=sid, user_id=str(repro_user)
    )
    assert "Nothing has been changed" in declined.message
    assert await _active_texts(live_service, repro_user) == ["repro-1666 keep me"]
    async with AsyncSessionFactory.session_scope() as s:
        r = await s.execute(
            text("SELECT count(*) FROM todo_items WHERE owner_id = :u"),
            {"u": str(repro_user)},
        )
        assert r.scalar() == 1, "row vanished on a DECLINED delete (#1666 breach)"
