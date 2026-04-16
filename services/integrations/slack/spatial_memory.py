"""
Slack Spatial Memory - Persistent Spatial Awareness Across Sessions
Implements persistent spatial memory for Piper Morgan's spatial awareness system.

Provides spatial memory persistence across sessions including:
- Room and relationship memory storage
- Territory navigation history persistence
- Spatial pattern learning and recognition
- Cross-session spatial context continuity
- Performance-optimized spatial data structures
"""

import json
import logging
import os
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
from uuid import uuid4

from .spatial_types import (
    AttentionLevel,
    EmotionalValence,
    Room,
    RoomPurpose,
    SpatialCoordinates,
    Territory,
    TerritoryType,
)

logger = logging.getLogger(__name__)


@dataclass
class SpatialMemoryRecord:
    """Individual spatial memory record for rooms and territories"""

    spatial_id: str  # room_id or territory_id
    spatial_type: str  # "room" or "territory"
    name: str

    # Visit tracking
    first_discovered: datetime
    last_visited: datetime
    visit_count: int = 0
    total_time_spent: float = 0.0  # seconds

    # Spatial characteristics learned
    purpose: Optional[str] = None
    activity_patterns: Dict[str, float] = field(default_factory=dict)  # time -> activity_level
    typical_inhabitants: Set[str] = field(default_factory=set)
    conversation_style: str = "unknown"

    # Relationships and connections
    connected_spaces: Set[str] = field(default_factory=set)  # Adjacent rooms/territories
    frequent_transitions: Dict[str, int] = field(default_factory=dict)  # target_id -> count

    # Attention and emotional associations
    attention_history: List[Dict[str, Any]] = field(default_factory=list)
    emotional_associations: Dict[str, float] = field(default_factory=dict)  # valence -> strength
    significant_events: List[Dict[str, Any]] = field(default_factory=list)

    # Learned patterns
    peak_activity_hours: List[int] = field(default_factory=list)  # hours 0-23
    common_topics: Dict[str, int] = field(default_factory=dict)  # topic -> frequency
    user_interaction_patterns: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        data = asdict(self)

        # Convert datetime objects to ISO strings
        data["first_discovered"] = self.first_discovered.isoformat()
        data["last_visited"] = self.last_visited.isoformat()

        # Convert sets to lists for JSON serialization
        data["typical_inhabitants"] = list(self.typical_inhabitants)
        data["connected_spaces"] = list(self.connected_spaces)

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpatialMemoryRecord":
        """Create from dictionary with type conversion"""

        # Convert ISO strings back to datetime objects
        data["first_discovered"] = datetime.fromisoformat(data["first_discovered"])
        data["last_visited"] = datetime.fromisoformat(data["last_visited"])

        # Convert lists back to sets
        data["typical_inhabitants"] = set(data["typical_inhabitants"])
        data["connected_spaces"] = set(data["connected_spaces"])

        return cls(**data)


@dataclass
class SpatialRelationship:
    """Relationship between spatial locations"""

    from_id: str
    to_id: str
    relationship_type: str  # "adjacent", "contains", "frequent_path", "workflow_link"

    # Relationship strength and characteristics
    strength: float = 0.0  # 0.0 to 1.0
    discovery_time: datetime = field(default_factory=datetime.now)
    last_used: datetime = field(default_factory=datetime.now)
    usage_count: int = 0

    # Context information
    transition_context: Dict[str, Any] = field(default_factory=dict)
    typical_transition_time: Optional[float] = None  # seconds

    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        data = asdict(self)
        data["discovery_time"] = self.discovery_time.isoformat()
        data["last_used"] = self.last_used.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpatialRelationship":
        """Create from dictionary with type conversion"""
        data["discovery_time"] = datetime.fromisoformat(data["discovery_time"])
        data["last_used"] = datetime.fromisoformat(data["last_used"])
        return cls(**data)


@dataclass
class SpatialPattern:
    """Learned spatial behavior pattern"""

    pattern_id: str
    pattern_type: str  # "navigation", "attention", "activity", "communication"
    pattern_name: str

    # Pattern characteristics
    confidence: float = 0.0  # 0.0 to 1.0
    discovery_time: datetime = field(default_factory=datetime.now)
    last_observed: datetime = field(default_factory=datetime.now)
    observation_count: int = 0

    # Pattern data
    pattern_data: Dict[str, Any] = field(default_factory=dict)
    trigger_conditions: Dict[str, Any] = field(default_factory=dict)
    expected_outcomes: Dict[str, Any] = field(default_factory=dict)

    # Context and applicability
    applicable_territories: Set[str] = field(default_factory=set)
    applicable_rooms: Set[str] = field(default_factory=set)
    time_constraints: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        data = asdict(self)
        data["discovery_time"] = self.discovery_time.isoformat()
        data["last_observed"] = self.last_observed.isoformat()
        data["applicable_territories"] = list(self.applicable_territories)
        data["applicable_rooms"] = list(self.applicable_rooms)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpatialPattern":
        """Create from dictionary with type conversion"""
        data["discovery_time"] = datetime.fromisoformat(data["discovery_time"])
        data["last_observed"] = datetime.fromisoformat(data["last_observed"])
        data["applicable_territories"] = set(data["applicable_territories"])
        data["applicable_rooms"] = set(data["applicable_rooms"])
        return cls(**data)


class SpatialMemoryStore:
    """
    Persistent storage and management for spatial memory.

    Handles persistent storage of spatial memories, relationships, and patterns
    with performance optimization and cross-session continuity.
    """

    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path or "data/spatial_memory")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # In-memory caches for performance
        self._memory_records: Dict[str, SpatialMemoryRecord] = {}
        self._relationships: Dict[str, SpatialRelationship] = {}
        self._patterns: Dict[str, SpatialPattern] = {}

        # Cache management
        self._cache_dirty = False
        self._last_save_time = datetime.now()
        self._auto_save_interval = timedelta(minutes=5)

        # Performance metrics
        self._access_counts: Dict[str, int] = {}
        self._load_times: Dict[str, float] = {}

        logger.info(f"SpatialMemoryStore initialized with storage: {self.storage_path}")

        # Load existing data
        self._load_all_data()

    # Core Memory Management

    def record_spatial_visit(
        self,
        spatial_id: str,
        spatial_type: str,
        name: str,
        visit_duration: Optional[float] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> SpatialMemoryRecord:
        """Record a visit to a spatial location"""

        now = datetime.now()
        context = context or {}

        # Get or create memory record
        memory = self._memory_records.get(spatial_id)
        if not memory:
            memory = SpatialMemoryRecord(
                spatial_id=spatial_id,
                spatial_type=spatial_type,
                name=name,
                first_discovered=now,
                last_visited=now,
            )
            self._memory_records[spatial_id] = memory
            logger.info(f"New spatial location discovered: {name} ({spatial_type})")

        # Update visit information
        memory.last_visited = now
        memory.visit_count += 1

        if visit_duration:
            memory.total_time_spent += visit_duration

        # Learn from context
        if context:
            self._update_memory_from_context(memory, context)

        self._mark_cache_dirty()
        self._track_access(spatial_id)

        return memory

    def record_spatial_relationship(
        self,
        from_id: str,
        to_id: str,
        relationship_type: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> SpatialRelationship:
        """Record a relationship between spatial locations"""

        relationship_key = f"{from_id}->{to_id}:{relationship_type}"

        relationship = self._relationships.get(relationship_key)
        if not relationship:
            relationship = SpatialRelationship(
                from_id=from_id, to_id=to_id, relationship_type=relationship_type
            )
            self._relationships[relationship_key] = relationship
            logger.debug(f"New spatial relationship: {from_id} -> {to_id} ({relationship_type})")

        # Update relationship strength and usage
        relationship.last_used = datetime.now()
        relationship.usage_count += 1

        # Increase strength based on usage (with diminishing returns)
        usage_factor = min(relationship.usage_count / 10.0, 1.0)
        relationship.strength = min(
            relationship.strength + 0.1 * (1.0 - relationship.strength), 1.0
        )

        if context:
            relationship.transition_context.update(context)

        self._mark_cache_dirty()

        return relationship

    def learn_spatial_pattern(
        self,
        pattern_type: str,
        pattern_name: str,
        pattern_data: Dict[str, Any],
        confidence: float = 0.5,
        applicable_locations: Optional[List[str]] = None,
    ) -> SpatialPattern:
        """Learn a new spatial behavior pattern"""

        pattern_id = f"{pattern_type}:{pattern_name}:{uuid4().hex[:8]}"

        pattern = SpatialPattern(
            pattern_id=pattern_id,
            pattern_type=pattern_type,
            pattern_name=pattern_name,
            confidence=confidence,
            pattern_data=pattern_data.copy(),
        )

        # Set applicable locations
        if applicable_locations:
            for location_id in applicable_locations:
                memory = self._memory_records.get(location_id)
                if memory:
                    if memory.spatial_type == "territory":
                        pattern.applicable_territories.add(location_id)
                    elif memory.spatial_type == "room":
                        pattern.applicable_rooms.add(location_id)

        self._patterns[pattern_id] = pattern
        self._mark_cache_dirty()

        logger.info(f"Learned new spatial pattern: {pattern_name} ({pattern_type})")

        return pattern

    # Query and Retrieval Methods

    def get_memory_record(self, spatial_id: str) -> Optional[SpatialMemoryRecord]:
        """Get memory record for a spatial location"""
        self._track_access(spatial_id)
        return self._memory_records.get(spatial_id)

    def get_territory_memories(self) -> List[SpatialMemoryRecord]:
        """Get all territory memory records"""
        return [
            memory for memory in self._memory_records.values() if memory.spatial_type == "territory"
        ]

    def get_room_memories(self, territory_id: Optional[str] = None) -> List[SpatialMemoryRecord]:
        """Get room memory records, optionally filtered by territory"""
        room_memories = [
            memory for memory in self._memory_records.values() if memory.spatial_type == "room"
        ]

        if territory_id:
            # Filter by territory through relationships
            territory_rooms = self.get_connected_spaces(territory_id, "contains")
            room_memories = [m for m in room_memories if m.spatial_id in territory_rooms]

        return room_memories

    def get_connected_spaces(
        self, spatial_id: str, relationship_type: Optional[str] = None
    ) -> List[str]:
        """Get spaces connected to the given location"""

        connected = []

        for rel_key, relationship in self._relationships.items():
            if relationship.from_id == spatial_id:
                if not relationship_type or relationship.relationship_type == relationship_type:
                    connected.append(relationship.to_id)

        return connected

    def find_patterns(
        self,
        pattern_type: Optional[str] = None,
        applicable_to: Optional[str] = None,
        min_confidence: float = 0.0,
    ) -> List[SpatialPattern]:
        """Find patterns matching criteria"""

        patterns = []

        for pattern in self._patterns.values():
            # Filter by type
            if pattern_type and pattern.pattern_type != pattern_type:
                continue

            # Filter by confidence
            if pattern.confidence < min_confidence:
                continue

            # Filter by applicability
            if applicable_to:
                if (
                    applicable_to not in pattern.applicable_territories
                    and applicable_to not in pattern.applicable_rooms
                ):
                    continue

            patterns.append(pattern)

        # Sort by confidence (highest first)
        patterns.sort(key=lambda p: p.confidence, reverse=True)

        return patterns

    def get_navigation_suggestions(
        self, current_location: str, context: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get navigation suggestions based on spatial memory"""

        suggestions = []
        current_memory = self.get_memory_record(current_location)

        if not current_memory:
            return suggestions

        # Suggest connected spaces with high relationship strength
        for rel_key, relationship in self._relationships.items():
            if relationship.from_id == current_location and relationship.strength > 0.3:
                target_memory = self.get_memory_record(relationship.to_id)
                if target_memory:
                    suggestions.append(
                        {
                            "target_id": relationship.to_id,
                            "target_name": target_memory.name,
                            "relationship_type": relationship.relationship_type,
                            "strength": relationship.strength,
                            "reason": f"Frequently accessed {relationship.relationship_type}",
                            "last_visit": target_memory.last_visited.isoformat(),
                        }
                    )

        # Suggest based on patterns
        navigation_patterns = self.find_patterns("navigation", current_location, 0.5)
        for pattern in navigation_patterns[:3]:  # Top 3 patterns
            if "suggested_next" in pattern.pattern_data:
                next_location = pattern.pattern_data["suggested_next"]
                target_memory = self.get_memory_record(next_location)
                if target_memory:
                    suggestions.append(
                        {
                            "target_id": next_location,
                            "target_name": target_memory.name,
                            "relationship_type": "pattern",
                            "strength": pattern.confidence,
                            "reason": f"Pattern: {pattern.pattern_name}",
                            "pattern_type": pattern.pattern_type,
                        }
                    )

        # Sort by strength and limit
        suggestions.sort(key=lambda s: s["strength"], reverse=True)
        return suggestions[:5]

    # Learning and Pattern Recognition

    def _update_memory_from_context(self, memory: SpatialMemoryRecord, context: Dict[str, Any]):
        """Update memory record with information from context"""

        # Learn activity patterns
        current_hour = datetime.now().hour
        activity_level = context.get("activity_level", "unknown")
        if activity_level != "unknown":
            memory.activity_patterns[str(current_hour)] = self._parse_activity_level(activity_level)

        # Learn inhabitants
        if "inhabitants" in context:
            memory.typical_inhabitants.update(context["inhabitants"])

        # Learn conversation style
        if "conversation_style" in context:
            memory.conversation_style = context["conversation_style"]

        # Learn purpose
        if "purpose" in context:
            memory.purpose = context["purpose"]

        # Track attention events
        if "attention_event" in context:
            memory.attention_history.append(
                {"timestamp": datetime.now().isoformat(), "event": context["attention_event"]}
            )

            # Keep only recent attention history (last 50 events)
            if len(memory.attention_history) > 50:
                memory.attention_history = memory.attention_history[-50:]

        # Track emotional associations
        if "emotional_valence" in context:
            valence = context["emotional_valence"]
            if valence in memory.emotional_associations:
                memory.emotional_associations[valence] = min(
                    memory.emotional_associations[valence] + 0.1, 1.0
                )
            else:
                memory.emotional_associations[valence] = 0.1

    def _parse_activity_level(self, activity_level: str) -> float:
        """Convert activity level string to numeric value"""
        mapping = {"quiet": 0.1, "moderate": 0.4, "active": 0.7, "busy": 1.0}
        return mapping.get(activity_level.lower(), 0.5)

    def analyze_spatial_patterns(self) -> Dict[str, Any]:
        """Analyze current spatial memory for patterns"""

        analysis = {
            "total_locations": len(self._memory_records),
            "territories": len(self.get_territory_memories()),
            "rooms": len(self.get_room_memories()),
            "relationships": len(self._relationships),
            "patterns": len(self._patterns),
            "most_visited": [],
            "strongest_relationships": [],
            "peak_activity_insights": {},
            "emotional_associations": {},
        }

        # Most visited locations
        most_visited = sorted(
            self._memory_records.values(), key=lambda m: m.visit_count, reverse=True
        )[:5]

        analysis["most_visited"] = [
            {
                "id": m.spatial_id,
                "name": m.name,
                "type": m.spatial_type,
                "visits": m.visit_count,
                "total_time": m.total_time_spent,
            }
            for m in most_visited
        ]

        # Strongest relationships
        strongest_rels = sorted(
            self._relationships.values(), key=lambda r: r.strength, reverse=True
        )[:5]

        analysis["strongest_relationships"] = [
            {
                "from": r.from_id,
                "to": r.to_id,
                "type": r.relationship_type,
                "strength": r.strength,
                "usage_count": r.usage_count,
            }
            for r in strongest_rels
        ]

        # Activity pattern analysis
        activity_by_hour = {}
        for memory in self._memory_records.values():
            for hour_str, activity in memory.activity_patterns.items():
                hour = int(hour_str)
                if hour not in activity_by_hour:
                    activity_by_hour[hour] = []
                activity_by_hour[hour].append(activity)

        peak_hours = {}
        for hour, activities in activity_by_hour.items():
            avg_activity = sum(activities) / len(activities)
            peak_hours[hour] = avg_activity

        if peak_hours:
            peak_hour = max(peak_hours.keys(), key=lambda h: peak_hours[h])
            analysis["peak_activity_insights"] = {
                "peak_hour": peak_hour,
                "activity_level": peak_hours[peak_hour],
                "hourly_distribution": peak_hours,
            }

        return analysis

    # Persistence Management

    def _mark_cache_dirty(self):
        """Mark cache as needing save"""
        self._cache_dirty = True

    def _track_access(self, spatial_id: str):
        """Track access for performance monitoring"""
        self._access_counts[spatial_id] = self._access_counts.get(spatial_id, 0) + 1

    def save_to_disk(self, force: bool = False) -> bool:
        """Save spatial memory to disk"""

        if not force and not self._cache_dirty:
            return True

        try:
            # Save memory records
            memories_file = self.storage_path / "spatial_memories.json"
            memories_data = {
                spatial_id: memory.to_dict() for spatial_id, memory in self._memory_records.items()
            }

            with open(memories_file, "w") as f:
                json.dump(memories_data, f, indent=2)

            # Save relationships
            relationships_file = self.storage_path / "spatial_relationships.json"
            relationships_data = {
                rel_key: relationship.to_dict()
                for rel_key, relationship in self._relationships.items()
            }

            with open(relationships_file, "w") as f:
                json.dump(relationships_data, f, indent=2)

            # Save patterns
            patterns_file = self.storage_path / "spatial_patterns.json"
            patterns_data = {
                pattern_id: pattern.to_dict() for pattern_id, pattern in self._patterns.items()
            }

            with open(patterns_file, "w") as f:
                json.dump(patterns_data, f, indent=2)

            # Save metadata
            metadata = {
                "last_save": datetime.now().isoformat(),
                "total_memories": len(self._memory_records),
                "total_relationships": len(self._relationships),
                "total_patterns": len(self._patterns),
                "access_counts": dict(
                    sorted(self._access_counts.items(), key=lambda x: x[1], reverse=True)[:100]
                ),  # Top 100 most accessed
            }

            metadata_file = self.storage_path / "metadata.json"
            with open(metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

            self._cache_dirty = False
            self._last_save_time = datetime.now()

            logger.info(
                f"Spatial memory saved: {len(self._memory_records)} memories, "
                f"{len(self._relationships)} relationships, {len(self._patterns)} patterns"
            )

            return True

        except Exception as e:
            logger.error(f"Failed to save spatial memory: {e}")
            return False

    def _load_all_data(self):
        """Load all spatial memory data from disk"""

        try:
            # Load memory records
            memories_file = self.storage_path / "spatial_memories.json"
            if memories_file.exists():
                with open(memories_file, "r") as f:
                    memories_data = json.load(f)

                for spatial_id, memory_dict in memories_data.items():
                    self._memory_records[spatial_id] = SpatialMemoryRecord.from_dict(memory_dict)

            # Load relationships
            relationships_file = self.storage_path / "spatial_relationships.json"
            if relationships_file.exists():
                with open(relationships_file, "r") as f:
                    relationships_data = json.load(f)

                for rel_key, relationship_dict in relationships_data.items():
                    self._relationships[rel_key] = SpatialRelationship.from_dict(relationship_dict)

            # Load patterns
            patterns_file = self.storage_path / "spatial_patterns.json"
            if patterns_file.exists():
                with open(patterns_file, "r") as f:
                    patterns_data = json.load(f)

                for pattern_id, pattern_dict in patterns_data.items():
                    self._patterns[pattern_id] = SpatialPattern.from_dict(pattern_dict)

            # Load metadata
            metadata_file = self.storage_path / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r") as f:
                    metadata = json.load(f)
                    self._access_counts.update(metadata.get("access_counts", {}))

            logger.info(
                f"Spatial memory loaded: {len(self._memory_records)} memories, "
                f"{len(self._relationships)} relationships, {len(self._patterns)} patterns"
            )

        except Exception as e:
            logger.error(f"Failed to load spatial memory: {e}")

    def auto_save_if_needed(self):
        """Auto-save if enough time has passed and cache is dirty"""

        if self._cache_dirty and datetime.now() - self._last_save_time > self._auto_save_interval:
            self.save_to_disk()

    def get_memory_statistics(self) -> Dict[str, Any]:
        """Get spatial memory system statistics"""

        return {
            "storage_path": str(self.storage_path),
            "memory_records": len(self._memory_records),
            "relationships": len(self._relationships),
            "patterns": len(self._patterns),
            "cache_dirty": self._cache_dirty,
            "last_save": self._last_save_time.isoformat(),
            "auto_save_interval": self._auto_save_interval.total_seconds(),
            "top_accessed": dict(
                sorted(self._access_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ),
        }
