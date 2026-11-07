"""Event-loop watchdog (#2101): name the call that blocks the loop.

Alpha stalled three times on 2026-10-19 and once on 2026-10-20 (07:18 PT), each inside a
chat turn: /health unanswered for more than ten seconds while Postgres read normal and
nothing was logged. A /health handler bounded at 2 s that cannot answer in 10 s means the
event loop itself was away (or the one shared CPU was saturated). Log reading cannot say
WHICH call held it; a thread can.

Shape: the loop refreshes a heartbeat every ``HEARTBEAT_SECONDS``; a daemon thread checks
it every ``CHECK_SECONDS``. When the heartbeat is older than ``STALL_SECONDS`` the thread
logs WARNING ``event_loop_blocked`` with the stale age and the main thread's current stack
(file, line, function; no locals, no arguments, so no user text or credential can appear),
then WARNING ``event_loop_resumed`` with the total once the heartbeat moves again. One
``event_loop_blocked`` per stall (the thread does not repeat while the same stall lasts).

The thread is the point: the loop cannot observe its own absence. ``sys._current_frames``
is the sampling primitive; it is read-only and costs one dict build per check.
"""

from __future__ import annotations

import asyncio
import sys
import threading
import time
import traceback
from typing import Callable, List, Optional

import structlog

logger = structlog.get_logger()

HEARTBEAT_SECONDS = 1.0
CHECK_SECONDS = 1.0
STALL_SECONDS = 3.0
STACK_LIMIT = 40

_clock = time.monotonic


def format_thread_stack(thread_id: int, limit: int = STACK_LIMIT) -> List[str]:
    """The named thread's current stack as ``file:line in function`` lines, innermost
    last; empty when the thread has no frame (gone, or never started)."""
    frame = sys._current_frames().get(thread_id)
    if frame is None:
        return []
    summary = traceback.extract_stack(frame, limit=limit)
    return [f"{fs.filename}:{fs.lineno} in {fs.name}" for fs in summary]


class LoopWatchdog:
    """Owns the heartbeat task (loop side) and the checker thread (off loop)."""

    def __init__(
        self,
        *,
        stall_seconds: float = STALL_SECONDS,
        check_seconds: float = CHECK_SECONDS,
        heartbeat_seconds: float = HEARTBEAT_SECONDS,
        thread_id: Optional[int] = None,
        on_block: Optional[Callable[[float, List[str]], None]] = None,
    ) -> None:
        self.stall_seconds = stall_seconds
        self.check_seconds = check_seconds
        self.heartbeat_seconds = heartbeat_seconds
        main_ident = threading.main_thread().ident
        self._thread_id: int = thread_id if thread_id is not None else int(main_ident or 0)
        self._on_block = on_block
        self._last_beat = _clock()
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._task: Optional["asyncio.Task[None]"] = None
        self._blocked_since: Optional[float] = None
        self.blocks_seen = 0

    # ---- loop side -------------------------------------------------------------
    def beat(self) -> None:
        self._last_beat = _clock()

    async def _heartbeat(self) -> None:
        while True:
            self.beat()
            await asyncio.sleep(self.heartbeat_seconds)

    # ---- thread side -----------------------------------------------------------
    def check_once(self) -> Optional[float]:
        """One checker step. Returns the stale age when a NEW stall is announced,
        else None. Pure enough to pin: it reads the heartbeat and the clock."""
        age = _clock() - self._last_beat
        if age > self.stall_seconds:
            if self._blocked_since is None:
                self._blocked_since = self._last_beat
                self.blocks_seen += 1
                stack = format_thread_stack(self._thread_id)
                # One string, innermost frame first (the configured renderer joins str
                # values; a list would break it).
                logger.warning(
                    "event_loop_blocked",
                    stale_s=round(age, 1),
                    stack=" <- ".join(reversed(stack)) or "(no frame)",
                )
                if self._on_block is not None:
                    self._on_block(age, stack)
                return age
            return None
        if self._blocked_since is not None:
            total = self._last_beat - self._blocked_since
            self._blocked_since = None
            logger.warning("event_loop_resumed", blocked_s=round(total, 1))
        return None

    def _run(self) -> None:
        while not self._stop.wait(self.check_seconds):
            try:
                self.check_once()
            except Exception as e:  # silent-ok: #2101 — the watchdog must never take the app down; logged ERROR and the thread keeps checking
                logger.error("event_loop_watchdog_check_failed", error=str(e))

    # ---- lifecycle -------------------------------------------------------------
    @property
    def is_running(self) -> bool:
        """True while the checker thread is alive (what /health reports)."""
        return self._thread is not None and self._thread.is_alive()

    def start(self) -> None:
        if self._thread is not None:
            return
        self.beat()
        self._task = asyncio.get_running_loop().create_task(self._heartbeat())
        self._thread = threading.Thread(target=self._run, name="event-loop-watchdog", daemon=True)
        self._thread.start()
        # WARNING, not INFO: alpha's structured log emits no INFO lines (PA, 2026-10-20),
        # and a watchdog whose start is invisible cannot have its silence read as a
        # finding. /health carries `services.loop_watchdog` for the same reason.
        logger.warning(
            "event_loop_watchdog_started",
            stall_s=self.stall_seconds,
            check_s=self.check_seconds,
        )

    async def stop(self) -> None:
        self._stop.set()
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except (
                asyncio.CancelledError,
                Exception,
            ):  # silent-ok: #2101 — shutdown; a cancelled heartbeat is the expected outcome
                pass
            self._task = None
        if self._thread is not None:
            self._thread.join(timeout=self.check_seconds * 2)
            self._thread = None
