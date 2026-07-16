"""
Semantic Indexing Service - PM-040 Phase 3
Metadata-focused semantic indexing for testing our hypothesis
Prepares for future pgvector integration while starting with metadata embeddings
"""

import hashlib
import json
from collections import Counter
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import structlog

from services.database.repositories import KnowledgeGraphRepository
from services.domain.models import KnowledgeEdge, KnowledgeNode
from services.knowledge.pattern_recognition_service import PatternRecognitionService
from services.shared_types import EdgeType, NodeType

logger = structlog.get_logger()


class SemanticIndexingService:
    """
    Semantic indexing service with metadata-focused approach
    Tests the hypothesis that metadata patterns provide sufficient semantic understanding
    """

    def __init__(
        self,
        knowledge_graph_repository: KnowledgeGraphRepository,
        pattern_recognition_service: Optional[PatternRecognitionService] = None,
    ):
        self.repo = knowledge_graph_repository
        self.pattern_service = pattern_recognition_service
        self.logger = logger.bind(service="semantic_indexing")

        # Embedding configuration
        self.embedding_dim = 128  # Start with smaller embeddings for metadata
        self.metadata_weights = {
            "node_type": 0.2,
            "properties": 0.3,
            "relationships": 0.3,
            "temporal": 0.1,
            "structural": 0.1,
        }

    async def generate_embedding(self, node: KnowledgeNode) -> List[float]:
        """
        Generate metadata-based embedding for a node
        Testing hypothesis: Can we achieve meaningful similarity from metadata alone?

        Args:
            node: KnowledgeNode to generate embedding for

        Returns:
            List of floats representing the embedding vector
        """
        self.logger.info(
            "Generating metadata embedding", node_id=node.id, node_type=node.node_type.value
        )

        # Initialize embedding components
        embedding_components = []

        # 1. Node type embedding (categorical)
        type_embedding = self._encode_node_type(node.node_type)
        embedding_components.append(("node_type", type_embedding))

        # 2. Properties embedding (structural features)
        props_embedding = self._encode_properties(node.properties)
        embedding_components.append(("properties", props_embedding))

        # 3. Relationship embedding (graph structure)
        rel_embedding = await self._encode_relationships(node.id)
        embedding_components.append(("relationships", rel_embedding))

        # 4. Temporal embedding (time-based features)
        temp_embedding = self._encode_temporal_features(node)
        embedding_components.append(("temporal", temp_embedding))

        # 5. Structural embedding (metadata structure)
        struct_embedding = self._encode_structural_features(node.metadata)
        embedding_components.append(("structural", struct_embedding))

        # Combine embeddings with weights
        final_embedding = self._combine_embeddings(embedding_components)

        # Normalize to unit length
        norm = np.linalg.norm(final_embedding)
        if norm > 0:
            final_embedding = final_embedding / norm

        return final_embedding.tolist()

    def _encode_node_type(self, node_type: NodeType) -> np.ndarray:
        """Encode node type as one-hot vector"""
        # Get all node types
        all_types = list(NodeType)
        type_vector = np.zeros(len(all_types))

        # Set the corresponding type to 1
        type_index = all_types.index(node_type)
        type_vector[type_index] = 1.0

        # Pad or truncate to fit embedding dimension segment
        segment_size = self.embedding_dim // 5  # Allocate 1/5 of embedding to type
        if len(type_vector) < segment_size:
            type_vector = np.pad(type_vector, (0, segment_size - len(type_vector)))
        else:
            type_vector = type_vector[:segment_size]

        return type_vector

    def _encode_properties(self, properties: Dict[str, Any]) -> np.ndarray:
        """Encode properties dictionary into vector"""
        segment_size = self.embedding_dim // 5

        if not properties:
            return np.zeros(segment_size)

        # Extract features from properties
        features = []

        # Number of properties
        features.append(len(properties))

        # Property key patterns
        key_lengths = [len(k) for k in properties.keys()]
        features.extend(
            [
                np.mean(key_lengths) if key_lengths else 0,
                np.std(key_lengths) if key_lengths else 0,
                max(key_lengths) if key_lengths else 0,
            ]
        )

        # Value type distribution
        type_counts = Counter(type(v).__name__ for v in properties.values())
        for t in ["str", "int", "float", "bool", "list", "dict"]:
            features.append(type_counts.get(t, 0))

        # Nested structure depth
        max_depth = self._get_max_depth(properties)
        features.append(max_depth)

        # Convert to numpy array and pad/truncate
        feature_vector = np.array(features, dtype=np.float32)
        if len(feature_vector) < segment_size:
            feature_vector = np.pad(feature_vector, (0, segment_size - len(feature_vector)))
        else:
            feature_vector = feature_vector[:segment_size]

        # Normalize
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm

        return feature_vector

    async def _encode_relationships(self, node_id: str) -> np.ndarray:
        """Encode relationship patterns for a node"""
        segment_size = self.embedding_dim // 5

        # Get neighbors
        neighbors = await self.repo.find_neighbors(node_id)

        # Get edges
        incoming_edges = []
        outgoing_edges = []
        all_edges = await self.repo.get_edges_by_session(None, limit=1000)

        for edge in all_edges:
            if edge.source_node_id == node_id:
                outgoing_edges.append(edge)
            elif edge.target_node_id == node_id:
                incoming_edges.append(edge)

        # Extract relationship features
        features = []

        # Degree features
        features.extend(
            [
                len(neighbors),
                len(incoming_edges),
                len(outgoing_edges),
                len(incoming_edges) + len(outgoing_edges),  # total degree
            ]
        )

        # Edge type distribution
        edge_type_counts = Counter()
        for edge in incoming_edges + outgoing_edges:
            edge_type_counts[edge.edge_type.value] += 1

        # Add edge type features
        for edge_type in EdgeType:
            features.append(edge_type_counts.get(edge_type.value, 0))

        # Weight statistics
        weights = [e.weight for e in incoming_edges + outgoing_edges]
        if weights:
            features.extend([np.mean(weights), np.std(weights), min(weights), max(weights)])
        else:
            features.extend([0, 0, 0, 0])

        # Convert to numpy array and pad/truncate
        feature_vector = np.array(features, dtype=np.float32)
        if len(feature_vector) < segment_size:
            feature_vector = np.pad(feature_vector, (0, segment_size - len(feature_vector)))
        else:
            feature_vector = feature_vector[:segment_size]

        # Normalize
        norm = np.linalg.norm(feature_vector)
        if norm > 0:
            feature_vector = feature_vector / norm

        return feature_vector

    def _encode_temporal_features(self, node: KnowledgeNode) -> np.ndarray:
        """Encode temporal features of a node"""
        segment_size = self.embedding_dim // 5
        features = []

        # Time-based features — match the node's tz-awareness: DB-loaded nodes
        # carry tz-aware created_at, ad-hoc query nodes may be naive. (#1420:
        # this code path was dead in production, so the naive/aware mismatch
        # had never executed.)
        if node.created_at is not None and node.created_at.tzinfo is not None:
            now = datetime.now(node.created_at.tzinfo)
        else:
            now = datetime.now()

        # Age in days
        age_days = (now - node.created_at).days if node.created_at else 0
        features.append(age_days)

        # Update recency
        if node.updated_at and node.created_at:
            update_days = (node.updated_at - node.created_at).days
            features.append(update_days)
        else:
            features.append(0)

        # Hour of creation (cyclical encoding)
        if node.created_at:
            hour = node.created_at.hour
            features.extend([np.sin(2 * np.pi * hour / 24), np.cos(2 * np.pi * hour / 24)])
        else:
            features.extend([0, 0])

        # Day of week (cyclical encoding)
        if node.created_at:
            dow = node.created_at.weekday()
            features.extend([np.sin(2 * np.pi * dow / 7), np.cos(2 * np.pi * dow / 7)])
        else:
            features.extend([0, 0])

        # Convert to numpy array and pad/truncate
        feature_vector = np.array(features, dtype=np.float32)
        if len(feature_vector) < segment_size:
            feature_vector = np.pad(feature_vector, (0, segment_size - len(feature_vector)))
        else:
            feature_vector = feature_vector[:segment_size]

        return feature_vector

    def _encode_structural_features(self, metadata: Dict[str, Any]) -> np.ndarray:
        """Encode structural features of metadata"""
        segment_size = self.embedding_dim - (4 * (self.embedding_dim // 5))  # Remaining space

        # Create a deterministic hash of the metadata structure
        structure_str = self._get_structure_string(metadata)
        structure_hash = hashlib.md5(structure_str.encode()).digest()

        # Convert hash to features
        features = list(structure_hash)[:segment_size]

        # Pad if necessary
        if len(features) < segment_size:
            features.extend([0] * (segment_size - len(features)))

        feature_vector = np.array(features, dtype=np.float32) / 255.0  # Normalize to [0, 1]

        return feature_vector

    def _combine_embeddings(self, components: List[Tuple[str, np.ndarray]]) -> np.ndarray:
        """Combine embedding components with weights"""
        combined = np.zeros(self.embedding_dim)

        for name, embedding in components:
            weight = self.metadata_weights.get(name, 0.1)
            start_idx = 0

            # Place each component in its section
            if name == "node_type":
                start_idx = 0
            elif name == "properties":
                start_idx = self.embedding_dim // 5
            elif name == "relationships":
                start_idx = 2 * (self.embedding_dim // 5)
            elif name == "temporal":
                start_idx = 3 * (self.embedding_dim // 5)
            elif name == "structural":
                start_idx = 4 * (self.embedding_dim // 5)

            end_idx = min(start_idx + len(embedding), self.embedding_dim)
            combined[start_idx:end_idx] = embedding[: end_idx - start_idx] * weight

        return combined

    async def similarity_search(
        self,
        query_node: KnowledgeNode,
        top_k: int = 10,
        min_similarity: float = 0.5,
        node_types: Optional[List[NodeType]] = None,
        *,
        owner_id: Optional[str] = None,
        session_id: Optional[str] = None,
        threshold: Optional[float] = None,
    ) -> List[Tuple[KnowledgeNode, float]]:
        """
        Find similar nodes using metadata-based embeddings — OWNER-SCOPED.

        #1420: candidate retrieval is filtered to the acting principal and
        FAILS CLOSED — no resolvable owner means no results, never a
        cross-tenant scan (nodes carry user text in metadata). Both production
        callers had passed ``session_id=``/``threshold=`` kwargs this signature
        didn't accept; the TypeError was swallowed upstream, so the feature was
        silently dead AND the unscoped body was a primed cross-user leak. The
        kwargs are now real.

        Args:
            query_node: Node to search for similar nodes
            top_k: Number of results to return
            min_similarity: Minimum similarity threshold
            node_types: Optional filter by node types
            owner_id: Acting principal; falls back to session_id then
                query_node.session_id (the callers' existing conventions)
            session_id: Legacy alias for owner_id (matches the repo layer)
            threshold: Legacy alias for min_similarity

        Returns:
            List of (node, similarity_score) tuples — the owner's nodes only
        """
        if threshold is not None:
            min_similarity = threshold
        owner = owner_id or session_id or query_node.session_id
        if not owner:
            self.logger.warning(
                "similarity_search without a resolvable owner — fail-closed empty (#1420)",
                query_node_id=query_node.id,
            )
            return []

        self.logger.info(
            "Performing similarity search", query_node_id=query_node.id, top_k=top_k, owner=owner
        )

        # Generate embedding for query node
        query_embedding = np.array(await self.generate_embedding(query_node))

        # Get candidate nodes — owner-scoped (repo param named session_id for
        # backward compatibility; it filters KnowledgeNodeDB.owner_id)
        candidates = []
        if node_types:
            for node_type in node_types:
                nodes = await self.repo.get_nodes_by_type(node_type, session_id=owner, limit=1000)
                candidates.extend(nodes)
        else:
            # Get all nodes (with reasonable limit)
            for node_type in NodeType:
                nodes = await self.repo.get_nodes_by_type(node_type, session_id=owner, limit=100)
                candidates.extend(nodes)

        # Calculate similarities
        similarities = []
        for candidate in candidates:
            if candidate.id == query_node.id:
                continue  # Skip self

            # Generate embedding for candidate
            candidate_embedding = np.array(await self.generate_embedding(candidate))

            # Calculate cosine similarity
            similarity = np.dot(query_embedding, candidate_embedding)

            if similarity >= min_similarity:
                similarities.append((candidate, float(similarity)))

        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    async def index_node(self, node: KnowledgeNode) -> bool:
        """
        Index a node by generating and storing its embedding

        Args:
            node: Node to index

        Returns:
            True if successful
        """
        try:
            # Generate embedding
            embedding = await self.generate_embedding(node)

            # For now, store in node's metadata (future: pgvector)
            if not node.metadata:
                node.metadata = {}

            node.metadata["_embedding"] = {
                "vector": embedding,
                "indexed_at": datetime.now().isoformat(),
                "version": "metadata_v1",
            }

            # Update node in repository
            await self.repo.update(node.id, metadata=node.metadata)

            self.logger.info(
                "Node indexed successfully", node_id=node.id, embedding_dim=len(embedding)
            )

            return True

        except Exception as e:
            self.logger.error("Failed to index node", node_id=node.id, error=str(e))
            return False

    async def index_subgraph(self, node_ids: List[str]) -> Dict[str, bool]:
        """
        Index multiple nodes as a batch

        Args:
            node_ids: List of node IDs to index

        Returns:
            Dict mapping node_id to success status
        """
        results = {}

        for node_id in node_ids:
            node = await self.repo.get_node_by_id(node_id)
            if node:
                results[node_id] = await self.index_node(node)
            else:
                results[node_id] = False

        return results

    async def get_clustering_features(self, nodes: List[KnowledgeNode]) -> np.ndarray:
        """
        Get feature matrix for clustering analysis

        Args:
            nodes: List of nodes to analyze

        Returns:
            2D numpy array where each row is a node's embedding
        """
        embeddings = []

        for node in nodes:
            embedding = await self.generate_embedding(node)
            embeddings.append(embedding)

        return np.array(embeddings)

    # Helper methods
    def _get_max_depth(self, obj: Any, current_depth: int = 0) -> int:
        """Get maximum nesting depth of a data structure"""
        if not isinstance(obj, (dict, list)):
            return current_depth

        if isinstance(obj, dict):
            if not obj:
                return current_depth
            return max(self._get_max_depth(v, current_depth + 1) for v in obj.values())

        if isinstance(obj, list):
            if not obj:
                return current_depth
            return max(self._get_max_depth(item, current_depth + 1) for item in obj)

    def _get_structure_string(self, obj: Any, path: str = "") -> str:
        """Get a string representation of data structure (keys only)"""
        if isinstance(obj, dict):
            parts = []
            for k in sorted(obj.keys()):
                new_path = f"{path}.{k}" if path else k
                parts.append(new_path)
                parts.append(self._get_structure_string(obj[k], new_path))
            return ";".join(parts)
        elif isinstance(obj, list) and obj:
            return f"{path}[]"
        else:
            return f"{path}:{type(obj).__name__}"

    # PM-specific semantic features
    async def extract_pm_features(self, node: KnowledgeNode) -> Dict[str, Any]:
        """
        Extract PM-relevant semantic features from a node

        Returns features like:
        - Project management domain indicators
        - Workflow patterns
        - Stakeholder relationships
        - Priority/urgency signals
        """
        features = {
            "is_pm_related": False,
            "workflow_indicators": [],
            "stakeholder_count": 0,
            "urgency_score": 0.0,
            "complexity_score": 0.0,
        }

        # Check for PM-related node types
        pm_node_types = {NodeType.DOCUMENT, NodeType.PROCESS, NodeType.METRIC}
        if node.node_type in pm_node_types:
            features["is_pm_related"] = True

        # Check metadata for PM keywords
        pm_keywords = [
            "project",
            "task",
            "sprint",
            "milestone",
            "deadline",
            "stakeholder",
            "requirement",
            "deliverable",
            "risk",
        ]

        metadata_str = json.dumps(node.metadata).lower()
        properties_str = json.dumps(node.properties).lower()

        for keyword in pm_keywords:
            if keyword in metadata_str or keyword in properties_str:
                features["workflow_indicators"].append(keyword)

        # Analyze relationships for stakeholder patterns
        neighbors = await self.repo.find_neighbors(node.id)
        person_neighbors = [n for n in neighbors if n.node_type == NodeType.PERSON]
        features["stakeholder_count"] = len(person_neighbors)

        # Calculate urgency score based on temporal features
        if "deadline" in node.metadata or "due_date" in node.metadata:
            features["urgency_score"] = 0.8
        elif "priority" in node.metadata:
            priority = str(node.metadata.get("priority", "")).lower()
            if priority in ["high", "critical", "urgent"]:
                features["urgency_score"] = 0.9
            elif priority == "medium":
                features["urgency_score"] = 0.5
            else:
                features["urgency_score"] = 0.2

        # Calculate complexity based on relationships and metadata
        edge_count = len(await self.repo.get_edges_by_session(node.session_id))
        metadata_depth = self._get_max_depth(node.metadata)

        features["complexity_score"] = min(
            1.0, (edge_count / 10) * 0.5 + (metadata_depth / 5) * 0.5
        )

        return features
