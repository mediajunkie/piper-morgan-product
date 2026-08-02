"""#1464: BaseRepository mutations must operate on the ORM row, not get_by_id().

Regression (found by the #1431 subagent, upgraded to LIVE by Lead triage):
`ProjectRepository.get_by_id` returns a DOMAIN `Project`, but the inherited
`BaseRepository.update` treated that return as a mapped ORM entity —
`setattr` then `session.refresh(entity)` → UnmappedInstanceError. Every
PortfolioService mutation (archive/restore/delete) crashed against the real
repository, chat-reachable via canonical_handlers "Archive my project X".

Second latent shape pinned here: `BaseRepository.delete` never awaited
`session.delete(entity)` (a coroutine in SQLAlchemy 2.x), so base delete was
a silent no-op (returned True, row survived) for EVERY subclass.

Fix: base mutations fetch the ORM row via `_get_db_row` (session.get) — the
idiom ArtifactRepository.delete/update_title already use.

Requires PostgreSQL on 5433 (same as the suite's other DB-backed tests).
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.database.models import ProjectDB
from services.database.repositories import ProjectRepository
from services.onboarding.portfolio_service import PortfolioService

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def owner_with_projects():
    """One user owning one active + one archived project.

    Yields (engine, user_id, active_id, active_name, archived_id, archived_name).
    Teardown via the canonical #1452 cascade (delete_test_user_fully).
    """
    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    user_id = str(uuid4())
    active_id, archived_id = str(uuid4()), str(uuid4())
    active_name = f"proj-live-{user_id[:6]}"
    archived_name = f"proj-arch-{user_id[:6]}"
    now = datetime.now(timezone.utc)
    async with async_session() as s:
        await s.execute(
            text(
                "INSERT INTO users (id, username, email, is_active, is_verified, "
                "created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
            ),
            {
                "id": user_id,
                "u": f"t1464_{user_id[:8]}",
                "e": f"t1464_{user_id[:8]}@test.example.com",
                "now": now,
            },
        )
        for pid, pname, archived in (
            (active_id, active_name, False),
            (archived_id, archived_name, True),
        ):
            await s.execute(
                text(
                    "INSERT INTO projects (id, name, owner_id, is_default, is_archived, "
                    "created_at, updated_at) VALUES (:pid, :name, :oid, false, :arch, :now, :now)"
                ),
                {"pid": pid, "name": pname, "oid": user_id, "arch": archived, "now": now},
            )
        await s.commit()
    try:
        yield engine, user_id, active_id, active_name, archived_id, archived_name
    finally:
        from tests.conftest import delete_test_user_fully

        async with async_session() as s:
            await delete_test_user_fully(s, user_id)
        await engine.dispose()


async def _row_state(engine, project_id):
    """(exists, is_archived) straight from the table — verification at the DB layer."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        row = (
            await s.execute(
                text("SELECT is_archived FROM projects WHERE id = :pid"), {"pid": project_id}
            )
        ).first()
    return (row is not None, row[0] if row else None)


# =============================================================================
# Repository level — the #1464 crash itself
# =============================================================================


async def test_repo_update_flips_is_archived(owner_with_projects):
    """update() on the real ProjectRepository must not UnmappedInstanceError,
    and the flag must actually land in the table."""
    engine, _, active_id, _, _, _ = owner_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        updated = await repo.update(active_id, is_archived=True, updated_at=datetime.now())
        assert updated is not None
        assert isinstance(updated, ProjectDB)  # mutation returns the ORM row
        await s.commit()
    exists, archived = await _row_state(engine, active_id)
    assert exists and archived is True


async def test_repo_update_missing_id_returns_none(owner_with_projects):
    engine, *_ = owner_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        assert await repo.update(str(uuid4()), is_archived=True) is None


async def test_repo_delete_actually_deletes(owner_with_projects):
    """Pins BOTH bugs: no UnmappedInstanceError, and the row is really gone
    (the un-awaited session.delete used to no-op while returning True)."""
    engine, _, _, _, archived_id, _ = owner_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        assert await repo.delete(archived_id) is True
        await s.commit()
    exists, _ = await _row_state(engine, archived_id)
    assert exists is False


# =============================================================================
# Service level — archive/restore/delete end-to-end against the REAL repo
# =============================================================================


async def test_service_archive_project_end_to_end(owner_with_projects):
    engine, user_id, active_id, active_name, _, _ = owner_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        service = PortfolioService(ProjectRepository(s))
        result = await service.archive_project(active_id, user_id)
        assert result.success, result.message
        assert result.project is not None and result.project.is_archived is True
        assert active_name in result.message
        await s.commit()
        # Appears in the archived list, gone from the active list
        assert active_id in [p.id for p in await service.list_archived_projects(user_id)]
        assert active_id not in [p.id for p in await service.list_active_projects(user_id)]
    _, archived = await _row_state(engine, active_id)
    assert archived is True


async def test_service_restore_project_end_to_end(owner_with_projects):
    engine, user_id, _, _, archived_id, archived_name = owner_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        service = PortfolioService(ProjectRepository(s))
        result = await service.restore_project(archived_id, user_id)
        assert result.success, result.message
        assert result.project is not None and result.project.is_archived is False
        assert archived_name in result.message
        await s.commit()
        assert archived_id in [p.id for p in await service.list_active_projects(user_id)]
    _, archived = await _row_state(engine, archived_id)
    assert archived is False


async def test_service_archive_not_owner_refused(owner_with_projects):
    """Ownership pre-check still holds (no scoping regression from the fix)."""
    engine, _, active_id, _, _, _ = owner_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        service = PortfolioService(ProjectRepository(s))
        result = await service.archive_project(active_id, str(uuid4()))
        assert not result.success
    _, archived = await _row_state(engine, active_id)
    assert archived is False


async def test_service_delete_project_confirmed(owner_with_projects):
    engine, user_id, active_id, _, _, _ = owner_with_projects
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        service = PortfolioService(ProjectRepository(s))
        result = await service.delete_project(active_id, user_id, confirmed=True)
        assert result.success, result.message
        await s.commit()
    exists, _ = await _row_state(engine, active_id)
    assert exists is False


# =============================================================================
# Chat path — canonical handler archive flow (canonical_handlers.py, #675 wiring)
# =============================================================================


async def test_chat_archive_handler_returns_success_message(owner_with_projects, monkeypatch):
    """"Archive my project X" through _handle_portfolio_query with the REAL repo.

    Before the fix this crashed in PortfolioService.archive_project and the
    handler's broad `except Exception` (#1423 shape) swallowed it into the
    generic "I'm having trouble managing projects right now." — this asserts
    the FIXED path returns the success message and actually archives the row.
    """
    from services.domain.models import Intent, IntentCategory
    from services.intent_service.canonical_handlers import CanonicalHandlers

    engine, user_id, active_id, active_name, _, _ = owner_with_projects

    handlers = CanonicalHandlers()
    message = f"Archive my project {active_name}"
    intent = Intent(
        category=IntentCategory.PORTFOLIO,
        action="portfolio_query",
        confidence=0.95,
        original_message=message,
        context={"original_message": message},
    )
    result = await handlers._handle_portfolio_query(intent, f"session-{user_id[:8]}", user_id)

    assert result["intent"]["action"] == "archive_project", result
    assert result["intent"]["context"]["status"] == "success", result
    assert "I've archived" in result["message"], result
    assert "having trouble managing projects" not in result["message"]

    _, archived = await _row_state(engine, active_id)
    assert archived is True
