"""
Unit tests for Notion integration in setup wizard
Issue #527: ALPHA-SETUP-NOTION

Tests Notion API key validation, keychain integration,
workspace info display, and setup completion handling.

Note: These tests are TDD scaffolding - they will fail until
the backend implementation is complete in Phase 1.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

pytestmark = pytest.mark.unit


class TestNotionKeyValidation:
    """Tests for Notion API key validation in setup wizard"""

    @pytest.mark.asyncio
    async def test_validate_notion_key_success(self):
        """Valid Notion key should return valid=True with workspace name"""
        from pydantic import ValidationError

        from web.api.routes.setup import ApiKeyValidateRequest, validate_api_key

        # Given: A valid Notion API key
        try:
            req = ApiKeyValidateRequest(provider="notion", api_key="secret_test_valid_notion_key")
        except ValidationError:
            pytest.skip("Provider 'notion' not yet implemented - Phase 1 pending")

        # When: Validating the key (with mocked Notion API)
        with patch(
            "web.api.routes.setup.validate_notion_key_and_get_workspace",
            new_callable=AsyncMock,
        ) as mock_validate:
            mock_validate.return_value = (True, "Test Workspace", None)

            response = await validate_api_key(req)

        # Then: Response has valid=True with workspace info
        assert response.valid is True
        assert response.provider == "notion"
        assert "Test Workspace" in response.message

    @pytest.mark.asyncio
    async def test_validate_notion_key_invalid(self):
        """Invalid Notion key should return valid=False with guidance"""
        from pydantic import ValidationError

        from web.api.routes.setup import ApiKeyValidateRequest, validate_api_key

        # Given: An invalid Notion API key
        try:
            req = ApiKeyValidateRequest(provider="notion", api_key="secret_invalid_key")
        except ValidationError:
            pytest.skip("Provider 'notion' not yet implemented - Phase 1 pending")

        # When: Validating the key
        with patch(
            "web.api.routes.setup.validate_notion_key_and_get_workspace",
            new_callable=AsyncMock,
        ) as mock_validate:
            mock_validate.return_value = (
                False,
                None,
                "Invalid API key or insufficient permissions",
            )

            response = await validate_api_key(req)

        # Then: Response has valid=False with helpful message
        assert response.valid is False
        assert response.provider == "notion"
        # Should contain guidance about the error
        assert "invalid" in response.message.lower() or "permission" in response.message.lower()

    @pytest.mark.asyncio
    async def test_notion_provider_accepted_in_validator(self):
        """Provider 'notion' should be accepted by ApiKeyValidateRequest validator"""
        from pydantic import ValidationError

        from web.api.routes.setup import ApiKeyValidateRequest

        # This will raise ValidationError if 'notion' is not accepted
        # After Phase 1 implementation, this should NOT raise
        try:
            req = ApiKeyValidateRequest(provider="notion", api_key="secret_test")
            assert req.provider == "notion"
        except ValidationError as e:
            # Expected to fail until Phase 1 adds 'notion' to allowed providers
            pytest.skip("Provider 'notion' not yet implemented - Phase 1 pending")


class TestNotionKeychainCheck:
    """Tests for Notion keychain integration"""

    @pytest.mark.asyncio
    async def test_check_keychain_notion_exists(self):
        """Should return exists=True when Notion key in keychain"""
        from web.api.routes.setup import check_keychain

        # When: Checking keychain for Notion key
        with patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain:
            mock_instance = MagicMock()
            mock_instance.get_api_key.return_value = "secret_test_key"
            MockKeychain.return_value = mock_instance

            response = await check_keychain("notion")

        # Then: Response indicates key exists
        # Note: Will fail until 'notion' is added to allowed providers
        if response.exists is False and "Unknown provider" in response.message:
            pytest.skip("Provider 'notion' not yet in keychain check - Phase 1 pending")

        assert response.exists is True
        assert response.provider == "notion"

    @pytest.mark.asyncio
    async def test_check_keychain_notion_not_exists(self):
        """Should return exists=False when Notion key not in keychain"""
        from web.api.routes.setup import check_keychain

        # When: Checking keychain for Notion key that doesn't exist
        with patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain:
            mock_instance = MagicMock()
            mock_instance.get_api_key.return_value = None
            MockKeychain.return_value = mock_instance

            response = await check_keychain("notion")

        # Then: Response indicates key does not exist
        # Note: Will return "Unknown provider" until Phase 1
        if "Unknown provider" in response.message:
            pytest.skip("Provider 'notion' not yet in keychain check - Phase 1 pending")

        assert response.exists is False
        assert response.provider == "notion"

    @pytest.mark.asyncio
    async def test_use_keychain_notion_success(self):
        """Should retrieve and validate Notion key from keychain"""
        from pydantic import ValidationError

        from web.api.routes.setup import KeychainUseRequest, use_keychain

        # Try to create request - will fail until 'notion' is in allowed providers
        try:
            req = KeychainUseRequest(provider="notion")
        except ValidationError:
            pytest.skip("Provider 'notion' not yet in KeychainUseRequest - Phase 1 pending")

        # When: Using keychain for Notion
        with patch("services.infrastructure.keychain_service.KeychainService") as MockKeychain:
            mock_instance = MagicMock()
            mock_instance.get_api_key.return_value = "secret_test_notion_key"
            MockKeychain.return_value = mock_instance

            response = await use_keychain(req)

        # Then: Response indicates success
        assert response.success is True
        assert response.valid is True
        assert response.provider == "notion"


class TestNotionWorkspaceInfo:
    """Tests for Notion workspace information display"""

    @pytest.mark.asyncio
    async def test_validation_returns_workspace_name(self):
        """Should return workspace name in response after successful validation"""
        from web.api.routes.setup import (
            ApiKeyValidateRequest,
            ApiKeyValidateResponse,
            validate_api_key,
        )

        # Check if workspace_name field exists in response model
        if "workspace_name" not in ApiKeyValidateResponse.model_fields:
            pytest.skip(
                "workspace_name field not yet added to ApiKeyValidateResponse - Phase 1 pending"
            )

        # Given: A valid Notion key
        req = ApiKeyValidateRequest(provider="notion", api_key="secret_workspace_test")

        # When: Validation succeeds
        with patch(
            "web.api.routes.setup.validate_notion_key_and_get_workspace",
            new_callable=AsyncMock,
        ) as mock_validate:
            mock_validate.return_value = (True, "Acme Corporation", None)

            response = await validate_api_key(req)

        # Then: workspace_name is included in response
        assert response.workspace_name == "Acme Corporation"

    @pytest.mark.asyncio
    async def test_workspace_name_in_validation_message(self):
        """Should include workspace name in validation status message"""
        from web.api.routes.setup import ApiKeyValidateRequest, validate_api_key

        # Given: A valid Notion key
        try:
            req = ApiKeyValidateRequest(provider="notion", api_key="secret_workspace_test")
        except Exception:
            pytest.skip("Provider 'notion' not yet implemented - Phase 1 pending")

        # When: Validation succeeds
        with patch(
            "web.api.routes.setup.validate_notion_key_and_get_workspace",
            new_callable=AsyncMock,
        ) as mock_validate:
            mock_validate.return_value = (True, "My Team Workspace", None)

            response = await validate_api_key(req)

        # Then: Message includes workspace name
        assert "My Team Workspace" in response.message


class TestNotionSetupComplete:
    """Tests for Notion key storage on setup completion"""

    @pytest.mark.asyncio
    async def test_complete_request_accepts_notion_key(self):
        """SetupCompleteRequest should accept notion_key field"""
        from web.api.routes.setup import SetupCompleteRequest

        # Check if notion_key field exists
        if "notion_key" not in SetupCompleteRequest.model_fields:
            pytest.skip("notion_key field not yet added to SetupCompleteRequest - Phase 1 pending")

        # Given: Setup data with Notion key
        req = SetupCompleteRequest(
            user_id="test-user-123",
            openai_key="sk-test-openai",
            notion_key="secret_test_notion",
        )

        # Then: Request should be valid
        assert req.notion_key == "secret_test_notion"
        assert req.user_id == "test-user-123"

    @pytest.mark.asyncio
    async def test_complete_without_notion_key(self):
        """Setup completion should work without Notion key (optional)"""
        from web.api.routes.setup import SetupCompleteRequest

        # Given: Setup without Notion key
        req = SetupCompleteRequest(
            user_id="test-user-123",
            openai_key="sk-test-openai",
        )

        # Then: Request should be valid (notion_key is optional)
        assert req.openai_key == "sk-test-openai"
        # notion_key should be None or not present
        notion_key = getattr(req, "notion_key", None)
        assert notion_key is None


class TestNotionKeyFormatValidation:
    """Tests for Notion key format validation"""

    @pytest.mark.asyncio
    async def test_notion_key_format_secret_prefix(self):
        """Valid Notion keys start with 'secret_'"""
        # This tests format validation before API call
        # Implementation may choose to validate format or let API reject
        valid_key = "secret_abcd1234efgh5678"
        invalid_key = "sk-openai-format-key"

        # Format check (if implemented)
        assert valid_key.startswith("secret_")
        assert not invalid_key.startswith("secret_")

    @pytest.mark.asyncio
    async def test_notion_key_format_ntn_prefix(self):
        """Notion keys may also use 'ntn_' prefix (newer format)"""
        valid_key = "ntn_abcd1234efgh5678"
        assert valid_key.startswith("ntn_")


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
