"""
Slack Attention Model - Advanced Attention Priority Algorithms
Implements sophisticated attention management for spatial Slack integration.

Provides advanced attention priority modeling including:
- Proximity-based attention weighting and spatial influence
- Urgency detection and escalation algorithms
- Relationship-based attention prioritization
- Temporal attention patterns and decay modeling
- Multi-factor attention scoring with context awareness
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from uuid import uuid4

from .spatial_memory import SpatialMemoryStore
from .spatial_types import AttentionAttractor, AttentionLevel, EmotionalValence, SpatialCoordinates

logger = logging.getLogger(__name__)


class AttentionSource(Enum):
    """Sources that can generate attention events"""

    MENTION = "mention"  # Direct @mentions
    MESSAGE = "message"  # General messages in monitored rooms
    REACTION = "reaction"  # Emoji reactions
    THREAD = "thread"  # Thread responses
    STATUS_CHANGE = "status"  # User status updates
    ACTIVITY_SPIKE = "activity"  # Unusual activity patterns
    WORKFLOW = "workflow"  # Workflow-generated attention
    EMERGENCY = "emergency"  # Emergency/urgent situations
    SOCIAL = "social"  # Social interaction patterns


class AttentionDecay(Enum):
    """Attention decay models"""

    LINEAR = "linear"  # Linear decay over time
    EXPONENTIAL = "exponential"  # Exponential decay (fast initial drop)
    STEPPED = "stepped"  # Step-wise decay at intervals
    CONTEXTUAL = "contextual"  # Context-dependent decay


@dataclass
class AttentionEvent:
    """Individual attention-generating event"""

    event_id: str
    source: AttentionSource
    spatial_coordinates: SpatialCoordinates

    # Core attention properties
    base_intensity: float  # 0.0 to 1.0
    urgency_level: float  # 0.0 to 1.0
    personal_relevance: float  # 0.0 to 1.0

    # Temporal properties
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    last_updated: datetime = field(default_factory=datetime.now)

    # Context information
    actor_id: Optional[str] = None
    target_users: Set[str] = field(default_factory=set)
    keywords: List[str] = field(default_factory=list)
    emotional_context: Optional[EmotionalValence] = None

    # Spatial influence
    influence_radius: str = "local"  # local, room, territory, global
    spatial_decay_factor: float = 1.0

    # Relationship context
    relationship_strength: float = 0.0  # Strength of relationship with actor
    social_context: Dict[str, Any] = field(default_factory=dict)

    # Workflow integration
    workflow_id: Optional[str] = None
    task_priority: Optional[str] = None
    deadline_pressure: float = 0.0

    def get_current_intensity(
        self,
        decay_model: AttentionDecay = AttentionDecay.EXPONENTIAL,
        now: Optional[datetime] = None,
    ) -> float:
        """Calculate current attention intensity with decay.

        Args:
            decay_model: The decay model to use for intensity calculation.
            now: Optional current time for deterministic time simulation (#738).
                 Defaults to datetime.now() if not provided.
        """
        current_time = now or datetime.now()

        if self.expires_at and current_time > self.expires_at:
            return 0.0

        # Calculate time-based decay
        age = (current_time - self.created_at).total_seconds()

        if decay_model == AttentionDecay.LINEAR:
            # Linear decay over 1 hour
            decay_factor = max(0.0, 1.0 - (age / 3600.0))

        elif decay_model == AttentionDecay.EXPONENTIAL:
            # Exponential decay with 30-minute half-life
            half_life = 1800.0  # 30 minutes
            decay_factor = math.exp(-age * math.log(2) / half_life)

        elif decay_model == AttentionDecay.STEPPED:
            # Step-wise decay every 15 minutes
            steps = int(age // 900)  # 15-minute intervals
            decay_factor = max(0.0, 1.0 - (steps * 0.2))

        else:  # CONTEXTUAL
            # Context-dependent decay based on source
            if self.source == AttentionSource.EMERGENCY:
                decay_factor = max(0.3, math.exp(-age * math.log(2) / 7200))  # 2-hour half-life
            elif self.source == AttentionSource.MENTION:
                decay_factor = max(0.1, math.exp(-age * math.log(2) / 3600))  # 1-hour half-life
            else:
                decay_factor = math.exp(-age * math.log(2) / 1800)  # 30-minute half-life

        return self.base_intensity * decay_factor * self.spatial_decay_factor


@dataclass
class AttentionFocus:
    """Current attention focus state"""

    primary_coordinates: Optional[SpatialCoordinates] = None
    focus_strength: float = 0.0
    focus_duration: timedelta = field(default_factory=lambda: timedelta(0))

    # Multi-focus management
    secondary_foci: List[Tuple[SpatialCoordinates, float]] = field(default_factory=list)
    attention_split: float = 0.0  # How split is attention (0.0 = focused, 1.0 = highly split)

    # Context
    focus_reason: str = "idle"
    established_at: datetime = field(default_factory=datetime.now)
    last_shift: datetime = field(default_factory=datetime.now)

    # Performance tracking
    focus_efficiency: float = 1.0  # How efficiently we're using current focus
    interruption_count: int = 0
    context_switches: int = 0


@dataclass
class AttentionPattern:
    """Learned attention behavior pattern"""

    pattern_id: str
    pattern_name: str

    # Pattern characteristics
    trigger_conditions: Dict[str, Any] = field(default_factory=dict)
    attention_response: Dict[str, Any] = field(default_factory=dict)
    success_rate: float = 0.0

    # Learning data
    observation_count: int = 0
    last_observed: datetime = field(default_factory=datetime.now)
    confidence: float = 0.0

    # Applicability
    applicable_contexts: Set[str] = field(default_factory=set)
    time_constraints: Dict[str, Any] = field(default_factory=dict)


class AttentionModel:
    """
    Advanced attention priority algorithms for spatial Slack integration.

    Manages attention events, focus, and prioritization using sophisticated
    algorithms that consider proximity, urgency, relationships, and patterns.

    Issue #365: Added user_id support for pattern persistence.
    """

    def __init__(
        self,
        memory_store: Optional[SpatialMemoryStore] = None,
        user_id: Optional[str] = None,
        db_session_factory: Optional[Any] = None,
        clock: Optional[Callable[[], datetime]] = None,
    ):
        """
        Initialize AttentionModel.

        Args:
            memory_store: Spatial memory store for location data
            user_id: Optional user ID for pattern persistence (Issue #365)
            db_session_factory: Optional database session factory for persistence
            clock: Optional clock function for time simulation in tests (Issue #738).
                   Defaults to datetime.now. Injected into create_attention_event()
                   and get_current_intensity() to enable deterministic time control.
        """
        self.memory_store = memory_store or SpatialMemoryStore()
        self._clock = clock or datetime.now

        # User context for pattern persistence (Issue #365)
        self._user_id = user_id
        self._db_session_factory = db_session_factory

        # Active attention management
        self._active_events: Dict[str, AttentionEvent] = {}
        self._attention_focus: AttentionFocus = AttentionFocus()
        self._attention_history: List[Dict[str, Any]] = []

        # Pattern learning
        self._learned_patterns: Dict[str, AttentionPattern] = {}
        self._pattern_statistics: Dict[str, Any] = {}

        # Configuration and tuning
        self._config = {
            "max_active_events": 100,
            "default_decay_model": AttentionDecay.EXPONENTIAL,
            "focus_threshold": 0.7,
            "attention_split_threshold": 0.3,
            "proximity_influence_factor": 0.4,
            "relationship_influence_factor": 0.3,
            "urgency_boost_factor": 0.5,
            "pattern_learning_threshold": 0.6,
        }

        # Performance metrics
        self._metrics = {
            "events_processed": 0,
            "focus_shifts": 0,
            "pattern_matches": 0,
            "successful_attention_responses": 0,
            "average_response_time": 0.0,
            "attention_efficiency": 1.0,
        }

        logger.info("AttentionModel initialized", extra={"user_id": user_id})

    def set_user_context(self, user_id: str) -> None:
        """
        Set user context for pattern persistence.

        Call this method to enable pattern persistence after model creation.
        Useful when user_id isn't available at initialization time.

        Args:
            user_id: The user ID to associate with learned patterns

        Issue #365: Hybrid approach for backward compatibility.
        """
        self._user_id = user_id
        logger.info("User context set for attention model", extra={"user_id": user_id})

    # Pattern Persistence (Issue #365)

    async def _save_pattern_to_db(self, pattern: AttentionPattern) -> bool:
        """
        Persist attention pattern to database.

        Args:
            pattern: The AttentionPattern to save

        Returns:
            True if saved successfully, False otherwise

        Issue #365: Pattern persistence implementation.
        """
        if not self._user_id:
            logger.debug("Cannot save pattern: no user_id set")
            return False

        if not self._db_session_factory:
            logger.debug("Cannot save pattern: no db_session_factory")
            return False

        try:
            from sqlalchemy import select

            from services.database.models import LearnedPattern
            from services.shared_types import PatternType

            async with self._db_session_factory.create_session() as session:
                # Check if pattern exists for this user
                # Use cast for proper JSON field access in PostgreSQL
                from sqlalchemy import String, cast

                result = await session.execute(
                    select(LearnedPattern).where(
                        LearnedPattern.user_id == self._user_id,
                        LearnedPattern.pattern_type == PatternType.INTEGRATION,
                        cast(LearnedPattern.pattern_data["name"], String) == pattern.pattern_name,
                    )
                )
                existing = result.scalar_one_or_none()

                if existing:
                    # Update existing pattern
                    existing.pattern_data = {
                        "name": pattern.pattern_name,
                        "triggers": pattern.trigger_conditions,
                        "attention_response": pattern.attention_response,
                    }
                    existing.confidence = pattern.confidence
                    existing.usage_count = pattern.observation_count
                    existing.last_used_at = pattern.last_observed
                    logger.debug(
                        "Updated existing attention pattern",
                        extra={"pattern_name": pattern.pattern_name},
                    )
                else:
                    # Create new pattern
                    new_pattern = LearnedPattern(
                        user_id=self._user_id,
                        pattern_type=PatternType.INTEGRATION,
                        pattern_data={
                            "name": pattern.pattern_name,
                            "triggers": pattern.trigger_conditions,
                            "attention_response": pattern.attention_response,
                        },
                        confidence=pattern.confidence,
                        usage_count=pattern.observation_count,
                        last_used_at=pattern.last_observed,
                    )
                    session.add(new_pattern)
                    logger.debug(
                        "Created new attention pattern",
                        extra={"pattern_name": pattern.pattern_name},
                    )

                await session.commit()
                return True

        except Exception as e:
            logger.error(
                "Failed to save attention pattern",
                extra={
                    "pattern_name": pattern.pattern_name,
                    "error": str(e),
                },
            )
            return False

    async def load_patterns_from_db(self) -> int:
        """
        Load persisted patterns from database.

        Returns:
            Number of patterns loaded

        Issue #365: Pattern persistence implementation.
        """
        if not self._user_id:
            logger.debug("Cannot load patterns: no user_id set")
            return 0

        if not self._db_session_factory:
            logger.debug("Cannot load patterns: no db_session_factory")
            return 0

        try:
            from sqlalchemy import select

            from services.database.models import LearnedPattern
            from services.shared_types import PatternType

            async with self._db_session_factory.create_session() as session:
                result = await session.execute(
                    select(LearnedPattern).where(
                        LearnedPattern.user_id == self._user_id,
                        LearnedPattern.pattern_type == PatternType.INTEGRATION,
                        LearnedPattern.enabled == True,
                    )
                )
                db_patterns = result.scalars().all()

                for db_pattern in db_patterns:
                    pattern_data = db_pattern.pattern_data or {}
                    pattern = AttentionPattern(
                        pattern_id=str(db_pattern.id),
                        pattern_name=pattern_data.get("name", ""),
                        trigger_conditions=pattern_data.get("triggers", {}),
                        attention_response=pattern_data.get("attention_response", {}),
                        observation_count=db_pattern.usage_count or 0,
                        confidence=db_pattern.confidence or 0.0,
                        last_observed=db_pattern.last_used_at,
                    )
                    self._learned_patterns[pattern.pattern_name] = pattern

                logger.info(
                    "Loaded attention patterns from database",
                    extra={"count": len(db_patterns), "user_id": self._user_id},
                )
                return len(db_patterns)

        except Exception as e:
            logger.error(
                "Failed to load attention patterns",
                extra={"error": str(e), "user_id": self._user_id},
            )
            return 0

    # Core Attention Event Management

    def create_attention_event(
        self,
        source: AttentionSource,
        coordinates: SpatialCoordinates,
        base_intensity: float,
        urgency_level: float = 0.5,
        context: Optional[Dict[str, Any]] = None,
    ) -> AttentionEvent:
        """Create a new attention event"""

        event_id = f"attn_{uuid4().hex[:8]}"
        context = context or {}

        # Calculate personal relevance
        personal_relevance = self._calculate_personal_relevance(coordinates, context)

        # Create attention event with injectable clock for time simulation (#738)
        now = self._clock()
        event = AttentionEvent(
            event_id=event_id,
            source=source,
            spatial_coordinates=coordinates,
            base_intensity=base_intensity,
            urgency_level=urgency_level,
            personal_relevance=personal_relevance,
            created_at=now,
            last_updated=now,
        )

        # Populate from context
        if "actor_id" in context:
            event.actor_id = context["actor_id"]

        if "target_users" in context:
            event.target_users = set(context["target_users"])

        if "keywords" in context:
            event.keywords = context["keywords"]

        if "emotional_context" in context:
            event.emotional_context = context["emotional_context"]

        if "workflow_id" in context:
            event.workflow_id = context["workflow_id"]

        # Calculate spatial influence
        event.influence_radius, event.spatial_decay_factor = self._calculate_spatial_influence(
            coordinates, source, context
        )

        # Calculate relationship strength
        if event.actor_id:
            event.relationship_strength = self._calculate_relationship_strength(
                event.actor_id, coordinates
            )

        # Set expiration based on source and urgency
        event.expires_at = self._calculate_expiration_time(source, urgency_level)

        # Store event
        self._active_events[event_id] = event
        self._metrics["events_processed"] += 1

        # Check if this should trigger focus shift
        self._evaluate_focus_shift(event)

        # Learn from this event
        self._learn_from_attention_event(event)

        logger.debug(f"Created attention event: {source.value} at {coordinates.room_id}")

        return event

    def update_attention_event(self, event_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing attention event"""

        if event_id not in self._active_events:
            return False

        event = self._active_events[event_id]
        event.last_updated = self._clock()

        # Apply updates
        for key, value in updates.items():
            if hasattr(event, key):
                setattr(event, key, value)

        # Re-evaluate focus if significant changes
        if any(key in updates for key in ["base_intensity", "urgency_level", "expires_at"]):
            self._evaluate_focus_shift(event)

        return True

    def resolve_attention_event(self, event_id: str, resolution: str = "handled") -> bool:
        """Resolve an attention event"""

        if event_id not in self._active_events:
            return False

        event = self._active_events[event_id]

        # Record resolution in history
        resolution_record = {
            "event_id": event_id,
            "source": event.source.value,
            "coordinates": event.spatial_coordinates.to_slack_reference(),
            "resolution": resolution,
            "resolution_time": self._clock().isoformat(),
            "response_time": (self._clock() - event.created_at).total_seconds(),
            "final_intensity": event.get_current_intensity(),
        }

        self._attention_history.append(resolution_record)

        # Update metrics
        if resolution == "handled":
            self._metrics["successful_attention_responses"] += 1

        # Update average response time
        response_time = resolution_record["response_time"]
        current_avg = self._metrics["average_response_time"]
        total_responses = self._metrics["successful_attention_responses"]

        if total_responses > 0:
            self._metrics["average_response_time"] = (
                current_avg * (total_responses - 1) + response_time
            ) / total_responses

        # Remove from active events
        del self._active_events[event_id]

        # Re-evaluate focus
        self._update_attention_focus()

        logger.debug(f"Resolved attention event: {event_id} ({resolution})")

        return True

    # Attention Prioritization and Scoring

    def get_attention_priorities(
        self, current_coordinates: Optional[SpatialCoordinates] = None, max_results: int = 10
    ) -> List[Tuple[AttentionEvent, float]]:
        """Get prioritized list of attention events"""

        # Clean up expired events
        self._cleanup_expired_events()

        if not self._active_events:
            return []

        # Score all active events
        scored_events = []

        for event in self._active_events.values():
            score = self._calculate_attention_score(event, current_coordinates)
            if score > 0.0:
                scored_events.append((event, score))

        # Sort by score (highest first) and limit results
        scored_events.sort(key=lambda x: x[1], reverse=True)

        return scored_events[:max_results]

    def _calculate_attention_score(
        self, event: AttentionEvent, current_coordinates: Optional[SpatialCoordinates] = None
    ) -> float:
        """Calculate comprehensive attention score for an event"""

        # Base intensity with decay
        base_score = event.get_current_intensity(self._config["default_decay_model"])

        if base_score <= 0.0:
            return 0.0

        # Urgency multiplier
        urgency_multiplier = 1.0 + (event.urgency_level * self._config["urgency_boost_factor"])

        # Personal relevance factor
        relevance_factor = 0.5 + (event.personal_relevance * 0.5)

        # Proximity factor
        proximity_factor = 1.0
        if current_coordinates:
            proximity_factor = self._calculate_proximity_factor(
                current_coordinates, event.spatial_coordinates
            )

        # Relationship factor
        relationship_factor = 1.0
        if event.actor_id and event.relationship_strength > 0:
            relationship_factor = 1.0 + (
                event.relationship_strength * self._config["relationship_influence_factor"]
            )

        # Source-specific modifiers
        source_modifier = self._get_source_modifier(event.source)

        # Workflow priority boost
        workflow_boost = 1.0
        if event.workflow_id and event.deadline_pressure > 0:
            workflow_boost = 1.0 + (event.deadline_pressure * 0.3)

        # Emotional context modifier
        emotional_modifier = 1.0
        if event.emotional_context:
            if event.emotional_context == EmotionalValence.NEGATIVE:
                emotional_modifier = 1.2  # Negative emotions get attention boost
            elif event.emotional_context == EmotionalValence.POSITIVE:
                emotional_modifier = 1.1

        # Pattern-based adjustment
        pattern_adjustment = self._get_pattern_adjustment(event)

        # Calculate final score
        final_score = (
            base_score
            * urgency_multiplier
            * relevance_factor
            * proximity_factor
            * relationship_factor
            * source_modifier
            * workflow_boost
            * emotional_modifier
            * pattern_adjustment
        )

        return min(final_score, 10.0)  # Cap at 10.0

    def _calculate_proximity_factor(
        self, current_coords: SpatialCoordinates, event_coords: SpatialCoordinates
    ) -> float:
        """Calculate proximity-based attention factor"""

        # Same location - maximum proximity
        if (
            current_coords.territory_id == event_coords.territory_id
            and current_coords.room_id == event_coords.room_id
            and current_coords.path_id == event_coords.path_id
        ):
            return 1.0

        # Same room, different thread
        if (
            current_coords.territory_id == event_coords.territory_id
            and current_coords.room_id == event_coords.room_id
        ):
            return 0.8

        # Same territory, different room
        if current_coords.territory_id == event_coords.territory_id:
            return 0.6

        # Different territory
        return 0.3

    def _get_source_modifier(self, source: AttentionSource) -> float:
        """Get attention modifier based on event source"""

        modifiers = {
            AttentionSource.EMERGENCY: 2.0,
            AttentionSource.MENTION: 1.5,
            AttentionSource.WORKFLOW: 1.3,
            AttentionSource.THREAD: 1.2,
            AttentionSource.REACTION: 1.1,
            AttentionSource.MESSAGE: 1.0,
            AttentionSource.STATUS_CHANGE: 0.8,
            AttentionSource.ACTIVITY_SPIKE: 0.9,
            AttentionSource.SOCIAL: 0.7,
        }

        return modifiers.get(source, 1.0)

    # Focus Management

    def update_focus(
        self, coordinates: SpatialCoordinates, reason: str = "manual", strength: float = 1.0
    ) -> bool:
        """Update attention focus to new coordinates"""

        old_coordinates = self._attention_focus.primary_coordinates
        old_strength = self._attention_focus.focus_strength

        # Update focus
        self._attention_focus.primary_coordinates = coordinates
        self._attention_focus.focus_strength = strength
        self._attention_focus.focus_reason = reason
        self._attention_focus.last_shift = self._clock()

        # Calculate focus duration if we had previous focus
        if old_coordinates:
            focus_duration = self._clock() - self._attention_focus.established_at
            self._attention_focus.focus_duration += focus_duration
            self._metrics["focus_shifts"] += 1

        self._attention_focus.established_at = self._clock()

        # Record focus shift
        if old_coordinates != coordinates:
            focus_record = {
                "timestamp": self._clock().isoformat(),
                "from_coordinates": (
                    old_coordinates.to_slack_reference() if old_coordinates else None
                ),
                "to_coordinates": coordinates.to_slack_reference(),
                "reason": reason,
                "strength": strength,
                "previous_strength": old_strength,
            }

            # Store in spatial memory as attention pattern
            if old_coordinates:
                pattern_data = {
                    "focus_shift": focus_record,
                    "trigger_reason": reason,
                    "strength_change": strength - old_strength,
                }

                self.memory_store.learn_spatial_pattern(
                    "attention",
                    f"focus_shift_{reason}",
                    pattern_data,
                    0.5,
                    [coordinates.territory_id],
                )

        logger.info(
            f"Focus updated to {coordinates.room_id} (reason: {reason}, strength: {strength:.2f})"
        )

        return True

    def _evaluate_focus_shift(self, new_event: AttentionEvent) -> bool:
        """Evaluate if a new event should trigger focus shift"""

        # Get current attention score for the event
        event_score = self._calculate_attention_score(
            new_event, self._attention_focus.primary_coordinates
        )

        # Check if score exceeds focus threshold
        if event_score >= self._config["focus_threshold"]:
            # Additional checks for focus shift
            should_shift = False

            # Always shift for emergency events
            if new_event.source == AttentionSource.EMERGENCY:
                should_shift = True

            # Shift for high-priority mentions
            elif new_event.source == AttentionSource.MENTION and new_event.urgency_level > 0.7:
                should_shift = True

            # Shift if current focus is weak
            elif self._attention_focus.focus_strength < 0.5:
                should_shift = True

            # Shift based on pattern learning
            elif self._should_shift_based_on_patterns(new_event):
                should_shift = True

            if should_shift:
                return self.update_focus(
                    new_event.spatial_coordinates,
                    f"attention_event_{new_event.source.value}",
                    min(event_score / 5.0, 1.0),  # Scale score to strength
                )

        return False

    def _update_attention_focus(self):
        """Update attention focus based on current events"""

        # Get top priority events
        priorities = self.get_attention_priorities(self._attention_focus.primary_coordinates, 5)

        if not priorities:
            # No active events - reduce focus strength
            self._attention_focus.focus_strength *= 0.9
            return

        top_event, top_score = priorities[0]

        # Check if we should shift focus to top event
        if top_score >= self._config["focus_threshold"] and (
            not self._attention_focus.primary_coordinates
            or top_event.spatial_coordinates != self._attention_focus.primary_coordinates
        ):
            self.update_focus(
                top_event.spatial_coordinates,
                f"priority_shift_{top_event.source.value}",
                min(top_score / 5.0, 1.0),
            )

        # Update attention split based on secondary events
        if len(priorities) > 1:
            secondary_scores = [score for _, score in priorities[1:]]
            max_secondary = max(secondary_scores) if secondary_scores else 0.0

            self._attention_focus.attention_split = min(max_secondary / top_score, 1.0)

            # Store secondary foci
            self._attention_focus.secondary_foci = [
                (event.spatial_coordinates, score)
                for event, score in priorities[1:4]  # Top 3 secondary
            ]

    # Pattern Learning and Recognition

    def _learn_from_attention_event(self, event: AttentionEvent):
        """Learn patterns from attention events"""

        # Skip learning if below threshold
        if event.base_intensity < self._config["pattern_learning_threshold"]:
            return

        # Identify pattern triggers
        triggers = {
            "source": event.source.value,
            "territory": event.spatial_coordinates.territory_id,
            "room": event.spatial_coordinates.room_id,
            "urgency": event.urgency_level,
            "hour": event.created_at.hour,
            "day_of_week": event.created_at.weekday(),
        }

        if event.actor_id:
            triggers["actor"] = event.actor_id

        if event.keywords:
            triggers["has_keywords"] = True
            triggers["keyword_count"] = len(event.keywords)

        # Look for similar patterns
        pattern_name = f"{event.source.value}_{event.spatial_coordinates.territory_id}"

        if pattern_name in self._learned_patterns:
            pattern = self._learned_patterns[pattern_name]
            pattern.observation_count += 1
            pattern.last_observed = self._clock()

            # Update confidence based on consistency
            consistency = self._calculate_pattern_consistency(pattern, triggers)
            pattern.confidence = min(pattern.confidence + consistency * 0.1, 1.0)

        else:
            # Create new pattern
            pattern = AttentionPattern(
                pattern_id=f"attn_{uuid4().hex[:8]}",
                pattern_name=pattern_name,
                trigger_conditions=triggers,
                observation_count=1,
                confidence=0.3,
            )

            self._learned_patterns[pattern_name] = pattern

        self._metrics["pattern_matches"] += 1

        # Persist pattern to database (Issue #365)
        # Use fire-and-forget async save to avoid blocking
        if self._user_id and self._db_session_factory:
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self._save_pattern_to_db(pattern))
                else:
                    # If no event loop running, skip persistence
                    logger.debug("No event loop running, skipping pattern persistence")
            except RuntimeError:
                # No event loop available
                logger.debug("No event loop available, skipping pattern persistence")

    def _should_shift_based_on_patterns(self, event: AttentionEvent) -> bool:
        """Determine if focus should shift based on learned patterns"""

        # Look for matching patterns
        for pattern in self._learned_patterns.values():
            if pattern.confidence > 0.7 and self._pattern_matches_event(pattern, event):
                # Check if pattern suggests focus shift
                if "focus_shift_recommended" in pattern.attention_response:
                    return pattern.attention_response["focus_shift_recommended"]

        return False

    def _pattern_matches_event(self, pattern: AttentionPattern, event: AttentionEvent) -> bool:
        """Check if a pattern matches an event"""

        triggers = pattern.trigger_conditions

        # Check basic matching criteria
        if triggers.get("source") == event.source.value:
            return True

        if (
            triggers.get("territory") == event.spatial_coordinates.territory_id
            and triggers.get("urgency", 0) <= event.urgency_level
        ):
            return True

        return False

    # Helper Methods

    def _calculate_personal_relevance(
        self, coordinates: SpatialCoordinates, context: Dict[str, Any]
    ) -> float:
        """Calculate personal relevance of an attention event"""

        relevance = 0.5  # Base relevance

        # Direct mentions increase relevance
        if "target_users" in context and "piper" in context["target_users"]:
            relevance += 0.4

        # Keywords that indicate relevance to Piper Morgan
        keywords = context.get("keywords", [])
        relevant_keywords = ["help", "question", "issue", "problem", "piper", "urgent"]

        keyword_matches = sum(1 for kw in keywords if kw.lower() in relevant_keywords)
        relevance += min(keyword_matches * 0.1, 0.3)

        # Room-based relevance (some rooms are more relevant)
        room_memory = self.memory_store.get_memory_record(coordinates.room_id)
        if room_memory:
            if room_memory.purpose in ["support", "coordination"]:
                relevance += 0.2

        return min(relevance, 1.0)

    def _calculate_spatial_influence(
        self, coordinates: SpatialCoordinates, source: AttentionSource, context: Dict[str, Any]
    ) -> Tuple[str, float]:
        """Calculate spatial influence radius and decay factor"""

        # Determine influence radius based on source
        if source == AttentionSource.EMERGENCY:
            radius = "global"
            decay_factor = 1.0
        elif source == AttentionSource.MENTION:
            radius = "territory"
            decay_factor = 0.9
        elif source in [AttentionSource.MESSAGE, AttentionSource.THREAD]:
            radius = "room"
            decay_factor = 0.8
        else:
            radius = "local"
            decay_factor = 0.7

        # Adjust based on context
        if context.get("broadcast", False):
            if radius == "room":
                radius = "territory"
            elif radius == "local":
                radius = "room"
            decay_factor = min(decay_factor + 0.1, 1.0)

        return radius, decay_factor

    def _calculate_relationship_strength(
        self, actor_id: str, coordinates: SpatialCoordinates
    ) -> float:
        """Calculate relationship strength with actor"""

        # This would integrate with user relationship tracking
        # For now, return default moderate strength
        return 0.5

    def _calculate_expiration_time(
        self, source: AttentionSource, urgency_level: float
    ) -> Optional[datetime]:
        """Calculate when attention event should expire"""

        base_duration = {
            AttentionSource.EMERGENCY: timedelta(hours=4),
            AttentionSource.MENTION: timedelta(hours=2),
            AttentionSource.WORKFLOW: timedelta(hours=8),
            AttentionSource.THREAD: timedelta(hours=1),
            AttentionSource.MESSAGE: timedelta(minutes=30),
            AttentionSource.REACTION: timedelta(minutes=15),
            AttentionSource.STATUS_CHANGE: timedelta(minutes=10),
            AttentionSource.ACTIVITY_SPIKE: timedelta(minutes=20),
            AttentionSource.SOCIAL: timedelta(minutes=45),
        }

        duration = base_duration.get(source, timedelta(hours=1))

        # Extend duration for high urgency
        if urgency_level > 0.7:
            duration = duration * (1.0 + urgency_level)

        return self._clock() + duration

    def _cleanup_expired_events(self):
        """Remove expired attention events"""

        current_time = self._clock()
        expired_events = [
            event_id
            for event_id, event in self._active_events.items()
            if event.expires_at and current_time > event.expires_at
        ]

        for event_id in expired_events:
            del self._active_events[event_id]

        if expired_events:
            logger.debug(f"Cleaned up {len(expired_events)} expired attention events")

    def _calculate_pattern_consistency(
        self, pattern: AttentionPattern, new_triggers: Dict[str, Any]
    ) -> float:
        """Calculate how consistent new triggers are with existing pattern"""

        existing_triggers = pattern.trigger_conditions

        # Calculate similarity between trigger sets
        common_keys = set(existing_triggers.keys()) & set(new_triggers.keys())
        if not common_keys:
            return 0.0

        matches = 0
        for key in common_keys:
            if existing_triggers[key] == new_triggers[key]:
                matches += 1

        return matches / len(common_keys)

    def _get_pattern_adjustment(self, event: AttentionEvent) -> float:
        """Get pattern-based score adjustment"""

        # Look for patterns that apply to this event
        applicable_patterns = [
            p
            for p in self._learned_patterns.values()
            if self._pattern_matches_event(p, event) and p.confidence > 0.5
        ]

        if not applicable_patterns:
            return 1.0

        # Average pattern confidence as adjustment
        avg_confidence = sum(p.confidence for p in applicable_patterns) / len(applicable_patterns)

        return 1.0 + (avg_confidence * 0.2)  # Up to 20% boost

    # Status and Analytics

    def get_attention_status(self) -> Dict[str, Any]:
        """Get current attention model status"""

        self._cleanup_expired_events()

        # Calculate attention distribution
        attention_by_territory = {}
        attention_by_source = {}

        for event in self._active_events.values():
            territory = event.spatial_coordinates.territory_id
            source = event.source.value

            intensity = event.get_current_intensity()

            attention_by_territory[territory] = (
                attention_by_territory.get(territory, 0.0) + intensity
            )
            attention_by_source[source] = attention_by_source.get(source, 0.0) + intensity

        return {
            "active_events": len(self._active_events),
            "current_focus": {
                "coordinates": (
                    self._attention_focus.primary_coordinates.to_slack_reference()
                    if self._attention_focus.primary_coordinates
                    else None
                ),
                "strength": self._attention_focus.focus_strength,
                "reason": self._attention_focus.focus_reason,
                "duration": self._attention_focus.focus_duration.total_seconds(),
                "attention_split": self._attention_focus.attention_split,
                "secondary_foci_count": len(self._attention_focus.secondary_foci),
            },
            "attention_distribution": {
                "by_territory": attention_by_territory,
                "by_source": attention_by_source,
            },
            "learned_patterns": len(self._learned_patterns),
            "metrics": self._metrics.copy(),
            "configuration": self._config.copy(),
        }

    def get_attention_insights(self) -> Dict[str, Any]:
        """Get insights about attention patterns and performance"""

        insights = {
            "total_events_processed": self._metrics["events_processed"],
            "average_response_time": self._metrics["average_response_time"],
            "attention_efficiency": self._metrics["attention_efficiency"],
            "most_common_sources": {},
            "peak_attention_hours": {},
            "pattern_effectiveness": {},
            "focus_patterns": {},
        }

        # Analyze attention history
        if self._attention_history:
            # Most common sources
            source_counts = {}
            for record in self._attention_history[-100:]:  # Last 100 events
                source = record["source"]
                source_counts[source] = source_counts.get(source, 0) + 1

            insights["most_common_sources"] = dict(
                sorted(source_counts.items(), key=lambda x: x[1], reverse=True)
            )

            # Peak attention hours
            hour_activity = {}
            for record in self._attention_history[-100:]:
                try:
                    hour = datetime.fromisoformat(record["resolution_time"]).hour
                    hour_activity[hour] = hour_activity.get(hour, 0) + 1
                except Exception:
                    continue

            if hour_activity:
                peak_hour = max(hour_activity.keys(), key=lambda h: hour_activity[h])
                insights["peak_attention_hours"] = {
                    "peak_hour": peak_hour,
                    "hourly_distribution": hour_activity,
                }

        # Pattern effectiveness
        for pattern_name, pattern in self._learned_patterns.items():
            if pattern.observation_count > 5:
                insights["pattern_effectiveness"][pattern_name] = {
                    "confidence": pattern.confidence,
                    "observations": pattern.observation_count,
                    "success_rate": pattern.success_rate,
                }

        return insights
