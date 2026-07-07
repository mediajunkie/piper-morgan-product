"""ADR-075 Component B (#1366) — PersonalizationContextRepository.

The DB-backed, owner_id-scoped personalization store (ADR-075 D2). Mirrors the
#1226 ConnectorConfigRepository test setup (in-memory SQLite, single-table
create — the full metadata has PG-only types). Verifies repo get/upsert
idempotency, per-owner isolation, the strict-write/graceful-read asymmetry,
and the lazy-seed-on-first-access path (OQ-3).
"""

from __future__ import annotations

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import func, select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.configuration.personalization_repository import (  # noqa: E402
    PersonalizationContextRepository,
)
from services.database.models import PersonalizationContext  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"

_DEFAULT_CONTEXT = {"User Context": "neutral default persona"}


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: PersonalizationContext.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


async def _count(session) -> int:
    return (
        await session.execute(select(func.count()).select_from(PersonalizationContext))
    ).scalar_one()


class TestRepoUpsert:
    async def test_upsert_inserts_then_replaces_no_duplicate(self, session):
        repo = PersonalizationContextRepository(session)
        await repo.upsert(_ALPHA, {"User Context": "v1"})
        await session.commit()
        # same owner → replace in place, not a second row
        await repo.upsert(_ALPHA, {"User Context": "v2"})
        await session.commit()
        assert await _count(session) == 1
        row = await repo.get(_ALPHA)
        assert row.context["User Context"] == "v2"

    async def test_get_missing_returns_none(self, session):
        repo = PersonalizationContextRepository(session)
        assert await repo.get(_ALPHA) is None

    async def test_per_owner_isolation(self, session):
        repo = PersonalizationContextRepository(session)
        await repo.upsert(_ALPHA, {"User Context": "alpha's context"})
        await repo.upsert(_BETA, {"User Context": "beta's context"})
        await session.commit()

        alpha_row = await repo.get(_ALPHA)
        beta_row = await repo.get(_BETA)
        assert alpha_row.context["User Context"] == "alpha's context"
        assert beta_row.context["User Context"] == "beta's context"

    async def test_explicit_upsert_is_not_marked_seeded_default(self, session):
        repo = PersonalizationContextRepository(session)
        row = await repo.upsert(_ALPHA, {"User Context": "real customization"})
        assert row.is_seeded_default is False

    async def test_write_requires_valid_owner(self, session):
        repo = PersonalizationContextRepository(session)
        with pytest.raises(ValueError):
            await repo.upsert(None, {"User Context": "x"})
        with pytest.raises(ValueError):
            await repo.upsert("not-a-uuid", {"User Context": "x"})

    async def test_read_degrades_gracefully_on_malformed_owner(self, session):
        """Reads don't raise on a malformed owner — m-40 graceful (matches
        ADR-071's read/write asymmetry: writes are strict, reads degrade)."""
        repo = PersonalizationContextRepository(session)
        assert await repo.get(None) is None
        assert await repo.get("not-a-uuid") is None


class TestGetOrSeedDefault:
    async def test_seeds_when_no_row_exists(self, session):
        repo = PersonalizationContextRepository(session)
        row = await repo.get_or_seed_default(_ALPHA, _DEFAULT_CONTEXT)
        assert row is not None
        assert row.is_seeded_default is True
        assert row.context == _DEFAULT_CONTEXT
        assert await _count(session) == 1

    async def test_returns_existing_row_without_reseeding(self, session):
        repo = PersonalizationContextRepository(session)
        await repo.upsert(_ALPHA, {"User Context": "already customized"})
        await session.commit()

        row = await repo.get_or_seed_default(_ALPHA, _DEFAULT_CONTEXT)

        assert row.context == {"User Context": "already customized"}
        assert row.is_seeded_default is False
        assert await _count(session) == 1  # no second row created

    async def test_malformed_owner_seeds_nothing(self, session):
        repo = PersonalizationContextRepository(session)
        row = await repo.get_or_seed_default("not-a-uuid", _DEFAULT_CONTEXT)
        assert row is None
        assert await _count(session) == 0


class TestMarkNoticeSeen:
    async def test_marks_existing_row(self, session):
        repo = PersonalizationContextRepository(session)
        await repo.get_or_seed_default(_ALPHA, _DEFAULT_CONTEXT)
        await session.commit()

        await repo.mark_notice_seen(_ALPHA)
        await session.commit()

        row = await repo.get(_ALPHA)
        assert row.has_seen_personalization_notice is True

    async def test_noop_on_missing_row(self, session):
        """No row for this owner — must not raise, must not create one."""
        repo = PersonalizationContextRepository(session)
        await repo.mark_notice_seen(_ALPHA)  # should not raise
        assert await _count(session) == 0

    async def test_noop_on_malformed_owner(self, session):
        repo = PersonalizationContextRepository(session)
        await repo.mark_notice_seen("not-a-uuid")  # should not raise
        assert await _count(session) == 0
