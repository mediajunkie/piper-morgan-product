"""
Token Blacklist Cleanup Job

Background job for cleaning up expired token blacklist entries from database.
Redis entries expire automatically via TTL, so this only cleans database fallback.

Runs: Every 24 hours
Purpose: Remove expired tokens from database to prevent bloat
"""

import asyncio
from datetime import datetime, timezone
from typing import Optional

import structlog

from services.auth.token_blacklist import TokenBlacklist
from services.cache.redis_factory import RedisFactory
from services.database.session_factory import AsyncSessionFactory

logger = structlog.get_logger(__name__)


class BlacklistCleanupJob:
    """
    Background job to clean up expired blacklist entries.

    Runs periodically to remove expired tokens from database storage.
    Redis entries auto-expire via TTL and don't need cleanup.
    """

    def __init__(
        self,
        redis_factory: Optional[RedisFactory] = None,
        db_session_factory: Optional[AsyncSessionFactory] = None,
        interval_hours: int = 24,
    ):
        """
        Initialize cleanup job.

        Args:
            redis_factory: Redis factory for blacklist
            db_session_factory: Database session factory
            interval_hours: Hours between cleanup runs (default: 24)
        """
        self.redis_factory = redis_factory or RedisFactory()
        self.db_session_factory = db_session_factory or AsyncSessionFactory()
        self.interval_hours = interval_hours
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._blacklist: Optional[TokenBlacklist] = None

        logger.info("BlacklistCleanupJob initialized", interval_hours=interval_hours)

    async def _initialize_blacklist(self) -> None:
        """Initialize TokenBlacklist instance"""
        if self._blacklist is None:
            self._blacklist = TokenBlacklist(self.redis_factory, self.db_session_factory)
            await self._blacklist.initialize()
            logger.info("TokenBlacklist initialized for cleanup job")

    async def execute_cleanup(self) -> dict:
        """
        Execute cleanup of expired blacklist entries.

        Returns:
            Dict with cleanup results: {
                "removed": int,
                "timestamp": str,
                "success": bool,
                "error": Optional[str]
            }
        """
        try:
            await self._initialize_blacklist()

            # Remove expired entries from database
            count = await self._blacklist.remove_expired()

            result = {
                "removed": count,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "success": True,
                "error": None,
            }

            logger.info("Blacklist cleanup completed", removed=count, timestamp=result["timestamp"])

            return result

        except Exception as e:
            error_msg = f"Blacklist cleanup failed: {str(e)}"
            logger.error(error_msg, exc_info=True)

            return {
                "removed": 0,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "success": False,
                "error": error_msg,
            }

    async def start(self) -> None:
        """
        Start the cleanup job loop.

        Runs continuously, cleaning expired entries every 24 hours (default).
        Breaks sleep into smaller chunks for responsive shutdown.
        """
        if self._running:
            logger.warning("Cleanup job already running, ignoring start request")
            return

        self._running = True
        # #948: capture our wrapping task so stop() can cancel cleanly without
        # waiting up to 5 minutes for the sleep loop to notice the flag.
        self._task = asyncio.current_task()
        logger.info("Blacklist cleanup job starting", interval_hours=self.interval_hours)

        try:
            while self._running:
                try:
                    # Execute cleanup
                    logger.debug("Executing blacklist cleanup")
                    result = await self.execute_cleanup()

                    if result["success"]:
                        logger.info("Blacklist cleanup successful", removed=result["removed"])
                    else:
                        logger.warning(
                            "Blacklist cleanup encountered error", error=result.get("error")
                        )

                except Exception as e:
                    logger.error(
                        "Unexpected error in cleanup job loop", error=str(e), exc_info=True
                    )

                # Sleep until next run
                # Break into smaller chunks for responsive shutdown
                if self._running:
                    logger.debug(f"Sleeping for {self.interval_hours} hours until next cleanup")

                    # Sleep in 5-minute chunks for responsive shutdown
                    sleep_chunks = self.interval_hours * 12  # 12 chunks per hour
                    for _ in range(sleep_chunks):
                        if not self._running:
                            break
                        await asyncio.sleep(300)  # 5 minutes
        except asyncio.CancelledError:
            # #948: clean shutdown via task.cancel() (from stop() or event loop teardown)
            logger.info("Blacklist cleanup job cancelled (clean shutdown)")
            self._running = False
            raise
        finally:
            self._task = None

        logger.info("Blacklist cleanup job stopped")

    async def stop(self) -> None:
        """
        Stop the cleanup job gracefully.

        Cancels the wrapping task so the sleep loop terminates immediately
        rather than waiting up to interval_hours for the _running flag check.
        #948: prior implementation referenced self._task without ever assigning
        it (dead code), so the wait-for-task block never ran; the wrapping
        task was left pending when uvicorn tore down the event loop.
        """
        if not self._running:
            logger.warning("Cleanup job not running")
            return

        logger.info("Stopping blacklist cleanup job...")
        self._running = False

        # #948: cancel + await the wrapping task so we don't return until the
        # task is actually done. CancelledError from cancel() is normal.
        if self._task is not None and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

        logger.info("Blacklist cleanup job stopped")

    def is_running(self) -> bool:
        """Check if cleanup job is currently running"""
        return self._running
