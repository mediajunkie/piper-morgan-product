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


class TestGetSlackSettings:
    """Tests for GET /api/v1/settings/integrations/slack"""

    @pytest.mark.asyncio
    async def test_returns_not_configured_when_no_token(self):
        """Should return configured=False when no bot token is set"""
        with patch.dict("os.environ", {}, clear=True):
            result = await get_slack_settings()

            assert result["configured"] is False
            assert result["valid"] is False
            assert result["workspace"] is None
            assert result["bot_id"] is None
            assert result["error"] is None

    @pytest.mark.asyncio
    async def test_returns_configured_and_valid_when_token_works(self):
        """Should return configured=True, valid=True when token validates.

        #1110: test_auth returns a SlackResponse dataclass (not a dict), and the
        route requires a connector-owner user_id (SLACK_CONNECTOR_USER_ID) to
        resolve credentials for the workspace-level status check.
        """
        from services.integrations.slack.slack_client import SlackResponse

        mock_router = MagicMock()
        mock_router.test_auth = AsyncMock(
            return_value=SlackResponse(
                success=True,
                data={"team": "Test Workspace", "bot_id": "B12345"},
            )
        )

        with (
            patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb-test", "SLACK_CONNECTOR_USER_ID": "owner-1"},
                clear=True,
            ),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=mock_router,
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
        ):
            result = await get_slack_settings()

            assert result["configured"] is True
            assert result["valid"] is True
            assert result["workspace"] == "Test Workspace"
            assert result["bot_id"] == "B12345"
            assert result["error"] is None
            # The connector-owner user_id must be threaded to test_auth (#1110).
            mock_router.test_auth.assert_awaited_once_with(user_id="owner-1")

    @pytest.mark.asyncio
    async def test_returns_configured_but_invalid_when_token_fails(self):
        """Should return configured=True, valid=False when token is invalid (stuck state)."""
        from services.integrations.slack.slack_client import SlackError, SlackErrorType, SlackResponse

        mock_router = MagicMock()
        mock_router.test_auth = AsyncMock(
            return_value=SlackResponse(
                success=False,
                data={},
                error=SlackError(
                    type=SlackErrorType.AUTHENTICATION_ERROR, message="invalid_auth"
                ),
            )
        )

        with (
            patch.dict(
                "os.environ",
                {"SLACK_BOT_TOKEN": "xoxb-expired", "SLACK_CONNECTOR_USER_ID": "owner-1"},
                clear=True,
            ),
            patch(
                "services.integrations.slack.slack_integration_router.SlackIntegrationRouter",
                return_value=mock_router,
            ),
            patch("services.integrations.slack.config_service.SlackConfigService"),
        ):
            result = await get_slack_settings()

            assert result["configured"] is True
            assert result["valid"] is False
            assert result["workspace"] is None
            assert result["error"] == "invalid_auth"

    @pytest.mark.asyncio
    async def test_returns_invalid_when_connector_user_not_configured(self):
        """#1110: with a bot token but no SLACK_CONNECTOR_USER_ID, the route
        cannot resolve multi-tenant credentials, so it reports invalid with a
        clear error rather than passing None into get_config (the latent bug)."""
        with patch.dict("os.environ", {"SLACK_BOT_TOKEN": "xoxb-test"}, clear=True):
            result = await get_slack_settings()

            assert result["configured"] is True
            assert result["valid"] is False
            assert result["workspace"] is None
            assert "SLACK_CONNECTOR_USER_ID" in result["error"]


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
            # Verify user_id was passed to generate_authorization_url
            mock_oauth_handler.generate_authorization_url.assert_called_once_with(
                user_id="test-user-123"
            )

    @pytest.mark.asyncio
    async def test_handles_oauth_generation_failure(self):
        """Should raise HTTPException when OAuth URL generation fails"""
        mock_config = MagicMock()
        mock_config.get_config.side_effect = Exception("Missing client_id")

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "services.integrations.slack.config_service.SlackConfigService",
            return_value=mock_config,
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_slack_oauth_url(current_user=mock_user)

            assert exc_info.value.status_code == 500
            assert "Failed to generate" in str(exc_info.value.detail)


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
            mock_oauth_handler.revoke_workspace_access.assert_called_once_with("T12345")

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
            assert result["message"] == "Slack disconnected"

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

        mock_keychain = MagicMock()
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
        mock_keychain.delete_api_key.assert_any_call("slack_bot", username="user-789")
        mock_keychain.delete_api_key.assert_any_call("slack_user", username="user-789")
        # Slack-side revoke — the behavior the prior live route lacked
        mock_oauth_handler.revoke_workspace_access.assert_called_once_with("T999")
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
