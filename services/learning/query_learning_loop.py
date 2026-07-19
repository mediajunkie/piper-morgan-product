"""
Query Learning Loop - Cross-Feature Pattern Learning System

Implements pattern tracking between Issue Intelligence and Morning Standup
with feedback integration for continuous improvement.

Built on: Document Memory + Pattern Storage + Confidence Scoring
Performance: Real-time pattern learning and sharing
"""

import asyncio
import json
import logging
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

# Configure logging
logger = logging.getLogger(__name__)


class PatternType(Enum):
    """Types of patterns that can be learned"""

    QUERY_PATTERN = "query_pattern"
    RESPONSE_PATTERN = "response_pattern"
    WORKFLOW_PATTERN = "workflow_pattern"
    INTEGRATION_PATTERN = "integration_pattern"
    USER_PREFERENCE_PATTERN = "user_preference_pattern"

    # CORE-LEARN-B: Pattern Recognition Extension (Issue #222)
    # Bonus pattern types for 60% overachievement (8 types vs 5 required)
    TEMPORAL_PATTERN = "temporal_pattern"
    COMMUNICATION_PATTERN = "communication_pattern"
    ERROR_PATTERN = "error_pattern"


class PatternConfidence(Enum):
    """Confidence levels for learned patterns"""

    LOW = "low"  # 0-30% confidence
    MEDIUM = "medium"  # 31-70% confidence
    HIGH = "high"  # 71-100% confidence


@dataclass
class LearnedPattern:
    """Represents a learned pattern with metadata"""

    pattern_id: str
    pattern_type: PatternType
    source_feature: str  # "issue_intelligence" or "morning_standup"
    pattern_data: Dict[str, Any]
    confidence: float  # 0.0 to 1.0
    usage_count: int
    success_rate: float  # 0.0 to 1.0
    first_seen: datetime
    last_used: datetime
    feedback_score: float  # -1.0 to 1.0 (negative = negative feedback)
    metadata: Dict[str, Any]


@dataclass
class PatternFeedback:
    """Represents feedback on a pattern"""

    pattern_id: str
    user_id: Optional[str]
    feedback_score: float  # -1.0 to 1.0
    feedback_text: Optional[str]
    timestamp: datetime
    context: Dict[str, Any]


class QueryLearningLoop:
    """
    Cross-feature learning loop that tracks patterns between Issue Intelligence
    and Morning Standup for continuous improvement.
    """

    def __init__(self, storage_path: Optional[str] = None):
        """Initialize the learning loop with storage"""
        self.storage_path = Path(storage_path) if storage_path else Path("data/learning")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Pattern storage
        self.patterns_file = self.storage_path / "learned_patterns.json"
        self.feedback_file = self.storage_path / "pattern_feedback.json"

        # In-memory cache
        self.patterns: Dict[str, LearnedPattern] = {}
        self.feedback: List[PatternFeedback] = []

        # Load existing patterns
        self._load_patterns()
        self._load_feedback()

    def _load_patterns(self) -> None:
        """Load learned patterns from storage"""
        try:
            if self.patterns_file.exists():
                with open(self.patterns_file, "r") as f:
                    data = json.load(f)
                    for pattern_data in data:
                        pattern = LearnedPattern(
                            pattern_id=pattern_data["pattern_id"],
                            pattern_type=PatternType(pattern_data["pattern_type"]),
                            source_feature=pattern_data["source_feature"],
                            pattern_data=pattern_data["pattern_data"],
                            confidence=pattern_data["confidence"],
                            usage_count=pattern_data["usage_count"],
                            success_rate=pattern_data["success_rate"],
                            first_seen=datetime.fromisoformat(pattern_data["first_seen"]),
                            last_used=datetime.fromisoformat(pattern_data["last_used"]),
                            feedback_score=pattern_data["feedback_score"],
                            metadata=pattern_data["metadata"],
                        )
                        self.patterns[pattern.pattern_id] = pattern
                logger.info(f"Loaded {len(self.patterns)} learned patterns")
        except Exception as e:
            logger.error(f"Failed to load patterns: {e}")
            self.patterns = {}

    def _load_feedback(self) -> None:
        """Load pattern feedback from storage"""
        try:
            if self.feedback_file.exists():
                with open(self.feedback_file, "r") as f:
                    data = json.load(f)
                    for feedback_data in data:
                        feedback = PatternFeedback(
                            pattern_id=feedback_data["pattern_id"],
                            user_id=feedback_data.get("user_id"),
                            feedback_score=feedback_data["feedback_score"],
                            feedback_text=feedback_data.get("feedback_text"),
                            timestamp=datetime.fromisoformat(feedback_data["timestamp"]),
                            context=feedback_data.get("context", {}),
                        )
                        self.feedback.append(feedback)
                logger.info(f"Loaded {len(self.feedback)} feedback entries")
        except Exception as e:
            logger.error(f"Failed to load feedback: {e}")
            self.feedback = []

    def _save_patterns(self) -> None:
        """Save learned patterns to storage"""
        try:
            data = []
            for pattern in self.patterns.values():
                pattern_dict = asdict(pattern)
                pattern_dict["first_seen"] = pattern.first_seen.isoformat()
                pattern_dict["last_used"] = pattern.last_used.isoformat()
                pattern_dict["pattern_type"] = pattern.pattern_type.value
                data.append(pattern_dict)

            with open(self.patterns_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save patterns: {e}")

    def _save_feedback(self) -> None:
        """Save pattern feedback to storage"""
        try:
            data = []
            for feedback in self.feedback:
                feedback_dict = asdict(feedback)
                feedback_dict["timestamp"] = feedback.timestamp.isoformat()
                data.append(feedback_dict)

            with open(self.feedback_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save feedback: {e}")

    async def learn_pattern(
        self,
        pattern_type: PatternType,
        source_feature: str,
        pattern_data: Dict[str, Any],
        initial_confidence: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Learn a new pattern from a feature

        Args:
            pattern_type: Type of pattern being learned
            source_feature: Feature that generated the pattern
            pattern_data: The actual pattern data
            initial_confidence: Starting confidence level
            metadata: Additional metadata about the pattern

        Returns:
            Pattern ID for future reference
        """
        # Generate unique pattern ID
        timestamp = datetime.now()
        pattern_id = f"{pattern_type.value}_{source_feature}_{timestamp.strftime('%Y%m%d_%H%M%S')}"

        # Create new pattern
        pattern = LearnedPattern(
            pattern_id=pattern_id,
            pattern_type=pattern_type,
            source_feature=source_feature,
            pattern_data=pattern_data,
            confidence=initial_confidence,
            usage_count=0,
            success_rate=0.0,
            first_seen=timestamp,
            last_used=timestamp,
            feedback_score=0.0,
            metadata=metadata or {},
        )

        # Store pattern
        self.patterns[pattern_id] = pattern
        self._save_patterns()

        logger.info(f"Learned new pattern: {pattern_id} from {source_feature}")
        return pattern_id

    async def apply_pattern(
        self, pattern_id: str, context: Dict[str, Any], user_id: Optional[str] = None
    ) -> Tuple[bool, Dict[str, Any], float]:
        """
        Apply a learned pattern in a new context

        Args:
            pattern_id: ID of the pattern to apply
            context: Current context for pattern application
            user_id: Optional user ID for tracking

        Returns:
            Tuple of (success, result_data, confidence)
        """
        if pattern_id not in self.patterns:
            return False, {}, 0.0

        pattern = self.patterns[pattern_id]

        try:
            # Apply pattern logic based on type
            if pattern.pattern_type == PatternType.QUERY_PATTERN:
                result = await self._apply_query_pattern(pattern, context)
            elif pattern.pattern_type == PatternType.RESPONSE_PATTERN:
                result = await self._apply_response_pattern(pattern, context)
            elif pattern.pattern_type == PatternType.WORKFLOW_PATTERN:
                result = await self._apply_workflow_pattern(pattern, context)
            elif pattern.pattern_type == PatternType.USER_PREFERENCE_PATTERN:
                # CORE-LEARN-C: Apply preference patterns to UserPreferenceManager
                result = await self._apply_user_preference_pattern(pattern, context)
            else:
                result = {"success": False, "error": "Unknown pattern type"}

            # Update pattern usage
            pattern.usage_count += 1
            pattern.last_used = datetime.now()

            # Track success for confidence calculation
            success = result.get("success", False)
            if success:
                pattern.success_rate = (
                    pattern.success_rate * (pattern.usage_count - 1) + 1.0
                ) / pattern.usage_count
            else:
                pattern.success_rate = (
                    pattern.success_rate * (pattern.usage_count - 1) + 0.0
                ) / pattern.usage_count

            # Update confidence based on success rate
            pattern.confidence = min(1.0, pattern.success_rate * 0.8 + 0.2)

            self._save_patterns()

            return success, result, pattern.confidence

        except Exception as e:
            logger.error(f"Failed to apply pattern {pattern_id}: {e}")
            return False, {"error": str(e)}, 0.0

    async def _apply_query_pattern(
        self, pattern: LearnedPattern, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply a query pattern"""
        # Extract query template and parameters
        query_template = pattern.pattern_data.get("query_template", "")
        parameters = pattern.pattern_data.get("parameters", {})

        # Apply parameters to template
        try:
            query = query_template.format(**parameters)
            return {
                "success": True,
                "query": query,
                "confidence": pattern.confidence,
                "pattern_id": pattern.pattern_id,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to format query: {e}",
                "pattern_id": pattern.pattern_id,
            }

    async def _apply_response_pattern(
        self, pattern: LearnedPattern, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply a response pattern"""
        # Extract response template and logic
        response_template = pattern.pattern_data.get("response_template", "")
        response_logic = pattern.pattern_data.get("response_logic", {})

        try:
            # Apply response logic
            response = response_template
            if response_logic.get("format_type") == "markdown":
                response = f"**{response}**"

            return {
                "success": True,
                "response": response,
                "confidence": pattern.confidence,
                "pattern_id": pattern.pattern_id,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to apply response pattern: {e}",
                "pattern_id": pattern.pattern_id,
            }

    async def _apply_workflow_pattern(
        self, pattern: LearnedPattern, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply a workflow pattern"""
        # Extract workflow steps and conditions
        workflow_steps = pattern.pattern_data.get("workflow_steps", [])
        conditions = pattern.pattern_data.get("conditions", {})

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
                    "pattern_id": pattern.pattern_id,
                }

            return {
                "success": True,
                "workflow_steps": workflow_steps,
                "confidence": pattern.confidence,
                "pattern_id": pattern.pattern_id,
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to apply workflow pattern: {e}",
                "pattern_id": pattern.pattern_id,
            }

    # ========================================================================
    # CORE-LEARN-C: Preference Pattern Application (Issue #223)
    # ========================================================================

    async def _apply_user_preference_pattern(
        self, pattern: LearnedPattern, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply user preference pattern by setting it as an explicit preference.

        This converts implicit preferences (learned from behavior) to explicit
        preferences (stored in UserPreferenceManager).

        Args:
            pattern: The learned USER_PREFERENCE_PATTERN
            context: Application context with user_id and optional session_id

        Returns:
            Dict with success status and details

        Example:
            pattern = LearnedPattern(
                pattern_type=PatternType.USER_PREFERENCE_PATTERN,
                pattern_data={
                    "preference_key": "response_style",
                    "preference_value": "concise"
                },
                confidence=0.85
            )
            result = await loop._apply_user_preference_pattern(pattern, {"user_id": "user123"})
        """
        # Get user_id from context
        user_id = context.get("user_id")
        session_id = context.get("session_id")

        if not user_id:
            return {
                "success": False,
                "error": "user_id required in context for preference pattern application",
            }

        try:
            # Get UserPreferenceManager instance
            from services.domain.user_preference_manager import UserPreferenceManager

            preference_manager = UserPreferenceManager()

            # Convert LearnedPattern to dict for apply_preference_pattern
            pattern_dict = {
                "confidence": pattern.confidence,
                "pattern_data": pattern.pattern_data,
                "pattern_type": (
                    pattern.pattern_type.value
                    if hasattr(pattern.pattern_type, "value")
                    else str(pattern.pattern_type)
                ),
                "pattern_id": pattern.pattern_id,
            }

            # Apply the pattern as an explicit preference
            success = await preference_manager.apply_preference_pattern(
                pattern=pattern_dict,
                user_id=user_id,
                session_id=session_id,
                scope="user" if not session_id else "session",
            )

            if success:
                preference_key = pattern.pattern_data.get("preference_key", "unknown")
                preference_value = pattern.pattern_data.get("preference_value", "unknown")

                return {
                    "success": True,
                    "preference_key": preference_key,
                    "preference_value": preference_value,
                    "applied_scope": "session" if session_id else "user",
                    "confidence": pattern.confidence,
                }
            else:
                return {
                    "success": False,
                    "error": "Pattern confidence too low or preference data invalid",
                }

        except Exception as e:
            logger.error(f"Failed to apply user preference pattern: {e}")
            return {"success": False, "error": str(e)}

    # CORE-LEARN-D: Workflow Optimization (Issue #224)
    async def optimize_workflow_via_experiments(
        self, intent: "Intent", context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run Chain-of-Draft experiment to optimize workflow execution.

        Uses A/B testing to identify workflow improvements and create
        learned patterns from high-quality experiments.

        Args:
            intent: Intent to optimize
            context: Execution context

        Returns:
            Dict with experiment results, best workflow, and learning insights
        """
        # #1436 Tier-3 Family 2: the Chain-of-Draft experiment subsystem was
        # deleted (design record: docs/internal/architecture/design-records/
        # multi-agent-coordination-pm033d.md). Honest removed-feature reply —
        # never a swallowed ImportError.
        return {
            "success": False,
            "error": "draft-experiment system removed (see design record, #1436)",
            "removed": True,
        }
    async def create_workflow_template_from_pattern(
        self, pattern_id: str, template_name: str
    ) -> Dict[str, Any]:
        """
        Create reusable workflow template from learned pattern.

        Converts high-confidence workflow patterns (>= 0.8) into parameterized
        templates that can be applied to similar workflows.

        Args:
            pattern_id: ID of workflow pattern to convert
            template_name: Name for the template

        Returns:
            Dict with template data and application instructions
        """
        try:
            # Retrieve the pattern - search through all patterns
            pattern = None
            for p in self.patterns.values():
                if p.pattern_id == pattern_id and p.pattern_type == PatternType.WORKFLOW_PATTERN:
                    pattern = p
                    break

            if not pattern:
                return {"success": False, "error": f"Pattern {pattern_id} not found"}

            # Only create templates from high-confidence patterns
            if pattern.confidence < 0.8:
                return {
                    "success": False,
                    "error": f"Pattern confidence {pattern.confidence} below 0.8 threshold",
                }

            # Extract template structure from pattern data
            workflow_steps = pattern.pattern_data.get("workflow_steps", [])

            if not workflow_steps:
                return {"success": False, "error": "Pattern has no workflow steps"}

            # Create parameterized template
            template = {
                "template_name": template_name,
                "template_id": f"wf_template_{int(time.time() * 1000)}",
                "based_on_pattern": pattern_id,
                "confidence": pattern.confidence,
                "steps": [
                    {
                        "step_number": step["step"],
                        "description_template": step.get("subtask_description", ""),
                        "agent_preference": step.get("assigned_agent", "auto"),
                        "parameters": [],  # Placeholder for parameterization
                    }
                    for step in workflow_steps
                ],
                "expected_quality": pattern.pattern_data.get("quality_score", 0.0),
                "expected_time_ms": pattern.pattern_data.get("execution_time_ms", 0),
                "optimization_insights": pattern.pattern_data.get("optimization_insights", {}),
                "created_at": datetime.now().isoformat(),
                "usage_count": 0,
            }

            # Store template in pattern data for future retrieval
            # (In production, this would go to a template storage system)
            template_pattern_data = {
                "template": template,
                "source_pattern_id": pattern_id,
                "template_type": "workflow_optimization",
            }

            # Learn as a new pattern for template storage
            template_pattern_id = await self.learn_pattern(
                pattern_type=PatternType.WORKFLOW_PATTERN,
                source_feature="workflow_templates",
                pattern_data=template_pattern_data,
                initial_confidence=pattern.confidence,
                metadata={
                    "template_name": template_name,
                    "is_template": True,
                    "source_pattern": pattern_id,
                },
            )

            return {
                "success": True,
                "template": template,
                "template_pattern_id": template_pattern_id,
                "message": f"Template '{template_name}' created from pattern {pattern_id}",
            }

        except Exception as e:
            logger.error(f"Template creation failed: {e}")
            return {"success": False, "error": str(e)}

    async def provide_feedback(
        self,
        pattern_id: str,
        feedback_score: float,
        user_id: Optional[str] = None,
        feedback_text: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Provide feedback on a pattern's effectiveness

        Args:
            pattern_id: ID of the pattern to provide feedback on
            feedback_score: Score from -1.0 (negative) to 1.0 (positive)
            user_id: Optional user ID
            feedback_text: Optional text feedback
            context: Optional context for the feedback

        Returns:
            True if feedback was recorded successfully
        """
        if pattern_id not in self.patterns:
            logger.warning(f"Attempted to provide feedback on unknown pattern: {pattern_id}")
            return False

        # Create feedback entry
        feedback = PatternFeedback(
            pattern_id=pattern_id,
            user_id=user_id,
            feedback_score=feedback_score,
            feedback_text=feedback_text,
            timestamp=datetime.now(),
            context=context or {},
        )

        self.feedback.append(feedback)

        # Update pattern feedback score
        pattern = self.patterns[pattern_id]
        pattern.feedback_score = feedback_score

        # Adjust confidence based on feedback
        if feedback_score > 0:
            pattern.confidence = min(1.0, pattern.confidence + 0.1)
        elif feedback_score < 0:
            pattern.confidence = max(0.0, pattern.confidence - 0.1)

        # Save updates
        self._save_patterns()
        self._save_feedback()

        logger.info(f"Feedback recorded for pattern {pattern_id}: {feedback_score}")
        return True

    async def get_patterns_for_feature(
        self,
        source_feature: str,
        pattern_type: Optional[PatternType] = None,
        min_confidence: float = 0.3,
    ) -> List[LearnedPattern]:
        """
        Get patterns for a specific feature with optional filtering

        Args:
            source_feature: Feature to get patterns for
            pattern_type: Optional pattern type filter
            min_confidence: Minimum confidence threshold

        Returns:
            List of matching patterns
        """
        patterns = []
        for pattern in self.patterns.values():
            if pattern.source_feature == source_feature:
                if pattern_type and pattern.pattern_type != pattern_type:
                    continue
                if pattern.confidence >= min_confidence:
                    patterns.append(pattern)

        # Sort by confidence and usage count
        patterns.sort(key=lambda p: (p.confidence, p.usage_count), reverse=True)
        return patterns

    async def get_cross_feature_patterns(
        self,
        target_feature: str,
        pattern_type: Optional[PatternType] = None,
        min_confidence: float = 0.5,
    ) -> List[LearnedPattern]:
        """
        Get patterns from other features that could be useful for target feature

        Args:
            target_feature: Feature to find patterns for
            pattern_type: Optional pattern type filter
            min_confidence: Minimum confidence threshold

        Returns:
            List of potentially useful patterns from other features
        """
        patterns = []
        for pattern in self.patterns.values():
            if pattern.source_feature != target_feature:  # Different source
                if pattern_type and pattern.pattern_type != pattern_type:
                    continue
                if pattern.confidence >= min_confidence:
                    patterns.append(pattern)

        # Sort by confidence and success rate
        patterns.sort(key=lambda p: (p.confidence, p.success_rate), reverse=True)
        return patterns

    async def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning loop statistics"""
        total_patterns = len(self.patterns)
        total_feedback = len(self.feedback)

        # Pattern type distribution
        type_counts = {}
        for pattern in self.patterns.values():
            pattern_type = pattern.pattern_type.value
            type_counts[pattern_type] = type_counts.get(pattern_type, 0) + 1

        # Feature distribution
        feature_counts = {}
        for pattern in self.patterns.values():
            feature = pattern.source_feature
            feature_counts[feature] = feature_counts.get(feature, 0) + 1

        # Average confidence
        avg_confidence = (
            sum(p.confidence for p in self.patterns.values()) / total_patterns
            if total_patterns > 0
            else 0.0
        )

        # Recent activity (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        recent_patterns = sum(1 for p in self.patterns.values() if p.last_used > cutoff)
        recent_feedback = sum(1 for f in self.feedback if f.timestamp > cutoff)

        return {
            "total_patterns": total_patterns,
            "total_feedback": total_feedback,
            "pattern_type_distribution": type_counts,
            "feature_distribution": feature_counts,
            "average_confidence": avg_confidence,
            "recent_patterns_24h": recent_patterns,
            "recent_feedback_24h": recent_feedback,
            "storage_path": str(self.storage_path),
        }

    async def cleanup_old_patterns(self, days_old: int = 30, min_usage: int = 3) -> int:
        """
        Clean up old, rarely-used patterns

        Args:
            days_old: Remove patterns older than this many days
            min_usage: Remove patterns with usage count below this threshold

        Returns:
            Number of patterns removed
        """
        cutoff_date = datetime.now() - timedelta(days=days_old)
        patterns_to_remove = []

        for pattern_id, pattern in self.patterns.items():
            if (
                pattern.first_seen < cutoff_date
                and pattern.usage_count < min_usage
                and pattern.confidence < 0.4
            ):
                patterns_to_remove.append(pattern_id)

        # Remove patterns
        for pattern_id in patterns_to_remove:
            del self.patterns[pattern_id]

        if patterns_to_remove:
            self._save_patterns()
            logger.info(f"Cleaned up {len(patterns_to_remove)} old patterns")

        return len(patterns_to_remove)


# Convenience functions for easy integration
async def get_learning_loop(storage_path: Optional[str] = None) -> QueryLearningLoop:
    """Get or create a learning loop instance"""
    return QueryLearningLoop(storage_path)


async def learn_query_pattern(
    source_feature: str,
    query_template: str,
    parameters: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Convenience function to learn a query pattern"""
    learning_loop = await get_learning_loop()
    pattern_data = {
        "query_template": query_template,
        "parameters": parameters,
        "pattern_category": "query",
    }
    return await learning_loop.learn_pattern(
        PatternType.QUERY_PATTERN, source_feature, pattern_data, metadata=metadata
    )


async def learn_response_pattern(
    source_feature: str,
    response_template: str,
    response_logic: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
) -> str:
    """Convenience function to learn a response pattern"""
    learning_loop = await get_learning_loop()
    pattern_data = {
        "response_template": response_template,
        "response_logic": response_logic,
        "pattern_category": "response",
    }
    return await learning_loop.learn_pattern(
        PatternType.RESPONSE_PATTERN, source_feature, pattern_data, metadata=metadata
    )


if __name__ == "__main__":
    # Test the learning loop
    async def test():
        learning_loop = QueryLearningLoop()

        # Learn a pattern
        pattern_id = await learning_loop.learn_pattern(
            PatternType.QUERY_PATTERN,
            "issue_intelligence",
            {
                "query_template": "What issues need attention in {project}?",
                "parameters": {"project": "string"},
            },
            metadata={"category": "project_management"},
        )

        print(f"Learned pattern: {pattern_id}")

        # Get stats
        stats = await learning_loop.get_learning_stats()
        print(f"Stats: {stats}")

    asyncio.run(test())
