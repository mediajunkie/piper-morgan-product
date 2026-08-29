# ADR-003: LLM-Based Intent Classification

**Date**: July 8, 2025
**Status**: Proposed
**Deciders**: Principal Architect, Chief of Staff, CTO

## Context

During Claude Code integration, we discovered that Piper Morgan's regex-based intent classifier is too rigid for natural conversation. Users must use specific command patterns rather than natural language.

Current limitations:

- Cannot understand context ("show that again")
- No conversation memory
- Cannot resolve references ("that summary")
- Forces command-like interaction patterns

## Decision

We will enhance the intent classifier to use LLM-based classification with conversation memory, enabling natural conversational interactions while maintaining high accuracy.

## Consequences

### Positive

- Natural conversational flow
- Context-aware understanding
- Better user experience
- Synergy with MCP dynamic capabilities
- Enables multi-turn interactions

### Negative

- Additional LLM API calls (cost)
- Potential latency increase
- More complex implementation
- Risk of intent hallucination

### Neutral

- Requires conversation state management
- Changes interaction patterns
- New testing strategies needed

## Alternatives Considered

1. **Enhance Regex Patterns**: Would not solve context/reference issues
2. **Rule-Based Context**: Too brittle, exponential complexity
3. **Hybrid Forever**: Maintains two systems indefinitely

## Implementation Plan

1. Build hybrid system for testing
2. Implement conversation memory
3. Migrate to full LLM classification
4. Optimize for latency and cost

## Related Decisions

- ADR-002: Claude Code Integration (revealed this need)
- ADR-001: MCP Integration Pilot (potential synergies)

---
*Last Updated: July 09, 2025*

## Revision Log
- **July 09, 2025**: Added vertical resize feature to chat window for improved usability
