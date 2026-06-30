"""
Unit tests for Integration Health Check API
Issue #530: ALPHA-SETUP-VERIFY

Tests the integration health dashboard API endpoints following TDD approach.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.integrations import (
    INTEGRATION_REGISTRY,
    ConnectionTestResponse,
    IntegrationHealthResponse,
    IntegrationStatus,
    _check_integration_health,
    _get_integration_config_status,
    _test_calendar,
    _test_github,
    _test_notion,
    _test_slack,
    check_all_connections,
    check_integration_connection,
    get_integrations_health,
)


class TestIntegrationHealthEndpoint:
    """Tests for GET /api/v1/integrations/health"""

    @pytest.fixture
    def mock_user(self):
        """The endpoint now requires auth (current_user: JWTClaims) and reads
        current_user.sub. Calling it directly must pass a user (matching the
        sibling TestIntegrationConnectionTesting tests); otherwise current_user
        defaults to the Depends() sentinel → 'Depends' object has no attribute 'sub'."""
        user = MagicMock()
        user.sub = "test-user-123"
        return user

    @pytest.mark.asyncio
    async def test_health_returns_all_integrations(self, mock_user):
        """Health endpoint should return status for all 4 integrations"""
        response = await get_integrations_health(current_user=mock_user)

        assert isinstance(response, IntegrationHealthResponse)
        assert response.total_count == 4
        assert len(response.integrations) == 4

        # Verify all expected integrations are present
        integration_names = {i.name for i in response.integrations}
        assert integration_names == {"notion", "slack", "github", "calendar"}

    @pytest.mark.asyncio
    async def test_health_returns_valid_timestamp(self, mock_user):
        """Health response should include valid ISO timestamp"""
        response = await get_integrations_health(current_user=mock_user)

        # Should parse without error
        timestamp = datetime.fromisoformat(response.timestamp)
        assert timestamp is not None

    @pytest.mark.asyncio
    async def test_health_calculates_overall_status_correctly(self, mock_user):
        """Overall status should be healthy/degraded/unhealthy based on counts"""
        response = await get_integrations_health(current_user=mock_user)

        # Verify overall status logic
        if response.healthy_count == response.total_count:
            assert response.overall_status == "healthy"
        elif response.healthy_count > 0:
            assert response.overall_status == "degraded"
        else:
            assert response.overall_status == "unhealthy"

    @pytest.mark.asyncio
    async def test_health_integration_has_required_fields(self, mock_user):
        """Each integration should have all required fields"""
        response = await get_integrations_health(current_user=mock_user)

        for integration in response.integrations:
            assert integration.name is not None
            assert integration.display_name is not None
            assert integration.status in [
                "healthy",
                "degraded",
                "failed",
                "unknown",
                "not_configured",
            ]
            assert integration.status_message is not None
            assert isinstance(integration.can_test, bool)


class TestIntegrationConfigStatus:
    """Tests for configuration status checking"""

    @pytest.mark.asyncio
    async def test_notion_configured_with_token(self):
        """Notion should be configured when NOTION_API_TOKEN is set"""
        with patch.dict("os.environ", {"NOTION_API_TOKEN": "test_token"}):
            status = await _get_integration_config_status("notion")
            assert status == "configured"

    @pytest.mark.asyncio
    async def test_notion_configured_with_api_key(self):
        """Notion should be configured when NOTION_API_KEY is set"""
        with patch.dict("os.environ", {"NOTION_API_KEY": "test_key"}, clear=True):
            status = await _get_integration_config_status("notion")
            assert status == "configured"

    @pytest.mark.asyncio
    async def test_notion_not_configured_without_env(self):
        """Notion should be not_configured when no env vars set"""
        with patch.dict("os.environ", {}, clear=True):
            status = await _get_integration_config_status("notion")
            assert status == "not_configured"

    @pytest.mark.asyncio
    async def test_github_configured_with_token(self):
        """GitHub should be configured when GITHUB_TOKEN is set"""
        with patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_test"}, clear=True):
            status = await _get_integration_config_status("github")
            assert status == "configured"

    @pytest.mark.asyncio
    async def test_slack_configured_with_bot_token(self):
        """Slack should be configured when SLACK_BOT_TOKEN is set"""
        with patch.dict("os.environ", {"SLACK_BOT_TOKEN": "xoxb-test"}, clear=True):
            status = await _get_integration_config_status("slack")
            assert status == "configured"

    @pytest.mark.asyncio
    async def test_calendar_configured_with_mcp(self):
        """Calendar should be configured when MCP_ENABLED is set"""
        with patch.dict("os.environ", {"MCP_ENABLED": "true"}, clear=True):
            status = await _get_integration_config_status("calendar")
            assert status == "configured"

    @pytest.mark.asyncio
    async def test_notion_configured_via_user_scoped_key_1337(self):
        """#1337: UI-configured Notion (user-scoped #358 store) must read 'configured' —
        the notion branch was env-only and missed the user-scoped key save_notion_key writes."""
        mock_session = AsyncMock()
        mock_scope = MagicMock()
        mock_scope.__aenter__ = AsyncMock(return_value=mock_session)
        mock_scope.__aexit__ = AsyncMock(return_value=False)
        mock_factory = MagicMock()
        mock_factory.session_scope_fresh.return_value = mock_scope
        mock_svc = MagicMock()
        mock_svc.retrieve_user_key = AsyncMock(return_value="secret-notion-key")

        with (
            patch.dict("os.environ", {}, clear=True),
            patch("services.database.session_factory.AsyncSessionFactory", mock_factory),
            patch(
                "services.security.user_api_key_service.UserAPIKeyService",
                return_value=mock_svc,
            ),
        ):
            status = await _get_integration_config_status("notion", user_id="user-123")

        assert status == "configured"
        mock_svc.retrieve_user_key.assert_awaited_once()
        args, _ = mock_svc.retrieve_user_key.call_args
        assert args[1] == "user-123" and args[2] == "notion"

    @pytest.mark.asyncio
    async def test_notion_not_configured_when_no_user_key_1337(self):
        """#1337: no env var + no user-scoped key → stays not_configured (no false positive)."""
        mock_session = AsyncMock()
        mock_scope = MagicMock()
        mock_scope.__aenter__ = AsyncMock(return_value=mock_session)
        mock_scope.__aexit__ = AsyncMock(return_value=False)
        mock_factory = MagicMock()
        mock_factory.session_scope_fresh.return_value = mock_scope
        mock_svc = MagicMock()
        mock_svc.retrieve_user_key = AsyncMock(return_value=None)

        with (
            patch.dict("os.environ", {}, clear=True),
            patch("services.database.session_factory.AsyncSessionFactory", mock_factory),
            patch(
                "services.security.user_api_key_service.UserAPIKeyService",
                return_value=mock_svc,
            ),
        ):
            status = await _get_integration_config_status("notion", user_id="user-123")

        assert status == "not_configured"


class TestSingleIntegrationTest:
    """Tests for POST /api/v1/integrations/test/{integration_name}"""

    @pytest.mark.asyncio
    async def test_unknown_integration_raises_404(self):
        """Testing unknown integration should raise 404"""
        from fastapi import HTTPException

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with pytest.raises(HTTPException) as exc_info:
            await check_integration_connection("unknown_integration", current_user=mock_user)

        assert exc_info.value.status_code == 404
        assert "Unknown integration" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_successful_connection_returns_success(self):
        """Successful connection test should return success=True with latency"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch("web.api.routes.integrations._test_notion", new_callable=AsyncMock) as mock_test:
            mock_test.return_value = {"success": True}

            response = await check_integration_connection("notion", current_user=mock_user)

            assert response.success is True
            assert response.integration == "notion"
            assert response.latency_ms is not None
            assert response.latency_ms >= 0

    @pytest.mark.asyncio
    async def test_failed_connection_returns_error_guidance(self):
        """Failed connection should return error message and fix suggestion"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch("web.api.routes.integrations._test_notion", new_callable=AsyncMock) as mock_test:
            mock_test.return_value = {
                "success": False,
                "error_type": "api_key_invalid",
                "error": "Invalid token",
            }

            response = await check_integration_connection("notion", current_user=mock_user)

            assert response.success is False
            assert response.integration == "notion"
            assert response.message is not None
            assert response.fix_suggestion is not None

    @pytest.mark.asyncio
    async def test_connection_exception_handled_gracefully(self):
        """Exceptions during test should be caught and return proper response"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch("web.api.routes.integrations._test_notion", new_callable=AsyncMock) as mock_test:
            mock_test.side_effect = Exception("Network error")

            response = await check_integration_connection("notion", current_user=mock_user)

            assert response.success is False
            assert "Network error" in response.message or "Network error" in str(response.error)


class TestAllConnectionsEndpoint:
    """Tests for POST /api/v1/integrations/test-all"""

    @pytest.mark.asyncio
    async def test_test_all_returns_results_for_all_integrations(self):
        """Test all should return results for each integration"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "web.api.routes.integrations._test_integration", new_callable=AsyncMock
        ) as mock_test:
            mock_test.return_value = {"success": True}

            results = await check_all_connections(current_user=mock_user)

            assert len(results) == 4
            integration_names = {r.integration for r in results}
            assert integration_names == {"notion", "slack", "github", "calendar"}

    @pytest.mark.asyncio
    async def test_test_all_continues_after_individual_failure(self):
        """Test all should continue testing even if one fails"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        call_count = 0

        async def mock_test_with_failure(name, user_id=None):
            nonlocal call_count
            call_count += 1
            if name == "notion":
                return {"success": False, "error": "Failed"}
            return {"success": True}

        with patch(
            "web.api.routes.integrations._test_integration", side_effect=mock_test_with_failure
        ):
            results = await check_all_connections(current_user=mock_user)

            # Should have tested all 4 integrations
            assert len(results) == 4
            # At least one should have failed
            failed = [r for r in results if not r.success]
            assert len(failed) >= 1


class TestNotionIntegration:
    """Tests for Notion-specific test logic (Issue #562: Uses stored API key)"""

    @pytest.mark.asyncio
    async def test_notion_success_when_api_valid(self):
        """Notion test should return success when API key is valid (Issue #562)"""
        mock_config = MagicMock()
        mock_config.api_key = "test_api_key"

        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config

        mock_response = AsyncMock()
        mock_response.status = 200

        mock_session_instance = MagicMock()
        mock_session_instance.get = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.integrations.notion.config_service.NotionConfigService",
                return_value=mock_config_service,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
        ):
            result = await _test_notion()

            assert result["success"] is True

    @pytest.mark.asyncio
    async def test_notion_failure_when_api_key_invalid(self):
        """Notion test should return api_key_invalid error type when API returns non-200 (Issue #562)"""
        mock_config = MagicMock()
        mock_config.api_key = "invalid_api_key"

        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config

        mock_response = AsyncMock()
        mock_response.status = 401

        mock_session_instance = MagicMock()
        mock_session_instance.get = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.integrations.notion.config_service.NotionConfigService",
                return_value=mock_config_service,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
        ):
            result = await _test_notion()

            assert result["success"] is False
            assert result["error_type"] == "api_key_invalid"

    @pytest.mark.asyncio
    async def test_notion_not_configured_when_no_api_key(self):
        """Notion test should return not_configured when no API key stored (Issue #562)"""
        mock_config = MagicMock()
        mock_config.api_key = None

        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config

        with patch(
            "services.integrations.notion.config_service.NotionConfigService",
            return_value=mock_config_service,
        ):
            result = await _test_notion()

            assert result["success"] is False
            assert result["error_type"] == "not_configured"
            assert "not connected" in result["error"].lower()


class TestGitHubIntegration:
    """Tests for GitHub-specific test logic (Issue #562: Uses stored PAT)"""

    @pytest.mark.asyncio
    async def test_github_success_when_token_valid(self):
        """GitHub test should succeed when stored PAT is valid (Issue #562)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "ghp_test_token"

        mock_response = AsyncMock()
        mock_response.status = 200

        mock_session_instance = MagicMock()
        mock_session_instance.get = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
        ):
            result = await _test_github()

            assert result["success"] is True

    @pytest.mark.asyncio
    async def test_github_failure_when_token_invalid(self):
        """GitHub test should fail when token returns 401 (Issue #562)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "invalid_token"

        mock_response = AsyncMock()
        mock_response.status = 401

        mock_session_instance = MagicMock()
        mock_session_instance.get = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
        ):
            result = await _test_github()

            assert result["success"] is False
            assert result["error_type"] == "token_invalid"

    @pytest.mark.asyncio
    async def test_github_not_configured_when_no_token(self):
        """GitHub test should return not_configured when no token stored (Issue #562)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await _test_github()

            assert result["success"] is False
            assert result["error_type"] == "not_configured"
            assert "not connected" in result["error"].lower()


class TestSlackIntegration:
    """Tests for Slack-specific test logic (Issue #562: Uses stored OAuth token)"""

    @pytest.mark.asyncio
    async def test_slack_success_when_token_valid(self):
        """Slack test should succeed when stored OAuth token is valid (Issue #562)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "xoxb-test-token"

        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"ok": True})

        mock_session_instance = MagicMock()
        mock_session_instance.get = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
        ):
            result = await _test_slack()

            assert result["success"] is True

    @pytest.mark.asyncio
    async def test_slack_failure_when_token_invalid(self):
        """Slack test should fail and include error when API returns ok=False (Issue #562)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "invalid_token"

        mock_response = AsyncMock()
        mock_response.json = AsyncMock(return_value={"ok": False, "error": "invalid_auth"})

        mock_session_instance = MagicMock()
        mock_session_instance.get = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
        ):
            result = await _test_slack()

            assert result["success"] is False
            assert result["error"] == "invalid_auth"
            assert result["error_type"] == "token_invalid"

    @pytest.mark.asyncio
    async def test_slack_not_configured_when_no_token(self):
        """Slack test should return not_configured when no token stored (Issue #562)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await _test_slack()

            assert result["success"] is False
            assert result["error_type"] == "not_configured"
            assert "not connected" in result["error"].lower()


class TestCalendarIntegration:
    """Tests for Calendar-specific test logic (Issue #539: OAuth token validation)"""

    @pytest.mark.asyncio
    async def test_calendar_success_when_token_valid(self):
        """Calendar test should succeed when OAuth token can be refreshed"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "valid_refresh_token"

        mock_handler = MagicMock()
        mock_handler.refresh_access_token = AsyncMock(
            return_value=MagicMock(access_token="new_access_token")
        )

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=mock_handler,
            ),
        ):
            result = await _test_calendar()

            assert result["success"] is True
            mock_keychain.get_api_key.assert_called_once_with("google_calendar")
            mock_handler.refresh_access_token.assert_called_once_with("valid_refresh_token")

    @pytest.mark.asyncio
    async def test_calendar_failure_when_not_configured(self):
        """Calendar test should fail when no refresh token in keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await _test_calendar()

            assert result["success"] is False
            assert result["error_type"] == "not_configured"
            assert "not connected" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_calendar_failure_when_token_invalid(self):
        """Calendar test should fail when token refresh fails (Issue #539)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "expired_refresh_token"

        mock_handler = MagicMock()
        mock_handler.refresh_access_token = AsyncMock(return_value=None)

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=mock_handler,
            ),
        ):
            result = await _test_calendar()

            assert result["success"] is False
            assert result["error_type"] == "token_invalid"
            assert "expired" in result["error"].lower() or "revoked" in result["error"].lower()


class TestIntegrationRegistry:
    """Tests for the INTEGRATION_REGISTRY configuration"""

    def test_registry_has_all_integrations(self):
        """Registry should have all 4 integrations"""
        assert "notion" in INTEGRATION_REGISTRY
        assert "slack" in INTEGRATION_REGISTRY
        assert "github" in INTEGRATION_REGISTRY
        assert "calendar" in INTEGRATION_REGISTRY

    def test_registry_has_display_names(self):
        """Each integration should have a display_name"""
        for name, config in INTEGRATION_REGISTRY.items():
            assert "display_name" in config
            assert isinstance(config["display_name"], str)

    def test_registry_has_configure_urls(self):
        """Each integration should have a configure_url key (may be None for OAuth)"""
        for name, config in INTEGRATION_REGISTRY.items():
            assert "configure_url" in config
            # Configure URLs can be settings pages, setup wizard (Issue #527), or
            # None for OAuth integrations (Issue #529 - Slack, Calendar)
            url = config["configure_url"]
            if url is not None:
                assert url.startswith("/settings/integrations/") or url.startswith("/setup")

    def test_registry_has_error_guidance(self):
        """Each integration should have error guidance"""
        for name, config in INTEGRATION_REGISTRY.items():
            assert "errors" in config
            assert isinstance(config["errors"], dict)
            # Should have at least one error type defined
            assert len(config["errors"]) >= 1
