"""
TDD Tests for GitHub Spatial Intelligence Integration
Following ADR-013: MCP + Spatial Intelligence Pattern
"""

import asyncio
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence
from services.integrations.spatial_adapter import SpatialContext, SpatialPosition


class TestGitHubSpatialIntelligence:
    """Test suite for GitHub 8-dimensional spatial intelligence"""

    @pytest.fixture
    async def github_spatial(self):
        """Create GitHubSpatialIntelligence instance for testing"""
        spatial = GitHubSpatialIntelligence()
        await spatial.initialize()
        return spatial

    @pytest.fixture
    def sample_issue(self):
        """Sample GitHub issue data.

        Dates are relative to now (#1353/#1355): the original hardcoded
        absolute dates (~Aug 2025) only satisfied the "2 days ago" / "high
        urgency" assertions below at authoring time and silently rotted as
        calendar time passed. `age_days`/`urgency`/`time_to_milestone_days`
        below all derive from these three fields.
        """
        now = datetime.now(timezone.utc)
        return {
            "number": 156,
            "title": "Login authentication failing",
            "state": "open",
            "created_at": (now - timedelta(days=2, hours=1)).isoformat(),
            "updated_at": (now - timedelta(hours=3)).isoformat(),
            "labels": [{"name": "bug"}, {"name": "high-priority"}],
            "assignees": [{"login": "john_doe"}],
            "milestone": {
                "title": "v1.2",
                "due_on": (now + timedelta(days=2, hours=1)).isoformat(),
            },
            "comments": 5,
            "reactions": {"total_count": 3},
            "pull_request": None,
            "repository": {"owner": "mediajunkie", "name": "piper-morgan-product"},
        }

    # DIMENSION 1: HIERARCHY Tests
    @pytest.mark.asyncio
    async def test_github_spatial_hierarchy(self, github_spatial, sample_issue):
        """Test issue hierarchy analysis (issues, PRs, parent-child relationships)"""
        hierarchy = await github_spatial.analyze_issue_hierarchy(sample_issue)

        assert hierarchy["level"] == "root"  # No parent issue
        assert hierarchy["type"] == "issue"  # Not a PR
        assert hierarchy["depth"] == 0
        assert hierarchy["has_children"] == False

    # DIMENSION 2: TEMPORAL Tests
    @pytest.mark.asyncio
    async def test_github_spatial_temporal(self, github_spatial, sample_issue):
        """Test timeline analysis (created, updated, activity patterns)"""
        temporal = await github_spatial.analyze_timeline(sample_issue)

        assert temporal["age_days"] == 2  # Created 2 days ago
        assert temporal["last_activity_hours"] < 24  # Updated within day
        assert temporal["activity_level"] == "active"
        assert temporal["urgency"] == "high"  # Due to milestone proximity

    # DIMENSION 3: PRIORITY Tests
    @pytest.mark.asyncio
    async def test_github_spatial_priority(self, github_spatial, sample_issue):
        """Test priority signal analysis (labels, milestones, assignees)"""
        priority = await github_spatial.analyze_priority_signals(sample_issue)

        assert priority["priority_level"] == "high"
        assert priority["has_milestone"] == True
        assert priority["is_bug"] == True
        assert priority["assigned"] == True
        assert priority["attention_score"] >= 0.8  # High attention needed

    # DIMENSION 4: COLLABORATIVE Tests
    @pytest.mark.asyncio
    async def test_github_spatial_collaborative(self, github_spatial, sample_issue):
        """Test team activity analysis (assignees, reviewers, commenters)"""
        collaborative = await github_spatial.analyze_team_activity(sample_issue)

        assert collaborative["assignee_count"] == 1
        assert collaborative["comment_count"] == 5
        assert collaborative["engagement_level"] == "moderate"
        assert collaborative["reaction_count"] == 3
        assert "john_doe" in collaborative["participants"]

    # DIMENSION 5: FLOW Tests
    @pytest.mark.asyncio
    async def test_github_spatial_flow(self, github_spatial, sample_issue):
        """Test workflow state analysis (open/closed, blocked, in-progress)"""
        flow = await github_spatial.analyze_workflow_state(sample_issue)

        assert flow["state"] == "open"
        assert flow["is_blocked"] == False
        assert flow["workflow_stage"] == "assigned"
        assert flow["completion_percentage"] == 25  # Assigned stage

    # DIMENSION 6: QUANTITATIVE Tests
    @pytest.mark.asyncio
    async def test_github_spatial_quantitative(self, github_spatial, sample_issue):
        """Test metrics analysis (counts, sizes, velocities)"""
        metrics = await github_spatial.analyze_metrics(sample_issue)

        assert metrics["comment_velocity"] > 0  # Comments per day
        assert metrics["engagement_score"] > 0
        assert metrics["complexity_estimate"] == "low"
        assert metrics["time_to_milestone_days"] == 2

    # DIMENSION 7: CAUSAL Tests
    @pytest.mark.asyncio
    async def test_github_spatial_causal(self, github_spatial, sample_issue):
        """Test dependency analysis (linked issues, blocks, dependencies)"""
        causal = await github_spatial.analyze_dependencies(sample_issue)

        assert causal["blocks"] == []
        assert causal["blocked_by"] == []
        assert causal["related_issues"] == []
        assert causal["dependency_chain_length"] == 0

    # DIMENSION 8: CONTEXTUAL Tests
    @pytest.mark.asyncio
    async def test_github_spatial_contextual(self, github_spatial, sample_issue):
        """Test project context analysis (repository, organization context)"""
        context = await github_spatial.analyze_project_context(sample_issue)

        assert context["repository"] == "piper-morgan-product"
        assert context["organization"] == "mediajunkie"
        assert context["domain"] == "product_management"
        assert context["visibility"] == "public"

    # INTEGRATION Tests
    @pytest.mark.asyncio
    async def test_github_spatial_full_integration(self, github_spatial, sample_issue):
        """Test full MCP+Spatial flow with all 8 dimensions"""
        # Create spatial context
        spatial_context = await github_spatial.create_spatial_context(sample_issue)

        # Verify all dimensions present
        assert spatial_context.territory_id == "github"
        assert spatial_context.room_id == "piper-morgan-product"
        assert spatial_context.path_id == "issues/156"
        assert spatial_context.attention_level == "urgent"
        assert spatial_context.emotional_valence == "negative"  # Bug
        assert spatial_context.navigation_intent == "respond"

        # Verify external context has all dimension data
        external = spatial_context.external_context
        assert "hierarchy" in external
        assert "temporal" in external
        assert "priority" in external
        assert "collaborative" in external
        assert "flow" in external
        assert "quantitative" in external
        assert "causal" in external
        assert "contextual" in external

    @pytest.mark.asyncio
    async def test_github_spatial_mcp_adapter_integration(self, github_spatial):
        """Test integration with existing MCP GitHub adapter"""
        # Verify MCP adapter is properly initialized
        # (#1355: the adapter's real inverse-mapping method is `map_from_position`
        # per the SpatialAdapter protocol — `resolve_from_position` never existed
        # anywhere in this repo's history; this was a stale/typo'd assertion.)
        assert github_spatial.mcp_adapter is not None
        assert hasattr(github_spatial.mcp_adapter, "map_to_position")
        assert hasattr(github_spatial.mcp_adapter, "map_from_position")

        # Test mapping issue to spatial position
        position = await github_spatial.map_issue_to_position("156", {})
        assert isinstance(position, SpatialPosition)
        assert position.position > 0

    @pytest.mark.asyncio
    async def test_github_spatial_backward_compatibility(self, github_spatial):
        """Test backward compatibility with existing GitHub integration"""
        # Should still support basic issue fetching. get_issue() resolves an
        # owner via repo_resolver when given a bare repo name (no "/") — mock
        # that resolution (#1355) rather than depend on ambient PIPER_DEFAULT_REPO
        # env state / a real user_id, neither of which this call provides.
        from services.integrations.github.repo_resolver import ResolvedRepo

        with patch.object(github_spatial.mcp_adapter, "_call_github_api") as mock_api, patch(
            "services.integrations.github.repo_resolver.resolve_repo"
        ) as mock_resolve:
            mock_api.return_value = {"number": 156}
            mock_resolve.return_value = ResolvedRepo(
                owner="mediajunkie", name="piper-morgan-product", source="explicit"
            )

            issue = await github_spatial.get_issue("piper-morgan-product", 156)
            assert issue["number"] == 156
            mock_api.assert_called_once()

    @pytest.mark.asyncio
    async def test_github_spatial_performance(self, github_spatial, sample_issue):
        """Test spatial analysis performance requirements"""
        import time

        start = time.time()
        spatial_context = await github_spatial.create_spatial_context(sample_issue)
        elapsed = time.time() - start

        # Should complete all 8-dimensional analysis in <50ms
        assert elapsed < 0.05, f"Spatial analysis took {elapsed*1000:.2f}ms"
        assert spatial_context is not None
