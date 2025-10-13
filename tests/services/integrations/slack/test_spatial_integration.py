"""
Tests for Slack Spatial Integration
Tests event processing through spatial metaphors and Piper's spatial awareness.
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.integrations.slack.config_service import SlackConfigService
from services.integrations.slack.event_handler import (
    EventProcessingResult,
    EventType,
    SlackEvent,
    SlackEventHandler,
)
from services.integrations.slack.spatial_agent import (
    NavigationDecision,
    NavigationIntent,
    SlackSpatialAgent,
    SpatialAwarenessLevel,
    SpatialAwarenessState,
    SpatialMemory,
)
from services.integrations.slack.spatial_types import (
    AttentionAttractor,
    AttentionLevel,
    EmotionalMarker,
    EmotionalValence,
    SpatialCoordinates,
    SpatialEvent,
)


class TestSlackEventHandler:
    """Test Slack event handler with spatial mapping"""

    @pytest.fixture
    def config_service(self):
        """Mock config service"""
        return Mock(spec=SlackConfigService)

    @pytest.fixture
    def event_handler(self, config_service):
        """Event handler instance"""
        return SlackEventHandler(config_service)

    @pytest.fixture
    def mock_spatial_mapper(self):
        """Mock spatial mapper"""
        mapper = Mock()
        mapper.map_message_to_spatial_object = AsyncMock()
        mapper.map_reaction_to_emotional_marker = AsyncMock()
        mapper.map_mention_to_attention_attractor = AsyncMock()
        mapper.map_channel_to_room = AsyncMock()
        return mapper

    @patch("services.integrations.slack.event_handler.SlackSpatialMapper")
    async def test_process_message_event(
        self, mock_mapper_class, event_handler, mock_spatial_mapper
    ):
        """Test processing message event through spatial metaphors"""
        mock_mapper_class.return_value = mock_spatial_mapper

        # Mock spatial object
        mock_spatial_object = Mock()
        mock_spatial_mapper.map_message_to_spatial_object.return_value = mock_spatial_object

        # Test message event
        message_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Hello world",
            "team": "T123456",
        }

        result = await event_handler.process_event(message_event)

        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "message_placed"
        assert result.attention_level == AttentionLevel.LOW
        assert result.emotional_valence == EmotionalValence.NEUTRAL
        assert len(result.spatial_changes) == 1
        assert result.spatial_changes[0]["type"] == "message_placed"

    @patch("services/integrations/slack.event_handler.SlackSpatialMapper")
    async def test_process_mention_event(
        self, mock_mapper_class, event_handler, mock_spatial_mapper
    ):
        """Test processing mention event as attention attractor"""
        mock_mapper_class.return_value = mock_spatial_mapper

        # Mock attention attractor
        mock_attractor = Mock()
        mock_spatial_mapper.map_mention_to_attention_attractor.return_value = mock_attractor

        # Test mention event
        mention_event = {
            "type": "app_mention",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "<@U123456> help me with this",
            "team": "T123456",
        }

        result = await event_handler.process_event(mention_event)

        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "attention_attracted"
        assert result.attention_level == AttentionLevel.HIGH
        assert result.emotional_valence == EmotionalValence.POSITIVE
        assert len(result.navigation_suggestions) == 1
        assert "Navigate to room" in result.navigation_suggestions[0]

    @patch("services.integrations.slack.event_handler.SlackSpatialMapper")
    def test_process_reaction_event(self, mock_mapper_class, event_handler, mock_spatial_mapper):
        """Test processing reaction event as emotional marker"""
        mock_mapper_class.return_value = mock_spatial_mapper

        # Mock emotional marker
        mock_marker = Mock()
        mock_marker.valence = EmotionalValence.POSITIVE
        mock_spatial_mapper.map_reaction_to_emotional_marker.return_value = mock_marker

        # Test reaction event
        reaction_event = {
            "type": "reaction_added",
            "reaction": "thumbsup",
            "item": {"type": "message", "channel": "C123456", "ts": "1234567890.123456"},
            "team": "T123456",
        }

        result = await event_handler.process_event(reaction_event)

        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "emotional_marker_updated"
        assert result.attention_level == AttentionLevel.MEDIUM
        assert result.emotional_valence == EmotionalValence.POSITIVE

    def test_process_unsupported_event(self, event_handler):
        """Test processing unsupported event type"""
        unsupported_event = {"type": "unsupported_event_type", "data": "some data"}

        result = await event_handler.process_event(unsupported_event)

        assert result.success is False
        assert "Unsupported event type" in result.error

    def test_get_spatial_state(self, event_handler):
        """Test getting spatial state"""
        state = event_handler.get_spatial_state()
        assert isinstance(state, dict)
        assert "rooms" in state
        assert "objects" in state
        assert "attention_attractors" in state
        assert "emotional_markers" in state

    def test_get_recent_events(self, event_handler):
        """Test getting recent events"""
        events = event_handler.get_recent_events(limit=5)
        assert isinstance(events, list)
        assert len(events) <= 5


class TestSlackSpatialAgent:
    """Test Piper's spatial awareness and navigation agent"""

    @pytest.fixture
    def config_service(self):
        """Mock config service"""
        return Mock(spec=SlackConfigService)

    @pytest.fixture
    def event_handler(self, config_service):
        """Mock event handler"""
        return Mock(spec=SlackEventHandler)

    @pytest.fixture
    def spatial_agent(self, config_service, event_handler):
        """Spatial agent instance"""
        return SlackSpatialAgent(config_service, event_handler)

    def test_process_spatial_event_no_event(self, spatial_agent):
        """Test processing spatial event with no valid event"""
        result = EventProcessingResult(success=False, spatial_event=None, error="No event")

        decision = await spatial_agent.process_spatial_event(result)

        assert decision.intent == NavigationIntent.MONITOR
        assert decision.confidence == 0.0
        assert "No valid spatial event" in decision.reasoning

    def test_process_high_attention_event(self, spatial_agent):
        """Test processing high attention event"""
        # Create mock spatial event
        spatial_event = Mock()
        spatial_event.coordinates = Mock()
        spatial_event.coordinates.room_id = "C123456"
        spatial_event.event_type = "attention_attracted"

        result = EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            attention_level=AttentionLevel.HIGH,
            emotional_valence=EmotionalValence.POSITIVE,
        )

        decision = await spatial_agent.process_spatial_event(result)

        assert decision.intent == NavigationIntent.RESPOND
        assert decision.target_room == "C123456"
        assert decision.confidence == 0.9
        assert decision.urgency == 0.9
        assert "requires immediate response" in decision.reasoning

    def test_process_emotional_event(self, spatial_agent):
        """Test processing emotional event"""
        # Create mock spatial event
        spatial_event = Mock()
        spatial_event.coordinates = Mock()
        spatial_event.coordinates.room_id = "C123456"
        spatial_event.event_type = "emotional_marker_updated"

        result = EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            attention_level=AttentionLevel.MEDIUM,
            emotional_valence=EmotionalValence.NEGATIVE,
        )

        decision = await spatial_agent.process_spatial_event(result)

        assert decision.intent == NavigationIntent.INVESTIGATE
        assert decision.target_room == "C123456"
        assert decision.confidence == 0.7
        assert decision.urgency == 0.6
        assert "requires investigation" in decision.reasoning

    def test_process_new_room_event(self, spatial_agent):
        """Test processing new room creation event"""
        # Create mock spatial event
        spatial_event = Mock()
        spatial_event.coordinates = Mock()
        spatial_event.coordinates.room_id = "C789012"
        spatial_event.event_type = "room_created"

        result = EventProcessingResult(
            success=True,
            spatial_event=spatial_event,
            attention_level=AttentionLevel.LOW,
            emotional_valence=EmotionalValence.NEUTRAL,
        )

        decision = await spatial_agent.process_spatial_event(result)

        assert decision.intent == NavigationIntent.EXPLORE
        assert decision.target_room == "C789012"
        assert decision.confidence == 0.8
        assert decision.urgency == 0.5
        assert "exploring new territory" in decision.reasoning

    def test_get_spatial_summary(self, spatial_agent):
        """Test getting spatial summary"""
        summary = spatial_agent.get_spatial_summary()

        assert isinstance(summary, dict)
        assert "current_position" in summary
        assert "spatial_memories" in summary
        assert "attention_focus" in summary
        assert "emotional_state" in summary
        assert "navigation_history" in summary
        assert "last_activity" in summary

    def test_get_navigation_suggestions(self, spatial_agent):
        """Test getting navigation suggestions"""
        # Add some test data to spatial state
        spatial_agent.spatial_state.attention_focus = [
            Mock(level=AttentionLevel.HIGH),
            Mock(level=AttentionLevel.MEDIUM),
        ]

        spatial_agent.spatial_state.spatial_memories = {
            "C123456": SpatialMemory(
                room_id="C123456",
                room_name="Test Room",
                last_visited=datetime.now() - timedelta(minutes=20),
                recent_activity=[{"type": "message", "timestamp": datetime.now()}],
            )
        }

        suggestions = spatial_agent.get_navigation_suggestions()

        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        assert any("high-priority attention attractors" in suggestion for suggestion in suggestions)
        assert any("rooms with recent activity" in suggestion for suggestion in suggestions)

    def test_clear_attention_focus(self, spatial_agent):
        """Test clearing attention focus"""
        # Add test attention attractors
        attractor1 = Mock()
        attractor1.coordinates.room_id = "C123456"
        attractor2 = Mock()
        attractor2.coordinates.room_id = "C789012"

        spatial_agent.spatial_state.attention_focus = [attractor1, attractor2]

        # Clear specific room
        spatial_agent.clear_attention_focus("C123456")
        assert len(spatial_agent.spatial_state.attention_focus) == 1
        assert spatial_agent.spatial_state.attention_focus[0] == attractor2

        # Clear all
        spatial_agent.clear_attention_focus()
        assert len(spatial_agent.spatial_state.attention_focus) == 0


class TestSpatialIntegration:
    """Integration tests for spatial metaphor processing"""

    @pytest.fixture
    def config_service(self):
        """Mock config service"""
        return Mock(spec=SlackConfigService)

    @pytest.fixture
    def event_handler(self, config_service):
        """Event handler with mocked spatial mapper"""
        handler = SlackEventHandler(config_service)

        # Mock spatial mapper methods
        handler.spatial_mapper.map_message_to_spatial_object = AsyncMock(return_value=Mock())
        handler.spatial_mapper.map_reaction_to_emotional_marker = AsyncMock(return_value=Mock())
        handler.spatial_mapper.map_mention_to_attention_attractor = AsyncMock(return_value=Mock())
        handler.spatial_mapper.map_channel_to_room = AsyncMock(return_value=Mock())

        return handler

    @pytest.fixture
    def spatial_agent(self, config_service, event_handler):
        """Spatial agent with mocked dependencies"""
        return SlackSpatialAgent(config_service, event_handler)

    async def test_end_to_end_message_processing(self, event_handler, spatial_agent):
        """Test end-to-end message processing through spatial metaphors"""
        # Process message event
        message_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Hello world",
            "team": "T123456",
        }

        event_result = await event_handler.process_event(message_event)

        # Process through spatial agent
        navigation_decision = await spatial_agent.process_spatial_event(event_result)

        # Verify results
        assert event_result.success is True
        assert event_result.spatial_event is not None
        assert navigation_decision.intent == NavigationIntent.MONITOR
        assert navigation_decision.target_room == "C123456"

    async def test_end_to_end_mention_processing(self, event_handler, spatial_agent):
        """Test end-to-end mention processing through spatial metaphors"""
        # Process mention event
        mention_event = {
            "type": "app_mention",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "<@U123456> help me",
            "team": "T123456",
        }

        event_result = await event_handler.process_event(mention_event)

        # Process through spatial agent
        navigation_decision = await spatial_agent.process_spatial_event(event_result)

        # Verify results
        assert event_result.success is True
        assert event_result.spatial_event is not None
        assert navigation_decision.intent == NavigationIntent.RESPOND
        assert navigation_decision.target_room == "C123456"
        assert navigation_decision.confidence == 0.9
