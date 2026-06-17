"""
#1035 Phase 3 — InsightRepository unit tests.

Mirrors the #1018 EthicsAuditRepository test pattern: in-memory SQLite via
aiosqlite, table created via SQLAlchemy metadata, full CRUD + query-shape
coverage for the new repository layer that backs the rewritten InsightJournal.

Methods covered:
- add / get
- list_for_user (recency-ordered)
- get_for_object
- get_unsurfaced (Push candidate retrieval; trust gate + confidence + cooldown)
- get_for_context (Pull relevance scoring)
- mark_surfaced (state mutation: count + last_surfaced + user_response)
- count (total / per-user)
- clear (per-user)

User-scoping verified throughout per PM directive (May 3 #1035 Q5).
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
import pytest_asyncio


# Skip module if aiosqlite missing (parallel to #1018 pattern).
aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402

from services.database.models import InsightDB  # noqa: E402
from services.database.repositories import InsightRepository  # noqa: E402
from services.mux.composting_models import ExtractedLearning, Pattern  # noqa: E402
from services.mux.composting_pipeline import SurfaceableInsight  # noqa: E402


pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def session():
    """Fresh in-memory SQLite session per test with insights table created."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: InsightDB.__table__.create(sync_conn, checkfirst=True)
        )

    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s

    await engine.dispose()


def _make_insight(
    *,
    user_id: str = "alpha",
    object_id: str | None = None,
    confidence: float = 0.85,
    topic_tags: list[str] | None = None,
    applies_to_entities: list[str] | None = None,
    context_tags: list[str] | None = None,
    min_trust_stage: int = 1,
    surfaced_count: int = 0,
    last_surfaced: datetime | None = None,
    user_response: str | None = None,
    created_at: datetime | None = None,
) -> SurfaceableInsight:
    """Helper: build a SurfaceableInsight with sensible defaults."""
    learning = ExtractedLearning(
        pattern=Pattern(description=f"pattern for {user_id}"),
        confidence=confidence,
        applies_to_entities=applies_to_entities or [],
        topic_tags=topic_tags or [],
        expression=f"Having reflected, {user_id}'s pattern.",
    )
    return SurfaceableInsight(
        object_id=object_id or f"obj-{uuid4().hex[:8]}",
        user_id=user_id,
        learning=learning,
        min_trust_stage=min_trust_stage,
        context_tags=context_tags or [],
        surfaced_count=surfaced_count,
        last_surfaced=last_surfaced,
        user_response=user_response,
        created_at=created_at or datetime.now(timezone.utc),
    )


# =============================================================================
# Basic CRUD
# =============================================================================


async def test_add_and_get_roundtrip(session):
    repo = InsightRepository(session)
    insight = _make_insight()
    await repo.add(insight)
    await session.commit()

    fetched = await repo.get(insight.id)
    assert fetched is not None
    assert fetched.id == insight.id
    assert fetched.user_id == insight.user_id
    assert fetched.learning.confidence == insight.learning.confidence


async def test_get_returns_none_for_missing_id(session):
    repo = InsightRepository(session)
    fetched = await repo.get("does-not-exist")
    assert fetched is None


# =============================================================================
# Listing
# =============================================================================


async def test_list_for_user_returns_only_user_insights(session):
    """User-scoping: alpha sees only alpha's insights, not bravo's."""
    repo = InsightRepository(session)
    a1 = _make_insight(user_id="alpha")
    a2 = _make_insight(user_id="alpha")
    b1 = _make_insight(user_id="bravo")
    for ins in (a1, a2, b1):
        await repo.add(ins)
    await session.commit()

    alpha_results = await repo.list_for_user("alpha")
    assert len(alpha_results) == 2
    assert {i.id for i in alpha_results} == {a1.id, a2.id}

    bravo_results = await repo.list_for_user("bravo")
    assert len(bravo_results) == 1
    assert bravo_results[0].id == b1.id


async def test_list_for_user_recency_ordered(session):
    """Newest insight first."""
    repo = InsightRepository(session)
    now = datetime.now(timezone.utc)
    older = _make_insight(user_id="alpha", created_at=now - timedelta(days=5))
    newer = _make_insight(user_id="alpha", created_at=now)
    await repo.add(older)
    await repo.add(newer)
    await session.commit()

    results = await repo.list_for_user("alpha")
    assert results[0].id == newer.id
    assert results[1].id == older.id


async def test_list_for_user_honors_limit(session):
    repo = InsightRepository(session)
    for _ in range(5):
        await repo.add(_make_insight(user_id="alpha"))
    await session.commit()

    results = await repo.list_for_user("alpha", limit=2)
    assert len(results) == 2


async def test_get_for_object_filters_by_object_id(session):
    repo = InsightRepository(session)
    obj_a = "obj-shared"
    obj_b = "obj-other"
    i1 = _make_insight(user_id="alpha", object_id=obj_a)
    i2 = _make_insight(user_id="alpha", object_id=obj_a)
    i3 = _make_insight(user_id="alpha", object_id=obj_b)
    for ins in (i1, i2, i3):
        await repo.add(ins)
    await session.commit()

    results = await repo.get_for_object(obj_a)
    assert {i.id for i in results} == {i1.id, i2.id}


async def test_get_for_object_scopes_by_principal_1252(session):
    """#1252 (a,3) fix: get_for_object scopes to the principal when one is
    provided. Two users with insights on the SAME object_id must not see each
    other's — the cross-owner leak (fetch-by-object, no owner filter) closed."""
    repo = InsightRepository(session)
    shared = "obj-shared"
    a1 = _make_insight(user_id="alpha", object_id=shared)
    a2 = _make_insight(user_id="alpha", object_id=shared)
    b1 = _make_insight(user_id="beta", object_id=shared)
    for ins in (a1, a2, b1):
        await repo.add(ins)
    await session.commit()

    alpha = await repo.get_for_object(shared, user_id="alpha")
    assert {i.id for i in alpha} == {a1.id, a2.id}
    beta = await repo.get_for_object(shared, user_id="beta")
    assert {i.id for i in beta} == {b1.id}


async def test_get_for_object_no_principal_is_unscoped_shim_1252(session):
    """m-40 shim: omitting the principal returns ALL insights for the object
    (+ a logged WARNING) — non-breaking until every caller threads the
    principal. Behaviour-preserving for the pre-existing unscoped callers."""
    repo = InsightRepository(session)
    shared = "obj-shared"
    a1 = _make_insight(user_id="alpha", object_id=shared)
    b1 = _make_insight(user_id="beta", object_id=shared)
    for ins in (a1, b1):
        await repo.add(ins)
    await session.commit()

    everyone = await repo.get_for_object(shared)
    assert {i.id for i in everyone} == {a1.id, b1.id}


# =============================================================================
# Push candidate retrieval (get_unsurfaced)
# =============================================================================


async def test_get_unsurfaced_excludes_surfaced(session):
    repo = InsightRepository(session)
    fresh = _make_insight(user_id="alpha", surfaced_count=0)
    surfaced = _make_insight(user_id="alpha", surfaced_count=1)
    await repo.add(fresh)
    await repo.add(surfaced)
    await session.commit()

    results = await repo.get_unsurfaced(user_id="alpha", min_confidence=0.5, trust_stage=4)
    assert len(results) == 1
    assert results[0].id == fresh.id


async def test_get_unsurfaced_honors_trust_gate(session):
    """Insights with min_trust_stage=3 invisible to Stage 1-2 users."""
    repo = InsightRepository(session)
    stage1_eligible = _make_insight(user_id="alpha", min_trust_stage=1)
    stage3_eligible = _make_insight(user_id="alpha", min_trust_stage=3)
    await repo.add(stage1_eligible)
    await repo.add(stage3_eligible)
    await session.commit()

    stage1_results = await repo.get_unsurfaced(user_id="alpha", trust_stage=1, min_confidence=0.5)
    assert {i.id for i in stage1_results} == {stage1_eligible.id}

    stage3_results = await repo.get_unsurfaced(user_id="alpha", trust_stage=3, min_confidence=0.5)
    assert {i.id for i in stage3_results} == {stage1_eligible.id, stage3_eligible.id}


async def test_get_unsurfaced_excludes_low_confidence(session):
    repo = InsightRepository(session)
    high = _make_insight(user_id="alpha", confidence=0.9)
    low = _make_insight(user_id="alpha", confidence=0.5)
    await repo.add(high)
    await repo.add(low)
    await session.commit()

    results = await repo.get_unsurfaced(user_id="alpha", min_confidence=0.75, trust_stage=4)
    assert len(results) == 1
    assert results[0].id == high.id


# =============================================================================
# Pull relevance scoring (get_for_context)
# =============================================================================


async def test_get_for_context_scores_by_overlap(session):
    """More overlap → higher rank. Insights with no overlap excluded."""
    repo = InsightRepository(session)
    relevant = _make_insight(
        user_id="alpha",
        topic_tags=["deadlines", "scheduling"],
        applies_to_entities=["sprint-planning"],
    )
    less_relevant = _make_insight(user_id="alpha", topic_tags=["scheduling"])
    irrelevant = _make_insight(user_id="alpha", topic_tags=["unrelated"])
    for ins in (relevant, less_relevant, irrelevant):
        await repo.add(ins)
    await session.commit()

    results = await repo.get_for_context(
        user_id="alpha",
        context_topics=["deadlines", "scheduling"],
        context_entities=["sprint-planning"],
        trust_stage=4,
    )
    assert len(results) == 2  # irrelevant excluded
    assert results[0].id == relevant.id  # higher overlap first
    assert results[1].id == less_relevant.id


async def test_get_for_context_user_scoped(session):
    """Bravo's insights never returned for alpha's context query."""
    repo = InsightRepository(session)
    alpha_insight = _make_insight(user_id="alpha", topic_tags=["deadlines"])
    bravo_insight = _make_insight(user_id="bravo", topic_tags=["deadlines"])
    await repo.add(alpha_insight)
    await repo.add(bravo_insight)
    await session.commit()

    results = await repo.get_for_context(
        user_id="alpha",
        context_topics=["deadlines"],
        trust_stage=4,
    )
    assert {i.id for i in results} == {alpha_insight.id}


# =============================================================================
# State mutation (mark_surfaced)
# =============================================================================


async def test_mark_surfaced_increments_count(session):
    repo = InsightRepository(session)
    insight = _make_insight(user_id="alpha")
    await repo.add(insight)
    await session.commit()

    updated = await repo.mark_surfaced(insight.id, response="engaged")
    await session.commit()

    assert updated is not None
    assert updated.surfaced_count == 1
    assert updated.user_response == "engaged"
    assert updated.last_surfaced is not None


async def test_mark_surfaced_returns_none_for_missing_id(session):
    repo = InsightRepository(session)
    result = await repo.mark_surfaced("does-not-exist", response="engaged")
    assert result is None


# =============================================================================
# Counting + clearing
# =============================================================================


async def test_count_total_and_per_user(session):
    repo = InsightRepository(session)
    await repo.add(_make_insight(user_id="alpha"))
    await repo.add(_make_insight(user_id="alpha"))
    await repo.add(_make_insight(user_id="bravo"))
    await session.commit()

    assert await repo.count() == 3
    assert await repo.count(user_id="alpha") == 2
    assert await repo.count(user_id="bravo") == 1


async def test_clear_is_per_user(session):
    """PM directive May 3: clear() is per-user only, never system-wide."""
    repo = InsightRepository(session)
    await repo.add(_make_insight(user_id="alpha"))
    await repo.add(_make_insight(user_id="alpha"))
    await repo.add(_make_insight(user_id="bravo"))
    await session.commit()

    deleted = await repo.clear(user_id="alpha")
    await session.commit()
    assert deleted == 2
    assert await repo.count(user_id="alpha") == 0
    # Bravo's data is untouched
    assert await repo.count(user_id="bravo") == 1
