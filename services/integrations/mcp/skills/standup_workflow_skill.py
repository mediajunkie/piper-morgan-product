"""
StandupWorkflowSkill - Complete standup workflow as single MCP skill

Consolidates 5+ standup-related issues into one efficient skill:
- MVP-STAND-FTUX: Standup Experience Excellence
- MVP-STAND-INTERACTIVE: Interactive Standup Assistant
- MVP-STAND-MODEL: Sprint Model & Team Coordination
- MVP-STAND-MODES-UI: Advanced Multi-Modal UI Controls
- MVP-STAND-SLACK-INTERACT: Interactive Slack Standup Features

Token reduction: 90%+ vs passing full context
Execution time: <2 seconds
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID

from services.domain.github_domain_service import GitHubDomainService
from services.domain.notion_domain_service import NotionDomainService
from services.domain.slack_domain_service import SlackDomainService
from services.domain.user_preference_manager import UserPreferenceManager
from services.integrations.mcp.skills.base_skill import BaseSkill
from services.standup.assembler import build_user_standup_summary


def _summary_to_legacy_dict(summary) -> dict:
    """Adapter: StandupSummary → legacy dict shape consumed by _format_* formatters (#1289).

    The formatters read keys: yesterday_accomplishments, today_priorities, blockers,
    generated_at. StandupSummary has .yesterday / .today / .watch (lists of StandupItem
    with .display + .meta). The legacy "blockers" key maps to the Watch slot — callers
    that need the honest label already read from the formatted output which says "Watch".
    """

    def lines(items):
        return [f"{it.display}{(' — ' + it.meta) if it.meta else ''}" for it in items]

    return {
        "yesterday_accomplishments": lines(summary.yesterday),
        "today_priorities": lines(summary.today),
        "blockers": lines(summary.watch),  # legacy key; Watch is the honest source
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


class _WorkflowShim:
    """Minimal shim replacing MorningStandupWorkflow (#1289).

    The preference-reading helpers (_get_user_slack_workspace etc.) previously
    read through ``self.workflow.preference_manager``. Rather than re-plumbing
    three helpers, we keep the same attribute path via this thin shim.
    """

    def __init__(self, preference_manager):
        self.preference_manager = preference_manager


class StandupWorkflowSkill(BaseSkill):
    """
    Complete standup workflow in single MCP skill

    Handles:
    1. Standup generation from persistent context
    2. Multi-system updates (Slack, GitHub, Notion)
    3. Interactive refinement via chat
    4. Token-efficient processing

    Usage:
        skill = StandupWorkflowSkill()
        result = await skill.execute({
            'user_id': 'user-123',
            'include_slack': True,
            'include_github': True,
            'include_notion': True,
            'format': 'markdown'
        })
    """

    name = "standup"
    description = "Generate and distribute standup across Slack, GitHub, and Notion"

    def __init__(self):
        """Initialize skill with domain services.

        #1289: Replaced MorningStandupWorkflow (fabricating /generate path) with the
        honest engine (build_user_standup_summary from services.standup.assembler).
        ``self.workflow`` is retained as a thin shim holding a ``UserPreferenceManager``
        so the preference-reading helpers (_get_user_slack_workspace, _get_user_github_repo,
        _get_user_notion_database) continue to work without an adapter layer.
        """
        self.workflow = _WorkflowShim(UserPreferenceManager())
        self.github_service = GitHubDomainService()
        self.slack_service = SlackDomainService()
        self._notion_service = NotionDomainService()

    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute standup workflow with multi-system updates

        Args:
            params: {
                'user_id': str | UUID (required),
                'include_slack': bool (default True),
                'include_github': bool (default True),
                'include_notion': bool (default True),
                'format': str 'markdown'|'json'|'plain' (default 'markdown'),
                'interactive': bool (allow refinement via chat, default False),
                'post_now': bool (post immediately or draft, default True),
            }

        Returns:
            {
                'success': bool,
                'message': str,
                'standup': dict (generated standup content),
                'posted_to': list (systems where posted),
                'issues_created': int,
                'issues_closed': int,
                'tokens_saved': int,
                'execution_time_ms': int,
            }
        """
        try:
            # Validate parameters
            if not self.validate_params(params):
                raise ValueError("Invalid parameters: user_id is required")

            user_id = params.get("user_id")
            if isinstance(user_id, str):
                try:
                    user_id = UUID(user_id)
                except ValueError:
                    pass

            # Extract options
            include_slack = params.get("include_slack", True)
            include_github = params.get("include_github", True)
            include_notion = params.get("include_notion", True)
            output_format = params.get("format", "markdown")
            post_now = params.get("post_now", True)

            # Step 1: Generate standup from honest engine (#1289)
            summary = await build_user_standup_summary(str(user_id))
            standup = _summary_to_legacy_dict(summary)

            # Step 2: Format for requested output type
            formatted_standup = self._format_standup(standup, output_format)

            # Step 3: Multi-system updates
            posted_to = []
            issues_created = 0
            issues_closed = 0

            if include_slack and post_now:
                try:
                    slack_result = await self._post_to_slack(
                        user_id=str(user_id),
                        standup=formatted_standup,
                    )
                    if slack_result.get("success"):
                        posted_to.append("slack")
                except Exception as e:
                    # Log but don't fail entire operation
                    print(f"Slack posting failed: {e}")

            if include_github and post_now:
                try:
                    github_result = await self._process_github_items(
                        user_id=str(user_id),
                        standup=standup,
                    )
                    if github_result.get("success"):
                        posted_to.append("github")
                        issues_created = github_result.get("issues_created", 0)
                        issues_closed = github_result.get("issues_closed", 0)
                except Exception as e:
                    # Log but don't fail entire operation
                    print(f"GitHub processing failed: {e}")

            if include_notion and post_now:
                try:
                    notion_result = await self._update_notion(
                        user_id=str(user_id),
                        standup=formatted_standup,
                    )
                    if notion_result.get("success"):
                        posted_to.append("notion")
                except Exception as e:
                    # Log but don't fail entire operation
                    print(f"Notion update failed: {e}")

            # Step 4: Calculate token savings
            tokens_saved = self.estimate_tokens_saved(params)

            return {
                "success": True,
                "message": f"Standup generated and posted to {len(posted_to)} system(s)",
                "standup": formatted_standup,
                "posted_to": posted_to,
                "issues_created": issues_created,
                "issues_closed": issues_closed,
                "tokens_saved": tokens_saved,
                "execution_time_ms": 0,  # #1289: honest engine has no timing field
            }

        except Exception as e:
            return await self.on_error(e)

    async def _post_to_slack(self, user_id: str, standup: Dict[str, Any]) -> Dict[str, Any]:
        """
        Post formatted standup to Slack

        Args:
            user_id: User ID for Slack workspace lookup
            standup: Formatted standup content

        Returns:
            {
                'success': bool,
                'channel': str,
                'timestamp': str,
                'message': str,
            }
        """
        try:
            # Get Slack workspace for user
            slack_workspace = await self._get_user_slack_workspace(user_id)
            if not slack_workspace:
                return {
                    "success": False,
                    "message": "No Slack workspace configured for user",
                }

            # Format standup for Slack with rich formatting
            slack_formatted = self._format_for_slack(standup)

            # Post to Slack
            result = await self.slack_service.post_message(
                channel=slack_workspace.get("default_channel", "#standups"),
                message=slack_formatted["text"],
                blocks=slack_formatted.get("blocks"),
                thread_ts=slack_formatted.get("thread_ts"),
            )

            return {
                "success": True,
                "channel": result.get("channel"),
                "timestamp": result.get("ts"),
                "message": "Posted to Slack successfully",
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _process_github_items(self, user_id: str, standup: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create GitHub issues based on standup items.

        Issue #1113 cleanup:
        - Switched ``create_issue(repo=...)`` to ``create_issue(repo_name=...)``
          to match GitHubDomainService.create_issue signature (kw fixed in #1112).
        - Removed dead close-completed-items loop. It called the nonexistent
          ``GitHubDomainService.close_issue_by_title`` and was gated by
          ``_extract_completed_items`` which always returned ``[]``. When
          standup format gains explicit completion markers, file a new
          issue with a real product driver to add closure behavior.

        Args:
            user_id: User ID for GitHub repo lookup
            standup: Standup content with action items

        Returns:
            {
                'success': bool,
                'issues_created': int,
                'issues_closed': int,  # Always 0 until close-completion feature lands
                'issues': list,
            }
        """
        try:
            issues_created = 0
            created_issues = []

            # Extract action items from standup
            action_items = self._extract_action_items(standup)

            # Get user's GitHub repo
            repo = await self._get_user_github_repo(user_id)
            if not repo:
                return {
                    "success": False,
                    "message": "No GitHub repo configured",
                }

            # Create issues for action items
            for item in action_items:
                try:
                    issue = await self.github_service.create_issue(
                        repo_name=repo,
                        title=item.get("title"),
                        body=self._format_github_issue_body(item, standup),
                        labels=["standup", item.get("category", "task")],
                    )
                    created_issues.append(issue)
                    issues_created += 1
                except Exception as e:
                    print(f"Failed to create issue for '{item}': {e}")

            return {
                "success": True,
                "issues_created": issues_created,
                "issues_closed": 0,  # Close-completion deferred per #1113 cleanup
                "issues": created_issues,
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    async def _update_notion(self, user_id: str, standup: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update Notion database with standup summary.

        Issue #1113 cleanup: NotionDomainService.create_page takes
        ``parent_id`` (the database is the parent of a page in Notion's API
        model), not ``database_id``. Also returns ``Optional[Dict]`` and
        can return None on API failure — handle that path.

        Args:
            user_id: User ID for Notion workspace lookup
            standup: Standup content to store

        Returns:
            {
                'success': bool,
                'page_id': str,
                'database_id': str,
                'message': str,
            }
        """
        try:
            # Get user's Notion workspace and database
            notion_db = await self._get_user_notion_database(user_id)
            if not notion_db:
                return {
                    "success": False,
                    "message": "No Notion database configured",
                }

            # Build properties payload for the new page
            page_data = {
                "date": standup.get("generated_at"),
                "user_id": user_id,
                "summary": standup.get("summary"),
                "accomplishments": standup.get("yesterday_accomplishments"),
                "priorities": standup.get("today_priorities"),
                "blockers": standup.get("blockers"),
                "time_saved_minutes": standup.get("time_saved_minutes"),
            }

            result = await self._notion_service.create_page(
                parent_id=notion_db,
                properties=page_data,
            )

            if result is None:
                return {
                    "success": False,
                    "message": "Notion page creation failed (API error)",
                }

            return {
                "success": True,
                "page_id": result.get("id"),
                "database_id": notion_db,
                "message": "Standup recorded in Notion",
            }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _format_standup(
        self, standup: Dict[str, Any], format_type: str = "markdown"
    ) -> Dict[str, Any]:
        """Format standup for output type"""
        if format_type == "json":
            return standup
        elif format_type == "plain":
            return self._format_as_plain_text(standup)
        else:  # markdown (default)
            return self._format_as_markdown(standup)

    def _format_for_slack(self, standup: Dict[str, Any]) -> Dict[str, Any]:
        """Format standup for Slack with rich blocks"""
        return {
            "text": self._text_version(standup),
            "blocks": [
                {
                    "type": "header",
                    "text": {"type": "plain_text", "text": "📋 Daily Standup"},
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": self._markdown_version(standup),
                    },
                },
            ],
        }

    def _format_as_markdown(self, standup: Dict[str, Any]) -> Dict[str, Any]:
        """Format standup as markdown"""
        return {
            "content": f"""# Daily Standup

## Yesterday's Accomplishments
{self._list_items(standup.get('yesterday_accomplishments', []))}

## Today's Priorities
{self._list_items(standup.get('today_priorities', []))}

## Watch
{self._list_items(standup.get('blockers', [])) or 'None'}
""",
            "format": "markdown",
        }

    def _format_as_plain_text(self, standup: Dict[str, Any]) -> Dict[str, Any]:
        """Format standup as plain text"""
        return {
            "content": f"""DAILY STANDUP

Yesterday's Accomplishments:
{self._list_items_plain(standup.get('yesterday_accomplishments', []))}

Today's Priorities:
{self._list_items_plain(standup.get('today_priorities', []))}

Watch:
{self._list_items_plain(standup.get('blockers', [])) or 'None'}
""",
            "format": "plain",
        }

    def _list_items(self, items: List[str]) -> str:
        """Convert list to markdown bullet points"""
        if not items:
            return "None"
        return "\n".join(f"- {item}" for item in items)

    def _list_items_plain(self, items: List[str]) -> str:
        """Convert list to plain text bullet points"""
        if not items:
            return "None"
        return "\n".join(f"• {item}" for item in items)

    def _text_version(self, standup: Dict[str, Any]) -> str:
        """Get plain text version for Slack text field"""
        return f"Daily Standup - {standup.get('generated_at', 'Today')}"

    def _markdown_version(self, standup: Dict[str, Any]) -> str:
        """Get markdown version for Slack blocks"""
        yesterday = self._list_items(standup.get("yesterday_accomplishments", []))
        today = self._list_items(standup.get("today_priorities", []))
        blockers = self._list_items(standup.get("blockers", [])) or "None"

        return f"""*Yesterday's Accomplishments:*
{yesterday}

*Today's Priorities:*
{today}

*Watch:*
{blockers}"""

    def _extract_action_items(self, standup: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract action items to become GitHub issues"""
        items = []
        for priority in standup.get("today_priorities", []):
            items.append({"title": priority, "category": "priority"})
        for blocker in standup.get("blockers", []):
            items.append({"title": f"BLOCKER: {blocker}", "category": "blocker"})
        return items

    # _extract_completed_items helper removed 2026-05-24 per #1113 cleanup —
    # was Pattern-073 placeholder returning [] alongside a dead call site to
    # nonexistent GitHubDomainService.close_issue_by_title. When standup format
    # gains completion markers, file a new issue with a real product driver
    # and add both the extractor and a real close method.

    def _format_github_issue_body(self, item: Dict[str, Any], standup: Dict[str, Any]) -> str:
        """Format issue body with context"""
        return f"""From daily standup

**Item**: {item.get('title')}
**Category**: {item.get('category')}
**Date**: {standup.get('generated_at')}
**User**: {standup.get('user_id')}

---
Created from standup workflow
"""

    async def _get_user_slack_workspace(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get configured Slack workspace for user (Issue #693).

        Resolves the ``slack_default_channel`` preference via
        ``UserPreferenceManager``. Returns a dict shape (matching the
        downstream consumer's ``slack_workspace.get('default_channel')``
        call) when set, or ``None`` when the user hasn't configured one.

        Returns:
            ``{"default_channel": "#channel"}`` if preference is set,
            ``None`` if unset OR if user_id isn't UUID-parseable.
        """
        parsed_user_id = self._parse_user_id_for_prefs(user_id)
        if parsed_user_id is None:
            return None
        channel = await self.workflow.preference_manager.get_slack_default_channel(parsed_user_id)
        if not channel:
            return None
        return {"default_channel": channel}

    async def _get_user_github_repo(self, user_id: str) -> Optional[str]:
        """Get configured GitHub repo for user (Issue #693).

        Delegates to the existing ``default_repo`` preference (#1042) since
        the skill needs exactly one repo to create issues against. Future
        enhancement: consume ``active_repos`` (#1050) and fan out across the
        list — out of scope for #693.

        Returns:
            ``owner/name`` string if the preference is set,
            ``None`` if unset OR if user_id isn't UUID-parseable.
        """
        parsed_user_id = self._parse_user_id_for_prefs(user_id)
        if parsed_user_id is None:
            return None
        return await self.workflow.preference_manager.get_default_repo(parsed_user_id)

    async def _get_user_notion_database(self, user_id: str) -> Optional[str]:
        """Get configured Notion database for user (Issue #693).

        Resolves the ``notion_database`` preference via
        ``UserPreferenceManager``. Returns the database ID string when set
        (the downstream consumer passes it as ``database_id`` to Notion's
        page-create call), or ``None`` when unset.

        Note: even with a configured database, the downstream ``_update_notion``
        method has additional defects tracked in separate issues —
        ``_notion_service`` is never initialized in ``__init__``. Wiring this
        gate open doesn't yet make Notion fully work; it just stops the
        short-circuit at the placeholder boundary.

        Returns:
            Notion database ID string if set, ``None`` if unset OR if
            user_id isn't UUID-parseable.
        """
        parsed_user_id = self._parse_user_id_for_prefs(user_id)
        if parsed_user_id is None:
            return None
        return await self.workflow.preference_manager.get_notion_database(parsed_user_id)

    @staticmethod
    def _parse_user_id_for_prefs(user_id: str) -> Optional[UUID]:
        """Convert a user_id string to UUID for typed-preference accessors.

        Returns None if the input isn't a parseable UUID. Helpers calling
        this should treat None as 'preference unavailable' and short-circuit
        the downstream action — same fail-graceful pattern as #1050.
        """
        if not user_id:
            return None
        try:
            return UUID(str(user_id))
        except (TypeError, ValueError):
            return None

    def validate_params(self, params: Dict[str, Any]) -> bool:
        """Validate required parameters"""
        return "user_id" in params

    def estimate_tokens_saved(self, params: Dict[str, Any]) -> int:
        """
        Estimate tokens saved by using this skill

        Assumptions:
        - Full standup context: ~20K tokens
        - Skill output: ~1K tokens
        - Savings: ~19K tokens per execution
        """
        # Return conservative estimate based on typical standup size
        return 15000  # Conservative 15K token savings
