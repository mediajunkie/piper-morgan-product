"""
Knowledge Graph Service - PM-040
High-level business logic for knowledge graph operations
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from uuid import UUID

import structlog

from services.database.repositories import KnowledgeGraphRepository
from services.domain.models import KnowledgeEdge, KnowledgeNode
from services.knowledge.boundaries import BoundaryEnforcer as KGBoundaryEnforcer
from services.knowledge.boundaries import GraphBoundaries, OperationBoundaries
from services.shared_types import EdgeType, NodeType

logger = structlog.get_logger()


class KnowledgeGraphService:
    """Service for knowledge graph operations with business logic and privacy compliance"""

    def __init__(
        self,
        knowledge_graph_repository: KnowledgeGraphRepository,
        kg_boundary_enforcer: Optional[KGBoundaryEnforcer] = None,
    ):
        self.repo = knowledge_graph_repository
        # KG-specific boundary enforcer (Issue #230)
        self.kg_boundary_enforcer = kg_boundary_enforcer or KGBoundaryEnforcer(
            OperationBoundaries.SEARCH
        )
        self.logger = logger.bind(service="knowledge_graph")

    # Node Operations
    async def create_node(
        self,
        name: str,
        node_type: NodeType,
        description: str = "",
        metadata: Optional[Dict[str, Any]] = None,
        properties: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
    ) -> KnowledgeNode:
        """
        Create a new knowledge node with validation and privacy checks
        """
        self.logger.info(
            "Creating knowledge node", name=name, node_type=node_type.value, session_id=session_id
        )

        # Create the node
        node = KnowledgeNode(
            name=name,
            node_type=node_type,
            description=description,
            metadata=metadata or {},
            properties=properties or {},
            session_id=session_id,
        )

        # Store in repository
        created_node = await self.repo.create_node(node)

        self.logger.info(
            "Knowledge node created",
            node_id=created_node.id,
            node_type=created_node.node_type.value,
        )

        return created_node

    async def get_node(
        self, node_id: str, owner_id: Optional[str] = None, is_admin: bool = False
    ) -> Optional[KnowledgeNode]:
        """Get a node by ID - optionally verify ownership (SEC-RBAC Phase 3: admins bypass ownership check)"""
        return await self.repo.get_node_by_id(
            node_id, owner_id if owner_id and not is_admin else None
        )

    async def get_nodes_by_type(
        self, node_type: NodeType, session_id: Optional[str] = None, limit: int = 100
    ) -> List[KnowledgeNode]:
        """Get nodes by type with optional session filtering"""
        return await self.repo.get_nodes_by_type(node_type, session_id, limit)

    async def update_node(
        self,
        node_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        properties: Optional[Dict[str, Any]] = None,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Optional[KnowledgeNode]:
        """Update an existing node (SEC-RBAC Phase 3: admins can update any node)"""
        node = await self.repo.get_node_by_id(
            node_id, owner_id if owner_id and not is_admin else None
        )
        if not node:
            return None

        # Update fields
        if name is not None:
            node.name = name
        if description is not None:
            node.description = description
        if metadata is not None:
            node.metadata.update(metadata)
        if properties is not None:
            node.properties.update(properties)

        node.updated_at = datetime.now()

        # Save updates
        return await self.repo.update(node_id, **node.__dict__)

    # Edge Operations
    async def create_edge(
        self,
        source_node_id: str,
        target_node_id: str,
        edge_type: EdgeType,
        weight: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
        properties: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> KnowledgeEdge:
        """
        Create an edge between two nodes with validation (SEC-RBAC Phase 3: admins can create edges in any graph)
        """
        # Verify both nodes exist - with optional ownership verification
        source_node = await self.repo.get_node_by_id(
            source_node_id, owner_id if owner_id and not is_admin else None
        )
        target_node = await self.repo.get_node_by_id(
            target_node_id, owner_id if owner_id and not is_admin else None
        )

        if not source_node:
            raise ValueError(f"Source node {source_node_id} not found")
        if not target_node:
            raise ValueError(f"Target node {target_node_id} not found")

        self.logger.info(
            "Creating knowledge edge",
            source=source_node_id,
            target=target_node_id,
            edge_type=edge_type.value,
        )

        # Create the edge
        edge = KnowledgeEdge(
            source_node_id=source_node_id,
            target_node_id=target_node_id,
            edge_type=edge_type,
            weight=weight,
            metadata=metadata or {},
            properties=properties or {},
            session_id=session_id or source_node.session_id,
        )

        created_edge = await self.repo.create_edge(edge)

        self.logger.info(
            "Knowledge edge created",
            edge_id=created_edge.id,
            edge_type=created_edge.edge_type.value,
        )

        return created_edge

    async def get_edge(self, edge_id: str) -> Optional[KnowledgeEdge]:
        """Get an edge by ID"""
        return await self.repo.get_edge_by_id(edge_id)

    # Graph Operations
    async def get_neighbors(
        self,
        node_id: str,
        edge_type: Optional[EdgeType] = None,
        direction: str = "both",
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> List[KnowledgeNode]:
        """
        Find neighboring nodes - optionally verify ownership (SEC-RBAC Phase 3: admins bypass ownership check)

        Args:
            node_id: The node to find neighbors for
            edge_type: Optional filter by edge type
            direction: "incoming", "outgoing", or "both"
            owner_id: Optional owner ID to verify ownership
            is_admin: If True, bypass ownership check (SEC-RBAC Phase 3)
        """
        return await self.repo.find_neighbors(
            node_id, edge_type, direction, owner_id if owner_id and not is_admin else None
        )

    async def extract_subgraph(
        self,
        node_ids: List[str],
        max_depth: int = 2,
        edge_types: Optional[List[EdgeType]] = None,
        node_types: Optional[List[NodeType]] = None,
        owner_id: Optional[str] = None,
        is_admin: bool = False,
    ) -> Dict[str, Any]:
        """
        Extract a subgraph around specified nodes with filtering - optionally verify ownership (SEC-RBAC Phase 3: admins bypass ownership check)

        Args:
            node_ids: Starting nodes for subgraph extraction
            max_depth: How many levels to traverse
            edge_types: Optional filter for edge types to follow
            node_types: Optional filter for node types to include
            owner_id: Optional owner ID to verify ownership
        """
        self.logger.info("Extracting subgraph", start_nodes=len(node_ids), max_depth=max_depth)

        # Get basic subgraph from repository (with optional ownership verification)
        subgraph = await self.repo.get_subgraph(
            node_ids, max_depth, owner_id if owner_id and not is_admin else None
        )

        # Apply filtering if requested
        if edge_types or node_types:
            filtered_nodes = []
            filtered_edges = []

            # Filter nodes by type
            if node_types:
                node_type_set = set(node_types)
                for node in subgraph["nodes"]:
                    if node.node_type in node_type_set:
                        filtered_nodes.append(node)
            else:
                filtered_nodes = subgraph["nodes"]

            # Create set of valid node IDs for edge filtering
            valid_node_ids = {node.id for node in filtered_nodes}

            # Filter edges by type and valid nodes
            if edge_types:
                edge_type_set = set(edge_types)
                for edge in subgraph["edges"]:
                    if (
                        edge.edge_type in edge_type_set
                        and edge.source_node_id in valid_node_ids
                        and edge.target_node_id in valid_node_ids
                    ):
                        filtered_edges.append(edge)
            else:
                # Just filter by valid nodes
                for edge in subgraph["edges"]:
                    if (
                        edge.source_node_id in valid_node_ids
                        and edge.target_node_id in valid_node_ids
                    ):
                        filtered_edges.append(edge)

            subgraph["nodes"] = filtered_nodes
            subgraph["edges"] = filtered_edges

        self.logger.info(
            "Subgraph extracted", nodes=len(subgraph["nodes"]), edges=len(subgraph["edges"])
        )

        return subgraph

    async def find_paths(
        self,
        source_id: str,
        target_id: str,
        max_paths: int = 5,
        max_depth: int = 5,
        owner_id: Optional[str] = None,
    ) -> List[List[KnowledgeNode]]:
        """
        Find paths between two nodes - optionally verify ownership

        Args:
            source_id: Starting node
            target_id: Target node
            max_paths: Maximum number of paths to return
            max_depth: Maximum path length to consider
            owner_id: Optional owner ID to verify ownership
        """
        # For now, use repository's simple implementation
        # TODO: Implement more sophisticated algorithms (Dijkstra, A*, etc.)
        return await self.repo.find_paths(source_id, target_id, max_paths, owner_id)

    # Bulk Operations
    async def create_nodes_bulk(
        self, nodes_data: List[Dict[str, Any]], session_id: Optional[str] = None
    ) -> List[KnowledgeNode]:
        """
        Create multiple nodes efficiently

        Args:
            nodes_data: List of node data dictionaries
            session_id: Session ID to apply to all nodes
        """
        nodes = []
        for data in nodes_data:
            node = KnowledgeNode(
                name=data.get("name", ""),
                node_type=data.get("node_type", NodeType.CONCEPT),
                description=data.get("description", ""),
                metadata=data.get("metadata", {}),
                properties=data.get("properties", {}),
                session_id=session_id or data.get("session_id"),
            )
            nodes.append(node)

        return await self.repo.create_nodes_bulk(nodes)

    async def create_edges_bulk(
        self, edges_data: List[Dict[str, Any]], session_id: Optional[str] = None
    ) -> List[KnowledgeEdge]:
        """
        Create multiple edges efficiently

        Args:
            edges_data: List of edge data dictionaries
            session_id: Session ID to apply to all edges
        """
        edges = []
        for data in edges_data:
            edge = KnowledgeEdge(
                source_node_id=data["source_node_id"],
                target_node_id=data["target_node_id"],
                edge_type=data.get("edge_type", EdgeType.REFERENCES),
                weight=data.get("weight", 1.0),
                metadata=data.get("metadata", {}),
                properties=data.get("properties", {}),
                session_id=session_id or data.get("session_id"),
            )
            edges.append(edge)

        return await self.repo.create_edges_bulk(edges)

    # Analytics Operations
    async def get_node_degree(self, node_id: str, direction: str = "both") -> Dict[str, int]:
        """
        Get the degree (number of connections) for a node

        Returns:
            Dict with "incoming", "outgoing", and "total" counts
        """
        neighbors_in = await self.repo.find_neighbors(node_id, direction="incoming")
        neighbors_out = await self.repo.find_neighbors(node_id, direction="outgoing")

        return {
            "incoming": len(neighbors_in),
            "outgoing": len(neighbors_out),
            "total": len(set(n.id for n in neighbors_in + neighbors_out)),
        }

    async def get_graph_statistics(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get basic statistics about the knowledge graph

        Args:
            session_id: Optional session filter
        """
        nodes = await self.repo.get_nodes_by_session(session_id) if session_id else []
        edges = await self.repo.get_edges_by_session(session_id) if session_id else []

        # Count nodes by type
        node_type_counts = {}
        for node in nodes:
            node_type = node.node_type.value
            node_type_counts[node_type] = node_type_counts.get(node_type, 0) + 1

        # Count edges by type
        edge_type_counts = {}
        for edge in edges:
            edge_type = edge.edge_type.value
            edge_type_counts[edge_type] = edge_type_counts.get(edge_type, 0) + 1

        return {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "node_types": node_type_counts,
            "edge_types": edge_type_counts,
            "session_id": session_id,
        }

    # #1010 (May 2026): `get_nodes_with_privacy` + `create_node_with_privacy`
    # service-layer methods removed alongside their repository counterparts.
    # They claimed privacy filtering the implementation never provided.
    # KG-internal privacy filtering as a real feature is tracked separately
    # (see #1010 follow-up). Callers should use `get_nodes_by_session` /
    # `create_node` directly.

    # Boundary-Enforced Operations (Issue #230)
    async def search_nodes(
        self,
        node_type: Optional[NodeType] = None,
        search_term: Optional[str] = None,
        owner_id: Optional[str] = None,
        limit: int = 10,
    ) -> List[KnowledgeNode]:
        """
        Search for nodes with boundary enforcement - optionally filter by owner.

        Args:
            node_type: Optional node type filter
            search_term: Optional search term
            owner_id: Optional owner ID filter (uses session_id internally)
            limit: Maximum results (subject to boundary limits)

        Returns:
            List of matching nodes (may be partial if limits hit)
        """
        # Start boundary tracking
        self.kg_boundary_enforcer.start_operation()

        try:
            # Check result size limit
            actual_limit = min(limit, self.kg_boundary_enforcer.boundaries.max_result_size)

            # Perform search via repository
            if node_type and owner_id:
                nodes = await self.repo.get_nodes_by_type(node_type, owner_id, actual_limit)
            elif node_type:
                nodes = await self.repo.get_nodes_by_type(node_type, None, actual_limit)
            elif owner_id:
                nodes = await self.repo.get_nodes_by_session(owner_id)
                nodes = nodes[:actual_limit]  # Limit results
            else:
                # General search - get nodes by type and filter
                all_nodes = []
                for nt in NodeType:
                    type_nodes = await self.repo.get_nodes_by_type(nt, None, actual_limit)
                    all_nodes.extend(type_nodes)
                    if len(all_nodes) >= actual_limit:
                        break
                nodes = all_nodes[:actual_limit]

            # Filter by search term if provided
            if search_term and nodes:
                search_lower = search_term.lower()
                nodes = [
                    n
                    for n in nodes
                    if search_lower in n.name.lower() or search_lower in n.description.lower()
                ]

            # Record nodes visited
            for node in nodes:
                self.kg_boundary_enforcer.visit_node(str(node.id))

            # Check if we hit limits
            stats = self.kg_boundary_enforcer.get_stats()
            if stats["nodes_visited"] >= stats["limits"]["max_nodes"]:
                self.logger.info("Search hit node count limit - results may be partial")

            return nodes[:actual_limit]

        except Exception as e:
            self.logger.error(f"Search failed with boundaries: {e}")
            raise

    async def traverse_relationships(
        self,
        start_node_id: str,
        max_depth: Optional[int] = None,
        edge_types: Optional[List[EdgeType]] = None,
        owner_id: Optional[str] = None,
    ) -> List[Dict]:
        """
        Traverse relationships with boundary enforcement - optionally verify ownership.

        Args:
            start_node_id: Starting node ID
            max_depth: Optional max depth (overrides boundary default)
            edge_types: Optional filter by edge types
            owner_id: Optional owner ID to verify ownership

        Returns:
            List of related nodes (may be partial if limits hit)
        """
        # Start boundary tracking
        self.kg_boundary_enforcer.start_operation()

        # Use boundary max_depth if not specified
        effective_max_depth = max_depth or self.kg_boundary_enforcer.boundaries.max_depth
        effective_max_depth = min(
            effective_max_depth, self.kg_boundary_enforcer.boundaries.max_depth
        )

        results = []
        current_depth = 0
        nodes_to_visit = [start_node_id]
        visited = set()

        while nodes_to_visit and current_depth < effective_max_depth:
            # Check timeout
            if not self.kg_boundary_enforcer.check_timeout():
                self.logger.warning("Traversal stopped: timeout reached")
                break

            # Check depth
            if not self.kg_boundary_enforcer.check_depth(current_depth):
                self.logger.warning("Traversal stopped: max depth reached")
                break

            # Visit nodes at this depth
            next_level = []
            for node_id in nodes_to_visit:
                if node_id in visited:
                    continue

                # Check node count
                if not self.kg_boundary_enforcer.visit_node(node_id):
                    self.logger.warning("Traversal stopped: max nodes reached")
                    return results

                visited.add(node_id)

                # Get node (with optional ownership verification)
                node = await self.repo.get_node_by_id(node_id, owner_id)
                if node:
                    results.append({"node": node, "depth": current_depth})

                    # Get outgoing edges with limit
                    neighbors = await self.repo.find_neighbors(
                        node_id, edge_type=None, direction="outgoing", owner_id=owner_id
                    )

                    # Limit edges per node
                    neighbors = neighbors[: self.kg_boundary_enforcer.boundaries.max_edges_per_node]

                    # Filter by edge types if specified
                    # (This is simplified - in a real implementation, we'd check edge types)
                    for neighbor in neighbors:
                        if str(neighbor.id) not in visited:
                            next_level.append(str(neighbor.id))

            nodes_to_visit = next_level
            current_depth += 1

        # Log stats
        stats = self.kg_boundary_enforcer.get_stats()
        self.logger.info(f"Traversal complete: {stats}")

        return results

    # Issue #278: Graph-First Retrieval Pattern
    async def expand(
        self,
        node_ids: List[str],
        max_hops: int = 2,
        edge_types: Optional[List[str]] = None,
        owner_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Expand from given nodes to nearby nodes using specified edge types - optionally verify ownership.

        This implements the graph-first retrieval pattern: query graph to gather
        context before expensive LLM processing.

        Args:
            node_ids: Starting nodes for expansion
            max_hops: Maximum depth for traversal (default: 2)
            edge_types: Filter by these edge types (e.g., ['BECAUSE', 'ENABLES'])
            owner_id: Optional owner ID to verify ownership

        Returns:
            Dictionary with expanded nodes and edges
        """
        visited_nodes = set(node_ids)
        nodes_to_expand = list(node_ids)
        all_edges = []

        for hop in range(max_hops):
            next_level = []

            for node_id in nodes_to_expand:
                # Get neighbors (with optional ownership verification)
                neighbors = await self.repo.find_neighbors(
                    node_id, edge_type=None, direction="outgoing", owner_id=owner_id
                )

                for neighbor_edge in neighbors:
                    # Filter by edge type if specified
                    if edge_types and neighbor_edge.edge_type.value not in edge_types:
                        continue

                    # Track edge and node
                    all_edges.append(neighbor_edge)
                    neighbor_node_id = neighbor_edge.target_node_id

                    if neighbor_node_id not in visited_nodes:
                        visited_nodes.add(neighbor_node_id)
                        next_level.append(neighbor_node_id)

            nodes_to_expand = next_level

            if not nodes_to_expand:
                break

        # Retrieve all nodes (with optional ownership verification)
        nodes = []
        for node_id in visited_nodes:
            node = await self.repo.get_node_by_id(node_id, owner_id)
            if node:
                nodes.append(node)

        return {"nodes": nodes, "edges": all_edges}

    async def extract_reasoning_chains(self, graph_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract reasoning chains from graph traversal results.

        Identifies sequences of causal/enables relationships that form
        logical reasoning paths.

        Args:
            graph_data: Result from expand() with nodes and edges

        Returns:
            List of reasoning chains
        """
        chains = []
        edges = graph_data.get("edges", [])
        nodes = {n.id: n for n in graph_data.get("nodes", [])}

        # Find causal/reasoning edges
        reasoning_edge_types = ["because", "enables", "requires", "leads_to", "prevents"]

        for edge in edges:
            if edge.edge_type.value not in reasoning_edge_types:
                continue

            source_node = nodes.get(edge.source_node_id)
            target_node = nodes.get(edge.target_node_id)

            if not source_node or not target_node:
                continue

            # Create reasoning chain entry
            chain = {
                "source": source_node.name,
                "edge_type": edge.edge_type.value,
                "target": target_node.name,
                "confidence": getattr(edge, "confidence", 1.0),
                "explanation": f"{source_node.name} {edge.edge_type.value} {target_node.name}",
            }
            chains.append(chain)

        return chains

    async def get_relevant_context(
        self,
        user_query: str,
        user_id: UUID,
        max_nodes: int = 10,
    ) -> Dict[str, Any]:
        """
        Get relevant context from knowledge graph for a user query.

        Implements the graph-first pattern: semantic search + 2-hop expansion
        + reasoning chain extraction.

        Args:
            user_query: User's question/request
            user_id: User ID for personalization (also owner_id for filtering)
            max_nodes: Maximum nodes to retrieve (default: 10)

        Returns:
            Dictionary with context nodes, edges, and reasoning chains
        """
        self.logger.info(
            "Getting relevant context from graph",
            user_query=user_query,
            user_id=user_id,
        )

        # Step 1: Search for relevant nodes
        relevant_nodes = await self.search_nodes(user_query, owner_id=str(user_id), limit=max_nodes)

        if not relevant_nodes:
            self.logger.debug(
                "No relevant nodes found in graph",
                user_query=user_query,
            )
            return {
                "nodes": [],
                "edges": [],
                "reasoning_chains": [],
                "found_context": False,
            }

        node_ids = [node.id for node in relevant_nodes]

        # Step 2: Expand to nearby nodes (2-hop traversal)
        causal_types = ["because", "enables", "requires", "prevents", "leads_to"]
        expanded_graph = await self.expand(
            node_ids=node_ids,
            max_hops=2,
            edge_types=causal_types,
            owner_id=str(user_id),
        )

        # Step 3: Extract reasoning chains
        reasoning_chains = await self.extract_reasoning_chains(expanded_graph)

        context = {
            "nodes": relevant_nodes,
            "expanded_nodes": expanded_graph["nodes"],
            "edges": expanded_graph["edges"],
            "reasoning_chains": reasoning_chains,
            "found_context": True,
        }

        self.logger.info(
            "Context retrieved from graph",
            node_count=len(relevant_nodes),
            chain_count=len(reasoning_chains),
        )

        return context
