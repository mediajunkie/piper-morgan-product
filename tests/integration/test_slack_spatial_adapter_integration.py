"""
Test Slack Spatial Adapter Integration
Tests the integration between Slack spatial adapter and webhook router.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import SpatialEvent, SpatialObject
from services.integrations.slack.spatial_adapter import SlackSpatialAdapter

# #1499 Class 2 member strip (2026-09-23): TestWebhookRouterIntegration (which
# lived here, exercising SlackWebhookRouter._process_message_event /
# _process_mention_event / _process_reaction_event / _determine_emotional_valence)
# was removed — those methods were dead code, reachable only from the unmounted
# Events API FastAPI route, never from Socket Mode. See
# docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md.


class TestSlackSpatialAdapter:
    """Test Slack spatial adapter functionality"""

    @pytest.mark.asyncio
    async def test_slack_adapter_creation(self):
        """Test creating Slack spatial adapter"""
        # Act
        adapter = SlackSpatialAdapter()

        # Assert
        assert adapter.system_name == "slack"
        assert adapter._timestamp_to_position == {}
        assert adapter._position_to_timestamp == {}
        assert adapter._context_storage == {}

    @pytest.mark.asyncio
    async def test_map_slack_timestamp_to_position(self):
        """Test mapping Slack timestamp to spatial position"""
        # Arrange
        adapter = SlackSpatialAdapter()
        slack_timestamp = "1234567890.123456"
        context = {
            "territory_id": "T123456",
            "room_id": "C789012",
            "user_id": "U123456",
            "attention_level": "high",
        }

        # Act
        position = await adapter.map_to_position(slack_timestamp, context)

        # Assert
        assert isinstance(position, SpatialPosition)
        assert position.position == 1  # First position
        assert position.context["external_id"] == slack_timestamp
        assert position.context["external_system"] == "slack"
        assert position.context["spatial_context"]["territory_id"] == "T123456"
        assert position.context["spatial_context"]["room_id"] == "C789012"

    @pytest.mark.asyncio
    async def test_bidirectional_mapping(self):
        """Test bidirectional mapping between timestamp and position"""
        # Arrange
        adapter = SlackSpatialAdapter()
        slack_timestamp = "1234567890.123456"
        context = {"territory_id": "T123456", "room_id": "C789012"}

        # Act - Map timestamp to position
        position = await adapter.map_to_position(slack_timestamp, context)

        # Act - Map position back to timestamp
        mapped_timestamp = await adapter.map_from_position(position)

        # Assert
        assert mapped_timestamp == slack_timestamp
        assert adapter._timestamp_to_position[slack_timestamp] == position.position
        assert adapter._position_to_timestamp[position.position] == slack_timestamp

    @pytest.mark.asyncio
    async def test_create_spatial_event_from_slack(self):
        """Test creating spatial event from Slack timestamp"""
        # Arrange
        adapter = SlackSpatialAdapter()
        slack_timestamp = "1234567890.123456"
        event_type = "message_posted"
        context = {
            "territory_id": "T123456",
            "room_id": "C789012",
            "user_id": "U123456",
            "content": "Hello world",
            "attention_level": "medium",
            "significance_level": "routine",
        }

        # Act
        spatial_event = await adapter.create_spatial_event_from_slack(
            slack_timestamp, event_type, context
        )

        # Assert
        assert isinstance(spatial_event, SpatialEvent)
        assert spatial_event.event_type == event_type
        assert spatial_event.territory_position == 0  # Default from context
        assert spatial_event.room_position == 0  # Default from context
        assert spatial_event.object_position == 1  # First position
        assert spatial_event.actor_id == "U123456"
        assert spatial_event.significance_level == "routine"

    @pytest.mark.asyncio
    async def test_create_spatial_object_from_slack(self):
        """Test creating spatial object from Slack timestamp"""
        # Arrange
        adapter = SlackSpatialAdapter()
        slack_timestamp = "1234567890.123456"
        object_type = "text_message"
        context = {
            "territory_id": "T123456",
            "room_id": "C789012",
            "user_id": "U123456",
            "content": "Hello world",
            "size_category": "standard",
        }

        # Act
        spatial_object = await adapter.create_spatial_object_from_slack(
            slack_timestamp, object_type, context
        )

        # Assert
        assert isinstance(spatial_object, SpatialObject)
        assert spatial_object.object_type == object_type
        assert spatial_object.territory_position == 0  # Default from context
        assert spatial_object.room_position == 0  # Default from context
        assert spatial_object.object_position == 1  # First position
        assert spatial_object.content == "Hello world"
        assert spatial_object.creator_id == "U123456"
        assert spatial_object.size_category == "standard"

    @pytest.mark.asyncio
    async def test_get_response_context(self):
        """Test getting response context for Slack routing"""
        # Arrange
        adapter = SlackSpatialAdapter()
        slack_timestamp = "1234567890.123456"
        context = {
            "territory_id": "T123456",
            "room_id": "C789012",
            "path_id": "1234567890.123457",
            "user_id": "U123456",
            "attention_level": "high",
            "navigation_intent": "respond",
        }

        # Act - Create mapping first
        await adapter.map_to_position(slack_timestamp, context)

        # Act - Get response context
        response_context = await adapter.get_response_context(slack_timestamp)

        # Assert
        assert response_context is not None
        assert response_context["channel_id"] == "C789012"
        assert response_context["thread_ts"] == "1234567890.123457"
        assert response_context["workspace_id"] == "T123456"
        assert response_context["user_id"] == "U123456"
        assert response_context["attention_level"] == "high"
        assert response_context["navigation_intent"] == "respond"

    @pytest.mark.asyncio
    async def test_parse_slack_timestamp(self):
        """Test parsing Slack timestamp to datetime"""
        # Arrange
        adapter = SlackSpatialAdapter()
        slack_timestamp = "1234567890.123456"

        # Act
        parsed_time = adapter._parse_slack_timestamp(slack_timestamp)

        # Assert
        assert isinstance(parsed_time, datetime)
        assert parsed_time.timestamp() == pytest.approx(1234567890.123456, abs=1)

    @pytest.mark.asyncio
    async def test_cleanup_old_mappings(self):
        """Test cleaning up old mappings"""
        # Arrange
        adapter = SlackSpatialAdapter()
        old_timestamp = "1234567890.123456"  # Old timestamp
        new_timestamp = str(datetime.now().timestamp())  # Current timestamp

        context = {"territory_id": "T123456", "room_id": "C789012"}

        # Act - Create mappings
        await adapter.map_to_position(old_timestamp, context)
        await adapter.map_to_position(new_timestamp, context)

        # Act - Clean up old mappings
        removed_count = await adapter.cleanup_old_mappings(max_age_hours=1)

        # Assert
        assert removed_count >= 1  # At least the old timestamp should be removed
        assert new_timestamp in adapter._timestamp_to_position  # New timestamp should remain


class TestSpatialAdapterRegistryIntegration:
    """Test spatial adapter registry with Slack adapter"""

    @pytest.mark.asyncio
    async def test_register_slack_adapter(self):
        """Test registering Slack adapter with registry"""
        # Arrange
        from services.integrations.spatial_adapter import SpatialAdapterRegistry

        registry = SpatialAdapterRegistry()
        slack_adapter = SlackSpatialAdapter()

        # Act
        registry.register_adapter("slack", slack_adapter)

        # Assert
        assert registry.get_adapter("slack") == slack_adapter
        assert "slack" in registry.list_adapters()

    @pytest.mark.asyncio
    async def test_map_through_registry(self):
        """Test mapping through registry with Slack adapter"""
        # Arrange
        from services.integrations.spatial_adapter import SpatialAdapterRegistry

        registry = SpatialAdapterRegistry()
        slack_adapter = SlackSpatialAdapter()
        registry.register_adapter("slack", slack_adapter)

        slack_timestamp = "1234567890.123456"
        context = {"territory_id": "T123456", "room_id": "C789012"}

        # Act
        position = await registry.map_to_position("slack", slack_timestamp, context)

        # Assert
        assert isinstance(position, SpatialPosition)
        assert position.position == 1
        assert position.context["external_id"] == slack_timestamp
