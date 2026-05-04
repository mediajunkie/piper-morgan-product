"""
GitHub Spatial Intelligence Implementation
Following ADR-013: MCP + Spatial Intelligence Pattern

Retrofit from MCP-only to full 8-dimensional spatial analysis.
"""

import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)
from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

logger = logging.getLogger(__name__)


class GitHubSpatialIntelligence:
    """
    GitHub integration using MCP + Spatial Intelligence pattern.
    Retrofit from MCP-only to full 8-dimensional spatial analysis.

    8 Dimensions:
    1. HIERARCHY - Issue/PR relationships, parent-child structures
    2. TEMPORAL - Created/updated patterns, activity timelines
    3. PRIORITY - Labels, milestones, assignee signals
    4. COLLABORATIVE - Team activity, reviewers, commenters
    5. FLOW - Workflow states, open/closed, blocked status
    6. QUANTITATIVE - Counts, sizes, velocities, metrics
    7. CAUSAL - Dependencies, linked issues, blocks
    8. CONTEXTUAL - Repository, organization, project context
    """

    def __init__(self):
        """Initialize GitHub spatial intelligence with MCP adapter"""
        self.mcp_adapter = GitHubMCPSpatialAdapter()

        # 8-dimensional analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_issue_hierarchy,
            "TEMPORAL": self.analyze_timeline,
            "PRIORITY": self.analyze_priority_signals,
            "COLLABORATIVE": self.analyze_team_activity,
            "FLOW": self.analyze_workflow_state,
            "QUANTITATIVE": self.analyze_metrics,
            "CAUSAL": self.analyze_dependencies,
            "CONTEXTUAL": self.analyze_project_context,
        }

        logger.info("GitHubSpatialIntelligence initialized with 8 dimensions")

    async def initialize(self):
        """Initialize MCP adapter and connections"""
        await self.mcp_adapter.configure_github_api()
        logger.info("GitHub MCP adapter configured")

    # DIMENSION 1: HIERARCHY
    async def analyze_issue_hierarchy(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze issue/PR hierarchy and relationships"""
        hierarchy = {
            "level": "root",  # root, child, subtask
            "type": "pull_request" if issue.get("pull_request") else "issue",
            "depth": 0,
            "has_children": False,
            "parent_issue": None,
            "child_issues": [],
        }

        # Check for parent-child relationships in body/comments
        body = issue.get("body", "")
        if "closes #" in body.lower() or "fixes #" in body.lower():
            hierarchy["level"] = "child"
            hierarchy["depth"] = 1

        return hierarchy

    # DIMENSION 2: TEMPORAL
    async def analyze_timeline(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze temporal patterns and activity timeline"""
        from datetime import timezone

        now = datetime.now(timezone.utc)
        created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
        updated = datetime.fromisoformat(issue["updated_at"].replace("Z", "+00:00"))

        age_days = (now - created).days
        last_activity_hours = (now - updated).total_seconds() / 3600

        # Determine activity level
        if last_activity_hours < 24:
            activity_level = "active"
        elif last_activity_hours < 72:
            activity_level = "recent"
        elif last_activity_hours < 168:  # 1 week
            activity_level = "moderate"
        else:
            activity_level = "stale"

        # Check milestone urgency
        urgency = "normal"
        if milestone := issue.get("milestone"):
            if due_on := milestone.get("due_on"):
                due_date = datetime.fromisoformat(due_on.replace("Z", "+00:00"))
                days_to_due = (due_date - now).days
                if days_to_due <= 3:
                    urgency = "high"
                elif days_to_due <= 7:
                    urgency = "medium"

        return {
            "age_days": age_days,
            "last_activity_hours": last_activity_hours,
            "activity_level": activity_level,
            "urgency": urgency,
            "created_at": created.isoformat(),
            "updated_at": updated.isoformat(),
        }

    # DIMENSION 3: PRIORITY
    async def analyze_priority_signals(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze priority signals from labels, milestones, assignees"""
        labels = [label["name"] for label in issue.get("labels", [])]

        # Determine priority level
        priority_level = "normal"
        if any(label in ["critical", "urgent", "p0"] for label in labels):
            priority_level = "critical"
        elif any(label in ["high-priority", "important", "p1"] for label in labels):
            priority_level = "high"
        elif any(label in ["low-priority", "nice-to-have", "p3"] for label in labels):
            priority_level = "low"

        # Calculate attention score (0.0 - 1.0)
        attention_score = 0.5  # Base score

        if priority_level == "critical":
            attention_score = 1.0
        elif priority_level == "high":
            attention_score = 0.8
        elif priority_level == "low":
            attention_score = 0.3

        if issue.get("milestone"):
            attention_score = min(1.0, attention_score + 0.2)

        if issue.get("assignees"):
            attention_score = min(1.0, attention_score + 0.1)

        return {
            "priority_level": priority_level,
            "has_milestone": bool(issue.get("milestone")),
            "is_bug": "bug" in labels,
            "is_feature": "enhancement" in labels or "feature" in labels,
            "assigned": bool(issue.get("assignees")),
            "attention_score": attention_score,
            "labels": labels,
        }

    # DIMENSION 4: COLLABORATIVE
    async def analyze_team_activity(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze team collaboration and engagement"""
        assignees = [a["login"] for a in issue.get("assignees", [])]
        comment_count = issue.get("comments", 0)
        reaction_count = issue.get("reactions", {}).get("total_count", 0)

        # Determine engagement level
        total_engagement = comment_count + reaction_count
        if total_engagement >= 10:
            engagement_level = "high"
        elif total_engagement >= 5:
            engagement_level = "moderate"
        else:
            engagement_level = "low"

        participants = set(assignees)
        if author := issue.get("user", {}).get("login"):
            participants.add(author)

        return {
            "assignee_count": len(assignees),
            "comment_count": comment_count,
            "reaction_count": reaction_count,
            "engagement_level": engagement_level,
            "participants": list(participants),
            "assignees": assignees,
        }

    # DIMENSION 5: FLOW
    async def analyze_workflow_state(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow state and progress"""
        state = issue.get("state", "open")
        labels = [label["name"] for label in issue.get("labels", [])]

        # Determine workflow stage
        workflow_stage = "new"
        if state == "closed":
            workflow_stage = "completed"
        elif any(label in ["in-progress", "doing", "wip"] for label in labels):
            workflow_stage = "in_progress"
        elif any(label in ["review", "testing", "qa"] for label in labels):
            workflow_stage = "review"
        elif any(label in ["blocked", "waiting", "on-hold"] for label in labels):
            workflow_stage = "blocked"
        elif issue.get("assignees"):
            workflow_stage = "assigned"

        is_blocked = "blocked" in labels or "waiting" in labels

        # Estimate completion percentage
        completion = 0
        if state == "closed":
            completion = 100
        elif workflow_stage == "review":
            completion = 75
        elif workflow_stage == "in_progress":
            completion = 50
        elif workflow_stage == "assigned":
            completion = 25

        return {
            "state": state,
            "workflow_stage": workflow_stage,
            "is_blocked": is_blocked,
            "completion_percentage": completion,
            "is_pull_request": bool(issue.get("pull_request")),
        }

    # DIMENSION 6: QUANTITATIVE
    async def analyze_metrics(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quantitative metrics and velocities"""
        from datetime import timezone

        created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        age_days = max(1, (now - created).days)

        comment_count = issue.get("comments", 0)
        comment_velocity = comment_count / age_days

        # Engagement score calculation
        reactions = issue.get("reactions", {}).get("total_count", 0)
        engagement_score = comment_count + (reactions * 2)

        # Complexity estimation based on various factors
        complexity = "low"
        if comment_count > 10 or age_days > 30:
            complexity = "high"
        elif comment_count > 5 or age_days > 14:
            complexity = "medium"

        # Time to milestone
        time_to_milestone_days = None
        if milestone := issue.get("milestone"):
            if due_on := milestone.get("due_on"):
                due_date = datetime.fromisoformat(due_on.replace("Z", "+00:00"))
                time_to_milestone_days = (due_date - now).days

        return {
            "comment_velocity": comment_velocity,
            "engagement_score": engagement_score,
            "complexity_estimate": complexity,
            "time_to_milestone_days": time_to_milestone_days,
            "age_days": age_days,
            "comment_count": comment_count,
        }

    # DIMENSION 7: CAUSAL
    async def analyze_dependencies(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze causal relationships and dependencies"""
        body = issue.get("body", "")

        # Parse common dependency patterns
        blocks = []
        blocked_by = []
        related_issues = []

        # Look for blocking patterns
        if "blocks #" in body.lower():
            # Extract issue numbers (simplified)
            import re

            blocks_matches = re.findall(r"blocks #(\d+)", body.lower())
            blocks = [int(num) for num in blocks_matches]

        if "blocked by #" in body.lower():
            import re

            blocked_matches = re.findall(r"blocked by #(\d+)", body.lower())
            blocked_by = [int(num) for num in blocked_matches]

        if "related to #" in body.lower() or "see #" in body.lower():
            import re

            related_matches = re.findall(r"(?:related to|see) #(\d+)", body.lower())
            related_issues = [int(num) for num in related_matches]

        dependency_chain_length = len(blocks) + len(blocked_by)

        return {
            "blocks": blocks,
            "blocked_by": blocked_by,
            "related_issues": related_issues,
            "dependency_chain_length": dependency_chain_length,
            "has_dependencies": dependency_chain_length > 0,
        }

    # DIMENSION 8: CONTEXTUAL
    async def analyze_project_context(self, issue: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze repository and organizational context"""
        repo_data = issue.get("repository", {})

        repository = repo_data.get("name", "unknown")
        organization = repo_data.get("owner", "unknown")

        # Determine domain based on repository name
        domain = "general"
        if "product" in repository.lower() or "pm" in repository.lower():
            domain = "product_management"
        elif "api" in repository.lower() or "backend" in repository.lower():
            domain = "engineering"
        elif "docs" in repository.lower():
            domain = "documentation"
        elif "ui" in repository.lower() or "frontend" in repository.lower():
            domain = "user_interface"

        visibility = repo_data.get("visibility", "public")

        return {
            "repository": repository,
            "organization": organization,
            "domain": domain,
            "visibility": visibility,
            "full_name": f"{organization}/{repository}",
        }

    # MAIN SPATIAL CONTEXT CREATION
    async def create_spatial_context(self, issue: Dict[str, Any]) -> SpatialContext:
        """Create full 8-dimensional spatial context for GitHub issue"""
        # Run all dimensional analyses in parallel
        dimension_results = await asyncio.gather(
            self.analyze_issue_hierarchy(issue),
            self.analyze_timeline(issue),
            self.analyze_priority_signals(issue),
            self.analyze_team_activity(issue),
            self.analyze_workflow_state(issue),
            self.analyze_metrics(issue),
            self.analyze_dependencies(issue),
            self.analyze_project_context(issue),
        )

        # Unpack results
        hierarchy, temporal, priority, collaborative, flow, quantitative, causal, contextual = (
            dimension_results
        )

        # Determine attention level based on priority and temporal urgency
        if priority["priority_level"] == "critical" or temporal["urgency"] == "high":
            attention_level = "urgent"
        elif priority["priority_level"] == "high" or temporal["activity_level"] == "active":
            attention_level = "high"
        elif temporal["activity_level"] == "stale":
            attention_level = "low"
        else:
            attention_level = "medium"

        # Determine emotional valence
        if priority["is_bug"] or flow["is_blocked"]:
            emotional_valence = "negative"
        elif priority["is_feature"]:
            emotional_valence = "positive"
        else:
            emotional_valence = "neutral"

        # Determine navigation intent
        if flow["is_blocked"]:
            navigation_intent = "investigate"
        elif priority["assigned"] and flow["workflow_stage"] == "in_progress":
            navigation_intent = "monitor"
        elif priority["priority_level"] in ["critical", "high"]:
            navigation_intent = "respond"
        else:
            navigation_intent = "explore"

        # Create spatial context
        return SpatialContext(
            territory_id="github",
            room_id=contextual["repository"],
            path_id=f"issues/{issue['number']}",
            attention_level=attention_level,
            emotional_valence=emotional_valence,
            navigation_intent=navigation_intent,
            external_system="github",
            external_id=str(issue["number"]),
            external_context={
                "hierarchy": hierarchy,
                "temporal": temporal,
                "priority": priority,
                "collaborative": collaborative,
                "flow": flow,
                "quantitative": quantitative,
                "causal": causal,
                "contextual": contextual,
            },
        )

    # HELPER METHODS FOR INTEGRATION
    async def map_issue_to_position(
        self, issue_number: str, context: Dict[str, Any]
    ) -> SpatialPosition:
        """Map GitHub issue to spatial position using MCP adapter"""
        return await self.mcp_adapter.map_to_position(issue_number, context)

    async def get_issue(self, repository: str, issue_number: int) -> Dict[str, Any]:
        """Get issue data using MCP adapter (backward compatibility).

        Issue #1042: ``repository`` may be either ``"name"`` (legacy) or
        ``"owner/name"`` (preferred). Owner is resolved via ``repo_resolver``
        if not embedded in the slug.
        """
        if "/" in repository:
            slug = repository
        else:
            from services.integrations.github.repo_resolver import (
                UnresolvedRepoError,
                resolve_repo,
            )

            try:
                resolved = await resolve_repo()
                slug = f"{resolved.owner}/{repository}"
            except UnresolvedRepoError:
                # Best effort: caller passed only repo name, no resolver path
                # available; return graceful empty result.
                return {"number": issue_number, "error": "no_owner_resolved"}
        result = await self.mcp_adapter._call_github_api(
            f"/repos/{slug}/issues/{issue_number}"
        )
        return result or {"number": issue_number}
