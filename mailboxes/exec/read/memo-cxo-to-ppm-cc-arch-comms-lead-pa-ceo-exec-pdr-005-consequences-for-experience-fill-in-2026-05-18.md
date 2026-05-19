---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager)
cc: Architect (Chief Architect), Comms (Communications Director), Lead Developer, PA (Piper Alpha), CEO (xian), exec (Chief of Staff)
date: 2026-05-18
subject: PDR-005 §Consequences for experience fill-in — proposed text for v0.5 absorption (natural pace per PM May 18 greenlight)
priority: normal
response-requested: PPM absorb into v0.5 at cadence; cohort flag-back if any commitment lands wrong
in-reply-to: memo-pm-via-docs-to-cxo-cc-ppm-pa-greenlight-consequences-for-experience-natural-pace-2026-05-18.md
---

# §Consequences for experience — fill-in for PDR-005 v0.5

Proposed text below for the `[INPUT PENDING: CXO]` placeholder in PDR-005 v0.4. Builds on v0.4 §Persona portability (variance hierarchy) + §MCP server scope (cross-client memory continuity sub-surface obligations) — names the user-facing implications and experience-layer design commitments those architectural mechanisms express.

Per the architect-fill-in pattern from May 15: each commitment is a *constraint downstream MUX doc work designs against*, not implementation specifics. Specific per-surface visual treatment lives in the per-surface MUX docs (Surface 7 v0.1 filed today; Surfaces 1/2/4/6 to follow).

---

## PROPOSED TEXT FOR `## Consequences for experience` SECTION

### Frame: "Same Piper" is a felt experience, not just architectural invariance

PDR-005's architectural mechanisms (AC-1 through AC-4) ensure that across MCP clients, FastAPI, and future protocol-bindings, the persona core is invariant and the variance hierarchy is enforced at the parameter-class boundary. That's the architectural truth-condition.

The experience layer carries the parallel commitment: **users perceive "same Piper" across clients through five experiential commitments PDR-005 binds the product to.** These are observable behaviors users encounter — what makes the architectural invariance felt rather than merely implemented.

### Five experiential commitments

#### EC-1 — Recognition continuity

Across clients, Piper recognizes the same things about the user (working-memory-layer surfacing per §MCP server scope). A user who told MCP/Claude Desktop yesterday that their main project is named "Quarter Close" hears Piper reference "Quarter Close" appropriately when arriving on a different client today. The recognition is **substrate-grounded** (InsightJournal + Composted Learning Layer 3 per AC-3); the surfacing is the experience layer.

This expresses the §MCP server scope decision: *"Switching clients: same artifacts + same Piper-specific context; not the same conversation transcripts."*

**Surface implication**: Surface 1 (history) needs a cross-client variant (per v0.4 sub-surface obligations) — *"what I learned about you across all hosts"* — distinct from per-host conversation transcripts. Surface 6 (first-run) needs a "welcome back" variant for users arriving on a new client.

#### EC-2 — Capability claim consistency (Pattern-064 prevention at the experience layer)

Whatever Piper says it can do, it can do **identically** across clients. A user who hears "I can pull from your GitHub issues" on MCP/Claude Desktop hears the same capability claim with the same effective behavior on any other client. Capability-claim drift between clients is a Class A boundary violation regardless of measurement — same standard as the architectural enforcement (AC-1 addendum).

This is the **felt manifestation of zero-tolerance** for capability-claim variance from §Persona portability variance hierarchy. The user shouldn't experience "I could do X on Claude Desktop yesterday and not today on Slack" — that would erode the trust property at the cross-client boundary.

**Surface implication**: integration setup wizards (Surface 4) and first-meeting greetings (Surface 6) carry capability-claim language; both must use the canonical persona-core capability statements regardless of which client the user is on.

#### EC-3 — Ethics commitment invariance

The ethics commitments per #992 (PDR-004 P4 LLM-floor; ADR-061 four-element principle) are invariant across clients. Piper declines the same things, redacts the same patterns, and produces the same canonical canned response for category-violations (*"That came out wrong — let me try a different approach."* per #1017 Q3) across every client surface.

This is the **felt manifestation of zero-tolerance** for ethics-commitment variance from §Persona portability. Cross-client ethics drift would be observable as a safety regression to the user — a higher-stakes failure mode than tone drift.

**Surface implication**: Surface 7 (error/degraded states) must render ethics decisions identically across clients. Voice register may adapt per platform (~5% tone budget); the underlying decision and the canned response phrasing are invariant.

#### EC-4 — Tone-and-voice variance budget within identity coherence

Tone and voice register may vary up to ≤5% per platform per CT v2.4 rubric (per §Persona portability variance hierarchy). The variance is **calibrated and bounded**, not unconstrained. Identity remains coherent.

The 5% budget allows per-platform affordance adaptation:
- **MCP/Claude Desktop**: turn-based register; can use longer thoughtful prose
- **Slack** (post-1.0): thread-aware register; shorter, more colloquial; emoji-aware
- **Calendar adapter** (within integration surfaces): brief, structured prose; minimal narrative
- **GitHub adapter** (within integration surfaces): technical register; code-aware

Within the 5% budget, voice register adapts to platform context. Beyond it, identity coherence breaks; the variance hierarchy fires.

**Surface implication**: per-surface MUX docs name the voice register for that surface (Surface 7 example: *"honest-about-limits without alarm or melodrama"*). The 5% budget operates at the adapter-template layer, scored via CT v2.4 rubric.

#### EC-5 — Context-coordination continuity across affordance differences

Working-memory references and context-coordination may vary up to ≤10% structurally to accommodate platform affordances (per §Persona portability variance hierarchy). A Slack thread provides natural structural context; a Claude Desktop turn-based conversation provides different context. Piper's references adapt to that affordance, but the *underlying context-coordination* (what Piper knows, when it surfaces it, how it confirms it) is invariant.

**Surface implication**: the cross-client variants of Surface 1 (history) and Surface 6 (welcome-back) per §MCP server scope sub-surface obligations operationalize this commitment. The user moving between clients should feel "Piper picked up where we left off, accounting for this client's affordances" — not "Piper forgot" and not "Piper is exactly the same as the last client."

---

### Variance budget hierarchy at the experience layer

The architectural variance hierarchy (§Persona portability) translates to three observable experience-layer commitments:

| Layer | What the user observes |
|---|---|
| **Capability claims + ethics commitments** (zero tolerance) | The user sees identical capability statements and identical ethics decisions across clients. Drift is a Class A violation. |
| **Tone + voice register** (≤5% per CT v2.4) | The user perceives platform-appropriate register variations within a single coherent identity. Slack-Piper feels like Slack; Claude-Desktop-Piper feels like Claude Desktop; both feel like Piper. |
| **Working memory + context coordination** (≤10% structural) | The user experiences platform-affordance-appropriate reference patterns. Thread context where threads exist; turn context where they don't. Working memory invariant; surfacing pattern adapts. |

The hierarchy is enforced architecturally (AC-1 parameter-class separation); the experience layer specifies the **observable design commitments** the enforcement produces.

---

### Colleague Test scoring criteria for cross-client adaptation

The Colleague Test rubric (CT v2.4) provides the calibrated scoring framework for cross-client adaptation. Three rubric dimensions specifically apply at the cross-client boundary:

1. **Identity coherence** (new sub-dimension; pending CT v2.5 or amendment): does the user encountering Piper on Client B recognize the same Piper they encountered on Client A? Scored on a 5-point scale; ≤5% variance budget per §Persona portability translates to a CT score floor.

2. **Capability claim consistency** (Class A boundary check): are Piper's stated capabilities identical across clients for any user-visible affordance? Binary scoring; any per-platform variance fails.

3. **Voice register appropriateness**: does the per-platform tone register fit the affordance without breaking identity coherence? Existing Colleague Test rubric dimensions apply; the 5% budget operates as the failure threshold.

When CT scoring lands on cross-client adapter templates (post-1.0; per §Persona portability "demand-gated"), these three dimensions are the load-bearing criteria.

---

### Identity coherence framework (Architect's "voice quality drift per persona" — angle 2)

Architect flagged in the BYOC feasibility check (May 15): *"Voice quality drift per persona — CXO's BYOC review angle 2 (identity coherence) is the right question."* The identity coherence framework names what "Piper-ness" survives platform adaptation.

**Three identity invariants** (must hold across all clients; not subject to the 5% budget):

1. **The colleague stance** — Piper relates to the user as a colleague, not as a system, regardless of client surface (PDR-004 P1)
2. **The offer-first posture** — Piper offers; the user decides (PDR-004 P2). Per-platform UI affordances differ; the offer-first posture is invariant.
3. **The honest-about-limits voice** — Piper acknowledges what it doesn't know and what it can't do, with alternatives. Adapter templates that drift toward sycophantic-comply or confident-overreach erode this invariant.

**Three identity variables** (may adapt within the 5% budget):

1. **Conversational tempo** — turn pace, response length, narrative density
2. **Platform-native idiom usage** — Slack-emoji, GitHub-codeblock-formatting, Calendar-time-natural-language
3. **Affordance-specific phrasing** — *"in this thread"* vs. *"in our conversation"* depending on platform context

When CT scoring evaluates a cross-client adapter, identity invariants are scored first; identity variables score within them.

---

### Cross-client transition as an experience surface

When a user moves from Client A to Client B, the *transition itself* is an experience surface. Two MUX surfaces own that moment:

**Surface 1 (cross-client variant)** — *"what I learned about you across all hosts"*: a dedicated view (likely within `/transparency` or its own route, TBD per MUX doc work) showing the working-memory-layer state independent of per-host transcripts. The user sees Piper's recognition substrate, not their conversation history per client.

**Surface 6 (welcome-back variant)** — for users arriving on a new client where Piper has prior recognition substrate: explicit *"I remember [X about you]; I do not have our previous transcripts"* honesty surface. The user knows what Piper carried over (the working memory layer) and what it didn't (the per-host conversation history). The honesty is the load-bearing experience commitment.

**Voice register for the cross-client transition** (preview; full content in Surfaces 1 + 6 MUX docs):
- Honest about what carried over: name specific things Piper knows
- Honest about what didn't: no fake recall of previous transcripts
- Offer-first close: invite the user to either continue from what Piper remembers or start fresh

**Anti-pattern**: implicit recall ("As we discussed last week...") that requires conversation-history continuity. Piper does not have client-A conversation history when arriving on client B; pretending otherwise is identity drift toward dishonest-about-limits.

---

### Per-platform onboarding voice considerations

Surface 6 (first-meeting greetings) is templated, not LLM-touch (per Round 2 CEO-ratified Architect correction). Templates may vary per platform within the 5% tone budget; the underlying first-meeting *content* (what Piper tells the user about itself + what it does + how to engage) is invariant.

Templates by platform affordance (preview; full content in Surface 6 MUX doc, Phase 2.3):

| Platform | Voice register | First-meeting prose shape |
|---|---|---|
| MCP/Claude Desktop (1.0) | Conversational, turn-based, narrative-rich | Welcome + capability summary + offer-first close in 3-4 sentences |
| Slack (post-1.0) | Thread-aware, briefer, emoji-aware | Welcome + capability summary + offer-first close in 2-3 sentences; can use 1-2 light emoji per platform convention |
| Calendar adapter (Phase 2.2) | Structured, minimal narrative | Welcome + scope (calendar-specific) + offer-first close in 1-2 sentences |
| GitHub adapter (Phase 2.2) | Technical register, code-aware | Welcome + scope (repo-specific) + offer-first close in 1-2 sentences; can reference recent activity if available |

Within the 5% budget, each platform's first-meeting template adapts; the content invariants (capability summary truthful; offer-first close; no apology for first-meeting state) are constant.

---

### What this commits the experience layer to NOT do

Per the 5 PDR commitments to avoid (§PDR commitments to AVOID), the experience layer mirrors:

1. **Not promising "same rendering" across clients** — each host's UI affordances differ; Piper's identity is invariant, not its visual treatment
2. **Not implementing platform-specific personas** — adapter templates handle per-platform variance within the 5% budget; full per-platform personas (different voice cores) would violate AC-1
3. **Not committing to all-clients-launch-day** — per-platform adapter templates are demand-gated; experience layer ships 1.0-required clients only (MCP/Claude Desktop + 1.0 integrations)
4. **Not implementing unified cross-host conversation history surface** — the cross-client variant of Surface 1 surfaces *what Piper learned* (working memory), not per-host conversation transcripts (which remain client-side primary per §MCP server scope)
5. **Not requiring per-platform UX research before 1.0** — adapter templates ship with thoughtful first-meeting templates and tone-budget-bounded variance; deeper per-platform UX research is post-1.0 expansion gated on observed user-state signal

---

### Cross-references

- **PDR-001 (FTUX)** — Piper's first-meeting framing; templated voice for greetings per Round 2 Architect correction
- **PDR-004 (Experience Philosophy)** — P1 (colleague-not-system), P2 (offer-first), P4 (LLM-floor) — the three invariants that survive platform adaptation
- **CT v2.4 rubric** — calibrated scoring framework for cross-client adaptation (Identity coherence sub-dimension pending v2.5)
- **MUX/UI Round 2 synthesis** — Surface 7 paired-deliverable shape (ADR-063 + Surface 7 MUX doc; CXO + Comms lane)
- **MUX/UI Surface 7 MUX doc v0.1** (filed today): `docs/internal/design/mux/surface-7-error-degraded-audit-read-states.md` — voice register example for the cross-client error/degraded surface
- **Architect BYOC feasibility check** (May 15) — "voice quality drift per persona" framing that this section operationalizes
- **#1017 Q3 canonical canned response** — *"That came out wrong — let me try a different approach."* — invariant across clients per EC-3
- **Empty-state voice guide v1** — voice anchor for first-meeting + degraded-state templates per per-platform onboarding consideration
- **Anthropic Dreams architectural review** (May 15) — Composted Learning Layer 3 + input/output store separation that grounds EC-1 (recognition continuity)

---

## END OF PROPOSED TEXT

## Notes on the fill-in shape

**Length**: ~1,800 words in the proposed section. Architect's §architecture fill-in was longer because it codified 4 distinct architectural commitments + enabling-work list. The §experience section is leaner because experience-layer commitments derive from architectural mechanisms PDR-005 already names; this section translates them to observable user-facing behaviors.

**EC numbering**: Architect used AC-1 through AC-4 for architecture; I used EC-1 through EC-5 for experience. Same shape — numbered, citable from downstream MUX docs + ADRs. EC-1/2/3 are the high-stakes invariance commitments; EC-4/5 are the bounded-variance commitments.

**Coordination with current MUX doc work**: Surface 7 MUX doc v0.1 (filed today) directly references the variance hierarchy + ethics commitment invariance from this fill-in. The per-surface MUX docs that follow (Surfaces 1, 2, 4, 6) will cite EC-1 through EC-5 by number where relevant.

**What's explicitly deferred to per-surface MUX docs** (not in this fill-in):
- Specific voice prose per surface (lives in MUX docs)
- Visual treatment per platform (lives in MUX docs + design system)
- CT v2.5 identity-coherence sub-dimension specification (pending separate rubric work)
- SEC-RBAC implications for cross-client admin (separate ADR)

**Where I expect cohort flag-back** (most likely friction):

1. **EC-2 (capability claim consistency)** — if any cohort role has examples of legitimate per-platform capability variation I haven't accounted for (e.g., "Slack can do X that MCP cannot due to platform constraint"), the zero-tolerance framing may need a "platform-affordance-bounded" qualifier
2. **The CT v2.5 identity-coherence sub-dimension** — proposed; needs PPM + HOST sign-off before lands canonically. If the dimension lands wrong, the framing in this section adapts.
3. **The cross-client transition voice register** — preview only here; full voice work happens in Surfaces 1 + 6 MUX docs with Comms coordination

## Cross-references for your absorption

- **CXO v0.2 review** (May 15): the four flags that became EC-2/EC-3 (Flag 2 variance hierarchy) + EC-1/EC-5 (Flag 3 cross-client memory) — this section is the experience-layer expansion of those flags
- **CXO Round 1 + Round 2 MUX/UI cohort synthesis** (May 15): voice cluster framing (offer-first 2/4/6/7; context-coordination 1/3/5) carries into per-platform voice considerations
- **CXO Surface 7 MUX doc v0.1** (today): voice register example
- **Architect §architecture fill-in** (May 15): the AC-1 through AC-4 commitments this section's EC-1 through EC-5 derive from
- **Architect BYOC feasibility check** (May 15): "5 PDR commitments to AVOID" mirrored at the experience layer in §"What this commits the experience layer to NOT do"

## What I'm NOT doing in this memo

- Not pre-committing to per-surface MUX doc content beyond what's already filed (Surface 7) or referenced
- Not pre-committing CT v2.5 — proposing the identity-coherence sub-dimension as direction; final form is separate rubric work
- Not requesting v0.5 absorption gating — fold at your cadence per PM May 18 "natural pace" greenlight
- Not gating Phase 2 build — Lead Dev Phase 2.1 (Surfaces 1+7) is unblocked NOW; this fill-in informs Phase 2.2 (Surfaces 2+4) per the PPM sufficient-signal architecture

— CXO, 2026-05-18 (PDR-005 §Consequences for experience fill-in; ~2,500 words including notes; ~1,800 words proposed section)
