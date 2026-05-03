"""
Composting pipeline - wires Extractor to InsightJournal with typed learnings.

Part of #667 COMPOSTING-PIPELINE (child of #436 MUX-TECH-PHASE4-COMPOSTING).

This module provides:
- SurfaceableInsight: Enhanced entry with surfacing control
- InsightJournal: Query interface for surfacing
- CompostingPipeline: Orchestrates extraction and storage

Flow:
  CompostBin (#666) → Pipeline → InsightJournal → Surfacing (#415)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from .composting_models import (
    CompostingTrigger,
    ExtractedLearning,
    create_correction_learning,
    create_insight_learning,
    create_pattern_learning,
)
from .lifecycle import CompostingExtractor, CompostResult, LifecycleState

# =============================================================================
# SurfaceableInsight - Enhanced Entry with Surfacing Control
# =============================================================================


@dataclass
class SurfaceableInsight:
    """
    An insight ready for surfacing to the user.

    Extends the base InsightJournalEntry concept with:
    - Typed ExtractedLearning instead of string
    - Surfacing control fields
    - Trust-based visibility
    - User response tracking

    This is the model that #415 PREMONITION queries to
    determine what insights to surface and when.
    """

    # Identity
    id: str = field(default_factory=lambda: str(uuid4()))
    object_id: str = ""  # What was composted
    user_id: str = ""  # Who this insight belongs to
    created_at: datetime = field(default_factory=datetime.now)

    # The learning (typed, not just str)
    learning: Optional[ExtractedLearning] = None

    # Surfacing control
    surfaced_count: int = 0
    last_surfaced: Optional[datetime] = None
    user_response: Optional[str] = None  # "engaged", "dismissed", "corrected"

    # Trust-based visibility (Stage 1-4 per trust model)
    min_trust_stage: int = 1  # 1=all can see, 3=push eligible, 4=proactive

    # Relevance tracking
    connected_insights: List[str] = field(default_factory=list)
    context_tags: List[str] = field(default_factory=list)

    def is_surfaceable(self, trust_stage: int) -> bool:
        """
        Check if this insight can be surfaced at given trust level.

        Args:
            trust_stage: Current trust stage (1-4)

        Returns:
            True if insight can be surfaced
        """
        # Must meet minimum trust
        if trust_stage < self.min_trust_stage:
            return False

        # Don't resurface recently surfaced
        if self.last_surfaced is not None:
            hours_since = (datetime.now() - self.last_surfaced).total_seconds() / 3600
            if hours_since < 24:  # 24 hour cooldown
                return False

        # Don't resurface dismissed insights
        if self.user_response == "dismissed":
            return False

        return True

    @property
    def is_high_confidence(self) -> bool:
        """Check if the underlying learning is high confidence."""
        if self.learning is None:
            return False
        return self.learning.is_high_confidence

    @property
    def requires_attention(self) -> bool:
        """Check if this insight requires user attention."""
        if self.learning is None:
            return False
        return self.learning.requires_attention

    @property
    def learning_type(self) -> str:
        """Get the type of learning."""
        if self.learning is None:
            return "unknown"
        return self.learning.learning_type

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "object_id": self.object_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "learning": self.learning.to_dict() if self.learning else None,
            "surfaced_count": self.surfaced_count,
            "last_surfaced": (self.last_surfaced.isoformat() if self.last_surfaced else None),
            "user_response": self.user_response,
            "min_trust_stage": self.min_trust_stage,
            "connected_insights": self.connected_insights,
            "context_tags": self.context_tags,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SurfaceableInsight":
        """Create from dictionary."""
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif created_at is None:
            created_at = datetime.now()

        last_surfaced = data.get("last_surfaced")
        if isinstance(last_surfaced, str):
            last_surfaced = datetime.fromisoformat(last_surfaced)

        learning = None
        learning_data = data.get("learning")
        if learning_data:
            learning = ExtractedLearning.from_dict(learning_data)

        return cls(
            id=data.get("id", str(uuid4())),
            object_id=data.get("object_id", ""),
            user_id=data.get("user_id", ""),
            created_at=created_at,
            learning=learning,
            surfaced_count=data.get("surfaced_count", 0),
            last_surfaced=last_surfaced,
            user_response=data.get("user_response"),
            min_trust_stage=data.get("min_trust_stage", 1),
            connected_insights=data.get("connected_insights", []),
            context_tags=data.get("context_tags", []),
        )


# =============================================================================
# InsightJournal - Query Interface for Surfacing
# =============================================================================


class InsightJournal:
    """
    Durable query interface for surfaceable insights.

    The journal is where Piper "files away" learnings during quiet-hours
    composting (per `composting-experience-design.md`). Per #1035 (May 3,
    2026), the journal is durable: insights persist across process restarts
    via PostgreSQL, matching the MUX framing that the journal exists across
    "sleep" cycles.

    Each public method opens its own DB session via
    `AsyncSessionFactory.session_scope()` and delegates to `InsightRepository`.
    Transaction-boundary is per-call so a journal-write failure doesn't cascade
    into the caller's transaction (mirrors #1018 Q2 ratification).

    Tests that need an in-memory store for testing OTHER classes (composting
    pipeline / scheduler / premonition surfacers) use `FakeInsightJournal`
    at `tests/unit/services/mux/_fake_insight_journal.py`. This separation
    makes the test/production boundary explicit; the production path has
    no in-memory branch.
    """

    def __init__(self):
        """No-arg constructor preserved for callers that defaulted it."""
        # Lazy import to avoid services/mux ↔ services/database circularity
        # at module load time.
        pass

    @staticmethod
    def _session_scope():
        """Open a fresh session for one journal operation.

        Imported lazily so that services/mux doesn't depend on
        services/database at module-load time.
        """
        from services.database.session_factory import AsyncSessionFactory

        return AsyncSessionFactory.session_scope()

    @staticmethod
    def _new_repo(session):
        """Construct an InsightRepository over the given session."""
        from services.database.repositories import InsightRepository

        return InsightRepository(session)

    async def add(self, insight: SurfaceableInsight) -> SurfaceableInsight:
        """Persist an insight via the repository."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            await repo.add(insight)
        return insight

    async def get(self, insight_id: str) -> Optional[SurfaceableInsight]:
        """Get insight by ID."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            return await repo.get(insight_id)

    async def get_unsurfaced(
        self,
        user_id: str,
        min_confidence: float = 0.75,
        trust_stage: int = 3,
        limit: int = 10,
    ) -> List[SurfaceableInsight]:
        """Push candidate retrieval — see InsightRepository.get_unsurfaced."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            return await repo.get_unsurfaced(
                user_id=user_id,
                min_confidence=min_confidence,
                trust_stage=trust_stage,
                limit=limit,
            )

    async def get_for_context(
        self,
        user_id: str,
        context_entities: Optional[List[str]] = None,
        context_topics: Optional[List[str]] = None,
        trust_stage: int = 1,
        limit: int = 5,
    ) -> List[SurfaceableInsight]:
        """Pull relevance scoring — see InsightRepository.get_for_context."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            return await repo.get_for_context(
                user_id=user_id,
                context_entities=context_entities,
                context_topics=context_topics,
                trust_stage=trust_stage,
                limit=limit,
            )

    async def mark_surfaced(
        self,
        insight_id: str,
        response: str,
    ) -> Optional[SurfaceableInsight]:
        """Record that insight was surfaced + user response."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            return await repo.mark_surfaced(insight_id, response)

    async def get_for_object(self, object_id: str) -> List[SurfaceableInsight]:
        """Get all insights for a specific composted object."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            return await repo.get_for_object(object_id)

    async def count(self, user_id: Optional[str] = None) -> int:
        """Row count, optionally scoped to a single user."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            return await repo.count(user_id=user_id)

    async def clear(self, user_id: str) -> int:
        """Per-user clear (#1035 Q6). Returns count deleted."""
        async with self._session_scope() as session:
            repo = self._new_repo(session)
            return await repo.clear(user_id=user_id)


# =============================================================================
# CompostingPipeline - Orchestrates Extraction and Storage
# =============================================================================


class CompostingPipeline:
    """
    Orchestrates extraction and journal storage.

    Takes objects from CompostBin, extracts learnings using
    CompostingExtractor, and stores as SurfaceableInsights
    in the InsightJournal.

    Example:
        pipeline = CompostingPipeline(
            extractor=CompostingExtractor(),
            journal=InsightJournal(),
        )

        learnings = await pipeline.process(old_task, user_id="user-123")
        # Now insights are in journal, ready for #415 to surface
    """

    def __init__(
        self,
        extractor: Optional[CompostingExtractor] = None,
        journal: Optional[InsightJournal] = None,
    ):
        """
        Initialize pipeline.

        Args:
            extractor: CompostingExtractor instance (creates default if None)
            journal: InsightJournal instance (creates default if None)
        """
        self.extractor = extractor or CompostingExtractor()
        self.journal = journal or InsightJournal()

    async def process(
        self,
        obj: Any,
        user_id: str = "",
        trigger: Optional[CompostingTrigger] = None,
    ) -> List[ExtractedLearning]:
        """
        Extract learnings from object and store in journal.

        Args:
            obj: Object to compost
            user_id: User ID to associate with learnings
            trigger: What triggered composting (for context)

        Returns:
            List of ExtractedLearning objects created
        """
        # Extract using existing extractor
        result = self.extractor.extract(obj)

        # Convert to typed learnings
        learnings = self._to_extracted_learnings(result, obj)

        # Store each learning as surfaceable insight
        object_id = getattr(obj, "id", str(id(obj)))

        for learning in learnings:
            insight = SurfaceableInsight(
                object_id=object_id,
                user_id=user_id,
                learning=learning,
                min_trust_stage=self._determine_trust_stage(learning),
                context_tags=learning.topic_tags.copy(),
            )
            await self.journal.add(insight)

        return learnings

    def _to_extracted_learnings(
        self,
        result: CompostResult,
        obj: Any,
    ) -> List[ExtractedLearning]:
        """
        Convert CompostResult to typed ExtractedLearning objects.

        Analyzes lessons and journey to create appropriate
        Pattern, Insight, or Correction learnings.
        """
        learnings = []
        object_id = result.object_summary.get("id", str(id(obj)))

        # Calculate base confidence from journey
        base_confidence = self._calculate_confidence(result.journey)

        # Extract topic tags from summary
        topic_tags = self._extract_topic_tags(result.object_summary)

        for lesson in result.lessons:
            learning = self._lesson_to_learning(
                lesson=lesson,
                source_objects=[object_id],
                confidence=base_confidence,
                topic_tags=topic_tags,
                journey=result.journey,
            )
            learnings.append(learning)

        return learnings

    def _lesson_to_learning(
        self,
        lesson: str,
        source_objects: List[str],
        confidence: float,
        topic_tags: List[str],
        journey: List[LifecycleState],
    ) -> ExtractedLearning:
        """
        Convert a lesson string to typed ExtractedLearning.

        Analyzes the lesson text to determine if it's a
        pattern, insight, or correction.
        """
        lesson_lower = lesson.lower()

        # Check for correction signals
        if any(
            signal in lesson_lower
            for signal in ["wrong", "incorrect", "not", "actually", "instead"]
        ):
            return create_correction_learning(
                previous_understanding="Previous assumption",
                new_understanding=lesson,
                evidence=source_objects,
                confidence=confidence,
                source_objects=source_objects,
                topic_tags=topic_tags,
            )

        # Check for pattern signals
        if any(
            signal in lesson_lower
            for signal in [
                "pattern",
                "recurring",
                "repeated",
                "always",
                "usually",
                "often",
            ]
        ):
            return create_pattern_learning(
                description=lesson,
                occurrences=source_objects,
                frequency=0.5,  # Unknown frequency
                predictive_power=confidence,
                source_objects=source_objects,
                confidence=confidence,
                topic_tags=topic_tags,
            )

        # Default to insight
        return create_insight_learning(
            description=lesson,
            derived_from=source_objects,
            confidence=confidence,
            surprisingness=self._calculate_surprisingness(journey),
            source_objects=source_objects,
            topic_tags=topic_tags,
        )

    def _calculate_confidence(self, journey: List[LifecycleState]) -> float:
        """
        Calculate confidence based on lifecycle journey.

        Longer journeys through more states = more confident.
        Reaching RATIFIED = boost.
        """
        if not journey:
            return 0.5

        base = 0.5

        # Longer journey = more confident
        journey_bonus = min(len(journey) * 0.05, 0.25)

        # Ratified = validated
        if LifecycleState.RATIFIED in journey:
            ratified_bonus = 0.15
        else:
            ratified_bonus = 0

        return min(base + journey_bonus + ratified_bonus, 1.0)

    def _calculate_surprisingness(self, journey: List[LifecycleState]) -> float:
        """
        Calculate how surprising the insight is.

        Unusual journeys (skipping states, quick deprecation) = surprising.
        """
        if not journey:
            return 0.0

        surprisingness = 0.0

        # Short journey = somewhat surprising
        if len(journey) <= 2:
            surprisingness += 0.3

        # Skipped derivation = surprising
        if (
            LifecycleState.EMERGENT in journey
            and LifecycleState.NOTICED in journey
            and LifecycleState.DERIVED not in journey
        ):
            surprisingness += 0.2

        return min(surprisingness, 1.0)

    def _extract_topic_tags(self, summary: Dict[str, Any]) -> List[str]:
        """Extract topic tags from object summary."""
        tags = []

        # Use type/category if available
        if "type" in summary:
            tags.append(str(summary["type"]).lower())
        if "category" in summary:
            tags.append(str(summary["category"]).lower())

        return tags

    def _determine_trust_stage(self, learning: ExtractedLearning) -> int:
        """
        Determine minimum trust stage for surfacing.

        Corrections require higher trust (stage 3).
        High confidence can be pushed (stage 3).
        Others start at stage 1.
        """
        # Corrections need high trust
        if learning.learning_type == "correction":
            return 3

        # High confidence can be pushed
        if learning.is_high_confidence:
            return 2

        # Default to pull-only
        return 1
