# Pattern-058: Ownership Graph Navigation

## Status

**Proven** — demonstrated in #435 Ownership-Model (promoted 2026-06-17, instance verified)

## Context

AI assistants observe data from many sources: GitHub issues, Slack messages, calendar events, internal state. Without a clear model of how the assistant relates to each piece of information, several problems emerge:

- **Epistemological confusion**: Is this a fact Piper knows, or an inference Piper made?
- **Trust miscalibration**: Treating uncertain inferences as certain facts
- **Stale data blindness**: Not knowing when external data might be outdated
- **Modification confusion**: Can Piper change this, or is it read-only external data?

This pattern introduces a three-category ownership model that tracks Piper's relationship to knowledge: what Piper creates (Mind), observes (Senses), and understands (Understanding).

## Pattern Description

**Core Concept**: Track Piper's epistemological relationship to every object.

1. **NATIVE (Piper's Mind)**: Objects Piper creates and owns directly
   - Sessions, memories, trust states, learning
   - Full confidence, fully modifiable
   - "I know this because I created it"

2. **FEDERATED (Piper's Senses)**: Objects Piper observes from external sources
   - GitHub issues, Slack messages, calendar events
   - May be stale, cannot modify
   - "I see this in [Place]"

3. **SYNTHETIC (Piper's Understanding)**: Objects Piper constructs through reasoning
   - Inferred status, assembled risk, pattern recognition
   - Uncertain, requires verification
   - "I understand this to mean..."

The model also tracks valid transformations between categories as Piper's relationship to knowledge evolves.

## Implementation

### Structure

```
┌─────────────────────────────────────────────────┐
│           OwnershipCategory (Enum)              │
│  NATIVE | FEDERATED | SYNTHETIC                 │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│             OwnershipResolver                   │
│  Determines category from source/attributes     │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│            OwnershipMetadata                    │
│  Embeds in domain models to track relationship  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│          OwnershipTransformation                │
│  Tracks valid category transitions              │
└─────────────────────────────────────────────────┘
```

### Code Example

```python
class OwnershipCategory(Enum):
    """
    Describes Piper's epistemological relationship to knowledge.

    The three categories represent how Piper knows things:
    - NATIVE: "I know this because I created it" (Mind)
    - FEDERATED: "I see this in [Place]" (Senses)
    - SYNTHETIC: "I understand this to mean..." (Understanding)
    """

    NATIVE = "native"
    FEDERATED = "federated"
    SYNTHETIC = "synthetic"

    @property
    def metaphor(self) -> str:
        """Consciousness metaphor for this category."""
        metaphors = {
            OwnershipCategory.NATIVE: "Piper's Mind",
            OwnershipCategory.FEDERATED: "Piper's Senses",
            OwnershipCategory.SYNTHETIC: "Piper's Understanding",
        }
        return metaphors[self]

    @property
    def experience_phrase(self) -> str:
        """How Piper expresses knowledge from this category."""
        phrases = {
            OwnershipCategory.NATIVE: "I know this because I created it",
            OwnershipCategory.FEDERATED: "I see this in {place}",
            OwnershipCategory.SYNTHETIC: "I understand this to mean...",
        }
        return phrases[self]
```

### Ownership Resolution

```python
class OwnershipResolver:
    """
    Resolves ownership categories based on source and attributes.
    """

    NATIVE_SOURCES = frozenset({"piper", "system", "internal", "memory"})
    FEDERATED_SOURCES = frozenset({
        "github", "slack", "notion", "calendar", "jira", "linear", "email"
    })
    SYNTHETIC_SOURCES = frozenset({
        "inference", "analysis", "synthesis", "aggregation", "computation"
    })

    def determine(
        self,
        source: str,
        created_by: Optional[str] = None,
        is_derived: bool = False,
    ) -> OwnershipCategory:
        """Determine ownership category from source and attributes."""
        # Derived objects are always SYNTHETIC
        if is_derived:
            return OwnershipCategory.SYNTHETIC

        source_lower = source.lower()

        if source_lower in self.NATIVE_SOURCES:
            return OwnershipCategory.NATIVE

        if created_by and created_by.lower() in self.NATIVE_SOURCES:
            return OwnershipCategory.NATIVE

        if source_lower in self.FEDERATED_SOURCES:
            return OwnershipCategory.FEDERATED

        if source_lower in self.SYNTHETIC_SOURCES:
            return OwnershipCategory.SYNTHETIC

        # Default to FEDERATED for unknown external sources
        return OwnershipCategory.FEDERATED
```

### Ownership Metadata (Embeddable)

```python
@dataclass
class OwnershipMetadata:
    """
    Metadata tracking Piper's relationship to an object.

    Embed in domain models to track ownership throughout the system.
    """

    category: OwnershipCategory
    source: str
    confidence: float = 1.0
    requires_verification: bool = False
    can_modify: bool = True
    derived_from: List[str] = field(default_factory=list)

    @classmethod
    def native(cls, source: str = "piper") -> "OwnershipMetadata":
        """Factory for NATIVE objects (Piper's Mind)."""
        return cls(
            category=OwnershipCategory.NATIVE,
            source=source,
            confidence=1.0,
            requires_verification=False,
            can_modify=True,
        )

    @classmethod
    def federated(cls, source: str) -> "OwnershipMetadata":
        """Factory for FEDERATED objects (Piper's Senses)."""
        return cls(
            category=OwnershipCategory.FEDERATED,
            source=source,
            confidence=0.9,  # May be stale
            requires_verification=True,
            can_modify=False,  # External truth
        )

    @classmethod
    def synthetic(
        cls, source: str, derived_from: List[str]
    ) -> "OwnershipMetadata":
        """Factory for SYNTHETIC objects (Piper's Understanding)."""
        return cls(
            category=OwnershipCategory.SYNTHETIC,
            source=source,
            confidence=0.7,  # Inference has uncertainty
            requires_verification=True,
            can_modify=True,
            derived_from=derived_from,
        )
```

### Valid Transformations

```python
# Valid transformation paths
VALID_TRANSFORMATIONS = frozenset({
    # FEDERATED -> SYNTHETIC: Observation becomes understanding
    (OwnershipCategory.FEDERATED, OwnershipCategory.SYNTHETIC),

    # SYNTHETIC -> NATIVE: Understanding becomes memory (user confirms)
    (OwnershipCategory.SYNTHETIC, OwnershipCategory.NATIVE),

    # FEDERATED -> NATIVE: Observation becomes memory (rare, direct capture)
    (OwnershipCategory.FEDERATED, OwnershipCategory.NATIVE),
})

# Invalid transformations:
# - NATIVE -> FEDERATED: Can't "un-create" something
# - NATIVE -> SYNTHETIC: Can't make certain knowledge uncertain
# - SYNTHETIC -> FEDERATED: Can't turn inference into observation
```

### Domain Model Integration

```python
@dataclass
class Session:
    """User session - NATIVE to Piper."""
    id: str
    user_id: str
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata.native("piper-core")
    )


@dataclass
class GitHubIssue:
    """GitHub issue - FEDERATED from GitHub."""
    id: str
    title: str
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata.federated("github")
    )


@dataclass
class InferredRisk:
    """Risk assessment - SYNTHETIC from analysis."""
    id: str
    level: str
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata.synthetic(
            source="risk-analysis",
            derived_from=["github-issues", "calendar-events"]
        )
    )
```

## Usage Guidelines

### When to Use

- Building AI assistants that aggregate data from multiple sources
- Need to track confidence and staleness of information
- Want explicit control over what the AI can vs. cannot modify
- Building systems that explain their reasoning provenance

### When NOT to Use

- Single-source systems with no external data
- When all data has equal confidence and freshness
- Performance-critical paths where metadata overhead matters

### Best Practices

1. **Assign ownership at creation** - Every object should have ownership from the start
2. **Use factory methods** - `native()`, `federated()`, `synthetic()` ensure correct defaults
3. **Track derivation chains** - Synthetic objects should know what they derived from
4. **Validate transformations** - Only allow valid category transitions
5. **Express ownership in responses** - "I see in GitHub..." vs "I remember..." vs "I infer..."

## Examples in Codebase

### Primary Usage

- `services/mux/ownership.py` - Full ownership model implementation
- `services/mux/__init__.py` - Exports for module access

### Test Examples

- `tests/unit/services/mux/test_ownership.py` - 61 tests covering all ownership scenarios

## Related Patterns

### Complements

- [Pattern-056: Consciousness Attribute Layering](pattern-056-consciousness-attribute-layering.md) - Entity awareness model
- [Pattern-057: Grammar-Driven Classification](pattern-057-grammar-driven-classification.md) - Intent categorization

### Dependencies

- ADR-055: Object Model Specification - Ownership as core concept
- #435: MUX-TECH-PHASE3-OWNERSHIP - Implementation issue

## References

### Documentation

- Issue #435: MUX-TECH-PHASE3-OWNERSHIP
- ADR-055: Object Model Specification
- `docs/internal/architecture/current/models/object-model-specification.md`

### Design Rationale

The three-category model was chosen over:
- **Binary (internal/external)**: Loses the distinction between observation and inference
- **Flat source tracking**: Doesn't capture epistemological relationship
- **Confidence-only**: Doesn't express why confidence varies

The Mind/Senses/Understanding metaphor provides both technical precision and intuitive explanation for how Piper relates to different types of knowledge.

---

_Pattern documented: January 21, 2026_
_Part of MUX-GATE-2 pattern discovery ceremony_
