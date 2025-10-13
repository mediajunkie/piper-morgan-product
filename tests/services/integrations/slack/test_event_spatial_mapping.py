"""
Tests for Events → Spatial Mapping Integration
Tests the integration between Slack events and spatial metaphor conversions.

Following TDD principles: Write failing test → See it fail → Verify integration works → Make test pass
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.integrations.slack.config_service import SlackConfigService
from services.integrations.slack.event_handler import EventProcessingResult, SlackEventHandler
from services.integrations.slack.spatial_mapper import SlackSpatialMapper
from services.integrations.slack.spatial_types import (
    AttentionAttractor,
    AttentionLevel,
    EmotionalMarker,
    EmotionalValence,
    ObjectType,
    Room,
    RoomPurpose,
    SpatialCoordinates,
    SpatialEvent,
    SpatialObject,
    Territory,
    TerritoryType,
)


class TestEventSpatialMapping:
    """Test Slack events to spatial metaphor conversions"""

    @pytest.fixture
    def config_service(self):
        """Mock config service"""
        return Mock(spec=SlackConfigService)

    @pytest.fixture
    def event_handler(self, config_service):
        """Event handler instance"""
        return SlackEventHandler(config_service)

    @pytest.fixture
    def spatial_mapper(self):
        """Spatial mapper instance"""
        return SlackSpatialMapper()

    async def test_message_event_maps_to_spatial_object(self, event_handler, spatial_mapper):
        """Test that message events map to spatial objects"""
        # Arrange
        message_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Hello world",
            "team": "T123456",
            "user": "U123456",
        }

        # Act
        result = await event_handler.process_event(message_event)

        # Assert
        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "message_placed"
        assert result.spatial_event.coordinates.room_id == "C123456"
        assert result.spatial_event.coordinates.territory_id == "T123456"
        assert result.spatial_event.coordinates.object_id == "1234567890.123456"

    async def test_mention_event_maps_to_attention_attractor(self, event_handler, spatial_mapper):
        """Test that mention events map to attention attractors"""
        # Arrange
        mention_event = {
            "type": "app_mention",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "<@U123456> help me with this bug",
            "team": "T123456",
            "user": "U789012",
        }

        # Act
        result = await event_handler.process_event(mention_event)

        # Assert
        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "attention_attracted"
        assert result.attention_level == AttentionLevel.HIGH
        assert result.spatial_event.attention_attractor is not None
        assert result.spatial_event.attention_attractor.level == AttentionLevel.HIGH

    async def test_reaction_event_maps_to_emotional_marker(self, event_handler, spatial_mapper):
        """Test that reaction events map to emotional markers"""
        # Arrange
        reaction_event = {
            "type": "reaction_added",
            "reaction": "thumbsup",
            "item": {"type": "message", "channel": "C123456", "ts": "1234567890.123456"},
            "team": "T123456",
            "user": "U123456",
        }

        # Act
        result = await event_handler.process_event(reaction_event)

        # Assert
        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "emotional_marker_updated"
        assert result.spatial_event.emotional_marker is not None
        assert result.spatial_event.emotional_marker.reaction == "thumbsup"
        assert result.emotional_valence in [EmotionalValence.POSITIVE, EmotionalValence.NEUTRAL]

    def test_channel_created_event_maps_to_room(self, event_handler, spatial_mapper):
        """Test that channel creation events map to rooms"""
        # Arrange
        channel_event = {
            "type": "channel_created",
            "channel": {"id": "C789012", "name": "new-channel", "creator": "U123456"},
            "team": "T123456",
        }

        # Act
        result = await event_handler.process_event(channel_event)

        # Assert
        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "room_created"
        assert result.spatial_event.coordinates.room_id == "C789012"
        assert result.spatial_event.room is not None
        assert result.spatial_event.room.room_id == "C789012"
        assert result.spatial_event.room.name == "new-channel"

    def test_thread_event_maps_to_conversational_path(self, event_handler, spatial_mapper):
        """Test that thread events map to conversational paths"""
        # Arrange
        thread_event = {
            "type": "thread_created",
            "channel": "C123456",
            "thread_ts": "1234567890.123456",
            "ts": "1234567890.123457",
            "team": "T123456",
        }

        # Act
        result = await event_handler.process_event(thread_event)

        # Assert
        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "conversational_path_created"
        assert result.spatial_event.coordinates.path_id == "1234567890.123456"
        assert result.spatial_event.coordinates.room_id == "C123456"

    def test_user_joined_event_updates_spatial_state(self, event_handler, spatial_mapper):
        """Test that user joined events update spatial state"""
        # Arrange
        user_event = {
            "type": "user_joined",
            "channel": "C123456",
            "user": "U123456",
            "team": "T123456",
        }

        # Act
        result = await event_handler.process_event(user_event)

        # Assert
        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "inhabitant_joined"
        assert result.spatial_event.coordinates.room_id == "C123456"

    def test_negative_reaction_maps_to_negative_emotional_marker(
        self, event_handler, spatial_mapper
    ):
        """Test that negative reactions map to negative emotional markers"""
        # Arrange
        negative_reaction_event = {
            "type": "reaction_added",
            "reaction": "thumbsdown",
            "item": {"type": "message", "channel": "C123456", "ts": "1234567890.123456"},
            "team": "T123456",
            "user": "U123456",
        }

        # Act
        result = await event_handler.process_event(negative_reaction_event)

        # Assert
        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "emotional_marker_updated"
        assert result.spatial_event.emotional_marker.reaction == "thumbsdown"
        assert result.emotional_valence == EmotionalValence.NEGATIVE

    def test_channel_deleted_event_removes_room(self, event_handler, spatial_mapper):
        """Test that channel deletion events remove rooms from spatial state"""
        # Arrange
        channel_deleted_event = {"type": "channel_deleted", "channel": "C789012", "team": "T123456"}

        # Act
        result = await event_handler.process_event(channel_deleted_event)

        # Assert
        assert result.success is True
        assert result.spatial_event is not None
        assert result.spatial_event.event_type == "room_deleted"
        assert result.spatial_event.coordinates.room_id == "C789012"

    def test_multiple_events_update_spatial_state_sequentially(self, event_handler, spatial_mapper):
        """Test that multiple events update spatial state sequentially"""
        # Arrange
        events = [
            {
                "type": "message",
                "channel": "C123456",
                "ts": "1234567890.123456",
                "text": "First message",
                "team": "T123456",
            },
            {
                "type": "app_mention",
                "channel": "C123456",
                "ts": "1234567890.123457",
                "text": "<@U123456> help",
                "team": "T123456",
            },
            {
                "type": "reaction_added",
                "reaction": "heart",
                "item": {"type": "message", "channel": "C123456", "ts": "1234567890.123456"},
                "team": "T123456",
            },
        ]

        # Act
        results = []
        for event in events:
            result = await event_handler.process_event(event)
            results.append(result)

        # Assert
        assert len(results) == 3
        assert all(result.success for result in results)
        assert results[0].spatial_event.event_type == "message_placed"
        assert results[1].spatial_event.event_type == "attention_attracted"
        assert results[2].spatial_event.event_type == "emotional_marker_updated"

        # Check spatial state has been updated
        spatial_state = event_handler.get_spatial_state()
        assert "objects" in spatial_state
        assert "attention_attractors" in spatial_state
        assert "emotional_markers" in spatial_state

    def test_unsupported_event_returns_error(self, event_handler, spatial_mapper):
        """Test that unsupported events return error"""
        # Arrange
        unsupported_event = {"type": "unsupported_event_type", "data": "some data"}

        # Act
        result = await event_handler.process_event(unsupported_event)

        # Assert
        assert result.success is False
        assert "Unsupported event type" in result.error

    def test_spatial_coordinates_are_consistent(self, event_handler, spatial_mapper):
        """Test that spatial coordinates are consistent across events"""
        # Arrange
        message_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Test message",
            "team": "T123456",
        }

        # Act
        result = await event_handler.process_event(message_event)
        coords = result.spatial_event.coordinates

        # Assert
        assert coords.territory_id == "T123456"
        assert coords.room_id == "C123456"
        assert coords.object_id == "1234567890.123456"
        assert coords.path_id is None  # No thread

    def test_spatial_event_timestamps_are_preserved(self, event_handler, spatial_mapper):
        """Test that spatial event timestamps are preserved"""
        # Arrange
        message_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Test message",
            "team": "T123456",
        }

        # Act
        result = await event_handler.process_event(message_event)
        spatial_event = result.spatial_event

        # Assert
        assert spatial_event.timestamp is not None
        assert isinstance(spatial_event.timestamp, datetime)

    def test_spatial_changes_are_tracked(self, event_handler, spatial_mapper):
        """Test that spatial changes are tracked in results"""
        # Arrange
        message_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Test message",
            "team": "T123456",
        }

        # Act
        result = await event_handler.process_event(message_event)

        # Assert
        assert len(result.spatial_changes) > 0
        assert result.spatial_changes[0]["type"] == "message_placed"
        assert result.spatial_changes[0]["room_id"] == "C123456"
        assert result.spatial_changes[0]["object_id"] == "1234567890.123456"
