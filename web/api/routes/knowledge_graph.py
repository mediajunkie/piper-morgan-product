"""
Knowledge Graph API Routes (Issue #357: SEC-RBAC Phase 1.3)

Provides knowledge graph CRUD endpoints with ownership validation:
- Create knowledge nodes
- Create relationships/edges
- Query knowledge graph
- User-isolated knowledge access
"""

from typing import Optional

import structlog
from fastapi import APIRouter, Depends, HTTPException, status

from services.auth.auth_middleware import get_current_user
from services.auth.jwt_service import JWTClaims
from services.shared_types import EdgeType, NodeType
from web.api.dependencies import get_knowledge_graph_service

router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge-graph"])
logger = structlog.get_logger(__name__)


@router.post("/nodes")
async def create_node(
    name: str,
    node_type: str,
    description: Optional[str] = None,
    properties: Optional[dict] = None,
    current_user: JWTClaims = Depends(get_current_user),
    kg_service=Depends(get_knowledge_graph_service),
) -> dict:
    """
    Create a knowledge graph node with ownership validation (SEC-RBAC).

    Args:
        name: Node name
        node_type: Type of node (CONCEPT, DOCUMENT, PERSON, etc.)
        description: Optional node description
        properties: Optional additional properties
        current_user: Current authenticated user
        kg_service: Knowledge graph service (injected)

    Returns:
        Created node with ID and metadata

    Raises:
        HTTPException 400: Invalid input
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        if not name or not name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Node name is required",
            )

        if not node_type or not node_type.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Node type is required",
            )

        # #1436 B14: coerce to the enum the service requires; the old code
        # built a domain object with an owner_id field the dataclass doesn't
        # have and passed it positionally into a kwargs API — TypeError -> 500.
        try:
            node_type_enum = NodeType(node_type.strip().upper())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid node_type: {node_type}. "
                f"Must be one of: {', '.join(t.value for t in NodeType)}",
            )

        created_node = await kg_service.create_node(
            name=name,
            node_type=node_type_enum,
            description=description or "",
            properties=properties or {},
            # Owner rides session_id (the service/repo convention; the
            # owner_id-column population gap is the tracked #1420 residual).
            session_id=current_user.sub,
        )

        logger.info(
            "knowledge_node_created",
            user_id=current_user.sub,
            node_id=created_node.id,
            node_type=node_type,
        )

        return {
            "id": created_node.id,
            "name": created_node.name,
            "node_type": created_node.node_type.value
            if isinstance(created_node.node_type, NodeType)
            else created_node.node_type,
            "description": created_node.description,
            "owner_id": current_user.sub,
            "created_at": created_node.created_at.isoformat() if created_node.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "knowledge_node_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create knowledge node",
        )


@router.get("/nodes/{node_id}")
async def get_node(
    node_id: str,
    current_user: JWTClaims = Depends(get_current_user),
    kg_service=Depends(get_knowledge_graph_service),
) -> dict:
    """
    Get knowledge node by ID with ownership validation (SEC-RBAC).

    Only returns node if current user is the owner.

    Args:
        node_id: Node ID to retrieve
        current_user: Current authenticated user
        kg_service: Knowledge graph service (injected)

    Returns:
        Node details (if owned by current user)

    Raises:
        HTTPException 404: Node not found or not owned by current user
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # #1436 B14: get_node_by_id doesn't exist on the service — get_node does.
        node = await kg_service.get_node(node_id, owner_id=current_user.sub)

        if not node:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Knowledge node not found: {node_id}",
            )

        logger.info(
            "knowledge_node_retrieved",
            user_id=current_user.sub,
            node_id=node_id,
        )

        return {
            "id": node.id,
            "name": node.name,
            "node_type": node.node_type,
            "description": node.description,
            "properties": node.properties,
            "owner_id": current_user.sub,
            "created_at": node.created_at.isoformat() if node.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "knowledge_node_get_error",
            user_id=current_user.sub,
            node_id=node_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve knowledge node",
        )


@router.post("/edges")
async def create_edge(
    source_node_id: str,
    target_node_id: str,
    edge_type: str,
    properties: Optional[dict] = None,
    current_user: JWTClaims = Depends(get_current_user),
    kg_service=Depends(get_knowledge_graph_service),
) -> dict:
    """
    Create knowledge graph edge with ownership validation (SEC-RBAC).

    Both source and target nodes must be owned by current user.

    Args:
        source_node_id: Source node ID
        target_node_id: Target node ID
        edge_type: Type of edge relationship
        properties: Optional edge properties
        current_user: Current authenticated user
        kg_service: Knowledge graph service (injected)

    Returns:
        Created edge with ID

    Raises:
        HTTPException 400: Invalid input or nodes not owned by user
        HTTPException 404: Nodes not found
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        if not edge_type or not edge_type.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Edge type is required",
            )

        # Verify both nodes are owned by current user
        source = await kg_service.get_node(source_node_id, owner_id=current_user.sub)
        target = await kg_service.get_node(target_node_id, owner_id=current_user.sub)

        if not source or not target:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="One or both nodes not found or not owned by user",
            )

        # #1436 B14: enum-coerce + the service's kwargs API (see create_node).
        try:
            edge_type_enum = EdgeType(edge_type.strip().upper())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid edge_type: {edge_type}. "
                f"Must be one of: {', '.join(t.value for t in EdgeType)}",
            )

        created_edge = await kg_service.create_edge(
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            edge_type=edge_type_enum,
            properties=properties or {},
            session_id=current_user.sub,
            owner_id=current_user.sub,
        )

        logger.info(
            "knowledge_edge_created",
            user_id=current_user.sub,
            edge_id=created_edge.id,
            edge_type=edge_type,
        )

        return {
            "id": created_edge.id,
            "source_node_id": created_edge.source_node_id,
            "target_node_id": created_edge.target_node_id,
            "edge_type": created_edge.edge_type.value
            if isinstance(created_edge.edge_type, EdgeType)
            else created_edge.edge_type,
            "owner_id": current_user.sub,
            "created_at": created_edge.created_at.isoformat() if created_edge.created_at else None,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "knowledge_edge_create_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create knowledge edge",
        )


@router.get("/query")
async def query_graph(
    node_type: Optional[str] = None,
    search_term: Optional[str] = None,
    limit: int = 100,
    current_user: JWTClaims = Depends(get_current_user),
    kg_service=Depends(get_knowledge_graph_service),
) -> dict:
    """
    Query knowledge graph with ownership validation (SEC-RBAC).

    Returns only nodes owned by current user.

    Args:
        node_type: Filter by node type (optional)
        search_term: Search term to match node names/descriptions (optional)
        limit: Maximum results to return
        current_user: Current authenticated user
        kg_service: Knowledge graph service (injected)

    Returns:
        List of matching nodes (owned by current user)

    Raises:
        HTTPException 500: Server error

    Issue #357: SEC-RBAC Phase 1.3 Endpoint Protection
    """
    try:
        # #1436 B14: query_nodes doesn't exist — search_nodes is the real API.
        node_type_enum = None
        if node_type:
            try:
                node_type_enum = NodeType(node_type.strip().upper())
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid node_type: {node_type}. "
                    f"Must be one of: {', '.join(t.value for t in NodeType)}",
                )
        nodes = await kg_service.search_nodes(
            node_type=node_type_enum,
            search_term=search_term,
            owner_id=current_user.sub,
            limit=limit,
        )

        logger.info(
            "knowledge_graph_queried",
            user_id=current_user.sub,
            count=len(nodes),
            node_type=node_type,
        )

        return {
            "nodes": [
                {
                    "id": n.id,
                    "name": n.name,
                    "node_type": n.node_type.value
                    if isinstance(n.node_type, NodeType)
                    else n.node_type,
                    "description": n.description,
                    "created_at": n.created_at.isoformat() if n.created_at else None,
                }
                for n in nodes
            ],
            "count": len(nodes),
        }

    except Exception as e:
        logger.error(
            "knowledge_graph_query_error",
            user_id=current_user.sub,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to query knowledge graph",
        )
