"""#1436 B2/B14: the knowledge-graph routes call the service API that exists.

Regression, three layers deep (mypy census; every KG route call previously
exploded and surfaced as a 500):
  - DI yielded ``KnowledgeGraphService(session)`` — the constructor requires a
    ``KnowledgeGraphRepository`` (B2)
  - routes built domain objects with an ``owner_id`` field the dataclass
    doesn't have and passed them positionally into a kwargs API (B14)
  - routes called ``get_node_by_id``/``query_nodes`` — methods that don't
    exist on the service (``get_node``/``search_nodes`` do)
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from services.shared_types import EdgeType, NodeType
from web.api.routes.knowledge_graph import create_edge, create_node, get_node, query_graph

CLAIMS = SimpleNamespace(sub="user-abc")


def _node(nid="n1", name="concept-1"):
    return SimpleNamespace(
        id=nid,
        name=name,
        node_type=NodeType.CONCEPT,
        description="",
        created_at=None,
        metadata={},
        properties={},
    )


async def test_create_node_calls_the_real_kwargs_api_with_enum():
    svc = SimpleNamespace(create_node=AsyncMock(return_value=_node()))
    out = await create_node(
        name="concept-1",
        node_type="concept",  # lowercase in, enum out
        current_user=CLAIMS,
        kg_service=svc,
    )
    kwargs = svc.create_node.await_args.kwargs
    assert kwargs["node_type"] is NodeType.CONCEPT
    assert kwargs["session_id"] == "user-abc"
    assert out["node_type"] == "CONCEPT"


async def test_create_node_invalid_type_is_400_not_500():
    svc = SimpleNamespace(create_node=AsyncMock())
    with pytest.raises(HTTPException) as exc:
        await create_node(
            name="x", node_type="not_a_type", current_user=CLAIMS, kg_service=svc
        )
    assert exc.value.status_code == 400
    svc.create_node.assert_not_awaited()


async def test_get_node_uses_get_node_and_404s_honestly():
    svc = SimpleNamespace(get_node=AsyncMock(return_value=None))
    with pytest.raises(HTTPException) as exc:
        await get_node(node_id="missing", current_user=CLAIMS, kg_service=svc)
    assert exc.value.status_code == 404
    svc.get_node.assert_awaited_once_with("missing", owner_id="user-abc")


async def test_create_edge_checks_ownership_then_calls_real_api():
    edge = SimpleNamespace(
        id="e1",
        source_node_id="n1",
        target_node_id="n2",
        edge_type=EdgeType.REFERENCES,
        created_at=None,
    )
    svc = SimpleNamespace(
        get_node=AsyncMock(side_effect=[_node("n1"), _node("n2")]),
        create_edge=AsyncMock(return_value=edge),
    )
    out = await create_edge(
        source_node_id="n1",
        target_node_id="n2",
        edge_type="references",
        current_user=CLAIMS,
        kg_service=svc,
    )
    kwargs = svc.create_edge.await_args.kwargs
    assert kwargs["edge_type"] is EdgeType.REFERENCES
    assert kwargs["owner_id"] == "user-abc"
    assert out["edge_type"] == "REFERENCES"


async def test_query_uses_search_nodes_owner_scoped():
    svc = SimpleNamespace(search_nodes=AsyncMock(return_value=[_node()]))
    out = await query_graph(
        node_type="concept", search_term="milk", current_user=CLAIMS, kg_service=svc
    )
    kwargs = svc.search_nodes.await_args.kwargs
    assert kwargs["owner_id"] == "user-abc"
    assert kwargs["node_type"] is NodeType.CONCEPT
    assert out["nodes"][0]["node_type"] == "CONCEPT"


async def test_di_yields_service_with_a_real_repository():
    from services.database.repositories import KnowledgeGraphRepository
    from web.api.dependencies import get_knowledge_graph_service

    agen = get_knowledge_graph_service()
    svc = await agen.__anext__()
    try:
        assert isinstance(svc.repo, KnowledgeGraphRepository)
    finally:
        await agen.aclose()
