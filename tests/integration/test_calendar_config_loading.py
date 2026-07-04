"""Tests for Calendar configuration loading from PIPER.user.md.

Implements test coverage for CalendarConfigService YAML loading functionality,
ensuring proper configuration priority order: env vars > PIPER.user.md > defaults.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from services.integrations.calendar.config_service import CalendarConfig, CalendarConfigService


class TestCalendarConfigLoading:
    """Test CalendarConfigService configuration loading from PIPER.user.md."""

    def test_loads_from_piper_user_md(self, tmp_path):
        """Test that config loads from PIPER.user.md when present."""
        # Create temporary PIPER.user.md with calendar config
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
# Test Configuration

## 📅 Calendar Integration

Configure Google Calendar integration with OAuth 2.0 credentials.

```yaml
calendar:
  client_secrets_file: "test_credentials.json"
  token_file: "test_token.json"
  calendar_id: "test@calendar.com"
  timeout_seconds: 60
  circuit_timeout: 600
  error_threshold: 10
```

## Other Section
        """
        )

        # Patch Path to use temp file
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                # Load config
                service = CalendarConfigService()
                config = service.get_config("test-user-1354")

                # Verify values from PIPER.user.md
                assert config.client_secrets_file == "test_credentials.json"
                # Issue #734: token_file is always user-scoped — "test_token.json"
                # doesn't contain the user_id, so it's transformed to include it.
                assert config.token_file == "test_token_test-user-1354.json"
                assert config.calendar_id == "test@calendar.com"
                assert config.timeout_seconds == 60
                assert config.circuit_timeout == 600
                assert config.error_threshold == 10

    def test_env_vars_override_user_config(self, tmp_path):
        """Test that environment variables override PIPER.user.md."""
        # Create PIPER.user.md with one set of values
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📅 Calendar Integration

```yaml
calendar:
  calendar_id: "user_config@calendar.com"
  timeout_seconds: 30
```
        """
        )

        # Set environment variable to override calendar_id
        original_env = os.environ.get("GOOGLE_CALENDAR_ID")
        os.environ["GOOGLE_CALENDAR_ID"] = "env_override@calendar.com"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = CalendarConfigService()
                    config = service.get_config("test-user-1354")

                    # Verify env var overrides user config
                    assert config.calendar_id == "env_override@calendar.com"
                    # Verify non-overridden value still from user config
                    assert config.timeout_seconds == 30
        finally:
            # Clean up environment
            if original_env is None:
                os.environ.pop("GOOGLE_CALENDAR_ID", None)
            else:
                os.environ["GOOGLE_CALENDAR_ID"] = original_env

    def test_defaults_when_no_config(self, tmp_path):
        """Test that defaults are used when neither PIPER.user.md nor env vars present."""
        # Create empty PIPER.user.md
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("# Empty config\n\nNo calendar section here.")

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = CalendarConfigService()
                config = service.get_config("test-user-1354")

                # Verify defaults
                assert config.client_secrets_file == "credentials.json"
                # Issue #734: the default token_file is already user-scoped from the start.
                assert config.token_file == "token_test-user-1354.json"
                assert config.calendar_id == "primary"
                assert config.timeout_seconds == 30
                assert config.circuit_timeout == 300
                assert config.error_threshold == 5
                assert config.scopes == ["https://www.googleapis.com/auth/calendar.readonly"]

    def test_graceful_fallback_when_piper_missing(self, tmp_path):
        """Test graceful fallback when PIPER.user.md doesn't exist."""
        # Point to non-existent file
        with patch.object(Path, "exists", return_value=False):
            # Should not raise exception
            service = CalendarConfigService()
            config = service.get_config("test-user-1354")

            # Should use defaults
            assert config.calendar_id == "primary"
            assert config.timeout_seconds == 30

    def test_graceful_fallback_when_yaml_malformed(self, tmp_path):
        """Test graceful fallback when PIPER.user.md has malformed YAML."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📅 Calendar Integration

```yaml
calendar:
  bad: yaml: syntax: here:
  - invalid
  missing: quote
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                # Should not raise exception
                service = CalendarConfigService()
                config = service.get_config("test-user-1354")

                # Should use defaults
                assert config.calendar_id == "primary"
                assert config.timeout_seconds == 30

    def test_scopes_parsing_from_user_config(self, tmp_path):
        """Test that scopes list is properly parsed from PIPER.user.md."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📅 Calendar Integration

```yaml
calendar:
  scopes:
    - "https://www.googleapis.com/auth/calendar.readonly"
    - "https://www.googleapis.com/auth/calendar.events"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = CalendarConfigService()
                config = service.get_config("test-user-1354")

                # Verify scopes list properly parsed
                assert len(config.scopes) == 2
                assert "https://www.googleapis.com/auth/calendar.readonly" in config.scopes
                assert "https://www.googleapis.com/auth/calendar.events" in config.scopes

    def test_env_var_scopes_override_user_config_scopes(self, tmp_path):
        """Test that GOOGLE_CALENDAR_SCOPES env var overrides PIPER.user.md scopes."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📅 Calendar Integration

```yaml
calendar:
  scopes:
    - "https://www.googleapis.com/auth/calendar.readonly"
```
        """
        )

        # Set environment variable for scopes
        original_env = os.environ.get("GOOGLE_CALENDAR_SCOPES")
        os.environ["GOOGLE_CALENDAR_SCOPES"] = (
            "https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/calendar.events"
        )

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = CalendarConfigService()
                    config = service.get_config("test-user-1354")

                    # Verify env var overrides user config scopes
                    assert len(config.scopes) == 2
                    assert "https://www.googleapis.com/auth/calendar" in config.scopes
                    assert "https://www.googleapis.com/auth/calendar.events" in config.scopes
        finally:
            # Clean up environment
            if original_env is None:
                os.environ.pop("GOOGLE_CALENDAR_SCOPES", None)
            else:
                os.environ["GOOGLE_CALENDAR_SCOPES"] = original_env

    def test_configuration_priority_order_comprehensive(self, tmp_path):
        """Test comprehensive scenario with all three config layers."""
        # Create PIPER.user.md with middle-priority values
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📅 Calendar Integration

```yaml
calendar:
  client_secrets_file: "user_credentials.json"
  token_file: "user_token.json"
  calendar_id: "user@calendar.com"
  timeout_seconds: 45
```
        """
        )

        # Set one environment variable to override
        original_env = os.environ.get("GOOGLE_CALENDAR_ID")
        os.environ["GOOGLE_CALENDAR_ID"] = "env@calendar.com"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = CalendarConfigService()
                    config = service.get_config("test-user-1354")

                    # Verify priority order:
                    # 1. calendar_id from env var (highest)
                    assert config.calendar_id == "env@calendar.com"

                    # 2. timeout_seconds from PIPER.user.md (middle)
                    assert config.timeout_seconds == 45

                    # 3. circuit_timeout from defaults (lowest)
                    assert config.circuit_timeout == 300

                    # Also verify user config values used when no env var
                    assert config.client_secrets_file == "user_credentials.json"
                    # Issue #734: user-scoped, same as the other token_file assertions above.
                    assert config.token_file == "user_token_test-user-1354.json"
        finally:
            # Clean up environment
            if original_env is None:
                os.environ.pop("GOOGLE_CALENDAR_ID", None)
            else:
                os.environ["GOOGLE_CALENDAR_ID"] = original_env
