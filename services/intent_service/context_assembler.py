"""
Context Assembler for Conversational Floor (#911 Phase 2)

Gathers structured data for the conversational floor, organized by intent
category. The floor LLM receives raw facts and decides what's relevant to
the user's question.

Design principles:
1. Declarative — returns structured data (facts, lists), not formatted text
2. Fail-graceful — partial results on failure, never throws
3. Cache-ready — design for Redis TTL caching later (not implemented yet)
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger()


class ContextAssembler:
    """Gathers structured context for the conversational floor."""

    async def gather_context(
        self,
        intent_category: str,
        user_id: str = None,
        session_id: str = None,
    ) -> Dict[str, Any]:
        """
        Main entry point. Returns structured data for floor injection.

        Routes to category-specific gatherers based on intent_category.
        Always returns a dict (possibly empty on total failure).
        """
        context: Dict[str, Any] = {}

        # Current time is always useful
        context["current_time"] = datetime.now().strftime("%I:%M %p")

        category = (intent_category or "").upper()

        try:
            if category in ("IDENTITY", "DISCOVERY"):
                ctx = await self._gather_identity_context(user_id)
                context.update(ctx)
            elif category == "TRUST":
                ctx = await self._gather_trust_context(user_id)
                context.update(ctx)
            elif category == "MEMORY":
                ctx = await self._gather_memory_context(user_id, session_id)
                context.update(ctx)
            elif category == "CONVERSATION":
                # Issue #903: Surface due reminders for greeting context
                ctx = await self._gather_reminder_context(user_id)
                if ctx:
                    context.update(ctx)
            elif category == "TEMPORAL":
                # #965: Temporal context for non-date queries (agenda, retrospective, etc.)
                ctx = await self._gather_temporal_context(user_id, session_id)
                context.update(ctx)
            elif category in ("STATUS", "PRIORITY"):
                # #925: Project status and priority context for floor
                ctx = await self._gather_status_priority_context(user_id)
                context.update(ctx)
            else:
                # #960: UNKNOWN and other unhandled categories get basic user
                # context to reduce fabrication risk. Better to give the floor
                # real entities (even if not the right ones for the specific
                # query) than zero context where it might invent data.
                if user_id:
                    ctx = await self._gather_status_priority_context(user_id)
                    context.update(ctx)
        except Exception as e:
            logger.warning(
                "context_assembler_gather_error",
                category=category,
                error=str(e),
            )

        # #960: Context contract violation logging — warn when a data-query
        # category reaches the floor with no user data in context.
        _DATA_CATEGORIES = {"TEMPORAL", "STATUS", "PRIORITY"}
        _DATA_KEYS = {"pending_todos", "completed_todos", "projects", "priorities"}
        if category in _DATA_CATEGORIES:
            has_data = any(k in context for k in _DATA_KEYS)
            if not has_data:
                logger.warning(
                    "context_contract_empty_data",
                    category=category,
                    user_id=user_id,
                    session_id=session_id,
                    context_keys=list(context.keys()),
                    note="Floor received a data-query category with no user data",
                )

        return context

    async def _gather_identity_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Gather Piper's capabilities and plugin status for identity-adjacent questions.

        #923: Capabilities are derived from the workflow dispatcher registry
        and plugin registry — not hardcoded. This ensures the LLM's awareness
        of what Piper can do stays in sync with runtime truth.
        """
        context: Dict[str, Any] = {}

        # #923: Build capabilities from dispatcher registry + conversational strengths
        capabilities = [
            "conversational PM guidance",
            "strategic thinking and prioritization frameworks",
        ]
        try:
            from services.intent_service.workflow_dispatcher import get_registered_workflows

            registered = get_registered_workflows()
            for wf_type, entry in registered.items():
                desc = entry.description or wf_type.replace("_", " ")
                capabilities.append(desc)
        except Exception as e:
            logger.warning("context_assembler_registry_error", error=str(e))

        context["capabilities"] = capabilities

        # Integrations from plugin registry (dynamic, reflects runtime state)
        try:
            from services.plugins import get_plugin_registry

            registry = get_plugin_registry()
            plugin_status = registry.get_status_all()

            integrations = []
            for name, status in plugin_status.items():
                is_configured = status.get("configured", False)
                is_active = status.get("active", False) or status.get("status") == "active"
                integrations.append(
                    {
                        "name": name,
                        "status": "active" if (is_configured or is_active) else "inactive",
                    }
                )

            context["integrations"] = integrations
        except Exception as e:
            logger.warning("context_assembler_identity_capabilities_error", error=str(e))

        return context

    async def _gather_discovery_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Gather available capabilities list for DISCOVERY intents.

        Same data as identity context — capabilities and integrations.
        """
        return await self._gather_identity_context(user_id)

    async def _gather_trust_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Gather trust profile data for TRUST intents.

        Reads from UserTrustProfileRepository if user_id available.
        """
        context: Dict[str, Any] = {}

        if not user_id:
            context["trust_profile"] = {
                "stage": "unknown",
                "note": "No user ID available — trust profile not loaded",
            }
            return context

        try:
            from uuid import UUID

            from services.database.session_factory import AsyncSessionFactory
            from services.repositories.user_trust_profile_repository import (
                UserTrustProfileRepository,
            )

            async with AsyncSessionFactory.session_scope() as session:
                trust_repo = UserTrustProfileRepository(session)
                profile = await trust_repo.get_by_user_id(UUID(user_id))

                if profile:
                    context["trust_profile"] = {
                        "stage": profile.trust_stage.value if profile.trust_stage else "new",
                        "interaction_count": getattr(profile, "interaction_count", 0),
                    }
                else:
                    context["trust_profile"] = {
                        "stage": "new",
                        "interaction_count": 0,
                    }
        except Exception as e:
            logger.warning("context_assembler_trust_error", error=str(e))
            context["trust_profile"] = {
                "stage": "unknown",
                "note": "Could not load trust profile",
            }

        return context

    async def _gather_memory_context(
        self, user_id: str = None, session_id: str = None
    ) -> Dict[str, Any]:
        """
        Gather conversation history summary for MEMORY intents.

        Reads from in-memory conversation context and UserHistoryService.
        """
        context: Dict[str, Any] = {}

        # Conversation context (in-memory turns)
        if session_id:
            try:
                from services.intent_service.conversation_context import get_or_create_context

                conv_ctx = get_or_create_context(session_id, user_id=user_id)
                recent_topics = []
                for turn in conv_ctx.turns[-6:]:
                    if turn.message:
                        # Extract a short summary (first 80 chars)
                        summary = turn.message[:80]
                        if len(turn.message) > 80:
                            summary += "..."
                        recent_topics.append(summary)

                context["conversation_history_summary"] = {
                    "recent_topics": recent_topics,
                    "turn_count": len(conv_ctx.turns),
                }
            except Exception as e:
                logger.warning("context_assembler_memory_history_error", error=str(e))

        # User history service (persistent memory)
        if user_id:
            try:
                from services.memory.user_history import (
                    InMemoryUserHistoryRepository,
                    UserHistoryService,
                )

                history_repo = InMemoryUserHistoryRepository()
                history_service = UserHistoryService(history_repo)
                summary = await history_service.get_history_summary(user_id=user_id)

                if summary:
                    context["persistent_memory"] = {
                        "has_history": True,
                        "summary": summary,
                    }
            except Exception as e:
                logger.warning("context_assembler_memory_persistent_error", error=str(e))

        return context

    async def _gather_temporal_context(
        self, user_id: str = None, session_id: str = None
    ) -> Dict[str, Any]:
        """
        #965: Gather temporal context for non-date queries routed to the floor.

        Provides data that the LLM needs to answer questions like:
        - "What did we accomplish yesterday?" → completed todos, project activity
        - "What's on the agenda for today?" → calendar events, pending todos
        - "When was the last time we worked on this?" → project activity dates
        - "How long have we been working on this?" → project creation dates

        All sources are fail-graceful: missing data is expressed as absence,
        never as an exception. The floor LLM composes honestly around gaps.
        """
        context: Dict[str, Any] = {}

        # Current date with day of week (useful for all temporal questions)
        now = datetime.now()
        context["current_date"] = now.strftime("%A, %B %d, %Y")
        context["current_day_of_week"] = now.strftime("%A")

        # Pending todos (for agenda queries)
        if user_id:
            try:
                from uuid import UUID

                from services.todo.todo_management_service import TodoManagementService

                todo_svc = TodoManagementService()
                pending = await todo_svc.list_todos(
                    user_id=UUID(user_id), include_completed=False
                )
                if pending:
                    context["pending_todos"] = [
                        {"text": t.text, "priority": getattr(t, "priority", "medium")}
                        for t in pending[:10]  # cap at 10
                    ]
                    context["pending_todo_count"] = len(pending)

                # Completed todos (for retrospective queries)
                all_todos = await todo_svc.list_todos(
                    user_id=UUID(user_id), include_completed=True
                )
                completed = [t for t in all_todos if getattr(t, "completed", False)]
                if completed:
                    context["completed_todos"] = [
                        {"text": t.text, "completed_at": str(getattr(t, "completed_at", ""))}
                        for t in completed[:10]
                    ]
                    context["completed_todo_count"] = len(completed)
            except Exception as e:
                logger.warning("context_assembler_temporal_todos_error", error=str(e))

        # Project metadata (for duration and activity queries)
        if user_id:
            try:
                from uuid import UUID

                from services.database.session_factory import AsyncSessionFactory

                async with AsyncSessionFactory.session_scope() as session:
                    from sqlalchemy import select, text

                    result = await session.execute(
                        text(
                            "SELECT name, created_at, updated_at FROM projects "
                            "WHERE owner_id = :uid ORDER BY updated_at DESC LIMIT 5"
                        ),
                        {"uid": user_id},
                    )
                    rows = result.fetchall()
                    if rows:
                        context["projects"] = [
                            {
                                "name": r[0],
                                "created_at": str(r[1]) if r[1] else None,
                                "last_updated": str(r[2]) if r[2] else None,
                            }
                            for r in rows
                        ]
            except Exception as e:
                logger.warning("context_assembler_temporal_projects_error", error=str(e))

        # Conversation history summary (for "what did we discuss" context)
        if session_id:
            try:
                from services.intent_service.conversation_context import get_or_create_context

                conv_ctx = get_or_create_context(session_id, user_id=user_id)
                if conv_ctx.turns:
                    context["conversation_history_summary"] = {
                        "turn_count": len(conv_ctx.turns),
                        "recent_topics": [
                            t.message[:80] for t in conv_ctx.turns[-4:] if t.message
                        ],
                    }
            except Exception as e:
                logger.warning("context_assembler_temporal_history_error", error=str(e))

        return context

    async def _gather_status_priority_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        #925: Gather project status and priority context for floor routing.

        Provides data for queries like:
        - "What am I working on?" → project list with GitHub metadata
        - "What's my top priority?" → priorities with high-priority issues
        - "Show me project landscape" → project overview
        - "Which project should I focus on?" → priority-ranked projects

        Same data sources as the canonical STATUS/PRIORITY handlers, but
        assembled as structured context for the floor LLM to compose from.
        """
        context: Dict[str, Any] = {}

        # User context (projects, priorities, organization)
        try:
            from services.user_context_service import user_context_service

            user_ctx = await user_context_service.get_user_context(
                session_id=None, user_id=user_id
            )
            if user_ctx:
                if hasattr(user_ctx, "projects") and user_ctx.projects:
                    context["projects"] = [
                        {"name": p} if isinstance(p, str) else p
                        for p in user_ctx.projects[:10]
                    ]
                if hasattr(user_ctx, "priorities") and user_ctx.priorities:
                    context["priorities"] = user_ctx.priorities[:5]
                if hasattr(user_ctx, "organization") and user_ctx.organization:
                    context["organization"] = user_ctx.organization
        except Exception as e:
            logger.warning("context_assembler_status_user_context_error", error=str(e))

        # Pending todos (relevant for "what should I work on" context)
        if user_id:
            try:
                from uuid import UUID

                from services.todo.todo_management_service import TodoManagementService

                todo_svc = TodoManagementService()
                pending = await todo_svc.list_todos(
                    user_id=UUID(user_id), include_completed=False
                )
                if pending:
                    context["pending_todos"] = [
                        {"text": t.text, "priority": getattr(t, "priority", "medium")}
                        for t in pending[:5]
                    ]
            except Exception as e:
                logger.warning("context_assembler_status_todos_error", error=str(e))

        # GitHub high-priority issues (for priority context)
        try:
            from services.plugins import get_plugin_registry

            registry = get_plugin_registry()
            github_status = registry.get_status_all().get("github", {})
            if github_status.get("configured") or github_status.get("active"):
                context["github_connected"] = True
            else:
                context["github_connected"] = False
        except Exception as e:
            logger.warning("context_assembler_status_github_error", error=str(e))
            context["github_connected"] = False

        return context

    async def _gather_reminder_context(self, user_id: str = None) -> Dict[str, Any]:
        """
        Issue #903: Check for due reminders to surface at greeting time.

        Queries todos with reminder_date <= now that are still active.
        Returns context that the floor can weave into the greeting.
        """
        if not user_id:
            return {}

        try:
            from uuid import UUID

            from services.intent_service.todo_handlers import TodoIntentHandlers

            handlers = TodoIntentHandlers()
            due_reminders = await handlers.get_due_reminders(UUID(user_id))

            if due_reminders:
                return {
                    "due_reminders": due_reminders,
                    "reminder_count": len(due_reminders),
                }
        except Exception as e:
            logger.warning("context_assembler_reminder_error", error=str(e))

        return {}
