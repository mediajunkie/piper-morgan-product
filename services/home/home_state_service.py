"""
Home State Service

Issue #419: MUX-NAV-HOME - Home State Design
Pattern-050: Context Dataclass Pair
Pattern-051: Parallel Place Gathering
Pattern-052: Personality Bridge

Composes the home state experience from multiple sources:
- User's trust stage
- Recent activity / observations
- Standup-like briefing data
- Available lenses (always present)

Trust-gates the visibility of objects by hardness level.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog

from services.shared_types import HardnessLevel, TrustStage

logger = structlog.get_logger()

# #1214: dev/seed composting insights (services/mux/seed_compostable.py) carry
# these category/type markers in their context_tags (via _extract_topic_tags).
# They are DEV/TEST fixtures and must NEVER render in the user-facing home
# "Recently" module. Filtered at the home surface, not the shared
# journal.list_for_user — debug/review surfaces (e.g. the Insight Journal page)
# may legitimately want to see everything.
_DEV_SEED_TAGS = frozenset({"dev_seed", "seed_demo_object"})
# Over-fetch then filter: a test user can accumulate many seed rows newer than
# its real reflections, which would otherwise crowd the real ones out of top-N.
_RECENCY_FETCH_CAP = 50


@dataclass
class HomeStateContext:
    """
    Context for generating home state (Pattern-050).

    Inputs needed to compose the home state experience.
    """

    user_id: UUID
    trust_stage: TrustStage
    timestamp: datetime
    # Optional: specific time-of-day context
    time_of_day: str = "default"  # "morning", "midday", "evening", "default"
    # Optional: recent activity for context-aware display
    recent_conversation_ids: List[UUID] = field(default_factory=list)


@dataclass
class HomeStateItem:
    """
    A single item in the home state.

    Items have hardness levels that determine trust-gated visibility.
    """

    id: str
    title: str
    description: str
    hardness: HardnessLevel
    # Item type for rendering decisions
    item_type: str  # "lens", "project", "observation", "suggestion", "ephemeral"
    # Source for transparency ("Piper noticed from GitHub", etc.)
    source: Optional[str] = None
    # Action available for this item
    action: Optional[str] = None
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HomeStateResult:
    """
    Result of home state generation (Pattern-050).

    Contains the composed home state filtered by trust-gated hardness.
    """

    user_id: UUID
    trust_stage: TrustStage
    generated_at: datetime
    # Items grouped by hardness for rendering
    items: List[HomeStateItem]
    # Time-of-day greeting variation
    greeting: str
    # Standup-style briefing (if applicable)
    briefing_summary: Optional[str] = None
    # #1194 / #1033: composted insights surfaced with reflective framing (Stage 3+).
    # Each: {"id": insight_id, "text": framed_reflection}. Marked surfaced on render.
    surfaced_insights: List[Dict[str, str]] = field(default_factory=list)
    # Generation metrics
    generation_time_ms: int = 0


class HomeStateService:
    """
    Composes the trust-gated home state experience.

    Issue #419: MUX-NAV-HOME
    ADR-053: Trust Computation Architecture

    The home state adapts to trust level:
    - Stage 1 (NEW): Only hardest objects (user-initiated)
    - Stage 2 (BUILDING): + Hard objects with capability hints
    - Stage 3 (ESTABLISHED): + Soft observations ("I noticed...")
    - Stage 4 (TRUSTED): All levels including anticipatory (softest)
    """

    def __init__(
        self,
        trust_service: Optional[Any] = None,
        standup_service: Optional[Any] = None,
        journal: Optional[Any] = None,
    ):
        """
        Initialize with optional service dependencies.

        Services can be injected or will use defaults.
        """
        self.trust_service = trust_service
        self.standup_service = standup_service
        self._journal = journal  # InsightJournal; lazily defaulted (avoid import cycle)

    def _get_journal(self):
        """Lazy InsightJournal (avoids services.home ↔ services.mux import cycle)."""
        if self._journal is None:
            from services.mux.composting_pipeline import InsightJournal

            self._journal = InsightJournal()
        return self._journal

    async def _surface_composted_insights(
        self, context: HomeStateContext, limit: int = 3
    ) -> List[Dict[str, str]]:
        """#1194 / #1033: the home "Recently" module — show the user's most RECENT
        composted reflections (newest-first), framed.

        This is a PERSISTENT recency digest, NOT a one-shot push: it does NOT mark
        insights surfaced, so a page reload keeps showing them (mark-on-render
        consumes them, which is right for a proactive push but wrong for a home
        module — PM 2026-06-12). New composting pushes older reflections off the
        top-N naturally. Stage-gated by the caller (ESTABLISHED+). Failure → []."""
        try:
            from services.mux.premonition import frame_insight_for_surfacing

            journal = self._get_journal()
            # #1214: over-fetch then drop dev/seed insights so seeded rows can't
            # crowd real reflections out of the top-N.
            insights = await journal.list_for_user(str(context.user_id), limit=_RECENCY_FETCH_CAP)
            real = [
                ins for ins in insights if not _DEV_SEED_TAGS.intersection(ins.context_tags or [])
            ]
            return [
                {"id": ins.id, "text": frame_insight_for_surfacing(ins)} for ins in real[:limit]
            ]
        except Exception as e:
            logger.warning(f"home recent-reflections surfacing failed: {e}")
            return []

    async def generate_home_state(self, context: HomeStateContext) -> HomeStateResult:
        """
        Generate the trust-gated home state.

        Pattern-050: Context → Result transformation.
        Pattern-051: Would gather from multiple places in parallel.
        Pattern-052: Transforms raw data into experience language.
        """
        start_time = datetime.now(timezone.utc)

        # Determine minimum hardness based on trust stage
        min_hardness = self._get_min_hardness_for_stage(context.trust_stage)

        # Gather items from various sources (would be parallel in full implementation)
        all_items = await self._gather_home_items(context)

        # Filter by trust-gated hardness
        visible_items = [item for item in all_items if item.hardness >= min_hardness]

        # Generate greeting based on time and trust
        greeting = self._generate_greeting(context)

        # Generate briefing summary if trust allows
        briefing_summary = None
        surfaced_insights: List[Dict[str, str]] = []
        if context.trust_stage >= TrustStage.ESTABLISHED:
            briefing_summary = await self._generate_briefing_summary(context)
            # #1194 / #1033: surface composted insights with reflective framing.
            surfaced_insights = await self._surface_composted_insights(context)

        end_time = datetime.now(timezone.utc)
        generation_time_ms = int((end_time - start_time).total_seconds() * 1000)

        return HomeStateResult(
            user_id=context.user_id,
            trust_stage=context.trust_stage,
            generated_at=end_time,
            items=visible_items,
            greeting=greeting,
            briefing_summary=briefing_summary,
            surfaced_insights=surfaced_insights,
            generation_time_ms=generation_time_ms,
        )

    def _get_min_hardness_for_stage(self, stage: TrustStage) -> HardnessLevel:
        """
        Determine minimum hardness level visible at a trust stage.

        Higher min_hardness = fewer objects visible (more restrictive).
        Lower min_hardness = more objects visible (more permissive).

        From #419 design:
        - Stage 1 (NEW): Only hardest
        - Stage 2 (BUILDING): Hard and above
        - Stage 3 (ESTABLISHED): Soft and above
        - Stage 4 (TRUSTED): All (softest and above)
        """
        stage_to_min_hardness = {
            TrustStage.NEW: HardnessLevel.HARDEST,
            TrustStage.BUILDING: HardnessLevel.HARD,
            TrustStage.ESTABLISHED: HardnessLevel.SOFT,
            TrustStage.TRUSTED: HardnessLevel.SOFTEST,
        }
        return stage_to_min_hardness.get(stage, HardnessLevel.HARDEST)

    async def _gather_home_items(self, context: HomeStateContext) -> List[HomeStateItem]:
        """
        Gather items from various sources.

        Pattern-051: In full implementation, this would gather in parallel from:
        - GitHub (recent activity, PRs)
        - Calendar (upcoming events)
        - Todos/Projects (user's work)
        - Observations (Piper's notices)

        For now, returns the always-present lenses.
        """
        items: List[HomeStateItem] = []

        # HARDEST: Lenses - always present, part of the furniture
        items.extend(self._get_lens_items())

        # HARD: User's persistent data (would come from repositories)
        # items.extend(await self._get_user_projects(context))

        # SOFT: Observations (would come from observation service)
        # if context.trust_stage >= TrustStage.ESTABLISHED:
        #     items.extend(await self._get_observations(context))

        # SOFTEST: Anticipatory suggestions (Stage 4 only)
        # if context.trust_stage >= TrustStage.TRUSTED:
        #     items.extend(await self._get_anticipatory_items(context))

        return items

    def _get_lens_items(self) -> List[HomeStateItem]:
        """
        Get the always-present lens items.

        Lenses are HARDEST - part of the furniture, always reachable.
        From #419: "What's stuck", "What's urgent", "What's coming"
        """
        return [
            HomeStateItem(
                id="lens-stuck",
                title="What's stuck",
                description="Tasks and projects that need attention",
                hardness=HardnessLevel.HARDEST,
                item_type="lens",
                action="show_stuck",
            ),
            HomeStateItem(
                id="lens-urgent",
                title="What's urgent",
                description="Time-sensitive items requiring action",
                hardness=HardnessLevel.HARDEST,
                item_type="lens",
                action="show_urgent",
            ),
            HomeStateItem(
                id="lens-coming",
                title="What's coming",
                description="Upcoming deadlines and events",
                hardness=HardnessLevel.HARDEST,
                item_type="lens",
                action="show_coming",
            ),
        ]

    def _generate_greeting(self, context: HomeStateContext) -> str:
        """
        Generate trust-appropriate greeting.

        Pattern-052: Personality Bridge - transforms context into experience language.

        From #419 design:
        - Stage 1: Minimal, responsive
        - Stage 2: Hints at capabilities
        - Stage 3: Shows awareness ("I noticed...")
        - Stage 4: Shows agency ("I've been thinking...")
        """
        greetings = {
            TrustStage.NEW: "Welcome. What can I help you with?",
            TrustStage.BUILDING: "Good to see you. I'm here to help.",
            TrustStage.ESTABLISHED: "I noticed a few things while you were away.",
            TrustStage.TRUSTED: "I've been thinking about your priorities.",
        }

        # Time-of-day variations could be added here
        base_greeting = greetings.get(context.trust_stage, greetings[TrustStage.NEW])

        if context.time_of_day == "morning":
            return f"Good morning. {base_greeting}"
        elif context.time_of_day == "evening":
            return f"Good evening. {base_greeting}"

        return base_greeting

    async def _generate_briefing_summary(self, context: HomeStateContext) -> Optional[str]:
        """
        Generate standup-style briefing summary.

        Only for Stage 3+ (ESTABLISHED) users.
        Pattern-052: Transforms standup data into consciousness-aware narrative.
        """
        # Would integrate with StandupOrchestrationService in full implementation
        if self.standup_service:
            try:
                # standup = await self.standup_service.generate(...)
                # return self._transform_standup_to_briefing(standup)
                pass
            except Exception as e:
                logger.warning(f"Error generating briefing: {e}")

        # Default placeholder for now
        return None
