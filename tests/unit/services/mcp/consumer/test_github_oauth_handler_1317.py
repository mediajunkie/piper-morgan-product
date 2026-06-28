"""#1317 inc.2 slice A — GitHubOAuthHandler (option C: plain GitHub OAuth App flow).

Security-critical, network-free behaviors (state CSRF + user-binding + single-use, #734)
are tested directly; the code-exchange is tested with a mocked aiohttp session (GitHub's
200-with-error-field quirk included). No real network, no real credentials.
"""

import pytest

from services.mcp.consumer import github_oauth_handler as gh_oauth
from services.mcp.consumer.github_oauth_handler import GitHubOAuthHandler

_ALPHA = "11111111-1111-1111-1111-111111111111"
_BETA = "22222222-2222-2222-2222-222222222222"


@pytest.fixture(autouse=True)
def _creds(monkeypatch):
    monkeypatch.setenv("GITHUB_OAUTH_CLIENT_ID", "cid")
    monkeypatch.setenv("GITHUB_OAUTH_CLIENT_SECRET", "sec")


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
    def test_url_has_required_params(self):
        url, state = GitHubOAuthHandler().generate_authorization_url(_ALPHA)
        assert url.startswith("https://github.com/login/oauth/authorize?")
        assert "client_id=cid" in url
        assert "scope=repo" in url
        assert f"state={state[:8]}" in url or "state=" in url

    def test_state_round_trips_user_id(self):
        h = GitHubOAuthHandler()
        _, state = h.generate_authorization_url(_ALPHA)
        ok, uid = h.verify_state(state)
        assert ok and uid == _ALPHA

    def test_missing_user_id_raises(self):
        with pytest.raises(ValueError):
            GitHubOAuthHandler().generate_authorization_url("")


class TestStateVerification:
    def test_tampered_state_rejected(self):
        h = GitHubOAuthHandler()
        _, state = h.generate_authorization_url(_ALPHA)
        assert h.verify_state(state + "tamper")[0] is False

    def test_unknown_state_rejected(self):
        assert GitHubOAuthHandler().verify_state("bogus")[0] is False

    def test_state_is_single_use(self):
        h = GitHubOAuthHandler()
        _, state = h.generate_authorization_url(_ALPHA)
        assert h.verify_state(state)[0] is True
        assert h.verify_state(state)[0] is False  # consumed


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
            await GitHubOAuthHandler().handle_oauth_callback("code", "bogus-state")
