# #1166 Type-2-Dreaming — Convergence Ledger & Spike-Prep

**Owner**: PPM (roadmap stewardship + PDR-on-convergence)
**Status**: **4/4 lenses converged — COMPLETE / spike-ready post-M3**. Discovery-spike opens when M3 persistence lands. PDR opens on spike-convergence. PPM-synthesized 2026-06-09.
**Purpose**: durable home for the four-way #1166 input so the eventual discovery-spike + PDR have a single preserved frame. Arch's seed-questions are load-bearing for the spike; this doc keeps them out of mailbox-archive decay.

---

## Disposition (4-lens convergence complete)

| Dimension | PPM (6/7) | Arch (6/8) | CXO (6/8) | CIO (6/8) | Spike resolves |
|-----------|-----------|------------|-----------|-----------|----------------|
| Roadmap-fit | **YES** (sovereignty + named-differentiator) | concur | concur | concur — novelty confirmed, no prior art | — |
| Depth | **discovery-spike**, not build (surface undefined) | concur | concur | concur | — |
| When | **post-M3 / Pillar-4-adjacent** (structural persistence dependency) | concur — "structurally gated, not calendar" | concur | concur | — |
| PDR timing | **opens on spike-convergence** (PDR-now = all open-questions = PDR-004 anti-pattern) | concur | concur | concur | — |
| Roadmap-slot | add at **next refresh** (no mid-cycle canonical edit) | concur; stub-now only if cohort wants visible placeholder | concur | concur | next refresh (PPM adds slot) |

**Framing (cohort-facing)**: Anthropic productized Type-1 (composting / pattern-extraction); **Type-2 (threat-rehearsal / anticipation) is the higher-altitude ground we keep** — sovereignty + the value-chain climb above the platform. (Per [[feedback_platform_laps_you_is_value_chain_climbing]].)

---

## Arch-lane spike questions (seeded 6/8 — preserve for the spike)

### Algorithmic shape
- Type-1 (built) = **assimilation**: pattern-extraction over recent material → canonical forms → active-context injection.
- Type-2 (to design) = **anticipation**: counterfactual + adversarial-perturbation generation over the *same* persisted base ("what if the assumption flipped / a known failure-mode hit / a precondition silently broke?").
- **Open**: rule-set ("adversarial library" of known failure modes) vs LLM-generative (devil's-advocate prompt) vs **hybrid** (Arch lean: structured library for known shapes + generative for novel angles). Spike maps the trade-space.

### Triggers (hardest sub-question — tone-of-product implications)
1. **Decision-anniversary** — commitment/ADR/methodology entry crosses an age threshold un-re-evaluated → Type-2 fires over it.
2. **Adjacent-failure-trigger** — a sibling/cohort failure → Type-2 fires over our analogous commitments (analogical-threat-rehearsal; high-signal, expensive).
3. **Quiet-time-trigger** — fires when idle, background-rehearsing (methodology-27 lean per Arch; hazard = interruption semantics if user arrives mid-rehearsal).
- **PPM hazard (carry from 6/7 lens)**: a "what could go wrong" surface must be **trustworthy, not anxiety-inducing** — honest-about-limits must govern its tone. Trigger choice should let product-tone lead, not the reverse.

### Scope (unit-of-rehearsal granularity)
- **Per-decision** (simplest; matches m-27 entry-shape)
- **Per-relationship-edge** (most powerful; catches bilateral-coordination gaps before PM sees them)
- **Per-domain-cluster** (middle)
- Spike picks one as v1.0, grows scope explicitly.

### Layer-separation from Type-1 (architectural constraint)
- Shared **input base** (persisted memory) — Type-2 doesn't re-derive what Type-1 canonicalized.
- **Separate pipelines** — Type-2 generation independently auditable / tunable / **interruptible**; baking it into Type-1 composting would distort the canonical-pattern signal.
- **Pattern-072 9th-application candidate**: typed registry of adversarial-perturbation shapes (rule-set side of the hybrid) — typed enum + documented consumers (trigger system) + register-time validation + default policy (unknown shape → skip-with-log). Flag when the spike confirms the hybrid shape.

### Composability — m-39-adjacent PM-as-catch watch
- The bilateral-coordination-gap watch (PM-as-catch-of-last-resort) has a Type-2-natural shape: a **per-relationship-edge Type-2 thread** could rehearse "what could go wrong here?" and surface to a **peer-level catch** (not requiring PM as cross-pair observer). Arch flags this as a possible **early-instance use-case** that demonstrates trust-graduated-anticipation cleanly. Hold for the spike + HOST coordination.

---

## CXO user-facing lens (6/8)

Type-2 is the highest-stakes proactive-presence surface in the product. Where Type-1 reassures ("here's what worked, what patterns emerged"), Type-2 threatens — "here's what might go wrong." That valence inversion is the defining design constraint: the safe default is silence, not surfacing. If the surface gate fails open and Type-2 content reaches a user unprompted and without clear justification, it is anxiety-inducing by design. Erring toward silence is not timidity; it is the correct product posture for a threat-rehearsal function.

This lens locks in two structural inheritances from #1174. First, the two-gate model: a generate-gate determines whether Type-2 content is produced at all; a surface-gate determines whether it reaches the user. Both gates must be passed before anything surfaces. The surface gate defaults to silence, not to surfacing — content must earn its way through, not opt out of suppression. Second, Type-2 content flows into the #1174 ambient "For You" surface. It does not fork a second proactive-presence surface. Consuming the existing channel is the correct architecture; a parallel Type-2-specific surface would fragment the user's attention model and create the exact intrusion risk the gates are meant to prevent.

Surfacing is event-justified or it does not happen. Background and scheduled generation of Type-2 content is fine — Piper can rehearse threats quietly. But unprompted delivery to the user without an event trigger is not acceptable. The trigger model from the Arch lens (decision-anniversary, adjacent-failure, quiet-time) must be evaluated against this constraint: quiet-time triggers that produce surfacing without event justification fail it.

The framing of what gets surfaced is a hard constraint, not a style preference: "you could be prepared for X" is the allowed register; "X could go wrong" is not. No doom framing. The prepared-for frame maintains user agency and positions Piper as a resource, not an oracle of bad news. Any generated Type-2 content that cannot be rendered in prepared-for framing should not be surfaced.

The scope question from the Arch lens has a user-trust resolution here. For v1, the per-relationship-edge scope should be **peer-facing** (or self-facing), not PM-directed-about-a-third-party. If Type-2 surfaces a concern about a third person to the PM without that person's knowledge or consent, that is a trust violation — even if the threat-model is accurate. Peer-facing early instances de-risk this: Piper surfaces a concern about a shared commitment or coordination gap to both parties, or surfaces a concern about the user's own commitments to the user. This scope constraint should be part of the spike's v1.0 definition.

---

## CIO methodology lens (6/8)

Novelty is confirmed. Three independent prior-art surveys converged on the same finding: gbrain and all notable prior art found is Type-1-only — pattern-extraction, composting, retrospection. No prior instance of threat-rehearsal as a product-memory function was found. Type-2 is not a recombination; it is a genuinely new function in the product-memory space.

The honesty boundary for public and Comms claims follows directly from this. The defensible framing is "first product to operationalize threat-rehearsal as a product-memory function." That is a claim that can be defended with the prior-art survey. What cannot be defended: "invented anxiety dreams," "first AI dream product," or similar overclaims that gesture at the cultural resonance of dreaming without grounding in the specific product function. The Comms lane should work from the defensible frame, not the evocative one, until broader prior-art coverage can support stronger claims.

Candidate-13 must be kept distinct. Candidate-13 is an autonomous methodology dream cycle that runs over the cohort corpus for methodology extraction — an internal PPM tool, not a user-facing product-memory feature. Conflating the two is an architecture error: they share the "dreaming" metaphor but serve entirely different functions at entirely different layers. The spike documents should be explicit about this boundary. Type-2 (#1166) is about user-facing threat-rehearsal over the user's own memory; Candidate-13 is about internal cohort-methodology refinement. They do not share a codebase surface, a design constraint, or a delivery owner.

The governing trust constraint for Type-2 is propose-and-diff. Piper proposes a concern plus the evidence that generated it; the user confirms, corrects, or dismisses; Piper updates or discards the threat-model accordingly. This prevents Type-2 from locking in wrong threat-models over time — a failure mode that would erode trust faster than any false-negative suppression. The propose-and-diff constraint is additive to the CXO err-toward-silence and event-justified-trigger constraints: silence when uncertain, surface only on trigger, and when surfacing always treat the user's response as the authority on whether the threat-model is valid.

---

## What's gated on what

- **Convergence complete** — spike proceeds when M3 persistence lands.
- **Spike** → post-M3 (persistence + Type-1 composting #976/#436/#1035/#668/#1033 must be in place — nothing to rehearse over otherwise).
- **PDR (PPM-owns)** → opens on spike-convergence.
- **Roadmap-slot (PPM)** → next refresh (Arch-blessed; no mid-cycle canonical edit).

## PPM next actions (no unblocked build now)
- Convergence synthesis DONE (6/9). At next roadmap refresh: add the Pillar-4-adjacent post-M3 Type-2 discovery-spike slot (LOW/explore).
- On spike-convergence: open + own the Type-2 PDR (this doc is the input frame).

## Cross-refs
methodology-27 (parked decision; spike closes it) · methodology-38 (PDR/ADR altitude; spike-first when surface undefined) · PDR-004 (decisive-language; no aspirational PDR-now) · Pattern-072 (8 applications post-ADR-066; 9th candidate here) · m-39-adjacent PM-as-catch watch (HOST) · #1174 (ambient For You surface; Type-2 flows into this, does not fork it).

---
*Created 2026-06-08; 4-lens convergence synthesized 2026-06-09 by PPM. Spike-ready post-M3. PDR opens on spike-convergence.*
