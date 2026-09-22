# DDD Model: ResponsePersonalityEnhancer

## Bounded Context Definition

### Personality Enhancement Context
**Purpose**: Transform functional responses into warm, confident, actionable communication across all Piper interfaces

**Core Responsibility**: Cross-cutting concern that enhances responses with consistent personality while preserving technical accuracy

**Boundaries**:
- **Owns**: Personality profiles, tone transformation, confidence display, actionability enhancement
- **Uses**: Intent confidence scores, user preferences, response templates
- **Does NOT Own**: Intent classification, template content, response routing

## Domain Model

### Core Entities

```python
@dataclass
class PersonalityProfile:
    """User's preferred personality configuration"""
    id: str
    user_id: str
    warmth_level: float  # 0.0 (professional) to 1.0 (friendly)
    confidence_style: ConfidenceDisplayStyle  # NUMERIC, DESCRIPTIVE, CONTEXTUAL, HIDDEN
    action_orientation: ActionLevel  # HIGH, MEDIUM, LOW
    technical_depth: TechnicalPreference  # DETAILED, BALANCED, SIMPLIFIED
    created_at: datetime
    updated_at: datetime

    def adjust_for_context(self, context: ResponseContext) -> 'PersonalityProfile':
        """Create context-adjusted profile without mutating original"""
        pass

@dataclass
class ResponseContext:
    """Context for response enhancement"""
    intent_confidence: float  # From Intent (0.0-1.0)
    intent_category: IntentCategory
    intent_action: str
    response_type: ResponseType  # STANDUP, CHAT, CLI, WEB, ERROR
    user_stress_indicators: List[str]  # deadline pressure, error recovery, etc.
    conversation_history: Optional[List[Message]]

@dataclass
class EnhancedResponse:
    """Response after personality enhancement"""
    original_content: str
    enhanced_content: str
    personality_profile_used: PersonalityProfile
    confidence_displayed: Optional[float]
    enhancements_applied: List[Enhancement]
    processing_time_ms: float
```

### Value Objects

```python
class ConfidenceDisplayStyle(Enum):
    NUMERIC = "numeric"  # "87% confident"
    DESCRIPTIVE = "descriptive"  # "high confidence"
    CONTEXTUAL = "contextual"  # "Based on recent patterns..."
    HIDDEN = "hidden"  # No confidence shown

class ActionLevel(Enum):
    HIGH = "high"  # Every response has explicit next steps
    MEDIUM = "medium"  # Actionable when relevant
    LOW = "low"  # Minimal action orientation

class ResponseType(Enum):
    STANDUP = "standup"
    CHAT = "chat"
    CLI = "cli"
    WEB = "web"
    ERROR = "error"

class Enhancement(Enum):
    WARMTH_ADDED = "warmth_added"
    CONFIDENCE_INJECTED = "confidence_injected"
    ACTION_EXTRACTED = "action_extracted"
    CONTEXT_ADAPTED = "context_adapted"
    ERROR_SOFTENED = "error_softened"
```

## Aggregate Design

### ResponsePersonalityEnhancer (Aggregate Root)

```python
class ResponsePersonalityEnhancer:
    """Aggregate root for personality enhancement"""

    def __init__(self,
                 profile_repository: PersonalityProfileRepository,
                 transformation_rules: TransformationRuleSet):
        self.profile_repository = profile_repository
        self.transformation_rules = transformation_rules
        self.metrics_collector = MetricsCollector()

    async def enhance_response(self,
                              content: str,
                              context: ResponseContext,
                              user_id: str) -> EnhancedResponse:
        """Core domain operation"""
        # 1. Load or create personality profile
        profile = await self._get_profile(user_id)

        # 2. Adjust profile for context
        adjusted_profile = profile.adjust_for_context(context)

        # 3. Apply transformations
        enhanced = await self._apply_transformations(
            content, adjusted_profile, context
        )

        # 4. Record metrics
        self.metrics_collector.record(enhanced)

        return enhanced

    def _apply_transformations(self, content, profile, context):
        """Apply personality transformations in order"""
        # Order matters: warmth → confidence → actions
        pass
```

## Domain Services

### TransformationService
```python
class TransformationService:
    """Domain service for content transformation"""

    def add_warmth(self, content: str, warmth_level: float) -> str:
        """Add appropriate warmth without losing professionalism"""
        pass

    def inject_confidence(self,
                         content: str,
                         confidence: float,
                         style: ConfidenceDisplayStyle) -> str:
        """Add confidence indicators based on intent confidence"""
        pass

    def extract_actions(self, content: str, action_level: ActionLevel) -> str:
        """Make response actionable with clear next steps"""
        pass
```

### BridgingService
```python
class StandupToChatBridge:
    """Service to unify standup and chat experiences"""

    def adapt_standup_for_chat(self, standup_response: str) -> str:
        """Transform standup HTML/markdown for conversational UI"""
        pass

    def apply_personality_to_standup(self,
                                    standup_data: dict,
                                    profile: PersonalityProfile) -> str:
        """Apply personality to standup-specific formatting"""
        pass
```

## Repository Interfaces

```python
class PersonalityProfileRepository:
    """Repository for personality profiles"""

    async def get_by_user_id(self, user_id: str) -> Optional[PersonalityProfile]:
        pass

    async def save(self, profile: PersonalityProfile) -> None:
        pass

    async def get_default(self) -> PersonalityProfile:
        """Return default Piper personality"""
        pass
```

## Integration Points

### Inbound Adapters
1. **From Intent Service**: Receive confidence scores and intent classification
2. **From Templates**: Intercept template output for enhancement
3. **From Standup**: Bridge standup formatting to personality system
4. **From User Config**: Load personality preferences

### Outbound Adapters
1. **To ActionHumanizer**: Pass enhanced content for final processing
2. **To Chat UI**: Provide personality-enhanced responses
3. **To Metrics**: Record enhancement performance and user engagement

## Anti-Corruption Layer

### Template Compatibility
```python
class TemplateCompatibilityLayer:
    """Ensure personality enhancement doesn't break existing templates"""

    def validate_enhanced_response(self,
                                  original: str,
                                  enhanced: str) -> bool:
        """Ensure critical information preserved"""
        # Check: issue numbers, URLs, data values maintained
        # Check: markdown/HTML structure intact
        # Check: action buttons/links functional
        pass
```

## Domain Events

```python
class PersonalityEnhancementCompleted:
    """Event when response enhanced"""
    response_id: str
    user_id: str
    enhancements_applied: List[Enhancement]
    processing_time_ms: float
    confidence_level: float

class PersonalityProfileUpdated:
    """Event when user updates preferences"""
    user_id: str
    changes: Dict[str, Any]

class LowConfidenceResponseDetected:
    """Event for responses below confidence threshold"""
    response_id: str
    confidence: float
    context: ResponseContext
```

## Ubiquitous Language

- **Warmth**: Professional friendliness without casualness
- **Confidence Indicator**: Transparent display of certainty level
- **Actionable**: Contains clear, specific next steps
- **Context-Sensitive**: Adapts personality to situation
- **Enhancement**: Transformation applied to response
- **Bridge**: Connection between standup and chat experiences
- **Profile**: User's personality preferences
- **Baseline**: Default Piper personality

## Implementation Strategy

### Phase 1: Core Enhancement (Current Focus)
1. Build ResponsePersonalityEnhancer aggregate
2. Implement basic transformations (warmth, confidence, actions)
3. Integrate with existing templates
4. Add to response pipeline

### Phase 2: Standup Bridge
1. Create StandupToChatBridge service
2. Apply personality to standup responses
3. Unify formatting for chat UI

### Phase 3: Advanced Features
1. A/B testing framework
2. Personality learning from feedback
3. Context-sensitive adaptation
4. Multi-language support

## Testing Strategy

### Unit Tests
- Transformation rules (warmth levels, confidence styles)
- Profile adjustments for context
- Enhancement preservation of data

### Integration Tests
- Pipeline integration (Intent → Templates → Personality → Output)
- Standup bridge functionality
- User preference loading

### Acceptance Tests
- "Response feels warm but professional"
- "Confidence is clearly communicated"
- "Every response has actionable next steps"
- "Standup and chat feel consistent"

## Documentation Requirements

### New Documentation to Create

#### 1. Domain Service Documentation
**File**: `docs/architecture/domain-services.md` (UPDATE)
```markdown
## ResponsePersonalityEnhancer Domain Service

**File**: `services/personality/response_enhancer.py`
**Purpose**: Transform functional responses into warm, confident, actionable communication
**Domain**: Response Enhancement / User Experience

### Business Rules Enforced
1. **Warmth Levels**: 0.0-1.0 scale maintaining professionalism
2. **Confidence Display**: Contextual based on Intent confidence (0.0-1.0)
3. **Action Extraction**: Every response includes clear next steps
4. **Context Adaptation**: Personality adjusts for stress/error situations

### Usage
[Code examples]

### Integration Points
- **Intent Service**: Receives confidence scores
- **Template Layer**: Intercepts template output
- **ActionHumanizer**: Passes enhanced content
- **Standup Service**: Bridges standup formatting

### Monitoring
[Metrics and logging patterns]
```

#### 2. New Pattern Documentation
**File**: `docs/architecture/pattern-catalog.md` (UPDATE)
Add new section:
```markdown
## Personality Enhancement Pattern

### Purpose
Provide consistent warm, confident, actionable responses across all interfaces

### Implementation
[ResponsePersonalityEnhancer aggregate pattern]

### Usage Guidelines
- Apply to all user-facing responses
- Respect user personality preferences
- Maintain data integrity during enhancement
- Bridge standup and chat experiences

### Anti-patterns to Avoid
- ❌ Over-casualization losing professionalism
- ❌ Hiding low confidence with false certainty
- ❌ Breaking template structure with enhancements
- ❌ Different personalities per interface
```

#### 3. API Documentation
**File**: `docs/api/personality-enhancement-api.md` (NEW)
```markdown
# Personality Enhancement API

## Endpoints

All endpoints require authentication; the profile is resolved from the authenticated
session (no user-id path segment).

### GET /api/v1/personality/profile
Retrieve the authenticated user's personality preferences

### PUT /api/v1/personality/profile
Update personality preferences (admin-only)

### POST /api/v1/personality/enhance
Enhance a response with personality (body: `{"content": "..."}`)

## Configuration
[User preference options and defaults]

## Examples
[Before/after enhancement examples]
```

#### 4. Integration Guide
**File**: `docs/development/UX-105-personality-integration-guide.md` (NEW)
```markdown
# UX-105 Personality Enhancement Integration Guide

## Quick Start
[How to use ResponsePersonalityEnhancer]

## Integration Points
1. CLI commands enhancement
2. Web API responses
3. Slack message formatting
4. Standup report bridging

## Testing
[How to test personality enhancements]

## Configuration
[How to configure personality profiles]
```

### Documentation to Update

#### 1. Architecture Overview
**File**: `docs/architecture/architecture.md`
Add section:
```markdown
### Response Enhancement Layer
- ResponsePersonalityEnhancer service
- Personality profiles and preferences
- Confidence-based adaptation
- Cross-interface consistency
```

#### 2. Domain Models Index
**File**: `docs/architecture/domain-models-index.md`
Add:
```markdown
## Personality Enhancement Models
- PersonalityProfile
- ResponseContext
- EnhancedResponse
- Enhancement (enum)
```

#### 3. Dependency Diagrams
**File**: `docs/architecture/dependency-diagrams.md`
Update diagram to show:
- ResponsePersonalityEnhancer dependencies
- Integration with Intent Service
- Connection to UI Messages layer
- Standup bridge relationship

#### 4. Test Strategy
**File**: `docs/architecture/test-strategy.md`
Add:
```markdown
## Personality Enhancement Testing
- Warmth level validation
- Confidence display accuracy
- Action extraction verification
- Context adaptation scenarios
- Performance (<100ms) tests
```

#### 5. User Guide
**File**: `docs/user-guide.md`
Add section:
```markdown
## Personality Customization
How to configure Piper's response personality:
- Warmth level (professional to friendly)
- Confidence display style
- Action orientation
- Technical depth preferences
```

#### 6. Development Guidelines
**File**: `docs/development/dev-guidelines.md`
Add:
```markdown
## Response Enhancement Guidelines
- All user-facing responses must go through PersonalityEnhancer
- Maintain consistency across CLI/Web/Slack
- Preserve data integrity during enhancement
- Test personality with A/B framework
```

#### 7. Morning Standup Guide
**File**: `docs/development/MORNING_STANDUP_MVP_GUIDE.md`
Add:
```markdown
## Personality Integration
Standup responses now enhanced with:
- Warm, encouraging tone
- Confidence indicators for metrics
- Actionable daily recommendations
- Consistent with chat personality
```

### Migration Documentation

#### ADR (Architecture Decision Record)
**File**: `docs/architecture/adr/adr-xxx-personality-enhancement.md` (NEW)
```markdown
# ADR-XXX: Response Personality Enhancement

## Status
Accepted

## Context
Piper's responses are functional but lack warmth and personality

## Decision
Implement ResponsePersonalityEnhancer as cross-cutting concern

## Consequences
- Consistent personality across all interfaces
- Additional processing overhead (<100ms)
- User preference configuration required
- Standup formatting must be bridged
```

### Testing Documentation

#### Test Patterns
**File**: `docs/testing/personality-test-patterns.md` (NEW)
```markdown
# Personality Enhancement Test Patterns

## Unit Tests
- Transformation accuracy
- Profile adjustments
- Enhancement preservation

## Integration Tests
- Pipeline integration
- Standup bridge
- Preference loading

## Acceptance Tests
- Warmth perception
- Confidence clarity
- Action identification
```

### Monitoring Documentation

#### Metrics Guide
**File**: `docs/operations/personality-metrics.md` (NEW)
```markdown
# Personality Enhancement Metrics

## Performance Metrics
- Enhancement latency (target <100ms)
- Cache hit rate for profiles
- Transformation success rate

## Engagement Metrics
- User response follow-through
- Conversation continuation rate
- Satisfaction indicators
```

## Documentation Impact Summary

### Critical Updates (Block deployment if missing)
1. `domain-services.md` - Add ResponsePersonalityEnhancer
2. `pattern-catalog.md` - Add Personality Enhancement Pattern
3. `architecture.md` - Update with enhancement layer
4. `UX-105-personality-integration-guide.md` - Create integration guide

### Important Updates (Should complete soon after)
5. `test-strategy.md` - Add personality testing section
6. `user-guide.md` - Add customization section
7. `dependency-diagrams.md` - Update relationships

### Nice to Have (Can be gradual)
8. ADR for decision record
9. Test patterns guide
10. Metrics monitoring guide

This documentation strategy ensures agents know exactly what to update and create!
