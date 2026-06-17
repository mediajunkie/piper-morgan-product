"""#1238 (ADR-071 P2) — DocumentRepository: owner-anchoring for the ChromaDB doc store.

Verifies the read-authorization core (the (c,3)→(a,1+global-flag) close):
`get_readable_base_ids(principal)` returns base_ids where `is_global_pm_domain`
is true OR `owner_id == principal`; a None/non-UUID principal sees global-only
(m-40 graceful). Plus `upsert_document` idempotency by chromadb_base_id and
`get_by_base_id`. In-memory SQLite (#1035 pattern).
"""

from __future__ import annotations

import uuid

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import func, select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import DocumentDB  # noqa: E402
from services.repositories.document_repository import DocumentRepository  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: DocumentDB.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


async def _seed(session):
    """Global doc + alpha-private + beta-private."""
    repo = DocumentRepository(session)
    await repo.upsert_document("g1", owner_id=_ALPHA, is_global_pm_domain=True, title="global")
    await repo.upsert_document("p_alpha", owner_id=_ALPHA, is_global_pm_domain=False)
    await repo.upsert_document("p_beta", owner_id=_BETA, is_global_pm_domain=False)
    await session.commit()
    return repo


class TestUpsert1238:
    async def test_upsert_inserts_then_updates_no_duplicate(self, session):
        repo = DocumentRepository(session)
        await repo.upsert_document("pdf_x", owner_id=_ALPHA, is_global_pm_domain=False, title="v1")
        await session.commit()
        # Same base_id again → update in place, not a second row
        await repo.upsert_document("pdf_x", owner_id=_ALPHA, is_global_pm_domain=True, title="v2")
        await session.commit()
        count = (await session.execute(select(func.count()).select_from(DocumentDB))).scalar_one()
        assert count == 1
        row = await repo.get_by_base_id("pdf_x")
        assert row.title == "v2"
        assert row.is_global_pm_domain is True

    async def test_get_by_base_id_missing_returns_none(self, session):
        repo = DocumentRepository(session)
        assert await repo.get_by_base_id("nope") is None


class TestReadableBaseIds1238:
    async def test_owner_sees_global_plus_own_private(self, session):
        repo = await _seed(session)
        assert await repo.get_readable_base_ids(_ALPHA) == {"g1", "p_alpha"}
        assert await repo.get_readable_base_ids(_BETA) == {"g1", "p_beta"}

    async def test_none_principal_sees_global_only(self, session):
        repo = await _seed(session)
        assert await repo.get_readable_base_ids(None) == {"g1"}

    async def test_non_uuid_principal_sees_global_only(self, session):
        # m-40 graceful: a legacy non-UUID id can't match a UUID owner → global-only
        repo = await _seed(session)
        assert await repo.get_readable_base_ids("default_user") == {"g1"}

    async def test_uuid_object_principal_accepted(self, session):
        repo = await _seed(session)
        assert await repo.get_readable_base_ids(uuid.UUID(_ALPHA)) == {"g1", "p_alpha"}
