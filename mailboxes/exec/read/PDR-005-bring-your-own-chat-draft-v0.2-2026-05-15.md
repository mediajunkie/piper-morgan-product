# PDR-005 (DRAFT v0.2): Bring Your Own Chat — Distribution Model

**Status**: **DRAFT v0.2 — Architect feasibility check absorbed; cohort iteration ongoing**
**Author**: PPM
**Date**: 2026-05-15 (v0.2 supersedes v0.1 filed earlier today)
**Tier**: Foundational (PDR-005, alongside PDRs 001-004) — pending PM confirmation
**Supersedes**: None (new PDR; codifies Vision V2.3 §"Bring Your Own Chat")
**Related**: PDR-001 (FTUX), PDR-004 (Experience Philosophy), ADR-059 (Workflow Dispatcher), ADR-060 (Floor-First Routing), ADR-061 (LLM-touch boundary enforcement), Vision V2.3 §BYOC + Pillar 7
**Predecessor flag**: PPM Apr 25 handoff §1 + Agent 360 §8.3

---

## v0.2 changelog (vs. v0.1, ~30 min ago)

- **§Consequences for architecture** filled with Architect's feasibility-check substance (was `[INPUT PENDING: Architect]`)
- **§Decision** refined per Architect's "commit to mechanisms, not implementations" framing — mechanism set named explicitly as new sub-section
- **§Open questions** updated with Architect's four explicit-open questions
- **New §PDR commitments to AVOID** added per Architect recommendation
- **§Audit trail** updated with Architect feasibility-check memo (May 15)

---

## Context

Vision V2.3 made BYOC canonical strategic direction (Apr 11, 2026). Vision-level treatment doesn't substitute for PDR-level codification: vision answers "where are we going"; PDRs answer "what must we build and why" with decision-rule specificity downstream ADRs can refer back to.

**Cross-project convergence**: PA May 10 scan: Klatch + Piper Morgan independently arrived at "products as services for agents" within 48 hours of each other. Convergent evolution under common substrate pressure (Anthropic Managed Agents, SDK compaction-helper deprecation).

**Architecture has been quietly preparing for it**: Architect May 15 feasibility check verdict — "BYOC isn't a leap; it's the next natural step." Five structural decisions over 18 months (domain layer separation, ethics floor at universal entry point, audit_transparency Phase 2, intent classification + workflow dispatch, repository pattern + RequestContext) produced a codebase where BYOC is mostly packaging + targeted refactors.

---

## Decision

PDR-005 binds Piper Morgan to *mechanisms* downstream work designs against — not specific implementations that pre-empt design choices PM doesn't yet have enough information to make.

### Core decision rule

**[DECISION: (b) — primary MCP delivery + thin bespoke UI for the discrete surfaces chat cannot adequately support]**

Per Apr 26 scoping outline's three framings (a/b/c). The honest commitment is (b): **MCP primary + thin web UI bound to the 5 1.0-required MUX surfaces** identified in today's MUX/UI cohort scoping. The "thin" qualifier is load-bearing: anything that *can* live in chat *must* live in chat; web UI exists only for the explicit cases where it cannot.

### The mechanism set (Architect framing — "commit to mechanisms, not implementations")

PDR-005 commits to these mechanisms; specific implementations land in subsequent ADRs.

1. **Persona-template parameterization** — `persona_id` registry pattern, sibling to existing `task_type` registry. Same backend supports multiple per-host configurations. Per-host *content* demand-gated post-1.0; the *mechanism* lands in 1.0.
2. **MCP-server packaging alongside FastAPI** — both surfaces consume same domain layer; MCP server in `services/mcp/server/`. First variant: MCP/Claude Desktop. Other variants (ChatGPT custom GPT, Slack app, etc.) demand-gated.
3. **RequestContext-based auth abstraction** — completes #1015 Phase 4 migration; accepts JWT (FastAPI path) or host-provided MCP context.
4. **Audit envelope `host_id` field** — small schema addition for future-extensibility; cross-host audit semantic (unified vs. per-host) deferred to follow-up ADR with HOST + CEO input.
5. **Context-package format negotiated with sibling projects** — Klatch Daedalus alignment per Apr 11 cross-pollination brief + today's PPM-to-Architect request; ADR work happens after alignment.

### Persona portability scope

**[DECISION: server-invariant persona core + per-client adapter templates; consistency contract = "same Piper"]**

Server holds persona core (capabilities, posture, ethics commitments per #992). Adapter templates handle per-client prompt-engineering variance. Per-platform variance budget: tone may vary up to ~5% per CT v2.4 rubric scoring; capability claims and ethics commitments are invariant.

### MCP server scope vs. client scope

**[DECISION: server holds working memory + tools + persistence + trust-graduation; client holds LLM + conversation surface + client-side history]**

- Conversation history: client-side primary; server-side reflective copy of *what Piper learned* lives in InsightJournal + ADR-054 Composted Learning layers
- Switching clients: same artifacts + same Piper-specific context; *not* the same conversation transcripts
- Cross-client persistence: opt-in only

### Bespoke UI commitment depth

**[DECISION: bespoke UI bound to today's 7 MUX/UI surfaces, 1.0-required subset]**

Per PPM Round 1 input filed today: 5 of 7 surfaces 1.0-required; 4 carry Class A Review Gate triggers. Any bespoke UI beyond this 1.0-required subset requires explicit re-scoping with PDR-005-precedent justification.

### Standards-evolution hedge

**[DECISION: explicit packaging-layer abstraction; MCP-binding is one implementation; successor-standard support gated on multi-factor maturity]**

Criterion for considering successor: ≥2 of (a) Anthropic substrate changes, (b) Klatch coordination requires it, (c) ≥10% of users on the successor, (d) external standards body GA-tier ratification. PM + Architect joint sign-off.

### User-facing language commitment

**[DECISION: BYOC stays internal; external one-sentence frame `[INPUT PENDING: Comms]`]**

---

## PDR commitments to AVOID (per Architect)

Five commitments would force expensive architectural change. PDR-005 explicitly **does not** commit to:

1. "Same UI experience across all hosts" — commits Piper to maintaining N rendering paths
2. "Single canonical context format from day 1" — pre-empts the cross-project alignment conversation
3. "All persona templates available out of the box" — locks in voice work that should land per-host as demand surfaces
4. "Unified cross-host audit log by default" — pre-empts the audit semantics question
5. "No backend changes required to add a host" — false at the boundary

---

## Consequences for product

- 1.0 scope bounded by 7 MUX/UI surfaces (1.0-required subset) + MCP server feature parity
- Persona core decisions need explicit PDR-005 traceability when they affect cross-client consistency
- Capability claims bounded by which MCP tools + integrations the server supports (Pattern-064 prevention at product layer)
- Per-host persona templates ship demand-gated, not all-at-once; PDR-005 commits to *one* template at 1.0 (MCP/Claude Desktop)

## Consequences for architecture (Architect feasibility check, May 15)

### BYOC-ready as-is (5 surfaces)

- Domain layer separation (`services/domain/`)
- Ethics floor at universal entry point (ADR-060 + #992 Phase F + #1004)
- Audit transparency Phase 2 (#1018) — needs `host_id` field
- Intent classification + workflow dispatch (ADR-059)
- Repository pattern + RequestContext (ADR-051; complete #1015 Phase 4)

### Surfaces requiring change (6 surfaces; none showstoppers)

1. Prompt-system / persona parameterization — small refactor (~1-2 days)
2. MCP-server packaging layer — medium (~3-5 days)
3. Context-package format alignment — coordination-heavy (1-2 weeks), implementation-light (~1 week)
4. Auth abstraction layer — small-medium (~3-5 days); closes #1015
5. Cross-host audit semantics — schema small (~1 day); semantic decision deferred
6. Configuration / packaging variants — variable per variant; MCP-server-first

### Security gap to land before MCP packaging

**#1087 SEC-JWT-SECRET-PROD-GUARD** (May 14): `jwt_service.py` hardcoded dev key when env unset. **PPM product-priority: P1, sequenced ahead of MCP packaging.**

---

## Consequences for experience

**`[INPUT PENDING: CXO — experience review per May 4 ack, ~2-3 weeks]`**

PPM frames consistency contract ("same Piper" with up-to-~5% per-platform variance per CT v2.4); CXO produces experience-layer commitments + Colleague Test scoring criteria for cross-client adaptation. Architect flagged: "Voice quality drift per persona — CXO's BYOC review angle 2 (identity coherence) is the right question."

---

## Alternatives considered

- Bespoke web UI primary: rejected (standard SaaS pattern; loses substrate-convergence advantage)
- Native apps per platform: rejected (rebuilding N times; loses persona portability)
- Hybrid (chat input, web UI output): rejected (bifurcates the conversation)
- MCP-only (option (a)): rejected this cycle (5 1.0-required MUX surfaces show *some* bespoke UI is 1.0-necessary)

---

## Open questions

1. Audit semantics decision (cross-host unified vs. per-host) — CEO + HOST input; deferred to follow-up ADR
2. Per-host persona-template authoring lifecycle — CXO lane; deferred to per-template decision case post-1.0
3. Klatch Daedalus alignment cadence — in flight per today's PPM-to-Architect request
4. #1087 SEC-JWT-SECRET-PROD-GUARD priority — PPM commits to P1, sequenced ahead of MCP packaging
5. PDR-006 (post-1.0): per-platform persona variance budget formalization
6. ADR (Architect's lane): canonical context-package format aligned with Klatch L1-L5 + MCPB hybrid
7. ADR (Architect's lane): packaging-layer abstraction implementation

---

## Audit trail

- Vision V2.3 §"Bring Your Own Chat" + Pillar 7 (Apr 11)
- PPM Apr 26 scoping outline: `dev/2026/04/26/ppm-pdr-byoc-scoping-outline-2026-04-26.md`
- BYOC discovery thread opening (May 4): `mailboxes/ppm/sent/`
- PA cross-pollination scan (May 10): `mailboxes/ppm/read/`
- **Architect feasibility check (May 15)**: `mailboxes/ppm/read/memo-arch-to-ppm-cc-cxo-pa-lead-ceo-exec-byoc-feasibility-check-2026-05-15.md`
- Architect↔Daedalus alignment conversation request (May 15): `mailboxes/arch/inbox/`
- MUX/UI 7-surface cohort convene + Round 1 inputs (May 15)
- Anthropic Dreams architectural review (May 15)
- #1087 SEC-JWT-SECRET-PROD-GUARD (May 14)

---

*DRAFT v0.2 | PPM | 2026-05-15 — Architect feasibility check absorbed within 30 min of v0.1 distribution; cohort iteration continues; not canonical until PM ratification*
