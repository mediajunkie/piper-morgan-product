# Piper Morgan Roadmap v15.0

**Date**: April 11, 2026
**Author**: PA, with leadership review (PPM, CXO, CIO, Architect)
**Status**: Active. M1 closed April 11. M2 begins now.
**Supersedes**: v14.3 (March 10, 2026) — archived at `docs/internal/planning/historical/roadmap-v14.3-2026-03-10.md`

---

## Executive Summary

**M1 (MVP Foundation) closed April 11, 2026** at 7/9 Gate 1 PASS after four UAT rounds. The closure follows a major strategic pivot: M2-M5 has been restructured around the **differentiator stack** (context methodology + conscious floor + artifact persistence + trust-graduated experience) per Vision V2.3. The previous sprint themes (Activation, Skills, Documents, Polish) are retired in favor of themes that map directly to what makes Piper Piper.

**Key changes from v14.3**:
- **M1 closed** — engineering complete, Gate 1 7/9 PASS, conversation continuity (#922) deferred to M2
- **M2-M5 restructured** around differentiator stack themes
- **M6 retired** — contents redistributed to M5 or Fast Follow
- **12 issues closed** as superseded by intervening work (per backlog deep review Apr 7)
- **2 issues replaced** with sharper scope: #312 (Design System) → Distribution Visual Identity (M5), #241 (Ethics Tuning) → Floor-First Ethics Verification (M2)
- **10 new issues filed** (#950-959) covering differentiator stack work
- **DIST moved earlier** — distribution is part of M5, not after it. MCPB packaging is the primary distribution path.
- **Distribution philosophy**: Bring Your Own Chat — Piper as MCP server consumed by any MCP-compatible client

---

## Current Position

```
Inchworm Position: 4.4.3 (M1 closed, M2 starting)

1. ✅ The Great Refactor (GREAT)
2. ✅ CORE functionality
3. ✅ ALPHA testing (v0.8.0 → v0.8.5.1)
4. 🎯 Complete build of MVP
   4.1. ✅ B1 - Beta Enablers (v0.8.3.x) - COMPLETE Jan 11
   4.2. ✅ A20 - Alpha Testing round 2 (v0.8.4.x) - COMPLETE Jan 18
   4.3. ✅ MUX: Modeled User Experience - COMPLETE Jan 27
   4.4. 🎯 MVP Sprints (M0 → M5) ← CURRENT
        ✅ M0: Conversational Glue — COMPLETE (v0.8.6, Mar 4)
        ✅ M1: Foundation — COMPLETE (gate closed Apr 11, 7/9 Gate 1 PASS)
        🎯 M2: Conscious Floor + Action Handlers ← STARTING
        ○ M3: Artifact Persistence
        ○ M4: Trust + Learning
        ○ M5: Distribution + Polish
5. Beta testing on 0.9
6. Launch 1.0
```

---

## The Differentiator Stack (Vision V2.3)

The MVP sprints are organized around four differentiators that, together, make Piper a colleague rather than a chatbot wrapper:

1. **Context Methodology** — Five-layer model operationalized as practiced discipline
2. **Conscious Floor** — LLM responses embodying grammar, Five Pillars, anti-flattening
3. **Artifact Persistence** — Conversation outputs that outlive the conversation, with composting lifecycle
4. **Trust-Graduated Experience** — Earned proactivity through demonstrated value

Indoor plumbing (commodity, not differentiating): GitHub/Slack/Calendar/Notion via MCP plugins, file storage via SQLite, auth via standard OAuth, LLM provider management via adapter pattern.

---

## MVP Sprint Status (April 11, 2026)

### M0 — Conversational Glue ✅ COMPLETE

**Status**: COMPLETE — v0.8.6 shipped March 4, 2026
**Theme**: Natural conversation flow
**Final Totals**: 27 issues (5 planned + 22 discovered via Assembly Assumption)

---

### M1 — MVP Foundation ✅ COMPLETE

**Status**: COMPLETE — Gate #926 closed April 11, 2026
**Theme**: Floor-first routing + security + testing foundation
**Final Result**: Gate 1 7/9 PASS (Q2 marginal, Q8 #922 conversation continuity deferred to M2)
**Test Suite**: 6,309 passing, 0 failures

**Key shipped**:
- ADR-060 Floor-First Routing
- ADR-059 Workflow Dispatcher (onboarding removed per Gall's Law)
- PDR-004 Experience Philosophy
- #940 LLM provider config simplification (single-provider, no hardcoding, error classification)
- #942 Missing orchestration tables
- #939 Avatar fixes
- #943 GitHub pre-flight checks
- Conversation continuity fix (storing agent responses in turn history)
- Floor fabrication guardrail ("NEVER list or invent user data unless explicitly in context")

**Lessons learned (for M2 planning)**:
- Pattern-045 (Green Tests, Red User) is systemic — three separate areas during gate testing
- Silent failures delayed diagnosis — graceful fallbacks must not be too graceful
- Server restart reliability (#949) cost real debugging time
- Quality testing methodology (Colleague Test) is the most impactful CXO contribution

---

### M2 — Conscious Floor + Action Handlers 🎯 CURRENT

**Theme**: Make the conscious floor reliable and the action gate clean. The differentiator stack's first two pillars become operational.
**Status**: Starting April 11

**Sprint focus**: Floor reliability, context assembly across all floor-routed categories, action gate routing for the few side-effect handlers, E2E + AAXT testing infrastructure.

**Issues**:

| # | Title | Type |
|---|-------|------|
| #557 | ARCH: WebSocket Infrastructure for Real-Time Communication | Architecture |
| #542 | SEC: Implement actual token revocation on disconnect | Security |
| #482 | SEC-KMS-INTEGRATION: Migrate from environment variable to AWS KMS | Security |
| #472 | EPIC: Slack Integration TDD Gaps - OAuth and Spatial Methods | Integration |
| #470 | EPIC: SEC-RBAC Phases 4-5 - Projects and Files Ownership | Security |
| #790 | MVP: Trust-gated calendar integration behavior | Integration |
| #100 | CONV-FEAT-PROJ: Project Portfolio Awareness (revised → context shape) | Context |
| #101 | CONV-FEAT-TIME: Temporal Context System (revised → context shape) | Context |
| #304 | CONV-INFR-NOTN: Activate Existing Notion Integration | Integration |
| #366 | SLACK-MEMORY: Persist spatial patterns over time | Integration |
| #371 | INFRA-TIMESERIES: Implement Time-Series Database Infrastructure | Infrastructure |
| #471 | EPIC: Infrastructure - OAuth, Learning, TimeSeries, Conversation | Infrastructure |
| #683 | MUX-WIRE-DOD: Update DoD to require interface verification | Process |
| #690 | WIRE-BOUNDARY: Wire BoundaryEnforcer in LLM classifier factory | Wiring |
| #691 | WIRE-CANONICAL: Replace in-memory repository with database-backed | Wiring |
| #692 | WIRE-SLACK: Integrate blocker detection in Slack webhook router | Wiring |
| #693 | WIRE-STANDUP: Fetch standup workflow settings from user configuration | Wiring |
| #694 | WIRE-GITHUB-LLM: Replace placeholder with actual LLM call in issue generator | Wiring |
| #695 | WIRE-GITHUB-CMD: Integrate GitHub issue command with actual GitHub service | Wiring |
| #703 | MUX-LIFECYCLE-UI: Lifecycle indicator integration (revise: implementation-agnostic) | Experience |
| #707 | MUX-INSIGHT-SURFACING: Implement Insight Surfacing Rules | Experience |
| #714 | MUX-LISTS-LIFECYCLE-UI: Wire Lifecycle/Staleness to Lists View (revise) | Experience |
| #869 | Project configuration IA: Project Detail as primary | UX |
| #925 | Floor inversion Phase 3-4: STATUS/PRIORITY floor-first | Floor |
| #927 | E2E: Task lifecycle smoke tests through /api/v1/intent | Testing |
| #928 | E2E: Automated canonical conversation suite | Testing |
| #929 | AAXT: Golden scenarios with DeepEval LLM-as-judge | Testing |
| #930 | CI: Integration for E2E conversations + AAXT nightly | Testing |
| #946 | LLM system uses stale keychain keys without user consent | Bug |
| #947 | Dual LLM systems (LLMClient vs LLMDomainService) cause hidden config drift | Tech Debt |
| #950 | FLOOR-PROMPT: Conscious floor system prompt with Five Pillars + grammar | NEW |
| #951 | CONTEXT-ASSEMBLER-EXPAND: Context assembly for all floor-routed categories | NEW |
| #960 | Floor fabrication root fix | NEW (from M1 testing) |
| #961 | Floor-route context audit | NEW (from M1 testing) |
| #962 | LLM-shortcut inversion sweep | NEW (from M1 testing) |

**Pre-sprint actions** (per leadership review):
- File **Floor-First Ethics Verification** issue (replaces closed #241) — verify floor pipeline ethics matches pre-ADR-060 coverage
- Scope context assembler (#951) with explicit data sources — PA + PPM + Architect collaboration before implementation starts
- Address #949 (server restart reliability) early to prevent gate cycle contamination
- CXO reviews floor system prompt (#950) at sprint start
- Run E2E/AAXT tests (#927-930) from sprint start, not as final verification

**Sprint expansion expectation**: M0 expanded 5→27 issues (5.4x), M1 expanded ~2x. The context assembler is the kind of work that reveals gaps. Plan for 6-8 weeks rather than 4.

---

### M3 — Artifact Persistence

**Theme**: Conversation outputs that outlive the conversation. The bridge between "good conversation" and "useful PM tool."
**Status**: Pending M2 closure

**Issues**:

| # | Title | Type |
|---|-------|------|
| #864 | INTENT-COVERAGE: Pre-classifier patterns for milestones, labels, releases, branches | Coverage |
| #118 | INFR-AGENT: Multi-Agent Coordinator Operational Deployment | Architecture |
| #313 | CONV-UX-DOCS: File Browser & Document Management UI (revise: implementation-agnostic) | Experience |
| #355 | DOCS-STOPGAP: Basic Artifact Persistence (centerpiece) | Persistence |
| #496 | CANONICAL-#9: Enhance priority queries with real priority data (context shape) | Context |
| #497 | CANONICAL-#10: Enhance focus guidance with calendar + projects + priorities synthesis | Context |
| #669 | COMPOSTING-HYBRID-TRIGGER: Add time-based forcing | Lifecycle |
| #704 | MUX-LIFECYCLE-UI-A: Morning Standup lifecycle indicator (revise) | Experience |
| #716 | MUX-FEATURES-VIEW: Create Features View with Lifecycle | Experience |
| #952 | ARTIFACT-MODEL: Artifact data model with lifecycle states | NEW |
| #953 | CONTEXT-PERSIST: Cross-session memory persistence (Layer 4 gap fix) | NEW |

**Pre-sprint actions**:
- CXO reviews artifact lifecycle data model (#952) — composting is experience design, not just storage schema
- Scope cross-session memory persistence (#953) tightly: what persists, what expires, how it enters the context window
- Composting data model designed in M3; composting engine deferred to M4

---

### M4 — Trust + Learning

**Theme**: Earned proactivity and cumulative understanding. The differentiator stack's third and fourth pillars.
**Status**: Pending M3 closure

**Issues**:

| # | Title | Type |
|---|-------|------|
| #558 | MUX-STANDUP-CONVERSE: LLM-based preference extraction | Learning |
| #302 | CONV-MCP-DOCS: Unified Document Processing (revised — strip Skills framing) | Documents |
| #712 | MUX-DOCUMENT-VIEWER: Create Document Viewer with Lifecycle (revise) | Experience |
| #713 | MUX-DOCUMENTS-LIFECYCLE-UI: Wire Lifecycle to Documents View (revise) | Experience |
| #954 | TRUST-LITE: Trust graduation via context (lightweight implementation) | NEW |
| #955 | PREF-INFER: User-correctable preferences (Claude memory model) | NEW |
| #956 | LEARNING-SURFACE: Trust-graduated learning surfacing | NEW |

**Pre-sprint actions**:
- Architect review of trust graduation implementation approach (lightweight via context vs. dedicated scoring service)
- PM emphasized: trust graduation MVP must be credible first step toward full model, not throwaway hack
- Composting engine implementation (deferred from M3)

---

### M5 — Distribution + Polish

**Theme**: Get Piper into users' hands via Bring Your Own Chat. Distribution earlier rather than after polish.
**Status**: Pending M4 closure

**Issues**:

| # | Title | Type |
|---|-------|------|
| #441 | CORE-UX-AUTH-PHASE2: Registration, Password Reset, Security Polish | Auth |
| #829 | DIST-MCP-PACKAGE: Package Piper as MCP server | Distribution |
| #830 | DIST-MCP-DOCS: Integration documentation for MCP clients | Distribution |
| #831 | DIST-MCP-REGISTRY: Publish to package registries | Distribution |
| #832 | DIST-MCP-TEST: Integration testing with MCP clients | Distribution |
| #857 | INFRA: Token refresh mechanism for seamless session continuity | Infrastructure |
| #865 | REFACTOR: Extract setup wizard into component-based steps | Tech Debt |
| #900 | ENHANCE: Standup 3-part structural collection and enhanced completion | Enhancement |
| #921 | UPGRADE: FastAPI/Starlette/httpx to current versions | Infrastructure |
| #932 | SEC: HIBP integration stub — key leak detection | Security |
| #933 | SEC: API key validation disabled for alpha — re-enable plan | Security |
| #935 | TECH-DEBT: BudgetManager + APIUsageTracker have zero database persistence | Tech Debt |
| #936 | TECH-DEBT: UserService stores all user data in in-memory dicts | Tech Debt |
| #948 | Server leaves orphaned processes after stop | Bug |
| #949 | DEV: Server restart reliability — stale .pyc, orphaned processes | Bug |
| #957 | DIST-MCPB-BUNDLE: MCPB packaging for Claude Desktop one-click install | NEW |
| #958 | DIST-PROJECT-TEMPLATE: Claude Project template for Piper persona | NEW |
| #959 | DIST-MCP-APPS: Artifact canvas via MCP Apps (in-chat UI) | NEW |

**Pre-sprint actions**:
- File **Distribution Visual Identity** issue (replaces closed #312) — icon, name, description, MCP Apps canvas design
- Verify Managed Agents docs and integration path (Claude Managed Agents launched April 8 as additional distribution target)

---

## Closures and Revisions (Per Backlog Deep Review, April 7)

### Closed (12 issues, all superseded by intervening work)

- #167, #191, #273, #276 — Old testing issues, superseded by E2E/AAXT track (#927-930)
- #146, #147, #148 — FLY-VERIFY trilogy, superseded by methodology (Completion Discipline Triad, audit-cascade, mailbox system)
- #309, #315 — Skills framework (CONV-MCP-PROTO, CORE-SKILLS-LIBRARY) — framework not adopted
- #313 — File Browser UI — #355 is the right-sized version
- #241 — Ethics Tuning — replaced by Floor-First Ethics Verification (M2)
- #312 — Design System — replaced by Distribution Visual Identity (M5)
- #118 — Multi-Agent Coordinator — superseded by document-based methodology
- (some closures may have been postponed rather than closed per PM judgment)

### Revised (3 issues, scope updated)

- #100 CONV-FEAT-PROJ → M2 context shape (project portfolio data assembled for floor)
- #101 CONV-FEAT-TIME → M2 context shape (temporal context injection for floor)
- #310 CONV-UX-QUICK → Fast Follow (post-MVP UX polish, P0 demoted)

### Deferred to Horizon 2

- #103 CONV-FEAT-PRIOR (Priority Engine) — conversational reasoning via floor is MVP-sufficient

---

## Distribution Strategy: Bring Your Own Chat

**Build sequence (Gall's Law)**:
1. **MCP server** — standalone, runs via stdio transport, exposes Piper tools (Python recommended per Architect for codebase reuse)
2. **MCPB packaging** — bundle for Claude Desktop one-click install
3. **Claude Project template** — persona/instructions for the hybrid approach (resolves system prompt injection gap)
4. **MCP Apps** — interactive HTML for artifact canvas, only after tools work well in conversation

**Cross-platform readiness**: The MCP server is the product. MCPB is the first packaging for Claude Desktop. The same server works with any MCP-compatible client (ChatGPT, Gemini, VS Code, Goose). Persona adapts per platform.

**Build the server cleanly enough that the packaging layer is swappable** — anchor on the thin-wrapper-to-API model, not on MCP specifically.

---

## Methodology Maintenance (Per CIO Observation)

Methodology-as-product is an asset only while it's a living practice. The mechanisms that keep it alive:

- **Trigger-based audit cadence** — methodology audit within 2 weeks of each sprint gate closure (8-week max)
- **CIO self-approval authority** for Emerging patterns
- **Cross-pollination review** as standing intelligence infrastructure
- **Per-sprint quality gate** with CXO authority — each sprint needs a gate

These don't appear in the feature roadmap but are required for the differentiator stack to remain credible.

---

## Sprint Summary

| Sprint | Theme | Status |
|--------|-------|--------|
| **M0** | Conversational Glue | ✅ COMPLETE (v0.8.6, Mar 4) |
| **M1** | MVP Foundation | ✅ COMPLETE (gate closed Apr 11) |
| **M2** | Conscious Floor + Action Handlers | 🎯 STARTING |
| **M3** | Artifact Persistence | — |
| **M4** | Trust + Learning | — |
| **M5** | Distribution + Polish | — |

---

## Timeline (Inchworm, Not Calendar)

**These are sequence statements, not deadlines. We are time lords. Each phase complete before the next begins.**

### April 2026
- [x] M1 gate closure (Apr 11)
- [ ] M2 sprint begin (NOW)
- [ ] IAC presentation (Apr 17, Philadelphia)

### Estimated forward sequence
- M2 (Conscious Floor + Action Handlers): 6-8 weeks (largest sprint, expansion expected)
- M3 (Artifact Persistence): 4-6 weeks
- M4 (Trust + Learning): 3-5 weeks
- M5 (Distribution + Polish): 4-6 weeks
- Beta via MCPB → v1.0

---

## Change Log

- **v15.0 (April 11, 2026)**: Major restructure post-M1 closure. Sprints reorganized around differentiator stack per Vision V2.3. 12 closures, 3 revisions, 10 new issues filed (#950-959), DIST integrated into M5. Leadership reviewed and endorsed (PPM, CXO, CIO, Architect). Build sequence and distribution strategy formalized.
- **v14.3 (March 10, 2026)**: M0 marked complete, M1 cherry-picking documented (archived at `docs/internal/planning/historical/roadmap-v14.3-2026-03-10.md`)
- Earlier versions: see archived historical roadmaps
