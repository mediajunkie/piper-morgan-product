"""#1472 AC: real-DB round-trip for the retrospective completed-todos lookup.

`_get_completed_todos_for_date` (canonical_handlers, #501) was dead in three
stacked ways, all swallowed into the #1425 None sentinel:
  1. `TodoDB.status == TodoStatus.COMPLETED` — raw enum against a String
     column; asyncpg DataError ("expected str, got TodoStatus").
  2. `todo.title` — TodoDB has no `title` (text was title; only the DOMAIN
     Todo grew a title property).
  3. `todo.priority.value` — TodoDB.priority is a plain str.
So "what did I get done yesterday" ALWAYS reported "couldn't check", never
the real completed list. This test seeds a real completed todo and requires
the lookup to return it.

Requires live Postgres (POSTGRES_PORT=5433, docker compose up -d).
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text as _text

from services.database.session_factory import AsyncSessionFactory
from services.domain.models import Todo
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.repositories.todo_repository import TodoRepository


async def _seed_user(prefix: str = "retro1472") -> str:
    """Seed a real users row (owner_id is a UUID FK, #484/#1312)."""
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
        await s.execute(
            _text("DELETE FROM personalization_contexts WHERE owner_id = CAST(:u AS uuid)"),
            {"u": uid},
        )
        await s.execute(_text("DELETE FROM users WHERE id = :u"), {"u": uid})
        await s.commit()


@pytest.fixture
async def seeded_user_id():
    uid = await _seed_user()
    yield uid
    await _delete_user(uid)


async def test_completed_todo_round_trips_into_retrospective(seeded_user_id):
    """Seed a completed todo; the retrospective lookup must return it (not None)."""
    now = datetime.now(timezone.utc)
    todo_id = str(uuid4())

    async with AsyncSessionFactory.session_scope_fresh() as session:
        repo = TodoRepository(session)
        await repo.create_todo(
            Todo(
                id=todo_id,
                text="Shipped the retrospective fix",
                priority="high",
                owner_id=seeded_user_id,
                status="completed",
                completed=True,
                completed_at=now,
                created_at=now,
                updated_at=now,
            )
        )
        await session.commit()

    try:
        result = await CanonicalHandlers()._get_completed_todos_for_date(
            session_id=seeded_user_id, target_date=now
        )

        # Old behavior: DataError/AttributeError -> swallow -> None sentinel
        # ("couldn't check"). Required behavior: the real completed list.
        assert result is not None, (
            "retrospective lookup returned the #1425 None sentinel — the query "
            "or row-shaping crashed (raw enum bind / .title / .priority.value, #1472)"
        )
        assert len(result) == 1
        assert result[0]["title"] == "Shipped the retrospective fix"
        assert result[0]["priority"] == "high"
        assert result[0]["completed_at"] is not None
    finally:
        async with AsyncSessionFactory.session_scope_fresh() as s:
            await s.execute(_text("DELETE FROM todo_items WHERE id = :i"), {"i": todo_id})
            await s.execute(_text("DELETE FROM items WHERE id = :i"), {"i": todo_id})
            await s.commit()
