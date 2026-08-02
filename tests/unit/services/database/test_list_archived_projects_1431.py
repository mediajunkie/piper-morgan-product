"""#1431: list_archived_projects returns archived projects, owner-scoped.

Regression (F20, census 2026-07-16): PortfolioService.list_archived_projects
filtered the output of a helper that only called the repo's
list_active_projects — whose query filters is_archived == False. Intersecting
that with p.is_archived is mathematically always empty, so the archived list
was always []. Fix: a dedicated owner-scoped ProjectRepository method
(list_archived_projects, mirroring list_active_projects) and the service uses
it directly.

Requires PostgreSQL on 5433 (same as the suite's other DB-backed tests).
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.database.repositories import ProjectRepository
from services.onboarding.portfolio_service import PortfolioService

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def two_tenants_with_archives():
    """Two users: A owns one active + one archived project, B owns one archived.

    Yields (engine, a_id, b_id, a_active_name, a_archived_name, b_archived_name).
    """
    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    a_id, b_id = str(uuid4()), str(uuid4())
    a_active_name = f"proj-a-active-{a_id[:6]}"
    a_archived_name = f"proj-a-archived-{a_id[:6]}"
    b_archived_name = f"proj-b-archived-{b_id[:6]}"
    now = datetime.now(timezone.utc)
    async with async_session() as s:
        for uid in (a_id, b_id):
            await s.execute(
                text(
                    "INSERT INTO users (id, username, email, is_active, is_verified, "
                    "created_at, updated_at, role, is_alpha) "
                    "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
                ),
                {"id": uid, "u": f"t1431_{uid[:8]}", "e": f"t1431_{uid[:8]}@test.example.com", "now": now},
            )
        for pname, oid, archived in (
            (a_active_name, a_id, False),
            (a_archived_name, a_id, True),
            (b_archived_name, b_id, True),
        ):
            await s.execute(
                text(
                    "INSERT INTO projects (id, name, owner_id, is_default, is_archived, "
                    "created_at, updated_at) VALUES (:pid, :name, :oid, false, :arch, :now, :now)"
                ),
                {"pid": str(uuid4()), "name": pname, "oid": oid, "arch": archived, "now": now},
            )
        await s.commit()
    try:
        yield engine, a_id, b_id, a_active_name, a_archived_name, b_archived_name
    finally:
        async with async_session() as s:
            for uid in (a_id, b_id):
                await s.execute(text("DELETE FROM projects WHERE owner_id = :uid"), {"uid": uid})
                await s.execute(text("DELETE FROM users WHERE id = :uid"), {"uid": uid})
            await s.commit()
        await engine.dispose()


# =============================================================================
# Repository level
# =============================================================================


async def test_repo_archived_project_appears(two_tenants_with_archives):
    """The archived project is returned; the active one is not."""
    engine, a_id, _, a_active_name, a_archived_name, _ = two_tenants_with_archives
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        archived = await repo.list_archived_projects(owner_id=a_id)
    names = [p.name for p in archived]
    assert a_archived_name in names
    assert a_active_name not in names


async def test_repo_archived_list_is_owner_scoped(two_tenants_with_archives):
    """User A's archived list never contains user B's archived project (ADR-079)."""
    engine, a_id, b_id, _, a_archived_name, b_archived_name = two_tenants_with_archives
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        a_archived = await repo.list_archived_projects(owner_id=a_id)
        b_archived = await repo.list_archived_projects(owner_id=b_id)
    assert [p.name for p in a_archived] == [a_archived_name]
    assert [p.name for p in b_archived] == [b_archived_name]


# =============================================================================
# Service level
# =============================================================================


class _FakeProjectRepository:
    """Stateful in-memory stand-in exposing the repo surface the service uses.

    Why not the real repo for the archive->list flow: BaseRepository.update is
    broken against ProjectRepository (get_by_id returns a domain object, update
    then session.refresh()es it -> UnmappedInstanceError). Pre-existing latent
    bug, discovered while testing #1431 and tracked separately; the DB-backed
    tests above cover the new query, this covers the service flow.
    """

    def __init__(self, projects):
        self._projects = {p.id: p for p in projects}

    async def get_by_id(self, project_id):
        return self._projects.get(project_id)

    async def update(self, project_id, **kwargs):
        project = self._projects.get(project_id)
        for key, value in kwargs.items():
            setattr(project, key, value)
        return project

    async def list_active_projects(self, owner_id=None):
        return [
            p for p in self._projects.values()
            if not p.is_archived and p.owner_id == owner_id
        ]

    async def list_archived_projects(self, owner_id=None):
        return [
            p for p in self._projects.values()
            if p.is_archived and p.owner_id == owner_id
        ]


async def test_service_archive_then_appears_in_archived_list():
    """Archive a project via the service -> it appears in the archived list;
    the active list no longer contains it."""
    from services.domain.models import Project

    user_id = str(uuid4())
    now = datetime.now(timezone.utc)
    target = Project(
        id=str(uuid4()),
        owner_id=user_id,
        name="SoonArchived",
        description="",
        is_archived=False,
        created_at=now,
        updated_at=now,
    )
    service = PortfolioService(_FakeProjectRepository([target]))

    assert [p.id for p in await service.list_active_projects(user_id)] == [target.id]
    assert await service.list_archived_projects(user_id) == []

    result = await service.archive_project(target.id, user_id)
    assert result.success, result.message

    archived_after = await service.list_archived_projects(user_id)
    assert [p.id for p in archived_after] == [target.id]
    assert await service.list_active_projects(user_id) == []


async def test_service_archived_list_not_empty_regression(two_tenants_with_archives):
    """The F20 bug: this list was mathematically always []. It must not be."""
    engine, a_id, _, _, a_archived_name, _ = two_tenants_with_archives
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        service = PortfolioService(ProjectRepository(s))
        archived = await service.list_archived_projects(a_id)
    assert [p.name for p in archived] == [a_archived_name]
