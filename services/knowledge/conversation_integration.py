"""
Knowledge Graph integration for conversation enhancement.
Issue #99 - CORE-KNOW Phase 2

Provides context enrichment from the Knowledge Graph for conversation processing.
Follows the proven pattern from Ethics integration (#197).
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from services.database.repositories import KnowledgeGraphRepository
from services.database.session_factory import AsyncSessionFactory
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.shared_types import NodeType

logger = logging.getLogger(__name__)


class ConversationKnowledgeGraphIntegration:
    """
    Integrate Knowledge Graph with conversation flow.

    Follows the proven pattern from Ethics integration (#197).
    """

    def __init__(self, kg_service: Optional[KnowledgeGraphService] = None):
        """
        Initialize conversation integration.

        Args:
            kg_service: Optional KnowledgeGraphService instance (for testing)
        """
        self.kg_service = kg_service  # Will be set on first use if None
        self.enabled = True  # Will be controlled by feature flag

    async def _ensure_kg_service(self) -> KnowledgeGraphService:
        """Ensure KG service is initialized with repository."""
        if self.kg_service is None:
            # Create service with repository from session
            async with AsyncSessionFactory.session_scope() as session:
                repo = KnowledgeGraphRepository(session)
                self.kg_service = KnowledgeGraphService(
                    knowledge_graph_repository=repo,
                )
        return self.kg_service

    async def enhance_conversation_context(
        self, message: str, session_id: str, base_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhance conversation context with Knowledge Graph insights.

        Args:
            message: User's message text
            session_id: Conversation session identifier
            base_context: Optional base context to enhance

        Returns:
            Enhanced context dictionary with graph insights
        """
        if not self.enabled:
            logger.debug("Knowledge Graph enhancement disabled")
            return base_context or {}

        try:
            # Start with base context
            enhanced_context = base_context.copy() if base_context else {}

            # Query Knowledge Graph for relevant context
            graph_insights = await self._query_graph_context(message, session_id)

            # Merge graph insights into context
            enhanced_context["knowledge_graph"] = graph_insights

            # Add specific enrichments
            if graph_insights.get("concepts"):
                enhanced_context["related_concepts"] = graph_insights["concepts"]

            if graph_insights.get("patterns"):
                enhanced_context["recent_patterns"] = graph_insights["patterns"]

            if graph_insights.get("entities"):
                enhanced_context["mentioned_entities"] = graph_insights["entities"]

            logger.info(
                f"Enhanced context with {len(graph_insights.get('concepts', []))} concepts, "
                f"{len(graph_insights.get('patterns', []))} patterns"
            )

            return enhanced_context

        except Exception as e:
            # Graceful degradation - log error but continue
            logger.error(f"Knowledge Graph enhancement failed: {e}", exc_info=True)
            return base_context or {}

    async def _query_graph_context(self, message: str, session_id: str) -> Dict[str, Any]:
        """
        Query Knowledge Graph for relevant context.

        Args:
            message: User's message
            session_id: Session identifier

        Returns:
            Dictionary with graph insights
        """
        insights = {"concepts": [], "patterns": [], "entities": [], "relationships": []}

        try:
            # Use session-scoped repository for queries
            async with AsyncSessionFactory.session_scope() as session:
                repo = KnowledgeGraphRepository(session)
                kg_service = KnowledgeGraphService(knowledge_graph_repository=repo)

                # Query for concept-related nodes
                # Extract potential concept mentions from message
                concept_keywords = self._extract_keywords(
                    message, ["project", "website", "site", "feature"]
                )

                if concept_keywords:
                    concepts = await self._query_concepts(kg_service, concept_keywords)
                    insights["concepts"] = concepts

                # Query for recent patterns in this session
                patterns = await self._query_session_patterns(kg_service, session_id)
                insights["patterns"] = patterns

                # Query for entities mentioned
                entities = await self._query_entities(kg_service, message)
                insights["entities"] = entities

            return insights

        except Exception as e:
            logger.error(f"Graph query failed: {e}")
            return insights

    async def _query_concepts(
        self, kg_service: KnowledgeGraphService, keywords: List[str]
    ) -> List[Dict[str, Any]]:
        """Query for concept nodes matching keywords."""
        try:
            # Search for concept nodes (using CONCEPT node type since PROJECT doesn't exist)
            concepts = []

            # Get recent concepts from the graph
            nodes = await kg_service.get_nodes_by_type(NodeType.CONCEPT, limit=10)

            # Simple keyword matching against node names/descriptions
            for node in nodes:
                node_text = f"{node.name} {node.description}".lower()
                if any(keyword.lower() in node_text for keyword in keywords):
                    concepts.append(
                        {
                            "id": str(node.id),
                            "name": node.name,
                            "description": node.description,
                            "metadata": node.metadata,
                        }
                    )

                    if len(concepts) >= 3:  # Limit to top 3
                        break

            return concepts

        except Exception as e:
            logger.error(f"Concept query failed: {e}")
            return []

    async def _query_session_patterns(
        self, kg_service: KnowledgeGraphService, session_id: str
    ) -> List[Dict[str, Any]]:
        """Query for patterns in this session."""
        try:
            # Find nodes for this session
            nodes = await kg_service.repo.get_nodes_by_session(session_id, limit=10)

            # Extract patterns from recent interactions
            patterns = []
            for node in nodes[-5:]:  # Last 5 interactions
                patterns.append(
                    {
                        "timestamp": node.created_at.isoformat() if node.created_at else None,
                        "type": (
                            node.node_type.value
                            if hasattr(node.node_type, "value")
                            else str(node.node_type)
                        ),
                        "summary": node.description,
                    }
                )

            return patterns

        except Exception as e:
            logger.error(f"Pattern query failed: {e}")
            return []

    async def _query_entities(
        self, kg_service: KnowledgeGraphService, message: str
    ) -> List[Dict[str, Any]]:
        """Query for entities mentioned in message."""
        try:
            # Simple entity extraction (enhance later with NER)
            entities = []

            # Look for capitalized words that might be entities
            words = message.split()
            potential_entities = [w.strip(".,!?") for w in words if len(w) > 0 and w[0].isupper()]

            # Get nodes that might match (using multiple node types)
            for node_type in [NodeType.PERSON, NodeType.ORGANIZATION, NodeType.TECHNOLOGY]:
                nodes = await kg_service.get_nodes_by_type(node_type, limit=5)

                for node in nodes:
                    # Check if node name matches any potential entity
                    if any(entity.lower() in node.name.lower() for entity in potential_entities):
                        entities.append(
                            {
                                "name": node.name,
                                "type": (
                                    node.node_type.value
                                    if hasattr(node.node_type, "value")
                                    else str(node.node_type)
                                ),
                                "id": str(node.id),
                            }
                        )

                        if len(entities) >= 5:  # Limit to 5
                            break

                if len(entities) >= 5:
                    break

            return entities

        except Exception as e:
            logger.error(f"Entity query failed: {e}")
            return []

    def _extract_keywords(self, text: str, topic_words: List[str]) -> List[str]:
        """Extract keywords related to topic words."""
        keywords = []
        text_lower = text.lower()

        for topic in topic_words:
            if topic in text_lower:
                # Simple extraction - find words near topic word
                words = text_lower.split()
                if topic in words:
                    idx = words.index(topic)
                    # Get context words around topic
                    start = max(0, idx - 2)
                    end = min(len(words), idx + 3)
                    context = words[start:end]
                    keywords.extend([w for w in context if len(w) > 3])

        return list(set(keywords))[:5]  # Limit to 5 unique keywords
