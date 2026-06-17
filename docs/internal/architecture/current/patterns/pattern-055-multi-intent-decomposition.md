# Pattern-055: Multi-Intent Decomposition

## Status

**Proven** — demonstrated in #595 MUX-INTENT-MULTI (promoted 2026-06-17, instance verified)

## Context

Users naturally combine multiple intents in single messages:
- "Hi Piper! What's on my agenda?" (greeting + calendar query)
- "Thanks! What should I focus on next?" (thanks + priority query)
- "Good morning, show my todos" (greeting + todo query)

Traditional intent classification returns a single intent, causing:
- First-match-wins behavior (greeting detected, query lost)
- User frustration when substantive requests are ignored
- Perception that the system doesn't understand compound requests

This pattern addresses how to detect, decompose, and handle multiple intents in a single user message.

## Pattern Description

**Core Concept**: Separate intent detection from intent handling strategy.

1. **Detection Phase**: Scan for ALL matching patterns, not just the first
2. **Result Structure**: Return a collection of intents with metadata
3. **Strategy Selection**: Choose how to handle multiple intents (handle all, chain, clarify)
4. **Priority Ordering**: Substantive intents take precedence over conversational

The pattern enables strategy evolution without rewriting detection logic.

## Implementation

### Structure

```
User Message
    ↓
┌─────────────────────┐
│ detect_multiple_    │ → MultiIntentResult
│ intents()           │   - intents: List[Intent]
└─────────────────────┘   - is_multi_intent: bool
    ↓                     - primary_intent
┌─────────────────────┐   - secondary_intents
│ Strategy Selection  │   - has_greeting
│ (handle all/chain/  │   - has_substantive_intent
│  clarify)           │
└─────────────────────┘
    ↓
Handler(s) Execute
```

### Code Example

```python
@dataclass
class MultiIntentResult:
    """Result of multi-intent detection."""

    intents: List[Intent] = field(default_factory=list)
    original_message: str = ""
    is_multi_intent: bool = False

    @property
    def primary_intent(self) -> Optional[Intent]:
        """Get primary intent - substantive over conversational."""
        if not self.intents:
            return None
        # Substantive intents take precedence
        for intent in self.intents:
            if intent.category != IntentCategory.CONVERSATION:
                return intent
        return self.intents[0]

    @property
    def has_greeting(self) -> bool:
        """Check if greeting is among detected intents."""
        return any(
            i.category == IntentCategory.CONVERSATION and i.action == "greeting"
            for i in self.intents
        )

    @property
    def has_substantive_intent(self) -> bool:
        """Check for non-conversational intent."""
        return any(i.category != IntentCategory.CONVERSATION for i in self.intents)
```

### Detection Implementation

```python
@staticmethod
def detect_multiple_intents(message: str) -> MultiIntentResult:
    """Detect ALL intents in a message."""
    intents = []

    # Check each pattern group (don't return early!)
    pattern_groups = [
        (GREETING_PATTERNS, IntentCategory.CONVERSATION, "greeting"),
        (CALENDAR_PATTERNS, IntentCategory.QUERY, "meeting_time"),
        (TODO_PATTERNS, IntentCategory.QUERY, "list_todos"),
        # ... more pattern groups
    ]

    for patterns, category, action in pattern_groups:
        if matches_patterns(message, patterns):
            intents.append(Intent(category=category, action=action))

    return MultiIntentResult(
        intents=intents,
        original_message=message,
        is_multi_intent=len(intents) > 1,
    )
```

### Strategy: Handle All (Current Implementation)

```python
# In IntentService._process_intent_internal()
multi_result = await self.intent_classifier.classify_multiple(message)

if multi_result.is_multi_intent and multi_result.has_greeting and multi_result.has_substantive_intent:
    # Use substantive intent for processing
    intent = multi_result.primary_intent
    # Mark greeting for response prefix
    intent.context["multi_intent_greeting"] = True

# Later, when building response:
if intent.context.get("multi_intent_greeting"):
    response = f"Hi there! {substantive_response}"
```

## Usage Guidelines

### When to Use

- User messages commonly combine greetings with requests
- System needs to handle compound queries
- You want to evolve handling strategy without changing detection

### When NOT to Use

- Single-purpose command interfaces (CLIs)
- High-precision domains where ambiguity is dangerous
- When clarification is always preferred over assumption

### Best Practices

1. **Detection should be exhaustive** - Check all pattern groups
2. **Keep detection separate from strategy** - Makes strategy changes easy
3. **Substantive intents are primary** - Users expect their request handled
4. **Acknowledge secondary intents** - "Hi there!" prefix shows greeting was heard
5. **Log multi-intent occurrences** - Helps tune detection patterns

## Examples in Codebase

### Primary Usage

- `services/intent_service/pre_classifier.py` - `MultiIntentResult`, `detect_multiple_intents()`
- `services/intent_service/classifier.py` - `classify_multiple()`
- `services/intent/intent_service.py` - Handle-all strategy in `_process_intent_internal()`

### Test Examples

- `tests/unit/services/test_multi_intent.py` - 27 comprehensive tests

## Related Patterns

### Complements

- [Pattern-028: Intent Classification](pattern-028-intent-classification.md) - Single intent classification
- [Pattern-032: Intent Pattern Catalog](pattern-032-intent-pattern-catalog.md) - Pattern definitions

### Future Evolution

- **#427 Unified Conversation Model** - Will add sophisticated strategy selection
- **Chain Strategy** - Handle intents sequentially with context carry-over
- **Clarify Strategy** - Ask user which intent to prioritize

## References

### Documentation

- Issue #595: MUX-INTENT-MULTI
- Issue #427: Unified Conversation Model (future)
- ADR-049: Two-Tier Intent Classification

### Discovery

- Discovered: January 15, 2026 during alpha testing
- Implemented: January 21, 2026
- Anti-pattern fixed: First-Match-Wins behavior

---

_Pattern documented: January 21, 2026_
_Part of MUX-GATE-2 pattern discovery ceremony_
