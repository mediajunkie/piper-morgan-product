# PDR-005 (DRAFT v0.3): Bring Your Own Chat — Distribution Model

**Status**: **DRAFT v0.3 — Architect §architecture fill-in absorbed; CXO 4-flag review absorbed; (b)/(c) framing refined; cohort iteration continues**
**Author**: PPM
**Date**: 2026-05-15 (v0.3 supersedes v0.2 filed earlier today)
**Tier**: Foundational (PDR-005, alongside PDRs 001-004) — pending PM confirmation
**Supersedes**: None (new PDR; codifies Vision V2.3 §"Bring Your Own Chat")
**Related**: PDR-001 (FTUX), PDR-004 (Experience Philosophy), ADR-051 (RequestContext, #1015 Phase 4), ADR-054 (Cross-Session Memory), ADR-059 (Workflow Dispatcher), ADR-060 (Floor-First Routing), ADR-061 (LLM-touch boundary enforcement), Vision V2.3 §BYOC + Pillar 7
**Predecessor flag**: PPM Apr 25 handoff §1 + Agent 360 §8.3

---

## v0.3 changelog (vs. v0.2, ~4 hours ago)

- **§Decision §Core decision rule** — (b)/(c) framing refined per Architect ack ((c) is asymptotic-target, not structurally identical); added 3-criterion "must be UI" test per CXO Flag 1
- **§Decision §Persona portability** — variance budget replaced with hierarchy per CXO Flag 2 (zero tolerance for capability/ethics; ≤5% for tone; ≤10% structural)
- **§Decision §MCP server scope vs. client scope** — cross-client memory sub-surface obligations added for Surfaces 1 + 6 per CXO Flag 3
- **§Decision §Standards-evolution hedge** — successor criterion (c) updated with absolute MAU floor per CXO Flag 4 (≥10% MAU AND ≥50 absolute users); footnote on early-alpha MAU operationalization per Architect
- **§Consequences for architecture** — full Architect fill-in absorbed; four named architectural commitments (AC-1 through AC-4); AC-1 includes parameter-class addendum per Architect cohort-response intersection
- **§Open questions** — updated with ADR-NN slot for User-Facing Audit Envelope Read-Surface (per Architect cohort divergence-1 answer)
- **§Audit trail** — Architect fill-in memo + CXO v0.2 review + Architect cohort-response added

---

## Context

### Why this PDR is needed

Vision V2.3 made BYOC canonical strategic direction (Apr 11, 2026). Vision-level treatment doesn't substitute for PDR-level codification: vision answers "where are we going"; PDRs answer "what must we build and why" with decision-rule specificity downstream ADRs can refer back to.

### Cross-project convergence as substrate

PA May 10 scan: **Klatch and Piper Morgan independently arrived at "products as services for agents" within 48 hours of each other** (PM Apr 8 BYOC, Klatch Apr 10 futures memo). Convergent evolution under common substrate pressure.

### Architecture has been quietly preparing for it

Architect May 15 feasibility check: **"BYOC isn't a leap; it's the next natural step."** Five structural decisions over 18 months produced a codebase where BYOC is mostly packaging + targeted refactors. AC-1 through AC-4 (below) name the architectural commitments that close the BYOC framing.

---

## Decision

PDR-005 binds Piper Morgan to *mechanisms* downstream work designs against — not specific implementations that pre-empt design choices PM doesn't yet have enough information to make.

### Core decision rule

**[DECISION: (b) — primary MCP delivery + thin bespoke UI for the discrete surfaces chat cannot adequately support; (c) is asymptotic-target, contingent on bespoke-UI surfaces graduating to in-chat or MCP-tool delivery as the protocol matures]**

Per Apr 26 scoping outline's three framings:
- (a) "no Piper-specific UI in v1.0" — infeasible today (the 7 MUX/UI surfaces empirically require at least 5 bespoke surfaces)
- **(b)** "primarily MCP; thin web UI for Piper-specific functions that don't fit chat" ← **decision rule today**
- (c) "any surface supporting the protocol; client choice user-driven; server invariant" — **asymptotic target**; the (b)→(c) transition path is contingent on bespoke-UI surfaces graduating to in-chat or MCP-tool delivery as the protocol matures

The "thin" qualifier is load-bearing. Anything that *can* live in chat *must* live in chat; web UI exists only for the surfaces meeting the 3-criterion test below.

### The 3-criterion "must be UI" test

**[DECISION]**: PDR-005 commits to a falsifiable test downstream ADRs apply per surface. A bespoke UI surface earns 1.0 inclusion only if it meets ≥1 of:

1. **Visual-state-essential** — communicates state that text-only representation loses meaningfully (e.g., privacy indicator visibility on every interaction; integration connection health at a glance)
2. **Multi-turn-coordination-cost-prohibitive** — chat-only flow exceeds ~3 user turns for what UI handles in one interaction (e.g., OAuth wizard with scope selection)
3. **Safety/audit-affordance** — affords visible state for safety-relevant interactions where ambiguity is unacceptable (e.g., Surface 7 audit envelope read; Surface 2 privacy banner)

Per CXO Round 1 synthesis: Surfaces 2/4/6/7 meet ≥1 criterion clearly; Surfaces 1/3 meet weaker forms (mostly criterion 1); Surface 5 doesn't strongly meet any (consistent with post-1.0 disposition).

### The mechanism set (Architect framing — "commit to mechanisms, not implementations")

PDR-005 commits to these mechanisms; specific implementations land in subsequent ADRs:

1. **Persona-template parameterization** — `persona_id` registry pattern, sibling to existing `task_type` registry. Same backend supports multiple per-host configurations. Per-host *content* demand-gated post-1.0; the *mechanism* lands in 1.0.
2. **MCP-server packaging alongside FastAPI** — both surfaces consume same domain layer; MCP server in `services/mcp/server/`. First variant: MCP/Claude Desktop. Other variants demand-gated.
3. **RequestContext-based auth abstraction** — completes #1015 Phase 4 migration; accepts JWT (FastAPI path) or host-provided MCP context.
4. **Audit envelope `host_id` field** — small schema addition for future-extensibility; cross-host audit semantic (unified vs. per-host) deferred to follow-up ADR with HOST + CEO input.
5. **Context-package format negotiated with sibling projects** — Klatch Daedalus alignment in flight; ADR work happens after alignment.

### Persona portability scope

**[DECISION: server-invariant persona core + per-client adapter templates; consistency contract = "same Piper" enforced via tiered variance hierarchy]**

Server holds persona core (capabilities, posture, ethics commitments per #992). Per-client adapter templates handle prompt-engineering variance for client-specific affordances.

**Variance hierarchy** (per CXO Flag 2; Pattern-064 prevention at persona layer):

| Layer | Variance budget | Enforcement |
|---|---|---|
| **Capability claims + ethics commitments** | **Zero tolerance** | Immutable from adapter scope; any per-platform variance is a Class A boundary violation regardless of measurement |
| **Tone + voice register** | ≤5% per CT v2.4 rubric | CXO-calibrated; rubric-scored per platform |
| **Working memory references + context coordination** | ≤10% structural variance | Acceptable for platform-affordance differences (Slack thread context vs. Claude Desktop turn context) |

The hierarchy is architecturally enforced via AC-1 (parameter-class separation): adapter loading only binds tone-class parameters; capability/ethics parameters are not addressable from adapter scope.

### MCP server scope vs. client scope

**[DECISION: server holds working memory + tools + persistence + trust-graduation; client holds LLM + conversation surface + client-side history]**

- Conversation history: client-side primary; server-side reflective copy of *what Piper learned* lives in InsightJournal + ADR-054 Composted Learning layers
- Switching clients: same artifacts + same Piper-specific context; *not* the same conversation transcripts
- Cross-client persistence: opt-in only

**Cross-client memory continuity sub-surface obligations** (per CXO Flag 3):

- **Surface 1 (history) needs a cross-client variant**: "what I learned about you across all hosts" — working-memory-layer surfacing distinct from per-host conversation transcripts
- **Surface 6 (first-run) needs a "welcome back" variant**: for users arriving on a new client — explicit "I remember [X about you]; I do not have our previous transcripts" honesty surface

These fold into the MUX/UI cohort Round 2 scoping rather than treating them as new surfaces.

### Bespoke UI commitment depth

**[DECISION: bespoke UI bound to today's 7 MUX/UI surfaces, 1.0-required subset, per the 3-criterion test above]**

Per CXO Round 1 synthesis: 5 of 7 surfaces 1.0-required; 4 carry Class A Review Gate triggers (privacy, integration wizards, first-run, error/degraded). Any bespoke UI beyond this 1.0-required subset requires explicit re-scoping with PDR-005-precedent justification.

### Standards-evolution hedge

**[DECISION: explicit packaging-layer abstraction; MCP-binding is one implementation; successor-standard support gated on multi-factor maturity]**

Criterion for considering successor support: **≥2 of** (a) Anthropic substrate changes, (b) Klatch coordination requires it, (c) **≥10% of active users (MAU) AND ≥50 absolute users** on the successor, (d) external standards body GA-tier ratification.

*Footnote on (c) operationalization*: at very-early alpha (current state), "active users" is itself a fuzzy concept. Pre-MAU-instrumentation period uses single-active-user-week heuristic; PDR-001 §X user-state methodology applies once instrumentation lands.

PM + Architect joint sign-off on adding new protocol-binding; PPM identifies product implications.

### User-facing language commitment

**[DECISION: BYOC stays internal; external one-sentence frame `[INPUT PENDING: Comms]`]**

---

## PDR commitments to AVOID (per Architect)

Five commitments would force expensive architectural change. PDR-005 explicitly **does not** commit to:

1. "Same UI experience across all hosts"
2. "Single canonical context format from day 1"
3. "All persona templates available out of the box"
4. "Unified cross-host audit log by default"
5. "No backend changes required to add a host"

---

## Consequences for product

- 1.0 scope bounded by 7 MUX/UI surfaces (1.0-required subset, per 3-criterion test) + MCP server feature parity
- Persona core decisions need explicit PDR-005 traceability when they affect cross-client consistency
- Capability claims bounded by which MCP tools + integrations the server supports (Pattern-064 prevention at product layer)
- Per-host persona templates ship demand-gated, not all-at-once; PDR-005 commits to *one* template at 1.0 (MCP/Claude Desktop)

---

## Consequences for architecture (Architect fill-in, May 15)

### Architectural commitments

PDR-005's product commitments translate to four architectural commitments. These are constraints downstream ADRs and implementation work must design against; deviation requires explicit PDR-005-precedent justification.

#### AC-1 — Persona-template parameterization

PM commits to a **persona-registry pattern**: persona definitions are first-class typed entries dispatched at consumption, sibling to the existing `task_type` registry that operates at every `LLMClient.complete()` call site. The server holds a canonical persona core; per-client adapter templates are registered entries that load by client identifier.

Architectural implications:
- Prompt construction at `services/llm/prompts.py` separates persona-core directives from task-specific scaffolding
- Adapter templates live in a discoverable directory with explicit registry entries
- Loading defaults to canonical persona core when no client-specific adapter is registered (fail-safe default)
- The Pattern-064 prevention discipline applies: an adapter template that *appears* registered but produces no actual prompt variance must fail loudly, not silently degrade to canonical

**AC-1 addendum (variance hierarchy enforcement)**: adapter templates may override persona-core parameters at the tone-and-voice layer only; capability-claim and ethics-commitment parameters are immutable from adapter scope. Architectural enforcement: **separate parameter classes; adapter loading only binds tone-class parameters**. This encodes the variance hierarchy (above) in the parameterization mechanism rather than relying on convention.

**Closes the cross-client consistency contract architecturally**.

#### AC-2 — Packaging-layer abstraction

PM commits to an **internal protocol-binding interface** that decouples server logic from delivery-surface protocol. MCP-server-binding is one implementation; future bindings are additional implementations behind the same interface.

Architectural implications:
- Server domain layer operates against an internal request/response shape; protocol bindings translate
- New protocol-binding requires implementing the same interface; does NOT require domain-layer changes
- Existing FastAPI binding and MCP server packaging path sit alongside each other; both consume the same domain layer
- Protocol-binding addition gated on §Standards-evolution hedge criterion; the *mechanism* to add bindings is unblocked

**Closes the swappable-packaging-layer commitment architecturally**.

#### AC-3 — Composted Learning input/output store separation

PM commits to ADR-054 Layer 3 operating on the **input-store / output-store / review-then-adopt** pattern from Anthropic Dreams reference architecture. Input working memory is never modified in place; consolidation passes produce candidate output stores; adopt-gate is explicit lifecycle step (per Pattern-070 cleanup-job-with-cancellation-hygiene).

Architectural implications:
- `InsightJournal` + KG + working-memory layers are *read-only* during consolidation
- Adopt-gate is a explicit lifecycle step; consolidation pipeline is itself a Cleanup-Job instance (Pattern-070's prospective fourth Reference Instance)
- BYOC implication: cross-client consolidation produces *the same* candidate output regardless of which client surfaced the input — this is what makes "same Piper learns" architecturally true rather than rhetorical
- Failure-mode isolation: a consolidation-pass failure must not roll back unrelated session state

**Closes the "Piper-learns-across-clients" commitment architecturally**.

#### AC-4 — Runtime adapter-template dispatch

PM commits to **runtime persona-template dispatch by client identifier**: the server detects (via MCP context, JWT claims, or explicit client-id header) which client surface is invoking the request and loads the corresponding adapter template at request time. Default to canonical persona core when no specific adapter is registered.

Architectural implications:
- Client-identification flows through `RequestContext` (per ADR-051; #1015 Phase 4 work completes the migration). The `client_id` becomes a typed RequestContext field
- Adapter loading at request time is light (~1 dict lookup against the registry); does NOT add request-path latency materially
- Adapter content is static at server startup; new adapter templates ship in deployment artifacts, not registered at request time (prevents Pattern-064 silent-extension failure modes)
- Audit envelope (#1018 audit_transparency Phase 2) captures `client_id` per request; cross-client audit forensics works without schema migration

**Closes the per-client adaptation commitment architecturally**.

### Enabling work (prerequisite or co-shipping)

- **#1015** — ADR-051 RequestContext Phase 4: P2; land before MCP server packaging
- **#1087** — SEC-JWT-SECRET-PROD-GUARD: P1, sequenced ahead of MCP packaging
- **#1075** — route-prefix migration (in flight): consistent `/api/v1/` before parallel MCP routes
- **Pattern-070 cleanup-job adoption** for the consolidation pipeline (Anthropic Dreams Type 1; Pattern-070's prospective fourth instance)

None are blockers for v1.0 ratification; all tracked as enabling work.

### What architecture explicitly does NOT commit to

Per the 5 AVOID commitments in §PDR commitments to AVOID, architecture mirrors: host owns rendering; format-decision deferred to Daedalus alignment; adapter content per-host demand-gated; cross-host audit semantic deferred; non-zero per-host integration work.

---

## Consequences for experience

**`[INPUT PENDING: CXO — 2-3 week deeper review per May 4 ack; 2026-05-25 → 2026-06-01 target window]`**

Per CXO May 15 v0.2 review §Deferral: the experience-section deep content lands as the 2-3 week deliverable. Will cover:
- Experience-layer commitments for cross-client adaptation (variance hierarchy from §Persona portability)
- Colleague Test scoring criteria for cross-client adaptation
- Identity coherence framework (Architect's flagged "voice quality drift per persona — angle 2")
- Per-platform onboarding voice considerations (intersecting Surface 6 + Surface 1 cross-client variants from §MCP server scope)

The MUX/UI cohort Round 2 + a focused experience-review sub-session is the right shape.

---

## Alternatives considered

- Bespoke web UI primary: rejected (standard SaaS; loses substrate-convergence advantage)
- Native apps per platform: rejected (rebuilding N times; loses persona portability)
- Hybrid (chat input, web UI output): rejected (bifurcates the conversation)
- MCP-only (option (a)): rejected this cycle (5 1.0-required MUX surfaces show some bespoke UI is 1.0-necessary)

---

## Open questions

1. **Audit semantics decision** (cross-host unified vs. per-host) — CEO + HOST input; deferred to follow-up ADR
2. **Per-host persona-template authoring lifecycle** — CXO lane; deferred post-1.0
3. **Klatch Daedalus alignment cadence** — in flight; Architect-authored brief filed for Janus relay
4. **#1087 SEC-JWT-SECRET-PROD-GUARD priority** — PPM committed P1, sequenced ahead of MCP packaging
5. **PDR-006 (post-1.0)**: per-platform persona variance budget formalization
6. **ADR (Architect's lane)**: canonical context-package format aligned with Klatch L1-L5 + MCPB hybrid
7. **ADR (Architect's lane)**: packaging-layer abstraction implementation
8. **ADR-NN (next slot)**: User-Facing Audit Envelope Read-Surface — extends ADR-061 element-4 to user-visibility dimension; companion to Surface 7 MUX doc (per Architect cohort divergence-1 answer; CIO slot-availability check at filing time)

---

## Audit trail

- Vision V2.3 §"Bring Your Own Chat" + Pillar 7 (Apr 11)
- PPM Apr 26 scoping outline: `dev/2026/04/26/ppm-pdr-byoc-scoping-outline-2026-04-26.md`
- BYOC discovery thread opening (May 4): `mailboxes/ppm/sent/`
- PA cross-pollination scan (May 10): `mailboxes/ppm/read/`
- Architect feasibility check (May 15): `mailboxes/ppm/read/`
- Architect §Consequences for architecture fill-in (May 15): `mailboxes/ppm/inbox/memo-arch-to-ppm-cc-cxo-pa-lead-ceo-exec-pdr-005-architect-section-fill-in-2026-05-15.md`
- CXO PDR-005 v0.2 review (May 15): `mailboxes/ppm/inbox/memo-cxo-to-ppm-cc-pa-arch-lead-comms-ceo-exec-pdr-005-v0.2-cxo-review-2026-05-15.md`
- Architect MUX/UI Round 1 cohort response + PDR-005 v0.2 concur (May 15): `mailboxes/ppm/inbox/memo-arch-to-cxo-cc-ppm-comms-lead-pa-ceo-exec-mux-ui-round-1-cohort-response-pdr-005-v0.2-concur-2026-05-15.md`
- CXO MUX/UI Round 1 synthesis (May 15): `mailboxes/ppm/inbox/mux-ui-gap-cxo-round-1-synthesis-2026-05-15.md`
- Architect↔Daedalus alignment brief (May 15, filed for Janus relay): `mailboxes/ppm/inbox/memo-arch-to-janus-cc-ceo-ppm-pa-cxo-exec-daedalus-context-package-alignment-brief-2026-05-15.md`
- Anthropic Dreams architectural review (May 15)
- #1087 SEC-JWT-SECRET-PROD-GUARD (May 14)

---

*DRAFT v0.3 | PPM | 2026-05-15 — Architect §architecture fill-in + CXO 4-flag review + (b)/(c) framing refinement absorbed; cohort iteration continues; not canonical until PM ratification*
