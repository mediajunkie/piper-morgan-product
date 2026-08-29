# Pattern-057: Grammar-Driven Classification

## Status

**Proven** — demonstrated in #433 Core-Object-Model-Grammar (promoted 2026-06-17, instance verified)

## Context

Intent classification often devolves into arbitrary action categories or loose taxonomies that don't reflect the underlying nature of what users are requesting. This leads to:
- Inconsistent routing decisions
- Overlapping categories with unclear boundaries
- Difficulty extending the system coherently
- Loss of semantic meaning in classification

The MUX Object Model (ADR-055) introduces a formal grammar: "Entities experience Moments at Places." This pattern applies grammatical thinking to intent classification, where each intent category maps to a distinct grammatical role or verb type.

## Pattern Description

**Core Concept**: Ground intent categories in grammatical semantics rather than arbitrary taxonomy.

1. **Verb-Based Categories**: Each IntentCategory maps to a type of verb (action, perception, cognition)
2. **Grammar Mapping**: Categories align with grammatical roles (Actor doing, Observer perceiving, etc.)
3. **Semantic Boundaries**: Category boundaries are defined by grammatical rules, not convenience
4. **Extensibility**: New categories must justify their grammatical role

The key insight: "What should I do?" (GUIDANCE) is grammatically different from "What am I doing?" (STATUS) - one asks for direction, the other observes current state.

## Implementation

### Structure

```
User Message
    ↓
┌─────────────────────────────────────┐
│     Grammatical Analysis            │
│  "What verb type is the user        │
│   expressing?"                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│     IntentCategory (Enum)           │
│  - Action verbs → EXECUTION         │
│  - Perception verbs → QUERY         │
│  - Cognition verbs → ANALYSIS       │
│  - Planning verbs → PLANNING        │
│  - Social verbs → CONVERSATION      │
└─────────────────────────────────────┘
    ↓
Handler Selection (grammar-aware)
```

### Code Example

```python
class IntentCategory(Enum):
    """
    Intent categories grounded in grammatical verb types.

    Each category represents a distinct type of user intention
    mapped to grammatical semantics from the MUX grammar.
    """

    # Action Verbs - User wants something DONE
    EXECUTION = "execution"      # "Create X", "Update Y", "Delete Z"

    # Perception Verbs - User wants to SEE/KNOW
    QUERY = "query"              # "Show me X", "What is Y?"
    STATUS = "status"            # "What am I working on?"
    IDENTITY = "identity"        # "Who are you?"
    TEMPORAL = "temporal"        # "What day is it?"

    # Cognition Verbs - User wants UNDERSTANDING
    ANALYSIS = "analysis"        # "Analyze X", "Why is Y?"
    SYNTHESIS = "synthesis"      # "Summarize X", "Combine Y and Z"
    LEARNING = "learning"        # "Teach me X", "How does Y work?"

    # Planning Verbs - User wants DIRECTION
    PLANNING = "planning"        # "Plan X", "Design Y"
    STRATEGY = "strategy"        # "What's the approach for X?"
    GUIDANCE = "guidance"        # "What should I focus on?"
    PRIORITY = "priority"        # "What's most important?"

    # Social Verbs - User wants CONNECTION
    CONVERSATION = "conversation"  # "Hello", "Thanks", "Goodbye"

    # Review Verbs - User wants VALIDATION
    REVIEW = "review"            # "Review X", "Check Y"

    # Fallback
    UNKNOWN = "unknown"          # Grammatically ambiguous


# Grammatical mapping for classification hints
GRAMMAR_HINTS = {
    # Action verb patterns
    ("create", "make", "build", "add", "write"): IntentCategory.EXECUTION,
    ("update", "change", "modify", "edit"): IntentCategory.EXECUTION,
    ("delete", "remove", "cancel"): IntentCategory.EXECUTION,

    # Perception verb patterns
    ("show", "display", "list", "get"): IntentCategory.QUERY,
    ("what is", "what are", "tell me about"): IntentCategory.QUERY,

    # Cognition verb patterns
    ("analyze", "examine", "investigate"): IntentCategory.ANALYSIS,
    ("summarize", "combine", "synthesize"): IntentCategory.SYNTHESIS,
    ("explain", "teach", "how does"): IntentCategory.LEARNING,

    # Planning verb patterns
    ("plan", "design", "outline"): IntentCategory.PLANNING,
    ("what should", "recommend", "suggest"): IntentCategory.GUIDANCE,
    ("prioritize", "most important", "focus on"): IntentCategory.PRIORITY,

    # Social verb patterns
    ("hello", "hi", "hey", "good morning"): IntentCategory.CONVERSATION,
    ("thanks", "thank you", "bye", "goodbye"): IntentCategory.CONVERSATION,
}
```

### Canonical Handlers by Grammatical Role

```python
class IntentService:
    """
    Intent handlers organized by grammatical role.

    Each handler group processes a grammatically-related
    set of intent categories.
    """

    # Action handlers - process execution requests
    async def _handle_execution_intent(self, intent: Intent) -> str:
        """Handle action verbs - something needs to be DONE."""
        pass

    # Perception handlers - answer observation questions
    async def _handle_query_canonical(self, intent: Intent) -> str:
        """Handle perception verbs - user wants to SEE."""
        pass

    async def _handle_status_canonical(self, intent: Intent) -> str:
        """Handle status perception - user observes their state."""
        pass

    async def _handle_identity_canonical(self, intent: Intent) -> str:
        """Handle identity perception - user observes Piper."""
        pass

    # Cognition handlers - provide understanding
    async def _handle_analysis_intent(self, intent: Intent) -> str:
        """Handle cognition verbs - user wants UNDERSTANDING."""
        pass

    # Planning handlers - provide direction
    async def _handle_guidance_canonical(self, intent: Intent) -> str:
        """Handle guidance - user wants DIRECTION."""
        pass

    # Social handlers - maintain connection
    async def _handle_conversation_intent(self, intent: Intent) -> str:
        """Handle social verbs - user wants CONNECTION."""
        pass
```

## Usage Guidelines

### When to Use

- Designing intent classification systems for AI assistants
- Need clear, defensible category boundaries
- Want semantic consistency across classification
- Building systems that need to explain their routing decisions

### When NOT to Use

- Simple command-response systems with fixed commands
- When categories are purely technical (file types, API endpoints)
- Performance-critical paths where semantic analysis is too slow

### Best Practices

1. **Map to grammar first** - When adding a category, identify its verb type
2. **Justify boundaries** - If two categories overlap, they may be grammatically identical
3. **Test with paraphrasing** - Same meaning in different words should route identically
4. **Use grammatical debugging** - "What verb type is this?" clarifies routing issues
5. **Document the mapping** - Make grammatical basis explicit in code comments

## Examples in Codebase

### Primary Usage

- `services/shared_types.py` - `IntentCategory` enum definition
- `services/intent/intent_service.py` - Canonical handlers organized by grammar
- `services/intent_service/pre_classifier.py` - Pattern-to-category mapping

### Test Examples

- `tests/unit/services/test_intent_classification.py` - Category boundary tests
- `tests/unit/services/test_canonical_handlers.py` - Handler routing tests

## Related Patterns

### Complements

- [Pattern-028: Intent Classification](pattern-028-intent-classification.md) - The classification mechanism
- [Pattern-055: Multi-Intent Decomposition](pattern-055-multi-intent-decomposition.md) - Handling multiple grammatical intents
- [Pattern-056: Consciousness Attribute Layering](pattern-056-consciousness-attribute-layering.md) - Entity grammar roles

### Dependencies

- ADR-055: Object Model Specification - "Entities experience Moments at Places" grammar
- #433: MUX-TECH-PHASE1-GRAMMAR - Implementation issue

## References

### Documentation

- Issue #433: MUX-TECH-PHASE1-GRAMMAR
- ADR-055: Object Model Specification
- `docs/internal/architecture/current/models/object-model-specification.md`

### Design Rationale

The grammar-driven approach was chosen over:
- **Flat taxonomy**: No semantic basis for categories
- **Use-case driven**: Categories proliferate without principled limits
- **ML-only classification**: Black box without debuggable routing

Grammar provides both semantic grounding and clear extensibility rules: new categories must identify their verb type and prove they're grammatically distinct from existing categories.

---

_Pattern documented: January 21, 2026_
_Part of MUX-GATE-2 pattern discovery ceremony_
