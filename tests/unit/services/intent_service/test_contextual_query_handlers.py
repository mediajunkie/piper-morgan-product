"""
Unit tests for Contextual Intelligence Query Handlers (Issue #521 - Queries #29 and #30)

Tests the canonical query handlers for:
- Query #29: "What changed since X?" - activity summary with time expressions
- Query #30: "What needs my attention?" - attention items aggregation

Additionally tests full routing integration from pre-classifier to handlers.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.pre_classifier import PreClassifier
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


class TestChangesQueryRouting:
    """Test routing to changes query handler"""

    @pytest.mark.asyncio
    async def test_routes_changes_query_action(self, intent_service, mock_workflow):
        """Test that changes_query action routes to handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday"},
        )

        with patch.object(
            intent_service, "_handle_changes_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Activity summary",
                intent_data={"category": "query", "action": "changes_query"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id, "test-session")

    @pytest.mark.asyncio
    async def test_routes_what_changed_action(self, intent_service, mock_workflow):
        """Test that what_changed action also routes to handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="what_changed",
            context={"original_message": "show me what changed"},
        )

        with patch.object(
            intent_service, "_handle_changes_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Activity summary",
                intent_data={"category": "query", "action": "what_changed"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once()


class TestAttentionQueryRouting:
    """Test routing to attention query handler"""

    @pytest.mark.asyncio
    async def test_routes_attention_query_action(self, intent_service, mock_workflow):
        """Test that attention_query action routes to handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs my attention"},
        )

        with patch.object(
            intent_service, "_handle_attention_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Attention items",
                intent_data={"category": "query", "action": "attention_query"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            # Issue #849: user_id is now threaded through to _handle_attention_query
            mock_handler.assert_called_once_with(
                intent, mock_workflow.id, "test-session", user_id=None
            )

    @pytest.mark.asyncio
    async def test_routes_needs_attention_action(self, intent_service, mock_workflow):
        """Test that needs_attention action also routes to handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="needs_attention",
            context={"original_message": "show items needing attention"},
        )

        with patch.object(
            intent_service, "_handle_attention_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Attention items",
                intent_data={"category": "query", "action": "needs_attention"},
            )

            result = await intent_service._handle_query_intent(
                intent, mock_workflow, "test-session"
            )

            mock_handler.assert_called_once()


class TestChangesQueryTimeExpressionParsing:
    """Test time expression parsing in changes query"""

    @pytest.mark.asyncio
    async def test_parses_yesterday_correctly(self, intent_service):
        """Test parsing 'since yesterday' returns 1 day"""
        result = intent_service._parse_time_expression("what changed since yesterday")
        assert result == 1

    @pytest.mark.asyncio
    async def test_parses_last_week_correctly(self, intent_service):
        """Test parsing 'since last week' returns 7 days"""
        result = intent_service._parse_time_expression("show changes since last week")
        assert result == 7

    @pytest.mark.asyncio
    async def test_parses_specific_days_correctly(self, intent_service):
        """Test parsing '3 days' returns 3"""
        result = intent_service._parse_time_expression("what changed in the last 3 days")
        assert result == 3

    @pytest.mark.asyncio
    async def test_parses_month_correctly(self, intent_service):
        """Test parsing 'last month' returns 30 days"""
        result = intent_service._parse_time_expression("changes since last month")
        assert result == 30

    @pytest.mark.asyncio
    async def test_parses_hour_correctly(self, intent_service):
        """Test parsing 'last hour' returns 0 (partial day)"""
        result = intent_service._parse_time_expression("what changed in the last hour")
        assert result == 0

    @pytest.mark.asyncio
    async def test_parses_day_of_week_correctly(self, intent_service):
        """Test parsing day of week returns appropriate days"""
        # This will vary based on current day, but should return 1-7
        result = intent_service._parse_time_expression("changes since monday")
        assert 1 <= result <= 7


class TestChangesQueryResults:
    """Test changes query result formatting"""

    @pytest.mark.asyncio
    async def test_formats_todo_activity_correctly(self, intent_service):
        """Test changes query formats todo activity"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday"},
        )

        # Mock database session and todo data
        mock_todo_1 = MagicMock()
        mock_todo_1.text = "Review PR #521"
        mock_todo_1.priority = "high"
        mock_todo_1.created_at = datetime.now(timezone.utc) - timedelta(hours=2)
        mock_todo_1.updated_at = datetime.now(timezone.utc) - timedelta(hours=2)
        mock_todo_1.completed_at = None
        mock_todo_1.owner_id = "test-session"

        mock_todo_2 = MagicMock()
        mock_todo_2.text = "Write tests"
        mock_todo_2.priority = "medium"
        mock_todo_2.created_at = datetime.now(timezone.utc) - timedelta(days=2)
        mock_todo_2.updated_at = datetime.now(timezone.utc) - timedelta(hours=1)
        mock_todo_2.completed_at = datetime.now(timezone.utc) - timedelta(hours=1)
        mock_todo_2.owner_id = "test-session"

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session_instance = MagicMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)

            # Mock execute to return todos
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = [mock_todo_1, mock_todo_2]
            mock_session_instance.execute = AsyncMock(return_value=mock_result)

            mock_session.return_value = mock_session_instance

            result = await intent_service._handle_changes_query(
                intent, "workflow-id", "test-session"
            )

            assert result.success is True
            assert "Activity Summary" in result.message
            assert result.intent_data["time_range_days"] == 1
            assert result.intent_data["total_activities"] >= 0

    @pytest.mark.asyncio
    async def test_handles_no_activity(self, intent_service):
        """Test changes query handles empty activity list"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday"},
        )

        # Mock empty results
        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session_instance = MagicMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)

            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_session_instance.execute = AsyncMock(return_value=mock_result)

            mock_session.return_value = mock_session_instance

            result = await intent_service._handle_changes_query(
                intent, "workflow-id", "test-session"
            )

            assert result.success is True
            assert "No activity detected" in result.message
            assert result.intent_data["total_activities"] == 0


class TestAttentionQueryResults:
    """Test attention query result formatting"""

    @pytest.mark.asyncio
    async def test_identifies_high_priority_todos(self, intent_service):
        """Test attention query identifies high-priority todos"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs my attention"},
        )

        # Mock high-priority todo
        mock_todo = MagicMock()
        mock_todo.text = "Critical bug fix"
        mock_todo.priority = "urgent"
        mock_todo.completed = False
        mock_todo.due_date = None
        mock_todo.owner_id = "test-session"

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session_instance = MagicMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)

            # Mock execute to return high-priority todo
            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = [mock_todo]
            mock_session_instance.execute = AsyncMock(return_value=mock_result)

            mock_session.return_value = mock_session_instance

            # Mock calendar to avoid errors
            with patch(
                "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
            ) as MockAdapter:
                mock_adapter = MagicMock()
                mock_adapter.authenticate = AsyncMock(return_value=False)
                MockAdapter.return_value = mock_adapter

                result = await intent_service._handle_attention_query(
                    intent, "workflow-id", "test-session"
                )

                assert result.success is True
                assert "Critical bug fix" in result.message
                assert result.intent_data["total_attention_items"] >= 1
                assert len(result.intent_data["high_priority_todos"]) >= 1

    @pytest.mark.asyncio
    async def test_identifies_overdue_todos(self, intent_service):
        """Test attention query identifies overdue todos"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs my attention"},
        )

        # Mock overdue todo
        mock_todo = MagicMock()
        mock_todo.text = "Overdue task"
        mock_todo.priority = "medium"
        mock_todo.completed = False
        mock_todo.due_date = datetime.now(timezone.utc) - timedelta(days=3)
        mock_todo.owner_id = "test-session"

        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session_instance = MagicMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)

            # First call returns empty (high priority), second returns overdue
            mock_result_1 = MagicMock()
            mock_result_1.scalars.return_value.all.return_value = []

            mock_result_2 = MagicMock()
            mock_result_2.scalars.return_value.all.return_value = [mock_todo]

            mock_session_instance.execute = AsyncMock(
                side_effect=[mock_result_1, mock_result_2, mock_result_1]
            )

            mock_session.return_value = mock_session_instance

            # Mock calendar
            with patch(
                "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
            ) as MockAdapter:
                mock_adapter = MagicMock()
                mock_adapter.authenticate = AsyncMock(return_value=False)
                MockAdapter.return_value = mock_adapter

                result = await intent_service._handle_attention_query(
                    intent, "workflow-id", "test-session"
                )

                assert result.success is True
                assert "Overdue task" in result.message
                assert len(result.intent_data["overdue_todos"]) >= 1

    @pytest.mark.asyncio
    async def test_handles_no_attention_items(self, intent_service):
        """Test attention query handles case with no items needing attention"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs my attention"},
        )

        # Mock empty results
        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session_instance = MagicMock()
            mock_session_instance.__aenter__ = AsyncMock(return_value=mock_session_instance)
            mock_session_instance.__aexit__ = AsyncMock(return_value=None)

            mock_result = MagicMock()
            mock_result.scalars.return_value.all.return_value = []
            mock_session_instance.execute = AsyncMock(return_value=mock_result)

            mock_session.return_value = mock_session_instance

            # Mock calendar
            with patch(
                "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
            ) as MockAdapter:
                mock_adapter = MagicMock()
                mock_adapter.authenticate = AsyncMock(return_value=False)
                MockAdapter.return_value = mock_adapter

                result = await intent_service._handle_attention_query(
                    intent, "workflow-id", "test-session"
                )

                assert result.success is True
                # #1069: empty-state wording is source-transparent
                assert "I don't see anything urgent" in result.message
                assert result.intent_data["total_attention_items"] == 0


class TestContextualQueryErrorHandling:
    """Test error handling in contextual query handlers"""

    @pytest.mark.asyncio
    async def test_changes_query_handles_database_error(self, intent_service):
        """Test changes query gracefully handles database errors by continuing with empty results"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday"},
        )

        # Mock database error for all queries
        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session.side_effect = Exception("Database connection failed")

            result = await intent_service._handle_changes_query(
                intent, "workflow-id", "test-session"
            )

            # Handler gracefully degrades by logging warnings and showing no activity
            assert result.success is True
            assert "No activity detected" in result.message
            assert result.intent_data["total_activities"] == 0

    @pytest.mark.asyncio
    async def test_attention_query_handles_database_error(self, intent_service):
        """Test attention query gracefully handles database errors by continuing with empty results"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs my attention"},
        )

        # Mock database error for all queries
        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session.side_effect = Exception("Database timeout")

            # Mock calendar to avoid additional errors
            with patch(
                "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
            ) as MockAdapter:
                mock_adapter = MagicMock()
                mock_adapter.authenticate = AsyncMock(return_value=False)
                MockAdapter.return_value = mock_adapter

                result = await intent_service._handle_attention_query(
                    intent, "workflow-id", "test-session"
                )

                # Handler gracefully degrades by logging warnings and showing no items
                assert result.success is True
                # #1069: empty-state wording is source-transparent
                assert "I don't see anything urgent" in result.message
                assert result.intent_data["total_attention_items"] == 0


class TestPreClassifierRoutingIntegration:
    """Test full routing path from pre-classifier to handlers (Issue #521)"""

    def test_attention_query_routes_to_query_category(self):
        """Test 'what needs my attention' routes to QUERY not PRIORITY"""
        result = PreClassifier.pre_classify("what needs my attention")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "attention_query"
        assert result.confidence == 1.0

    def test_attention_query_variants(self):
        """Test attention query pattern variants all route correctly"""
        test_cases = [
            "what needs my attention",
            "what needs attention",
            "show me what needs my attention",
            "items that need attention",
            "attention items",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to match: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "attention_query", f"Wrong action for: {query}"

    def test_changes_query_routes_to_query_category(self):
        """Test 'what changed since yesterday' routes to QUERY"""
        result = PreClassifier.pre_classify("what changed since yesterday")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "changes_query"
        assert result.confidence == 1.0

    def test_changes_query_variants(self):
        """Test changes query pattern variants all route correctly"""
        test_cases = [
            "what changed since yesterday",
            "what's changed since last week",
            "show me changes since monday",
            "show me what changed",
            "changes since yesterday",
            "activity since yesterday",
            "updates since last week",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to match: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "changes_query", f"Wrong action for: {query}"

    def test_priority_patterns_still_work(self):
        """Test existing PRIORITY patterns are not broken"""
        priority_queries = [
            "what are my priorities",
            "what's my top priority",
            "show me my priorities",
            "what should i focus on",
            "what's most important",
        ]

        for query in priority_queries:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to match: {query}"
            assert result.category == IntentCategory.PRIORITY, f"Wrong category for: {query}"
            assert result.action == "get_top_priority", f"Wrong action for: {query}"

    def test_contextual_queries_checked_before_priority(self):
        """Verify contextual queries are checked before priority to prevent collision"""
        # This query would match PRIORITY pattern r"\bneeds.*attention\b"
        # but should be caught by CONTEXTUAL_QUERY first
        result = PreClassifier.pre_classify("what needs my attention right now")

        assert result is not None
        assert result.category == IntentCategory.QUERY, "Should be QUERY, not PRIORITY"
        assert result.action == "attention_query"

    @pytest.mark.asyncio
    async def test_full_routing_attention_query_to_handler(self, intent_service, mock_workflow):
        """Test full path: pre-classifier → QUERY intent → attention handler"""
        # Step 1: Pre-classifier routes correctly
        pre_intent = PreClassifier.pre_classify("what needs my attention")
        assert pre_intent.category == IntentCategory.QUERY
        assert pre_intent.action == "attention_query"

        # Step 2: IntentService routes to correct handler
        with patch.object(
            intent_service, "_handle_attention_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Attention items",
                intent_data={"category": "query", "action": "attention_query"},
            )

            # Use the pre-classified intent
            result = await intent_service._handle_query_intent(
                pre_intent, mock_workflow, "test-session"
            )

            # Verify handler was called
            # Issue #849: user_id is now threaded through to _handle_attention_query
            mock_handler.assert_called_once_with(
                pre_intent, mock_workflow.id, "test-session", user_id=None
            )
            assert result.success is True

    @pytest.mark.asyncio
    async def test_full_routing_changes_query_to_handler(self, intent_service, mock_workflow):
        """Test full path: pre-classifier → QUERY intent → changes handler"""
        # Step 1: Pre-classifier routes correctly
        pre_intent = PreClassifier.pre_classify("what changed since yesterday")
        assert pre_intent.category == IntentCategory.QUERY
        assert pre_intent.action == "changes_query"

        # Step 2: IntentService routes to correct handler
        with patch.object(
            intent_service, "_handle_changes_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Activity summary",
                intent_data={"category": "query", "action": "changes_query"},
            )

            # Use the pre-classified intent
            result = await intent_service._handle_query_intent(
                pre_intent, mock_workflow, "test-session"
            )

            # Verify handler was called
            mock_handler.assert_called_once_with(pre_intent, mock_workflow.id, "test-session")
            assert result.success is True
