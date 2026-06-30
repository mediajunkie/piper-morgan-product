"""#1338 — Slack user-token request path + search.messages on the router.

Covers the four layers: config loads the user token, the client's _make_request
selects bot-vs-user token and honest-degrades when the user token is absent, the
client/router expose search_messages + test_auth(use_user_token=), so the mentions
aggregator can drop its direct-aiohttp workaround (#1085 slice 3).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.slack.config_service import SlackConfig
from services.integrations.slack.slack_client import (
    SlackClient,
    SlackErrorType,
    SlackResponse,
)
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter

pytestmark = pytest.mark.asyncio

_USER = "owner-1"


def _client(config: SlackConfig) -> SlackClient:
    cfg_service = MagicMock()
    cfg_service.get_config.return_value = config
    return SlackClient(config_service=cfg_service, user_id=_USER)


# ---- Layer 1: config ----

async def test_config_loads_user_token_from_keychain_1338():
    from services.integrations.slack.config_service import SlackConfigService

    keychain = MagicMock()
    # bot vs user keychain keys resolve distinctly
    keychain.get_api_key.side_effect = lambda provider, username=None: {
        "slack_bot": "xoxb-bot",
        "slack_user": "xoxp-user",
    }.get(provider, "")

    with (
        patch.dict("os.environ", {}, clear=True),
        patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=keychain,
        ),
    ):
        cfg = SlackConfigService().get_config(user_id=_USER)

    assert cfg.user_token == "xoxp-user"
    assert cfg.bot_token == "xoxb-bot"


# ---- Layer 2: client ----

async def test_make_request_honest_degrades_without_user_token_1338():
    client = _client(SlackConfig(bot_token="xoxb-bot", user_token=""))
    client._ensure_session = AsyncMock()
    client._check_rate_limit = AsyncMock()
    client._session = MagicMock()  # must NOT be used

    resp = await client._make_request("GET", "search.messages", use_user_token=True)

    assert resp.success is False
    assert resp.error.type == SlackErrorType.AUTHENTICATION_ERROR
    client._session.request.assert_not_called()  # no call with an empty bearer


async def test_search_messages_uses_user_token_and_params_1338():
    client = _client(SlackConfig(bot_token="b", user_token="xoxp-user"))
    client._make_request = AsyncMock(return_value=SlackResponse(success=True, data={}))

    await client.search_messages("@me", count=20)

    _, kwargs = client._make_request.call_args
    assert kwargs["use_user_token"] is True
    assert kwargs["params"]["query"] == "@me"
    args, _ = client._make_request.call_args
    assert args[1] == "search.messages"


async def test_test_auth_threads_use_user_token_1338():
    client = _client(SlackConfig(bot_token="b", user_token="u"))
    client._make_request = AsyncMock(return_value=SlackResponse(success=False, data={}))

    await client.test_auth(use_user_token=True)

    _, kwargs = client._make_request.call_args
    assert kwargs["use_user_token"] is True


# ---- Layer 3: router ----

async def test_router_search_messages_delegates_1338():
    router = SlackIntegrationRouter(config_service=MagicMock())
    mock_client = MagicMock()
    mock_client.search_messages = AsyncMock(
        return_value=SlackResponse(success=True, data={})
    )
    router._ensure_config_service = MagicMock()
    router._get_preferred_integration = MagicMock(return_value=(mock_client, False))

    await router.search_messages("@me", user_id=_USER, count=5)

    args, kwargs = mock_client.search_messages.call_args
    assert args[0] == "@me"
    assert kwargs["count"] == 5


async def test_router_test_auth_passes_use_user_token_1338():
    router = SlackIntegrationRouter(config_service=MagicMock())
    mock_client = MagicMock()
    mock_client.test_auth = AsyncMock(return_value=SlackResponse(success=True, data={}))
    router._ensure_config_service = MagicMock()
    router._get_preferred_integration = MagicMock(return_value=(mock_client, False))

    await router.test_auth(user_id=_USER, use_user_token=True)

    _, kwargs = mock_client.test_auth.call_args
    assert kwargs["use_user_token"] is True


# ---- Layer 4: assembler migration ----

async def test_mentions_aggregator_uses_router_1338():
    from services.intent_service.context_assembler import ContextAssembler

    mock_router = MagicMock()
    mock_router.test_auth = AsyncMock(
        return_value=SlackResponse(success=True, data={"user": "alice"})
    )
    mock_router.search_messages = AsyncMock(
        return_value=SlackResponse(
            success=True,
            data={
                "messages": {
                    "matches": [
                        {
                            "ts": "9999999999.0",  # far-future ts → within window
                            "text": "hey @alice ping",
                            "channel": {"id": "C1"},
                            "user": "bob",
                            "permalink": "http://x",
                        }
                    ]
                }
            },
        )
    )

    with (
        patch(
            "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
            return_value=mock_router,
        ),
        patch("services.integrations.slack.config_service.SlackConfigService"),
    ):
        items = await ContextAssembler()._fetch_slack_mentions_items(_USER)

    mock_router.test_auth.assert_awaited_once()
    _, akwargs = mock_router.test_auth.call_args
    assert akwargs["use_user_token"] is True
    assert len(items) == 1
    assert items[0]["channel_type"] == "mention"
    assert items[0]["channel"] == "C1"


async def test_mentions_aggregator_honest_degrades_to_empty_1338():
    from services.intent_service.context_assembler import ContextAssembler

    mock_router = MagicMock()
    mock_router.test_auth = AsyncMock(
        return_value=SlackResponse(success=False, data={})  # no user token / auth fail
    )
    mock_router.search_messages = AsyncMock()

    with (
        patch(
            "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
            return_value=mock_router,
        ),
        patch("services.integrations.slack.config_service.SlackConfigService"),
    ):
        items = await ContextAssembler()._fetch_slack_mentions_items(_USER)

    assert items == []
    mock_router.search_messages.assert_not_awaited()  # never reaches search on auth-fail
