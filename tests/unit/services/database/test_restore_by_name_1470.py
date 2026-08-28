"""#1470: restore-by-name chat path can never find an archived project.

Regression (found while fixing #1464): the restore chat path calls
`PortfolioService.find_project_by_name(..., include_archived=True)`, but the
service delegated to `ProjectRepository.find_by_name`, whose query included
`ProjectDB.is_archived == False` unconditionally. The service-level
`include_archived` flag only governed a POST-filter on a result set that could
never contain archived rows — so "Restore project X" always answered
"I couldn't find an archived project called 'X'".

Fix: thread `include_archived` into the repository query (same conditional
filter shape `search_projects` already uses) and pass it through from
`PortfolioService.find_project_by_name`.

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
async def owner_with_archived_project():
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
                "u": f"t1470_{user_id[:8]}",
                "e": f"t1470_{user_id[:8]}@test.example.com",
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


async def _row_archived(engine, project_id):
    """is_archived straight from the table — verification at the DB layer."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        row = (
            await s.execute(
                text("SELECT is_archived FROM projects WHERE id = :pid"), {"pid": project_id}
            )
        ).first()
    return row[0] if row else None


# =============================================================================
# Repository level — the #1470 defect itself
# =============================================================================


async def test_repo_find_by_name_include_archived_finds_archived_row(
    owner_with_archived_project,
):
    """include_archived=True must return an archived project by name.

    Before the fix the query hard-filtered `is_archived == False`, so this
    returned None for every archived project regardless of any flag.
    """
    engine, user_id, _, _, archived_id, archived_name = owner_with_archived_project
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        project = await repo.find_by_name(
            name=archived_name, owner_id=user_id, include_archived=True
        )
    assert project is not None, "archived project not found with include_archived=True"
    assert project.id == archived_id
    assert project.is_archived is True


async def test_repo_find_by_name_default_still_excludes_archived(
    owner_with_archived_project,
):
    """Guard: default (include_archived=False) behavior is unchanged —
    archived rows stay invisible, active rows stay findable."""
    engine, user_id, active_id, active_name, _, archived_name = owner_with_archived_project
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        repo = ProjectRepository(s)
        assert await repo.find_by_name(name=archived_name, owner_id=user_id) is None
        active = await repo.find_by_name(name=active_name, owner_id=user_id)
    assert active is not None and active.id == active_id


# =============================================================================
# Service level — flag threads through instead of dead post-filtering
# =============================================================================


async def test_service_find_project_by_name_include_archived(owner_with_archived_project):
    engine, user_id, _, _, archived_id, archived_name = owner_with_archived_project
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        service = PortfolioService(ProjectRepository(s))
        found = await service.find_project_by_name(
            name=archived_name, user_id=user_id, include_archived=True
        )
        hidden = await service.find_project_by_name(name=archived_name, user_id=user_id)
    assert found is not None and found.id == archived_id
    assert hidden is None  # default still hides archived


# =============================================================================
# Chat path — "Restore project X" end-to-end with the REAL repo
# =============================================================================


async def test_chat_restore_by_name_returns_success_and_unarchives(
    owner_with_archived_project,
):
    """ "Restore project X" through _handle_portfolio_query with the REAL repo.

    Before the fix this always hit the not-found branch ("I couldn't find an
    archived project called 'X'") because find_by_name could never return an
    archived row. Asserts the fixed path returns the restore success message
    and actually un-archives the row.
    """
    from services.domain.models import Intent, IntentCategory
    from services.intent_service.canonical_handlers import CanonicalHandlers

    engine, user_id, _, _, archived_id, archived_name = owner_with_archived_project

    handlers = CanonicalHandlers()
    message = f"Restore project {archived_name}"
    intent = Intent(
        category=IntentCategory.PORTFOLIO,
        action="portfolio_query",
        confidence=0.95,
        original_message=message,
        context={"original_message": message},
    )
    result = await handlers._handle_portfolio_query(intent, f"session-{user_id[:8]}", user_id)

    assert result["intent"]["action"] == "restore_project", result
    assert result["intent"]["context"]["status"] == "success", result
    assert "I've restored" in result["message"], result
    assert "couldn't find an archived project" not in result["message"]

    archived = await _row_archived(engine, archived_id)
    assert archived is False
