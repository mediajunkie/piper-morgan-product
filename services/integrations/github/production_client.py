"""
Production GitHub Client
Enhanced GitHub API client with comprehensive error handling, retry logic,
authentication management, and rate limiting for production use.

Implements PM-012 requirements for production GitHub API design.
"""

import asyncio
import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from github import (
    BadCredentialsException,
    Github,
    GithubException,
    RateLimitExceededException,
    UnknownObjectException,
)

from services.api.errors import GitHubAuthFailedError, GitHubRateLimitError
from services.integrations.github.config_service import (
    GitHubClientConfig as ConfigServiceClientConfig,
)
from services.integrations.github.config_service import (
    GitHubConfigService,
)

logger = logging.getLogger(__name__)


class AuthenticationMode(Enum):
    """GitHub authentication modes"""

    PERSONAL_TOKEN = "personal_token"
    GITHUB_APP = "github_app"
    OAUTH = "oauth"


@dataclass
class RetryConfig:
    """Configuration for retry logic"""

    max_attempts: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    exponential_base: float = 2.0
    rate_limit_retry: bool = True


@dataclass
class RateLimitInfo:
    """Rate limit information from GitHub API"""

    limit: int
    remaining: int
    reset_at: int
    used: int

    @property
    def seconds_until_reset(self) -> int:
        """Seconds until rate limit resets"""
        return max(0, self.reset_at - int(time.time()))

    @property
    def usage_percentage(self) -> float:
        """Percentage of rate limit used"""
        return (self.used / self.limit) * 100 if self.limit > 0 else 0


@dataclass
class GitHubClientConfig:
    """Production GitHub client configuration"""

    token: Optional[str] = None
    auth_mode: AuthenticationMode = AuthenticationMode.PERSONAL_TOKEN
    retry_config: RetryConfig = field(default_factory=RetryConfig)
    user_agent: str = "Piper-Morgan-PM/1.0"
    per_page: int = 30
    enable_rate_limit_handling: bool = True
    enable_metrics: bool = True
    timeout: int = 30


class ProductionGitHubClient:
    """
    Production-ready GitHub API client with comprehensive error handling.

    Features:
    - Multiple authentication modes (Personal Access Token, GitHub App, OAuth)
    - Exponential backoff retry logic with configurable parameters
    - Comprehensive rate limit handling and monitoring
    - Enhanced error reporting with recovery suggestions
    - Request/response logging and metrics
    - Connection pooling and timeout management
    - Graceful degradation when GitHub is unavailable
    """

    def __init__(
        self,
        config: Optional[ConfigServiceClientConfig] = None,
        config_service: Optional[GitHubConfigService] = None,
    ):
        # ADR-010: Use ConfigService for application layer configuration
        # #1436 B16: get_client_configuration requires a principal; the bare
        # constructor is the system-scoped default path ("system" marker per
        # the config service's documented convention) — per-user callers pass
        # `config` explicitly (#891 threading).
        self.config_service = config_service or GitHubConfigService()
        self.config = config or self.config_service.get_client_configuration("system")

        self._client: Optional[Github] = None
        self._authenticated_user = None
        self._rate_limit_info: Optional[RateLimitInfo] = None
        self._request_count = 0
        self._error_count = 0
        self._last_request_time = 0

        self._initialize_client()

    def _initialize_client(self):
        """Initialize GitHub client with authentication"""
        try:
            # ADR-010: Use ConfigService for token resolution
            token = self.config.token
            if not token:
                raise GitHubAuthFailedError(
                    details={
                        "reason": "No GitHub token provided",
                        "recovery": "Set GITHUB_TOKEN environment variable or configure authentication",
                        "environment": self.config_service.get_environment().value,
                    }
                )

            self._client = Github(
                token,
                user_agent=self.config.user_agent,
                per_page=self.config.per_page,
                timeout=self.config.timeout_seconds,
            )

            # Verify authentication
            self._authenticated_user = self._client.get_user()
            logger.info(f"GitHub client initialized for user: {self._authenticated_user.login}")

        except BadCredentialsException as e:
            raise GitHubAuthFailedError(
                details={
                    "reason": "Invalid GitHub token",
                    "recovery": "Check that GITHUB_TOKEN is valid and has required permissions",
                }
            ) from e
        except Exception as e:
            raise ConnectionError(f"Failed to initialize GitHub client: {e}") from e

    async def _execute_with_retry(self, operation, *args, **kwargs):
        """Execute GitHub operation with retry logic and rate limit handling"""
        last_exception = None

        for attempt in range(self.config.retry_config.max_attempts):
            try:
                # Update request metrics
                self._request_count += 1
                self._last_request_time = time.time()

                # Execute the operation
                result = operation(*args, **kwargs)

                # Update rate limit info if available
                if hasattr(self._client, "get_rate_limit"):
                    try:
                        rate_limit = self._client.get_rate_limit()
                        self._rate_limit_info = RateLimitInfo(
                            limit=rate_limit.core.limit,
                            remaining=rate_limit.core.remaining,
                            reset_at=int(rate_limit.core.reset.timestamp()),
                            used=rate_limit.core.limit - rate_limit.core.remaining,
                        )
                    except Exception:
                        pass  # Don't fail the main operation for rate limit info

                return result

            except RateLimitExceededException as e:
                self._error_count += 1
                logger.warning(f"GitHub rate limit exceeded (attempt {attempt + 1})")

                if not self.config.retry_config.rate_limit_retry:
                    raise GitHubRateLimitError(
                        retry_after=60, details={"reason": "Rate limit exceeded, retries disabled"}
                    ) from e

                if attempt < self.config.retry_config.max_attempts - 1:
                    # Calculate retry delay (respect GitHub's Retry-After header)
                    retry_after = int(e.headers.get("Retry-After", 60))
                    delay = min(retry_after, self.config.retry_config.max_delay_seconds)

                    logger.info(f"Rate limited, waiting {delay} seconds before retry")
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise GitHubRateLimitError(
                        retry_after=retry_after, details={"attempts": attempt + 1}
                    ) from e

            except (BadCredentialsException, UnknownObjectException) as e:
                # Don't retry auth failures or not-found errors
                self._error_count += 1
                if isinstance(e, BadCredentialsException):
                    raise GitHubAuthFailedError() from e
                else:
                    raise ValueError(f"GitHub resource not found: {str(e)}") from e

            except GithubException as e:
                self._error_count += 1
                last_exception = e

                if attempt < self.config.retry_config.max_attempts - 1:
                    # Exponential backoff for other GitHub API errors
                    delay = min(
                        self.config.retry_config.base_delay_seconds
                        * (self.config.retry_config.exponential_base**attempt),
                        self.config.retry_config.max_delay_seconds,
                    )

                    logger.warning(
                        f"GitHub API error (attempt {attempt + 1}): {e}. "
                        f"Retrying in {delay} seconds"
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise ConnectionError(
                        f"GitHub API error after {attempt + 1} attempts: {e}"
                    ) from e

            except Exception as e:
                self._error_count += 1
                last_exception = e

                if attempt < self.config.retry_config.max_attempts - 1:
                    delay = min(
                        self.config.retry_config.base_delay_seconds
                        * (self.config.retry_config.exponential_base**attempt),
                        self.config.retry_config.max_delay_seconds,
                    )

                    logger.warning(
                        f"Unexpected error (attempt {attempt + 1}): {e}. "
                        f"Retrying in {delay} seconds"
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise ConnectionError(
                        f"Operation failed after {attempt + 1} attempts: {e}"
                    ) from e

        # This should never be reached, but just in case
        raise ConnectionError(f"Operation failed: {last_exception}")

    async def create_issue(
        self,
        repo_name: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
        milestone: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a GitHub issue with enhanced error handling and retry logic.

        Args:
            repo_name: Repository name in format "owner/repo"
            title: Issue title
            body: Issue body/description
            labels: List of label names to apply
            assignees: List of usernames to assign
            milestone: Milestone title or number

        Returns:
            Dict containing issue details

        Raises:
            GitHubAuthFailedError: Authentication failed
            GitHubRateLimitError: Rate limit exceeded
            ValueError: Invalid input or resource not found
            ConnectionError: API communication error
        """

        def _create_issue():
            # ADR-010: Repository access validation using ConfigService
            if not self.config_service.is_repository_allowed(repo_name):
                raise ValueError(
                    f"Repository '{repo_name}' not in allowed list. "
                    f"Check GITHUB_ALLOWED_REPOS configuration."
                )

            repo = self._client.get_repo(repo_name)

            # Validate labels exist
            validated_labels = []
            if labels:
                repo_labels = {label.name for label in repo.get_labels()}
                for label in labels:
                    if label in repo_labels:
                        validated_labels.append(label)
                    else:
                        logger.warning(f"Label '{label}' not found in {repo_name}, skipping")

            # Create the issue
            issue = repo.create_issue(title=title, body=body or "", labels=validated_labels)

            # Add assignees if specified
            if assignees:
                try:
                    issue.add_to_assignees(*assignees)
                except Exception as e:
                    logger.warning(f"Failed to add assignees {assignees}: {e}")

            # Set milestone if specified
            if milestone:
                try:
                    milestones = {m.title: m for m in repo.get_milestones()}
                    if milestone in milestones:
                        issue.edit(milestone=milestones[milestone])
                    else:
                        logger.warning(f"Milestone '{milestone}' not found in {repo_name}")
                except Exception as e:
                    logger.warning(f"Failed to set milestone {milestone}: {e}")

            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "body": issue.body,
                "url": issue.html_url,
                "state": issue.state,
                "labels": [label.name for label in issue.labels],
                "assignees": [assignee.login for assignee in issue.assignees],
                "created_at": issue.created_at.isoformat(),
                "repository": repo_name,
            }

        logger.info(f"Creating GitHub issue in {repo_name}: '{title}'")
        return await self._execute_with_retry(_create_issue)

    async def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """Get issue details with retry logic"""

        def _get_issue():
            repo = self._client.get_repo(repo_name)
            issue = repo.get_issue(issue_number)

            return {
                "id": issue.id,
                "number": issue.number,
                "title": issue.title,
                "body": issue.body or "",
                "state": issue.state,
                "labels": [label.name for label in issue.labels],
                "assignees": [assignee.login for assignee in issue.assignees],
                "created_at": issue.created_at.isoformat(),
                "updated_at": issue.updated_at.isoformat(),
                "html_url": issue.html_url,
                "user": {"login": issue.user.login, "name": issue.user.name or issue.user.login},
                "repository": repo_name,
                "comments_count": issue.comments,
                "is_pull_request": issue.pull_request is not None,
            }

        logger.info(f"Fetching GitHub issue {repo_name}#{issue_number}")
        return await self._execute_with_retry(_get_issue)

    async def list_repositories(self, organization: Optional[str] = None) -> List[Dict[str, Any]]:
        """List accessible repositories with pagination handling"""

        def _list_repos():
            if organization:
                org = self._client.get_organization(organization)
                repos = org.get_repos()
            else:
                repos = self._authenticated_user.get_repos()

            result = []
            for repo in repos:
                result.append(
                    {
                        "id": repo.id,
                        "name": repo.name,
                        "full_name": repo.full_name,
                        "private": repo.private,
                        "html_url": repo.html_url,
                        "description": repo.description,
                        "language": repo.language,
                        "default_branch": repo.default_branch,
                        "created_at": repo.created_at.isoformat(),
                        "updated_at": repo.updated_at.isoformat(),
                        "permissions": (
                            {
                                "admin": repo.permissions.admin,
                                "push": repo.permissions.push,
                                "pull": repo.permissions.pull,
                            }
                            if hasattr(repo, "permissions")
                            else None
                        ),
                    }
                )
            return result

        logger.info(f"Listing repositories for {organization or 'authenticated user'}")
        return await self._execute_with_retry(_list_repos)

    def get_rate_limit_info(self) -> Optional[RateLimitInfo]:
        """Get current rate limit information"""
        return self._rate_limit_info

    def get_client_metrics(self) -> Dict[str, Any]:
        """Get client performance metrics"""
        return {
            "request_count": self._request_count,
            "error_count": self._error_count,
            "error_rate": self._error_count / max(self._request_count, 1),
            "last_request_time": self._last_request_time,
            "rate_limit": self._rate_limit_info.__dict__ if self._rate_limit_info else None,
            "authenticated_user": (
                self._authenticated_user.login if self._authenticated_user else None
            ),
        }

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on GitHub API connectivity"""
        try:
            start_time = time.time()

            # Simple API call to test connectivity
            user = await self._execute_with_retry(lambda: self._client.get_user())

            response_time = time.time() - start_time

            return {
                "status": "healthy",
                "response_time_ms": round(response_time * 1000, 2),
                "authenticated_user": user.login,
                "rate_limit": self._rate_limit_info.__dict__ if self._rate_limit_info else None,
            }

        except Exception as e:
            return {"status": "unhealthy", "error": str(e), "error_type": type(e).__name__}
