"""
Config service user isolation tests.

Phase 7 of Issue #734: Multi-Tenancy Isolation Architecture Implementation

These tests verify that config services require user_id and return user-scoped
credentials rather than global credentials.
"""

from unittest.mock import Mock, patch

import pytest


class TestSlackConfigServiceIsolation:
    """Verify Slack config service returns user-scoped credentials."""

    def test_get_config_requires_user_id(self):
        """SlackConfigService.get_config() must require user_id parameter."""
        from services.integrations.slack.config_service import SlackConfigService

        config_service = SlackConfigService()

        # Calling without user_id should raise TypeError (missing required arg)
        with pytest.raises(TypeError):
            config_service.get_config()

    def test_get_config_rejects_none_user_id(self):
        """get_config() must raise ValueError if user_id is None."""
        from services.integrations.slack.config_service import SlackConfigService

        config_service = SlackConfigService()

        with pytest.raises(ValueError, match="user_id is required"):
            config_service.get_config(user_id=None)

    def test_get_config_rejects_empty_user_id(self):
        """get_config() must raise ValueError if user_id is empty string."""
        from services.integrations.slack.config_service import SlackConfigService

        config_service = SlackConfigService()

        with pytest.raises(ValueError, match="user_id is required"):
            config_service.get_config(user_id="")

    def test_different_users_get_different_tokens(self):
        """Different users should get their own tokens, not shared tokens."""
        from services.integrations.slack.config_service import SlackConfigService

        # Mock keychain to return different tokens for different users
        with patch(
            "services.infrastructure.keychain_service.KeychainService"
        ) as mock_keychain_class:
            mock_keychain = Mock()
            mock_keychain_class.return_value = mock_keychain

            # Setup: user_a has token_a, user_b has token_b
            def get_api_key_side_effect(provider, username=None):
                if username == "user_a" and provider == "slack_bot":
                    return "token_for_user_a"
                elif username == "user_b" and provider == "slack_bot":
                    return "token_for_user_b"
                return None

            mock_keychain.get_api_key.side_effect = get_api_key_side_effect

            config_service = SlackConfigService()

            # User A gets their token
            config_a = config_service.get_config(user_id="user_a")
            # User B gets their token
            config_b = config_service.get_config(user_id="user_b")

            # Tokens should be different
            assert config_a.bot_token != config_b.bot_token
            assert config_a.bot_token == "token_for_user_a"
            assert config_b.bot_token == "token_for_user_b"

    def test_is_configured_requires_user_id(self):
        """is_configured() must require user_id parameter."""
        from services.integrations.slack.config_service import SlackConfigService

        config_service = SlackConfigService()

        with pytest.raises(TypeError):
            config_service.is_configured()


class TestCalendarConfigServiceIsolation:
    """Verify Calendar config service returns user-scoped credentials."""

    def test_get_config_requires_user_id(self):
        """CalendarConfigService.get_config() must require user_id parameter."""
        from services.integrations.calendar.config_service import CalendarConfigService

        config_service = CalendarConfigService()

        with pytest.raises(TypeError):
            config_service.get_config()

    def test_get_config_rejects_none_user_id(self):
        """get_config() must raise ValueError if user_id is None."""
        from services.integrations.calendar.config_service import CalendarConfigService

        config_service = CalendarConfigService()

        with pytest.raises(ValueError, match="user_id is required"):
            config_service.get_config(user_id=None)

    def test_is_configured_requires_user_id(self):
        """is_configured() must require user_id parameter."""
        from services.integrations.calendar.config_service import CalendarConfigService

        config_service = CalendarConfigService()

        with pytest.raises(TypeError):
            config_service.is_configured()


class TestGitHubConfigServiceIsolation:
    """Verify GitHub config service returns user-scoped credentials."""

    def test_get_authentication_token_requires_user_id(self):
        """get_authentication_token() must require user_id parameter."""
        from services.integrations.github.config_service import GitHubConfigService

        config_service = GitHubConfigService()

        with pytest.raises(TypeError):
            config_service.get_authentication_token()

    def test_get_authentication_token_rejects_none_user_id(self):
        """get_authentication_token() must raise ValueError if user_id is None."""
        from services.integrations.github.config_service import GitHubConfigService

        config_service = GitHubConfigService()

        with pytest.raises(ValueError, match="user_id is required"):
            config_service.get_authentication_token(user_id=None)

    def test_get_config_requires_user_id(self):
        """get_config() must require user_id parameter."""
        from services.integrations.github.config_service import GitHubConfigService

        config_service = GitHubConfigService()

        with pytest.raises(TypeError):
            config_service.get_config()

    def test_is_configured_requires_user_id(self):
        """is_configured() must require user_id parameter."""
        from services.integrations.github.config_service import GitHubConfigService

        config_service = GitHubConfigService()

        with pytest.raises(TypeError):
            config_service.is_configured()


class TestNotionConfigServiceIsolation:
    """Verify Notion config service returns user-scoped credentials."""

    def test_get_config_requires_user_id(self):
        """NotionConfigService.get_config() must require user_id parameter."""
        from services.integrations.notion.config_service import NotionConfigService

        config_service = NotionConfigService()

        with pytest.raises(TypeError):
            config_service.get_config()

    def test_get_config_rejects_none_user_id(self):
        """get_config() must raise ValueError if user_id is None."""
        from services.integrations.notion.config_service import NotionConfigService

        config_service = NotionConfigService()

        with pytest.raises(ValueError, match="user_id is required"):
            config_service.get_config(user_id=None)

    def test_is_configured_requires_user_id(self):
        """is_configured() must require user_id parameter."""
        from services.integrations.notion.config_service import NotionConfigService

        config_service = NotionConfigService()

        with pytest.raises(TypeError):
            config_service.is_configured()


class TestCrossUserTokenIsolation:
    """Cross-user token isolation verification tests."""

    def test_user_a_cannot_access_user_b_slack_token(self):
        """User A's query must not return User B's Slack bot token."""
        from services.integrations.slack.config_service import SlackConfigService

        with patch(
            "services.infrastructure.keychain_service.KeychainService"
        ) as mock_keychain_class:
            mock_keychain = Mock()
            mock_keychain_class.return_value = mock_keychain

            # Only user_b has a token stored
            def get_api_key_side_effect(provider, username=None):
                if username == "user_b" and provider == "slack_bot":
                    return "user_b_secret_token"
                return None

            mock_keychain.get_api_key.side_effect = get_api_key_side_effect

            config_service = SlackConfigService()

            # User A queries - should NOT get User B's token
            config_a = config_service.get_config(user_id="user_a")

            # User A should get no token (empty string is the default)
            assert config_a.bot_token == ""
            assert config_a.bot_token != "user_b_secret_token"

    def test_user_a_cannot_access_user_b_github_token(self, monkeypatch):
        """User A's query must not return User B's token NOR the system env floor.

        #1461 (PM decision (a), 2026-08-01): the env token is system-only — a real
        user without their own PAT gets None, never the shared credential. The
        sentinel injected below makes this assertion MEANINGFUL in keyless CI:
        before it, keyless CI passed this test vacuously (no env token existed to
        leak), while every keyed seat failed it (m-44 false-clear shape).
        """
        from services.integrations.github.config_service import GitHubConfigService

        # The floor credential that must NOT reach a real user (all four
        # env vars get_authentication_token consults; one suffices, set all
        # to defeat any precedence reshuffle).
        for var in ("GITHUB_TOKEN", "GITHUB_API_TOKEN", "GH_TOKEN"):
            monkeypatch.setenv(var, "system-floor-sentinel-must-not-leak")

        with patch(
            "services.infrastructure.keychain_service.KeychainService"
        ) as mock_keychain_class:
            mock_keychain = Mock()
            mock_keychain_class.return_value = mock_keychain

            # Only user_b has a token stored
            def get_api_key_side_effect(provider, username=None):
                if username == "user_b" and provider == "github_token":
                    return "user_b_github_secret"
                return None

            mock_keychain.get_api_key.side_effect = get_api_key_side_effect

            config_service = GitHubConfigService()

            # User A queries - should NOT get User B's token
            token_a = config_service.get_authentication_token(user_id="user_a")

            # User A should get no token — not user_b's, and not the env floor
            assert token_a is None
            assert token_a != "user_b_github_secret"

    def test_system_identity_still_receives_env_floor(self, monkeypatch):
        """The other half of #1461 decision (a): 'system' (no real user) keeps the
        env credential — the floor narrowed to system-only, it didn't vanish."""
        from services.integrations.github.config_service import GitHubConfigService

        monkeypatch.setenv("GITHUB_TOKEN", "system-floor-sentinel")

        with patch(
            "services.infrastructure.keychain_service.KeychainService"
        ) as mock_keychain_class:
            mock_keychain = Mock()
            mock_keychain_class.return_value = mock_keychain
            mock_keychain.get_api_key.return_value = None

            token = GitHubConfigService().get_authentication_token(user_id="system")
            assert token == "system-floor-sentinel"
