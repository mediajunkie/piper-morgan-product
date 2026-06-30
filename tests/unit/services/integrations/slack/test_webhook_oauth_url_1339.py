"""#1339 — the webhook OAuth-URL path must thread the connector-owner's Piper user_id.

`SlackWebhookRouter._get_oauth_authorization_url` called `generate_authorization_url`
without a `user_id`, but that method REQUIRES one (it's embedded in the OAuth state,
#734/#759) — so the path would ValueError. The fix threads `_get_connector_user_id()`
(the connector OWNER, not the message sender's Slack id — #1110) and fails loudly +
clearly when it isn't configured.
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.slack.webhook_router import SlackWebhookRouter

pytestmark = pytest.mark.asyncio


def _router(oauth_handler):
    # Inject all deps so __init__ builds nothing heavy/real.
    return SlackWebhookRouter(
        config_service=MagicMock(),
        oauth_handler=oauth_handler,
        spatial_mapper=MagicMock(),
        integration_router=MagicMock(),
        response_handler=MagicMock(),
    )


async def test_threads_connector_owner_user_id_1339():
    oauth = MagicMock()
    oauth.generate_authorization_url = AsyncMock(
        return_value=("https://slack.com/oauth/v2/authorize?x=1", "state-xyz")
    )
    router = _router(oauth)

    with patch.dict("os.environ", {"SLACK_CONNECTOR_USER_ID": "owner-42"}, clear=True):
        resp = await router._get_oauth_authorization_url(scopes="chat:write")

    assert resp.status_code == 200
    # the connector-owner user_id must reach generate_authorization_url (#1339)
    _, kwargs = oauth.generate_authorization_url.call_args
    assert kwargs["user_id"] == "owner-42"


async def test_fails_clearly_when_connector_owner_unconfigured_1339():
    from fastapi import HTTPException

    oauth = MagicMock()
    oauth.generate_authorization_url = AsyncMock()
    router = _router(oauth)

    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(HTTPException) as exc:
            await router._get_oauth_authorization_url(scopes="chat:write")

    assert exc.value.status_code == 500
    assert "SLACK_CONNECTOR_USER_ID" in exc.value.detail
    # must NOT have attempted the call with a missing user_id (no ValueError path)
    oauth.generate_authorization_url.assert_not_awaited()
