"""
Unit tests for Productivity Query Handler in IntentService.

Issue #518: Phase A Quick Wins - Productivity Query (Canonical Query #51)

Tests cover:
- Handler routing for productivity query actions
- Todo completion stats aggregation
- GitHub stats integration (optional)
- Graceful handling when GitHub unavailable
- Productivity summary formatting
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


class TestProductivityQueryRouting:
    """Test routing to productivity query handler"""

    @pytest.mark.asyncio
    async def test_routes_productivity_action(self, intent_service, mock_workflow):
        """Test that productivity action routes to productivity handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            context={"original_message": "what's my productivity this week"},
        )

        with patch.object(
            intent_service, "_handle_productivity_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Productivity: 5 tasks completed",
                intent_data={"category": "query", "action": "productivity"},
            )

            # #1124: productivity queries now dispatch via the action-dispatch rail —
            # _handle_query_intent's elif was removed. Route by intent.action through
            # the real rail. Factory threads (intent, workflow_id, session_id).
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

            mock_handler.assert_called_once_with(intent, mock_workflow.id, "test-session")

    @pytest.mark.asyncio
    async def test_routes_my_productivity_action(self, intent_service, mock_workflow):
        """Test that my_productivity action routes to productivity handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="my_productivity",
            context={"original_message": "show my productivity"},
        )

        with patch.object(
            intent_service, "_handle_productivity_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True, message="Metrics", intent_data={"category": "query"}
            )

            # #1124: productivity queries now dispatch via the action-dispatch rail.
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
    async def test_routes_weekly_metrics_action(self, intent_service, mock_workflow):
        """Test that weekly_metrics action routes to productivity handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="weekly_metrics",
            context={"original_message": "weekly metrics"},
        )

        with patch.object(
            intent_service, "_handle_productivity_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True, message="Metrics", intent_data={"category": "query"}
            )

            # #1124: productivity queries now dispatch via the action-dispatch rail.
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


class TestProductivityQueryHandler:
    """Test productivity query handler implementation"""

    @pytest.mark.asyncio
    async def test_returns_todo_completion_stats(self, intent_service):
        """Test handler returns todo completion statistics"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            context={"original_message": "what's my productivity"},
        )

        # Mock TodoRepository
        mock_stats = {
            "total_created": 10,
            "completed": 7,
            "active": 3,
            "completion_rate": 70.0,
        }

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_factory:
            mock_session = MagicMock()
            mock_factory.return_value.__aenter__.return_value = mock_session

            with patch("services.repositories.todo_repository.TodoRepository") as mock_repo_class:
                mock_repo = MagicMock()
                mock_repo.get_completion_stats = AsyncMock(return_value=mock_stats)
                mock_repo_class.return_value = mock_repo

                # Mock GitHub to fail gracefully
                with patch(
                    "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
                ) as mock_gh:
                    mock_gh.return_value.initialize = AsyncMock()
                    mock_gh.return_value.config_service.is_configured.return_value = False

                    # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
                    mock_gh.return_value.is_available = AsyncMock(return_value=False)
                    result = await intent_service._handle_productivity_query(
                        intent, "workflow-123", "user-456"
                    )

                    assert result.success is True
                    assert "7" in result.message  # Completed count
                    assert "10" in result.message  # Total created
                    assert "3" in result.message  # Active count
                    assert "70.0%" in result.message  # Completion rate
                    assert result.intent_data["todo_stats"] == mock_stats

    @pytest.mark.asyncio
    async def test_includes_github_stats_when_configured(self, intent_service):
        """Test handler includes GitHub stats when GitHub is configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            context={"original_message": "productivity metrics"},
        )

        mock_todo_stats = {
            "total_created": 5,
            "completed": 3,
            "active": 2,
            "completion_rate": 60.0,
        }

        # Mock closed GitHub issues
        now = datetime.now(timezone.utc)
        mock_closed_items = [
            {"number": 123, "title": "Fix bug", "closed_at": now.isoformat()},
            {
                "number": 124,
                "title": "Add feature",
                "closed_at": (now - timedelta(days=2)).isoformat(),
            },
        ]

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_factory:
            mock_session = MagicMock()
            mock_factory.return_value.__aenter__.return_value = mock_session

            with patch("services.repositories.todo_repository.TodoRepository") as mock_repo_class:
                mock_repo = MagicMock()
                mock_repo.get_completion_stats = AsyncMock(return_value=mock_todo_stats)
                mock_repo_class.return_value = mock_repo

                with patch(
                    "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
                ) as mock_gh_class:
                    mock_gh = MagicMock()
                    mock_gh.initialize = AsyncMock()
                    mock_gh.config_service.is_configured.return_value = True
                    # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
                    mock_gh.is_available = AsyncMock(return_value=True)
                    mock_gh.get_closed_issues = AsyncMock(return_value=mock_closed_items)
                    mock_gh_class.return_value = mock_gh

                    result = await intent_service._handle_productivity_query(
                        intent, "workflow-123", "user-456"
                    )

                    assert result.success is True
                    assert "GitHub" in result.message
                    assert "2" in result.message  # GitHub items closed
                    assert result.intent_data["github_stats"]["issues_closed"] == 2
                    assert result.intent_data["total_completed"] == 5  # 3 todos + 2 github

    @pytest.mark.asyncio
    async def test_handles_no_completed_items(self, intent_service):
        """Test handler provides helpful message when no items completed"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            context={"original_message": "my productivity"},
        )

        mock_stats = {"total_created": 5, "completed": 0, "active": 5, "completion_rate": 0.0}

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_factory:
            mock_session = MagicMock()
            mock_factory.return_value.__aenter__.return_value = mock_session

            with patch("services.repositories.todo_repository.TodoRepository") as mock_repo_class:
                mock_repo = MagicMock()
                mock_repo.get_completion_stats = AsyncMock(return_value=mock_stats)
                mock_repo_class.return_value = mock_repo

                with patch(
                    "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
                ) as mock_gh:
                    mock_gh.return_value.initialize = AsyncMock()
                    mock_gh.return_value.config_service.is_configured.return_value = False

                    # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
                    mock_gh.return_value.is_available = AsyncMock(return_value=False)
                    result = await intent_service._handle_productivity_query(
                        intent, "workflow-123", "user-456"
                    )

                    assert result.success is True
                    assert "No completed items" in result.message
                    assert "achievable goals" in result.message

    @pytest.mark.asyncio
    async def test_handles_github_unavailable_gracefully(self, intent_service):
        """Test handler continues gracefully when GitHub fails"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            context={"original_message": "productivity"},
        )

        mock_stats = {"total_created": 8, "completed": 6, "active": 2, "completion_rate": 75.0}

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_factory:
            mock_session = MagicMock()
            mock_factory.return_value.__aenter__.return_value = mock_session

            with patch("services.repositories.todo_repository.TodoRepository") as mock_repo_class:
                mock_repo = MagicMock()
                mock_repo.get_completion_stats = AsyncMock(return_value=mock_stats)
                mock_repo_class.return_value = mock_repo

                # Make GitHub raise an exception
                with patch(
                    "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
                ) as mock_gh:
                    mock_gh.return_value.initialize = AsyncMock(
                        side_effect=Exception("GitHub API error")
                    )

                    result = await intent_service._handle_productivity_query(
                        intent, "workflow-123", "user-456"
                    )

                    # Should still succeed with just todo stats
                    assert result.success is True
                    assert "6" in result.message  # Todo completed count
                    assert result.intent_data["github_stats"] is None

    @pytest.mark.asyncio
    async def test_provides_assessment_for_high_productivity(self, intent_service):
        """Test handler provides positive assessment for high productivity"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            context={"original_message": "how productive was I"},
        )

        mock_stats = {
            "total_created": 20,
            "completed": 18,
            "active": 2,
            "completion_rate": 90.0,
        }

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_factory:
            mock_session = MagicMock()
            mock_factory.return_value.__aenter__.return_value = mock_session

            with patch("services.repositories.todo_repository.TodoRepository") as mock_repo_class:
                mock_repo = MagicMock()
                mock_repo.get_completion_stats = AsyncMock(return_value=mock_stats)
                mock_repo_class.return_value = mock_repo

                with patch(
                    "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
                ) as mock_gh:
                    mock_gh.return_value.initialize = AsyncMock()
                    mock_gh.return_value.config_service.is_configured.return_value = False

                    # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
                    mock_gh.return_value.is_available = AsyncMock(return_value=False)
                    result = await intent_service._handle_productivity_query(
                        intent, "workflow-123", "user-456"
                    )

                    assert result.success is True
                    assert "Highly productive" in result.message or "Excellent" in result.message

    @pytest.mark.asyncio
    async def test_handles_database_error(self, intent_service):
        """Test handler returns error when database fails"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            context={"original_message": "productivity"},
        )

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_factory:
            # Make database raise an exception
            mock_factory.return_value.__aenter__.side_effect = Exception(
                "Database connection failed"
            )

            result = await intent_service._handle_productivity_query(
                intent, "workflow-123", "user-456"
            )

            assert result.success is False
            assert "analyzing productivity" in result.message
            assert result.error_type == "ProductivityQueryError"

    @pytest.mark.asyncio
    async def test_filters_github_issues_by_date(self, intent_service):
        """Test handler only counts GitHub issues closed in past 7 days"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            context={"original_message": "productivity"},
        )

        mock_todo_stats = {
            "total_created": 3,
            "completed": 2,
            "active": 1,
            "completion_rate": 66.7,
        }

        now = datetime.now(timezone.utc)
        old_date = now - timedelta(days=10)  # Too old
        recent_date = now - timedelta(days=3)  # Within 7 days

        mock_closed_items = [
            {"number": 1, "title": "Old issue", "closed_at": old_date.isoformat()},
            {"number": 2, "title": "Recent issue", "closed_at": recent_date.isoformat()},
            {"number": 3, "title": "Today issue", "closed_at": now.isoformat()},
        ]

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_factory:
            mock_session = MagicMock()
            mock_factory.return_value.__aenter__.return_value = mock_session

            with patch("services.repositories.todo_repository.TodoRepository") as mock_repo_class:
                mock_repo = MagicMock()
                mock_repo.get_completion_stats = AsyncMock(return_value=mock_todo_stats)
                mock_repo_class.return_value = mock_repo

                with patch(
                    "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
                ) as mock_gh_class:
                    mock_gh = MagicMock()
                    mock_gh.initialize = AsyncMock()
                    mock_gh.config_service.is_configured.return_value = True
                    # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
                    mock_gh.is_available = AsyncMock(return_value=True)
                    mock_gh.get_closed_issues = AsyncMock(return_value=mock_closed_items)
                    mock_gh_class.return_value = mock_gh

                    result = await intent_service._handle_productivity_query(
                        intent, "workflow-123", "user-456"
                    )

                    assert result.success is True
                    # Should only count 2 recent items, not the old one
                    assert result.intent_data["github_stats"]["issues_closed"] == 2
                    assert result.intent_data["total_completed"] == 4  # 2 todos + 2 github


class TestPreClassifierRoutingIntegration:
    """Test full routing path from pre-classifier to handlers (Issue #521)"""

    def test_productivity_query_routes_to_query_category(self):
        """Test 'what's my productivity this week' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("what's my productivity this week")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "productivity_query"
        assert result.confidence == 1.0

    def test_productivity_query_variants(self):
        """Test productivity query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "what's my productivity this week",
            "show my productivity",
            "productivity metrics",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "productivity_query", f"Wrong action for: {query}"
