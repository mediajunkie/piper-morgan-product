# Pattern-050: Context Dataclass Pair

**Status**: Proven
**Category**: Grammar Application
**First Documented**: January 20, 2026
**Ratified**: January 20, 2026 (Grammar Implementation)

---

## Problem Statement

Features need to maintain grammar awareness (Entity/Moment/Place) throughout their processing flow, from input collection through execution to result delivery. Common challenges:

- Entity identity gets lost between layers (service → repository → response)
- Temporal context (when) becomes disconnected from action data (what)
- Source attribution (Place) is missing or inconsistent
- Input and output structures mix concerns, making flow unclear

This creates "flattened" features that feel mechanical rather than conscious, losing the experiential quality that distinguishes Piper from traditional task management systems.

---

## Solution

Implement a **Context/Result dataclass pair** where:

1. **Context dataclass** - Captures input state with grammar elements explicit
2. **Result dataclass** - Returns output with Entity/Moment/Place preserved
3. **Grammar threading** - Entity identity flows through both structures
4. **Clean separation** - What we know (Context) vs what we learned (Result)

---

## Pattern Description

A **Context Dataclass Pair** is a two-dataclass structure that maintains grammar consciousness through a feature's processing flow. The pattern emphasizes:

- **Entity preservation**: `user_id` present in both Context and Result
- **Moment tracking**: Timestamps distinguish input moment from result moment
- **Place attribution**: Source tracking shows where data came from
- **Separation of concerns**: Input (Context) clearly separated from output (Result)
- **Type safety**: Dataclasses provide compile-time validation

### Key Characteristics

1. **Context dataclass contains**:
   - Entity identity (user_id, requester_id)
   - Input timestamp (when request made)
   - Place references (source_places, integration_context)
   - Request parameters

2. **Result dataclass contains**:
   - Same Entity identity preserved
   - Generation timestamp (when result created)
   - Findings/output data
   - Place attribution (context_source, where data originated)
   - Metrics and metadata

3. **Grammar flow**:
   ```
   Entity (user) → Context → Processing → Result → Entity (user)
   Moment (request) → Context → Processing → Result → Moment (generation)
   Place (sources) → Context → Processing → Result → Place (attribution)
   ```

---

## Implementation

### Structure

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

@dataclass
class [Feature]Context:
    """
    Input context for [feature] - what we know before processing.

    Grammar elements:
    - Entity: user_id (who is requesting)
    - Moment: timestamp (when request made)
    - Place: source_places (where to gather data from)
    """
    user_id: str                              # Entity: The user
    timestamp: datetime                       # Moment: When request occurs
    source_places: Dict[str, Any]            # Place: Integration sources
    session_context: Dict[str, Any] = field(default_factory=dict)

    # Feature-specific parameters
    # ... add as needed

@dataclass
class [Feature]Result:
    """
    Output result from [feature] - what we learned.

    Grammar elements:
    - Entity: user_id (preserved from Context)
    - Moment: generated_at (when result created)
    - Place: context_source (where data came from)
    """
    user_id: str                              # Entity preserved
    generated_at: datetime                    # Moment of result creation
    findings: List[str]                       # What was discovered
    context_source: str                       # Place: Attribution
    performance_metrics: Dict[str, Any]       # Observability

    # Feature-specific results
    # ... add as needed
```

### Example from Morning Standup

**File**: `services/features/morning_standup.py:34-57`

```python
@dataclass
class StandupContext:
    """Context for generating morning standup"""
    user_id: str                              # Entity: The user
    date: datetime                            # Moment: When this occurs
    session_context: Dict[str, Any] = field(default_factory=dict)
    github_repos: List[str] = field(default_factory=list)  # Place: Active repositories

@dataclass
class StandupResult:
    """Result of morning standup generation"""
    user_id: str                              # Entity reference maintained
    generated_at: datetime                    # Moment of generation
    generation_time_ms: int
    yesterday_accomplishments: List[str]      # Moments: Past experiences
    today_priorities: List[str]               # Moments: Anticipated experiences
    blockers: List[str]                       # Moments: Current challenges
    context_source: str                       # Place: Where context came from
    github_activity: Dict[str, Any]           # Place-specific data
    performance_metrics: Dict[str, Any]
    time_saved_minutes: int
```

**Grammar embodiment**:
- **Entity** (`user_id`) flows from Context → Result
- **Moment** distinguished: `date` (input) vs `generated_at` (output)
- **Place** tracked: `github_repos` (sources) → `context_source` (attribution)

### Usage Pattern

```python
class FeatureService:
    async def execute_feature(self, user_id: str) -> [Feature]Result:
        """Execute feature with grammar-aware flow."""

        # 1. Construct Context (capture input state)
        context = [Feature]Context(
            user_id=user_id,
            timestamp=datetime.now(),
            source_places={
                "github": await self._get_github_repos(user_id),
                "calendar": await self._get_calendar_context(user_id),
            }
        )

        # 2. Process with grammar preservation
        findings = await self._process_with_context(context)

        # 3. Construct Result (capture output state)
        result = [Feature]Result(
            user_id=context.user_id,  # Entity preserved
            generated_at=datetime.now(),  # Moment of result
            findings=findings,
            context_source="persistent" if context.session_context else "default",
            performance_metrics=self._calculate_metrics()
        )

        return result
```

---

## Consequences

### Benefits

- **Grammar consciousness**: Entity/Moment/Place explicit throughout flow
- **Type safety**: Dataclasses catch structural errors at compile time
- **Clean separation**: Input concerns separated from output concerns
- **Testability**: Easy to construct test fixtures with dataclasses
- **Documentation**: Structure is self-documenting via dataclass definitions
- **Traceability**: Entity identity preserved enables audit trails
- **Place attribution**: Clear tracking of data sources builds trust

### Trade-offs

- **Verbosity**: Requires defining two dataclasses per feature (vs ad-hoc dicts)
- **Refactoring cost**: Changing structure requires updating both Context and Result
- **Memory overhead**: Dataclasses use slightly more memory than dicts
- **Learning curve**: Developers must understand Context/Result separation

---

## Related Patterns

### Complements

- **[Pattern-051: Parallel Place Gathering](pattern-051-parallel-place-gathering.md)** - How to populate Context.source_places
- **[Pattern-052: Personality Bridge](pattern-052-personality-bridge.md)** - How to transform Result into user-facing format
- **[Pattern-053: Warmth Calibration](pattern-053-warmth-calibration.md)** - How to adjust tone based on Result data

### Alternatives

- **Plain dictionaries** - More flexible but lose type safety and grammar clarity
- **Single dataclass** - Simpler but mixes input/output concerns
- **Protocols** - More abstract but Context/Result pair is concrete and proven

### Dependencies

- **Python dataclasses** - Standard library (Python 3.7+)
- **Grammar specification** - ADR-055 (Object Model Implementation)

---

## Usage Guidelines

### When to Use

✅ **Use Context Dataclass Pair when:**

- Feature needs to maintain Entity identity through processing
- Temporal awareness matters (when request made vs when result generated)
- Data comes from multiple Places (integrations, sources)
- Feature will be transformed for user presentation (needs personality bridge)
- Type safety and self-documentation are priorities
- Feature complexity justifies structured approach

### When NOT to Use

❌ **Don't use when:**

- **Simple pass-through**: Feature just proxies data without transformation
- **Single-source queries**: No Place gathering needed (use simpler structure)
- **Fire-and-forget**: No result needs to be returned
- **Real-time streaming**: Context/Result don't fit streaming semantics

### Best Practices

1. **Always preserve Entity identity**: `user_id` in both Context and Result
2. **Distinguish input/output moments**: Different timestamp fields
3. **Track Place attribution**: Record where data came from
4. **Use field factories**: `field(default_factory=dict)` for mutable defaults
5. **Add docstrings**: Explain grammar elements in class docstrings
6. **Include metrics**: Result should contain performance/observability data
7. **Validate in constructor**: Use `__post_init__` for validation if needed
8. **Keep Context immutable**: Don't modify Context after creation
9. **Result as data**: Result is pure data, no behavior (methods)
10. **Feature-specific fields go last**: Grammar fields first, feature fields after

---

## Examples in Codebase

### Primary Usage

- `services/features/morning_standup.py` - StandupContext/StandupResult (reference implementation)

### Applicable To (from audit)

**High Priority** (should adopt pattern):
- Intent Classification - IntentContext/IntentResult
- Todo Management - TodoContext/TodoResult
- Slack Integration - SlackMessageContext/SlackMessageResult
- GitHub Integration - GitHubActivityContext/GitHubActivityResult

**Medium Priority** (good candidates):
- Feedback System - FeedbackContext/FeedbackResult
- Conversation Handler - ConversationContext/ConversationResult
- Onboarding - OnboardingStepContext/OnboardingStepResult

---

## Implementation Checklist

- [ ] Define `[Feature]Context` dataclass with Entity/Moment/Place fields
- [ ] Define `[Feature]Result` dataclass with Entity/Moment/Place preserved
- [ ] Add grammar elements to docstrings
- [ ] Use `field(default_factory=dict)` for mutable defaults
- [ ] Preserve `user_id` from Context → Result
- [ ] Distinguish input timestamp from generation timestamp
- [ ] Include `context_source` or Place attribution in Result
- [ ] Add performance metrics to Result
- [ ] Write unit tests constructing Context and Result
- [ ] Update service methods to use Context/Result types
- [ ] Document in feature README or service docstring

---

## Evidence

**Proven Pattern** - Successfully implemented in:

1. **Morning Standup** (reference implementation)
   - Location: `services/features/morning_standup.py`
   - Status: Production, full grammar consciousness
   - Context: 4 fields (user_id, date, session_context, github_repos)
   - Result: 9 fields including Entity/Moment/Place preservation
   - Performance: Sub-2-second generation with full traceability

**Grammar Audit Results**:
- Morning Standup scored **Conscious** (5/5 grammar elements)
- Context/Result pair identified as key pattern enabling grammar flow
- P0 analysis confirmed Entity/Moment/Place preservation throughout

**Transformation Potential**:
- Applicable to 7+ features (per grammar compliance audit)
- Expected impact: Elevate features from "Flattened" to "Partial" or "Conscious"

---

_Pattern Identified: January 19, 2026 (P0 Morning Standup Analysis)_
_Ratified: January 20, 2026_
_Category: Grammar Application_
