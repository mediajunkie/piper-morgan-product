"""
Learning Handler - Database-Backed Pattern Learning

Real-time pattern detection and application using database persistence.
Implements Basic Auto-Learning (Issue #300 - CORE-ALPHA-LEARNING-BASIC).

Architecture:
- Database-backed (uses LearnedPattern model)
- Async operations for performance
- Confidence-based suggestions (>0.7 threshold)
- Pattern similarity detection (no duplicates)

Issue #300: CORE-ALPHA-LEARNING-BASIC - Foundation Stone #1
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

import structlog
from sqlalchemy import String, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import LearnedPattern
from services.shared_types import IntentCategory, PatternType

logger = structlog.get_logger(__name__)


class LearningHandler:
    """
    Database-backed learning handler for real-time pattern detection.

    Captures user actions, detects patterns, updates confidence based on
    outcomes, and suggests high-confidence patterns.

    Issue #300: CORE-ALPHA-LEARNING-BASIC - Level 1 Basic Auto-Learning
    """

    # Confidence thresholds (from gameplan)
    SUGGESTION_THRESHOLD = 0.7  # Show to user
    AUTOMATION_THRESHOLD = 0.9  # Apply automatically (future)
    DISABLE_THRESHOLD = 0.3  # Turn off pattern

    # Similarity threshold for pattern matching
    SIMILARITY_THRESHOLD = 0.8

    def __init__(self):
        """Initialize learning handler"""
        self.logger = logger.bind(component="learning_handler")
        self.logger.info("LearningHandler initialized (database-backed)")

    async def capture_action(
        self,
        user_id: UUID,
        action_type: IntentCategory,
        context: Dict[str, Any],
        session: AsyncSession,
    ) -> Optional[UUID]:
        """
        Capture user action for pattern learning.

        Finds similar patterns or creates new one. Updates usage count
        and last_used_at timestamp.

        Args:
            user_id: User performing the action
            action_type: Intent category (from IntentCategory enum)
            context: Action context (intent, input, etc.)
            session: Database session

        Returns:
            Pattern ID if pattern found/created, None if error

        Performance Target: <10ms
        """
        start_time = datetime.now(timezone.utc)

        try:
            # Extract pattern features
            pattern_data = {
                "action_type": action_type.value,
                "context": context,
                "timestamp": start_time.isoformat(),
            }

            # Determine pattern type from action
            pattern_type = self._determine_pattern_type(action_type)

            # Find similar pattern
            similar_pattern = await self.find_similar_pattern(
                user_id=user_id,
                pattern_data=pattern_data,
                session=session,
            )

            if similar_pattern:
                # Update existing pattern
                similar_pattern.usage_count += 1
                similar_pattern.last_used_at = start_time
                similar_pattern.updated_at = start_time
                pattern_id = similar_pattern.id

                self.logger.info(
                    "Updated existing pattern",
                    pattern_id=str(pattern_id),
                    usage_count=similar_pattern.usage_count,
                )
            else:
                # Create new pattern
                new_pattern = LearnedPattern(
                    id=uuid4(),
                    user_id=user_id,
                    pattern_type=pattern_type,
                    pattern_data=pattern_data,
                    confidence=0.5,  # Start neutral
                    usage_count=1,
                    success_count=0,
                    failure_count=0,
                    enabled=True,
                    last_used_at=start_time,
                )
                session.add(new_pattern)
                pattern_id = new_pattern.id

                self.logger.info(
                    "Created new pattern",
                    pattern_id=str(pattern_id),
                    pattern_type=pattern_type.value,
                )

            await session.commit()

            # Performance monitoring
            elapsed_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000
            self.logger.debug(
                "Pattern capture complete",
                elapsed_ms=round(elapsed_ms, 2),
                pattern_id=str(pattern_id),
            )

            return pattern_id

        except Exception as e:
            self.logger.error(
                "Pattern capture failed",
                error=str(e),
                user_id=str(user_id),
                action_type=action_type.value,
            )
            await session.rollback()
            return None

    async def record_outcome(
        self,
        user_id: UUID,
        pattern_id: UUID,
        success: bool,
        session: AsyncSession,
    ) -> bool:
        """
        Record outcome of pattern application and update confidence.

        Updates success/failure counts and recalculates confidence using
        the formula from the LearnedPattern model.

        Args:
            user_id: User who performed the action
            pattern_id: Pattern that was applied
            success: Whether the action succeeded
            session: Database session

        Returns:
            True if outcome recorded successfully, False otherwise

        Performance Target: <5ms
        """
        start_time = datetime.now(timezone.utc)

        try:
            # Find the pattern
            result = await session.execute(
                select(LearnedPattern).where(
                    and_(
                        LearnedPattern.id == pattern_id,
                        LearnedPattern.user_id == user_id,
                    )
                )
            )
            pattern = result.scalar_one_or_none()

            if not pattern:
                self.logger.warning(
                    "Pattern not found for outcome recording",
                    pattern_id=str(pattern_id),
                    user_id=str(user_id),
                )
                return False

            # Update success/failure counts
            if success:
                pattern.success_count += 1
            else:
                pattern.failure_count += 1

            # Recalculate confidence using model method
            pattern.update_confidence()

            await session.commit()

            # Performance monitoring
            elapsed_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

            self.logger.info(
                "Outcome recorded",
                pattern_id=str(pattern_id),
                success=success,
                confidence=round(pattern.confidence, 2),
                enabled=pattern.enabled,
                elapsed_ms=round(elapsed_ms, 2),
            )

            return True

        except Exception as e:
            self.logger.error(
                "Outcome recording failed",
                error=str(e),
                pattern_id=str(pattern_id),
                user_id=str(user_id),
            )
            await session.rollback()
            return False

    async def get_suggestions(
        self,
        user_id: UUID,
        context: Dict[str, Any],
        session: AsyncSession,
    ) -> List[Dict[str, Any]]:
        """
        Get high-confidence pattern suggestions for current context.

        Returns patterns with confidence >= SUGGESTION_THRESHOLD (0.7)
        that are enabled and match the current context.

        Args:
            user_id: User requesting suggestions
            context: Current context (intent, input, etc.)
            session: Database session

        Returns:
            List of suggestion dicts with pattern_id, confidence, pattern_data

        Performance Target: <1ms (cached)
        """
        start_time = datetime.now(timezone.utc)

        try:
            # Query high-confidence patterns for user
            result = await session.execute(
                select(LearnedPattern)
                .where(
                    and_(
                        LearnedPattern.user_id == user_id,
                        LearnedPattern.confidence >= self.SUGGESTION_THRESHOLD,
                        LearnedPattern.enabled == True,  # noqa: E712
                    )
                )
                .order_by(LearnedPattern.confidence.desc())
                .limit(5)  # Top 5 suggestions
            )
            patterns = result.scalars().all()

            # Format suggestions
            suggestions = []
            for pattern in patterns:
                suggestions.append(
                    {
                        "pattern_id": str(pattern.id),
                        "confidence": round(pattern.confidence, 2),
                        "pattern_type": pattern.pattern_type.value,
                        "pattern_data": pattern.pattern_data,
                        "usage_count": pattern.usage_count,
                        "auto_triggered": False,  # Phase 4: Regular (reactive) suggestions
                    }
                )

            # Performance monitoring
            elapsed_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

            self.logger.debug(
                "Suggestions retrieved",
                count=len(suggestions),
                elapsed_ms=round(elapsed_ms, 2),
            )

            return suggestions

        except Exception as e:
            self.logger.error(
                "Suggestion retrieval failed",
                error=str(e),
                user_id=str(user_id),
            )
            return []

    async def get_automation_patterns(
        self,
        user_id: UUID,
        context: Optional[Dict[str, Any]] = None,
        min_confidence: float = 0.9,
        limit: int = 3,
        # #1438: REQUIRED — the old Optional=None default was a lying signature
        # (the body dereferences it unconditionally; None = AttributeError).
        session: AsyncSession = None,  # type: ignore[assignment]
    ) -> List[LearnedPattern]:
        """
        Get patterns eligible for proactive application (Phase 4).

        Similar to get_suggestions but with higher confidence threshold
        and context matching for proactive triggering.

        Args:
            user_id: User to get patterns for
            context: Current context for matching
            min_confidence: Minimum confidence (default 0.9 for automation)
            limit: Maximum patterns to return
            session: Database session

        Returns:
            List of high-confidence LearnedPattern objects that match context
        """
        # Query high-confidence enabled patterns
        result = await session.execute(
            select(LearnedPattern)
            .where(
                and_(
                    LearnedPattern.user_id == user_id,
                    LearnedPattern.confidence >= min_confidence,
                    LearnedPattern.enabled == True,  # noqa: E712
                )
            )
            .order_by(LearnedPattern.confidence.desc())
            .limit(limit)
        )

        patterns = result.scalars().all()

        # Filter by context if provided
        if context:
            from services.learning.context_matcher import ContextMatcher

            matched_patterns = []

            for pattern in patterns:
                pattern_context = pattern.pattern_data.get("context", {})
                if await ContextMatcher.matches(pattern_context, context):
                    matched_patterns.append(pattern)

            return matched_patterns

        return list(patterns)

    async def find_similar_pattern(
        self,
        user_id: UUID,
        pattern_data: Dict[str, Any],
        session: AsyncSession,
    ) -> Optional[LearnedPattern]:
        """
        Find similar pattern to avoid duplicates.

        Uses simple similarity matching based on action_type.
        More sophisticated matching can be added in future.

        Args:
            user_id: User to search patterns for
            pattern_data: Pattern data to match against
            session: Database session

        Returns:
            Similar pattern if found, None otherwise
        """
        try:
            action_type = pattern_data.get("action_type")
            if not action_type:
                return None

            # Find patterns with same action_type for this user
            # For now, simple match on action_type
            # Future: More sophisticated similarity (cosine, jaccard, etc.)
            result = await session.execute(
                select(LearnedPattern)
                .where(
                    and_(
                        LearnedPattern.user_id == user_id,
                        # #1438: MUST be ->> (returns text). The old `->` returned
                        # JSONB, whose String cast renders the value WITH quotes
                        # ('"execution"') — never equal to the plain string, so
                        # similarity never matched and every capture created a new
                        # pattern (the dead-upsert facet of the dead learning loop).
                        # The action_type leaf is plaintext by design (EncryptedJSON
                        # leaf-split whitelist) so server-side matching is supported.
                        LearnedPattern.pattern_data.op("->>")("action_type")
                        == action_type,
                        LearnedPattern.enabled == True,  # noqa: E712
                    )
                )
                .order_by(LearnedPattern.last_used_at.desc())
                .limit(1)
            )
            pattern = result.scalar_one_or_none()

            if pattern:
                self.logger.debug(
                    "Similar pattern found",
                    pattern_id=str(pattern.id),
                    confidence=round(pattern.confidence, 2),
                )

            return pattern

        except Exception as e:
            self.logger.error(
                "Similarity search failed",
                error=str(e),
                user_id=str(user_id),
            )
            return None

    def _determine_pattern_type(self, action_type: IntentCategory) -> PatternType:
        """
        Determine PatternType from IntentCategory.

        Maps intent categories to pattern types for classification.

        Args:
            action_type: Intent category from orchestration

        Returns:
            PatternType enum value
        """
        # Simple mapping for now
        # Future: More sophisticated pattern type detection
        mapping = {
            IntentCategory.EXECUTION: PatternType.COMMAND_SEQUENCE,
            IntentCategory.ANALYSIS: PatternType.USER_WORKFLOW,
            IntentCategory.SYNTHESIS: PatternType.USER_WORKFLOW,
            IntentCategory.STRATEGY: PatternType.USER_WORKFLOW,
            IntentCategory.LEARNING: PatternType.USER_WORKFLOW,
            IntentCategory.QUERY: PatternType.CONTEXT_BASED,
            IntentCategory.CONVERSATION: PatternType.PREFERENCE,
            IntentCategory.IDENTITY: PatternType.PREFERENCE,
            IntentCategory.TEMPORAL: PatternType.TIME_BASED,
            IntentCategory.STATUS: PatternType.CONTEXT_BASED,
            IntentCategory.PRIORITY: PatternType.CONTEXT_BASED,
            IntentCategory.GUIDANCE: PatternType.USER_WORKFLOW,
            IntentCategory.UNKNOWN: PatternType.USER_WORKFLOW,
        }

        return mapping.get(action_type, PatternType.USER_WORKFLOW)
