"""
Unit tests for StandupWorkflowSkill

Tests the core skill functionality:
- Parameter validation
- Standup generation
- Multi-system integration
- Token estimation
- Error handling
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.integrations.mcp.skills.standup_workflow_skill import StandupWorkflowSkill


@pytest.fixture
def skill():
    """Create skill instance with mocked dependencies.

    #1289: MorningStandupWorkflow + StandupOrchestrationService + SessionPersistenceManager
    are no longer imported by the skill; patches removed accordingly.
    """
    with (
        patch("services.integrations.mcp.skills.standup_workflow_skill.GitHubDomainService"),
        patch("services.integrations.mcp.skills.standup_workflow_skill.SlackDomainService"),
        patch("services.integrations.mcp.skills.standup_workflow_skill.UserPreferenceManager"),
        patch("services.integrations.mcp.skills.standup_workflow_skill.NotionDomainService"),
    ):
        return StandupWorkflowSkill()


@pytest.fixture
def sample_standup():
    """Sample standup data"""
    return {
        "user_id": str(uuid4()),
        "generated_at": datetime.now().isoformat(),
        "generation_time_ms": 1500,
        "yesterday_accomplishments": [
            "Fixed auth bug in password change endpoint",
            "Implemented breadcrumb navigation",
        ],
        "today_priorities": [
            "Deploy #310 changes to staging",
            "Review PR #352 for code quality",
            "Plan M3 sprint kickoff",
        ],
        "blockers": [
            "Database migration for new tables pending approval",
            "Waiting on security review for RBAC changes",
        ],
        "github_activity": {
            "commits": 5,
            "prs_merged": 2,
            "issues_closed": 3,
        },
        "time_saved_minutes": 18,
    }


class TestStandupWorkflowSkillValidation:
    """Test parameter validation"""

    @pytest.mark.smoke
    def test_validate_params_requires_user_id(self, skill):
        """Missing user_id should fail validation"""
        assert not skill.validate_params({})
        assert not skill.validate_params({"other_param": "value"})

    @pytest.mark.smoke
    def test_validate_params_accepts_user_id(self, skill):
        """Valid user_id should pass validation"""
        assert skill.validate_params({"user_id": str(uuid4())})
        assert skill.validate_params({"user_id": "user-123"})


_PATCH_ASSEMBLER = (
    "services.integrations.mcp.skills.standup_workflow_skill.build_user_standup_summary"
)


class TestStandupWorkflowSkillExecution:
    """Test main skill execution"""

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_execute_success_with_defaults(self, skill, sample_standup):
        """Execution with default parameters should succeed.

        #1289: patching build_user_standup_summary (honest engine) instead of
        the old skill.workflow.generate_standup (hollow MorningStandupWorkflow).
        _summary_to_legacy_dict is also patched to return the test legacy dict
        so execution tests don't need a real StandupSummary object.
        """
        with (
            patch(_PATCH_ASSEMBLER, new=AsyncMock(return_value=MagicMock())),
            patch(
                "services.integrations.mcp.skills.standup_workflow_skill._summary_to_legacy_dict",
                return_value=sample_standup,
            ),
        ):
            result = await skill.execute({"user_id": sample_standup["user_id"]})

        assert result["success"] is True
        assert "standup" in result
        assert result["tokens_saved"] > 0

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_execute_validation_failure(self, skill):
        """Invalid parameters should return error"""
        result = await skill.execute({})

        assert result["success"] is False
        assert "message" in result

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_execute_respects_include_flags(self, skill, sample_standup):
        """Should respect include_slack, include_github, include_notion flags"""
        skill._post_to_slack = AsyncMock(return_value={"success": True})
        skill._process_github_items = AsyncMock(
            return_value={"success": True, "issues_created": 3, "issues_closed": 1}
        )
        skill._update_notion = AsyncMock(return_value={"success": True})

        with (
            patch(_PATCH_ASSEMBLER, new=AsyncMock(return_value=MagicMock())),
            patch(
                "services.integrations.mcp.skills.standup_workflow_skill._summary_to_legacy_dict",
                return_value=sample_standup,
            ),
        ):
            # Test with only Slack
            result = await skill.execute(
                {
                    "user_id": sample_standup["user_id"],
                    "include_slack": True,
                    "include_github": False,
                    "include_notion": False,
                }
            )

        assert "slack" in result["posted_to"]
        assert "github" not in result["posted_to"]
        assert "notion" not in result["posted_to"]

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_execute_returns_issue_counts(self, skill, sample_standup):
        """Should return created and closed issue counts"""
        skill._process_github_items = AsyncMock(
            return_value={"success": True, "issues_created": 5, "issues_closed": 2}
        )

        with (
            patch(_PATCH_ASSEMBLER, new=AsyncMock(return_value=MagicMock())),
            patch(
                "services.integrations.mcp.skills.standup_workflow_skill._summary_to_legacy_dict",
                return_value=sample_standup,
            ),
        ):
            result = await skill.execute(
                {"user_id": sample_standup["user_id"], "include_github": True}
            )

        assert result["issues_created"] == 5
        assert result["issues_closed"] == 2


class TestStandupFormatting:
    """Test output formatting"""

    @pytest.mark.smoke
    def test_format_standup_markdown(self, skill, sample_standup):
        """Should format standup as markdown"""
        result = skill._format_standup(sample_standup, format_type="markdown")

        assert "Daily Standup" in result["content"]
        assert "Yesterday's Accomplishments" in result["content"]
        assert "Today's Priorities" in result["content"]
        assert "Watch" in result["content"]  # #1289: renamed from "Blockers"
        assert result["format"] == "markdown"

    @pytest.mark.smoke
    def test_format_standup_plain_text(self, skill, sample_standup):
        """Should format standup as plain text"""
        result = skill._format_standup(sample_standup, format_type="plain")

        assert "DAILY STANDUP" in result["content"]
        assert result["format"] == "plain"

    @pytest.mark.smoke
    def test_format_standup_json(self, skill, sample_standup):
        """Should return standup as-is for JSON"""
        result = skill._format_standup(sample_standup, format_type="json")

        assert result == sample_standup

    @pytest.mark.smoke
    def test_format_for_slack_creates_blocks(self, skill, sample_standup):
        """Should create Slack message blocks"""
        result = skill._format_for_slack(sample_standup)

        assert "text" in result
        assert "blocks" in result
        assert len(result["blocks"]) > 0
        assert result["blocks"][0]["type"] == "header"

    @pytest.mark.smoke
    def test_list_items_formatting(self, skill):
        """Should format lists correctly"""
        items = ["Item 1", "Item 2", "Item 3"]

        markdown = skill._list_items(items)
        plain = skill._list_items_plain(items)

        assert "- Item 1" in markdown
        assert "• Item 1" in plain

    @pytest.mark.smoke
    def test_list_items_empty(self, skill):
        """Should handle empty lists"""
        assert skill._list_items([]) == "None"
        assert skill._list_items_plain([]) == "None"


class TestActionItemExtraction:
    """Test extracting action items from standup"""

    @pytest.mark.smoke
    def test_extract_action_items(self, skill, sample_standup):
        """Should extract priorities and blockers as action items"""
        items = skill._extract_action_items(sample_standup)

        assert len(items) > 0
        # Should have items from priorities
        assert any("Deploy" in item["title"] for item in items)
        # Should have items from blockers
        assert any("BLOCKER" in item["title"] for item in items)

    @pytest.mark.smoke
    def test_extract_action_items_categorization(self, skill, sample_standup):
        """Should categorize items correctly"""
        items = skill._extract_action_items(sample_standup)

        priorities = [i for i in items if i["category"] == "priority"]
        blockers = [i for i in items if i["category"] == "blocker"]

        assert len(priorities) == len(sample_standup["today_priorities"])
        assert len(blockers) == len(sample_standup["blockers"])


class TestTokenEstimation:
    """Test token usage estimation"""

    @pytest.mark.smoke
    def test_estimate_tokens_saved(self, skill):
        """Should estimate tokens saved"""
        tokens = skill.estimate_tokens_saved({"user_id": "test"})

        assert isinstance(tokens, int)
        assert tokens > 0
        # Should be significant savings
        assert tokens >= 10000

    @pytest.mark.smoke
    def test_token_savings_consistent(self, skill):
        """Token savings should be consistent across calls"""
        tokens1 = skill.estimate_tokens_saved({"user_id": "user1"})
        tokens2 = skill.estimate_tokens_saved({"user_id": "user2"})

        # Should be similar (conservative estimate)
        assert tokens1 == tokens2


class TestErrorHandling:
    """Test error handling and graceful degradation"""

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_execute_slack_failure_continues(self, skill, sample_standup):
        """Slack failure should not stop entire workflow"""
        skill._post_to_slack = AsyncMock(side_effect=Exception("Slack API error"))
        skill._process_github_items = AsyncMock(
            return_value={"success": True, "issues_created": 3, "issues_closed": 0}
        )

        with (
            patch(_PATCH_ASSEMBLER, new=AsyncMock(return_value=MagicMock())),
            patch(
                "services.integrations.mcp.skills.standup_workflow_skill._summary_to_legacy_dict",
                return_value=sample_standup,
            ),
        ):
            result = await skill.execute(
                {
                    "user_id": sample_standup["user_id"],
                    "include_slack": True,
                    "include_github": True,
                }
            )

        # Should still succeed overall
        assert result["success"] is True
        # Slack should not be in posted_to
        assert "slack" not in result["posted_to"]
        # GitHub should be in posted_to
        assert "github" in result["posted_to"]

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_on_error_handling(self, skill):
        """Error handling should return proper error response"""
        error = ValueError("Test error")
        result = await skill.on_error(error)

        assert result["success"] is False
        assert "error" in result
        assert "ValueError" in result["error"]


class TestGitHubIssueFormatting:
    """Test GitHub issue body formatting"""

    @pytest.mark.smoke
    def test_format_github_issue_body(self, skill, sample_standup):
        """Should create well-formatted GitHub issue body"""
        item = {"title": "Deploy changes to staging", "category": "priority"}

        body = skill._format_github_issue_body(item, sample_standup)

        assert "From daily standup" in body
        assert "**Item**:" in body
        assert "Deploy changes" in body
        assert "**Category**:" in body

    @pytest.mark.smoke
    def test_github_issue_includes_context(self, skill, sample_standup):
        """GitHub issue body should include standup context"""
        item = {"title": "Test item", "category": "blocker"}

        body = skill._format_github_issue_body(item, sample_standup)

        assert sample_standup["generated_at"] in body
        assert sample_standup["user_id"] in body


class TestSkillIntegration:
    """Integration-level tests"""

    @pytest.mark.smoke
    def test_skill_has_required_attributes(self, skill):
        """Skill should have required attributes"""
        assert hasattr(skill, "name")
        assert hasattr(skill, "description")
        assert skill.name == "standup"
        assert len(skill.description) > 0

    @pytest.mark.smoke
    def test_skill_methods_exist(self, skill):
        """Skill should have all required methods"""
        assert hasattr(skill, "execute")
        assert hasattr(skill, "validate_params")
        assert hasattr(skill, "estimate_tokens_saved")
        assert callable(skill.execute)
        assert callable(skill.validate_params)
