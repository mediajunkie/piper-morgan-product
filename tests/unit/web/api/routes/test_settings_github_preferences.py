"""
Unit tests for GitHub Repository Preferences API
Issue #573: GitHub repository preferences

Tests the GitHub repository list and preferences endpoints in settings_integrations.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    GitHubPreferencesRequest,
    get_github_preferences,
    get_github_repositories,
    save_github_preferences,
)


class TestGetGitHubRepositories:
    """Tests for GET /api/v1/settings/integrations/github/repositories"""

    @pytest.mark.asyncio
    async def test_returns_401_when_not_connected(self):
        """Should return 401 when no token configured.

        The function has two token sources: keychain and env vars.
        Both must return None for the 401 path to trigger.
        """
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # Patch at source (local import) AND block env var fallback
        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch.dict(
                "os.environ",
                {"GITHUB_TOKEN": "", "GH_TOKEN": ""},
                clear=False,
            ),
        ):
            # Clear any cached env values
            import os

            old_github = os.environ.pop("GITHUB_TOKEN", None)
            old_gh = os.environ.pop("GH_TOKEN", None)

            try:
                from fastapi import HTTPException

                with pytest.raises(HTTPException) as exc_info:
                    await get_github_repositories(current_user=mock_user)

                assert exc_info.value.status_code == 401
                assert "not connected" in str(exc_info.value.detail).lower()
            finally:
                if old_github:
                    os.environ["GITHUB_TOKEN"] = old_github
                if old_gh:
                    os.environ["GH_TOKEN"] = old_gh

    @pytest.mark.asyncio
    async def test_returns_repository_list_when_connected(self):
        """Should return list of repositories when connected"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "ghp_test_token"

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # Mock GitHub API response
        mock_github_response = [
            {
                "id": 123456789,
                "name": "piper-morgan-product",
                "full_name": "mediajunkie/piper-morgan-product",
                "description": "Piper Morgan AI Assistant",
            },
            {
                "id": 987654321,
                "name": "other-project",
                "full_name": "mediajunkie/other-project",
                "description": None,
            },
        ]

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_github_response)

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
            patch(
                "web.api.routes.settings_integrations._load_github_preferences",
                return_value={},
            ),
        ):
            result = await get_github_repositories(current_user=mock_user)

            assert len(result.repositories) == 2
            assert result.repositories[0].id == 123456789
            assert result.repositories[0].name == "piper-morgan-product"
            assert result.repositories[0].full_name == "mediajunkie/piper-morgan-product"
            assert result.repositories[0].description == "Piper Morgan AI Assistant"
            assert result.repositories[1].id == 987654321
            assert result.repositories[1].name == "other-project"
            assert result.repositories[1].description == ""

    @pytest.mark.asyncio
    async def test_returns_error_when_github_api_fails(self):
        """Should return error when GitHub API returns error"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "ghp_test_token"

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text = AsyncMock(return_value="Bad credentials")

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
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_github_repositories(current_user=mock_user)

            # Should return an error status (either 502 from our code or 500 from exception handling)
            assert exc_info.value.status_code >= 500


class TestGetGitHubPreferences:
    """Tests for GET /api/v1/settings/integrations/github/preferences"""

    @pytest.mark.asyncio
    async def test_returns_empty_preferences_when_not_saved(self):
        """Should return empty preferences when user has no saved preferences"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "web.api.routes.settings_integrations._load_github_preferences",
            return_value={},
        ):
            result = await get_github_preferences(current_user=mock_user)

            assert result.selected_repositories == []
            assert result.default_repository is None

    @pytest.mark.asyncio
    async def test_returns_saved_preferences(self):
        """Should return saved preferences for the user"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        saved_prefs = {
            "test-user-123": {
                "selected_repositories": [
                    "mediajunkie/piper-morgan-product",
                    "mediajunkie/other-project",
                ],
                "default_repository": "mediajunkie/piper-morgan-product",
            }
        }

        with patch(
            "web.api.routes.settings_integrations._load_github_preferences",
            return_value=saved_prefs,
        ):
            result = await get_github_preferences(current_user=mock_user)

            assert result.selected_repositories == [
                "mediajunkie/piper-morgan-product",
                "mediajunkie/other-project",
            ]
            assert result.default_repository == "mediajunkie/piper-morgan-product"

    @pytest.mark.asyncio
    async def test_returns_empty_for_different_user(self):
        """Should return empty for user without saved preferences"""
        mock_user = MagicMock()
        mock_user.sub = "different-user-456"

        saved_prefs = {
            "test-user-123": {
                "selected_repositories": ["mediajunkie/piper-morgan-product"],
                "default_repository": "mediajunkie/piper-morgan-product",
            }
        }

        with patch(
            "web.api.routes.settings_integrations._load_github_preferences",
            return_value=saved_prefs,
        ):
            result = await get_github_preferences(current_user=mock_user)

            assert result.selected_repositories == []
            assert result.default_repository is None


class TestSaveGitHubPreferences:
    """Tests for POST /api/v1/settings/integrations/github/preferences"""

    @pytest.mark.asyncio
    async def test_saves_preferences_successfully(self):
        """Should save preferences and return them"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        preferences = GitHubPreferencesRequest(
            selected_repositories=[
                "mediajunkie/piper-morgan-product",
                "mediajunkie/other-project",
            ],
            default_repository="mediajunkie/piper-morgan-product",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_github_preferences",
                return_value={},
            ),
            patch(
                "web.api.routes.settings_integrations._save_github_preferences",
                side_effect=mock_save,
            ),
            patch(
                "web.api.routes.settings_integrations._dual_write_github_prefs_to_db",
                new_callable=AsyncMock,
            ),
        ):
            result = await save_github_preferences(preferences=preferences, current_user=mock_user)

            assert result.selected_repositories == [
                "mediajunkie/piper-morgan-product",
                "mediajunkie/other-project",
            ]
            assert result.default_repository == "mediajunkie/piper-morgan-product"
            assert "test-user-123" in saved_data
            assert saved_data["test-user-123"]["selected_repositories"] == [
                "mediajunkie/piper-morgan-product",
                "mediajunkie/other-project",
            ]

    @pytest.mark.asyncio
    async def test_overwrites_existing_preferences(self):
        """Should overwrite existing preferences for the user"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        existing_prefs = {
            "test-user-123": {
                "selected_repositories": ["old-org/old-repo"],
                "default_repository": "old-org/old-repo",
            }
        }

        new_preferences = GitHubPreferencesRequest(
            selected_repositories=["new-org/new-repo"],
            default_repository="new-org/new-repo",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_github_preferences",
                return_value=existing_prefs,
            ),
            patch(
                "web.api.routes.settings_integrations._save_github_preferences",
                side_effect=mock_save,
            ),
            patch(
                "web.api.routes.settings_integrations._dual_write_github_prefs_to_db",
                new_callable=AsyncMock,
            ),
        ):
            result = await save_github_preferences(
                preferences=new_preferences, current_user=mock_user
            )

            assert result.selected_repositories == ["new-org/new-repo"]
            assert result.default_repository == "new-org/new-repo"
            assert saved_data["test-user-123"]["selected_repositories"] == ["new-org/new-repo"]

    @pytest.mark.asyncio
    async def test_preserves_other_users_preferences(self):
        """Should not affect other users' preferences"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        existing_prefs = {
            "other-user-456": {
                "selected_repositories": ["other-org/other-repo"],
                "default_repository": "other-org/other-repo",
            }
        }

        new_preferences = GitHubPreferencesRequest(
            selected_repositories=["my-org/my-repo"],
            default_repository="my-org/my-repo",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_github_preferences",
                return_value=existing_prefs,
            ),
            patch(
                "web.api.routes.settings_integrations._save_github_preferences",
                side_effect=mock_save,
            ),
            patch(
                "web.api.routes.settings_integrations._dual_write_github_prefs_to_db",
                new_callable=AsyncMock,
            ),
        ):
            await save_github_preferences(preferences=new_preferences, current_user=mock_user)

            # Other user's preferences should be preserved
            assert "other-user-456" in saved_data
            assert saved_data["other-user-456"]["selected_repositories"] == ["other-org/other-repo"]
            # New user's preferences should be added
            assert "test-user-123" in saved_data
            assert saved_data["test-user-123"]["selected_repositories"] == ["my-org/my-repo"]

    @pytest.mark.asyncio
    async def test_save_also_dual_writes_to_db(self):
        """WS-1 (#1226): save mirrors the github prefs into the DB-backed connector_configs store."""
        mock_user = MagicMock()
        mock_user.sub = "11111111-1111-1111-1111-111111111111"
        preferences = GitHubPreferencesRequest(
            selected_repositories=["o/r"], default_repository="o/r"
        )
        dual = AsyncMock()
        with (
            patch(
                "web.api.routes.settings_integrations._load_github_preferences",
                return_value={},
            ),
            patch("web.api.routes.settings_integrations._save_github_preferences"),
            patch("web.api.routes.settings_integrations._dual_write_github_prefs_to_db", dual),
        ):
            await save_github_preferences(preferences=preferences, current_user=mock_user)

        dual.assert_awaited_once()
        owner_arg, prefs_arg = dual.await_args.args
        assert owner_arg == "11111111-1111-1111-1111-111111111111"
        assert prefs_arg["default_repository"] == "o/r"

    @pytest.mark.asyncio
    async def test_dual_write_swallows_db_failure(self):
        """WS-1 (#1226): the dual-write helper is best-effort — a DB error is swallowed, not raised
        (the flat file is the source of truth; a save must never fail on the DB mirror)."""
        from web.api.routes.settings_integrations import _dual_write_github_prefs_to_db

        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            side_effect=RuntimeError("DB down"),
        ):
            # must NOT raise
            await _dual_write_github_prefs_to_db(
                "11111111-1111-1111-1111-111111111111", {"default_repository": "o/r"}
            )


class TestGitHubPreferencesFileStorage:
    """Tests for GitHub preferences file-based storage helpers"""

    def test_load_preferences_returns_empty_when_file_missing(self):
        """Should return empty dict when preferences file doesn't exist"""
        from web.api.routes.settings_integrations import _load_github_preferences

        with patch("os.path.exists", return_value=False):
            result = _load_github_preferences()
            assert result == {}

    def test_load_preferences_returns_data_when_file_exists(self):
        """Should return parsed JSON when file exists"""
        import json

        from web.api.routes.settings_integrations import _load_github_preferences

        test_data = {
            "user-123": {
                "selected_repositories": ["org/repo1"],
                "default_repository": "org/repo1",
            }
        }

        with (
            patch("os.path.exists", return_value=True),
            patch(
                "builtins.open",
                MagicMock(
                    return_value=MagicMock(
                        __enter__=MagicMock(
                            return_value=MagicMock(
                                read=MagicMock(return_value=json.dumps(test_data))
                            )
                        ),
                        __exit__=MagicMock(return_value=False),
                    )
                ),
            ),
            patch("json.load", return_value=test_data),
        ):
            result = _load_github_preferences()
            assert result == test_data

    def test_save_preferences_creates_directory(self):
        """Should create data directory if it doesn't exist"""
        from web.api.routes.settings_integrations import _save_github_preferences

        mock_makedirs = MagicMock()
        mock_open = MagicMock()
        mock_file = MagicMock()
        mock_open.return_value.__enter__ = MagicMock(return_value=mock_file)
        mock_open.return_value.__exit__ = MagicMock(return_value=False)

        with (
            patch("os.makedirs", mock_makedirs),
            patch("builtins.open", mock_open),
            patch("json.dump"),
        ):
            _save_github_preferences({"test": "data"})

            # Should call makedirs with exist_ok=True
            mock_makedirs.assert_called_once()
            assert mock_makedirs.call_args[1]["exist_ok"] is True
