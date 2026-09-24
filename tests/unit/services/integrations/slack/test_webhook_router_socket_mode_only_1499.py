"""#1499 Class 2 member strip — SlackWebhookRouter is Socket-Mode-only now.

Context: SlackWebhookRouter used to be a FastAPI router (self.router, an
APIRouter) with six HTTP route handlers wired up in __init__. The Oct 2025
CORE-GREAT-2D refactor removed the mount and #1129/#1496 rebuilt inbound on
Socket Mode, but the dead FastAPI surface (the APIRouter construction, route
registration, the six HTTP handlers, and — on closer inspection during this
strip — the entire Events-API event-processing pipeline underneath them,
which nothing ever called even before the mount was removed, since Socket
Mode's own event handling bypasses this class) stayed in the file.

This test pins two things:
1. The FastAPI surface is GONE — no self.router, no get_router(), no
   register_webhook_routes() — so it can't silently regrow without the
   member-strip discipline being re-run.
2. The Socket Mode call path
   (SlackSocketModeRunner._handle_slash_command -> SlackWebhookRouter()
   ._process_slash_command) still resolves and correctly handles a /piper
   payload, with the #1466 identity-binding seam
   (SlackWebhookRouter._resolve_todo_principal) patched so the test doesn't
   need a live DB.

See docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md
for the full member table and caller evidence this strip is based on.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.slack.socket_mode_runner import SlackSocketModeRunner
from services.integrations.slack.webhook_router import SlackWebhookRouter


class TestFastAPISurfaceRemoved:
    """The dead HTTP-webhook surface must not silently regrow."""

    def test_no_router_attribute(self):
        router = SlackWebhookRouter()
        assert not hasattr(router, "router"), (
            "SlackWebhookRouter grew a `router` (APIRouter) attribute again — "
            "the class is Socket-Mode-only (#1499 Class 2 member strip)"
        )

    def test_no_get_router_method(self):
        assert not hasattr(SlackWebhookRouter, "get_router"), (
            "get_router() was removed as dead (nothing ever mounted this router) "
            "— it must not come back without a live caller"
        )

    def test_no_route_registration_methods(self):
        for name in ("_register_routes", "register_webhook_routes", "get_webhook_urls"):
            assert not hasattr(
                SlackWebhookRouter, name
            ), f"{name} was removed as dead FastAPI-route-registration surface"

    def test_no_event_processing_pipeline(self):
        """The Events-API pipeline was reachable only from the unmounted HTTP
        route and the equally-unreached direct-testing method — never from
        Socket Mode, which handles events itself in SlackSocketModeRunner."""
        for name in (
            "handle_slack_events",
            "_handle_events_webhook",
            "_process_event_callback",
            "_process_event_callback_with_observability",
            "_process_message_event",
            "_process_mention_event",
            "_process_reaction_event",
            "_process_channel_join_event",
            "_process_interactive_component",
            "_verify_slack_signature",
            "_compute_and_verify_signature",
        ):
            assert not hasattr(SlackWebhookRouter, name), f"{name} should have been stripped"

    def test_live_slash_command_surface_intact(self):
        """The methods Socket Mode actually calls must still be there."""
        for name in (
            "_process_slash_command",
            "_handle_piper_command",
            "_handle_standup_command",
            "_handle_link_command",
            "_resolve_todo_principal",
        ):
            assert hasattr(SlackWebhookRouter, name), f"{name} is on the live path — must remain"


def _runner() -> SlackSocketModeRunner:
    return SlackSocketModeRunner(
        intent_service=MagicMock(),
        app_token="xapp-test",
        bot_token="xoxb-test",
        bound_user_id="user-1",
    )


class TestSocketModeSlashCommandPathStillResolves:
    """The live call path: Socket Mode envelope -> SlackWebhookRouter()._process_slash_command."""

    @pytest.mark.asyncio
    async def test_piper_help_over_socket_mode(self):
        """A /piper help payload arriving over Socket Mode gets a real answer,
        going through the actual (unmocked) SlackWebhookRouter — no HTTP,
        no APIRouter, just the class Socket Mode instantiates directly."""
        runner = _runner()
        payload = {
            "command": "/piper",
            "text": "help",
            "user_id": "U123",
            "team_id": "T123",
            "channel_id": "C123",
            "response_url": "https://hooks.slack.com/commands/T123/respond",
        }
        webhook = MagicMock()
        webhook.send_dict = AsyncMock()
        with patch(
            "slack_sdk.webhook.async_client.AsyncWebhookClient",
            return_value=webhook,
        ):
            await runner._handle_slash_command(payload)

        # The real SlackWebhookRouter processed it and posted a real reply.
        webhook.send_dict.assert_awaited_once()
        (sent,), _ = webhook.send_dict.call_args
        assert sent["response_type"] == "ephemeral"
        assert "help" in sent["text"].lower() or "piper" in sent["text"].lower()

    @pytest.mark.asyncio
    async def test_standup_over_socket_mode_with_unlinked_identity(self):
        """#1466 seam: an unresolved principal must not crash the live path —
        _resolve_todo_principal is the sanctioned identity-binding surface,
        patched here to the honest "not linked" outcome rather than hitting a
        real DB."""
        runner = _runner()
        payload = {
            "command": "/standup",
            "text": "",
            "user_id": "U999",
            "team_id": "T999",
            "channel_id": "C999",
            "response_url": "https://hooks.slack.com/commands/T999/respond",
        }
        webhook = MagicMock()
        webhook.send_dict = AsyncMock()
        with (
            patch.object(
                SlackWebhookRouter, "_resolve_todo_principal", AsyncMock(return_value=None)
            ),
            patch(
                "slack_sdk.webhook.async_client.AsyncWebhookClient",
                return_value=webhook,
            ),
        ):
            await runner._handle_slash_command(payload)

        webhook.send_dict.assert_awaited_once()
        (sent,), _ = webhook.send_dict.call_args
        assert sent["response_type"] == "in_channel"
        assert "isn't linked" in sent["text"]
