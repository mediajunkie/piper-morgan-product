# Canonical Queries Architecture

**Status**: Historical / Superseded by ADR-060 (March 2026)
**Originally Created**: August 23, 2025
**Last Updated**: April 11, 2026

---

## Notice

This document originally described canonical queries as "the foundation of
query handling" — a learning-loop, pattern-sharing, confidence-scoring
architecture intended to be the central routing mechanism for Piper Morgan's
conversational interface.

**That design has been inverted.** After M1's floor-first routing work
(Issue #911) and the April 8, 2026 IDENTITY migration to the conversational
floor (commit `33e6758a`), canonical queries are now the **narrow exception**
rather than the foundation. Most user queries route through the conversational
floor with contextual assembly; canonical handlers run only for operations
that require side effects, database writes, or deterministic fast-path
responses.

**For current routing truth, see**:
- [ADR-060: Floor-First Routing](current/adrs/adr-060-floor-first-routing.md) —
  principle and rationale
- [`docs/guides/canonical-handlers-architecture.md`](../../guides/canonical-handlers-architecture.md) —
  current canonical handler scope
- [`docs/guides/intent-classification-guide.md`](../../guides/intent-classification-guide.md) —
  current classification and routing flow
- `services/intent/intent_service.py` (see `_requires_canonical_handler` and
  `_should_route_to_floor`) — source of truth for routing decisions
- `services/intent_service/canonical_handlers.py` (see `can_handle()`) —
  source of truth for canonical category scope

---

## Queries as Spec (retained as north star)

One idea from the original design remains useful as a north star even
though the implementation has changed: **canonical queries are a compact
expression of user intent.** When you can describe a capability as a small
set of reusable query shapes ("what day is it?", "what's my status?",
"archive this project"), you get a cleaner contract with the rest of the
system than a tangle of endpoint-specific handlers. That framing still
holds — it just no longer implies that canonical handlers should be the
default destination for every query. The floor is now the default; canonical
handlers are the reserved path for queries whose answers are deterministic,
time-sensitive, or side-effecting.

---

## Historical Context

The original August 2025 document described:

- A `QueryLearningLoop` with pattern type classification and confidence
  scoring
- A `CrossFeatureKnowledgeService` for sharing patterns between features
- CLI integration via `IssuesCommand` (triage, status, patterns)
- A learning lifecycle: Pattern Creation → Usage → Improvement → Sharing
- Integration points with a future Code Agent's
  `IssueIntelligenceQueries` / `CanonicalQueryEngine` classes

The learning-loop infrastructure was built and demonstrated, but the
assumption that canonical queries would be the **central** routing
mechanism did not survive contact with user testing. UAT Round 2 (March
2026) showed canned canonical responses scoring poorly on the Colleague
Test (1/3), while floor-generated responses scored 7+. That evidence drove
the inversion documented in ADR-060.

The original full-text document is preserved in git history. If you need it
for archaeological reasons, check commits prior to April 11, 2026 for this
path.

---

## Changelog

- **2026-04-11**: Replaced body with a pointer to ADR-060 and the current
  routing docs. Retained queries-as-spec paragraph as a north-star idea.
- **2025-08-23**: Original document describing canonical queries as the
  foundation of query handling.
</content>
</invoke>
