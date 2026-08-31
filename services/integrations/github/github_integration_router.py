"""
GitHub Integration Router - MCP + Spatial Integration
PM-033b-deprecation: Week 4 Complete - Legacy Removed (CORE-INT #109)
CORE-MCP-MIGRATION #198: MCP Adapter Integration (October 17, 2025)

This router provides GitHub integration through:
- GitHubMCPSpatialAdapter (MCP protocol + spatial intelligence) - DEFAULT
- GitHubSpatialIntelligence (direct API + spatial intelligence) - FALLBACK

MCP Migration (CORE-MCP-MIGRATION #198):
- MCP adapter provides tool-based integration following Calendar pattern
- Feature flag USE_MCP_GITHUB controls MCP adapter usage (default: true)
- Graceful fallback to GitHubSpatialIntelligence if MCP unavailable

Deprecation timeline completed:
Week 1: ✅ Both integrations available, spatial default
Week 2: ✅ Deprecation warnings when legacy used
Week 3: ✅ Legacy disabled by default, emergency rollback available
Week 4: ✅ Legacy code removed (October 15, 2025)

Architecture Decision: ADR-013 MCP+Spatial Integration Pattern
"""

import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from services.infrastructure.config.feature_flags import FeatureFlags
from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence

from .config_service import GitHubConfigService

logger = logging.getLogger(__name__)


class GitHubIntegrationRouter:
    """
    Routes GitHub operations to MCP adapter or spatial intelligence.

    CORE-MCP-MIGRATION #198: Now supports GitHubMCPSpatialAdapter (tool-based MCP).
    Week 4 Complete (CORE-INT #109): Legacy code removed, spatial-only.

    Integration priority:
    1. GitHubMCPSpatialAdapter (if USE_MCP_GITHUB=true, default)
    2. GitHubSpatialIntelligence (fallback if MCP unavailable)

    ADAPTER PATTERN (ADR-013 Phase 2):
    - Router provides stable interface for consumers (get_recent_issues, get_issue, etc.)
    - Router delegates to MCP adapter using adapter methods
    - MCP adapter has different method names (list_github_issues_direct, get_github_issue_direct)
    - Adapter methods translate interface during migration period
    - Spatial intelligence used as fallback with direct method calls

    Follows service injection pattern (ADR-010) for configuration management.
    """

    def __init__(self, config_service: Optional[GitHubConfigService] = None):
        """
        Initialize GitHub integration router with MCP adapter support and config service.

        Args:
            config_service: Optional GitHubConfigService for dependency injection.
                          If not provided, creates a default instance.
        """
        # Store config service (service injection pattern)
        self.config_service = config_service or GitHubConfigService()

        # MCP adapter (tool-based integration, CORE-MCP-MIGRATION #198)
        self.mcp_adapter = None

        # Spatial intelligence (fallback)
        self.spatial_github = None

        # Initialization tracking (for lazy initialization)
        self._initialized = False
        self._initialization_lock = None  # Will be set in async context

        # Issue #1042: stash user_id from initialize() so general-query
        # methods (get_open_issues, get_closed_issues, etc.) can resolve
        # the user's default_repo without callers passing it through.
        self._user_id: Optional[str] = None

        # Feature flags
        self.use_mcp = self._get_boolean_flag("USE_MCP_GITHUB", True)
        self.allow_legacy = FeatureFlags.is_legacy_github_allowed()
        self.use_spatial = FeatureFlags.should_use_spatial_github()

        # Initialize integrations (MCP preferred, spatial fallback)
        self._initialize_integrations()

        logger.info(
            f"GitHubIntegrationRouter initialized - MCP: {self.mcp_adapter is not None}, Spatial: {self.spatial_github is not None}"
        )

    def _initialize_integrations(self):
        """
        Initialize GitHub integrations with MCP adapter priority.

        CORE-MCP-MIGRATION #198: Try MCP adapter first, fall back to spatial.
        """
        # Try MCP adapter first (if enabled)
        if self.use_mcp:
            try:
                from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

                self.mcp_adapter = GitHubMCPSpatialAdapter()
                logger.info("GitHubMCPSpatialAdapter initialized (token config pending)")
            except Exception as e:
                logger.warning(
                    f"Failed to initialize GitHubMCPSpatialAdapter: {e}, falling back to GitHubSpatialIntelligence"
                )
                self.mcp_adapter = None

        # Initialize spatial as fallback or primary (if MCP disabled)
        try:
            self.spatial_github = GitHubSpatialIntelligence()
            logger.info("GitHubSpatialIntelligence initialized successfully")
        except Exception as e:
            if not self.mcp_adapter:
                logger.error(f"Failed to initialize GitHubSpatialIntelligence: {e}")
                raise RuntimeError("No GitHub integration available") from e
            logger.warning(f"GitHubSpatialIntelligence failed, using MCP adapter only: {e}")

    async def initialize(self, user_id: Optional[str] = None):
        """
        Initialize the GitHub integration asynchronously.

        Idempotent - safe to call multiple times (uses initialization lock).

        Args:
            user_id: Optional user ID for scoped credential lookup (Issue #891).
                     If None, falls back to environment variable tokens only.
        """
        # Skip if already initialized
        if self._initialized:
            return

        # Create lock if it doesn't exist (first async call)
        if self._initialization_lock is None:
            import asyncio

            self._initialization_lock = asyncio.Lock()

        # Use lock to prevent concurrent initialization
        async with self._initialization_lock:
            # Double-check after acquiring lock
            if self._initialized:
                return

            # Issue #1042: stash user_id for downstream repo resolution
            self._user_id = user_id

            # Configure MCP adapter with GitHub token (async operation)
            if self.mcp_adapter:
                try:
                    token = self.config_service.get_authentication_token(user_id or "system")
                except (ValueError, Exception) as e:
                    logger.warning(f"GitHub token lookup failed: {e}")
                    token = None
                if token:
                    await self.mcp_adapter.configure_github_api(token)
                    logger.info("GitHubMCPSpatialAdapter configured with authentication token")
                else:
                    logger.warning("No GitHub authentication token available for MCP adapter")

            # Initialize spatial intelligence if available
            if self.spatial_github and hasattr(self.spatial_github, "initialize"):
                await self.spatial_github.initialize()

            # Mark as initialized
            self._initialized = True
            logger.info("GitHubIntegrationRouter initialization complete")

    async def close(self):
        """Release the resources ``initialize()`` opened (#1279).

        The MCP adapter's ``configure_github_api()`` opens an aiohttp
        ``ClientSession``; callers that construct a fresh router per request
        (places route, Radar's WorkItem/Place providers) leaked one session per
        call because nothing ever closed it ("Unclosed client session" in the
        logs). Delegates to the adapter's own idempotent ``disconnect()`` —
        safe to call when never initialized, already closed, or keyless (no
        session was opened). Never raises: cleanup must not mask the request's
        real outcome. The spatial fallback holds no session (verified — no
        aiohttp/httpx/requests state), so there is nothing to close there.
        """
        if self.mcp_adapter:
            try:
                await self.mcp_adapter.disconnect()
            except Exception as e:
                logger.warning(f"GitHubIntegrationRouter close failed (non-fatal): {e}")
        self._initialized = False

    def _get_integration(self, operation: str) -> Any:
        """
        Get the GitHub integration (MCP adapter preferred, spatial fallback).

        CORE-MCP-MIGRATION #198: Prefers MCP adapter when available.

        Args:
            operation: Operation name (for error messages)

        Returns:
            GitHubMCPSpatialAdapter or GitHubSpatialIntelligence instance

        Raises:
            RuntimeError: If no integration available
        """
        # Prefer MCP adapter if available
        if self.mcp_adapter:
            return self.mcp_adapter

        # Fall back to spatial intelligence
        if self.spatial_github:
            return self.spatial_github

        raise RuntimeError(f"No GitHub integration available for {operation}")

    async def get_issue(
        self,
        issue_number: int,
        *,
        owner: Optional[str] = None,
        repo_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get GitHub issue by number, with optional explicit owner/repo.

        ADAPTER METHOD (ADR-013 Phase 2): Translates interface for MCP adapter.
        Uses lazy initialization to ensure GitHub token is loaded.

        Issue #1042: ``owner`` and ``repo_name`` are now keyword-only optional
        args. If not provided, the router resolves via ``repo_resolver``.
        Returns ``None`` if no repo resolves (graceful empty-state).
        """
        # Lazy initialization (ensures token loaded on first use)
        if not self._initialized:
            await self.initialize()

        if owner is None or repo_name is None:
            resolved = await self._resolve_default_repo()
            if resolved is None:
                return None
            owner, repo_name = resolved

        # MCP adapter uses different method name and parameters
        if self.mcp_adapter:
            return await self.mcp_adapter.get_github_issue_direct(
                issue_number=str(issue_number),  # MCP adapter expects string
                repo=repo_name,
                owner=owner,
            )
        # Spatial fallback
        return await self.spatial_github.get_issue(repo_name, issue_number)

    async def list_issues(self, repository: str, **kwargs) -> List[Dict[str, Any]]:
        """
        List GitHub issues.

        Note: ``repository`` is the full ``owner/name`` slug here; the
        underlying integration handles parsing.
        """
        return await self._get_integration("list_issues").list_issues(repository, **kwargs)

    async def is_available(self) -> bool:
        """#1220/#1382: is GitHub usable for THIS user — via the per-user OAuth
        binding (the tester path on hosted, status BOUND) OR the legacy PAT
        config (local dev / pre-OAuth users).

        The chat handlers' capability gates previously used the PAT-only
        ``config_service.is_configured``, which made connected-via-OAuth users
        read as "not connected" and degrade before any connector call could
        run — found live during the v0.8.10.1 first-real-write attempt
        (2026-07-09). This check is the single gate the chat surfaces use.
        """
        if self._user_id:
            try:
                from services.connectors.binding_repository import (
                    ConnectorBindingRepository,
                )
                from services.database.session_factory import AsyncSessionFactory
                from services.mcp.consumer.connector import ConnectorStatusState

                async with AsyncSessionFactory.session_scope() as session:
                    binding = await ConnectorBindingRepository(session).get(self._user_id, "github")
                if binding is not None and binding.status == ConnectorStatusState.BOUND.value:
                    return True
            except Exception as e:  # binding check is additive — legacy still decides
                logger.debug(f"is_available binding check failed: {e}")
        return self.config_service.is_configured(self._user_id or "system")

    async def _try_connector_write(self, method_name: str, **kwargs):
        """#1220: attempt a write over the per-user OAuth grant.

        Returns the raw issue dict on VERIFIED success (the #1322 read-back
        guard); ``None`` when the write was definitively never fired (no
        user_id stashed, no adapter, or a pre-call rail degrade) — the ONLY
        state where the caller may fall back to the native PAT path without a
        double-write hazard. A fired-but-unverified write raises: the caller
        must surface honest uncertainty, never a confident success and never
        a second write through different credentials.
        """
        if not self.mcp_adapter or not self._user_id:
            return None
        method = getattr(self.mcp_adapter, method_name, None)
        if method is None:
            return None
        wr = await method(self._user_id, **kwargs)
        if wr.verified:
            logger.info("github_write_via_connector_verified")
            return wr.raw
        if not wr.attempted:
            return None  # never fired — safe native fallback
        raise RuntimeError(
            "GitHub write could not be verified — it may or may not have "
            "landed. Check the repository directly before retrying; do not "
            "assume success."
        )

    async def create_issue(
        self,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
        *,
        owner: Optional[str] = None,
        repo_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create GitHub issue.

        Issue #1042: ``owner`` and ``repo_name`` are now keyword-only optional
        args; resolved internally via ``repo_resolver`` if not provided.
        Raises ``RuntimeError`` if no repo resolves (creation must target
        a real repo).
        """
        if owner is None or repo_name is None:
            resolved = await self._resolve_default_repo()
            if resolved is None:
                raise RuntimeError(
                    "Cannot create GitHub issue: no repo could be resolved. "
                    "Pass owner/repo_name explicitly or configure default_repo."
                )
            owner, repo_name = resolved
        # #1220 write-path cutover: the user's OAuth grant first (read-back
        # verified, #1322 hard gate); native PAT only when the connector write
        # was definitively never fired (attempted=False) — a mid-flight failure
        # must NOT retry through another credential (double-write hazard).
        wr = await self._try_connector_write(
            "create_issue_connector",
            owner=owner,
            repo=repo_name,
            title=title,
            body=body,
            labels=labels,
            assignees=assignees,
        )
        if wr is not None:
            return wr
        return await self._get_integration("create_issue").create_issue(
            owner, repo_name, title, body, labels, assignees
        )

    async def update_issue(
        self,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
        *,
        owner: Optional[str] = None,
        repo_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update existing GitHub issue.

        Issue #1042: ``owner`` and ``repo_name`` are now keyword-only optional
        args; resolved internally via ``repo_resolver`` if not provided.
        Raises ``RuntimeError`` if no repo resolves.
        """
        if owner is None or repo_name is None:
            resolved = await self._resolve_default_repo()
            if resolved is None:
                raise RuntimeError(
                    f"Cannot update GitHub issue #{issue_number}: no repo " "could be resolved."
                )
            owner, repo_name = resolved
        # #1220: connector-first, no-double-write fallback (see create_issue).
        wr = await self._try_connector_write(
            "update_issue_connector",
            owner=owner,
            repo=repo_name,
            issue_number=issue_number,
            title=title,
            body=body,
            state=state,
            labels=labels,
            assignees=assignees,
        )
        if wr is not None:
            return wr
        return await self._get_integration("update_issue").update_issue(
            owner, repo_name, issue_number, title, body, state, labels, assignees
        )

    async def add_comment(
        self,
        issue_number: int,
        body: str,
        *,
        owner: Optional[str] = None,
        repo_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add comment to GitHub issue.

        Issue #1042: ``owner`` and ``repo_name`` are now keyword-only optional
        args; resolved internally via ``repo_resolver`` if not provided.
        Raises ``RuntimeError`` if no repo resolves.
        """
        if owner is None or repo_name is None:
            resolved = await self._resolve_default_repo()
            if resolved is None:
                raise RuntimeError(
                    f"Cannot add comment to GitHub issue #{issue_number}: "
                    "no repo could be resolved."
                )
            owner, repo_name = resolved
        # #1220: connector-first, no-double-write fallback (see create_issue).
        wr = await self._try_connector_write(
            "add_comment_connector",
            owner=owner,
            repo=repo_name,
            issue_number=issue_number,
            comment=body,
        )
        if wr is not None:
            return wr
        return await self._get_integration("add_comment").add_comment(
            owner, repo_name, issue_number, body
        )

    def get_integration_status(self) -> Dict[str, Any]:
        """Get current integration status for monitoring and debugging."""
        integration = self._get_integration("get_integration_status")
        if hasattr(integration, "get_integration_status"):
            return integration.get_integration_status()
        # Fallback status if integration doesn't support status method
        return {
            "router_initialized": True,
            "mcp_adapter_available": self.mcp_adapter is not None,
            "spatial_available": self.spatial_github is not None,
            "using_mcp": self.mcp_adapter is not None,
            "mcp_migration_complete": self.mcp_adapter is not None,
            "legacy_removed": True,
            "deprecation_timeline": {
                "week": self._get_deprecation_week(),
                "status": "Week 4 Complete - Legacy removed, MCP integrated",
                "legacy_removal_date": "2025-10-15",
                "mcp_integration_date": "2025-10-17",  # Today!
            },
        }

    def _get_boolean_flag(self, flag_name: str, default: bool = False) -> bool:
        """
        Get boolean environment variable with safe parsing.

        Supports: true/false, 1/0, yes/no, on/off

        Args:
            flag_name: Environment variable name
            default: Default value if not set

        Returns:
            Boolean value
        """
        try:
            value = os.getenv(flag_name, str(default)).lower().strip()
            return value in ("true", "1", "yes", "on", "enabled")
        except Exception:
            return default

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

        Used by: domain/github_domain_service.py.
        (issue_analyzer.py removed 2026-05-24 per #694 orphan-cleanup.)
        """
        return await self._get_integration("get_issue_by_url").get_issue_by_url(url)

    async def _resolve_default_repo(self, project: Optional[str] = None) -> Optional[tuple]:
        """Issue #1042: resolve (owner, name) for general queries.

        Decision tree per ``repo_resolver``: project-scoped → user default →
        env-var → ``None`` (signals graceful empty-result to caller).
        """
        try:
            from uuid import UUID

            from services.integrations.github.repo_resolver import (
                UnresolvedRepoError,
                resolve_repo,
            )

            user_uuid = None
            if self._user_id:
                try:
                    user_uuid = UUID(self._user_id)
                except (ValueError, TypeError):
                    user_uuid = None

            try:
                resolved = await resolve_repo(user_id=user_uuid, project_id=project)
                return (resolved.owner, resolved.name)
            except UnresolvedRepoError:
                logger.warning(
                    "GitHub general-query: no repo could be resolved "
                    "(no user default_repo, no PIPER_DEFAULT_REPO env var). "
                    "Returning empty result. (Issue #1042)"
                )
                return None
        except Exception as e:
            logger.warning(f"_resolve_default_repo failed: {e}")
            return None

    async def get_open_issues(
        self,
        project: Optional[str] = None,
        limit: int = 10,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get open issues from GitHub repository.

        Used by: domain/github_domain_service.py, domain/pm_number_manager.py

        ADAPTER METHOD (ADR-013 Phase 2): Translates interface for MCP adapter.
        Uses lazy initialization to ensure GitHub token is loaded.

        Issue #1042: ``owner``/``repo`` are now optional kwargs; if not
        provided, the router resolves via ``repo_resolver``. Returns ``[]``
        when no repo can be resolved (graceful empty-state).
        """
        # Lazy initialization (ensures token loaded on first use)
        if not self._initialized:
            await self.initialize()

        # MCP adapter uses different method name and parameters
        if self.mcp_adapter:
            if not owner or not repo:
                resolved = await self._resolve_default_repo(project)
                if resolved is None:
                    return []
                owner, repo = resolved
            all_issues = await self.mcp_adapter.list_github_issues_direct(repo, owner)
            # Filter for open issues only and limit
            open_issues = [issue for issue in all_issues if issue.get("state") == "open"]
            return open_issues[:limit] if open_issues else []
        # Spatial fallback
        return await self.spatial_github.get_open_issues(project, limit)

    async def get_recent_issues(
        self,
        limit: int = 10,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get recent issues (both open and closed) from GitHub repository.

        Used by: domain/github_domain_service.py

        ADAPTER METHOD (ADR-013 Phase 2): Translates interface for MCP adapter.
        Uses lazy initialization to ensure GitHub token is loaded.

        Issue #1042: ``owner``/``repo`` are now optional kwargs; router
        resolves via ``repo_resolver`` if not provided.
        """
        # Lazy initialization (ensures token loaded on first use)
        if not self._initialized:
            await self.initialize()

        # MCP adapter uses different method name and parameters
        if self.mcp_adapter:
            if not owner or not repo:
                resolved = await self._resolve_default_repo()
                if resolved is None:
                    return []
                owner, repo = resolved
            issues = await self.mcp_adapter.list_github_issues_direct(repo, owner)
            # Filter to limit (MCP adapter returns all, we limit here)
            return issues[:limit] if issues else []
        # Spatial fallback
        return await self.spatial_github.get_recent_issues(limit)

    async def list_milestones_via_mcp(
        self,
        state: str = "open",
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List GitHub milestones via MCP adapter (Issue #1039).

        ``owner``/``repo`` optional kwargs; router resolves via
        ``repo_resolver`` if not provided. Returns ``[]`` if unresolved.

        Args:
            state: GitHub milestone state filter — "open" (default),
                "closed", "all". User-facing UX is deferred to #1051;
                this kwarg is the underlying capability.
            owner: Repository owner (optional; resolved if not passed)
            repo: Repository name (optional; resolved if not passed)
        """
        if not self._initialized:
            await self.initialize()

        if self.mcp_adapter:
            if not owner or not repo:
                resolved = await self._resolve_default_repo()
                if resolved is None:
                    return []
                owner, repo = resolved
            return await self.mcp_adapter.list_milestones(repo, owner, state=state)
        # Spatial fallback: no spatial integration for milestones at MVP
        return []

    async def list_releases_via_mcp(
        self,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List GitHub releases via MCP adapter (Issue #1039).

        ``owner``/``repo`` optional kwargs; router resolves via
        ``repo_resolver`` if not provided. Returns ``[]`` if unresolved.

        Note: prerelease-only / stable-only filter is deferred to #1051.
        Handler shows prerelease flag inline where useful.
        """
        if not self._initialized:
            await self.initialize()

        if self.mcp_adapter:
            if not owner or not repo:
                resolved = await self._resolve_default_repo()
                if resolved is None:
                    return []
                owner, repo = resolved
            return await self.mcp_adapter.list_releases(repo, owner)
        # Spatial fallback: no spatial integration for releases at MVP
        return []

    async def list_labels_via_mcp(
        self,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """List GitHub labels via MCP adapter (Issue #1040).

        ``owner``/``repo`` optional kwargs; router resolves via
        ``repo_resolver`` if not provided. Returns ``[]`` if unresolved.
        """
        if not self._initialized:
            await self.initialize()

        if self.mcp_adapter:
            if not owner or not repo:
                resolved = await self._resolve_default_repo()
                if resolved is None:
                    return []
                owner, repo = resolved
            return await self.mcp_adapter.list_labels(repo, owner)
        # Spatial fallback: no spatial integration for labels at MVP
        return []

    async def list_branches_via_mcp(
        self,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List GitHub branches + default-branch identification (Issue #1040).

        Returns a dict with ``branches`` (list) + ``default_branch`` (str)
        so handler can sort default-first per Q5 disposition.

        ``owner``/``repo`` optional kwargs; router resolves via
        ``repo_resolver`` if not provided. Returns empty shape if unresolved.
        """
        if not self._initialized:
            await self.initialize()

        empty = {"branches": [], "default_branch": ""}
        if self.mcp_adapter:
            if not owner or not repo:
                resolved = await self._resolve_default_repo()
                if resolved is None:
                    return empty
                owner, repo = resolved
            branches = await self.mcp_adapter.list_branches(repo, owner)
            repo_info = await self.mcp_adapter.get_repository_info(repo, owner)
            default_branch = (repo_info or {}).get("default_branch", "") or ""
            return {"branches": branches, "default_branch": default_branch}
        # Spatial fallback
        return empty

    async def get_recent_activity(
        self, days: int = 7, repository: Optional[str] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get recent GitHub activity for standup (commits, PRs, issues).

        Used by: domain/standup_orchestration_service.py

        Issue #1646: ``repository`` (an ``owner/name`` full name) scopes the
        fetch to the repo the caller RESOLVED — the ANALYSIS handlers name a
        resolved repository in their copy, so the fetch must receive the same
        repo or the message claims a scope the query didn't have (m-43).
        ``None`` keeps the pre-#1646 shape (the integration's internally
        configured repo) for callers that never name one (canonical standup).
        """
        integration = self._get_integration("get_recent_activity")
        if repository is not None:
            return await integration.get_recent_activity(days, repository=repository)
        return await integration.get_recent_activity(days)

    def list_repositories(self) -> List[Dict[str, Any]]:
        """
        List accessible repositories.

        Used by: domain/github_domain_service.py
        """
        return self._get_integration("list_repositories").list_repositories()

    async def create_issue_from_work_item(
        self, repo_name: str, work_item: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create GitHub issue from work item data.
        """
        return await self._get_integration(
            "create_issue_from_work_item"
        ).create_issue_from_work_item(repo_name, work_item)

    async def create_pm_issue(
        self,
        repo_name: str,
        pm_number: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Create PM-specific GitHub issue."""
        return await self._get_integration("create_pm_issue").create_pm_issue(
            repo_name, pm_number, title, body, labels, assignees
        )

    async def get_closed_issues(
        self, project: Optional[str] = None, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get closed issues from GitHub repository.
        """
        return await self._get_integration("get_closed_issues").get_closed_issues(project, limit)

    async def get_issues_by_priority(self) -> List[Dict[str, Any]]:
        """
        Get GitHub issues organized by priority.
        """
        return await self._get_integration("get_issues_by_priority").get_issues_by_priority()

    async def get_development_context(self) -> Dict[str, Any]:
        """
        Get development context from GitHub.
        """
        return await self._get_integration("get_development_context").get_development_context()

    def parse_github_url(self, url: str) -> Optional[Tuple[str, str, int]]:
        """
        Parse GitHub issue URL to extract owner, repo, and issue number.
        """
        return self._get_integration("parse_github_url").parse_github_url(url)

    def test_connection(self) -> Dict[str, Any]:
        """
        Test GitHub connection and return status.
        """
        return self._get_integration("test_connection").test_connection()


# Convenience factory function
def create_github_integration() -> GitHubIntegrationRouter:
    """
    Create and initialize GitHub integration router.

    This is the primary entry point for all GitHub operations during the deprecation period.

    Returns:
        Configured GitHubIntegrationRouter instance
    """
    return GitHubIntegrationRouter()
