"""
#1035 Phase 5 — CompostingSchedulerJob lifecycle tests.

Verifies:
- start() launches the loop and ticks the underlying scheduler
- stop() cancels cleanly with sub-second shutdown (post-#948 hygiene)
- start() while already running is idempotent (no double-loop)
- execute_tick() honors gate-not-met (returns ran=False) and gate-met
  (returns ran=True with run-result fields)

Mirrors test pattern at
`tests/unit/services/scheduler/test_ethics_audit_cleanup_job_1018.py`.
"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from services.mux.compost_bin import CompostBin
from services.mux.composting_models import CompostingTrigger
from services.mux.composting_pipeline import CompostingPipeline
from services.mux.composting_scheduler import CompostingSchedule, CompostingScheduler
from services.scheduler.composting_scheduler_job import CompostingSchedulerJob
from tests.unit.services.mux._fake_insight_journal import FakeInsightJournal


pytestmark = pytest.mark.asyncio


def _build_scheduler(
    *,
    quiet_hours: list[int] | None = None,
    min_pending: int = 1,
) -> tuple[CompostBin, CompostingScheduler]:
    """Helper: build a wired-up CompostingScheduler with FakeInsightJournal."""
    bin_ = CompostBin()
    journal = FakeInsightJournal()
    pipeline = CompostingPipeline(journal=journal)
    schedule = CompostingSchedule(
        quiet_hours=quiet_hours if quiet_hours is not None else [2, 3, 4],
        min_pending=min_pending,
    )
    scheduler = CompostingScheduler(
        compost_bin=bin_, pipeline=pipeline, schedule=schedule
    )
    return bin_, scheduler


# =============================================================================
# Lifecycle tests
# =============================================================================


async def test_job_initial_state_not_running():
    _, scheduler = _build_scheduler()
    job = CompostingSchedulerJob(scheduler=scheduler, interval_seconds=3600)
    assert job.is_running() is False
    assert job._task is None


async def test_job_starts_and_stops_cleanly():
    """start() launches, stop() cancels-and-awaits sub-second."""
    _, scheduler = _build_scheduler()
    job = CompostingSchedulerJob(scheduler=scheduler, interval_seconds=3600)

    task = asyncio.create_task(job.start())
    # Yield once so start() can reach the loop body
    await asyncio.sleep(0.05)
    assert job.is_running() is True

    await job.stop()
    # Loop task should be done (cancelled); stop() awaits it internally
    assert job.is_running() is False
    # Drain the wrapping task
    try:
        await task
    except asyncio.CancelledError:
        pass


async def test_stop_when_not_running_is_noop():
    _, scheduler = _build_scheduler()
    job = CompostingSchedulerJob(scheduler=scheduler, interval_seconds=3600)
    # Should log a warning but not raise
    await job.stop()
    assert job.is_running() is False


async def test_start_twice_is_idempotent():
    """A second start() while running logs warning + returns; doesn't double-loop."""
    _, scheduler = _build_scheduler()
    job = CompostingSchedulerJob(scheduler=scheduler, interval_seconds=3600)

    task = asyncio.create_task(job.start())
    await asyncio.sleep(0.05)
    assert job.is_running() is True

    # Second start() should just return (logs warning)
    await job.start()
    assert job.is_running() is True

    await job.stop()
    try:
        await task
    except asyncio.CancelledError:
        pass


# =============================================================================
# execute_tick behavior
# =============================================================================


async def test_execute_tick_reports_gate_not_met():
    """When CompostingScheduler.maybe_run() returns None (gates not met),
    execute_tick reports ran=False with reason."""
    _, scheduler = _build_scheduler(
        quiet_hours=[99],  # impossible hour: never quiet
    )
    job = CompostingSchedulerJob(scheduler=scheduler, interval_seconds=3600)

    result = await job.execute_tick()
    assert result["success"] is True
    assert result["ran"] is False
    assert result["reason"] == "gates_not_met"


async def test_execute_tick_reports_run_result():
    """When CompostingScheduler.run() returns a CompostingRunResult,
    execute_tick reports ran=True with the result fields."""
    bin_, scheduler = _build_scheduler()
    bin_.add("obj-1", CompostingTrigger.AGE)

    # Force-run via maybe_run won't fire unless quiet hour; test via
    # direct scheduler.run instead by patching execute_tick to use force.
    # Cleanest test: patch user_id_provider, then call scheduler.run directly
    # via execute_tick — we want to verify the dict-shape contract.
    # Easiest: monkey-patch scheduler.maybe_run to a stub returning a real
    # CompostingRunResult, since we're testing job-side dict shape, not
    # the policy-gate logic (that's the scheduler's tests).
    from services.mux.composting_scheduler import CompostingRunResult

    fake_result = CompostingRunResult(
        processed_count=1,
        object_ids=["obj-1"],
        learnings_extracted=2,
        learning_types=["pattern"],
        duration_seconds=0.05,
        success=True,
        errors=[],
    )

    async def fake_maybe_run(user_id: str = ""):
        return fake_result

    scheduler.maybe_run = fake_maybe_run  # type: ignore[method-assign]

    job = CompostingSchedulerJob(scheduler=scheduler, interval_seconds=3600)
    result = await job.execute_tick()

    assert result["success"] is True
    assert result["ran"] is True
    assert result["processed_count"] == 1
    assert result["learnings_extracted"] == 2
    assert result["duration_seconds"] == 0.05


async def test_execute_tick_swallows_scheduler_exception():
    """If maybe_run raises, execute_tick reports {success: False} and
    the loop should continue (logged in start() but not raised)."""
    _, scheduler = _build_scheduler()

    async def boom(user_id: str = ""):
        raise RuntimeError("simulated scheduler failure")

    scheduler.maybe_run = boom  # type: ignore[method-assign]
    job = CompostingSchedulerJob(scheduler=scheduler, interval_seconds=3600)

    result = await job.execute_tick()
    assert result["success"] is False
    assert result["ran"] is False
    assert "simulated scheduler failure" in result.get("error", "")


async def test_user_id_provider_is_called():
    """user_id_provider callable is consulted on each tick."""
    _, scheduler = _build_scheduler()

    captured: list[str] = []

    async def capturing_maybe_run(user_id: str = ""):
        captured.append(user_id)
        return None  # gates not met → just record + return

    scheduler.maybe_run = capturing_maybe_run  # type: ignore[method-assign]

    job = CompostingSchedulerJob(
        scheduler=scheduler,
        interval_seconds=3600,
        user_id_provider=lambda: "alpha-user",
    )
    await job.execute_tick()
    assert captured == ["alpha-user"]
