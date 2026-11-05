"""#2288 (Arch 2026-11-05 10:31, PA's served finding): a 401 from GitHub on an account's
grant is the stale state, on whichever path sees it first. The card's own login read
(#2279's ``GET /user``) sends it through the one function that marks the binding STALE,
and the card reads "Needs reconnecting" on that render. Any other failure keeps the
"Connected." fallback, because unknown is not stale. A rejected personal token says
nothing about the OAuth grant and never marks it.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.integrations.github.read_failed import GitHubReadFailed
from services.integrations.principal_test_results import PrincipalTestResultStore
from services.mcp.consumer.connector import DegradationReason
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubMCPSpatialAdapter
from web.api.routes import integrations as integrations_routes

_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
_VALIDATOR = "services.integrations.github.token_validator.verify_github_token"
METADATA = integrations_routes.INTEGRATION_REGISTRY["github"]
OAUTH = GitHubCredential(owner_id="user-1", mcp_server_ref="github", token="t", leg="oauth")
PAT = GitHubCredential(owner_id="user-1", mcp_server_ref="github", token="p", leg="pat")
REJECTED = {"authenticated": False, "username": None, "error": "401", "status_code": 401}


async def _card(login_mock):
    with (
        patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=OAUTH)),
        patch(f"{_ADAPTER}.account_login", new=login_mock),
        patch.object(
            integrations_routes, "_get_test_result_store", return_value=PrincipalTestResultStore()
        ),
    ):
        return await integrations_routes._github_card(METADATA, "user-1")


class TestTheCard:
    @pytest.mark.asyncio
    async def test_a_rejected_grant_renders_needs_reconnecting(self):
        stale = GitHubReadFailed("rejected", DegradationReason.STALE_TOKEN, detail="token_rejected")
        card = await _card(AsyncMock(side_effect=stale))
        assert card.status == "degraded"
        assert card.status_message == "Needs reconnecting"
        assert card.status_detail == integrations_routes.GITHUB_CARD_RECONNECT_DETAIL
        assert card.action == "reconnect"

    @pytest.mark.asyncio
    async def test_an_unknown_failure_stays_connected(self):
        unknown = GitHubReadFailed("down", DegradationReason.UNREACHABLE, detail="unreachable")
        card = await _card(AsyncMock(side_effect=unknown))
        assert card.status == "connected"
        assert card.status_message == "Connected."


async def _login(credential, verify_result):
    adapter = GitHubMCPSpatialAdapter.__new__(GitHubMCPSpatialAdapter)
    mark = AsyncMock(return_value=True)
    with (
        patch.object(
            GitHubMCPSpatialAdapter,
            "_grant_headers_or_raise",
            AsyncMock(return_value={"Authorization": "Bearer t"}),
        ),
        patch.object(
            GitHubMCPSpatialAdapter, "resolve_credential", AsyncMock(return_value=credential)
        ),
        patch.object(GitHubMCPSpatialAdapter, "_mark_oauth_binding_stale", mark),
        patch(_VALIDATOR, new=AsyncMock(return_value=verify_result)),
    ):
        try:
            return await adapter.account_login("user-1"), mark
        except GitHubReadFailed as e:
            return e, mark


class TestTheLoginRead:
    @pytest.mark.asyncio
    async def test_a_401_on_the_oauth_leg_marks_stale(self):
        err, mark = await _login(OAUTH, REJECTED)
        assert isinstance(err, GitHubReadFailed)
        assert err.reason is DegradationReason.STALE_TOKEN and err.detail == "token_rejected"
        mark.assert_awaited_once_with(OAUTH)

    @pytest.mark.asyncio
    async def test_a_grant_that_changed_since_the_read_is_not_marked(self):
        """Arch 15:28: the 401 was for token "t"; the binding now holds another grant."""
        rotated = GitHubCredential(
            owner_id="user-1", mcp_server_ref="github", token="new-grant", leg="oauth"
        )
        err, mark = await _login(rotated, REJECTED)
        assert isinstance(err, GitHubReadFailed) and err.reason is None
        mark.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_a_401_on_the_pat_leg_never_marks_the_grant(self):
        err, mark = await _login(PAT, REJECTED)
        assert isinstance(err, GitHubReadFailed)
        assert err.reason is None and err.detail == "login_unresolved"
        mark.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_a_403_is_not_stale(self):
        forbidden = {"authenticated": False, "username": None, "error": "403"}
        err, mark = await _login(OAUTH, forbidden)
        assert isinstance(err, GitHubReadFailed) and err.reason is None
        mark.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_a_good_read_returns_the_login(self):
        login, mark = await _login(OAUTH, {"authenticated": True, "username": "octocat"})
        assert login == "octocat"
        mark.assert_not_awaited()


@pytest.mark.asyncio
async def test_the_validator_names_a_401():
    from services.integrations.github import token_validator

    class _Resp:
        status_code = 401

    class _Client:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def get(self, *a, **k):
            return _Resp()

    with patch("httpx.AsyncClient", lambda *a, **k: _Client()):
        result = await token_validator.verify_github_token("ghp_dead")
    assert result["status_code"] == 401 and result["authenticated"] is False
