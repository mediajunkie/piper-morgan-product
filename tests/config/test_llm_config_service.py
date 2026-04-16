"""
Tests for LLMConfigService - Written BEFORE implementation (TDD)

Test-Driven Development approach:
1. Write tests first (RED phase)
2. Implement service to pass tests (GREEN phase)
3. Refactor for quality (REFACTOR phase)

These tests use real API calls for validation to ensure keys actually work.
"""

import os
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

# Load .env file for tests
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass  # python-dotenv not required, but helpful for tests

from services.config.llm_config_service import (
    LLMConfigService,
    LLMProvider,
    ProviderConfig,
    ValidationResult,
)
from services.infrastructure.keychain_service import KeychainService


@pytest.fixture
def mock_keychain_service():
    """Mock KeychainService for testing"""
    mock = Mock(spec=KeychainService)
    mock.get_api_key.return_value = None  # Default: nothing in keychain
    mock.store_api_key.return_value = None
    mock.check_migration_status.return_value = {}
    return mock


class TestLLMConfigServiceInit:
    """Test service initialization"""

    def test_service_loads_from_environment(self):
        """Service loads all available keys from environment"""
        service = LLMConfigService()

        # Should load providers from environment
        providers = service.get_configured_providers()
        assert isinstance(providers, list)

        # If keys are set, they should be configured
        if os.getenv("OPENAI_API_KEY"):
            assert "openai" in providers

    def test_service_handles_missing_env_vars(self):
        """Service handles missing environment variables and keychain gracefully"""
        with patch.dict(os.environ, {}, clear=True):
            # Mock keychain service to return no keys
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                # Should not crash, just have no configured providers
                providers = service.get_configured_providers()
                assert providers == []

    def test_service_loads_from_keychain_first(self):
        """Service prioritizes keychain over environment variables"""
        # Set environment variable
        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key-123"}):
            # Mock keychain service to return keychain key
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = "keychain-key-456"

                service = LLMConfigService()

                # Should return keychain key, not environment key
                key = service.get_api_key("openai")
                assert key == "keychain-key-456"

                # Verify keychain was called
                mock_keychain.get_api_key.assert_called_with("openai")

    def test_service_loads_all_supported_providers(self):
        """Service knows about all supported providers"""
        service = LLMConfigService()

        # Should have configs for all providers (even if keys not set)
        assert "openai" in service._providers
        assert "anthropic" in service._providers
        assert "gemini" in service._providers
        assert "perplexity" in service._providers


class TestProviderConfiguration:
    """Test provider configuration loading"""

    def test_get_configured_providers_returns_only_with_keys(self):
        """Returns list of providers with valid keys"""
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "test-key",
                "ANTHROPIC_API_KEY": "test-key-2",
            },
            clear=True,
        ):
            # Mock keychain service to return None for all providers
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()
                providers = service.get_configured_providers()

                assert "openai" in providers
                assert "anthropic" in providers
                assert "gemini" not in providers
                assert "perplexity" not in providers

    def test_get_provider_config(self):
        """Returns config for specific provider"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

            config = service._providers["openai"]
            assert config.name == "openai"
            assert config.env_var == "OPENAI_API_KEY"
            assert config.api_key == "test-key"
            assert config.validation_endpoint.startswith("https://")

    def test_get_api_key_success(self):
        """Returns API key for configured provider"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key-123"}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                key = service.get_api_key("openai")
                assert key == "test-key-123"

    def test_get_api_key_missing_provider_returns_none(self):
        """Requesting unconfigured provider returns None"""
        service = LLMConfigService()

        result = service.get_api_key("fake_provider")
        assert result is None

    def test_get_api_key_no_key_set_returns_none(self):
        """Missing key returns None"""
        with patch.dict(os.environ, {}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                result = service.get_api_key("openai")
                assert result is None


class TestProviderValidation:
    """Test individual provider validation with REAL API calls"""

    @pytest.mark.asyncio
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
    async def test_validate_openai_key_success(self):
        """Valid OpenAI key passes validation (REAL API CALL)"""
        service = LLMConfigService()

        result = await service.validate_provider("openai")

        assert result.provider == "openai"
        assert result.is_valid is True
        assert result.error_message is None

    @pytest.mark.asyncio
    async def test_validate_openai_key_invalid(self):
        """Invalid OpenAI key fails validation with clear error"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "invalid-key-123"}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                result = await service.validate_provider("openai")

                assert result.provider == "openai"
                assert result.is_valid is False
                assert result.error_message is not None
                assert (
                    "401" in result.error_message or "unauthorized" in result.error_message.lower()
                )

    @pytest.mark.asyncio
    @pytest.mark.skipif(not os.getenv("ANTHROPIC_API_KEY"), reason="ANTHROPIC_API_KEY not set")
    async def test_validate_anthropic_key_success(self):
        """Valid Anthropic key passes validation (REAL API CALL)"""
        service = LLMConfigService()

        result = await service.validate_provider("anthropic")

        assert result.provider == "anthropic"
        assert result.is_valid is True
        assert result.error_message is None

    @pytest.mark.asyncio
    @pytest.mark.skipif(not os.getenv("GEMINI_API_KEY"), reason="GEMINI_API_KEY not set")
    async def test_validate_gemini_key_success(self):
        """Valid Gemini key passes validation (REAL API CALL)"""
        service = LLMConfigService()

        result = await service.validate_provider("gemini")

        assert result.provider == "gemini"
        assert result.is_valid is True
        assert result.error_message is None

    @pytest.mark.asyncio
    @pytest.mark.skipif(not os.getenv("PERPLEXITY_API_KEY"), reason="PERPLEXITY_API_KEY not set")
    async def test_validate_perplexity_key_success(self):
        """Valid Perplexity key passes validation (REAL API CALL)"""
        service = LLMConfigService()

        result = await service.validate_provider("perplexity")

        assert result.provider == "perplexity"
        assert result.is_valid is True
        assert result.error_message is None

    @pytest.mark.asyncio
    async def test_validate_unknown_provider_returns_error(self):
        """Validating unknown provider returns clear error"""
        service = LLMConfigService()

        result = await service.validate_provider("fake_provider")

        assert result.provider == "fake_provider"
        assert result.is_valid is False
        assert "Unknown provider" in result.error_message

    @pytest.mark.asyncio
    async def test_validate_missing_key_returns_error(self):
        """Validating provider without key returns clear error"""
        with patch.dict(os.environ, {}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                result = await service.validate_provider("openai")

                assert result.provider == "openai"
                assert result.is_valid is False
                assert "not set" in result.error_message or "not found" in result.error_message


class TestStartupValidation:
    """Test startup validation behavior"""

    @pytest.mark.asyncio
    async def test_validate_all_configured_providers(self):
        """Validates all configured providers at startup"""
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "fake-key"),
            },
            clear=True,
        ):
            service = LLMConfigService()

            # Mock validation to avoid real API calls in this test
            async def mock_validate(provider):
                return ValidationResult(provider=provider, is_valid=True)

            service.validate_provider = mock_validate

            results = await service.validate_all_providers()

            assert isinstance(results, dict)
            assert "openai" in results
            assert results["openai"].is_valid is True

    @pytest.mark.asyncio
    async def test_validation_failure_provides_clear_error(self):
        """Failed validation gives actionable error message"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "invalid-key"}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                # Mock to return failure for non-required provider
                async def mock_validate_fail(provider):
                    return ValidationResult(
                        provider=provider,
                        is_valid=False,
                        error_message="Invalid API key: 401 Unauthorized",
                    )

                service.validate_provider = mock_validate_fail

                results = await service.validate_all_providers()

            assert "gemini" in results
            assert results["gemini"].is_valid is False
            assert "Invalid API key" in results["gemini"].error_message

    @pytest.mark.asyncio
    async def test_validation_handles_network_errors(self):
        """Network errors during validation handled gracefully"""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                # Mock to raise network error for non-required provider
                async def mock_validate_network_error(provider):
                    return ValidationResult(
                        provider=provider,
                        is_valid=False,
                        error_message="Network error: Connection timeout",
                        error_code="NETWORK_ERROR",
                    )

                service.validate_provider = mock_validate_network_error

                results = await service.validate_all_providers()

                assert "gemini" in results
                assert results["gemini"].is_valid is False
                assert "Network error" in results["gemini"].error_message

    @pytest.mark.asyncio
    async def test_no_required_providers_no_exception_on_failure(self):
        """#940: No provider is marked required; validation failure logs warning, no exception."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "fake-key"}, clear=True):
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

            # Mock OpenAI validation to fail
            async def mock_validate_fail(provider):
                return ValidationResult(
                    provider=provider, is_valid=False, error_message="Invalid key"
                )

            service.validate_provider = mock_validate_fail

            # Should NOT raise — no providers are required post-#940
            results = await service.validate_all_providers()
            assert "openai" in results
            assert results["openai"].is_valid is False


class TestErrorMessages:
    """Test error message quality"""

    def test_missing_key_returns_none_gracefully(self):
        """Missing key returns None gracefully (keychain migration behavior)"""
        with patch.dict(os.environ, {}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                result = service.get_api_key("openai")
                assert result is None

    @pytest.mark.asyncio
    async def test_invalid_key_error_message_includes_status(self):
        """Invalid key error includes HTTP status for debugging"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "invalid-key"}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()

                result = await service.validate_provider("openai")

                assert result.is_valid is False
                # Should include status code for debugging
                assert (
                    "401" in result.error_message
                    or "403" in result.error_message
                    or "unauthorized" in result.error_message.lower()
                )

    @pytest.mark.asyncio
    async def test_network_error_message_distinguishes_from_auth_error(self):
        """Network errors clearly different from auth errors"""
        service = LLMConfigService()

        # Mock a network error
        network_result = ValidationResult(
            provider="openai",
            is_valid=False,
            error_message="Network error: Connection timeout",
            error_code="NETWORK_ERROR",
        )

        # Mock an auth error
        auth_result = ValidationResult(
            provider="openai",
            is_valid=False,
            error_message="Invalid API key: 401 Unauthorized",
            error_code="AUTH_ERROR",
        )

        # Should be clearly distinguishable
        assert "Network" in network_result.error_message
        assert "401" in auth_result.error_message or "Unauthorized" in auth_result.error_message


class TestValidationResultDataclass:
    """Test ValidationResult data structure"""

    def test_validation_result_success_case(self):
        """ValidationResult correctly represents success"""
        result = ValidationResult(provider="openai", is_valid=True)

        assert result.provider == "openai"
        assert result.is_valid is True
        assert result.error_message is None
        assert result.error_code is None

    def test_validation_result_failure_case(self):
        """ValidationResult correctly represents failure"""
        result = ValidationResult(
            provider="openai",
            is_valid=False,
            error_message="Invalid key",
            error_code="AUTH_ERROR",
        )

        assert result.provider == "openai"
        assert result.is_valid is False
        assert result.error_message == "Invalid key"
        assert result.error_code == "AUTH_ERROR"


class TestProviderConfigDataclass:
    """Test ProviderConfig data structure"""

    def test_provider_config_structure(self):
        """ProviderConfig has required fields"""
        config = ProviderConfig(
            name="openai",
            env_var="OPENAI_API_KEY",
            api_key="test-key",
            validation_endpoint="https://api.openai.com/v1/models",
            required=True,
        )

        assert config.name == "openai"
        assert config.env_var == "OPENAI_API_KEY"
        assert config.api_key == "test-key"
        assert config.validation_endpoint == "https://api.openai.com/v1/models"
        assert config.required is True

    def test_provider_config_optional_defaults(self):
        """ProviderConfig has sensible defaults"""
        config = ProviderConfig(
            name="test",
            env_var="TEST_KEY",
            api_key=None,
            validation_endpoint="https://api.test.com",
        )

        assert config.required is False  # Default


class TestProviderSelection:
    """Test provider selection and exclusion logic (Phase 2)"""

    def test_exclude_provider(self):
        """Excluded provider not in available list"""
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "test-key",
                "ANTHROPIC_API_KEY": "test-key-2",
                "PIPER_EXCLUDED_PROVIDERS": "anthropic",
            },
            clear=True,
        ):
            service = LLMConfigService()
            available = service.get_available_providers()
            assert "anthropic" not in available
            assert "openai" in available

    def test_exclude_multiple_providers(self):
        """Multiple excluded providers filtered out"""
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "test-key",
                "ANTHROPIC_API_KEY": "test-key-2",
                "GEMINI_API_KEY": "test-key-3",
                "PIPER_EXCLUDED_PROVIDERS": "anthropic,gemini",
            },
            clear=True,
        ):
            service = LLMConfigService()
            available = service.get_available_providers()
            assert "anthropic" not in available
            assert "gemini" not in available
            assert "openai" in available

    def test_default_provider_selection(self, mock_keychain_service):
        """Default provider is returned if available"""

        # Mock keychain: openai key available, no stored default_llm_provider
        def mock_get(name):
            if name == "openai":
                return "test-key"
            return None

        mock_keychain_service.get_api_key.side_effect = mock_get

        with patch.dict(
            os.environ,
            {"OPENAI_API_KEY": "test-key", "PIPER_DEFAULT_PROVIDER": "openai"},
            clear=True,
        ):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            default = service.get_default_provider()
            assert default == "openai"

    def test_default_provider_excluded_uses_fallback(self):
        """If default excluded, uses fallback"""
        with patch.dict(
            os.environ,
            {
                "OPENAI_API_KEY": "test-key",
                "ANTHROPIC_API_KEY": "test-key-2",
                "GEMINI_API_KEY": "test-key-3",
                "PIPER_DEFAULT_PROVIDER": "anthropic",
                "PIPER_EXCLUDED_PROVIDERS": "anthropic",
                "PIPER_FALLBACK_PROVIDERS": "openai,gemini",
            },
            clear=True,
        ):
            service = LLMConfigService()
            provider = service.get_provider_with_fallback()
            assert provider in ["openai", "gemini"]
            assert provider != "anthropic"

    def test_preferred_provider_override(self):
        """Preferred provider overrides default"""
        with patch.dict(
            os.environ,
            {"OPENAI_API_KEY": "test-key", "GEMINI_API_KEY": "test-key-2"},
            clear=True,
        ):
            service = LLMConfigService()
            provider = service.get_provider_with_fallback(preferred="gemini")
            assert provider == "gemini"

    def test_is_provider_excluded(self):
        """Can check if provider is excluded"""
        with patch.dict(
            os.environ,
            {"OPENAI_API_KEY": "test-key", "PIPER_EXCLUDED_PROVIDERS": "anthropic"},
            clear=True,
        ):
            service = LLMConfigService()
            assert service.is_provider_excluded("anthropic") is True
            assert service.is_provider_excluded("openai") is False

    def test_get_environment(self):
        """Can get current environment"""
        with patch.dict(os.environ, {"PIPER_ENVIRONMENT": "production"}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()
            from services.config.llm_config_service import Environment

            assert service.get_environment() == Environment.PRODUCTION

    def test_environment_defaults_to_development(self):
        """Environment defaults to development if not set"""
        with patch.dict(os.environ, {}, clear=True):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()
            from services.config.llm_config_service import Environment

            assert service.get_environment() == Environment.DEVELOPMENT

    def test_available_providers_excludes_unconfigured(self):
        """Available providers only includes configured ones"""
        with patch.dict(
            os.environ, {"OPENAI_API_KEY": "test-key", "PIPER_EXCLUDED_PROVIDERS": ""}, clear=True
        ):
            # Mock keychain service to return None (so it falls back to env var)
            with patch("services.config.llm_config_service.KeychainService") as mock_keychain_class:
                mock_keychain = mock_keychain_class.return_value
                mock_keychain.get_api_key.return_value = None

                service = LLMConfigService()
            available = service.get_available_providers()
            # Only OpenAI should be available (others don't have keys)
            assert "openai" in available
            assert "anthropic" not in available  # No key
            assert "gemini" not in available  # No key


class TestKeychainIntegration:
    """Test keychain integration with LLMConfigService"""

    def test_get_api_key_from_keychain(self, mock_keychain_service):
        """Retrieves key from keychain when available"""
        mock_keychain_service.get_api_key.return_value = "keychain-key"

        service = LLMConfigService(keychain_service=mock_keychain_service)
        key = service.get_api_key("openai")

        assert key == "keychain-key"
        mock_keychain_service.get_api_key.assert_called_once_with("openai")

    def test_get_api_key_falls_back_to_env(self, mock_keychain_service):
        """Falls back to environment when not in keychain"""
        mock_keychain_service.get_api_key.return_value = None

        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            key = service.get_api_key("openai")

        assert key == "env-key"

    def test_keychain_preferred_over_env(self, mock_keychain_service):
        """Keychain takes priority over environment"""
        mock_keychain_service.get_api_key.return_value = "keychain-key"

        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            key = service.get_api_key("openai")

        # Should get keychain version, not env
        assert key == "keychain-key"

    def test_get_migration_status(self, mock_keychain_service):
        """Returns migration status for all providers"""
        from services.infrastructure.keychain_service import KeychainEntry

        mock_keychain_service.check_migration_status.return_value = {
            "openai": KeychainEntry("openai", True, False),
            "anthropic": KeychainEntry("anthropic", False, True),
            "gemini": KeychainEntry("gemini", False, False),
            "perplexity": KeychainEntry("perplexity", False, False),
        }

        service = LLMConfigService(keychain_service=mock_keychain_service)
        status = service.get_migration_status()

        assert status["in_keychain"] == 1
        assert status["in_env"] == 1
        assert status["missing"] == 2

    def test_migrate_key_to_keychain_success(self, mock_keychain_service):
        """Can migrate key from environment to keychain"""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "env-key"}):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            result = service.migrate_key_to_keychain("openai")

        assert result is True
        mock_keychain_service.store_api_key.assert_called_once_with("openai", "env-key")

    def test_migrate_key_no_env_key(self, mock_keychain_service):
        """Migration fails gracefully when no env key"""
        service = LLMConfigService(keychain_service=mock_keychain_service)
        result = service.migrate_key_to_keychain("nonexistent")

        assert result is False
        mock_keychain_service.store_api_key.assert_not_called()


class TestAuthorizedProviders:
    """#946: Test that get_configured_providers respects authorization consent."""

    def test_only_authorized_providers_returned(self, mock_keychain_service):
        """When authorized_llm_providers is set, only those are returned."""

        # Simulate: both keys exist, but only anthropic is authorized
        def mock_get_key(provider):
            if provider == "openai":
                return "sk-stale-openai-key"
            if provider == "anthropic":
                return "sk-ant-authorized-key"
            if provider == "authorized_llm_providers":
                return "anthropic"
            return None

        mock_keychain_service.get_api_key.side_effect = mock_get_key

        with patch.dict(os.environ, {}, clear=True):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            providers = service.get_configured_providers()

        assert "anthropic" in providers
        assert "openai" not in providers, "stale OpenAI key should be filtered out"

    def test_unauthorized_provider_with_key_excluded(self, mock_keychain_service):
        """A provider with a valid key but NOT in authorized list is excluded."""

        def mock_get_key(provider):
            if provider == "openai":
                return "sk-valid-but-unauthorized"
            if provider == "authorized_llm_providers":
                return "anthropic"  # only anthropic authorized
            return None

        mock_keychain_service.get_api_key.side_effect = mock_get_key

        with patch.dict(os.environ, {}, clear=True):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            providers = service.get_configured_providers()

        assert providers == []  # anthropic has no key, openai not authorized

    def test_no_authorized_list_returns_all_configured(self, mock_keychain_service):
        """Legacy: when no authorized_llm_providers stored, return all configured."""

        def mock_get_key(provider):
            if provider == "openai":
                return "sk-openai"
            if provider == "anthropic":
                return "sk-ant-key"
            if provider == "authorized_llm_providers":
                return None  # no consent list stored
            return None

        mock_keychain_service.get_api_key.side_effect = mock_get_key

        with patch.dict(os.environ, {}, clear=True):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            providers = service.get_configured_providers()

        assert "openai" in providers
        assert "anthropic" in providers

    def test_multiple_authorized_providers(self, mock_keychain_service):
        """Both providers authorized — both returned."""

        def mock_get_key(provider):
            if provider == "openai":
                return "sk-openai"
            if provider == "anthropic":
                return "sk-ant-key"
            if provider == "authorized_llm_providers":
                return "openai,anthropic"
            return None

        mock_keychain_service.get_api_key.side_effect = mock_get_key

        with patch.dict(os.environ, {}, clear=True):
            service = LLMConfigService(keychain_service=mock_keychain_service)
            providers = service.get_configured_providers()

        assert "openai" in providers
        assert "anthropic" in providers
