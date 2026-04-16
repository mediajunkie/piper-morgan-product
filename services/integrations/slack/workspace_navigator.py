"""
Slack Workspace Navigator - Multi-Territory Navigation Intelligence
Implements intelligent navigation across multiple Slack workspaces (territories).

Provides multi-workspace territory switching and navigation including:
- Cross-territory context switching and state management
- Intelligent territory selection based on activity and priorities
- Multi-workspace relationship mapping and navigation
- Territory-specific navigation optimization
- Cross-workspace pattern recognition and learning
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import uuid4

from .spatial_memory import SpatialMemoryStore, SpatialPattern
from .spatial_types import (
    AttentionLevel,
    EmotionalValence,
    SpatialCoordinates,
    Territory,
    TerritoryType,
)

logger = logging.getLogger(__name__)


class NavigationIntent(Enum):
    """Intent behind navigation decisions"""

    EXPLORATION = "exploration"  # Discovering new areas
    ATTENTION_RESPONSE = "attention"  # Responding to attention attractors
    PATROL = "patrol"  # Regular monitoring rounds
    WORKFLOW = "workflow"  # Following workflow patterns
    SOCIAL = "social"  # Social interaction priorities
    EMERGENCY = "emergency"  # Urgent response navigation
    OPTIMIZATION = "optimization"  # Efficiency-based routing


class TerritoryStatus(Enum):
    """Current status of a territory"""

    ACTIVE = "active"  # Currently being monitored
    BACKGROUND = "background"  # Passively monitored
    PAUSED = "paused"  # Temporarily not monitored
    OFFLINE = "offline"  # Not accessible
    MAINTENANCE = "maintenance"  # Under maintenance/setup


@dataclass
class NavigationContext:
    """Context information for navigation decisions"""

    intent: NavigationIntent
    priority: float  # 0.0 to 1.0
    time_sensitive: bool = False
    estimated_duration: Optional[float] = None  # seconds
    required_capabilities: Set[str] = field(default_factory=set)
    context_data: Dict[str, Any] = field(default_factory=dict)

    # Workflow integration
    workflow_id: Optional[str] = None
    task_context: Optional[Dict[str, Any]] = None

    # Social context
    target_users: Set[str] = field(default_factory=set)
    interaction_type: Optional[str] = None


@dataclass
class TerritoryState:
    """Current state of a territory in the navigator"""

    territory_id: str
    territory_name: str
    territory_type: TerritoryType
    status: TerritoryStatus

    # Current position within territory
    current_room: Optional[str] = None
    last_room: Optional[str] = None
    entry_time: Optional[datetime] = None

    # Activity and attention tracking
    attention_score: float = 0.0  # Current attention priority
    activity_level: float = 0.0  # Current activity level
    unread_mentions: int = 0
    pending_workflows: List[str] = field(default_factory=list)

    # Navigation efficiency
    navigation_efficiency: float = 1.0  # How efficiently we navigate this territory
    frequent_paths: Dict[str, int] = field(default_factory=dict)  # path -> usage_count

    # Territory-specific capabilities
    available_capabilities: Set[str] = field(default_factory=set)
    permission_level: str = "basic"  # basic, elevated, admin

    # Learning data
    optimal_visit_frequency: Optional[timedelta] = None
    peak_activity_hours: List[int] = field(default_factory=list)
    typical_session_duration: Optional[float] = None

    def get_priority_score(self) -> float:
        """Calculate current priority score for this territory"""
        base_score = self.attention_score * 0.4 + self.activity_level * 0.3

        # Boost for unread mentions
        mention_boost = min(self.unread_mentions * 0.1, 0.5)

        # Boost for pending workflows
        workflow_boost = min(len(self.pending_workflows) * 0.05, 0.3)

        # Efficiency factor
        efficiency_factor = 0.5 + (self.navigation_efficiency * 0.5)

        return min((base_score + mention_boost + workflow_boost) * efficiency_factor, 1.0)


@dataclass
class NavigationPlan:
    """Plan for navigation across territories"""

    plan_id: str
    intent: NavigationIntent
    total_estimated_time: float
    confidence: float

    # Planned navigation steps
    steps: List[Dict[str, Any]] = field(default_factory=list)
    alternative_plans: List["NavigationPlan"] = field(default_factory=list)

    # Execution tracking
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    current_step: int = 0

    # Performance prediction
    predicted_outcomes: Dict[str, Any] = field(default_factory=dict)
    risk_factors: List[str] = field(default_factory=list)


class WorkspaceNavigator:
    """
    Multi-territory navigation intelligence for Slack workspaces.

    Manages navigation across multiple Slack workspaces (territories) with
    intelligent routing, context switching, and cross-workspace optimization.
    """

    def __init__(self, memory_store: Optional[SpatialMemoryStore] = None):
        self.memory_store = memory_store or SpatialMemoryStore()

        # Territory management
        self._territories: Dict[str, TerritoryState] = {}
        self._current_territory: Optional[str] = None
        self._navigation_history: List[Dict[str, Any]] = []

        # Navigation planning
        self._active_plans: Dict[str, NavigationPlan] = {}
        self._navigation_patterns: Dict[str, Any] = {}

        # Performance optimization
        self._navigation_metrics: Dict[str, Any] = {
            "total_navigations": 0,
            "successful_navigations": 0,
            "average_navigation_time": 0.0,
            "territory_switches": 0,
            "pattern_matches": 0,
        }

        # Configuration
        self._max_concurrent_territories = 5
        self._auto_patrol_interval = timedelta(minutes=10)
        self._attention_threshold = 0.7
        self._last_patrol_time = datetime.now()

        logger.info("WorkspaceNavigator initialized")

    # Territory Management

    def register_territory(
        self,
        territory: Territory,
        initial_status: TerritoryStatus = TerritoryStatus.BACKGROUND,
        capabilities: Optional[Set[str]] = None,
    ) -> TerritoryState:
        """Register a new territory for navigation"""

        territory_state = TerritoryState(
            territory_id=territory.id,
            territory_name=territory.name,
            territory_type=territory.territory_type,
            status=initial_status,
            available_capabilities=capabilities or set(),
        )

        self._territories[territory.id] = territory_state

        # Initialize in spatial memory
        self.memory_store.record_spatial_visit(
            territory.id,
            "territory",
            territory.name,
            context={
                "territory_type": territory.territory_type.value,
                "registration_time": datetime.now().isoformat(),
                "capabilities": list(capabilities or []),
            },
        )

        logger.info(f"Registered territory: {territory.name} ({territory.territory_type.value})")

        return territory_state

    def set_territory_status(self, territory_id: str, status: TerritoryStatus) -> bool:
        """Set the status of a territory"""

        if territory_id not in self._territories:
            return False

        old_status = self._territories[territory_id].status
        self._territories[territory_id].status = status

        logger.info(f"Territory {territory_id} status: {old_status.value} -> {status.value}")

        # Handle status-specific logic
        if status == TerritoryStatus.ACTIVE and old_status != TerritoryStatus.ACTIVE:
            self._territories[territory_id].entry_time = datetime.now()

        return True

    def switch_territory(
        self, target_territory_id: str, context: Optional[NavigationContext] = None
    ) -> bool:
        """Switch to a different territory"""

        if target_territory_id not in self._territories:
            logger.error(f"Unknown territory: {target_territory_id}")
            return False

        # Record navigation
        old_territory = self._current_territory
        switch_time = datetime.now()

        # Update previous territory
        if old_territory and old_territory in self._territories:
            old_state = self._territories[old_territory]
            if old_state.status == TerritoryStatus.ACTIVE:
                old_state.status = TerritoryStatus.BACKGROUND

                # Calculate session duration
                if old_state.entry_time:
                    session_duration = (switch_time - old_state.entry_time).total_seconds()
                    if old_state.typical_session_duration:
                        old_state.typical_session_duration = (
                            old_state.typical_session_duration * 0.8 + session_duration * 0.2
                        )
                    else:
                        old_state.typical_session_duration = session_duration

        # Activate new territory
        new_state = self._territories[target_territory_id]
        new_state.status = TerritoryStatus.ACTIVE
        new_state.entry_time = switch_time

        self._current_territory = target_territory_id

        # Record in navigation history
        navigation_record = {
            "timestamp": switch_time.isoformat(),
            "from_territory": old_territory,
            "to_territory": target_territory_id,
            "context": context.context_data if context else {},
            "intent": context.intent.value if context else "manual",
        }

        self._navigation_history.append(navigation_record)
        self._navigation_metrics["territory_switches"] += 1

        # Record relationship in spatial memory
        if old_territory:
            self.memory_store.record_spatial_relationship(
                old_territory,
                target_territory_id,
                "territory_switch",
                {
                    "switch_time": switch_time.isoformat(),
                    "intent": context.intent.value if context else "manual",
                },
            )

        logger.info(f"Switched territory: {old_territory} -> {target_territory_id}")

        return True

    # Navigation Planning and Execution

    def plan_navigation(
        self, target_coordinates: SpatialCoordinates, context: NavigationContext
    ) -> Optional[NavigationPlan]:
        """Plan navigation to target coordinates"""

        plan_id = f"nav_{uuid4().hex[:8]}"

        # Determine if territory switch is needed
        current_territory = self._current_territory
        target_territory = target_coordinates.territory_id
        needs_territory_switch = current_territory != target_territory

        steps = []
        estimated_time = 0.0
        confidence = 1.0

        # Step 1: Territory switch if needed
        if needs_territory_switch:
            if target_territory not in self._territories:
                logger.error(f"Target territory not registered: {target_territory}")
                return None

            territory_state = self._territories[target_territory]

            # Estimate territory switch time
            switch_time = self._estimate_territory_switch_time(current_territory, target_territory)
            steps.append(
                {
                    "type": "territory_switch",
                    "from_territory": current_territory,
                    "to_territory": target_territory,
                    "estimated_time": switch_time,
                    "requirements": [],
                }
            )
            estimated_time += switch_time

            # Reduce confidence if territory is offline or has issues
            if territory_state.status == TerritoryStatus.OFFLINE:
                confidence *= 0.3
            elif territory_state.status == TerritoryStatus.MAINTENANCE:
                confidence *= 0.6

        # Step 2: Room navigation within territory
        if target_coordinates.room_id:
            room_navigation = self._plan_room_navigation(
                target_territory, target_coordinates.room_id, context
            )

            if room_navigation:
                steps.extend(room_navigation["steps"])
                estimated_time += room_navigation["estimated_time"]
                confidence *= room_navigation["confidence"]

        # Step 3: Path navigation within room (if thread/conversation path)
        if target_coordinates.path_id:
            path_time = 2.0  # Estimated time to navigate to thread
            steps.append(
                {
                    "type": "path_navigation",
                    "target_path": target_coordinates.path_id,
                    "estimated_time": path_time,
                    "requirements": ["thread_access"],
                }
            )
            estimated_time += path_time

        # Create navigation plan
        plan = NavigationPlan(
            plan_id=plan_id,
            intent=context.intent,
            total_estimated_time=estimated_time,
            confidence=confidence,
            steps=steps,
        )

        # Add risk factors
        plan.risk_factors = self._assess_navigation_risks(target_coordinates, context)

        # Generate alternatives if confidence is low
        if confidence < 0.7:
            alternatives = self._generate_alternative_plans(target_coordinates, context)
            plan.alternative_plans = alternatives

        self._active_plans[plan_id] = plan

        logger.info(f"Navigation plan created: {len(steps)} steps, {estimated_time:.1f}s estimated")

        return plan

    def execute_navigation_plan(self, plan: NavigationPlan) -> bool:
        """Execute a navigation plan"""

        if plan.started_at:
            logger.warning(f"Plan {plan.plan_id} already started")
            return False

        plan.started_at = datetime.now()
        success = True

        try:
            for i, step in enumerate(plan.steps):
                plan.current_step = i
                step_success = self._execute_navigation_step(step, plan)

                if not step_success:
                    success = False
                    logger.error(f"Navigation step {i} failed: {step['type']}")
                    break

                # Update metrics
                self._navigation_metrics["total_navigations"] += 1

        except Exception as e:
            logger.error(f"Navigation plan execution failed: {e}")
            success = False

        # Complete plan
        plan.completed_at = datetime.now()

        if success:
            self._navigation_metrics["successful_navigations"] += 1

            # Update average navigation time
            execution_time = (plan.completed_at - plan.started_at).total_seconds()
            current_avg = self._navigation_metrics["average_navigation_time"]
            total_navs = self._navigation_metrics["total_navigations"]

            self._navigation_metrics["average_navigation_time"] = (
                current_avg * (total_navs - 1) + execution_time
            ) / total_navs

        # Clean up completed plan
        if plan.plan_id in self._active_plans:
            del self._active_plans[plan.plan_id]

        logger.info(f"Navigation plan {'completed' if success else 'failed'}: {plan.plan_id}")

        return success

    def _execute_navigation_step(self, step: Dict[str, Any], plan: NavigationPlan) -> bool:
        """Execute a single navigation step"""

        step_type = step["type"]

        if step_type == "territory_switch":
            target_territory = step["to_territory"]
            context = NavigationContext(intent=plan.intent, priority=0.8)
            return self.switch_territory(target_territory, context)

        elif step_type == "room_navigation":
            target_room = step["target_room"]
            return self._navigate_to_room(target_room)

        elif step_type == "path_navigation":
            target_path = step["target_path"]
            return self._navigate_to_path(target_path)

        else:
            logger.warning(f"Unknown navigation step type: {step_type}")
            return False

    # Intelligent Navigation Features

    def suggest_next_territory(self, context: Optional[NavigationContext] = None) -> Optional[str]:
        """Suggest the next territory to visit based on priorities and patterns"""

        if not self._territories:
            return None

        # Score all available territories
        territory_scores = {}

        for territory_id, state in self._territories.items():
            if state.status == TerritoryStatus.OFFLINE:
                continue

            score = state.get_priority_score()

            # Apply context-based adjustments
            if context:
                if context.intent == NavigationIntent.EMERGENCY:
                    # Boost territories with emergency capabilities
                    if "emergency_response" in state.available_capabilities:
                        score *= 1.5

                elif context.intent == NavigationIntent.SOCIAL:
                    # Boost territories with target users
                    if context.target_users:
                        # This would need integration with user presence tracking
                        pass

                elif context.intent == NavigationIntent.WORKFLOW:
                    # Boost territories with pending workflows
                    if state.pending_workflows:
                        score *= 1.0 + len(state.pending_workflows) * 0.2

            # Pattern-based adjustments
            patterns = self.memory_store.find_patterns("navigation", territory_id, 0.5)
            if patterns:
                pattern_boost = sum(p.confidence for p in patterns[:3]) / len(patterns[:3])
                score *= 1.0 + pattern_boost * 0.3

            territory_scores[territory_id] = score

        # Return highest-scoring territory
        if territory_scores:
            best_territory = max(territory_scores.keys(), key=lambda t: territory_scores[t])
            return best_territory

        return None

    def auto_patrol(self) -> List[str]:
        """Perform automatic patrol of territories based on learned patterns"""

        if datetime.now() - self._last_patrol_time < self._auto_patrol_interval:
            return []

        visited_territories = []

        # Find territories that need attention
        for territory_id, state in self._territories.items():
            if (
                state.status in [TerritoryStatus.ACTIVE, TerritoryStatus.BACKGROUND]
                and state.get_priority_score() > self._attention_threshold
            ):
                # Quick visit to check status
                if self.switch_territory(territory_id):
                    visited_territories.append(territory_id)

                    # Update attention score based on what we find
                    state.attention_score *= 0.8  # Decay after visit

        self._last_patrol_time = datetime.now()

        if visited_territories:
            logger.info(f"Auto-patrol completed: visited {len(visited_territories)} territories")

        return visited_territories

    def learn_navigation_pattern(
        self, pattern_data: Dict[str, Any], confidence: float = 0.5
    ) -> bool:
        """Learn a new navigation pattern from observed behavior"""

        pattern_type = "navigation"
        pattern_name = pattern_data.get("name", f"pattern_{uuid4().hex[:8]}")

        # Determine applicable territories
        applicable_territories = []
        if "territories" in pattern_data:
            applicable_territories = pattern_data["territories"]
        elif "current_territory" in pattern_data:
            applicable_territories = [pattern_data["current_territory"]]

        # Store pattern in spatial memory
        pattern = self.memory_store.learn_spatial_pattern(
            pattern_type, pattern_name, pattern_data, confidence, applicable_territories
        )

        self._navigation_metrics["pattern_matches"] += 1

        logger.info(f"Learned navigation pattern: {pattern_name} (confidence: {confidence:.2f})")

        return True

    # Helper Methods

    def _plan_room_navigation(
        self, territory_id: str, target_room_id: str, context: NavigationContext
    ) -> Optional[Dict[str, Any]]:
        """Plan navigation within a territory to a specific room"""

        # Get current room in territory
        territory_state = self._territories.get(territory_id)
        if not territory_state:
            return None

        current_room = territory_state.current_room

        # Check if we're already in the target room
        if current_room == target_room_id:
            return {"steps": [], "estimated_time": 0.0, "confidence": 1.0}

        # Estimate navigation time based on room relationships
        if current_room:
            relationship = self.memory_store._relationships.get(
                f"{current_room}->{target_room_id}:adjacent"
            )
            if relationship:
                estimated_time = relationship.typical_transition_time or 3.0
                confidence = relationship.strength
            else:
                # Unknown path - estimate conservatively
                estimated_time = 8.0
                confidence = 0.5
        else:
            # No current room - direct navigation
            estimated_time = 5.0
            confidence = 0.7

        steps = [
            {
                "type": "room_navigation",
                "from_room": current_room,
                "target_room": target_room_id,
                "estimated_time": estimated_time,
                "requirements": ["room_access"],
            }
        ]

        return {"steps": steps, "estimated_time": estimated_time, "confidence": confidence}

    def _estimate_territory_switch_time(
        self, from_territory: Optional[str], to_territory: str
    ) -> float:
        """Estimate time required for territory switch"""

        if not from_territory:
            return 2.0  # Initial territory entry

        # Look for historical switch time in relationships
        relationship = self.memory_store._relationships.get(
            f"{from_territory}->{to_territory}:territory_switch"
        )

        if relationship and relationship.typical_transition_time:
            return relationship.typical_transition_time

        # Estimate based on territory types
        from_state = self._territories.get(from_territory)
        to_state = self._territories.get(to_territory)

        base_time = 4.0

        # Adjust based on territory characteristics
        if to_state and to_state.status == TerritoryStatus.MAINTENANCE:
            base_time *= 1.5

        if from_state and to_state:
            # Corporate to corporate is typically faster
            if (
                from_state.territory_type == TerritoryType.CORPORATE
                and to_state.territory_type == TerritoryType.CORPORATE
            ):
                base_time *= 0.8

        return base_time

    def _navigate_to_room(self, room_id: str) -> bool:
        """Navigate to a specific room within current territory"""

        if not self._current_territory:
            return False

        territory_state = self._territories[self._current_territory]

        # Update current room
        old_room = territory_state.current_room
        territory_state.last_room = old_room
        territory_state.current_room = room_id

        # Record the navigation
        self.memory_store.record_spatial_visit(
            room_id,
            "room",
            f"Room {room_id}",
            context={
                "navigation_time": datetime.now().isoformat(),
                "previous_room": old_room,
                "territory": self._current_territory,
            },
        )

        # Record room relationship if we have a previous room
        if old_room:
            self.memory_store.record_spatial_relationship(
                old_room, room_id, "adjacent", {"navigation_time": datetime.now().isoformat()}
            )

        logger.debug(f"Navigated to room: {room_id} in territory {self._current_territory}")

        return True

    def _navigate_to_path(self, path_id: str) -> bool:
        """Navigate to a specific conversational path (thread)"""

        # This would involve focusing on a specific thread
        # For now, just log the navigation

        logger.debug(f"Navigated to conversational path: {path_id}")

        return True

    def _assess_navigation_risks(
        self, target_coordinates: SpatialCoordinates, context: NavigationContext
    ) -> List[str]:
        """Assess potential risks for navigation"""

        risks = []

        target_territory = target_coordinates.territory_id

        if target_territory in self._territories:
            territory_state = self._territories[target_territory]

            if territory_state.status == TerritoryStatus.OFFLINE:
                risks.append("target_territory_offline")

            if territory_state.status == TerritoryStatus.MAINTENANCE:
                risks.append("target_territory_maintenance")

            if territory_state.navigation_efficiency < 0.5:
                risks.append("low_navigation_efficiency")

            # Check capability requirements
            if context.required_capabilities:
                missing_caps = (
                    context.required_capabilities - territory_state.available_capabilities
                )
                if missing_caps:
                    risks.append(f"missing_capabilities: {', '.join(missing_caps)}")

        else:
            risks.append("unknown_territory")

        return risks

    def _generate_alternative_plans(
        self, target_coordinates: SpatialCoordinates, context: NavigationContext
    ) -> List[NavigationPlan]:
        """Generate alternative navigation plans"""

        # For now, return empty list
        # In full implementation, would generate alternative routes
        return []

    # Status and Analytics

    def get_navigation_status(self) -> Dict[str, Any]:
        """Get current navigation status and statistics"""

        return {
            "current_territory": self._current_territory,
            "registered_territories": len(self._territories),
            "active_territories": len(
                [t for t in self._territories.values() if t.status == TerritoryStatus.ACTIVE]
            ),
            "active_plans": len(self._active_plans),
            "navigation_metrics": self._navigation_metrics.copy(),
            "last_patrol": self._last_patrol_time.isoformat(),
            "territories": {
                tid: {
                    "name": state.territory_name,
                    "status": state.status.value,
                    "priority_score": state.get_priority_score(),
                    "current_room": state.current_room,
                    "unread_mentions": state.unread_mentions,
                    "pending_workflows": len(state.pending_workflows),
                }
                for tid, state in self._territories.items()
            },
        }

    def get_territory_insights(self, territory_id: str) -> Optional[Dict[str, Any]]:
        """Get insights about a specific territory"""

        if territory_id not in self._territories:
            return None

        state = self._territories[territory_id]
        memory = self.memory_store.get_memory_record(territory_id)

        insights = {
            "territory_id": territory_id,
            "name": state.territory_name,
            "type": state.territory_type.value,
            "status": state.status.value,
            "priority_score": state.get_priority_score(),
            "navigation_efficiency": state.navigation_efficiency,
            "visit_statistics": {},
            "room_count": 0,
            "relationship_count": 0,
            "learned_patterns": 0,
        }

        if memory:
            insights["visit_statistics"] = {
                "first_discovered": memory.first_discovered.isoformat(),
                "last_visited": memory.last_visited.isoformat(),
                "visit_count": memory.visit_count,
                "total_time_spent": memory.total_time_spent,
            }

        # Get room count for this territory
        territory_rooms = self.memory_store.get_room_memories(territory_id)
        insights["room_count"] = len(territory_rooms)

        # Get relationship count
        connected_spaces = self.memory_store.get_connected_spaces(territory_id)
        insights["relationship_count"] = len(connected_spaces)

        # Get learned patterns
        patterns = self.memory_store.find_patterns(applicable_to=territory_id)
        insights["learned_patterns"] = len(patterns)

        return insights
