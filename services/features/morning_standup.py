"""
Morning Standup — back-compat re-exports + route-layer result types.

Created: 2025-08-21 (Morning Standup MVP).

#1289 (2026-06-21): the hollow ``MorningStandupWorkflow`` engine — which
fabricated "time saved" / efficiency metrics — has been retired and deleted.
The honest standup now derives from the live Radar EntitySources via
``StandupAssembler`` (services/standup/assembler.py), wrapped by
``StandupOrchestrationService``. This module is retained only for the
back-compat re-export of ``StandupItem`` and the route-layer result types
``StandupResult`` / ``StandupIntegrationError`` (the honest adapter populates
``StandupResult`` from real data; ``time_saved_minutes`` is left at 0).
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from services.domain.models import StandupItem  # Re-exported for back-compat (#900 Phase 2)

__all__ = ["StandupItem", "StandupResult", "StandupIntegrationError"]


class StandupIntegrationError(Exception):
    """Raised when standup integrations fail and cannot provide real data"""

    def __init__(self, message: str, service: str = None, suggestion: str = None):
        self.service = service
        self.suggestion = suggestion
        super().__init__(message)


@dataclass
class StandupResult:
    """Result of morning standup generation.

    Per #1034 (May 3): list fields carry `StandupItem` instances rather
    than pre-formatted strings, so structured per-item metadata
    (`lifecycle_state`, `source`, `icon`) reaches consumers — most
    notably the standup.html template via #704.
    """

    user_id: str
    generated_at: datetime
    generation_time_ms: int
    yesterday_accomplishments: List[StandupItem]
    today_priorities: List[StandupItem]
    blockers: List[StandupItem]
    context_source: str  # "persistent", "default", etc.
    github_activity: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    time_saved_minutes: int
    # #1889: user-facing labels of any source that genuinely FAILED this assemble
    # (#1587). The formatters disclose them first, and never render an empty
    # section list (or "No blockers ✅") under a read that didn't happen.
    degraded_sources: List[str] = field(default_factory=list)
    degraded_details: List[dict] = field(default_factory=list)  # #1965 (b)

    def is_empty(self) -> bool:
        return not (self.yesterday_accomplishments or self.today_priorities or self.blockers)
