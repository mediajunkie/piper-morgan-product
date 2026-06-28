"""
QueryRouter Migration to Multi-Tool Spatial Intelligence
Following ADR-013: MCP + Spatial Intelligence Pattern

This module provides a migration path for QueryRouter to use
spatial intelligence for multiple tools including GitHub, Linear, CI/CD, and Development Environments.
"""

import logging
from typing import Any, Dict, List, Optional

from services.integrations.spatial.cicd_spatial import CICDSpatialIntelligence
from services.integrations.spatial.devenvironment_spatial import DevEnvironmentSpatialIntelligence
from services.integrations.spatial.gitbook_spatial import GitBookSpatialIntelligence
from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence
from services.integrations.spatial.linear_spatial import LinearSpatialIntelligence

logger = logging.getLogger(__name__)


class QueryRouterSpatialEnhancement:
    """Enhancement layer for QueryRouter to use spatial intelligence for multiple tools"""

    def __init__(self, query_router):
        """Initialize with existing QueryRouter instance"""
        self.query_router = query_router
        self.github_spatial = None
        self.linear_spatial = None
        self.cicd_spatial = None
        self.devenvironment_spatial = None
        self.gitbook_spatial = None

        # Replace adapters with spatial intelligence
        if self.query_router.enable_mcp_federation:
            self._upgrade_to_spatial()

    def _upgrade_to_spatial(self):
        """Upgrade integrations to spatial intelligence"""
        try:
            # Create spatial intelligence instances
            self.github_spatial = GitHubSpatialIntelligence()
            self.linear_spatial = LinearSpatialIntelligence()
            self.cicd_spatial = CICDSpatialIntelligence()
            self.devenvironment_spatial = DevEnvironmentSpatialIntelligence()
            self.gitbook_spatial = GitBookSpatialIntelligence()

            # Store original adapter for backward compatibility
            self.original_github_adapter = getattr(self.query_router, "github_adapter", None)

            # Replace with spatial-aware adapter
            self.query_router.github_adapter = self.github_spatial.mcp_adapter

            # Add Linear adapter to query router
            self.query_router.linear_adapter = self.linear_spatial.mcp_adapter

            # Add CI/CD adapter to query router
            self.query_router.cicd_adapter = self.cicd_spatial.mcp_adapter

            # Add Development Environment adapter to query router
            self.query_router.devenvironment_adapter = self.devenvironment_spatial.mcp_adapter

            # Add GitBook adapter to query router
            self.query_router.gitbook_adapter = self.gitbook_spatial.mcp_adapter

            logger.info(
                "QueryRouter upgraded to Multi-Tool Spatial Intelligence (GitHub + Linear + CI/CD + DevEnvironment + GitBook)"
            )

        except Exception as e:
            logger.error(f"Failed to upgrade to spatial intelligence: {e}")

    async def federated_search_with_spatial(
        self,
        query: str,
        include_linear: bool = True,
        include_cicd: bool = True,
        include_devenvironment: bool = True,
        include_gitbook: bool = True,
    ) -> Dict[str, Any]:
        """
        Enhanced federated search with 8-dimensional spatial analysis across GitHub, Linear, CI/CD, Development Environments, and GitBook
        """
        # Get basic results from original federated search
        results = await self.query_router.federated_search(query)

        # Add Linear search results
        if include_linear and self.linear_spatial:
            linear_results = await self._search_linear_with_spatial(query)
            results["linear_results"] = linear_results
            if linear_results:
                results["sources"].append("linear_mcp")

        # Add CI/CD search results
        if include_cicd and self.cicd_spatial:
            cicd_results = await self._search_cicd_with_spatial(query)
            results["cicd_results"] = cicd_results
            if cicd_results:
                results["sources"].append("cicd_mcp")

        # Add Development Environment search results
        if include_devenvironment and self.devenvironment_spatial:
            devenvironment_results = await self._search_devenvironment_with_spatial(query)
            results["devenvironment_results"] = devenvironment_results
            if devenvironment_results:
                results["sources"].append("devenvironment_mcp")

        # Add GitBook search results
        if include_gitbook and self.gitbook_spatial:
            gitbook_results = await self._search_gitbook_with_spatial(query)
            results["gitbook_results"] = gitbook_results
            if gitbook_results:
                results["sources"].append("gitbook_mcp")

        # Enhance GitHub results with spatial intelligence
        if self.github_spatial and results.get("github_results"):
            enhanced_github_results = []

            for issue_data in results["github_results"]:
                try:
                    # Create full issue object (simplified for demo)
                    issue = {
                        "number": issue_data["number"],
                        "title": issue_data["title"],
                        "body": issue_data.get("description", ""),
                        "state": issue_data.get("state", "open"),
                        "created_at": issue_data.get("created_at", "2025-08-12T00:00:00Z"),
                        "updated_at": issue_data.get("updated_at", "2025-08-12T00:00:00Z"),
                        "labels": issue_data.get("labels", []),
                        "assignees": issue_data.get("assignees", []),
                        "milestone": issue_data.get("milestone"),
                        "comments": issue_data.get("comments", 0),
                        "reactions": {"total_count": 0},
                        # Issue #1042: was hardcoded to mediajunkie/piper-morgan-product;
                        # repository now derived from incoming issue_data when present.
                        "repository": issue_data.get("repository") or {},
                    }

                    # Create spatial context with 8-dimensional analysis
                    spatial_context = await self.github_spatial.create_spatial_context(issue)

                    # Add spatial intelligence to result
                    issue_data["spatial_intelligence"] = {
                        "source": "github",
                        "attention_level": spatial_context.attention_level,
                        "emotional_valence": spatial_context.emotional_valence,
                        "navigation_intent": spatial_context.navigation_intent,
                        "dimensions": spatial_context.external_context,
                    }

                    enhanced_github_results.append(issue_data)

                except Exception as e:
                    logger.warning(
                        f"Failed to enhance GitHub issue {issue_data.get('number')} with spatial: {e}"
                    )
                    enhanced_github_results.append(issue_data)  # Keep original if enhancement fails

            results["github_results"] = enhanced_github_results
            results["spatial_enhanced"] = True

            logger.info(
                f"Enhanced {len(enhanced_github_results)} GitHub results with spatial intelligence"
            )

        # Update total results
        all_results = (
            results["github_results"]
            + results.get("linear_results", [])
            + results.get("cicd_results", [])
            + results.get("devenvironment_results", [])
            + results.get("local_results", [])
        )
        results["total_results"] = len(all_results)
        results["all_results"] = all_results

        return results

    async def _search_linear_with_spatial(self, query: str) -> List[Dict[str, Any]]:
        """Search Linear issues and enhance with spatial intelligence"""
        try:
            # Configure Linear adapter if needed
            await self.linear_spatial.initialize()

            # Search Linear issues
            linear_issues = await self.linear_spatial.mcp_adapter.search_issues(query, limit=10)

            enhanced_linear_results = []
            for issue in linear_issues:
                try:
                    # Create spatial context with 8-dimensional analysis
                    spatial_context = await self.linear_spatial.create_spatial_context(issue)

                    # Format result with spatial intelligence
                    result = {
                        "source": "linear_mcp",
                        "type": "issue",
                        "id": issue.get("id"),
                        "number": issue.get("number"),
                        "title": issue.get("title"),
                        "description": (
                            issue.get("description", "")[:200] + "..."
                            if issue.get("description")
                            else ""
                        ),
                        "state": issue.get("state", {}).get("name", "unknown"),
                        "priority": issue.get("priority", 0),
                        "team": issue.get("team", {}).get("key", "unknown"),
                        "project": (
                            issue.get("project", {}).get("name") if issue.get("project") else None
                        ),
                        "assignee": (
                            issue.get("assignee", {}).get("email")
                            if issue.get("assignee")
                            else None
                        ),
                        "spatial_intelligence": {
                            "source": "linear",
                            "attention_level": spatial_context.attention_level,
                            "emotional_valence": spatial_context.emotional_valence,
                            "navigation_intent": spatial_context.navigation_intent,
                            "dimensions": spatial_context.external_context,
                        },
                    }

                    enhanced_linear_results.append(result)

                except Exception as e:
                    logger.warning(
                        f"Failed to enhance Linear issue {issue.get('id')} with spatial: {e}"
                    )
                    # Keep basic result without spatial enhancement
                    basic_result = {
                        "source": "linear_mcp",
                        "type": "issue",
                        "id": issue.get("id"),
                        "number": issue.get("number"),
                        "title": issue.get("title"),
                        "description": (
                            issue.get("description", "")[:200] + "..."
                            if issue.get("description")
                            else ""
                        ),
                        "state": issue.get("state", {}).get("name", "unknown"),
                        "team": issue.get("team", {}).get("key", "unknown"),
                    }
                    enhanced_linear_results.append(basic_result)

            logger.info(
                f"Found {len(enhanced_linear_results)} Linear results with spatial intelligence for '{query}'"
            )
            return enhanced_linear_results

        except Exception as e:
            logger.warning(f"Linear search failed: {e}")
            return []

    async def _search_cicd_with_spatial(self, query: str) -> List[Dict[str, Any]]:
        """Search CI/CD pipelines and enhance with spatial intelligence"""
        try:
            # Configure CI/CD adapter if needed
            await self.cicd_spatial.initialize()

            # Issue #1042: was hardcoded to ["mediajunkie/piper-morgan-product"];
            # now resolves via repo_resolver. Returns empty if unresolved
            # (search_pipelines requires a repo target).
            try:
                from services.integrations.github.repo_resolver import (
                    UnresolvedRepoError,
                    resolve_repo,
                )

                resolved = await resolve_repo()
                repositories = [f"{resolved.owner}/{resolved.name}"]
            except UnresolvedRepoError:
                logger.warning("CI/CD search: no repo could be resolved; skipping " "(Issue #1042)")
                return []
            cicd_pipelines = await self.cicd_spatial.mcp_adapter.search_pipelines(
                query, repositories, limit=10
            )

            enhanced_cicd_results = []
            for pipeline in cicd_pipelines:
                try:
                    # Create spatial context with 8-dimensional analysis
                    spatial_context = await self.cicd_spatial.create_spatial_context(pipeline)

                    # Format result with spatial intelligence
                    result = {
                        "source": "cicd_mcp",
                        "type": "pipeline",
                        "id": pipeline.get("id"),
                        "run_id": pipeline.get("run_id", pipeline.get("id")),
                        "workflow_name": pipeline.get("workflow_name"),
                        "status": pipeline.get("status"),
                        "conclusion": pipeline.get("conclusion"),
                        "platform": pipeline.get("platform"),
                        "branch": pipeline.get("branch"),
                        "repository": pipeline.get("repository", {}).get("full_name"),
                        "triggered_by": (
                            pipeline.get("triggered_by", {}).get("login")
                            if pipeline.get("triggered_by")
                            else None
                        ),
                        "environment": pipeline.get("environment"),
                        "url": pipeline.get("url"),
                        "created_at": pipeline.get("created_at"),
                        "updated_at": pipeline.get("updated_at"),
                        "spatial_intelligence": {
                            "source": "cicd",
                            "attention_level": spatial_context.attention_level,
                            "emotional_valence": spatial_context.emotional_valence,
                            "navigation_intent": spatial_context.navigation_intent,
                            "dimensions": spatial_context.external_context,
                        },
                    }

                    enhanced_cicd_results.append(result)

                except Exception as e:
                    logger.warning(
                        f"Failed to enhance CI/CD pipeline {pipeline.get('id')} with spatial: {e}"
                    )
                    # Keep basic result without spatial enhancement
                    basic_result = {
                        "source": "cicd_mcp",
                        "type": "pipeline",
                        "id": pipeline.get("id"),
                        "workflow_name": pipeline.get("workflow_name"),
                        "status": pipeline.get("status"),
                        "platform": pipeline.get("platform"),
                        "branch": pipeline.get("branch"),
                        "repository": pipeline.get("repository", {}).get("full_name"),
                    }
                    enhanced_cicd_results.append(basic_result)

            logger.info(
                f"Found {len(enhanced_cicd_results)} CI/CD results with spatial intelligence for '{query}'"
            )
            return enhanced_cicd_results

        except Exception as e:
            logger.warning(f"CI/CD search failed: {e}")
            return []

    async def _search_devenvironment_with_spatial(self, query: str) -> List[Dict[str, Any]]:
        """Search development environments and enhance with spatial intelligence"""
        try:
            # Configure Development Environment adapter if needed
            await self.devenvironment_spatial.initialize()

            # Search development environments across platforms
            platforms = ["docker", "vscode"]  # Default platforms
            dev_environments = await self.devenvironment_spatial.mcp_adapter.search_environments(
                query, platforms, limit=10
            )

            enhanced_devenvironment_results = []
            for environment in dev_environments:
                try:
                    # Create spatial context with 8-dimensional analysis
                    spatial_context = await self.devenvironment_spatial.create_spatial_context(
                        environment
                    )

                    # Format result with spatial intelligence
                    result = {
                        "source": "devenvironment_mcp",
                        "type": "environment",
                        "id": environment.get("id"),
                        "name": environment.get("name"),
                        "env_type": environment.get("type"),
                        "status": environment.get("status"),
                        "health_status": environment.get("health_status"),
                        "platform": environment.get("platform"),
                        "project": environment.get("project", {}).get("name"),
                        "workspace": environment.get("workspace", {}).get("name"),
                        "technologies": environment.get("technologies", []),
                        "cpu_usage": environment.get("cpu_usage", 0),
                        "memory_usage": environment.get("memory_usage", 0),
                        "uptime_seconds": environment.get("uptime_seconds"),
                        "restart_count": environment.get("restart_count", 0),
                        "created_at": environment.get("created_at"),
                        "spatial_intelligence": {
                            "source": "development",
                            "attention_level": spatial_context.attention_level,
                            "emotional_valence": spatial_context.emotional_valence,
                            "navigation_intent": spatial_context.navigation_intent,
                            "dimensions": spatial_context.external_context,
                        },
                    }

                    enhanced_devenvironment_results.append(result)

                except Exception as e:
                    logger.warning(
                        f"Failed to enhance development environment {environment.get('id')} with spatial: {e}"
                    )
                    # Keep basic result without spatial enhancement
                    basic_result = {
                        "source": "devenvironment_mcp",
                        "type": "environment",
                        "id": environment.get("id"),
                        "name": environment.get("name"),
                        "status": environment.get("status"),
                        "platform": environment.get("platform"),
                        "project": environment.get("project", {}).get("name"),
                    }
                    enhanced_devenvironment_results.append(basic_result)

            logger.info(
                f"Found {len(enhanced_devenvironment_results)} development environment results with spatial intelligence for '{query}'"
            )
            return enhanced_devenvironment_results

        except Exception as e:
            logger.warning(f"Development environment search failed: {e}")
            return []

    async def _search_gitbook_with_spatial(self, query: str) -> List[Dict[str, Any]]:
        """Search GitBook content and enhance with spatial intelligence"""
        try:
            # Configure GitBook adapter if needed
            await self.gitbook_spatial.initialize()

            # Search across all accessible spaces
            spaces = await self.gitbook_spatial.mcp_adapter.get_spaces()
            all_gitbook_results = []

            for space in spaces[:3]:  # Limit to first 3 spaces for performance
                try:
                    # Search pages within this space
                    space_results = await self.gitbook_spatial.mcp_adapter.search_pages(
                        space["id"], query, limit=5
                    )

                    for page in space_results:
                        try:
                            # Create spatial context with 8-dimensional analysis
                            spatial_context = await self.gitbook_spatial.create_spatial_context(
                                page
                            )

                            # Format result with spatial intelligence
                            result = {
                                "source": "gitbook_mcp",
                                "type": "page",
                                "id": page.get("id"),
                                "title": page.get("title"),
                                "description": (
                                    page.get("description", "")[:200] + "..."
                                    if page.get("description")
                                    else ""
                                ),
                                "visibility": page.get("visibility", "public"),
                                "space_id": space.get("id"),
                                "space_name": space.get("name"),
                                "collection_id": page.get("collectionId"),
                                "collection_name": page.get("collectionName"),
                                "created_at": page.get("createdAt"),
                                "updated_at": page.get("updatedAt"),
                                "author": page.get("author", {}).get("name"),
                                "tags": page.get("tags", []),
                                "spatial_intelligence": {
                                    "source": "gitbook",
                                    "attention_level": spatial_context.attention_level,
                                    "emotional_valence": spatial_context.emotional_valence,
                                    "navigation_intent": spatial_context.navigation_intent,
                                    "dimensions": spatial_context.external_context,
                                },
                            }

                            all_gitbook_results.append(result)

                        except Exception as e:
                            logger.warning(
                                f"Failed to enhance GitBook page {page.get('id')} with spatial: {e}"
                            )
                            # Keep basic result without spatial enhancement
                            basic_result = {
                                "source": "gitbook_mcp",
                                "type": "page",
                                "id": page.get("id"),
                                "title": page.get("title"),
                                "description": (
                                    page.get("description", "")[:200] + "..."
                                    if page.get("description")
                                    else ""
                                ),
                                "visibility": page.get("visibility", "public"),
                                "space_id": space.get("id"),
                                "space_name": space.get("name"),
                            }
                            all_gitbook_results.append(basic_result)

                except Exception as e:
                    logger.warning(f"Failed to search space {space.get('id')}: {e}")
                    continue

            logger.info(
                f"Found {len(all_gitbook_results)} GitBook results with spatial intelligence for '{query}'"
            )
            return all_gitbook_results

        except Exception as e:
            logger.warning(f"GitBook search failed: {e}")
            return []


def migrate_query_router_to_spatial(query_router) -> QueryRouterSpatialEnhancement:
    """
    Migration function to upgrade QueryRouter to spatial intelligence

    Usage:
        from services.queries.query_router import QueryRouter
        from services.queries.query_router_spatial_migration import migrate_query_router_to_spatial

        router = QueryRouter(...)
        spatial_router = migrate_query_router_to_spatial(router)

        # Use enhanced federated search
        results = await spatial_router.federated_search_with_spatial("high priority bugs")
    """
    return QueryRouterSpatialEnhancement(query_router)
