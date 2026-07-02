# Architecture Decision Records (ADRs)

## Overview

This directory contains Architecture Decision Records (ADRs) that document significant architectural decisions, their context, rationale, and consequences.

**Total ADRs**: 74 records (000-073)

## Recent ADRs

- **[ADR-073: No Destructive Git in PM Main Checkout](adr-073-no-destructive-git-in-pm-main-checkout.md)** (Jun 2026) - Prohibition on destructive git in PM's main checkout (pm-work-safety)
- **[ADR-072: Skill-Routing Architecture](adr-072-skill-routing-architecture.md)** (Jun 2026) - Procedural skills as routing targets (ACCEPTED)
- **[ADR-071: Connector Registration Pattern](adr-071-connector-registration-pattern.md)** (Jun 2026) - Connector registration and configuration patterns
- **[ADR-070: MCP Connector Architecture](adr-070-mcp-connector-architecture.md)** (Jun 2026) - MCP server integration as first-class connectors
- **[ADR-060: Floor-First Routing](adr-060-floor-first-routing.md)** (Mar 2026) - Invert routing: floor handles everything, handlers prove specificity
- **[ADR-059: Workflow Dispatcher & Offer Consolidation](adr-059-workflow-dispatcher-offer-consolidation.md)** (Mar 2026) - Unified dispatch replacing per-handler workflow management
- **[ADR-058: Multi-Tenancy Isolation](adr-058-multi-tenancy-isolation.md)** (Mar 2026) - User data isolation patterns

- **[ADR-057: CommandRegistry - Unified Command Discovery](adr-057-command-registry.md)** (Jan 2026) - Central registry for command parity across interfaces (#551)
- **[ADR-056: Consciousness Expression Patterns](adr-056-consciousness-expression-patterns.md)** (Jan 2026) - Template-based personality consistency
- **[ADR-055: Object Model Implementation](adr-055-object-model-implementation.md)** (Jan 2026) - Domain model dataclass patterns
- **[ADR-054: Cross-Session Memory Architecture](adr-054-cross-session-memory-architecture.md)** (Jan 2026) - Three-layer context persistence from PDR-002
- **[ADR-053: Trust Computation Architecture](adr-053-trust-computation-architecture.md)** (Jan 2026) - Trust gradient model from PDR-002
- **[ADR-052: Tool-Based MCP Standardization](adr-052-tool-based-mcp-standardization.md)** (Oct 2025, updated Jan 2026) - MCP implementation pattern standardization
- **[ADR-051: Unified User Session Context](adr-051-unified-user-session-context.md)** (Jan 2026) - User context unification
- **[ADR-050: Conversation-as-Graph Model](adr-050-conversation-as-graph-model.md)** (Jan 2026) - Multi-party conversation modeling
- **[ADR-049: Conversational State and Hierarchical Intent](adr-049-conversational-state-hierarchical-intent.md)** (Jan 2026) - Multi-turn conversation architecture
- **[ADR-048: ServiceContainer Lifecycle Management](adr-048-service-container-lifecycle.md)** (Jan 2026) - Service container singleton pattern
- **[ADR-047: Async Event Loop Awareness](adr-047-async-event-loop-awareness.md)** (Dec 2025) - Database connection event loop handling
- **[ADR-046: Moment.type Agent Architecture](adr-046-moment-type-agent-architecture.md)** (Nov 2025) - Typed input decomposition and specialized agent routing

## ADR Categories

ADRs are organized by decision domain:
- **Platform & Integration** (MCP, Claude Code, spatial intelligence)
- **Infrastructure** (staging, monitoring, configuration)
- **Security & Auth** (JWT, authentication patterns)
- **Development Process** (testing, session management)
- **Product Strategy** (mobile, features, prioritization)

## Creating New ADRs

See [adr-000-meta-platform.md](adr-000-meta-platform.md) for the standard ADR template and decision-making framework.

## How to read this catalog (citation framework)

Added 2026-04-27 after a code-side citation audit revealed that *zero code citations does not equal "decorative ADR."* Future Architects (and reviewers of this catalog) should classify each ADR along two independent dimensions:

| Status | Code citations | What it means |
|---|---|---|
| **Load-bearing — interface** | ≥5 in code | The ADR documents an active, named API or pattern that engineers grep for and cite in code (e.g., ADR-059 Workflow Dispatcher at 53 citations, ADR-053 Trust at 39, ADR-013 Spatial at 33). When the code interface changes, the ADR must change. |
| **Load-bearing — decision** | Often 0–2 in code, but high session-log/discussion citations | The ADR documents a decision so embedded in the architecture that the code *is* the ADR — there's nothing to grep because the logic flow encodes the choice (canonical example: ADR-060 Floor-First Routing — most-discussed ADR in session logs, zero code citations). When the underlying *decision* is revisited, the ADR must change; otherwise it stays stable. |
| **Internalized** | 0 in code, low session-log presence | The ADR documents a foundational pattern that's *followed implicitly* (e.g., Repository Pattern, Service Layer). Engineers don't cite it because it's the default; they only deviate with justification. Stable; archival. |
| **Archival** | 0 in code, 0 active discussion | The ADR documented a one-time decision that has fully landed and no longer needs reference (canonical examples: ADR-006 Async Sessions, ADR-025 Unified Session Management, ADR-028 Verification Pyramid). The work is *done*; the architecture absorbed the change. Stable; historical record only. |
| **Genuinely decorative** | 0 in code, 0 active discussion, *and* the decision was never executed or has been silently superseded | These are the ADRs worth retiring or annotating as superseded. Distinct from Archival because the work *didn't* land. |

**Why this framework matters**:

Counting code citations is a *necessary but not sufficient* signal of an ADR's load-bearing status. The CIO M1 methodology audit (Apr 17, 2026) flagged ADR-060 as the most-cited ADR in session logs (26 files); a separate code audit (Apr 27) found ADR-060 has zero code citations. Both data points are correct; they describe different things.

When auditing the catalog for staleness or relevance:
- **Don't retire ADRs based on zero code citations alone.** Check whether they're Archival (work landed, no further reference needed), Internalized (followed implicitly), or Decision-load-bearing (referenced in conversations, not code).
- **Do retire ADRs that are Genuinely Decorative.** These are the candidates for explicit deprecation or supersession.

This framework also applies to the [Pattern Index](../patterns/README.md) and the [PDR catalog](../../product/pdr/) — same code-vs-discussion-vs-internalized distinction.

## Navigation

- **[← Back to Current](../README.md)**
- **[📚 Documentation Home](../../README.md)**
- **[Pattern Index](../patterns/README.md)** - Related architectural patterns

---

**Last Updated**: April 27, 2026 (citation framework added)
**Maintained By**: Documentation Team + Chief Architect (catalog meta-doc)
**Purpose**: Directory navigation, content overview, and citation-status framework
