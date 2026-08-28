"""
#948 — Verify background jobs cancel cleanly on stop().

Pre-fix bug: stop() set a flag and slept 0.1s; meanwhile the wrapping task
was mid-asyncio.sleep(60) (or 300 for blacklist cleanup) and didn't notice
the flag for up to a minute. Uvicorn tore down the event loop with the
wrapping task still pending → orphan task warnings + incomplete cleanup.

Fix: each job captures asyncio.current_task() in start(); stop() cancels
+ awaits that task, returning only when the task is actually done.
"""

from __future__ import annotations

import asyncio

import pytest

pytestmark = pytest.mark.asyncio


# ----- AttentionDecayJob -----


@pytest.mark.asyncio
async def test_attention_decay_job_stop_cancels_wrapping_task_immediately():
    """The pre-fix bug: stop() returned in 0.1s but the loop was mid-
    asyncio.sleep(60) and stayed pending. Post-fix: stop() cancels and
    awaits, so the wrapping task is done() by the time stop() returns."""
    from services.scheduler.attention_decay_job import AttentionDecayJob

    class _StubAttentionModel:
        async def update_decay_for_active_users(self):
            return {"users_updated": 0}

    job = AttentionDecayJob(
        attention_model=_StubAttentionModel(),
        interval_minutes=5,  # would imply up to 5 chunks of asyncio.sleep(60)
    )

    # Start the job and let it advance past the first execute_decay_update
    # into the sleep loop.
    task = asyncio.create_task(job.start())
    # Give the event loop time to enter start() and reach the sleep.
    for _ in range(20):
        await asyncio.sleep(0.01)
        if job.is_running():
            break
    assert job.is_running(), "job should be running"

    # Stop the job. Pre-fix this would sleep 0.1s and return; the wrapping
    # task would still be pending. Post-fix: stop() cancels + awaits.
    await asyncio.wait_for(job.stop(), timeout=2.0)

    # The wrapping task should now be done (cancelled).
    assert task.done(), "wrapping task should be done after stop()"
    assert not job.is_running()


@pytest.mark.asyncio
async def test_attention_decay_job_stop_idempotent_when_not_running():
    """stop() called when not running is a no-op, not an error."""
    from services.scheduler.attention_decay_job import AttentionDecayJob

    class _StubAttentionModel:
        async def update_decay_for_active_users(self):
            return {"users_updated": 0}

    job = AttentionDecayJob(attention_model=_StubAttentionModel())
    # Never started; stop() should return cleanly.
    await asyncio.wait_for(job.stop(), timeout=1.0)
    assert not job.is_running()


# ----- BlacklistCleanupJob -----


@pytest.mark.asyncio
async def test_blacklist_cleanup_job_stop_cancels_wrapping_task_immediately():
    """Pre-fix: stop() referenced self._task without ever assigning it
    (dead code), so the await-task block never ran; wrapping task was
    left pending. Post-fix: start() captures the task, stop() cancels it."""
    from services.scheduler.blacklist_cleanup_job import BlacklistCleanupJob

    job = BlacklistCleanupJob(interval_hours=24)

    # Patch execute_cleanup to be a no-op so the loop reaches sleep quickly
    async def _noop_cleanup():
        return {"success": True, "removed": 0}

    job.execute_cleanup = _noop_cleanup  # type: ignore[assignment]

    task = asyncio.create_task(job.start())
    for _ in range(20):
        await asyncio.sleep(0.01)
        if job.is_running():
            break
    assert job.is_running(), "job should be running"

    await asyncio.wait_for(job.stop(), timeout=2.0)

    assert task.done(), "wrapping task should be done after stop()"
    assert not job.is_running()


@pytest.mark.asyncio
async def test_blacklist_cleanup_job_stop_idempotent_when_not_running():
    from services.scheduler.blacklist_cleanup_job import BlacklistCleanupJob

    job = BlacklistCleanupJob(interval_hours=24)
    await asyncio.wait_for(job.stop(), timeout=1.0)
    assert not job.is_running()


# ----- Integration: lifespan-shape shutdown -----


@pytest.mark.asyncio
async def test_lifespan_shape_shutdown_completes_within_seconds():
    """End-to-end: simulate the shutdown phase calling stop() on both jobs
    in sequence (as web/startup.py does). Total shutdown should be sub-
    second post-fix; pre-fix it could take up to 5 minutes (blacklist
    sleep chunk) before the wrapping task noticed the flag."""
    from services.scheduler.attention_decay_job import AttentionDecayJob
    from services.scheduler.blacklist_cleanup_job import BlacklistCleanupJob

    class _StubAttentionModel:
        async def update_decay_for_active_users(self):
            return {"users_updated": 0}

    decay_job = AttentionDecayJob(attention_model=_StubAttentionModel())
    cleanup_job = BlacklistCleanupJob(interval_hours=24)

    async def _noop_cleanup():
        return {"success": True, "removed": 0}

    cleanup_job.execute_cleanup = _noop_cleanup  # type: ignore[assignment]

    decay_task = asyncio.create_task(decay_job.start())
    cleanup_task = asyncio.create_task(cleanup_job.start())

    # Let both reach their sleep loops
    for _ in range(40):
        await asyncio.sleep(0.01)
        if decay_job.is_running() and cleanup_job.is_running():
            break
    assert decay_job.is_running() and cleanup_job.is_running()

    # Shut down (lifespan.shutdown calls these in reverse order)
    loop = asyncio.get_event_loop()
    t0 = loop.time()
    await asyncio.wait_for(decay_job.stop(), timeout=2.0)
    await asyncio.wait_for(cleanup_job.stop(), timeout=2.0)
    elapsed = loop.time() - t0

    assert decay_task.done()
    assert cleanup_task.done()
    # Sub-second shutdown is the regression target. Pre-fix could be
    # up to interval_minutes * 60 seconds for decay job; up to
    # interval_hours * 3600 / chunks for cleanup.
    assert elapsed < 1.0, f"shutdown took {elapsed:.3f}s; expected <1s"
