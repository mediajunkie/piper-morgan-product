"""
Unit tests for Slack OAuth in setup wizard
Issue #528: ALPHA-SETUP-SLACK

Tests Slack OAuth flow initiation, callback handling,
and status checking in the setup wizard context.

Note: These tests mock the SlackOAuthHandler at the import location
within the function (services.integrations.slack.oauth_handler).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

pytestmark = pytest.mark.unit


class TestSlackOAuthTrigger:
    """Tests for initiating Slack OAuth from setup wizard"""

    @pytest.mark.asyncio
    async def test_get_slack_oauth_url_returns_authorization_url(self):
        """Should return Slack OAuth URL with state"""
        from web.api.routes.setup import start_slack_oauth

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # When: Requesting OAuth start (must mock both config and handler)
        with patch("services.integrations.slack.config_service.SlackConfigService") as MockConfig:
            # Mock config service to return valid credentials
            mock_config_instance = MagicMock()
            mock_config = MagicMock()
            mock_config.client_id = "test_client_id"
            mock_config.client_secret = "test_client_secret"
            mock_config_instance.get_config.return_value = mock_config
            MockConfig.return_value = mock_config_instance

            with patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler"
            ) as MockHandler:
                mock_instance = MagicMock()
                # Issue #1109: generate_authorization_url is async → AsyncMock
                mock_instance.generate_authorization_url = AsyncMock(
                    return_value=(
                        "https://slack.com/oauth/v2/authorize?client_id=test&scope=chat:write",
                        "state_abc123",
                    )
                )
                MockHandler.return_value = mock_instance

                response = await start_slack_oauth(current_user=mock_user)

        # Then: Response contains auth URL and state
        assert "auth_url" in response
        assert "state" in response
        assert "slack.com/oauth" in response["auth_url"]
        assert response["state"] == "state_abc123"
        # Verify user_id was passed (redirect_uri may be None)
        mock_instance.generate_authorization_url.assert_called_once_with(
            user_id="test-user-123", redirect_uri=None
        )

    @pytest.mark.asyncio
    async def test_oauth_url_includes_required_scopes(self):
        """OAuth URL should include bot scopes"""
        from web.api.routes.setup import start_slack_oauth

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # When: Requesting OAuth start (must mock both config and handler)
        with patch("services.integrations.slack.config_service.SlackConfigService") as MockConfig:
            # Mock config service to return valid credentials
            mock_config_instance = MagicMock()
            mock_config = MagicMock()
            mock_config.client_id = "test_client_id"
            mock_config.client_secret = "test_client_secret"
            mock_config_instance.get_config.return_value = mock_config
            MockConfig.return_value = mock_config_instance

            with patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler"
            ) as MockHandler:
                mock_instance = MagicMock()
                # Simulating URL with scopes parameter
                # Issue #1109: generate_authorization_url is async → AsyncMock
                mock_instance.generate_authorization_url = AsyncMock(
                    return_value=(
                        "https://slack.com/oauth/v2/authorize?client_id=test&scope=chat:write,channels:read",
                        "state_xyz789",
                    )
                )
                MockHandler.return_value = mock_instance

                response = await start_slack_oauth(current_user=mock_user)

        # Then: URL should contain scope parameter
        assert "scope=" in response["auth_url"]


class TestSlackOAuthCallback:
    """Tests for OAuth callback handling in setup context"""

    @pytest.mark.asyncio
    async def test_callback_success_redirects_to_setup_with_success(self):
        """Successful callback should redirect to setup with success params"""
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_slack_oauth_callback

        # When: Handling successful callback
        with patch("services.integrations.slack.oauth_handler.SlackOAuthHandler") as MockHandler:
            mock_instance = MagicMock()
            mock_instance.handle_oauth_callback = AsyncMock(
                return_value={
                    "workspace": {"workspace_name": "Test Workspace", "workspace_id": "T12345"}
                }
            )
            MockHandler.return_value = mock_instance

            response = await handle_slack_oauth_callback(
                code="test_code_123", state="valid_state_abc", error=None
            )

        # Then: Redirects to setup with success
        assert isinstance(response, RedirectResponse)
        assert response.status_code == 302
        assert "slack_success=true" in str(response.headers.get("location", ""))
        assert "Test%20Workspace" in str(
            response.headers.get("location", "")
        ) or "Test+Workspace" in str(response.headers.get("location", ""))

    @pytest.mark.asyncio
    async def test_callback_error_redirects_to_setup_with_error(self):
        """OAuth error should redirect with error message"""
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_slack_oauth_callback

        # When: Callback has error parameter
        response = await handle_slack_oauth_callback(code=None, state=None, error="access_denied")

        # Then: Redirects with error
        assert isinstance(response, RedirectResponse)
        assert response.status_code == 302
        assert "slack_error=access_denied" in str(response.headers.get("location", ""))

    @pytest.mark.asyncio
    async def test_callback_missing_params_returns_error(self):
        """Missing code/state should return error redirect"""
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_slack_oauth_callback

        # When: Callback missing required params
        response = await handle_slack_oauth_callback(code=None, state=None, error=None)

        # Then: Redirects with missing_params error
        assert isinstance(response, RedirectResponse)
        assert "slack_error=missing_params" in str(response.headers.get("location", ""))

    @pytest.mark.asyncio
    async def test_callback_invalid_state_returns_error(self):
        """Invalid/expired state should return clear error"""
        from starlette.responses import RedirectResponse

        from web.api.routes.setup import handle_slack_oauth_callback

        # When: Callback with invalid state
        with patch("services.integrations.slack.oauth_handler.SlackOAuthHandler") as MockHandler:
            mock_instance = MagicMock()
            mock_instance.handle_oauth_callback = AsyncMock(
                side_effect=ValueError("Invalid or expired state")
            )
            MockHandler.return_value = mock_instance

            response = await handle_slack_oauth_callback(
                code="test_code", state="expired_state", error=None
            )

        # Then: Redirects with callback_failed error
        assert isinstance(response, RedirectResponse)
        assert "slack_error=callback_failed" in str(response.headers.get("location", ""))


class TestSlackSetupStatus:
    """Tests for Slack status in setup wizard"""

    @pytest.mark.asyncio
    async def test_check_slack_configured_with_token(self):
        """Should return configured=True when bot token exists"""
        from web.api.routes.setup import get_slack_status

        # When: Slack has bot token configured
        with patch("services.integrations.slack.config_service.SlackConfigService") as MockConfig:
            mock_instance = MagicMock()
            mock_config = MagicMock()
            mock_config.bot_token = "xoxb-test-token"
            mock_instance.get_config.return_value = mock_config
            MockConfig.return_value = mock_instance

            response = await get_slack_status()

        # Then: Status is configured
        assert response["configured"] is True

    @pytest.mark.asyncio
    async def test_check_slack_not_configured(self):
        """Should return configured=False when no token"""
        from web.api.routes.setup import get_slack_status

        # When: Slack has no bot token
        with patch("services.integrations.slack.config_service.SlackConfigService") as MockConfig:
            mock_instance = MagicMock()
            mock_config = MagicMock()
            mock_config.bot_token = None
            mock_instance.get_config.return_value = mock_config
            MockConfig.return_value = mock_instance

            response = await get_slack_status()

        # Then: Status is not configured
        assert response["configured"] is False


class TestSlackOAuthStartEndpoint:
    """Tests for /setup/slack/oauth/start endpoint"""

    @pytest.mark.asyncio
    async def test_start_endpoint_returns_json(self):
        """Endpoint should return JSON with auth_url"""
        from web.api.routes.setup import start_slack_oauth

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch("services.integrations.slack.config_service.SlackConfigService") as MockConfig:
            # Mock config service to return valid credentials
            mock_config_instance = MagicMock()
            mock_config = MagicMock()
            mock_config.client_id = "test_client_id"
            mock_config.client_secret = "test_client_secret"
            mock_config_instance.get_config.return_value = mock_config
            MockConfig.return_value = mock_config_instance

            with patch(
                "services.integrations.slack.oauth_handler.SlackOAuthHandler"
            ) as MockHandler:
                mock_instance = MagicMock()
                # Issue #1109: generate_authorization_url is async → AsyncMock
                mock_instance.generate_authorization_url = AsyncMock(
                    return_value=(
                        "https://slack.com/oauth/v2/authorize?test=1",
                        "test_state",
                    )
                )
                MockHandler.return_value = mock_instance

                result = await start_slack_oauth(current_user=mock_user)

        assert isinstance(result, dict)
        assert "auth_url" in result
        assert "state" in result

    @pytest.mark.asyncio
    async def test_start_uses_setup_redirect_uri_env(self):
        """Should use SLACK_SETUP_REDIRECT_URI if available"""
        import os

        from web.api.routes.setup import start_slack_oauth

        # Issue #734: Mock current_user with user_id
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # When: SLACK_SETUP_REDIRECT_URI is set
        with patch.dict(
            os.environ,
            {
                "SLACK_SETUP_REDIRECT_URI": "http://localhost:8001/setup/slack/oauth/callback",
                "SLACK_REDIRECT_URI": "http://localhost:8001/slack/oauth/callback",
            },
        ):
            with patch(
                "services.integrations.slack.config_service.SlackConfigService"
            ) as MockConfig:
                # Mock config service to return valid credentials
                mock_config_instance = MagicMock()
                mock_config = MagicMock()
                mock_config.client_id = "test_client_id"
                mock_config.client_secret = "test_client_secret"
                mock_config_instance.get_config.return_value = mock_config
                MockConfig.return_value = mock_config_instance

                with patch(
                    "services.integrations.slack.oauth_handler.SlackOAuthHandler"
                ) as MockHandler:
                    mock_instance = MagicMock()
                    # Issue #1109: generate_authorization_url is async → AsyncMock
                    mock_instance.generate_authorization_url = AsyncMock(
                        return_value=(
                            "https://slack.com/oauth/v2/authorize",
                            "state",
                        )
                    )
                    MockHandler.return_value = mock_instance

                    await start_slack_oauth(current_user=mock_user)

                    # Then: Handler should be called with user_id
                    mock_instance.generate_authorization_url.assert_called_once()
