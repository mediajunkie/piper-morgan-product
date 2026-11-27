"""#1317 inc.2 slice A — GitHubOAuthHandler (option C: plain GitHub OAuth App flow).

Security-critical, network-free behaviors (state CSRF + user-binding + single-use, #734)
are tested directly; the code-exchange is tested with a mocked aiohttp session (GitHub's
200-with-error-field quirk included). No real network, no real credentials.
"""

from contextlib import asynccontextmanager
from unittest.mock import patch

import pytest

from services.mcp.consumer import github_oauth_handler as gh_oauth
from services.mcp.consumer.github_oauth_handler import GitHubOAuthHandler
from tests.unit.services.integrations.slack.test_oauth_redis_state_1109 import _FakeRedis

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"


@pytest.fixture(autouse=True)
def _state_redis():
    """#2345: the pending state lives in Redis; Slack's in-memory fake stands in."""
    fake = _FakeRedis()

    @asynccontextmanager
    async def _scope():
        yield fake

    with patch("services.cache.redis_factory.RedisFactory.redis_scope", side_effect=_scope):
        yield fake


@pytest.fixture(autouse=True)
def _creds(monkeypatch):
    monkeypatch.setenv("GITHUB_OAUTH_CLIENT_ID", "cid")
    monkeypatch.setenv("GITHUB_OAUTH_CLIENT_SECRET", "sec")


@pytest.fixture
def app_on(monkeypatch):
    """Issue 2261: a connect (state, exchange, callback) runs only in GitHub App mode."""
    monkeypatch.setenv("GITHUB_APP_CLIENT_ID", "test-app-client-id")
    monkeypatch.setenv("GITHUB_APP_CLIENT_SECRET", "test-app-client-secret")


# ── mocked aiohttp session (session → post/get → response, all async CMs) ──
class _FakeResp:
    def __init__(self, status, payload):
        self.status, self._payload = status, payload

    async def json(self):
        return self._payload

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class _FakeSession:
    def __init__(self, resp):
        self._resp = resp

    def post(self, *a, **k):
        return self._resp

    def get(self, *a, **k):
        return self._resp

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class TestAuthorizationUrl:
    async def test_classic_client_makes_no_url(self):
        # Issue 2261: was test_url_has_required_params, which pinned scope=repo on the
        # classic OAuth App's URL. With only the classic client configured (this file's
        # _creds fixture) there is no URL now: the named refusal.
        from services.mcp.consumer.github_oauth_handler import GitHubConnectNotConfigured

        with pytest.raises(GitHubConnectNotConfigured):
            await GitHubOAuthHandler().generate_authorization_url(_ALPHA)

    @pytest.mark.usefixtures("app_on")
    async def test_state_round_trips_user_id(self):
        h = GitHubOAuthHandler()
        _, state = await h.generate_authorization_url(_ALPHA)
        ok, uid = await h.verify_state(state)
        assert ok and uid == _ALPHA

    @pytest.mark.usefixtures("app_on")
    async def test_missing_user_id_raises(self):
        with pytest.raises(ValueError):
            await GitHubOAuthHandler().generate_authorization_url("")


@pytest.mark.usefixtures("app_on")
class TestStateVerification:
    async def test_tampered_state_rejected(self):
        h = GitHubOAuthHandler()
        _, state = await h.generate_authorization_url(_ALPHA)
        assert (await h.verify_state(state + "tamper"))[0] is False

    async def test_unknown_state_rejected(self):
        assert (await GitHubOAuthHandler().verify_state("bogus"))[0] is False

    async def test_state_is_single_use(self):
        h = GitHubOAuthHandler()
        _, state = await h.generate_authorization_url(_ALPHA)
        assert (await h.verify_state(state))[0] is True
        assert (await h.verify_state(state))[0] is False  # consumed


@pytest.mark.usefixtures("app_on")
class TestCodeExchange:
    async def test_exchange_parses_github_token(self, monkeypatch):
        monkeypatch.setattr(
            gh_oauth.aiohttp,
            "ClientSession",
            lambda *a, **k: _FakeSession(
                _FakeResp(200, {"access_token": "gho_x", "token_type": "bearer", "scope": "repo"})
            ),
        )
        tokens = await GitHubOAuthHandler()._exchange_code_for_tokens("code123")
        assert tokens.access_token == "gho_x"
        assert tokens.scope == "repo"
        assert tokens.refresh_token is None  # classic OAuth-App token: no refresh

    async def test_exchange_github_error_raises(self, monkeypatch):
        # GitHub returns HTTP 200 with an error field on a bad code.
        monkeypatch.setattr(
            gh_oauth.aiohttp,
            "ClientSession",
            lambda *a, **k: _FakeSession(_FakeResp(200, {"error": "bad_verification_code"})),
        )
        with pytest.raises(ValueError):
            await GitHubOAuthHandler()._exchange_code_for_tokens("bad")

    async def test_callback_rejects_bad_state(self):
        with pytest.raises(ValueError):
            await GitHubOAuthHandler().handle_oauth_callback(
                "code", "bogus-state", session_user_id="u1"
            )
