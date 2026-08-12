"""#1603: chat-path todo completion against the REAL repository.

PM's live failure (2026-08-12): every chat 'complete todo N' returned
"I had trouble marking that as complete." Root cause: todo_items.id /
owner_id are String columns, and the chat handler passes a UUID object
(a #1436 type-coercion) — Postgres has no varchar = uuid operator. The
mocked tests stayed green through it (#1548's lesson), so this test
drives handler → service → real repository → real Postgres, with the
handler's actual UUID-typed call. No mocks at the boundary that failed.
"""

import uuid

import pytest
from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Intent
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory


@pytest.fixture
async def repro_user():
    """A scratch user, removed with its todos afterwards."""
    username = f"todo-1603-{uuid.uuid4().hex[:8]}"
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
        await s.execute(
            text("DELETE FROM todo_items WHERE owner_id = :u"), {"u": str(uid)}
        )
        await s.execute(
            text(
                "DELETE FROM items WHERE id NOT IN (SELECT id FROM todo_items) "
                "AND text LIKE 'repro-1603%'"
            )
        )
        await s.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


def _intent(action: str, message: str) -> Intent:
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=1.0,
        context={"original_message": message},
    )


@pytest.mark.asyncio
async def test_complete_todo_1_succeeds_via_real_repository(repro_user):
    """The exact shape PM ran three times: bare 'complete todo 1'."""
    th = TodoIntentHandlers()
    created = await th.todo_service.create_todo(
        text="repro-1603 stretch", user_id=repro_user
    )
    assert created is not None

    out = await th.handle_complete_todo(
        _intent("complete_todo", "complete todo 1"),
        session_id="s-1603",
        user_id=repro_user,
    )

    # The failure mode this pins: the broad catch rendering "I had trouble".
    assert "had trouble" not in out, out
    # And the positive claim must be true in the DB, not just in the prose:
    todos = await th.todo_service.list_todos(
        user_id=repro_user, include_completed=False
    )
    assert todos == [], "todo still active after a claimed completion"


@pytest.mark.asyncio
async def test_uuid_typed_service_call_reaches_string_columns(repro_user):
    """The precise coercion #1436 introduced: service called with UUID(id)."""
    from uuid import UUID

    th = TodoIntentHandlers()
    created = await th.todo_service.create_todo(
        text="repro-1603 uuid-typed", user_id=repro_user
    )
    completed = await th.todo_service.complete_todo(
        todo_id=UUID(created.id), user_id=repro_user
    )
    assert completed is not None, (
        "UUID-typed todo_id must reach the String columns "
        "(repo normalizes at entry — #1603)"
    )
    assert completed.completed is True


@pytest.mark.asyncio
async def test_delete_todo_chat_path(repro_user):
    """delete_todo shares the normalized entry point; pin it too."""
    th = TodoIntentHandlers()
    await th.todo_service.create_todo(
        text="repro-1603 deletable", user_id=repro_user
    )
    out = await th.handle_delete_todo(
        _intent("delete_todo", "delete todo 1"),
        session_id="s-1603",
        user_id=repro_user,
    )
    assert "trouble" not in out.lower(), out
    todos = await th.todo_service.list_todos(
        user_id=repro_user, include_completed=False
    )
    assert todos == []
