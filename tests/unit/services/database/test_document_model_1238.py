"""#1238 (ADR-071 P2) — DocumentDB model: relational anchor for the ChromaDB doc store.

The doc store (`pm_knowledge` ChromaDB collection) is ChromaDB-only — no relational
row backs each document. This table is the canonical owner-anchored row ADR-071 D2
mandates (Arch ruling 2026-06-16: marker on the DB row, NOT ChromaDB metadata).

Verifies the schema contract: `chromadb_base_id` link, `owner_id` provenance
(CrossDialectUUID round-trip), `is_global_pm_domain` D1-exemption marker (defaults
false), title/source, TimestampMixin. In-memory SQLite (#1035 pattern).
"""

from __future__ import annotations

import uuid

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import DocumentDB  # noqa: E402

pytestmark = pytest.mark.asyncio

_OWNER = "a25db09c-6d79-41e4-8d82-87b6a005bbb0"  # configured PM (xian)


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: DocumentDB.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


class TestDocumentModel1238:
    async def test_insert_and_read_back(self, session):
        doc = DocumentDB(
            chromadb_base_id="pdf_88388894",
            owner_id=uuid.UUID(_OWNER),
            is_global_pm_domain=True,
            title="chapter.pdf",
            source="/tests/fixtures/chapter.pdf",
        )
        session.add(doc)
        await session.commit()
        row = (await session.execute(select(DocumentDB))).scalar_one()
        assert row.chromadb_base_id == "pdf_88388894"
        assert str(row.owner_id) == _OWNER  # CrossDialectUUID round-trips on SQLite
        assert row.is_global_pm_domain is True
        assert row.title == "chapter.pdf"
        assert row.source == "/tests/fixtures/chapter.pdf"
        assert row.created_at is not None  # TimestampMixin
        assert row.id is not None  # UUID PK default

    async def test_is_global_pm_domain_defaults_false_owner_nullable(self, session):
        # Omitting both fields: marker defaults False (not global), owner None (m-40 graceful)
        doc = DocumentDB(chromadb_base_id="pdf_local")
        session.add(doc)
        await session.commit()
        row = (await session.execute(select(DocumentDB))).scalar_one()
        assert row.is_global_pm_domain is False
        assert row.owner_id is None

    async def test_chromadb_base_id_unique(self, session):
        session.add(DocumentDB(chromadb_base_id="dup"))
        await session.commit()
        session.add(DocumentDB(chromadb_base_id="dup"))
        with pytest.raises(Exception):  # IntegrityError — unique constraint
            await session.commit()
        await session.rollback()
