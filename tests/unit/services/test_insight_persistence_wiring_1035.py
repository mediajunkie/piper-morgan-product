"""
#1035 Phase 6 — End-to-end persistence wiring tests.

Verifies the gameplan-mandated invariant: insights composted in one
"process" survive across to a different repository instance reading the
same DB. This is the canonical "did the persistence actually work" test —
without it, the InsightJournal rewrite is just async indirection over a
dict.

Uses in-memory SQLite via aiosqlite + a single shared engine across
two distinct sessions (simulating "wrote in session A, read in session B
as if after a restart").

Wiring chain verified:
    SurfaceableInsight → InsightRepository.add (session A) → DB row →
    InsightRepository.get/list (session B, fresh) → SurfaceableInsight

Repository tests at test_insight_repository_1035.py exercise individual
methods within a single session. This file specifically verifies the
cross-session durability that #1035 promises.
"""

from __future__ import annotations

import os
import tempfile

import pytest
import pytest_asyncio


aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from services.database.models import InsightDB  # noqa: E402
from services.database.repositories import InsightRepository  # noqa: E402
from services.mux.composting_models import ExtractedLearning, Pattern  # noqa: E402
from services.mux.composting_pipeline import SurfaceableInsight  # noqa: E402


pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def shared_engine():
    """File-backed SQLite engine that persists across sessions within
    the same test (simulating cross-restart durability that #1035 promises)."""
    fd, db_path = tempfile.mkstemp(suffix=".sqlite", prefix="insight_wiring_")
    os.close(fd)
    try:
        engine = create_async_engine(f"sqlite+aiosqlite:///{db_path}")
        async with engine.begin() as conn:
            await conn.run_sync(
                lambda sync_conn: InsightDB.__table__.create(sync_conn, checkfirst=True)
            )
        yield engine
        await engine.dispose()
    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


def _make_insight(*, user_id: str = "alpha", confidence: float = 0.85) -> SurfaceableInsight:
    learning = ExtractedLearning(
        pattern=Pattern(description="user front-loads small tasks"),
        confidence=confidence,
        applies_to_entities=["deadlines"],
        topic_tags=["work-patterns"],
        expression="Having reflected, you tend to front-load small tasks",
    )
    return SurfaceableInsight(
        object_id=f"obj-{user_id}",
        user_id=user_id,
        learning=learning,
    )


async def test_insight_persists_across_sessions(shared_engine):
    """Write in session A, read in session B (fresh) — insight survives."""
    SessionLocal = async_sessionmaker(
        shared_engine, class_=AsyncSession, expire_on_commit=False
    )

    insight = _make_insight()

    # Session A: write
    async with SessionLocal() as session_a:
        repo_a = InsightRepository(session_a)
        await repo_a.add(insight)
        await session_a.commit()

    # Session B (fresh): read
    async with SessionLocal() as session_b:
        repo_b = InsightRepository(session_b)
        retrieved = await repo_b.get(insight.id)
        assert retrieved is not None
        assert retrieved.id == insight.id
        assert retrieved.user_id == "alpha"
        assert retrieved.learning.confidence == 0.85
        assert retrieved.learning.expression == insight.learning.expression


async def test_user_scoping_holds_across_sessions(shared_engine):
    """Bravo's insights stay invisible to alpha across sessions."""
    SessionLocal = async_sessionmaker(
        shared_engine, class_=AsyncSession, expire_on_commit=False
    )

    alpha_insight = _make_insight(user_id="alpha")
    bravo_insight = _make_insight(user_id="bravo")

    async with SessionLocal() as session_a:
        repo = InsightRepository(session_a)
        await repo.add(alpha_insight)
        await repo.add(bravo_insight)
        await session_a.commit()

    # Fresh session
    async with SessionLocal() as session_b:
        repo = InsightRepository(session_b)
        alpha_results = await repo.list_for_user("alpha")
        bravo_results = await repo.list_for_user("bravo")
        assert {i.id for i in alpha_results} == {alpha_insight.id}
        assert {i.id for i in bravo_results} == {bravo_insight.id}


async def test_mark_surfaced_persists_across_sessions(shared_engine):
    """Surface event written in session A is visible in session B."""
    SessionLocal = async_sessionmaker(
        shared_engine, class_=AsyncSession, expire_on_commit=False
    )

    insight = _make_insight()

    async with SessionLocal() as session_a:
        repo = InsightRepository(session_a)
        await repo.add(insight)
        await session_a.commit()

    async with SessionLocal() as session_b:
        repo = InsightRepository(session_b)
        await repo.mark_surfaced(insight.id, response="engaged")
        await session_b.commit()

    async with SessionLocal() as session_c:
        repo = InsightRepository(session_c)
        retrieved = await repo.get(insight.id)
        assert retrieved is not None
        assert retrieved.surfaced_count == 1
        assert retrieved.user_response == "engaged"
        assert retrieved.last_surfaced is not None


async def test_clear_persists_per_user_across_sessions(shared_engine):
    """Per-user clear removes only that user's insights, durably."""
    SessionLocal = async_sessionmaker(
        shared_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with SessionLocal() as session_a:
        repo = InsightRepository(session_a)
        await repo.add(_make_insight(user_id="alpha"))
        await repo.add(_make_insight(user_id="alpha"))
        await repo.add(_make_insight(user_id="bravo"))
        await session_a.commit()

    async with SessionLocal() as session_b:
        repo = InsightRepository(session_b)
        deleted = await repo.clear(user_id="alpha")
        await session_b.commit()
        assert deleted == 2

    async with SessionLocal() as session_c:
        repo = InsightRepository(session_c)
        assert await repo.count(user_id="alpha") == 0
        assert await repo.count(user_id="bravo") == 1
