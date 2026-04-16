"""
Slack Spatial Mapper - Core Spatial Metaphor Engine
Implements spatial metaphor mapping for Slack integration following GitHub pattern.

Transforms Slack API data into spatial metaphor representations enabling Piper Morgan
to navigate and understand Slack environments as physical spaces with:
- Workspaces as territories/buildings to navigate
- Channels as rooms with specific purposes and inhabitants
- Threads as conversational paths/corridors
- Messages as objects placed in rooms
- @mentions as attention attractors
- Reactions as emotional valence markers
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from .spatial_types import (
    AttentionAttractor,
    AttentionLevel,
    ConversationalPath,
    EmotionalMarker,
    EmotionalValence,
    ObjectType,
    PathType,
    Room,
    RoomPurpose,
    SpatialCoordinates,
    SpatialEvent,
    SpatialObject,
    Territory,
    TerritoryType,
)

logger = logging.getLogger(__name__)


class SlackSpatialMapper:
    """
    Core spatial metaphor engine for Slack integration.

    Transforms Slack API responses into spatial metaphor representations
    following the established GitHub integration patterns for configuration,
    error handling, and type safety.
    """

    def __init__(self):
        self._territory_cache: Dict[str, Territory] = {}
        self._room_cache: Dict[str, Room] = {}
        self._spatial_analytics: Dict[str, Any] = {
            "territories_mapped": 0,
            "rooms_mapped": 0,
            "objects_placed": 0,
            "events_processed": 0,
        }

    # Territory (Workspace) Mapping

    def map_workspace(self, slack_workspace: Dict[str, Any]) -> Territory:
        """
        Map Slack workspace to Territory spatial metaphor.

        Args:
            slack_workspace: Slack workspace API response

        Returns:
            Territory representation of workspace
        """
        try:
            workspace_id = slack_workspace.get("id", "")
            workspace_name = slack_workspace.get("name", "Unknown Territory")

            # Determine territory type from workspace characteristics
            territory_type = self._classify_territory_type(slack_workspace)

            # Extract spatial properties
            domain = slack_workspace.get("domain")

            # Build territory representation
            territory = Territory(
                id=workspace_id,
                name=workspace_name,
                territory_type=territory_type,
                domain=domain,
                total_rooms=0,  # Will be populated when rooms are mapped
                active_inhabitants=0,
                primary_language=self._detect_primary_language(slack_workspace),
                timezone_region=self._extract_timezone_region(slack_workspace),
                created_at=self._parse_slack_timestamp(slack_workspace.get("created")),
            )

            # Cache for spatial navigation
            self._territory_cache[workspace_id] = territory
            self._spatial_analytics["territories_mapped"] += 1

            logger.info(f"Mapped workspace {workspace_name} to {territory_type.value} territory")
            return territory

        except Exception as e:
            logger.error(f"Failed to map workspace to territory: {e}")
            raise ValueError(f"Workspace mapping failed: {e}") from e

    def _classify_territory_type(self, workspace: Dict[str, Any]) -> TerritoryType:
        """Classify workspace as territory type based on characteristics"""

        # Check for corporate indicators
        if workspace.get("enterprise_id") or workspace.get("is_org_shared"):
            return TerritoryType.CORPORATE

        # Check domain patterns for classification
        domain = (workspace.get("domain") or "").lower()

        if any(pattern in domain for pattern in ["community", "group", "club"]):
            return TerritoryType.COMMUNITY
        elif any(pattern in domain for pattern in ["project", "temp", "poc"]):
            return TerritoryType.PROJECT
        elif workspace.get("is_paid_plan", False):
            return TerritoryType.CORPORATE
        else:
            return TerritoryType.COMMUNITY

    def _detect_primary_language(self, workspace: Dict[str, Any]) -> str:
        """Detect primary language from workspace locale"""
        locale = workspace.get("locale", "en-US")
        return locale.split("-")[0] if "-" in locale else "en"

    def _extract_timezone_region(self, workspace: Dict[str, Any]) -> Optional[str]:
        """Extract timezone region from workspace data"""
        return workspace.get("timezone", None)

    # Room (Channel) Mapping

    def map_channel(self, slack_channel: Dict[str, Any], territory_id: str) -> Room:
        """
        Map Slack channel to Room spatial metaphor.

        Args:
            slack_channel: Slack channel API response
            territory_id: ID of containing territory

        Returns:
            Room representation of channel
        """
        try:
            channel_id = slack_channel.get("id", "")
            channel_name = slack_channel.get("name", "unnamed-room")

            # Determine room purpose from channel characteristics
            purpose = self._classify_room_purpose(slack_channel)

            # Extract room characteristics
            is_private = slack_channel.get("is_private", False)
            description = slack_channel.get("purpose", {}).get("value")
            topic = slack_channel.get("topic", {}).get("value")

            # Analyze inhabitant patterns
            member_count = slack_channel.get("num_members", 0)
            current_inhabitants = set(slack_channel.get("members", []))

            # Build room representation
            room = Room(
                id=channel_id,
                name=channel_name,
                territory_id=territory_id,
                purpose=purpose,
                is_private=is_private,
                description=description,
                topic=topic,
                current_inhabitants=current_inhabitants,
                activity_level=self._assess_activity_level(slack_channel),
                conversation_style=self._detect_conversation_style(slack_channel),
                created_at=self._parse_slack_timestamp(slack_channel.get("created")),
            )

            # Cache for spatial navigation
            self._room_cache[channel_id] = room
            self._spatial_analytics["rooms_mapped"] += 1

            logger.info(
                f"Mapped channel #{channel_name} to {purpose.value} room in territory {territory_id}"
            )
            return room

        except Exception as e:
            logger.error(f"Failed to map channel to room: {e}")
            raise ValueError(f"Channel mapping failed: {e}") from e

    async def map_channel_to_room(self, channel_data: Dict[str, Any]) -> Room:
        """
        Map Slack channel data to Room spatial metaphor (async wrapper for map_channel).

        This method adapts the synchronous map_channel() method for use in async event handling.
        It extracts the territory_id from the channel data and delegates to map_channel().

        Args:
            channel_data: Slack channel data from event

        Returns:
            Room representation of channel
        """
        # Extract territory ID from channel data
        territory_id = channel_data.get("team_id") or channel_data.get("team", "unknown")

        # Delegate to existing synchronous method
        return self.map_channel(slack_channel=channel_data, territory_id=territory_id)

    def _classify_room_purpose(self, channel: Dict[str, Any]) -> RoomPurpose:
        """Classify channel as room purpose based on characteristics"""

        channel_name = channel.get("name", "").lower()

        # Check for announcement patterns
        if any(pattern in channel_name for pattern in ["announce", "news", "updates"]):
            return RoomPurpose.ANNOUNCEMENT

        # Check for general/social patterns
        if channel_name in ["general", "random", "watercooler", "social"]:
            return RoomPurpose.GENERAL if channel_name == "general" else RoomPurpose.SOCIAL

        # Check for project work patterns
        if any(pattern in channel_name for pattern in ["project", "dev", "build", "sprint"]):
            return RoomPurpose.PROJECT_WORK

        # Check for coordination patterns
        if any(
            pattern in channel_name for pattern in ["standup", "sync", "coordination", "planning"]
        ):
            return RoomPurpose.COORDINATION

        # Check for support patterns
        if any(pattern in channel_name for pattern in ["help", "support", "questions", "tech"]):
            return RoomPurpose.SUPPORT

        # Check privacy for meeting rooms
        if channel.get("is_private", False):
            return RoomPurpose.PRIVATE_MEETING

        # Default to discussion
        return RoomPurpose.DISCUSSION

    def _assess_activity_level(self, channel: Dict[str, Any]) -> str:
        """Assess channel activity level from message patterns"""

        # Use available metrics to estimate activity
        member_count = channel.get("num_members", 0)

        if member_count < 5:
            return "quiet"
        elif member_count < 20:
            return "moderate"
        elif member_count < 100:
            return "active"
        else:
            return "busy"

    def _detect_conversation_style(self, channel: Dict[str, Any]) -> str:
        """Detect conversation style from channel characteristics"""

        channel_name = channel.get("name", "").lower()

        if any(pattern in channel_name for pattern in ["dev", "tech", "api", "code"]):
            return "technical"
        elif any(pattern in channel_name for pattern in ["random", "social", "fun"]):
            return "casual"
        else:
            return "professional"

    # Message and Thread Mapping

    def map_message_to_spatial_event(
        self, slack_message: Dict[str, Any], territory_id: str, room_id: str
    ) -> SpatialEvent:
        """
        Map Slack message to SpatialEvent with contextual spatial objects.

        Args:
            slack_message: Slack message API response
            territory_id: ID of containing territory
            room_id: ID of containing room

        Returns:
            SpatialEvent representing message placement and interactions
        """
        try:
            message_ts = slack_message.get("ts", "")
            thread_ts = slack_message.get("thread_ts")

            # Create spatial coordinates
            coordinates = SpatialCoordinates(
                territory_id=territory_id,
                room_id=room_id,
                path_id=thread_ts,
                object_position=None,  # Position within thread if applicable
            )

            # Create spatial object for message
            spatial_object = self._create_spatial_object(slack_message, coordinates)

            # Extract attention attractors (@mentions)
            attention_attractors = self._extract_attention_attractors(slack_message)

            # Extract emotional markers (reactions)
            emotional_markers = self._extract_emotional_markers(slack_message)

            # Determine event type
            event_type = (
                "thread_message" if thread_ts and thread_ts != message_ts else "room_message"
            )

            # Create spatial event
            spatial_event = SpatialEvent(
                event_id=f"{room_id}:{message_ts}",
                event_type=event_type,
                coordinates=coordinates,
                actor_id=slack_message.get("user"),
                affected_objects=[spatial_object.id],
                spatial_changes={
                    "object_placed": spatial_object.get_spatial_context(),
                    "attention_attracted": len(attention_attractors),
                    "emotional_markers": len(emotional_markers),
                },
                event_time=self._parse_slack_timestamp(message_ts),
                significance_level=self._assess_message_significance(slack_message),
            )

            self._spatial_analytics["events_processed"] += 1
            self._spatial_analytics["objects_placed"] += 1

            logger.debug(f"Mapped message {message_ts} to spatial event in room {room_id}")
            return spatial_event

        except Exception as e:
            logger.error(f"Failed to map message to spatial event: {e}")
            raise ValueError(f"Message mapping failed: {e}") from e

    def _create_spatial_object(
        self, message: Dict[str, Any], coordinates: SpatialCoordinates
    ) -> SpatialObject:
        """Create spatial object representation of message"""

        message_ts = message.get("ts", "")
        content = message.get("text", "")
        user_id = message.get("user", "")

        # Classify object type
        object_type = self._classify_object_type(message)

        # Assess size category
        size_category = self._assess_object_size(content)

        return SpatialObject(
            id=message_ts,
            coordinates=coordinates,
            object_type=object_type,
            content=content,
            creator_id=user_id,
            size_category=size_category,
            placement_time=self._parse_slack_timestamp(message_ts),
        )

    async def map_message_to_spatial_object(
        self,
        message_data: Dict[str, Any],
        room_id: str,
        thread_ts: Optional[str] = None,
    ) -> SpatialObject:
        """
        Map Slack message to SpatialObject for event processing.

        This async method creates a spatial object representation of a message,
        suitable for real-time event processing. It uses the existing _create_spatial_object
        helper but accepts event-based parameters.

        Args:
            message_data: Slack message event data
            room_id: Channel ID where message was posted
            thread_ts: Thread timestamp if message is in thread

        Returns:
            SpatialObject representation of message
        """
        # Extract territory ID from message data
        territory_id = message_data.get("team") or message_data.get("team_id", "unknown")

        # Create spatial coordinates for the object
        coordinates = SpatialCoordinates(
            territory_id=territory_id,
            room_id=room_id,
            path_id=thread_ts,
            object_position=None,
        )

        # Use existing helper to create spatial object
        return self._create_spatial_object(message=message_data, coordinates=coordinates)

    def _classify_object_type(self, message: Dict[str, Any]) -> ObjectType:
        """Classify message as spatial object type"""

        # Check for files
        if message.get("files"):
            file_type = message["files"][0].get("mimetype", "")
            if file_type.startswith("image/"):
                return ObjectType.IMAGE_ARTIFACT
            else:
                return ObjectType.FILE_DOCUMENT

        # Check for code blocks
        text = message.get("text", "")
        if "```" in text or "`" in text:
            return ObjectType.CODE_BLOCK

        # Check for links
        if message.get("attachments") or "http" in text.lower():
            return ObjectType.LINK_REFERENCE

        # Check for system messages
        if message.get("subtype") in ["bot_message", "channel_join", "channel_leave"]:
            return ObjectType.SYSTEM_NOTIFICATION

        # Default to text message
        return ObjectType.TEXT_MESSAGE

    def _assess_object_size(self, content: str) -> str:
        """Assess spatial object size based on content length"""

        content_length = len(content)

        if content_length < 50:
            return "minimal"
        elif content_length < 200:
            return "standard"
        elif content_length < 1000:
            return "substantial"
        else:
            return "extensive"

    def _extract_attention_attractors(self, message: Dict[str, Any]) -> List[AttentionAttractor]:
        """Extract @mentions as attention attractors"""

        attractors = []
        text = message.get("text", "")
        message_ts = message.get("ts", "")

        # Simple mention detection (would need more sophisticated parsing in production)
        if "@channel" in text or "@here" in text:
            attractors.append(
                AttentionAttractor(
                    target_id="channel",
                    attractor_type=AttentionLevel.FOCUSED,
                    source_object_id=message_ts,
                    attention_radius="room-wide",
                    urgency_indicators=["@channel"] if "@channel" in text else ["@here"],
                )
            )

        # User mention detection (simplified)
        if "<@" in text:
            attractors.append(
                AttentionAttractor(
                    target_id="user",
                    attractor_type=AttentionLevel.DIRECT,
                    source_object_id=message_ts,
                    attention_radius="focused",
                )
            )

        return attractors

    async def map_mention_to_attention_attractor(
        self, mention_data: Dict[str, Any]
    ) -> AttentionAttractor:
        """
        Map Slack mention to AttentionAttractor for event processing.

        Analyzes a message containing a mention and creates an attention attractor
        representing the @mention event. Classifies the attention level based on
        the type of mention (@user, @channel, @here, etc.).

        Args:
            mention_data: Slack message event data containing mention

        Returns:
            AttentionAttractor representing the mention
        """
        text = mention_data.get("text", "")
        message_ts = mention_data.get("ts", "")

        # Determine attention level and target based on mention type
        if "@channel" in text:
            attention_level = AttentionLevel.FOCUSED
            target_id = "channel"
            attention_radius = "room-wide"
            urgency_indicators = ["@channel"]
        elif "@here" in text:
            attention_level = AttentionLevel.FOCUSED
            target_id = "here"
            attention_radius = "room-wide"
            urgency_indicators = ["@here"]
        elif "<@" in text:
            # Extract user ID from mention format <@U12345>
            import re

            user_match = re.search(r"<@([A-Z0-9]+)>", text)
            target_id = user_match.group(1) if user_match else "user"
            attention_level = AttentionLevel.DIRECT
            attention_radius = "focused"
            urgency_indicators = []
        else:
            # Fallback for other mention types
            target_id = "unknown"
            attention_level = AttentionLevel.AMBIENT
            attention_radius = "focused"
            urgency_indicators = []

        # Check for urgency keywords
        urgency_keywords = ["urgent", "asap", "emergency", "critical", "help"]
        text_lower = text.lower()
        for keyword in urgency_keywords:
            if keyword in text_lower:
                urgency_indicators.append(keyword)
                # Upgrade attention level if urgent keywords present
                if attention_level == AttentionLevel.DIRECT:
                    attention_level = AttentionLevel.URGENT
                elif attention_level == AttentionLevel.FOCUSED:
                    attention_level = AttentionLevel.URGENT

        # Extract context keywords (simple word extraction)
        context_keywords = [
            word for word in text_lower.split() if len(word) > 4 and word not in urgency_keywords
        ][:5]  # Limit to top 5 meaningful words

        return AttentionAttractor(
            target_id=target_id,
            attractor_type=attention_level,
            source_object_id=message_ts,
            urgency_indicators=urgency_indicators,
            context_keywords=context_keywords,
            attention_radius=attention_radius,
            persistence_level="sustained" if urgency_indicators else "standard",
            created_at=self._parse_slack_timestamp(message_ts),
        )

    def _extract_emotional_markers(self, message: Dict[str, Any]) -> List[EmotionalMarker]:
        """Extract reactions as emotional markers"""

        markers = []
        reactions = message.get("reactions", [])
        message_ts = message.get("ts", "")

        for reaction in reactions:
            emoji_name = reaction.get("name", "")
            users = reaction.get("users", [])

            # Classify emotional valence
            valence = self._classify_emotional_valence(emoji_name)

            for user_id in users:
                markers.append(
                    EmotionalMarker(
                        reaction_type=emoji_name,
                        valence=valence,
                        source_object_id=message_ts,
                        reactor_id=user_id,
                        intensity=self._assess_reaction_intensity(emoji_name),
                        social_signal="individual" if len(users) == 1 else "social",
                    )
                )

        return markers

    async def map_reaction_to_emotional_marker(
        self, reaction_data: Dict[str, Any], added: bool
    ) -> EmotionalMarker:
        """
        Map Slack reaction to EmotionalMarker for event processing.

        Creates an emotional marker from a reaction_added or reaction_removed event.
        Classifies the emotional valence and assesses the social context of the reaction.

        Args:
            reaction_data: Slack reaction event data
            added: True if reaction was added, False if removed

        Returns:
            EmotionalMarker representing the reaction
        """
        # Extract reaction details from event structure
        # Reaction events have structure: {reaction: "emoji_name", item: {type, channel, ts}, user: "U123"}
        emoji_name = reaction_data.get("reaction", "")
        user_id = reaction_data.get("user", "")

        # Get message reference from item
        item = reaction_data.get("item", {})
        message_ts = item.get("ts", "")

        # Classify emotional valence using existing helper
        valence = self._classify_emotional_valence(emoji_name)

        # Assess intensity using existing helper
        intensity = self._assess_reaction_intensity(emoji_name)

        # Determine timing significance
        # If we had message timestamp and reaction timestamp, we could calculate this
        # For now, use simple heuristic
        timing_significance = "immediate"  # Reactions in event stream are typically immediate

        # Assess social signal (would need to check if others reacted with same emoji)
        # For event-based processing, we default to individual unless we have aggregate data
        social_signal = "individual"

        # Determine emotional radius based on reaction type
        if valence in [EmotionalValence.POSITIVE, EmotionalValence.SUPPORTIVE]:
            emotional_radius = "room"  # Positive emotions spread
            contagion_potential = "medium"
        elif valence == EmotionalValence.NEGATIVE:
            emotional_radius = "local"  # Negative emotions more contained
            contagion_potential = "low"
        elif valence == EmotionalValence.HUMOROUS:
            emotional_radius = "room"  # Humor spreads
            contagion_potential = "high"
        else:
            emotional_radius = "local"
            contagion_potential = "low"

        return EmotionalMarker(
            reaction_type=emoji_name,
            valence=valence,
            source_object_id=message_ts,
            reactor_id=user_id,
            intensity=intensity,
            social_signal=social_signal,
            timing_significance=timing_significance,
            emotional_radius=emotional_radius,
            contagion_potential=contagion_potential,
            created_at=self._parse_slack_timestamp(message_ts) if message_ts else None,
        )

    def _classify_emotional_valence(self, emoji_name: str) -> EmotionalValence:
        """Classify emoji reaction as emotional valence"""

        positive_patterns = ["thumbsup", "+1", "heart", "tada", "clap", "muscle", "raised_hands"]
        negative_patterns = ["thumbsdown", "-1", "x", "warning", "disappointed"]
        humorous_patterns = ["laughing", "smile", "wink", "joy", "rofl"]
        supportive_patterns = ["clap", "muscle", "raised_hands", "pray"]

        if any(pattern in emoji_name for pattern in positive_patterns):
            return EmotionalValence.POSITIVE
        elif any(pattern in emoji_name for pattern in negative_patterns):
            return EmotionalValence.NEGATIVE
        elif any(pattern in emoji_name for pattern in humorous_patterns):
            return EmotionalValence.HUMOROUS
        elif any(pattern in emoji_name for pattern in supportive_patterns):
            return EmotionalValence.SUPPORTIVE
        else:
            return EmotionalValence.NEUTRAL

    def _assess_reaction_intensity(self, emoji_name: str) -> str:
        """Assess reaction intensity level"""

        strong_reactions = ["fire", "100", "exploding_head", "mind_blown"]

        if any(pattern in emoji_name for pattern in strong_reactions):
            return "strong"
        else:
            return "standard"

    def _assess_message_significance(self, message: Dict[str, Any]) -> str:
        """Assess message significance for spatial event classification"""

        text = message.get("text", "").lower()

        # Check for critical indicators
        if any(word in text for word in ["urgent", "critical", "emergency", "help"]):
            return "critical"

        # Check for notable indicators
        if message.get("files") or "@channel" in text or "@here" in text:
            return "notable"

        # Check for significant indicators
        if message.get("thread_ts") or len(text) > 500:
            return "significant"

        return "routine"

    # Thread (Conversational Path) Mapping

    def map_thread_to_conversational_path(
        self, thread_messages: List[Dict[str, Any]], territory_id: str, room_id: str
    ) -> ConversationalPath:
        """
        Map Slack thread to ConversationalPath spatial metaphor.

        Args:
            thread_messages: List of Slack messages in thread
            territory_id: ID of containing territory
            room_id: ID of containing room

        Returns:
            ConversationalPath representation of thread
        """
        try:
            if not thread_messages:
                raise ValueError("Empty thread cannot be mapped to conversational path")

            # Get thread identifier from first message
            origin_message = thread_messages[0]
            thread_ts = origin_message.get("thread_ts") or origin_message.get("ts")

            # Analyze thread characteristics
            participants = set()
            for msg in thread_messages:
                if msg.get("user"):
                    participants.add(msg["user"])

            # Classify path type
            path_type = self._classify_path_type(thread_messages)

            # Assess conversation dynamics
            momentum = self._assess_conversation_momentum(thread_messages)
            coherence = self._assess_topic_coherence(thread_messages)
            temperature = self._assess_emotional_temperature(thread_messages)

            # Identify waypoints and branching points
            waypoints = self._identify_major_waypoints(thread_messages)
            branching_points = self._identify_branching_points(thread_messages)

            # Create conversational path
            path = ConversationalPath(
                id=thread_ts,
                room_id=room_id,
                territory_id=territory_id,
                path_type=path_type,
                origin_object_id=origin_message.get("ts", ""),
                current_length=len(thread_messages),
                active_participants=participants,
                conversation_momentum=momentum,
                topic_coherence=coherence,
                emotional_temperature=temperature,
                major_waypoints=waypoints,
                branching_points=branching_points,
                created_at=self._parse_slack_timestamp(origin_message.get("ts")),
                last_activity=self._parse_slack_timestamp(thread_messages[-1].get("ts")),
            )

            logger.info(f"Mapped thread {thread_ts} to {path_type.value} conversational path")
            return path

        except Exception as e:
            logger.error(f"Failed to map thread to conversational path: {e}")
            raise ValueError(f"Thread mapping failed: {e}") from e

    def _classify_path_type(self, messages: List[Dict[str, Any]]) -> PathType:
        """Classify thread as conversational path type"""

        if len(messages) <= 3:
            return PathType.LINEAR

        # Analyze participant patterns
        participants = [msg.get("user") for msg in messages if msg.get("user")]
        unique_participants = set(participants)

        if len(unique_participants) == 2:
            return PathType.LINEAR
        elif len(unique_participants) > 5:
            return PathType.BRANCHING
        else:
            return PathType.LINEAR  # Default assumption

    def _assess_conversation_momentum(self, messages: List[Dict[str, Any]]) -> str:
        """Assess conversation momentum from message timing patterns"""

        if len(messages) < 2:
            return "building"

        # Simple momentum assessment based on message count
        # In production, would analyze timestamp gaps
        if len(messages) > 10:
            return "maintaining"
        elif len(messages) > 5:
            return "building"
        else:
            return "stalled"

    def _assess_topic_coherence(self, messages: List[Dict[str, Any]]) -> str:
        """Assess topic coherence from content analysis"""

        # Simplified coherence assessment
        # In production, would use NLP analysis
        return "focused"  # Default assumption

    def _assess_emotional_temperature(self, messages: List[Dict[str, Any]]) -> str:
        """Assess emotional temperature from reaction patterns"""

        # Count total reactions across thread
        total_reactions = 0
        for msg in messages:
            reactions = msg.get("reactions", [])
            for reaction in reactions:
                total_reactions += len(reaction.get("users", []))

        if total_reactions > 20:
            return "heated"
        elif total_reactions > 10:
            return "warm"
        elif total_reactions > 3:
            return "neutral"
        else:
            return "cool"

    def _identify_major_waypoints(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Identify significant messages as major waypoints"""

        waypoints = []

        for msg in messages:
            # Consider messages with attachments or long content as waypoints
            if msg.get("files") or len(msg.get("text", "")) > 500 or msg.get("reactions"):
                waypoints.append(msg.get("ts", ""))

        return waypoints

    def _identify_branching_points(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Identify topic shift points as branching points"""

        # Simplified branching point detection
        # In production, would use topic modeling
        branching_points = []

        for i, msg in enumerate(messages):
            if i > 0 and "but" in msg.get("text", "").lower():
                branching_points.append(msg.get("ts", ""))

        return branching_points

    # Utility Methods

    def _parse_slack_timestamp(self, timestamp: Optional[str]) -> Optional[datetime]:
        """Parse Slack timestamp to datetime object"""

        if not timestamp:
            return None

        try:
            # Slack timestamps are Unix timestamps with decimals
            timestamp_float = float(timestamp)
            return datetime.fromtimestamp(timestamp_float)
        except (ValueError, TypeError):
            logger.warning(f"Failed to parse Slack timestamp: {timestamp}")
            return None

    # Analytics and Context Methods

    def get_spatial_analytics(self) -> Dict[str, Any]:
        """Get spatial mapping analytics and performance metrics"""

        return {
            **self._spatial_analytics,
            "cached_territories": len(self._territory_cache),
            "cached_rooms": len(self._room_cache),
            "mapping_health": "operational",
        }

    def get_territory_context(self, territory_id: str) -> Optional[Dict[str, Any]]:
        """Get spatial context for specific territory"""

        territory = self._territory_cache.get(territory_id)
        if not territory:
            return None

        return territory.get_navigation_context()

    def get_room_context(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Get spatial context for specific room"""

        room = self._room_cache.get(room_id)
        if not room:
            return None

        return room.get_room_atmosphere()

    def clear_spatial_cache(self):
        """Clear spatial caches (useful for testing and memory management)"""

        self._territory_cache.clear()
        self._room_cache.clear()

        logger.info("Spatial mapper caches cleared")

    def update_room_activity(self, room_id: str, activity_data: Dict[str, Any]):
        """Update room activity and inhabitant data"""

        room = self._room_cache.get(room_id)
        if not room:
            return

        # Update activity level
        if "message_count" in activity_data:
            message_count = activity_data["message_count"]
            if message_count > 100:
                room.activity_level = "busy"
            elif message_count > 50:
                room.activity_level = "active"
            elif message_count > 10:
                room.activity_level = "moderate"
            else:
                room.activity_level = "quiet"

        # Update current inhabitants
        if "active_users" in activity_data:
            room.current_inhabitants = set(activity_data["active_users"])

        logger.debug(f"Updated activity for room {room_id}: {room.activity_level}")
