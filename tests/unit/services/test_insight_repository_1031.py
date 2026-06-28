"""
#1031 — InsightRepository soft-delete + correction extension tests.

Builds on the #1035 repository test pattern (in-memory SQLite, importorskip).
Verifies:
- list_for_user excludes soft-deleted by default
- list_for_user with exclude_deleted=False includes them (admin/diagnostic)
- update_user_correction stores text + sets user_response="corrected"
- update_user_correction returns None when insight not found / cross-user
- soft_delete returns True/False per ownership; cross-user returns False
- soft_delete_all returns count + actually soft-deletes
- Pull/Push retrieval (get_for_context, get_unsurfaced) excludes deleted
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

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
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: InsightDB.__table__.create(sync_conn, checkfirst=True)
        )
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


def _make_insight(*, user_id="alpha", confidence=0.85, min_trust_stage=1):
    learning = ExtractedLearning(
        pattern=Pattern(description="some pattern"),
        confidence=confidence,
        applies_to_entities=["work"],
        topic_tags=["productivity"],
    )
    return SurfaceableInsight(
        object_id=f"obj-{uuid4().hex[:8]}",
        user_id=user_id,
        learning=learning,
        min_trust_stage=min_trust_stage,
    )


# =============================================================================
# list_for_user soft-delete semantics
# =============================================================================


async def test_list_for_user_excludes_soft_deleted_by_default(session):
    repo = InsightRepository(session)
    keeper = _make_insight()
    deleted = _make_insight()
    await repo.add(keeper)
    await repo.add(deleted)
    await session.commit()

    # Soft delete one
    ok = await repo.soft_delete(insight_id=deleted.id, user_id="alpha")
    await session.commit()
    assert ok is True

    results = await repo.list_for_user("alpha")
    assert {i.id for i in results} == {keeper.id}


async def test_list_for_user_includes_deleted_when_exclude_false(session):
    repo = InsightRepository(session)
    keeper = _make_insight()
    deleted = _make_insight()
    await repo.add(keeper)
    await repo.add(deleted)
    await session.commit()
    await repo.soft_delete(deleted.id, "alpha")
    await session.commit()

    results = await repo.list_for_user("alpha", exclude_deleted=False)
    assert {i.id for i in results} == {keeper.id, deleted.id}


# =============================================================================
# update_user_correction
# =============================================================================


async def test_update_user_correction_stores_text_and_sets_response(session):
    repo = InsightRepository(session)
    insight = _make_insight()
    await repo.add(insight)
    await session.commit()

    updated = await repo.update_user_correction(
        insight_id=insight.id,
        user_id="alpha",
        correction_text="actually I do the opposite",
    )
    await session.commit()

    assert updated is not None
    assert updated.user_correction == "actually I do the opposite"
    assert updated.user_response == "corrected"


async def test_update_user_correction_cross_user_returns_none(session):
    repo = InsightRepository(session)
    insight = _make_insight(user_id="alpha")
    await repo.add(insight)
    await session.commit()

    # Bravo tries to correct alpha's insight
    result = await repo.update_user_correction(
        insight_id=insight.id, user_id="bravo", correction_text="trying to corrupt"
    )
    assert result is None
    # And alpha's insight is unchanged
    fresh = await repo.get(insight.id)
    assert fresh.user_correction is None
    assert fresh.user_response != "corrected"


async def test_update_user_correction_missing_insight_returns_none(session):
    repo = InsightRepository(session)
    result = await repo.update_user_correction(
        insight_id="does-not-exist", user_id="alpha", correction_text="x"
    )
    assert result is None


# =============================================================================
# soft_delete
# =============================================================================


async def test_soft_delete_owner_succeeds(session):
    repo = InsightRepository(session)
    insight = _make_insight()
    await repo.add(insight)
    await session.commit()

    ok = await repo.soft_delete(insight.id, "alpha")
    await session.commit()
    assert ok is True
    fetched = await repo.get(insight.id)
    assert fetched.is_deleted is True


async def test_soft_delete_cross_user_returns_false(session):
    repo = InsightRepository(session)
    insight = _make_insight(user_id="alpha")
    await repo.add(insight)
    await session.commit()

    ok = await repo.soft_delete(insight.id, "bravo")
    assert ok is False
    fetched = await repo.get(insight.id)
    assert fetched.is_deleted is False  # untouched


async def test_soft_delete_missing_returns_false(session):
    repo = InsightRepository(session)
    ok = await repo.soft_delete("does-not-exist", "alpha")
    assert ok is False


# =============================================================================
# soft_delete_all
# =============================================================================


async def test_soft_delete_all_per_user_returns_count(session):
    repo = InsightRepository(session)
    await repo.add(_make_insight(user_id="alpha"))
    await repo.add(_make_insight(user_id="alpha"))
    await repo.add(_make_insight(user_id="alpha"))
    await repo.add(_make_insight(user_id="bravo"))
    await session.commit()

    deleted = await repo.soft_delete_all("alpha")
    await session.commit()
    assert deleted == 3

    # Alpha's insights all soft-deleted; Bravo's untouched
    alpha_visible = await repo.list_for_user("alpha")
    bravo_visible = await repo.list_for_user("bravo")
    assert len(alpha_visible) == 0
    assert len(bravo_visible) == 1


async def test_soft_delete_all_idempotent(session):
    """Running reset-all twice should report 0 the second time (already deleted)."""
    repo = InsightRepository(session)
    await repo.add(_make_insight(user_id="alpha"))
    await session.commit()

    first = await repo.soft_delete_all("alpha")
    await session.commit()
    second = await repo.soft_delete_all("alpha")
    await session.commit()
    assert first == 1
    assert second == 0


# =============================================================================
# Soft-deleted excluded from Pull / Push retrieval
# =============================================================================


async def test_get_for_context_excludes_deleted(session):
    """Pull mode (#1030) consumes get_for_context; should not see deleted insights."""
    repo = InsightRepository(session)
    keeper = _make_insight()
    deleted = _make_insight()
    await repo.add(keeper)
    await repo.add(deleted)
    await session.commit()
    await repo.soft_delete(deleted.id, "alpha")
    await session.commit()

    results = await repo.get_for_context(
        user_id="alpha",
        context_topics=["productivity"],
        trust_stage=4,
    )
    assert {i.id for i in results} == {keeper.id}


async def test_get_unsurfaced_excludes_deleted(session):
    """Push mode (#1032) consumes get_unsurfaced; should not see deleted insights."""
    repo = InsightRepository(session)
    keeper = _make_insight(min_trust_stage=3)
    deleted = _make_insight(min_trust_stage=3)
    await repo.add(keeper)
    await repo.add(deleted)
    await session.commit()
    await repo.soft_delete(deleted.id, "alpha")
    await session.commit()

    results = await repo.get_unsurfaced(user_id="alpha", trust_stage=4, min_confidence=0.5)
    assert {i.id for i in results} == {keeper.id}


# =============================================================================
# Roundtrip: from_domain / to_domain preserves new fields
# =============================================================================


async def test_roundtrip_preserves_is_deleted_and_correction(session):
    repo = InsightRepository(session)
    insight = _make_insight()
    insight.is_deleted = True
    insight.user_correction = "this was wrong"
    await repo.add(insight)
    await session.commit()

    # Fetch with exclude_deleted=False since it IS deleted
    results = await repo.list_for_user("alpha", exclude_deleted=False)
    assert len(results) == 1
    fetched = results[0]
    assert fetched.is_deleted is True
    assert fetched.user_correction == "this was wrong"
