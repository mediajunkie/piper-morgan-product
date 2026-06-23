"""
Standup Orchestration Domain Service
Mediates standup workflow coordination following DDD principles

Created: 2025-09-12 by Code Agent Phase 1 - Layer Separation Refactoring
Addresses architectural violation: Direct integration access from application layer

Updated: 2026-06-20 (#1289) — replaced hollow MorningStandupWorkflow with
StandupAssembler (honest derivation from live Radar EntitySources). The
/generate URL is preserved; the fabricated workflow is retired.
"""

import time
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from services.configuration.piper_config_loader import piper_config_loader
from services.domain.models import StandupSummary
from services.features.morning_standup import (
    StandupIntegrationError,
    StandupResult,
)
from services.standup.assembler import StandupCalendarProvider, build_standup_assembler

# Re-export exception for clean domain boundary
__all__ = ["StandupOrchestrationService", "StandupIntegrationError"]


def _summary_to_result(summary: StandupSummary, user_id: str, generation_time_ms: int) -> StandupResult:
    """Adapt StandupSummary (assembler output) → StandupResult (route layer shape).

    Maps:
      summary.yesterday → result.yesterday_accomplishments
      summary.today     → result.today_priorities
      summary.watch     → result.blockers  (inferred potential blockers)

    Hollow fields (time_saved_minutes, github_activity) are set to honest
    zero/empty values — the assembler derives from real data, not metrics.
    """
    return StandupResult(
        user_id=user_id,
        generated_at=datetime.now(),
        generation_time_ms=generation_time_ms,
        yesterday_accomplishments=list(summary.yesterday),
        today_priorities=list(summary.today),
        blockers=list(summary.watch),
        context_source="assembled",
        github_activity={},
        performance_metrics={"total_time_ms": generation_time_ms},
        time_saved_minutes=0,
    )


class StandupOrchestrationService:
    """
    Domain service for standup workflow coordination

    Encapsulates integration orchestration following DDD principles:
    - Mediates between application layer and integration layer
    - Delegates to StandupAssembler (honest derivation from Radar EntitySources)
    - Provides clean interface for standup operations
    """

    def __init__(self):
        """Initialize orchestration service with dependency management"""
        pass

    def _initialize_dependencies(self) -> None:
        """No-op — kept for call-site compatibility; assembler wires its own deps."""
        pass

    async def orchestrate_standup_workflow(
        self, user_id: Optional[UUID] = None, workflow_type: str = "standard"
    ) -> StandupResult:
        """
        Orchestrate complete standup workflow through domain layer.

        Delegates to StandupAssembler which derives a StandupSummary from live
        Radar EntitySources (same wiring as the Radar feed). The workflow_type
        parameter is accepted for API compatibility but ignored — StandupAssembler
        handles all source types in a single assemble() call.

        Args:
            user_id: User identifier (resolved from config if not provided)
            workflow_type: Accepted for compatibility; all paths use assembler

        Returns:
            StandupResult containing all standup data

        Raises:
            StandupIntegrationError: When assembly fails
        """
        # Resolve user_id from configuration if not provided
        resolved_user_id: str
        if user_id is None:
            config = piper_config_loader.load_standup_config()
            resolved_user_id = config.get("user_identity", {}).get("user_id", "default_user")
        else:
            resolved_user_id = str(user_id)

        try:
            from services.database.repositories import DBUserHistoryRepository
            from services.database.session_factory import AsyncSessionFactory
            from services.memory.user_history import UserHistoryService

            t0 = time.monotonic()
            async with AsyncSessionFactory.session_scope_fresh() as session:
                uhs = UserHistoryService(DBUserHistoryRepository(session))
                assembler = build_standup_assembler(
                    uhs, calendar_provider=StandupCalendarProvider()
                )
                summary = await assembler.assemble(resolved_user_id)
            generation_time_ms = int((time.monotonic() - t0) * 1000)
        except Exception as exc:
            raise StandupIntegrationError(
                f"StandupAssembler failed: {exc}",
                service="standup",
            ) from exc

        return _summary_to_result(summary, resolved_user_id, generation_time_ms)

    async def get_standup_context(self, user_id: UUID) -> Dict[str, Any]:
        """
        Get standup context without executing full workflow.

        Returns lightweight metadata; actual derivation happens in
        orchestrate_standup_workflow via StandupAssembler.

        Args:
            user_id: User identifier

        Returns:
            Dictionary containing context information
        """
        return {
            "user_id": str(user_id),
            "github_activity": {},
            "timestamp": datetime.now().isoformat(),
        }

    def get_supported_workflow_types(self) -> list[str]:
        """
        Get list of supported workflow types.

        All types delegate to StandupAssembler (workflow_type is accepted for
        API compatibility but the assembler handles all sources in one pass).

        Returns:
            List of workflow type identifiers
        """
        return ["standard", "with_issues", "with_documents", "with_calendar", "trifecta"]
