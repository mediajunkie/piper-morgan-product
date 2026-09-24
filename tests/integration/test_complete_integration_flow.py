"""
Test Complete Integration Flow
Tests SlackResponseHandler's spatial-event-to-response integration.

#1499 Class 2 member strip (2026-09-23): this file originally also covered
SlackWebhookRouter's event-processing methods (_process_message_event,
_process_mention_event, _process_reaction_event) via a webhook-router
fixture. Those methods were removed from SlackWebhookRouter as dead code —
they were reachable only from the unmounted Events API FastAPI route
(_handle_events_webhook) and the equally-unreached direct-testing method
(handle_slack_events); Socket Mode's own event handling
(SlackSocketModeRunner._handle_event) never called into this class. See
docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md.
"""

from unittest.mock import MagicMock

import pytest

from services.domain.models import Intent, IntentCategory, SpatialEvent
from services.integrations.slack.response_handler import SlackResponseHandler


class TestResponseHandlerIntegration:
    """Test response handler integration with dependencies"""

    @pytest.mark.asyncio
    async def test_response_handler_with_mock_dependencies(self):
        """Test response handler with mocked dependencies"""
        # Arrange
        mock_spatial_adapter = MagicMock()
        mock_intent_classifier = MagicMock()
        mock_orchestration_engine = MagicMock()
        mock_slack_client = MagicMock()

        response_handler = SlackResponseHandler(
            spatial_adapter=mock_spatial_adapter,
            intent_classifier=mock_intent_classifier,
            slack_client=mock_slack_client,
        )

        # Create test spatial event
        spatial_event = SpatialEvent(
            event_type="attention_attracted",
            territory_position=1,
            room_position=2,
            object_position=3,
            actor_id="U123456",
            significance_level="significant",
        )

        # Mock adapter to return context
        mock_context = {
            "channel_id": "C789012",
            "thread_ts": None,
            "workspace_id": "T123456",
            "user_id": "U123456",
            "attention_level": "high",
            "navigation_intent": "respond",
        }
        mock_spatial_adapter.get_response_context.return_value = mock_context

        # Mock intent classifier
        mock_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="respond_to_mention",
            confidence=0.9,
            context={"spatial_context": mock_context},
        )
        mock_intent_classifier.classify.return_value = mock_intent

        # Mock orchestration engine
        mock_workflow_result = {
            "success": True,
            "message": "Response sent successfully",
            "data": {"response_text": "Hello! I'm here to help."},
        }
        mock_orchestration_engine.execute_workflow.return_value = mock_workflow_result

        # Mock Slack client
        mock_slack_response = {"ok": True, "ts": "1234567890.123457"}
        mock_slack_client.send_message.return_value = mock_slack_response

        # Act
        result = await response_handler.handle_spatial_event(spatial_event)

        # Assert
        assert result is not None
        assert result.get("status") == "sent"
        assert result.get("channel") == "C789012"

        # Verify all components were called
        mock_spatial_adapter.get_response_context.assert_called_once()
        mock_intent_classifier.classify.assert_called_once()
        mock_orchestration_engine.execute_workflow.assert_called_once()
        mock_slack_client.send_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_response_handler_no_context_found(self):
        """Test response handler when no context is found"""
        # Arrange
        mock_spatial_adapter = MagicMock()
        mock_intent_classifier = MagicMock()
        mock_orchestration_engine = MagicMock()
        mock_slack_client = MagicMock()

        response_handler = SlackResponseHandler(
            spatial_adapter=mock_spatial_adapter,
            intent_classifier=mock_intent_classifier,
            slack_client=mock_slack_client,
        )

        # Create test spatial event
        spatial_event = SpatialEvent(
            event_type="message_posted",
            territory_position=1,
            room_position=2,
            object_position=999,  # Non-existent position
            actor_id="U123456",
        )

        # Mock adapter to return None (no context found)
        mock_spatial_adapter.get_response_context.return_value = None

        # Act
        result = await response_handler.handle_spatial_event(spatial_event)

        # Assert
        assert result is None

        # Verify only adapter was called, others should not be called
        mock_spatial_adapter.get_response_context.assert_called_once()
        mock_intent_classifier.classify.assert_not_called()
        mock_orchestration_engine.execute_workflow.assert_not_called()
        mock_slack_client.send_message.assert_not_called()
