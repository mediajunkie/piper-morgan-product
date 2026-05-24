"""Tests for Action Registry and Command Pattern.

Issue #695 (WIRE-GH-ISSUE) update: ``GithubIssueCommand`` no longer returns
mock data; it dispatches to ``GitHubDomainService.create_issue``. Tests below
inject a mock service via ``context["github_service"]`` so we don't touch
real GitHub. Deeper coverage (error paths, signature regression for #1112)
lives in ``test_github_issue_command_695.py``.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from services.actions import ActionRegistry
from services.actions.commands import BaseCommand, GithubIssueCommand


def _mock_github_service(issue_payload=None):
    """Build a mock GitHubDomainService that returns a realistic issue dict."""
    payload = issue_payload or {
        "number": 4242,
        "html_url": "https://github.com/test-org/test-repo/issues/4242",
        "title": "stub",
    }
    svc = MagicMock()
    svc.create_issue = AsyncMock(return_value=payload)
    return svc


class TestActionRegistry:
    """Test ActionRegistry functionality"""

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_github_issue_command(self):
        """Test GitHub issue creation command — wires to GitHubDomainService."""
        params = {
            "title": "Test issue from unit test",
            "repo": "test-org/test-repo",
            "labels": ["test", "automated"],
            "assignees": ["xian"],
        }
        github_svc = _mock_github_service(
            {"number": 7777, "html_url": "https://github.com/test-org/test-repo/issues/7777"}
        )
        context = {
            "user_id": "test-user-123",
            "session_id": "test-session-456",
            "github_service": github_svc,
        }

        result = await ActionRegistry.execute("create_github_issue", params, context)

        assert result["status"] == "success"
        assert result["action"] == "create_github_issue"
        assert result["title"] == "Test issue from unit test"
        assert result["labels"] == ["test", "automated"]
        assert result["repo"] == "test-org/test-repo"
        # Real issue identity replaces mock-123:
        assert result["issue_id"] == 7777
        assert result["issue_url"] == "https://github.com/test-org/test-repo/issues/7777"
        assert "message" in result
        github_svc.create_issue.assert_awaited_once_with(
            repo_name="test-org/test-repo",
            title="Test issue from unit test",
            body="",
            labels=["test", "automated"],
            assignees=["xian"],
        )

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_github_issue_command_defaults(self):
        """Test GitHub issue creation with default parameters."""
        params = {"repo": "test-org/test-repo"}
        github_svc = _mock_github_service()
        context = {"user_id": "test-user-123", "github_service": github_svc}

        result = await ActionRegistry.execute("create_github_issue", params, context)

        assert result["status"] == "success"
        assert result["title"] == "Action item from standup"
        assert result["labels"] == ["standup", "action-item"]

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_unknown_action(self):
        """Test unknown action raises ValueError"""
        params = {}
        context = {"user_id": "test-user-123"}

        with pytest.raises(ValueError) as exc_info:
            await ActionRegistry.execute("unknown_action", params, context)

        assert "Unknown action type: unknown_action" in str(exc_info.value)
        assert "Available: create_github_issue" in str(exc_info.value)

    @pytest.mark.smoke
    def test_is_registered(self):
        """Test checking if action is registered"""
        assert ActionRegistry.is_registered("create_github_issue") is True
        assert ActionRegistry.is_registered("unknown_action") is False

    @pytest.mark.smoke
    def test_list_actions(self):
        """Test listing all registered actions"""
        actions = ActionRegistry.list_actions()
        assert isinstance(actions, list)
        assert "create_github_issue" in actions
        assert len(actions) >= 1  # At least one action registered


class TestGithubIssueCommand:
    """Test GithubIssueCommand directly"""

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_execute_success(self):
        """Test successful execution via injected GitHubDomainService mock."""
        github_svc = _mock_github_service(
            {"number": 999, "html_url": "https://github.com/test-org/test-repo/issues/999"}
        )
        params = {"title": "Direct test", "repo": "test-org/test-repo", "labels": ["direct"]}
        context = {"user_id": "test-123", "github_service": github_svc}

        command = GithubIssueCommand(params, context)
        result = await command.execute()

        assert result["status"] == "success"
        assert result["title"] == "Direct test"
        assert result["labels"] == ["direct"]
        assert result["issue_id"] == 999

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_validate_params(self):
        """Test parameter validation (currently no-op but should not raise)"""
        params = {}
        context = {}

        command = GithubIssueCommand(params, context)
        # Should not raise
        command.validate_params()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_rollback_not_implemented(self):
        """Test rollback raises NotImplementedError for alpha"""
        params = {}
        context = {}

        command = GithubIssueCommand(params, context)

        with pytest.raises(NotImplementedError) as exc_info:
            await command.rollback()

        assert "Rollback not implemented in alpha" in str(exc_info.value)


class TestBaseCommand:
    """Test BaseCommand abstract class"""

    @pytest.mark.smoke
    def test_cannot_instantiate_directly(self):
        """Test that BaseCommand cannot be instantiated directly"""
        with pytest.raises(TypeError):
            BaseCommand({}, {})

    @pytest.mark.smoke
    def test_subclass_must_implement_execute(self):
        """Test that subclass must implement execute()"""

        class IncompleteCommand(BaseCommand):
            pass

        with pytest.raises(TypeError):
            IncompleteCommand({}, {})
