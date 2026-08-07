"""#1496: Socket Mode slash-command transport.

The defect: the HTTP mount for SlackWebhookRouter was removed in Oct 2025, and
the #1129 Socket Mode rebuild dispatched only ``events_api`` — so /link (#1466),
/standup and /piper were acked-and-dropped: tested handlers, no live transport.
Every prior test called _process_slash_command directly, which is exactly how
the gap stayed invisible. These tests pin the TRANSPORT: a slash_commands
envelope must reach _process_slash_command and the reply must go to
response_url.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.slack.socket_mode_runner import SlackSocketModeRunner


def _runner() -> SlackSocketModeRunner:
    return SlackSocketModeRunner(
        intent_service=MagicMock(),
        app_token="xapp-test",
        bot_token="xoxb-test",
        bound_user_id="user-1",
    )


def _req(req_type: str, payload: dict):
    req = MagicMock()
    req.type = req_type
    req.payload = payload
    req.envelope_id = "env-1"
    return req


SLASH_PAYLOAD = {
    "command": "/link",
    "text": "ABC123",
    "user_id": "U123",
    "team_id": "T123",
    "channel_id": "C123",
    "response_url": "https://hooks.slack.com/commands/T123/respond",
}


class TestSlashEnvelopeDispatch:
    """The listener-level routing: slash_commands is no longer dropped."""

    @pytest.mark.asyncio
    async def test_slash_envelope_is_acked_and_dispatched(self):
        runner = _runner()
        client = MagicMock()
        client.send_socket_mode_response = AsyncMock()
        with patch.object(runner, "_handle_slash_command", new=AsyncMock()) as handle:
            await runner._on_socket_request(client, _req("slash_commands", SLASH_PAYLOAD))
            # ack went back (Slack retries unacked envelopes)
            client.send_socket_mode_response.assert_awaited_once()
            # and the payload was dispatched to the slash path (create_task
            # schedules it; let the loop run it)
            import asyncio

            await asyncio.sleep(0)
            handle.assert_awaited_once_with(SLASH_PAYLOAD)

    @pytest.mark.asyncio
    async def test_events_api_still_dispatches_events(self):
        """Regression pin: extracting the closure must not break the DM path."""
        runner = _runner()
        client = MagicMock()
        client.send_socket_mode_response = AsyncMock()
        event = {"type": "message", "channel_type": "im", "text": "hi"}
        with patch.object(runner, "_handle_event", new=AsyncMock()) as handle:
            await runner._on_socket_request(client, _req("events_api", {"event": event}))
            import asyncio

            await asyncio.sleep(0)
            handle.assert_awaited_once_with(event)

    @pytest.mark.asyncio
    async def test_other_envelope_types_ack_and_drop(self):
        runner = _runner()
        client = MagicMock()
        client.send_socket_mode_response = AsyncMock()
        with (
            patch.object(runner, "_handle_slash_command", new=AsyncMock()) as slash,
            patch.object(runner, "_handle_event", new=AsyncMock()) as event,
        ):
            await runner._on_socket_request(client, _req("interactive", {"x": 1}))
            client.send_socket_mode_response.assert_awaited_once()
            slash.assert_not_awaited()
            event.assert_not_awaited()


class TestSlashCommandHandling:
    """The handler half: payload → _process_slash_command → response_url."""

    @pytest.mark.asyncio
    async def test_payload_routed_and_reply_sent_to_response_url(self):
        runner = _runner()
        router = MagicMock()
        router._process_slash_command = AsyncMock(
            return_value={"response_type": "ephemeral", "text": "linked!"}
        )
        webhook = MagicMock()
        webhook.send_dict = AsyncMock()
        with (
            patch(
                "services.integrations.slack.webhook_router.SlackWebhookRouter",
                return_value=router,
            ),
            patch(
                "slack_sdk.webhook.async_client.AsyncWebhookClient",
                return_value=webhook,
            ) as webhook_cls,
        ):
            await runner._handle_slash_command(SLASH_PAYLOAD)
            # the socket payload reaches the SAME tested processor, unchanged
            router._process_slash_command.assert_awaited_once_with(SLASH_PAYLOAD)
            webhook_cls.assert_called_once_with(SLASH_PAYLOAD["response_url"])
            webhook.send_dict.assert_awaited_once_with(
                {"response_type": "ephemeral", "text": "linked!"}
            )

    @pytest.mark.asyncio
    async def test_router_built_once_and_reused(self):
        runner = _runner()
        router = MagicMock()
        router._process_slash_command = AsyncMock(return_value=None)
        with patch(
            "services.integrations.slack.webhook_router.SlackWebhookRouter",
            return_value=router,
        ) as router_cls:
            await runner._handle_slash_command(dict(SLASH_PAYLOAD, response_url=""))
            await runner._handle_slash_command(dict(SLASH_PAYLOAD, response_url=""))
            router_cls.assert_called_once()  # lazy singleton, not per-command
            assert router._process_slash_command.await_count == 2

    @pytest.mark.asyncio
    async def test_handler_exception_is_contained(self):
        """A slash failure must never escape into the socket loop."""
        runner = _runner()
        with patch(
            "services.integrations.slack.webhook_router.SlackWebhookRouter",
            side_effect=RuntimeError("boom"),
        ):
            await runner._handle_slash_command(SLASH_PAYLOAD)  # must not raise
