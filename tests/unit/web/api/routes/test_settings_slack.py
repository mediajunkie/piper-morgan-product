"""
Unit tests for Slack Settings API
Issue #528: ALPHA-SETUP-SLACK - Add Slack OAuth to setup wizard
Issue #576: OAuth App Credential Configuration in UI

Tests the Slack OAuth management endpoints in settings_integrations.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    SlackAppCredentialsRequest,
    disconnect_slack,
    get_slack_app_credentials_status,
    get_slack_oauth_url,
    get_slack_settings,
    save_slack_app_credentials,
)


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


class TestGetSlackSettings:
    """Tests for GET /api/v1/settings/integrations/slack.

    #2151 (route group 1): the CALLER's status (binding-first status service), then
    auth.test AS the caller. It read only the host's env with no caller, so an OAuth
    user read "not configured" and the host's bot was everyone's workspace."""

    @staticmethod
    def _patch(status, auth=None, auth_raises=None):
        router = MagicMock()
        router.test_auth = (
            AsyncMock(side_effect=auth_raises) if auth_raises else AsyncMock(return_value=auth)
        )
        return router, [
            patch(
                "services.integrations.integration_status_service.IntegrationStatusService.get_status",
                new=AsyncMock(return_value=status),
            ),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=router,
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
        ]

    async def _get(self, patches, sub="u-slack"):
        for p in patches:
            p.start()
        try:
            return await get_slack_settings(current_user=MagicMock(sub=sub))
        finally:
            for p in patches:
                p.stop()

    @pytest.mark.asyncio
    async def test_returns_not_configured_when_the_caller_has_no_slack(self):
        router, patches = self._patch({"configured": False, "check_failed": False})
        result = await self._get(patches)
        assert result["configured"] is False and result["valid"] is False
        router.test_auth.assert_not_called()

    @pytest.mark.asyncio
    async def test_returns_the_callers_workspace_when_auth_test_works(self):
        auth = MagicMock(success=True, data={"ok": True, "team": "Fake Team", "bot_id": "B1"})
        router, patches = self._patch({"configured": True, "check_failed": False}, auth=auth)
        result = await self._get(patches, sub="u-me")
        assert result == {
            "configured": True,
            "valid": True,
            "workspace": "Fake Team",
            "bot_id": "B1",
            "error": None,
        }
        router.test_auth.assert_awaited_once_with(user_id="u-me")

    @pytest.mark.asyncio
    async def test_a_refused_token_says_reconnect(self):
        from web.api.routes.settings_integrations import SLACK_STATUS_REFUSED_LINE

        auth = MagicMock(success=True, data={"ok": False, "error": "token_revoked"})
        _r, patches = self._patch({"configured": True, "check_failed": False}, auth=auth)
        result = await self._get(patches)
        assert result["configured"] is True and result["valid"] is False
        assert result["error"] == SLACK_STATUS_REFUSED_LINE

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "status,auth,raises",
        [
            ({"configured": False, "check_failed": True}, None, None),
            ({"configured": True, "check_failed": False}, MagicMock(success=False, data={}), None),
            ({"configured": True, "check_failed": False}, None, RuntimeError("fake")),
        ],
    )
    async def test_a_check_that_couldnt_run_is_check_failed(self, status, auth, raises):
        from web.api.routes.settings_integrations import SLACK_STATUS_CHECK_FAILED_LINE

        _r, patches = self._patch(status, auth=auth, auth_raises=raises)
        result = await self._get(patches)
        assert result["check_failed"] is True
        assert result["error"] == SLACK_STATUS_CHECK_FAILED_LINE


class TestGetSlackOAuthUrl:
    """Tests for GET /api/v1/settings/integrations/slack/authorize"""

    @pytest.mark.asyncio
    async def test_returns_authorization_url(self):
        """Should return OAuth authorization URL and state"""
        mock_oauth_handler = MagicMock()
        # Issue #1109: generate_authorization_url is async → AsyncMock
        mock_oauth_handler.generate_authorization_url = AsyncMock(
            return_value=(
                "https://slack.com/oauth/v2/authorize?client_id=test&scope=chat:write",
                "secure_state_token",
            )
        )

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            result = await get_slack_oauth_url(current_user=mock_user)

            assert result["success"] is True
            assert "slack.com/oauth" in result["authorization_url"]
            assert result["state"] == "secure_state_token"
            # Verify user_id was passed to generate_authorization_url, and that the
            # route supplies an explicit redirect_uri (2026-08-07: the legacy route
            # passed NONE, so Slack received an empty redirect_uri — the assertion
            # now pins the #1324 fallback chain, localhost default in test env)
            mock_oauth_handler.generate_authorization_url.assert_called_once_with(
                user_id="test-user-123",
                redirect_uri="http://localhost:8001/api/v1/settings/integrations/slack/callback",
            )

    @pytest.mark.asyncio
    async def test_handles_oauth_generation_failure(self):
        """Should raise HTTPException when OAuth URL generation fails.

        #1499: this route now delegates to `connect_slack`, so the failure it
        surfaces is that one's (`Failed to start Slack OAuth`), not a second
        message maintained here. Updated with the collapse — the OLD version
        patched `SlackConfigService`, a collaborator the single implementation
        never touches directly (`SlackOAuthHandler` binds its own at import
        time), so after the collapse it asserted against a failure that could no
        longer occur. Fail the handler itself instead, which is the real failure
        mode: Slack unreachable / credentials missing at URL-generation time.
        """
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.generate_authorization_url = AsyncMock(
            side_effect=Exception("Missing client_id")
        )

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "services.integrations.slack.oauth_handler.SlackOAuthHandler",
            return_value=mock_oauth_handler,
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_slack_oauth_url(current_user=mock_user)

            assert exc_info.value.status_code == 500
            assert "Failed to start Slack OAuth" in str(exc_info.value.detail)
            assert "Missing client_id" in str(exc_info.value.detail)


class TestDisconnectSlack:
    """Tests for POST /api/v1/settings/integrations/slack/disconnect"""

    @pytest.mark.asyncio
    async def test_disconnects_and_returns_success(self):
        """Should revoke access and return success"""
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.revoke_workspace_access = AsyncMock(return_value=True)

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb-test", "SLACK_TEAM_ID": "T12345"},
                clear=True,
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            result = await disconnect_slack(current_user=mock_user)

            assert result["success"] is True
            assert result["message"] == "Slack disconnected"
            # 2026-07-06 (#542): revoke_workspace_access now takes user_id, not the
            # workspace_id env var -- the real per-user token lookup needs user_id.
            mock_oauth_handler.revoke_workspace_access.assert_called_once_with("test-user-123")

    @pytest.mark.asyncio
    async def test_succeeds_even_when_revoke_fails(self):
        """Should still succeed even if API revoke fails (clears local config)"""
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.revoke_workspace_access = AsyncMock(side_effect=Exception("API error"))

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb-test"},
                clear=True,
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            # Should not raise, just log warning
            result = await disconnect_slack(current_user=mock_user)

            assert result["success"] is True
            # #2172: Piper holds no copy, so success, with CXO's line that it stays valid at Slack
            assert result["message"].startswith("Slack disconnected. Piper no longer holds")

    @pytest.mark.asyncio
    async def test_handles_missing_token_gracefully(self):
        """Should succeed even if no token exists to clear (#1334-P2: clearing is
        best-effort in the disconnect_connector helper)."""
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.revoke_workspace_access = AsyncMock(return_value=True)
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch.dict("os.environ", {}, clear=True),
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            result = await disconnect_slack(current_user=mock_user)

            assert result["success"] is True
            assert result["message"] == "Slack disconnected"

    @pytest.mark.asyncio
    async def test_clears_user_scoped_keychain_and_revokes_1334(self):
        """#1334: the consolidated disconnect must do BOTH — delete the user-scoped
        keychain creds (slack_bot + slack_user, #849) AND revoke on Slack's side. The
        two prior duplicate defs each did only one (the live one skipped the revoke;
        the shadowed one leaked the keychain creds)."""
        import os

        mock_keychain = _async_keychain()
        mock_oauth_handler = MagicMock()
        mock_oauth_handler.revoke_workspace_access = AsyncMock(return_value=True)
        mock_user = MagicMock()
        mock_user.sub = "user-789"

        with (
            patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb", "SLACK_TEAM_ID": "T999"},
                clear=True,
            ),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
            patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler",
                return_value=mock_oauth_handler,
            ),
        ):
            result = await disconnect_slack(current_user=mock_user)

        assert result["success"] is True
        # user-scoped keychain creds removed (#849) — the behavior the dead dup lacked
        mock_keychain.adelete_api_key.assert_any_await("slack_bot", "user-789")
        mock_keychain.adelete_api_key.assert_any_await("slack_user", "user-789")
        # Slack-side revoke — the behavior the prior live route lacked
        # 2026-07-06 (#542): takes user_id now, not the workspace_id env var
        mock_oauth_handler.revoke_workspace_access.assert_called_once_with("user-789")
        # env cleared
        assert "SLACK_BOT_TOKEN" not in os.environ
        assert "SLACK_TEAM_ID" not in os.environ


class TestIntegrationRegistrySlackUrl:
    """Tests for Slack configure_url in INTEGRATION_REGISTRY (Issue #528)"""

    def test_slack_configure_url_points_to_settings_page(self):
        """Slack configure_url should point to dedicated settings page"""
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        slack_config = INTEGRATION_REGISTRY.get("slack")
        assert slack_config is not None
        assert slack_config["configure_url"] == "/settings/integrations/slack"
        # Should NOT be None anymore
        assert slack_config["configure_url"] is not None


class TestSlackAppCredentials:
    """Tests for Slack app credentials endpoints (Issue #576)"""

    @pytest.mark.asyncio
    async def test_save_credentials_stores_in_keychain(self):
        """Should store client_id and client_secret in keychain"""
        # Issue #734: Now uses IntegrationConfigService
        mock_config_service = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "test_user"

        credentials = SlackAppCredentialsRequest(
            client_id="1234567890.1234567890", client_secret="test_secret_value"
        )

        with patch(
            "services.integrations.integration_config_service.IntegrationConfigService",
            return_value=mock_config_service,
        ):
            result = await save_slack_app_credentials(credentials, mock_user)

            assert result["success"] is True
            assert "saved" in result["message"].lower()
            # Verify IntegrationConfigService was called
            mock_config_service.store_slack_credentials.assert_called_once_with(
                "1234567890.1234567890", "test_secret_value"
            )

    @pytest.mark.asyncio
    async def test_save_credentials_strips_whitespace(self):
        """Should strip whitespace from credentials before storing"""
        # Issue #734: Now uses IntegrationConfigService
        mock_config_service = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "test_user"

        credentials = SlackAppCredentialsRequest(
            client_id="  1234567890.1234567890  ", client_secret="  secret_with_spaces  "
        )

        with patch(
            "services.integrations.integration_config_service.IntegrationConfigService",
            return_value=mock_config_service,
        ):
            await save_slack_app_credentials(credentials, mock_user)

            # Verify whitespace was stripped by checking store_slack_credentials was called with stripped values
            mock_config_service.store_slack_credentials.assert_called_once_with(
                "1234567890.1234567890", "secret_with_spaces"
            )

    @pytest.mark.asyncio
    async def test_get_status_returns_configured_when_both_present(self):
        """Should return configured=True when both client_id and client_secret exist"""
        mock_config_service = MagicMock()
        mock_config = MagicMock()
        mock_config.client_id = "1234567890.1234567890"
        mock_config.client_secret = "secret_value"
        mock_config_service.get_config.return_value = mock_config
        mock_user = MagicMock()

        with patch(
            "services.integrations.slack.config_service.SlackConfigService",
            return_value=mock_config_service,
        ):
            result = await get_slack_app_credentials_status(mock_user)

            assert result.configured is True
            assert result.has_client_id is True
            assert result.has_client_secret is True

    @pytest.mark.asyncio
    async def test_get_status_returns_not_configured_when_missing_id(self):
        """Should return configured=False when client_id is missing"""
        mock_config_service = MagicMock()
        mock_config = MagicMock()
        mock_config.client_id = ""  # Empty
        mock_config.client_secret = "secret_value"
        mock_config_service.get_config.return_value = mock_config
        mock_user = MagicMock()

        with patch(
            "services.integrations.slack.config_service.SlackConfigService",
            return_value=mock_config_service,
        ):
            result = await get_slack_app_credentials_status(mock_user)

            assert result.configured is False
            assert result.has_client_id is False
            assert result.has_client_secret is True

    @pytest.mark.asyncio
    async def test_get_status_returns_not_configured_when_missing_secret(self):
        """Should return configured=False when client_secret is missing"""
        mock_config_service = MagicMock()
        mock_config = MagicMock()
        mock_config.client_id = "1234567890.1234567890"
        mock_config.client_secret = ""  # Empty
        mock_config_service.get_config.return_value = mock_config
        mock_user = MagicMock()

        with patch(
            "services.integrations.slack.config_service.SlackConfigService",
            return_value=mock_config_service,
        ):
            result = await get_slack_app_credentials_status(mock_user)

            assert result.configured is False
            assert result.has_client_id is True
            assert result.has_client_secret is False

    @pytest.mark.asyncio
    async def test_get_status_never_exposes_credentials(self):
        """Status response should never contain actual credential values"""
        mock_config_service = MagicMock()
        mock_config = MagicMock()
        mock_config.client_id = "secret_client_id"
        mock_config.client_secret = "super_secret_value"
        mock_config_service.get_config.return_value = mock_config
        mock_user = MagicMock()

        with patch(
            "services.integrations.slack.config_service.SlackConfigService",
            return_value=mock_config_service,
        ):
            result = await get_slack_app_credentials_status(mock_user)

            # Convert to dict to check all fields
            result_dict = result.model_dump()

            # Should not contain actual credential values
            for value in result_dict.values():
                if isinstance(value, str):
                    assert "secret_client_id" not in value
                    assert "super_secret_value" not in value

            # Only boolean fields should exist
            assert isinstance(result.configured, bool)
            assert isinstance(result.has_client_id, bool)
            assert isinstance(result.has_client_secret, bool)


@__import__("pytest").fixture(autouse=True)
def _all_connectors_offered_2237(monkeypatch):
    """These tests exercise the Slack/Notion route bodies themselves; #2237's guard
    (pinned in test_offered_connector_guard_2237.py) is stepped aside here."""
    from services.integrations import integration_status_service as svc

    monkeypatch.setattr(
        svc,
        "BETA_OFFERED_CONNECTORS",
        {"github": "GitHub", "slack": "Slack", "calendar": "Google Calendar", "notion": "Notion"},
    )
