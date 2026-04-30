"""
Attention Decay Background Job

Updates attention event intensities based on decay models.
Runs periodically to maintain accurate attention scores even without user activity.

Issue #365: SLACK-ATTENTION-DECAY
Pattern: Pattern-048 (Periodic Background Job)
"""

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import structlog

logger = structlog.get_logger(__name__)


class AttentionDecayJob:
    """
    Background job to update attention decay calculations.

    Runs periodically to ensure attention scores decay over time
    even without user activity triggering recalculation.

    Implements Pattern-048: Periodic Background Job
    - Configurable interval with bounds
    - 1-minute sleep chunks for responsive shutdown
    - start(), stop(), is_running() lifecycle
    """

    # Tuneable interval bounds (per PM Decision 2)
    DEFAULT_INTERVAL_MINUTES = 5
    MIN_INTERVAL_MINUTES = 1
    MAX_INTERVAL_MINUTES = 30

    def __init__(
        self,
        attention_model: Any,  # AttentionModel - use Any to avoid circular import
        interval_minutes: Optional[int] = None,
    ):
        """
        Initialize the attention decay job.

        Args:
            attention_model: The AttentionModel instance to update
            interval_minutes: Override default interval (bounded by MIN/MAX)
        """
        self.attention_model = attention_model

        # Tuneable interval with bounds checking
        # Use None check (not truthiness) so 0 is treated as explicit value
        interval = (
            interval_minutes if interval_minutes is not None else self.DEFAULT_INTERVAL_MINUTES
        )
        self.interval_minutes = max(
            self.MIN_INTERVAL_MINUTES,
            min(interval, self.MAX_INTERVAL_MINUTES),
        )

        self._running = False
        self._task: Optional[asyncio.Task] = None

        logger.info(
            "AttentionDecayJob initialized",
            interval_minutes=self.interval_minutes,
        )

    async def execute_decay_update(self) -> Dict[str, Any]:
        """
        Execute decay update on all active attention events.

        Triggers intensity recalculation for all events and cleans up
        any that have fully expired.

        Returns:
            Dict with update results including counts and timing
        """
        try:
            start_time = datetime.now(timezone.utc)

            # Count events and trigger decay calculations
            updated_count = 0
            expired_count = 0

            # Iterate over active events and trigger intensity recalculation
            for event_id, event in list(self.attention_model._active_events.items()):
                current_intensity = event.get_current_intensity()

                if current_intensity <= 0.01:  # Effectively expired
                    expired_count += 1
                else:
                    updated_count += 1

            # Cleanup expired events
            self.attention_model._cleanup_expired_events()

            elapsed_ms = (datetime.now(timezone.utc) - start_time).total_seconds() * 1000

            result = {
                "updated": updated_count,
                "expired": expired_count,
                "elapsed_ms": round(elapsed_ms, 2),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "success": True,
            }

            logger.debug("Attention decay update completed", **result)
            return result

        except Exception as e:
            logger.error("Attention decay update failed", error=str(e))
            return {
                "updated": 0,
                "expired": 0,
                "elapsed_ms": 0,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "success": False,
                "error": str(e),
            }

    async def start(self) -> None:
        """
        Start the decay job loop.

        Runs continuously, updating decay every interval_minutes.
        Uses 1-minute sleep chunks for responsive shutdown (Pattern-048).
        """
        if self._running:
            logger.warning("Attention decay job already running, ignoring start request")
            return

        self._running = True
        # #948: capture our wrapping task so stop() can cancel cleanly without
        # waiting up to interval_minutes for the sleep loop to notice the flag.
        self._task = asyncio.current_task()
        logger.info(
            "Attention decay job starting",
            interval_minutes=self.interval_minutes,
        )

        try:
            while self._running:
                try:
                    # Execute decay update
                    await self.execute_decay_update()

                except Exception as e:
                    logger.error("Unexpected error in decay job loop", error=str(e))

                # Sleep until next run (in 1-minute chunks for responsive shutdown)
                if self._running:
                    for _ in range(self.interval_minutes):
                        if not self._running:
                            break
                        await asyncio.sleep(60)  # 1 minute chunks
        except asyncio.CancelledError:
            # #948: clean shutdown via task.cancel() (from stop() or event loop teardown)
            logger.info("Attention decay job cancelled (clean shutdown)")
            self._running = False
            raise
        finally:
            self._task = None

        logger.info("Attention decay job stopped")

    async def stop(self) -> None:
        """
        Stop the decay job gracefully.

        Cancels the wrapping task so the sleep loop terminates immediately
        rather than waiting up to interval_minutes for the _running flag check.
        #948: prior implementation only set the flag + slept 0.1s, leaving the
        task pending when uvicorn tore down the event loop.
        """
        if not self._running:
            logger.warning("Attention decay job not running")
            return

        logger.info("Stopping attention decay job...")
        self._running = False

        # #948: cancel + await the wrapping task so we don't return until the
        # task is actually done. CancelledError from cancel() is normal.
        if self._task is not None and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def is_running(self) -> bool:
        """Check if the decay job is currently running."""
        return self._running

    def get_status(self) -> Dict[str, Any]:
        """
        Get current job status for monitoring.

        Returns:
            Dict with running state, interval, and configuration
        """
        return {
            "running": self._running,
            "interval_minutes": self.interval_minutes,
            "default_interval": self.DEFAULT_INTERVAL_MINUTES,
            "min_interval": self.MIN_INTERVAL_MINUTES,
            "max_interval": self.MAX_INTERVAL_MINUTES,
        }
