"""
Tests for SYNTHESIS category handlers in IntentService.

These tests cover content generation and summarization handlers that CREATE new artifacts
(as opposed to ANALYSIS handlers that read/analyze existing data).

Test Coverage:
- _handle_generate_content (Phase 3)
  - status_report generation
  - readme_section generation
  - issue_template generation

- _handle_summarize (Phase 3B)
  - github_issue summarization
  - commit_range summarization
  - text summarization
  - multiple output formats
  - validation and error handling

Created: 2025-10-11 (Phase 3 & 3B - GREAT-4D)
Updated: 2025-10-11 (Phase 3B - Added summarization tests)
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.shared_types import IntentCategory


@pytest.fixture
def mock_orchestration_engine():
    """Mock orchestration engine for testing."""
    from unittest.mock import Mock

    mock_engine = Mock()
    mock_engine.create_workflow_from_intent = AsyncMock()

    # Mock workflow
    mock_workflow = Mock()
    mock_workflow.id = "test-workflow-synthesis"
    mock_engine.create_workflow_from_intent.return_value = mock_workflow

    return mock_engine


@pytest.fixture
def intent_service(mock_orchestration_engine):
    """Create IntentService instance for testing."""
    return IntentService()


class TestSynthesisHandlers:
    """Test suite for SYNTHESIS category handlers."""

    # =========================================================================
    # HANDLER EXISTENCE AND VALIDATION TESTS
    # =========================================================================

    def test_generate_content_handler_exists(self, intent_service):
        """Test that _handle_generate_content handler exists and is callable."""
        assert hasattr(intent_service, "_handle_generate_content")
        assert callable(intent_service._handle_generate_content)

    @pytest.mark.asyncio
    async def test_generate_content_missing_content_type(self, intent_service):
        """Test validation when content_type parameter is missing."""
        intent = Intent(
            original_message="generate content",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                # Missing content_type
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "content_type_required"
        assert "content type" in result.message.lower() or "content_type" in result.message.lower()

    @pytest.mark.asyncio
    async def test_generate_content_unknown_content_type(self, intent_service):
        """Test validation when content_type is not supported."""
        intent = Intent(
            original_message="generate unknown type",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={"content_type": "unknown_type"},
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "unsupported_content_type"
        assert "unsupported" in result.message.lower() or "unknown" in result.message.lower()
        assert "content type" in result.message.lower() or "content_type" in result.message.lower()

    # =========================================================================
    # STATUS REPORT TESTS
    # =========================================================================

    @pytest.mark.asyncio
    async def test_generate_status_report_success(self, intent_service):
        """Test successful status report generation with repository_metrics."""

        # Mock the _handle_analyze_data method to return analysis results
        mock_analysis_result = IntentProcessingResult(
            success=True,
            message="Analysis complete",
            intent_data={
                "category": "ANALYSIS",
                "action": "analyze_data",
                "data_type": "repository_metrics",
                "metrics": {
                    "total_activity_count": 45,
                    "commits_count": 30,
                    "prs_count": 8,
                    "issues_created_count": 4,
                    "issues_closed_count": 3,
                    "activity_distribution": {
                        "commits": 66.7,
                        "prs": 17.8,
                        "issues_created": 8.9,
                        "issues_closed": 6.7,
                    },
                },
            },
            workflow_id="test_wf",
            requires_clarification=False,
        )

        with patch.object(
            intent_service, "_handle_analyze_data", return_value=mock_analysis_result
        ):
            intent = Intent(
                original_message="generate status report",
                category=IntentCategory.SYNTHESIS,
                action="generate_content",
                confidence=0.95,
                context={
                    "content_type": "status_report",
                    "repository": "test-org/test-repo",
                    "days": 7,
                    "data_type": "repository_metrics",
                },
            )

            result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

            # Should succeed
            assert result.success is True
            assert result.requires_clarification is False

            # Should contain generated content
            assert "generated_content" in result.intent_data
            content = result.intent_data["generated_content"]
            assert isinstance(content, str)
            assert len(content) > 100  # Substantial content

            # Content should be markdown with expected structure
            assert "# " in content  # Markdown header
            assert "test-org/test-repo" in content
            assert "45" in content  # Total activity
            assert "30" in content  # Commits

            # Should have proper metadata
            assert result.intent_data["content_type"] == "status_report"
            assert result.intent_data["repository"] == "test-org/test-repo"
            assert result.intent_data["days"] == 7
            assert result.intent_data["data_type"] == "repository_metrics"
            assert "content_length" in result.intent_data
            assert result.intent_data["content_length"] > 100

            # Should mention generation in message
            assert "generated" in result.message.lower() or "status" in result.message.lower()

    @pytest.mark.asyncio
    async def test_generate_status_report_activity_trends(self, intent_service):
        """Test status report generation with activity_trends data type."""

        # Mock analysis result with trends data
        mock_analysis_result = IntentProcessingResult(
            success=True,
            message="Analysis complete",
            intent_data={
                "category": "ANALYSIS",
                "action": "analyze_data",
                "data_type": "activity_trends",
                "metrics": {
                    "total_activity_count": 45,
                    "commits_count": 30,
                    "prs_count": 8,
                    "issues_created_count": 4,
                    "issues_closed_count": 3,
                },
                "trends": {
                    "most_active_type": "commits",
                    "issue_closure_rate": 75.0,
                    "commit_velocity": "4.3 commits/day",
                    "pr_activity": "8 PRs updated",
                },
                "insights": [
                    "Most active in commits (30 total)",
                    "Issue closure rate: 75.0%",
                    "Commit velocity: 4.3 commits/day",
                ],
            },
            workflow_id="test_wf",
            requires_clarification=False,
        )

        with patch.object(
            intent_service, "_handle_analyze_data", return_value=mock_analysis_result
        ):
            intent = Intent(
                original_message="generate activity trends report",
                category=IntentCategory.SYNTHESIS,
                action="generate_content",
                confidence=0.95,
                context={
                    "content_type": "status_report",
                    "repository": "test-org/test-repo",
                    "data_type": "activity_trends",
                },
            )

            result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

            # Should succeed
            assert result.success is True
            assert result.requires_clarification is False

            # Should contain trends-specific content
            content = result.intent_data["generated_content"]
            assert "trends" in content.lower() or "velocity" in content.lower()
            assert "commits" in content.lower()

            # Should have trends data type in metadata
            assert result.intent_data["data_type"] == "activity_trends"

    @pytest.mark.asyncio
    async def test_generate_status_report_contributor_stats(self, intent_service):
        """Test status report generation with contributor_stats data type."""

        # Mock analysis result with contributor data
        mock_analysis_result = IntentProcessingResult(
            success=True,
            message="Analysis complete",
            intent_data={
                "category": "ANALYSIS",
                "action": "analyze_data",
                "data_type": "contributor_stats",
                "metrics": {
                    "total_contributors": 3,
                    "commit_authors": 2,
                    "pr_authors": 2,
                    "issue_authors": 1,
                },
                "contributors": {
                    "commits": {"Alice": 20, "Bob": 10},
                    "prs": {"Alice": 5, "Charlie": 3},
                    "issues": {"Bob": 4},
                },
                "insights": [
                    "3 total contributors across all activities",
                    "Alice is most active committer (20 commits)",
                ],
            },
            workflow_id="test_wf",
            requires_clarification=False,
        )

        with patch.object(
            intent_service, "_handle_analyze_data", return_value=mock_analysis_result
        ):
            intent = Intent(
                original_message="generate contributor stats report",
                category=IntentCategory.SYNTHESIS,
                action="generate_content",
                confidence=0.95,
                context={
                    "content_type": "status_report",
                    "repository": "test-org/test-repo",
                    "data_type": "contributor_stats",
                },
            )

            result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

            # Should succeed
            assert result.success is True
            assert result.requires_clarification is False

            # Should contain contributor-specific content
            content = result.intent_data["generated_content"]
            assert "contributor" in content.lower() or "alice" in content.lower()

            # Should have contributor_stats data type in metadata
            assert result.intent_data["data_type"] == "contributor_stats"

    @pytest.mark.asyncio
    async def test_generate_status_report_no_placeholder(self, intent_service):
        """Test that status report does not contain placeholder messages."""

        # Mock successful analysis
        mock_analysis_result = IntentProcessingResult(
            success=True,
            message="Analysis complete",
            intent_data={
                "category": "ANALYSIS",
                "action": "analyze_data",
                "metrics": {
                    "total_activity_count": 10,
                    "commits_count": 5,
                    "prs_count": 3,
                    "issues_created_count": 1,
                    "issues_closed_count": 1,
                    "activity_distribution": {
                        "commits": 50.0,
                        "prs": 30.0,
                        "issues_created": 10.0,
                        "issues_closed": 10.0,
                    },
                },
            },
            workflow_id="test_wf",
            requires_clarification=False,
        )

        with patch.object(
            intent_service, "_handle_analyze_data", return_value=mock_analysis_result
        ):
            intent = Intent(
                original_message="generate status report",
                category=IntentCategory.SYNTHESIS,
                action="generate_content",
                confidence=0.95,
                context={
                    "content_type": "status_report",
                    "repository": "test-org/test-repo",
                },
            )

            result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

            # If successful, should not contain placeholder messages
            if result.success:
                content = result.intent_data.get("generated_content", "")
                message = result.message.lower()

                # Should NOT contain these phrases
                assert "implementation in progress" not in message
                assert "implementation in progress" not in content.lower()
                assert "placeholder" not in message
                assert "placeholder" not in content.lower()
                assert "handler is ready" not in message
                assert "handler ready" not in message

                # Success means requires_clarification should be False
                assert result.requires_clarification is False

    # =========================================================================
    # README SECTION TESTS
    # =========================================================================

    @pytest.mark.asyncio
    async def test_generate_readme_missing_section_type(self, intent_service):
        """Test validation when section_type is missing for readme_section."""
        intent = Intent(
            original_message="generate readme section",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "readme_section",
                # Missing section_type
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "section_type_required"
        assert "section type" in result.message.lower() or "section_type" in result.message.lower()

    @pytest.mark.asyncio
    async def test_generate_readme_unknown_section_type(self, intent_service):
        """Test validation when section_type is not supported."""
        intent = Intent(
            original_message="generate unknown readme section",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "readme_section",
                "section_type": "unknown_section",
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "unsupported_section_type"
        assert "unsupported" in result.message.lower() or "unknown" in result.message.lower()
        assert "section" in result.message.lower()

    @pytest.mark.asyncio
    async def test_generate_readme_installation_success(self, intent_service):
        """Test successful README installation section generation."""
        intent = Intent(
            original_message="generate installation section",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "readme_section",
                "section_type": "installation",
                "repository": "test-org/test-repo",
                "language": "python",
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain generated content
        assert "generated_content" in result.intent_data
        content = result.intent_data["generated_content"]
        assert isinstance(content, str)
        assert len(content) > 50  # Reasonable content length

        # Content should contain installation-related keywords
        content_lower = content.lower()
        assert "install" in content_lower or "installation" in content_lower
        assert "##" in content  # Markdown section header

        # Should have proper metadata
        assert result.intent_data["content_type"] == "readme_section"
        assert result.intent_data["section_type"] == "installation"
        assert "content_length" in result.intent_data

    @pytest.mark.asyncio
    async def test_generate_readme_usage_success(self, intent_service):
        """Test successful README usage section generation."""
        intent = Intent(
            original_message="generate usage section",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "readme_section",
                "section_type": "usage",
                "language": "python",
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain usage-related content
        content = result.intent_data["generated_content"]
        content_lower = content.lower()
        assert "usage" in content_lower or "example" in content_lower or "use" in content_lower

        # Should have proper metadata
        assert result.intent_data["section_type"] == "usage"

    @pytest.mark.asyncio
    async def test_generate_readme_no_placeholder(self, intent_service):
        """Test that README sections do not contain placeholder messages."""
        intent = Intent(
            original_message="generate contributing section",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "readme_section",
                "section_type": "contributing",
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # If successful, should not contain placeholder messages
        if result.success:
            content = result.intent_data.get("generated_content", "")
            message = result.message.lower()

            # Should NOT contain these phrases
            assert "implementation in progress" not in message
            assert "implementation in progress" not in content.lower()
            assert "placeholder" not in message
            assert "placeholder" not in content.lower()
            assert "handler is ready" not in message
            assert "handler ready" not in message

            # Success means requires_clarification should be False
            assert result.requires_clarification is False

    # =========================================================================
    # ISSUE TEMPLATE TESTS
    # =========================================================================

    @pytest.mark.asyncio
    async def test_generate_issue_template_missing_template_type(self, intent_service):
        """Test validation when template_type is missing for issue_template."""
        intent = Intent(
            original_message="generate issue template",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "issue_template",
                # Missing template_type
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "template_type_required"
        assert (
            "template type" in result.message.lower() or "template_type" in result.message.lower()
        )

    @pytest.mark.asyncio
    async def test_generate_issue_template_unknown_template_type(self, intent_service):
        """Test validation when template_type is not supported."""
        intent = Intent(
            original_message="generate unknown issue template",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "issue_template",
                "template_type": "unknown_template",
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should fail validation
        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "unsupported_template_type"
        assert "unsupported" in result.message.lower() or "unknown" in result.message.lower()
        assert "template" in result.message.lower()

    @pytest.mark.asyncio
    async def test_generate_issue_template_bug_report_success(self, intent_service):
        """Test successful bug report issue template generation."""
        intent = Intent(
            original_message="generate bug report template",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "issue_template",
                "template_type": "bug_report",
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain generated content
        assert "generated_content" in result.intent_data
        content = result.intent_data["generated_content"]
        assert isinstance(content, str)
        assert len(content) > 50  # Reasonable content length

        # Content should be YAML + markdown format
        assert "---" in content  # YAML frontmatter markers
        assert "name:" in content.lower()  # YAML field
        assert "##" in content or "#" in content  # Markdown headers

        # Should contain bug-report specific content
        content_lower = content.lower()
        assert "bug" in content_lower or "error" in content_lower or "issue" in content_lower

        # Should have proper metadata
        assert result.intent_data["content_type"] == "issue_template"
        assert result.intent_data["template_type"] == "bug_report"
        assert "metadata" in result.intent_data
        assert "filename" in result.intent_data["metadata"]

    @pytest.mark.asyncio
    async def test_generate_issue_template_feature_request_success(self, intent_service):
        """Test successful feature request issue template generation."""
        intent = Intent(
            original_message="generate feature request template",
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            confidence=0.95,
            context={
                "content_type": "issue_template",
                "template_type": "feature_request",
            },
        )

        result = await intent_service._handle_generate_content(intent, workflow_id="test_wf")

        # Should succeed
        assert result.success is True
        assert result.requires_clarification is False

        # Should contain feature-request specific content
        content = result.intent_data["generated_content"]
        content_lower = content.lower()
        assert "feature" in content_lower or "enhancement" in content_lower

        # Should have YAML structure
        assert "---" in content
        assert "name:" in content.lower()

        # Should have proper metadata
        assert result.intent_data["template_type"] == "feature_request"
        assert "filename" in result.intent_data["metadata"]

    # =========================================================================
    # SUMMARIZATION TESTS (Phase 3B)
    # =========================================================================

    def test_summarize_handler_exists(self, intent_service):
        """Test that _handle_summarize handler exists and is not a placeholder."""
        assert hasattr(intent_service, "_handle_summarize")
        assert callable(intent_service._handle_summarize)

    @pytest.mark.asyncio
    async def test_summarize_missing_source_type(self, intent_service):
        """Test error handling when source_type is missing."""
        intent = Intent(
            original_message="summarize something",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={},  # No source_type
        )

        result = await intent_service._handle_summarize(intent, "test_wf")

        assert result.success is False
        assert result.requires_clarification is True
        assert result.clarification_type == "source_type_required"
        assert "source type not specified" in result.message.lower()

    @pytest.mark.asyncio
    async def test_summarize_unknown_source_type(self, intent_service):
        """Test error handling for unsupported source type."""
        intent = Intent(
            original_message="summarize this",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={"source_type": "invalid_type"},  # Unsupported
        )

        result = await intent_service._handle_summarize(intent, "test_wf")

        assert result.success is False
        assert result.error_type == "ValidationError"
        assert "unknown source type" in result.message.lower()
        assert "github_issue" in result.message  # Should list valid types

    @pytest.mark.asyncio
    async def test_summarize_github_issue_success(self, intent_service):
        """Test successful GitHub issue summarization."""
        import json

        # Mock GitHubDomainService
        mock_issue = {
            "number": 123,
            "title": "Test Issue - API Performance Problems",
            "body": "This is a test issue body with enough content to create a meaningful summary. The API response times have increased significantly.",
            "state": "open",
            "user": {"login": "testuser"},
            "created_at": "2025-10-01T10:00:00Z",
            "comments": [
                {
                    "user": {"login": "commenter1"},
                    "body": "This is a test comment with some discussion about the issue. We need to investigate the database queries.",
                    "created_at": "2025-10-02T10:00:00Z",
                }
            ],
        }

        # #1187: _fetch_issue_content now fetches via GitHubIntegrationRouter
        # (router resolves repo internally, #1042) and gates on is_configured.
        mock_router = MagicMock()
        mock_router.initialize = AsyncMock(return_value=None)
        mock_router.config_service.is_configured.return_value = True
        mock_router.get_issue = AsyncMock(return_value=mock_issue)

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=mock_router,
        ):
            # Mock LLM client
            mock_llm_response = {
                "title": "Test Issue Summary",
                "document_type": "GitHub Issue",
                "key_findings": [
                    "Issue discusses API performance problems",
                    "User testuser reported the issue",
                    "One comment provides additional context about database queries",
                ],
                "sections": [],
            }

            mock_llm_client = MagicMock()
            mock_llm_client.complete = AsyncMock(return_value=json.dumps(mock_llm_response))
            intent_service.llm_client = mock_llm_client

            # Test intent
            intent = Intent(
                original_message="summarize issue #123",
                category=IntentCategory.SYNTHESIS,
                action="summarize",
                confidence=0.9,
                context={
                    "source_type": "github_issue",
                    "repository": "owner/repo",
                    "issue_number": 123,
                },
            )

            result = await intent_service._handle_summarize(intent, "test_wf")

            # Verify success
            assert result.success is True
            assert result.requires_clarification is False

            # Verify summary content
            assert "summary" in result.intent_data
            assert len(result.intent_data["summary"]) > 0
            assert (
                "test issue" in result.intent_data["summary"].lower()
                or "api" in result.intent_data["summary"].lower()
            )

            # Verify metadata
            assert result.intent_data["source_type"] == "github_issue"
            assert result.intent_data["source_metadata"]["issue_number"] == 123
            assert result.intent_data["compression_ratio"] < 1.0  # Summary is shorter

    @pytest.mark.asyncio
    async def test_summarize_commit_range_success(self, intent_service):
        """Test successful commit range summarization."""
        import json

        # Mock Phase 2C handler response
        mock_commit_result = IntentProcessingResult(
            success=True,
            message="Analyzed 5 commits",
            intent_data={
                "category": "analysis",
                "action": "analyze_commits",
                "commit_count": 5,
                "recent_messages": [
                    "feat(api): add user endpoint",
                    "fix(auth): resolve token issue",
                    "docs: update readme",
                    "feat(ui): add dark mode",
                    "chore: update dependencies",
                ],
                "authors": {"alice": 3, "bob": 2},
            },
            workflow_id="test_wf",
        )

        with patch.object(
            intent_service, "_handle_analyze_commits", return_value=mock_commit_result
        ):
            # Mock LLM client
            mock_llm_response = {
                "title": "Commit Summary: owner/repo",
                "document_type": "Commit Range",
                "key_findings": [
                    "5 commits in last 7 days",
                    "2 new features added",
                    "1 bug fix implemented",
                    "Primary contributors: alice (3), bob (2)",
                ],
                "sections": [],
            }

            mock_llm_client = MagicMock()
            mock_llm_client.complete = AsyncMock(return_value=json.dumps(mock_llm_response))
            intent_service.llm_client = mock_llm_client

            # Test intent
            intent = Intent(
                original_message="summarize commits from last week",
                category=IntentCategory.SYNTHESIS,
                action="summarize",
                confidence=0.9,
                context={"source_type": "commit_range", "repository": "owner/repo", "days": 7},
            )

            result = await intent_service._handle_summarize(intent, "test_wf")

            # Verify success
            assert result.success is True
            assert result.requires_clarification is False

            # Verify summary
            assert "summary" in result.intent_data
            assert (
                "5 commits" in result.intent_data["summary"].lower()
                or "commit" in result.intent_data["summary"].lower()
            )

            # Verify metadata
            assert result.intent_data["source_type"] == "commit_range"
            assert result.intent_data["source_metadata"]["commit_count"] == 5

    @pytest.mark.asyncio
    async def test_summarize_text_success(self, intent_service):
        """Test successful text summarization."""
        import json

        # Mock LLM client
        mock_llm_response = {
            "title": "Project Requirements",
            "document_type": "Specification",
            "key_findings": [
                "Project aims to build task management system",
                "Target launch: Q1 2026",
                "Budget: $500K",
                "Team: 8 people",
            ],
            "sections": [],
        }

        mock_llm_client = MagicMock()
        mock_llm_client.complete = AsyncMock(return_value=json.dumps(mock_llm_response))
        intent_service.llm_client = mock_llm_client

        # Test intent
        long_text = (
            """
        This is a project requirements document for building an AI-powered task management system.
        The project is scheduled for launch in Q1 2026 with a total budget of $500,000.
        The team consists of 5 developers, 2 designers, and 1 project manager.
        The system must support 10,000+ concurrent users with 99.9% uptime SLA.
        """
            * 10
        )  # Make it longer

        intent = Intent(
            original_message="summarize this document",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={
                "source_type": "text",
                "content": long_text,
                "title": "Project Requirements",
                "document_type": "Specification",
            },
        )

        result = await intent_service._handle_summarize(intent, "test_wf")

        # Verify success
        assert result.success is True
        assert result.requires_clarification is False

        # Verify summary
        assert "summary" in result.intent_data
        assert len(result.intent_data["summary"]) > 0
        assert len(result.intent_data["summary"]) < len(long_text)

        # Verify compression
        assert result.intent_data["compression_ratio"] < 1.0

    @pytest.mark.asyncio
    async def test_summarize_different_formats(self, intent_service):
        """Test different output formats (bullet_points, paragraph, executive_summary)."""
        import json

        # Mock LLM response
        mock_llm_response = {
            "title": "Test Document",
            "document_type": "Test",
            "key_findings": ["Finding 1", "Finding 2", "Finding 3"],
            "sections": [],
        }

        mock_llm_client = MagicMock()
        mock_llm_client.complete = AsyncMock(return_value=json.dumps(mock_llm_response))
        intent_service.llm_client = mock_llm_client

        test_content = "This is test content. " * 50  # Make it long enough

        # Test bullet_points format
        intent_bullets = Intent(
            original_message="summarize",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={"source_type": "text", "content": test_content, "format": "bullet_points"},
        )

        result_bullets = await intent_service._handle_summarize(intent_bullets, "test_wf")
        assert result_bullets.success is True
        assert result_bullets.intent_data["summary_format"] == "bullet_points"
        assert "- " in result_bullets.intent_data["summary"]  # Has bullet points

        # Test paragraph format
        intent_para = Intent(
            original_message="summarize",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={"source_type": "text", "content": test_content, "format": "paragraph"},
        )

        result_para = await intent_service._handle_summarize(intent_para, "test_wf")
        assert result_para.success is True
        assert result_para.intent_data["summary_format"] == "paragraph"

        # Test executive_summary format
        intent_exec = Intent(
            original_message="summarize",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={"source_type": "text", "content": test_content, "format": "executive_summary"},
        )

        result_exec = await intent_service._handle_summarize(intent_exec, "test_wf")
        assert result_exec.success is True
        assert result_exec.intent_data["summary_format"] == "executive_summary"

    @pytest.mark.asyncio
    async def test_summarize_empty_content(self, intent_service):
        """Test error handling for empty or too-short content."""
        # Test empty content
        intent_empty = Intent(
            original_message="summarize",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={"source_type": "text", "content": ""},
        )

        result_empty = await intent_service._handle_summarize(intent_empty, "test_wf")
        assert result_empty.success is False
        assert result_empty.error_type == "ValidationError"

        # Test too-short content
        intent_short = Intent(
            original_message="summarize",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={"source_type": "text", "content": "Too short"},  # Less than 50 characters
        )

        result_short = await intent_service._handle_summarize(intent_short, "test_wf")
        assert result_short.success is False
        assert "too short" in result_short.message.lower()

    @pytest.mark.asyncio
    async def test_summarize_no_placeholder(self, intent_service):
        """Test that summarization does not contain placeholder messages."""
        import json

        # Mock LLM response
        mock_llm_response = {
            "title": "Test Summary",
            "document_type": "Test",
            "key_findings": ["Test finding 1", "Test finding 2"],
            "sections": [],
        }

        mock_llm_client = MagicMock()
        mock_llm_client.complete = AsyncMock(return_value=json.dumps(mock_llm_response))
        intent_service.llm_client = mock_llm_client

        intent = Intent(
            original_message="summarize text",
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            confidence=0.9,
            context={
                "source_type": "text",
                "content": "This is a test document with enough content to summarize. " * 10,
            },
        )

        result = await intent_service._handle_summarize(intent, "test_wf")

        # If successful, should not contain placeholder messages
        if result.success:
            summary = result.intent_data.get("summary", "")
            message = result.message.lower()

            # Should NOT contain these phrases
            assert "implementation in progress" not in message
            assert "implementation in progress" not in summary.lower()
            assert "placeholder" not in message
            assert "placeholder" not in summary.lower()
            assert "handler is ready" not in message
            assert "handler ready" not in message
            assert "summarization ready" not in message

            # Success means requires_clarification should be False
            assert result.requires_clarification is False
