# ADR-039: Canonical Handler Fast-Path Pattern

## Status
Approved & Implemented (October 7, 2025)

**Related Epics**: GREAT-4C, GREAT-4D, GREAT-4E, GREAT-4F
**Deciders**: Chief Architect, Lead Developer
**Technical Story**: Intent classification dual-path architecture

## Context and Problem Statement

The intent classification system (ADR-032) routes user queries to appropriate handlers. However, not all queries require the same level of processing complexity or response time. Users expect instant responses for simple queries like "who are you?" or "what day is it?", while complex operations like "analyze last week's commits" naturally take longer.

**Key questions addressed**:
- Why do some intents need fast responses while others can be slower?
- What's the tradeoff between speed and capability?
- When should an intent use canonical vs workflow path?
- How do we maintain both simplicity and sophistication?

**Performance requirements**:
- Simple queries should respond in ~1ms (near-instant)
- Complex operations can take 2-3 seconds (includes LLM processing)
- System must handle high throughput for common queries
- Must avoid unnecessary overhead for deterministic operations

## Decision Drivers

### User Experience
- **Instant gratification**: Simple queries deserve instant answers
- **Perceived responsiveness**: 1ms feels instantaneous; 2000ms feels deliberate
- **Natural expectations**: "What time is it?" should be as fast as checking a clock
- **Context-appropriate speed**: Users understand complex tasks take longer

### System Performance
- **Resource optimization**: Don't use expensive LLM processing when unnecessary
- **Scalability**: Fast path can handle 600K+ requests/second
- **Cost efficiency**: Canonical handlers avoid per-query LLM API costs
- **Throughput**: High-frequency queries need low-latency path

### Architectural Clarity
- **Separation of concerns**: Simple handlers for simple queries, orchestration for complexity
- **Maintainability**: Clear boundary between deterministic and dynamic processing
- **Testing**: Canonical handlers have deterministic test cases
- **Predictability**: Fast path behavior is consistent and reliable

### Implementation Pragmatism
- **Incremental value**: Can implement canonical handlers first, add workflows later
- **Risk mitigation**: Fast path provides fallback if workflow system has issues
- **Developer experience**: Clear decision criteria for categorizing new intents
- **Measurable outcomes**: Distinct performance characteristics enable clear validation

## Considered Options

### Option 1: Single Path (All Through Workflows)
**Description**: Route all intents through workflow orchestration, regardless of complexity.

**Pros**:
- Simple mental model (one code path)
- Consistent behavior across all intents
- Easier to add cross-cutting concerns
- Single testing strategy

**Cons**:
- 2000-3000ms latency for simple queries (poor UX)
- Unnecessary LLM overhead for deterministic queries
- Lower throughput capability
- Higher operational costs
- Overkill for "who are you?" type queries

**Verdict**: ❌ Rejected - unacceptable latency for simple queries

### Option 2: Single Path (All Canonical)
**Description**: Implement all intents as fast canonical handlers with hardcoded logic.

**Pros**:
- Consistently fast (~1ms for all queries)
- Predictable behavior
- Lower operational costs
- Simple codebase

**Cons**:
- Cannot handle complex multi-step operations
- No orchestration capability
- Rigid and inflexible
- Difficult to add sophisticated features
- Doesn't leverage LLM capabilities where valuable

**Verdict**: ❌ Rejected - insufficient capability for complex operations

### Option 3: Dual Path (Canonical + Workflow) ✅
**Description**: Fast canonical handlers for simple deterministic queries, workflow orchestration for complex operations.

**Pros**:
- Optimal performance for each use case
- Best user experience (instant for simple, capable for complex)
- Resource-efficient
- Scalable architecture
- Clear decision criteria

**Cons**:
- Two code paths to maintain
- Requires classification accuracy
- More complex mental model
- Need to categorize each new intent

**Verdict**: ✅ **CHOSEN** - optimal tradeoff between speed and capability

## Decision Outcome

**Chosen option**: **Dual-path architecture** with canonical handlers for simple, deterministic queries and workflow orchestration for complex operations.

### Canonical Path (Fast-Path)

**Intent Categories**: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE

**Characteristics**:
- **Deterministic responses**: No LLM needed for execution (may be used for classification)
- **Simple operations**: Data retrieval, formatting, basic transformations
- **Pattern recognition**: Pre-classifier can recognize instantly
- **Performance**: ~1ms response time
- **Throughput**: 600K+ requests/second sustained
- **Predictability**: Consistent behavior, easy to test

**Implementation Location**: `services/intent/intent_service.py` lines 123-131

**Example routing code**:
```python
# Canonical handler routing (simplified)
if intent.category == IntentCategory.IDENTITY:
    return await self._handle_identity_intent(intent, session_id)
elif intent.category == IntentCategory.TEMPORAL:
    return await self._handle_temporal_intent(intent, session_id)
elif intent.category == IntentCategory.STATUS:
    return await self._handle_status_intent(intent, session_id)
elif intent.category == IntentCategory.PRIORITY:
    return await self._handle_priority_intent(intent, session_id)
elif intent.category == IntentCategory.GUIDANCE:
    return await self._handle_guidance_intent(intent, session_id)
```

**Canonical Handler Examples**:

| Category | Example Query | Response Type | Speed |
|----------|--------------|---------------|-------|
| IDENTITY | "Who are you?" | Static text from config | ~1ms |
| TEMPORAL | "What day is it?" | datetime.now() formatting | ~1ms |
| STATUS | "Show standup" | PIPER.md section retrieval | ~1ms |
| PRIORITY | "What's my priority?" | PIPER.md priority parsing | ~1ms |
| GUIDANCE | "How do I...?" | Help text lookup | ~1ms |

### Workflow Path (Standard Path)

**Intent Categories**: EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, UNKNOWN, QUERY, CONVERSATION

**Characteristics**:
- **Complex multi-step operations**: Require orchestration
- **External service integration**: GitHub, Slack, Calendar APIs
- **State management**: Track operation progress
- **LLM reasoning**: Generate content, analyze data
- **Performance**: 2000-3000ms (includes LLM classification + processing)
- **Capability**: Full orchestration and coordination

**Implementation**: Routes to `WorkflowFactory` which creates appropriate workflow instances

**Workflow Handler Examples**:

| Category | Example Query | Operations Required | Speed |
|----------|--------------|---------------------|-------|
| EXECUTION | "Create GitHub issue" | LLM classify → GitHub API call → Confirmation | 2-3s |
| ANALYSIS | "Analyze commits" | Git log retrieval → LLM analysis → Report generation | 2-3s |
| SYNTHESIS | "Summarize PRs" | GitHub API → LLM summarization → Formatting | 2-3s |
| STRATEGY | "Plan sprint" | Context gathering → LLM planning → Structured output | 2-3s |
| LEARNING | "What patterns exist?" | Data extraction → Pattern recognition → Learning update | 2-3s |

### Positive Consequences

#### User Experience
- ✅ **Instant responses** for common queries (IDENTITY, TEMPORAL, STATUS)
- ✅ **Appropriate delays** for complex operations (users expect these to take time)
- ✅ **Natural interaction** patterns match user mental models
- ✅ **Predictable behavior** for deterministic queries

#### Performance
- ✅ **Optimal resource usage**: Avoid LLM when not needed
- ✅ **High throughput**: 600K+ req/sec for canonical handlers (GREAT-4E validation)
- ✅ **Scalability**: Fast path handles volume without bottlenecks
- ✅ **Cost efficiency**: Reduced LLM API costs for simple queries

#### Architecture
- ✅ **Clear separation**: Simple vs complex logic well-defined
- ✅ **Maintainability**: Canonical handlers are easy to understand and test
- ✅ **Flexibility**: Can add sophisticated workflows without impacting fast path
- ✅ **Progressive enhancement**: Start with canonical, add workflows as needed

#### Validation
- ✅ **Measurable performance**: Clear targets for each path (~1ms vs 2-3s)
- ✅ **Testability**: Deterministic canonical handlers have predictable tests
- ✅ **Monitoring**: Distinct metrics for each path enable focused optimization

### Negative Consequences

#### Complexity
- ⚠️ **Dual maintenance**: Two code paths to maintain and understand
- ⚠️ **Mental overhead**: Developers must know which path for new intents
- ⚠️ **Decision burden**: Must categorize each new intent category
- ⚠️ **Documentation need**: Requires clear guidance on path selection

#### Dependencies
- ⚠️ **Classification critical**: Mis-classification causes poor UX (GREAT-4F addresses this)
- ⚠️ **Accuracy requirement**: Pre-classifier must achieve 95%+ accuracy
- ⚠️ **Fallback needed**: QUERY category provides safety net for mis-classifications

#### Testing
- ⚠️ **Different strategies**: Canonical uses mocks, workflows need integration tests
- ⚠️ **Coverage tracking**: Must ensure both paths adequately tested
- ⚠️ **Performance validation**: Different benchmarks for each path

### Mitigation Strategies

**For classification accuracy** (GREAT-4F):
- QUERY fallback handler prevents timeout errors
- Pre-classifier with pattern matching for canonical categories
- LLM prompt enhancement with disambiguation rules
- Target: 95%+ accuracy for canonical categories

**For developer experience**:
- Clear decision criteria (documented below)
- ADR-043 provides guidance for future intents
- Pattern-032 documents existing patterns
- Implementation guides for each handler type

**For maintenance burden**:
- Shared utilities for common operations
- Consistent handler interface patterns
- Comprehensive test coverage for both paths
- Monitoring and metrics for both paths

## Implementation Notes

### How Classification Works

**Two-stage classification process**:

1. **Pre-classifier** (Fast Pattern Matching)
   - Checks for canonical category patterns
   - High-confidence keyword/phrase matching
   - Instant routing for recognized patterns
   - Falls back to LLM if uncertain

2. **LLM Classifier** (Full Understanding)
   - Natural language understanding
   - Routes to appropriate workflow type
   - Current accuracy: 85-95% (GREAT-4F goal: 95%+)
   - Caching improves performance (84.6% hit rate)

### Performance Metrics (from GREAT-4E Validation)

**Canonical Path**:
- Response time: ~1ms average
- Throughput: 602,907 req/sec sustained over 5 minutes
- Cache hit rate: 84.6%
- Cache speedup: 7.6x
- Memory: Stable, no leaks detected

**Workflow Path**:
- Response time: 2000-3000ms (includes LLM classification)
- Throughput: Limited by LLM API rate limits
- Success rate: 100% when correctly classified
- Failure mode: Graceful degradation with user-friendly errors

**Overall System**:
- Test coverage: 126 tests (52 interface + 65 contract + 9 coverage reports)
- Load testing: 5/5 benchmarks passed
- Production status: ✅ Deployed October 6, 2025

### Decision Criteria for New Intent Categories

Use **Canonical Path** if ALL of these are true:
- ✅ Response is deterministic (same input → same output, no reasoning needed)
- ✅ Simple data retrieval or transformation
- ✅ User expects instant response (< 100ms)
- ✅ High frequency query (will benefit from optimization)
- ✅ No external service calls required
- ✅ No multi-step orchestration needed

Use **Workflow Path** if ANY of these are true:
- ✅ Requires multi-step orchestration
- ✅ Needs external service calls (GitHub, Slack, Calendar)
- ✅ Benefits from state management
- ✅ Complex reasoning or content generation needed
- ✅ Non-deterministic output (varies based on context/data)
- ✅ Lower frequency query (optimization less critical)

**When in doubt**: Start with workflow path. Can optimize to canonical later if usage patterns warrant.

### Examples of Path Selection

**Canonical Candidates** ✅:
- "Who are you?" → IDENTITY (static config lookup)
- "What day is it?" → TEMPORAL (datetime formatting)
- "Show my standup" → STATUS (config section retrieval)
- "What's my top priority?" → PRIORITY (config parsing)
- "How do I create an issue?" → GUIDANCE (help text lookup)

**Workflow Candidates** ✅:
- "Create GitHub issue for bug" → EXECUTION (GitHub API + coordination)
- "Analyze last week's commits" → ANALYSIS (git log + LLM analysis)
- "Summarize open PRs" → SYNTHESIS (GitHub API + LLM summarization)
- "Plan next sprint" → STRATEGY (data gathering + LLM planning)
- "What patterns exist in my code?" → LEARNING (analysis + pattern recognition)
- "What's the weather?" → QUERY (external API lookup)
- "Let's chat about the project" → CONVERSATION (LLM dialogue)

### Codebase Locations

**Canonical Handler Implementation**:
- Main routing: `services/intent/intent_service.py` lines 123-131
- Handler methods: `services/intent/intent_service.py` lines 200-450
- Tests: `tests/intent/test_direct_interface.py`

**Workflow Handler Implementation**:
- Workflow factory: `services/orchestration/workflow_factory.py`
- Workflow types: `services/orchestration/workflows/`
- Tests: `tests/intent/test_direct_interface.py` (workflow categories)

**Classification**:
- Pre-classifier: `services/intent_service/pre_classifier.py`
- LLM classifier: Integrated in intent service
- Configuration: `services/config.py`

## Related Decisions

- [ADR-032: Intent Classification Universal Entry](./adr-032-intent-classification-universal-entry.md) - Overall intent classification architecture
- [Pattern-032: Intent Pattern Catalog](../patterns/pattern-032-intent-pattern-catalog.md) - Comprehensive pattern documentation
- [ADR-013: MCP Spatial Integration Pattern](./adr-013-mcp-spatial-integration-pattern.md) - Context-aware response formatting

## References

### Documentation
- Intent Classification Guide: `docs/guides/intent-classification-guide.md`
- Canonical Handlers Architecture: `docs/guides/canonical-handlers-architecture.md`
- Intent Categories Reference: `docs/reference/intent-categories.md`
- Intent Migration Guide: `docs/guides/intent-migration.md`

### Implementation Evidence
- GREAT-4C: Canonical handler implementation (October 6, 2025)
- GREAT-4D: Workflow handler implementation (October 6, 2025)
- GREAT-4E: Validation and load testing (October 6, 2025)
- GREAT-4F: Classifier accuracy improvements (October 7, 2025)

### Performance Validation
- Load test results: `dev/2025/10/06/great4e-2-phase0-assessment.md`
- Cache performance: `dev/2025/10/06/piper-cache-implementation.md`
- Validation report: `dev/2025/10/06/great-4c-validation-report.md`

---

## Appendix: Architecture Diagram

```
User Input (CLI/Web/Slack)
          ↓
    Intent Service
          ↓
    Pre-Classifier
     /           \
    /             \
FAST PATH      UNCERTAIN
 (~1ms)            ↓
   ↓          LLM Classifier
   ↓           /           \
   ↓      CANONICAL      WORKFLOW
   ↓      (re-route)     (2-3s)
   ↓          ↓              ↓
Canonical ←───┘              ↓
Handlers               Workflow Factory
   ↓                         ↓
   ↓                   Orchestration
   ↓                         ↓
   └────────────┬────────────┘
                ↓
            Response
```

**Path Selection Logic**:
1. Pre-classifier attempts pattern match
2. High confidence → Canonical path (~1ms)
3. Low confidence → LLM classifier
4. LLM determines category
5. Canonical categories → Fast handlers
6. Workflow categories → Orchestration
7. QUERY mis-classifications → Smart fallback (GREAT-4F)

---

**Status**: ✅ Approved and Implemented
**Date**: October 7, 2025
**Next Review**: When adding new intent categories or observing classification accuracy issues
**Maintained By**: Lead Developer, Chief Architect
