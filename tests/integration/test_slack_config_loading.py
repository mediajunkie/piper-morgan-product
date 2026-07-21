"""Tests for Slack configuration loading from PIPER.user.md.

Implements test coverage for SlackConfigService YAML loading functionality,
ensuring proper configuration priority order: env vars > PIPER.user.md > defaults.

Pattern based on Calendar and Notion configuration loading tests.
Tests Slack's direct spatial architecture (ADR-039).
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from services.integrations.slack.config_service import (
    SlackConfig,
    SlackConfigService,
    SlackEnvironment,
)


class TestSlackConfigLoading:
    """Test SlackConfigService configuration loading from PIPER.user.md."""

    def test_loads_from_piper_user_md(self, tmp_path):
        """Test that config loads from PIPER.user.md when present."""
        # Create temporary PIPER.user.md with slack config
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
# Test Configuration

## 💬 Slack Integration

Configure Slack workspace integration.

```yaml
slack:
  authentication:
    bot_token: "xoxb-test-from-file"
    app_token: "xapp-test-from-file"
    signing_secret: "secret-from-file"
  api:
    base_url: "https://test.slack.com/api"
    timeout_seconds: 60
    max_retries: 5
  behavior:
    default_channel: "testing"
    rate_limit_per_minute: 60
```

## Other Section
        """
        )

        # Patch Path to use temp file
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                # Load config
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify values from PIPER.user.md
                assert config.bot_token == "xoxb-test-from-file"
                assert config.app_token == "xapp-test-from-file"
                assert config.signing_secret == "secret-from-file"
                assert config.api_base_url == "https://test.slack.com/api"
                assert config.timeout_seconds == 60
                assert config.max_retries == 5
                assert config.default_channel == "testing"
                assert config.requests_per_minute == 60

    def test_env_vars_override_user_config(self, tmp_path):
        """Test that environment variables override PIPER.user.md."""
        # Create PIPER.user.md with one set of values
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  authentication:
    bot_token: "xoxb-user-token"
    app_token: "xapp-user-token"
  behavior:
    default_channel: "general"
    rate_limit_per_minute: 50
```
        """
        )

        # Set environment variables to override
        original_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        original_app_token = os.environ.get("SLACK_APP_TOKEN")
        original_channel = os.environ.get("SLACK_DEFAULT_CHANNEL")

        os.environ["SLACK_BOT_TOKEN"] = "xoxb-env-override"
        os.environ["SLACK_APP_TOKEN"] = "xapp-env-override"
        os.environ["SLACK_DEFAULT_CHANNEL"] = "testing"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = SlackConfigService()
                    config = service.get_config("test-user-slack-config")

                    # Verify env vars override user config
                    assert config.bot_token == "xoxb-env-override"
                    assert config.app_token == "xapp-env-override"
                    assert config.default_channel == "testing"
                    # Verify non-overridden value still from user config
                    assert config.requests_per_minute == 50
        finally:
            # Clean up environment
            if original_bot_token is None:
                os.environ.pop("SLACK_BOT_TOKEN", None)
            else:
                os.environ["SLACK_BOT_TOKEN"] = original_bot_token
            if original_app_token is None:
                os.environ.pop("SLACK_APP_TOKEN", None)
            else:
                os.environ["SLACK_APP_TOKEN"] = original_app_token
            if original_channel is None:
                os.environ.pop("SLACK_DEFAULT_CHANNEL", None)
            else:
                os.environ["SLACK_DEFAULT_CHANNEL"] = original_channel

    def test_defaults_when_no_config(self, tmp_path):
        """Test that defaults are used when neither PIPER.user.md nor env vars present."""
        # Create empty PIPER.user.md
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("# Empty config\n\nNo slack section here.")

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify defaults
                assert config.bot_token == ""
                assert config.app_token == ""
                assert config.api_base_url == "https://slack.com/api"
                assert config.timeout_seconds == 30
                assert config.max_retries == 3
                assert config.requests_per_minute == 50
                assert config.environment == SlackEnvironment.DEVELOPMENT

    def test_graceful_fallback_when_piper_missing(self, tmp_path):
        """Test graceful fallback when PIPER.user.md doesn't exist."""
        # Point to non-existent file
        with patch.object(Path, "exists", return_value=False):
            # Should not raise exception
            service = SlackConfigService()
            config = service.get_config("test-user-slack-config")

            # Should use defaults
            assert config.bot_token == ""
            assert config.timeout_seconds == 30
            assert config.max_retries == 3

    def test_graceful_fallback_when_yaml_malformed(self, tmp_path):
        """Test graceful fallback when PIPER.user.md has malformed YAML."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  bad: yaml: syntax: here:
  - invalid
  missing: quote
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                # Should not raise exception
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Should use defaults
                assert config.bot_token == ""
                assert config.timeout_seconds == 30

    def test_authentication_section_parsing(self, tmp_path):
        """Test that authentication section is properly parsed from PIPER.user.md."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  authentication:
    bot_token: "xoxb-secret-test-token-123"
    app_token: "xapp-secret-test-token-456"
    signing_secret: "test-signing-secret-789"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify authentication section properly parsed
                assert config.bot_token == "xoxb-secret-test-token-123"
                assert config.app_token == "xapp-secret-test-token-456"
                assert config.signing_secret == "test-signing-secret-789"

    def test_missing_authentication_section(self, tmp_path):
        """Test handling when authentication section is missing from PIPER.user.md."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  api:
    timeout_seconds: 45
    max_retries: 5
  behavior:
    default_channel: "general"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Should use defaults for authentication
                assert config.bot_token == ""
                assert config.app_token == ""
                assert config.signing_secret == ""
                # But still load other config
                assert config.timeout_seconds == 45
                assert config.max_retries == 5
                assert config.default_channel == "general"

    def test_api_config_settings(self, tmp_path):
        """Test API configuration settings load correctly."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  api:
    base_url: "https://custom.slack.com/api"
    timeout_seconds: 120
    max_retries: 10
    environment: "production"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify API config
                assert config.api_base_url == "https://custom.slack.com/api"
                assert config.timeout_seconds == 120
                assert config.max_retries == 10
                assert config.environment == SlackEnvironment.PRODUCTION

    def test_behavior_configuration(self, tmp_path):
        """Test behavior settings load correctly."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  behavior:
    default_channel: "engineering"
    rate_limit_per_minute: 100
    burst_limit: 20
    webhook_url: "https://hooks.slack.com/test"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify behavior config
                assert config.default_channel == "engineering"
                assert config.requests_per_minute == 100
                assert config.burst_limit == 20
                assert config.webhook_url == "https://hooks.slack.com/test"

    def test_features_configuration(self, tmp_path):
        """Test feature flags load correctly."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  features:
    enable_webhooks: false
    enable_socket_mode: true
    enable_spatial_mapping: false
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify feature flags
                assert config.enable_webhooks is False
                assert config.enable_socket_mode is True
                assert config.enable_spatial_mapping is False

    def test_oauth_configuration(self, tmp_path):
        """Test OAuth settings load correctly."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  oauth:
    client_id: "test-client-id-123"
    client_secret: "test-client-secret-456"
    redirect_uri: "https://example.com/oauth/callback"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify OAuth config
                assert config.client_id == "test-client-id-123"
                assert config.client_secret == "test-client-secret-456"
                assert config.redirect_uri == "https://example.com/oauth/callback"

    def test_configuration_priority_order_comprehensive(self, tmp_path):
        """Test comprehensive scenario with all three config layers."""
        # Create PIPER.user.md with middle-priority values
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  authentication:
    bot_token: "xoxb-user-token"
    app_token: "xapp-user-token"
  api:
    timeout_seconds: 45
    max_retries: 5
  behavior:
    default_channel: "general"
```
        """
        )

        # Set one environment variable to override
        original_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        os.environ["SLACK_BOT_TOKEN"] = "xoxb-env-token"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = SlackConfigService()
                    config = service.get_config("test-user-slack-config")

                    # Verify priority order:
                    # 1. bot_token from env var (highest)
                    assert config.bot_token == "xoxb-env-token"

                    # 2. app_token, timeout, etc. from PIPER.user.md (middle)
                    assert config.app_token == "xapp-user-token"
                    assert config.timeout_seconds == 45
                    assert config.max_retries == 5
                    assert config.default_channel == "general"

                    # 3. requests_per_minute from defaults (lowest)
                    assert config.requests_per_minute == 50
        finally:
            # Clean up environment
            if original_bot_token is None:
                os.environ.pop("SLACK_BOT_TOKEN", None)
            else:
                os.environ["SLACK_BOT_TOKEN"] = original_bot_token

    def test_partial_configuration(self, tmp_path):
        """Test handling of partially specified configuration."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  authentication:
    bot_token: "xoxb-partial-token"
  api:
    timeout_seconds: 60
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify partial config loads
                assert config.bot_token == "xoxb-partial-token"
                assert config.timeout_seconds == 60
                # Verify defaults for missing fields
                assert config.app_token == ""
                assert config.max_retries == 3
                assert config.requests_per_minute == 50

    def test_empty_piper_user_md_file(self, tmp_path):
        """Test handling of completely empty PIPER.user.md file."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("")

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Should use all defaults
                assert config.bot_token == ""
                assert config.timeout_seconds == 30
                assert config.max_retries == 3

    def test_slack_section_with_no_yaml_block(self, tmp_path):
        """Test slack section exists but has no YAML block."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

This section exists but has no YAML configuration.

Just some text here.
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Should gracefully fall back to defaults
                assert config.bot_token == ""
                assert config.timeout_seconds == 30

    def test_supports_direct_slack_pattern(self, tmp_path):
        """Test slack: direct pattern (Slack-specific)."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
slack:
```yaml
authentication:
  bot_token: "xoxb-direct-pattern"
  app_token: "xapp-direct-pattern"
behavior:
  default_channel: "testing"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                config = service.get_config("test-user-slack-config")

                # Verify direct pattern works
                assert config.bot_token == "xoxb-direct-pattern"
                assert config.app_token == "xapp-direct-pattern"
                assert config.default_channel == "testing"

    def test_env_var_rate_limit_override(self, tmp_path):
        """Test SLACK_RATE_LIMIT_RPM env var overrides user config."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  behavior:
    rate_limit_per_minute: 50
```
        """
        )

        # Set environment variable
        original_rate_limit = os.environ.get("SLACK_RATE_LIMIT_RPM")
        os.environ["SLACK_RATE_LIMIT_RPM"] = "120"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = SlackConfigService()
                    config = service.get_config("test-user-slack-config")

                    # Verify env var overrides
                    assert config.requests_per_minute == 120
        finally:
            # Clean up environment
            if original_rate_limit is None:
                os.environ.pop("SLACK_RATE_LIMIT_RPM", None)
            else:
                os.environ["SLACK_RATE_LIMIT_RPM"] = original_rate_limit


class TestSlackConfigServiceBasics:
    """Test basic SlackConfigService functionality."""

    def test_service_initializes_successfully(self):
        """Test that SlackConfigService initializes without errors."""
        service = SlackConfigService()
        assert service is not None
        assert hasattr(service, "_load_from_user_config")
        assert hasattr(service, "_load_config")
        assert hasattr(service, "get_config")

    def test_config_caching(self):
        """Test that config is cached after first load."""
        service = SlackConfigService()

        # First call loads config
        config1 = service.get_config("test-user-slack-config")

        # Second call should return same instance (cached)
        config2 = service.get_config("test-user-slack-config")

        assert config1 is config2

    def test_is_configured_method(self, tmp_path):
        """Test is_configured method returns correct status."""
        # With bot token
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 💬 Slack Integration

```yaml
slack:
  authentication:
    bot_token: "xoxb-test-token"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = SlackConfigService()
                assert service.is_configured("test-user-slack-config") is True

        # Without bot token (should return False)
        empty_config = tmp_path / "PIPER.empty.md"
        empty_config.write_text("")

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=empty_config.read_text()):
                service2 = SlackConfigService()
                assert service2.is_configured("test-user-slack-config") is False
