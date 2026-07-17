"""#1436 B8: todo creation actually reaches the knowledge graph now.

Regression: ``create_todo`` called ``create_todo_knowledge_node(saved_todo)``
— the signature requires ``(todo, user_id)`` — so every call raised TypeError,
swallowed by a bare ``print()``. The KG never received a single todo node
(census F14: "KG starves"; the write-side gap noted in #1420's close).

DB-backed (the service opens its own session): requires PostgreSQL on 5433.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.todo.todo_management_service import TodoManagementService

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def db_user():
    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    user_id = str(uuid4())
    async with async_session() as s:
        await s.execute(
            text(
                "INSERT INTO users (id, username, email, is_active, is_verified, "
                "created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
            ),
            {
                "id": user_id,
                "u": f"b8_{user_id[:8]}",
                "e": f"b8_{user_id[:8]}@test.example.com",
                "now": datetime.now(timezone.utc),
            },
        )
        await s.commit()
    try:
        yield user_id
    finally:
        async with async_session() as s:
            await s.execute(
                text("DELETE FROM todo_items WHERE owner_id = CAST(:uid AS uuid)"),
                {"uid": user_id},
            )
            await s.execute(
                text(
                    "DELETE FROM items WHERE list_id IN "
                    "(SELECT id FROM lists WHERE owner_id = CAST(:uid AS uuid))"
                ),
                {"uid": user_id},
            )
            await s.execute(
                text("DELETE FROM lists WHERE owner_id = CAST(:uid AS uuid)"), {"uid": user_id}
            )
            await s.execute(text("DELETE FROM users WHERE id = :uid"), {"uid": user_id})
            await s.commit()
        await engine.dispose()


async def test_created_todo_reaches_the_knowledge_graph_with_the_principal(db_user):
    svc = TodoManagementService.__new__(TodoManagementService)
    svc.knowledge_service = AsyncMock()

    todo = await svc.create_todo(user_id=db_user, text="Review PR")

    assert todo is not None
    svc.knowledge_service.create_todo_knowledge_node.assert_awaited_once()
    args = svc.knowledge_service.create_todo_knowledge_node.await_args.args
    assert args[0].text == "Review PR"
    assert args[1] == str(db_user)  # the principal, not a missing arg


async def test_kg_failure_still_creates_the_todo(db_user):
    svc = TodoManagementService.__new__(TodoManagementService)
    svc.knowledge_service = AsyncMock()
    svc.knowledge_service.create_todo_knowledge_node.side_effect = RuntimeError("kg down")

    todo = await svc.create_todo(user_id=db_user, text="Still works")
    assert todo is not None and todo.text == "Still works"
