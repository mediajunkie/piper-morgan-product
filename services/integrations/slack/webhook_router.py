"""
Slack Socket Mode slash-command processor.

Originally a FastAPI router carrying the full Slack webhook surface (Events
API, OAuth callback, interactive components, slash commands, signature
verification). The Oct 2025 CORE-GREAT-2D refactor removed the HTTP mount;
#1129 rebuilt inbound on Socket Mode instead
(services/integrations/slack/socket_mode_runner.py). Socket Mode's
events_api envelopes are handled directly by
SlackSocketModeRunner._handle_event(), which talks to intent_service
directly — this class is no longer in that path at all.

What's still live: SlackSocketModeRunner._handle_slash_command() lazily
builds one instance of this class on the first slash command and calls
_process_slash_command() with the same form-body dict the old HTTP webhook
carried (#1496), so the /piper, /standup and /link command logic below —
including _handle_link_command, the sanctioned caller of the #1466
identity-binding invariant (see tests/test_slack_identity_binding_guard.py)
— kept working without a rewrite.

#1499 Class 2 member strip (2026-09-23): removed the entire dead FastAPI
surface (self.router / APIRouter construction, _register_routes,
register_webhook_routes, get_router, get_webhook_urls, and the six HTTP
route handlers), PLUS the Events-API event-processing pipeline
(_process_event_callback and everything under it) and the
signature-verification/DI plumbing that only those two dead trees used.
That pipeline was previously believed "live and tested" (see the disposal
record below) — it is directly unit-tested, but nothing in production ever
calls it: the Events API route was never mounted, and Socket Mode's own
event handling bypasses this class entirely (it never calls
handle_slack_events, _process_event_callback, or any of
_process_message_event / _process_mention_event / _process_reaction_event /
_process_channel_join_event). "Tested" was not "live" for that tree.
See docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md
for the full disposal history and the member table this strip is based on.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy import select

logger = logging.getLogger(__name__)


class SlackWebhookRouter:
    """
    Socket Mode slash-command processor for /piper, /standup, and /link.

    Constructed with no arguments — socket_mode_runner.py lazily builds one
    instance and reuses it for every slash command. Holds no instance state:
    every method below either dispatches on the incoming command payload or
    does its own local service lookups per call, so there is no __init__ to
    speak of (the default one from object is sufficient).
    """

    # Private processing methods

    async def _process_slash_command(self, command_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process slash command and route to appropriate handler.

        Issue #520: Implements routing for Canonical Queries #49, #50
        - /piper help → _handle_piper_command()
        - /standup → _handle_standup_command()

        Args:
            command_data: Slack command payload with command, text, user_id, channel_id

        Returns:
            Dict with response_type and text/blocks for Slack response
        """
        try:
            command = command_data.get("command", "")
            text = command_data.get("text", "").strip().lower()
            channel_id = command_data.get("channel_id")
            user_id = command_data.get("user_id")
            # #1466: slash payloads carry team_id; principal resolution is keyed
            # by the (slack_user_id, slack_team_id) pair.
            team_id = command_data.get("team_id")

            logger.info(f"Slash command {command} from user {user_id} in channel {channel_id}")

            # Route based on command
            if command == "/piper":
                return await self._handle_piper_command(text, user_id, channel_id)
            elif command == "/standup":
                return await self._handle_standup_command(user_id, channel_id, team_id=team_id)
            elif command == "/link":
                # #1466: redeem-in-Slack half of the linking handshake
                return await self._handle_link_command(text, user_id, team_id)
            else:
                return {
                    "response_type": "ephemeral",
                    "text": f"Unknown command: {command}. Try `/piper help` for available commands.",
                }

        except Exception as e:
            logger.error(f"Error processing slash command: {e}")
            return {"response_type": "ephemeral", "text": "Error processing command"}

    async def _handle_piper_command(
        self, text: str, user_id: str, channel_id: str
    ) -> Dict[str, Any]:
        """
        Handle /piper commands.

        Issue #520: Query #50 - "/piper help"
        Issue #551 Phase 4: Extended subcommands for calendar, status, priority

        Subcommands:
        - help: Show available commands and capabilities
        - (empty): Same as help
        - calendar: Show today's calendar
        - status: Show current project status
        - priority: Show top priority item

        Args:
            text: Command text after /piper
            user_id: Slack user ID
            channel_id: Slack channel ID

        Returns:
            Ephemeral response with command output
        """
        # Normalize and parse subcommand
        subcommand = text.strip().lower() if text else ""

        if subcommand == "help" or subcommand == "":
            return await self._build_help_response()

        # Issue #551 Phase 4: Calendar subcommand
        elif subcommand in ("calendar", "cal", "today"):
            return await self._handle_calendar_subcommand(user_id, channel_id)

        # Issue #551 Phase 4: Status subcommand
        elif subcommand in ("status", "projects"):
            return await self._handle_status_subcommand(user_id, channel_id)

        # Issue #551 Phase 4: Priority subcommand
        elif subcommand in ("priority", "focus", "top"):
            return await self._handle_priority_subcommand(user_id, channel_id)

        else:
            # Issue #628: Warm response for unknown commands
            return {
                "response_type": "ephemeral",
                "text": f"I don't recognize `{subcommand}` - try `/piper help` to see what I can do!",
            }

    async def _handle_calendar_subcommand(self, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Handle /piper calendar subcommand.

        Issue #551 Phase 4: Calendar parity on Slack.
        Routes to canonical temporal handler for calendar information.
        """
        try:
            from services.domain.models import Intent
            from services.intent_service.canonical_handlers import CanonicalHandlers
            from services.shared_types import IntentCategory

            handlers = CanonicalHandlers()

            # Create a minimal intent for calendar query
            # #1436: Intent's real shape is (category, action, ...) — the old
            # raw_input/classification kwargs TypeError'd, so every /piper
            # calendar hit the generic failure copy.
            intent = Intent(
                category=IntentCategory.TEMPORAL,
                action="get_current_time",
                confidence=1.0,
                original_message="what's on my calendar today?",
            )

            # Call the canonical handler
            result = await handlers._handle_temporal_query(
                intent, session_id=f"slack_{user_id}", user_id=user_id
            )

            message = result.get("message", "I couldn't retrieve your calendar.")

            return {
                "response_type": "ephemeral",
                "text": message,
            }

        except Exception as e:
            logger.error(f"Error handling calendar subcommand: {e}")
            return {
                "response_type": "ephemeral",
                "text": "I'm having trouble accessing your calendar right now. Please try again later.",
            }

    async def _handle_status_subcommand(self, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Handle /piper status subcommand.

        Issue #551 Phase 4: Status parity on Slack.
        Routes to canonical status handler for project status.
        """
        try:
            from services.domain.models import Intent
            from services.intent_service.canonical_handlers import CanonicalHandlers
            from services.shared_types import IntentCategory

            handlers = CanonicalHandlers()

            # Create a minimal intent for status query
            # #1436: real Intent shape (see calendar subcommand note).
            intent = Intent(
                category=IntentCategory.STATUS,
                action="get_project_status",
                confidence=1.0,
                original_message="what am I working on?",
            )

            # Call the canonical handler
            result = await handlers._handle_status_query(
                intent, session_id=f"slack_{user_id}", user_id=user_id
            )

            message = result.get("message", "I couldn't retrieve your project status.")

            return {
                "response_type": "ephemeral",
                "text": message,
            }

        except Exception as e:
            logger.error(f"Error handling status subcommand: {e}")
            return {
                "response_type": "ephemeral",
                "text": "I'm having trouble accessing your project status right now. Please try again later.",
            }

    async def _handle_priority_subcommand(self, user_id: str, channel_id: str) -> Dict[str, Any]:
        """
        Handle /piper priority subcommand.

        Issue #551 Phase 4: Priority parity on Slack.
        Routes to canonical priority handler for top priority item.
        """
        try:
            from services.domain.models import Intent
            from services.intent_service.canonical_handlers import CanonicalHandlers
            from services.shared_types import IntentCategory

            handlers = CanonicalHandlers()

            # Create a minimal intent for priority query
            # #1436: real Intent shape (see calendar subcommand note).
            intent = Intent(
                category=IntentCategory.PRIORITY,
                action="get_top_priority",
                confidence=1.0,
                original_message="what's my top priority?",
            )

            # Call the canonical handler
            result = await handlers._handle_priority_query(
                intent, session_id=f"slack_{user_id}", user_id=user_id
            )

            message = result.get("message", "I couldn't determine your top priority.")

            return {
                "response_type": "ephemeral",
                "text": message,
            }

        except Exception as e:
            logger.error(f"Error handling priority subcommand: {e}")
            return {
                "response_type": "ephemeral",
                "text": "I'm having trouble determining your priority right now. Please try again later.",
            }

    async def _build_help_response(self) -> Dict[str, Any]:
        """
        Build help response with dynamic capabilities.

        Issue #520: Query #50 - Uses _get_dynamic_capabilities() from canonical_handlers
        Issue #551: Now uses CommandRegistry for command list, falls back to capabilities
        """
        from services.commands.adapters.slack_adapter import SlackCommandAdapter
        from services.commands.definitions import register_all_commands
        from services.commands.registry import CommandRegistry
        from services.intent_service.canonical_handlers import CanonicalHandlers

        # Issue #551: Try to use CommandRegistry first
        if not CommandRegistry.is_initialized():
            register_all_commands()

        # Check if we have commands registered
        slack_commands = CommandRegistry.list_commands(interface=SlackCommandAdapter.interface)

        if slack_commands:
            # Use the new registry-based help
            return SlackCommandAdapter.build_help_response()

        # Fallback to original capability-based help if registry empty
        handlers = CanonicalHandlers()
        capabilities = handlers._get_dynamic_capabilities()

        # Format capabilities
        core = capabilities.get("core", [])
        integrations = capabilities.get("integrations", [])

        # Issue #628: Grammar-conscious help text
        help_text = "Hi! I'm Piper, your PM assistant. Here's how I can help:\n\n"

        help_text += "*Quick Commands*\n"
        help_text += "• `/standup` - I'll help you prep for standup\n"
        help_text += "• `/piper help` - Show this message\n\n"

        help_text += "*What I Can Do*\n"
        for cap in core:
            help_text += f"• {cap}\n"

        if integrations:
            help_text += "\n*I'm Connected To*\n"
            for integration in integrations:
                name = integration.get("name", "Unknown")
                help_text += f"• {name}\n"

        help_text += "\nJust ask me anything about your projects - I'm here to help!"

        return {
            "response_type": "ephemeral",
            "text": help_text,
        }

    async def _handle_standup_command(
        self, user_id: str, channel_id: str, team_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Handle /standup command.

        Issue #520: Query #49 - "/standup"

        Generates standup from:
        1. Completed items since yesterday
        2. High-priority todos for today
        3. Current blockers

        Issue #1429: Yesterday/Today are wired to the real todo services,
        scoped to the acting user's principal. When the Slack caller can't
        be resolved to a todo principal, the sections say so honestly instead
        of the affirmative-false "No completed items recorded" (we didn't
        look — say so).

        Issue #1466: resolution now consumes the slack_identities mapping
        (keyed by slack_user_id + team_id), and the unlinked copy carries the
        CXO §2 one-click deep link instead of prose alone.

        Args:
            user_id: Slack user ID
            channel_id: Slack channel ID
            team_id: Slack workspace/team ID (required for mapping resolution)

        Returns:
            In-channel response with standup format
        """
        try:
            standup_parts = []

            principal = await self._resolve_todo_principal(user_id, team_id)

            if principal is None:
                # #1429 honesty: no principal → we did NOT query anything.
                not_linked = (
                    "This Slack account isn't linked to a Piper user yet, "
                    "so I can't look up your todos"
                )
                standup_parts.append(f"*Yesterday:*\n• {not_linked}")
                standup_parts.append(f"\n*Today:*\n• {not_linked}")
                # #1466 (CXO §2/§3a): carry the link AS a link — a one-click
                # path to the settings link section with the caller's Slack
                # context as opaque params, so the code arrives pre-minted.
                from services.auth.slack_link_service import build_link_deep_url
                from services.integrations.slack import link_copy

                standup_parts.append(
                    "\n"
                    + link_copy.UNLINKED_DECLINE_LINK_LINE.format(
                        link_url=build_link_deep_url(user_id, team_id)
                    )
                )
            else:
                # 1. What I did yesterday (completed items)
                yesterday_items = await self._get_completed_since_yesterday(principal)
                standup_parts.append("*Yesterday:*")
                if yesterday_items is None:
                    # Lookup failed ≠ nothing completed (#1425 shape)
                    standup_parts.append(
                        "• I couldn't check completed items just now — try again shortly"
                    )
                elif yesterday_items:
                    for item in yesterday_items[:3]:
                        standup_parts.append(f"• {item}")
                else:
                    standup_parts.append("• No completed items recorded")

                # 2. What I'm doing today (high-priority todos)
                today_items = await self._get_today_priorities(principal)
                standup_parts.append("\n*Today:*")
                if today_items is None:
                    standup_parts.append(
                        "• I couldn't check today's priorities just now — try again shortly"
                    )
                elif today_items:
                    for item in today_items[:3]:
                        standup_parts.append(f"• {item}")
                else:
                    standup_parts.append("• No high-priority items scheduled")

            # 3. Blockers
            blockers = await self._get_blockers()
            standup_parts.append("\n*Blockers:*")
            if blockers:
                for blocker in blockers[:2]:
                    standup_parts.append(f"• {blocker}")
            else:
                standup_parts.append("• None")

            return {
                "response_type": "in_channel",  # Share with team
                "text": "\n".join(standup_parts),
            }

        except Exception as e:
            logger.error(f"Error generating standup: {e}")
            return {
                "response_type": "ephemeral",
                "text": "Unable to generate standup. Please try again.",
            }

    @staticmethod
    async def _resolve_todo_principal(
        user_id: Optional[str], team_id: Optional[str] = None
    ) -> Optional[UUID]:
        """
        Resolve the Slack caller to a todo-service principal.

        Issue #1429: the todo services key ownership by user UUID
        (``TodoDB.owner_id`` is a UUID FK to ``users.id``).

        Issue #1466: a raw Slack id now resolves through the slack_identities
        mapping, keyed by the FULL (slack_user_id, slack_team_id) pair. All
        misses fail CLOSED to None (honest not-linked copy) — never a default
        or cross-workspace owner:
        - no team_id → no mapping lookup (a bare U… id is ambiguous across
          workspaces);
        - no mapping row → None;
        - mapping lookup error → None.
        A user_id that already IS a Piper user UUID resolves directly
        (pre-#1466 behavior, still used by web-originating callers and tests).
        """
        if not user_id:
            return None
        try:
            return UUID(user_id)
        except (ValueError, AttributeError, TypeError):
            pass
        if not team_id:
            return None
        try:
            from services.auth.slack_link_service import resolve_slack_principal
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope_fresh() as session:
                return await resolve_slack_principal(session, user_id, team_id)
        except Exception as e:
            logger.warning(f"slack principal resolution failed (fail-closed to None): {e}")
            return None

    async def _handle_link_command(
        self, text: str, user_id: Optional[str], team_id: Optional[str]
    ) -> Dict[str, Any]:
        """
        Handle /link <code> — the redeem-in-Slack half of the #1466 linking
        handshake (code minted by the authenticated user in Piper settings;
        Slack never holds a Piper credential).

        All copy comes from link_copy (CXO-owned constants, never inline):
        - linked        → CXO §3b Slack-side confirmation (names the next action)
        - invalid_code  → honest miss + deep link to mint a fresh one
        - already_linked→ Arch condition 2 fail-closed copy (unlink-first path)
        - rate_limited  → Arch condition 1 fail-closed copy
        """
        from services.auth.slack_link_service import (
            ALREADY_LINKED,
            LINKED,
            RATE_LIMITED,
            build_link_deep_url,
            redeem_link_code,
        )
        from services.database.session_factory import AsyncSessionFactory
        from services.integrations.slack import link_copy

        link_url = build_link_deep_url(user_id, team_id)
        code = (text or "").strip()
        if not code:
            return {
                "response_type": "ephemeral",
                "text": link_copy.LINK_USAGE_PROMPT.format(link_url=link_url),
            }
        if not user_id or not team_id:
            # Cannot bind an identity we can't see — fail closed, honestly.
            return {
                "response_type": "ephemeral",
                "text": link_copy.INVALID_CODE_DECLINE.format(link_url=link_url),
            }

        try:
            async with AsyncSessionFactory.session_scope_fresh() as session:
                outcome = await redeem_link_code(session, code, user_id, team_id)
                piper_account = None
                if outcome.status == LINKED:
                    from services.database.models import User

                    piper_account = (
                        await session.execute(
                            select(User.username).where(User.id == outcome.owner_id)
                        )
                    ).scalar_one_or_none()
                # session_scope_fresh does NOT commit on clean exit; the
                # attempt-ledger row must persist on EVERY outcome (Arch
                # condition 1) and the mapping on LINKED.
                await session.commit()
        except Exception as e:
            logger.error(f"/link redemption failed: {e}")
            return {
                "response_type": "ephemeral",
                "text": link_copy.INVALID_CODE_DECLINE.format(link_url=link_url),
            }

        if outcome.status == LINKED:
            return {
                "response_type": "ephemeral",
                "text": link_copy.LINKED_CONFIRMATION_SLACK.format(
                    slack_handle=f"<@{user_id}>",
                    piper_account=f"`{piper_account}`" if piper_account else "your account",
                ),
            }
        if outcome.status == ALREADY_LINKED:
            return {"response_type": "ephemeral", "text": link_copy.ALREADY_LINKED_DECLINE}
        if outcome.status == RATE_LIMITED:
            return {"response_type": "ephemeral", "text": link_copy.RATE_LIMITED_DECLINE}
        return {
            "response_type": "ephemeral",
            "text": link_copy.INVALID_CODE_DECLINE.format(link_url=link_url),
        }

    async def _get_completed_since_yesterday(self, principal: UUID) -> Optional[list]:
        """
        Get the user's todos completed since the start of yesterday (UTC).

        Issue #520: Helper for /standup command.
        Issue #1429: wired to TodoManagementService (was a placeholder []).
        Returns None when the lookup fails — the caller renders honest
        "couldn't check" copy, never "No completed items recorded" (#1425).
        """
        try:
            from services.todo.todo_management_service import TodoManagementService

            todos = await TodoManagementService().list_todos(
                user_id=principal, include_completed=True
            )
            now = datetime.now(timezone.utc)
            cutoff = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            completed = []
            for todo in todos:
                if not getattr(todo, "completed", False):
                    continue
                completed_at = getattr(todo, "completed_at", None)
                if completed_at is None:
                    continue
                if completed_at.tzinfo is None:
                    completed_at = completed_at.replace(tzinfo=timezone.utc)
                if completed_at >= cutoff:
                    completed.append((completed_at, todo.text))
            completed.sort(key=lambda pair: pair[0], reverse=True)
            return [text for _, text in completed]
        except Exception as e:
            logger.warning(f"/standup completed-items lookup failed: {e}")
            return None

    async def _get_today_priorities(self, principal: UUID) -> Optional[list]:
        """
        Get the user's pending todos for today: urgent first, then high, then
        anything due today or overdue (whatever its priority).

        Issue #520: Helper for /standup command.
        Issue #1429: wired to TodoManagementService (was a placeholder []).
        Issue #1541: due-date awareness. This helper read ONLY urgent/high
        priority and never looked at due_date — so a todo created on the
        /todos page as "due today" (the page offers no priority field;
        everything it creates is medium) was invisible to /standup by
        construction, even though both surfaces share the same storage
        (TodoRepository → todo_items). Due-today/overdue items now render
        after the priority items, deduplicated.
        Returns None when the lookup fails — the caller renders honest
        "couldn't check" copy, never "No high-priority items scheduled".
        """
        try:
            from services.todo.todo_management_service import TodoManagementService

            todos = await TodoManagementService().list_todos(
                user_id=principal, include_completed=False
            )

            def _priority(todo) -> str:
                p = getattr(todo, "priority", "") or ""
                return (p.value if hasattr(p, "value") else str(p)).lower()

            end_of_today = datetime.now(timezone.utc).replace(
                hour=23, minute=59, second=59, microsecond=999999
            )

            def _due_today_or_overdue(todo) -> bool:
                due = getattr(todo, "due_date", None)
                if due is None:
                    return False
                if due.tzinfo is None:
                    due = due.replace(tzinfo=timezone.utc)
                return due <= end_of_today

            urgent = [t for t in todos if _priority(t) == "urgent"]
            high = [t for t in todos if _priority(t) == "high"]
            already = {id(t) for t in urgent + high}
            due = [t for t in todos if id(t) not in already and _due_today_or_overdue(t)]
            return [t.text for t in urgent + high + due]
        except Exception as e:
            logger.warning(f"/standup today-priorities lookup failed: {e}")
            return None

    async def _get_blockers(self) -> list:
        """
        Get current blockers — placeholder (always returns empty list).

        Issue #520: Helper for /standup command's "Blockers:" section.
        Issue #692 cleanup (2026-05-24): the prior
        ``TODO: Integrate with blocker detection when available`` was
        removed because no blocker-detection service exists in the
        codebase and none is planned in M2. The method intentionally
        returns ``[]`` so the /standup command's "Blockers:" section
        renders "None" — that's the current product behavior. If
        blocker detection becomes a real feature, file a new issue
        with proper scope; this method is the wire-up point.
        """
        return []
