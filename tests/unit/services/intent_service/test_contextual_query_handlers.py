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


class TestChangesQueryRouting:
    """Test routing to changes query handler"""

    @pytest.mark.asyncio
    async def test_routes_changes_query_action(self, intent_service, mock_workflow):
        """#1124 migration #3: changes_query now dispatches via the action-dispatch
        rail (run_changes_query_workflow → _handle_changes_query), not
        _handle_query_intent's elif (which was removed)."""
        from services.intent_service.workflow_entries import run_changes_query_workflow

        intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday", "user_id": "u-2140"},
        )

        with patch.object(
            intent_service, "_handle_changes_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Activity summary",
                intent_data={"category": "query", "action": "changes_query"},
            )

            await run_changes_query_workflow(
                session_id="test-session",
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id, "test-session")

    @pytest.mark.asyncio
    async def test_routes_what_changed_action(self, intent_service, mock_workflow):
        """#1124 migration #3: what_changed also dispatches via the rail."""
        from services.intent_service.workflow_entries import run_changes_query_workflow

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

            await run_changes_query_workflow(
                session_id="test-session",
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
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

            # #1124: attention queries now dispatch via the action-dispatch rail —
            # _handle_query_intent's elif was removed. Route by intent.action through
            # the real rail. Factory threads (intent, workflow_id, session_id, user_id)
            # positionally (user_id=None from dispatch).
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

            # Issue #849: user_id is now threaded through to _handle_attention_query.
            # #1124: the rail's factory passes user_id POSITIONALLY (was a kwarg in the
            # removed elif).
            mock_handler.assert_called_once_with(intent, mock_workflow.id, "test-session", None)

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

            # #1124: attention queries now dispatch via the action-dispatch rail.
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
            context={"original_message": "what changed since yesterday", "user_id": "u-2140"},
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
            assert result.message.startswith(
                "Here's what changed in your Piper tasks, projects and activity log since "
                "yesterday. I haven't checked GitHub for this."
            )  # #2140 (CXO)
            assert result.intent_data["time_range_days"] == 1
            assert result.intent_data["total_activities"] >= 0

    @pytest.mark.asyncio
    async def test_handles_no_activity(self, intent_service):
        """Test changes query handles empty activity list"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday", "user_id": "u-2140"},
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
            assert result.message == (
                "I don't see anything new in your Piper tasks, projects or activity log since "
                "yesterday. I haven't checked GitHub for this."
            )  # #2140 (CXO): all three read ok and all three empty
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

            # Read order (#1985 (b)): high-priority, due-today, overdue, projects.
            mock_result_1 = MagicMock()
            mock_result_1.scalars.return_value.all.return_value = []

            mock_result_2 = MagicMock()
            mock_result_2.scalars.return_value.all.return_value = [mock_todo]

            mock_session_instance.execute = AsyncMock(
                side_effect=[mock_result_1, mock_result_1, mock_result_2, mock_result_1]
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
                # #1985 (b): verified-empty reads serve CXO's exact line, then
                # the #1069 source-transparent second line.
                assert "Nothing due today and nothing overdue." in result.message
                assert "nothing urgent" not in result.message.lower()
                assert result.intent_data["total_attention_items"] == 0


class TestContextualQueryErrorHandling:
    """Test error handling in contextual query handlers"""

    @pytest.mark.asyncio
    async def test_changes_query_handles_database_error(self, intent_service):
        """#2140 (Arch 10-23): every read failing is not "no activity"; it is a failed read."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday", "user_id": "u-2140"},
        )

        # Mock database error for all queries
        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session.side_effect = Exception("Database connection failed")

            result = await intent_service._handle_changes_query(
                intent, "workflow-id", "test-session"
            )

            # Fail-closed: all three reads failed, so success=False and the words
            # name every source; never the empty line.
            assert result.success is False
            assert result.message == (
                "I couldn't read your Piper tasks, projects or activity log just now, so I "
                "can't say what changed since yesterday. Try again in a moment; if it keeps "
                "failing, tell us."
            )
            assert result.intent_data["failed_sources"] == ["tasks", "projects", "activity log"]

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
                # #1069 / #1985 (b): a FAILED read is not an empty list — never
                # the exact empty line over a timeout.
                assert "couldn't check your todos" in result.message
                assert "Nothing due today and nothing overdue." not in result.message
                assert result.intent_data["total_attention_items"] == 0


class TestPreClassifierRoutingIntegration:
    """Test full routing path from pre-classifier to handlers (Issue #521)

    #1595 Phase 3 thirteenth deletion (2026-10-03): `CONTEXTUAL_QUERY_PATTERNS`
    is now `[]` (tombstoned, FULL deletion) — `pre_classify` can no longer
    claim any of these phrases. Every "routes to QUERY" assertion below is
    converted to pin the new reality (surface-1 DECLINE, `result is None`);
    see `TestContextualQueryInversionRoutesSurvive` below for the live-routes
    pins that prove changes_query/attention_query are still reachable through
    the Inversion (both are WORKFLOW-disposition rail ops with a flip_group
    live under this epic's --live set: changes_query→read_temporal,
    attention_query→read_status)."""

    def test_attention_query_routes_to_query_category(self):
        """'what needs my attention' is claimed again at surface 1 by the
        RESTORED `\\bneeds my attention\\b` literal (#1973-shape restore,
        2026-10-10, Lead): QUERY / attention_query."""
        result = PreClassifier.pre_classify("what needs my attention")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "attention_query"

    def test_attention_query_variants(self):
        """Only the phrasings containing the RESTORED `\\bneeds my attention\\b`
        literal (#1973-shape restore, 2026-10-10) claim at surface 1; the
        rest still decline."""
        claimed = [
            "what needs my attention",
            "show me what needs my attention",
        ]
        declined = [
            "what needs attention",
            "items that need attention",
            "attention items",
        ]

        for query in claimed:
            result = PreClassifier.pre_classify(query)
            assert result is not None and result.action == "attention_query", query
        for query in declined:
            result = PreClassifier.pre_classify(query)
            assert result is None, f"unexpectedly still classifies: {query}"

    def test_changes_query_routes_to_query_category(self):
        """'what changed since yesterday' no longer claims at surface 1."""
        result = PreClassifier.pre_classify("what changed since yesterday")

        assert result is None

    def test_changes_query_variants(self):
        """Changes query phrasings no longer claim at surface 1."""
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
            assert result is None, f"unexpectedly still classifies: {query}"

    def test_priority_patterns_still_work(self):
        """#1595 Phase 3 sixth deletion (2026-10-02): PRIORITY_PATTERNS is
        `[]` (tombstoned) — these phrases no longer claim at surface 1.
        get_top_priority is a FLOOR-disposition action with NO WorkflowEntry
        (confirmed via get_action_workflows()), so unlike the rail-live ops
        this deletion also touched (attention_query, prioritize — see
        TestContextualQueryRouting's own coverage), there is no
        `assert_inversion_routes` pin to add here: the Inversion never
        dispatches get_top_priority by name, and once surface 1 declines
        the phrase reaches the floor by CATEGORY (PRIORITY) through the LLM
        classifier, not through a rail key this test could stub and prove.
        Converted to pin the decline, per the dispatch's own exclusion
        rationale for other floor-routed actions (e.g. get_project_status,
        close_issue_query) in the prior two deletions."""
        priority_queries = [
            "what are my priorities",
            "what's my top priority",
            "show me my priorities",
            "what should i focus on",
            "what's most important",
        ]

        for query in priority_queries:
            result = PreClassifier.pre_classify(query)
            assert result is None, f"Expected decline (PRIORITY_PATTERNS deleted) for: {query}"

    def test_contextual_queries_checked_before_priority(self):
        """#1595 Phase 3: both CONTEXTUAL_QUERY_PATTERNS (thirteenth deletion)
        and PRIORITY_PATTERNS (sixth deletion) are now `[]` — the collision
        this test guarded against (CONTEXTUAL_QUERY needing to be checked
        before PRIORITY's `\\bneeds.*attention\\b`) is doubly moot: neither
        list can claim anything any more. Converted to pin the decline.
        2026-10-10 (#1973-shape restore, Lead): CONTEXTUAL_QUERY_PATTERNS
        regained `\\bneeds my attention\\b`, so this phrase is claimed again as
        QUERY / attention_query (PRIORITY_PATTERNS is still `[]`, so the
        collision this test originally guarded cannot recur)."""
        result = PreClassifier.pre_classify("what needs my attention right now")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "attention_query"

    @pytest.mark.asyncio
    async def test_full_routing_attention_query_to_handler(self, intent_service, mock_workflow):
        """Test full path: QUERY intent → attention handler (#1595 thirteenth
        deletion: surface 1 no longer claims "what needs my attention", so
        the intent is constructed directly — same idiom
        TestAttentionQueryUserIdPassthroughAuthenticated below already uses —
        rather than routed through pre_classify)."""
        # Step 1: construct the intent directly (surface 1 no longer claims this)
        pre_intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs my attention"},
        )

        # Step 2: IntentService routes to correct handler
        with patch.object(
            intent_service, "_handle_attention_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Attention items",
                intent_data={"category": "query", "action": "attention_query"},
            )

            # #1124: attention queries now dispatch via the action-dispatch rail —
            # _handle_query_intent's elif was removed. Use the pre-classified intent.
            register_default_workflows()
            result = await dispatch_workflow(
                workflow_type=pre_intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": pre_intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            # Verify handler was called
            # Issue #849: user_id is now threaded through to _handle_attention_query.
            # #1124: the rail's factory passes user_id POSITIONALLY (was a kwarg).
            mock_handler.assert_called_once_with(pre_intent, mock_workflow.id, "test-session", None)
            assert result.success is True

    @pytest.mark.asyncio
    async def test_full_routing_changes_query_to_handler(self, intent_service, mock_workflow):
        """Test full path: changes_query action → action-dispatch rail (#1124
        migration #3) → changes handler. #1595 thirteenth deletion: surface 1
        no longer claims "what changed since yesterday", so the intent is
        constructed directly."""
        from services.intent_service.workflow_entries import run_changes_query_workflow

        # Step 1: construct the intent directly (surface 1 no longer claims this)
        pre_intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday", "user_id": "u-2140"},
        )

        # Step 2: the action-dispatch rail routes changes_query to its handler
        # (replaces the removed _handle_query_intent elif).
        with patch.object(
            intent_service, "_handle_changes_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Activity summary",
                intent_data={"category": "query", "action": "changes_query"},
            )

            result = await run_changes_query_workflow(
                session_id="test-session",
                context={
                    "intent": pre_intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(pre_intent, mock_workflow.id, "test-session")
            assert result.success is True


class TestAttentionQueryUserIdPassthroughAuthenticated:
    """#1533 (principal-dropping audit). Issue #849 threaded user_id to
    _handle_attention_query as the 4th positional arg — every routing test
    above pins that pass-through, but only ever with user_id=None
    (`mock_handler.assert_called_once_with(intent, mock_workflow.id,
    "test-session", None)`), so a regression that broke forwarding for a
    REAL value specifically would read identical to this file's own suite.
    This pins the same #849 pass-through with a real user_id."""

    @pytest.mark.asyncio
    async def test_attention_query_forwards_the_real_user_id(self, intent_service, mock_workflow):
        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs my attention"},
        )
        real_user_id = "1533-authenticated-user"

        with patch.object(
            intent_service, "_handle_attention_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Attention items",
                intent_data={"category": "query", "action": "attention_query"},
            )

            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=real_user_id,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(
                intent, mock_workflow.id, "test-session", real_user_id
            )


class TestContextualQueryInversionRoutesSurvive:
    """#1595 Phase 3 thirteenth deletion: a representative sample of
    TestPreClassifierRoutingIntegration's phrases still route correctly
    through the Inversion's live consult (stubbed router — no LLM call,
    ever), proving changes_query/attention_query didn't just vanish when
    surface 1 stopped claiming them."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "phrase,action,live_categories",
        [
            ("what needs my attention", "attention_query", "read_status"),
            ("what changed since yesterday", "changes_query", "read_temporal"),
        ],
    )
    async def test_routes_live(self, monkeypatch, phrase, action, live_categories):
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        await assert_inversion_routes(
            monkeypatch,
            phrase,
            live_categories=live_categories,
            expected_action=action,
        )


class TestTodoReadsScopeByPrincipal1985:
    """#1985 (alpha c613beabf5, 2026-10-12): `show today's tasks` answered
    "nothing urgent" over an overdue todo because `_handle_attention_query`
    filtered TodoDB by owner_id == SESSION_id while todos are written with
    owner_id = user_id — the #1395 principal-confusion class (ADR-071 D5).
    These pins read the bound parameters of the statements the handlers
    execute: the principal must be bound, the session id must not.
    """

    USER = "f13937fb-182b-44db-a9fd-0d722a3a223e"
    SESSION = "lead-1985-session"

    @staticmethod
    def _capture_session(captured):
        mock_session = AsyncMock()

        async def _execute(stmt, *args, **kwargs):
            captured.append(stmt)
            result = MagicMock()
            result.scalars.return_value.all.return_value = []
            result.scalar.return_value = 0
            result.all.return_value = []
            return result

        mock_session.execute = _execute
        scope = MagicMock()
        scope.__aenter__ = AsyncMock(return_value=mock_session)
        scope.__aexit__ = AsyncMock(return_value=False)
        return scope

    @staticmethod
    def _bound_values(stmt):
        try:
            return {str(v) for v in stmt.compile().params.values() if v is not None}
        except Exception:
            return set()

    @pytest.mark.asyncio
    async def test_attention_query_binds_the_principal_not_the_session(self, intent_service):
        captured = []
        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "show today's tasks", "user_id": self.USER},
        )
        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope",
            return_value=self._capture_session(captured),
        ):
            result = await intent_service._handle_attention_query(
                intent, "wf-1985", self.SESSION, None
            )
        assert result.success is True
        bound = set().union(*(self._bound_values(s) for s in captured)) if captured else set()
        todo_stmts = [s for s in captured if "todos" in str(s).lower()]
        assert todo_stmts, "the handler must read the todo table"
        assert self.USER in bound, f"principal not bound; bound={bound}"
        assert self.SESSION not in bound, f"session id still bound; bound={bound}"

    @pytest.mark.asyncio
    async def test_attention_query_falls_back_to_the_threaded_user_id(self, intent_service):
        """#849 threads user_id positionally; without a stamped principal it is the owner."""
        captured = []
        intent = Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "what needs my attention"},
        )
        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope",
            return_value=self._capture_session(captured),
        ):
            await intent_service._handle_attention_query(intent, "wf-1985", self.SESSION, self.USER)
        bound = set().union(*(self._bound_values(s) for s in captured)) if captured else set()
        assert self.USER in bound
        assert self.SESSION not in bound

    @pytest.mark.asyncio
    async def test_changes_query_binds_the_principal_not_the_session(self, intent_service):
        captured = []
        intent = Intent(
            category=IntentCategory.QUERY,
            action="changes_query",
            context={"original_message": "what changed since yesterday", "user_id": self.USER},
        )
        with patch(
            "services.intent.intent_service.AsyncSessionFactory.session_scope",
            return_value=self._capture_session(captured),
        ):
            result = await intent_service._handle_changes_query(intent, "wf-1985", self.SESSION)
        assert result.success is True
        bound = set().union(*(self._bound_values(s) for s in captured)) if captured else set()
        assert self.USER in bound, f"principal not bound; bound={bound}"
        assert self.SESSION not in bound, f"session id still bound; bound={bound}"


class TestAttentionReplyShape1985b:
    """#1985 (b) — CXO's reply-shape ruling (2026-10-12): the todo list LEADS
    under "Today:", due today first, then overdue, each marked; the exact
    empty line when both are empty; "Nothing due today." then the overdue
    list when only overdue exist; never "nothing urgent" over a non-empty
    list; a flagged todo already listed is not repeated.
    """

    USER = "f13937fb-182b-44db-a9fd-0d722a3a223e"

    class _Todo:
        def __init__(self, text, priority="medium", due_date=None, updated_at=None):
            self.text = text
            self.priority = priority
            self.due_date = due_date
            self.updated_at = updated_at
            self.name = text

    @classmethod
    def _session(cls, due_today, overdue, flagged):
        """A fake session that answers each read by the SHAPE of its statement:
        two datetime bounds = due today; one datetime bound + no IN = overdue;
        an IN list = flagged; anything else (projects) = nothing."""
        mock_session = AsyncMock()

        async def _execute(stmt, *args, **kwargs):
            params = list(stmt.compile().params.values())
            sql = str(stmt).lower()
            dts = [v for v in params if isinstance(v, datetime)]
            result = MagicMock()
            if "todos" not in sql:
                rows = []
            elif any(isinstance(v, (list, tuple)) for v in params):
                rows = flagged
            elif len(dts) >= 2:
                rows = due_today
            elif len(dts) == 1:
                rows = overdue
            else:
                rows = []
            result.scalars.return_value.all.return_value = rows
            return result

        mock_session.execute = _execute
        scope = MagicMock()
        scope.__aenter__ = AsyncMock(return_value=mock_session)
        scope.__aexit__ = AsyncMock(return_value=False)
        return scope

    def _intent(self):
        return Intent(
            category=IntentCategory.QUERY,
            action="attention_query",
            context={"original_message": "show today's tasks", "user_id": self.USER},
        )

    async def _run(self, intent_service, due_today, overdue, flagged=(), calendar="empty"):
        """``calendar``: "empty" (connected, read OK, no meetings; the #1985 success
        path), "not_connected", or "failed" (#2151: the read failed)."""
        _router = (
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        )
        with (
            patch(
                "services.intent.intent_service.AsyncSessionFactory.session_scope",
                return_value=self._session(list(due_today), list(overdue), list(flagged)),
            ),
            patch(
                "services.utils.datetime_utils.user_timezone_name",
                new=AsyncMock(return_value="America/Los_Angeles"),
            ),
            patch(
                f"{_router}.authenticate", new=AsyncMock(return_value=calendar != "not_connected")
            ),
            patch(f"{_router}.get_todays_events", new=AsyncMock(return_value=[])),
            patch(
                f"{_router}.last_read_error",
                new="network" if calendar == "failed" else None,
                create=True,
            ),
        ):
            return await intent_service._handle_attention_query(
                self._intent(), "wf-1985b", "session-1985b", None
            )

    @pytest.mark.asyncio
    async def test_due_today_leads_then_overdue_each_marked(self, intent_service):
        now = datetime.now(timezone.utc)
        due = self._Todo("send the budget review to the board", due_date=now + timedelta(hours=3))
        late = self._Todo("revise the pr", due_date=now - timedelta(days=5))
        result = await self._run(intent_service, [due], [late])
        lines = [ln for ln in result.message.split("\n") if ln.strip()]
        assert lines[0] == "**Today:**"
        assert lines[1] == "📅 send the budget review to the board (due today)"
        assert lines[2].startswith("⏰ revise the pr (") and lines[2].endswith("days overdue)")
        assert "nothing urgent" not in result.message.lower()
        assert result.intent_data["due_today_todos"][0]["text"] == due.text

    @pytest.mark.asyncio
    async def test_exact_empty_line_when_nothing_due_or_overdue(self, intent_service):
        result = await self._run(intent_service, [], [])
        lines = [ln for ln in result.message.split("\n") if ln.strip()]
        assert lines[0] == "**Today:**"
        assert lines[1] == "Nothing due today and nothing overdue."
        assert "nothing urgent" not in result.message.lower()

    @pytest.mark.asyncio
    async def test_nothing_due_today_line_then_overdue(self, intent_service):
        now = datetime.now(timezone.utc)
        late = self._Todo("revise the pr", due_date=now - timedelta(days=2))
        result = await self._run(intent_service, [], [late])
        lines = [ln for ln in result.message.split("\n") if ln.strip()]
        assert lines[0] == "**Today:**"
        assert lines[1] == "Nothing due today."
        assert lines[2].startswith("⏰ revise the pr (")

    @pytest.mark.asyncio
    async def test_1999_due_today_whose_time_has_passed_reads_due_earlier_today(
        self, intent_service
    ):
        """CXO's #1999 ruling: under one whole day overdue, say it in words,
        under the Today: line, never '(0 days overdue)' beneath 'Nothing due
        today.'"""
        now = datetime.now(timezone.utc)
        passed = self._Todo(
            "send the budget review to the board", due_date=now - timedelta(hours=2)
        )
        ahead = self._Todo("web check alpha", due_date=now + timedelta(hours=2))
        result = await self._run(intent_service, [passed, ahead], [])
        lines = [ln for ln in result.message.split("\n") if ln.strip()]
        assert lines[0] == "**Today:**"
        assert lines[1] == "📅 send the budget review to the board (due earlier today)"
        assert lines[2] == "📅 web check alpha (due today)"
        assert "0 days overdue" not in result.message
        assert "Nothing due today" not in result.message

    @pytest.mark.asyncio
    async def test_1996_overdue_age_is_calendar_days_on_the_users_clock(self, intent_service):
        """Alpha 651756d520 (Web, 2026-10-12): 'revise the pr' read 4 days
        overdue at 16:27 and 5 days a few minutes later — the age was elapsed
        24-hour periods. An item due at 23:50 local five calendar days ago is
        5 days overdue all day today, whatever the hour."""
        from zoneinfo import ZoneInfo

        tz = ZoneInfo("America/Los_Angeles")
        local_now = datetime.now(timezone.utc).astimezone(tz)
        due_local = (local_now - timedelta(days=5)).replace(hour=23, minute=50, second=0)
        late = self._Todo("revise the pr", due_date=due_local.astimezone(timezone.utc))
        result = await self._run(intent_service, [], [late])
        assert "⏰ revise the pr (5 days overdue)" in result.message
        assert result.intent_data["overdue_todos"][0]["days_overdue"] == 5

    @pytest.mark.asyncio
    async def test_2001_one_day_overdue_is_singular_two_is_plural(self, intent_service):
        """CXO #2001 (Web's served run on 6e48d9ebb2): the Today: list said
        "(1 days overdue)" while the prose said "1 day overdue". One source
        for the age label: 1 → "1 day overdue", N → "N days overdue", in the
        list line AND the attention item's detail."""
        from zoneinfo import ZoneInfo

        from services.intent.intent_service import _overdue_age_label

        assert _overdue_age_label(1) == "1 day overdue"
        assert _overdue_age_label(2) == "2 days overdue"
        assert _overdue_age_label(0) == "0 days overdue"  # never rendered (#1999), pinned for shape
        tz = ZoneInfo("America/Los_Angeles")
        local_now = datetime.now(timezone.utc).astimezone(tz)
        one = self._Todo(
            "send the budget review to the board",
            due_date=(local_now - timedelta(days=1))
            .replace(hour=9, minute=0)
            .astimezone(timezone.utc),
        )
        two = self._Todo(
            "send the budget review to finance",
            due_date=(local_now - timedelta(days=2))
            .replace(hour=9, minute=0)
            .astimezone(timezone.utc),
        )
        result = await self._run(intent_service, [], [one, two])
        assert "⏰ send the budget review to the board (1 day overdue)" in result.message
        assert "⏰ send the budget review to finance (2 days overdue)" in result.message
        assert "1 days overdue" not in result.message

    @pytest.mark.asyncio
    async def test_1996_both_reads_split_at_local_midnight_not_now(self, intent_service):
        """The due-today read's lower bound and the overdue read's upper bound
        are the SAME instant: local midnight on the user's clock. Before #1996
        both were `now`, which put an item due earlier today in the overdue
        list as '(0 days overdue)'."""
        from zoneinfo import ZoneInfo

        seen = []

        async def _execute(stmt, *args, **kwargs):
            params = list(stmt.compile().params.values())
            if "todos" in str(stmt).lower():
                seen.append(sorted(v for v in params if isinstance(v, datetime)))
            result = MagicMock()
            result.scalars.return_value.all.return_value = []
            return result

        session = AsyncMock()
        session.execute = _execute
        scope = MagicMock()
        scope.__aenter__ = AsyncMock(return_value=session)
        scope.__aexit__ = AsyncMock(return_value=False)
        with (
            patch(
                "services.intent.intent_service.AsyncSessionFactory.session_scope",
                return_value=scope,
            ),
            patch(
                "services.utils.datetime_utils.user_timezone_name",
                new=AsyncMock(return_value="America/Los_Angeles"),
            ),
        ):
            await intent_service._handle_attention_query(
                self._intent(), "wf-1996", "session-1996", None
            )
        now = datetime.now(timezone.utc)
        local_midnight = (
            now.astimezone(ZoneInfo("America/Los_Angeles"))
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .astimezone(timezone.utc)
        )
        two_bound = [d for d in seen if len(d) == 2]
        one_bound = [d for d in seen if len(d) == 1]
        assert two_bound and one_bound, seen
        assert two_bound[0][0] == local_midnight
        assert two_bound[0][1] == local_midnight + timedelta(days=1)
        assert one_bound[0][0] == local_midnight
        assert local_midnight <= now

    @pytest.mark.asyncio
    async def test_flagged_todo_already_listed_appears_once(self, intent_service):
        now = datetime.now(timezone.utc)
        late = self._Todo("revise the pr", priority="high", due_date=now - timedelta(days=2))
        other = self._Todo("call finance", priority="urgent")
        result = await self._run(intent_service, [], [late], flagged=[late, other])
        assert result.message.count("revise the pr") == 1
        assert "call finance" in result.message
        assert result.message.index("revise the pr") < result.message.index("call finance")
