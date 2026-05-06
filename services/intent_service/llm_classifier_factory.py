"""
PM-034: Factory for creating LLMIntentClassifier with proper dependencies

This factory handles the wiring of PM-040 Knowledge Graph services
into the LLM Intent Classifier for production use.
"""

from typing import Optional

import structlog

from services.database.repositories import KnowledgeGraphRepository
from services.database.session_factory import AsyncSessionFactory
from services.intent_service.llm_classifier import LLMIntentClassifier
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.semantic_indexing_service import SemanticIndexingService

logger = structlog.get_logger()


class LLMClassifierFactory:
    """Factory for creating properly wired LLMIntentClassifier instances"""

    @staticmethod
    async def create(
        confidence_threshold: float = 0.75,
        enable_learning: bool = True,
        enable_knowledge_graph: bool = True,
    ) -> LLMIntentClassifier:
        """
        Create LLMIntentClassifier with all dependencies wired

        Args:
            confidence_threshold: Minimum confidence for classification
            enable_learning: Whether to store classifications for learning
            enable_knowledge_graph: Whether to use Knowledge Graph context

        Returns:
            Fully configured LLMIntentClassifier
        """

        knowledge_graph_service = None
        semantic_indexing_service = None

        if enable_knowledge_graph:
            try:
                # Create Knowledge Graph dependencies
                async with AsyncSessionFactory.session_scope() as session:
                    # Create repository
                    kg_repository = KnowledgeGraphRepository(session)

                    # Create services
                    knowledge_graph_service = KnowledgeGraphService(
                        knowledge_graph_repository=kg_repository,
                    )

                    semantic_indexing_service = SemanticIndexingService(
                        knowledge_graph_repository=kg_repository,
                        pattern_recognition_service=None,  # Optional dependency
                    )

                    logger.info("Knowledge Graph services initialized for LLM classifier")

            except Exception as e:
                logger.warning(
                    f"Failed to initialize Knowledge Graph services: {e}. "
                    "Continuing without Knowledge Graph context."
                )
                knowledge_graph_service = None
                semantic_indexing_service = None

        # Create classifier with dependencies
        classifier = LLMIntentClassifier(
            knowledge_graph_service=knowledge_graph_service,
            semantic_indexing_service=semantic_indexing_service,
            confidence_threshold=confidence_threshold,
            enable_learning=enable_learning,
        )

        logger.info(
            "LLMIntentClassifier created",
            has_knowledge_graph=knowledge_graph_service is not None,
            confidence_threshold=confidence_threshold,
            enable_learning=enable_learning,
        )

        return classifier

    @staticmethod
    async def create_for_testing(
        mock_knowledge_graph_service=None,
        mock_semantic_indexing_service=None,
        mock_llm_service=None,
        confidence_threshold: float = 0.75,
    ) -> LLMIntentClassifier:
        """
        Create LLMIntentClassifier for testing with mock dependencies

        Args:
            mock_knowledge_graph_service: Mock KnowledgeGraphService
            mock_semantic_indexing_service: Mock SemanticIndexingService
            mock_llm_service: Mock LLM service (Issue #322 - required for DI)
            confidence_threshold: Minimum confidence for classification

        Returns:
            LLMIntentClassifier configured for testing
        """

        return LLMIntentClassifier(
            llm_service=mock_llm_service,
            knowledge_graph_service=mock_knowledge_graph_service,
            semantic_indexing_service=mock_semantic_indexing_service,
            confidence_threshold=confidence_threshold,
            enable_learning=False,  # Disable learning in tests
        )
