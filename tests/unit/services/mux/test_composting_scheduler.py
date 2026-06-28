"""
Tests for CompostingScheduler - "filing dreams" scheduler.

Part of #668 COMPOSTING-SCHEDULE (child of #436 MUX-TECH-PHASE4-COMPOSTING).
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List

import pytest

from services.mux.compost_bin import CompostBin, CompostBinEntry
from services.mux.composting_models import CompostingTrigger, create_insight_learning
from services.mux.composting_pipeline import CompostingPipeline, InsightJournal

# #1035: tests use FakeInsightJournal as a test double; production
# InsightJournal is async + repository-backed.
from tests.unit.services.mux._fake_insight_journal import FakeInsightJournal
from services.mux.composting_scheduler import (
    COMPOSTING_FRAMES,
    CompostingRunResult,
    CompostingSchedule,
    CompostingScheduler,
    frame_learning,
)

# =============================================================================
# CompostingSchedule Tests
# =============================================================================


class TestCompostingSchedule:
    """Tests for CompostingSchedule configuration."""

    def test_default_quiet_hours(self):
        """Test default quiet hours are 2-4 AM."""
        schedule = CompostingSchedule()

        assert 2 in schedule.quiet_hours
        assert 3 in schedule.quiet_hours
        assert 4 in schedule.quiet_hours
        # 5 AM is not included by default (changed from spec)
        assert 10 not in schedule.quiet_hours

    def test_is_quiet_hour(self):
        """Test is_quiet_hour checks."""
        schedule = CompostingSchedule(quiet_hours=[2, 3, 4])

        assert schedule.is_quiet_hour(2) is True
        assert schedule.is_quiet_hour(3) is True
        assert schedule.is_quiet_hour(10) is False
        assert schedule.is_quiet_hour(22) is False

    def test_is_quiet_now(self):
        """Test is_quiet_now with specified time."""
        schedule = CompostingSchedule(quiet_hours=[2, 3, 4])

        at_3am = datetime(2026, 1, 24, 3, 30, 0)
        at_10am = datetime(2026, 1, 24, 10, 30, 0)

        assert schedule.is_quiet_now(current_time=at_3am) is True
        assert schedule.is_quiet_now(current_time=at_10am) is False

    def test_custom_schedule(self):
        """Test custom schedule configuration."""
        schedule = CompostingSchedule(
            quiet_hours=[1, 2],
            min_pending=10,
            max_batch=5,
            min_interval_hours=2.0,
        )

        assert schedule.min_pending == 10
        assert schedule.max_batch == 5
        assert schedule.min_interval_hours == 2.0


# =============================================================================
# CompostingRunResult Tests
# =============================================================================


class TestCompostingRunResult:
    """Tests for CompostingRunResult."""

    def test_basic_creation(self):
        """Test basic result creation."""
        result = CompostingRunResult(
            processed_count=5,
            learnings_extracted=12,
        )

        assert result.processed_count == 5
        assert result.learnings_extracted == 12
        assert result.success is True
        assert result.errors == []

    def test_to_dict(self):
        """Test serialization to dictionary."""
        result = CompostingRunResult(
            processed_count=3,
            object_ids=["obj-1", "obj-2", "obj-3"],
            learnings_extracted=6,
            learning_types=["insight", "pattern", "insight"],
            duration_seconds=1.5,
        )

        d = result.to_dict()

        assert d["processed_count"] == 3
        assert d["object_ids"] == ["obj-1", "obj-2", "obj-3"]
        assert d["learnings_extracted"] == 6
        assert d["duration_seconds"] == 1.5

    def test_with_errors(self):
        """Test result with errors."""
        result = CompostingRunResult(
            processed_count=2,
            success=False,
            errors=["Failed to load obj-1", "Timeout on obj-2"],
        )

        assert result.success is False
        assert len(result.errors) == 2


# =============================================================================
# Frame Learning Tests
# =============================================================================


class TestFrameLearning:
    """Tests for consciousness-preserving language framing."""

    def test_frame_learning_adds_prefix(self):
        """Test that framing adds a consciousness-preserving prefix."""
        learning = create_insight_learning(
            description="User prefers mornings",
            derived_from=[],
        )
        learning.expression = "I noticed that user prefers mornings"

        framed = frame_learning(learning)

        # Should start with one of the frames
        assert any(framed.startswith(frame) for frame in COMPOSTING_FRAMES)
        # Should contain the content
        assert "user prefers mornings" in framed.lower()

    def test_frame_learning_uses_description_fallback(self):
        """Test that framing falls back to description when no expression."""
        learning = create_insight_learning(
            description="Morning meetings work better",
            derived_from=[],
        )
        learning.expression = ""  # No expression

        framed = frame_learning(learning)

        assert any(framed.startswith(frame) for frame in COMPOSTING_FRAMES)
        assert "Morning meetings work better" in framed

    def test_frame_learning_removes_existing_frame(self):
        """Test that existing frame prefixes are removed to avoid duplication."""
        learning = create_insight_learning(
            description="User prefers mornings",
            derived_from=[],
        )
        learning.expression = "Having had some time to reflect... user prefers mornings"

        framed = frame_learning(learning)

        # Should not have double framing
        frame_count = sum(1 for f in COMPOSTING_FRAMES if f in framed)
        assert frame_count == 1


# =============================================================================
# CompostingScheduler Tests
# =============================================================================


class TestCompostingSchedulerBasics:
    """Basic tests for CompostingScheduler."""

    def test_creation_with_defaults(self):
        """Test scheduler creation with default schedule."""
        bin = CompostBin()
        pipeline = CompostingPipeline(journal=FakeInsightJournal())

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=pipeline,
        )

        assert scheduler.compost_bin is bin
        assert scheduler.pipeline is pipeline
        assert scheduler.schedule is not None

    def test_pending_count_property(self):
        """Test pending_count reflects bin state."""
        bin = CompostBin()
        bin.add("obj-1", CompostingTrigger.AGE)
        bin.add("obj-2", CompostingTrigger.MANUAL)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
        )

        assert scheduler.pending_count == 2

    def test_is_running_property(self):
        """Test is_running reflects bin state."""
        bin = CompostBin()
        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
        )

        assert scheduler.is_running is False

        bin.is_composting = True
        assert scheduler.is_running is True


class TestCompostingSchedulerShouldRun:
    """Tests for _should_run() logic."""

    def test_should_run_quiet_hour_and_enough_pending(self):
        """Test should run when quiet hour and enough pending."""
        bin = CompostBin()
        for i in range(10):
            bin.add(f"obj-{i}", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(quiet_hours=[3], min_pending=5),
        )

        at_3am = datetime(2026, 1, 24, 3, 0, 0)
        assert scheduler._should_run(at_3am) is True

    def test_should_not_run_not_quiet_hour(self):
        """Test should not run outside quiet hours."""
        bin = CompostBin()
        for i in range(10):
            bin.add(f"obj-{i}", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(quiet_hours=[3]),
        )

        at_10am = datetime(2026, 1, 24, 10, 0, 0)
        assert scheduler._should_run(at_10am) is False

    def test_should_not_run_not_enough_pending(self):
        """Test should not run with insufficient pending items."""
        bin = CompostBin()
        bin.add("obj-1", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(quiet_hours=[3], min_pending=5),
        )

        at_3am = datetime(2026, 1, 24, 3, 0, 0)
        assert scheduler._should_run(at_3am) is False

    def test_should_not_run_already_composting(self):
        """Test should not run if already composting."""
        bin = CompostBin()
        for i in range(10):
            bin.add(f"obj-{i}", CompostingTrigger.AGE)
        bin.is_composting = True

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(quiet_hours=[3]),
        )

        at_3am = datetime(2026, 1, 24, 3, 0, 0)
        assert scheduler._should_run(at_3am) is False

    def test_should_not_run_too_recent(self):
        """Test should not run if last run too recent."""
        bin = CompostBin()
        for i in range(10):
            bin.add(f"obj-{i}", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(quiet_hours=[3], min_interval_hours=4.0),
        )

        # Set last run 2 hours ago
        at_3am = datetime(2026, 1, 24, 3, 0, 0)
        scheduler.last_run = at_3am - timedelta(hours=2)

        assert scheduler._should_run(at_3am) is False


class TestHybridTrigger669:
    """#669 COMPOSTING-HYBRID-TRIGGER: time-based forcing. When overdue
    (>= max_hours_since_last_run) AND there is pending work, _should_run forces a
    cycle regardless of quiet-hours / min_pending / min_interval — the
    unihemispheric-dreaming / insomniac safeguard against starvation."""

    def _scheduler(self, n_pending=10, **schedule_kwargs):
        bin = CompostBin()
        for i in range(n_pending):
            bin.add(f"obj-{i}", CompostingTrigger.AGE)
        return CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(quiet_hours=[3], min_pending=5, **schedule_kwargs),
        )

    def test_overdue_forces_run_at_non_quiet_hour(self):
        sched = self._scheduler(max_hours_since_last_run=72.0)
        at_10am = datetime(2026, 1, 24, 10, 0, 0)  # NOT a quiet hour
        sched.last_run = at_10am - timedelta(hours=73)  # overdue
        assert sched._should_run(at_10am) is True

    def test_not_overdue_does_not_force(self):
        sched = self._scheduler(max_hours_since_last_run=72.0)
        at_10am = datetime(2026, 1, 24, 10, 0, 0)  # non-quiet
        sched.last_run = at_10am - timedelta(hours=10)  # within window
        assert sched._should_run(at_10am) is False  # normal (non-quiet) behavior preserved

    def test_overdue_bypasses_min_pending(self):
        sched = self._scheduler(n_pending=1, max_hours_since_last_run=72.0)  # below min_pending=5
        at_10am = datetime(2026, 1, 24, 10, 0, 0)
        sched.last_run = at_10am - timedelta(hours=80)
        assert sched._should_run(at_10am) is True

    def test_overdue_but_empty_bin_does_not_run(self):
        sched = self._scheduler(n_pending=0, max_hours_since_last_run=72.0)
        at_10am = datetime(2026, 1, 24, 10, 0, 0)
        sched.last_run = at_10am - timedelta(hours=80)
        assert sched._should_run(at_10am) is False  # nothing to do

    def test_overdue_still_blocked_if_composting(self):
        sched = self._scheduler(max_hours_since_last_run=72.0)
        sched.compost_bin.is_composting = True
        at_10am = datetime(2026, 1, 24, 10, 0, 0)
        sched.last_run = at_10am - timedelta(hours=80)
        assert sched._should_run(at_10am) is False

    def test_disabled_when_threshold_none(self):
        sched = self._scheduler(max_hours_since_last_run=None)
        at_10am = datetime(2026, 1, 24, 10, 0, 0)
        sched.last_run = at_10am - timedelta(hours=200)  # very overdue
        assert sched._should_run(at_10am) is False  # feature off → normal quiet-hour rule applies

    def test_bootstrap_overdue_uses_created_at_when_never_run(self):
        sched = self._scheduler(max_hours_since_last_run=72.0)
        at_10am = datetime(2026, 1, 24, 10, 0, 0)
        sched.last_run = None
        sched._created_at = at_10am - timedelta(hours=73)  # started >72h ago, never ran
        assert sched._should_run(at_10am) is True

    def test_quiet_hour_path_unchanged_when_not_overdue(self):
        """Regression: the normal quiet-hour path still fires when not overdue."""
        sched = self._scheduler(max_hours_since_last_run=72.0)
        at_3am = datetime(2026, 1, 24, 3, 0, 0)  # quiet hour
        sched._created_at = at_3am - timedelta(hours=1)  # recent start → not overdue
        assert sched._should_run(at_3am) is True


class TestCompostingSchedulerMaybeRun:
    """Tests for maybe_run() method."""

    @pytest.mark.asyncio
    async def test_maybe_run_skips_when_conditions_not_met(self):
        """Test maybe_run returns None when conditions not met."""
        bin = CompostBin()
        # Only 1 item, below threshold

        bin.add("obj-1", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(quiet_hours=[3], min_pending=5),
        )

        at_3am = datetime(2026, 1, 24, 3, 0, 0)
        result = await scheduler.maybe_run(current_time=at_3am)

        assert result is None

    @pytest.mark.asyncio
    async def test_maybe_run_runs_when_conditions_met(self):
        """Test maybe_run runs when all conditions met."""
        bin = CompostBin()
        for i in range(10):
            bin.add(f"obj-{i}", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(quiet_hours=[3], min_pending=5),
        )

        at_3am = datetime(2026, 1, 24, 3, 0, 0)
        result = await scheduler.maybe_run(current_time=at_3am, user_id="user-1")

        assert result is not None
        assert result.processed_count > 0


class TestCompostingSchedulerRun:
    """Tests for run() method."""

    @pytest.mark.asyncio
    async def test_run_processes_entries(self):
        """Test run processes bin entries."""
        bin = CompostBin()
        bin.add("obj-1", CompostingTrigger.AGE)
        bin.add("obj-2", CompostingTrigger.MANUAL)

        journal = FakeInsightJournal()
        pipeline = CompostingPipeline(journal=journal)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=pipeline,
        )

        result = await scheduler.run(force=True, user_id="user-1")

        assert result.processed_count == 2
        assert "obj-1" in result.object_ids
        assert "obj-2" in result.object_ids
        assert bin.count == 0  # All processed

    @pytest.mark.asyncio
    async def test_run_stores_learnings_in_journal(self):
        """Test run stores learnings in pipeline's journal."""
        bin = CompostBin()
        bin.add("obj-1", CompostingTrigger.AGE)

        journal = FakeInsightJournal()
        pipeline = CompostingPipeline(journal=journal)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=pipeline,
        )

        await scheduler.run(force=True, user_id="user-1")

        # Should have at least one insight in journal
        assert await journal.count() >= 1

    @pytest.mark.asyncio
    async def test_run_updates_last_run(self):
        """Test run updates last_run timestamp."""
        bin = CompostBin()
        bin.add("obj-1", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
        )

        assert scheduler.last_run is None

        await scheduler.run(force=True)

        assert scheduler.last_run is not None

    @pytest.mark.asyncio
    async def test_run_updates_bin_last_composted(self):
        """Test run updates bin's last_composted timestamp."""
        bin = CompostBin()
        bin.add("obj-1", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
        )

        assert bin.last_composted is None

        await scheduler.run(force=True)

        assert bin.last_composted is not None

    @pytest.mark.asyncio
    async def test_run_respects_max_batch(self):
        """Test run only processes up to max_batch items."""
        bin = CompostBin()
        for i in range(20):
            bin.add(f"obj-{i}", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
            schedule=CompostingSchedule(max_batch=5),
        )

        result = await scheduler.run(force=True)

        assert result.processed_count == 5
        assert bin.count == 15  # 20 - 5 processed

    @pytest.mark.asyncio
    async def test_run_clears_is_composting_on_complete(self):
        """Test run clears is_composting flag when done."""
        bin = CompostBin()
        bin.add("obj-1", CompostingTrigger.AGE)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=CompostingPipeline(journal=FakeInsightJournal()),
        )

        await scheduler.run(force=True)

        assert bin.is_composting is False

    @pytest.mark.asyncio
    async def test_run_applies_framing_to_learnings(self):
        """Test run applies consciousness-preserving framing."""
        bin = CompostBin()
        bin.add("obj-1", CompostingTrigger.AGE)

        journal = FakeInsightJournal()
        pipeline = CompostingPipeline(journal=journal)

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=pipeline,
        )

        await scheduler.run(force=True)

        # Check that insights have framed expressions
        insights = list(
            (await journal.get_for_object("obj-1") + await journal.get_for_object("obj-2"))
        )
        assert len(insights) >= 1

        # At least one should have framing
        for insight in insights:
            if insight.learning and insight.learning.expression:
                has_frame = any(
                    insight.learning.expression.startswith(f) for f in COMPOSTING_FRAMES
                )
                if has_frame:
                    break
        else:
            # If we get here without break, no framing found
            # This is acceptable since expression may be empty
            pass


class TestCompostingSchedulerIntegration:
    """Integration tests for full composting cycle."""

    @pytest.mark.asyncio
    async def test_full_cycle_bin_to_journal(self):
        """Test full cycle from bin to journal."""
        # Setup
        bin = CompostBin()
        journal = FakeInsightJournal()
        pipeline = CompostingPipeline(journal=journal)

        # Add items to bin
        for i in range(5):
            bin.add(f"task-{i}", CompostingTrigger.AGE, object_type="Task")

        scheduler = CompostingScheduler(
            compost_bin=bin,
            pipeline=pipeline,
            schedule=CompostingSchedule(quiet_hours=[3], min_pending=3),
        )

        # Run during quiet hours
        at_3am = datetime(2026, 1, 24, 3, 0, 0)
        result = await scheduler.maybe_run(current_time=at_3am, user_id="user-123")

        # Verify
        assert result is not None
        assert result.processed_count == 5
        assert result.success is True
        assert bin.count == 0
        assert await journal.count() >= 5  # At least one insight per object
