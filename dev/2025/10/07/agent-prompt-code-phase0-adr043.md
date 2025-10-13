# Prompt for Code Agent: GREAT-4F Phase 0 - ADR-043 Documentation

## Context

GREAT-4F mission: Address 5-15% mis-classification rate and formalize canonical handler pattern.

**This is Phase 0**: Document the canonical handler fast-path pattern with ADR-043.

## Session Log

Start new log: `dev/2025/10/07/2025-10-07-0730-prog-code-log.md`

## Mission

Create ADR-043 documenting why and how the dual-path architecture (canonical vs workflow) exists and works.

---

## Background from GREAT-4E

**What we know**:
- Canonical handlers exist at lines 123-131 in `services/intent/intent_service.py`
- 5 categories use fast path: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE
- 8 categories use workflow path: EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, UNKNOWN, QUERY, CONVERSATION
- Fast path: ~1ms response time
- Workflow path: 2000-3000ms (LLM classification + orchestration)
- Architecture is intentional and working correctly
- Problem is LLM mis-classification (85-95% accuracy), not routing

---

## Task: Create ADR-043

**File**: `docs/internal/architecture/current/adrs/adr-043-canonical-handler-pattern.md`

### Required Structure

```markdown
# ADR-043: Canonical Handler Fast-Path Pattern

**Status**: Approved
**Date**: October 7, 2025
**Deciders**: Chief Architect, Lead Developer
**Technical Story**: GREAT-4C-4E Intent System Implementation

## Context and Problem Statement

[Explain the need for two different paths through the intent system]

Questions to answer:
- Why do some intents need fast responses while others can be slower?
- What's the tradeoff between speed and capability?
- When should an intent use canonical vs workflow path?

## Decision Drivers

[List factors that led to dual-path design]

Examples:
- User experience (fast responses for simple queries)
- System performance (avoid LLM overhead when unnecessary)
- Architectural clarity (simple handlers for simple intents)
- Scalability (fast path can handle higher throughput)

## Considered Options

[What alternatives were considered?]

1. **Single path (all through workflows)** - Simple but slow
2. **Single path (all canonical)** - Fast but inflexible
3. **Dual path (current decision)** - Optimal tradeoff

## Decision Outcome

Chosen option: **Dual-path architecture** with canonical handlers for simple, deterministic queries and workflow orchestration for complex operations.

### Canonical Path (Fast)

**Categories**: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE

**Characteristics**:
- Deterministic responses (no LLM needed for execution)
- Simple data retrieval or transformation
- Pre-classifier can recognize patterns instantly
- ~1ms response time
- High throughput capability

**Implementation**: Lines 123-131 in `services/intent/intent_service.py`

```python
# Canonical handler routing (simplified example)
if intent.category == IntentCategory.IDENTITY:
    return await self._handle_identity_intent(intent, session_id)
elif intent.category == IntentCategory.TEMPORAL:
    return await self._handle_temporal_intent(intent, session_id)
# ... etc for STATUS, PRIORITY, GUIDANCE
```

### Workflow Path (Standard)

**Categories**: EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, UNKNOWN, QUERY, CONVERSATION

**Characteristics**:
- Complex multi-step operations
- Requires orchestration and state management
- May need external service calls
- 2000-3000ms response time (includes LLM classification)
- Lower throughput but higher capability

**Implementation**: Routes to `WorkflowFactory` for orchestration

### Positive Consequences

- Fast responses for common simple queries (IDENTITY: "who are you?", STATUS: "show standup")
- Full orchestration capability for complex operations
- Optimal resource usage (don't use LLM when not needed)
- Clear architectural separation of concerns
- Scalable (fast path handles high volume)

### Negative Consequences

- Two code paths to maintain
- Classifier accuracy critical (mis-classification causes issues)
- Need to decide which path for new intent categories
- More complex mental model for developers

## Implementation Notes

### How Classification Works

1. **Pre-classifier** checks for canonical patterns (fast path)
   - Keyword matching for common phrases
   - High-confidence instant routing
   - Falls back to LLM if uncertain

2. **LLM Classifier** for workflow path
   - Full natural language understanding
   - Routes to appropriate workflow type
   - 85-95% accuracy (GREAT-4F goal: improve to 95%+)

### Performance Metrics (from GREAT-4E)

- Pre-classifier: ~1ms for canonical categories
- LLM classification: 2000-3000ms for workflow categories
- Cache hit rate: 84.6%
- Cache speedup: 7.6x
- Sustained throughput: 602,907 req/sec

### Adding New Intent Categories

**Decision criteria**:

Use **Canonical Path** if:
- Response is deterministic (no reasoning needed)
- Simple data retrieval or formatting
- User expects instant response
- High frequency query

Use **Workflow Path** if:
- Requires multi-step orchestration
- Needs external service calls
- Benefits from state management
- Complex reasoning or generation needed

## Related Decisions

- [ADR-032: Intent Classification Universal Entry](./adr-032-intent-classification-universal-entry.md)
- [Pattern-032: Intent Pattern Catalog](../patterns/pattern-032-intent-pattern-catalog.md)

## References

- GREAT-4C: Canonical handler implementation
- GREAT-4D: Workflow handler implementation
- GREAT-4E: Validation and load testing
- Intent Classification Guide: `docs/guides/intent-classification-guide.md`

---

**Status**: ✅ Approved and Implemented
**Last Updated**: October 7, 2025
**Next Review**: When adding new intent categories
```

---

## Verification

After creating ADR-043, verify:

```bash
# File exists
ls -la docs/internal/architecture/current/adrs/adr-043*.md

# Has substantial content
wc -l docs/internal/architecture/current/adrs/adr-043*.md
# Should be >100 lines

# Explains dual-path decision
grep -i "canonical\|workflow" docs/internal/architecture/current/adrs/adr-043*.md | wc -l
# Should have many mentions
```

---

## Success Criteria

- [ ] ADR-043 created in correct location
- [ ] Explains WHY dual-path architecture exists
- [ ] Documents WHEN to use each path
- [ ] Includes performance metrics from GREAT-4E
- [ ] References related ADRs and patterns
- [ ] Approved status
- [ ] >100 lines of substantive content
- [ ] Session log updated

---

## Critical Notes

- This ADR documents an EXISTING pattern, not a new decision
- Focus on explaining the rationale, not the implementation details
- Performance metrics from GREAT-4E are critical evidence
- Should help future developers decide which path for new intents

---

**Effort**: Small (~20-30 minutes)
**Priority**: HIGH (foundation for GREAT-4F)
**Deliverable**: ADR-043 documenting canonical handler pattern
