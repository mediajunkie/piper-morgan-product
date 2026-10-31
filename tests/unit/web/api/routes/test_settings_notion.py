"""
Unit tests for Notion Settings API
Issue #540: ALPHA-SETUP-NOTION stuck state recovery

Tests the Notion API key management endpoints in settings_integrations.py.
"""

from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from web.api.routes.settings_integrations import (
    disconnect_notion,
    get_notion_settings,
    save_notion_key,
)


@dataclass
class MockJWTClaims:
    """Minimal JWT claims mock for testing - Issue #746."""

    user_id: UUID
    user_email: str = "test@example.com"
    sub: str = "test-user-123"


class TestGetNotionSettings:
    """Tests for GET /api/v1/settings/integrations/notion"""

    @pytest.mark.asyncio
    async def test_returns_not_configured_when_no_key(self):
        """Should return configured=False when no API key in keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await get_notion_settings(current_user=mock_user)

            assert result["configured"] is False
            assert result["valid"] is False
            assert result["workspace"] is None
            assert result["error"] is None
            # Issue #849: Verify user-scoped key retrieval
            mock_keychain.get_api_key.assert_called_once_with("notion", username="test-user-123")

    @pytest.mark.asyncio
    async def test_returns_configured_and_valid_when_key_valid(self):
        """Should return configured=True, valid=True when API key validates"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "secret_test_key"

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "web.api.routes.setup.validate_notion_key_and_get_workspace",
                new_callable=AsyncMock,
                return_value=(True, "Test Workspace", None),
            ) as mock_validate,
        ):
            result = await get_notion_settings(current_user=mock_user)

            assert result["configured"] is True
            assert result["valid"] is True
            assert result["workspace"] == "Test Workspace"
            assert result["error"] is None
            mock_validate.assert_called_once_with("secret_test_key")

    @pytest.mark.asyncio
    async def test_returns_configured_but_invalid_when_key_fails(self):
        """Should return configured=True, valid=False when API key is invalid (stuck state)"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "secret_expired_key"

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "web.api.routes.setup.validate_notion_key_and_get_workspace",
                new_callable=AsyncMock,
                return_value=(False, None, "API key is invalid"),
            ),
        ):
            result = await get_notion_settings(current_user=mock_user)

            assert result["configured"] is True
            assert result["valid"] is False
            assert result["workspace"] is None
            assert result["error"] == "API key is invalid"


class TestSaveNotionKey:
    """Tests for POST /api/v1/settings/integrations/notion/save"""

    @pytest.fixture
    def mock_current_user(self):
        """Create mock JWT claims for authenticated user - Issue #746."""
        return MockJWTClaims(user_id=uuid4())

    @pytest.mark.asyncio
    async def test_rejects_invalid_key(self, mock_current_user):
        """Should return 400 when API key validation fails"""
        with patch(
            "web.api.routes.setup.validate_notion_key_and_get_workspace",
            new_callable=AsyncMock,
            return_value=(False, None, "Invalid API key"),
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await save_notion_key("secret_invalid_key", mock_current_user)

            assert exc_info.value.status_code == 400
            assert "Invalid API key" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_saves_valid_key_and_returns_success(self, mock_current_user):
        """Should store key and return success when validation passes"""
        mock_service = MagicMock()
        mock_service.store_user_key = AsyncMock(return_value=MagicMock())

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)

        with (
            patch(
                "web.api.routes.setup.validate_notion_key_and_get_workspace",
                new_callable=AsyncMock,
                return_value=(True, "My Workspace", None),
            ),
            patch("services.database.session_factory.AsyncSessionFactory") as mock_session_factory,
            patch(
                "services.security.user_api_key_service.UserAPIKeyService",
                return_value=mock_service,
            ),
        ):
            # Setup session context manager
            mock_session_factory.session_scope_fresh.return_value = mock_session

            result = await save_notion_key("secret_valid_key", mock_current_user)

            assert result["success"] is True
            assert result["workspace"] == "My Workspace"
            assert "My Workspace" in result["message"]


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


def _notion_store_ok():
    """The #358 user-key store clears cleanly (no DB in a unit test)."""
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=AsyncMock())
    scope.__aexit__ = AsyncMock(return_value=False)
    factory = MagicMock()
    factory.session_scope_fresh.return_value = scope
    svc = MagicMock()
    svc.delete_user_key = AsyncMock(return_value=True)
    from contextlib import ExitStack

    stack = ExitStack()
    stack.enter_context(patch("services.database.session_factory.AsyncSessionFactory", factory))
    stack.enter_context(
        patch("services.security.user_api_key_service.UserAPIKeyService", return_value=svc)
    )
    return stack


class TestDisconnectNotion:
    """Tests for POST /api/v1/settings/integrations/notion/disconnect"""

    @pytest.mark.asyncio
    async def test_disconnects_and_returns_success(self):
        """Should remove key from keychain and return success"""
        mock_keychain = _async_keychain()

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            _notion_store_ok(),
        ):
            result = await disconnect_notion(current_user=mock_user)

            assert result["success"] is True
            assert result["message"] == "Notion disconnected"
            # Issue #849: Verify user-scoped key deletion
            mock_keychain.adelete_api_key.assert_awaited_once_with("notion", "test-user-123")

    @pytest.mark.asyncio
    async def test_handles_missing_key_gracefully(self):
        """Should succeed even if no key exists to delete"""
        mock_keychain = _async_keychain()
        mock_keychain.adelete_api_key.side_effect = KeyError("notion")

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            _notion_store_ok(),
        ):
            result = await disconnect_notion(current_user=mock_user)

            # Should still succeed - key not existing is fine
            assert result["success"] is True
            assert result["message"] == "Notion disconnected"


class TestIntegrationRegistryNotionUrl:
    """Tests for Notion configure_url in INTEGRATION_REGISTRY (Issue #540)"""

    def test_notion_configure_url_points_to_settings_page(self):
        """Notion configure_url should point to dedicated settings page, not setup wizard"""
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        notion_config = INTEGRATION_REGISTRY.get("notion")
        assert notion_config is not None
        assert notion_config["configure_url"] == "/settings/integrations/notion"
        # Should NOT point to setup wizard
        assert notion_config["configure_url"] != "/setup#step-2"


class TestNotionConfigServiceKeychainFallback:
    """Tests for NotionConfigService keychain fallback (Issue #579)"""

    def test_get_config_returns_env_var_first(self):
        """Should return env var API key when available (priority over keychain)"""
        from services.integrations.notion.config_service import NotionConfigService

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "secret_keychain_key"

        with (
            patch.dict("os.environ", {"NOTION_API_KEY": "secret_env_key"}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            config_service = NotionConfigService()
            config_service._config = None  # Ensure fresh lookup
            # Issue #734: Now requires user_id
            config = config_service.get_config(user_id="test-user-123")

            assert config.api_key == "secret_env_key"
            # Keychain should NOT be called when env var is present
            mock_keychain.get_api_key.assert_not_called()

    def test_get_config_falls_back_to_keychain(self):
        """Should fall back to keychain when no env var is set (Issue #579)"""
        from services.integrations.notion.config_service import NotionConfigService

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "secret_keychain_key"

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            config_service = NotionConfigService()
            config_service._config = None  # Ensure fresh lookup
            # Issue #734: Now requires user_id
            config = config_service.get_config(user_id="test-user-123")

            assert config.api_key == "secret_keychain_key"
            # Issue #734: Now passes user_id to keychain
            mock_keychain.get_api_key.assert_called_once_with("notion", username="test-user-123")

    def test_get_config_returns_empty_when_nothing_configured(self):
        """Should return empty string when neither env var nor keychain has key"""
        from services.integrations.notion.config_service import NotionConfigService

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            config_service = NotionConfigService()
            config_service._config = None  # Ensure fresh lookup
            # Issue #734: Now requires user_id
            config = config_service.get_config(user_id="test-user-123")

            assert config.api_key == ""

    def test_get_config_handles_keychain_error_gracefully(self):
        """Should return empty string if keychain throws an error"""
        from services.integrations.notion.config_service import NotionConfigService

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.side_effect = Exception("Keychain unavailable")

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            config_service = NotionConfigService()
            config_service._config = None  # Ensure fresh lookup
            # Issue #734: Now requires user_id
            config = config_service.get_config(user_id="test-user-123")

            # Should gracefully return empty string, not raise
            assert config.api_key == ""


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
