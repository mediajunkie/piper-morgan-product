"""#1421: get_default_project is owner-scoped and fail-closed.

Regression: the zero-arg form selected the single process-global is_default row,
so one user's default project became every user's project context (cross-tenant
read; sprint #1424 census S2). Now: owner filter in the WHERE, and no principal
means no default — never another tenant's.

Requires PostgreSQL on 5433 (same as the suite's other DB-backed tests).
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.database.repositories import ProjectRepository

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def two_tenants_with_defaults():
    """Two users, each owning an is_default project. Yields (engine, a_id, b_id, a_name, b_name)."""
    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    a_id, b_id = str(uuid4()), str(uuid4())
    a_name, b_name = f"proj-a-{a_id[:6]}", f"proj-b-{b_id[:6]}"
    now = datetime.now(timezone.utc)
    async with async_session() as s:
        for uid, pname in ((a_id, a_name), (b_id, b_name)):
            await s.execute(
                text(
                    "INSERT INTO users (id, username, email, is_active, is_verified, "
                    "created_at, updated_at, role, is_alpha) "
                    "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
                ),
                {"id": uid, "u": f"t1421_{uid[:8]}", "e": f"t1421_{uid[:8]}@test.example.com", "now": now},
            )
            await s.execute(
                text(
                    "INSERT INTO projects (id, name, owner_id, is_default, is_archived, "
                    "created_at, updated_at) VALUES (:pid, :name, :oid, true, false, :now, :now)"
                ),
                {"pid": str(uuid4()), "name": pname, "oid": uid, "now": now},
            )
        await s.commit()
    try:
        yield engine, a_id, b_id, a_name, b_name
    finally:
        async with async_session() as s:
            for uid in (a_id, b_id):
                await s.execute(text("DELETE FROM projects WHERE owner_id = :uid"), {"uid": uid})
                await s.execute(text("DELETE FROM users WHERE id = :uid"), {"uid": uid})
            await s.commit()
        await engine.dispose()


async def test_each_owner_gets_only_their_own_default(two_tenants_with_defaults):
    engine, a_id, b_id, a_name, b_name = two_tenants_with_defaults
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        a_default = await repo.get_default_project(a_id)
        b_default = await repo.get_default_project(b_id)
    assert a_default is not None and a_default.name == a_name
    assert b_default is not None and b_default.name == b_name
    assert a_default.id != b_default.id


async def test_no_principal_fails_closed(two_tenants_with_defaults):
    """No owner -> None, even though is_default rows exist (the old code would
    have returned one of them — someone else's project)."""
    engine, *_ = two_tenants_with_defaults
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        assert await repo.get_default_project(None) is None
        assert await repo.get_default_project("") is None


async def test_owner_without_default_gets_none(two_tenants_with_defaults):
    engine, *_ = two_tenants_with_defaults
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        assert await repo.get_default_project(str(uuid4())) is None
