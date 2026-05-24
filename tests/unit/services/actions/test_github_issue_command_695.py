"""Deep coverage for #695 GithubIssueCommand wire-to-real-GitHub + #1112 domain-service fix.

This file pairs with ``test_action_registry.py`` (which has the smoke
coverage). Here we drill into:

- Error paths: GitHub auth failure, rate limit, generic exception
- Missing-repo guard (params + context fallback)
- Result envelope contract (issue_id / issue_url defensive extraction)
- Default ``GitHubDomainService`` lazy-construction when no service injected
- Signature regression for ``GitHubDomainService.create_issue`` against the
  real ``GitHubIntegrationRouter`` contract (#1112)
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.actions.commands.github_issue_command import GithubIssueCommand
from services.api.errors import GitHubAuthFailedError, GitHubRateLimitError


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------


def _svc(side_effect=None, return_value=None):
    """Build a mock GitHubDomainService with the create_issue surface."""
    svc = MagicMock()
    svc.create_issue = AsyncMock(side_effect=side_effect, return_value=return_value)
    return svc


def _ok_issue(number=4242, repo="test-org/test-repo"):
    return {
        "number": number,
        "html_url": f"https://github.com/{repo}/issues/{number}",
        "title": "stub",
    }


# -------------------------------------------------------------------
# Happy path + envelope
# -------------------------------------------------------------------


class TestHappyPath:
    @pytest.mark.asyncio
    async def test_full_params_forwarded_to_service(self):
        """All params and an explicit owner/name slug forwarded as-is."""
        svc = _svc(return_value=_ok_issue(number=7777))
        params = {
            "title": "Action item",
            "body": "details here",
            "repo": "test-org/test-repo",
            "labels": ["bug", "auto"],
            "assignees": ["alice", "bob"],
        }
        cmd = GithubIssueCommand(params, {"github_service": svc})

        result = await cmd.execute()

        assert result["status"] == "success"
        assert result["issue_id"] == 7777
        assert result["issue_url"] == "https://github.com/test-org/test-repo/issues/7777"
        assert result["repo"] == "test-org/test-repo"
        svc.create_issue.assert_awaited_once_with(
            repo_name="test-org/test-repo",
            title="Action item",
            body="details here",
            labels=["bug", "auto"],
            assignees=["alice", "bob"],
        )

    @pytest.mark.asyncio
    async def test_defaults_when_optional_params_missing(self):
        """body→'', labels→standup defaults, assignees→[]."""
        svc = _svc(return_value=_ok_issue())
        params = {"repo": "test-org/test-repo"}
        cmd = GithubIssueCommand(params, {"github_service": svc})

        result = await cmd.execute()

        assert result["status"] == "success"
        assert result["title"] == "Action item from standup"
        svc.create_issue.assert_awaited_once_with(
            repo_name="test-org/test-repo",
            title="Action item from standup",
            body="",
            labels=["standup", "action-item"],
            assignees=[],
        )

    @pytest.mark.asyncio
    async def test_repo_falls_back_to_context_when_not_in_params(self):
        """If params lacks 'repo' but context has one, use context value."""
        svc = _svc(return_value=_ok_issue())
        cmd = GithubIssueCommand(
            {"title": "x"},
            {"github_service": svc, "repo": "ctx-org/ctx-repo"},
        )

        result = await cmd.execute()

        assert result["status"] == "success"
        assert result["repo"] == "ctx-org/ctx-repo"
        svc.create_issue.assert_awaited_once()
        kwargs = svc.create_issue.await_args.kwargs
        assert kwargs["repo_name"] == "ctx-org/ctx-repo"

    @pytest.mark.asyncio
    async def test_envelope_extracts_id_fallback_when_number_missing(self):
        """If router returns 'id' but not 'number', envelope still populates issue_id."""
        svc = _svc(return_value={"id": 99999, "url": "https://api.github.com/repos/x/x/issues/1"})
        cmd = GithubIssueCommand(
            {"repo": "test-org/test-repo"}, {"github_service": svc}
        )

        result = await cmd.execute()

        assert result["status"] == "success"
        assert result["issue_id"] == 99999
        assert result["issue_url"] == "https://api.github.com/repos/x/x/issues/1"


# -------------------------------------------------------------------
# Missing-repo guard
# -------------------------------------------------------------------


class TestMissingRepoGuard:
    @pytest.mark.asyncio
    async def test_no_repo_in_params_or_context_returns_error(self):
        """No repo anywhere → error envelope, no service call."""
        svc = _svc()
        cmd = GithubIssueCommand({"title": "x"}, {"github_service": svc})

        result = await cmd.execute()

        assert result["status"] == "error"
        assert "No repo specified" in result["error"]
        svc.create_issue.assert_not_awaited()


# -------------------------------------------------------------------
# Error paths
# -------------------------------------------------------------------


class TestErrorPaths:
    @pytest.mark.asyncio
    async def test_auth_failure_returns_error_envelope(self):
        """GitHubAuthFailedError → status=error with auth message."""
        svc = _svc(side_effect=GitHubAuthFailedError({"reason": "token rejected"}))
        cmd = GithubIssueCommand(
            {"repo": "test-org/test-repo"}, {"github_service": svc}
        )

        result = await cmd.execute()

        assert result["status"] == "error"
        assert result["error"] == "GitHub authentication failed"
        # APIError str() format is "API Error [CODE]"; the code identifies the path
        assert "GITHUB_AUTH_FAILED" in result["detail"]

    @pytest.mark.asyncio
    async def test_rate_limit_returns_error_envelope(self):
        """GitHubRateLimitError → status=error with rate-limit message."""
        svc = _svc(side_effect=GitHubRateLimitError(retry_after=60))
        cmd = GithubIssueCommand(
            {"repo": "test-org/test-repo"}, {"github_service": svc}
        )

        result = await cmd.execute()

        assert result["status"] == "error"
        assert result["error"] == "GitHub rate limit exceeded"
        assert "GITHUB_RATE_LIMIT" in result["detail"]

    @pytest.mark.asyncio
    async def test_unexpected_exception_returns_error_envelope(self):
        """Generic exception → status=error with raw error string."""
        svc = _svc(side_effect=RuntimeError("network blip"))
        cmd = GithubIssueCommand(
            {"repo": "test-org/test-repo"}, {"github_service": svc}
        )

        result = await cmd.execute()

        assert result["status"] == "error"
        assert result["error"] == "network blip"


# -------------------------------------------------------------------
# Service-resolution mechanics
# -------------------------------------------------------------------


class TestServiceResolution:
    @pytest.mark.asyncio
    async def test_injected_service_wins_over_lazy_construct(self):
        """If context has github_service, lazy import path is never hit."""
        svc = _svc(return_value=_ok_issue())
        cmd = GithubIssueCommand(
            {"repo": "test-org/test-repo"}, {"github_service": svc}
        )

        with patch(
            "services.domain.github_domain_service.GitHubDomainService"
        ) as MockSvcClass:
            await cmd.execute()

        MockSvcClass.assert_not_called()
        svc.create_issue.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_lazy_construct_when_no_service_injected(self):
        """When context lacks github_service, command constructs one."""
        params = {"repo": "test-org/test-repo"}
        cmd = GithubIssueCommand(params, {"user_id": "u1"})

        # Patch the symbol at the import-target module so lazy import inside
        # _get_github_service picks up the mock.
        with patch(
            "services.domain.github_domain_service.GitHubDomainService"
        ) as MockSvcClass:
            mock_instance = MagicMock()
            mock_instance.create_issue = AsyncMock(return_value=_ok_issue())
            MockSvcClass.return_value = mock_instance

            result = await cmd.execute()

        MockSvcClass.assert_called_once_with()
        assert result["status"] == "success"

    @pytest.mark.asyncio
    async def test_lazy_construct_cached_across_calls(self):
        """Second execute() reuses the same lazy-constructed service."""
        params = {"repo": "test-org/test-repo"}
        cmd = GithubIssueCommand(params, {"user_id": "u1"})

        with patch(
            "services.domain.github_domain_service.GitHubDomainService"
        ) as MockSvcClass:
            mock_instance = MagicMock()
            mock_instance.create_issue = AsyncMock(return_value=_ok_issue())
            MockSvcClass.return_value = mock_instance

            await cmd.execute()
            await cmd.execute()

        # Constructor called only once across two execute() invocations.
        assert MockSvcClass.call_count == 1
        assert mock_instance.create_issue.await_count == 2


# -------------------------------------------------------------------
# #1112 — GitHubDomainService.create_issue signature regression
# -------------------------------------------------------------------


class TestDomainServiceSignature1112:
    """Verify the #1042-fallout fix in GitHubDomainService.create_issue.

    Before #1112: domain called router with 5 positional args, but router
    signature became ``(title, body, labels, assignees, *, owner, repo_name)``
    in #1042 — the 5th positional would raise TypeError. Tests had used
    ``MagicMock()`` without ``spec=`` so the mismatch was silent.

    After fix: domain splits owner/name and forwards via kwargs.
    """

    @pytest.mark.asyncio
    async def test_full_slug_split_and_forwarded_as_kwargs(self):
        """'owner/name' → owner='owner', repo_name='name' via kwargs."""
        from services.domain.github_domain_service import GitHubDomainService
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        # spec=GitHubIntegrationRouter enforces the real signature on the mock
        # — this is the regression-test discipline: if router signature drifts
        # again, this mock will reject the call and the test fails.
        mock_router = MagicMock(spec=GitHubIntegrationRouter)
        mock_router.create_issue = AsyncMock(
            return_value={"number": 1, "html_url": "https://x"}
        )

        svc = GitHubDomainService(github_agent=mock_router)
        result = await svc.create_issue(
            repo_name="test-org/test-repo",
            title="t",
            body="b",
            labels=["l"],
            assignees=["a"],
        )

        assert result["number"] == 1
        mock_router.create_issue.assert_awaited_once_with(
            title="t",
            body="b",
            labels=["l"],
            assignees=["a"],
            owner="test-org",
            repo_name="test-repo",
        )

    @pytest.mark.asyncio
    async def test_bare_name_passes_through_for_router_default_resolution(self):
        """Bare 'name' (no slash) → router's resolve-from-config path."""
        from services.domain.github_domain_service import GitHubDomainService
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        mock_router = MagicMock(spec=GitHubIntegrationRouter)
        mock_router.create_issue = AsyncMock(
            return_value={"number": 2, "html_url": "https://x"}
        )

        svc = GitHubDomainService(github_agent=mock_router)
        await svc.create_issue(
            repo_name="just-the-name",
            title="t",
            body="b",
            labels=None,
            assignees=None,
        )

        mock_router.create_issue.assert_awaited_once_with(
            title="t",
            body="b",
            labels=None,
            assignees=None,
            repo_name="just-the-name",
        )
        # Notably: owner is NOT passed — router will resolve from default config.
        kwargs = mock_router.create_issue.await_args.kwargs
        assert "owner" not in kwargs

    @pytest.mark.asyncio
    async def test_signature_compatible_with_existing_kwarg_callers(self):
        """cli/commands/issues.py and intent_service.py call with kwargs:
        repo_name=..., title=..., body=..., labels=..., assignees=...
        Verify those callers' shape still works through the domain service.
        """
        from services.domain.github_domain_service import GitHubDomainService
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        mock_router = MagicMock(spec=GitHubIntegrationRouter)
        mock_router.create_issue = AsyncMock(
            return_value={"number": 3, "html_url": "https://x"}
        )

        svc = GitHubDomainService(github_agent=mock_router)
        # Matches cli/commands/issues.py:776 call site exactly
        await svc.create_issue(
            repo_name="mediajunkie/piper-morgan-product",
            title="PM issue",
            body="some body",
            labels=["pm-tracking"],
        )

        mock_router.create_issue.assert_awaited_once()
        kwargs = mock_router.create_issue.await_args.kwargs
        assert kwargs["owner"] == "mediajunkie"
        assert kwargs["repo_name"] == "piper-morgan-product"

    @pytest.mark.asyncio
    async def test_auth_error_propagates(self):
        """GitHubAuthFailedError from router bubbles up unchanged."""
        from services.domain.github_domain_service import GitHubDomainService
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        mock_router = MagicMock(spec=GitHubIntegrationRouter)
        mock_router.create_issue = AsyncMock(
            side_effect=GitHubAuthFailedError({"reason": "nope"})
        )

        svc = GitHubDomainService(github_agent=mock_router)
        with pytest.raises(GitHubAuthFailedError):
            await svc.create_issue(
                repo_name="o/r", title="t", body="b", labels=[], assignees=[]
            )
