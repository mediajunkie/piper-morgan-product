"""
Unit tests for Calendar query handlers in IntentService.

Issue #518: Phase A Quick Wins - Calendar Cluster (Canonical Queries #34, #35, #61)

Tests cover:
- Handler routing for Calendar query actions
- Graceful fallback when Calendar is not configured
- Meeting time summary result formatting (Query #34)
- Recurring meetings result formatting (Query #35)
- Week calendar view result formatting (Query #61)
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


class TestMeetingTimeQueryRouting:
    """Test routing to meeting time query handler"""

    @pytest.mark.asyncio
    async def test_routes_meeting_time_action(self, intent_service, mock_workflow):
        """Test that meeting_time action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
        )

        with patch.object(
            intent_service, "_handle_meeting_time_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="3 hours in meetings",
                intent_data={"category": "query", "action": "meeting_time"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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

            # Issue #586: user_id is now passed as third argument (None by default)
            mock_handler.assert_called_once_with(intent, mock_workflow.id, None)

    @pytest.mark.asyncio
    async def test_routes_how_much_time_in_meetings_action(self, intent_service, mock_workflow):
        """Test that how_much_time_in_meetings action also routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="how_much_time_in_meetings",
            context={"original_message": "meeting time this week"},
        )

        with patch.object(
            intent_service, "_handle_meeting_time_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="2 hours in meetings",
                intent_data={"category": "query", "action": "how_much_time_in_meetings"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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
    async def test_routes_calendar_analysis_action(self, intent_service, mock_workflow):
        """Test that calendar_analysis action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="calendar_analysis",
            context={"original_message": "analyze my calendar time"},
        )

        with patch.object(
            intent_service, "_handle_meeting_time_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="4 hours in meetings",
                intent_data={"category": "query", "action": "calendar_analysis"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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


class TestRecurringMeetingsQueryRouting:
    """Test routing to recurring meetings query handler"""

    @pytest.mark.asyncio
    async def test_routes_recurring_meetings_action(self, intent_service, mock_workflow):
        """Test that recurring_meetings action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review my recurring meetings"},
        )

        with patch.object(
            intent_service, "_handle_recurring_meetings_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="5 recurring meetings found",
                intent_data={"category": "query", "action": "recurring_meetings"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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

            # Issue #586: user_id is now passed as third argument (None by default)
            mock_handler.assert_called_once_with(intent, mock_workflow.id, None)

    @pytest.mark.asyncio
    async def test_routes_review_recurring_meetings_action(self, intent_service, mock_workflow):
        """Test that review_recurring_meetings action also routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="review_recurring_meetings",
            context={"original_message": "audit my standing meetings"},
        )

        with patch.object(
            intent_service, "_handle_recurring_meetings_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="3 recurring meetings found",
                intent_data={"category": "query", "action": "review_recurring_meetings"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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
    async def test_routes_audit_meetings_action(self, intent_service, mock_workflow):
        """Test that audit_meetings action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="audit_meetings",
            context={"original_message": "which meetings can I drop"},
        )

        with patch.object(
            intent_service, "_handle_recurring_meetings_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="7 recurring meetings found",
                intent_data={"category": "query", "action": "audit_meetings"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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


class TestWeekCalendarQueryRouting:
    """Test routing to week calendar query handler"""

    @pytest.mark.asyncio
    async def test_routes_week_calendar_action(self, intent_service, mock_workflow):
        """Test that week_calendar action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        with patch.object(
            intent_service, "_handle_week_calendar_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Week calendar view",
                intent_data={"category": "query", "action": "week_calendar"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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

            # Issue #586: user_id is now passed as third argument (None by default)
            mock_handler.assert_called_once_with(intent, mock_workflow.id, None)

    @pytest.mark.asyncio
    async def test_routes_week_ahead_action(self, intent_service, mock_workflow):
        """Test that week_ahead action also routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_ahead",
            context={"original_message": "week ahead"},
        )

        with patch.object(
            intent_service, "_handle_week_calendar_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Week ahead view",
                intent_data={"category": "query", "action": "week_ahead"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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
    async def test_routes_whats_my_week_like_action(self, intent_service, mock_workflow):
        """Test that whats_my_week_like action routes to Calendar handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="whats_my_week_like",
            context={"original_message": "this week's schedule"},
        )

        with patch.object(
            intent_service, "_handle_week_calendar_query", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Week schedule view",
                intent_data={"category": "query", "action": "whats_my_week_like"},
            )

            # #1124: calendar queries now dispatch via the action-dispatch rail
            # (_CALENDAR_QUERY_COHORT, user-scoped factory) — _handle_query_intent's
            # elif was removed. Route by intent.action through the real rail.
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


class TestCalendarNotConfiguredGracefulDegradation:
    """Test graceful fallback when Calendar is not configured"""

    @pytest.mark.asyncio
    async def test_meeting_time_returns_graceful_message_when_calendar_not_configured(
        self, intent_service
    ):
        """Test meeting time handler returns helpful message when Calendar not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=False)
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_meeting_time_query(intent, "workflow-id")

            assert result.success is True
            assert "isn't connected yet" in result.message
            assert "how do I connect Google Calendar?" in result.message
            assert result.implemented is False

    @pytest.mark.asyncio
    async def test_recurring_meetings_returns_graceful_message_when_calendar_not_configured(
        self, intent_service
    ):
        """Test recurring meetings handler returns helpful message when Calendar not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review recurring meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=False)
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_recurring_meetings_query(intent, "workflow-id")

            assert result.success is True
            assert "isn't connected yet" in result.message
            assert "how do I connect Google Calendar?" in result.message
            assert result.implemented is False

    @pytest.mark.asyncio
    async def test_week_calendar_returns_graceful_message_when_calendar_not_configured(
        self, intent_service
    ):
        """Test week calendar handler returns helpful message when Calendar not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=False)
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_week_calendar_query(intent, "workflow-id")

            assert result.success is True
            assert "isn't connected yet" in result.message
            assert "how do I connect Google Calendar?" in result.message
            assert result.implemented is False


class TestMeetingTimeQueryResults:
    """Test meeting time query result formatting"""

    @pytest.mark.asyncio
    async def test_formats_meeting_time_correctly(self, intent_service):
        """Test meeting time is formatted properly"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
            original_message="how much time in meetings",  # Issue #588: needed for temporal parsing
        )

        mock_events = [
            {
                "id": "event-1",
                "summary": "Team Standup",
                "duration_minutes": 30,
                "is_all_day": False,
            },
            {
                "id": "event-2",
                "summary": "Project Review",
                "duration_minutes": 60,
                "is_all_day": False,
            },
            {
                "id": "event-3",
                "summary": "Company Holiday",
                "duration_minutes": 0,
                "is_all_day": True,  # Should be excluded
            },
        ]

        # Issue #588: Mock at router level since handler now uses get_events_in_range
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.authenticate = AsyncMock(return_value=True)
            mock_router.get_events_in_range = AsyncMock(return_value=mock_events)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_meeting_time_query(intent, "workflow-id")

            assert result.success is True
            assert "1 hour 30 minutes" in result.message
            assert "2 meetings" in result.message
            assert "Team Standup" in result.message
            assert "Project Review" in result.message
            assert result.intent_data["total_minutes"] == 90
            assert result.intent_data["meeting_count"] == 2

    @pytest.mark.asyncio
    async def test_handles_no_meetings(self, intent_service):
        """Test handling when no meetings scheduled"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
            original_message="how much time in meetings",  # Issue #588: needed for temporal parsing
        )

        # Issue #588: Mock at router level since handler now uses get_events_in_range
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.authenticate = AsyncMock(return_value=True)
            mock_router.get_events_in_range = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_meeting_time_query(intent, "workflow-id")

            assert result.success is True
            assert "no meetings scheduled" in result.message.lower()
            assert result.intent_data["total_minutes"] == 0
            assert result.intent_data["meeting_count"] == 0


class TestRecurringMeetingsQueryResults:
    """Test recurring meetings query result formatting"""

    @pytest.mark.asyncio
    async def test_formats_recurring_meetings_correctly(self, intent_service):
        """Test recurring meetings are formatted properly with frequency"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review recurring meetings"},
        )

        mock_events = [
            {
                "summary": "Daily Standup",
                "recurrence": ["RRULE:FREQ=DAILY"],
                "start": {"dateTime": "2025-12-26T09:00:00Z"},
                "end": {"dateTime": "2025-12-26T09:30:00Z"},
            },
            {
                "summary": "Weekly Team Sync",
                "recurrence": ["RRULE:FREQ=WEEKLY"],
                "start": {"dateTime": "2025-12-26T14:00:00Z"},
                "end": {"dateTime": "2025-12-26T15:00:00Z"},
            },
        ]

        # Issue #518: Handler now uses CalendarIntegrationRouter (CORE-QUERY-1 pattern)
        # Mock the router's get_recurring_events method directly
        mock_processed_events = [
            {
                "summary": "Daily Standup",
                "frequency": "Daily",
                "duration_minutes": 30,
            },
            {
                "summary": "Weekly Team Sync",
                "frequency": "Weekly",
                "duration_minutes": 60,
            },
        ]

        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.authenticate = AsyncMock(return_value=True)
            mock_router.get_recurring_events = AsyncMock(return_value=mock_processed_events)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_recurring_meetings_query(intent, "workflow-id")

            assert result.success is True
            assert "2 found" in result.message
            assert "Daily Standup" in result.message
            assert "Weekly Team Sync" in result.message
            assert "Daily" in result.message
            assert "Weekly" in result.message
            assert result.intent_data["recurring_count"] == 2

    @pytest.mark.asyncio
    async def test_handles_no_recurring_meetings(self, intent_service):
        """Test handling when no recurring meetings found"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review recurring meetings"},
        )

        # Issue #518: Handler now uses CalendarIntegrationRouter (CORE-QUERY-1 pattern)
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.authenticate = AsyncMock(return_value=True)
            mock_router.get_recurring_events = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_recurring_meetings_query(intent, "workflow-id")

            assert result.success is True
            assert "didn't find any recurring meetings" in result.message
            assert result.intent_data["recurring_count"] == 0


class TestWeekCalendarQueryResults:
    """Test week calendar query result formatting"""

    @pytest.mark.asyncio
    async def test_formats_week_calendar_correctly(self, intent_service):
        """Test week calendar is formatted properly by day"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        # Mock events for different days
        now = datetime.now(timezone.utc)
        tomorrow = now + timedelta(days=1)

        mock_events = [
            {
                "id": "event-1",
                "summary": "Morning Meeting",
                "start": {"dateTime": now.isoformat() + "Z"},
                "end": {"dateTime": (now + timedelta(hours=1)).isoformat() + "Z"},
            },
            {
                "id": "event-2",
                "summary": "Afternoon Review",
                "start": {"dateTime": tomorrow.isoformat() + "Z"},
                "end": {"dateTime": (tomorrow + timedelta(hours=2)).isoformat() + "Z"},
            },
        ]

        # Issue #518: Handler now uses CalendarIntegrationRouter (CORE-QUERY-1 pattern)
        # The router's get_events_in_range returns processed events
        mock_processed_events = [
            {
                "id": "event-1",
                "summary": "Morning Meeting",
                "start_time": now.isoformat(),
                "end_time": (now + timedelta(hours=1)).isoformat(),
                "duration_minutes": 60,
                "is_all_day": False,
                "date": now.strftime("%Y-%m-%d"),
            },
            {
                "id": "event-2",
                "summary": "Afternoon Review",
                "start_time": tomorrow.isoformat(),
                "end_time": (tomorrow + timedelta(hours=2)).isoformat(),
                "duration_minutes": 120,
                "is_all_day": False,
                "date": tomorrow.strftime("%Y-%m-%d"),
            },
        ]

        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.authenticate = AsyncMock(return_value=True)
            mock_router.get_events_in_range = AsyncMock(return_value=mock_processed_events)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_week_calendar_query(intent, "workflow-id")

            assert result.success is True
            assert "Your Week Ahead" in result.message
            assert "Morning Meeting" in result.message
            assert "Afternoon Review" in result.message
            assert result.intent_data["days_count"] == 2

    @pytest.mark.asyncio
    async def test_handles_no_events_in_week(self, intent_service):
        """Test handling when no events scheduled for the week"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        # Issue #518: Handler now uses CalendarIntegrationRouter (CORE-QUERY-1 pattern)
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.authenticate = AsyncMock(return_value=True)
            mock_router.get_events_in_range = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_week_calendar_query(intent, "workflow-id")

            assert result.success is True
            assert "didn't find any events" in result.message
            assert result.intent_data["days_count"] == 0


class TestCalendarHandlerErrors:
    """Test error handling in Calendar handlers"""

    @pytest.mark.asyncio
    async def test_meeting_time_handles_calendar_error(self, intent_service):
        """Test meeting time handler gracefully handles Calendar API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="meeting_time",
            context={"original_message": "how much time in meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter.get_todays_events = AsyncMock(
                side_effect=Exception("API connection failed")
            )
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_meeting_time_query(intent, "workflow-id")

            assert result.success is False
            assert "looking up meeting times" in result.message
            assert result.error is not None
            assert result.error_type == "CalendarMeetingTimeQueryError"

    @pytest.mark.asyncio
    async def test_recurring_meetings_handles_calendar_error(self, intent_service):
        """Test recurring meetings handler gracefully handles Calendar API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="recurring_meetings",
            context={"original_message": "review recurring meetings"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter.get_todays_events = AsyncMock(side_effect=Exception("Rate limit exceeded"))
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_recurring_meetings_query(intent, "workflow-id")

            assert result.success is False
            assert "checking recurring meetings" in result.message
            assert result.error is not None
            assert result.error_type == "CalendarRecurringMeetingsQueryError"

    @pytest.mark.asyncio
    async def test_week_calendar_handles_calendar_error(self, intent_service):
        """Test week calendar handler gracefully handles Calendar API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="week_calendar",
            context={"original_message": "what's my week look like"},
        )

        with patch(
            "services.mcp.consumer.google_calendar_adapter.GoogleCalendarMCPAdapter"
        ) as MockAdapter:
            mock_adapter = MagicMock()
            mock_adapter.authenticate = AsyncMock(return_value=True)
            mock_adapter._service = MagicMock()
            mock_adapter._service.events.return_value.list.return_value.execute.side_effect = (
                Exception("Network timeout")
            )
            MockAdapter.return_value = mock_adapter

            result = await intent_service._handle_week_calendar_query(intent, "workflow-id")

            assert result.success is False
            assert "pulling up your week's calendar" in result.message
            assert result.error is not None
            assert result.error_type == "CalendarWeekQueryError"


class TestPreClassifierRoutingIntegration:
    """Test full routing path from pre-classifier to handlers (Issue #521)"""

    def test_meeting_time_routes_to_query_category(self):
        """Test 'how much time in meetings' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("how much time in meetings")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        # Issue #589: Action changed to match IntentService handler expectation
        assert result.action == "meeting_time"
        assert result.confidence == 1.0

    def test_meeting_time_variants(self):
        """Test meeting time query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "how much time in meetings",
            "how much time in meetings today",
            "time spent in meetings",
            "meeting time today",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "meeting_time", f"Wrong action for: {query}"

    def test_recurring_meetings_routes_to_query_category(self):
        """Test 'review my recurring meetings' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("review my recurring meetings")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "recurring_meetings"
        assert result.confidence == 1.0

    def test_recurring_meetings_variants(self):
        """Test recurring meetings query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "review my recurring meetings",
            "show recurring meetings",
            "audit my standing meetings",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "recurring_meetings", f"Wrong action for: {query}"

    def test_week_calendar_routes_to_query_category(self):
        """Test 'what's my week look like' routes to QUERY category"""
        from services.intent_service.pre_classifier import PreClassifier

        result = PreClassifier.pre_classify("what's my week look like")

        assert result is not None
        assert result.category == IntentCategory.QUERY
        assert result.action == "week_calendar"
        assert result.confidence == 1.0

    def test_week_calendar_variants(self):
        """Test week calendar query pattern variants all route correctly"""
        from services.intent_service.pre_classifier import PreClassifier

        test_cases = [
            "what's my week look like",
            "show me my week",
            "week ahead",
        ]

        for query in test_cases:
            result = PreClassifier.pre_classify(query)
            assert result is not None, f"Failed to classify: {query}"
            assert result.category == IntentCategory.QUERY, f"Wrong category for: {query}"
            assert result.action == "week_calendar", f"Wrong action for: {query}"
