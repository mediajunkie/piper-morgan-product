"""#2178 (Arch 2026-10-25; P0 before any invite, xian 2026-11-04 19:31): GitHub Disconnect
revokes the OAuth grant AT GITHUB, before Piper clears its own copies (the token is read
first, the Slack ordering). A failed revoke still disconnects and the message gains CXO's
sentence. A PAT is never revoked by Piper: it is the person's own credential (ADR-081 D4).
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.connectors import disconnect as d
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_oauth_handler import GitHubOAuthHandler

USER = "2178aaaa-0000-4000-8000-000000002178"


def _scope():
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=MagicMock())
    scope.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock()
    factory.session_scope.return_value = scope
    return factory


class _Order:
    def __init__(self):
        self.calls: list[str] = []


async def _run(grant_value=None, grant_raises=False, revoke_ok=True):
    order = _Order()
    store = MagicMock()
    if grant_raises:
        store.get_strict = AsyncMock(side_effect=RuntimeError("decrypt"))
    else:
        store.get_strict = AsyncMock(return_value=grant_value)

    async def _delete(*a, **k):
        order.calls.append("local_grant_delete")
        return True

    store.delete = AsyncMock(side_effect=_delete)

    async def _revoke(self, token):
        order.calls.append(f"revoke:{token}")
        return revoke_ok

    repo = MagicMock()
    repo.set_status = AsyncMock()
    with (
        patch("services.database.session_factory.AsyncSessionFactory", _scope()),
        patch(
            "services.mcp.consumer.connector_grant_store.ConnectorGrantStore", return_value=store
        ),
        patch(
            "services.connectors.binding_repository.ConnectorBindingRepository", return_value=repo
        ),
        patch.object(GitHubOAuthHandler, "__init__", lambda self: None),
        patch.object(GitHubOAuthHandler, "revoke_grant", _revoke),
        patch.object(d, "_keychain_copy_gone", AsyncMock(return_value=True)),
        patch("services.connectors.github_pat_store.delete_user_pat_at_rest", AsyncMock()),
        patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
            AsyncMock(return_value=MagicMock(leg=None, reason=DegradationReason.CONNECT_REQUIRED)),
        ),
        patch("services.integrations.github.config_service.GitHubConfigService"),
    ):
        remaining, revoke_failed = await d._disconnect_github(USER)
    assert remaining == []  # every local copy verified gone
    return order.calls, revoke_failed


@pytest.mark.asyncio
async def test_an_oauth_grant_is_revoked_at_github_before_the_local_clear():
    calls, failed = await _run(grant_value="gho_token")
    assert calls[:2] == ["revoke:gho_token", "local_grant_delete"]
    assert failed is False


@pytest.mark.asyncio
async def test_a_failed_revoke_still_disconnects_and_reports_it():
    calls, failed = await _run(grant_value="gho_token", revoke_ok=False)
    assert "local_grant_delete" in calls
    assert failed is True


@pytest.mark.asyncio
async def test_a_pat_only_account_makes_no_github_revoke_call():
    calls, failed = await _run(grant_value=None)
    assert not [c for c in calls if c.startswith("revoke:")]
    assert failed is False


@pytest.mark.asyncio
async def test_an_unreadable_grant_cannot_be_revoked_so_it_is_reported():
    calls, failed = await _run(grant_raises=True)
    assert not [c for c in calls if c.startswith("revoke:")]
    assert failed is True


def test_the_route_message_carries_cxos_sentence_on_a_failed_revoke():
    from web.api.routes.settings_integrations import _disconnected_message

    msg = _disconnected_message("GitHub", d.DisconnectResult("github", (), True))
    assert msg == (
        "GitHub disconnected. Piper no longer holds your access. I couldn't revoke it at "
        "GitHub, so it stays valid there until you remove Piper in GitHub's settings."
    )
    assert _disconnected_message("GitHub", d.DisconnectResult("github", (), False)) == (
        "GitHub disconnected"
    )


class _Resp:
    def __init__(self, status):
        self.status = status

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False


class _Session:
    """DELETE answers ``delete_status``; GET /user answers ``user_status``."""

    def __init__(self, delete_status, user_status, seen):
        self._d, self._u, self._seen = delete_status, user_status, seen

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return False

    def delete(self, url, auth=None, headers=None, json=None):
        self._seen.update(url=url, auth=auth, json=json)
        return _Resp(self._d)

    def get(self, url, headers=None):
        self._seen.setdefault("gets", []).append(url)
        return _Resp(self._u)


def _handler():
    h = GitHubOAuthHandler.__new__(GitHubOAuthHandler)
    h.client_id, h.client_secret = "Iv1.client", "app-secret"
    return h


@pytest.mark.asyncio
@pytest.mark.parametrize("status,ok", [(204, True), (401, False), (500, False)])
async def test_revoke_grant_calls_githubs_delete_grant_with_the_apps_basic_auth(status, ok):
    seen: dict = {}
    with patch("aiohttp.ClientSession", lambda: _Session(status, 200, seen)):
        assert await _handler().revoke_grant("gho_token") is ok
    assert seen["url"] == "https://api.github.com/applications/Iv1.client/grant"
    assert seen["auth"].login == "Iv1.client" and seen["auth"].password == "app-secret"
    assert seen["json"] == {"access_token": "gho_token"}
    assert "gets" not in seen  # only a 404 is confirmed


@pytest.mark.asyncio
async def test_a_404_confirmed_by_get_user_401_is_revoked():
    """Arch 20:21: GitHub no longer accepts the token, so it is gone."""
    seen: dict = {}
    with patch("aiohttp.ClientSession", lambda: _Session(404, 401, seen)):
        assert await _handler().revoke_grant("gho_token") is True
    assert seen["gets"] == [GitHubOAuthHandler.USER_URL]


@pytest.mark.asyncio
@pytest.mark.parametrize("user_status", [200, 403, 500])
async def test_a_404_with_a_token_that_still_works_is_a_failed_revoke(user_status):
    """Arch 20:21: a 404 from mismatched app credentials would otherwise report revoked
    while the access stays valid at GitHub (the #2151 shape)."""
    seen: dict = {}
    with patch("aiohttp.ClientSession", lambda: _Session(404, user_status, seen)):
        assert await _handler().revoke_grant("gho_token") is False


@pytest.mark.asyncio
async def test_revoke_grant_without_app_credentials_reports_failure_and_calls_nothing():
    h = GitHubOAuthHandler.__new__(GitHubOAuthHandler)
    h.client_id, h.client_secret = "", ""
    with patch("aiohttp.ClientSession", side_effect=AssertionError("no call")):
        assert await h.revoke_grant("gho_token") is False
