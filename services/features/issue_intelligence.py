"""
Issue Intelligence Canonical Query Extension - Core Implementation
Built on canonical handlers and GitHub integration infrastructure

Created: 2025-08-23 by Claude Code Agent - Parallel Deployment Plan
Extends existing CanonicalHandlers with GitHub issue intelligence
Performance target: <150ms enhancement, preserves original response structure
"""

import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory
from services.utils.text_sanitation import display_title


@dataclass
class IssueIntelligenceContext:
    """Context object containing GitHub issue intelligence data"""

    user_id: str
    priority_level: str
    priority_issues: List[Dict[str, Any]] = field(default_factory=list)
    open_issues_count: int = 0
    closed_issues_count: int = 0
    assignee_context: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class IssueIntelligenceResult:
    """Result object containing enhanced canonical response with issue intelligence"""

    original_response: Dict[str, Any]
    enhanced_message: str
    issue_intelligence: Dict[str, Any]
    context_source: str = "github_integration"
    enhancement_time_ms: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)


class IssueIntelligenceCanonicalQueryEngine:
    """
    Issue Intelligence Canonical Query Engine

    Enhances existing CanonicalHandlers with GitHub issue intelligence
    while preserving original response structure and behavior.

    Architecture:
    - Delegates to existing CanonicalHandlers for base responses
    - Enhances responses with GitHub issue context
    - Maintains full compatibility with canonical query patterns
    """

    def __init__(
        self,
        github_integration: Any,
        canonical_handlers: CanonicalHandlers,
        session_manager: Any,
        user_id: str = None,  # Issue #909: No hardcoded default
    ):
        """Initialize with required dependencies"""
        self.github_integration = github_integration
        self.canonical_handlers = canonical_handlers
        self.session_manager = session_manager
        self.user_id = user_id

    async def enhance_canonical_query(
        self, intent: Intent, session_id: str
    ) -> IssueIntelligenceResult:
        """
        Enhance canonical query responses with GitHub issue intelligence

        Args:
            intent: Intent object from canonical query
            session_id: Session identifier

        Returns:
            IssueIntelligenceResult with enhanced response and intelligence data
        """
        start_time = time.time()

        # Step 1: Get original canonical response (delegate to existing handlers)
        original_response = await self.canonical_handlers.handle(intent, session_id)

        # Step 2: Gather issue intelligence based on query category
        issue_intelligence = await self._gather_issue_intelligence(intent)

        # Step 3: Enhance the message with issue context
        enhanced_message = await self._enhance_message_with_issues(
            original_response["message"], issue_intelligence, intent
        )

        # Step 4: Calculate performance metrics
        enhancement_time_ms = int((time.time() - start_time) * 1000)

        return IssueIntelligenceResult(
            original_response=original_response,
            enhanced_message=enhanced_message,
            issue_intelligence=issue_intelligence,
            context_source="github_integration",
            enhancement_time_ms=enhancement_time_ms,
        )

    async def create_issue_intelligence_context(
        self, priority_level: str = "top"
    ) -> IssueIntelligenceContext:
        """
        Create issue intelligence context for priority-based queries

        Args:
            priority_level: Priority level filter ("top", "high", "all")

        Returns:
            IssueIntelligenceContext with relevant issue data
        """
        # Get priority-related issues from GitHub
        priority_issues = await self.github_integration.get_issues_by_priority()

        # Calculate issue metrics
        open_count = len([issue for issue in priority_issues if issue.get("state") == "open"])
        closed_count = len([issue for issue in priority_issues if issue.get("state") == "closed"])

        # Extract assignee context
        assignee_context = {}
        for issue in priority_issues:
            if issue.get("assignee") and issue["assignee"].get("login"):
                login = issue["assignee"]["login"]
                if login not in assignee_context:
                    assignee_context[login] = []
                assignee_context[login].append({"number": issue["number"], "title": issue["title"]})

        return IssueIntelligenceContext(
            user_id=self.user_id,
            priority_level=priority_level,
            priority_issues=priority_issues,
            open_issues_count=open_count,
            closed_issues_count=closed_count,
            assignee_context=assignee_context,
        )

    async def _gather_issue_intelligence(self, intent: Intent) -> Dict[str, Any]:
        """Gather relevant GitHub issue intelligence based on intent category"""

        intelligence = {}

        try:
            if intent.category == IntentCategory.PRIORITY:
                # For priority queries, get recent issues and counts
                recent_issues = await self.github_integration.get_recent_issues()
                intelligence["recent_issues"] = recent_issues
                intelligence["open_issues_count"] = len(
                    [i for i in recent_issues if i.get("state") == "open"]
                )
                intelligence["closed_issues_count"] = len(
                    [i for i in recent_issues if i.get("state") == "closed"]
                )

            elif intent.category == IntentCategory.GUIDANCE:
                # For guidance queries, get development context
                dev_context = await self.github_integration.get_development_context()
                intelligence.update(dev_context)

            elif intent.category == IntentCategory.STATUS:
                # For status queries, get project-related issues
                project_issues = await self.github_integration.get_recent_issues()
                intelligence["project_issues"] = project_issues
                intelligence["active_issues"] = [
                    i for i in project_issues if i.get("state") == "open"
                ]

            else:
                # Default intelligence for other categories
                recent_issues = await self.github_integration.get_recent_issues()
                intelligence["recent_issues"] = recent_issues[:3]  # Limit to top 3

        except Exception as e:
            # Graceful degradation - don't break canonical queries
            intelligence["error"] = f"Issue intelligence temporarily unavailable: {str(e)}"
            intelligence["fallback_mode"] = True

        return intelligence

    async def _enhance_message_with_issues(
        self, original_message: str, issue_intelligence: Dict[str, Any], intent: Intent
    ) -> str:
        """Enhance original message with issue intelligence context"""

        if issue_intelligence.get("fallback_mode"):
            # Don't modify message if intelligence failed
            return original_message

        enhanced_message = original_message

        # Add issue context based on intent category
        if intent.category == IntentCategory.PRIORITY and "recent_issues" in issue_intelligence:
            recent_issues = issue_intelligence["recent_issues"]
            if recent_issues:
                enhanced_message += "\n\n**Recent GitHub Activity:**"
                for issue in recent_issues[:2]:  # Top 2 issues
                    state_emoji = "🔴" if issue.get("state") == "open" else "✅"
                    # #1628: degenerate GitHub titles never render verbatim
                    title = display_title(
                        issue.get("title"), f"(untitled issue #{issue['number']})"
                    )
                    enhanced_message += f"\n{state_emoji} #{issue['number']}: {title}"

                open_count = issue_intelligence.get("open_issues_count", 0)
                if open_count > 0:
                    enhanced_message += f"\n\n*{open_count} open issues need attention*"

        elif intent.category == IntentCategory.GUIDANCE and any(
            key in issue_intelligence for key in ["active_prs", "pending_reviews"]
        ):
            enhanced_message += "\n\n**Development Context:**"
            if "active_prs" in issue_intelligence:
                enhanced_message += f"\n• {issue_intelligence['active_prs']} active PRs"
            if "pending_reviews" in issue_intelligence:
                enhanced_message += f"\n• {issue_intelligence['pending_reviews']} pending reviews"
            if "recent_commits" in issue_intelligence:
                enhanced_message += f"\n• {issue_intelligence['recent_commits']} recent commits"

        return enhanced_message
