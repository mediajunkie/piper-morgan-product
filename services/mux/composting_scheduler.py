"""
Composting scheduler - "filing dreams" during rest periods.

Part of #668 COMPOSTING-SCHEDULE (child of #436 MUX-TECH-PHASE4-COMPOSTING).

This module provides:
- CompostingSchedule: Configuration for when composting happens
- CompostingScheduler: Orchestrates scheduled composting runs
- CompostingRunResult: Result of a composting cycle
- COMPOSTING_FRAMES: Consciousness-preserving language

The metaphor: Piper files away lessons during quiet hours, like
the brain consolidates memories during sleep.
"""

import logging
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple

from .compost_bin import CompostBin, CompostBinEntry
from .composting_models import ExtractedLearning
from .composting_pipeline import CompostingPipeline

logger = logging.getLogger(__name__)


# =============================================================================
# Consciousness-Preserving Language
# =============================================================================


COMPOSTING_FRAMES = [
    "Having had some time to reflect...",
    "Looking back at our work together...",
    "Something I've been thinking about...",
    "It occurs to me that...",
    "I've been mulling over...",
    "After some thought...",
    "In quiet moments, I realized...",
]


def frame_learning(learning: ExtractedLearning) -> str:
    """
    Apply consciousness-preserving framing to a learning.

    Returns the learning's expression wrapped in natural
    "reflection" language, as if Piper had time to think.

    Per #1033 (May 3): output is run through the anti-surveillance guardrail
    before return. Compost-time framing happens before storage, so this
    catches surveillance phrasing at the source — the stored expression
    never contains forbidden surveillance language. Surface-time framing
    (`frame_insight_for_surfacing` in premonition.py) provides a second
    layer for any LLM-generated text wrapping insights at surface time.
    """
    frame = random.choice(COMPOSTING_FRAMES)

    # Use the learning's expression if available
    if learning.expression:
        # Remove any existing framing prefix
        expression = learning.expression
        for f in COMPOSTING_FRAMES:
            if expression.startswith(f):
                expression = expression[len(f) :].strip()
                break
        framed = f"{frame} {expression}"
    else:
        # Fall back to description
        framed = f"{frame} {learning.description}"

    # #1033: anti-surveillance guardrail. Lazy import to avoid module-load
    # cycle (anti_surveillance has no service deps; this is just paranoia).
    from services.mux.anti_surveillance import safe_surface

    return safe_surface(framed)


# =============================================================================
# CompostingSchedule
# =============================================================================


@dataclass
class CompostingSchedule:
    """
    Configuration for when composting happens.

    The default schedule runs during "quiet hours" (2-5 AM),
    mirroring the brain's memory consolidation during sleep.
    """

    # Which hours are "quiet" (0-23, local time)
    quiet_hours: List[int] = field(default_factory=lambda: [2, 3, 4])

    # Don't wake up for fewer than this many items
    min_pending: int = 5

    # Process at most this many per cycle
    max_batch: int = 20

    # Minimum time between runs (in hours)
    min_interval_hours: float = 4.0

    # #669 hybrid trigger: max time since the last run before forcing a cycle
    # regardless of quiet-hours / min_pending (the "unihemispheric dreaming" /
    # insomniac safeguard). Guards against starvation when the quiet-hour +
    # min_pending conjunction is never met — e.g. a deployment never up at 2-5 AM.
    # Set to None or <= 0 to disable the hybrid trigger.
    max_hours_since_last_run: Optional[float] = 72.0

    def is_quiet_hour(self, hour: int) -> bool:
        """Check if the given hour is a quiet hour."""
        return hour in self.quiet_hours

    def is_quiet_now(self, current_time: Optional[datetime] = None) -> bool:
        """Check if right now is a quiet hour."""
        current_time = current_time or datetime.now()
        return self.is_quiet_hour(current_time.hour)


# =============================================================================
# CompostingRunResult
# =============================================================================


@dataclass
class CompostingRunResult:
    """
    Result of a composting run.

    Captures what was processed and what was learned
    for logging and observability.
    """

    # What was processed
    processed_count: int
    object_ids: List[str] = field(default_factory=list)

    # What was learned
    learnings_extracted: int = 0
    learning_types: List[str] = field(default_factory=list)

    # Timing
    run_at: datetime = field(default_factory=datetime.now)
    duration_seconds: float = 0.0

    # Status
    success: bool = True
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary for logging/serialization."""
        return {
            "processed_count": self.processed_count,
            "object_ids": self.object_ids,
            "learnings_extracted": self.learnings_extracted,
            "learning_types": self.learning_types,
            "run_at": self.run_at.isoformat(),
            "duration_seconds": self.duration_seconds,
            "success": self.success,
            "errors": self.errors,
        }


# =============================================================================
# CompostingScheduler
# =============================================================================


class CompostingScheduler:
    """
    Orchestrates scheduled composting runs.

    The scheduler checks if conditions are right for composting
    (quiet hour, enough pending items, not too recent) and
    runs the composting pipeline on ready items.

    Example:
        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=pipeline,
        )

        # In a background task or cron job:
        result = await scheduler.maybe_run()
        if result:
            print(f"Processed {result.processed_count} items")

        # For testing:
        result = await scheduler.run(force=True)
    """

    def __init__(
        self,
        compost_bin: CompostBin,
        pipeline: CompostingPipeline,
        schedule: Optional[CompostingSchedule] = None,
        object_loader: Optional[Callable[[CompostBinEntry], Any]] = None,
    ):
        """
        Initialize the scheduler.

        Args:
            compost_bin: The bin containing items to compost
            pipeline: Pipeline to process composted items
            schedule: Schedule configuration (uses defaults if None)
            object_loader: Optional function to load full objects from entries
        """
        self.compost_bin = compost_bin
        self.pipeline = pipeline
        self.schedule = schedule or CompostingSchedule()
        self.object_loader = object_loader

        self.last_run: Optional[datetime] = None
        # #669: baseline for the overdue (hybrid-trigger) check before the first
        # run establishes last_run, so a never-yet-composted scheduler still
        # force-composts once max_hours_since_last_run elapses since startup.
        self._created_at: datetime = datetime.now()

    async def maybe_run(
        self,
        current_time: Optional[datetime] = None,
        user_id: str = "",
    ) -> Optional[CompostingRunResult]:
        """
        Check if should run, and run if conditions are met.

        Args:
            current_time: Time to check against (default: now)
            user_id: User ID to associate with learnings

        Returns:
            CompostingRunResult if run, None if skipped
        """
        current_time = current_time or datetime.now()

        if not self._should_run(current_time):
            logger.debug(
                "composting_skipped",
                extra={
                    "reason": "conditions_not_met",
                    "current_hour": current_time.hour,
                    "pending_count": len(self.compost_bin.pending),
                },
            )
            return None

        return await self.run(user_id=user_id)

    async def run(
        self,
        force: bool = False,
        user_id: str = "",
    ) -> CompostingRunResult:
        """
        Run a composting cycle.

        Args:
            force: If True, skip condition checks
            user_id: User ID to associate with learnings

        Returns:
            CompostingRunResult with details of what was processed
        """
        start_time = datetime.now()
        self.compost_bin.is_composting = True

        try:
            # Get entries to process
            entries = self.compost_bin.get_ready(limit=self.schedule.max_batch)

            if not entries and not force:
                return CompostingRunResult(
                    processed_count=0,
                    run_at=start_time,
                )

            results: List[Tuple[CompostBinEntry, List[ExtractedLearning]]] = []
            errors: List[str] = []

            for entry in entries:
                try:
                    obj = await self._load_object(entry)
                    learnings = await self.pipeline.process(
                        obj,
                        user_id=user_id,
                        trigger=entry.trigger,
                    )

                    # Apply consciousness-preserving framing
                    for learning in learnings:
                        learning.expression = frame_learning(learning)

                    results.append((entry, learnings))
                    self.compost_bin.remove(entry.object_id)

                except Exception as e:
                    error_msg = f"Failed to process {entry.object_id}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(
                        "composting_entry_failed",
                        extra={
                            "object_id": entry.object_id,
                            "error": str(e),
                        },
                    )

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            # Collect learning types
            all_learnings = [learning for _, ls in results for learning in ls]
            learning_types = [learning.learning_type for learning in all_learnings]

            result = CompostingRunResult(
                processed_count=len(results),
                object_ids=[e.object_id for e, _ in results],
                learnings_extracted=len(all_learnings),
                learning_types=learning_types,
                run_at=start_time,
                duration_seconds=duration,
                success=len(errors) == 0,
                errors=errors,
            )

            self.last_run = start_time
            self.compost_bin.last_composted = start_time

            logger.info(
                "composting_run_complete",
                extra=result.to_dict(),
            )

            return result

        finally:
            self.compost_bin.is_composting = False

    async def _load_object(self, entry: CompostBinEntry) -> Any:
        """
        Load the full object from an entry.

        Uses the custom object_loader if provided, otherwise
        falls back to the entry's object_ref.
        """
        if self.object_loader:
            return await self.object_loader(entry)

        if entry.object_ref is not None:
            return entry.object_ref

        # Return a minimal mock object for processing
        return MockCompostableObject(
            id=entry.object_id,
            object_type=entry.object_type,
        )

    def _should_run(self, current_time: Optional[datetime] = None) -> bool:
        """
        Check if conditions are right for running.

        Conditions:
        1. Must not already be composting
        2. #669 hybrid trigger: if OVERDUE (too long since last run) and there is
           pending work, force a cycle regardless of conditions 3-5.
        3. Must be quiet hour
        4. Must have minimum pending items
        5. Must have passed minimum interval since last run
        """
        current_time = current_time or datetime.now()

        # Already composting
        if self.compost_bin.is_composting:
            return False

        # #669 hybrid trigger: if we're overdue (too long since the last run),
        # force a cycle regardless of quiet-hours / min_pending / min_interval —
        # as long as there is work to do. Prevents starvation when the normal
        # quiet-hour + min_pending conjunction is never met (insomniac case).
        if len(self.compost_bin.pending) > 0 and self._is_overdue(current_time):
            return True

        # Not quiet hour
        if not self.schedule.is_quiet_now(current_time):
            return False

        # Not enough pending
        if len(self.compost_bin.pending) < self.schedule.min_pending:
            return False

        # Too recent
        if self.last_run is not None:
            hours_since = (current_time - self.last_run).total_seconds() / 3600
            if hours_since < self.schedule.min_interval_hours:
                return False

        return True

    def _is_overdue(self, current_time: datetime) -> bool:
        """#669: True when at least ``max_hours_since_last_run`` has elapsed since
        the last run (or, before the first run, since the scheduler started).

        Disabled (returns False) when ``max_hours_since_last_run`` is None or <= 0.
        Callers still require pending work before forcing a cycle.
        """
        max_hours = self.schedule.max_hours_since_last_run
        if max_hours is None or max_hours <= 0:
            return False
        reference = self.last_run or self._created_at
        hours_since = (current_time - reference).total_seconds() / 3600
        return hours_since >= max_hours

    @property
    def is_running(self) -> bool:
        """Check if currently running a composting cycle."""
        return self.compost_bin.is_composting

    @property
    def pending_count(self) -> int:
        """Number of items waiting to be composted."""
        return len(self.compost_bin.pending)


# =============================================================================
# Helper Classes
# =============================================================================


@dataclass
class MockCompostableObject:
    """
    Minimal object for when only ID is available.

    Used when the CompostBin entry doesn't have an object_ref
    and no custom object_loader is provided.
    """

    id: str
    object_type: str = "unknown"
    created_at: datetime = field(default_factory=datetime.now)
    lifecycle_state: Optional[str] = None
    lifecycle_history: List = field(default_factory=list)
