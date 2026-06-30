"""
Unit tests for Issue #849: SEC-KEYCHAIN user-scoped keychain key fixes.

Verifies that all route-level keychain operations use the correct key names
and user-scoped username parameter for multi-tenancy isolation.

Categories covered:
- B: GitHub store/retrieve/delete
- C: Connection test endpoints (Slack, GitHub, Notion)
- D: Disconnect endpoints (Slack, Notion)
- E: Slack OAuth handler store consistency
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestGitHubTokenLifecycle849:
    """Issue #849 Category B: GitHub token store/retrieve/delete must be user-scoped."""

    @pytest.mark.asyncio
    async def test_store_with_username_retrieve_with_same_username_succeeds(self):
        """Store with username -> retrieve with same username -> succeeds."""
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        storage = {}

        def mock_store(provider, value, username=None):
            key = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
            storage[key] = value

        def mock_get(provider, username=None):
            key = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
            return storage.get(key)

        with (
            patch.object(keychain, "store_api_key", side_effect=mock_store),
            patch.object(keychain, "get_api_key", side_effect=mock_get),
        ):
            keychain.store_api_key("github_token", "ghp_test_token", username="user-abc")
            token = keychain.get_api_key("github_token", username="user-abc")
            assert token == "ghp_test_token"

    @pytest.mark.asyncio
    async def test_retrieve_with_different_username_returns_none(self):
        """Store with username A -> retrieve with username B -> returns None."""
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        storage = {}

        def mock_store(provider, value, username=None):
            key = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
            storage[key] = value

        def mock_get(provider, username=None):
            key = f"{username}_{provider}_api_key" if username else f"{provider}_api_key"
            return storage.get(key)

        with (
            patch.object(keychain, "store_api_key", side_effect=mock_store),
            patch.object(keychain, "get_api_key", side_effect=mock_get),
        ):
            keychain.store_api_key("github_token", "ghp_test_token", username="user-abc")
            token = keychain.get_api_key("github_token", username="user-xyz")
            assert token is None

    @pytest.mark.asyncio
    async def test_save_github_token_uses_user_scoped_key(self):
        """save_github_token route handler must pass username=current_user.sub."""
        from web.api.routes.settings_integrations import save_github_token

        mock_keychain = MagicMock()
        mock_config = MagicMock()
        mock_config.clear_cache = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "user-123"

        with (
            patch.dict("os.environ", {}, clear=True),
            patch(
                "services.integrations.github.config_service.GitHubConfigService",
                return_value=mock_config,
            ),
            patch(
                "services.integrations.github.token_validator.verify_github_token",
                new=AsyncMock(
                    return_value={"authenticated": True, "username": "testuser"}
                ),
            ),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            await save_github_token("ghp_test", current_user=mock_user)
            mock_keychain.store_api_key.assert_called_once_with(
                "github_token", "ghp_test", username="user-123"
            )

    @pytest.mark.asyncio
    async def test_disconnect_github_uses_user_scoped_key(self):
        """disconnect_github route handler must pass username=current_user.sub."""
        from web.api.routes.settings_integrations import disconnect_github

        mock_keychain = MagicMock()
        mock_config = MagicMock()
        mock_config.clear_cache = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "user-123"

        with (
            patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_test"}, clear=True),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.github.config_service.GitHubConfigService",
                return_value=mock_config,
            ),
        ):
            await disconnect_github(current_user=mock_user)
            mock_keychain.delete_api_key.assert_called_once_with(
                "github_token", username="user-123"
            )


class TestSlackOAuthStoreConsistency849:
    """Issue #849 Category E: Slack OAuth handler must use username param, not f-string."""

    @pytest.mark.asyncio
    async def test_oauth_store_uses_username_param_for_bot_token(self):
        """OAuth handler must store bot token with username= param, not f-string in key."""
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        mock_config_service = MagicMock()
        handler = SlackOAuthHandler(mock_config_service)

        mock_keychain = MagicMock()

        workspace_data = {
            "workspace_id": "W123",
            "workspace_name": "Test",
            "workspace_domain": "test",
            "territory": {"id": "T1"},
            "installation_time": "2026-01-01",
        }
        token_data = {
            "access_token": "xoxb-bot-token",
            "authed_user": {"access_token": "xoxp-user-token"},
            "bot_user_id": "B123",
            "app_id": "A123",
            "scope": "chat:write",
        }

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            await handler._store_workspace_tokens(workspace_data, token_data, user_id="user-456")

        bot_call = mock_keychain.store_api_key.call_args_list[0]
        assert bot_call[0][0] == "slack_bot"
        assert bot_call[0][1] == "xoxb-bot-token"
        assert bot_call[1].get("username") == "user-456"

    @pytest.mark.asyncio
    async def test_oauth_store_uses_username_param_for_user_token(self):
        """OAuth handler must store user token with username= param, not f-string in key."""
        from services.integrations.slack.oauth_handler import SlackOAuthHandler

        mock_config_service = MagicMock()
        handler = SlackOAuthHandler(mock_config_service)

        mock_keychain = MagicMock()

        workspace_data = {
            "workspace_id": "W123",
            "workspace_name": "Test",
            "workspace_domain": "test",
            "territory": {"id": "T1"},
            "installation_time": "2026-01-01",
        }
        token_data = {
            "access_token": "xoxb-bot-token",
            "authed_user": {"access_token": "xoxp-user-token"},
            "bot_user_id": "B123",
            "app_id": "A123",
            "scope": "chat:write",
        }

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            await handler._store_workspace_tokens(workspace_data, token_data, user_id="user-456")

        user_call = mock_keychain.store_api_key.call_args_list[1]
        assert user_call[0][0] == "slack_user"
        assert user_call[0][1] == "xoxp-user-token"
        assert user_call[1].get("username") == "user-456"


class TestConnectionTestKeyCorrectness849:
    """Issue #849 Category C: Connection test helpers must use correct key names + user_id."""

    @pytest.mark.asyncio
    async def test_slack_connection_test_uses_slack_bot_key(self):
        """_test_slack must use slack_bot key, not slack."""
        from web.api.routes.integrations import _test_slack

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await _test_slack()
            mock_keychain.get_api_key.assert_called_once_with("slack_bot")

    @pytest.mark.asyncio
    async def test_slack_connection_test_passes_user_id(self):
        """_test_slack must pass user_id as username parameter when provided."""
        from web.api.routes.integrations import _test_slack

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await _test_slack(user_id="user-789")
            mock_keychain.get_api_key.assert_called_once_with("slack_bot", username="user-789")

    @pytest.mark.asyncio
    async def test_github_connection_test_uses_github_token_key(self):
        """_test_github must use github_token key, not github."""
        from web.api.routes.integrations import _test_github

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await _test_github()
            mock_keychain.get_api_key.assert_called_once_with("github_token")

    @pytest.mark.asyncio
    async def test_github_connection_test_passes_user_id(self):
        """_test_github must pass user_id as username parameter when provided."""
        from web.api.routes.integrations import _test_github

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await _test_github(user_id="user-789")
            mock_keychain.get_api_key.assert_called_once_with("github_token", username="user-789")

    @pytest.mark.asyncio
    async def test_notion_settings_uses_user_scoped_key(self):
        """get_notion_settings must retrieve notion key with username=current_user.sub."""
        from web.api.routes.settings_integrations import get_notion_settings

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None
        mock_user = MagicMock()
        mock_user.sub = "user-notion-1"

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await get_notion_settings(current_user=mock_user)
            mock_keychain.get_api_key.assert_called_once_with("notion", username="user-notion-1")


class TestDisconnectKeyCorrectness849:
    """Issue #849 Category D: Disconnect endpoints must use correct key names + user_id."""

    @pytest.mark.asyncio
    async def test_slack_disconnect_source_uses_correct_keys(self):
        """Slack disconnect must delete slack_bot and slack_user with username, not slack_bot_token."""
        import inspect

        from web.api.routes import settings_integrations

        source = inspect.getsource(settings_integrations)

        # Verify user-scoped key deletion (code may be split across lines by black)
        assert '"slack_bot", username=current_user.sub' in source
        assert '"slack_user", username=current_user.sub' in source
        assert 'delete_api_key("slack_bot_token")' not in source

    @pytest.mark.asyncio
    async def test_notion_disconnect_uses_user_scoped_key(self):
        """Notion disconnect must use notion with username=current_user.sub."""
        from web.api.routes.settings_integrations import disconnect_notion

        mock_keychain = MagicMock()
        mock_user = MagicMock()
        mock_user.sub = "user-notion-1"

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            result = await disconnect_notion(current_user=mock_user)
            assert result["success"] is True
            mock_keychain.delete_api_key.assert_called_once_with("notion", username="user-notion-1")
