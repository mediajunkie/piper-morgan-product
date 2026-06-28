"""
Unit tests for GitHub Repository Preferences API
Issue #573: GitHub repository preferences

Tests the GitHub repository list and preferences endpoints in settings_integrations.py.

WS-1 P4 (#1199 / #1226): the flat-file + in-memory GitHub-config stores were RETIRED — the
DB-backed connector_configs store is the SOLE home. The handlers now read/write through two
async helpers (``_load_github_prefs_db`` returns the user's github config blob directly;
``_save_github_prefs_db`` MERGE-writes it and RAISES on failure). These tests patch those
helpers; the file-storage and dual-write tests are gone with the machinery they covered.
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
                "web.api.routes.settings_integrations._load_github_prefs_db",
                new=AsyncMock(return_value={}),
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
        """Should return empty preferences when user has no saved preferences.

        WS-1 P4: ``_load_github_prefs_db`` returns the user's config blob directly (or {} on
        miss), no longer a dict keyed by user sub.
        """
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "web.api.routes.settings_integrations._load_github_prefs_db",
            new=AsyncMock(return_value={}),
        ):
            result = await get_github_preferences(current_user=mock_user)

            assert result.selected_repositories == []
            assert result.default_repository is None

    @pytest.mark.asyncio
    async def test_returns_saved_preferences(self):
        """Should return saved preferences for the user.

        WS-1 P4: the helper returns the user's config blob DIRECTLY — per-user isolation now
        lives in the DB layer (owner_id), so the blob is already this user's.
        """
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        saved_prefs = {
            "selected_repositories": [
                "mediajunkie/piper-morgan-product",
                "mediajunkie/other-project",
            ],
            "default_repository": "mediajunkie/piper-morgan-product",
        }

        with patch(
            "web.api.routes.settings_integrations._load_github_prefs_db",
            new=AsyncMock(return_value=saved_prefs),
        ):
            result = await get_github_preferences(current_user=mock_user)

            assert result.selected_repositories == [
                "mediajunkie/piper-morgan-product",
                "mediajunkie/other-project",
            ]
            assert result.default_repository == "mediajunkie/piper-morgan-product"


class TestSaveGitHubPreferences:
    """Tests for POST /api/v1/settings/integrations/github/preferences

    WS-1 P4 (#1199 / #1226): the DB is the SOLE store. ``save_github_preferences`` calls the
    single async helper ``_save_github_prefs_db(owner_sub, payload)``; a write failure must
    SURFACE as a 500 (no silent swallow — that would be data loss).
    """

    @pytest.mark.asyncio
    async def test_saves_calls_db_helper_with_payload(self):
        """Save awaits the DB helper exactly once with (str(sub), payload) and echoes it back."""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        preferences = GitHubPreferencesRequest(
            selected_repositories=[
                "mediajunkie/piper-morgan-product",
                "mediajunkie/other-project",
            ],
            default_repository="mediajunkie/piper-morgan-product",
        )

        save_db = AsyncMock()
        with patch("web.api.routes.settings_integrations._save_github_prefs_db", save_db):
            result = await save_github_preferences(preferences=preferences, current_user=mock_user)

        save_db.assert_awaited_once_with(
            "test-user-123",
            {
                "selected_repositories": [
                    "mediajunkie/piper-morgan-product",
                    "mediajunkie/other-project",
                ],
                "default_repository": "mediajunkie/piper-morgan-product",
            },
        )
        assert result.selected_repositories == [
            "mediajunkie/piper-morgan-product",
            "mediajunkie/other-project",
        ]
        assert result.default_repository == "mediajunkie/piper-morgan-product"

    @pytest.mark.asyncio
    async def test_save_surfaces_db_failure(self):
        """A DB write failure surfaces as HTTP 500 — the DB is the only store, so silent
        failure would be data loss."""
        from fastapi import HTTPException

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        preferences = GitHubPreferencesRequest(
            selected_repositories=["o/r"],
            default_repository="o/r",
        )

        with patch(
            "web.api.routes.settings_integrations._save_github_prefs_db",
            new=AsyncMock(side_effect=RuntimeError("DB down")),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await save_github_preferences(preferences=preferences, current_user=mock_user)

        assert exc_info.value.status_code == 500
