# PDR-005 (DRAFT v0.1): Bring Your Own Chat — Distribution Model

**Status**: **DRAFT v0.1 — opened for cohort iteration**
**Author**: PPM
**Date**: 2026-05-15
**Tier**: Foundational (PDR-005, alongside PDRs 001-004) — pending PM confirmation
**Supersedes**: None (new PDR; codifies Vision V2.3 §"Bring Your Own Chat")
**Related**: PDR-001 (FTUX), PDR-004 (Experience Philosophy), ADR-060 (Floor-First Routing), Vision V2.3 §BYOC + Pillar 7
**Predecessor flag**: PPM Apr 25 handoff §1 + Agent 360 §8.3 — "the most consequential strategic decision since ADR-060 lacks formal PDR treatment"

---

## DRAFT framing — read before reviewing

This is a DRAFT v0.1 opened today (2026-05-15) per PM direction to move PDR-005 from HELD into active drafting cadence. **Do not treat as canonical**. Sections marked `[INPUT PENDING: role]` are open for cohort contribution; sections marked `[DECISION: x]` are PPM proposals for cohort review + PM ratification. The artifact lives in `dev/active/` until ratification; landing target is `docs/internal/product/pdr/PDR-005-bring-your-own-chat.md`.

**Substantive inputs absorbed**:
- PPM Apr 26 scoping outline (`dev/2026/04/26/ppm-pdr-byoc-scoping-outline-2026-04-26.md`) — six decision-rule areas + suggested division of labor
- PA May 10 cross-pollination scan (`mailboxes/ppm/read/memo-pa-to-ppm-cc-arch-cxo-ceo-exec-byoc-cross-pollination-scan-2026-05-10.md`) — five principle-level convergences with Klatch
- Architect feasibility check (ongoing, folded into #1016 Phase 4 per May 4 ack)
- CXO experience review (~2-3 weeks per CXO ack May 4; pending)
- Architect↔Daedalus context-package alignment conversation (requested today)
- MUX/UI 7-surface cohort convene today (parallel scoping; intersects §4 below)

---

## Context

### Why this PDR is needed

Vision V2.3 made BYOC canonical strategic direction (April 11, 2026). Vision-level treatment doesn't substitute for PDR-level codification because:

- Vision answers "where are we going"; PDRs answer "what must we build and why" with decision-rule specificity that downstream ADRs and product decisions can refer back to.
- BYOC determines delivery surface, packaging, persona delivery, and what "Piper" means to a user in ways other vision pillars don't. ADRs (MCPB packaging, server architecture, persona portability) need a product anchor; without a PDR, those ADRs either re-litigate product direction inside architecture decisions OR accept product direction implicitly without traceable rationale.
- Predecessor PPM identified this as the most-flagged carry-forward; two PPM instances now agree it's overdue.

### Cross-project convergence as substrate

PA May 10 scan: **Klatch and Piper Morgan independently arrived at "products as services for agents" within 48 hours of each other** (PM Apr 8 BYOC, Klatch Apr 10 futures memo). Both projects responded to the same Anthropic infrastructure shifts (Managed Agents public beta Apr 8, SDK compaction-helper deprecation v0.83.0). This is **not coincidence; it is convergent evolution** under common substrate pressure.

Implications for this PDR:
- The thesis ("products as services for agents") does not need argument from first principles; cite the convergence
- The shape (MCP server as primary product surface) does not need defense as future-direction; it is current architectural commitment
- The architectural patterns (export-format-as-protocol, five-layer + MCPB hybrid, input/output store + review-then-adopt) are validated cross-project

---

## Decision

PDR-005 binds Piper Morgan to the following product commitments. Each is a *decision rule* downstream work designs against, not a policy statement.

### Core decision rule

**[DECISION: (b) — primary MCP delivery + thin bespoke UI for surfaces that don't fit chat]**

Per the Apr 26 scoping outline's three candidate framings:
- (a) "Piper is delivered via the user's preferred MCP-compatible client; there is no Piper-specific UI in v1.0"
- **(b)** "Piper is primarily delivered via MCP; a thin web UI exists for Piper-specific functions that don't fit the chat client model" ← **PPM lean**
- (c) "Piper is delivered via *any* surface that supports the protocol; client choice is user-driven and the server is invariant"

**Rationale for (b)**: Vision V2.3 leans (c) in spirit but (a) is too strict and (c) is structurally identical to (b) with different framing. The seven UI surfaces enumerated in today's MUX/UI cohort convene (Lead Dev May 14, CXO May 15) — conversation history, privacy controls, integration wizards, first-run, error states — establish empirically that *some* bespoke UI is 1.0-necessary. The honest PDR commitment is (b): **MCP primary, thin web UI for the discrete surfaces chat cannot adequately support**, scope-bound and explicitly enumerated rather than open-ended.

The "thin" qualifier is load-bearing. Anything that *can* live in chat *must* live in chat; web UI exists only for the falsifiable cases where it cannot.

### Persona portability scope

**[DECISION: server-invariant persona core + per-client adapter templates; consistency contract = "same Piper"]**

The server holds the persona core (capabilities, posture, ethics-as-IA commitments per #992). Per-client adapter templates (Claude Project instructions, Custom GPT instructions, Gem instructions) handle prompt-engineering variance for client-specific affordances. **The consistency contract is "same Piper" — a user must recognize Piper across clients** even though presentation varies per platform.

- Ownership: PPM owns the persona core decisions; CXO owns adapter template voice; Architect owns the abstraction layer between them.
- Per-platform variance budget: tone may vary up to ~5% per CT v2.4 rubric scoring (within the cohort's tolerance); capability claims and ethics commitments are invariant.

### MCP server scope vs. out-of-scope

**[DECISION: server holds working memory, tools, persistence, trust-graduation; client holds LLM, conversation surface, client-side history]**

- Conversation history: **client-side primary** (the user's history with that client is theirs and lives there); **server-side reflective copy** of *what Piper learned* from the conversation lives in the InsightJournal + ADR-054 Composted Learning layers. Switching clients: user sees same artifacts, same Piper-specific context, *not* the same conversation transcripts (those stay with the client they happened in).
- Preferred-client memory: server tracks last-connected client for diagnostics; does *not* assume continuity unless user opts in. Per-connection independence is the default; cross-client persistence is opt-in.

### The "no bespoke UI" commitment depth

**[DECISION: bespoke UI permitted only for the 7 enumerated MUX/UI surfaces, scope-bound to 1.0-required subset]**

Today's MUX/UI cohort scoping (CXO May 15) identified 7 candidate surfaces (conversation history, privacy controls, settings, integration wizards, search, first-run, error/degraded). PPM Round 1 input flagged 5 as 1.0-required (subset of those marked Class A Review Gate triggers; see `mailboxes/cxo/inbox/mux-ui-gap-ppm-input-2026-05-15.md`). **The PDR binds: any bespoke UI beyond the 1.0-required subset requires explicit re-scoping with PDR-005-precedent justification.**

Specific test cases per scoping outline:
- Setup/onboarding: **first-run state UI** (1.0-required per PPM lens)
- Artifact browse/retrieve at scale: **conversation history UI** (1.0-required)
- Trust-level configuration: chat-only (post-1.0 settings surface)
- Integration setup (OAuth flows): **integration wizard UI** (1.0-required for scope-bound integrations)

### Standards-evolution hedge

**[DECISION: explicit packaging-layer abstraction; MCP-binding is one implementation; successor-standard support gated on substrate maturity]**

- The server is built against a Piper-internal interface layer; MCP-protocol-binding is one implementation of that interface. Successor standards (or alternative protocols) can be added by implementing the same internal interface.
- Criterion for considering successor support: when ≥2 of (a) Anthropic substrate changes, (b) Klatch coordination requires it, (c) ≥10% of users on the successor, (d) external standards body ratification at GA-tier maturity.
- Decision authority: PM + Architect joint sign-off on adding new protocol-binding; PPM identifies product implications.

### User-facing language commitment

**[DECISION: "BYOC" stays internal; external one-sentence frame TBD with Comms]**

- Internal language: "Bring Your Own Chat" (BYOC) remains canonical for internal/PDR/ADR work.
- External language: needs CXO + Comms collaboration on the marketing-stable frame.
- **`[INPUT PENDING: Comms]`** — one-sentence description of Piper that works for someone who has never heard of MCP; two-sentence description of the Piper/client relationship; marketing-stable name for the distribution model.

---

## Consequences for product

- 1.0 scope is bounded by the 7 MUX/UI surfaces (1.0-required subset) + MCP server feature parity. Anything not in those bounds is post-1.0 by default.
- Persona core decisions need explicit PDR-005 traceability when they affect cross-client consistency.
- Capability claims (what Piper says it can do) are bounded by which MCP tools + which integrations the server supports. Wizards for an integration imply that integration works end-to-end (the Pattern-064 prevention discipline at the product layer).

## Consequences for architecture

**`[INPUT PENDING: Architect — feasibility check output from #1016 Phase 4]`**

PPM frames product-side requirements: server-invariant persona core, abstraction layer between server logic and protocol-binding, isolated input-store/output-store for Composted Learning, per-client adapter template loading. Architect produces the architectural commitments that support these.

## Consequences for experience

**`[INPUT PENDING: CXO — experience review per May 4 ack, ~2-3 weeks]`**

PPM frames the consistency contract ("same Piper" across clients with up-to-~5% per-platform variance per CT v2.4); CXO produces the experience-layer commitments and the Colleague Test scoring criteria for cross-client adaptation.

## Alternatives considered

- **Bespoke web UI primary, chat as alternative interface**: rejected; structurally identical to the standard SaaS pattern, loses the substrate-convergence advantage with Klatch + Anthropic ecosystem
- **Native apps per platform**: rejected; rebuilding the same product N times; loses persona portability; Mobile-skunkworks-paused context applies
- **Hybrid: chat for input, web UI for output**: rejected; bifurcates the conversation; users have to context-switch mid-task
- **MCP-only (option (a) above)**: rejected this cycle; the 7 MUX/UI surfaces show empirically that *some* bespoke UI is 1.0-necessary

## Open questions deferred to follow-up PDRs or ADRs

- PDR-006 (post-1.0): per-platform persona variance budget formalization, including which adapter templates ship in the v1.0 distribution vs. user-bring-your-own
- ADR-NN (Architect's lane): canonical context-package format aligned with Klatch L1-L5 + MCPB hybrid (Architect↔Daedalus conversation requested today)
- ADR-NN (Architect's lane): packaging-layer abstraction implementation
- Question for the next BYOC discovery cycle: when MCP successor standards emerge, do we ship multi-protocol packaging (one server, multiple bindings) or one-binding-at-a-time?

---

## Audit trail

- Vision V2.3 §"Bring Your Own Chat" + Pillar 7 + Strategic Pivot — canonical strategic direction (Apr 11)
- Predecessor PPM handoff §1 + Agent 360 §8.3 — flag as overdue (Apr 25)
- PPM Apr 26 scoping outline: `dev/2026/04/26/ppm-pdr-byoc-scoping-outline-2026-04-26.md`
- BYOC discovery thread opening: `mailboxes/ppm/sent/memo-ppm-to-pa-arch-cxo-cc-ceo-exec-byoc-discovery-thread-opening-2026-05-04.md`
- PA cross-pollination scan: `mailboxes/ppm/read/memo-pa-to-ppm-cc-arch-cxo-ceo-exec-byoc-cross-pollination-scan-2026-05-10.md`
- Architect feasibility-check ack: per May 4 BYOC distribution; folded into #1016 Phase 4
- CXO experience review ack: per May 4 BYOC distribution; ~2-3 weeks
- Architect↔Daedalus alignment conversation: requested today (`mailboxes/arch/inbox/memo-ppm-to-arch-cc-pa-cxo-ceo-exec-daedalus-alignment-conversation-request-2026-05-15.md`)
- MUX/UI 7-surface cohort convene: CXO May 15
- PPM MUX/UI Round 1 input: `mailboxes/cxo/inbox/mux-ui-gap-ppm-input-2026-05-15.md`

---

*DRAFT v0.1 | PPM | 2026-05-15 — opened for cohort iteration; not canonical until PM ratification*
