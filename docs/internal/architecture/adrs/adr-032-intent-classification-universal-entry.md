# ADR-032: Intent Classification as Universal Entry Point

## Status
Accepted & Validated (GREAT-4E Phase 4 - October 6, 2025)

## Context
Currently, users must learn specific commands and syntax to interact with Piper Morgan effectively. The May 28 vision proposed natural language as the primary interface, with intent classification routing all interactions. Recent advances in LLM capabilities make this vision more achievable now than at conception.

## Decision
We will implement intent classification as the universal entry point for all Piper Morgan interactions. Every user input, regardless of source (CLI, web, Slack), will first pass through intent classification before routing to appropriate handlers.

### Classification Layer Architecture
```
User Input → Intent Classifier → Router → Handler → Response
                     ↓                       ↓
              Learning System        Canonical Handlers
                                    (Fast-path for 5 categories)
```

### Intent Categories (13 Total)

**Canonical Categories** (Fast-path handlers):
- **IDENTITY**: "Who are you?" queries about Piper's identity and capabilities
- **TEMPORAL**: Time, date, schedule queries ("What day is it?")
- **STATUS**: Project/work status queries ("What am I working on?")
- **PRIORITY**: Priority and focus queries ("What's my top priority?")
- **GUIDANCE**: Help and how-to queries ("How do I create an issue?")

**Workflow Categories** (Orchestrated processing):
- **EXECUTION**: Create/update work items (GitHub issues, tasks)
- **ANALYSIS**: Analyze commits, PRs, data patterns
- **SYNTHESIS**: Generate reports, summaries, documentation
- **STRATEGY**: Strategic planning, prioritization decisions
- **LEARNING**: Pattern learning, system improvements
- **QUERY**: Information retrieval from integrated systems
- **CONVERSATION**: General conversation and clarifications
- **UNKNOWN**: Ambiguous queries requiring clarification

## Consequences

### Positive
- **Natural interaction**: No command memorization required
- **Universal interface**: Works identically across all entry points
- **Learning opportunity**: Every interaction improves classification
- **Progressive enhancement**: Can start simple, evolve to sophisticated
- **Reduced cognitive load**: Users think in intentions, not commands

### Negative
- **Initial accuracy issues**: Early classification will have errors
- **Latency addition**: Extra processing step for all interactions
- **Ambiguity handling**: Some inputs have multiple valid interpretations
- **Training data requirement**: Needs accumulated interactions to improve

### Neutral
- **Development complexity**: Adds abstraction layer to all interactions
- **Testing requirements**: Need comprehensive intent test coverage

## Implementation Status

**Date Updated**: October 6, 2025

### GREAT-4A through 4E Completion
- **GREAT-4A**: QueryRouter foundation ✅
- **GREAT-4B**: Monitoring and enforcement ✅
- **GREAT-4C**: Canonical handlers (5 categories) ✅
- **GREAT-4D**: Workflow handlers (8 categories) ✅
- **GREAT-4E**: Complete validation (126 tests, 5 load benchmarks) ✅

### Handler Coverage
**13/13 intent categories implemented (100%)**:
- Canonical handlers: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE
- Workflow handlers: EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, UNKNOWN, QUERY, CONVERSATION

### Test Coverage
- Direct interface: 14 tests (all passing)
- Web interface: 14 tests (all passing)
- Slack interface: 14 tests (all passing)
- CLI interface: 14 tests (all passing)
- Contract tests: 70 tests (performance, accuracy, error, multi-user, bypass)
- **Total**: 126 tests passing

### Performance Metrics (from GREAT-4E load testing)
- Pre-classifier fast path: ~1ms (canonical handlers)
- LLM classification: 2000-3000ms (expected)
- Cache effectiveness: 7.6x speedup
- Cache hit rate: 84.6%
- Sustained throughput: 602,907 req/sec over 5 minutes
- Memory stability: No leaks detected, stable over sustained load

### Production Status
- **Status**: ✅ PRODUCTION READY
- **Deployed**: October 6, 2025
- **Coverage**: 100% of intent categories
- **Quality**: All tests passing, all benchmarks met

## Architecture Validation

### Dual-Path Design Confirmed
Investigation during GREAT-4E confirmed the dual-path architecture is intentional and working correctly:

**Fast Path** (Canonical Handlers):
- Categories: IDENTITY, TEMPORAL, STATUS, PRIORITY, GUIDANCE
- Pre-classifier recognizes patterns instantly
- Routes to canonical handlers in ~1ms
- No workflow overhead needed
- Use case: Simple queries with deterministic responses

**Workflow Path** (Orchestration):
- Categories: EXECUTION, ANALYSIS, SYNTHESIS, STRATEGY, LEARNING, UNKNOWN, QUERY, CONVERSATION
- Requires full LLM classification
- Routes to orchestration workflows
- Takes 2000-3000ms (necessary complexity)
- Use case: Complex operations requiring multi-step orchestration

### Known Issues
**Classifier Accuracy** (GREAT-4F scope):
- LLM mis-classifications cause timeouts (e.g., TEMPORAL mis-classified as QUERY)
- Estimated accuracy: 85-95%
- Solution: Improve classifier prompts and add fallback workflows
- Not blocking: Core architecture validated and working

## Original Implementation Plan

### Phase 1: Basic Classifier (Week 1)
- Keyword-based classification
- Logging for training data
- Integration with existing router

### Phase 2: LLM Enhancement (Week 2)
- Use Claude for classification
- Fallback to keyword approach
- A/B testing for accuracy

### Phase 3: Learning Integration (Week 3)
- Store classifications with outcomes
- Build training dataset
- Implement feedback loop

## Code Location
- Implementation: `services/intent/intent_service.py` (main router)
- Canonical handlers: `services/intent_service/canonical_handlers.py`
- Pre-classifier: `services/intent_service/pre_classifier.py`
- Tests: `tests/intent/` (21 files, 126 tests)
- Integration: All interfaces route through intent classification

## References
- Original vision: May 28, 2025
- Pattern-032: Intent Pattern Catalog
- Issue #96: FEAT-INTENT
- Related: ADR-031 (MVP Redefinition)
- GREAT-4E Completion: October 6, 2025
