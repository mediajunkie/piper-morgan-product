"""Tests for SlackDomainService.post_message (#1871).

Before this fix, ``services/integrations/mcp/skills/standup_workflow_skill.py``
called ``self.slack_service.post_message(...)`` on a ``SlackDomainService``
that had no such method — live, this raised ``AttributeError`` before any
message was sent. The unit tests mocked ``post_message`` on a class that
lacked it, so they certified the render but never the delivery (m-43:
probe-shape != live-shape).

These tests exercise the REAL method on the REAL class (no MagicMock
stand-in for ``post_message`` itself), patching only
``SlackIntegrationRouter.send_message`` — the actual outbound seam — so no
live Slack call is made.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.slack_domain_service import SlackDomainService
from services.integrations.slack.slack_client import SlackError, SlackErrorType, SlackResponse
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

SEND_MESSAGE_SEAM = (
    "services.integrations.slack.slack_integration_router.SlackIntegrationRouter.send_message"
)


def _make_service() -> SlackDomainService:
    """A real SlackDomainService, no MagicMock substitution."""
    return SlackDomainService()


class TestPostMessageExistsOnRealClass:
    def test_slack_domain_service_really_has_post_message(self):
        """m-43 guard: post_message must exist on the actual class, not just
        on a test double standing in for it."""
        service = _make_service()
        assert hasattr(service, "post_message")
        assert callable(service.post_message)
        # Not a MagicMock auto-attribute — a bound method of the real class.
        assert service.post_message.__func__ is SlackDomainService.post_message


class TestPostMessageDelegatesToIntegrationRouter:
    @pytest.mark.asyncio
    async def test_post_message_calls_router_send_message_with_threaded_args(self):
        """channel/text/user_id/blocks/thread_ts all reach the real send seam."""
        service = _make_service()
        fake_response = SlackResponse(success=True, data={"channel": "C123", "ts": "111.222"})

        with patch(SEND_MESSAGE_SEAM, new=AsyncMock(return_value=fake_response)) as mock_send:
            result = await service.post_message(
                channel="#standups",
                message="hello team",
                user_id="user-abc",
                blocks=[{"type": "section"}],
                thread_ts="999.111",
            )

        mock_send.assert_awaited_once()
        call_args, call_kwargs = mock_send.call_args
        assert call_args[0] == "#standups"  # channel
        assert call_args[1] == "hello team"  # text
        assert call_kwargs["user_id"] == "user-abc"
        assert call_kwargs["blocks"] == [{"type": "section"}]
        assert call_kwargs["thread_ts"] == "999.111"

        assert result == {"success": True, "channel": "C123", "ts": "111.222"}

    @pytest.mark.asyncio
    async def test_post_message_omits_blocks_and_thread_ts_when_not_given(self):
        """No fabricated kwargs reach the send seam when the caller passes none."""
        service = _make_service()
        fake_response = SlackResponse(success=True, data={"channel": "C1", "ts": "1.1"})

        with patch(SEND_MESSAGE_SEAM, new=AsyncMock(return_value=fake_response)) as mock_send:
            await service.post_message(channel="C1", message="hi", user_id="u1")

        _, call_kwargs = mock_send.call_args
        assert "blocks" not in call_kwargs
        assert "thread_ts" not in call_kwargs

    @pytest.mark.asyncio
    async def test_post_message_requires_user_id(self):
        """#1466/#1481: a Slack send must be scoped to the acting user, never
        the connector owner — no silent unscoped send."""
        service = _make_service()
        with patch(SEND_MESSAGE_SEAM, new=AsyncMock()) as mock_send:
            with pytest.raises(ValueError, match="user_id"):
                await service.post_message(channel="C1", message="hi", user_id="")
        mock_send.assert_not_awaited()


class TestPostMessageHonestFailureMapping:
    @pytest.mark.asyncio
    async def test_post_message_maps_api_failure_honestly(self):
        """A failed SlackResponse maps to success: False with the real reason —
        never a fabricated success."""
        service = _make_service()
        fake_response = SlackResponse(
            success=False,
            data={},
            error=SlackError(type=SlackErrorType.API_ERROR, message="channel_not_found"),
        )

        with patch(SEND_MESSAGE_SEAM, new=AsyncMock(return_value=fake_response)):
            result = await service.post_message(channel="C-missing", message="hi", user_id="u1")

        assert result["success"] is False
        assert "channel_not_found" in result["error"]

    @pytest.mark.asyncio
    async def test_post_message_maps_transport_exception_honestly(self):
        """A raised exception from the send seam is caught and reported, not
        swallowed into a fake success (no silent death)."""
        service = _make_service()

        with patch(SEND_MESSAGE_SEAM, new=AsyncMock(side_effect=RuntimeError("boom"))):
            result = await service.post_message(channel="C1", message="hi", user_id="u1")

        assert result == {"success": False, "error": "boom"}

    @pytest.mark.asyncio
    async def test_post_message_never_fabricates_ts_when_response_lacks_one(self):
        """If the Slack response doesn't carry a ts, the result says so
        honestly (None) rather than inventing one."""
        service = _make_service()
        fake_response = SlackResponse(success=True, data={"channel": "C1"})  # no "ts" key

        with patch(SEND_MESSAGE_SEAM, new=AsyncMock(return_value=fake_response)):
            result = await service.post_message(channel="C1", message="hi", user_id="u1")

        assert result["success"] is True
        assert result["ts"] is None


class TestPostMessageRouterCaching:
    @pytest.mark.asyncio
    async def test_integration_router_is_built_lazily_and_cached(self):
        """The SlackIntegrationRouter is built once, lazily, not at __init__
        (mirrors the router's own per-user SlackClient laziness, #1110)."""
        service = SlackDomainService()
        assert service._integration_router is None  # not built at construction

        with patch(
            SEND_MESSAGE_SEAM, new=AsyncMock(return_value=SlackResponse(success=True, data={}))
        ):
            await service.post_message(channel="C1", message="hi", user_id="u1")
            router_after_first_call = service._get_integration_router()
            assert isinstance(router_after_first_call, SlackIntegrationRouter)

            await service.post_message(channel="C1", message="hi again", user_id="u1")
            # Same router instance reused across calls.
            assert service._get_integration_router() is router_after_first_call
