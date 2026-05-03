"""
Issue #1035 Phase 5: Periodic invocation of CompostingScheduler.maybe_run().

Wraps the domain-level `CompostingScheduler` (services/mux/composting_scheduler.py)
in a runtime loop that fires `maybe_run()` on a configurable interval.
`maybe_run()` itself does the heavy lifting: it checks whether the current
hour is a quiet hour, whether enough items are pending, and whether the
minimum interval since last run has elapsed. The job loop's only
responsibility is "call maybe_run on a tick," not "decide whether composting
runs."

Pattern: parallels `EthicsAuditCleanupJob` (#1018 Phase 2) including the
post-#948 task-cancellation hygiene (capture `asyncio.current_task()` in
`start()`, cancel-and-await in `stop()`) so shutdown is sub-second on
SIGTERM/Ctrl-C.

Architectural alignment:
- The domain class (`CompostingScheduler`) is testable as a pure
  policy/scheduling abstraction. It doesn't own the loop.
- The runtime job class (this file) is testable for lifecycle behavior
  (start → tick → stop, with no orphaned tasks). It doesn't own the
  scheduling policy.

Per #1035 audit Q2 (May 3): separate-job-wrapper preserves the domain
class's testability and matches the established #1018 split.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, Optional

import structlog

from services.mux.composting_scheduler import CompostingScheduler

logger = structlog.get_logger()


class CompostingSchedulerJob:
    """Periodic ticking of CompostingScheduler.maybe_run().

    Default cadence: every hour. CompostingScheduler.maybe_run() decides
    whether the tick should actually run a composting cycle (quiet-hours
    + min_pending + min_interval gates). The loop's sleep is shorter than
    the gate interval so a tick is never missed.
    """

    def __init__(
        self,
        scheduler: CompostingScheduler,
        interval_seconds: int = 3600,  # 1 hour default
        user_id_provider: Optional[Any] = None,
    ):
        """
        Args:
            scheduler: domain-level CompostingScheduler with bin + pipeline
            interval_seconds: how often to call maybe_run()
            user_id_provider: optional callable returning the user_id to
                associate with composted insights. Default: empty string
                (acceptable in alpha; per Q5, schema is per-user-correct
                from day one even when only one user exists).
        """
        self.scheduler = scheduler
        self.interval_seconds = interval_seconds
        self.user_id_provider = user_id_provider or (lambda: "")
        self._running = False
        self._task: Optional[asyncio.Task] = None
        logger.info(
            "CompostingSchedulerJob initialized",
            interval_seconds=interval_seconds,
        )

    async def execute_tick(self) -> Dict[str, Any]:
        """Run one tick of maybe_run(). Returns status dict."""
        try:
            user_id = self.user_id_provider()
            result = await self.scheduler.maybe_run(user_id=user_id)
            if result is None:
                return {"success": True, "ran": False, "reason": "gates_not_met"}
            return {
                "success": result.success,
                "ran": True,
                "processed_count": result.processed_count,
                "learnings_extracted": result.learnings_extracted,
                "duration_seconds": result.duration_seconds,
                "errors": result.errors,
            }
        except Exception as e:
            logger.error("CompostingSchedulerJob.execute_tick failed", error=str(e))
            return {"success": False, "ran": False, "error": str(e)}

    async def start(self) -> None:
        """Run the composting tick loop until stop() is called.

        Captures `asyncio.current_task()` in `_task` so `stop()` can
        cancel cleanly without waiting for the sleep chunk to notice
        the `_running` flag (post-#948 pattern).
        """
        if self._running:
            logger.warning(
                "CompostingSchedulerJob already running, ignoring start request"
            )
            return

        self._running = True
        self._task = asyncio.current_task()
        logger.info(
            "CompostingSchedulerJob starting",
            interval_seconds=self.interval_seconds,
        )

        try:
            while self._running:
                try:
                    result = await self.execute_tick()
                    if result.get("ran"):
                        logger.info(
                            "CompostingSchedulerJob tick — composting ran",
                            processed=result.get("processed_count"),
                            learnings=result.get("learnings_extracted"),
                            duration=result.get("duration_seconds"),
                        )
                    else:
                        logger.debug(
                            "CompostingSchedulerJob tick — gates not met",
                            reason=result.get("reason") or result.get("error"),
                        )
                except Exception as e:
                    logger.error(
                        "Unexpected error in composting tick loop",
                        error=str(e),
                        exc_info=True,
                    )

                # Sleep until next tick, in 5-minute chunks for responsive
                # shutdown via the _running flag (cancel-and-await in stop()
                # is the primary mechanism; chunked sleep is a defensive layer).
                if self._running:
                    chunk_seconds = 300  # 5 minutes
                    chunks = max(1, self.interval_seconds // chunk_seconds)
                    for _ in range(chunks):
                        if not self._running:
                            break
                        await asyncio.sleep(min(chunk_seconds, self.interval_seconds))
        except asyncio.CancelledError:
            logger.info("CompostingSchedulerJob cancelled (clean shutdown)")
            self._running = False
            raise
        finally:
            self._task = None

        logger.info("CompostingSchedulerJob stopped")

    async def stop(self) -> None:
        """Cancel the wrapping task + await it. Sub-second shutdown."""
        if not self._running:
            logger.warning("CompostingSchedulerJob not running")
            return

        logger.info("Stopping CompostingSchedulerJob...")
        self._running = False

        if self._task is not None and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        logger.info("CompostingSchedulerJob stopped")

    def is_running(self) -> bool:
        return self._running

    def get_status(self) -> Dict[str, Any]:
        return {
            "running": self._running,
            "interval_seconds": self.interval_seconds,
        }
