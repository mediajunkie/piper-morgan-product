"""#1238 (ADR-071 P2) — DocumentService anchors ingested docs (wiring test).

Real DocumentService + real DocumentRepository + a real (SQLite) session; only the
external ChromaDB ingester is faked. Verifies owner_id + is_global_pm_domain
propagate from ingest_path → the documents anchor row (no mocked internals — the
#490 wiring-test discipline). Also covers non-PDF rejection + re-ingest idempotency.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

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
from services.knowledge_graph.document_service import DocumentService  # noqa: E402
from services.repositories.document_repository import DocumentRepository  # noqa: E402

pytestmark = pytest.mark.asyncio

_PM = "a25db09c-6d79-41e4-8d82-87b6a005bbb0"


class _FakeIngester:
    """Stub for the ChromaDB DocumentIngester (external store)."""

    def __init__(self):
        self.calls = []

    async def ingest_pdf(self, file_path, metadata=None):
        self.calls.append(file_path)
        return {"status": "success", "document_id": "pdf_wiretest", "chunks_created": 3}


@pytest_asyncio.fixture
async def sqlite_service():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: DocumentDB.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def scope():
        async with SessionLocal() as s:
            yield s
            await s.commit()

    svc = DocumentService(session_scope=scope, ingester=_FakeIngester())
    yield svc, SessionLocal
    await engine.dispose()


class TestIngestAnchors1238:
    async def test_ingest_path_writes_anchor_row(self, sqlite_service):
        svc, SessionLocal = sqlite_service
        result = await svc.ingest_path(
            "/tmp/chapter.pdf", {"title": "Chapter"}, owner_id=_PM, is_global_pm_domain=True
        )
        assert result["status"] == "success"
        async with SessionLocal() as s:
            row = await DocumentRepository(s).get_by_base_id("pdf_wiretest")
        assert row is not None
        assert str(row.owner_id) == _PM
        assert row.is_global_pm_domain is True
        assert row.title == "Chapter"
        assert row.source == "/tmp/chapter.pdf"

    async def test_ingest_path_rejects_non_pdf(self, sqlite_service):
        svc, _ = sqlite_service
        with pytest.raises(ValueError):
            await svc.ingest_path("/tmp/notpdf.txt", {"title": "x"})

    async def test_reingest_is_idempotent(self, sqlite_service):
        svc, SessionLocal = sqlite_service
        await svc.ingest_path("/tmp/c.pdf", {"title": "v1"}, owner_id=_PM, is_global_pm_domain=True)
        await svc.ingest_path("/tmp/c.pdf", {"title": "v2"}, owner_id=_PM, is_global_pm_domain=True)
        async with SessionLocal() as s:
            count = (await s.execute(select(func.count()).select_from(DocumentDB))).scalar_one()
            row = await DocumentRepository(s).get_by_base_id("pdf_wiretest")
        assert count == 1  # same base_id → upsert in place, not a duplicate
        assert row.title == "v2"


class TestListForUser1238:
    """#1238 Radar: list_for_user returns the user's own docs (detached dicts)."""

    async def test_list_returns_owner_docs_and_isolates_others(self, sqlite_service):
        svc, _ = sqlite_service
        await svc.ingest_path("/tmp/a.pdf", {"title": "A"}, owner_id=_PM, is_global_pm_domain=True)
        docs = await svc.list_for_user(_PM)
        assert len(docs) == 1
        assert docs[0]["title"] == "A"
        assert docs[0]["chromadb_base_id"] == "pdf_wiretest"
        assert docs[0]["source"] == "/tmp/a.pdf"
        # a different user sees none of the PM's docs in their personal list
        assert await svc.list_for_user("99999999-9999-9999-9999-999999999999") == []
