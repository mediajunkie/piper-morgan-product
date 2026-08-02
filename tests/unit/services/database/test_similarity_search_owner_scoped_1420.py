"""#1420: similarity_search is owner-scoped, fail-closed, and its signature is real.

Regression, two defects in one site (sprint #1424 census S1/B7):
  1. Both production callers passed ``session_id=``/``threshold=`` kwargs the
     signature didn't accept — the TypeError was swallowed upstream, so
     "similar todos" and classifier intent-hinting silently returned [] for
     everyone (feature dead).
  2. The candidate-retrieval body called ``get_nodes_by_type`` with NO owner —
     the moment the signature was reconciled without also threading the owner,
     every user's node content (metadata carries user text) would have gone
     cross-tenant. This test pins that the leak can't come back.

Read-side only: the write path's owner_id population is tracked separately
(B8 / F14 — create_todo_knowledge_node missing user_id), so rows here are
inserted directly with owner_id set.

Requires PostgreSQL on 5433 (same as the suite's other DB-backed tests).
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.database.repositories import KnowledgeGraphRepository
from services.domain.models import KnowledgeNode
from services.knowledge.semantic_indexing_service import SemanticIndexingService
from services.shared_types import NodeType

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


def _query_node(owner: str | None, content: str = "buy milk at the store") -> KnowledgeNode:
    return KnowledgeNode(
        name="query",
        node_type=NodeType.CONCEPT,
        metadata={"semantic_content": content, "type": "intent_query"},
        session_id=owner,
    )


# ---------------------------------------------------------------------------
# Signature + fail-closed (no DB needed — repo mocked)
# ---------------------------------------------------------------------------


async def test_exact_caller_kwargs_are_accepted():
    """The two production call shapes must not TypeError (the dead-feature half)."""
    repo = AsyncMock(spec=KnowledgeGraphRepository)
    repo.get_nodes_by_type.return_value = []
    svc = SemanticIndexingService(knowledge_graph_repository=repo)

    # todo_knowledge_service.py:127 shape
    out1 = await svc.similarity_search(
        query_node=_query_node("user-a"),
        top_k=5,
        threshold=0.7,
        node_types=[NodeType.CONCEPT],
        session_id="user-a",
    )
    # shape from the deleted PM-034 llm_classifier (git history, #1432)
    out2 = await svc.similarity_search(
        query_node=_query_node("user-a"),
        top_k=5,
        threshold=0.7,
        node_types=[NodeType.CONCEPT, NodeType.PROCESS],
    )
    assert out1 == [] and out2 == []
    # Every candidate fetch carried the owner
    for call in repo.get_nodes_by_type.call_args_list:
        assert call.kwargs.get("session_id") == "user-a"


async def test_no_resolvable_owner_fails_closed():
    repo = AsyncMock(spec=KnowledgeGraphRepository)
    svc = SemanticIndexingService(knowledge_graph_repository=repo)
    out = await svc.similarity_search(query_node=_query_node(owner=None))
    assert out == []
    repo.get_nodes_by_type.assert_not_called()


# ---------------------------------------------------------------------------
# Two-tenant isolation (DB-backed)
# ---------------------------------------------------------------------------


@pytest.fixture
async def two_tenants_with_nodes():
    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    a_id, b_id = str(uuid4()), str(uuid4())
    now = datetime.now(timezone.utc)
    async with async_session() as s:
        for uid in (a_id, b_id):
            await s.execute(
                text(
                    "INSERT INTO users (id, username, email, is_active, is_verified, "
                    "created_at, updated_at, role, is_alpha) "
                    "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
                ),
                {"id": uid, "u": f"t1420_{uid[:8]}", "e": f"t1420_{uid[:8]}@test.example.com", "now": now},
            )
            await s.execute(
                text(
                    "INSERT INTO knowledge_nodes (id, name, node_type, node_metadata, "
                    "properties, owner_id, created_at, updated_at) "
                    "VALUES (:nid, :name, :ntype, CAST(:meta AS json), '{}', "
                    "CAST(:oid AS uuid), :now, :now)"
                ),
                {
                    "ntype": NodeType.CONCEPT.value,
                    "nid": f"node-{uid[:8]}",
                    "name": f"milk-note-{uid[:8]}",
                    "meta": '{"semantic_content": "buy milk at the store", "todo_id": "%s"}' % uid[:8],
                    "oid": uid,
                    "now": now,
                },
            )
        await s.commit()
    try:
        yield engine, a_id, b_id
    finally:
        async with async_session() as s:
            for uid in (a_id, b_id):
                await s.execute(
                    text("DELETE FROM knowledge_nodes WHERE owner_id = CAST(:uid AS uuid)"),
                    {"uid": uid},
                )
                await s.execute(text("DELETE FROM users WHERE id = :uid"), {"uid": uid})
            await s.commit()
        await engine.dispose()


async def test_user_a_never_sees_user_b_nodes(two_tenants_with_nodes):
    engine, a_id, b_id = two_tenants_with_nodes
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        svc = SemanticIndexingService(knowledge_graph_repository=KnowledgeGraphRepository(s))
        # threshold=0.0: scoping is under test, not ranking — every candidate
        # the query CAN see comes back.
        results = await svc.similarity_search(
            query_node=_query_node(a_id), threshold=0.0, session_id=a_id
        )
    names = {node.name for node, _score in results}
    assert f"milk-note-{a_id[:8]}" in names, "owner's own node must be searchable"
    assert f"milk-note-{b_id[:8]}" not in names, "#1420 CROSS-TENANT LEAK: B's node visible to A"
