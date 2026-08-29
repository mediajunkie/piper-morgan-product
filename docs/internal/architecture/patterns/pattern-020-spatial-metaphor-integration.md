# Pattern-020: Spatial Metaphor Integration Pattern (PM-074)

## Status

**Proven**

## Context

Traditional event processing systems treat external events (like Slack messages) as abstract data points without spatial context, making it difficult for AI agents to develop natural navigation patterns and environmental awareness. Without spatial metaphors, AI interactions lack the embodied experience that enables intuitive prioritization, memory formation, and contextual understanding. The Spatial Metaphor Integration Pattern addresses:

- Creating embodied AI experiences through physical space metaphors
- Enabling natural navigation and interaction patterns for AI agents
- Providing persistent spatial memory across sessions for pattern learning
- Supporting intelligent attention management with contextual prioritization
- Integrating spatial events seamlessly with workflow systems
- Maintaining coherent spatial metaphors across multi-workspace environments

## Pattern Description

The Spatial Metaphor Integration Pattern processes external system events as spatial changes to an AI agent's environment, creating embodied AI experiences through persistent spatial memory, attention-based prioritization, and natural navigation patterns. The pattern maps abstract events to spatial objects and locations, enabling AI agents to develop environmental awareness and contextual understanding.

## Implementation

### Structure

```python
# Spatial metaphor integration framework
class SpatialMetaphorEngine:
    def __init__(self):
        self.spatial_memory = SpatialMemoryStore()
        self.attention_model = AttentionModel()
        self.workspace_navigator = WorkspaceNavigator()
        self.spatial_mapper = SpatialMapper()

    async def process_external_event(self, event: ExternalEvent) -> SpatialProcessingResult:
        """Process external event through spatial metaphor system"""
        pass

    def create_spatial_context(self, event_data: Dict[str, Any]) -> SpatialContext:
        """Create spatial context from event data"""
        pass

    async def update_attention_model(self, spatial_event: SpatialEvent) -> AttentionUpdate:
        """Update attention model based on spatial event"""
        pass
```

### Example (Core Spatial Architecture)

```python
from dataclasses import dataclass, field
from typing import Dict, Any, Set, List, Optional
from datetime import datetime
from enum import Enum
import math
import uuid

class TerritoryType(Enum):
    CORPORATE = "corporate"
    STARTUP = "startup"
    COMMUNITY = "community"

class RoomPurpose(Enum):
    GENERAL = "general"
    ANNOUNCEMENT = "announcement"
    DISCUSSION = "discussion"
    PROJECT_WORK = "project_work"
    COORDINATION = "coordination"
    SOCIAL = "social"
    SUPPORT = "support"
    PRIVATE_MEETING = "private_meeting"

class AttentionSource(Enum):
    MENTION = "mention"
    MESSAGE = "message"
    EMERGENCY = "emergency"
    WORKFLOW = "workflow"

class AttentionDecay(Enum):
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    STEP = "step"

@dataclass
class Territory:
    """Slack workspace as navigable territory/building"""
    id: str
    name: str
    territory_type: TerritoryType
    domain: Optional[str] = None
    spatial_properties: Dict[str, Any] = field(default_factory=dict)

    def get_spatial_description(self) -> str:
        """Generate natural language description of territory"""
        type_descriptions = {
            TerritoryType.CORPORATE: "a structured corporate office building",
            TerritoryType.STARTUP: "a dynamic startup workspace with flexible areas",
            TerritoryType.COMMUNITY: "an open community center with diverse spaces"
        }
        return f"{self.name} - {type_descriptions[self.territory_type]}"

@dataclass
class Room:
    """Slack channel as specialized room with purpose"""
    id: str
    name: str
    territory_id: str
    purpose: RoomPurpose
    inhabitants: Set[str] = field(default_factory=set)
    attention_history: List[Dict[str, Any]] = field(default_factory=list)

    def get_room_atmosphere(self) -> Dict[str, Any]:
        """Calculate room atmosphere based on recent activity"""
        recent_activity = len([event for event in self.attention_history
                             if (datetime.now() - event['timestamp']).seconds < 3600])

        atmosphere_levels = {
            'activity_level': min(recent_activity / 10.0, 1.0),
            'collaboration_intensity': len(self.inhabitants) / 20.0,
            'urgency_indicator': max([event.get('urgency', 0.0)
                                   for event in self.attention_history[-5:]], default=0.0)
        }
        return atmosphere_levels

@dataclass
class SpatialCoordinates:
    """Precise spatial location within the metaphor system"""
    territory_id: str
    room_id: str
    object_id: Optional[str] = None

    def to_slack_reference(self) -> str:
        """Convert spatial coordinates to Slack reference"""
        if self.object_id:
            return f"<#{self.room_id}|{self.room_id}>:{self.object_id}"
        return f"<#{self.room_id}|{self.room_id}>"

@dataclass
class AttentionEvent:
    """Attention-generating event with decay models"""
    event_id: str
    source: AttentionSource
    spatial_coordinates: SpatialCoordinates
    base_intensity: float  # 0.0 to 1.0
    urgency_level: float
    keywords: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def get_current_intensity(self, decay_model: AttentionDecay = AttentionDecay.EXPONENTIAL) -> float:
        """Calculate attention intensity with temporal decay"""
        age = (datetime.now() - self.created_at).total_seconds()

        if decay_model == AttentionDecay.EXPONENTIAL:
            half_life = 1800.0  # 30 minutes
            return self.base_intensity * math.exp(-age * math.log(2) / half_life)
        elif decay_model == AttentionDecay.LINEAR:
            decay_rate = 0.1  # 10% per hour
            return max(0.0, self.base_intensity - (age / 3600.0) * decay_rate)
        elif decay_model == AttentionDecay.STEP:
            # Step decay: full intensity for 1 hour, then 50%, then 0
            if age < 3600:
                return self.base_intensity
            elif age < 7200:
                return self.base_intensity * 0.5
            else:
                return 0.0

        return self.base_intensity
```

### Example (Spatial Memory with Pattern Learning)

```python
class SpatialMemoryStore:
    """Persistent spatial memory across sessions"""

    def __init__(self):
        self._patterns: Dict[str, SpatialPattern] = {}
        self._territory_memory: Dict[str, TerritoryMemory] = {}
        self._navigation_history: List[NavigationEvent] = []

    def learn_spatial_pattern(self, category: str, pattern_name: str,
                            pattern_data: Dict[str, Any], confidence: float,
                            applicable_locations: List[str]):
        """Learn navigation and interaction patterns"""
        pattern = SpatialPattern(
            pattern_id=f"spatial_{uuid.uuid4().hex[:8]}",
            category=category,
            pattern_name=pattern_name,
            pattern_data=pattern_data,
            confidence=confidence,
            applicable_locations=applicable_locations,
            learned_at=datetime.now()
        )

        self._patterns[pattern.pattern_id] = pattern

        logger.info(
            "Learned new spatial pattern",
            pattern_id=pattern.pattern_id,
            category=category,
            pattern_name=pattern_name,
            confidence=confidence
        )

    def get_relevant_patterns(self, location: SpatialCoordinates,
                            context: Optional[Dict[str, Any]] = None) -> List[SpatialPattern]:
        """Retrieve patterns relevant to current spatial context"""
        relevant_patterns = []

        for pattern in self._patterns.values():
            if (location.territory_id in pattern.applicable_locations or
                location.room_id in pattern.applicable_locations):

                # Apply context filtering if provided
                if context:
                    pattern_relevance = self._calculate_pattern_relevance(pattern, context)
                    if pattern_relevance > 0.5:
                        relevant_patterns.append(pattern)
                else:
                    relevant_patterns.append(pattern)

        # Sort by confidence and recency
        return sorted(relevant_patterns,
                     key=lambda p: (p.confidence, p.learned_at),
                     reverse=True)

    def update_territory_memory(self, territory_id: str, experience: Dict[str, Any]):
        """Update persistent memory about territory characteristics"""
        if territory_id not in self._territory_memory:
            self._territory_memory[territory_id] = TerritoryMemory(
                territory_id=territory_id,
                experiences=[],
                learned_behaviors={},
                relationship_patterns={}
            )

        self._territory_memory[territory_id].experiences.append({
            **experience,
            'timestamp': datetime.now().isoformat()
        })

        # Limit memory size to prevent unbounded growth
        if len(self._territory_memory[territory_id].experiences) > 1000:
            self._territory_memory[territory_id].experiences = \
                self._territory_memory[territory_id].experiences[-500:]

class WorkspaceNavigator:
    """Navigate across multiple territories with intelligence"""

    def __init__(self, spatial_memory: SpatialMemoryStore, attention_model: AttentionModel):
        self.spatial_memory = spatial_memory
        self.attention_model = attention_model
        self._territories: Dict[str, Territory] = {}
        self._current_territory: Optional[str] = None
        self._navigation_history: List[Dict[str, Any]] = []

    def suggest_next_territory(self, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Suggest territory based on attention priorities"""
        priorities = self.attention_model.get_attention_priorities()

        if priorities:
            top_event, score = priorities[0]
            suggested_territory = top_event.spatial_coordinates.territory_id

            # Consider navigation patterns from spatial memory
            relevant_patterns = self.spatial_memory.get_relevant_patterns(
                top_event.spatial_coordinates, context
            )

            # Apply learned navigation preferences
            for pattern in relevant_patterns:
                if pattern.category == 'navigation' and pattern.confidence > 0.8:
                    pattern_suggestion = pattern.pattern_data.get('preferred_territory')
                    if pattern_suggestion:
                        suggested_territory = pattern_suggestion
                        break

            return suggested_territory

        return None

    def switch_territory(self, territory_id: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """Execute territory switch with state management"""
        if territory_id not in self._territories:
            logger.warning(f"Territory {territory_id} not found in known territories")
            return False

        old_territory = self._current_territory
        self._current_territory = territory_id

        # Record navigation history for pattern learning
        navigation_event = {
            "from_territory": old_territory,
            "to_territory": territory_id,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "navigation_reason": context.get('reason') if context else None
        }

        self._navigation_history.append(navigation_event)

        # Update spatial memory with navigation experience
        self.spatial_memory.update_territory_memory(territory_id, {
            'event_type': 'navigation',
            'navigation_data': navigation_event
        })

        logger.info(
            "Territory switch completed",
            from_territory=old_territory,
            to_territory=territory_id,
            context=context
        )

        return True
```

### Example (Slack Integration Pipeline)

```python
class SlackSpatialMapper:
    """Convert Slack events to spatial objects"""

    def __init__(self, spatial_memory: SpatialMemoryStore):
        self.spatial_memory = spatial_memory
        self.event_classifiers = {
            'help_request': self._classify_help_request,
            'urgent_issue': self._classify_urgent_issue,
            'collaboration': self._classify_collaboration,
            'status_update': self._classify_status_update
        }

    async def map_message_to_spatial_event(self, slack_event: Dict[str, Any],
                                         room: Room,
                                         attention_attractor: Optional[AttentionAttractor] = None) -> SpatialEvent:
        """Map Slack message to spatial event with full context"""

        coordinates = SpatialCoordinates(
            territory_id=slack_event["team"],
            room_id=slack_event["channel"],
            object_id=slack_event["ts"]
        )

        # Determine event type from content analysis
        event_type = self._classify_event_type(slack_event["text"])

        # Extract attention-generating keywords
        keywords = self._extract_attention_keywords(slack_event["text"])

        # Calculate base urgency from multiple factors
        base_urgency = self._calculate_base_urgency(
            slack_event, room, event_type, keywords
        )

        spatial_event = SpatialEvent(
            event_type=event_type,
            coordinates=coordinates,
            content=slack_event["text"],
            timestamp=datetime.fromtimestamp(float(slack_event["ts"])),
            attention_attractor=attention_attractor,
            keywords=keywords,
            urgency_level=base_urgency,
            spatial_context={
                'room_atmosphere': room.get_room_atmosphere(),
                'inhabitant_count': len(room.inhabitants),
                'recent_activity_level': len(room.attention_history[-10:])
            }
        )

        return spatial_event

    def _classify_event_type(self, message_text: str) -> str:
        """Classify message into spatial event type"""
        text_lower = message_text.lower()

        # Apply multiple classification strategies
        for event_type, classifier in self.event_classifiers.items():
            if classifier(text_lower):
                return event_type

        return 'general_message'

    def _calculate_base_urgency(self, slack_event: Dict[str, Any],
                              room: Room, event_type: str, keywords: List[str]) -> float:
        """Calculate base urgency from multiple contextual factors"""
        urgency_factors = []

        # Event type urgency
        event_urgency_map = {
            'help_request': 0.7,
            'urgent_issue': 0.9,
            'collaboration': 0.5,
            'status_update': 0.3,
            'general_message': 0.2
        }
        urgency_factors.append(event_urgency_map.get(event_type, 0.2))

        # Keyword-based urgency
        urgent_keywords = ['urgent', 'emergency', 'asap', 'critical', 'broken', 'down']
        keyword_urgency = sum(0.1 for keyword in keywords if keyword in urgent_keywords)
        urgency_factors.append(min(keyword_urgency, 0.5))

        # Room context urgency
        room_atmosphere = room.get_room_atmosphere()
        urgency_factors.append(room_atmosphere.get('urgency_indicator', 0.0) * 0.3)

        # Time-based urgency (working hours vs off-hours)
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 17:  # Business hours
            urgency_factors.append(0.1)
        else:
            urgency_factors.append(0.05)  # Lower base urgency off-hours

        # Calculate weighted average
        return min(sum(urgency_factors) / len(urgency_factors), 1.0)

class SpatialWorkflowIntegration:
    """Connect spatial events to Piper workflows"""

    def __init__(self, workflow_factory: WorkflowFactory):
        self.workflow_factory = workflow_factory

    async def create_workflow_from_spatial_event(self, spatial_event: SpatialEvent,
                                               attention_event: AttentionEvent) -> Dict[str, Any]:
        """Create Piper workflow with spatial context enrichment"""

        workflow_context = {
            "spatial_trigger": {
                "event_type": spatial_event.event_type,
                "coordinates": spatial_event.coordinates.to_slack_reference(),
                "urgency": attention_event.urgency_level,
                "requires_immediate_response": attention_event.urgency_level > 0.7,
                "spatial_context": spatial_event.spatial_context
            },
            "attention_metadata": {
                "source": attention_event.source.value,
                "intensity": attention_event.base_intensity,
                "current_intensity": attention_event.get_current_intensity(),
                "keywords": attention_event.keywords,
                "decay_model": "exponential"
            },
            "environmental_context": {
                "territory_description": spatial_event.coordinates.territory_id,
                "room_purpose": spatial_event.spatial_context.get('room_purpose'),
                "inhabitant_count": spatial_event.spatial_context.get('inhabitant_count', 0),
                "activity_level": spatial_event.spatial_context.get('recent_activity_level', 0)
            }
        }

        # Create workflow with enriched spatial context
        workflow = await self.workflow_factory.create_workflow(
            workflow_type=self._determine_workflow_type(spatial_event),
            context=workflow_context,
            priority=self._calculate_workflow_priority(attention_event)
        )

        return workflow

    def _determine_workflow_type(self, spatial_event: SpatialEvent) -> str:
        """Determine appropriate workflow type from spatial event"""
        event_to_workflow_map = {
            'help_request': 'support_workflow',
            'urgent_issue': 'incident_response_workflow',
            'collaboration': 'collaboration_workflow',
            'status_update': 'notification_workflow',
            'general_message': 'general_response_workflow'
        }

        return event_to_workflow_map.get(spatial_event.event_type, 'general_response_workflow')
```

## Usage Guidelines

### Spatial Consistency Best Practices

- **Coherent Metaphors**: Maintain consistent spatial metaphors across all interactions and territories
- **Natural Navigation**: Design navigation patterns that match user mental models of physical spaces
- **Environmental Awareness**: Provide AI agents with contextual understanding of their spatial environment
- **Persistent Memory**: Enable cross-session spatial learning and pattern recognition
- **Multi-Territory Support**: Handle complex multi-workspace scenarios with intelligent prioritization

### Attention Management Best Practices

- **Multi-Factor Scoring**: Use proximity, urgency, relationships, and temporal factors for attention prioritization
- **Temporal Decay**: Implement appropriate decay models for different types of attention events
- **Context Awareness**: Consider room atmosphere, inhabitant count, and recent activity levels
- **Dynamic Prioritization**: Continuously update attention priorities based on new events and context changes
- **Performance Requirements**: Maintain <100ms spatial processing for real-time responsiveness

### Integration Best Practices

- **Seamless Workflow Integration**: Connect spatial events naturally to existing workflow systems
- **Rich Context Propagation**: Ensure spatial context is preserved throughout workflow execution
- **Pattern Learning**: Enable automatic behavior adaptation from interaction history
- **Scalable Architecture**: Design for multiple workspaces with persistent memory across sessions
- **Event Classification**: Implement robust classification of events into appropriate spatial categories

### Anti-Patterns to Avoid

- **Abstract Event Processing**: Treating events as abstract data without spatial context
- **Ignoring Temporal Decay**: Not implementing attention decay and emotional dimensions
- **Memory Amnesia**: Not maintaining persistent spatial memory across sessions
- **Complex Metaphors**: Using spatial metaphors that don't match user mental models
- **Single-Workspace Assumptions**: Designing for single workspace in multi-territory environments
- **Performance Neglect**: Allowing spatial processing to impact real-time responsiveness

## Benefits

- **Embodied AI Experience**: Creates natural spatial navigation and environmental awareness for AI agents
- **Intelligent Attention Management**: Provides context-aware prioritization with sophisticated decay algorithms
- **Pattern Learning Capabilities**: Enables automatic behavior adaptation from interaction history and spatial patterns
- **Scalable Multi-Workspace Architecture**: Supports multiple workspaces with persistent memory and intelligent navigation
- **Seamless Workflow Integration**: Connects spatial events naturally to existing workflow and orchestration systems
- **Enhanced User Experience**: Provides more intuitive and contextual AI interactions through spatial metaphors

## Trade-offs

- **Implementation Complexity**: Requires sophisticated spatial modeling and attention management systems
- **Memory and Performance Overhead**: Persistent spatial memory and real-time processing require significant resources
- **Learning Curve**: Users and developers need to understand spatial metaphor concepts and navigation patterns
- **Debugging Complexity**: Spatial interactions and attention models can be difficult to debug and troubleshoot
- **Maintenance Requirements**: Spatial patterns and attention models require ongoing tuning and optimization
- **Integration Challenges**: Requires careful integration with existing systems to maintain spatial context consistency

## Related Patterns

- [Pattern-016: Repository Context Enrichment](pattern-016-repository-context-enrichment.md) - Context enrichment for spatial events
- [Pattern-017: Background Task Error Handling](pattern-017-background-task-error-handling.md) - Error handling for spatial processing
- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Async processing of spatial events
- [Pattern-002: Service Pattern](pattern-002-service.md) - Service architecture for spatial systems

## Migration Notes (for consolidation from legacy systems)

- **From `pattern-catalog.md`**: Section 20 "Spatial Metaphor Integration Pattern (PM-074)" - comprehensive implementation with advanced components
- **From `PATTERN-INDEX.md`**: No direct equivalent - this is a novel AI interaction pattern
- **From PM-074**: Core spatial intelligence requirements and TDD integration testing approach
- **Consolidation Strategy**: Expanded pattern-catalog.md content with comprehensive workflow integration, attention management, and pattern learning frameworks

## Quality Assurance Checklist

- [x] Pattern description is clear and concise
- [x] Context explains problem and applicability
- [x] Implementation examples are provided and correct
- [x] Usage guidelines are comprehensive
- [x] Related patterns are linked
- [x] All information from source catalog is preserved
- [x] Follows ADR-style numbering and naming conventions

## Agent Coordination Notes

- **Agent A (Code)**: Responsible for spatial processing infrastructure and attention model implementation
- **Agent B (Cursor)**: Responsible for spatial metaphor documentation and integration pattern validation
- **Integration Points**: Spatial processing engines, attention models, workflow integration systems, and memory stores

## References

- Original catalog: `docs/architecture/pattern-catalog.md#20-spatial-metaphor-integration-pattern-pm-074`
- PM-074: Spatial Intelligence implementation requirements
- Spatial processing: `services/spatial/`
- Attention models: `services/attention/`
- Slack integration: `services/integrations/slack/spatial_adapter.py`

_Last updated: September 15, 2025_
