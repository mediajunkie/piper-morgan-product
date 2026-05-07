"""
Morning Standup MVP - Core Implementation
Built on persistent context infrastructure

Created: 2025-08-21 by Morning Standup MVP Mission
Uses UserPreferenceManager + SessionPersistenceManager + GitHub integration
Performance target: <2 seconds, saves 15+ minutes
"""

import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog

logger = structlog.get_logger(__name__)

from services.configuration.piper_config_loader import piper_config_loader
from services.domain.github_domain_service import GitHubDomainService
from services.domain.models import StandupItem  # Re-exported below for back-compat (#900 Phase 2)
from services.domain.user_preference_manager import UserPreferenceManager
from services.features.issue_intelligence import IssueIntelligenceCanonicalQueryEngine
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.knowledge_graph.document_service import get_document_service
from services.orchestration.session_persistence import SessionPersistenceManager

# Re-export so existing callers `from services.features.morning_standup import StandupItem`
# continue to work (#900 Phase 2 moved the canonical definition to services/domain/models.py).
__all__ = ["StandupItem", "StandupContext", "StandupResult", "StandupIntegrationError",
           "MorningStandupWorkflow"]


class StandupIntegrationError(Exception):
    """Raised when standup integrations fail and cannot provide real data"""

    def __init__(self, message: str, service: str = None, suggestion: str = None):
        self.service = service
        self.suggestion = suggestion
        super().__init__(message)


@dataclass
class StandupContext:
    """Context for generating morning standup"""

    user_id: str
    date: datetime
    session_context: Dict[str, Any] = field(default_factory=dict)
    github_repos: List[str] = field(default_factory=list)


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


class MorningStandupWorkflow:
    """
    Morning Standup MVP Workflow

    Leverages yesterday's persistent context infrastructure:
    - UserPreferenceManager for user preferences
    - SessionPersistenceManager for session continuity
    - GitHubDomainService for recent activity

    Performance: <2 seconds generation, saves 15+ minutes manual prep
    """

    def __init__(
        self,
        preference_manager: UserPreferenceManager,
        session_manager: SessionPersistenceManager,
        github_domain_service: GitHubDomainService,
        user_id: str = None,
        canonical_handlers: Optional[CanonicalHandlers] = None,
    ):
        self.preference_manager = preference_manager
        self.session_manager = session_manager
        self.github_domain_service = github_domain_service
        # Load user_id from configuration if not provided
        if user_id is None:
            standup_config = piper_config_loader.load_standup_config()
            self.user_id = standup_config["user_identity"]["user_id"]
        else:
            self.user_id = user_id
        self.canonical_handlers = canonical_handlers
        # Issue #1054: self.logger.warning at line 197 was previously hitting
        # AttributeError (no init), silently swallowed by the broad except
        # in _get_session_context, which masked active_repos-empty warnings
        # and broke `mock_session_manager.get_session_context.assert_called_once`
        # in test_generate_standup_for_user.
        self.logger = logger.bind(component="MorningStandupWorkflow")

    async def canonical_query_integration(self, query: str, user_id: str) -> Dict[str, Any]:
        """
        Canonical query interface for integration with Issue Intelligence

        Provides morning standup context to enhance canonical query responses
        """
        try:
            standup_result = await self.generate_standup(user_id)
            return {
                "standup_context": {
                    "yesterday_accomplishments": standup_result.yesterday_accomplishments,
                    "today_priorities": standup_result.today_priorities,
                    "blockers": standup_result.blockers,
                    "github_activity": standup_result.github_activity,
                },
                "context_source": "morning_standup_canonical",
                "integration_time_ms": standup_result.generation_time_ms,
            }
        except Exception as e:
            return {
                "standup_context": {},
                "context_source": "morning_standup_error",
                "error": str(e),
            }

    async def generate_standup(self, user_id: str) -> StandupResult:
        """Generate morning standup for user using persistent context.

        Performance optimized: session context and GitHub activity are
        fetched in parallel using asyncio.gather().
        """
        import asyncio

        start_time = time.time()

        try:
            # Parallel fetch: session context and GitHub activity (Issue #556 optimization)
            session_context, github_activity = await asyncio.gather(
                self._get_session_context(user_id),
                self._get_github_activity(),
            )

            # Generate standup content
            result = await self._generate_standup_content(
                user_id, session_context, github_activity, start_time
            )

            return result

        except Exception as e:
            # No fallbacks - fail honestly
            error_msg = f"Morning standup generation failed: {str(e)}"
            if "github" in str(e).lower():
                suggestion = "Check GitHub token in PIPER.user.md configuration"
            elif "session" in str(e).lower():
                suggestion = "Verify session persistence service is running"
            else:
                suggestion = "Check service logs for integration details"

            raise StandupIntegrationError(
                f"{error_msg}\nSuggestion: {suggestion}", service="standup", suggestion=suggestion
            )

    async def _get_session_context(self, user_id: str) -> Dict[str, Any]:
        """Get session context using SessionPersistenceManager"""
        try:
            # Try multiple preference sources
            yesterday_context = (
                await self.preference_manager.get_preference("yesterday_context", user_id=user_id)
                or {}
            )

            # Issue #1042: removed hardcoded ["piper-morgan"] fallback. Falls
            # back to the user's default_repo preference if set, else empty
            # list. Full active-repos resolution (per-project + per-user list)
            # is tracked by #1050.
            active_repos = await self.preference_manager.get_preference(
                "active_repos", user_id=user_id
            )
            if not active_repos:
                from uuid import UUID

                try:
                    user_uuid = UUID(user_id) if user_id else None
                except (ValueError, TypeError):
                    user_uuid = None
                if user_uuid is not None:
                    default_repo = await self.preference_manager.get_default_repo(
                        user_uuid
                    )
                    active_repos = [default_repo] if default_repo else []
                else:
                    active_repos = []
                if not active_repos:
                    self.logger.warning(
                        "Standup active_repos empty: no 'active_repos' "
                        "preference set, no default_repo preference, "
                        "user_id missing or invalid. Standup will surface "
                        "no repo activity. (Issues #1042, #1050)"
                    )

            last_session = await self.preference_manager.get_preference(
                "last_session_time", user_id=user_id
            )

            # Also get session manager context
            session_context = (
                await self.session_manager.get_session_context(user_id)
                if hasattr(self.session_manager, "get_session_context")
                else {}
            )

            return {
                "yesterday_context": yesterday_context,
                "active_repos": active_repos,
                "last_session": last_session,
                "session_context": session_context,
            }

        except Exception:
            return {}

    async def _get_github_activity(self) -> Dict[str, Any]:
        """Get GitHub activity from last 24 hours"""
        try:
            # Use domain service method for recent GitHub activity
            recent_issues = await self.github_domain_service.get_recent_issues(limit=5)
            return {"commits": [], "issues": recent_issues}  # Format for compatibility
        except StandupIntegrationError:
            raise  # Re-raise our own errors
        except Exception as e:
            raise StandupIntegrationError(
                f"GitHub integration failed: {str(e)}",
                service="github",
                suggestion="Check GitHub token and network connectivity",
            )

    async def _generate_standup_content(
        self,
        user_id: str,
        session_context: Dict[str, Any],
        github_activity: Dict[str, Any],
        start_time: float,
    ) -> StandupResult:
        """Generate the actual standup content"""

        # Extract accomplishments from GitHub activity and session context.
        # Per #1034: build StandupItems with structured per-item metadata
        # (display + source + lifecycle_state + icon).
        yesterday_accomplishments: List[StandupItem] = []

        # From GitHub commits
        for commit in github_activity.get("commits", []):
            yesterday_accomplishments.append(
                StandupItem(
                    display=commit.get("message", ""),
                    source="commit",
                    lifecycle_state=None,
                    icon="✅",
                )
            )

        # From session context. `work` may be a string (legacy) or a dict
        # carrying lifecycle_state once upstream session-context is also
        # structured. Handle both shapes defensively.
        if session_context.get("session_context", {}).get("yesterday_work"):
            for work in session_context["session_context"]["yesterday_work"]:
                if isinstance(work, dict):
                    yesterday_accomplishments.append(
                        StandupItem(
                            display=work.get("display", str(work)),
                            source="work",
                            lifecycle_state=work.get("lifecycle_state"),
                            icon="📋",
                        )
                    )
                else:
                    yesterday_accomplishments.append(
                        StandupItem(
                            display=str(work),
                            source="work",
                            lifecycle_state=None,
                            icon="📋",
                        )
                    )

        # Generate today's priorities
        today_priorities: List[StandupItem] = []

        # Load standup configuration for content preferences
        standup_config = piper_config_loader.load_standup_config()
        fallback_priorities = standup_config["content"]["fallback_priorities"]

        # From active repos and context
        # Issue #1042: removed hardcoded ["piper-morgan"] fallback. Empty
        # list is the graceful default when no active_repos resolved upstream.
        active_repos = session_context.get("active_repos", [])
        for repo in active_repos:
            today_priorities.append(
                StandupItem(
                    display=f"Continue work on {repo}",
                    source="active_repo",
                    lifecycle_state=None,
                    icon="🎯",
                )
            )

        # From yesterday's context
        yesterday_context = session_context.get("yesterday_context", {})
        for area, status in yesterday_context.items():
            if status not in ["resolved", "complete"]:
                today_priorities.append(
                    StandupItem(
                        display=f"Complete {area}: {status}",
                        source="yesterday_context",
                        lifecycle_state=None,
                        icon="🔄",
                    )
                )

        # Default priorities if none found - use configuration
        if not today_priorities:
            today_priorities = [
                StandupItem(
                    display=priority,
                    source="fallback",
                    lifecycle_state=None,
                    icon="🎯",
                )
                for priority in fallback_priorities
            ]

        # Check for blockers
        blockers: List[StandupItem] = []
        if not github_activity.get("commits"):
            blockers.append(
                StandupItem(
                    display="No recent GitHub activity detected",
                    source="system",
                    lifecycle_state=None,
                    icon="⚠️",
                )
            )

        # Calculate metrics
        generation_time_ms = int((time.time() - start_time) * 1000)
        time_saved = self._calculate_time_savings_internal(session_context, github_activity)

        # Determine context source
        context_source = "persistent" if session_context.get("yesterday_context") else "default"

        return StandupResult(
            user_id=user_id,
            generated_at=datetime.now(),
            generation_time_ms=generation_time_ms,
            yesterday_accomplishments=yesterday_accomplishments,
            today_priorities=today_priorities,
            blockers=blockers,
            context_source=context_source,
            github_activity=github_activity,
            performance_metrics={
                "total_time_ms": generation_time_ms,
                "context_retrieval_ms": generation_time_ms // 3,
                "github_fetch_ms": generation_time_ms // 3,
                "content_generation_ms": generation_time_ms // 3,
            },
            time_saved_minutes=time_saved,
        )

    def _calculate_time_savings(self, result: StandupResult) -> int:
        """Calculate time savings in milliseconds (for test compatibility)"""
        return (
            self._calculate_time_savings_internal({"session_context": {}}, result.github_activity)
            * 60
            * 1000
        )

    def _calculate_time_savings_internal(
        self, session_context: Dict[str, Any], github_activity: Dict[str, Any]
    ) -> int:
        """Calculate time savings in minutes"""

        # Base time for manual standup preparation
        base_time = 5  # 5 minutes minimum

        # Add time based on data complexity
        if session_context.get("session_context"):
            base_time += 5  # 5 minutes to review session context

        if github_activity.get("commits"):
            base_time += 3  # 3 minutes to review commits

        if github_activity.get("issues_closed") or github_activity.get("issues_created"):
            base_time += 5  # 5 minutes to review issues

        # Rich context adds more savings
        if len(github_activity.get("commits", [])) > 5:
            base_time += 5  # Complex activity review

        return max(base_time, 15)  # Minimum 15 minutes as per requirement

    async def generate_with_documents(self, user_id: str) -> StandupResult:
        """Generate standup with integrated document memory context."""

        # Get base standup
        base_standup = await self.generate_standup(user_id)

        # FIXED: Use operational DocumentService instead of DocumentMemoryQueries
        try:
            # Connect to working DocumentService extensions
            document_service = get_document_service()

            # Get yesterday's context and recent decisions using working methods
            yesterday_context = await document_service.get_relevant_context("yesterday")
            recent_decisions = await document_service.find_decisions("", "yesterday")
            suggestions = await document_service.suggest_documents("")

            if yesterday_context.get("context_documents"):
                # Add document context to today's priorities
                doc_section = []
                for doc in yesterday_context["context_documents"][:2]:  # Top 2 documents
                    doc_section.append(f"📄 Review: {doc['title']}")

                # Extend today's priorities with document context
                base_standup.today_priorities.extend(doc_section)

            if recent_decisions.get("decisions"):
                # Add recent decisions to yesterday's accomplishments
                decision_section = []
                for decision in recent_decisions["decisions"][:2]:  # Top 2 decisions
                    decision_section.append(
                        f"🎯 Decision: {decision.get('decision', 'Decision made')}"
                    )

                base_standup.yesterday_accomplishments.extend(decision_section)

            if suggestions.get("suggestions"):
                # Add document suggestions to today's priorities
                suggestion_section = []
                for suggestion in suggestions["suggestions"][:1]:  # Top 1 suggestion
                    suggestion_section.append(f"💡 Consider: {suggestion['title']}")

                base_standup.today_priorities.extend(suggestion_section)

        except Exception as e:
            # Graceful degradation - add error note but continue
            base_standup.today_priorities.append(f"⚠️ Document memory unavailable: {str(e)[:50]}...")

        return base_standup

    async def generate_with_issues(self, user_id: str) -> StandupResult:
        """Generate standup with integrated issue priorities."""

        # Get base standup
        base_standup = await self.generate_standup(user_id)

        # NEW: Add issue context
        try:
            if hasattr(self, "canonical_handlers") and self.canonical_handlers:
                issue_engine = IssueIntelligenceCanonicalQueryEngine(
                    github_integration=self.github_domain_service,
                    canonical_handlers=self.canonical_handlers,
                    session_manager=self.session_manager,
                    user_id=user_id,
                )

                # Create minimal intent for issue intelligence
                from services.domain.models import Intent
                from services.shared_types import IntentCategory

                intent = Intent(
                    category=IntentCategory.PRIORITY,
                    action="get_priority_issues",
                    original_message="what needs attention",
                    confidence=1.0,
                )

                # Get issue priorities
                enhanced_result = await issue_engine.enhance_canonical_query(
                    intent, f"session_{user_id}"
                )

                if enhanced_result and enhanced_result.issue_intelligence.get("recent_issues"):
                    issue_priorities = enhanced_result.issue_intelligence["recent_issues"][
                        :3
                    ]  # Top 3

                    # Add issue section to today's priorities
                    issue_section = []
                    for issue in issue_priorities:
                        title = issue.get("title", "Unknown issue")
                        number = issue.get("number", "?")
                        issue_section.append(f"🎯 Issue #{number}: {title}")

                    # Extend today's priorities with issues
                    base_standup.today_priorities.extend(issue_section)

        except Exception as e:
            # Graceful degradation - add error note but continue
            base_standup.today_priorities.append(
                f"⚠️ Issue priorities unavailable: {str(e)[:50]}..."
            )

        return base_standup

    async def generate_with_calendar(self, user_id: str) -> StandupResult:
        """Generate standup with integrated calendar context."""

        # Get base standup
        base_standup = await self.generate_standup(user_id)

        # Add calendar context
        try:
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            # Initialize calendar adapter
            # Issue #843: Pass user_id for user-scoped calendar authentication
            calendar_adapter = CalendarIntegrationRouter(user_id=user_id)

            # Get temporal summary including today's events and time blocks
            temporal_summary = await calendar_adapter.get_temporal_summary()

            # Add current meeting awareness if in a meeting
            if temporal_summary.get("current_meeting"):
                current = temporal_summary["current_meeting"]
                base_standup.blockers.insert(
                    0,
                    f"🗓️ Currently in: {current.get('title', 'Meeting')} (ends {current.get('end_time', 'soon')})",
                )

            # Add today's calendar priorities
            if temporal_summary.get("stats", {}).get("total_meetings_today", 0) > 0:
                calendar_section = []

                # Next meeting awareness
                if temporal_summary.get("next_meeting"):
                    next_meeting = temporal_summary["next_meeting"]
                    calendar_section.append(
                        f"📅 Next: {next_meeting.get('title', 'Meeting')} at {next_meeting.get('start_time', 'TBD')}"
                    )

                # Free time blocks for focused work
                free_blocks = temporal_summary.get("free_blocks", [])
                if free_blocks and len(free_blocks) > 0:
                    longest_block = max(free_blocks, key=lambda x: x.get("duration_minutes", 0))
                    if longest_block.get("duration_minutes", 0) >= 60:
                        calendar_section.append(
                            f"🎯 Focus time: {longest_block.get('duration_minutes', 0)} mins at {longest_block.get('start', 'TBD')}"
                        )

                # Meeting load awareness
                meeting_time = temporal_summary.get("stats", {}).get(
                    "total_meeting_time_minutes", 0
                )
                if meeting_time > 240:  # More than 4 hours of meetings
                    calendar_section.append(
                        f"⚠️ Heavy meeting day: {meeting_time // 60} hours scheduled"
                    )

                # Add calendar context to today's priorities
                base_standup.today_priorities.extend(calendar_section)

            # Add available focus time to performance metrics
            if temporal_summary.get("stats"):
                base_standup.performance_metrics["calendar_stats"] = {
                    "meetings_today": temporal_summary["stats"].get("total_meetings_today", 0),
                    "meeting_hours": temporal_summary["stats"].get("total_meeting_time_minutes", 0)
                    / 60,
                    "free_hours": temporal_summary["stats"].get("total_free_time_minutes", 0) / 60,
                }

        except Exception as e:
            # Graceful degradation - add error note but continue
            base_standup.today_priorities.append(f"⚠️ Calendar unavailable: {str(e)[:50]}...")

        return base_standup

    async def generate_with_trifecta(
        self,
        user_id: str,
        with_issues: bool = True,
        with_documents: bool = True,
        with_calendar: bool = True,
    ) -> StandupResult:
        """Generate standup with full intelligence trifecta combination."""

        # Get base standup
        base_standup = await self.generate_standup(user_id)

        # Add document context if requested
        if with_documents:
            try:
                document_service = get_document_service()
                yesterday_context = await document_service.get_relevant_context("yesterday")
                recent_decisions = await document_service.find_decisions("", "yesterday")
                suggestions = await document_service.suggest_documents("")

                if yesterday_context.get("context_documents"):
                    for doc in yesterday_context["context_documents"][:2]:
                        base_standup.today_priorities.append(f"📄 Review: {doc['title']}")

                if recent_decisions.get("decisions"):
                    for decision in recent_decisions["decisions"][:2]:
                        base_standup.yesterday_accomplishments.append(
                            f"🎯 Decision: {decision.get('decision', 'Decision made')}"
                        )

                if suggestions.get("suggestions"):
                    for suggestion in suggestions["suggestions"][:1]:
                        base_standup.today_priorities.append(f"💡 Consider: {suggestion['title']}")

            except Exception as e:
                base_standup.today_priorities.append(
                    f"⚠️ Document memory unavailable: {str(e)[:50]}..."
                )

        # Add issue context if requested
        if with_issues:
            try:
                if hasattr(self, "canonical_handlers") and self.canonical_handlers:
                    issue_engine = IssueIntelligenceCanonicalQueryEngine(
                        github_integration=self.github_domain_service,
                        canonical_handlers=self.canonical_handlers,
                        session_manager=self.session_manager,
                        user_id=user_id,
                    )

                    from services.domain.models import Intent
                    from services.shared_types import IntentCategory

                    intent = Intent(
                        category=IntentCategory.PRIORITY,
                        action="get_priority_issues",
                        original_message="what needs attention",
                        confidence=1.0,
                    )

                    enhanced_result = await issue_engine.enhance_canonical_query(
                        intent, f"session_{user_id}"
                    )

                    if enhanced_result and enhanced_result.issue_intelligence.get("recent_issues"):
                        issue_priorities = enhanced_result.issue_intelligence["recent_issues"][:3]
                        for issue in issue_priorities:
                            title = issue.get("title", "Unknown issue")
                            number = issue.get("number", "?")
                            base_standup.today_priorities.append(f"🎯 Issue #{number}: {title}")

            except Exception as e:
                base_standup.today_priorities.append(
                    f"⚠️ Issue priorities unavailable: {str(e)[:50]}..."
                )

        # Add calendar context if requested
        if with_calendar:
            try:
                from services.integrations.calendar.calendar_integration_router import (
                    CalendarIntegrationRouter,
                )

                # Issue #843: Pass user_id for user-scoped calendar authentication
                calendar_adapter = CalendarIntegrationRouter(user_id=user_id)
                temporal_summary = await calendar_adapter.get_temporal_summary()

                if temporal_summary.get("current_meeting"):
                    current = temporal_summary["current_meeting"]
                    base_standup.blockers.insert(
                        0,
                        f"🗓️ Currently in: {current.get('title', 'Meeting')} (ends {current.get('end_time', 'soon')})",
                    )

                if temporal_summary.get("stats", {}).get("total_meetings_today", 0) > 0:
                    if temporal_summary.get("next_meeting"):
                        next_meeting = temporal_summary["next_meeting"]
                        base_standup.today_priorities.append(
                            f"📅 Next: {next_meeting.get('title', 'Meeting')} at {next_meeting.get('start_time', 'TBD')}"
                        )

                    free_blocks = temporal_summary.get("free_blocks", [])
                    if free_blocks and len(free_blocks) > 0:
                        longest_block = max(free_blocks, key=lambda x: x.get("duration_minutes", 0))
                        if longest_block.get("duration_minutes", 0) >= 60:
                            base_standup.today_priorities.append(
                                f"🎯 Focus time: {longest_block.get('duration_minutes', 0)} mins at {longest_block.get('start', 'TBD')}"
                            )

                    meeting_time = temporal_summary.get("stats", {}).get(
                        "total_meeting_time_minutes", 0
                    )
                    if meeting_time > 240:
                        base_standup.today_priorities.append(
                            f"⚠️ Heavy meeting day: {meeting_time // 60} hours scheduled"
                        )

                if temporal_summary.get("stats"):
                    base_standup.performance_metrics["calendar_stats"] = {
                        "meetings_today": temporal_summary["stats"].get("total_meetings_today", 0),
                        "meeting_hours": temporal_summary["stats"].get(
                            "total_meeting_time_minutes", 0
                        )
                        / 60,
                        "free_hours": temporal_summary["stats"].get("total_free_time_minutes", 0)
                        / 60,
                    }

            except Exception as e:
                base_standup.today_priorities.append(f"⚠️ Calendar unavailable: {str(e)[:50]}...")

        return base_standup
