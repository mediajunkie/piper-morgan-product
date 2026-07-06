"""#542 — GoogleCalendarOAuthHandler.revoke_token(): real Google-side revocation on
disconnect (previously local-clear only, never actually revoked). Mocked aiohttp
session, no real network -- same pattern as test_github_oauth_handler_1317.py.
"""

import pytest

from services.integrations.calendar import oauth_handler as cal_oauth
from services.integrations.calendar.oauth_handler import GoogleCalendarOAuthHandler


class _FakeResp:
    def __init__(self, status):
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class _FakeSession:
    def __init__(self, resp):
        self._resp = resp

    def post(self, *a, **k):
        return self._resp

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class TestRevokeToken:
    async def test_revoke_success_returns_true(self, monkeypatch):
        monkeypatch.setattr(
            cal_oauth.aiohttp, "ClientSession", lambda *a, **k: _FakeSession(_FakeResp(200))
        )
        result = await GoogleCalendarOAuthHandler().revoke_token("a-real-refresh-token")
        assert result is True

    async def test_revoke_http_failure_returns_false_not_raises(self, monkeypatch):
        # Google returns 400 for an already-invalid/expired token -- must not raise.
        monkeypatch.setattr(
            cal_oauth.aiohttp, "ClientSession", lambda *a, **k: _FakeSession(_FakeResp(400))
        )
        result = await GoogleCalendarOAuthHandler().revoke_token("stale-token")
        assert result is False

    async def test_revoke_network_error_returns_false_not_raises(self, monkeypatch):
        def _raise(*a, **k):
            raise ConnectionError("network down")

        monkeypatch.setattr(cal_oauth.aiohttp, "ClientSession", _raise)
        result = await GoogleCalendarOAuthHandler().revoke_token("token")
        assert result is False

    async def test_revoke_posts_token_to_revoke_url(self, monkeypatch):
        captured = {}

        class _CapturingSession(_FakeSession):
            def post(self, url, data=None, **k):
                captured["url"] = url
                captured["data"] = data
                return self._resp

        monkeypatch.setattr(
            cal_oauth.aiohttp,
            "ClientSession",
            lambda *a, **k: _CapturingSession(_FakeResp(200)),
        )
        await GoogleCalendarOAuthHandler().revoke_token("the-token-value")
        assert captured["url"] == GoogleCalendarOAuthHandler.REVOKE_URL
        assert captured["data"] == {"token": "the-token-value"}
