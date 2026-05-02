"""
#1018 Phase 2 — EthicsAuditCleanupJob lifecycle tests.

Mirrors `test_948_orphan_cleanup.py` shape: verifies that start() captures
the wrapping task and stop() cancels-and-awaits cleanly, so shutdown is
sub-second instead of waiting up to a 5-minute sleep chunk.

DB-free: `execute_cleanup` is patched to a no-op so we don't need a live
PostgreSQL connection.
"""

from __future__ import annotations

import asyncio

import pytest


pytestmark = pytest.mark.asyncio


@pytest.mark.asyncio
async def test_cleanup_job_stop_cancels_wrapping_task_immediately():
    """Pre-#948 pattern: stop() set flag and slept; loop mid-sleep(300)
    didn't notice. Post-#948 pattern (applied here): stop() cancels +
    awaits the captured task; sub-second return."""
    from services.scheduler.ethics_audit_cleanup_job import EthicsAuditCleanupJob

    job = EthicsAuditCleanupJob(interval_hours=24, retention_days=90)

    async def _noop_cleanup():
        return {"success": True, "removed": 0}

    job.execute_cleanup = _noop_cleanup  # type: ignore[assignment]

    task = asyncio.create_task(job.start())
    for _ in range(20):
        await asyncio.sleep(0.01)
        if job.is_running():
            break
    assert job.is_running()

    await asyncio.wait_for(job.stop(), timeout=2.0)

    assert task.done(), "wrapping task should be done after stop()"
    assert not job.is_running()


@pytest.mark.asyncio
async def test_cleanup_job_stop_idempotent_when_not_running():
    from services.scheduler.ethics_audit_cleanup_job import EthicsAuditCleanupJob

    job = EthicsAuditCleanupJob()
    await asyncio.wait_for(job.stop(), timeout=1.0)
    assert not job.is_running()


@pytest.mark.asyncio
async def test_cleanup_job_get_status_reports_running_state():
    from services.scheduler.ethics_audit_cleanup_job import EthicsAuditCleanupJob

    job = EthicsAuditCleanupJob(interval_hours=12, retention_days=30)
    status = job.get_status()
    assert status["running"] is False
    assert status["interval_hours"] == 12
    assert status["retention_days"] == 30
