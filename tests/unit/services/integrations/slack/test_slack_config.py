"""
Tests for Slack Configuration Service
Tests ADR-010 compliant configuration patterns for Slack integration.

Issue #734: Updated to require user_id parameter for multi-tenancy isolation.
"""

import os
from unittest.mock import Mock, patch

import pytest

from services.integrations.slack.config_service import (
    SlackConfig,
    SlackConfigService,
    SlackEnvironment,
)


# Test user ID for all tests
def _mirror_read_secret(kc):
    """#2151: SlackConfigService reads user tokens with provenance (read_secret);
    mirror the mocked get_api_key: present when set, verified absent otherwise."""
    from services.infrastructure.keychain_service import SecretProvenance, SecretRead

    def _read(provider, username=None):
        value = kc.get_api_key(provider, username)
        if value:
            return SecretRead(SecretProvenance.PRESENT, value=value)
        return SecretRead(SecretProvenance.VERIFIED_ABSENT)

    kc.read_secret = _read
    return kc


TEST_USER_ID = "test-user-123"


class TestSlackConfig:
    """Test Slack configuration dataclass"""

    @pytest.mark.smoke
    def test_default_config(self):
        """Test default configuration values"""
        config = SlackConfig()

        assert config.bot_token == ""
        assert config.app_token == ""
        assert config.api_base_url == "https://slack.com/api"
        assert config.timeout_seconds == 30
        assert config.max_retries == 3
        assert config.environment == SlackEnvironment.DEVELOPMENT
        assert config.enable_webhooks is True
        assert config.enable_socket_mode is False
        assert config.enable_spatial_mapping is True

    @pytest.mark.smoke
    def test_config_validation_valid(self):
        """Test configuration validation with valid settings"""
        config = SlackConfig(
            bot_token="xoxb-test-token", webhook_url="https://hooks.slack.com/test"
        )

        assert config.validate() is True

    @pytest.mark.smoke
    def test_config_validation_missing_bot_token(self):
        """Test configuration validation with missing bot token"""
        config = SlackConfig(webhook_url="https://hooks.slack.com/test")

        assert config.validate() is False

    @pytest.mark.smoke
    def test_config_validation_webhooks_enabled_no_url(self):
        """Test configuration validation with webhooks enabled but no URL"""
        config = SlackConfig(bot_token="xoxb-test-token", enable_webhooks=True, webhook_url="")

        assert config.validate() is False


class TestSlackConfigService:
    """Test Slack configuration service"""

    @pytest.mark.smoke
    def test_init_with_feature_flags(self):
        """Test initialization with feature flags"""
        mock_flags = Mock()
        service = SlackConfigService(feature_flags=mock_flags)

        assert service.feature_flags == mock_flags
        # Issue #734: Now uses _config_cache dict instead of _config
        assert service._config_cache == {}

    @pytest.mark.smoke
    def test_init_without_feature_flags(self):
        """Test initialization without feature flags"""
        service = SlackConfigService()

        assert service.feature_flags is not None
        # Issue #734: Now uses _config_cache dict instead of _config
        assert service._config_cache == {}

    @patch.dict(
        os.environ,
        {
            "SLACK_BOT_TOKEN": "xoxb-test-token",
            "SLACK_APP_TOKEN": "xapp-test-token",
            "SLACK_SIGNING_SECRET": "test-secret",
            "SLACK_ENVIRONMENT": "production",
            "SLACK_TIMEOUT_SECONDS": "60",
            "SLACK_MAX_RETRIES": "5",
        },
    )
    @pytest.mark.smoke
    def test_load_config_from_environment(self):
        """Test loading configuration from environment variables"""
        service = SlackConfigService()
        # Issue #734: Now requires user_id
        config = service.get_config(user_id=TEST_USER_ID)

        assert config.bot_token == "xoxb-test-token"
        assert config.app_token == "xapp-test-token"
        assert config.signing_secret == "test-secret"
        assert config.environment == SlackEnvironment.PRODUCTION
        assert config.timeout_seconds == 60
        assert config.max_retries == 5

    @pytest.mark.smoke
    def test_load_config_defaults(self):
        """Test loading configuration with default values"""
        # Mock keychain to return empty (Issue #576 added keychain support)
        mock_keychain = Mock()
        mock_keychain.get_api_key.return_value = None
        _mirror_read_secret(mock_keychain)

        with (
            patch.dict(os.environ, {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            service = SlackConfigService()
            # Issue #734: Now requires user_id
            config = service.get_config(user_id=TEST_USER_ID)

            assert config.bot_token == ""
            assert config.api_base_url == "https://slack.com/api"
            assert config.timeout_seconds == 30
            assert config.environment == SlackEnvironment.DEVELOPMENT

    @pytest.mark.smoke
    def test_config_caching(self):
        """Test that configuration is cached after first load"""
        service = SlackConfigService()

        # First call should load config
        # Issue #734: Now requires user_id
        config1 = service.get_config(user_id=TEST_USER_ID)
        assert TEST_USER_ID in service._config_cache

        # Second call should return cached config
        config2 = service.get_config(user_id=TEST_USER_ID)
        assert config1 is config2

    @pytest.mark.smoke
    def test_is_configured_valid(self):
        """Test is_configured with valid configuration"""
        # Set all required env vars for valid configuration
        # Note: SLACK_WEBHOOK_URL required because PIPER.user.md may have enable_webhooks: true
        with patch.dict(
            os.environ,
            {
                "SLACK_BOT_TOKEN": "xoxb-test-token",
                "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/test",
            },
        ):
            service = SlackConfigService()
            # Issue #734: Now requires user_id
            assert service.is_configured(user_id=TEST_USER_ID) is True

    @pytest.mark.smoke
    def test_is_configured_invalid(self):
        """Test is_configured with invalid configuration"""
        # Mock keychain to return empty (Issue #576 added keychain support)
        mock_keychain = Mock()
        mock_keychain.get_api_key.return_value = None
        _mirror_read_secret(mock_keychain)

        with (
            patch.dict(os.environ, {}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            service = SlackConfigService()
            # Issue #734: Now requires user_id
            assert service.is_configured(user_id=TEST_USER_ID) is False

    @pytest.mark.smoke
    def test_get_environment(self):
        """Test getting current environment"""
        with patch.dict(os.environ, {"SLACK_ENVIRONMENT": "staging"}):
            service = SlackConfigService()
            # Issue #734: Now requires user_id
            assert service.get_environment(user_id=TEST_USER_ID) == SlackEnvironment.STAGING

    @pytest.mark.smoke
    def test_is_production_true(self):
        """Test is_production when in production environment"""
        with patch.dict(os.environ, {"SLACK_ENVIRONMENT": "production"}):
            service = SlackConfigService()
            # Issue #734: Now requires user_id
            assert service.is_production(user_id=TEST_USER_ID) is True

    @pytest.mark.smoke
    def test_is_production_false(self):
        """Test is_production when not in production environment"""
        with patch.dict(os.environ, {"SLACK_ENVIRONMENT": "development"}):
            service = SlackConfigService()
            # Issue #734: Now requires user_id
            assert service.is_production(user_id=TEST_USER_ID) is False


class TestSlackEnvironment:
    """Test Slack environment enum"""

    @pytest.mark.smoke
    def test_environment_values(self):
        """Test environment enum values"""
        assert SlackEnvironment.DEVELOPMENT.value == "development"
        assert SlackEnvironment.STAGING.value == "staging"
        assert SlackEnvironment.PRODUCTION.value == "production"

    @pytest.mark.smoke
    def test_environment_from_string(self):
        """Test creating environment from string"""
        assert SlackEnvironment("development") == SlackEnvironment.DEVELOPMENT
        assert SlackEnvironment("staging") == SlackEnvironment.STAGING
        assert SlackEnvironment("production") == SlackEnvironment.PRODUCTION
