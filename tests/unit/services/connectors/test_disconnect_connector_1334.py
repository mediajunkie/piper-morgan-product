"""#1334 Part 2 — uniform disconnect_connector helper (Arch-ruled 2026-06-30).

One call surface, per-model dispatch behind it. Recurrence-proofs #1330 (github
binding/grant leak) and fixes the notion two-store gap (#1337): the real token is in
the user-scoped #358 store, not just the keychain.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.connectors.disconnect import SUPPORTED_CONNECTORS, disconnect_connector

pytestmark = pytest.mark.asyncio

_U = "user-42"


def _async_keychain(get_value=None):
    """KeychainService double for the async disconnect path (#2172): deletes succeed and
    the provenance read-back answers VERIFIED_ABSENT unless a test says otherwise."""
    from services.infrastructure.keychain_service import SecretProvenance, SecretRead

    kc = MagicMock()
    kc.adelete_api_key = AsyncMock(return_value=True)
    kc.aget_api_key = AsyncMock(return_value=get_value)
    kc.aread_secret = AsyncMock(return_value=SecretRead(SecretProvenance.VERIFIED_ABSENT))
    return kc


def _github_credential_gone():
    """The GitHub read-back (#2172) finds no credential: CONNECT_REQUIRED, no leg."""
    from types import SimpleNamespace

    from services.mcp.consumer.connector import DegradationReason

    return patch(
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential",
        AsyncMock(return_value=SimpleNamespace(reason=DegradationReason.CONNECT_REQUIRED)),
    )


async def test_unknown_connector_raises():
    with pytest.raises(ValueError):
        await disconnect_connector(_U, "dropbox")


def test_supported_set():
    assert set(SUPPORTED_CONNECTORS) == {"github", "slack", "calendar", "notion"}


async def test_github_clears_credential_binding_and_grant_1330():
    """github disconnect clears the keychain PAT, sets the binding UNBOUND, and revokes
    the #358 grant (the #1330 recurrence-proof)."""
    keychain = _async_keychain()
    binding_repo = MagicMock()
    binding_repo.set_status = AsyncMock()
    grant_store = MagicMock()
    grant_store.delete = AsyncMock(return_value=True)

    session = AsyncMock()
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=session)
    scope.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock()
    factory.session_scope.return_value = scope

    with (
        patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_x"}, clear=True),
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch("services.integrations.github.config_service.GitHubConfigService"),
        patch("services.database.session_factory.AsyncSessionFactory", factory),
        patch(
            "services.connectors.binding_repository.ConnectorBindingRepository",
            return_value=binding_repo,
        ),
        patch(
            "services.mcp.consumer.connector_grant_store.ConnectorGrantStore",
            return_value=grant_store,
        ),
        patch("services.connectors.github_pat_store.delete_user_pat_at_rest", AsyncMock()),  # #1982
        _github_credential_gone(),
    ):
        result = await disconnect_connector(_U, "github")

    assert result.cleared, result.remaining
    keychain.adelete_api_key.assert_any_await("github_token", _U)
    binding_repo.set_status.assert_awaited_once_with(_U, "github", "unbound")
    grant_store.delete.assert_awaited_once()


async def test_slack_clears_keychain_and_revokes():
    keychain = _async_keychain()
    oauth = MagicMock()
    oauth.revoke_workspace_access = AsyncMock(return_value=True)

    with (
        patch.dict("os.environ", {"SLACK_TEAM_ID": "T1", "SLACK_BOT_TOKEN": "xoxb"}, clear=True),
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch("services.integrations.slack.config_service.SlackConfigService"),
        patch("services.integrations.slack.oauth_handler.SlackOAuthHandler", return_value=oauth),
    ):
        result = await disconnect_connector(_U, "slack")

    assert result.cleared, result.remaining
    keychain.adelete_api_key.assert_any_await("slack_bot", _U)
    keychain.adelete_api_key.assert_any_await("slack_user", _U)
    # 2026-07-06 (#542): revoke_workspace_access now takes user_id, not workspace_id --
    # the old workspace_id (from an env var) had no relationship to which user was
    # disconnecting, and the real per-user token lookup needs user_id anyway.
    oauth.revoke_workspace_access.assert_awaited_once_with(_U)


async def test_calendar_clears_user_scoped_key():
    keychain = _async_keychain(get_value=None)  # no stored token -> revoke is skipped
    with (
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
    ):
        result = await disconnect_connector(_U, "calendar")
    assert result.cleared, result.remaining
    keychain.aget_api_key.assert_awaited_once_with(f"google_calendar_{_U}")
    keychain.adelete_api_key.assert_awaited_once_with(f"google_calendar_{_U}", None)
    keychain.aread_secret.assert_awaited_once_with(f"google_calendar_{_U}", None)


async def test_calendar_revokes_before_clearing_1334_542():
    """#542: a real stored token gets revoked on Google's side before the local
    keychain entry is cleared (not just deleted, as it was before this fix)."""
    keychain = _async_keychain(get_value="refresh-token-abc")
    oauth = MagicMock()
    order = []

    async def _revoke(token):
        order.append("revoke")
        return True

    async def _delete(*args):
        order.append("delete")
        return True

    oauth.revoke_token = AsyncMock(side_effect=_revoke)
    keychain.adelete_api_key = AsyncMock(side_effect=_delete)

    with (
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
            return_value=oauth,
        ),
    ):
        result = await disconnect_connector(_U, "calendar")

    assert result.cleared, result.remaining
    oauth.revoke_token.assert_awaited_once_with("refresh-token-abc")
    keychain.adelete_api_key.assert_awaited_once_with(f"google_calendar_{_U}", None)
    assert order == ["revoke", "delete"]  # revoke on Google's side BEFORE the local clear


async def test_notion_clears_keychain_AND_user_scoped_358_store_1337():
    """The #1337/#1334-P2 fix: notion's real token is in the #358 store — clear BOTH
    the legacy keychain key and the UserAPIKeyService store."""
    keychain = _async_keychain()
    svc = MagicMock()
    svc.delete_user_key = AsyncMock(return_value=True)

    session = AsyncMock()
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=session)
    scope.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock()
    factory.session_scope_fresh.return_value = scope

    with (
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch("services.database.session_factory.AsyncSessionFactory", factory),
        patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc),
    ):
        result = await disconnect_connector(_U, "notion")

    assert result.cleared, result.remaining
    keychain.adelete_api_key.assert_any_await("notion", _U)
    svc.delete_user_key.assert_awaited_once()
    args, _ = svc.delete_user_key.call_args
    assert args[1] == _U and args[2] == "notion"
