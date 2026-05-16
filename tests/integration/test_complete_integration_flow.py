"""
Test Complete Integration Flow
Tests the complete flow from Slack webhook to response through spatial adapter and response handler.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent, IntentCategory, SpatialEvent
from services.integrations.slack.response_handler import SlackResponseHandler
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter
from services.integrations.slack.webhook_router import SlackWebhookRouter


class TestCompleteIntegrationFlow:
    """Test complete integration flow from webhook to response"""

    @pytest.mark.asyncio
    async def test_webhook_router_with_response_handler(self):
        """Test webhook router initialization with response handler"""
        # Act
        router = SlackWebhookRouter()

        # Assert
        assert router.response_handler is not None
        assert isinstance(router.response_handler, SlackResponseHandler)
        assert router.spatial_adapter is not None
        assert isinstance(router.spatial_adapter, SlackSpatialAdapter)

    @pytest.mark.asyncio
    async def test_message_event_complete_flow(self):
        """Test complete flow for message event"""
        # Arrange
        router = SlackWebhookRouter()
        event = {
            "type": "message",
            "channel": "C789012",
            "ts": "1234567890.123456",
            "user": "U123456",
            "text": "Hello world",
        }
        team_id = "T123456"

        # Mock response handler to return success
        mock_response_result = {"status": "sent", "channel": "C789012"}
        router.response_handler.handle_spatial_event = AsyncMock(return_value=mock_response_result)

        # Act
        await router._process_message_event(event, team_id)

        # Assert
        # Check that spatial event was created and stored
        response_context = await router.spatial_adapter.get_response_context("1234567890.123456")
        assert response_context is not None
        assert response_context["channel_id"] == "C789012"
        assert response_context["user_id"] == "U123456"

        # Check that response handler was called
        router.response_handler.handle_spatial_event.assert_called_once()
        spatial_event = router.response_handler.handle_spatial_event.call_args[0][0]
        assert isinstance(spatial_event, SpatialEvent)
        assert spatial_event.event_type == "message_posted"
        assert spatial_event.object_position is not None

    @pytest.mark.asyncio
    async def test_mention_event_complete_flow(self):
        """Test complete flow for mention event"""
        # Arrange
        router = SlackWebhookRouter()
        event = {
            "type": "app_mention",
            "channel": "C789012",
            "ts": "1234567890.123456",
            "user": "U123456",
            "text": "<@U123456> Hello Piper!",
        }
        team_id = "T123456"

        # Mock response handler to return success
        mock_response_result = {"status": "sent", "channel": "C789012"}
        router.response_handler.handle_spatial_event = AsyncMock(return_value=mock_response_result)

        # Act
        await router._process_mention_event(event, team_id)

        # Assert
        # Check that spatial event was created with high attention
        response_context = await router.spatial_adapter.get_response_context("1234567890.123456")
        assert response_context is not None
        assert response_context["attention_level"] == "high"
        assert response_context["navigation_intent"] == "respond"

        # Check that response handler was called
        router.response_handler.handle_spatial_event.assert_called_once()
        spatial_event = router.response_handler.handle_spatial_event.call_args[0][0]
        assert isinstance(spatial_event, SpatialEvent)
        assert spatial_event.event_type == "attention_attracted"
        assert spatial_event.significance_level == "significant"

    @pytest.mark.asyncio
    async def test_reaction_event_complete_flow(self):
        """Test complete flow for reaction event"""
        # Arrange
        router = SlackWebhookRouter()
        event = {
            "type": "reaction_added",
            "reaction": "heart",
            "user": "U123456",
            "item": {
                "type": "message",
                "channel": "C789012",
                "ts": "1234567890.123456",
            },
        }
        team_id = "T123456"

        # Mock response handler to return success
        mock_response_result = {"status": "sent", "channel": "C789012"}
        router.response_handler.handle_spatial_event = AsyncMock(return_value=mock_response_result)

        # Act
        await router._process_reaction_event(event, team_id)

        # Assert
        # Check that spatial event was created with emotional context
        response_context = await router.spatial_adapter.get_response_context("1234567890.123456")
        assert response_context is not None
        assert response_context["channel_id"] == "C789012"

        # Check that response handler was called
        router.response_handler.handle_spatial_event.assert_called_once()
        spatial_event = router.response_handler.handle_spatial_event.call_args[0][0]
        assert isinstance(spatial_event, SpatialEvent)
        assert spatial_event.event_type == "emotional_marker_updated"

    @pytest.mark.asyncio
    async def test_response_handler_error_handling(self):
        """Test error handling in response handler integration"""
        # Arrange
        router = SlackWebhookRouter()
        event = {
            "type": "message",
            "channel": "C789012",
            "ts": "1234567890.123456",
            "user": "U123456",
            "text": "Hello world",
        }
        team_id = "T123456"

        # Mock response handler to raise exception
        router.response_handler.handle_spatial_event = AsyncMock(
            side_effect=Exception("Test error")
        )

        # Act
        await router._process_message_event(event, team_id)

        # Assert
        # Check that spatial event was still created and stored
        response_context = await router.spatial_adapter.get_response_context("1234567890.123456")
        assert response_context is not None
        assert response_context["channel_id"] == "C789012"

        # Check that response handler was called (error should be logged but not crash)
        router.response_handler.handle_spatial_event.assert_called_once()


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


class TestSpatialAdapterRegistryIntegration:
    """Test spatial adapter registry integration with complete flow"""

    @pytest.mark.asyncio
    async def test_complete_flow_with_registry(self):
        """Test complete flow using spatial adapter registry"""
        # Arrange
        from services.integrations.spatial_adapter import SpatialAdapterRegistry

        registry = SpatialAdapterRegistry()
        slack_adapter = SlackSpatialAdapter()
        registry.register_adapter("slack", slack_adapter)

        # Create webhook router with registry
        router = SlackWebhookRouter(spatial_adapter=slack_adapter)

        event = {
            "type": "app_mention",
            "channel": "C789012",
            "ts": "1234567890.123456",
            "user": "U123456",
            "text": "<@U123456> Hello Piper!",
        }
        team_id = "T123456"

        # Mock response handler
        mock_response_result = {"status": "sent", "channel": "C789012"}
        router.response_handler.handle_spatial_event = AsyncMock(return_value=mock_response_result)

        # Act
        await router._process_mention_event(event, team_id)

        # Assert
        # Check registry has the mapping
        position = await registry.map_to_position(
            "slack", "1234567890.123456", {"territory_id": team_id, "room_id": "C789012"}
        )
        assert position is not None
        assert position.position == 1

        # Check reverse mapping works
        timestamp = await registry.map_from_position("slack", position)
        assert timestamp == "1234567890.123456"

        # Check response handler was called
        router.response_handler.handle_spatial_event.assert_called_once()
