"""
Premonition - when and how Piper surfaces insights.

Part of #415 MUX-INTERACT-PREMONITION.

This module provides:
- InsightReadiness: Assessment of whether an insight is ready to surface
- SurfacingContext: Current context for surfacing decisions
- PremonitionService: Orchestrates insight surfacing
- Surfacing frames for gentle, first-person language

Three surfacing modes:
- Pull: User asks "What have you learned?"
- Passive: User navigates to Learning Dashboard
- Push: Piper initiates "Can I share something?"

Push mode has strict gates per D4 spec:
1. Trust Stage 3+ (ESTABLISHED or TRUSTED)
2. Confidence ≥ 0.75
3. Contextually relevant
4. ≥24 hours since last similar push
5. User not in focus mode
"""

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

from services.shared_types import TrustStage

from .composting_models import ExtractedLearning
from .composting_pipeline import InsightJournal, SurfaceableInsight

# =============================================================================
# Surfacing Language Frames
# =============================================================================


SURFACING_FRAMES = {
    "reflection": [
        "Having had some time to reflect, it occurs to me that {insight}",
        "I've been thinking about our work together, and {insight}",
        "Something I've noticed over time: {insight}",
        "Looking back at what we've done, {insight}",
    ],
    "concern": [
        "I'm a little concerned about {insight}",
        "This might be worth considering: {insight}",
        "Something I think we should pay attention to: {insight}",
    ],
    "offer": [
        "Can I share something that might help?",
        "I noticed something that could be useful...",
        "There's something I've been meaning to mention...",
    ],
    "correction": [
        "I think I had something wrong - {insight}",
        "I've realized I may have been mistaken: {insight}",
        "After more thought, I see that {insight}",
    ],
}


# #1194: leading first-person frame fragments that `expression` may already carry
# (from composting_models factories) — stripped before re-framing so a pre-framed
# expression isn't double-framed when wrapped for surfacing.
_LEADING_FRAME_FRAGMENTS = (
    "it occurs to me that ",
    "i've noticed a pattern: ",
    "i've noticed that ",
    "i noticed that ",
    "i think i had something wrong - ",
    "i've realized i may have been mistaken: ",
    "after more thought, i see that ",
    "something i've noticed over time: ",
)


def _strip_leading_frame(text: str) -> str:
    """Strip a known leading first-person frame fragment (case-insensitive) so a
    pre-framed `expression` isn't double-framed when wrapped for surfacing (#1194)."""
    if not text:
        return text
    stripped = text.lstrip()
    low = stripped.lower()
    for frag in _LEADING_FRAME_FRAGMENTS:
        if low.startswith(frag):
            return stripped[len(frag) :]
    return text


def frame_insight_for_surfacing(insight: SurfaceableInsight) -> str:
    """
    Frame an insight in gentle, first-person language.

    Selects appropriate frame based on insight type and
    whether it requires attention.

    Per #1033 (May 3): output is run through the anti-surveillance guardrail
    before return. If the framed string contains forbidden surveillance
    phrasing (e.g., "I've been watching", "Based on my surveillance"), the
    guardrail logs the violation and the function returns a gentle fallback
    ("I don't have anything to share right now.") rather than letting the
    surveillance phrasing reach the user.

    Args:
        insight: The insight to frame

    Returns:
        Framed message ready for display, guardrail-protected
    """
    if insight.learning is None:
        return "I've noticed something that might be helpful."

    learning = insight.learning

    # Select frame category based on learning type
    if learning.learning_type == "correction":
        frames = SURFACING_FRAMES["correction"]
    elif learning.requires_attention:
        frames = SURFACING_FRAMES["concern"]
    else:
        frames = SURFACING_FRAMES["reflection"]

    frame = random.choice(frames)

    # #1194: wrap the BARE description, not `expression`. `expression` is already a
    # first-person frame (composting_models factories build it as
    # "It occurs to me that {description}" / "I've noticed a pattern: {description}"),
    # so framing it again double-frames ("...it occurs to me that It occurs to me
    # that ..."). Prefer description; if only a pre-framed expression exists, strip
    # its leading frame so the surfacing frame doesn't double up.
    content = learning.description or _strip_leading_frame(learning.expression or "")

    framed = frame.format(insight=content)

    # #1033: anti-surveillance guardrail. Strict per Q3 disposition;
    # surveillance-shaped output never reaches the user.
    from services.mux.anti_surveillance import safe_surface

    return safe_surface(framed)


# =============================================================================
# SurfacingContext
# =============================================================================


@dataclass
class SurfacingContext:
    """
    Context for making surfacing decisions.

    Captures the current state needed to decide whether
    and how to surface insights.
    """

    # User and trust
    user_id: str
    trust_stage: TrustStage = TrustStage.NEW

    # Current work context
    active_entities: List[str] = field(default_factory=list)
    topic_tags: List[str] = field(default_factory=list)

    # User state
    user_in_focus_mode: bool = False
    is_catching_up: bool = False  # Reading history, not live
    is_online: bool = True

    # Session state
    suggestions_this_session: int = 0
    last_push_time: Optional[datetime] = None

    def can_receive_push(self) -> bool:
        """Check if user can receive a push insight right now."""
        # Must be at least ESTABLISHED (Stage 3)
        if self.trust_stage < TrustStage.ESTABLISHED:
            return False

        # Not in focus mode
        if self.user_in_focus_mode:
            return False

        # Not catching up on history
        if self.is_catching_up:
            return False

        # Must be online
        if not self.is_online:
            return False

        return True


# =============================================================================
# InsightReadiness
# =============================================================================


@dataclass
class InsightReadiness:
    """
    Assessment of whether an insight is ready to surface.

    Combines insight properties with context to determine
    if push surfacing is appropriate.
    """

    insight_id: str
    confidence: float
    relevance_to_context: float
    learning_type: str
    requires_attention: bool = False
    last_similar_surfaced: Optional[datetime] = None

    # Thresholds
    CONFIDENCE_THRESHOLD: float = 0.75
    RELEVANCE_THRESHOLD: float = 0.5
    SIMILAR_COOLDOWN_HOURS: int = 24

    def is_ready_for_push(self, context: SurfacingContext) -> bool:
        """
        Check all prerequisites for push surfacing.

        D4 specification gates:
        1. Trust Stage 3+ (ESTABLISHED or TRUSTED)
        2. Confidence ≥ 0.75
        3. Contextually relevant (≥ 0.5)
        4. ≥24 hours since last similar push
        5. User not in focus mode

        Args:
            context: Current surfacing context

        Returns:
            True if all gates pass
        """
        # Gate 1: Trust stage (checked in context)
        if not context.can_receive_push():
            return False

        # Gate 2: Confidence
        if self.confidence < self.CONFIDENCE_THRESHOLD:
            return False

        # Gate 3: Relevance
        if self.relevance_to_context < self.RELEVANCE_THRESHOLD:
            return False

        # Gate 4: Cooldown for similar insights
        if self.last_similar_surfaced is not None:
            hours_since = (datetime.now() - self.last_similar_surfaced).total_seconds() / 3600
            if hours_since < self.SIMILAR_COOLDOWN_HOURS:
                return False

        return True

    @property
    def is_high_priority(self) -> bool:
        """Check if this insight should be prioritized."""
        # Corrections are high priority
        if self.learning_type == "correction":
            return True
        # Insights requiring attention are high priority
        if self.requires_attention:
            return True
        return False


# =============================================================================
# Relevance Scoring
# =============================================================================


def score_relevance(
    insight: SurfaceableInsight,
    context: SurfacingContext,
) -> float:
    """
    Score how relevant an insight is to current work.

    Scoring factors (per D4 spec):
    - Entity match (40%): Insight applies to active entities
    - Topic match (30%): Insight tags match context topics
    - Recency (20%): Fresher insights more relevant
    - Surprisingness (10%): Unexpected insights more valuable

    Args:
        insight: The insight to score
        context: Current work context

    Returns:
        Relevance score 0.0-1.0
    """
    if insight.learning is None:
        return 0.0

    learning = insight.learning
    score = 0.0

    # Entity match (40% weight)
    if learning.applies_to_entities and context.active_entities:
        entity_overlap = set(learning.applies_to_entities) & set(context.active_entities)
        entity_score = len(entity_overlap) / len(learning.applies_to_entities)
        score += 0.4 * entity_score

    # Topic match (30% weight)
    if learning.topic_tags and context.topic_tags:
        topic_overlap = set(learning.topic_tags) & set(context.topic_tags)
        topic_score = len(topic_overlap) / len(learning.topic_tags)
        score += 0.3 * topic_score

    # Recency (20% weight) - fresher insights more relevant
    age_days = (datetime.now() - insight.created_at).days
    recency_score = max(0, 1 - age_days / 30)  # Decay over 30 days
    score += 0.2 * recency_score

    # Surprisingness (10% weight)
    if learning.insight is not None:
        surprisingness = learning.insight.surprisingness
        score += 0.1 * surprisingness

    return min(1.0, score)


# =============================================================================
# PremonitionService
# =============================================================================


class PremonitionService:
    """
    Orchestrates insight surfacing.

    Provides three surfacing modes:
    - Pull: User asks for insights
    - Passive: Insights for dashboard/journal view
    - Push: Proactive surfacing when appropriate

    Example:
        service = PremonitionService(journal)

        # Pull mode
        insights = await service.get_insights_for_user(user_id)

        # Push mode (check if ready, get best insight)
        context = SurfacingContext(user_id=user_id, trust_stage=TrustStage.ESTABLISHED)
        message = await service.maybe_surface_insight(context)
        if message:
            send_to_user(message)
    """

    def __init__(
        self,
        journal: Optional[InsightJournal] = None,
        last_surfaced_cache: Optional[Dict[str, datetime]] = None,
    ):
        """
        Initialize the premonition service.

        Args:
            journal: InsightJournal to query (creates default if None)
            last_surfaced_cache: Cache of last surfaced time by topic
        """
        self.journal = journal or InsightJournal()
        self._last_surfaced_by_topic: Dict[str, datetime] = last_surfaced_cache or {}

    # =========================================================================
    # Pull Mode - User asks for insights
    # =========================================================================

    async def get_insights_for_user(
        self,
        user_id: str,
        limit: int = 10,
    ) -> List[SurfaceableInsight]:
        """
        Get insights for user (pull mode).

        Returns insights without trust/confidence gates since
        user explicitly asked.

        Args:
            user_id: User to get insights for
            limit: Maximum insights to return

        Returns:
            List of insights ordered by relevance
        """
        # For pull, we don't need high confidence
        return await self.journal.get_unsurfaced(
            user_id=user_id,
            min_confidence=0.0,  # Accept any confidence for pull
            trust_stage=1,  # Accept any trust for pull
            limit=limit,
        )

    async def get_insights_for_context(
        self,
        user_id: str,
        context: SurfacingContext,
        limit: int = 5,
    ) -> List[SurfaceableInsight]:
        """
        Get insights relevant to current context (pull mode).

        Args:
            user_id: User to get insights for
            context: Current work context
            limit: Maximum insights to return

        Returns:
            List of contextually relevant insights
        """
        return await self.journal.get_for_context(
            user_id=user_id,
            context_entities=context.active_entities,
            context_topics=context.topic_tags,
            trust_stage=1,  # Accept any trust for pull
            limit=limit,
        )

    # =========================================================================
    # Passive Mode - Dashboard/Journal view
    # =========================================================================

    async def get_learning_dashboard_insights(
        self,
        user_id: str,
        include_surfaced: bool = True,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """
        Get insights for Learning Dashboard (passive mode).

        Returns insights formatted for dashboard display,
        including already-surfaced ones.

        Args:
            user_id: User to get insights for
            include_surfaced: Whether to include already-surfaced insights
            limit: Maximum insights to return

        Returns:
            List of insight dicts with display metadata
        """
        insights = await self.journal.get_unsurfaced(
            user_id=user_id,
            min_confidence=0.0,
            trust_stage=1,
            limit=limit,
        )

        return [
            {
                "id": insight.id,
                "type": insight.learning_type,
                "description": (insight.learning.description if insight.learning else ""),
                "expression": (insight.learning.expression if insight.learning else ""),
                "confidence": (insight.learning.confidence if insight.learning else 0),
                "created_at": insight.created_at.isoformat(),
                "surfaced_count": insight.surfaced_count,
                "requires_attention": insight.requires_attention,
            }
            for insight in insights
        ]

    # =========================================================================
    # Push Mode - Proactive surfacing
    # =========================================================================

    async def maybe_surface_insight(
        self,
        context: SurfacingContext,
    ) -> Optional[str]:
        """
        Check if any insight should surface, return message if so.

        This is the main entry point for push surfacing.
        Applies all D4 specification gates.

        Args:
            context: Current surfacing context

        Returns:
            Framed message if insight should surface, None otherwise
        """
        # Check context allows push
        if not context.can_receive_push():
            return None

        # Get candidate insights
        candidates = await self.journal.get_unsurfaced(
            user_id=context.user_id,
            min_confidence=InsightReadiness.CONFIDENCE_THRESHOLD,
            trust_stage=context.trust_stage.value,
        )

        if not candidates:
            return None

        # Score and filter candidates
        ready_candidates: List[tuple] = []
        for insight in candidates:
            relevance = score_relevance(insight, context)

            # Get last surfaced time for similar topic
            last_similar = self._get_last_similar_surfaced(insight)

            readiness = InsightReadiness(
                insight_id=insight.id,
                confidence=insight.learning.confidence if insight.learning else 0,
                relevance_to_context=relevance,
                learning_type=insight.learning_type,
                requires_attention=insight.requires_attention,
                last_similar_surfaced=last_similar,
            )

            if readiness.is_ready_for_push(context):
                # Score: priority bonus + relevance + confidence
                priority_bonus = 1.0 if readiness.is_high_priority else 0.0
                score = (
                    priority_bonus
                    + relevance
                    + (insight.learning.confidence if insight.learning else 0)
                )
                ready_candidates.append((insight, readiness, score))

        if not ready_candidates:
            return None

        # Select best candidate (highest score)
        best_insight, _, _ = max(ready_candidates, key=lambda x: x[2])

        # Mark as surfaced
        await self.journal.mark_surfaced(best_insight.id, "surfaced")

        # Update last surfaced cache
        self._record_surfaced(best_insight)

        # Frame and return
        return frame_insight_for_surfacing(best_insight)

    async def surface_specific_insight(
        self,
        insight_id: str,
        response: str = "engaged",
    ) -> Optional[str]:
        """
        Surface a specific insight (after user interaction).

        Used when user selects an insight from dashboard
        or responds to an offer.

        Args:
            insight_id: ID of insight to surface
            response: User's response ("engaged", "dismissed", "corrected")

        Returns:
            Framed message if insight found, None otherwise
        """
        insight = await self.journal.get(insight_id)
        if insight is None:
            return None

        await self.journal.mark_surfaced(insight_id, response)
        return frame_insight_for_surfacing(insight)

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def _get_last_similar_surfaced(
        self,
        insight: SurfaceableInsight,
    ) -> Optional[datetime]:
        """Get last time a similar topic was surfaced."""
        if insight.learning is None:
            return None

        # Check each topic tag
        for tag in insight.learning.topic_tags:
            if tag in self._last_surfaced_by_topic:
                return self._last_surfaced_by_topic[tag]

        return None

    def _record_surfaced(self, insight: SurfaceableInsight) -> None:
        """Record that this insight was surfaced."""
        if insight.learning is None:
            return

        now = datetime.now()
        for tag in insight.learning.topic_tags:
            self._last_surfaced_by_topic[tag] = now
