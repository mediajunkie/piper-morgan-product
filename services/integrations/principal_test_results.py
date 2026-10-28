"""Per-principal Integrations Test results (#2071, Arch-ruled shape).

The Integrations page's Test button records one outcome: did THIS person's
connection to THIS integration answer just now. Before #2071 that outcome was
stored once per integration for the whole host (``IntegrationHealthMonitor``
keyed by integration name), so one account's Test set the status, error text
and check time every other account saw on the card and in chat, and failure
counts accumulated across accounts.

This store keys the result by ``(principal, integration)``:

- The Test route writes under the caller's principal (``current_user.sub``).
- Every user-facing reader passes the principal: the card's generic path,
  ``_recorded_check_iso`` (the GitHub OAuth card's time, #2066) and
  ``IntegrationStatusService.get_status`` (chat).
- No record for this principal means "never checked" (the #2044 unchecked
  card, ``healthy=None``). There is no host-level entry to fall back to.

Process memory only (Arch): a restart gives every account the honest unchecked
card until it presses Test again. Host-level components (``redis_connection``,
``conversation_cache``) stay on the host ``IntegrationHealthMonitor``; this
store holds only the per-person Test result.

``tests/test_architecture_enforcement.py::TestPerPrincipalTestResultRatchet2071``
keeps user-facing integration ids off the host monitor's ``get_component_health``.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class IntegrationTestResult:
    """The latest Test outcome for one principal's connection to one integration."""

    principal: str
    integration: str
    ok: bool
    checked_at: float  # epoch seconds
    error: Optional[str]  # this principal's own error text, None on success
    latency_ms: float
    error_count: int  # consecutive failed Tests for this principal; a success resets it

    @property
    def checked_at_iso(self) -> str:
        return datetime.fromtimestamp(self.checked_at, tz=timezone.utc).isoformat()


class PrincipalTestResultStore:
    """In-memory map of ``(principal, integration) -> IntegrationTestResult``."""

    def __init__(self) -> None:
        self._results: Dict[Tuple[str, str], IntegrationTestResult] = {}
        self._lock = Lock()

    def record_test_result(
        self,
        principal: Optional[str],
        integration: str,
        ok: bool,
        error: Optional[str] = None,
        latency_ms: float = 0.0,
    ) -> Optional[IntegrationTestResult]:
        """Record one Test outcome under ``principal``. No principal, no record."""
        if not principal:
            return None
        key = (str(principal), integration)
        with self._lock:
            previous = self._results.get(key)
            error_count = 0 if ok else (previous.error_count if previous else 0) + 1
            result = IntegrationTestResult(
                principal=key[0],
                integration=integration,
                ok=ok,
                checked_at=time.time(),
                error=None if ok else (error or "Connection failed"),
                latency_ms=latency_ms,
                error_count=error_count,
            )
            self._results[key] = result
        return result

    def get_test_result(
        self, principal: Optional[str], integration: str
    ) -> Optional[IntegrationTestResult]:
        """This principal's latest Test result, else None. Never another principal's."""
        if not principal:
            return None
        return self._results.get((str(principal), integration))

    def clear(self) -> None:
        with self._lock:
            self._results.clear()

    def forget(self, principal: Optional[str], integration: str) -> bool:
        """#2187: drop THIS principal's record for ONE integration, so a new grant or a
        disconnect never inherits the previous grant's check (the card then reads
        "Not checked yet. Press Test." until Test runs). Returns True if a record
        existed. No principal, nothing to forget."""
        if not principal:
            return False
        with self._lock:
            return self._results.pop((str(principal), integration), None) is not None


_store: Optional[PrincipalTestResultStore] = None


def get_test_result_store() -> PrincipalTestResultStore:
    """The process-wide store (one per process; results never leave memory)."""
    global _store
    if _store is None:
        _store = PrincipalTestResultStore()
    return _store
