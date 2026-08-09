"""#1501: ProjectQueryService reads are owner-scoped and fail-closed.

Regression: find_project_by_name(name) matched ANY tenant's project,
list_active_projects()/count_active_projects() returned global data — the
service passed no principal to the repository, so its optional owner filter
never engaged (cross-tenant read, live in beta). Same shape #1421 fixed for
get_default_project in this same service; these tests mirror
test_default_project_owner_scoped_1421.py.

Now: owner_id is a required argument on all three; no principal means empty
([]/None/0) — never global, and never another tenant's row.

DB-backed tests require PostgreSQL on 5433 (same as the suite's other
DB-backed tests). The fail-closed short-circuit tests use a tripwire repo and
need no DB.

Audit standing rule (principal-dropping audit 2026-08-08): every test of a
principal-keyed surface asserts at least once under a NON-None principal —
see test_cross_user_name_lookup_cannot_return_other_tenants_project and
test_list_and_count_scoped_per_owner.
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.database.repositories import ProjectRepository
from services.queries.project_queries import ProjectQueryService

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def two_tenants_with_projects():
    """Two users, each owning one active project. Yields (engine, a_id, b_id, a_name, b_name)."""
    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    a_id, b_id = str(uuid4()), str(uuid4())
    a_name, b_name = f"proj-a-1501-{a_id[:6]}", f"proj-b-1501-{b_id[:6]}"
    now = datetime.now(timezone.utc)
    async with async_session() as s:
        for uid, pname in ((a_id, a_name), (b_id, b_name)):
            await s.execute(
                text(
                    "INSERT INTO users (id, username, email, is_active, is_verified, "
                    "created_at, updated_at, role, is_alpha) "
                    "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
                ),
                {"id": uid, "u": f"t1501_{uid[:8]}", "e": f"t1501_{uid[:8]}@test.example.com", "now": now},
            )
            await s.execute(
                text(
                    "INSERT INTO projects (id, name, owner_id, is_default, is_archived, "
                    "created_at, updated_at) VALUES (:pid, :name, :oid, false, false, :now, :now)"
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


def _service(session) -> ProjectQueryService:
    return ProjectQueryService(ProjectRepository(session))


async def test_cross_user_name_lookup_cannot_return_other_tenants_project(
    two_tenants_with_projects,
):
    """User B looking up user A's project name gets None; A gets their own row."""
    engine, a_id, b_id, a_name, _b_name = two_tenants_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        svc = _service(s)
        # Authenticated (non-None principal) — the leak: this returned A's project.
        assert await svc.find_project_by_name(a_name, owner_id=b_id) is None
        mine = await svc.find_project_by_name(a_name, owner_id=a_id)
    assert mine is not None
    assert mine.name == a_name
    assert mine.owner_id == a_id


async def test_list_and_count_scoped_per_owner(two_tenants_with_projects):
    """Each owner's list/count covers exactly their own projects."""
    engine, a_id, b_id, a_name, b_name = two_tenants_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        svc = _service(s)
        a_projects = await svc.list_active_projects(a_id)
        b_projects = await svc.list_active_projects(b_id)
        a_count = await svc.count_active_projects(a_id)
        b_count = await svc.count_active_projects(b_id)
    assert [p.name for p in a_projects] == [a_name]
    assert [p.name for p in b_projects] == [b_name]
    assert all(p.owner_id == a_id for p in a_projects)
    assert all(p.owner_id == b_id for p in b_projects)
    assert (a_count, b_count) == (1, 1)


async def test_no_principal_fails_closed_even_when_rows_exist(two_tenants_with_projects):
    """No owner -> empty/None/0, even though matching rows exist (the old code
    returned them — someone else's projects)."""
    engine, _a_id, _b_id, a_name, _b_name = two_tenants_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        svc = _service(s)
        for no_principal in (None, ""):
            assert await svc.find_project_by_name(a_name, owner_id=no_principal) is None
            assert await svc.list_active_projects(no_principal) == []
            assert await svc.count_active_projects(no_principal) == 0


class _TripwireRepo:
    """Fails the test if the service touches the repository at all."""

    def __getattr__(self, name):
        raise AssertionError(
            f"fail-closed path must not reach the repository (attempted .{name})"
        )


async def test_fail_closed_short_circuits_before_repository():
    """The no-principal path returns empty WITHOUT querying — same fail-closed
    contract as #1421's get_default_project. No DB required."""
    svc = ProjectQueryService(_TripwireRepo())
    assert await svc.find_project_by_name("anything", owner_id=None) is None
    assert await svc.list_active_projects(None) == []
    assert await svc.count_active_projects(None) == 0
