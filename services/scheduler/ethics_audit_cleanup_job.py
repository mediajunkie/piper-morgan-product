"""
Issue #1018 Phase 2: Scheduled retention sweep for ethics audit log.

Replaces the legacy on-demand `audit_transparency.cleanup_old_entries()`
in-memory list cleanup with a scheduled DB DELETE on the
`ethics_audit_log` table. 90-day TTL preserved.

Pattern follows `services/scheduler/blacklist_cleanup_job.py` exactly,
including the post-#948 task-cancellation hygiene
(`asyncio.current_task()` capture in `start()` + cancel-and-await in
`stop()`).
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import structlog

logger = structlog.get_logger()


class EthicsAuditCleanupJob:
    """Periodic retention sweep on the `ethics_audit_log` table.

    Default cadence: every 24 hours; deletes entries with
    `timestamp < (now - retention_days)`. Mirrors `BlacklistCleanupJob`
    shape so the lifespan startup/shutdown wiring is identical.
    """

    def __init__(self, interval_hours: int = 24, retention_days: int = 90):
        self.interval_hours = interval_hours
        self.retention_days = retention_days
        self._running = False
        self._task: Optional[asyncio.Task] = None
        logger.info(
            "EthicsAuditCleanupJob initialized",
            interval_hours=interval_hours,
            retention_days=retention_days,
        )

    async def execute_cleanup(self) -> Dict[str, Any]:
        """Run one cleanup sweep. Returns status dict."""
        try:
            from services.database.repositories import EthicsAuditRepository
            from services.database.session_factory import AsyncSessionFactory

            cutoff = datetime.now(timezone.utc) - timedelta(days=self.retention_days)
            async with AsyncSessionFactory.session_scope() as session:
                repo = EthicsAuditRepository(session)
                removed = await repo.delete_older_than(cutoff)
                await session.commit()
            return {
                "success": True,
                "removed": removed,
                "cutoff": cutoff.isoformat(),
            }
        except Exception as e:
            logger.error("EthicsAuditCleanupJob.execute_cleanup failed", error=str(e))
            return {"success": False, "error": str(e), "removed": 0}

    async def start(self) -> None:
        """Run the cleanup loop until stop() is called.

        Captures `asyncio.current_task()` in `_task` so `stop()` can
        cancel cleanly without waiting for the sleep chunk to notice
        the `_running` flag (post-#948 pattern).
        """
        if self._running:
            logger.warning("EthicsAuditCleanupJob already running, ignoring start request")
            return

        self._running = True
        self._task = asyncio.current_task()
        logger.info(
            "EthicsAuditCleanupJob starting",
            interval_hours=self.interval_hours,
        )

        try:
            while self._running:
                try:
                    result = await self.execute_cleanup()
                    if result["success"]:
                        logger.info(
                            "EthicsAuditCleanupJob sweep complete",
                            removed=result["removed"],
                        )
                    else:
                        logger.warning(
                            "EthicsAuditCleanupJob sweep encountered error",
                            error=result.get("error"),
                        )
                except Exception as e:
                    logger.error(
                        "Unexpected error in cleanup loop", error=str(e), exc_info=True
                    )

                # Sleep until next run, in 5-minute chunks for responsive
                # shutdown via the _running flag (the cancel-and-await in
                # stop() is the primary mechanism, but the chunked sleep
                # is a defensive layer in case cancel() is missed).
                if self._running:
                    sleep_chunks = self.interval_hours * 12  # 12 chunks per hour
                    for _ in range(sleep_chunks):
                        if not self._running:
                            break
                        await asyncio.sleep(300)
        except asyncio.CancelledError:
            logger.info("EthicsAuditCleanupJob cancelled (clean shutdown)")
            self._running = False
            raise
        finally:
            self._task = None

        logger.info("EthicsAuditCleanupJob stopped")

    async def stop(self) -> None:
        """Cancel the wrapping task + await it. Sub-second shutdown."""
        if not self._running:
            logger.warning("EthicsAuditCleanupJob not running")
            return

        logger.info("Stopping EthicsAuditCleanupJob...")
        self._running = False

        if self._task is not None and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        logger.info("EthicsAuditCleanupJob stopped")

    def is_running(self) -> bool:
        return self._running

    def get_status(self) -> Dict[str, Any]:
        return {
            "running": self._running,
            "interval_hours": self.interval_hours,
            "retention_days": self.retention_days,
        }
