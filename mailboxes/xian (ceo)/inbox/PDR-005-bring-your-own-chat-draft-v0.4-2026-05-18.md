# PDR-005 (DRAFT v0.4): Bring Your Own Chat — Distribution Model

**Status**: **DRAFT v0.4 — Round 2 CEO ratification absorbed; ADR-063 canonical Surface 7 reference; Phase 2.2 PPM signal architecture explicit; CXO §experience pending v0.5**
**Author**: PPM
**Date**: 2026-05-18 (v0.4 supersedes v0.3 filed 2026-05-15)
**Tier**: Foundational (PDR-005, alongside PDRs 001-004) — pending PM confirmation
**Supersedes**: None (new PDR; codifies Vision V2.3 §"Bring Your Own Chat")
**Related**: PDR-001 (FTUX), PDR-004 (Experience Philosophy), ADR-051 (RequestContext, #1015 Phase 4), ADR-054 (Cross-Session Memory), ADR-059 (Workflow Dispatcher), ADR-060 (Floor-First Routing), ADR-061 (LLM-touch boundary enforcement), **ADR-062 (e2e Phase 0), ADR-063 (User-Facing Audit Envelope Read-Surface, the canonical Surface 7 ADR), ADR-064 (Search Index Architecture, Surface 5 pre-1.0)**, Vision V2.3 §BYOC + Pillar 7
**Predecessor flag**: PPM Apr 25 handoff §1 + Agent 360 §8.3

---

## v0.4 changelog (vs. v0.3, May 15)

- **§Decision §Core decision rule (b)** — references concrete Round 2-ratified integration pick (GitHub + Calendar + Notion; defer Slack) in support of (b)'s "thin bespoke UI" qualifier
- **§Decision §Bespoke UI commitment depth** — Round 2 CEO ratification absorbed; Phase 2.1/2.2/2.3 sequencing referenced; **per-surface sufficient-signal architecture explicit** for Phase 2.2 unblocking
- **§Consequences for architecture** — `ADR-NN` placeholders replaced with `ADR-063` (canonical Surface 7 ADR); ADR-062 (e2e Phase 0) + ADR-064 (Surface 5 index) referenced
- **§Open questions** — item 8 (ADR-NN audit-envelope read-surface) RESOLVED via ADR-063; new item 9 (Pattern-073 Documentation-Asserted-Behavior Drift discipline) added as enabling-discipline thread; new item 10 (Multi-Agent API characterization, queued post-v0.4) added
- **§Audit trail** — Round 2 CEO ratification memo + Lead Dev Phase 2 scoping memo + PM v0.4-proceed-now memo added

---

## Context

### Why this PDR is needed

Vision V2.3 made BYOC canonical strategic direction (Apr 11, 2026). Vision-level treatment doesn't substitute for PDR-level codification: vision answers "where are we going"; PDRs answer "what must we build and why" with decision-rule specificity downstream ADRs can refer back to.

### Cross-project convergence as substrate

PA May 10 scan: **Klatch and Piper Morgan independently arrived at "products as services for agents" within 48 hours of each other** (PM Apr 8 BYOC, Klatch Apr 10 futures memo). Convergent evolution under common substrate pressure.

### Architecture has been quietly preparing for it

Architect May 15 feasibility check: **"BYOC isn't a leap; it's the next natural step."** Five structural decisions over 18 months produced a codebase where BYOC is mostly packaging + targeted refactors. AC-1 through AC-4 (below) name the architectural commitments that close the BYOC framing. ADR-062, ADR-063, ADR-064 landed May 16 in the ratified sequence (per Lead Dev's Phase 2 scoping memo + Architect's clarification at `04f4f488`).

### MUX/UI Round 2 CEO ratification (May 16)

PM ratified all 6 locked decisions from CXO's Round 2 cohort synthesis (May 15) via Architect walkthrough (May 16, 12:48 PT). Bundle ratification — no subset adjustments. Six decisions ratified:

1. Surface 4 integration pick — **GitHub + Calendar + Notion; defer Slack**
2. Surface 7 audit-envelope read surface — paired ADR-063 + Surface 7 MUX doc (both lanes)
3. Surface 2 privacy granularity — per-conversation for 1.0; per-message reserved post-1.0
4. Surface 1 sidebar reconciliation — assign roles (left rail = current session; right slide-out = archive); don't merge
5. Surface 6 framing — templated voice surface (Class A + Class C; NOT four-element principle obligations at greeting composition layer)
6. Total build estimate — ~13-18 working days + voice work in parallel + PDR-005 v0.3+ sequencing dependency

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

**1.0 bespoke-UI surfaces are now empirically scoped** (Round 2 CEO ratification): 5 of 7 MUX/UI surfaces (the 1.0-required subset) + concrete integration scope (GitHub + Calendar + Notion). Slack deferred. Anything beyond requires explicit re-scoping with PDR-005-precedent justification.

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

**[DECISION: bespoke UI bound to today's 7 MUX/UI surfaces, 1.0-required subset, per the 3-criterion test above; Round 2 CEO-ratified scope]**

Per Round 2 CEO ratification: 5 of 7 surfaces 1.0-required; 4 carry Class A Review Gate triggers (privacy, integration wizards, first-run, error/degraded). Concrete integration pick: **GitHub + Calendar + Notion; defer Slack**. Surface 5 (search) is post-1.0 with ADR-064 (index architecture) pre-1.0.

Build sequencing (Lead Dev Phase 2 scoping memo, May 17):

- **Phase 2.1**: Surface 1 + Surface 7 — unblocked NOW; ~4-6 working days sequential
- **Phase 2.2**: Surface 2 + Surface 4 — gated on PDR-005 v0.4 sufficiency (PPM signal architecture below); ~7-10 working days when unblocked
- **Phase 2.3**: Surface 6 — anytime after Phase 2.1; ~2-3 working days

### Phase 2.2 PPM signal architecture (new in v0.4)

**[DECISION: per-surface sufficient-signals from PPM to Lead Dev unblock Phase 2.2 build]**

Per Round 2 CEO ratification (Q2 of PPM's May 17 ask): **two separate sufficient-signal memos**, not a composite signal. Composite explicitly declined — per-surface signals match Lead Dev's Phase 2.2 sub-phase model cleanly and allow start-whichever-surface-is-unblocked-first.

PPM signal shape:
- **"Surface 2 build is unblocked"**: short memo to Lead Dev (CC cohort) when v0.4's §Decision §Persona portability + §MCP server scope content is sufficient for per-conversation privacy build (Surface 2 only). Per-conversation privacy is the 1.0 scope; per-message expansion deferred post-1.0.
- **"Surface 4 build is unblocked"**: short memo to Lead Dev (CC cohort) when v0.4's §Decision §Bespoke UI + §MCP server scope content is sufficient for integration wizard build (GitHub + Calendar + Notion). Slack explicitly out of 1.0 scope.

Signals may ship simultaneously (if v0.4 reaches sufficient content for both at once) or staggered (as content stabilizes per surface). Lead Dev acts on each independently.

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

- 1.0 scope bounded by 7 MUX/UI surfaces (1.0-required subset, per 3-criterion test) + MCP server feature parity + **GitHub + Calendar + Notion integrations only** (Slack deferred per Round 2 ratification)
- Persona core decisions need explicit PDR-005 traceability when they affect cross-client consistency
- Capability claims bounded by which MCP tools + integrations the server supports (Pattern-064 prevention at product layer)
- Per-host persona templates ship demand-gated, not all-at-once; PDR-005 commits to *one* template at 1.0 (MCP/Claude Desktop)
- Phase 2.2 build window opens per-surface as PPM signals "Surface 2 unblocked" + "Surface 4 unblocked" (separate signals; may ship simultaneously)

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

### Surface-7-specific architectural commitments (ADR-063)

ADR-063 (User-Facing Audit Envelope Read-Surface) IS the canonical Surface 7 ADR per Lead Dev's Phase 2 scoping clarification (the "Surface 7 ADR-NN" placeholder in v0.3 resolved at slot allocation). Four-Element READ-Side Principle + field-bucket split + Pattern-071 (audit-as-attack-surface) architectural commitments. ADR-061 remains the four-element-boundary template reference for adjacent LLM-touch surfaces.

### Enabling work (prerequisite or co-shipping)

- **#1015** — ADR-051 RequestContext Phase 4: P2; land before MCP server packaging
- **#1087** — SEC-JWT-SECRET-PROD-GUARD: P1, sequenced ahead of MCP packaging
- **#1075** — route-prefix migration: **CLOSED May 16** (Lead Dev's transparency-wire + admin_compose migration commit `eb4ec8e2`); Surface 4 callback URL stability dependency RESOLVED
- **Pattern-070 cleanup-job adoption** for the consolidation pipeline (Anthropic Dreams Type 1; Pattern-070's prospective fourth instance)
- **Pattern-073 (Documentation-Asserted-Behavior Drift)** — emerging pattern filed May 16; doc-sync-sweep skill discipline applies during PDR-005 → ADR → implementation cycle; each surface ships gets a doc-sync-sweep pass to verify code matches PDR-asserted + ADR-asserted + MUX-doc-asserted + docstring-asserted claims

None are blockers for v1.0 ratification; all tracked as enabling work.

### What architecture explicitly does NOT commit to

Per the 5 AVOID commitments in §PDR commitments to AVOID, architecture mirrors: host owns rendering; format-decision deferred to Daedalus alignment; adapter content per-host demand-gated; cross-host audit semantic deferred; non-zero per-host integration work.

---

## Consequences for experience

**`[INPUT PENDING: CXO — natural-pace per PM May 18 greenlight; v0.5 absorbs whenever it lands]`**

Per PM May 18 directive (Docs-relayed): CXO greenlit to produce §Consequences-for-experience at natural pace, in parallel with v0.4. v0.4 ships now (per Option Y); v0.5 absorbs CXO content whenever it lands — no re-litigation of Round 2 decisions or v0.4 mechanism set.

The previous May 4 CXO-committed "May 25 – Jun 1 target" was rejected as Time Lord pacing assumption that predated the bias-to-action substrate. Cohort velocity since May 4 (CIO V1 v0.1→v0.4 in one day; CLI B 30-min design; etc.) demonstrates the target was conservative.

When v0.5 ships, the §Consequences-for-experience section will cover:
- Experience-layer commitments for cross-client adaptation (variance hierarchy from §Persona portability)
- Colleague Test scoring criteria for cross-client adaptation
- Identity coherence framework (Architect's flagged "voice quality drift per persona — angle 2")
- Per-platform onboarding voice considerations (intersecting Surface 6 + Surface 1 cross-client variants from §MCP server scope)
- Sub-surface obligations refinement based on actual MUX doc drafting outputs

The MUX/UI cohort Round 2 + the CXO-Comms voice-pass coordination pattern (per PM May 18 Surface 7 memo) inform the experience-section shape when it lands.

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
3. **Klatch Daedalus alignment cadence** — in flight; Architect-authored brief filed for Janus relay (May 15); reply window Tue May 19 → Thu May 21 per Architect's shape memo
4. **#1087 SEC-JWT-SECRET-PROD-GUARD priority** — PPM committed P1, sequenced ahead of MCP packaging
5. **PDR-006 (post-1.0)**: per-platform persona variance budget formalization
6. **ADR (Architect's lane)**: canonical context-package format aligned with Klatch L1-L5 + MCPB hybrid (post-Daedalus alignment)
7. **ADR (Architect's lane)**: packaging-layer abstraction implementation
8. ~~ADR-NN slot for User-Facing Audit Envelope Read-Surface~~ — **RESOLVED: ADR-063 is the canonical Surface 7 ADR**; companion to Surface 7 MUX doc (CXO-Comms voice-pass coordination pattern per PM May 18)
9. **Pattern-073 Documentation-Asserted-Behavior Drift discipline** — emerging pattern filed May 16; doc-sync-sweep skill v0.1 (Lead Dev draft, CIO ratification pending) runs after each surface ships during MUX/UI Phase 2 build; verifies code matches PDR-asserted + ADR-asserted + MUX-doc-asserted + docstring-asserted claims
10. **Multi-Agent API characterization** (post-v0.4 PPM session) — per CIO May 18 Anthropic Outcomes disposition memo; PPM characterizes Multi-Agent API surface against cohort-coordination patterns; identifies where Multi-Agent simplifies (Task subagent spawning) vs. orthogonal (mailbox protocol, role essential briefings, methodology corpus)

---

## Audit trail

- Vision V2.3 §"Bring Your Own Chat" + Pillar 7 (Apr 11)
- PPM Apr 26 scoping outline: `dev/2026/04/26/ppm-pdr-byoc-scoping-outline-2026-04-26.md`
- BYOC discovery thread opening (May 4): `mailboxes/ppm/sent/`
- PA cross-pollination scan (May 10): `mailboxes/ppm/read/`
- Architect feasibility check (May 15): `mailboxes/ppm/read/`
- Architect §Consequences for architecture fill-in (May 15): `mailboxes/ppm/read/memo-arch-to-ppm-cc-cxo-pa-lead-ceo-exec-pdr-005-architect-section-fill-in-2026-05-15.md`
- CXO PDR-005 v0.2 review (May 15): `mailboxes/ppm/read/memo-cxo-to-ppm-cc-pa-arch-lead-comms-ceo-exec-pdr-005-v0.2-cxo-review-2026-05-15.md`
- Architect MUX/UI Round 1 cohort response + PDR-005 v0.2 concur (May 15)
- CXO MUX/UI Round 1 + Round 2 synthesis (May 15)
- Architect↔Daedalus alignment brief (May 15, filed for Janus relay)
- Anthropic Dreams architectural review (May 15)
- **MUX/UI Round 2 CEO ratification (May 16)**: `mailboxes/ppm/read/memo-arch-to-cxo-lead-comms-ppm-cc-ceo-pa-exec-mux-ui-round-2-ceo-ratification-2026-05-16.md`
- **Lead Dev MUX/UI Phase 2 scoping (May 17)**: `mailboxes/ppm/read/memo-lead-to-cxo-cc-arch-ppm-comms-ceo-exec-pa-mux-ui-phase-2-lead-dev-lane-scoping-2026-05-17.md`
- **PM v0.4 proceed-now decision (May 18)**: `mailboxes/ppm/read/memo-pm-via-docs-to-ppm-cc-cxo-lead-pa-pdr-005-v0.4-proceed-now-2026-05-18.md`
- **PM CXO greenlight natural-pace experience (May 18)**: `mailboxes/ppm/read/memo-pm-via-docs-to-cxo-cc-ppm-pa-greenlight-consequences-for-experience-natural-pace-2026-05-18.md`
- **CIO Anthropic Outcomes platform-productization disposition (May 18)**: `mailboxes/ppm/read/memo-cio-to-ceo-cc-arch-lead-host-exec-docs-pa-ppm-anthropic-outcomes-platform-productization-disposition-2026-05-18.md`
- #1087 SEC-JWT-SECRET-PROD-GUARD (May 14)
- #1075 route-prefix migration CLOSED (May 16)
- ADR-062, ADR-063, ADR-064 (May 16)
- Pattern-070, Pattern-071, Pattern-073 (May 16)

---

*DRAFT v0.4 | PPM | 2026-05-18 — Round 2 CEO ratification absorbed; ADR-063 canonical Surface 7 reference; Phase 2.2 PPM signal architecture explicit; CXO §experience pending v0.5; not canonical until PM ratification*
