"""
Unit tests for GitHub query handlers in IntentService.

Issue #518: Phase A Quick Wins - GitHub Cluster (Canonical Queries #41, #42)

Tests cover:
- Handler routing for GitHub query actions
- Graceful fallback when GitHub is not configured
- Shipped items result formatting (Query #41)
- Stale PRs result formatting (Query #42)
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.workflow_dispatcher import dispatch_workflow
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory


@pytest.fixture
def mock_workflow():
    """Mock workflow object"""
    workflow = MagicMock()
    workflow.id = "test-workflow-id"
    return workflow


@pytest.fixture
def intent_service():
    """Create IntentService instance for testing"""
    # Patch dependencies to avoid initialization issues
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            service = IntentService()
            return service


class TestShippedThisWeekRouting:
    """Test routing to shipped this week handler"""

    @pytest.mark.asyncio
    async def test_routes_shipped_this_week_action(self, intent_service, mock_workflow):
        """Test that shipped_this_week action routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="shipped_this_week",
            context={"original_message": "what did we ship this week"},
        )

        with patch.object(
            intent_service, "_handle_shipped_this_week", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Shipped 3 items",
                intent_data={"category": "query", "action": "shipped_this_week"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id)

    @pytest.mark.asyncio
    async def test_routes_what_shipped_action(self, intent_service, mock_workflow):
        """Test that what_shipped action also routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="what_shipped",
            context={"original_message": "show me what shipped"},
        )

        with patch.object(
            intent_service, "_handle_shipped_this_week", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Shipped 5 items",
                intent_data={"category": "query", "action": "what_shipped"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_routes_show_closed_prs_action(self, intent_service, mock_workflow):
        """Test that show_closed_prs action routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="show_closed_prs",
            context={"original_message": "show closed PRs"},
        )

        with patch.object(
            intent_service, "_handle_shipped_this_week", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Shipped 2 items",
                intent_data={"category": "query", "action": "show_closed_prs"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()


class TestStalePRsRouting:
    """Test routing to stale PRs handler"""

    @pytest.mark.asyncio
    async def test_routes_stale_prs_action(self, intent_service, mock_workflow):
        """Test that stale_prs action routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="stale_prs",
            context={"original_message": "show me stale PRs"},
        )

        with patch.object(
            intent_service, "_handle_stale_prs", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Found 4 stale PRs",
                intent_data={"category": "query", "action": "stale_prs"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id)

    @pytest.mark.asyncio
    async def test_routes_old_prs_action(self, intent_service, mock_workflow):
        """Test that old_prs action also routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="old_prs",
            context={"original_message": "show old pull requests"},
        )

        with patch.object(
            intent_service, "_handle_stale_prs", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Found 2 stale PRs",
                intent_data={"category": "query", "action": "old_prs"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_routes_show_stale_prs_action(self, intent_service, mock_workflow):
        """Test that show_stale_prs action routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="show_stale_prs",
            context={"original_message": "show stale PRs needing review"},
        )

        with patch.object(
            intent_service, "_handle_stale_prs", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Found 6 stale PRs",
                intent_data={"category": "query", "action": "show_stale_prs"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()


class TestGitHubNotConfiguredGracefulDegradation:
    """Test graceful fallback when GitHub is not configured"""

    @pytest.mark.asyncio
    async def test_shipped_returns_graceful_message_when_github_not_configured(
        self, intent_service
    ):
        """Test shipped handler returns helpful message when GitHub not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="shipped_this_week",
            context={"original_message": "what did we ship"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = False
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=False)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_shipped_this_week(intent, "workflow-id")

            assert result.success is True
            assert "GitHub isn't configured yet" in result.message
            assert "GITHUB_TOKEN" in result.message
            assert result.implemented is False

    @pytest.mark.asyncio
    async def test_stale_prs_returns_graceful_message_when_github_not_configured(
        self, intent_service
    ):
        """Test stale PRs handler returns helpful message when GitHub not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="stale_prs",
            context={"original_message": "show stale PRs"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = False
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=False)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_stale_prs(intent, "workflow-id")

            assert result.success is True
            assert "isn't connected yet" in result.message
            assert "Settings" in result.message  # #1322: OAuth connect, not env token
            assert result.implemented is False


class TestShippedThisWeekResults:
    """Test shipped this week result formatting"""

    @pytest.mark.asyncio
    async def test_formats_shipped_items_correctly(self, intent_service):
        """Test shipped items are formatted properly"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="shipped_this_week",
            context={"original_message": "what did we ship"},
        )

        now = datetime.now(timezone.utc)
        recent = (now - timedelta(days=2)).isoformat().replace("+00:00", "Z")

        mock_closed_items = [
            {
                "number": 123,
                "title": "Fix login bug",
                "html_url": "https://github.com/org/repo/issues/123",
                "closed_at": recent,
                "pull_request": None,  # Issue
            },
            {
                "number": 456,
                "title": "Add new feature",
                "html_url": "https://github.com/org/repo/pull/456",
                "closed_at": recent,
                "pull_request": {"url": "https://api.github.com/repos/org/repo/pulls/456"},  # PR
            },
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_closed_issues = AsyncMock(return_value=mock_closed_items)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_shipped_this_week(intent, "workflow-id")

            assert result.success is True
            assert "2 items" in result.message
            assert "Fix login bug" in result.message
            assert "Add new feature" in result.message
            assert result.intent_data["shipped_count"] == 2

    @pytest.mark.asyncio
    async def test_handles_no_shipped_items(self, intent_service):
        """Test handling when no items were shipped"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="shipped_this_week",
            context={"original_message": "what shipped"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_closed_issues = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_shipped_this_week(intent, "workflow-id")

            assert result.success is True
            assert "No closed issues or PRs returned from GitHub" in result.message
            assert result.intent_data["shipped_count"] == 0


class TestStalePRsResults:
    """Test stale PRs result formatting"""

    @pytest.mark.asyncio
    async def test_formats_stale_prs_correctly(self, intent_service):
        """Test stale PRs are formatted properly with age"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="stale_prs",
            context={"original_message": "show stale PRs"},
        )

        now = datetime.now(timezone.utc)
        old_date = (now - timedelta(days=14)).isoformat().replace("+00:00", "Z")

        mock_open_items = [
            {
                "number": 789,
                "title": "Refactor database layer",
                "html_url": "https://github.com/org/repo/pull/789",
                "created_at": old_date,
                "pull_request": {"url": "https://api.github.com/repos/org/repo/pulls/789"},
            },
            {
                "number": 234,
                "title": "Recent issue (not a PR)",
                "html_url": "https://github.com/org/repo/issues/234",
                "created_at": old_date,
                "pull_request": None,  # Not a PR, should be filtered out
            },
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_open_issues = AsyncMock(return_value=mock_open_items)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_stale_prs(intent, "workflow-id")

            assert result.success is True
            assert "1 found" in result.message  # Only 1 PR (not the issue)
            assert "Refactor database layer" in result.message
            assert "14 days old" in result.message
            assert result.intent_data["stale_count"] == 1

    @pytest.mark.asyncio
    async def test_handles_no_stale_prs(self, intent_service):
        """Test handling when no stale PRs found"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="stale_prs",
            context={"original_message": "show stale PRs"},
        )

        now = datetime.now(timezone.utc)
        recent = (now - timedelta(days=2)).isoformat().replace("+00:00", "Z")

        mock_open_items = [
            {
                "number": 999,
                "title": "Recent PR",
                "html_url": "https://github.com/org/repo/pull/999",
                "created_at": recent,
                "pull_request": {"url": "https://api.github.com/repos/org/repo/pulls/999"},
            },
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_open_issues = AsyncMock(return_value=mock_open_items)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_stale_prs(intent, "workflow-id")

            assert result.success is True
            assert "No stale PRs among the" in result.message
            assert result.intent_data["stale_count"] == 0


class TestGitHubHandlerErrors:
    """Test error handling in GitHub handlers"""

    @pytest.mark.asyncio
    async def test_shipped_handles_github_error(self, intent_service):
        """Test shipped handler gracefully handles GitHub API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="shipped_this_week",
            context={"original_message": "what shipped"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_closed_issues = AsyncMock(
                side_effect=Exception("API connection failed")
            )
            MockRouter.return_value = mock_router

            result = await intent_service._handle_shipped_this_week(intent, "workflow-id")

            assert result.success is False
            assert "fetching what was shipped this week" in result.message
            assert result.error is not None
            assert result.error_type == "GitHubShippedQueryError"

    @pytest.mark.asyncio
    async def test_stale_prs_handles_github_error(self, intent_service):
        """Test stale PRs handler gracefully handles GitHub API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="stale_prs",
            context={"original_message": "show stale PRs"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_open_issues = AsyncMock(side_effect=Exception("Rate limit exceeded"))
            MockRouter.return_value = mock_router

            result = await intent_service._handle_stale_prs(intent, "workflow-id")

            assert result.success is False
            assert "checking for stale pull requests" in result.message
            assert result.error is not None
            assert result.error_type == "GitHubStalePRsQueryError"


class TestReviewIssueRouting:
    """Test routing to review issue handler (Issue #519 Query #60)"""

    @pytest.mark.asyncio
    async def test_routes_review_issue_action(self, intent_service, mock_workflow):
        """Test that review_issue_query action routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="review_issue_query",
            context={"original_message": "show me issue #123"},
        )

        with patch.object(
            intent_service, "_handle_review_issue_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Issue details here",
                intent_data={"category": "query", "action": "review_issue_query"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id)

    @pytest.mark.asyncio
    async def test_routes_show_issue_action(self, intent_service, mock_workflow):
        """Test that show_issue action also routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="show_issue",
            context={"original_message": "show issue #456"},
        )

        with patch.object(
            intent_service, "_handle_review_issue_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Issue details",
                intent_data={"category": "query", "action": "show_issue"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()


class TestCloseIssueRouting:
    """Test routing to close issue handler (Issue #519 Query #45)"""

    @pytest.mark.asyncio
    async def test_routes_close_issue_action(self, intent_service, mock_workflow):
        """Test that close_issue_query action routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close issue #123"},
        )

        with patch.object(
            intent_service, "_handle_close_issue_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Issue closed",
                intent_data={"category": "query", "action": "close_issue_query"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id)

    @pytest.mark.asyncio
    async def test_routes_close_issue_variant(self, intent_service, mock_workflow):
        """Test that close_issue action variant also routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue",
            context={"original_message": "close issue 456"},
        )

        with patch.object(
            intent_service, "_handle_close_issue_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Closed",
                intent_data={"category": "query", "action": "close_issue"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()


class TestReviewIssueResults:
    """Test review issue result formatting (Issue #519 Query #60)"""

    @pytest.mark.asyncio
    async def test_formats_issue_details_correctly(self, intent_service):
        """Test issue details are formatted properly"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="review_issue_query",
            context={"original_message": "show me issue #123"},
        )

        mock_issue = {
            "number": 123,
            "title": "Fix authentication bug",
            "state": "open",
            "html_url": "https://github.com/org/repo/issues/123",
            "body": "This is a detailed description of the bug that needs to be fixed.",
            "labels": [{"name": "bug"}, {"name": "priority-high"}],
            "assignees": [{"login": "developer1"}, {"login": "developer2"}],
        }

        # #1327 cutover: connector is preferred first. Simulate "not OAuth-connected"
        # (CONNECT_REQUIRED) so the handler falls back to the native PAT path this test exercises.
        from services.mcp.consumer.connector import DegradationReason, DegradationResponse
        from services.mcp.consumer.github_adapter import GitHubIssueResult

        connect_required = GitHubIssueResult(
            degradation=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED,
                user_message="Connect GitHub to continue.",
                action_hint="/api/v1/settings/integrations/github/connect",
            )
        )
        with patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.get_issue_connector",
            new=AsyncMock(return_value=connect_required),
        ):
            with patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
            ) as MockRouter:
                mock_router = MagicMock()
                mock_router.config_service.is_configured.return_value = True
                # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
                mock_router.is_available = AsyncMock(return_value=True)
                mock_router.initialize = AsyncMock()
                mock_router.get_issue = AsyncMock(return_value=mock_issue)
                MockRouter.return_value = mock_router

                result = await intent_service._handle_review_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "Issue #123: Fix authentication bug" in result.message
            assert "open" in result.message
            assert "bug, priority-high" in result.message
            assert "developer1, developer2" in result.message
            assert result.intent_data["issue_number"] == 123

    @pytest.mark.asyncio
    async def test_handles_missing_issue_number(self, intent_service):
        """Test handling when issue number is missing from request"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="review_issue_query",
            context={"original_message": "show me the issue"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_review_issue_query(intent, "workflow-id")

            assert result.success is False
            assert "couldn't find an issue number" in result.message
            assert result.requires_clarification is True

    @pytest.mark.asyncio
    async def test_review_issue_returns_graceful_message_when_github_not_configured(
        self, intent_service
    ):
        """Test review issue handler returns helpful message when GitHub not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="review_issue_query",
            context={"original_message": "show me issue #123"},
        )

        # #1327 cutover: connector preferred → CONNECT_REQUIRED falls back to native; native is
        # also unconfigured → the "GitHub isn't configured" graceful message this test asserts.
        from services.mcp.consumer.connector import DegradationReason, DegradationResponse
        from services.mcp.consumer.github_adapter import GitHubIssueResult

        connect_required = GitHubIssueResult(
            degradation=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED,
                user_message="Connect GitHub to continue.",
                action_hint="/api/v1/settings/integrations/github/connect",
            )
        )
        with patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.get_issue_connector",
            new=AsyncMock(return_value=connect_required),
        ):
            with patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
            ) as MockRouter:
                mock_router = MagicMock()
                mock_router.config_service.is_configured.return_value = False
                # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
                mock_router.is_available = AsyncMock(return_value=False)
                mock_router.initialize = AsyncMock()
                MockRouter.return_value = mock_router

                result = await intent_service._handle_review_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "GitHub isn't configured yet" in result.message
            assert "GITHUB_TOKEN" in result.message
            assert result.implemented is False


class TestCloseIssueResults:
    """Test close issue result formatting (Issue #519 Query #45)"""

    @pytest.mark.asyncio
    async def test_formats_close_confirmation_correctly(self, intent_service):
        """Test confirmed close is formatted properly (Issue #902: needs 'yes')."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "yes, close issue #123"},
        )

        mock_updated_issue = {
            "number": 123,
            "title": "Fix authentication bug",
            "state": "closed",
            "html_url": "https://github.com/org/repo/issues/123",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.update_issue = AsyncMock(return_value=mock_updated_issue)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "Closed issue #123" in result.message
            assert "Fix authentication bug" in result.message
            assert result.intent_data["issue_number"] == 123

    @pytest.mark.asyncio
    async def test_handles_missing_issue_number_for_close(self, intent_service):
        """Test handling when issue number is missing and no fuzzy matches found"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close the issue"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            # Fuzzy search returns no matches (empty search terms after stripping "close the issue")
            mock_router.get_open_issues = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "workflow-id")

            # With fuzzy matching, no search terms extracted → asks for issue number
            assert result.requires_clarification is True
            assert (
                "issue number" in result.message.lower()
                or "couldn't find" in result.message.lower()
            )

    @pytest.mark.asyncio
    async def test_close_issue_returns_graceful_message_when_github_not_configured(
        self, intent_service
    ):
        """Test close issue handler returns helpful message when GitHub not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close issue #123"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = False
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=False)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "GitHub isn't configured yet" in result.message
            assert "GITHUB_TOKEN" in result.message
            assert result.implemented is False


class TestCommentIssueRouting:
    """Test routing to comment issue handler (Issue #519 Query #59)"""

    @pytest.mark.asyncio
    async def test_routes_comment_issue_action(self, intent_service, mock_workflow):
        """Test that comment_issue_query action routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="comment_issue_query",
            context={"original_message": "comment on issue #123 saying looks good"},
        )

        with patch.object(
            intent_service, "_handle_comment_issue_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Comment added",
                intent_data={"category": "query", "action": "comment_issue_query"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            # #1122: the rail threads session_id so the handler's slot
            # extraction can build conversation history for antecedents.
            mock_handler.assert_called_once_with(
                intent, mock_workflow.id, session_id="test-session"
            )

    @pytest.mark.asyncio
    async def test_routes_comment_issue_variant(self, intent_service, mock_workflow):
        """Test that add_comment action variant also routes to GitHub handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="add_comment",
            context={"original_message": "add comment to issue 456"},
        )

        with patch.object(
            intent_service, "_handle_comment_issue_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Comment added",
                intent_data={"category": "query", "action": "add_comment"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()


class TestCommentIssueResults:
    """Test comment issue result formatting (Issue #519 Query #59)"""

    @pytest.mark.asyncio
    async def test_formats_comment_confirmation_correctly(self, intent_service):
        """Test comment confirmation is formatted properly"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="comment_issue_query",
            context={"original_message": "comment on issue #123 saying this looks great"},
        )

        mock_comment_result = {
            "id": 987654,
            "body": "this looks great",
            "html_url": "https://github.com/org/repo/issues/123#issuecomment-987654",
        }

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.add_comment = AsyncMock(return_value=mock_comment_result)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_comment_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "Successfully added comment to issue #123" in result.message
            assert "this looks great" in result.message
            assert result.intent_data["issue_number"] == 123
            assert result.intent_data["comment_body"] == "this looks great"

    @pytest.mark.asyncio
    async def test_handles_missing_issue_number(self, intent_service):
        """Test handling when issue number is missing from comment request"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="comment_issue_query",
            context={"original_message": "comment on the issue saying good job"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_comment_issue_query(intent, "workflow-id")

            assert result.success is False
            assert "couldn't find an issue number" in result.message
            assert result.requires_clarification is True

    @pytest.mark.asyncio
    async def test_comment_issue_returns_graceful_message_when_github_not_configured(
        self, intent_service
    ):
        """Test comment issue handler returns helpful message when GitHub not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="comment_issue_query",
            context={"original_message": "comment on issue #123 saying looks good"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = False
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=False)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_comment_issue_query(intent, "workflow-id")

            assert result.success is True
            assert "GitHub isn't configured yet" in result.message
            assert "GITHUB_TOKEN" in result.message
            assert result.implemented is False


class TestGitHubIssueHandlerErrors:
    """Test error handling in GitHub issue handlers (Issue #519)"""

    @pytest.mark.asyncio
    async def test_review_issue_handles_github_error(self, intent_service):
        """Test review issue handler gracefully handles GitHub API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="review_issue_query",
            context={"original_message": "show me issue #123"},
        )

        # #1327 cutover: connector preferred → CONNECT_REQUIRED falls back to native, whose
        # get_issue raises → the graceful error path this test exercises.
        from services.mcp.consumer.connector import DegradationReason, DegradationResponse
        from services.mcp.consumer.github_adapter import GitHubIssueResult

        connect_required = GitHubIssueResult(
            degradation=DegradationResponse(
                reason=DegradationReason.CONNECT_REQUIRED,
                user_message="Connect GitHub to continue.",
                action_hint="/api/v1/settings/integrations/github/connect",
            )
        )
        with patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.get_issue_connector",
            new=AsyncMock(return_value=connect_required),
        ):
            with patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
            ) as MockRouter:
                mock_router = MagicMock()
                mock_router.config_service.is_configured.return_value = True
                # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
                mock_router.is_available = AsyncMock(return_value=True)
                mock_router.initialize = AsyncMock()
                mock_router.get_issue = AsyncMock(side_effect=Exception("Issue not found"))
                MockRouter.return_value = mock_router

                result = await intent_service._handle_review_issue_query(intent, "workflow-id")

            assert result.success is False
            assert "reviewing that issue" in result.message
            assert result.error is not None
            assert result.error_type == "GitHubReviewIssueQueryError"

    @pytest.mark.asyncio
    async def test_close_issue_handles_github_error(self, intent_service):
        """Test close issue handler gracefully handles GitHub API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="close_issue_query",
            context={"original_message": "close issue #123"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.update_issue = AsyncMock(side_effect=Exception("Permission denied"))
            MockRouter.return_value = mock_router

            result = await intent_service._handle_close_issue_query(intent, "workflow-id")

            assert result.success is False
            assert "closing that issue" in result.message
            assert result.error is not None
            assert result.error_type == "GitHubCloseIssueQueryError"


class TestPreClassifierRoutingIntegration:
    """Test full routing path from pre-classifier to handlers (Issue #521)"""

    def test_shipped_query_routes_to_query_category(self):
        """Test 'what did we ship this week' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("what did we ship this week")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "shipped_query"
        assert result.confidence == 1.0

    def test_shipped_query_variants(self):
        """Test shipped query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "what did we ship this week",
            "what shipped",
            "show me what we shipped",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "shipped_query", f"Wrong action for: {query}"

    def test_stale_prs_query_routes_to_query_category(self):
        """Test 'show me stale PRs' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("show me stale PRs")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "stale_prs_query"
        assert result.confidence == 1.0

    def test_stale_prs_query_variants(self):
        """Test stale PRs query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "show me stale PRs",
            "stale pull requests",
            "old PRs needing review",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "stale_prs_query", f"Wrong action for: {query}"

    def test_review_issue_query_routes_to_query_category(self):
        """Test 'show me issue #123' routes to QUERY category (Issue #519 Query #60)"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("show me issue #123")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "review_issue_query"
        assert result.confidence == 1.0

    def test_review_issue_query_variants(self):
        """Test review issue query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "review issue #123",
            "show me issue #456",
            "issue #789 details",
            "get issue #999",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "review_issue_query", f"Wrong action for: {query}"

    def test_close_issue_query_routes_to_query_category(self):
        """Test 'close issue #123' routes to QUERY category (Issue #519 Query #45)"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("close issue #123")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "close_issue_query"
        assert result.confidence == 1.0

    def test_close_issue_query_variants(self):
        """Test close issue query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "close issue #123",
            "close issue 456",
            "close completed issue",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "close_issue_query", f"Wrong action for: {query}"

    def test_comment_issue_query_routes_to_query_category(self):
        """Test 'comment on issue #123' routes to QUERY category (Issue #519 Query #59)"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("comment on issue #123 saying looks good")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "comment_issue_query"
        assert result.confidence == 1.0

    def test_comment_issue_query_variants(self):
        """Test comment issue query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "comment on issue #123 saying this is great",
            "add comment to issue #456 with message well done",
            "reply to issue #789 with good progress",
            "comment on #999 with nice work",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "comment_issue_query", f"Wrong action for: {query}"


class TestListPRsRouting:
    """Test routing to list PRs handler (Issue #851)"""

    @pytest.mark.asyncio
    async def test_routes_list_prs_query_action(self, intent_service, mock_workflow):
        """Test that list_prs_query action routes to list PRs handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_prs_query",
            context={"original_message": "show my PRs"},
        )

        with patch.object(
            intent_service, "_handle_list_prs_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="You have 3 open PRs",
                intent_data={"category": "query", "action": "list_prs_query"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id)

    @pytest.mark.asyncio
    async def test_routes_list_prs_action(self, intent_service, mock_workflow):
        """Test that list_prs action also routes to list PRs handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_prs",
            context={"original_message": "my pull requests"},
        )

        with patch.object(
            intent_service, "_handle_list_prs_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="You have 2 open PRs",
                intent_data={"category": "query", "action": "list_prs"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_routes_list_pull_requests_action(self, intent_service, mock_workflow):
        """Test that list_pull_requests action also routes to list PRs handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_pull_requests",
            context={"original_message": "open pull requests"},
        )

        with patch.object(
            intent_service, "_handle_list_prs_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="You have 5 open PRs",
                intent_data={"category": "query", "action": "list_pull_requests"},
            )

            # #1124/#1189: these cohorts dispatch via the action-dispatch rail —
            # their elifs were removed from _handle_query_intent. Route by
            # intent.action through the real rail (idiom: calendar query tests).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()


class TestListPRsResults:
    """Test list PRs handler response formatting (Issue #851)"""

    @pytest.mark.asyncio
    async def test_returns_pr_list_with_results(self, intent_service):
        """Test handler returns formatted PR list when PRs exist"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_prs_query",
            context={"original_message": "show my PRs"},
        )

        mock_open_items = [
            {
                "number": 100,
                "title": "Add feature X",
                "html_url": "https://github.com/test/repo/pull/100",
                "pull_request": {"url": "https://api.github.com/repos/test/repo/pulls/100"},
            },
            {
                "number": 101,
                "title": "Fix bug Y",
                "html_url": "https://github.com/test/repo/pull/101",
                "pull_request": {"url": "https://api.github.com/repos/test/repo/pulls/101"},
            },
            {
                "number": 50,
                "title": "Regular issue (not a PR)",
            },
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_open_issues = AsyncMock(return_value=mock_open_items)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_list_prs_query(intent, "test-workflow-id")

            assert result.success is True
            assert "2 open PRs" in result.message
            assert "#100" in result.message
            assert "Add feature X" in result.message
            assert "#101" in result.message
            assert "Fix bug Y" in result.message
            # Issue without pull_request field should be excluded
            assert "#50" not in result.message
            assert result.intent_data["action"] == "list_prs_query"
            assert result.intent_data["context"]["pr_count"] == 2

    @pytest.mark.asyncio
    async def test_returns_no_prs_message(self, intent_service):
        """Test handler returns appropriate message when no PRs exist"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_prs_query",
            context={"original_message": "show my PRs"},
        )

        # Return only non-PR issues
        mock_open_items = [
            {"number": 50, "title": "Regular issue"},
        ]

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = True
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=True)
            mock_router.initialize = AsyncMock()
            mock_router.get_open_issues = AsyncMock(return_value=mock_open_items)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_list_prs_query(intent, "test-workflow-id")

            assert result.success is True
            assert "don't have any open pull requests" in result.message
            assert result.intent_data["context"]["pr_count"] == 0

    @pytest.mark.asyncio
    async def test_returns_not_configured_message(self, intent_service):
        """Not OAuth-connected AND native not configured → graceful connect prompt.

        #1322 P3: the PR handler is connector-first; with no binding (CONNECT_REQUIRED) it
        falls back to native, and when native is also unconfigured it points the user at the
        OAuth connect flow (Settings → Integrations), not the deprecated GITHUB_TOKEN env path.
        """
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_prs_query",
            context={"original_message": "show my PRs"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.config_service.is_configured.return_value = False
            # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
            mock_router.is_available = AsyncMock(return_value=False)
            mock_router.initialize = AsyncMock()
            MockRouter.return_value = mock_router

            result = await intent_service._handle_list_prs_query(intent, "test-workflow-id")

            assert result.success is True
            assert "isn't connected" in result.message
            assert "Settings" in result.message

    @pytest.mark.asyncio
    async def test_handles_error_gracefully(self, intent_service):
        """Test handler returns graceful error message on failure"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="list_prs_query",
            context={"original_message": "show my PRs"},
        )

        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            MockRouter.side_effect = Exception("Connection failed")

            result = await intent_service._handle_list_prs_query(intent, "test-workflow-id")

            assert result.success is True
            assert "wasn't able to fetch" in result.message
            assert "error" in result.intent_data["context"]


class TestListPRsPreClassifierRouting:
    """Test pre-classifier pattern detection for PR listing queries (Issue #851)"""

    def test_list_prs_query_routes_to_query_category(self):
        """Test 'show my PRs' routes to QUERY category with list_prs_query action"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("show my PRs")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "list_prs_query"
        assert result.confidence == 1.0

    def test_list_prs_query_variants(self):
        """Test PR listing query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "show my PRs",
            "show my pull requests",
            "my PRs",
            "my pull requests",
            "list PRs",
            "list pull requests",
            "open pull requests",
            "open PRs",
            "PRs assigned to me",
            "pull requests assigned to me",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "list_prs_query", f"Wrong action for: {query}"

    def test_get_github_action_returns_list_prs_query(self):
        """Test _get_github_action returns list_prs_query for PR listing messages"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "show my prs",
            "my pull requests",
            "open prs",
            "list pull requests",
        ]

        for message in test_cases:
            action = PreClassifier._get_github_action(message)
            assert action == "list_prs_query", f"Wrong action for: {message}"
