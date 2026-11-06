"""#2271 (CXO 11-06): an exact name that matches only an ARCHIVED project answers
'"Beta" is already archived. Say "restore project Beta" to bring it back.' This pins,
against the REAL repository, that the line is true: the archive handler sees the
archived row, and "restore project <name>" through the restore handler restores
exactly that row by its exact name, even with a near active match ("<name> Launch")
present.

Requires PostgreSQL on 5433 (same as the suite's other DB-backed tests).
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def archived_beta():
    """One user owning an ARCHIVED "Beta<id>" and an ACTIVE "Beta<id> Launch"."""
    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    user_id = str(uuid4())
    archived_id, near_id = str(uuid4()), str(uuid4())
    name = f"Beta{user_id[:6]}"
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
                "u": f"t2271_{user_id[:8]}",
                "e": f"t2271_{user_id[:8]}@test.example.com",
                "now": now,
            },
        )
        for pid, pname, archived in ((archived_id, name, True), (near_id, f"{name} Launch", False)):
            await s.execute(
                text(
                    "INSERT INTO projects (id, name, owner_id, is_default, is_archived, "
                    "created_at, updated_at) VALUES (:pid, :name, :oid, false, :arch, :now, :now)"
                ),
                {"pid": pid, "name": pname, "oid": user_id, "arch": archived, "now": now},
            )
        await s.commit()
    try:
        yield engine, user_id, name, archived_id, near_id
    finally:
        from tests.conftest import delete_test_user_fully

        async with async_session() as s:
            await delete_test_user_fully(s, user_id)
        await engine.dispose()


async def _archived(engine, project_id):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        row = (
            await s.execute(
                text("SELECT is_archived FROM projects WHERE id = :pid"), {"pid": project_id}
            )
        ).first()
    return row[0]


def _intent(message):
    from services.domain.models import Intent, IntentCategory

    return Intent(
        category=IntentCategory.PORTFOLIO,
        action="archive_project",
        confidence=0.95,
        original_message=message,
        context={"original_message": message},
    )


async def test_archived_exact_name_points_at_restore_and_restore_by_that_name_works(
    archived_beta,
):
    from services.intent_service.canonical_handlers import CanonicalHandlers

    engine, user_id, name, archived_id, near_id = archived_beta
    handlers = CanonicalHandlers()

    out = await handlers._handle_archive_project(
        _intent(f"archive project {name}"), "s-2271", user_id
    )
    assert out["message"] == (
        f'"{name}" is already archived. Say "restore project {name}" to bring it back.'
    )
    assert await _archived(engine, near_id) is False  # the near active match is untouched

    restored = await handlers._handle_restore_project(
        _intent(f"restore project {name}"), "s-2271", user_id
    )
    assert restored["intent"]["action"] == "restore_project", restored
    assert await _archived(engine, archived_id) is False
    assert await _archived(engine, near_id) is False
