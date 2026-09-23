"""#1499 Class 1.1 — `/slack/authorize` and `/slack/connect` must be ONE implementation.

The audit's headline finding: Slack OAuth *initiation* existed in four places, two of
them live on this router, reached by two different buttons in two different templates:

  - `templates/integrations.html`  → generic `${integrationName}/connect`
  - `templates/settings_slack.html` → the "Add to Slack" button, `/slack/authorize`

They drifted. `/slack/authorize` never received #1324's redirect-URI fallback chain, so
with no `SLACK_REDIRECT_URI` set it handed Slack an EMPTY redirect_uri — found live in
PM's 2026-08-07 walkthrough and patched same-day by COPYING the chain across. Two copies
of a fix is the defect this test exists to prevent recurring: the next fix must not be
able to land one route away again.

LAYER (m-43): route, real `TestClient` through the real router + real dependency graph —
the same HTTP surface the two buttons hit. Not a source grep, not a direct function call.
DENOMINATOR: the two live OAuth-initiation routes on `settings_integrations.router`
(`/slack/connect`, `/slack/authorize`). The other two initiation sites named by the audit
are out of this test's scope: `setup.py:1241` is the wizard's own flow (already fixed
2026-08-07) and `webhook_router.py:184` sits on an unmounted router (#1499 Class 2,
disposal pending an Arch ruling).

Both paths stay ROUTABLE on purpose — deleting either one breaks a shipped button — but
only one of them computes anything.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import get_current_user
from web.api.routes.settings_integrations import router as settings_integrations_router

CONNECT_PATH = "/api/v1/settings/integrations/slack/connect"
AUTHORIZE_PATH = "/api/v1/settings/integrations/slack/authorize"

_AUTH_URL = "https://slack.com/oauth/v2/authorize?client_id=test&state=abc"
_STATE = "state-token-1499"


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(settings_integrations_router)

    claims = MagicMock()
    claims.sub = "user-1499"
    app.dependency_overrides[get_current_user] = lambda: claims

    return TestClient(app)


@pytest.fixture
def slack_handler():
    """A recording stand-in for SlackOAuthHandler, patched where both routes import it."""
    handler = MagicMock()
    handler.generate_authorization_url = AsyncMock(return_value=(_AUTH_URL, _STATE))
    with patch(
        "services.integrations.slack.oauth_handler.SlackOAuthHandler",
        return_value=handler,
    ):
        yield handler


class TestSlackOAuthInitiationIsOneImplementation:
    def test_both_routes_produce_the_same_redirect_target(self, slack_handler, monkeypatch):
        """Same user, same env → the browser is sent to the SAME Slack URL either way.

        This is the user-visible invariant: the "Add to Slack" button and the generic
        Connect button start the identical OAuth flow.
        """
        monkeypatch.delenv("SLACK_SETTINGS_REDIRECT_URI", raising=False)
        monkeypatch.delenv("SLACK_REDIRECT_URI", raising=False)
        client = _client()

        connect = client.get(CONNECT_PATH).json()
        authorize = client.get(AUTHORIZE_PATH).json()

        # The two routes keep their (different, shipped) response SHAPES — the callers
        # read different field names — but the target and state must be identical.
        assert connect["auth_url"] == authorize["authorization_url"] == _AUTH_URL
        assert connect["state"] == authorize["state"] == _STATE

    def test_both_routes_pass_identical_arguments_to_the_oauth_handler(
        self, slack_handler, monkeypatch
    ):
        """The #1324 defect lived in the ARGUMENTS, not the response — pin those."""
        monkeypatch.delenv("SLACK_SETTINGS_REDIRECT_URI", raising=False)
        monkeypatch.delenv("SLACK_REDIRECT_URI", raising=False)
        client = _client()

        client.get(CONNECT_PATH)
        client.get(AUTHORIZE_PATH)

        calls = slack_handler.generate_authorization_url.await_args_list
        assert len(calls) == 2
        assert calls[0] == calls[1], "the two routes diverged in what they ask Slack for"

    def test_authorize_carries_the_1324_redirect_uri_fallback(self, slack_handler, monkeypatch):
        """With NO redirect env set, the fallback must be a real URL, never empty.

        The live bug (2026-08-07): Slack's consent screen showed a blank "Passed URI:".
        """
        monkeypatch.delenv("SLACK_SETTINGS_REDIRECT_URI", raising=False)
        monkeypatch.delenv("SLACK_REDIRECT_URI", raising=False)
        monkeypatch.setenv("PIPER_BASE_URL", "https://piper.example")

        _client().get(AUTHORIZE_PATH)

        kwargs = slack_handler.generate_authorization_url.await_args.kwargs
        assert kwargs["user_id"] == "user-1499"
        assert (
            kwargs["redirect_uri"]
            == "https://piper.example/api/v1/settings/integrations/slack/callback"
        )

    def test_env_override_reaches_both_routes(self, slack_handler, monkeypatch):
        """The fallback CHAIN, not just its last link — an override must win on both."""
        monkeypatch.setenv("SLACK_SETTINGS_REDIRECT_URI", "https://override.example/cb")
        client = _client()

        client.get(CONNECT_PATH)
        client.get(AUTHORIZE_PATH)

        for call in slack_handler.generate_authorization_url.await_args_list:
            assert call.kwargs["redirect_uri"] == "https://override.example/cb"

    def test_both_paths_remain_routable(self):
        """Collapsing must not un-ship either button: both paths still exist."""
        paths = {r.path for r in settings_integrations_router.routes}
        assert CONNECT_PATH in paths
        assert AUTHORIZE_PATH in paths

    def test_only_one_route_computes_the_redirect_uri(self):
        """The structural half of the fix (m-43: source, deliberately).

        The behavioral tests above would pass with two copies that happen to agree
        TODAY. This one pins that there is only one copy to keep in agreement — which
        is the actual thing #1499 asked for.
        """
        import inspect

        from web.api.routes.settings_integrations import get_slack_oauth_url

        body = inspect.getsource(get_slack_oauth_url)
        assert "SLACK_SETTINGS_REDIRECT_URI" not in body, (
            "/slack/authorize grew its own copy of the #1324 fallback chain again — "
            "it must delegate to connect_slack (#1499)"
        )
        assert "connect_slack" in body
