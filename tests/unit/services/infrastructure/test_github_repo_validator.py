"""
Tests for GitHub Repository Validator.

Issue #867: Soft validation via GitHub API when linking repositories.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Repository
from services.infrastructure.github_repo_validator import (
    RepoValidationResult,
    apply_validation_metadata,
    get_github_token,
    validate_github_repo,
)


class TestRepoValidationResult:
    """Tests for the RepoValidationResult dataclass."""

    def test_metadata_available_on_success(self):
        result = RepoValidationResult(validated=True, exists=True, accessible=True)
        assert result.metadata_available is True

    def test_metadata_not_available_when_not_validated(self):
        result = RepoValidationResult(validated=False, exists=False, accessible=False)
        assert result.metadata_available is False

    def test_metadata_not_available_when_not_found(self):
        result = RepoValidationResult(validated=True, exists=False, accessible=False)
        assert result.metadata_available is False


class TestGetGithubToken:
    """Tests for token resolution from environment."""

    def test_returns_github_token(self):
        with patch.dict("os.environ", {"GITHUB_TOKEN": "ghp_abc123"}, clear=False):
            assert get_github_token() == "ghp_abc123"

    def test_falls_back_to_gh_token(self):
        env = {"GH_TOKEN": "ghp_fallback"}
        with patch.dict("os.environ", env, clear=True):
            assert get_github_token() == "ghp_fallback"

    def test_returns_none_when_no_token(self):
        with patch.dict("os.environ", {}, clear=True):
            assert get_github_token() is None


class TestValidateGithubRepo:
    """Tests for the async validation function."""

    @pytest.mark.asyncio
    async def test_skips_when_no_token(self):
        with patch.dict("os.environ", {}, clear=True):
            result = await validate_github_repo("owner/repo", token=None)
        assert result.validated is False
        assert result.error is None  # Not an error — token simply absent
        assert result.not_checked_reason == "no_credential"

    @staticmethod
    def _mock_aiohttp(mock_response):
        """Create properly nested async context manager mocks for aiohttp."""
        # Inner context manager: session.get() -> response
        mock_get_cm = MagicMock()
        mock_get_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_cm.__aexit__ = AsyncMock(return_value=False)

        # Session with .get() method
        mock_session = MagicMock()
        mock_session.get.return_value = mock_get_cm

        # Outer context manager: ClientSession() -> session
        mock_session_cm = MagicMock()
        mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_cm.__aexit__ = AsyncMock(return_value=False)

        return mock_session_cm, mock_session

    @pytest.mark.asyncio
    async def test_success_populates_metadata(self):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "description": "A cool repo",
                "language": "Python",
                "visibility": "public",
                "default_branch": "main",
                "stargazers_count": 42,
            }
        )

        mock_session_cm, _ = self._mock_aiohttp(mock_response)

        with patch(
            "services.infrastructure.github_repo_validator.aiohttp.ClientSession",
            return_value=mock_session_cm,
        ):
            result = await validate_github_repo("owner/repo", token="ghp_test")

        assert result.validated is True
        assert result.exists is True
        assert result.accessible is True
        assert result.description == "A cool repo"
        assert result.language == "Python"
        assert result.visibility == "public"
        assert result.default_branch == "main"
        assert result.status_code == 200
        assert result.not_checked_reason is None

    @pytest.mark.asyncio
    async def test_404_returns_not_found(self):
        mock_response = MagicMock()
        mock_response.status = 404

        mock_session_cm, _ = self._mock_aiohttp(mock_response)

        with patch(
            "services.infrastructure.github_repo_validator.aiohttp.ClientSession",
            return_value=mock_session_cm,
        ):
            result = await validate_github_repo("owner/nonexistent", token="ghp_test")

        assert result.validated is True
        assert result.exists is False
        assert "not found" in result.error
        assert result.status_code == 404
        assert result.not_checked_reason is None

    @pytest.mark.asyncio
    async def test_401_returns_auth_error(self):
        mock_response = MagicMock()
        mock_response.status = 401

        mock_session_cm, _ = self._mock_aiohttp(mock_response)

        with patch(
            "services.infrastructure.github_repo_validator.aiohttp.ClientSession",
            return_value=mock_session_cm,
        ):
            result = await validate_github_repo("owner/repo", token="ghp_bad")

        assert result.validated is True
        assert result.accessible is False
        assert "invalid or expired" in result.error
        assert result.status_code == 401
        assert result.not_checked_reason is None

    @pytest.mark.asyncio
    @pytest.mark.parametrize("status", [403, 500, 502])
    async def test_403_and_other_statuses_set_status_code(self, status):
        mock_response = MagicMock()
        mock_response.status = status

        mock_session_cm, _ = self._mock_aiohttp(mock_response)

        with patch(
            "services.infrastructure.github_repo_validator.aiohttp.ClientSession",
            return_value=mock_session_cm,
        ):
            result = await validate_github_repo("owner/repo", token="ghp_test")

        assert result.validated is True
        assert result.status_code == status
        assert result.not_checked_reason == (None if status == 403 else "error")

    @pytest.mark.asyncio
    async def test_network_error_returns_graceful_failure(self):
        import aiohttp as _aiohttp

        # Session whose .get() raises a network error
        mock_session = MagicMock()
        mock_session.get.side_effect = _aiohttp.ClientError("Connection failed")

        mock_session_cm = MagicMock()
        mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_cm.__aexit__ = AsyncMock(return_value=False)

        with patch(
            "services.infrastructure.github_repo_validator.aiohttp.ClientSession",
            return_value=mock_session_cm,
        ):
            result = await validate_github_repo("owner/repo", token="ghp_test")

        assert result.validated is False
        assert "Network error" in result.error
        assert result.not_checked_reason == "network"

    @pytest.mark.asyncio
    async def test_unexpected_exception_reason_is_error(self):
        mock_session = MagicMock()
        mock_session.get.side_effect = RuntimeError("boom")
        mock_session_cm = MagicMock()
        mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_cm.__aexit__ = AsyncMock(return_value=False)

        with patch(
            "services.infrastructure.github_repo_validator.aiohttp.ClientSession",
            return_value=mock_session_cm,
        ):
            result = await validate_github_repo("owner/repo", token="ghp_test")

        assert result.validated is False
        assert result.not_checked_reason == "error"


class TestApplyValidationMetadata:
    """Tests for merging metadata into domain entity."""

    def test_applies_metadata_on_success(self):
        repo = Repository(full_name="owner/repo")
        result = RepoValidationResult(
            validated=True,
            exists=True,
            accessible=True,
            description="A repo",
            language="Python",
            visibility="public",
            default_branch="main",
        )
        apply_validation_metadata(repo, result)
        assert repo.description == "A repo"
        assert repo.language == "Python"
        assert repo.visibility == "public"
        assert repo.default_branch == "main"

    def test_does_not_apply_when_not_validated(self):
        repo = Repository(full_name="owner/repo")
        result = RepoValidationResult(validated=False, exists=False, accessible=False)
        apply_validation_metadata(repo, result)
        assert repo.description is None
        assert repo.language is None
