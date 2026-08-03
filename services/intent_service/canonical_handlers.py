"""
Canonical Query Handlers
Specialized handlers for the 4 canonical categories:
- TEMPORAL: "What time is it?" / "What's on my calendar?"
- GUIDANCE: "What should I do?" / "How can you help me?"
- PORTFOLIO: Project management operations
- CONVERSATION: Simple greetings and conversational responses

Issue #286: CONVERSATION added to canonical section (was handled separately)
Issue #963: Removed dead handlers for IDENTITY, DISCOVERY, TRUST, MEMORY
  (migrated to conversational floor Apr 8-11). Removed STATUS, PRIORITY
  from can_handle() (floor-routed since #925, Apr 13). STATUS/PRIORITY
  handler methods retained as safety net (still callable from handle()).
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

from services.configuration.piper_config_loader import piper_config_loader
from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent, IntentCategory
from services.plugins import get_plugin_registry
from services.shared_types import IntentCategory as IntentCategoryEnum
from services.user_context_service import user_context_service

logger = structlog.get_logger()

# Issue #287: Timezone abbreviation mapping
# Maps IANA timezone identifiers to common abbreviations
TIMEZONE_ABBREVIATIONS = {
    # US Timezones
    "America/Los_Angeles": "PT",
    "America/New_York": "ET",
    "America/Chicago": "CT",
    "America/Denver": "MT",
    "America/Phoenix": "MST",  # Arizona (no DST)
    "America/Anchorage": "AKT",
    "Pacific/Honolulu": "HST",
    # International
    "Europe/London": "GMT",
    "Europe/Paris": "CET",
    "Europe/Berlin": "CET",
    "Asia/Tokyo": "JST",
    "Asia/Shanghai": "CST",
    "Asia/Hong_Kong": "HKT",
    "Asia/Singapore": "SGT",
    "Australia/Sydney": "AEDT",
    "Australia/Melbourne": "AEDT",
    # Fallback
    "UTC": "UTC",
}


class CanonicalHandlers:
    """Handlers for canonical standup queries using PIPER.md context"""

    def __init__(self):
        self.config_loader = piper_config_loader

    def _get_dynamic_capabilities(self) -> Dict[str, list]:
        """
        #923: Get dynamic capabilities from dispatcher registry + PluginRegistry.

        Capabilities are derived from runtime sources — not hardcoded lists.
        This ensures IDENTITY/DISCOVERY responses match what Piper can actually do.

        Returns a dict with:
        - core: Core PM capabilities (conversational, always present)
        - workflows: Registered workflow capabilities from dispatcher
        - integrations: Active integrations from plugins
        - capabilities_list: Flat list for API response
        """
        # Conversational capabilities always available
        core_capabilities = [
            "conversational PM guidance",
            "strategic thinking and prioritization",
        ]

        # #923: Workflow capabilities from dispatcher registry
        workflow_capabilities = []
        try:
            from services.intent_service.workflow_dispatcher import get_registered_workflows

            registered = get_registered_workflows()
            for wf_type, entry in registered.items():
                desc = entry.description or wf_type.replace("_", " ")
                workflow_capabilities.append(desc)
        except Exception as e:
            logger.warning(f"Could not get workflow capabilities: {e}")

        # Integration capabilities from plugin registry
        integrations = []
        try:
            registry = get_plugin_registry()
            plugin_status = registry.get_status_all()

            for name, status in plugin_status.items():
                is_configured = status.get("configured", False)
                is_active = status.get("active", False) or status.get("status") == "active"

                if is_configured or is_active:
                    plugin = registry.get_plugin(name)
                    if plugin:
                        metadata = plugin.get_metadata()
                        integrations.append(
                            {
                                "name": name,
                                "description": metadata.description,
                                "capabilities": metadata.capabilities,
                            }
                        )
        except Exception as e:
            logger.warning(f"Could not get plugin capabilities: {e}")

        # Build flat capabilities list for API response
        capabilities_list = core_capabilities.copy()
        capabilities_list.extend(workflow_capabilities)
        for integration in integrations:
            capabilities_list.append(f"{integration['name']} integration")

        return {
            "core": core_capabilities,
            "workflows": workflow_capabilities,
            "integrations": integrations,
            "capabilities_list": capabilities_list,
        }

    def can_handle(self, intent: Intent) -> bool:
        """Check if this handler can process the intent.

        Issue #963: After M1 floor inversion (#911) and Action Gate updates,
        only TEMPORAL, GUIDANCE, PORTFOLIO, and CONVERSATION remain canonical.
        IDENTITY/DISCOVERY/TRUST/MEMORY removed Apr 8-11.
        STATUS/PRIORITY removed Apr 13 (#925) — floor-routed via Action Gate.
        """
        canonical_categories = {
            IntentCategoryEnum.TEMPORAL,
            IntentCategoryEnum.GUIDANCE,  # Setup requests only (action gate enforces)
            IntentCategoryEnum.PORTFOLIO,  # Issue #675: Portfolio management queries
            IntentCategoryEnum.CONVERSATION,  # Issue #286: greeting only (action gate enforces)
            IntentCategoryEnum.PROVENANCE,  # Issue #1030 R4: "why did you suggest that?"
        }
        return intent.category in canonical_categories

    async def handle(self, intent: Intent, session_id: str, user_id: str = None) -> Dict:
        """Route to appropriate canonical handler.

        Issue #582: Added user_id parameter to enable database project lookup.
        Issue #963: Removed IDENTITY, DISCOVERY, TRUST, MEMORY branches (dead
        since Apr 8-11 Action Gate migration). Removed STATUS, PRIORITY branches
        (floor-routed since #925, Apr 13).
        """
        try:
            if intent.category == IntentCategoryEnum.TEMPORAL:
                # Issue #596: Pass user_id for timezone-aware calendar queries
                return await self._handle_temporal_query(intent, session_id, user_id)
            elif intent.category == IntentCategoryEnum.GUIDANCE:
                return await self._handle_guidance_query(intent, session_id, user_id)
            elif intent.category == IntentCategoryEnum.PORTFOLIO:
                # Issue #675: Handle portfolio management queries
                return await self._handle_portfolio_query(intent, session_id, user_id)
            elif intent.category == IntentCategoryEnum.CONVERSATION:
                # Issue #286: Handle CONVERSATION in canonical section
                # Issue #849: Thread user_id for user-scoped calendar auth
                return await self._handle_conversation_query(intent, session_id, user_id=user_id)
            elif intent.category == IntentCategoryEnum.PROVENANCE:
                # Issue #1030 R4: "why did you suggest that?" lookups
                return await self._handle_provenance_query(intent, session_id, user_id=user_id)
            else:
                # Fallback to conversation
                # Issue #908: Flag as generic — handler doesn't know what to do
                return {
                    "message": "I'm here to help with your questions!",
                    "is_generic_response": True,
                    "intent": {
                        "category": IntentCategoryEnum.CONVERSATION.value,
                        "action": "fallback_response",
                        "confidence": 0.5,
                        "context": {"original_intent": intent.category.value},
                    },
                    "requires_clarification": False,
                }

        except Exception as e:
            logger.error(f"Canonical handler failed: {e}")
            # Issue #908: Flag as generic — error response is not user-specific
            return {
                "message": "I'm having trouble processing that right now. You could try rephrasing, or ask me something else — I'm still here to help.",
                "is_generic_response": True,
                "intent": {
                    "category": IntentCategoryEnum.CONVERSATION.value,
                    "action": "error_fallback",
                    "confidence": 0.5,
                    "context": {"error": str(e)},
                },
                "requires_clarification": False,
            }

    async def _handle_temporal_query(
        self, intent: Intent, session_id: str, user_id: Optional[str] = None
    ) -> Dict:
        """
        Handle 'What day is it?' and time-related queries with spatial awareness.

        GREAT-4C Phase 1: Adds spatial intelligence for calendar detail level.
        Issue #499: Routes agenda requests to dedicated handler.
        Issue #501: Routes retrospective requests to dedicated handler.
        Issue #504: Routes last activity requests to dedicated handler.
        Issue #596: Added user_id parameter for timezone-aware calendar queries.
        """
        # Issue #499: Check if this is an agenda request first
        if self._detect_agenda_request(intent):
            # Issue #849: Thread user_id for user-scoped calendar auth
            return await self._handle_agenda_query(intent, session_id, user_id=user_id)

        # Issue #501: Check if this is a retrospective request
        if self._detect_retrospective_request(intent):
            return await self._handle_retrospective_query(intent, session_id)

        # Issue #504: Check if this is a last activity request
        project_name = self._detect_last_activity_request(intent)
        if project_name:
            return await self._handle_temporal_last_activity(intent, session_id, project_name)

        # Issue #505: Check if this is a duration request
        duration_project = self._detect_duration_request(intent)
        if duration_project:
            return await self._handle_temporal_project_duration(
                intent, session_id, duration_project, user_id=user_id
            )

        from services.configuration.piper_config_loader import piper_config_loader

        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Load timezone from configuration
        standup_config = piper_config_loader.load_standup_config()
        timezone = standup_config["timing"]["timezone"]
        # Issue #287 Fix #1: Use timezone abbreviation instead of city name
        timezone_short = TIMEZONE_ABBREVIATIONS.get(timezone, "UTC")
        # #1163 (sibling of #1150): compute date + time in the CONFIGURED tz so
        # they're correct regardless of the server process's tz. Was naive
        # datetime.now() (server-local) + a manual label — on a non-local-tz
        # instance that reported the wrong time/date. Fail-safe to naive.
        try:
            from zoneinfo import ZoneInfo

            _now = datetime.now(ZoneInfo(timezone))
        except Exception:
            _now = datetime.now()
        current_date = _now.strftime("%A, %B %d, %Y")
        current_time = _now.strftime(f"%I:%M %p {timezone_short}")

        # Base message
        if spatial_pattern == "EMBEDDED":
            # Brief: Just date/time
            message = f"{current_date}"
        else:
            # Standard/Granular: Include time
            message = f"Today is {current_date} at {current_time}."

        calendar_context = {}

        # Enhanced: Get real calendar data from CalendarIntegrationRouter
        try:
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            # Issue #596: Pass user_id for timezone-aware calendar queries
            # Issue #843: Pass user_id for user-scoped calendar authentication
            calendar_adapter = CalendarIntegrationRouter(user_id=user_id)
            temporal_summary = await calendar_adapter.get_temporal_summary(user_id=user_id)

            # Issue #597: Check explicit success state before interpreting calendar data
            # If calendar query failed, don't make claims about meeting count
            if not temporal_summary.get("success", True):  # Default True for backward compat
                logger.warning(
                    f"Calendar query failed: {temporal_summary.get('error', 'Unknown error')}"
                )
                if spatial_pattern != "EMBEDDED":
                    message += "\n\n⚠️ Note: Calendar data unavailable right now."
                calendar_context["calendar_service"] = "unavailable"
                calendar_context["error"] = temporal_summary.get("error")
            # Issue #790: Trust-gated calendar setup offer (supersedes #789 silent default).
            # Greeting context: not an explicit calendar query, so user_intent_mentions_calendar=False.
            # Helper looks up offer state + trust stage and decides whether to surface a one-time
            # offer or stay silent based on prior state.
            elif not temporal_summary.get("calendar_connected", True):
                logger.info(
                    "Calendar not connected - applying trust-gated offer policy (Issue #790)"
                )
                calendar_context["calendar_connected"] = False
                offer_text = await self._apply_calendar_offer(
                    user_id=user_id, user_intent_mentions_calendar=False
                )
                if offer_text:
                    message += "\n\n" + offer_text
            # Adjust calendar detail based on spatial pattern
            elif spatial_pattern == "EMBEDDED":
                # EMBEDDED: Minimal - just current/next meeting
                if temporal_summary.get("current_meeting"):
                    current_meeting = temporal_summary["current_meeting"]
                    message += f" (in meeting)"
                    calendar_context["current_meeting"] = current_meeting.get("title", "Meeting")
                elif temporal_summary.get("next_meeting"):
                    next_meeting = temporal_summary["next_meeting"]
                    message += f" (next: {next_meeting.get('start_time', 'TBD')})"
                    calendar_context["next_meeting"] = {
                        "time": next_meeting.get("start_time", "TBD")
                    }

            elif spatial_pattern == "GRANULAR":
                # GRANULAR: Comprehensive calendar breakdown
                if temporal_summary.get("current_meeting"):
                    current_meeting = temporal_summary["current_meeting"]
                    message += f"\n\n**Current Meeting**: {current_meeting.get('title', 'Meeting')}"
                    message += f"\n- Duration: {current_meeting.get('duration', 'Unknown')}"
                    calendar_context["current_meeting"] = current_meeting.get("title", "Meeting")

                if temporal_summary.get("next_meeting"):
                    next_meeting = temporal_summary["next_meeting"]
                    message += f"\n\n**Next Meeting**: {next_meeting.get('title', 'Meeting')}"
                    message += f"\n- Time: {next_meeting.get('start_time', 'TBD')}"
                    calendar_context["next_meeting"] = {
                        "title": next_meeting.get("title", "Meeting"),
                        "time": next_meeting.get("start_time", "TBD"),
                    }

                free_blocks = temporal_summary.get("free_blocks", [])
                if free_blocks:
                    message += f"\n\n**Focus Time Available**: {len(free_blocks)} blocks"
                    for block in free_blocks[:3]:  # Top 3
                        message += f"\n- {block.get('duration_minutes', 0)} min at {block.get('start', 'TBD')}"

                stats = temporal_summary.get("stats", {})
                if stats.get("total_meetings_today", 0) > 0:
                    meeting_count = stats["total_meetings_today"]
                    meeting_hours = stats.get("total_meeting_time_minutes", 0) / 60
                    message += f"\n\n**Meeting Load**: {meeting_count} meetings ({meeting_hours:.1f} hours)"
                    calendar_context["meeting_load"] = {
                        "count": meeting_count,
                        "hours": meeting_hours,
                    }

            else:
                # DEFAULT: Standard detail
                # Issue #287 Fix #2: Prevent contradictory messages
                # Only show stats block if no current/next meeting mentioned
                if temporal_summary.get("current_meeting"):
                    current_meeting = temporal_summary["current_meeting"]
                    # Issue #597: Use normalized 'title' field, fallback to 'summary'
                    meeting_title = current_meeting.get("title") or current_meeting.get(
                        "summary", "a meeting"
                    )
                    message += f" You're currently in: {meeting_title}"
                    calendar_context["current_meeting"] = meeting_title
                elif temporal_summary.get("next_meeting"):
                    next_meeting = temporal_summary["next_meeting"]
                    # Issue #597: Use pre-formatted time if available, fallback to manual formatting
                    start_time_formatted = next_meeting.get("start_time_formatted")
                    if not start_time_formatted:
                        start_time_raw = next_meeting.get("start_time", "TBD")
                        try:
                            from datetime import datetime as dt

                            start_dt = dt.fromisoformat(start_time_raw)
                            start_time_formatted = start_dt.strftime("%I:%M %p").lstrip("0")
                        except (ValueError, TypeError):
                            start_time_formatted = start_time_raw
                    # Issue #597: Use normalized 'title' field, fallback to 'summary'
                    meeting_title = next_meeting.get("title") or next_meeting.get(
                        "summary", "Meeting"
                    )
                    message += f" Your next meeting is: {meeting_title} at {start_time_formatted}"
                    calendar_context["next_meeting"] = {
                        "title": meeting_title,
                        "time": start_time_formatted,
                    }
                else:
                    # No current or upcoming meeting - show daily summary
                    stats = temporal_summary.get("stats", {})
                    if stats.get("total_meetings_today", 0) > 0:
                        meeting_count = stats["total_meetings_today"]
                        message += f" ({meeting_count} meetings scheduled today)"
                        calendar_context["meeting_load"] = {"count": meeting_count}
                    else:
                        message += " (No meetings - great day for deep work!)"
                        calendar_context["calendar_status"] = "free_day"

        except Exception as e:
            # Issue #287 Fix #3: Enhanced calendar validation and error handling
            # Calendar unavailable - log but continue with helpful message
            logger.warning(f"Calendar service unavailable: {e}", exc_info=True)

            if spatial_pattern != "EMBEDDED":
                # Provide user-friendly error message (not for EMBEDDED - too verbose)
                error_type = type(e).__name__
                if "timeout" in str(e).lower() or "TimeoutError" in error_type:
                    message += "\n\n⚠️ Note: Calendar check timed out. Your calendar may be temporarily unavailable."
                elif "auth" in str(e).lower() or "permission" in str(e).lower():
                    message += "\n\n⚠️ Note: Calendar authentication needed. Please check your calendar connection."
                else:
                    message += "\n\n⚠️ Note: I couldn't access your calendar right now. The calendar service may be unavailable."

            calendar_context["calendar_service"] = "unavailable"
            calendar_context["fallback_used"] = True
            calendar_context["error_type"] = type(e).__name__

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.TEMPORAL.value,
                "action": "provide_current_time_with_calendar",
                "confidence": 1.0,
                "context": {
                    "current_date": current_date,
                    "current_time": current_time,
                    "timezone": "Pacific Time",
                    "calendar_context": calendar_context,
                },
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    def _detect_project_specific_query(self, intent: Intent, projects: List[str]) -> Optional[str]:
        """
        Issue #500: Detect if query asks about a specific project.

        Returns the matched project name if found, None otherwise.
        Patterns recognized:
        - "What's the status of HealthTrack?"
        - "How is the HealthTrack project going?"
        - "Status of HealthTrack"
        - "Tell me about HealthTrack"
        """
        if not intent or not intent.original_message or not projects:
            return None

        query = intent.original_message.lower()

        # Patterns that indicate project-specific query
        specific_patterns = [
            r"status of\s+(.+?)(?:\?|$|\s+project)",
            r"how is\s+(.+?)\s+(?:going|doing|project)",
            r"tell me about\s+(.+?)(?:\?|$)",
            r"update on\s+(.+?)(?:\?|$)",
            r"(.+?)\s+status(?:\?|$)",
            r"what about\s+(.+?)(?:\?|$)",
        ]

        import re

        for pattern in specific_patterns:
            match = re.search(pattern, query)
            if match:
                potential_project = match.group(1).strip()
                # Try to match against known projects (case-insensitive)
                for project in projects:
                    if project.lower() == potential_project.lower():
                        return project
                    # Fuzzy match: project name contains the query term or vice versa
                    if (
                        potential_project.lower() in project.lower()
                        or project.lower() in potential_project.lower()
                    ):
                        return project

        return None

    def _detect_landscape_request(self, intent: Intent) -> bool:
        """
        Issue #510: Detect if this is a 'show me the project landscape' query.
        Returns True if landscape pattern detected, False otherwise.
        """
        import re

        if not intent or not intent.original_message:
            return False

        query = intent.original_message.lower()

        # Patterns for landscape/portfolio queries
        patterns = [
            r"project\s+landscape",
            r"portfolio",
            r"project\s+overview",
            r"all\s+projects?\s+health",
            r"project\s+health",
            r"portfolio\s+health",
        ]

        for pattern in patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True

        return False

    def _detect_status_report_request(self, intent: Intent) -> bool:
        """
        Issue #513: Detect if this is a 'give me a status report' query.
        Returns True if status report pattern detected, False otherwise.
        """
        import re

        if not intent or not intent.original_message:
            return False

        query = intent.original_message.lower()

        # Patterns for status report queries
        patterns = [
            r"status\s+report",
            r"give\s+me\s+(?:a\s+)?status",
            r"project\s+status",
            r"what'?s?\s+the\s+status",
            r"current\s+status",
            r"how\s+are\s+things\s+going",
        ]

        for pattern in patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True

        return False

    def _calculate_project_health(
        self, project_name: str, github_data: Optional[Dict]
    ) -> Dict[str, str]:
        """
        Issue #510: Calculate project health status.

        Returns dict with:
        - status: "healthy", "at-risk", or "stalled"
        - reason: Human-readable explanation

        Health criteria:
        - Healthy: Activity within 14 days
        - At-risk: 14-30 days since last activity OR >20 open issues
        - Stalled: >30 days since last activity
        """
        from datetime import datetime

        if not github_data:
            return {"status": "unknown", "reason": "No GitHub data available"}

        # Check days since last activity
        last_activity = github_data.get("updated_at")
        days_since_activity = None

        if last_activity:
            try:
                dt = datetime.fromisoformat(last_activity.replace("Z", "+00:00"))
                days_since_activity = (datetime.now(dt.tzinfo) - dt).days
            except Exception:
                pass

        # Check open issues count
        open_issues = github_data.get("open_issues_count", 0)

        # Determine health status
        if days_since_activity is not None:
            if days_since_activity > 30:
                return {
                    "status": "stalled",
                    "reason": f"{days_since_activity} days since last activity",
                }
            elif days_since_activity > 14 or open_issues > 20:
                reasons = []
                if days_since_activity > 14:
                    reasons.append(f"{days_since_activity} days since last activity")
                if open_issues > 20:
                    reasons.append(f"{open_issues} open issues")
                return {"status": "at-risk", "reason": ", ".join(reasons)}
            else:
                return {
                    "status": "healthy",
                    "reason": f"Active within {days_since_activity} days",
                }

        # Fallback to issue count only
        if open_issues > 20:
            return {"status": "at-risk", "reason": f"{open_issues} open issues"}

        return {"status": "healthy", "reason": "Recent activity"}

    def _detect_project_list_request(self, intent: Intent) -> bool:
        """
        Issue #509: Detect if this is a project list query.
        Returns True if asking for list of projects.

        Patterns recognized:
        - "what projects are we working on"
        - "list projects"
        - "show projects"
        - "our projects"
        """
        if not intent or not intent.original_message:
            return False

        query = intent.original_message.lower()

        project_list_patterns = [
            "what projects",
            "list projects",
            "show projects",
            "our projects",
            "my projects",
            "all projects",
            "which projects",
        ]

        return any(pattern in query for pattern in project_list_patterns)

    def _format_project_specific_status(
        self, project: str, metadata: Dict, user_context, spatial_pattern: Optional[str] = None
    ) -> str:
        """
        Issue #500: Format detailed status for a single project.
        """
        if spatial_pattern == "EMBEDDED":
            # Brief format
            issues_count = metadata.get("open_issues_count")
            if issues_count is not None:
                return f"{project}: {issues_count} open issues"
            return f"{project}: Active"

        # Standard/Granular format
        lines = [f"**{project} Status**\n"]

        # GitHub metadata if available
        if metadata.get("has_github"):
            issues_count = metadata.get("open_issues_count")
            if issues_count is not None:
                lines.append(f"📋 **Open Issues**: {issues_count}")

                # Show issue previews
                issues_preview = metadata.get("issues_preview", [])
                if issues_preview and spatial_pattern != "EMBEDDED":
                    for issue in issues_preview[: 5 if spatial_pattern == "GRANULAR" else 3]:
                        title = issue.get("title", "Untitled")[:60]
                        number = issue.get("number", "?")
                        lines.append(f"  - #{number}: {title}")

            repo = metadata.get("repository", "")
            if repo:
                lines.append(f"\n🔗 **Repository**: {repo}")
        else:
            lines.append("📊 **Status**: Active development")
            lines.append("ℹ️ No GitHub repository linked - add one in Settings → Projects")

        # Add organization context
        if user_context and user_context.organization:
            lines.append(f"\n🏢 **Organization**: {user_context.organization}")

        # Add priorities if GRANULAR
        if spatial_pattern == "GRANULAR" and user_context and user_context.priorities:
            lines.append("\n🎯 **Current Priorities**:")
            for priority in user_context.priorities[:3]:
                lines.append(f"  - {priority}")

        return "\n".join(lines)

    async def _handle_status_query(
        self, intent: Intent, session_id: str, user_id: str = None
    ) -> Dict:
        """
        Handle 'What am I working on?' queries with spatial awareness.

        GREAT-4C Phase 1: Adds spatial intelligence for response granularity.
        GREAT-4C Phase 2: Adds error handling for missing configuration.
        Issue #500: Routes project-specific queries to dedicated handler.
        Issue #582: Added user_id parameter to enable database project lookup.
        """
        # Try to get user context with error handling
        # Issue #582: Pass user_id to enable loading projects from database
        try:
            user_context = await user_context_service.get_user_context(session_id, user_id)
        except Exception as e:
            logger.error(f"Failed to load user context: {e}")
            # Issue #908: Flag as generic — config error is not user-specific
            return {
                "message": "I'm having trouble accessing your configuration right now. "
                "Your PIPER.md file may be missing or unreadable. "
                "Would you like help setting it up?",
                "error": "config_unavailable",
                "action_required": "setup_piper_config",
                "is_generic_response": True,
                "intent": {
                    "category": IntentCategoryEnum.STATUS.value,
                    "action": "provide_status",
                    "confidence": 1.0,
                },
            }

        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Get projects from user context
        projects = user_context.projects

        # Check if we have project data
        if not projects:
            # ADR-059: Onboarding session start disabled (onboarding on ice).
            # Instead of offering interactive onboarding, give a simple floor response.
            # Issue #908: Flag as generic — no project data means template response
            return {
                "message": "You don't have any active projects configured yet. "
                "You can tell me about your projects anytime and I'll help you track them.",
                "is_generic_response": True,
                "intent": {
                    "category": IntentCategoryEnum.STATUS.value,
                    "action": "provide_status",
                    "confidence": 1.0,
                },
            }

        # Issue #509: Check for project list request first
        if self._detect_project_list_request(intent):
            return await self._handle_spatial_project_list(
                intent, session_id, user_context, spatial_pattern
            )

        # Issue #510: Check for landscape/portfolio health request
        if self._detect_landscape_request(intent):
            return await self._handle_spatial_project_landscape(
                intent, session_id, user_context, spatial_pattern
            )

        # Issue #513: Check for status report request
        if self._detect_status_report_request(intent):
            return await self._handle_status_report(
                intent, session_id, user_context, spatial_pattern
            )

        # Issue #500: Check for project-specific query
        specific_project = self._detect_project_specific_query(intent, projects)
        if specific_project:
            # Fetch metadata for just this project
            project_metadata = await self._get_project_metadata([specific_project])
            metadata = project_metadata.get(specific_project, {})
            message = self._format_project_specific_status(
                specific_project, metadata, user_context, spatial_pattern
            )
            return {
                "message": message,
                "intent": {
                    "category": IntentCategoryEnum.STATUS.value,
                    "action": "provide_project_specific_status",
                    "confidence": 1.0,
                    "context": {
                        "project": specific_project,
                        "spatial_pattern": spatial_pattern,
                        "has_github": metadata.get("has_github", False),
                    },
                },
                "spatial_pattern": spatial_pattern,
                "project_specific": True,
                "requires_clarification": False,
            }

        # Issue #18: Fetch project metadata from GitHub (for all projects)
        project_metadata = await self._get_project_metadata(projects)

        # Adjust response detail based on spatial pattern
        if spatial_pattern == "GRANULAR":
            # Detailed status with full project breakdown
            message = self._format_detailed_status(projects, user_context, project_metadata)
        elif spatial_pattern == "EMBEDDED":
            # Brief consolidated status
            message = self._format_consolidated_status(projects, user_context, project_metadata)
        else:
            # Standard moderate detail
            message = self._format_standard_status(projects, user_context, project_metadata)

        message += self._degrade_nudge(project_metadata)  # #1231

        project_context = {
            "projects": projects,
            "spatial_pattern": spatial_pattern,
            "organization": user_context.organization,
            "project_metadata": project_metadata,  # Issue #18: Include metadata
        }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.STATUS.value,
                "action": "provide_project_status",
                "confidence": 1.0,
                "context": project_context,
            },
            "spatial_pattern": spatial_pattern,
            "has_github_metadata": bool(project_metadata),  # Issue #18: Flag for metadata
            "requires_clarification": False,
        }

    def _format_detailed_status(
        self, projects: list, user_context, project_metadata: Dict = None
    ) -> str:
        """GRANULAR: Full project details with comprehensive breakdown.

        Issue #18: Enhanced with real project metadata from GitHub when available.
        """
        if not projects:
            return "No active projects configured in your PIPER.md."

        project_metadata = project_metadata or {}
        details = ["Here's your detailed project status:\n"]

        for i, project in enumerate(projects, 1):
            details.append(f"\n**{i}. {project}**")

            # Issue #18: Use real metadata if available
            metadata = project_metadata.get(project, {})
            if metadata.get("has_github"):
                repo = metadata.get("repository", "")
                issues_count = metadata.get("open_issues_count")
                if issues_count is not None:
                    details.append(f"  - Open Issues: {issues_count}")
                    # Show issue previews in detailed view
                    issues_preview = metadata.get("issues_preview", [])
                    if issues_preview:
                        details.append("  - Recent issues:")
                        for issue in issues_preview[:3]:
                            title = issue.get("title", "Untitled")[:50]
                            number = issue.get("number", "?")
                            details.append(f"    - #{number}: {title}")
                if repo:
                    details.append(f"  - Repository: {repo}")
            else:
                details.append(f"  - Status: Active development")

            details.append(f"  - Organization: {user_context.organization or 'Not specified'}")

        if user_context.priorities:
            details.append(f"\n\nCurrent priorities: {', '.join(user_context.priorities[:3])}")

        return "\n".join(details)

    def _format_consolidated_status(
        self, projects: list, user_context, project_metadata: Dict = None
    ) -> str:
        """EMBEDDED: Brief overview suitable for embedded context.

        Issue #18: Enhanced with total open issues count when available.
        """
        if not projects:
            return "No active projects."

        project_metadata = project_metadata or {}

        # Issue #18: Calculate total open issues if metadata available
        total_issues = 0
        has_metadata = False
        for project in projects:
            metadata = project_metadata.get(project, {})
            if metadata.get("has_github"):
                has_metadata = True
                issues_count = metadata.get("open_issues_count")
                if issues_count is not None:
                    total_issues += issues_count

        # Build response with optional issue count
        if len(projects) == 1:
            base = f"Working on: {projects[0]}"
        elif len(projects) <= 3:
            base = f"Working on {len(projects)} projects: {', '.join(projects)}"
        else:
            base = f"Working on {len(projects)} projects: {', '.join(projects[:3])} + {len(projects)-3} more"

        if has_metadata and total_issues > 0:
            return f"{base} ({total_issues} open issues)"
        return base

    def _format_standard_status(
        self, projects: list, user_context, project_metadata: Dict = None
    ) -> str:
        """DEFAULT: Moderate detail level for standard queries.

        Issue #18: Enhanced with open issues count per project when available.
        """
        if not projects:
            return "No active projects configured in your PIPER.md. Add projects to the 'Projects' section to see them here."

        project_metadata = project_metadata or {}
        summary = [
            f"You're working on {len(projects)} active project{'s' if len(projects) != 1 else ''}:\n"
        ]

        for project in projects[:5]:  # Top 5
            # Issue #18: Add issue count if available
            metadata = project_metadata.get(project, {})
            issues_count = metadata.get("open_issues_count")
            if issues_count is not None:
                summary.append(f"- {project} ({issues_count} open issues)")
            else:
                summary.append(f"- {project}")

        if len(projects) > 5:
            summary.append(f"- ... and {len(projects) - 5} more")

        if user_context.organization:
            summary.append(f"\nOrganization: {user_context.organization}")

        return "\n".join(summary)

    def _format_project_list_embedded(self, projects: list, project_metadata: Dict = None) -> str:
        """
        Issue #509: EMBEDDED format for project list - brief overview.
        Returns: "You have X active projects: [names]"
        """
        if not projects:
            return "No active projects"

        project_count = len(projects)
        if project_count == 1:
            return f"You have 1 active project: {projects[0]}"
        elif project_count <= 3:
            return f"You have {project_count} active projects: {', '.join(projects)}"
        else:
            return f"You have {project_count} active projects: {', '.join(projects[:3])} + {project_count - 3} more"

    def _format_project_list_standard(self, projects: list, project_metadata: Dict = None) -> str:
        """
        Issue #509: STANDARD format for project list - names + issue counts + last activity.
        """
        if not projects:
            return "You don't have any active projects configured in your PIPER.md yet."

        project_metadata = project_metadata or {}
        lines = [f"You have {len(projects)} active project{'s' if len(projects) != 1 else ''}:\n"]

        for project in projects:
            metadata = project_metadata.get(project, {})

            # Build project line with metadata
            project_line = f"- **{project}**"

            # Add issue count if available
            issues_count = metadata.get("open_issues_count")
            if issues_count is not None:
                project_line += f" - {issues_count} open issue{'s' if issues_count != 1 else ''}"

            # Add last activity if available
            last_activity = metadata.get("last_activity")
            if last_activity:
                project_line += f", last activity: {last_activity}"

            lines.append(project_line)

        return "\n".join(lines)

    def _format_project_list_granular(self, projects: list, project_metadata: Dict = None) -> str:
        """
        Issue #509: GRANULAR format for project list - full details per project.
        """
        if not projects:
            return "You don't have any active projects configured in your PIPER.md yet."

        project_metadata = project_metadata or {}
        lines = ["**Your Active Projects**\n"]

        for i, project in enumerate(projects, 1):
            metadata = project_metadata.get(project, {})

            lines.append(f"\n**{i}. {project}**")

            # Repository info
            repo = metadata.get("repository")
            if repo:
                lines.append(f"   - Repository: {repo}")

            # Open issues
            issues_count = metadata.get("open_issues_count")
            if issues_count is not None:
                lines.append(f"   - Open Issues: {issues_count}")

                # Show issue previews
                issues_preview = metadata.get("issues_preview", [])
                if issues_preview:
                    lines.append("   - Recent issues:")
                    for issue in issues_preview[:3]:
                        title = issue.get("title", "Untitled")[:50]
                        number = issue.get("number", "?")
                        lines.append(f"     - #{number}: {title}")

            # Last activity
            last_activity = metadata.get("last_activity")
            if last_activity:
                lines.append(f"   - Last Activity: {last_activity}")

            # GitHub status
            if metadata.get("has_github"):
                lines.append("   - GitHub: Connected")
            else:
                lines.append("   - GitHub: Not configured")

        return "\n".join(lines)

    async def _handle_spatial_project_list(
        self, intent: Intent, session_id: str, user_context, spatial_pattern: Optional[str]
    ) -> Dict:
        """
        Issue #509: Handle "What projects are we working on?" queries with enhanced metadata.

        Returns formatted list of projects with GitHub metadata (issue counts, last activity).
        Response format varies based on spatial_pattern (EMBEDDED/STANDARD/GRANULAR).
        """
        # Get projects from user context
        projects = user_context.projects

        # Check if we have projects
        if not projects:
            return {
                "message": "You don't have any active projects configured in your PIPER.md yet. "
                "Would you like me to help you set up your project portfolio?",
                "action_required": "configure_projects",
                "intent": {
                    "category": IntentCategoryEnum.STATUS.value,
                    "action": "provide_project_list",
                    "confidence": 1.0,
                },
                "spatial_pattern": spatial_pattern,
                "requires_clarification": False,
            }

        # Fetch project metadata from GitHub
        project_metadata = await self._get_project_metadata(projects)

        # Format response based on spatial pattern
        if spatial_pattern == "EMBEDDED":
            message = self._format_project_list_embedded(projects, project_metadata)
        elif spatial_pattern == "GRANULAR":
            message = self._format_project_list_granular(projects, project_metadata)
        else:
            message = self._format_project_list_standard(projects, project_metadata)

        message += self._degrade_nudge(project_metadata)  # #1231

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.STATUS.value,
                "action": "provide_project_list",
                "confidence": 1.0,
                "context": {
                    "projects": projects,
                    "spatial_pattern": spatial_pattern,
                    "has_github_metadata": bool(project_metadata),
                },
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    async def _handle_priority_query(
        self, intent: Intent, session_id: str, user_id: str = None
    ) -> Dict:
        """
        Handle 'What's my top priority?' queries with spatial awareness.

        GREAT-4C Phase 1: Adds spatial intelligence for response granularity.
        GREAT-4C Phase 2: Adds error handling for missing configuration.
        Issue #511: Routes priority recommendation queries to dedicated handler.
        Issue #582: Added user_id parameter to enable database project lookup.
        """
        # Try to get user context with error handling
        # Issue #582: Pass user_id to enable loading projects from database
        try:
            user_context = await user_context_service.get_user_context(session_id, user_id)
        except Exception as e:
            logger.error(f"Failed to load user context: {e}")
            # Issue #908: Flag as generic — config error is not user-specific
            return {
                "message": "I'm having trouble accessing your configuration right now. "
                "Your PIPER.md file may be missing or unreadable. "
                "Would you like help setting it up?",
                "error": "config_unavailable",
                "action_required": "setup_piper_config",
                "is_generic_response": True,
                "intent": {
                    "category": IntentCategoryEnum.PRIORITY.value,
                    "action": "provide_priority",
                    "confidence": 1.0,
                },
            }

        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Issue #511: Check if this is a priority recommendation request
        if self._detect_priority_recommendation_request(intent):
            return await self._handle_spatial_priority_recommendation(
                intent, session_id, user_context, spatial_pattern
            )

        # Get priorities from user context
        priorities = user_context.priorities

        # Check if we have priority data
        if not priorities:
            # Issue #908: Flag as generic — no priority data means template response
            return {
                "message": "You don't have any priorities configured in your PIPER.md yet. "
                "Would you like me to help you set up your priority list?",
                "action_required": "configure_priorities",
                "is_generic_response": True,
                "intent": {
                    "category": IntentCategoryEnum.PRIORITY.value,
                    "action": "provide_priority",
                    "confidence": 1.0,
                },
            }

        # Issue #496: Fetch priority metadata from GitHub
        priority_metadata = await self._get_priority_metadata(user_id=user_id)

        # Adjust response detail based on spatial pattern
        if spatial_pattern == "GRANULAR":
            # Detailed priorities with breakdown
            message = self._format_detailed_priorities(priorities, user_context, priority_metadata)
        elif spatial_pattern == "EMBEDDED":
            # Brief priority statement
            message = self._format_consolidated_priorities(
                priorities, user_context, priority_metadata
            )
        else:
            # Standard moderate detail
            message = self._format_standard_priorities(priorities, user_context, priority_metadata)

        priority_context = {
            "priorities": priorities,
            "spatial_pattern": spatial_pattern,
            "organization": user_context.organization,
            "priority_metadata": priority_metadata,  # Issue #496: Include metadata
        }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.PRIORITY.value,
                "action": "provide_top_priority",
                "confidence": 1.0,
                "context": priority_context,
            },
            "spatial_pattern": spatial_pattern,
            "has_github_metadata": bool(priority_metadata.get("has_github")),  # Issue #496
            "requires_clarification": False,
        }

    def _format_detailed_priorities(
        self, priorities: list, user_context, priority_metadata: Dict = None
    ) -> str:
        """GRANULAR: Detailed priority breakdown.

        Issue #496: Enhanced with GitHub high-priority issues when available.
        """
        if not priorities:
            return "No priorities configured in your PIPER.md."

        priority_metadata = priority_metadata or {}
        details = ["Here are your priorities in detail:\n"]

        for i, priority in enumerate(priorities, 1):
            details.append(f"\n**Priority {i}: {priority}**")
            details.append(f"  - Status: Active")

        # Issue #496: Add high-priority GitHub issues if available
        high_priority_issues = priority_metadata.get("high_priority_issues", [])
        if high_priority_issues:
            details.append("\n\n**GitHub High-Priority Issues:**")
            for issue in high_priority_issues[:5]:
                number = issue.get("number", "?")
                title = issue.get("title", "Untitled")
                labels = ", ".join(issue.get("labels", []))
                details.append(f"  - #{number}: {title}")
                if labels:
                    details.append(f"    Labels: {labels}")
        elif priority_metadata.get("source_failed"):
            # #1425/F2: source errored — be honest that we couldn't check, never
            # assert emptiness (the false-claim this fix kills).
            details.append(
                "\n\n*I couldn't check your high-priority GitHub issues just now — "
                "try again in a moment.*"
            )
        elif priority_metadata.get("has_github"):
            details.append("\n\n*No high-priority (P0/P1) GitHub issues found.*")
        elif priority_metadata.get("degrade_reason"):
            # #1231 (Arch-ratified): derive the "connect me" nudge from the shared
            # reason→copy policy — not a silent omission, not an inline string.
            from services.intent_service.degradation_copy import degrade_nudge

            details.append(f"\n\n*{degrade_nudge(priority_metadata['degrade_reason'])}*")

        if user_context.organization:
            details.append(f"\n\nOrganization context: {user_context.organization}")

        return "\n".join(details)

    def _format_consolidated_priorities(
        self, priorities: list, user_context, priority_metadata: Dict = None
    ) -> str:
        """EMBEDDED: Brief priority summary.

        Issue #496: Enhanced with high-priority issue count when available.
        """
        if not priorities:
            return "No priorities set."

        priority_metadata = priority_metadata or {}
        high_priority_count = len(priority_metadata.get("high_priority_issues", []))

        base = f"Top priority: {priorities[0]}"
        if len(priorities) > 1:
            base += f" ({len(priorities)} total)"

        if high_priority_count > 0:
            return f"{base} + {high_priority_count} urgent GitHub issues"
        return base

    def _format_standard_priorities(
        self, priorities: list, user_context, priority_metadata: Dict = None
    ) -> str:
        """DEFAULT: Moderate detail for priorities.

        Issue #496: Enhanced with high-priority GitHub issues when available.
        """
        if not priorities:
            return "No priorities configured in your PIPER.md. Add priorities to the 'Priorities' section to see them here."

        priority_metadata = priority_metadata or {}
        message = [f"Your top priority today is: **{priorities[0]}**\n"]

        if len(priorities) > 1:
            message.append("\nOther priorities:")
            for priority in priorities[1:4]:  # Show up to 3 more
                message.append(f"- {priority}")

            if len(priorities) > 4:
                message.append(f"- ... and {len(priorities) - 4} more")

        # Issue #496: Add high-priority GitHub issues if available
        high_priority_issues = priority_metadata.get("high_priority_issues", [])
        if high_priority_issues:
            message.append("\n\n**Urgent GitHub Issues:**")
            for issue in high_priority_issues[:3]:  # Top 3 in standard view
                number = issue.get("number", "?")
                title = issue.get("title", "Untitled")
                message.append(f"- #{number}: {title}")

        if user_context.organization:
            message.append(f"\n\nOrganization: {user_context.organization}")

        return "\n".join(message)

    def _get_immediate_focus(self, current_hour: int, user_context) -> str:
        """Get time-based immediate focus suggestion with fallback for missing context."""
        if 6 <= current_hour < 9:
            if user_context and user_context.organization:
                return f"Morning development work - perfect time for deep focus on {user_context.organization} implementation and coordination."
            else:
                return "Morning development work - perfect time for deep focus and complex problem-solving."
        elif 9 <= current_hour < 14:
            if user_context and user_context.organization:
                return f"Collaboration time - coordinate with your team on {user_context.organization} implementation."
            else:
                return "Collaboration time - good for meetings and team coordination."
        elif 14 <= current_hour < 17:
            if user_context and user_context.projects:
                top_project = user_context.projects[0]
                return f"Project execution - work on {top_project} tasks."
            else:
                return "Execution time - work on your current tasks and deliverables."
        elif 17 <= current_hour < 18:
            return "Documentation and handoff preparation - wrap up today's work and prepare for tomorrow."
        else:
            return "Flexible time - consider strategic planning or methodology refinement."

    async def _get_calendar_context(self, user_id: Optional[str] = None) -> Optional[Dict]:
        """
        Issue #495: Get calendar context for meeting-aware guidance.

        Returns next meeting and free time blocks if calendar is configured.
        Falls back gracefully if calendar is not available.

        Issue #847: Uses config_service.is_configured(user_id) instead of
        plugin.is_configured() which always returns False without user context (#784).
        """
        try:
            # Issue #847: Check configuration using config_service with user_id
            # Plugin-level is_configured() always returns False without user context (#784)
            if not user_id:
                return None

            from services.integrations.calendar.config_service import CalendarConfigService

            try:
                config_service = CalendarConfigService()
                if not config_service.is_configured(user_id):
                    return None
            except Exception:
                return None

            # Get calendar router from plugin
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            # Issue #849: Thread user_id for user-scoped calendar auth
            calendar_router = CalendarIntegrationRouter(user_id=user_id)

            # Get next meeting
            next_meeting = await calendar_router.get_next_meeting()
            free_blocks = await calendar_router.get_free_time_blocks()

            calendar_context = {
                "has_calendar": True,
            }

            if next_meeting:
                calendar_context["next_meeting"] = {
                    "title": next_meeting.get("title", next_meeting.get("summary", "Untitled")),
                    "start": next_meeting.get("start"),
                    "end": next_meeting.get("end"),
                }

            if free_blocks:
                # Get first free block
                first_free = free_blocks[0] if free_blocks else None
                if first_free:
                    calendar_context["next_free_block"] = {
                        "start": first_free.get("start"),
                        "duration_minutes": first_free.get("duration_minutes"),
                    }
                calendar_context["free_blocks_count"] = len(free_blocks)

            return calendar_context

        except Exception as e:
            logger.debug(f"Calendar context unavailable: {e}")
            return None

    async def _apply_calendar_offer(
        self,
        *,
        user_id: Optional[str],
        user_intent_mentions_calendar: bool,
    ) -> str:
        """Issue #790: Apply trust-gated calendar setup offer policy.

        Looks up the user's trust stage + prior offer state, runs the
        decision helper, and persists any new state. Returns the offer
        text to append to the response message (empty if no offer).

        Returns "" if user_id is missing (anonymous request) or any
        infra lookup fails — never raises.
        """
        if not user_id:
            return ""

        try:
            from uuid import UUID

            from services.database.session_factory import AsyncSessionFactory
            from services.domain.user_preference_manager import UserPreferenceManager
            from services.intent_service.calendar_offer_policy import (
                decide_calendar_offer,
            )
            from services.repositories.user_trust_profile_repository import (
                UserTrustProfileRepository,
            )
            from services.shared_types import TrustStage
            from services.trust.trust_computation_service import (
                TrustComputationService,
            )

            user_uuid = UUID(user_id)
            preference_manager = UserPreferenceManager()
            current_state = await preference_manager.get_calendar_setup_offer_state(user_uuid)

            trust_stage = TrustStage.NEW
            try:
                async with AsyncSessionFactory.session_scope() as db_session:
                    trust_repo = UserTrustProfileRepository(db_session)
                    trust_service = TrustComputationService(trust_repo)
                    resolved = await trust_service.get_trust_stage(user_uuid)
                    if resolved is not None:
                        trust_stage = resolved
            except Exception as e:
                logger.debug(f"Trust stage lookup failed for offer policy: {e}")

            decision = decide_calendar_offer(
                calendar_connected=False,
                current_state=current_state,
                user_intent_mentions_calendar=user_intent_mentions_calendar,
                trust_stage=trust_stage,
            )

            if decision.new_state is not None and decision.new_state != current_state:
                await preference_manager.set_calendar_setup_offer_state(
                    user_uuid, decision.new_state
                )

            return decision.offer_text if decision.should_offer else ""
        except Exception as e:
            logger.warning(f"Calendar offer policy failed: {e}")
            return ""

    def _degrade_nudge(self, metadata: Dict) -> str:
        """#1231 (Arch-ratified): the "connect me" nudge to append ONCE when a connector was
        skipped (not-configured/not-connected), derived from the shared reason→copy policy —
        never a silent omission. '' when the connector is available. Once-per-response for
        connector-level degrade (Arch: per-item only for partial/item-level misses)."""
        reason = metadata.get("__degrade_reason__") if metadata else None
        if reason is None:
            return ""
        from services.intent_service.degradation_copy import degrade_nudge

        return f"\n\n*{degrade_nudge(reason)}*"

    async def _get_project_metadata(self, projects: list) -> Dict[str, Dict]:
        """
        Issue #18: Get real project metadata from GitHub.

        Returns metadata for each project including:
        - open_issues_count: Number of open issues
        - has_github: Whether GitHub is connected
        - repository: Repository name if matched

        Falls back gracefully if GitHub is not available.
        """
        project_metadata = {}

        try:
            # Check if GitHub plugin is registered and configured
            registry = get_plugin_registry()
            github_plugin = registry.get_plugin("github")

            if not github_plugin or not github_plugin.is_configured():
                from services.mcp.consumer.connector import DegradationReason

                logger.debug("GitHub not configured — honest-degrade (#1231)")
                return {"__degrade_reason__": DegradationReason.NOT_CONFIGURED}

            # Import and instantiate GitHub domain service
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            # Check connection status
            connection_status = github_service.get_connection_status()
            if not connection_status.get("connected"):
                from services.mcp.consumer.connector import DegradationReason

                logger.debug("GitHub not connected — honest-degrade (#1231)")
                return {"__degrade_reason__": DegradationReason.CONNECT_REQUIRED}

            # Get repositories list
            repos = github_service.list_repositories()
            repo_names = {repo.get("name", "").lower(): repo for repo in repos}

            # Try to match projects to repositories
            for project in projects:
                project_lower = project.lower().replace(" ", "-").replace("_", "-")

                # Look for matching repository
                matched_repo = None
                for repo_name, repo_data in repo_names.items():
                    if project_lower in repo_name or repo_name in project_lower:
                        matched_repo = repo_data
                        break

                if matched_repo:
                    # Get open issues for this repository
                    try:
                        full_name = matched_repo.get("full_name", "")
                        open_issues = await github_service.get_open_issues(full_name, days_back=30)
                        project_metadata[project] = {
                            "has_github": True,
                            "repository": full_name,
                            "open_issues_count": len(open_issues),
                            "issues_preview": open_issues[:3] if open_issues else [],
                        }
                    except Exception as e:
                        logger.debug(f"Could not get issues for {project}: {e}")
                        project_metadata[project] = {
                            "has_github": True,
                            "repository": matched_repo.get("full_name", ""),
                            "open_issues_count": None,
                        }
                else:
                    project_metadata[project] = {
                        "has_github": False,
                        "repository": None,
                    }

            return project_metadata

        except Exception as e:
            logger.debug(f"Project metadata unavailable: {e}")
            return {}

    async def _get_priority_metadata(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Issue #496: Get priority-related metadata from GitHub.

        Returns metadata including:
        - high_priority_issues: List of P0/P1 labeled issues
        - has_github: Whether GitHub is connected
        - milestone_info: Current milestone if any

        Falls back gracefully if GitHub is not available.

        Issue #847: Uses config_service.is_configured(user_id) instead of
        plugin.is_configured() which always returns False without user context (#784).
        """
        try:
            # Issue #847: Check configuration using config_service with user_id
            # Plugin-level is_configured() always returns False without user context (#784)
            if not user_id:
                logger.debug("No user_id, returning empty priority metadata")
                return {}

            from services.integrations.github.config_service import GitHubConfigService

            try:
                config_service = GitHubConfigService()
                if not config_service.is_configured(user_id):
                    # #1231 (Arch-ratified): carry the DegradationReason so the formatter
                    # surfaces "connect me" via the shared copy policy, never a silent {}.
                    # NOT_CONFIGURED = onboard gap (never set up), distinct from CONNECT_REQUIRED.
                    from services.mcp.consumer.connector import DegradationReason

                    logger.debug("GitHub not configured for user — honest-degrade (#1231)")
                    return {"degrade_reason": DegradationReason.NOT_CONFIGURED}
            except Exception:
                return {}

            # Import and instantiate GitHub domain service
            from services.domain.github_domain_service import GitHubDomainService

            github_service = GitHubDomainService()

            # Check connection status
            connection_status = github_service.get_connection_status()
            if not connection_status.get("connected"):
                # Configured but this user hasn't connected → CONNECT_REQUIRED (reconnect gap).
                from services.mcp.consumer.connector import DegradationReason

                logger.debug("GitHub not connected — honest-degrade (#1231)")
                return {"degrade_reason": DegradationReason.CONNECT_REQUIRED}

            # Get default repository from the user-scoped resolver (#1366 Component A).
            # piper_config_loader.load_github_config().default_repository is a single
            # unscoped file read at server-instance level — on a shared instance it would
            # hand every user PM's own default repo. ConnectorConfigService (via
            # get_user_default_repo) is the per-user, DB-backed source of truth.
            from uuid import UUID

            from services.integrations.github.repo_resolver import get_user_default_repo

            default_repo = await get_user_default_repo(UUID(user_id))

            if not default_repo:
                return {"has_github": True, "high_priority_issues": []}

            # Get open issues and filter by priority labels
            try:
                open_issues = await github_service.get_open_issues(default_repo, days_back=30)

                # Filter for high-priority issues (P0, P1, priority-high, urgent, critical)
                priority_labels = {
                    "p0",
                    "p1",
                    "priority-high",
                    "high-priority",
                    "urgent",
                    "critical",
                }
                high_priority_issues = []

                for issue in open_issues:
                    issue_labels = {label.lower() for label in issue.get("labels", [])}
                    if issue_labels & priority_labels:  # Intersection
                        high_priority_issues.append(
                            {
                                "number": issue.get("number"),
                                "title": issue.get("title", "")[:60],
                                "labels": issue.get("labels", []),
                                "url": issue.get("url", issue.get("html_url", "")),
                            }
                        )

                return {
                    "has_github": True,
                    "repository": default_repo,
                    "high_priority_issues": high_priority_issues[:5],  # Top 5
                    "total_open_issues": len(open_issues),
                }

            except Exception as e:  # silent-ok: failure surfaces as honest "couldn't check" via source_failed (#1425)
                # #1425/F2: source FAILED — flag it so the renderer says "I couldn't
                # check" (honest) instead of "no high-priority issues found" (a false
                # claim about the user's work). Raised from DEBUG to WARNING: a
                # swallowed error that changes what the user is told is not debug noise.
                logger.warning(f"Could not get priority issues (source failed): {e}")
                return {"has_github": True, "high_priority_issues": [], "source_failed": True}

        except Exception as e:  # silent-ok: failure surfaces as honest "couldn't check" via source_failed (#1425)
            logger.warning(f"Priority metadata unavailable (source failed): {e}")
            return {"source_failed": True}

    def _synthesize_focus_recommendation(
        self,
        current_hour: int,
        user_context,
        calendar_context: Optional[Dict],
        project_metadata: Optional[Dict],
        priority_metadata: Optional[Dict],
    ) -> Dict[str, Any]:
        """
        Issue #497: Synthesize focus recommendation from all available context.

        Combines calendar, projects, and priorities to provide personalized guidance.
        Suggests missing integrations when appropriate.

        Returns:
            Dict with:
            - recommendation: Primary focus recommendation
            - time_available: Minutes until next commitment (if known)
            - urgent_items: Count of urgent items needing attention
            - missing_integrations: List of integrations that would help
            - context_level: "rich" | "partial" | "minimal"
        """
        recommendation = {
            "primary_focus": None,
            "time_available": None,
            "urgent_items": 0,
            "open_issues": 0,
            "missing_integrations": [],
            "context_level": "minimal",
            "suggestions": [],
        }

        # Determine context richness
        has_calendar = bool(calendar_context and calendar_context.get("has_calendar"))
        has_projects = bool(project_metadata)
        has_priorities = bool(priority_metadata and priority_metadata.get("has_github"))
        has_user_priorities = bool(user_context and user_context.priorities)

        if has_calendar and has_projects and has_priorities:
            recommendation["context_level"] = "rich"
        elif has_calendar or has_projects or has_priorities:
            recommendation["context_level"] = "partial"

        # Suggest missing integrations
        if not has_calendar:
            recommendation["missing_integrations"].append("calendar")
        if not has_priorities and not has_projects:
            recommendation["missing_integrations"].append("github")

        # Calculate time available until next meeting
        if calendar_context and calendar_context.get("next_meeting"):
            next_meeting = calendar_context["next_meeting"]
            start_time = next_meeting.get("start")
            if start_time:
                # Try to parse and calculate minutes
                try:
                    from datetime import datetime

                    # Handle ISO format or time string
                    if "T" in str(start_time):
                        meeting_time = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                        now = (
                            datetime.now(meeting_time.tzinfo)
                            if meeting_time.tzinfo
                            else datetime.now()
                        )
                        delta = meeting_time - now
                        recommendation["time_available"] = max(0, int(delta.total_seconds() / 60))
                except Exception:
                    pass  # Can't parse, skip time calculation

        # Count urgent items
        if priority_metadata:
            urgent_issues = priority_metadata.get("high_priority_issues", [])
            recommendation["urgent_items"] = len(urgent_issues)
            recommendation["open_issues"] = priority_metadata.get("total_open_issues", 0)

        # Generate primary focus recommendation
        time_available = recommendation["time_available"]
        urgent_count = recommendation["urgent_items"]

        # Build contextual recommendation
        if time_available is not None and time_available < 30:
            # Less than 30 minutes - quick tasks only
            recommendation["primary_focus"] = "quick-tasks"
            recommendation["suggestions"].append(
                "Short time window - handle quick tasks or prepare for your meeting"
            )
        elif time_available is not None and time_available < 60:
            # 30-60 minutes - focused but short
            if urgent_count > 0:
                recommendation["primary_focus"] = "urgent-issues"
                recommendation["suggestions"].append(
                    f"Address {urgent_count} urgent issue(s) before your meeting"
                )
            else:
                recommendation["primary_focus"] = "focused-work"
                recommendation["suggestions"].append(
                    "Good window for focused work on your top priority"
                )
        elif urgent_count > 0:
            # Has urgent items
            recommendation["primary_focus"] = "urgent-issues"
            recommendation["suggestions"].append(
                f"You have {urgent_count} urgent GitHub issue(s) requiring attention"
            )
        elif has_user_priorities:
            # Focus on top priority
            recommendation["primary_focus"] = "top-priority"
            top_priority = user_context.priorities[0]
            recommendation["suggestions"].append(f"Focus on your top priority: {top_priority}")
        else:
            # Generic time-based recommendation
            recommendation["primary_focus"] = "time-based"

        # Add integration suggestions
        if recommendation["missing_integrations"]:
            missing = recommendation["missing_integrations"]
            if "calendar" in missing and "github" in missing:
                recommendation["suggestions"].append(
                    "Tip: Connect your calendar and GitHub for more personalized guidance"
                )
            elif "calendar" in missing:
                recommendation["suggestions"].append(
                    "Tip: Connect your calendar for meeting-aware recommendations"
                )
            elif "github" in missing:
                recommendation["suggestions"].append(
                    "Tip: Connect GitHub to see your project issues and priorities"
                )

        return recommendation

    def _format_detailed_guidance(
        self,
        current_hour: int,
        user_context,
        calendar_context: Optional[Dict] = None,
        project_metadata: Optional[Dict] = None,
        priority_metadata: Optional[Dict] = None,
        focus_recommendation: Optional[Dict] = None,
    ) -> str:
        """GRANULAR: Comprehensive guidance with all timeframes and context.

        Issue #497: Enhanced with synthesized focus recommendation.
        """
        focus = self._get_immediate_focus(current_hour, user_context)
        priority_text = (
            user_context.priorities[0]
            if user_context and user_context.priorities
            else "your key priorities"
        )
        org_text = (
            user_context.organization
            if user_context and user_context.organization
            else "your projects"
        )

        focus_recommendation = focus_recommendation or {}
        details = ["Here's comprehensive guidance for your focus:\n"]

        # Issue #497: Show synthesized recommendation first if available
        suggestions = focus_recommendation.get("suggestions", [])
        if suggestions:
            details.append("**Recommended Focus**:")
            for suggestion in suggestions[:2]:  # Top 2 suggestions
                details.append(f"  → {suggestion}")
            details.append("")

        details.append(f"**Immediate Focus (Right Now)**:")
        details.append(f"  {focus}\n")

        # Issue #495: Add calendar context if available
        if calendar_context and calendar_context.get("next_meeting"):
            next_meeting = calendar_context["next_meeting"]
            meeting_title = next_meeting.get("title", "Upcoming meeting")
            time_available = focus_recommendation.get("time_available")
            details.append(f"**Next Meeting**: {meeting_title}")
            if time_available is not None:
                details.append(f"  Time available: {time_available} minutes\n")
            elif next_meeting.get("start"):
                details.append(f"  Starting at: {next_meeting['start']}\n")
            else:
                details.append("")

        # Issue #497: Show urgent issues if available
        urgent_count = focus_recommendation.get("urgent_items", 0)
        if urgent_count > 0 and priority_metadata:
            high_priority_issues = priority_metadata.get("high_priority_issues", [])
            details.append(f"**Urgent Items ({urgent_count})**:")
            for issue in high_priority_issues[:3]:
                number = issue.get("number", "?")
                title = issue.get("title", "Untitled")
                details.append(f"  - #{number}: {title}")
            details.append("")

        details.append(f"**Today's Key Focus**:")
        details.append(f"  - Primary priority: {priority_text}")
        if user_context and user_context.priorities and len(user_context.priorities) > 1:
            details.append(f"  - Secondary priorities:")
            for priority in user_context.priorities[1:3]:
                details.append(f"    - {priority}")

        details.append(f"\n**This Week**:")
        details.append(f"  - Continue work on {org_text}")
        if user_context and user_context.projects:
            details.append(f"  - Active projects:")
            for project in user_context.projects[:3]:
                # Issue #497: Add issue count from project metadata
                meta = (project_metadata or {}).get(project, {})
                issues_count = meta.get("open_issues_count")
                if issues_count is not None:
                    details.append(f"    - {project} ({issues_count} issues)")
                else:
                    details.append(f"    - {project}")

        details.append(f"\n**Strategic Direction**:")
        details.append(
            f"  - Deliver on your priorities while maintaining progress across all projects"
        )
        details.append(f"  - Balance deep focus work with collaboration and coordination")
        details.append(f"  - Maintain quality standards throughout implementation")

        # Issue #497: Add integration tips if missing
        missing = focus_recommendation.get("missing_integrations", [])
        if missing:
            tip = suggestions[-1] if suggestions and "Tip:" in suggestions[-1] else None
            if tip:
                details.append(f"\n*{tip}*")

        return "\n".join(details)

    def _format_consolidated_guidance(
        self,
        current_hour: int,
        user_context,
        calendar_context: Optional[Dict] = None,
        focus_recommendation: Optional[Dict] = None,
    ) -> str:
        """EMBEDDED: Brief guidance suitable for embedded context.

        Issue #497: Uses synthesized focus recommendation when available.
        """
        focus_recommendation = focus_recommendation or {}
        suggestions = focus_recommendation.get("suggestions", [])

        # Issue #497: Use synthesized recommendation if available
        if suggestions:
            # Get first actionable suggestion (not a tip)
            for suggestion in suggestions:
                if not suggestion.startswith("Tip:"):
                    # Shorten for embedded context
                    if len(suggestion) > 50:
                        return f"Focus: {suggestion[:47]}..."
                    return f"Focus: {suggestion}"

        # Fallback to time-based focus
        focus = self._get_immediate_focus(current_hour, user_context)

        # Extract just the key action from the focus
        if "Morning development" in focus:
            return "Focus: Deep work"
        elif "Collaboration" in focus:
            return "Focus: Team coordination"
        elif "Project execution" in focus or "Execution time" in focus:
            return "Focus: Task execution"
        elif "Documentation" in focus:
            return "Focus: Wrap-up and handoff"
        else:
            return "Focus: Strategic planning"

    def _format_standard_guidance(
        self,
        current_hour: int,
        user_context,
        calendar_context: Optional[Dict] = None,
        priority_metadata: Optional[Dict] = None,
        focus_recommendation: Optional[Dict] = None,
    ) -> str:
        """
        DEFAULT: Moderate detail for standard guidance queries.
        Issue #495: Includes calendar context when available.
        Issue #497: Enhanced with synthesized focus recommendation.
        """
        focus = self._get_immediate_focus(current_hour, user_context)
        priority_text = (
            user_context.priorities[0]
            if user_context and user_context.priorities
            else "your key priorities"
        )
        org_text = (
            user_context.organization
            if user_context and user_context.organization
            else "your projects"
        )

        focus_recommendation = focus_recommendation or {}
        message = []

        # Issue #497: Show synthesized recommendation first if available
        suggestions = focus_recommendation.get("suggestions", [])
        if suggestions:
            # Get actionable suggestions (not tips)
            actionable = [s for s in suggestions if not s.startswith("Tip:")]
            if actionable:
                message.append(f"**Recommended**: {actionable[0]}\n")

        message.append(f"Based on your current priorities and the time of day:\n")
        message.append(f"**Right Now**: {focus}\n")

        # Issue #495: Add meeting context if available
        if calendar_context and calendar_context.get("next_meeting"):
            next_meeting = calendar_context["next_meeting"]
            meeting_title = next_meeting.get("title", "Upcoming meeting")
            time_available = focus_recommendation.get("time_available")
            if time_available is not None:
                message.append(
                    f'**Note**: You have "{meeting_title}" in {time_available} minutes.\n'
                )
            else:
                message.append(f'**Note**: You have "{meeting_title}" coming up.\n')

        # Issue #497: Show urgent items if available
        urgent_count = focus_recommendation.get("urgent_items", 0)
        if urgent_count > 0:
            message.append(
                f"**Urgent**: {urgent_count} high-priority GitHub issue(s) need attention.\n"
            )

        message.append(f"**Today's Key Focus**: {priority_text}\n")
        message.append(f"**This Week**: Continue work on {org_text}\n")
        message.append(
            f"**Strategic Direction**: Deliver on your priorities while maintaining progress across all projects."
        )

        # Issue #497: Add integration tips if missing
        tips = [s for s in suggestions if s.startswith("Tip:")]
        if tips:
            message.append(f"\n*{tips[0]}*")

        return "\n".join(message)

    def _detect_setup_request(self, intent: Intent) -> Optional[str]:
        """
        Issue #498: Detect if the intent is asking about setting up or configuring something.

        Returns the setup topic if detected, None otherwise.
        Recognizes common setup patterns:
        - "help me set up my projects"
        - "set up my project portfolio"
        - "configure my projects"
        - "set up integrations"
        """
        if not intent:
            return None
        # #1460 idiom B: attribute first, dict fallback — dict-only writers
        # (unbackfilled paths like the pre-fix detect_multiple route) must
        # still gate correctly. This detector guards the #814 setup flow.
        original_message = intent.original_message or (intent.context or {}).get(
            "original_message", ""
        )
        if not original_message:
            return None

        raw_input = original_message.lower()

        # Setup patterns with their topics
        setup_patterns = [
            # Project setup
            (["set up", "setup", "configure"], ["project", "projects", "portfolio"], "projects"),
            # Integration setup
            (
                ["set up", "setup", "configure", "connect"],
                ["integration", "integrations", "github", "slack", "calendar", "notion"],
                "integrations",
            ),
            # General setup
            (
                ["set up", "setup", "configure", "get started"],
                ["piper", "everything", "system"],
                "general",
            ),
        ]

        for verbs, nouns, topic in setup_patterns:
            has_verb = any(verb in raw_input for verb in verbs)
            has_noun = any(noun in raw_input for noun in nouns)
            if has_verb and has_noun:
                return topic

        return None

    def _format_project_setup_guidance(self, user_context=None) -> Dict:
        """
        Issue #498: Format guidance response for project setup requests.

        Returns structured guidance with link to settings page.
        """
        has_projects = user_context and user_context.projects

        if has_projects:
            # User already has projects - offer to manage them
            project_count = len(user_context.projects)
            message = f"""I see you already have {project_count} project(s) configured!

**Your Current Projects:**
"""
            for project in user_context.projects[:5]:
                message += f"- {project}\n"

            if len(user_context.projects) > 5:
                message += f"- ... and {len(user_context.projects) - 5} more\n"

            message += """
To add or manage projects, visit the **Projects** settings page:
→ [Settings → Projects](/settings/projects)

From there you can:
1. Add new projects
2. Edit existing project details
3. Link projects to GitHub repositories

Would you like me to explain what information to include for each project?"""
            # Issue #852: Track contextual offer for continuation
            offer_hint = {
                "continuation_hint": "explain what information to include for each project",
                "offer_text": "Would you like me to explain what information to include for each project?",
            }
        else:
            # No projects yet - guide through setup
            message = """I'd be happy to help you set up your projects!

To configure your project portfolio:
1. Visit the **Projects** settings page: [Settings → Projects](/settings/projects)
2. Click "Add Project" to create a new project
3. Optionally link it to a GitHub repository for issue tracking

**What to include for each project:**
- **Name**: A clear, descriptive project name
- **Description**: Brief summary of the project's purpose
- **Repository**: (Optional) GitHub repo for issue integration

Would you like me to explain more about how Piper uses project context, or are you ready to set up your first project?"""
            # Issue #852: Track contextual offer for continuation
            offer_hint = {
                "continuation_hint": "explain how Piper uses project context",
                "offer_text": "Would you like me to explain more about how Piper uses project context?",
            }

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.GUIDANCE.value,
                "action": "provide_setup_guidance",
                "confidence": 1.0,
                "context": {
                    "setup_topic": "projects",
                    "has_existing_projects": has_projects,
                    "settings_link": "/settings/projects",
                },
            },
            "setup_type": "projects",
            "requires_clarification": False,
            "offer_hint": offer_hint,  # Issue #852
        }

    async def _handle_project_setup_request(
        self, intent: Intent, session_id: str, user_id: str = None
    ) -> Dict:
        """
        Issue #814: Handle explicit project setup requests with interactive routing.

        0 projects: Start interactive portfolio onboarding conversation
        N>0 projects: Acknowledge existing + offer to add more (CXO Option C)
        No user_id: Fall back to static guidance
        """
        from services.personality.formality import DEFAULT_WARMTH, formality_label

        # If no user_id, fall back to static guidance
        if not user_id:
            return self._format_project_setup_guidance(None)

        # Fetch user context (same service already used in this code path)
        user_context = None
        try:
            user_context = await user_context_service.get_user_context(session_id, user_id)
        except Exception as e:
            logger.warning(f"Could not fetch user context for setup routing: {e}")

        has_projects = user_context and user_context.projects
        project_names = user_context.projects if has_projects else []
        project_count = len(project_names)

        # ADR-059: Interactive onboarding disabled (on ice).
        # Instead of launching onboarding workflow, give helpful guidance.
        if project_count == 0:
            return self._format_project_setup_guidance(None)

        # Case 2: N>0 projects — state-aware response (CXO Option C)
        label = formality_label(DEFAULT_WARMTH)

        if label == "warm":
            intro = f"You've already got {project_count} project{'s' if project_count != 1 else ''} set up"
            outro = "Want to add another, or would you like to review what you have?"
        elif label == "professional":
            intro = f"You currently have {project_count} active project{'s' if project_count != 1 else ''}"
            outro = "I can help you add a new project or review your existing portfolio."
        else:  # balanced
            intro = f"You have {project_count} project{'s' if project_count != 1 else ''} in your portfolio"
            outro = "Would you like to add another project, or review your current setup?"

        project_list = ""
        for project in project_names[:5]:
            project_list += f"- {project}\n"
        if len(project_names) > 5:
            project_list += f"- ... and {len(project_names) - 5} more\n"

        message = f"""{intro}!

**Your Projects:**
{project_list}
{outro}"""

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.GUIDANCE.value,
                "action": "provide_setup_guidance",
                "confidence": 1.0,
                "context": {
                    "setup_topic": "projects",
                    "has_existing_projects": True,
                    "project_count": project_count,
                    "triggered_by": "explicit_setup_request",
                },
            },
            "setup_type": "projects",
            "requires_clarification": False,
            "offer_hint": {
                "continuation_hint": "add another project or review existing portfolio",
                "offer_text": outro,
            },
        }

    def _format_integration_setup_guidance(self) -> Dict:
        """
        Issue #498: Format guidance response for integration setup requests.

        Returns structured guidance with link to settings page.
        """
        # Check which integrations are configured
        integrations_status = []
        try:
            registry = get_plugin_registry()
            plugin_status = registry.get_status_all()

            for name, status in plugin_status.items():
                is_configured = status.get("configured", False)
                integrations_status.append(
                    {
                        "name": name,
                        "configured": is_configured,
                    }
                )
        except Exception as e:
            logger.debug(f"Could not check integration status: {e}")

        configured = [i["name"] for i in integrations_status if i.get("configured")]
        not_configured = [i["name"] for i in integrations_status if not i.get("configured")]

        message = """I'd be happy to help you set up integrations!

**Available Integrations:**
"""
        if configured:
            message += "\n✅ **Connected:**\n"
            for name in configured[:5]:
                message += f"  - {name.title()}\n"

        if not_configured:
            message += "\n⚪ **Not connected:**\n"
            for name in not_configured[:5]:
                message += f"  - {name.title()}\n"

        message += """
To connect integrations, visit the **Settings** hub:
→ [Settings](/settings)

**Popular integrations to connect:**
1. **GitHub** - Issue tracking and project management
2. **Slack** - Team communication and notifications
3. **Calendar** - Meeting awareness and scheduling
4. **Notion** - Documentation and knowledge base

Each integration has its own setup process. Would you like guidance on setting up a specific integration?

Once you've connected an integration, let me know and I'll help test the connection."""

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.GUIDANCE.value,
                "action": "provide_setup_guidance",
                "confidence": 1.0,
                "context": {
                    "setup_topic": "integrations",
                    "configured_integrations": configured,
                    "available_integrations": not_configured,
                    "settings_link": "/settings",
                },
            },
            "setup_type": "integrations",
            "requires_clarification": False,
            # Issue #852: Track contextual offer for continuation
            "offer_hint": {
                "continuation_hint": "provide guidance on setting up a specific integration",
                "offer_text": "Would you like guidance on setting up a specific integration?",
            },
        }

    def _format_general_setup_guidance(self) -> Dict:
        """
        Issue #498: Format guidance response for general setup requests.

        Returns overview of all setup options.
        """
        message = """I'd be happy to help you get set up with Piper!

**Getting Started Checklist:**

1. **Configure your profile** ⚙️
   → [Settings](/settings)
   Set your name, timezone, and preferences

2. **Set up your projects** 📁
   → [Settings → Projects](/settings/projects)
   Add the projects you're working on

3. **Connect integrations** 🔗
   → [Settings](/settings)
   - GitHub for issue tracking
   - Slack for notifications
   - Calendar for meeting awareness

4. **Define your priorities** 🎯
   Edit your PIPER.md file to set daily priorities

**Quick Tips:**
- Ask "What can you help me with?" to see my capabilities
- Ask "What am I working on?" to see your project status
- Ask "What should I focus on?" for personalized guidance

What would you like to set up first?"""

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.GUIDANCE.value,
                "action": "provide_setup_guidance",
                "confidence": 1.0,
                "context": {
                    "setup_topic": "general",
                    "settings_link": "/settings",
                },
            },
            "setup_type": "general",
            "requires_clarification": False,
        }

    def _detect_agenda_request(self, intent: Intent) -> bool:
        """
        Issue #499: Detect if the intent is asking about today's agenda or schedule.

        Returns True if agenda request detected, False otherwise.
        Recognizes patterns like:
        - "What's on the agenda for today?"
        - "What's my schedule today?"
        - "What do I have today?"
        - "Show me today's agenda"
        """
        if not intent:
            return False
        # #1460 idiom B: attribute first, dict fallback (see _detect_setup_request).
        original_message = intent.original_message or (intent.context or {}).get(
            "original_message", ""
        )
        if not original_message:
            return False

        raw_input = original_message.lower()

        # Agenda/schedule keywords combined with today reference
        agenda_patterns = [
            # Direct agenda questions
            ("agenda", "today"),
            ("schedule", "today"),
            ("on for today", None),
            ("have today", None),
            ("have on today", None),
            ("today's agenda", None),
            ("today's schedule", None),
            ("today's plan", None),
            ("planned for today", None),
            ("lined up for today", None),
            ("coming up today", None),
        ]

        for pattern, required_suffix in agenda_patterns:
            if pattern in raw_input:
                if required_suffix is None or required_suffix in raw_input:
                    return True

        return False

    async def _get_todays_todos(self, session_id: str, limit: int = 10) -> List[Dict]:
        """
        Issue #499: Fetch today's pending todos for agenda aggregation.

        Returns a list of todo dictionaries with title, priority, and due info.
        """
        try:
            from services.database.models import TodoPriority, TodoStatus
            from services.database.session_factory import AsyncSessionFactory
            from services.repositories.todo_repository import TodoRepository

            async with AsyncSessionFactory.session_scope() as session:
                todo_repo = TodoRepository(session)

                # Get pending todos ordered by priority
                todos = await todo_repo.get_todos_by_owner(
                    owner_id=session_id,
                    status=TodoStatus.PENDING,
                    limit=limit,
                )

                # #1436 (B12 family): domain.Todo carries `.text` (not `.title`)
                # and a plain-str `.priority` — the old attribute reads raised
                # AttributeError into the swallow below, so the agenda's Tasks
                # section ALWAYS reported source-failed. Dict key stays "title"
                # (the formatters' contract).
                return [
                    {
                        "title": todo.text,
                        "priority": todo.priority or "medium",
                        "due_date": todo.due_date.isoformat() if todo.due_date else None,
                        "context": todo.context,
                    }
                    for todo in todos
                ]
        except Exception as e:  # silent-ok: None sentinel -> formatters render honest "couldn't check", never "no tasks" (#1425)
            logger.warning(f"Could not fetch todos for agenda (source failed): {e}")
            return None

    def _format_agenda_embedded(
        self, calendar_context: Optional[Dict], todos: List[Dict], priorities: List[str]
    ) -> str:
        """Issue #499: Format minimal agenda for EMBEDDED spatial pattern."""
        parts = []

        # Calendar summary (brief)
        if calendar_context:
            if calendar_context.get("current_meeting"):
                parts.append(
                    f"In meeting: {calendar_context['current_meeting'].get('title', 'Meeting')}"
                )
            elif calendar_context.get("next_meeting"):
                next_time = calendar_context["next_meeting"].get("start_time", "TBD")
                parts.append(f"Next: {next_time}")

        # Todo count (None = lookup failed, never claim zero — #1425)
        if todos is None:
            parts.append("tasks unavailable")
        elif todos:
            parts.append(f"{len(todos)} tasks")

        # Top priority
        if priorities:
            parts.append(f"Focus: {priorities[0][:30]}...")

        return " | ".join(parts) if parts else "No agenda items"

    def _format_agenda_standard(
        self, calendar_context: Optional[Dict], todos: List[Dict], priorities: List[str]
    ) -> str:
        """Issue #499: Format standard agenda response."""
        message = "Here's your agenda for today:\n\n"

        # Calendar section
        if calendar_context:
            if calendar_context.get("current_meeting"):
                meeting = calendar_context["current_meeting"]
                message += f"**Now**: {meeting.get('title', 'Meeting')}\n"
            if calendar_context.get("next_meeting"):
                next_meeting = calendar_context["next_meeting"]
                message += f"**Next Meeting**: {next_meeting.get('title', 'Meeting')} at {next_meeting.get('start_time', 'TBD')}\n"
            if calendar_context.get("meeting_count"):
                message += f"**Total Meetings**: {calendar_context['meeting_count']} today\n"
            message += "\n"

        # Tasks section (None = lookup failed, never claim "no pending" — #1425)
        if todos is None:
            message += "**Tasks**: I couldn't check your tasks just now — the todo lookup failed. Try again shortly.\n"
        elif todos:
            message += "**Tasks**:\n"
            for todo in todos[:5]:
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(
                    todo["priority"], "⚪"
                )
                message += f"- {priority_icon} {todo['title']}\n"
            if len(todos) > 5:
                message += f"  ... and {len(todos) - 5} more\n"
        else:
            message += "**Tasks**: No pending tasks\n"

        # Priorities section
        if priorities:
            message += f"\n**Focus Priority**: {priorities[0]}\n"

        return message

    def _format_agenda_granular(
        self, calendar_context: Optional[Dict], todos: List[Dict], priorities: List[str]
    ) -> str:
        """Issue #499: Format detailed agenda for GRANULAR spatial pattern."""
        message = "# Today's Full Agenda\n\n"

        # Calendar section with full details
        message += "## 📅 Calendar\n"
        if calendar_context:
            if calendar_context.get("current_meeting"):
                meeting = calendar_context["current_meeting"]
                message += f"**Currently In**: {meeting.get('title', 'Meeting')}\n"
                if meeting.get("duration"):
                    message += f"  Duration: {meeting['duration']}\n"

            if calendar_context.get("next_meeting"):
                next_meeting = calendar_context["next_meeting"]
                message += f"\n**Next Up**: {next_meeting.get('title', 'Meeting')}\n"
                message += f"  Time: {next_meeting.get('start_time', 'TBD')}\n"

            if calendar_context.get("free_blocks"):
                message += "\n**Focus Time Available**:\n"
                for block in calendar_context["free_blocks"][:3]:
                    message += f"  - {block.get('duration_minutes', 0)} min at {block.get('start', 'TBD')}\n"

            if calendar_context.get("meeting_count"):
                message += f"\n**Meeting Load**: {calendar_context['meeting_count']} meetings"
                if calendar_context.get("meeting_hours"):
                    message += f" ({calendar_context['meeting_hours']:.1f} hours)"
                message += "\n"
        else:
            message += "Calendar data not available.\n"

        # Tasks section with priority grouping (None = lookup failed — #1425)
        message += "\n## ✅ Tasks\n"
        if todos is None:
            message += (
                "I couldn't check your tasks just now — the todo lookup failed. "
                "Try again shortly.\n"
            )
        elif todos:
            # Group by priority
            high = [t for t in todos if t["priority"] == "high"]
            medium = [t for t in todos if t["priority"] == "medium"]
            low = [t for t in todos if t["priority"] == "low"]

            if high:
                message += "**High Priority**:\n"
                for todo in high:
                    message += f"  - 🔴 {todo['title']}\n"

            if medium:
                message += "**Medium Priority**:\n"
                for todo in medium[:5]:
                    message += f"  - 🟡 {todo['title']}\n"
                if len(medium) > 5:
                    message += f"  ... and {len(medium) - 5} more\n"

            if low:
                message += "**Low Priority**:\n"
                for todo in low[:3]:
                    message += f"  - 🟢 {todo['title']}\n"
                if len(low) > 3:
                    message += f"  ... and {len(low) - 3} more\n"

            message += f"\n**Total**: {len(todos)} pending tasks\n"
        else:
            message += "No pending tasks - great day for deep work!\n"

        # Priorities section
        message += "\n## 🎯 Priorities\n"
        if priorities:
            for i, priority in enumerate(priorities[:3], 1):
                message += f"{i}. {priority}\n"
        else:
            message += "No priorities configured.\n"

        return message

    async def _handle_agenda_query(
        self, intent: Intent, session_id: str, user_id: Optional[str] = None
    ) -> Dict:
        """
        Issue #499: Handle "What's on the agenda today?" queries.

        Aggregates calendar, todos, and priorities into a unified agenda view.
        Uses spatial awareness patterns for response granularity.
        """
        from services.configuration.piper_config_loader import piper_config_loader

        # Get spatial pattern
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Load timezone
        standup_config = piper_config_loader.load_standup_config()
        timezone = standup_config["timing"]["timezone"]
        timezone_short = TIMEZONE_ABBREVIATIONS.get(timezone, "UTC")

        # 1. Get calendar context (reuse existing helper)
        # Issue #849: Thread user_id for user-scoped calendar auth
        calendar_context = await self._get_calendar_context(user_id=user_id)

        # 2. Get todos
        todos = await self._get_todays_todos(session_id)

        # 3. Get priorities from user context
        priorities = []
        try:
            user_context = await user_context_service.get_user_context(session_id)
            priorities = user_context.priorities if user_context else []
        except Exception as e:
            logger.warning(f"Could not get user context for agenda: {e}")

        # Format based on spatial pattern
        if spatial_pattern == "EMBEDDED":
            message = self._format_agenda_embedded(calendar_context, todos, priorities)
        elif spatial_pattern == "GRANULAR":
            message = self._format_agenda_granular(calendar_context, todos, priorities)
        else:
            message = self._format_agenda_standard(calendar_context, todos, priorities)

        # Issue #790: When calendar is not connected on an explicit agenda query,
        # surface guidance regardless of prior offer state — the user just asked.
        if not calendar_context:
            offer_text = await self._apply_calendar_offer(
                user_id=user_id, user_intent_mentions_calendar=True
            )
            if offer_text:
                message = f"{message}\n\n{offer_text}" if message else offer_text

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.TEMPORAL.value,
                "action": "provide_agenda",
                "confidence": 1.0,
                "context": {
                    "timezone": timezone_short,
                    "has_calendar": bool(calendar_context),
                    "todo_count": len(todos),
                    "has_priorities": bool(priorities),
                },
            },
            "spatial_pattern": spatial_pattern,
            "agenda_sources": {
                "calendar": bool(calendar_context),
                "todos": len(todos),
                "priorities": len(priorities),
            },
            "requires_clarification": False,
        }

    def _detect_retrospective_request(self, intent: Intent) -> bool:
        """
        Issue #501: Detect if the intent is asking about past accomplishments.

        Returns True if retrospective request detected, False otherwise.
        Patterns recognized:
        - "What did we accomplish yesterday?"
        - "What did we do yesterday?"
        - "What got done yesterday?"
        - "Yesterday's accomplishments"
        """
        if not intent:
            return False
        # #1460 idiom B: attribute first, dict fallback (see _detect_setup_request).
        original_message = intent.original_message or (intent.context or {}).get(
            "original_message", ""
        )
        if not original_message:
            return False

        raw_input = original_message.lower()

        # Retrospective patterns
        retrospective_patterns = [
            "accomplish",
            "accomplished",
            "did we do yesterday",
            "did i do yesterday",
            "got done yesterday",
            "finished yesterday",
            "completed yesterday",
            "yesterday's accomplishments",
            "yesterday's progress",
            "what happened yesterday",
        ]

        return any(pattern in raw_input for pattern in retrospective_patterns)

    async def _get_completed_todos_for_date(
        self, session_id: str, target_date: datetime, limit: int = 20
    ) -> List[Dict]:
        """
        Issue #501: Fetch todos completed on a specific date.

        Returns a list of completed todo dictionaries.
        """
        try:
            from sqlalchemy import and_, select

            from services.database.models import TodoDB, TodoStatus
            from services.database.session_factory import AsyncSessionFactory
            from services.repositories.todo_repository import TodoRepository

            # Calculate date range for target date
            start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = target_date.replace(hour=23, minute=59, second=59, microsecond=999999)

            async with AsyncSessionFactory.session_scope() as session:
                # Query todos completed on target date
                query = (
                    select(TodoDB)
                    .where(
                        and_(
                            TodoDB.owner_id == session_id,
                            TodoDB.status == TodoStatus.COMPLETED,
                            TodoDB.completed_at >= start_of_day,
                            TodoDB.completed_at <= end_of_day,
                        )
                    )
                    .order_by(TodoDB.completed_at.desc())
                    .limit(limit)
                )

                result = await session.execute(query)
                db_todos = result.scalars().all()

                return [
                    {
                        "title": todo.title,
                        "priority": todo.priority.value if todo.priority else "medium",
                        "completed_at": (
                            todo.completed_at.isoformat() if todo.completed_at else None
                        ),
                        "context": todo.context,
                    }
                    for todo in db_todos
                ]
        except Exception as e:  # silent-ok: None sentinel -> formatters render honest "couldn't check", never "no completed tasks" (#1425)
            logger.warning(f"Could not fetch completed todos for retrospective (source failed): {e}")
            return None

    def _format_retrospective_embedded(
        self, completed_todos: List[Dict], target_date: datetime
    ) -> str:
        """Issue #501: Format minimal retrospective for EMBEDDED spatial pattern."""
        date_str = target_date.strftime("%B %d")
        if completed_todos is None:  # #1425: lookup failed is not "none completed"
            return f"{date_str}: I couldn't check completed tasks just now — the lookup failed. Try again shortly."
        if completed_todos:
            return f"{date_str}: {len(completed_todos)} tasks completed"
        return f"{date_str}: No completed tasks"

    def _format_retrospective_standard(
        self, completed_todos: List[Dict], target_date: datetime
    ) -> str:
        """Issue #501: Format standard retrospective response."""
        date_str = target_date.strftime("%A, %B %d, %Y")

        if completed_todos is None:  # #1425: lookup failed is not "none completed"
            return f"**Yesterday's Accomplishments** ({date_str})\n\nI couldn't check completed tasks just now — the lookup failed. Try again shortly."
        if not completed_todos:
            return f"**Yesterday's Accomplishments** ({date_str})\n\nNo completed tasks found for yesterday. Keep up the momentum today!"

        message = f"**Yesterday's Accomplishments** ({date_str})\n\n"
        message += f"✅ **Completed Tasks** ({len(completed_todos)}):\n"

        for todo in completed_todos[:8]:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(todo["priority"], "⚪")
            message += f"  - {priority_icon} {todo['title']}\n"

        if len(completed_todos) > 8:
            message += f"  - ... and {len(completed_todos) - 8} more\n"

        message += f"\n📊 **Summary**: Productive day with {len(completed_todos)} tasks completed!"
        return message

    def _format_retrospective_granular(
        self, completed_todos: List[Dict], target_date: datetime
    ) -> str:
        """Issue #501: Format detailed retrospective for GRANULAR spatial pattern."""
        date_str = target_date.strftime("%A, %B %d, %Y")

        if completed_todos is None:  # #1425: lookup failed is not "none completed"
            return f"# Yesterday's Accomplishments\n**Date**: {date_str}\n\n📋 I couldn't check completed tasks just now — the lookup failed. Try again shortly."
        if not completed_todos:
            return f"# Yesterday's Accomplishments\n**Date**: {date_str}\n\n📋 No completed tasks found.\n\n*Consider reviewing your task list to ensure work is being tracked.*"

        message = f"# Yesterday's Accomplishments\n**Date**: {date_str}\n\n"

        # Group by priority
        high = [t for t in completed_todos if t["priority"] == "high"]
        medium = [t for t in completed_todos if t["priority"] == "medium"]
        low = [t for t in completed_todos if t["priority"] == "low"]

        if high:
            message += "## 🔴 High Priority Completed\n"
            for todo in high:
                message += f"  - {todo['title']}\n"
            message += "\n"

        if medium:
            message += "## 🟡 Medium Priority Completed\n"
            for todo in medium:
                message += f"  - {todo['title']}\n"
            message += "\n"

        if low:
            message += "## 🟢 Low Priority Completed\n"
            for todo in low:
                message += f"  - {todo['title']}\n"
            message += "\n"

        # Summary stats
        message += "---\n"
        message += f"## 📊 Summary\n"
        message += f"- **Total Completed**: {len(completed_todos)} tasks\n"
        message += f"- **High Priority**: {len(high)} tasks\n"
        message += f"- **Medium Priority**: {len(medium)} tasks\n"
        message += f"- **Low Priority**: {len(low)} tasks\n"

        return message

    async def _handle_retrospective_query(self, intent: Intent, session_id: str) -> Dict:
        """
        Issue #501: Handle "What did we accomplish yesterday?" queries.

        Returns a summary of completed todos from the previous day.
        """
        from datetime import timedelta

        # Get spatial pattern
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Calculate yesterday's date
        today = datetime.now()
        yesterday = today - timedelta(days=1)

        # Fetch completed todos from yesterday
        completed_todos = await self._get_completed_todos_for_date(session_id, yesterday)

        # Format based on spatial pattern
        if spatial_pattern == "EMBEDDED":
            message = self._format_retrospective_embedded(completed_todos, yesterday)
        elif spatial_pattern == "GRANULAR":
            message = self._format_retrospective_granular(completed_todos, yesterday)
        else:
            message = self._format_retrospective_standard(completed_todos, yesterday)

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.TEMPORAL.value,
                "action": "provide_retrospective",
                "confidence": 1.0,
                "context": {
                    "target_date": yesterday.strftime("%Y-%m-%d"),
                    "completed_count": len(completed_todos or []),
                },
            },
            "spatial_pattern": spatial_pattern,
            "retrospective": {
                "date": yesterday.strftime("%Y-%m-%d"),
                "completed_tasks": len(completed_todos or []),
            },
            "requires_clarification": False,
        }

    def _detect_last_activity_request(self, intent: Intent) -> Optional[str]:
        """
        Issue #504: Detect if this is a 'when did we last work on X' query.
        Returns project name if detected, None otherwise.
        """
        import re

        if not intent:
            return None
        # #1460 idiom B: attribute first, dict fallback (see _detect_setup_request).
        original_message = intent.original_message or (intent.context or {}).get(
            "original_message", ""
        )
        if not original_message:
            return None

        query = original_message.lower()

        # Patterns for last activity queries
        patterns = [
            r"last\s+time.*work(?:ed)?\s+on\s+(.+?)(?:\?|$)",
            r"when\s+did\s+we.*work\s+on\s+(.+?)(?:\?|$)",
            r"last\s+work(?:ed)?\s+on\s+(.+?)(?:\?|$)",
            r"when.*last.*touch(?:ed)?\s+(.+?)(?:\?|$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    async def _handle_temporal_last_activity(
        self, intent: Intent, session_id: str, project_name: str
    ) -> Dict:
        """
        Issue #504: Handle 'When did we last work on X?' queries.
        Query GitHub for last project activity.
        """
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Try to get GitHub activity for the project
        activity_data = None
        try:
            from services.integrations.github.github_integration_router import (
                GitHubIntegrationRouter,
            )

            github = GitHubIntegrationRouter()
            # Issue #891: pass user_id for token lookup
            _user_id = (intent.context or {}).get("user_id")
            await github.initialize(user_id=_user_id)

            # Get recent activity (last 30 days)
            activity = await github.get_recent_activity(days=30)

            # Find most recent activity
            all_activities = []
            for activity_type, items in activity.items():
                for item in items:
                    all_activities.append(
                        {
                            "type": activity_type,
                            "date": item.get("created_at") or item.get("updated_at"),
                            "title": item.get("title") or item.get("message", ""),
                            **item,
                        }
                    )

            if all_activities:
                # Sort by date descending
                all_activities.sort(key=lambda x: x.get("date", ""), reverse=True)
                activity_data = all_activities[0]

        except Exception as e:
            logger.warning(f"Could not get GitHub activity: {e}")

        # Format response based on spatial pattern
        if spatial_pattern == "EMBEDDED":
            message = self._format_last_activity_embedded(project_name, activity_data)
        elif spatial_pattern == "GRANULAR":
            message = self._format_last_activity_granular(project_name, activity_data)
        else:
            message = self._format_last_activity_standard(project_name, activity_data)

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.TEMPORAL.value,
                "action": "provide_last_activity",
                "confidence": 1.0,
                "context": {
                    "project_name": project_name,
                    "activity": activity_data,
                },
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    async def _handle_spatial_project_landscape(
        self, intent: Intent, session_id: str, user_context, spatial_pattern: Optional[str]
    ) -> Dict:
        """
        Issue #510: Handle 'Show me the project landscape' queries.
        Provides portfolio health view with projects grouped by health status.
        """
        projects = user_context.projects if user_context else []

        if not projects:
            return {
                "message": "You don't have any projects configured yet. "
                "Visit /settings/projects to add your project portfolio.",
                "intent": {
                    "category": IntentCategoryEnum.STATUS.value,
                    "action": "provide_landscape",
                    "confidence": 1.0,
                },
                "requires_clarification": False,
            }

        # Fetch GitHub metadata for all projects
        project_metadata = await self._get_project_metadata(projects)

        # Calculate health for each project
        health_groups = {"healthy": [], "at-risk": [], "stalled": [], "unknown": []}

        for project in projects:
            github_data = project_metadata.get(project, {})
            health = self._calculate_project_health(project, github_data)
            status = health["status"]
            health_groups[status].append(
                {"name": project, "reason": health["reason"], "github_data": github_data}
            )

        # Format response based on spatial pattern
        if spatial_pattern == "EMBEDDED":
            message = self._format_landscape_embedded(health_groups)
        elif spatial_pattern == "GRANULAR":
            message = self._format_landscape_granular(health_groups)
        else:
            message = self._format_landscape_standard(health_groups)

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.STATUS.value,
                "action": "provide_landscape",
                "confidence": 1.0,
                "context": {
                    "health_summary": {
                        "healthy": len(health_groups["healthy"]),
                        "at-risk": len(health_groups["at-risk"]),
                        "stalled": len(health_groups["stalled"]),
                        "unknown": len(health_groups["unknown"]),
                    }
                },
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    async def _handle_status_report(
        self, intent: Intent, session_id: str, user_context, spatial_pattern: Optional[str]
    ) -> Dict:
        """
        Issue #513: Handle 'Give me a status report' queries.
        Provides aggregated status including projects and todos.
        """
        projects = user_context.projects if user_context else []

        # Fetch GitHub metadata for all projects
        project_metadata = await self._get_project_metadata(projects)

        # Calculate health for each project
        health_summary = {"healthy": 0, "at-risk": 0, "stalled": 0, "unknown": 0}

        for project in projects:
            github_data = project_metadata.get(project, {})
            health = self._calculate_project_health(project, github_data)
            status = health["status"]
            health_summary[status] += 1

        # Try to get open todos count
        open_todos_count = 0
        try:
            from services.database.models import TodoStatus
            from services.database.session_factory import AsyncSessionFactory
            from services.repositories.todo_repository import TodoRepository

            async with AsyncSessionFactory.session_scope() as session:
                todo_repo = TodoRepository(session)

                # Get user_id from user_context
                user_id = user_context.user_id if hasattr(user_context, "user_id") else None

                if user_id:
                    # Get all pending todos for the user
                    from sqlalchemy import select

                    from services.database.models import TodoDB

                    result = await session.execute(
                        select(TodoDB).where(
                            TodoDB.owner_id == user_id, TodoDB.status == TodoStatus.PENDING
                        )
                    )
                    todos = result.scalars().all()
                    open_todos_count = len(todos)
        except Exception as e:  # silent-ok: None sentinel -> formatters render honest "couldn't check", never "0 todos" (#1425)
            logger.warning(f"Could not fetch todos count (source failed): {e}")
            open_todos_count = None

        # Build report data
        report_data = {
            "total_projects": len(projects),
            "health_summary": health_summary,
            "open_todos": open_todos_count,
        }

        # Format response based on spatial pattern
        if spatial_pattern == "EMBEDDED":
            message = self._format_status_report_embedded(report_data)
        elif spatial_pattern == "GRANULAR":
            message = self._format_status_report_granular(report_data)
        else:
            message = self._format_status_report_standard(report_data)

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.STATUS.value,
                "action": "provide_status_report",
                "confidence": 1.0,
                "context": report_data,
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    async def _handle_spatial_priority_recommendation(
        self, intent: Intent, session_id: str, user_context, spatial_pattern: Optional[str]
    ) -> Dict:
        """
        Issue #511: Handle 'Which project should I focus on?' queries.
        Provides intelligent priority recommendation based on project health and activity.
        """
        projects = user_context.projects if user_context else []

        if not projects:
            return {
                "message": "You don't have any projects configured yet. "
                "Visit /settings/projects to add your project portfolio.",
                "intent": {
                    "category": IntentCategoryEnum.PRIORITY.value,
                    "action": "provide_priority_recommendation",
                    "confidence": 1.0,
                },
                "requires_clarification": False,
            }

        # Fetch GitHub metadata for all projects
        project_metadata = await self._get_project_metadata(projects)

        # Calculate priority score for each project
        ranked_projects = []
        for project in projects:
            github_data = project_metadata.get(project, {})
            priority_score = self._calculate_priority_score(project, github_data)
            ranked_projects.append(
                {
                    "name": project,
                    "score": priority_score["score"],
                    "top_reason": priority_score["top_reason"],
                    "breakdown": priority_score["breakdown"],
                    "github_data": github_data,
                }
            )

        # Sort by priority score (highest first)
        ranked_projects.sort(key=lambda x: x["score"], reverse=True)

        # Format response based on spatial pattern
        if spatial_pattern == "EMBEDDED":
            message = self._format_priority_embedded(ranked_projects)
        elif spatial_pattern == "GRANULAR":
            message = self._format_priority_granular(ranked_projects)
        else:
            message = self._format_priority_standard(ranked_projects)

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.PRIORITY.value,
                "action": "provide_priority_recommendation",
                "confidence": 1.0,
                "context": {
                    "top_recommendation": ranked_projects[0]["name"] if ranked_projects else None,
                    "ranked_projects": [
                        {"name": p["name"], "score": p["score"]} for p in ranked_projects
                    ],
                },
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    def _calculate_priority_score(
        self, project: str, github_data: Optional[Dict], calendar_context: Optional[Dict] = None
    ) -> Dict:
        """
        Issue #511: Calculate priority score (0-100) for a project.

        Scoring criteria:
        - Staleness (0-40 points): Longer gap since last activity = higher priority
        - Issue count (0-30 points): More open issues = higher priority
        - Urgency (0-30 points): High-priority/critical labels = higher priority

        Returns:
        - score: int (0-100)
        - top_reason: str (main reason for this score)
        - breakdown: dict (detailed scoring)
        """
        from datetime import datetime

        score = 0
        breakdown = {"staleness": 0, "issue_count": 0, "urgency": 0}
        reasons = []

        if not github_data:
            return {
                "score": 0,
                "top_reason": "No GitHub data available",
                "breakdown": breakdown,
            }

        # Staleness factor (0-40 points)
        last_activity = github_data.get("updated_at")
        if last_activity:
            try:
                dt = datetime.fromisoformat(last_activity.replace("Z", "+00:00"))
                days_since_activity = (datetime.now(dt.tzinfo) - dt).days

                if days_since_activity > 14:
                    staleness_score = min(40, days_since_activity)
                    breakdown["staleness"] = staleness_score
                    score += staleness_score
                    reasons.append(f"{days_since_activity} days since last activity")
            except Exception:
                pass

        # Issue count factor (0-30 points)
        open_issues = github_data.get("open_issues_count", 0)
        if open_issues > 0:
            issue_score = min(30, open_issues * 3)
            breakdown["issue_count"] = issue_score
            score += issue_score
            reasons.append(f"{open_issues} open issues")

        # Urgency factor (0-30 points) - Check for high-priority issues
        # This would require labels data from issues_preview
        issues_preview = github_data.get("issues_preview", [])
        high_priority_count = 0
        for issue in issues_preview:
            labels = issue.get("labels", [])
            if any(
                label.get("name", "").lower() in ["high-priority", "critical", "urgent"]
                for label in labels
            ):
                high_priority_count += 1

        if high_priority_count > 0:
            urgency_score = min(30, high_priority_count * 10)
            breakdown["urgency"] = urgency_score
            score += urgency_score
            reasons.append(f"{high_priority_count} high-priority issues")

        # Determine top reason
        if not reasons:
            top_reason = "Active and low issue count"
        else:
            top_reason = reasons[0]

        return {"score": score, "top_reason": top_reason, "breakdown": breakdown}

    def _format_priority_embedded(self, ranked_projects: List[Dict]) -> str:
        """Issue #511: Brief format for embedded contexts."""
        if not ranked_projects:
            return "No projects to prioritize"

        top_project = ranked_projects[0]
        return f"Focus on: {top_project['name']}"

    def _format_priority_standard(self, ranked_projects: List[Dict]) -> str:
        """Issue #511: Standard format with top 3 priorities."""
        if not ranked_projects:
            return "No projects to prioritize"

        lines = ["## Priority Recommendation\n"]

        # Show top 3
        for i, proj in enumerate(ranked_projects[:3], 1):
            lines.append(f"{i}. **{proj['name']}** (Score: {proj['score']})")
            lines.append(f"   - {proj['top_reason']}")
            lines.append("")

        if len(ranked_projects) > 3:
            lines.append(f"_Plus {len(ranked_projects) - 3} more projects_")

        return "\n".join(lines)

    def _format_priority_granular(self, ranked_projects: List[Dict]) -> str:
        """Issue #511: Detailed format with full priority analysis."""
        if not ranked_projects:
            return "No projects to prioritize"

        lines = ["## Full Priority Analysis\n"]
        lines.append(f"**Total Projects Analyzed**: {len(ranked_projects)}\n")

        for i, proj in enumerate(ranked_projects, 1):
            lines.append(f"### {i}. {proj['name']}")
            lines.append(f"**Priority Score**: {proj['score']}/100")
            lines.append(f"**Top Reason**: {proj['top_reason']}")
            lines.append("\n**Score Breakdown**:")
            breakdown = proj["breakdown"]
            lines.append(f"  - Staleness: {breakdown['staleness']}/40 points")
            lines.append(f"  - Issue Count: {breakdown['issue_count']}/30 points")
            lines.append(f"  - Urgency: {breakdown['urgency']}/30 points")

            github_data = proj.get("github_data", {})
            if github_data:
                lines.append(f"\n**GitHub Data**:")
                lines.append(f"  - Open Issues: {github_data.get('open_issues_count', 0)}")
                last_update = github_data.get("updated_at", "Unknown")
                lines.append(f"  - Last Updated: {last_update}")

            lines.append("")

        return "\n".join(lines)

    def _format_last_activity_embedded(self, project_name: str, activity: Optional[Dict]) -> str:
        """Issue #504: Brief format for embedded contexts."""
        if not activity:
            return f"{project_name}: no recent activity"

        from datetime import datetime

        activity_date = activity.get("date", "")
        if activity_date:
            try:
                dt = datetime.fromisoformat(activity_date.replace("Z", "+00:00"))
                days_ago = (datetime.now(dt.tzinfo) - dt).days
                if days_ago == 0:
                    return f"{project_name}: today"
                elif days_ago == 1:
                    return f"{project_name}: yesterday"
                else:
                    return f"{project_name}: {days_ago} days ago"
            except Exception:
                pass
        return f"{project_name}: recently"

    def _format_last_activity_standard(self, project_name: str, activity: Optional[Dict]) -> str:
        """Issue #504: Standard format with context."""
        if not activity:
            return f"I don't have recent activity data for {project_name}. The GitHub integration may need to be configured."

        from datetime import datetime

        activity_type = activity.get("type", "activity")
        title = activity.get("title", "")[:50]
        activity_date = activity.get("date", "")

        date_str = "recently"
        if activity_date:
            try:
                dt = datetime.fromisoformat(activity_date.replace("Z", "+00:00"))
                date_str = dt.strftime("%B %d, %Y")
            except Exception:
                pass

        return f'Last activity on **{project_name}**: {activity_type} on {date_str}\n\n"{title}"'

    def _format_last_activity_granular(self, project_name: str, activity: Optional[Dict]) -> str:
        """Issue #504: Detailed format with full activity breakdown."""
        if not activity:
            return f"No recent activity found for **{project_name}**.\n\nThis could mean:\n- No commits, issues, or PRs in the last 30 days\n- GitHub integration not configured for this project"

        from datetime import datetime

        result = f"**Last Activity on {project_name}**\n\n"

        activity_type = activity.get("type", "activity")
        title = activity.get("title", "")
        activity_date = activity.get("date", "")

        if activity_date:
            try:
                dt = datetime.fromisoformat(activity_date.replace("Z", "+00:00"))
                result += f"**Date**: {dt.strftime('%A, %B %d, %Y at %I:%M %p')}\n"
                days_ago = (datetime.now(dt.tzinfo) - dt).days
                result += f"**Time Since**: {days_ago} days ago\n"
            except Exception:
                result += f"**Date**: {activity_date}\n"

        result += f"**Type**: {activity_type}\n"
        if title:
            result += f"**Description**: {title}\n"

        return result

    def _format_landscape_embedded(self, health_groups: Dict[str, list]) -> str:
        """Issue #510: Brief format for embedded contexts."""
        healthy = len(health_groups["healthy"])
        at_risk = len(health_groups["at-risk"])
        stalled = len(health_groups["stalled"])

        parts = []
        if healthy > 0:
            parts.append(f"{healthy} healthy")
        if at_risk > 0:
            parts.append(f"{at_risk} at-risk")
        if stalled > 0:
            parts.append(f"{stalled} stalled")

        if not parts:
            return "Portfolio: No projects configured"

        return f"Portfolio: {', '.join(parts)}"

    def _format_landscape_standard(self, health_groups: Dict[str, list]) -> str:
        """Issue #510: Standard format with project lists."""
        lines = ["## Portfolio Health Overview\n"]

        total = sum(len(group) for group in health_groups.values())
        lines.append(f"**Total Projects**: {total}\n")

        # Healthy projects
        if health_groups["healthy"]:
            lines.append(f"✅ **Healthy** ({len(health_groups['healthy'])}):")
            for proj in health_groups["healthy"]:
                lines.append(f"  - {proj['name']}")
            lines.append("")

        # At-risk projects
        if health_groups["at-risk"]:
            lines.append(f"⚠️ **At Risk** ({len(health_groups['at-risk'])}):")
            for proj in health_groups["at-risk"]:
                lines.append(f"  - {proj['name']} ({proj['reason']})")
            lines.append("")

        # Stalled projects
        if health_groups["stalled"]:
            lines.append(f"🛑 **Stalled** ({len(health_groups['stalled'])}):")
            for proj in health_groups["stalled"]:
                lines.append(f"  - {proj['name']} ({proj['reason']})")
            lines.append("")

        # Unknown status
        if health_groups["unknown"]:
            lines.append(f"❓ **Unknown** ({len(health_groups['unknown'])}):")
            for proj in health_groups["unknown"]:
                lines.append(f"  - {proj['name']} (No GitHub data)")
            lines.append("")

        return "\n".join(lines)

    def _format_landscape_granular(self, health_groups: Dict[str, list]) -> str:
        """Issue #510: Detailed format with full health analysis."""
        lines = ["## Project Portfolio - Full Health Analysis\n"]

        total = sum(len(group) for group in health_groups.values())
        lines.append(f"**Total Projects**: {total}")
        lines.append(
            f"**Health Summary**: "
            f"{len(health_groups['healthy'])} healthy, "
            f"{len(health_groups['at-risk'])} at-risk, "
            f"{len(health_groups['stalled'])} stalled"
        )
        lines.append("")

        # Detailed breakdown by health status
        for status_name, emoji in [
            ("healthy", "✅"),
            ("at-risk", "⚠️"),
            ("stalled", "🛑"),
            ("unknown", "❓"),
        ]:
            projects = health_groups[status_name]
            if not projects:
                continue

            lines.append(f"### {emoji} {status_name.replace('-', ' ').title()} Projects\n")

            for proj in projects:
                lines.append(f"**{proj['name']}**")
                lines.append(f"  - Status: {status_name}")
                lines.append(f"  - Reason: {proj['reason']}")

                github_data = proj.get("github_data", {})
                if github_data:
                    open_issues = github_data.get("open_issues_count", 0)
                    lines.append(f"  - Open Issues: {open_issues}")
                    last_update = github_data.get("updated_at", "Unknown")
                    lines.append(f"  - Last Updated: {last_update}")

                lines.append("")

        return "\n".join(lines)

    def _format_status_report_embedded(self, report_data: Dict) -> str:
        """Issue #513: Brief format for embedded contexts."""
        total = report_data["total_projects"]
        health = report_data["health_summary"]
        todos = report_data["open_todos"]

        parts = []
        if total > 0:
            healthy = health["healthy"]
            at_risk = health["at-risk"]
            if healthy > 0:
                parts.append(f"{healthy} healthy")
            if at_risk > 0:
                parts.append(f"{at_risk} at-risk")

        if todos is None:  # #1425: count lookup failed, never claim zero
            parts.append("todos unavailable")
        elif todos > 0:
            parts.append(f"{todos} open todos")

        if not parts:
            return "Status: No projects or todos"

        return f"Status: {', '.join(parts)}"

    def _format_status_report_standard(self, report_data: Dict) -> str:
        """Issue #513: Standard format with project and todo summary."""
        lines = ["## Status Report\n"]

        total = report_data["total_projects"]
        health = report_data["health_summary"]
        todos = report_data["open_todos"]

        # Project summary
        lines.append(f"**Projects**: {total} total")
        if total > 0:
            lines.append(f"  - ✅ Healthy: {health['healthy']}")
            if health["at-risk"] > 0:
                lines.append(f"  - ⚠️ At Risk: {health['at-risk']}")
            if health["stalled"] > 0:
                lines.append(f"  - 🛑 Stalled: {health['stalled']}")
        lines.append("")

        # Todo summary (#1425: None = lookup failed)
        lines.append(
            "**Open Todos**: couldn't check just now"
            if todos is None
            else f"**Open Todos**: {todos}"
        )
        lines.append("")

        return "\n".join(lines)

    def _format_status_report_granular(self, report_data: Dict) -> str:
        """Issue #513: Detailed format with full breakdown."""
        lines = ["## Detailed Status Report\n"]

        total = report_data["total_projects"]
        health = report_data["health_summary"]
        todos = report_data["open_todos"]

        # Overview section
        lines.append("### Overview\n")
        lines.append(f"**Total Projects**: {total}")
        lines.append(
            "**Open Todos**: couldn't check just now"
            if todos is None
            else f"**Open Todos**: {todos}"
        )
        lines.append("")

        # Project health breakdown
        if total > 0:
            lines.append("### Project Health Breakdown\n")
            lines.append(f"✅ **Healthy**: {health['healthy']} projects")
            lines.append(f"⚠️ **At Risk**: {health['at-risk']} projects")
            lines.append(f"🛑 **Stalled**: {health['stalled']} projects")
            if health["unknown"] > 0:
                lines.append(f"❓ **Unknown**: {health['unknown']} projects")
            lines.append("")

        # Summary
        lines.append("### Summary\n")
        if health["healthy"] == total and total > 0:
            lines.append("All projects are healthy!")
        elif health["stalled"] > 0:
            lines.append(f"⚠️ Attention needed: {health['stalled']} stalled project(s)")
        elif health["at-risk"] > 0:
            lines.append(f"⚠️ Watch: {health['at-risk']} project(s) at risk")
        lines.append("")

        return "\n".join(lines)

    def _detect_priority_recommendation_request(self, intent: Intent) -> bool:
        """
        Issue #511: Detect if this is a priority recommendation request.
        Returns True if priority recommendation pattern detected.

        Patterns recognized:
        - "which project should I focus on"
        - "what project should I work on"
        - "what should I prioritize"
        - "what's most important"
        - "what should I focus on"
        """
        import re

        if not intent:
            return False
        # #1460 idiom B: attribute first, dict fallback (see _detect_setup_request).
        # 6th site per the #1460 audit — not currently live-broken (its only
        # callers set the attribute) but one wiring change from live.
        original_message = intent.original_message or (intent.context or {}).get(
            "original_message", ""
        )
        if not original_message:
            return False

        query = original_message.lower()

        # Patterns for priority recommendation
        patterns = [
            r"which\s+project.*(?:focus|work|prioritize)",
            r"what\s+project.*(?:focus|work|prioritize)",
            r"what.*should.*(?:focus|prioritize)",
            r"what.*most\s+important",
            r"where.*should.*(?:focus|attention)",
        ]

        for pattern in patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True

        return False

    def _detect_duration_request(self, intent: Intent) -> Optional[str]:
        """
        Detect if this is a 'how long have we been working on X' query.
        Returns project name if detected, None otherwise.
        Issue #505: Project duration temporal query.
        """
        import re

        if not intent:
            return None
        # #1460 idiom B: attribute first, dict fallback (see _detect_setup_request).
        original_message = intent.original_message or (intent.context or {}).get(
            "original_message", ""
        )
        if not original_message:
            return None

        query = original_message.lower()

        # Patterns for duration queries
        patterns = [
            r"how\s+long.*work(?:ing|ed)?\s+on\s+(.+?)(?:\?|$)",
            r"how\s+long.*been\s+on\s+(.+?)(?:\?|$)",
            r"(?:project|how\s+old\s+is)\s+(.+?)\s+duration",
            r"when\s+did\s+(?:we\s+)?start\s+(.+?)(?:\?|$)",
            r"how\s+long.*this\s+project",  # Generic "this project"
        ]

        for pattern in patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                project_name = match.group(1).strip() if match.lastindex else "this project"
                return project_name

        return None

    async def _handle_temporal_project_duration(
        self, intent: Intent, session_id: str, project_name: str, user_id: Optional[str] = None
    ) -> Dict:
        """
        Handle 'How long have we been working on X?' queries.
        Issue #505: Calculate project duration from created_at.

        Bug fix (found during ADR-075 Component B, #1366): this previously
        called `piper_config_loader.get_user_context()`, a method that has
        never existed on that class (would raise AttributeError any time this
        handler was actually reached). Repointed to the already-correct,
        already-user-scoped `user_context_service.get_user_context()` used by
        every other user-context call site in this file.
        """
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Try to find project in user_context
        try:
            user_context = await user_context_service.get_user_context(session_id, user_id)
        except Exception as e:
            logger.error(f"Failed to load user context for duration query: {e}")
            user_context = None

        project_data = None
        created_at = None

        # Search for matching project
        if user_context and user_context.projects:
            project_name_lower = project_name.lower()
            for project in user_context.projects:
                if project_name_lower in project.get("name", "").lower():
                    project_data = project
                    created_at = project.get("created_at")
                    break

        # Calculate duration if we have a date
        duration_data = None
        if created_at:
            duration_data = self._calculate_duration(created_at)

        # Format response based on spatial pattern
        if spatial_pattern == "EMBEDDED":
            message = self._format_duration_embedded(project_name, duration_data)
        elif spatial_pattern == "GRANULAR":
            message = self._format_duration_granular(project_name, duration_data, created_at)
        else:
            message = self._format_duration_standard(project_name, duration_data, created_at)

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.TEMPORAL.value,
                "action": "provide_project_duration",
                "confidence": 1.0,
                "context": {
                    "project_name": project_name,
                    "duration": duration_data,
                    "created_at": created_at,
                },
            },
            "spatial_pattern": spatial_pattern,
            "requires_clarification": False,
        }

    def _calculate_duration(self, created_at: str) -> Optional[Dict]:
        """Calculate human-readable duration from a date string."""
        from datetime import datetime

        try:
            if isinstance(created_at, str):
                # Handle ISO format
                dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            else:
                dt = created_at

            now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
            delta = now - dt

            total_days = delta.days
            months = total_days // 30
            remaining_days = total_days % 30
            weeks = remaining_days // 7
            days = remaining_days % 7

            return {
                "total_days": total_days,
                "months": months,
                "weeks": weeks,
                "days": days,
                "start_date": dt,
            }
        except Exception as e:
            logger.warning(f"Could not calculate duration: {e}")
            return None

    def _format_duration_embedded(self, project_name: str, duration: Optional[Dict]) -> str:
        """Brief format for embedded contexts."""
        if not duration:
            return f"{project_name}: unknown duration"

        months = duration.get("months", 0)
        if months > 0:
            return f"{project_name}: {months} month{'s' if months != 1 else ''}"

        total_days = duration.get("total_days", 0)
        if total_days > 0:
            return f"{project_name}: {total_days} day{'s' if total_days != 1 else ''}"

        return f"{project_name}: just started"

    def _format_duration_standard(
        self, project_name: str, duration: Optional[Dict], created_at: str
    ) -> str:
        """Standard format with context."""
        if not duration:
            return f"I don't have start date information for **{project_name}**. Check if the project is configured in your settings."

        # Build human-readable duration
        parts = []
        months = duration.get("months", 0)
        weeks = duration.get("weeks", 0)
        days = duration.get("days", 0)

        if months > 0:
            parts.append(f"{months} month{'s' if months != 1 else ''}")
        if weeks > 0:
            parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
        if days > 0:
            parts.append(f"{days} day{'s' if days != 1 else ''}")

        duration_str = " and ".join(parts) if parts else "just started"

        # Format start date
        start_date = duration.get("start_date")
        date_str = ""
        if start_date:
            date_str = f" (started {start_date.strftime('%B %d, %Y')})"

        return f"You've been working on **{project_name}** for {duration_str}{date_str}."

    def _format_duration_granular(
        self, project_name: str, duration: Optional[Dict], created_at: str
    ) -> str:
        """Detailed format with full timeline."""
        if not duration:
            return f"**{project_name}** duration unknown.\n\nThe project may not be configured with a start date. Check Settings → Projects to add project details."

        result = f"**Project Duration: {project_name}**\n\n"

        start_date = duration.get("start_date")
        if start_date:
            result += f"**Started**: {start_date.strftime('%A, %B %d, %Y')}\n"

        total_days = duration.get("total_days", 0)
        result += f"**Total Days**: {total_days}\n"

        # Detailed breakdown
        months = duration.get("months", 0)
        weeks = duration.get("weeks", 0)
        days = duration.get("days", 0)

        result += "\n**Breakdown**:\n"
        result += f"- Months: {months}\n"
        result += f"- Weeks: {weeks}\n"
        result += f"- Days: {days}\n"

        return result

    async def _handle_guidance_query(
        self, intent: Intent, session_id: str, user_id: str = None
    ) -> Dict:
        """
        Handle 'What should I focus on?' queries with spatial awareness.

        GREAT-4C Phase 1: Adds spatial intelligence for guidance granularity.
        GREAT-4C Phase 2: Adds error handling with fallback guidance.
        Issue #495: Adds calendar context for meeting-aware guidance.
        Issue #497: Synthesizes calendar + projects + priorities for personalized focus.
        Issue #498: Detects and routes setup requests to appropriate guidance.
        Issue #582: Added user_id parameter to enable database project lookup.
        """
        # Issue #498: Check if this is a setup request first
        setup_topic = self._detect_setup_request(intent)
        if setup_topic:
            # Route to appropriate setup guidance
            if setup_topic == "projects":
                # Issue #814: Route to interactive onboarding or state-aware response
                return await self._handle_project_setup_request(intent, session_id, user_id)
            elif setup_topic == "integrations":
                return self._format_integration_setup_guidance()
            else:  # general
                return self._format_general_setup_guidance()

        current_time = datetime.now()
        current_hour = current_time.hour

        # Try to get user-specific context with fallback to generic guidance
        # Issue #582: Pass user_id to enable loading projects from database
        user_context = None
        try:
            user_context = await user_context_service.get_user_context(session_id, user_id)
        except Exception as e:
            logger.warning(f"Using generic guidance, user context unavailable: {e}")

        # Issue #495: Try to get calendar context for meeting-aware guidance
        # Issue #849: Thread user_id for user-scoped calendar auth
        calendar_context = await self._get_calendar_context(user_id=user_id)

        # Issue #497: Gather project and priority metadata for rich context
        projects = user_context.projects if user_context else []
        project_metadata = await self._get_project_metadata(projects) if projects else {}
        priority_metadata = await self._get_priority_metadata(user_id=user_id)

        # Issue #497: Synthesize focus recommendation from all context
        focus_recommendation = self._synthesize_focus_recommendation(
            current_hour, user_context, calendar_context, project_metadata, priority_metadata
        )

        # Get spatial pattern (GREAT-4C Phase 1: Spatial intelligence)
        spatial_pattern = None
        if hasattr(intent, "spatial_context") and intent.spatial_context:
            spatial_pattern = intent.spatial_context.get("pattern")

        # Adjust response detail based on spatial pattern
        # Issue #497: Pass focus_recommendation to format methods
        if spatial_pattern == "GRANULAR":
            message = self._format_detailed_guidance(
                current_hour,
                user_context,
                calendar_context,
                project_metadata,
                priority_metadata,
                focus_recommendation,
            )
        elif spatial_pattern == "EMBEDDED":
            message = self._format_consolidated_guidance(
                current_hour, user_context, calendar_context, focus_recommendation
            )
        else:
            message = self._format_standard_guidance(
                current_hour,
                user_context,
                calendar_context,
                priority_metadata,
                focus_recommendation,
            )

        # Load timezone from configuration (same for all users)
        from services.configuration.piper_config_loader import piper_config_loader

        standup_config = piper_config_loader.load_standup_config()
        timezone = standup_config["timing"]["timezone"]
        # Issue #287: Use timezone abbreviation instead of city name
        timezone_short = TIMEZONE_ABBREVIATIONS.get(timezone, "UTC")

        # Extract guidance context components for API response
        focus = self._get_immediate_focus(current_hour, user_context)
        priority_text = (
            user_context.priorities[0]
            if user_context and user_context.priorities
            else "your key priorities"
        )
        org_text = (
            user_context.organization
            if user_context and user_context.organization
            else "your projects"
        )

        guidance_context = {
            "immediate_focus": focus,
            "daily_goal": priority_text,
            "weekly_focus": f"Continue work on {org_text}",
            "strategic_direction": "Deliver on your priorities while maintaining progress across all projects",
            "time_context": f"{current_hour}:00 {timezone_short}",
            "focus_recommendation": focus_recommendation,  # Issue #497
        }

        # Issue #495: Add calendar context if available
        if calendar_context:
            guidance_context["calendar"] = calendar_context

        # Issue #497: Add project and priority metadata
        if project_metadata:
            guidance_context["project_metadata"] = project_metadata
        if priority_metadata:
            guidance_context["priority_metadata"] = priority_metadata

        return {
            "message": message,
            "intent": {
                "category": IntentCategoryEnum.GUIDANCE.value,
                "action": "provide_contextual_guidance",
                "confidence": 1.0,
                "context": guidance_context,
            },
            "spatial_pattern": spatial_pattern,
            "personalized": bool(user_context),
            "fallback_guidance": not user_context,
            "calendar_aware": bool(calendar_context),  # Issue #495
            "context_level": focus_recommendation.get("context_level", "minimal"),  # Issue #497
            "requires_clarification": False,
        }

    async def _handle_portfolio_query(
        self, intent: Intent, session_id: str, user_id: str = None
    ) -> Dict:
        """
        Handle PORTFOLIO category intents - project management operations.

        Issue #675: MUX-WIRE-PORTFOLIO - Wire PortfolioService to chat interface.

        Routes to PortfolioService from services.onboarding for:
        - "Archive my project X" → PortfolioService.archive_project()
        - "Delete my project X" → PortfolioService.delete_project()
        - "Restore project X" → PortfolioService.restore_project()
        - "Search projects for Y" → PortfolioService.search_projects()
        - "Show my projects" → PortfolioService.list_active_projects()
        """
        # Delegate repo management to dedicated handler (Issue #862)
        if intent.action == "manage_repos":
            return await self._handle_repo_management(intent, session_id, user_id)

        import re

        from services.database.repositories import ProjectRepository
        from services.database.session_factory import AsyncSessionFactory
        from services.onboarding.portfolio_service import (
            ARCHIVE_PATTERNS,
            DELETE_PATTERNS,
            RESTORE_PATTERNS,
            PortfolioService,
        )

        try:
            # Get original message for pattern matching
            original_message = intent.context.get("original_message", "")
            message_lower = original_message.lower().strip()

            # Helper to strip common trailing words from project names
            # Fixes issue where "delete X please" captures "X please"
            def clean_project_name(name: str) -> str:
                if not name:
                    return name
                trailing_words = [
                    "please",
                    "now",
                    "thanks",
                    "thank you",
                    "asap",
                    "for me",
                    "right now",
                    "immediately",
                    "today",
                ]
                cleaned = name.strip()
                for word in trailing_words:
                    if cleaned.lower().endswith(f" {word}"):
                        cleaned = cleaned[: -(len(word) + 1)].strip()
                return cleaned

            # Determine operation type by matching against patterns
            # (This doesn't require DB access)
            operation = None
            project_name = None

            # Check archive patterns
            for pattern in ARCHIVE_PATTERNS:
                match = re.search(pattern, message_lower, re.IGNORECASE)
                if match:
                    operation = "archive"
                    project_name = (
                        clean_project_name(match.group(1).strip()) if match.groups() else None
                    )
                    break

            # Check delete patterns
            if not operation:
                for pattern in DELETE_PATTERNS:
                    match = re.search(pattern, message_lower, re.IGNORECASE)
                    if match:
                        operation = "delete"
                        project_name = (
                            clean_project_name(match.group(1).strip()) if match.groups() else None
                        )
                        break

            # Check restore patterns
            if not operation:
                for pattern in RESTORE_PATTERNS:
                    match = re.search(pattern, message_lower, re.IGNORECASE)
                    if match:
                        operation = "restore"
                        project_name = (
                            clean_project_name(match.group(1).strip()) if match.groups() else None
                        )
                        break

            # Check for list/show operations
            if not operation:
                if any(word in message_lower for word in ["show", "list", "view", "my projects"]):
                    operation = "list"

            # Check for add/create operations
            if not operation:
                if any(word in message_lower for word in ["add", "create", "new project"]):
                    operation = "add"

            # Check for search operations
            if not operation:
                if any(word in message_lower for word in ["search", "find project"]):
                    operation = "search"

            # Handle no user_id (doesn't need DB)
            if not user_id:
                return {
                    "message": (
                        "I can help you manage your projects once you're signed in. "
                        "You'll be able to add, archive, restore, and organize projects."
                    ),
                    "intent": {
                        "category": IntentCategoryEnum.PORTFOLIO.value,
                        "action": "portfolio_no_user",
                        "confidence": 0.8,
                        "context": {"original_message": original_message},
                    },
                    "requires_clarification": False,
                }

            # Handle add operation - create onboarding session for multi-turn flow
            # Issue #490, P5+P7: Wire to PortfolioOnboardingManager for conversation state
            if operation == "add":
                if user_id:
                    # Import onboarding components (lazy to avoid circular imports)
                    # Get or create singleton manager (same pattern as conversation_handler)
                    # We need to use the SAME singleton as conversation_handler
                    from services.conversation.conversation_handler import (
                        _get_onboarding_components,
                    )
                    from services.onboarding import (
                        PortfolioOnboardingHandler,
                        PortfolioOnboardingManager,
                    )
                    from services.shared_types import PortfolioOnboardingState

                    onboarding_manager, _ = _get_onboarding_components()

                    # Create session directly in GATHERING_PROJECTS state
                    # (user already asked to add, so skip INITIATED)
                    onboarding_session = onboarding_manager.create_session(
                        session_id=session_id,
                        user_id=user_id,
                    )

                    # Transition to GATHERING_PROJECTS since user initiated the add
                    onboarding_manager.transition_state(
                        onboarding_session.id,
                        PortfolioOnboardingState.GATHERING_PROJECTS,
                    )

                    # Record the turn
                    prompt_message = (
                        "I'd be happy to help you add a new project! "
                        "What would you like to call it?"
                    )
                    onboarding_manager.add_turn(
                        onboarding_session.id,
                        user_message=original_message,
                        assistant_response=prompt_message,
                    )

                    logger.info(
                        "portfolio_add_onboarding_started",
                        user_id=user_id,
                        session_id=session_id,
                        onboarding_id=onboarding_session.id,
                    )

                    return {
                        "message": prompt_message,
                        "intent": {
                            "category": IntentCategoryEnum.PORTFOLIO.value,
                            "action": "add_project_onboarding",
                            "confidence": 1.0,
                            "context": {"onboarding_id": onboarding_session.id},
                        },
                        "requires_clarification": False,  # Onboarding handles the flow
                    }
                else:
                    # No user_id - can't create session, fall back to prompt
                    return {
                        "message": (
                            "I'd be happy to help you add a new project! "
                            "Please sign in first so I can save it to your portfolio."
                        ),
                        "intent": {
                            "category": IntentCategoryEnum.PORTFOLIO.value,
                            "action": "add_project_no_user",
                            "confidence": 1.0,
                            "context": {},
                        },
                        "requires_clarification": False,
                    }

            # All remaining operations need DB access - wrap in session scope
            async with AsyncSessionFactory.session_scope() as session:
                project_repo = ProjectRepository(session)
                portfolio_service = PortfolioService(project_repo)

                # Handle list operation
                if operation == "list":
                    projects = await portfolio_service.list_active_projects(user_id=user_id)
                    if projects:
                        project_names = [p.name for p in projects[:5]]
                        response = f"You have {len(projects)} active projects:\n\n" + "\n".join(
                            f"- {name}" for name in project_names
                        )
                        if len(projects) > 5:
                            response += f"\n\n...and {len(projects) - 5} more."
                    else:
                        response = (
                            "You don't have any active projects yet. " "Would you like to add one?"
                        )
                    result_dict = {
                        "message": response,
                        "intent": {
                            "category": IntentCategoryEnum.PORTFOLIO.value,
                            "action": "list_projects",
                            "confidence": 1.0,
                            "context": {"project_count": len(projects)},
                        },
                        "requires_clarification": False,
                    }
                    # Issue #852: Track contextual offer when no projects exist
                    if not projects:
                        result_dict["offer_hint"] = {
                            "continuation_hint": "add a new project",
                            "offer_text": "Would you like to add one?",
                        }
                    return result_dict

                # Handle archive operation
                if operation == "archive" and project_name:
                    # Find project by name
                    project = await portfolio_service.find_project_by_name(
                        name=project_name, user_id=user_id
                    )
                    if project:
                        result = await portfolio_service.archive_project(
                            project_id=str(project.id), user_id=user_id
                        )
                        return {
                            "message": result.message,
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "archive_project",
                                "confidence": 1.0,
                                "context": {
                                    "project_name": project_name,
                                    "status": result.status.value,
                                },
                            },
                            "requires_clarification": False,
                        }
                    else:
                        return {
                            "message": (
                                f"I couldn't find a project called '{project_name}'. "
                                "Would you like me to list your projects?"
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "project_not_found",
                                "confidence": 0.8,
                                "context": {"searched_name": project_name},
                            },
                            "requires_clarification": True,
                            # Issue #852: Track contextual offer
                            "offer_hint": {
                                "continuation_hint": "list all projects",
                                "offer_text": "Would you like me to list your projects?",
                            },
                        }

                # Handle delete operation (with confirmation)
                if operation == "delete" and project_name:
                    project = await portfolio_service.find_project_by_name(
                        name=project_name, user_id=user_id, include_archived=True
                    )
                    if project:
                        # Return confirmation request for destructive action
                        return {
                            "message": (
                                f"Are you sure you want to delete '{project.name}'? "
                                "This action cannot be undone. "
                                "You could also archive it instead if you might need it later."
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "delete_confirm",
                                "confidence": 1.0,
                                "context": {
                                    "project_id": str(project.id),
                                    "project_name": project.name,
                                    "awaiting_confirmation": True,
                                },
                            },
                            "requires_clarification": True,
                        }
                    else:
                        return {
                            "message": (
                                f"I couldn't find a project called '{project_name}'. "
                                "Would you like me to list your projects?"
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "project_not_found",
                                "confidence": 0.8,
                                "context": {"searched_name": project_name},
                            },
                            "requires_clarification": True,
                            # Issue #852: Track contextual offer
                            "offer_hint": {
                                "continuation_hint": "list all projects",
                                "offer_text": "Would you like me to list your projects?",
                            },
                        }

                # Handle restore operation
                if operation == "restore" and project_name:
                    project = await portfolio_service.find_project_by_name(
                        name=project_name, user_id=user_id, include_archived=True
                    )
                    if project:
                        result = await portfolio_service.restore_project(
                            project_id=str(project.id), user_id=user_id
                        )
                        return {
                            "message": result.message,
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "restore_project",
                                "confidence": 1.0,
                                "context": {
                                    "project_name": project_name,
                                    "status": result.status.value,
                                },
                            },
                            "requires_clarification": False,
                        }
                    else:
                        return {
                            "message": (
                                f"I couldn't find an archived project called '{project_name}'. "
                                "Would you like me to list your archived projects?"
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "project_not_found",
                                "confidence": 0.8,
                                "context": {"searched_name": project_name},
                            },
                            "requires_clarification": True,
                            # Issue #852: Track contextual offer
                            "offer_hint": {
                                "continuation_hint": "list archived projects",
                                "offer_text": "Would you like me to list your archived projects?",
                            },
                        }

                # Handle search operation
                if operation == "search":
                    # Extract search terms
                    search_terms = message_lower
                    for prefix in ["search projects for", "find project", "search for"]:
                        if prefix in search_terms:
                            search_terms = search_terms.split(prefix)[-1].strip()
                            break

                    results = await portfolio_service.search_projects(
                        query=search_terms, user_id=user_id
                    )
                    if results:
                        project_names = [p.name for p in results[:5]]
                        response = (
                            f"Found {len(results)} projects matching '{search_terms}':\n\n"
                            + "\n".join(f"- {name}" for name in project_names)
                        )
                    else:
                        response = (
                            f"I couldn't find any projects matching '{search_terms}'. "
                            "Would you like to see all your projects?"
                        )
                    result_dict = {
                        "message": response,
                        "intent": {
                            "category": IntentCategoryEnum.PORTFOLIO.value,
                            "action": "search_projects",
                            "confidence": 1.0,
                            "context": {
                                "query": search_terms,
                                "result_count": len(results),
                            },
                        },
                        "requires_clarification": len(results) == 0,
                    }
                    # Issue #852: Track contextual offer when search found no results
                    if not results:
                        result_dict["offer_hint"] = {
                            "continuation_hint": "list all projects",
                            "offer_text": "Would you like to see all your projects?",
                        }
                    return result_dict

            # Fallback for unrecognized portfolio operations (outside session - no DB needed)
            return {
                "message": (
                    "I can help you manage your projects. You can ask me to:\n"
                    "- Show your projects\n"
                    "- Archive a project\n"
                    "- Restore an archived project\n"
                    "- Search for projects\n"
                    "\nWhat would you like to do?"
                ),
                "intent": {
                    "category": IntentCategoryEnum.PORTFOLIO.value,
                    "action": "portfolio_help",
                    "confidence": 0.7,
                    "context": {"original_message": original_message},
                },
                "requires_clarification": True,
            }

        except Exception as e:
            logger.error(f"Portfolio handler error: {e}")
            return {
                "message": (
                    "I'm having trouble managing projects right now. "
                    "Please try again in a moment."
                ),
                "intent": {
                    "category": IntentCategoryEnum.PORTFOLIO.value,
                    "action": "portfolio_error",
                    "confidence": 0.5,
                    "context": {"error": str(e)},
                },
                "requires_clarification": False,
            }

    async def _handle_repo_management(
        self, intent: Intent, session_id: str, user_id: str = None
    ) -> Dict:
        """
        Handle repository management intents — link, unlink, list repos for projects.

        Issue #862: Conversational handler for 'link repo to project'.
        Uses #866 RepositoryRepository APIs (not ProjectIntegration).
        """
        import re

        from services.database.repositories import ProjectRepository, RepositoryRepository
        from services.database.session_factory import AsyncSessionFactory
        from services.domain import models as domain

        try:
            original_message = intent.context.get("original_message", "")
            message_lower = original_message.lower().strip()

            if not user_id:
                return {
                    "message": (
                        "I need to know who you are to manage repositories. "
                        "Please sign in first."
                    ),
                    "intent": {
                        "category": IntentCategoryEnum.PORTFOLIO.value,
                        "action": "manage_repos",
                        "confidence": 1.0,
                        "context": {},
                    },
                    "requires_clarification": False,
                }

            # Detect operation and extract entities
            operation = None
            repo_name = None
            project_name = None

            # Extract repo name (owner/repo format) from original message
            repo_match = re.search(r"([\w.-]+/[\w.-]+)", original_message)
            if repo_match:
                repo_name = repo_match.group(1)

            # Link patterns
            link_patterns = [
                r"\b(?:link|connect|add)\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?\s+)?(?:[\w.-]+/[\w.-]+)\s+to\s+(?:(?:my|the)\s+)?(?:project\s+)?(.+)",
                r"\b(?:link|connect|add)\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+to\s+(?:(?:my|the)\s+)?(?:project\s+)?(.+)",
            ]
            for pattern in link_patterns:
                match = re.search(pattern, message_lower, re.IGNORECASE)
                if match:
                    operation = "link"
                    project_name = self._clean_trailing_words(match.group(1).strip())
                    break

            # Unlink patterns
            if not operation:
                unlink_patterns = [
                    r"\b(?:unlink|disconnect|remove)\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?\s+)?(?:[\w.-]+/[\w.-]+)\s+from\s+(?:(?:my|the)\s+)?(?:project\s+)?(.+)",
                    r"\b(?:unlink|disconnect|remove)\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)\s+from\s+(?:(?:my|the)\s+)?(?:project\s+)?(.+)",
                ]
                for pattern in unlink_patterns:
                    match = re.search(pattern, message_lower, re.IGNORECASE)
                    if match:
                        operation = "unlink"
                        project_name = self._clean_trailing_words(match.group(1).strip())
                        break

            # List patterns
            if not operation:
                list_patterns = [
                    r"\b(?:show|list|view|which)\s+(?:(?:my|the)\s+)?(?:linked\s+)?repos\b",
                    r"\bwhich\s+repos?\s+(?:are\s+)?(?:linked|connected)\b",
                    r"\bshow\s+(?:project\s+)?repositories\b",
                ]
                for pattern in list_patterns:
                    if re.search(pattern, message_lower, re.IGNORECASE):
                        operation = "list"
                        # Check if project name is mentioned
                        proj_match = re.search(
                            r"(?:for|of|on)\s+(?:(?:my|the)\s+)?(?:project\s+)?(.+)",
                            message_lower,
                        )
                        if proj_match:
                            project_name = self._clean_trailing_words(proj_match.group(1).strip())
                        break

            # Fallback: detect unlink/disconnect verb even without "from <project>"
            if not operation:
                if re.search(
                    r"\b(?:unlink|disconnect)\s+(?:(?:my|the|a)\s+)?(?:repo(?:sitory)?)",
                    message_lower,
                ):
                    operation = "unlink"

            # Default to list if no operation detected
            if not operation:
                operation = "list"

            async with AsyncSessionFactory.session_scope() as session:
                project_repo = ProjectRepository(session)
                repo_repo = RepositoryRepository(session)

                # --- LINK ---
                if operation == "link":
                    if not repo_name:
                        return {
                            "message": (
                                "Which repository would you like to link? "
                                "Please provide the repository name in owner/repo format "
                                "(e.g., octocat/hello-world)."
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "link_repo",
                                "confidence": 1.0,
                                "context": {"needs": "repo_name"},
                            },
                            "requires_clarification": True,
                        }

                    if not project_name:
                        return {
                            "message": (
                                f"Which project should I link {repo_name} to? "
                                "Please tell me the project name."
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "link_repo",
                                "confidence": 1.0,
                                "context": {
                                    "repo_name": repo_name,
                                    "needs": "project_name",
                                },
                            },
                            "requires_clarification": True,
                        }

                    # Find project
                    project = await project_repo.find_by_name(name=project_name, owner_id=user_id)
                    if not project:
                        return {
                            "message": (
                                f"I couldn't find a project called '{project_name}'. "
                                "Check the name and try again, or say 'show my projects' "
                                "to see your project list."
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "link_repo",
                                "confidence": 1.0,
                                "context": {
                                    "repo_name": repo_name,
                                    "project_name": project_name,
                                    "error": "project_not_found",
                                },
                            },
                            "requires_clarification": False,
                        }

                    # Find or create repo
                    repo = await repo_repo.get_by_full_name(
                        full_name=repo_name, provider="github", owner_id=user_id
                    )
                    validation_note = ""
                    if not repo:
                        # Issue #867: Soft-validate via GitHub API
                        from services.infrastructure.github_repo_validator import (
                            apply_validation_metadata,
                            validate_github_repo,
                        )

                        validation = await validate_github_repo(repo_name)
                        if validation.validated and not validation.exists:
                            validation_note = (
                                " (Note: I couldn't verify this repo on GitHub"
                                " — check the name in Settings if needed.)"
                            )

                        repo_domain = domain.Repository(
                            owner_id=user_id,
                            provider="github",
                            full_name=repo_name,
                            display_name=repo_name.split("/")[-1],
                            url=f"https://github.com/{repo_name}",
                        )
                        apply_validation_metadata(repo_domain, validation)
                        repo = await repo_repo.create_repository(repo_domain)

                    # Check if already linked
                    existing_links = await repo_repo.get_project_links(repo.id)
                    for link in existing_links:
                        if link.project_id == project.id:
                            return {
                                "message": (
                                    f"{repo_name} is already linked to {project.name}. "
                                    "No changes needed."
                                ),
                                "intent": {
                                    "category": IntentCategoryEnum.PORTFOLIO.value,
                                    "action": "link_repo",
                                    "confidence": 1.0,
                                    "context": {
                                        "repo_name": repo_name,
                                        "project_name": project.name,
                                        "status": "already_linked",
                                    },
                                },
                                "requires_clarification": False,
                            }

                    # Create the link
                    await repo_repo.link_to_project(
                        repository_id=repo.id,
                        project_id=project.id,
                        linked_by=user_id,
                    )

                    return {
                        "message": (
                            f"Done! I've linked {repo_name} to your {project.name} project. "
                            "I can now help you track issues, PRs, and activity for this repo."
                            f"{validation_note}"
                        ),
                        "intent": {
                            "category": IntentCategoryEnum.PORTFOLIO.value,
                            "action": "link_repo",
                            "confidence": 1.0,
                            "context": {
                                "repo_name": repo_name,
                                "project_name": project.name,
                                "project_id": project.id,
                                "repository_id": repo.id,
                            },
                        },
                        "requires_clarification": False,
                    }

                # --- UNLINK ---
                if operation == "unlink":
                    if not repo_name or not project_name:
                        return {
                            "message": (
                                "To unlink a repository, tell me both the repo name "
                                "(owner/repo) and the project name. For example: "
                                "'unlink octocat/hello-world from My Project'"
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "unlink_repo",
                                "confidence": 1.0,
                                "context": {"needs": "both"},
                            },
                            "requires_clarification": True,
                        }

                    project = await project_repo.find_by_name(name=project_name, owner_id=user_id)
                    if not project:
                        return {
                            "message": f"I couldn't find a project called '{project_name}'.",
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "unlink_repo",
                                "confidence": 1.0,
                                "context": {"error": "project_not_found"},
                            },
                            "requires_clarification": False,
                        }

                    repo = await repo_repo.get_by_full_name(
                        full_name=repo_name, provider="github", owner_id=user_id
                    )
                    if not repo:
                        return {
                            "message": f"I couldn't find a repository called '{repo_name}'.",
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "unlink_repo",
                                "confidence": 1.0,
                                "context": {"error": "repo_not_found"},
                            },
                            "requires_clarification": False,
                        }

                    removed = await repo_repo.unlink_from_project(repo.id, project.id)
                    if not removed:
                        return {
                            "message": (
                                f"{repo_name} wasn't linked to {project.name}. "
                                "Nothing to remove."
                            ),
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "unlink_repo",
                                "confidence": 1.0,
                                "context": {"status": "not_linked"},
                            },
                            "requires_clarification": False,
                        }

                    return {
                        "message": (f"Done! I've unlinked {repo_name} from {project.name}."),
                        "intent": {
                            "category": IntentCategoryEnum.PORTFOLIO.value,
                            "action": "unlink_repo",
                            "confidence": 1.0,
                            "context": {
                                "repo_name": repo_name,
                                "project_name": project.name,
                            },
                        },
                        "requires_clarification": False,
                    }

                # --- LIST ---
                if operation == "list":
                    if project_name:
                        # List repos for a specific project
                        project = await project_repo.find_by_name(
                            name=project_name, owner_id=user_id
                        )
                        if not project:
                            return {
                                "message": (f"I couldn't find a project called '{project_name}'."),
                                "intent": {
                                    "category": IntentCategoryEnum.PORTFOLIO.value,
                                    "action": "list_repos",
                                    "confidence": 1.0,
                                    "context": {"error": "project_not_found"},
                                },
                                "requires_clarification": False,
                            }

                        repos = await repo_repo.list_by_project(project.id)
                        if repos:
                            repo_lines = []
                            for r in repos:
                                icon = {"github": "🐙", "gitlab": "🦊", "bitbucket": "🪣"}.get(
                                    r.provider, "📦"
                                )
                                repo_lines.append(f"- {icon} {r.full_name} ({r.provider})")
                            response = (
                                f"**{project.name}** has {len(repos)} linked "
                                f"{'repository' if len(repos) == 1 else 'repositories'}:\n\n"
                                + "\n".join(repo_lines)
                            )
                        else:
                            response = (
                                f"{project.name} doesn't have any linked repositories yet. "
                                "You can link one by saying something like "
                                "'link owner/repo to " + project.name + "'."
                            )

                        return {
                            "message": response,
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "list_repos",
                                "confidence": 1.0,
                                "context": {
                                    "project_name": project.name,
                                    "repo_count": len(repos) if repos else 0,
                                },
                            },
                            "requires_clarification": False,
                        }
                    else:
                        # List all user's repos
                        repos = await repo_repo.list_by_owner(owner_id=user_id)
                        if repos:
                            repo_lines = []
                            for r in repos:
                                icon = {"github": "🐙", "gitlab": "🦊", "bitbucket": "🪣"}.get(
                                    r.provider, "📦"
                                )
                                repo_lines.append(f"- {icon} {r.full_name} ({r.provider})")
                            response = (
                                f"You have {len(repos)} registered "
                                f"{'repository' if len(repos) == 1 else 'repositories'}:\n\n"
                                + "\n".join(repo_lines)
                                + "\n\nTo see which project a repo is linked to, "
                                "ask 'show repos for [project name]'."
                            )
                        else:
                            response = (
                                "You don't have any registered repositories yet. "
                                "You can register one by saying 'link owner/repo to [project]'."
                            )

                        return {
                            "message": response,
                            "intent": {
                                "category": IntentCategoryEnum.PORTFOLIO.value,
                                "action": "list_repos",
                                "confidence": 1.0,
                                "context": {"repo_count": len(repos) if repos else 0},
                            },
                            "requires_clarification": False,
                        }

        except Exception as e:
            logger.error(f"Repo management handler error: {e}")
            return {
                "message": (
                    "I'm having trouble managing repositories right now. "
                    "Please try again in a moment."
                ),
                "intent": {
                    "category": IntentCategoryEnum.PORTFOLIO.value,
                    "action": "manage_repos_error",
                    "confidence": 0.5,
                    "context": {"error": str(e)},
                },
                "requires_clarification": False,
            }

    @staticmethod
    def _clean_trailing_words(name: str) -> str:
        """Remove common trailing filler words from extracted names."""
        if not name:
            return name
        trailing_words = [
            "please",
            "now",
            "thanks",
            "thank you",
            "asap",
            "for me",
            "right now",
            "immediately",
            "today",
        ]
        cleaned = name.strip()
        for word in trailing_words:
            if cleaned.lower().endswith(f" {word}"):
                cleaned = cleaned[: -(len(word) + 1)].strip()
        return cleaned

    async def _handle_conversation_query(
        self, intent: Intent, session_id: str, user_id: Optional[str] = None
    ) -> Dict:
        """
        Handle CONVERSATION category intents (Tier 1 bypass).

        Issue #286: Moved to canonical section for architectural consistency.
        CONVERSATION is a canonical category like IDENTITY, TEMPORAL, etc.

        Phase 3D: Conversation handling without full orchestration.
        """
        # Initialize conversation handler
        conversation_handler = ConversationHandler(session_manager=None)

        # Get conversation response
        # Issue #849: Thread user_id for user-scoped calendar auth
        result = await conversation_handler.respond(intent, session_id, user_id=user_id)

        # Return in canonical format (Dict)
        return {
            "message": result["message"],
            "intent": result["intent"],
            "workflow_id": result.get("workflow_id"),
            "requires_clarification": result.get("requires_clarification", False),
            "clarification_type": result.get("clarification_type"),
        }

    # Issue #1030 R4: human-readable phrases per provenance key. Used by
    # _handle_provenance_query to convert structured provenance dict into
    # colleague-prose citation (PM Q2 disposition (b)).
    _PROVENANCE_PHRASES = {
        "calendar": "your Google Calendar (your scheduled meetings + free blocks at the time)",
        "pending_todos": "your open todos from the todo manager",
        "completed_todos": "your recently-completed todos",
        "blocked_items": "the GitHub issues you have labeled `status:blocked`",
        "active_milestones": "the open milestones on your tracked GitHub repos",
        "recent_activity": "the cross-source activity feed (GitHub + calendar + Slack, merged)",
        "user_projects": "the projects in your user profile",
        "organization": "your organization profile",
        "recent_topics": "the recent topics from our conversation",
        "session_turn_count": "how many turns we've taken this session",
        "priorities": "your stated priorities + GitHub high-priority items",
        "urgent_items": "the high-priority GitHub items at the time",
        "user_priorities": "your stated priorities from your profile",
        "conversation_history_summary": "our conversation history",
        "persistent_memory": "what I remember about our prior conversations",
        "capabilities": "what I know I can do (workflow + plugin registries)",
        "integrations": "your active integrations (plugin registry)",
        "trust_profile": "your trust profile + stage",
        "insights": "the composted insights I've drawn from our work together",
        "reminders": "your due reminders",
        "projects": "your tracked projects",
    }

    async def _handle_provenance_query(
        self, intent: Intent, session_id: str, user_id: Optional[str] = None
    ) -> Dict:
        """Issue #1030 R4: handle 'why did you suggest that?' queries.

        Looks up the most recent assistant turn's provenance in the
        ConversationContext sidecar. Formats a colleague-prose citation per
        PM Q2 disposition (b): natural language, five-pillar voice, not terse.

        Honest empty-state: if no prior turn has provenance (out-of-window,
        first turn of session, or floor route without context), respond
        plainly that we don't have a record. Never fabricate.
        """
        try:
            from services.intent_service.conversation_context import get_or_create_context

            conv_ctx = get_or_create_context(session_id, user_id=user_id)
            prov = conv_ctx.get_last_turn_provenance()
            fallback_source = "sidecar"

            # Issue #1030 R4 Step 11: cross-session GUARANTEED (PM Q1).
            # When in-memory sidecar misses (turn aged out of 30-min/10-turn
            # window, or process restarted), fall back to ConversationRepository
            # which queries turn_metadata['provenance'] from ConversationTurnDB.
            if not prov:
                try:
                    from services.database.repositories import ConversationRepository
                    from services.database.session_factory import AsyncSessionFactory

                    async with AsyncSessionFactory.session_scope() as db_session:
                        repo = ConversationRepository(db_session)
                        prov = await repo.get_most_recent_turn_provenance(session_id)
                    if prov:
                        fallback_source = "db"
                        logger.info(
                            "provenance_query_db_fallback_hit",
                            session_id=session_id,
                            user_id=user_id,
                        )
                except Exception as db_err:
                    logger.warning(
                        "provenance_db_fallback_error",
                        session_id=session_id,
                        error=str(db_err),
                    )

            if not prov:
                # Honest no-record response
                message = (
                    "I don't have a clear record of what I was drawing on for that — "
                    "either it's been long enough that the context aged out, or I "
                    "didn't have specific facts in hand when I said it. If you can "
                    "point me at what you're asking about ('the meeting?' / "
                    "'the priority?'), I can try to reconstruct from what I know now."
                )
                logger.info(
                    "provenance_query_no_record",
                    session_id=session_id,
                    user_id=user_id,
                )
                return {
                    "message": message,
                    "intent": {
                        "category": IntentCategoryEnum.PROVENANCE.value,
                        "action": "explain_suggestion",
                        "confidence": intent.confidence,
                        "context": intent.context or {},
                    },
                    "requires_clarification": False,
                    "provenance_hit": False,  # Telemetry per Step 10
                    "keys_cited": 0,
                }

            # Format colleague-prose citation
            phrases = []
            for key in prov.keys():
                phrase = self._PROVENANCE_PHRASES.get(key)
                if phrase:
                    phrases.append(phrase)
                else:
                    # Unknown key — name it plainly rather than skip
                    phrases.append(f"{key.replace('_', ' ')}")

            # Special-case push_insight (added in Step 8)
            push_phrase = None
            if "push_insight" in prov:
                push_phrase = "an insight I composted from our prior work that seemed relevant"

            if push_phrase and push_phrase not in phrases:
                # push_insight is already in PROVENANCE_PHRASES? add only if missing
                pass  # already added via map lookup

            if not phrases:
                message = (
                    "I had context available when I composed that, but I'm not "
                    "able to name the specific sources right now. If you can be "
                    "more specific about what you're asking about, I can try to "
                    "track it down."
                )
            elif len(phrases) == 1:
                message = (
                    f"When I said that, I was drawing on {phrases[0]}. "
                    "Let me know if you want me to walk through it more concretely."
                )
            elif len(phrases) == 2:
                message = (
                    f"When I said that, I was drawing on {phrases[0]} and "
                    f"{phrases[1]}. Happy to walk through either more concretely."
                )
            else:
                # Use Oxford comma for 3+
                lead = ", ".join(phrases[:-1])
                message = (
                    f"When I said that, I was drawing on {lead}, and "
                    f"{phrases[-1]}. Happy to walk through any of those more concretely."
                )

            logger.info(
                "provenance_query_hit",
                session_id=session_id,
                user_id=user_id,
                provenance_hit=True,
                keys_cited=len(phrases),
                provenance_keys=list(prov.keys()),
                fallback_source=fallback_source,  # "sidecar" or "db"
            )
            return {
                "message": message,
                "intent": {
                    "category": IntentCategoryEnum.PROVENANCE.value,
                    "action": "explain_suggestion",
                    "confidence": intent.confidence,
                    "context": intent.context or {},
                },
                "requires_clarification": False,
                "provenance_hit": True,  # Telemetry per Step 10
                "keys_cited": len(phrases),
                "fallback_source": fallback_source,  # Step 11 telemetry
            }
        except Exception as e:
            logger.error(
                "provenance_query_error",
                error=str(e),
                session_id=session_id,
                user_id=user_id,
            )
            return {
                "message": (
                    "I ran into a snag retrieving what I was drawing on for that. "
                    "Could you ask again, or be more specific about which part?"
                ),
                "intent": {
                    "category": IntentCategoryEnum.PROVENANCE.value,
                    "action": "explain_suggestion",
                    "confidence": intent.confidence,
                    "context": intent.context or {},
                },
                "requires_clarification": False,
                "provenance_hit": False,
                "keys_cited": 0,
                "error": str(e),
            }


# Global instance
_canonical_handlers = None


def get_canonical_handlers() -> CanonicalHandlers:
    """Get singleton CanonicalHandlers instance"""
    global _canonical_handlers
    if _canonical_handlers is None:
        _canonical_handlers = CanonicalHandlers()
    return _canonical_handlers
