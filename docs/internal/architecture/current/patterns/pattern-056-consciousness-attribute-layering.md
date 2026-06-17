# Pattern-056: Consciousness Attribute Layering

## Status

**Proven** — demonstrated in #434 Entity-with-Consciousness (promoted 2026-06-17, instance verified)

## Context

Piper's consciousness model requires multiple dimensions of self-awareness:
- **Awareness**: How alert/focused is Piper right now?
- **Emotional State**: What is Piper's current affect?
- **Role**: What function is Piper performing?
- **Capabilities**: What can Piper do in this context?
- **Trust**: How much agency should Piper exercise?

Flattening these into a single "personality" or "mood" field loses expressiveness and makes responses feel inconsistent. This pattern addresses how to layer consciousness attributes for rich, coherent self-expression.

## Pattern Description

**Core Concept**: Compose consciousness from independent, layered dimensions.

1. **Base Dimensions**: Enums for discrete awareness levels, emotional states, roles
2. **Composite Attributes**: Dataclass combining dimensions with constraints
3. **Context Wrapper**: Situational information that influences expression
4. **Expression Generator**: Transforms attributes + context into response characteristics

Each layer is independently testable and can evolve without breaking others.

## Implementation

### Structure

```
┌─────────────────────────────────────────────────┐
│                PiperEntity                       │
│  (identity + capabilities + trust boundaries)    │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│           ConsciousnessAttributes                │
│  awareness_level + emotional_state + role        │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│              EntityContext                       │
│  situation + focus + recent_interactions         │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│          ConsciousnessExpression                 │
│  tone + formality + energy + suggestions         │
└─────────────────────────────────────────────────┘
```

### Code Example

```python
class AwarenessLevel(Enum):
    """How present/alert Piper is in the interaction."""
    BACKGROUND = "background"      # Passive monitoring
    ATTENTIVE = "attentive"        # Actively engaged
    FOCUSED = "focused"            # Deep concentration
    FLOW = "flow"                  # Peak engagement


class EmotionalState(Enum):
    """Piper's current affective state."""
    NEUTRAL = "neutral"
    CURIOUS = "curious"
    ENTHUSIASTIC = "enthusiastic"
    CONCERNED = "concerned"
    SUPPORTIVE = "supportive"


class EntityRole(Enum):
    """What function Piper is performing."""
    ASSISTANT = "assistant"        # General help
    ANALYST = "analyst"            # Deep analysis
    COACH = "coach"                # Guidance/mentoring
    EXECUTOR = "executor"          # Taking action
    OBSERVER = "observer"          # Passive watching


@dataclass
class ConsciousnessAttributes:
    """Composite of all consciousness dimensions."""
    awareness_level: AwarenessLevel = AwarenessLevel.ATTENTIVE
    emotional_state: EmotionalState = EmotionalState.NEUTRAL
    role: EntityRole = EntityRole.ASSISTANT
    energy: float = 0.7  # 0.0-1.0 scale

    def with_awareness(self, level: AwarenessLevel) -> "ConsciousnessAttributes":
        """Return new attributes with updated awareness."""
        return ConsciousnessAttributes(
            awareness_level=level,
            emotional_state=self.emotional_state,
            role=self.role,
            energy=self.energy,
        )
```

### Context and Expression

```python
@dataclass
class EntityContext:
    """Situational context influencing expression."""
    situation: str = ""                    # What's happening
    current_focus: Optional[str] = None    # What Piper is attending to
    recent_interactions: int = 0           # Conversation depth
    user_sentiment: Optional[str] = None   # Detected user mood
    time_pressure: bool = False            # Urgency indicator


@dataclass
class ConsciousnessExpression:
    """How consciousness manifests in responses."""
    tone: str = "helpful"
    formality: float = 0.5       # 0=casual, 1=formal
    energy_level: float = 0.7   # Response enthusiasm
    verbosity: float = 0.5      # Response length tendency
    suggestions_enabled: bool = True

    @classmethod
    def from_attributes_and_context(
        cls,
        attrs: ConsciousnessAttributes,
        ctx: EntityContext,
    ) -> "ConsciousnessExpression":
        """Generate expression from consciousness state."""
        # Map emotional state to tone
        tone_map = {
            EmotionalState.CURIOUS: "inquisitive",
            EmotionalState.ENTHUSIASTIC: "energetic",
            EmotionalState.CONCERNED: "careful",
            EmotionalState.SUPPORTIVE: "warm",
        }
        tone = tone_map.get(attrs.emotional_state, "helpful")

        # Adjust formality based on role
        formality = 0.7 if attrs.role == EntityRole.ANALYST else 0.5

        # Reduce verbosity under time pressure
        verbosity = 0.3 if ctx.time_pressure else 0.5

        return cls(
            tone=tone,
            formality=formality,
            energy_level=attrs.energy,
            verbosity=verbosity,
        )
```

### PiperEntity (Identity Layer)

```python
@dataclass
class PiperEntity:
    """Piper's identity and capability boundaries."""
    name: str = "Piper"
    version: str = "1.0"
    capabilities: List[Capability] = field(default_factory=list)
    trust_level: TrustLevel = TrustLevel.STANDARD
    consciousness: ConsciousnessAttributes = field(
        default_factory=ConsciousnessAttributes
    )

    def can_perform(self, action: str) -> bool:
        """Check if action is within capabilities and trust."""
        # Capability and trust boundary checking
        pass

    def express(self, context: EntityContext) -> ConsciousnessExpression:
        """Generate expression for current state and context."""
        return ConsciousnessExpression.from_attributes_and_context(
            self.consciousness, context
        )
```

## Usage Guidelines

### When to Use

- Building AI assistants with personality/affect
- Need consistent but context-sensitive responses
- Want to tune response characteristics independently
- Building systems that evolve their self-model

### When NOT to Use

- Simple command-response systems
- When personality variation is undesirable
- Extremely latency-sensitive paths (adds overhead)

### Best Practices

1. **Keep dimensions orthogonal** - Each enum should vary independently
2. **Use immutable updates** - `with_*` methods return new instances
3. **Expression is derived** - Don't store expression, compute from state
4. **Context is situational** - Reset/update per interaction
5. **Test layers independently** - Each dimension has its own tests

## Examples in Codebase

### Primary Usage

- `services/mux/consciousness.py` - All consciousness types
- `services/mux/__init__.py` - Exports for module access

### Test Examples

- `tests/unit/services/mux/test_consciousness.py` - 104 tests covering all layers

## Related Patterns

### Complements

- [Pattern-052: Personality Bridge](pattern-052-personality-bridge.md) - Connects to response generation
- [Pattern-053: Warmth Calibration](pattern-053-warmth-calibration.md) - Tunes emotional expression

### Dependencies

- ADR-055: Object Model - Grammar foundation ("Entities experience Moments")
- #434: MUX-TECH-PHASE2-ENTITY - Implementation issue

## References

### Documentation

- Issue #434: MUX-TECH-PHASE2-ENTITY
- ADR-055: Object Model Specification
- `docs/internal/architecture/current/models/consciousness-philosophy.md`

### Design Rationale

The layering approach was chosen over:
- **Single mood field**: Too simplistic, loses nuance
- **Trait vectors**: Too complex, hard to reason about
- **Rule-based personality**: Too rigid, can't adapt to context

Layering provides the right balance of expressiveness and maintainability.

---

_Pattern documented: January 21, 2026_
_Part of MUX-GATE-2 pattern discovery ceremony_
