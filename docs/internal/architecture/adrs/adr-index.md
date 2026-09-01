# Architectural Decision Records (ADR) Index — DERIVED VIEW

> 🤖 **GENERATED FILE — DO NOT EDIT.** Regenerate with `python3 scripts/derive-adr-index.py`; verify with `--check`. The individual ADR files' own Status lines are the single source of truth; this index is a build artifact (Architectural Review 2026 workstream B4, closes #1455). Per the B3 rule: counts here TRIAGE, they never DISPOSE — check the live document before treating any status as the whole story.

**Total ADR files**: 78 · **Numbering gaps (never filed)**: 067, 068 · **Counts by status**: Accepted: 53 · Proposed: 11 · Dormant (Proposed, unratified): 2 · Superseded: 8 · Other: 4


## Accepted (53)

- [ADR-001: MCP Integration Pilot](adr-001-mcp-integration.md) — Accepted · July 3, 2025
- [ADR-002: Claude Code Integration](adr-002-claude-code-integration.md) — Accepted · July 6, 2025
- [ADR-004: Action Humanizer Integration](adr-004-action-humanizer-integration.md) — Accepted
- [ADR-005: Eliminate Dual Repository Implementations via Pattern #1 Migration](adr-005-eliminate-dual-repository-implementations.md) — Accepted · July 14, 2025
- [ADR-006: Standardize Async Session Management Pattern](adr-006-standardize-async-session-management.md) — Accepted · July 14, 2025
- [ADR-007: Staging Environment Architecture with Docker Compose](adr-007-staging-environment-architecture.md) — Accepted · July 20, 2025
- [ADR-008: MCP Connection Pooling Strategy for Production](adr-008-mcp-connection-pooling-production.md) — Accepted · July 20, 2025
- [ADR-009: Health Monitoring System Design](adr-009-health-monitoring-system.md) — Accepted · July 20, 2025
- [ADR-010: Configuration Access Patterns](adr-010-configuration-patterns.md) — ✅ Implemented (October 2025, Phase 3)
- [ADR-011: Test Infrastructure Hanging Fixes](adr-011-test-infrastructure-hanging-fixes.md) — **Accepted** - 2025-07-30
- [ADR-012: Protocol-Ready JWT Authentication](adr-012-protocol-ready-jwt-authentication.md) — ACCEPTED · 2025-08-10
- [ADR-017: Spatial-MCP Refactoring](adr-017-spatial-mcp.md) — Implemented · August 17, 2025 (Documenting August 12, 2025 decision)
- [ADR-022: Autonomy Experimentation](adr-022-autonomy-experimentation.md) — Accepted · August 17, 2025
- [ADR-023: Test Infrastructure Activation Pattern](adr-023-test-infrastructure-activation.md) — Accepted · August 20, 2025
- [ADR-027: Configuration Architecture - User vs System Separation](adr-027-configuration-architecture-user-vs-system-separation.md) — Accepted · 2025-08-30
- [ADR-029: Domain Service Mediation Architecture](adr-029-domain-service-mediation-architecture.md) — Accepted (September 12, 2025)
- [ADR-030: Configuration Service Centralization](adr-030-configuration-service-centralization.md) — Accepted (September 12, 2025)
- [ADR-031: MVP Redefinition - Core vs Feature Distinction](adr-031-mvp-redefinition.md) — Accepted
- [ADR-032: Intent Classification as Universal Entry Point](adr-032-intent-classification-universal-entry.md) — Accepted & Validated (GREAT-4E Phase 4 - October 6, 2025)
- [ADR-033: Multi-Agent Scripts Deployment](adr-033-multi-agent-deployment.md) — Accepted
- [ADR-034: Plugin Architecture Implementation](adr-034-plugin-architecture.md) — **Implementation Status**: Complete (October 2-4, 2025)
- [ADR-035: The Inchworm Protocol](adr-035-inchworm-protocol.md) — Accepted · September 20, 2025
- [ADR-036: QueryRouter Resurrection Strategy](adr-036-queryrouter-resurrection.md) — ✅ Completed · September 20, 2025 (Planned) | September 22, 2025 (Implemented)
- [ADR-037: Test-Driven Locking Strategy](adr-037-test-driven-locking.md) — Accepted · September 26, 2025
- [ADR-038: Spatial Intelligence Architecture Patterns](adr-038-spatial-intelligence-patterns.md) — Accepted · **AMENDED 2026-07-30 (Amendment A, Arch)** — decision stands; verification claims corrected. Read Amendment A at the foot of this file before citing any operational claim. · September 30, 2025 (Updated: October 1, 2025)
- [ADR-039: Canonical Handler Fast-Path Pattern](adr-039-canonical-handler-pattern.md) — ✅ Approved and Implemented · October 7, 2025
- [ADR-040: Local Database Per Environment Architecture](adr-040-local-database-per-environment.md) — Accepted · 2025-11-01
- [ADR-041: Domain Primitives - Item and List Refactoring](adr-041-domain-primitives-refactoring.md) — ✅ Implemented (November 2025)
- [ADR-042: Mobile Strategy - Progressive Enhancement](adr-042-mobile-strategy-progressive-enhancement.md) — Accepted
- [ADR-043: Application-Layer Stored Procedures Pattern](adr-043-application-layer-stored-procedures.md) — Accepted · November 22, 2025
- [ADR-044: Lightweight RBAC vs Traditional Role-Permission Tables](adr-044-lightweight-rbac-vs-traditional.md) — ✅ Accepted · November 22, 2025
- [ADR-045: Object Model - "Entities Experience Moments in Places"](adr-045-object-model.md) — Accepted · November 28, 2025
- [ADR-050: Conversation-as-Graph Model](adr-050-conversation-as-graph-model.md) — Accepted · January 21, 2026 (Accepted)
- [ADR-051: Unified User Session Context](adr-051-unified-user-session-context.md) — AMENDED — Completed with scope-clarification (Phase 2/3, 2026-05-16) · 2026-01-13 (original) / 2026-05-16 (amendment)
- [ADR-052: Standardize on Tool-Based MCP Implementation](adr-052-tool-based-mcp-standardization.md) — Accepted · October 17, 2025
- [ADR-053: Trust Computation Architecture](adr-053-trust-computation-architecture.md) — ACCEPTED · 2026-01-13
- [ADR-054: Cross-Session Memory Architecture](adr-054-cross-session-memory-architecture.md) — APPROVED · 2026-01-13
- [ADR-055: Object Model Implementation - Core Grammar & Lens Infrastructure](adr-055-object-model-implementation.md) — Accepted (Implemented January 21, 2026) · January 19, 2026
- [ADR-057: CommandRegistry - Unified Command Discovery and Routing](adr-057-command-registry.md) — APPROVED (Phase 3 Implementation In Progress) · 2026-01-22
- [ADR-058: Multi-Tenancy Isolation Architecture](adr-058-multi-tenancy-isolation.md) — APPROVED · 2026-01-30
- [ADR-059: Workflow Dispatcher and Offer System Consolidation](adr-059-workflow-dispatcher-offer-consolidation.md) — APPROVED (2026-03-19, Chief Architect) · 2026-03-19
- [ADR-060: Floor-First Routing Architecture](adr-060-floor-first-routing.md) — Approved · 2026-03-19
- [ADR-061: LLM-Touch Boundary Enforcement — Two-Layer Detection with Floor as De-Facto Ethics Layer](adr-061-llm-touch-boundary-enforcement.md) — **Ratified** v1.0 (PM verbal ratification 2026-05-03); **v1.1 amendment 2026-05-15** (output-side companion shipped per #1017 — see §"Amendment 2026-05-15") · 2026-04-28 (v0.1) → 2026-04-30 (v1.0 — Lead Dev fixes + CEO calibration reframe applied) → 2026-05-03 (verbally ratified) → 2026-05-04 (status block updated) → 2026-05-15 (v1.1 — output-side companion amendment per #1017)
- [ADR-069: Domain Concept Projection Contract — System of Record vs. In-Process Working State](adr-069-domain-concept-projection-contract.md) — **v0.2 (RATIFIED 2026-06-12)** — Lead-Dev-authored from the #1207 implementation; Architect ratified the carve (memo ~19:35 "strong concur") and the artifact (memo ~22:30 "v0.1 clean, ratified"). v0.2 folds in Arch's three optional polish edits (D6 Intent-shape sketch · Source-incidents tracer · D5 negative-pattern made code-explicit). · 2026-06-12
- [ADR-070: MCP-Consumer Connector Architecture](adr-070-mcp-consumer-connector-architecture.md) — v0.1 (filed 2026-06-15) — Architect-authored; PM-ratified direction (2026-06-14: connectors move to MCP-consumer; staying native is "dated and clunky"); gates Lead Dev WS-1..9 decomposition on the RECONNECT sprint (#1220 umbrella + 12 issues). · 2026-06-15
- [ADR-071: User-Auth Anchoring Pattern for Content Stores](adr-071-user-auth-anchoring-pattern.md) — v0.1 (Lead-authored 2026-06-15) — **RATIFIED by Arch 2026-06-15** ("clean fold; every guidance point folded faithfully"; 2 minor cross-refs folded below). Grounded in the #1241 content-anchoring audit (PM-directed systemic flag 2026-06-14; Arch D1 ruling + D1–D7 grounding-confirm 2026-06-15). Companion to **ADR-058** (Multi-Tenancy Isolation) at the *content* altitude — same make-impossible-by-construction shape, one layer down from credentials. · 2026-06-15
- [ADR-072: Skill-Routing Architecture — Fluid Model with Defense-in-Depth](adr-072-skill-routing-architecture.md) — ACCEPTED (v0.2) — D1–D4 Arch-ratified in-lane; **D5 ratified 2026-06-17 with CXO + HOST trust-lens folded** (both aligned: gate Piper-initiated, never user-reaching-for-own; + HOST's consequential-action carve-out + transparency-when-gated) · 2026-06-17
- [ADR-073: No Destructive Git in PM's Main Checkout Working Tree](adr-073-no-destructive-git-in-pm-main-checkout.md) — ACCEPTED — PM-approved 2026-06-27. The operational rule has been in force via the CLAUDE.md ⚠️ HARD RULE callout since 2026-06-21 (`6d1292d09`); this ADR is the formal decision record + rationale for the archive. · 2026-06-27
- [ADR-074: Encryption at Rest Strategy](adr-074-encryption-at-rest-strategy.md) — ACCEPTED (documenting already-shipped work) — written 2026-07-05 (Lead Dev) as part of #358's closure, retroactively recording the design + decisions behind work implemented 2026-06-20 and live-verified on alpha 2026-06-25. No new decision is made here; this is the durable record #358 asked for.
- [ADR-075: Configuration / Personalization Ownership — Per-User Scoping for Instance Config](adr-075-configuration-personalization-ownership.md) — **v0.2 ACCEPTED (2026-07-06)** — Arch-authored; CXO + HOST trust-lens both PASS and folded (OQ-3 fully resolved); cut ACCEPTED per HOST ratification + CXO sign-off. (v0.1 was DRAFT-for-trust-lens.) Grounded in #1366 (PM-caught 2026-07-06: `PIPER.user.md` is a single unscoped instance-level file that leaks PM's personalization + GitHub default-repo to every user on the shared `alpha.pipermorgan.ai` instance). Component A (github default-repo scoping) shipped earlier this session (Lead, `f04cbeea6`/`1784ae017`). **Component B (system-prompt personalization) — IMPLEMENTED, BUILD-ratified, live-verified, and CLOSED** (Lead, #1373, closed 2026-07-07): owner_id-scoped store (`personalization_contexts`, migration `d075persctx`), principal resolution wired into every confirmed request-path caller, seeded neutral-default persona + one-time first-response notice per CXO's OQ-3 spec, D5 enforcement guard. Arch's BUILD ratification (2026-07-07): clean against D1-D5 + OQ-1/2/3, and structurally "impossible-by-construction" for the #1366 leak — the FK-constrained, always-scoped repository methods mean an unscoped read/write can't be expressed, not merely that it's avoided. Live-verified 2026-07-07 against a real local Postgres (direct-service verification, not mocked): distinct-principal scoping, lazy-seeding, and the one-time notice all confirmed against real DB rows. OQ-1 (dedicated store, not `personality_profiles`) and OQ-2 (`default_labels` stays with `ConnectorConfigService`, not a new store) both decided at build time as the ADR reserved. Component C (#1260 mechanism repoint) deferred as a smaller follow-up per D6 — the only open item, tracked separately. Completes the **server-owned-state family**: ADR-070 (per-user connector *bindings*), ADR-071 (per-user content *stores*), **ADR-075 (per-user config/personalization)** — all three now ratified AND implemented. · 2026-07-06
- [ADR-076 — Usage-Cap Enforcement (Alpha Load Backstop)](adr-076-usage-cap-enforcement.md) — ACCEPTED (v0.1, 2026-07-06) — Arch-authored; HOST trust-lens PASS folded; **implemented and closed** (#1370, `01c28848b`, 2026-07-06; BUILD-ratified clean against D1-D6 by Arch 2026-07-07; live-verified 2026-07-07 against a real server + real Redis — rate limit, concurrency cap, and fail-closed all hit their exact documented boundary and response shape) — `web/middleware/usage_cap_middleware.py`, 12 unit tests. Fully closed, no open items.
- [ADR-077 — Routing-Integrity Contract (Action↔Handler Reachability)](adr-077-routing-integrity-contract.md) — ACCEPTED (v0.1, 2026-07-09) — Arch-authored; formalizes the #1283 AC-4 SSOT ruling (2026-07-08) after Lead's static audit + behavioral probe validated the approach. Lead builds the enforcement.
- [ADR-079 — Owner-Scoping Integrity Contract (unscoped reads impossible-by-construction, mechanically enforced)](adr-079-owner-scoping-integrity-contract.md) — **ACCEPTED (v0.1, 2026-07-16)** — Arch-authored, on the integrity authority PM delegated + Lead's confirmation that the #1419 multi-tenancy audit's scope is systemic. Synthesizes already-accepted per-feature owner-scoping decisions into one contract + its mechanical enforcement. **HOST trust-lens welcome** (this is a trust-boundary contract) — informative, not gating, since the constituent decisions are already accepted. **PM retains veto.**

## Proposed (11)

- [ADR-000: Piper Morgan as Meta-Platform Vision](adr-000-meta-platform.md) — Proposed · August 17, 2025
- [ADR-003: LLM-Based Intent Classification](adr-003-intent-classifier-enhancement.md) — Proposed · July 8, 2025
- [ADR-014: Attribution-First Development](adr-014-attribution-first.md) — Proposed · August 17, 2025
- [ADR-015: Wild Claim Verification Protocol](adr-015-wild-claim.md) — Proposed · August 17, 2025
- [ADR-047: Async Event Loop Awareness for Database Connections](adr-047-async-event-loop-awareness.md) — Draft (Pending Chief Architect Review) · December 3, 2025
- [ADR-062: Project-Scope End-to-End Suite — Generalizing ADR-061 Simulation Harness](adr-062-project-scope-e2e-suite.md) — **Phase 0 ADR (scoping)** — v0.1 (drafted 2026-05-16); CEO ratification of proposal direction received 2026-05-15 via Architect decision walkthrough (Item 1); Phase 1+ gated on trigger signals (see §"Phase Sequencing") · 2026-05-16 (v0.1 — Phase 0 scoping ADR per CEO ratification of e2e suite design proposal direction May 15)
- [ADR-063: User-Facing Audit Envelope Read Surface — ADR-061 Companion (Four-Element READ-Side Principle)](adr-063-user-facing-audit-envelope-read-surface.md) — **v0.1 (drafted 2026-05-16)** — pairs with Surface 7 MUX doc (CXO + Comms lane); CEO ratification of paired-deliverable approach received 2026-05-16 via MUX/UI Round 2 ratification (Architect decision walkthrough Item 2) · 2026-05-16 (v0.1 — Phase 2 of MUX/UI Round 2 implementation; companion to #1095's Pattern-071 first fix shipped this morning)
- [ADR-064: Project-Scope Search Index Architecture — Pre-1.0 Commitment for Surface 5](adr-064-project-scope-search-index-architecture.md) — **v0.1 (drafted 2026-05-16)** — pre-1.0 Architect-lane ADR per MUX/UI Round 2 (Surface 5 user-facing search is post-1.0; this ADR commits to the index architecture before 1.0 so new surfaces have known indexing shape) · 2026-05-16 (v0.1 — third ADR in the MUX/UI Round 2 sequence: ADR-062 (e2e suite) → ADR-063 (audit-envelope read) → ADR-064 (search index))
- [ADR-065: Canonical Context-Package Format (BYOC / Plugin-Packaged)](adr-065-canonical-context-package-format.md) — v0.1 (filed 2026-06-06) — Architect-authored; companion to PDR-005 v1.0 §Open question 6; in-house material per Klatch-pause Evolution-section convention (HOST 2026-05-24). Three-fire bursty-lane drafted (Fire 1 skeleton + plugin-packaging framing; Fire 2 §Decision D1-D6 substantive content; Fire 3 polish + §Consequences refinement + v0.1 final). · 2026-06-06
- [ADR-066: Packaging-Layer Abstraction (BYOC Plugin Per-Host Deployment)](adr-066-packaging-layer-abstraction.md) — v0.2 (amended 2026-06-14) — Architect-authored; companion to PDR-005 v1.0 §Open question 7; gated by ADR-065 v0.1 ✅. · 2026-06-06
- [ADR-078 — Session-Activity Ledger + Pre-Classifier Reference Resolution (the #1394 cross-turn continuity architecture)](adr-078-session-activity-ledger-and-pre-classifier-reference-resolution.md) — **ACCEPTED (v0.2, 2026-07-14)** — Arch-accepted on the integrity authority PM delegated (2026-07-12, "maintain the architectural integrity") + greenlit authorship. Both ACCEPT gates cleared: (1) **Lead's ledger-feasibility read — DONE** (2026-07-14; it *corrected* D1 from association-over-existing to a dedicated additive `session_activity` ledger — see OQ-1); (2) **pre-classifier direction (D2/D4) — Lead CONCURS + HOST trust-lens PASS** (2026-07-13). **PM retains veto** — flagged to PM on acceptance (this is the architecture call PM asked me to hold; surfaced, not silently flipped). Lead is cleared to build B4 against the D1 `session_activity` contract. *(v0.1 PROPOSED 2026-07-12; HOST D1a folded 2026-07-13; D1 corrected + accepted 2026-07-14. **B4 built + Arch-ratified 2026-07-15** — SessionActivityDB + owner-scoped reader + central observer + recall, suite-green; B3 pre-classifier resolution pending, needs new ADR-077 D5 rows.)*

## Dormant (Proposed, unratified) (2)

- [ADR-046: Moment.type Agent Architecture](adr-046-moment-type-agent-architecture.md) — Proposed — DORMANT since 2025-12 (status annotated 2026-08-29) · November 30, 2025 (Updated December 1, 2025)
- [ADR-056: Consciousness Expression Patterns](adr-056-consciousness-expression-patterns.md) — Proposed — DORMANT since 2026-01 (status annotated 2026-08-29) · January 21, 2026

## Superseded (8)

- [ADR-013: MCP + Spatial Intelligence Integration Pattern](adr-013-mcp-spatial-integration-pattern.md) — Superseded/Deprecated (via notice heading — no formal Status line)
- [ADR-016: Ambiguity-Driven Architecture with Chain-of-Draft Integration](adr-016-ambiguity-driven.md) — Superseded (status corrected 2026-08-29) · August 17, 2025
- [ADR-018: Server Functionality Architecture](adr-018-server-functionality.md) — Superseded (status corrected 2026-08-29; prior status 'Implemented' was inaccurate) · August 17, 2025
- [ADR-019: Full Orchestration Commitment](adr-019-orchestration-commitment.md) — Superseded (status corrected 2026-08-29) · August 17, 2025
- [ADR-020: Protocol Development Investment](adr-020-protocol-investment.md) — Superseded — never executed (status corrected 2026-08-29) · August 17, 2025
- [ADR-021: Multi-Federation Achievement](adr-021-multi-federation.md) — Superseded — implementation claims disavowed (status corrected 2026-08-29) · August 17, 2025
- [ADR-024: Persistent Context Foundation Architecture](adr-024-persistent-context-architecture.md) — Superseded by ADR-075 (status corrected 2026-08-29 — see Status correction at end of file) · August 20, 2025
- [ADR-028: Three-Tier Verification Pyramid Architecture](adr-028-verification-pyramid.md) — SUPERSEDED (2026-07-26 — Arch fix-or-delete ruling 2026-07-25, decisions.log ~23:35 PT; PM-flagged per the #1322-supersession precedent). The runtime `methodology/` package this ADR specified was deleted as a zero-importer dead island; the pyramid's ideas live on as the cohort's prose discipline (evidence-required, verify-first, completion-theater pattern family, the #1452 CI-arbitrated gate). Design lineage: `docs/internal/architecture/current/design-record-methodology-as-code-2025.md`. · September 2, 2025

## Other (4)

- [ADR-025: Unified Session Management Architecture](adr-025-unified-session-management.md) — (no Status line — fix the ADR, not this index)
- [ADR-026: Notion Client Migration to Official Library](adr-026-notion-client-migration.md) — (no Status line — fix the ADR, not this index)
- [ADR-048: ServiceContainer Lifecycle Management](adr-048-service-container-lifecycle.md) — (no Status line — fix the ADR, not this index)
- [ADR-049: Conversational State and Hierarchical Intent Architecture](adr-049-conversational-state-hierarchical-intent.md) — (no Status line — fix the ADR, not this index)
