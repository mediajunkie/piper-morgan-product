"""#2279 (CXO's words 2026-11-04, Arch's durable guard under #2266): after someone connects
GitHub, Piper says which GitHub account it was. The Integrations card reads the login
through the account's own grant and says "Connected as {login}. Not the right account?
Disconnect, then connect again."; when that read fails it says "Connected." with no login
and no guess. The success line after the callback reads "GitHub is connected as {login}."
and names no one when the handler read no login. The login never comes from the
deployment's env handle or another account's credential.
"""

from __future__ import annotations

import contextlib
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.github.read_failed import GitHubReadFailed
from services.integrations.principal_test_results import PrincipalTestResultStore
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubReposResult
from web.api.routes import integrations as integrations_routes
from web.api.routes import settings_integrations as si

ROOT = Path(__file__).resolve().parents[3]
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
METADATA = integrations_routes.INTEGRATION_REGISTRY["github"]
OAUTH = GitHubCredential(owner_id="user-1", mcp_server_ref="github", token="g", leg="oauth")
CARD = "Connected as octocat. Not the right account? Disconnect, then connect again."


async def _card(login_mock, user_id="user-1"):
    with (
        patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=OAUTH)),
        patch(f"{_ADAPTER}.account_login", new=login_mock),
        patch.object(
            integrations_routes, "_get_test_result_store", return_value=PrincipalTestResultStore()
        ),
    ):
        return await integrations_routes._github_card(METADATA, user_id)


class TestTheCard:
    @pytest.mark.asyncio
    async def test_connected_as_the_accounts_own_login(self, monkeypatch):
        monkeypatch.setenv("PIPER_GITHUB_HANDLE", "mediajunkie")
        login = AsyncMock(return_value="octocat")
        card = await _card(login)
        assert card.status == "connected"
        assert card.status_message == CARD
        login.assert_awaited_once_with("user-1")  # this account's grant, nothing else
        assert "mediajunkie" not in card.status_message

    @pytest.mark.asyncio
    async def test_an_unreadable_login_is_connected_with_no_name(self, monkeypatch):
        monkeypatch.setenv("PIPER_GITHUB_HANDLE", "mediajunkie")
        login = AsyncMock(side_effect=GitHubReadFailed("no login", None, detail="login_unresolved"))
        card = await _card(login)
        assert card.status == "connected"
        assert card.status_message == "Connected."
        assert "mediajunkie" not in card.status_message

    @pytest.mark.asyncio
    async def test_an_empty_login_is_connected_with_no_name(self):
        card = await _card(AsyncMock(return_value=""))
        assert card.status_message == "Connected."

    def test_the_words_are_cxos(self):
        assert integrations_routes._GITHUB_CARD_CONNECTED_AS == (
            "Connected as {login}. Not the right account? Disconnect, then connect again."
        )
        assert integrations_routes._GITHUB_CARD_CONNECTED_NO_LOGIN == "Connected."
        assert not hasattr(integrations_routes, "_GITHUB_CARD_CONNECTED")


class TestTheSuccessLine:
    def test_the_page_renders_the_login_from_the_callback(self):
        src = (ROOT / "templates/integrations.html").read_text()
        i = src.index("params.get('github_success') === 'true'")
        block = src[i : i + 500]
        assert "`GitHub is connected as ${decodeURIComponent(login)}.`" in block
        assert "'GitHub is connected.'" in block
        assert "params.get('github_login')" in block

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "handler_result, expected_param",
        [({"login": "octocat"}, "github_login=octocat"), ({}, "github_login=")],
    )
    async def test_the_callback_passes_only_a_login_it_read(
        self, monkeypatch, handler_result, expected_param
    ):
        result = {
            "user_id": "user-1",
            "tokens": SimpleNamespace(access_token="t"),
            **handler_result,
        }
        handler = MagicMock()
        handler.return_value.handle_oauth_callback = AsyncMock(return_value=result)

        @contextlib.asynccontextmanager
        async def _scope():
            s = MagicMock()
            s.commit = AsyncMock()
            yield s

        monkeypatch.setattr(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            staticmethod(_scope),
        )
        with (
            patch("services.mcp.consumer.github_oauth_handler.GitHubOAuthHandler", handler),
            patch(
                "services.mcp.consumer.github_oauth_handler.persist_github_connection",
                new=AsyncMock(),
            ),
            patch(
                f"{_ADAPTER}.search_user_repositories",
                new=AsyncMock(return_value=GitHubReposResult(repositories=[])),
            ),
        ):
            response = await si.handle_github_callback(code="c", state="s")
        assert response.status_code == 302
        location = response.headers["location"]
        assert location.startswith("/settings/integrations?github_success=true&")
        assert location.endswith(expected_param)
        assert "github_login=github" not in location  # the old placeholder never ships
