"""#1238 (ADR-071 P2) — the (c,3) close: DocumentService reads are owner-scoped.

Cross-owner test. With docs A (owner α, private), B (global), C (owner β, private)
ALL matching the ChromaDB query, find_decisions / get_relevant_context /
suggest_documents return only docs the principal may read (own + global) — never
another owner's private doc; None principal → global-only. Real DocumentService +
real DocumentRepository + SQLite; only the ChromaDB collection is faked.

This is the (c,3)→(a,1+global-flag) close: the reads were unscoped (any principal saw
every doc); now the relational marker gates them.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import DocumentDB  # noqa: E402
from services.knowledge_graph.document_service import DocumentService  # noqa: E402
from services.repositories.document_repository import DocumentRepository  # noqa: E402

pytestmark = pytest.mark.asyncio

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"

# A ChromaDB query result whose chunks span all three documents (the leak surface:
# absent scoping, every principal would see all three).
_RESULTS = {
    "ids": [["pdfA_chunk_0", "pdfB_chunk_0", "pdfC_chunk_0"]],
    "documents": [
        [
            "Decision: alpha private decided X",
            "Decision: global agreed Y",
            "Decision: beta private resolved Z",
        ]
    ],
    "metadatas": [[{"title": "A"}, {"title": "B"}, {"title": "C"}]],
    "distances": [[0.1, 0.2, 0.3]],
}


class _FakeCollection:
    def query(self, **kwargs):
        return _RESULTS


class _FakeIngester:
    collection = _FakeCollection()


@pytest_asyncio.fixture
async def svc():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: DocumentDB.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def scope():
        async with SessionLocal() as s:
            yield s
            await s.commit()

    async with scope() as s:
        repo = DocumentRepository(s)
        await repo.upsert_document("pdfA", owner_id=_ALPHA, is_global_pm_domain=False, title="A")
        await repo.upsert_document("pdfB", owner_id=_ALPHA, is_global_pm_domain=True, title="B")
        await repo.upsert_document("pdfC", owner_id=_BETA, is_global_pm_domain=False, title="C")

    service = DocumentService(session_scope=scope, ingester=_FakeIngester())
    yield service
    await engine.dispose()


def _decision_titles(res):
    return {d["document_title"] for d in res["decisions"]}


class TestReadsAreOwnerScoped1238:
    async def test_find_decisions_alpha_sees_own_plus_global_not_beta(self, svc):
        res = await svc.find_decisions(topic="x", owner_id=_ALPHA)
        assert _decision_titles(res) == {"A", "B"}  # NOT C (β's private)

    async def test_find_decisions_beta_sees_own_plus_global_not_alpha(self, svc):
        res = await svc.find_decisions(topic="x", owner_id=_BETA)
        assert _decision_titles(res) == {"B", "C"}  # NOT A (α's private)

    async def test_find_decisions_none_principal_sees_global_only(self, svc):
        res = await svc.find_decisions(topic="x", owner_id=None)
        assert _decision_titles(res) == {"B"}  # global-only (m-40 graceful)

    async def test_get_relevant_context_is_scoped(self, svc):
        res = await svc.get_relevant_context("yesterday", owner_id=_ALPHA)
        assert {d["title"] for d in res["context_documents"]} == {"A", "B"}

    async def test_suggest_documents_is_scoped(self, svc):
        res = await svc.suggest_documents("focus", owner_id=_ALPHA)
        assert {s["title"] for s in res["suggestions"]} == {"A", "B"}

    async def test_suggest_documents_general_branch_is_scoped(self, svc):
        # empty focus_area → the "general suggestions" branch is also scoped
        res = await svc.suggest_documents("", owner_id=_BETA)
        assert {s["title"] for s in res["suggestions"]} == {"B", "C"}
