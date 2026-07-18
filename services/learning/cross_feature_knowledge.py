"""
Cross-Feature Knowledge Sharing Service

Provides mechanisms for different features to learn from each other's patterns
and share knowledge through the Document Memory system.

Built on: Knowledge Graph Service + Pattern Recognition + Learning Loop
Performance: Real-time knowledge sharing and pattern discovery
"""

import asyncio
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from services.database.repositories import KnowledgeGraphRepository
from services.domain.models import KnowledgeEdge, KnowledgeNode
from services.knowledge.knowledge_graph_service import KnowledgeGraphService
from services.knowledge.pattern_recognition_service import PatternRecognitionService
from services.shared_types import EdgeType, NodeType

from .query_learning_loop import LearnedPattern, PatternType, QueryLearningLoop

# Configure logging
logger = logging.getLogger(__name__)


class KnowledgeSharingType(Enum):
    """Types of knowledge sharing between features"""

    PATTERN_TRANSFER = "pattern_transfer"
    QUERY_ENHANCEMENT = "query_enhancement"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"
    RESPONSE_IMPROVEMENT = "response_improvement"
    INTEGRATION_KNOWLEDGE = "integration_knowledge"


class ConfidenceLevel(Enum):
    """Confidence levels for shared knowledge"""

    EXPERIMENTAL = "experimental"  # 0-30% confidence
    DEVELOPING = "developing"  # 31-60% confidence
    RELIABLE = "reliable"  # 61-85% confidence
    PROVEN = "proven"  # 86-100% confidence


@dataclass
class SharedKnowledge:
    """Represents knowledge shared between features"""

    knowledge_id: str
    source_feature: str
    target_feature: str
    sharing_type: KnowledgeSharingType
    knowledge_data: Dict[str, Any]
    confidence: float
    usage_count: int
    success_rate: float
    first_shared: datetime
    last_used: datetime
    feedback_score: float
    metadata: Dict[str, Any]


@dataclass
class CrossFeaturePattern:
    """Represents a pattern that can be shared between features"""

    pattern_id: str
    source_feature: str
    target_feature: str
    pattern_type: PatternType
    pattern_data: Dict[str, Any]
    transfer_confidence: float
    adaptation_required: bool
    adaptation_notes: Optional[str]
    metadata: Dict[str, Any]


class CrossFeatureKnowledgeService:
    """
    Service for sharing knowledge and patterns between different features
    of the Piper Morgan system.
    """

    def __init__(
        self,
        knowledge_service: KnowledgeGraphService,
        pattern_service: PatternRecognitionService,
        learning_loop: QueryLearningLoop,
    ):
        """Initialize the cross-feature knowledge service"""
        self.knowledge_service = knowledge_service
        self.pattern_service = pattern_service
        self.learning_loop = learning_loop

        # Knowledge sharing storage
        self.shared_knowledge: Dict[str, SharedKnowledge] = {}
        self.cross_feature_patterns: Dict[str, CrossFeaturePattern] = {}

        # Feature mapping for knowledge transfer
        self.feature_capabilities = {
            "issue_intelligence": {
                "query_patterns": True,
                "workflow_patterns": True,
                "response_patterns": True,
                "integration_patterns": True,
            },
            "morning_standup": {
                "query_patterns": True,
                "workflow_patterns": True,
                "response_patterns": True,
                "integration_patterns": False,  # Limited integration
            },
        }

    async def share_knowledge(
        self,
        source_feature: str,
        target_feature: str,
        sharing_type: KnowledgeSharingType,
        knowledge_data: Dict[str, Any],
        confidence: float,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Share knowledge from one feature to another

        Args:
            source_feature: Feature sharing the knowledge
            target_feature: Feature receiving the knowledge
            sharing_type: Type of knowledge being shared
            knowledge_data: The actual knowledge data
            confidence: Confidence level in the knowledge
            metadata: Additional metadata

        Returns:
            Knowledge ID for future reference
        """
        # Validate feature capabilities
        if not self._can_share_knowledge(source_feature, target_feature, sharing_type):
            logger.warning(
                f"Cannot share {sharing_type.value} from {source_feature} to {target_feature}"
            )
            return None

        # Generate unique knowledge ID
        timestamp = datetime.now()
        knowledge_id = (
            f"shared_{source_feature}_{target_feature}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        )

        # Create shared knowledge entry
        shared_knowledge = SharedKnowledge(
            knowledge_id=knowledge_id,
            source_feature=source_feature,
            target_feature=target_feature,
            sharing_type=sharing_type,
            knowledge_data=knowledge_data,
            confidence=confidence,
            usage_count=0,
            success_rate=0.0,
            first_shared=timestamp,
            last_used=timestamp,
            feedback_score=0.0,
            metadata=metadata or {},
        )

        # Store shared knowledge
        self.shared_knowledge[knowledge_id] = shared_knowledge

        # Create knowledge graph node for the shared knowledge
        await self._create_knowledge_node(shared_knowledge)

        logger.info(f"Knowledge shared: {knowledge_id} from {source_feature} to {target_feature}")
        return knowledge_id

    def _can_share_knowledge(
        self, source_feature: str, target_feature: str, sharing_type: KnowledgeSharingType
    ) -> bool:
        """Check if knowledge can be shared between features"""
        if source_feature not in self.feature_capabilities:
            return False

        if target_feature not in self.feature_capabilities:
            return False

        # Check if target feature can handle this type of knowledge
        if sharing_type == KnowledgeSharingType.INTEGRATION_KNOWLEDGE:
            return self.feature_capabilities[target_feature].get("integration_patterns", False)

        return True

    async def _create_knowledge_node(self, shared_knowledge: SharedKnowledge) -> None:
        """Create a knowledge graph node for shared knowledge"""
        try:
            node_name = f"Shared Knowledge: {shared_knowledge.sharing_type.value}"
            node_description = f"Knowledge shared from {shared_knowledge.source_feature} to {shared_knowledge.target_feature}"

            metadata = {
                "source_feature": shared_knowledge.source_feature,
                "target_feature": shared_knowledge.target_feature,
                "sharing_type": shared_knowledge.sharing_type.value,
                "confidence": shared_knowledge.confidence,
                "knowledge_id": shared_knowledge.knowledge_id,
            }

            # Create the knowledge node
            await self.knowledge_service.create_node(
                name=node_name,
                node_type=NodeType.KNOWLEDGE,
                description=node_description,
                metadata=metadata,
                properties=shared_knowledge.knowledge_data,
            )

        except Exception as e:
            logger.error(f"Failed to create knowledge node: {e}")

    async def transfer_pattern(
        self,
        source_feature: str,
        target_feature: str,
        pattern_id: str,
        adaptation_required: bool = False,
        adaptation_notes: Optional[str] = None,
    ) -> Optional[str]:
        """
        Transfer a learned pattern from one feature to another

        Args:
            source_feature: Feature with the pattern
            target_feature: Feature to transfer the pattern to
            pattern_id: ID of the pattern to transfer
            adaptation_required: Whether the pattern needs adaptation
            adaptation_notes: Notes about required adaptations

        Returns:
            Cross-feature pattern ID if successful
        """
        try:
            # Get the source pattern
            source_patterns = await self.learning_loop.get_patterns_for_feature(source_feature)
            source_pattern = next((p for p in source_patterns if p.pattern_id == pattern_id), None)

            if not source_pattern:
                logger.warning(f"Pattern {pattern_id} not found in {source_feature}")
                return None

            # Check if pattern can be transferred
            if not self._can_transfer_pattern(source_pattern, target_feature):
                logger.warning(f"Pattern {pattern_id} cannot be transferred to {target_feature}")
                return None

            # Create cross-feature pattern
            cross_pattern = CrossFeaturePattern(
                pattern_id=pattern_id,
                source_feature=source_feature,
                target_feature=target_feature,
                pattern_type=source_pattern.pattern_type,
                pattern_data=source_pattern.pattern_data,
                transfer_confidence=source_pattern.confidence
                * 0.8,  # Slightly lower confidence for transfer
                adaptation_required=adaptation_required,
                adaptation_notes=adaptation_notes,
                metadata=source_pattern.metadata,
            )

            # Store cross-feature pattern
            cross_pattern_id = f"cross_{source_feature}_{target_feature}_{pattern_id}"
            self.cross_feature_patterns[cross_pattern_id] = cross_pattern

            # Learn the pattern in the target feature
            target_pattern_id = await self.learning_loop.learn_pattern(
                pattern_type=source_pattern.pattern_type,
                source_feature=target_feature,
                pattern_data=source_pattern.pattern_data,
                initial_confidence=cross_pattern.transfer_confidence,
                metadata={
                    **source_pattern.metadata,
                    "transferred_from": source_feature,
                    "cross_feature_pattern_id": cross_pattern_id,
                    "adaptation_required": adaptation_required,
                    "adaptation_notes": adaptation_notes,
                },
            )

            logger.info(
                f"Pattern transferred: {pattern_id} from {source_feature} to {target_feature}"
            )
            return cross_pattern_id

        except Exception as e:
            logger.error(f"Failed to transfer pattern: {e}")
            return None

    def _can_transfer_pattern(self, pattern: LearnedPattern, target_feature: str) -> bool:
        """Check if a pattern can be transferred to a target feature"""
        if target_feature not in self.feature_capabilities:
            return False

        # Check feature capabilities for this pattern type
        if pattern.pattern_type == PatternType.INTEGRATION_PATTERN:
            return self.feature_capabilities[target_feature].get("integration_patterns", False)

        return True

    async def get_shared_knowledge(
        self,
        target_feature: str,
        sharing_type: Optional[KnowledgeSharingType] = None,
        min_confidence: float = 0.3,
    ) -> List[SharedKnowledge]:
        """
        Get knowledge shared with a specific feature

        Args:
            target_feature: Feature to get knowledge for
            sharing_type: Optional filter by sharing type
            min_confidence: Minimum confidence threshold

        Returns:
            List of shared knowledge entries
        """
        knowledge = []
        for shared in self.shared_knowledge.values():
            if shared.target_feature == target_feature:
                if sharing_type and shared.sharing_type != sharing_type:
                    continue
                if shared.confidence >= min_confidence:
                    knowledge.append(shared)

        # Sort by confidence and usage count
        knowledge.sort(key=lambda k: (k.confidence, k.usage_count), reverse=True)
        return knowledge

    async def get_cross_feature_patterns(
        self,
        target_feature: str,
        pattern_type: Optional[PatternType] = None,
        min_confidence: float = 0.4,
    ) -> List[CrossFeaturePattern]:
        """
        Get patterns that can be transferred to a target feature

        Args:
            target_feature: Feature to get patterns for
            pattern_type: Optional pattern type filter
            min_confidence: Minimum confidence threshold

        Returns:
            List of cross-feature patterns
        """
        patterns = []
        for cross_pattern in self.cross_feature_patterns.values():
            if cross_pattern.target_feature == target_feature:
                if pattern_type and cross_pattern.pattern_type != pattern_type:
                    continue
                if cross_pattern.transfer_confidence >= min_confidence:
                    patterns.append(cross_pattern)

        # Sort by transfer confidence
        patterns.sort(key=lambda p: p.transfer_confidence, reverse=True)
        return patterns

    async def apply_shared_knowledge(
        self, knowledge_id: str, context: Dict[str, Any], user_id: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any], float]:
        """
        Apply shared knowledge in a new context

        Args:
            knowledge_id: ID of the shared knowledge to apply
            context: Current context for application
            user_id: Optional user ID for tracking

        Returns:
            Tuple of (success, result_data, confidence)
        """
        if knowledge_id not in self.shared_knowledge:
            return False, {}, 0.0

        shared_knowledge = self.shared_knowledge[knowledge_id]

        try:
            # Apply knowledge based on sharing type
            if shared_knowledge.sharing_type == KnowledgeSharingType.PATTERN_TRANSFER:
                result = await self._apply_pattern_knowledge(shared_knowledge, context)
            elif shared_knowledge.sharing_type == KnowledgeSharingType.QUERY_ENHANCEMENT:
                result = await self._apply_query_knowledge(shared_knowledge, context)
            elif shared_knowledge.sharing_type == KnowledgeSharingType.WORKFLOW_OPTIMIZATION:
                result = await self._apply_workflow_knowledge(shared_knowledge, context)
            else:
                result = {"success": False, "error": "Unknown sharing type"}

            # Update usage statistics
            shared_knowledge.usage_count += 1
            shared_knowledge.last_used = datetime.now()

            # Track success for confidence calculation
            success = result.get("success", False)
            if success:
                shared_knowledge.success_rate = (
                    shared_knowledge.success_rate * (shared_knowledge.usage_count - 1) + 1.0
                ) / shared_knowledge.usage_count
            else:
                shared_knowledge.success_rate = (
                    shared_knowledge.success_rate * (shared_knowledge.usage_count - 1) + 0.0
                ) / shared_knowledge.usage_count

            # Update confidence based on success rate
            shared_knowledge.confidence = min(1.0, shared_knowledge.success_rate * 0.8 + 0.2)

            return success, result, shared_knowledge.confidence

        except Exception as e:
            logger.error(f"Failed to apply shared knowledge {knowledge_id}: {e}")
            return False, {"error": str(e)}, 0.0

    async def _apply_pattern_knowledge(
        self, shared_knowledge: SharedKnowledge, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply pattern knowledge"""
        pattern_data = shared_knowledge.knowledge_data
        pattern_type = pattern_data.get("pattern_type", "unknown")

        return {
            "success": True,
            "pattern_type": pattern_type,
            "pattern_data": pattern_data,
            "confidence": shared_knowledge.confidence,
            "knowledge_id": shared_knowledge.knowledge_id,
        }

    async def _apply_query_knowledge(
        self, shared_knowledge: SharedKnowledge, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply query knowledge"""
        query_template = shared_knowledge.knowledge_data.get("query_template", "")
        parameters = shared_knowledge.knowledge_data.get("parameters", {})

        try:
            # Apply parameters to template
            query = query_template.format(**parameters)
            return {
                "success": True,
                "query": query,
                "confidence": shared_knowledge.confidence,
                "knowledge_id": shared_knowledge.knowledge_id,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to format query: {e}",
                "knowledge_id": shared_knowledge.knowledge_id,
            }

    async def _apply_workflow_knowledge(
        self, shared_knowledge: SharedKnowledge, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply workflow knowledge"""
        workflow_steps = shared_knowledge.knowledge_data.get("workflow_steps", [])
        conditions = shared_knowledge.knowledge_data.get("conditions", {})

        try:
            # Check conditions
            conditions_met = True
            for condition, value in conditions.items():
                if context.get(condition) != value:
                    conditions_met = False
                    break

            if not conditions_met:
                return {
                    "success": False,
                    "error": "Workflow conditions not met",
                    "knowledge_id": shared_knowledge.knowledge_id,
                }

            return {
                "success": True,
                "workflow_steps": workflow_steps,
                "confidence": shared_knowledge.confidence,
                "knowledge_id": shared_knowledge.knowledge_id,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to apply workflow knowledge: {e}",
                "knowledge_id": shared_knowledge.knowledge_id,
            }

    async def provide_knowledge_feedback(
        self,
        knowledge_id: str,
        feedback_score: float,
        user_id: Optional[str] = None,
        feedback_text: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Provide feedback on shared knowledge effectiveness

        Args:
            knowledge_id: ID of the shared knowledge
            feedback_score: Score from -1.0 to 1.0
            user_id: Optional user ID
            feedback_text: Optional text feedback
            context: Optional context

        Returns:
            True if feedback was recorded successfully
        """
        if knowledge_id not in self.shared_knowledge:
            return False

        shared_knowledge = self.shared_knowledge[knowledge_id]

        # Update feedback score
        shared_knowledge.feedback_score = feedback_score

        # Adjust confidence based on feedback
        if feedback_score > 0:
            shared_knowledge.confidence = min(1.0, shared_knowledge.confidence + 0.1)
        elif feedback_score < 0:
            shared_knowledge.confidence = max(0.0, shared_knowledge.confidence - 0.1)

        logger.info(f"Feedback recorded for shared knowledge {knowledge_id}: {feedback_score}")
        return True

    async def get_knowledge_sharing_stats(self) -> Dict[str, Any]:
        """Get knowledge sharing statistics"""
        total_shared = len(self.shared_knowledge)
        total_patterns = len(self.cross_feature_patterns)

        # Feature distribution
        source_counts = {}
        target_counts = {}
        for shared in self.shared_knowledge.values():
            source_counts[shared.source_feature] = source_counts.get(shared.source_feature, 0) + 1
            target_counts[shared.target_feature] = target_counts.get(shared.target_feature, 0) + 1

        # Sharing type distribution
        type_counts = {}
        for shared in self.shared_knowledge.values():
            sharing_type = shared.sharing_type.value
            type_counts[sharing_type] = type_counts.get(sharing_type, 0) + 1

        # Average confidence
        avg_confidence = (
            sum(k.confidence for k in self.shared_knowledge.values()) / total_shared
            if total_shared > 0
            else 0.0
        )

        return {
            "total_shared_knowledge": total_shared,
            "total_cross_feature_patterns": total_patterns,
            "source_feature_distribution": source_counts,
            "target_feature_distribution": target_counts,
            "sharing_type_distribution": type_counts,
            "average_confidence": avg_confidence,
        }


# Convenience functions for easy integration
async def get_cross_feature_service(
    knowledge_service: KnowledgeGraphService,
    pattern_service: PatternRecognitionService,
    learning_loop: QueryLearningLoop,
) -> CrossFeatureKnowledgeService:
    """Get or create a cross-feature knowledge service instance"""
    return CrossFeatureKnowledgeService(knowledge_service, pattern_service, learning_loop)



if __name__ == "__main__":
    # Test the cross-feature knowledge service
    async def test():
        print("Cross-Feature Knowledge Service - Test Mode")
        print("This service requires KnowledgeGraphService and PatternRecognitionService instances")
        print("Use get_cross_feature_service() to create a proper instance")

    asyncio.run(test())
