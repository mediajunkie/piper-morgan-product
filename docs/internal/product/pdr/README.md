# Product Decision Records (PDRs)

## Overview

This directory contains Product Decision Records (PDRs) that document significant product decisions, their context, rationale, and implications for design and implementation.

**Total PDRs**: 6 records (001-004, 101)

## What is a PDR?

A PDR captures **what** Piper should do and **why**—the product perspective. PDRs complement ADRs (which capture **how** to build it) and UX briefs (which capture **how it should feel**).

| Artifact | Scope | Owner | Question Answered |
|----------|-------|-------|-------------------|
| **PDR** | Product decision | PM / PPM | What should we build? Why? |
| **ADR** | Architecture decision | Chief Architect | How should we build it? |
| **UX Brief** | Design decision | CXO | How should it feel to use? |

## PDR Tiers

PDRs are numbered by tier to indicate scope and foundational importance:

### Tier 00x: Foundational
Core product decisions that shape everything else. These establish patterns, principles, and constraints that downstream decisions must respect.

| PDR | Title | Status | Date |
|-----|-------|--------|------|
| [PDR-001](PDR-001-ftux-as-first-recognition-v3.md) | First Contact is First Recognition | Draft v3 | Jan 4, 2026 |
| [PDR-002](PDR-002-conversational-glue.md) | Conversational Glue | Draft v1 | Jan 4, 2026 |
| &nbsp; | [PDR-002 Appendix: Layer 2 Vision](PDR-002-appendix-layer-2-vision.md) | Appendix | Jan 2026 |
| [PDR-003](PDR-003-entity-concept-model.md) | Entity Concept Model | Approved | Mar 8, 2026 |
| [PDR-004](PDR-004-experience-philosophy.md) | Experience Philosophy | Approved | Mar 22, 2026 |
| [PDR-005](PDR-005-bring-your-own-chat.md) | Bring Your Own Chat — Distribution Model | Approved (v1.0) | Jun 5, 2026 |

### Tier 1xx: Feature/Capability
Major feature decisions that build on foundational PDRs. These define significant capabilities Piper should offer.

| PDR | Title | Status | Date |
|-----|-------|--------|------|
| [PDR-101](PDR-101-multi-entity-conversation.md) | Multi-Entity Conversation Support | Draft v1 | Jan 4, 2026 |

### Tier 2xx: Integration Patterns
*(Reserved for future use)*

Decisions about how Piper integrates with external systems, platforms, and workflows.

### Tier 3xx: Domain-Specific
*(Reserved for future use)*

Decisions specific to particular PM domains, industries, or use cases.

## PDR Lifecycle

| Stage | Description |
|-------|-------------|
| **Draft** | Initial proposal, open for feedback |
| **Review** | Stakeholder feedback being incorporated |
| **Approved** | PM accepts decision as authoritative |
| **Implemented** | Development work complete |
| **Validated** | Success criteria measured |

## Creating New PDRs

### When to Create a PDR

Create a PDR when:
- Making a significant product decision that affects user experience
- Establishing a pattern that other features should follow
- Capturing stakeholder input that shapes product direction
- Documenting the "why" behind a capability

Do NOT create a PDR for:
- Technical implementation details (use ADR)
- Visual/interaction design specifics (use UX brief)
- Bug fixes or minor enhancements (use GitHub issues)

### PDR Template

```markdown
# PDR-XXX: [Title]

**Status**: Draft v1
**Date**: [Date]
**Author**: [Role]
**Stakeholders**: [List]

---

## Decision

[One-paragraph summary of what was decided]

---

## Context

[Why this decision was needed]

---

## User Need

[What problem this solves for users]

---

## Decision Rationale

[Why this approach was chosen]

---

## Alternatives Rejected

[What else was considered and why it was rejected]

---

## Implications

[What this means for CXO, Chief Architect, Implementation]

---

## Success Criteria

[How we'll know this decision was correct]

---

## Open Questions

[What remains to be resolved]

---

## References

[Related documents, research, stakeholder input]

---

## Changelog

[Version history]
```

## Relationship to Other Artifacts

### PDR → ADR Flow
PDRs establish product requirements; ADRs document how to fulfill them.

Example:
- PDR-001 establishes "FTUX must embody recognition pattern"
- ADR would document "UserContextService architecture for recognition"

### PDR → UX Brief Flow
PDRs establish what capability is needed; UX briefs document how it should feel.

Example:
- PDR-002 establishes "contextual capability hints with throttling"
- UX brief would document hint visual design, animation, dismissal patterns

### Cross-PDR Dependencies
PDRs may reference and build on each other:
- PDR-101 (Multi-Entity) references PDR-001 (recognition) and PDR-002 (glue)
- Foundational PDRs (00x) inform Feature PDRs (1xx)

## Navigation

- **[← Back to Documentation](../README.md)**
- **[ADR Index](../adrs/README.md)** - Architecture decisions
- **[Pattern Index](../patterns/README.md)** - Implementation patterns

---

**Last Updated**: March 23, 2026
**Maintained By**: Principal Product Manager
**Purpose**: Directory navigation, PDR index, and creation guidance
