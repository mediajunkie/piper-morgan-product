"""#2187 — the GitHub card's Test record has an honest lifecycle (CXO's ruling 14:32 10-28; Lead's size read).

Two served states from xian's #2018 run on alpha 879d18bf72: (1) a grant with no Test on record read
"Connected with your GitHub account." with no checked line; (2) a FRESH grant showed the previous grant's
failed check ("Last checked 3 minutes ago", red) until Test was pressed. Both are one record's lifecycle:
``PrincipalTestResultStore`` had no per-key forget, and neither a new grant nor a disconnect touched it.

Pins: the no-record card carries the #2044 unchecked detail; ``forget`` drops exactly one key; a clean
disconnect forgets and an incomplete one does not; the GitHub OAuth callback forgets the old record when it
stores a new grant.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from services.connectors import disconnect as disconnect_mod
from services.integrations.principal_test_results import PrincipalTestResultStore
from web.api.routes import integrations as integrations_routes

METADATA = {"display_name": "GitHub", "configure_url": "/settings/integrations/github"}


def _adapter_cls():
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    return GitHubMCPSpatialAdapter


def _oauth_credential():
    return SimpleNamespace(leg="oauth", stale_oauth_reason=None)


class TestStoreForget:
    def test_forget_drops_exactly_one_key(self):
        store = PrincipalTestResultStore()
        store.record_test_result("u1", "github", ok=False, error="401")
        store.record_test_result("u1", "slack", ok=True)
        store.record_test_result("u2", "github", ok=True)
        assert store.forget("u1", "github") is True
        assert store.get_test_result("u1", "github") is None
        assert store.get_test_result("u1", "slack") is not None
        assert store.get_test_result("u2", "github") is not None

    def test_forget_is_a_no_op_without_a_record_or_a_principal(self):
        store = PrincipalTestResultStore()
        assert store.forget("u1", "github") is False
        assert store.forget(None, "github") is False


@pytest.mark.asyncio
async def test_no_record_card_says_not_checked_yet():
    with (
        patch.object(
            _adapter_cls(), "resolve_credential", AsyncMock(return_value=_oauth_credential())
        ),
        patch.object(
            integrations_routes, "_get_test_result_store", return_value=PrincipalTestResultStore()
        ),
    ):
        card = await integrations_routes._github_card(METADATA, "user-1")
    assert card.status == "connected"
    assert card.status_message == "Connected with your GitHub account."
    assert (
        card.status_detail == integrations_routes.UNCHECKED_DETAIL == "Not checked yet. Press Test."
    )
    assert card.last_check is None and card.can_test is True


@pytest.mark.asyncio
async def test_a_recorded_check_keeps_its_line_and_no_unchecked_detail():
    store = PrincipalTestResultStore()
    store.record_test_result("user-1", "github", ok=False, error="401 Bad credentials")
    with (
        patch.object(
            _adapter_cls(), "resolve_credential", AsyncMock(return_value=_oauth_credential())
        ),
        patch.object(integrations_routes, "_get_test_result_store", return_value=store),
    ):
        card = await integrations_routes._github_card(METADATA, "user-1")
    assert card.status == "failed" and card.status_detail is None and card.last_check is not None


@pytest.mark.asyncio
async def test_clean_disconnect_forgets_the_record_and_incomplete_does_not():
    store = PrincipalTestResultStore()
    store.record_test_result("u1", "github", ok=False, error="401")
    with (
        patch.object(disconnect_mod, "_disconnect_github", AsyncMock(return_value=[])),
        patch(
            "services.integrations.principal_test_results.get_test_result_store", return_value=store
        ),
    ):
        result = await disconnect_mod.disconnect_connector("u1", "github")
    assert result.cleared and store.get_test_result("u1", "github") is None

    store.record_test_result("u1", "github", ok=False, error="401")
    with (
        patch.object(
            disconnect_mod, "_disconnect_github", AsyncMock(return_value=["keychain_pat"])
        ),
        patch(
            "services.integrations.principal_test_results.get_test_result_store", return_value=store
        ),
    ):
        result = await disconnect_mod.disconnect_connector("u1", "github")
    assert not result.cleared and store.get_test_result("u1", "github") is not None


@pytest.mark.asyncio
async def test_a_new_grant_forgets_the_previous_grants_check():
    from web.api.routes import settings_integrations as settings_routes

    store = PrincipalTestResultStore()
    store.record_test_result("user-1", "github", ok=False, error="401 Bad credentials")

    @asynccontextmanager
    async def _scope():
        yield SimpleNamespace(commit=AsyncMock())

    handler = SimpleNamespace(
        handle_oauth_callback=AsyncMock(
            return_value={
                "user_id": "user-1",
                "tokens": SimpleNamespace(access_token="ghu_x"),
                "login": "someone",
            }
        )
    )
    with (
        patch(
            "services.mcp.consumer.github_oauth_handler.GitHubOAuthHandler", return_value=handler
        ),
        patch("services.mcp.consumer.github_oauth_handler.persist_github_connection", AsyncMock()),
        patch("services.database.session_factory.AsyncSessionFactory.session_scope", _scope),
        patch.object(
            _adapter_cls(),
            "search_user_repositories",
            AsyncMock(return_value=SimpleNamespace(repositories=[])),
        ),
        patch(
            "services.integrations.principal_test_results.get_test_result_store", return_value=store
        ),
    ):
        response = await settings_routes.handle_github_callback(code="c", state="s", error=None)
    assert response.status_code == 302 and "github_error" not in str(
        response.headers.get("location", "")
    )
    assert store.get_test_result("user-1", "github") is None
