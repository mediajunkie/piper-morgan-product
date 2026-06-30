"""
Slack Spatial Adapter
Slack-specific implementation of the spatial adapter interface.

Maps Slack timestamps and identifiers to integer spatial positions
for use within Piper Morgan's spatial metaphor system.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from services.domain.models import SpatialContext as DomainSpatialContext
from services.domain.models import SpatialEvent, SpatialObject
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

logger = logging.getLogger(__name__)


class SlackSpatialAdapter(BaseSpatialAdapter):
    """
    Slack-specific spatial adapter implementation.

    Maps Slack timestamps and identifiers to integer spatial positions,
    providing bidirectional mapping and context storage for response routing.
    """

    def __init__(self):
        super().__init__("slack")
        self._lock = asyncio.Lock()
        self._timestamp_to_position: Dict[str, int] = {}
        self._position_to_timestamp: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        logger.info("SlackSpatialAdapter initialized")

    async def map_to_position(self, external_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """
        Map Slack timestamp to spatial position.

        Args:
            external_id: Slack timestamp (e.g., "1234567890.123456")
            context: Additional context including channel, thread, user info

        Returns:
            SpatialPosition with integer position and context
        """
        async with self._lock:
            # Check if mapping already exists
            if external_id in self._mappings:
                return self._mappings[external_id]

            # Create new spatial position
            position = self._create_spatial_position(external_id, context)

            # Store bidirectional mapping
            self._timestamp_to_position[external_id] = position.position
            self._position_to_timestamp[position.position] = external_id

            # Store context for response routing
            self._store_context_for_routing(external_id, context)

            # Store mapping in parent class _mappings (no deadlock)
            self._mappings[external_id] = position

            logger.debug(f"Mapped Slack timestamp {external_id} to position {position.position}")
            return position

    async def map_from_position(self, position: SpatialPosition) -> Optional[str]:
        """
        Map spatial position back to Slack timestamp.

        Args:
            position: Spatial position to reverse map

        Returns:
            Slack timestamp if mapping exists, None otherwise
        """
        async with self._lock:
            return self._position_to_timestamp.get(position.position)

    async def store_mapping(self, external_id: str, position: SpatialPosition) -> bool:
        """
        Store mapping between Slack timestamp and spatial position.

        Args:
            external_id: Slack timestamp
            position: Spatial position to map to

        Returns:
            True if mapping stored successfully, False otherwise
        """
        try:
            async with self._lock:
                self._mappings[external_id] = position
                self._timestamp_to_position[external_id] = position.position
                self._position_to_timestamp[position.position] = external_id
                return True
        except Exception as e:
            logger.error(f"Failed to store mapping for {external_id}: {e}")
            return False

    async def get_context(self, external_id: str) -> Optional[SpatialContext]:
        """
        Get spatial context for Slack timestamp.

        Args:
            external_id: Slack timestamp

        Returns:
            SpatialContext if mapping exists, None otherwise
        """
        async with self._lock:
            if external_id not in self._context_storage:
                return None

            context_data = self._context_storage[external_id]

            return SpatialContext(
                territory_id=context_data.get("territory_id", ""),
                room_id=context_data.get("room_id", ""),
                path_id=context_data.get("path_id"),
                object_position=self._timestamp_to_position.get(external_id),
                attention_level=context_data.get("attention_level", "medium"),
                emotional_valence=context_data.get("emotional_valence", "neutral"),
                navigation_intent=context_data.get("navigation_intent", "monitor"),
                external_system="slack",
                external_id=external_id,
                external_context=context_data,
            )

    async def create_spatial_event_from_slack(
        self, slack_timestamp: str, event_type: str, context: Dict[str, Any]
    ) -> SpatialEvent:
        """
        Create SpatialEvent from Slack timestamp using adapter.

        Args:
            slack_timestamp: Slack message timestamp
            event_type: Type of spatial event
            context: Additional context for the event

        Returns:
            SpatialEvent with integer positioning
        """
        # Map timestamp to spatial position
        position = await self.map_to_position(slack_timestamp, context)

        # Extract spatial coordinates from context with proper mapping
        # Handle both integer positions and string IDs
        territory_position = context.get("territory_position", 0)
        if isinstance(territory_position, str):
            # Convert territory_id to integer position (simple hash for now)
            territory_position = hash(territory_position) % 1000

        room_position = context.get("room_position", 0)
        if isinstance(room_position, str):
            # Convert room_id to integer position (simple hash for now)
            room_position = hash(room_position) % 1000
        elif "room_id" in context and not room_position:
            # Use room_id if room_position not provided
            room_position = hash(context["room_id"]) % 1000

        path_position = context.get("path_position")
        if isinstance(path_position, str):
            # Convert path_id to integer position
            path_position = hash(path_position) % 1000

        object_position = position.position

        # Create spatial event with integer positioning
        spatial_event = SpatialEvent(
            event_type=event_type,
            territory_position=territory_position,
            room_position=room_position,
            path_position=path_position,
            object_position=object_position,
            actor_id=context.get("user_id"),
            affected_objects=context.get("affected_objects", []),
            spatial_changes=context.get("spatial_changes", {}),
            event_time=self._parse_slack_timestamp(slack_timestamp),
            significance_level=context.get("significance_level", "routine"),
        )

        logger.debug(f"Created SpatialEvent from Slack timestamp {slack_timestamp}")
        return spatial_event

    async def create_spatial_object_from_slack(
        self, slack_timestamp: str, object_type: str, context: Dict[str, Any]
    ) -> SpatialObject:
        """
        Create SpatialObject from Slack timestamp using adapter.

        Args:
            slack_timestamp: Slack message timestamp
            object_type: Type of spatial object
            context: Additional context for the object

        Returns:
            SpatialObject with integer positioning
        """
        # Map timestamp to spatial position
        position = await self.map_to_position(slack_timestamp, context)

        # Extract spatial coordinates from context
        territory_position = context.get("territory_position", 0)
        room_position = context.get("room_position", 0)
        path_position = context.get("path_position")
        object_position = position.position

        # Create spatial object with integer positioning
        spatial_object = SpatialObject(
            object_type=object_type,
            territory_position=territory_position,
            room_position=room_position,
            path_position=path_position,
            object_position=object_position,
            content=context.get("content", ""),
            creator_id=context.get("user_id", ""),
            size_category=context.get("size_category", "standard"),
            attention_attractors=context.get("attention_attractors", []),
            emotional_markers=context.get("emotional_markers", []),
            connected_objects=context.get("connected_objects", []),
            placement_time=self._parse_slack_timestamp(slack_timestamp),
            interaction_count=context.get("interaction_count", 0),
        )

        logger.debug(f"Created SpatialObject from Slack timestamp {slack_timestamp}")
        return spatial_object

    async def get_response_context(self, slack_timestamp: str) -> Optional[Dict[str, Any]]:
        """
        Get context for response routing to Slack.

        Args:
            slack_timestamp: Slack message timestamp

        Returns:
            Context dictionary for response routing, None if not found
        """
        async with self._lock:
            if slack_timestamp not in self._context_storage:
                return None

            context = self._context_storage[slack_timestamp]

            return {
                "channel_id": context.get("room_id") or context.get("original_channel_id"),
                "thread_ts": context.get("path_id") or context.get("thread_ts"),
                "workspace_id": context.get("territory_id"),
                "user_id": context.get("user_id"),
                # #1110: connector-owner Piper user_id, distinct from the sender's
                # Slack user_id above. The response handler uses it to resolve
                # outbound bot credentials (SlackConfigService.get_config).
                "connector_user_id": context.get("connector_user_id"),
                "attention_level": context.get("attention_level", "medium"),
                "navigation_intent": context.get("navigation_intent", "monitor"),
                "content": context.get("content", ""),
                # Issue #1081: Notion URL unfurling — preserve refs through the
                # spatial-adapter round-trip so the response handler can render
                # Notion document context alongside the Slack reply.
                "notion_refs": context.get("notion_refs", []),
            }

    def _store_context_for_routing(self, external_id: str, context: Dict[str, Any]) -> None:
        """Store context for response routing"""
        self._context_storage[external_id] = context.copy()

    def _parse_slack_timestamp(self, timestamp: str) -> Optional[datetime]:
        """Parse Slack timestamp to datetime object"""
        try:
            if not timestamp:
                return None

            # Slack timestamps are Unix timestamps with decimals
            timestamp_float = float(timestamp)
            return datetime.fromtimestamp(timestamp_float)
        except (ValueError, TypeError) as e:
            logger.warning(f"Failed to parse Slack timestamp: {timestamp}")
            return None

    async def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about current mappings"""
        async with self._lock:
            # Parent's get_mapping_stats is sync, don't await
            stats = super().get_mapping_stats()
            stats.update(
                {
                    "timestamp_mappings": len(self._timestamp_to_position),
                    "position_mappings": len(self._position_to_timestamp),
                    "context_entries": len(self._context_storage),
                }
            )
            return stats

    async def cleanup_old_mappings(self, max_age_hours: int = 24) -> int:
        """
        Clean up old mappings to prevent memory bloat.

        Args:
            max_age_hours: Maximum age in hours before mapping is considered stale

        Returns:
            Number of mappings removed
        """
        async with self._lock:
            current_time = datetime.now()
            cutoff_time = current_time.timestamp() - (max_age_hours * 3600)

            removed_count = 0

            # Find old timestamps
            old_timestamps = []
            for timestamp_str in self._timestamp_to_position.keys():
                try:
                    timestamp_float = float(timestamp_str)
                    if timestamp_float < cutoff_time:
                        old_timestamps.append(timestamp_str)
                except (ValueError, TypeError):
                    # Invalid timestamp, remove it
                    old_timestamps.append(timestamp_str)

            # Remove old mappings
            for timestamp in old_timestamps:
                position = self._timestamp_to_position.get(timestamp)
                if position:
                    del self._position_to_timestamp[position]
                del self._timestamp_to_position[timestamp]
                del self._mappings[timestamp]
                if timestamp in self._context_storage:
                    del self._context_storage[timestamp]
                removed_count += 1

            if removed_count > 0:
                logger.info(f"Cleaned up {removed_count} old Slack spatial mappings")

            return removed_count
