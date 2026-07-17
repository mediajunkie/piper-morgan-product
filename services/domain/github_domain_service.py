"""
GitHub Domain Service
Mediates all GitHub operations for the domain layer following DDD principles

Created: 2025-09-12 by Code Agent Step 5 - Domain Service Mediation Completion
Addresses architectural violation: Direct GitHub integration access from CLI/features/main layers
"""

from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.api.errors import GitHubAuthFailedError, GitHubRateLimitError
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

# Re-export exceptions for clean domain boundary
__all__ = ["GitHubDomainService", "GitHubAuthFailedError", "GitHubRateLimitError"]

logger = structlog.get_logger()


class GitHubDomainService:
    """
    Domain service for GitHub operations mediation

    Encapsulates GitHub integration access following DDD principles:
    - Mediates between application layer and GitHub integration layer
    - Provides clean domain interface for GitHub operations
    - Handles GitHub-specific error translation to domain exceptions
    - Manages GitHub agent lifecycle and configuration
    """

    def __init__(self, github_agent: Optional[GitHubIntegrationRouter] = None):
        """Initialize with optional GitHub agent injection"""
        try:
            self._github_agent = github_agent or GitHubIntegrationRouter()
            logger.info(
                "GitHub domain service initialized", agent_type=type(self._github_agent).__name__
            )
        except Exception as e:
            logger.error("Failed to initialize GitHub domain service", error=str(e))
            raise

    # Issue Operations

    async def get_issue_by_url(self, url: str) -> Dict[str, Any]:
        """Get GitHub issue by URL for domain consumption"""
        try:
            return await self._github_agent.get_issue_by_url(url)
        except GitHubAuthFailedError:
            logger.error("GitHub authentication failed", url=url)
            raise
        except GitHubRateLimitError:
            logger.warning("GitHub rate limit exceeded", url=url)
            raise
        except Exception as e:
            logger.error("GitHub issue retrieval failed", url=url, error=str(e))
            raise

    async def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """Get GitHub issue by repo and number for domain consumption"""
        try:
            # #1436 B13: router signature is (issue_number, *, owner, repo_name)
            # — the old positional call put repo_name into issue_number.
            return await self._github_agent.get_issue(issue_number, repo_name=repo_name)
        except GitHubAuthFailedError:
            logger.error("GitHub authentication failed", repo=repo_name, issue=issue_number)
            raise
        except GitHubRateLimitError:
            logger.warning("GitHub rate limit exceeded", repo=repo_name, issue=issue_number)
            raise
        except Exception as e:
            logger.error(
                "GitHub issue retrieval failed", repo=repo_name, issue=issue_number, error=str(e)
            )
            raise

    async def get_recent_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent GitHub issues for domain consumption"""
        try:
            return await self._github_agent.get_recent_issues(limit)
        except GitHubAuthFailedError:
            logger.error("GitHub authentication failed for recent issues")
            raise
        except GitHubRateLimitError:
            logger.warning("GitHub rate limit exceeded for recent issues")
            raise
        except Exception as e:
            logger.error("GitHub recent issues retrieval failed", error=str(e))
            raise

    async def get_open_issues(self, repo_name: str, days_back: int = 7) -> List[Dict[str, Any]]:
        """Get open GitHub issues for domain consumption"""
        try:
            return await self._github_agent.get_open_issues(repo_name, days_back)
        except GitHubAuthFailedError:
            logger.error("GitHub authentication failed for open issues", repo=repo_name)
            raise
        except GitHubRateLimitError:
            logger.warning("GitHub rate limit exceeded for open issues", repo=repo_name)
            raise
        except Exception as e:
            logger.error("GitHub open issues retrieval failed", repo=repo_name, error=str(e))
            raise

    # Repository Operations

    def list_repositories(self) -> List[Dict[str, Any]]:
        """List GitHub repositories for domain consumption"""
        try:
            return self._github_agent.list_repositories()
        except GitHubAuthFailedError:
            logger.error("GitHub authentication failed for repository listing")
            raise
        except GitHubRateLimitError:
            logger.warning("GitHub rate limit exceeded for repository listing")
            raise
        except Exception as e:
            logger.error("GitHub repository listing failed", error=str(e))
            raise

    # Issue Creation Operations

    async def create_issue(
        self,
        repo_name: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create GitHub issue for domain consumption.

        Issue #1112: router signature became kw-only on owner/repo_name in
        #1042; we split the slug and forward via kwargs so the call matches
        the router contract. `repo_name` accepts either:

        - "owner/name" full slug — split and passed explicitly to router
        - bare "name" — router resolves owner via its default-repo config
        """
        try:
            if "/" in repo_name:
                owner, repo = repo_name.split("/", 1)
                return await self._github_agent.create_issue(
                    title=title,
                    body=body,
                    labels=labels,
                    assignees=assignees,
                    owner=owner,
                    repo_name=repo,
                )
            return await self._github_agent.create_issue(
                title=title,
                body=body,
                labels=labels,
                assignees=assignees,
                repo_name=repo_name,
            )
        except GitHubAuthFailedError:
            logger.error("GitHub authentication failed for issue creation", repo=repo_name)
            raise
        except GitHubRateLimitError:
            logger.warning("GitHub rate limit exceeded for issue creation", repo=repo_name)
            raise
        except Exception as e:
            logger.error("GitHub issue creation failed", repo=repo_name, title=title, error=str(e))
            raise

    async def update_issue(
        self,
        repo_name: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Update existing GitHub issue for domain consumption"""
        try:
            # #1436 B13: router signature is (issue_number, title, body, state,
            # labels, assignees, *, owner, repo_name) — the old call shifted
            # every argument by one.
            return await self._github_agent.update_issue(
                issue_number, title, body, state, labels, assignees, repo_name=repo_name
            )
        except GitHubAuthFailedError:
            logger.error(
                "GitHub authentication failed for issue update", repo=repo_name, issue=issue_number
            )
            raise
        except GitHubRateLimitError:
            logger.warning(
                "GitHub rate limit exceeded for issue update", repo=repo_name, issue=issue_number
            )
            raise
        except Exception as e:
            logger.error(
                "GitHub issue update failed", repo=repo_name, issue=issue_number, error=str(e)
            )
            raise

    # Utility Operations

    def parse_github_url(self, url: str) -> Optional[Tuple[str, str, int]]:
        """Parse GitHub URL for domain consumption"""
        try:
            return self._github_agent.parse_github_url(url)
        except Exception as e:
            logger.error("GitHub URL parsing failed", url=url, error=str(e))
            return None

    # Health and Status Operations

    def get_connection_status(self) -> Dict[str, Any]:
        """Get GitHub connection status for domain monitoring"""
        try:
            # #1436 B13: the router has no `.user`/`.client` (PyGithub-era attrs
            # — every call here raised into the except and reported
            # disconnected). Report what the router actually knows: whether it
            # initialized. Deeper identity/rate-limit reporting needs a router
            # status surface (none exists yet — honest None, not a guess).
            initialized = bool(getattr(self._github_agent, "_initialized", False))
            return {
                "connected": initialized,
                "user": None,
                "rate_limit_remaining": None,
            }
        except Exception as e:
            logger.error("GitHub connection status check failed", error=str(e))
            return {"connected": False, "error": str(e)}
