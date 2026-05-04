"""
GitHub MCP Spatial Adapter

GitHub-specific MCP spatial adapter implementation following the established
spatial adapter pattern for external system integration.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp

from services.integrations.mcp.token_counter import TokenCounter
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

from .consumer_core import MCPConsumerCore

logger = logging.getLogger(__name__)


class GitHubMCPSpatialAdapter(BaseSpatialAdapter):
    """
    GitHub MCP spatial adapter implementation.

    Maps GitHub issue numbers to spatial positions using MCP protocol
    for external service integration.
    """

    def __init__(self):
        super().__init__("github_mcp")
        self.mcp_consumer = MCPConsumerCore()
        self._lock = asyncio.Lock()
        self._issue_to_position: Dict[str, int] = {}
        self._position_to_issue: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        # GitHub API configuration
        self._github_token: Optional[str] = None
        self._github_api_base = "https://api.github.com"
        self._session: Optional[aiohttp.ClientSession] = None

        # Token counting for MCP operations (Issue #369)
        self.token_counter = TokenCounter()

        logger.info("GitHubMCPSpatialAdapter initialized")

    async def configure_github_api(
        self, token: Optional[str] = None, api_base: Optional[str] = None
    ):
        """Configure GitHub API access"""
        try:
            self._github_token = token
            if api_base:
                self._github_api_base = api_base

            # Create HTTP session for GitHub API calls
            if self._session is None:
                headers = {}
                if self._github_token:
                    headers["Authorization"] = f"token {self._github_token}"
                headers["Accept"] = "application/vnd.github.v3+json"

                self._session = aiohttp.ClientSession(headers=headers)
                logger.info("GitHub API session created")

            return True

        except Exception as e:
            logger.error(f"Error configuring GitHub API: {e}")
            return False

    async def _call_github_api(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Make GitHub API call"""
        try:
            if not self._session:
                logger.warning("GitHub API session not configured")
                return None

            url = f"{self._github_api_base}/{endpoint}"
            async with self._session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    logger.error("GitHub API authentication failed")
                    return None
                elif response.status == 403:
                    logger.error("GitHub API rate limit exceeded")
                    return None
                else:
                    logger.error(f"GitHub API error: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error calling GitHub API: {e}")
            return None

    async def _post_github_api(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Make GitHub API POST call"""
        try:
            if not self._session:
                logger.warning("GitHub API session not configured")
                return None

            url = f"{self._github_api_base}/{endpoint}"
            async with self._session.post(url, json=data) as response:
                if response.status in (200, 201):
                    return await response.json()
                elif response.status == 401:
                    logger.error("GitHub API authentication failed")
                    return None
                elif response.status == 403:
                    logger.error("GitHub API rate limit exceeded")
                    return None
                else:
                    logger.error(f"GitHub API error: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error calling GitHub API: {e}")
            return None

    async def _patch_github_api(
        self, endpoint: str, data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Make GitHub API PATCH call.

        Issue #902: Added for update operations (close/reopen issues, edit titles, etc.).
        Mirrors _post_github_api but uses PATCH method.
        """
        try:
            if not self._session:
                logger.warning("GitHub API session not configured")
                return None

            url = f"{self._github_api_base}/{endpoint}"
            async with self._session.patch(url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 401:
                    logger.error("GitHub API authentication failed")
                    return None
                elif response.status == 403:
                    logger.error("GitHub API rate limit exceeded")
                    return None
                elif response.status == 404:
                    logger.error(f"GitHub resource not found: {endpoint}")
                    return None
                elif response.status == 422:
                    error_body = await response.text()
                    logger.error(f"GitHub API validation error: {response.status} — {error_body}")
                    return None
                else:
                    logger.error(f"GitHub API error: {response.status}")
                    return None

        except Exception as e:
            logger.error(f"Error calling GitHub API PATCH: {e}")
            return None

    async def create_issue(
        self,
        owner: str,
        repo_name: str,
        title: str,
        body: str,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a GitHub issue via the REST API.

        Issue #892: This method was missing from GitHubMCPSpatialAdapter,
        causing AttributeError when GitHubIntegrationRouter._get_integration()
        returned the MCP adapter for create_issue operations.

        Issue #1042: ``owner`` is now a required positional arg (was hardcoded
        to "mediajunkie"). Callers must resolve owner via ``repo_resolver``.
        """
        endpoint = f"repos/{owner}/{repo_name}/issues"
        data: Dict[str, Any] = {"title": title, "body": body}
        if labels:
            data["labels"] = labels
        if assignees:
            data["assignees"] = assignees
        result = await self._post_github_api(endpoint, data)
        if result is None:
            raise RuntimeError("Failed to create GitHub issue — API returned no response")
        return result

    async def update_issue(
        self,
        owner: str,
        repo_name: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        labels: Optional[List[str]] = None,
        assignees: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Update a GitHub issue via the REST API.

        Issue #902: Completes the issue lifecycle — create, update, close, reopen.
        Previously missing, causing AttributeError when router delegated
        update_issue to MCP adapter.

        Issue #1042: ``owner`` is now a required positional arg (was hardcoded
        to "mediajunkie"). Callers must resolve owner via ``repo_resolver``.

        Args:
            owner: Repository owner (e.g., GitHub username/org)
            repo_name: Repository name (without owner prefix)
            issue_number: Issue number to update
            title: New title (optional)
            body: New body (optional)
            state: "open" or "closed" (optional)
            labels: New label list (optional, replaces existing)
            assignees: New assignee list (optional, replaces existing)
        """
        endpoint = f"repos/{owner}/{repo_name}/issues/{issue_number}"
        data: Dict[str, Any] = {}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = body
        if state is not None:
            data["state"] = state
        if labels is not None:
            data["labels"] = labels
        if assignees is not None:
            data["assignees"] = assignees

        if not data:
            raise ValueError("update_issue called with no fields to update")

        result = await self._patch_github_api(endpoint, data)
        if result is None:
            raise RuntimeError(
                f"Failed to update GitHub issue #{issue_number} — API returned no response"
            )
        return result

    async def add_comment(
        self, owner: str, repo_name: str, issue_number: int, body: str
    ) -> Optional[Dict[str, Any]]:
        """Add comment to GitHub issue.

        Issue #1042: ``owner`` is now a required positional arg.
        """
        endpoint = f"repos/{owner}/{repo_name}/issues/{issue_number}/comments"
        return await self._post_github_api(endpoint, {"body": body})

    async def list_github_issues_direct(
        self, repo: str, owner: str
    ) -> List[Dict[str, Any]]:
        """List GitHub issues directly via GitHub API.

        Issue #1042: ``repo`` and ``owner`` are now required positional args
        (were defaulted to "piper-morgan-product" / "mediajunkie"). Callers
        must resolve via ``repo_resolver``.
        """
        try:

            async def _operation():
                endpoint = f"repos/{owner}/{repo}/issues"
                params = {"state": "all", "per_page": 100}

                issues_data = await self._call_github_api(endpoint, params)
                if not issues_data:
                    logger.warning("No GitHub issues data received")
                    return []

                # Transform GitHub API response to our format
                issues = []
                for issue in issues_data:
                    issue_info = {
                        "number": issue.get("number"),
                        "title": issue.get("title"),
                        "description": issue.get("body", ""),
                        "state": issue.get("state"),
                        "repository": repo,
                        "uri": issue.get("html_url"),
                        "mime_type": "text/markdown",
                        "created_at": issue.get("created_at"),
                        "updated_at": issue.get("updated_at"),
                        "labels": [label["name"] for label in issue.get("labels", [])],
                        "assignees": [assignee["login"] for assignee in issue.get("assignees", [])],
                        "milestone": (
                            issue.get("milestone", {}).get("title")
                            if issue.get("milestone")
                            else None
                        ),
                        "user": issue.get("user", {}).get("login"),
                        "retrieved_via": "github_api",
                    }
                    issues.append(issue_info)

                    # Store context for spatial mapping
                    await self._store_github_context(issue_info)

                return issues

            result = await self.token_counter.wrap_mcp_call(
                "github_list_issues_direct",
                _operation(),
                input_data=f"repo={repo},owner={owner}",
            )
            logger.info(f"Retrieved {len(result)} issues from GitHub API for {owner}/{repo}")
            return result

        except Exception as e:
            logger.error(f"Error listing GitHub issues directly: {e}")
            return []

    async def get_closed_issues(
        self,
        repo: str,
        owner: str,
        project: str = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """#969: Get closed issues from GitHub API.

        Filters issues by state=closed. Used by _handle_shipped_this_week().

        Issue #1042: ``repo`` and ``owner`` are now required positional args
        (were defaulted to "piper-morgan-product" / "mediajunkie").
        """
        try:
            endpoint = f"repos/{owner}/{repo}/issues"
            params = {"state": "closed", "per_page": min(limit, 100)}
            issues_data = await self._call_github_api(endpoint, params)
            if not issues_data:
                return []

            issues = []
            for issue in issues_data:
                issues.append(
                    {
                        "number": issue.get("number"),
                        "title": issue.get("title"),
                        "state": issue.get("state"),
                        "closed_at": issue.get("closed_at"),
                        "repository": repo,
                        "labels": [label["name"] for label in issue.get("labels", [])],
                        "user": issue.get("user", {}).get("login"),
                    }
                )
            return issues

        except Exception as e:
            logger.error(f"Error getting closed issues: {e}")
            return []

    async def get_github_issue_direct(
        self, issue_number: str, repo: str, owner: str
    ) -> Optional[Dict[str, Any]]:
        """Get specific GitHub issue directly via GitHub API.

        Issue #1042: ``repo`` and ``owner`` are now required positional args.
        """
        try:

            async def _operation():
                endpoint = f"repos/{owner}/{repo}/issues/{issue_number}"

                issue_data = await self._call_github_api(endpoint)
                if not issue_data:
                    return None

                # Transform to our format
                issue_info = {
                    "number": issue_data.get("number"),
                    "title": issue_data.get("title"),
                    "description": issue_data.get("body", ""),
                    "state": issue_data.get("state"),
                    "repository": repo,
                    "uri": issue_data.get("html_url"),
                    "mime_type": "text/markdown",
                    "created_at": issue_data.get("created_at"),
                    "updated_at": issue_data.get("updated_at"),
                    "labels": [label["name"] for label in issue_data.get("labels", [])],
                    "assignees": [
                        assignee["login"] for assignee in issue_data.get("assignees", [])
                    ],
                    "milestone": (
                        issue_data.get("milestone", {}).get("title")
                        if issue_data.get("milestone")
                        else None
                    ),
                    "user": issue_data.get("user", {}).get("login"),
                    "retrieved_via": "github_api",
                }

                # Store context for spatial mapping
                await self._store_github_context(issue_info)

                return issue_info

            result = await self.token_counter.wrap_mcp_call(
                "github_get_issue_direct",
                _operation(),
                input_data=f"issue_number={issue_number},repo={repo},owner={owner}",
            )
            logger.info(f"Retrieved GitHub issue #{issue_number} from API")
            return result

        except Exception as e:
            logger.error(f"Error getting GitHub issue {issue_number}: {e}")
            return None

    async def _store_github_context(self, issue_info: Dict[str, Any]) -> None:
        """Store GitHub issue context for spatial mapping"""
        try:
            issue_number = str(issue_info.get("number"))
            if issue_number:
                context = {
                    "repository": issue_info.get("repository"),
                    "labels": issue_info.get("labels", []),
                    "milestone": issue_info.get("milestone"),
                    "priority": (
                        "high"
                        if "urgent" in str(issue_info.get("labels", [])).lower()
                        else "medium"
                    ),
                    "sentiment": "positive" if issue_info.get("state") == "closed" else "neutral",
                    "intent": "monitor",
                    "timestamp": issue_info.get("updated_at"),
                    "user": issue_info.get("user"),
                    "assignees": issue_info.get("assignees", []),
                }

                async with self._lock:
                    self._context_storage[issue_number] = context

        except Exception as e:
            logger.error(f"Error storing GitHub context: {e}")

    async def connect_to_mcp(self, mcp_config: Optional[Dict[str, Any]] = None) -> bool:
        """Connect to GitHub MCP server"""
        try:
            logger.info("Connecting to GitHub MCP service")

            # Use provided config or default
            if mcp_config is None:
                mcp_config = {
                    "name": "github",
                    "version": "1.0.0",
                    "description": "GitHub MCP Service",
                    "transport": "stdio",
                    "simulation_mode": True,
                    "timeout": 30.0,
                }

            # Connect to GitHub MCP service
            success = await self.mcp_consumer.connect("github", mcp_config)

            if success:
                logger.info("Successfully connected to GitHub MCP service")
                return True
            else:
                logger.error("Failed to connect to GitHub MCP service")
                return False

        except Exception as e:
            logger.error(f"Error connecting to GitHub MCP service: {e}")
            return False

    async def map_to_position(self, external_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """
        Map GitHub issue number to spatial position.

        Args:
            external_id: GitHub issue number (e.g., "123")
            context: Additional context including repository, labels, etc.

        Returns:
            SpatialPosition with integer position and context
        """
        async with self._lock:
            # Check if mapping already exists
            if external_id in self._mappings:
                return self._mappings[external_id]

            # Create new spatial position
            position = self._create_spatial_position(external_id, context)

            # Store bidirectional mapping
            self._issue_to_position[external_id] = position.position
            self._position_to_issue[position.position] = external_id

            # Store context for response routing
            self._store_context_for_routing(external_id, context)

            # Store mapping in parent class _mappings (no deadlock)
            self._mappings[external_id] = position

            logger.debug(f"Mapped GitHub issue {external_id} to position {position.position}")
            return position

    async def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """
        Map spatial position back to GitHub issue number.

        Args:
            position: Spatial position to reverse map

        Returns:
            GitHub issue number if mapping exists, None otherwise
        """
        async with self._lock:
            return self._position_to_issue.get(position.position)

    async def store_mapping(self, external_id: str, position: SpatialPosition) -> bool:
        """
        Store mapping between GitHub issue number and spatial position.

        Args:
            external_id: GitHub issue number
            position: Spatial position to map to

        Returns:
            True if mapping stored successfully, False otherwise
        """
        try:
            async with self._lock:
                self._mappings[external_id] = position
                self._issue_to_position[external_id] = position.position
                self._position_to_issue[position.position] = external_id

                logger.debug(
                    f"Stored mapping: GitHub issue {external_id} -> position {position.position}"
                )
                return True

        except Exception as e:
            logger.error(f"Error storing mapping for GitHub issue {external_id}: {e}")
            return False

    async def get_context(self, external_id: str) -> Optional[SpatialContext]:
        """
        Get spatial context for GitHub issue.

        Args:
            external_id: GitHub issue number

        Returns:
            SpatialContext if available, None otherwise
        """
        async with self._lock:
            if external_id in self._context_storage:
                context_data = self._context_storage[external_id]

                return SpatialContext(
                    territory_id=context_data.get("repository", "unknown"),
                    room_id=context_data.get("labels", "general"),
                    path_id=context_data.get("milestone", None),
                    object_position=self._issue_to_position.get(external_id),
                    attention_level=context_data.get("priority", "medium"),
                    emotional_valence=context_data.get("sentiment", "neutral"),
                    navigation_intent=context_data.get("intent", "monitor"),
                    external_system="github",
                    external_id=external_id,
                    external_context=context_data,
                )

            return None

    async def create_spatial_event_from_github(
        self, issue_number: str, event_type: str, context: Dict[str, Any]
    ) -> Any:
        """
        Create spatial event from GitHub issue event.

        Args:
            issue_number: GitHub issue number
            event_type: Type of event (created, updated, closed, etc.)
            context: Event context including changes, user, timestamp

        Returns:
            SpatialEvent representing the GitHub event
        """
        try:
            # Get spatial position for this issue
            position = await self.map_to_position(issue_number, context)

            # Create spatial event (placeholder - would integrate with existing event system)
            event_data = {
                "type": event_type,
                "issue_number": issue_number,
                "position": position.position,
                "context": context,
                "timestamp": context.get("timestamp"),
                "user": context.get("user"),
                "changes": context.get("changes", {}),
            }

            logger.info(f"Created spatial event for GitHub issue {issue_number}: {event_type}")
            return event_data

        except Exception as e:
            logger.error(f"Error creating spatial event for GitHub issue {issue_number}: {e}")
            return None

    async def create_spatial_object_from_github(
        self, issue_number: str, object_type: str, context: Dict[str, Any]
    ) -> Any:
        """
        Create spatial object from GitHub issue.

        Args:
            issue_number: GitHub issue number
            object_type: Type of object (issue, pull_request, etc.)
            context: Object context including metadata

        Returns:
            SpatialObject representing the GitHub object
        """
        try:
            # Get spatial position for this issue
            position = await self.map_to_position(issue_number, context)

            # Create spatial object (placeholder - would integrate with existing object system)
            object_data = {
                "type": object_type,
                "issue_number": issue_number,
                "position": position.position,
                "context": context,
                "repository": context.get("repository"),
                "labels": context.get("labels", []),
                "assignees": context.get("assignees", []),
                "milestone": context.get("milestone"),
                "state": context.get("state", "open"),
            }

            logger.info(f"Created spatial object for GitHub issue {issue_number}: {object_type}")
            return object_data

        except Exception as e:
            logger.error(f"Error creating spatial object for GitHub issue {issue_number}: {e}")
            return None

    async def list_issues_via_mcp(
        self, repo: str, owner: str
    ) -> List[Dict[str, Any]]:
        """
        List GitHub issues via MCP protocol with fallback to GitHub API.

        Issue #1042: ``repo`` and ``owner`` are now required positional args
        (was defaulted to "piper-morgan-product"). The fallback to
        ``list_github_issues_direct`` now threads ``owner`` through.

        Args:
            repo: Repository name
            owner: Repository owner

        Returns:
            List of GitHub issues
        """
        try:

            async def _operation():
                # Try MCP first
                if self.mcp_consumer.is_connected():
                    issues = await self.mcp_consumer.execute("list_issues", repo=repo)
                    if issues and len(issues) > 0:
                        logger.info(f"Retrieved {len(issues)} issues from GitHub via MCP")
                        return issues

                # Fallback to direct GitHub API
                logger.info("MCP not available, falling back to GitHub API")

                # Ensure GitHub API is configured for fallback
                if not self._session:
                    await self.configure_github_api()

                issues = await self.list_github_issues_direct(repo, owner)
                if issues:
                    logger.info(f"Retrieved {len(issues)} issues from GitHub API")
                    return issues

                # Final fallback to demo data
                logger.warning("Both MCP and GitHub API failed, using demo data")
                return [
                    {
                        "number": 1,
                        "title": "MCP Integration Implementation",
                        "description": "Implement MCP Consumer for external service integration",
                        "state": "open",
                        "repository": repo,
                        "uri": "mcp://demo/issue/1",
                        "mime_type": "text/plain",
                        "retrieved_via": "demo_fallback",
                    },
                    {
                        "number": 2,
                        "title": "GitHub MCP Adapter",
                        "description": "Create GitHub MCP spatial adapter following established patterns",
                        "state": "open",
                        "repository": repo,
                        "uri": "mcp://demo/issue/2",
                        "mime_type": "text/plain",
                        "retrieved_via": "demo_fallback",
                    },
                ]

            result = await self.token_counter.wrap_mcp_call(
                "github_list_issues_via_mcp",
                _operation(),
                input_data=f"repo={repo}",
            )
            logger.info(f"Retrieved {len(result)} issues via MCP for repo {repo}")
            return result

        except Exception as e:
            logger.error(f"Error listing GitHub issues via MCP: {e}")
            return []

    async def get_issue_via_mcp(
        self, issue_number: str, repo: str, owner: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get specific GitHub issue via MCP protocol with fallback to GitHub API.

        Issue #1042: ``repo`` and ``owner`` are now required positional args
        (was defaulted to "piper-morgan-product").

        Args:
            issue_number: GitHub issue number
            repo: Repository name
            owner: Repository owner

        Returns:
            GitHub issue data if found, None otherwise
        """
        try:

            async def _operation():
                # Try MCP first
                if self.mcp_consumer.is_connected():
                    # This would use the MCP protocol to fetch specific issue data
                    # For now, return basic info
                    mcp_issue = {
                        "number": issue_number,
                        "repository": repo,
                        "title": f"Issue #{issue_number}",
                        "state": "open",
                        "retrieved_via": "mcp",
                    }
                    logger.info(f"Retrieved issue #{issue_number} via MCP")
                    return mcp_issue

                # Fallback to direct GitHub API
                logger.info(f"MCP not available, trying GitHub API for issue #{issue_number}")

                # Ensure GitHub API is configured for fallback
                if not self._session:
                    await self.configure_github_api()

                issue = await self.get_github_issue_direct(issue_number, repo, owner)
                if issue:
                    return issue

                # Final fallback
                logger.warning(f"Issue #{issue_number} not found via MCP or GitHub API")
                return None

            result = await self.token_counter.wrap_mcp_call(
                "github_get_issue_via_mcp",
                _operation(),
                input_data=f"issue_number={issue_number},repo={repo}",
            )
            logger.info(f"Retrieved issue #{issue_number} via MCP")
            return result

        except Exception as e:
            logger.error(f"Error getting GitHub issue {issue_number} via MCP: {e}")
            return None

    async def get_response_context(self, issue_number: str) -> Optional[Dict[str, Any]]:
        """
        Get response context for GitHub issue.

        Args:
            issue_number: GitHub issue number

        Returns:
            Response context if available, None otherwise
        """
        async with self._lock:
            return self._context_storage.get(issue_number, {})

    def _store_context_for_routing(self, external_id: str, context: Dict[str, Any]) -> None:
        """Store context for response routing"""
        self._context_storage[external_id] = context.copy()

    async def get_mapping_stats(self) -> Dict[str, Any]:
        """Get mapping statistics"""
        async with self._lock:
            return {
                "total_mappings": len(self._mappings),
                "github_issues": len(self._issue_to_position),
                "spatial_positions": len(self._position_to_issue),
                "context_entries": len(self._context_storage),
                "mcp_connected": self.mcp_consumer.is_connected(),
            }

    async def cleanup_old_mappings(self, max_age_hours: int = 24) -> int:
        """
        Clean up old mappings.

        Args:
            max_age_hours: Maximum age in hours for mappings

        Returns:
            Number of mappings cleaned up
        """
        # This would implement cleanup logic based on age
        # For now, return 0 (placeholder)
        logger.debug(f"Cleanup requested for mappings older than {max_age_hours} hours")
        return 0

    async def disconnect(self):
        """Disconnect from MCP service and cleanup GitHub API session"""
        try:
            # Disconnect MCP consumer
            await self.mcp_consumer.disconnect()

            # Close GitHub API session
            if self._session:
                await self._session.close()
                self._session = None
                logger.info("GitHub API session closed")

            logger.info("GitHub MCP spatial adapter disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting GitHub MCP spatial adapter: {e}")

    async def cleanup(self):
        """Cleanup all resources"""
        try:
            await self.disconnect()

            # Clear mappings and context
            async with self._lock:
                self._issue_to_position.clear()
                self._position_to_issue.clear()
                self._context_storage.clear()

            logger.info("GitHub MCP spatial adapter cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()
