"""#1327 gap 3 — GET /api/v1/settings/integrations/github/repositories OAuth-connector cutover.

The Settings repo-config dropdown now prefers the per-user OAuth connector
(``GitHubMCPSpatialAdapter.search_user_repositories`` → ``search_repositories`` user:@me),
mirroring the #1322 chat-read cutover. Native-PAT is the fallback ONLY when the user is not
OAuth-connected (``CONNECT_REQUIRED``). Connected-but-degraded (server unreachable / re-auth)
→ honest error, never a silent PAT fallback / silent empty (#1231).

These tests patch the adapter method + the (transitional) native-PAT path and assert the
decision rail. The selection-merge (``selected`` flags from saved prefs) is unchanged from
the pre-cutover handler and re-asserted here on the connector path.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubReposResult
from web.api.routes.settings_integrations import get_github_repositories

_ADAPTER = "web.api.routes.settings_integrations.GitHubMCPSpatialAdapter"
_PREFS = "web.api.routes.settings_integrations._load_github_prefs_db"

# A connector hit: two repos in the normalized GitHubRepositoryInfo shape.
_REPOS = [
    {
        "id": 123,
        "name": "piper-morgan-product",
        "full_name": "mediajunkie/piper-morgan-product",
        "description": "Piper Morgan AI Assistant",
    },
    {
        "id": 456,
        "name": "other-project",
        "full_name": "mediajunkie/other-project",
        "description": "",
    },
]


def _adapter_returning(result):
    """An adapter class whose search_user_repositories returns the given result."""
    instance = MagicMock()
    instance.search_user_repositories = AsyncMock(return_value=result)
    cls = MagicMock(return_value=instance)
    return cls, instance


def _degrade(reason):
    return GitHubReposResult(
        degradation=DegradationResponse(
            reason=reason, user_message=f"msg:{reason.value}", action_hint="/connect"
        )
    )


class TestRepositoriesConnectorPath:
    """The connector is preferred when the user is OAuth-connected (binding present)."""

    @pytest.mark.asyncio
    async def test_connector_hit_returns_repos_without_native_pat(self):
        mock_user = MagicMock()
        mock_user.sub = "user-uuid-1"

        cls, instance = _adapter_returning(GitHubReposResult(repositories=_REPOS))

        with (
            patch(_ADAPTER, cls),
            patch(_PREFS, new=AsyncMock(return_value={})),
            # If the native PAT path were taken, this aiohttp call would blow up the test.
            patch("aiohttp.ClientSession", side_effect=AssertionError("native PAT used")),
        ):
            result = await get_github_repositories(current_user=mock_user)

        instance.search_user_repositories.assert_awaited_once()
        assert [r.full_name for r in result.repositories] == [
            "mediajunkie/piper-morgan-product",
            "mediajunkie/other-project",
        ]
        assert result.repositories[0].id == 123
        assert result.repositories[0].description == "Piper Morgan AI Assistant"

    @pytest.mark.asyncio
    async def test_connector_hit_merges_selected_flag_from_prefs(self):
        mock_user = MagicMock()
        mock_user.sub = "user-uuid-1"

        cls, _ = _adapter_returning(GitHubReposResult(repositories=_REPOS))
        saved = {"selected_repositories": ["mediajunkie/other-project"]}

        with (
            patch(_ADAPTER, cls),
            patch(_PREFS, new=AsyncMock(return_value=saved)),
            patch("aiohttp.ClientSession", side_effect=AssertionError("native PAT used")),
        ):
            result = await get_github_repositories(current_user=mock_user)

        by_name = {r.full_name: r for r in result.repositories}
        assert by_name["mediajunkie/other-project"].selected is True
        assert by_name["mediajunkie/piper-morgan-product"].selected is False


class TestRepositoriesDegradedHonest:
    """Connected-but-degraded → honest error (>=500), never a silent PAT fallback (#1231)."""

    @pytest.mark.asyncio
    async def test_unreachable_degrade_raises_not_pat_fallback(self):
        from fastapi import HTTPException

        mock_user = MagicMock()
        mock_user.sub = "user-uuid-1"

        cls, _ = _adapter_returning(_degrade(DegradationReason.UNREACHABLE))

        with (
            patch(_ADAPTER, cls),
            patch("aiohttp.ClientSession", side_effect=AssertionError("native PAT used")),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await get_github_repositories(current_user=mock_user)

        assert exc_info.value.status_code >= 500
        assert "msg:unreachable" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_stale_token_degrade_raises_not_pat_fallback(self):
        from fastapi import HTTPException

        mock_user = MagicMock()
        mock_user.sub = "user-uuid-1"

        cls, _ = _adapter_returning(_degrade(DegradationReason.STALE_TOKEN))

        with (
            patch(_ADAPTER, cls),
            patch("aiohttp.ClientSession", side_effect=AssertionError("native PAT used")),
        ):
            with pytest.raises(HTTPException) as exc_info:
                await get_github_repositories(current_user=mock_user)

        assert exc_info.value.status_code >= 500


class TestRepositoriesConnectRequiredFallsBackToPat:
    """Not OAuth-connected (CONNECT_REQUIRED) → transitional native-PAT fallback (unchanged)."""

    @pytest.mark.asyncio
    async def test_connect_required_uses_native_pat(self):
        mock_user = MagicMock()
        mock_user.sub = "user-uuid-1"

        cls, _ = _adapter_returning(_degrade(DegradationReason.CONNECT_REQUIRED))

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "ghp_test_token"

        mock_github_response = [
            {
                "id": 999,
                "name": "native-repo",
                "full_name": "mediajunkie/native-repo",
                "description": "from PAT",
            }
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
            patch(_ADAPTER, cls),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
            patch(_PREFS, new=AsyncMock(return_value={})),
        ):
            result = await get_github_repositories(current_user=mock_user)

        assert len(result.repositories) == 1
        assert result.repositories[0].full_name == "mediajunkie/native-repo"

    @pytest.mark.asyncio
    async def test_connect_required_and_no_pat_returns_401(self):
        from fastapi import HTTPException

        mock_user = MagicMock()
        mock_user.sub = "user-uuid-1"

        cls, _ = _adapter_returning(_degrade(DegradationReason.CONNECT_REQUIRED))

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        with (
            patch(_ADAPTER, cls),
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
        ):
            import os

            old_github = os.environ.pop("GITHUB_TOKEN", None)
            old_gh = os.environ.pop("GH_TOKEN", None)
            try:
                with pytest.raises(HTTPException) as exc_info:
                    await get_github_repositories(current_user=mock_user)
                assert exc_info.value.status_code == 401
            finally:
                if old_github:
                    os.environ["GITHUB_TOKEN"] = old_github
                if old_gh:
                    os.environ["GH_TOKEN"] = old_gh
