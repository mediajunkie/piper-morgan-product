---
type: methodology
title: TDD and Domain Authority Requirements
valid_from: "2025-09-21"
last_updated: "2025-09-21"
---

# TDD and Domain Authority Requirements

## Domain Authority Principle

- Research findings and domain models take precedence over test convenience
- Tests must adapt to match proven domain design
- Never change domain architecture to match test expectations

## TDD Decision Tree

- If test expects behavior that doesn't exist → Fix implementation
- If test expects interface conflicting with domain → Fix test
- When uncertain → Check services/domain/models.py first

## Non-Negotiable Constraints

- Research-driven designs cannot be compromised for convenience
- Anti-silent-failure properties must be preserved
- Context preservation across async boundaries required

## Implementation Guidelines

### When Tests Conflict with Domain

1. **Check domain models first** - `services/domain/models.py`
2. **Verify research findings** - Look for domain analysis documents
3. **Adapt tests to domain** - Don't change domain for test convenience
4. **Document decisions** - Explain why domain takes precedence

### Domain-Driven Test Design

- Tests should reflect real domain concepts
- Use domain terminology in test names and assertions
- Align test structure with domain boundaries
- Respect domain invariants and business rules

### Research-First Approach

- Domain research findings are authoritative
- Implementation must match proven domain patterns
- Tests validate domain correctness, not convenience
- Architecture decisions based on domain understanding

## Quality Standards

### Test Quality

- Tests must be meaningful to domain experts
- Avoid testing implementation details
- Focus on domain behavior and outcomes
- Use domain language in test descriptions

### Implementation Quality

- Follow domain-driven design principles
- Preserve domain integrity
- Maintain research-backed architectural decisions
- Ensure domain concepts are clearly expressed in code
