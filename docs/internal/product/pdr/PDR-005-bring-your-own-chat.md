# PDR-005: Bring Your Own Chat — Distribution Model

**Status**: APPROVED (v1.0 — PM-ratified 2026-06-05, conveyed via PA). Foundational PDR; joins PDR-001→004. Core decision rule (b: primary MCP delivery + thin bespoke UI; c: full client-portability as asymptotic target) ratified, validated by the skunkworks thin-BYOC PoC (#1145, rungs 1+2). EC-2 platform-affordance-bounded qualifier cohort-concurred (Arch + CXO + Lead); Comms external-language frame is scaffolding (PM retains the public-copy voice-pass; folds at v1.1). Unblocks Architect companion ADRs Q6 (canonical context-package format) + Q7 (packaging-layer abstraction).
**Author**: PPM
**Date**: 2026-06-03 (v0.6 supersedes v0.5 filed 2026-05-19)

## v0.6 changelog (vs. v0.5, May 19)

- **EC-2 qualified** — the platform-affordance-bounded qualifier folded into §Consequences-for-experience EC-2 (zero-tolerance still binds *how* a claimed capability behaves; *whether claimed at all* is conditionally-surfaced-per-host where the platform exposes the surface; invisible-by-default + honest-boundary-on-demand; Colleague-Test-verified). Synthesized from Arch (architecture lens) + CXO (experience lens), both qualifier-needed; CXO confirmed faithful.
- **AC-1 — surface-presence detection** added as the paired architectural mechanism (host-aware capability-claim map at the claim layer).
- **Q7 companion ADR** note: packaging layer carries the per-host capability-claim map, not just persona prose.
- **§Open questions item 11 (EC-2 qualifier)** — marked RESOLVED.
- **Lead Dev EC-2 read folded** — three-way classification (structural platform-bounded → qualifier; scope-bounded → zero-tolerance; not-yet-built → zero-tolerance). EC-2 fully cohort-concurred (Arch+CXO+Lead).
- **§External-Language Frame added** — Comms external-language frame folded (external principle + two-sided promise + on-the-boundary voice + BYOC positioning + anti-patterns; PM voice-pass final on outward copy).
- **Packaging model corrected** — line-376 context-package ADR note updated MCPB-hybrid → plugin model (PM 6/1 via PA).
- **CT v2.3.2** (canonical) cited throughout (was drift-cited "v2.4").
**Tier**: Foundational (PDR-005, alongside PDRs 001-004) — pending PM confirmation
**Supersedes**: None (new PDR; codifies Vision V2.3 §"Bring Your Own Chat")
**Related**: PDR-001 (FTUX), PDR-004 (Experience Philosophy), ADR-051 (RequestContext, #1015 Phase 4), ADR-054 (Cross-Session Memory), ADR-059 (Workflow Dispatcher), ADR-060 (Floor-First Routing), ADR-061 (LLM-touch boundary enforcement), ADR-062 (e2e Phase 0), ADR-063 (User-Facing Audit Envelope Read-Surface, the canonical Surface 7 ADR), ADR-064 (Search Index Architecture, Surface 5 pre-1.0), Vision V2.3 §BYOC + Pillar 7
**Predecessor flag**: PPM Apr 25 handoff §1 + Agent 360 §8.3

---

## v0.5 changelog (vs. v0.4, May 18)

- **§Consequences for experience** — full CXO fill-in absorbed (was `[INPUT PENDING: CXO]`); five experience commitments (EC-1 through EC-5) + identity coherence framework + cross-client transition + per-platform onboarding voice + "what experience layer does NOT do"
- **§Open questions** — item added: EC-2 capability-claim-consistency potential platform-affordance-bounded qualifier (CXO flagged for cohort flag-back); CT v2.5 identity-coherence sub-dimension proposed (pending PPM + HOST sign-off)
- **§Audit trail** — CXO §experience fill-in memo + CXO Surface 7 MUX doc v0.1 + Lead Dev Surface 2/4 queued ack added

---

## Context

### Why this PDR is needed

Vision V2.3 made BYOC canonical strategic direction (Apr 11, 2026). Vision-level treatment doesn't substitute for PDR-level codification: vision answers "where are we going"; PDRs answer "what must we build and why" with decision-rule specificity downstream ADRs can refer back to.

### Cross-project convergence as substrate

PA May 10 scan: **Klatch and Piper Morgan independently arrived at "products as services for agents" within 48 hours of each other** (PM Apr 8 BYOC, Klatch Apr 10 futures memo). Convergent evolution under common substrate pressure.

### Architecture has been quietly preparing for it

Architect May 15 feasibility check: **"BYOC isn't a leap; it's the next natural step."** Five structural decisions over 18 months produced a codebase where BYOC is mostly packaging + targeted refactors. AC-1 through AC-4 (below) name the architectural commitments that close the BYOC framing. ADR-062, ADR-063, ADR-064 landed May 16 in the ratified sequence.

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
- (c) "any surface supporting the protocol; client choice user-driven; server invariant" — **asymptotic target**

The "thin" qualifier is load-bearing. Anything that *can* live in chat *must* live in chat; web UI exists only for the surfaces meeting the 3-criterion test below.

**1.0 bespoke-UI surfaces are empirically scoped** (Round 2 CEO ratification): 5 of 7 MUX/UI surfaces (the 1.0-required subset) + concrete integration scope (GitHub + Calendar + Notion). Slack deferred. Anything beyond requires explicit re-scoping with PDR-005-precedent justification.

*(Roster and per-surface naming: `docs/internal/design/surfaces-taxonomy-2026-08-16.md`, ratified v1.0 2026-08-21. Surface 3 = F-Settings, CEO-ratified since May; prefer names to numbers — "Surface N" is ambiguous across three schemes.)*

### The 3-criterion "must be UI" test

**[DECISION]**: PDR-005 commits to a falsifiable test downstream ADRs apply per surface. A bespoke UI surface earns 1.0 inclusion only if it meets ≥1 of:

1. **Visual-state-essential** — communicates state that text-only representation loses meaningfully
2. **Multi-turn-coordination-cost-prohibitive** — chat-only flow exceeds ~3 user turns for what UI handles in one interaction
3. **Safety/audit-affordance** — affords visible state for safety-relevant interactions where ambiguity is unacceptable

Per CXO Round 1 synthesis: Surfaces 2/4/6/7 meet ≥1 criterion clearly; Surfaces 1/3 meet weaker forms (mostly criterion 1); Surface 5 doesn't strongly meet any (consistent with post-1.0 disposition).

### The mechanism set (Architect framing — "commit to mechanisms, not implementations")

PDR-005 commits to these mechanisms; specific implementations land in subsequent ADRs:

1. **Persona-template parameterization** — `persona_id` registry pattern, sibling to existing `task_type` registry
2. **MCP-server packaging alongside FastAPI** — both surfaces consume same domain layer; MCP server in `services/mcp/server/`
3. **RequestContext-based auth abstraction** — completes #1015 Phase 4 migration
4. **Audit envelope `host_id` field** — small schema addition for future-extensibility; cross-host audit semantic deferred
5. **Context-package format negotiated with sibling projects** — Klatch Daedalus alignment in flight

### Persona portability scope

**[DECISION: server-invariant persona core + per-client adapter templates; consistency contract = "same Piper" enforced via tiered variance hierarchy]**

Server holds persona core (capabilities, posture, ethics commitments per #992). Per-client adapter templates handle prompt-engineering variance for client-specific affordances.

**Variance hierarchy** (per CXO Flag 2; Pattern-064 prevention at persona layer):

| Layer | Variance budget | Enforcement |
|---|---|---|
| **Capability claims + ethics commitments** | **Zero tolerance** | Immutable from adapter scope; any per-platform variance is a Class A boundary violation |
| **Tone + voice register** | ≤5% per CT v2.3.2 rubric | CXO-calibrated; rubric-scored per platform |
| **Working memory references + context coordination** | ≤10% structural variance | Acceptable for platform-affordance differences |

The hierarchy is architecturally enforced via AC-1 (parameter-class separation); the experience layer §Consequences for experience translates these to observable user-facing commitments (EC-1 through EC-5).

### MCP server scope vs. client scope

**[DECISION: server holds working memory + tools + persistence + trust-graduation; client holds LLM + conversation surface + client-side history]**

- Conversation history: client-side primary; server-side reflective copy of *what Piper learned* lives in InsightJournal + ADR-054 Composted Learning layers
- Switching clients: same artifacts + same Piper-specific context; *not* the same conversation transcripts
- Cross-client persistence: opt-in only

**Cross-client memory continuity sub-surface obligations**:

- **Surface 1 (history)** needs a cross-client variant: *"what I learned about you across all hosts"*
- **Surface 6 (first-run)** needs a "welcome back" variant: explicit *"I remember [X about you]; I do not have our previous transcripts"* honesty surface

These fold into MUX/UI cohort Round 2 scoping; see §Consequences for experience §"Cross-client transition as an experience surface" for the experience-layer commitment.

### Bespoke UI commitment depth

**[DECISION: bespoke UI bound to today's 7 MUX/UI surfaces, 1.0-required subset, per the 3-criterion test; Round 2 CEO-ratified scope]**

Per Round 2 CEO ratification: 5 of 7 surfaces 1.0-required; 4 carry Class A Review Gate triggers. Concrete integration pick: **GitHub + Calendar + Notion; defer Slack**. Surface 5 (search) is post-1.0 with ADR-064 pre-1.0.

*(Roster and per-surface naming: `docs/internal/design/surfaces-taxonomy-2026-08-16.md`, ratified v1.0 2026-08-21. Surface 3 = F-Settings, CEO-ratified since May; prefer names to numbers — "Surface N" is ambiguous across three schemes.)*

Build sequencing (Lead Dev Phase 2 scoping memo, May 17):

- **Phase 2.1**: Surface 1 + Surface 7 — unblocked NOW; ~4-6 working days sequential
- **Phase 2.2**: Surface 2 + Surface 4 — **UNBLOCKED via PPM Surface-2-sufficient + Surface-4-sufficient signals May 18** (Lead Dev queued per ack May 18 ~10:45 PT); ~7-10 working days when bandwidth lands
- **Phase 2.3**: Surface 6 — anytime after Phase 2.1; ~2-3 working days

### Phase 2.2 PPM signal architecture (operational status)

**[DECISION: per-surface sufficient-signals from PPM to Lead Dev unblock Phase 2.2 build]**

Both signals shipped May 18 + Lead Dev confirmed receipt + Phase 2.2 build is now queued for PM cadence call (build start sequencing). Surface 2 and Surface 4 are independently unblocked; Lead Dev can start either or both per PM cadence.

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
- Phase 2.2 build window opens per-surface as PPM signals "Surface 2 unblocked" + "Surface 4 unblocked" (separate signals; both shipped May 18)

---

## Consequences for architecture (Architect fill-in, May 15)

### Architectural commitments

PDR-005's product commitments translate to four architectural commitments. These are constraints downstream ADRs and implementation work must design against; deviation requires explicit PDR-005-precedent justification.

#### AC-1 — Persona-template parameterization

PM commits to a **persona-registry pattern**: persona definitions are first-class typed entries dispatched at consumption, sibling to the existing `task_type` registry. The server holds a canonical persona core; per-client adapter templates are registered entries that load by client identifier.

**AC-1 addendum (variance hierarchy enforcement)**: adapter templates may override persona-core parameters at the tone-and-voice layer only; capability-claim and ethics-commitment parameters are immutable from adapter scope. Architectural enforcement: **separate parameter classes; adapter loading only binds tone-class parameters**.

**AC-1 surface-presence detection (paired mechanism for EC-2's platform-affordance-bounded qualifier, folded v0.6 2026-06-03)**: the persona core's capability map is **host-aware at the claim layer** — capabilities are conditionally claimable per host based on which capability surfaces the host structurally exposes. Surface-presence is detected at host-handshake / session-start (or via BYOC client configuration); the persona only surfaces capability claims the current host supports. This is the architectural truth-condition under EC-2's conditional-claim experience commitment — the AC-1↔EC-2 paired-lens arriving at the same contract from two sides. **Forward implication for Q7** (packaging-layer abstraction companion ADR, gated by v1.0): the packaging layer carries the **per-host capability-claim map**, not just persona prose.

**Closes the cross-client consistency contract architecturally** — both the immutability of claimed-capability *behavior* (parameter-class separation) and the host-awareness of *which* capabilities are claimable (surface-presence detection).

#### AC-2 — Packaging-layer abstraction

PM commits to an **internal protocol-binding interface** that decouples server logic from delivery-surface protocol. MCP-server-binding is one implementation; future bindings are additional implementations behind the same interface.

**Closes the swappable-packaging-layer commitment architecturally**.

#### AC-3 — Composted Learning input/output store separation

PM commits to ADR-054 Layer 3 operating on the **input-store / output-store / review-then-adopt** pattern from Anthropic Dreams reference architecture. Input working memory is never modified in place; consolidation passes produce candidate output stores; adopt-gate is explicit lifecycle step (per Pattern-070 cleanup-job-with-cancellation-hygiene).

**Closes the "Piper-learns-across-clients" commitment architecturally**.

#### AC-4 — Runtime adapter-template dispatch

PM commits to **runtime persona-template dispatch by client identifier**: the server detects which client surface is invoking the request and loads the corresponding adapter template at request time. Default to canonical persona core when no specific adapter is registered.

**Closes the per-client adaptation commitment architecturally**.

### Surface-7-specific architectural commitments (ADR-063)

ADR-063 (User-Facing Audit Envelope Read-Surface) IS the canonical Surface 7 ADR. Four-Element READ-Side Principle + field-bucket split + Pattern-071 (audit-as-attack-surface) architectural commitments. ADR-061 remains the four-element-boundary template reference for adjacent LLM-touch surfaces.

### Enabling work

- **#1015** — ADR-051 RequestContext Phase 4: P2; land before MCP server packaging
- **#1087** — SEC-JWT-SECRET-PROD-GUARD: P1, sequenced ahead of MCP packaging
- **#1075** — route-prefix migration: CLOSED May 16; Surface 4 callback URL stability dependency RESOLVED
- **Pattern-070 cleanup-job adoption** for the consolidation pipeline
- **Pattern-073 (Documentation-Asserted-Behavior Drift)** — doc-sync-sweep skill discipline applies during PDR-005 → ADR → implementation cycle

---

## Consequences for experience (CXO fill-in, May 18)

### Frame: "Same Piper" is a felt experience, not just architectural invariance

PDR-005's architectural mechanisms (AC-1 through AC-4) ensure that across MCP clients, FastAPI, and future protocol-bindings, the persona core is invariant and the variance hierarchy is enforced at the parameter-class boundary. That's the architectural truth-condition.

The experience layer carries the parallel commitment: **users perceive "same Piper" across clients through five experiential commitments PDR-005 binds the product to.** These are observable behaviors users encounter — what makes the architectural invariance felt rather than merely implemented.

### Five experiential commitments

#### EC-1 — Recognition continuity

Across clients, Piper recognizes the same things about the user (working-memory-layer surfacing per §MCP server scope). The recognition is **substrate-grounded** (InsightJournal + Composted Learning Layer 3 per AC-3); the surfacing is the experience layer.

**Surface implication**: Surface 1 (history) needs a cross-client variant — *"what I learned about you across all hosts"* — distinct from per-host conversation transcripts. Surface 6 (first-run) needs a "welcome back" variant for users arriving on a new client.

#### EC-2 — Capability claim consistency (Pattern-064 prevention at the experience layer)

Whatever Piper says it can do, it can do **identically** across clients. Capability-claim drift between clients is a Class A boundary violation regardless of measurement — same standard as the architectural enforcement (AC-1 addendum).

This is the **felt manifestation of zero-tolerance** for capability-claim variance from §Persona portability variance hierarchy.

**Surface implication**: integration setup wizards (Surface 4) and first-meeting greetings (Surface 6) carry capability-claim language; both must use canonical persona-core capability statements regardless of which client the user is on.

**Platform-affordance-bounded qualifier (folded v0.6, 2026-06-03 — cohort flag-back resolved):** Zero tolerance binds *how* a claimed capability behaves across hosts — if Piper claims capability X on hosts A and B, X behaves identically on both (same answer to the same question, same tool-use semantics, same accuracy). That is the Pattern-064 prevention surface and it holds without exception. What is **platform-affordance-bounded and acceptable** is *whether a capability is claimed at all* on a given host: capabilities are **conditionally surfaced per host** where the platform structurally supports the capability surface (e.g., Slack thread-summarization claimed only where threads exist; voice transcription only where an audio surface is present; file-reference only where a file surface exists), never universally claimed-then-degraded. **At the experience layer**, platform-absence is invisible by default — never offered, never claimed-then-withdrawn (claimed-then-degraded is the same felt shape as fabrication). **The one exception to silence** is where a user **reaches for** a capability they've met elsewhere in their Piper experience, Piper **names the platform boundary honestly in voice** (*"thread-summarizing is a Slack thing — this host doesn't give me threads to work with"*) — a boundary-explanation on demand, not a claim. **Verified at the felt layer via the Colleague Test** (claimed-then-degraded scores as the fabrication-family auto-fail).

**Three-way classification of capability deltas (Lead Dev integration read, folded 2026-06-03):**
- **Structural platform-bounded → qualifier applies (conditional-claim).** Genuine platform surface-area asymmetries: most notably **push / proactive-surfacing and real-time event-reactivity primitives** (Slack has DM/channel writes, scheduled messages, Socket Mode event triggers; **MCP is structurally request-response only** — no affordance for Piper to initiate a turn) and **channel/space semantics** (threads, channels, membership). "I'll proactively surface insights" is honorable on Slack, structurally impossible on MCP — claim it only where the host supports it. (The R4 / #1032 INSIGHT-PUSH work makes this push/pull asymmetry concrete: "ask me what I've learned" is claimable everywhere; "I'll surface things proactively" only on push-capable hosts.)
- **Scope-bounded → stays zero-tolerance (NOT platform-structural).** Capabilities gated by user-granted token scope (GitHub `workflow` scope, Slack admin scopes, Calendar write scope) are the *same capability shape* on every host — **same platform + same granted scope = same claim.** These are inside EC-2's zero-tolerance, not the qualifier's exception.
- **Our-side-not-yet-built → stays zero-tolerance.** A capability we simply haven't built is not platform-forced; it binds zero-tolerance.

The precise line: *"host capability" ≠ "host structural capability."* Only genuine structural affordance asymmetry (push/event/channel) earns the conditional-claim exception; scope-bounded and not-yet-built both stay zero-tolerance.

#### EC-3 — Ethics commitment invariance

The ethics commitments per #992 (PDR-004 P4 LLM-floor; ADR-061 four-element principle) are invariant across clients. Piper declines the same things, redacts the same patterns, and produces the same canonical canned response for category-violations (*"That came out wrong — let me try a different approach."* per #1017 Q3) across every client surface.

**Surface implication**: Surface 7 (error/degraded states) must render ethics decisions identically across clients. Voice register may adapt per platform (~5% tone budget); the underlying decision and the canned response phrasing are invariant.

#### EC-4 — Tone-and-voice variance budget within identity coherence

Tone and voice register may vary up to ≤5% per platform per CT v2.3.2 rubric (per §Persona portability variance hierarchy). The variance is **calibrated and bounded**, not unconstrained. Identity remains coherent.

The 5% budget allows per-platform affordance adaptation:
- **MCP/Claude Desktop**: turn-based register; can use longer thoughtful prose
- **Slack** (post-1.0): thread-aware register; shorter, more colloquial; emoji-aware
- **Calendar adapter** (within integration surfaces): brief, structured prose; minimal narrative
- **GitHub adapter** (within integration surfaces): technical register; code-aware

Within the 5% budget, voice register adapts to platform context. Beyond it, identity coherence breaks; the variance hierarchy fires.

**Surface implication**: per-surface MUX docs name the voice register for that surface. The 5% budget operates at the adapter-template layer, scored via CT v2.3.2 rubric.

#### EC-5 — Context-coordination continuity across affordance differences

Working-memory references and context-coordination may vary up to ≤10% structurally to accommodate platform affordances. Piper's references adapt to the affordance, but the *underlying context-coordination* (what Piper knows, when it surfaces it, how it confirms it) is invariant.

**Surface implication**: the cross-client variants of Surface 1 (history) and Surface 6 (welcome-back) operationalize this commitment.

### Variance budget hierarchy at the experience layer

| Layer | What the user observes |
|---|---|
| **Capability claims + ethics commitments** (zero tolerance) | The user sees identical capability statements and identical ethics decisions across clients. Drift is a Class A violation. |
| **Tone + voice register** (≤5% per CT v2.3.2) | The user perceives platform-appropriate register variations within a single coherent identity. Slack-Piper feels like Slack; Claude-Desktop-Piper feels like Claude Desktop; both feel like Piper. |
| **Working memory + context coordination** (≤10% structural) | The user experiences platform-affordance-appropriate reference patterns. Thread context where threads exist; turn context where they don't. Working memory invariant; surfacing pattern adapts. |

The hierarchy is enforced architecturally (AC-1 parameter-class separation); the experience layer specifies the **observable design commitments** the enforcement produces.

### Colleague Test scoring criteria for cross-client adaptation

The Colleague Test rubric (CT v2.3.2) provides the calibrated scoring framework for cross-client adaptation. Three rubric dimensions specifically apply at the cross-client boundary:

1. **Identity coherence** (new sub-dimension; pending CT v2.5 or amendment): does the user encountering Piper on Client B recognize the same Piper they encountered on Client A?
2. **Capability claim consistency** (Class A boundary check): are Piper's stated capabilities identical across clients?
3. **Voice register appropriateness**: does the per-platform tone register fit the affordance without breaking identity coherence?

When CT scoring lands on cross-client adapter templates (post-1.0; per §Persona portability "demand-gated"), these three dimensions are the load-bearing criteria.

### Identity coherence framework

**Three identity invariants** (must hold across all clients; not subject to the 5% budget):

1. **The colleague stance** — Piper relates to the user as a colleague, not as a system (PDR-004 P1)
2. **The offer-first posture** — Piper offers; the user decides (PDR-004 P2)
3. **The honest-about-limits voice** — Piper acknowledges what it doesn't know and what it can't do, with alternatives

**Three identity variables** (may adapt within the 5% budget):

1. **Conversational tempo** — turn pace, response length, narrative density
2. **Platform-native idiom usage** — Slack-emoji, GitHub-codeblock-formatting, Calendar-time-natural-language
3. **Affordance-specific phrasing** — *"in this thread"* vs. *"in our conversation"* depending on platform context

### Cross-client transition as an experience surface

When a user moves from Client A to Client B, the *transition itself* is an experience surface. Two MUX surfaces own that moment:

**Surface 1 (cross-client variant)** — *"what I learned about you across all hosts"*: a dedicated view (TBD per MUX doc work) showing the working-memory-layer state independent of per-host transcripts.

**Surface 6 (welcome-back variant)** — for users arriving on a new client where Piper has prior recognition substrate: explicit *"I remember [X about you]; I do not have our previous transcripts"* honesty surface.

**Voice register for the cross-client transition** (preview; full content in Surfaces 1 + 6 MUX docs):
- Honest about what carried over: name specific things Piper knows
- Honest about what didn't: no fake recall of previous transcripts
- Offer-first close: invite the user to either continue from what Piper remembers or start fresh

**Anti-pattern**: implicit recall (*"As we discussed last week..."*) that requires conversation-history continuity. Piper does not have client-A conversation history when arriving on client B; pretending otherwise is identity drift toward dishonest-about-limits.

### Per-platform onboarding voice considerations

Surface 6 (first-meeting greetings) is templated, not LLM-touch (per Round 2 CEO-ratified Architect correction). Templates may vary per platform within the 5% tone budget; the underlying first-meeting *content* (what Piper tells the user about itself + what it does + how to engage) is invariant.

Templates by platform affordance (preview; full content in Surface 6 MUX doc, Phase 2.3):

| Platform | Voice register | First-meeting prose shape |
|---|---|---|
| MCP/Claude Desktop (1.0) | Conversational, turn-based, narrative-rich | Welcome + capability summary + offer-first close in 3-4 sentences |
| Slack (post-1.0) | Thread-aware, briefer, emoji-aware | Welcome + capability summary + offer-first close in 2-3 sentences; can use 1-2 light emoji per platform convention |
| Calendar adapter (Phase 2.2) | Structured, minimal narrative | Welcome + scope (calendar-specific) + offer-first close in 1-2 sentences |
| GitHub adapter (Phase 2.2) | Technical register, code-aware | Welcome + scope (repo-specific) + offer-first close in 1-2 sentences; can reference recent activity if available |

### What this commits the experience layer to NOT do

Per the 5 PDR commitments to avoid, the experience layer mirrors:

1. **Not promising "same rendering" across clients** — each host's UI affordances differ; Piper's identity is invariant, not its visual treatment
2. **Not implementing platform-specific personas** — adapter templates handle per-platform variance within the 5% budget; full per-platform personas (different voice cores) would violate AC-1
3. **Not committing to all-clients-launch-day** — per-platform adapter templates are demand-gated
4. **Not implementing unified cross-host conversation history surface** — the cross-client variant of Surface 1 surfaces *what Piper learned* (working memory), not per-host conversation transcripts
5. **Not requiring per-platform UX research before 1.0** — adapter templates ship with thoughtful first-meeting templates and tone-budget-bounded variance; deeper per-platform UX research is post-1.0 expansion

---

## Alternatives considered

- Bespoke web UI primary: rejected (standard SaaS; loses substrate-convergence advantage)
- Native apps per platform: rejected (rebuilding N times; loses persona portability)
- Hybrid (chat input, web UI output): rejected (bifurcates the conversation)
- MCP-only (option (a)): rejected this cycle (5 1.0-required MUX surfaces show some bespoke UI is 1.0-necessary)

---

## External-Language Frame (BYOC / EC-2 — Comms, folded 2026-06-03)

How the EC-2 contract reads *beyond the cohort* — to users, in docs, in positioning. **Comms-proposed scaffolding; final public phrasing is PM-ratified at the v1.0 voice-pass** (this unblocks v1.0; it does not pre-empt PM's outward-copy voice).

**External principle (one line):** *"Piper is the same colleague everywhere you work — it only offers what each place can actually do, and it's honest about the edges."* (Carries the whole contract: *same colleague* = persona invariance; *what each place can do* = platform-affordance-bounded claims; *honest about edges* = boundary-on-demand, never claimed-then-degraded.)

**Two-sided promise (both halves, always together — either alone misleads):**
1. **Constancy** — "Wherever you bring Piper, it's the same Piper. Same judgment, same values, same way of working. Not a different bot per app." (The BYOC value prop / marketing hook.)
2. **Honest-edge** — "Piper only offers what your platform actually supports; if you ask for something this place can't do, it tells you why, plainly." (The Pattern-064 / no-fabrication commitment, externalized — what keeps the hook truthful.) **Never ship the constancy claim without the honest-edge half.**

**On-the-boundary voice** (colleague naming a boundary, not a system reporting an error; locates the limit in the *platform*, not in Piper; **only on demand**, never volunteered): *"Thread-summarizing is a Slack thing — this host doesn't give me threads to work with."* / *"I'd need an audio surface to transcribe, and this place doesn't have one."* / *"No file surface here — bring it into the chat and I'm good."*

**BYOC positioning:** *"Bring Piper to where you already work."* — same colleague in every room, fluent in what each room affords. Prefer "the same Piper, at home in each tool"; **avoid** "works identically everywhere" / "full capabilities on every platform" (the overclaim EC-2 prevents).

**External anti-patterns (flag in any outward copy):** ❌ "identical capabilities on every platform" · ❌ framing a platform-absent capability as a *Piper* limitation (locate it in the platform) · ❌ burying platform variation in fine print / a feature-matrix asterisk (honesty is in-voice, on-demand) · ❌ claimed-then-degraded · ❌ marketing the boundary-explanation itself as a feature (it's quiet honesty, not a selling point).

*Continuous with the canonical voice spines (colleague-not-system, honest-about-limits, no-fabrication, offer-first) + the "When Your AI Makes Things Up" insight — EC-2 external language is those spines applied to the cross-host case.*

---

## Open questions

1. **Audit semantics decision** (cross-host unified vs. per-host) — CEO + HOST input; deferred to follow-up ADR
2. **Per-host persona-template authoring lifecycle** — CXO lane; deferred post-1.0
3. **Klatch Daedalus alignment cadence** — in flight; Architect-authored brief filed for Janus relay (May 15)
4. **#1087 SEC-JWT-SECRET-PROD-GUARD priority** — PPM committed P1, sequenced ahead of MCP packaging
5. **PDR-006 (post-1.0)**: per-platform persona variance budget formalization
6. **ADR (Architect's lane)**: canonical context-package format aligned with Klatch L1-L5, packaged within the **plugin model** (the plugin is the canonical Anthropic package — config + CLAUDE.md + skills + MCP server; MCPB/hosted-MCP are not the packaging unit, per PM 6/1 clarification)
7. **ADR (Architect's lane)**: packaging-layer abstraction implementation
8. ~~ADR-NN slot for User-Facing Audit Envelope Read-Surface~~ — RESOLVED: ADR-063 is the canonical Surface 7 ADR
9. **Pattern-073 Documentation-Asserted-Behavior Drift discipline** — doc-sync-sweep skill runs after each surface ships during MUX/UI Phase 2 build
10. **Multi-Agent API characterization** (post-v0.5 PPM session) — per CIO May 18 Anthropic Outcomes disposition memo
11. **EC-2 platform-affordance-bounded qualifier** — **RESOLVED 2026-06-03.** Cohort flag-back sent 6/3; Arch + CXO both surfaced genuine platform-forced examples → qualifier-needed; PPM synthesized the qualifier; CXO confirmed faithful ("take it to PM"). **Folded into EC-2 + paired AC-1 surface-presence detection (this v0.6).** **FULLY cohort-concurred: Arch + CXO + Lead all concur** (Lead's structural-vs-scope-bounded classification folded). Comms external-language frame folded (see §External-Language Frame). EC-2 fully closed.
12. **CT v2.5 identity-coherence sub-dimension** (proposed by CXO; pending PPM + HOST sign-off) — if landed wrong, EC-1 + the identity-coherence-framework framing adapts

---

## Audit trail

- Vision V2.3 §"Bring Your Own Chat" + Pillar 7 (Apr 11)
- PPM Apr 26 scoping outline: `dev/2026/04/26/ppm-pdr-byoc-scoping-outline-2026-04-26.md`
- BYOC discovery thread opening (May 4): `mailboxes/ppm/sent/`
- PA cross-pollination scan (May 10): `mailboxes/ppm/read/`
- Architect feasibility check (May 15): `mailboxes/ppm/read/`
- Architect §Consequences for architecture fill-in (May 15)
- CXO PDR-005 v0.2 review (May 15)
- Architect MUX/UI Round 1 cohort response + PDR-005 v0.2 concur (May 15)
- CXO MUX/UI Round 1 + Round 2 synthesis (May 15)
- Architect↔Daedalus alignment brief (May 15, filed for Janus relay)
- Anthropic Dreams architectural review (May 15)
- MUX/UI Round 2 CEO ratification (May 16)
- Lead Dev MUX/UI Phase 2 scoping (May 17)
- PM v0.4 proceed-now decision (May 18)
- PM CXO greenlight natural-pace experience (May 18)
- CIO Anthropic Outcomes platform-productization disposition (May 18)
- PPM Surface 2 + Surface 4 sufficient-signal memos to Lead Dev (May 18)
- **CXO §Consequences for experience fill-in (May 18)**: `mailboxes/ppm/read/memo-cxo-to-ppm-cc-arch-comms-lead-pa-ceo-exec-pdr-005-consequences-for-experience-fill-in-2026-05-18.md`
- **CXO Surface 7 MUX doc v0.1 handoff to Comms (May 18)**: `mailboxes/ppm/read/memo-cxo-to-comms-cc-arch-ppm-lead-pa-ceo-exec-surface-7-mux-doc-v0.1-handoff-2026-05-18.md`
- **Lead Dev Outcomes concur + Surfaces 2/4 queued (May 18)**: `mailboxes/ppm/read/memo-lead-to-cio-ppm-cc-ceo-cxo-arch-host-exec-comms-pa-outcomes-concur-absorbed-plus-surfaces-2-and-4-queued-2026-05-18.md`
- #1087 SEC-JWT-SECRET-PROD-GUARD (May 14)
- #1075 route-prefix migration CLOSED (May 16)
- ADR-062, ADR-063, ADR-064 (May 16)
- Pattern-070, Pattern-071, Pattern-073 (May 16)

---

## Readiness for v1.0 ratification

v0.5 absorbs all currently-pending substantive inputs. Remaining gates before v1.0 (canonical PDR landing at `docs/internal/product/pdr/PDR-005-bring-your-own-chat.md`):

1. **Cohort flag-back on EC-2 platform-affordance-bounded qualifier** (item 11) — PPM-driven; ~1 week soft cadence
2. **CT v2.5 identity-coherence sub-dimension** (item 12) — CXO + HOST + PPM coordination; can land in v1.1 if needed
3. **Comms external-language frame** (still `[INPUT PENDING: Comms]`) — Comms cadence
4. **PM ratification** — final gate

v0.5 → v1.0 transition is on the table once items 1 + 3 + 4 close (item 2 can defer to v1.1 if needed).

---

*DRAFT v0.6 | PPM | 2026-06-03 — EC-2 platform-affordance-bounded qualifier folded; all three lenses in (Arch architecture + CXO experience + Lead Dev integration's structural-vs-scope-bounded classification) + paired AC-1 surface-presence detection + Q7 note. Remaining v1.0 gates: Comms external-language frame + PM ratification. Not canonical until PM ratification.*
