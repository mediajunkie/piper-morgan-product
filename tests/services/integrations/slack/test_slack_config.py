"""
Tests for Slack Configuration Service
Tests ADR-010 compliant configuration patterns for Slack integration.
"""

import os
from unittest.mock import Mock, patch

import pytest

from services.integrations.slack.config_service import (
    SlackConfig,
    SlackConfigService,
    SlackEnvironment,
)


class TestSlackConfig:
    """Test Slack configuration dataclass"""

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

    def test_config_validation_valid(self):
        """Test configuration validation with valid settings"""
        config = SlackConfig(
            bot_token="xoxb-test-token", webhook_url="https://hooks.slack.com/test"
        )

        assert config.validate() is True

    def test_config_validation_missing_bot_token(self):
        """Test configuration validation with missing bot token"""
        config = SlackConfig(webhook_url="https://hooks.slack.com/test")

        assert config.validate() is False

    def test_config_validation_webhooks_enabled_no_url(self):
        """Test configuration validation with webhooks enabled but no URL"""
        config = SlackConfig(bot_token="xoxb-test-token", enable_webhooks=True, webhook_url="")

        assert config.validate() is False


class TestSlackConfigService:
    """Test Slack configuration service"""

    def test_init_with_feature_flags(self):
        """Test initialization with feature flags"""
        mock_flags = Mock()
        service = SlackConfigService(feature_flags=mock_flags)

        assert service.feature_flags == mock_flags
        assert service._config is None

    def test_init_without_feature_flags(self):
        """Test initialization without feature flags"""
        service = SlackConfigService()

        assert service.feature_flags is not None
        assert service._config is None

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
    def test_load_config_from_environment(self):
        """Test loading configuration from environment variables"""
        service = SlackConfigService()
        config = service.get_config()

        assert config.bot_token == "xoxb-test-token"
        assert config.app_token == "xapp-test-token"
        assert config.signing_secret == "test-secret"
        assert config.environment == SlackEnvironment.PRODUCTION
        assert config.timeout_seconds == 60
        assert config.max_retries == 5

    def test_load_config_defaults(self):
        """Test loading configuration with default values"""
        with patch.dict(os.environ, {}, clear=True):
            service = SlackConfigService()
            config = service.get_config()

            assert config.bot_token == ""
            assert config.api_base_url == "https://slack.com/api"
            assert config.timeout_seconds == 30
            assert config.environment == SlackEnvironment.DEVELOPMENT

    def test_config_caching(self):
        """Test that configuration is cached after first load"""
        service = SlackConfigService()

        # First call should load config
        config1 = service.get_config()
        assert service._config is not None

        # Second call should return cached config
        config2 = service.get_config()
        assert config1 is config2

    def test_is_configured_valid(self):
        """Test is_configured with valid configuration"""
        with patch.dict(os.environ, {"SLACK_BOT_TOKEN": "xoxb-test-token"}):
            service = SlackConfigService()
            assert service.is_configured() is True

    def test_is_configured_invalid(self):
        """Test is_configured with invalid configuration"""
        with patch.dict(os.environ, {}, clear=True):
            service = SlackConfigService()
            assert service.is_configured() is False

    def test_get_environment(self):
        """Test getting current environment"""
        with patch.dict(os.environ, {"SLACK_ENVIRONMENT": "staging"}):
            service = SlackConfigService()
            assert service.get_environment() == SlackEnvironment.STAGING

    def test_is_production_true(self):
        """Test is_production when in production environment"""
        with patch.dict(os.environ, {"SLACK_ENVIRONMENT": "production"}):
            service = SlackConfigService()
            assert service.is_production() is True

    def test_is_production_false(self):
        """Test is_production when not in production environment"""
        with patch.dict(os.environ, {"SLACK_ENVIRONMENT": "development"}):
            service = SlackConfigService()
            assert service.is_production() is False


class TestSlackEnvironment:
    """Test Slack environment enum"""

    def test_environment_values(self):
        """Test environment enum values"""
        assert SlackEnvironment.DEVELOPMENT.value == "development"
        assert SlackEnvironment.STAGING.value == "staging"
        assert SlackEnvironment.PRODUCTION.value == "production"

    def test_environment_from_string(self):
        """Test creating environment from string"""
        assert SlackEnvironment("development") == SlackEnvironment.DEVELOPMENT
        assert SlackEnvironment("staging") == SlackEnvironment.STAGING
        assert SlackEnvironment("production") == SlackEnvironment.PRODUCTION
