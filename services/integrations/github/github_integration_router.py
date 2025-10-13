"""
GitHub Integration Router - Deprecation Infrastructure
PM-033b-deprecation: Safe 4-week deprecation strategy implementation

This router provides feature flag-based switching between:
- GitHubSpatialIntelligence (8-dimensional spatial analysis - NEW DEFAULT)
- GitHubAgent (legacy direct API integration - BEING DEPRECATED)

During the 4-week deprecation timeline:
Week 1: Both integrations available, spatial default
Week 2: Deprecation warnings when legacy used
Week 3: Legacy disabled by default, emergency rollback available
Week 4: Legacy code removal

Architecture Decision: ADR-013 MCP+Spatial Integration Pattern
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from services.infrastructure.config.feature_flags import FeatureFlags
from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence

from .config_service import GitHubConfigService

logger = logging.getLogger(__name__)


class GitHubIntegrationRouter:
    """
    Routes GitHub operations between spatial and legacy integrations based on feature flags.

    Provides safe deprecation infrastructure during the 4-week migration timeline
    with comprehensive fallback support and deprecation warnings.

    Follows service injection pattern (ADR-010) for configuration management.
    """

    def __init__(self, config_service: Optional[GitHubConfigService] = None):
        """
        Initialize GitHub integration router with feature flag detection and config service.

        Args:
            config_service: Optional GitHubConfigService for dependency injection.
                          If not provided, creates a default instance.
        """
        # Store config service (service injection pattern)
        self.config_service = config_service or GitHubConfigService()

        self.spatial_github = None
        self.legacy_github = None

        # Feature flag state
        self.use_spatial = FeatureFlags.should_use_spatial_github()
        self.allow_legacy = FeatureFlags.is_legacy_github_allowed()
        self.warn_deprecation = FeatureFlags.should_warn_github_deprecation()

        # Initialize preferred integration
        self._initialize_integrations()

        logger.info(
            f"GitHubIntegrationRouter initialized - "
            f"Spatial: {self.use_spatial}, Legacy: {self.allow_legacy}, "
            f"Warnings: {self.warn_deprecation}"
        )

    def _initialize_integrations(self):
        """Initialize the appropriate GitHub integrations based on feature flags"""

        # Always initialize spatial integration (it's the future)
        if self.use_spatial:
            try:
                self.spatial_github = GitHubSpatialIntelligence()
                logger.info("GitHubSpatialIntelligence initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize GitHubSpatialIntelligence: {e}")
                if not self.allow_legacy:
                    raise RuntimeError("Spatial GitHub failed and legacy not allowed") from e

        # Initialize legacy integration if allowed
        if self.allow_legacy:
            try:
                # Import legacy GitHub agent dynamically to avoid dependency when not needed
                from services.integrations.github.github_agent import GitHubAgent

                self.legacy_github = GitHubAgent()
                logger.info("Legacy GitHubAgent initialized for fallback support")
            except Exception as e:
                logger.warning(f"Failed to initialize legacy GitHubAgent: {e}")
                if not self.use_spatial or self.spatial_github is None:
                    raise RuntimeError("Legacy GitHub failed and spatial not available") from e

    async def initialize(self):
        """Initialize the GitHub integrations asynchronously"""
        integration, is_legacy = self._get_preferred_integration("initialize")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("initialize", is_legacy)
            if hasattr(integration, "initialize"):
                await integration.initialize()
        else:
            raise RuntimeError("No GitHub integration available for initialize")

    def _warn_deprecation_if_needed(self, operation: str, used_legacy: bool):
        """Issue deprecation warnings when legacy integration is used"""
        if used_legacy and self.warn_deprecation:
            logger.warning(
                f"DEPRECATION WARNING: Legacy GitHub integration used for {operation}. "
                f"This will be removed in the upcoming release. "
                f"Please ensure spatial GitHub integration is working properly."
            )

    def _get_preferred_integration(self, operation: str) -> tuple[Any, bool]:
        """
        Get the preferred GitHub integration based on feature flags and availability.

        Returns:
            tuple: (integration_instance, is_legacy_used)
        """
        # Try spatial first if enabled
        if self.use_spatial and self.spatial_github:
            return self.spatial_github, False

        # Fall back to legacy if allowed and available
        if self.allow_legacy and self.legacy_github:
            logger.info(f"Falling back to legacy GitHub for {operation}")
            return self.legacy_github, True

        # No integration available
        raise RuntimeError(
            f"No GitHub integration available for {operation}. "
            f"Spatial: {self.spatial_github is not None}, "
            f"Legacy: {self.legacy_github is not None}"
        )

    async def get_issue(self, repo_name: str, issue_number: int) -> Dict[str, Any]:
        """
        Get GitHub issue.
        """
        integration, is_legacy = self._get_preferred_integration("get_issue")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_issue", is_legacy)
            return await integration.get_issue(repo_name, issue_number)
        else:
            raise RuntimeError("No GitHub integration available for get_issue")

    async def list_issues(self, repository: str, **kwargs) -> List[Dict[str, Any]]:
        """
        List GitHub issues.
        """
        integration, is_legacy = self._get_preferred_integration("list_issues")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("list_issues", is_legacy)
            return await integration.list_issues(repository, **kwargs)
        else:
            raise RuntimeError("No GitHub integration available for list_issues")

    async def create_issue(
        self, repo_name: str, title: str, body: str, labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create GitHub issue.
        """
        integration, is_legacy = self._get_preferred_integration("create_issue")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("create_issue", is_legacy)
            return await integration.create_issue(repo_name, title, body, labels)
        else:
            raise RuntimeError("No GitHub integration available for create_issue")

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
        """
        Update existing GitHub issue.

        Args:
            repo_name: Repository name (owner/repo format)
            issue_number: Issue number to update
            title: Optional new title
            body: Optional new body
            state: Optional new state ('open' or 'closed')
            labels: Optional new labels
            assignees: Optional new assignees

        Returns:
            Updated issue data from GitHub API
        """
        integration, is_legacy = self._get_preferred_integration("update_issue")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("update_issue", is_legacy)
            return await integration.update_issue(
                repo_name, issue_number, title, body, state, labels, assignees
            )
        else:
            raise RuntimeError("No GitHub integration available for update_issue")

    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get current integration status for monitoring and debugging.
        """
        integration, is_legacy = self._get_preferred_integration("get_integration_status")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_integration_status", is_legacy)
            # Get status from integration if it supports it, otherwise return router status
            if hasattr(integration, "get_integration_status"):
                return integration.get_integration_status()
            else:
                # Fallback to router-level status
                return {
                    "router_initialized": True,
                    "feature_flags": {
                        "use_spatial": self.use_spatial,
                        "allow_legacy": self.allow_legacy,
                        "warn_deprecation": self.warn_deprecation,
                    },
                    "integrations": {
                        "spatial_available": self.spatial_github is not None,
                        "legacy_available": self.legacy_github is not None,
                    },
                    "preferred_integration": (
                        "spatial" if self.use_spatial and self.spatial_github else "legacy"
                    ),
                    "deprecation_timeline": {
                        "week": self._get_deprecation_week(),
                        "legacy_removal_date": "2025-09-09",
                    },
                }
        else:
            raise RuntimeError("No GitHub integration available for get_integration_status")

    def _get_deprecation_week(self) -> int:
        """
        Determine current week in the 4-week deprecation timeline.

        Returns:
            Week number (1-4) in deprecation timeline
        """
        # Week 1: August 12-19, 2025
        deprecation_start = datetime(2025, 8, 12)
        now = datetime.now()
        days_since_start = (now - deprecation_start).days

        if days_since_start < 0:
            return 0  # Before deprecation starts
        elif days_since_start < 7:
            return 1  # Week 1: Parallel operation
        elif days_since_start < 14:
            return 2  # Week 2: Deprecation warnings
        elif days_since_start < 21:
            return 3  # Week 3: Legacy disabled by default
        elif days_since_start < 28:
            return 4  # Week 4: Legacy removal
        else:
            return 5  # Post-deprecation

    async def get_issue_by_url(self, url: str) -> Dict[str, Any]:
        """
        Fetch GitHub issue by URL, raising exceptions on failure.

        Used by: domain/github_domain_service.py, integrations/github/issue_analyzer.py
        """
        integration, is_legacy = self._get_preferred_integration("get_issue_by_url")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_issue_by_url", is_legacy)
            return await integration.get_issue_by_url(url)
        else:
            raise RuntimeError("No GitHub integration available for get_issue_by_url")

    async def get_open_issues(
        self, project: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get open issues from GitHub repository.

        Used by: domain/github_domain_service.py, domain/pm_number_manager.py
        """
        integration, is_legacy = self._get_preferred_integration("get_open_issues")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_open_issues", is_legacy)
            return await integration.get_open_issues(project, limit)
        else:
            raise RuntimeError("No GitHub integration available for get_open_issues")

    async def get_recent_issues(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent issues (both open and closed) from GitHub repository.

        Used by: domain/github_domain_service.py
        """
        integration, is_legacy = self._get_preferred_integration("get_recent_issues")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_recent_issues", is_legacy)
            return await integration.get_recent_issues(limit)
        else:
            raise RuntimeError("No GitHub integration available for get_recent_issues")

    async def get_recent_activity(self, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get recent GitHub activity for standup (commits, PRs, issues).

        Used by: domain/standup_orchestration_service.py
        """
        integration, is_legacy = self._get_preferred_integration("get_recent_activity")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_recent_activity", is_legacy)
            return await integration.get_recent_activity(days)
        else:
            raise RuntimeError("No GitHub integration available for get_recent_activity")

    def list_repositories(self) -> List[Dict[str, Any]]:
        """
        List accessible repositories.

        Used by: domain/github_domain_service.py
        """
        integration, is_legacy = self._get_preferred_integration("list_repositories")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("list_repositories", is_legacy)
            return integration.list_repositories()
        else:
            raise RuntimeError("No GitHub integration available for list_repositories")

    async def create_issue_from_work_item(
        self, repo_name: str, work_item: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create GitHub issue from work item data.
        """
        integration, is_legacy = self._get_preferred_integration("create_issue_from_work_item")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("create_issue_from_work_item", is_legacy)
            return await integration.create_issue_from_work_item(repo_name, work_item)
        else:
            raise RuntimeError("No GitHub integration available for create_issue_from_work_item")

    async def create_pm_issue(
        self,
        repo_name: str,
        pm_number: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create PM-specific GitHub issue.
        """
        integration, is_legacy = self._get_preferred_integration("create_pm_issue")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("create_pm_issue", is_legacy)
            return await integration.create_pm_issue(
                repo_name, pm_number, title, body, labels, assignees
            )
        else:
            raise RuntimeError("No GitHub integration available for create_pm_issue")

    async def get_closed_issues(
        self, project: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get closed issues from GitHub repository.
        """
        integration, is_legacy = self._get_preferred_integration("get_closed_issues")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_closed_issues", is_legacy)
            return await integration.get_closed_issues(project, limit)
        else:
            raise RuntimeError("No GitHub integration available for get_closed_issues")

    async def get_issues_by_priority(self) -> List[Dict[str, Any]]:
        """
        Get GitHub issues organized by priority.
        """
        integration, is_legacy = self._get_preferred_integration("get_issues_by_priority")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_issues_by_priority", is_legacy)
            return await integration.get_issues_by_priority()
        else:
            raise RuntimeError("No GitHub integration available for get_issues_by_priority")

    async def get_development_context(self) -> Dict[str, Any]:
        """
        Get development context from GitHub.
        """
        integration, is_legacy = self._get_preferred_integration("get_development_context")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_development_context", is_legacy)
            return await integration.get_development_context()
        else:
            raise RuntimeError("No GitHub integration available for get_development_context")

    def parse_github_url(self, url: str) -> Optional[Tuple[str, str, int]]:
        """
        Parse GitHub issue URL to extract owner, repo, and issue number.
        """
        integration, is_legacy = self._get_preferred_integration("parse_github_url")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("parse_github_url", is_legacy)
            return integration.parse_github_url(url)
        else:
            raise RuntimeError("No GitHub integration available for parse_github_url")

    def test_connection(self) -> Dict[str, Any]:
        """
        Test GitHub connection and return status.
        """
        integration, is_legacy = self._get_preferred_integration("test_connection")
        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("test_connection", is_legacy)
            return integration.test_connection()
        else:
            raise RuntimeError("No GitHub integration available for test_connection")


# Convenience factory function
def create_github_integration() -> GitHubIntegrationRouter:
    """
    Create and initialize GitHub integration router.

    This is the primary entry point for all GitHub operations during the deprecation period.

    Returns:
        Configured GitHubIntegrationRouter instance
    """
    return GitHubIntegrationRouter()
