"""#2342 (ADR-081 D3; Arch 2026-11-12 06:52): the main app's background refresh of GitHub
App grants.

The MCP app is decrypt-only (#1982) and can never refresh a token, so a person who uses
Piper only through the Claude connector would meet an expired token there after eight
hours. This job runs ``background_refresh_pass`` every 30 minutes on each main-app
machine; the per-owner lock and the re-read under it make a second machine find the pair
already fresh. Outside App mode, and in a scoped process, a pass does nothing.

Pattern-048 (Periodic Background Job): one-minute sleep chunks, ``start()`` captures its
task so ``stop()`` cancels it at once (#948).
"""

from __future__ import annotations

import asyncio
from typing import Optional

import structlog

from services.mcp.consumer.github_app_refresh import (
    BACKGROUND_INTERVAL_SECONDS,
    background_refresh_pass,
)

logger = structlog.get_logger(__name__)


class GitHubAppRefreshJob:
    def __init__(self, interval_seconds: int = BACKGROUND_INTERVAL_SECONDS):
        self.interval_seconds = max(60, int(interval_seconds))
        self._running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._task = asyncio.current_task()
        try:
            while self._running:
                try:
                    await background_refresh_pass()
                except Exception as e:  # the pass never raises; belt and braces
                    logger.error("github_app_refresh_job_pass_failed", error=type(e).__name__)
                remaining = self.interval_seconds
                while self._running and remaining > 0:
                    await asyncio.sleep(min(60, remaining))
                    remaining -= 60
        except asyncio.CancelledError:
            self._running = False
            raise
        finally:
            self._task = None

    async def stop(self) -> None:
        if not self._running:
            return
        self._running = False
        if self._task is not None and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def is_running(self) -> bool:
        return self._running
