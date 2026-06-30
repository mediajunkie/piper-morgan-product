"""
Tests for SlackClient multi-tenancy user_id threading (#1110, RECONNECT WS-7).

`SlackConfigService.get_config(user_id)` REQUIRES user_id (ADR-058 / #734). The
latent bug: SlackClient called get_config() with no user_id at 3 sites
(_ensure_session, _check_rate_limit, _make_request) and __init__ stored no user_id,
which would TypeError. These tests pin the fix:

1. SlackClient.__init__ stores user_id and REQUIRES it (guardrail: a client that
   can't call get_config is useless; never accept None/empty).
2. All 3 internal get_config call-sites pass the stored user_id.
3. SlackIntegrationRouter lazily builds a per-operation SlackClient with the
   operation's user_id (the router is a startup singleton, so user_id is
   per-operation, not per-construction).
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.integrations.slack.config_service import SlackConfig
from services.integrations.slack.slack_client import SlackClient

TEST_USER_ID = "u1"


def _mock_config_service(user_id_holder: dict) -> MagicMock:
    """A config_service whose get_config records the user_id it was called with
    and returns a usable SlackConfig."""
    svc = MagicMock()

    def _get_config(user_id):
        user_id_holder["user_id"] = user_id
        return SlackConfig(bot_token="xoxb-test", requests_per_minute=50, timeout_seconds=30)

    svc.get_config.side_effect = _get_config
    return svc


class TestSlackClientInitRequiresUserId:
    """__init__ guardrail: user_id is required and stored."""

    def test_init_stores_user_id(self):
        client = SlackClient(config_service=MagicMock(), user_id=TEST_USER_ID)
        assert client.user_id == TEST_USER_ID

    def test_init_without_user_id_raises(self):
        # Positional/kw omission must not silently recreate the latent bug.
        with pytest.raises((TypeError, ValueError)):
            SlackClient(config_service=MagicMock())

    def test_init_empty_user_id_raises(self):
        with pytest.raises(ValueError):
            SlackClient(config_service=MagicMock(), user_id="")

    def test_init_none_user_id_raises(self):
        with pytest.raises(ValueError):
            SlackClient(config_service=MagicMock(), user_id=None)


class TestGetConfigCallSitesThreadUserId:
    """The 3 internal call-sites must pass the stored user_id to get_config."""

    async def test_ensure_session_passes_user_id(self):
        holder: dict = {}
        svc = _mock_config_service(holder)
        client = SlackClient(config_service=svc, user_id=TEST_USER_ID)

        await client._ensure_session()
        try:
            svc.get_config.assert_called_with(TEST_USER_ID)
            assert holder["user_id"] == TEST_USER_ID
        finally:
            await client._close_session()

    async def test_check_rate_limit_passes_user_id(self):
        holder: dict = {}
        svc = _mock_config_service(holder)
        client = SlackClient(config_service=svc, user_id=TEST_USER_ID)

        await client._check_rate_limit()
        svc.get_config.assert_called_with(TEST_USER_ID)
        assert holder["user_id"] == TEST_USER_ID

    async def test_make_request_passes_user_id(self):
        holder: dict = {}
        svc = _mock_config_service(holder)
        client = SlackClient(config_service=svc, user_id=TEST_USER_ID)

        # Stub the session so _make_request never hits the network; we only care
        # that get_config was threaded the user_id before the request is built.
        class _FakeResp:
            status = 200
            ok = True
            headers: dict = {}

            async def json(self):
                return {"ok": True}

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

        fake_session = MagicMock()
        fake_session.closed = False
        fake_session.request = MagicMock(return_value=_FakeResp())
        client._session = fake_session

        await client._make_request("GET", "auth.test")
        svc.get_config.assert_called_with(TEST_USER_ID)
        assert holder["user_id"] == TEST_USER_ID


class TestRouterLazyPerOperationClient:
    """The router is a startup singleton; it must build the SlackClient lazily
    per operation with the operation's user_id (not at __init__)."""

    async def test_send_message_threads_user_id_to_get_config(self):
        from services.integrations.slack.slack_integration_router import (
            SlackIntegrationRouter,
        )

        holder: dict = {}
        svc = _mock_config_service(holder)
        router = SlackIntegrationRouter(config_service=svc)

        # No client should be built eagerly at construction time (lazy).
        assert getattr(router, "spatial_client", None) is None
        assert getattr(router, "legacy_client", None) is None

        await router.send_message("C1", "hello", user_id=TEST_USER_ID)

        # The lazily-built client must have asked get_config for THIS user.
        assert holder.get("user_id") == TEST_USER_ID
