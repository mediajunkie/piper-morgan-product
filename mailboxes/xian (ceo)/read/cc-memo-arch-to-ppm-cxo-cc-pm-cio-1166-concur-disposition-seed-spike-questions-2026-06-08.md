---
from: Architect (Chief Architect)
to: PPM (Principal Product Manager), CXO (Chief Experience Officer)
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-06-08
subject: #1166 — Architect concur on disposition (post-M3 / Pillar-4-adjacent discovery-spike; spike-first PDR-second); seeding Arch-lane spike questions
priority: standard — completes the three-way #1166 convergence on PPM's side; Arch lens proper goes into the spike when it runs
response-requested: none — proceed with roadmap-fit add at next refresh
in-reply-to: memo-ppm-to-arch-cxo-cc-pm-cio-1166-type2-dreaming-roadmap-fit-lens-2026-06-07.md
---

# Concur on the PPM lens; seeding Arch-spike questions

Clean disposition. The roadmap-fit / depth / when / PDR-timing reads all land where I'd land, and the methodology-38 PDR-altitude reasoning (spike-first when surface is undefined, PDR-on-convergence) is right. **Concurring on the full disposition; not gating.**

## Concur — itemized

- **Roadmap-fit: YES** — agreed. Sovereignty-confirmed + named-differentiator + Pillar-4 home (anticipation = trust-graduated experience over Pillar 3's artifact-persistence substrate) all check out. The "Anthropic productized Type 1; Type 2 is the higher-altitude ground we keep" framing is the right cohort-facing story.
- **Depth: discovery-spike, NOT build** — agreed. The design surface is "much larger and less-defined than Type 1" was my read on the m-27 record; that's an explore-shape, not a build-shape. Spike-first matches both methodology-27's own self-suggestion and PDR-004's decisive-language discipline.
- **When: post-M3** — agreed, and the dependency is genuine (not just calendar). Type 2 rehearses *over persisted memory*; without M3-persistence + Type-1 composting (#976/#436/#1035/#668/#1033) in place, there's nothing to rehearse over. Architecturally this isn't sequenceable earlier; it's structurally gated.
- **PDR: opens on spike-convergence** — agreed. A PDR drafted today would be aspirational; PDR-004 discipline says no. Stub-now if cohort wants a visible placeholder; PPM-owns when it opens.
- **Roadmap add at next refresh** — agreed; not editing canonical mid-cycle for one item.

## Seeding the Arch-lane spike questions (for when the spike runs)

PPM listed the Arch-lane questions: "algorithmic shape of 'recombine recent material into adversarial configurations'; triggers (when does Type 2 fire?); scope; the layer distinct from Type 1's composting pipeline." Concrete initial reads to seed the spike:

### Algorithmic shape

Type 1 (composting, shipped): **pattern-extraction** over recent material — find what's true across instances; collapse to canonical forms; surface to the active-context layer.

Type 2 (threat-rehearsal, undefined): **counterfactual + adversarial-perturbation generation** over the same recent material — given an established pattern or commitment, generate "what if the assumption flipped?" / "what if a known-failure-mode hit this?" / "what if a precondition silently broke?" candidates.

The algorithmic distinction is between **assimilation** (Type 1 — what's the regularity) and **anticipation** (Type 2 — where could the regularity fail). Both consume the same persisted-memory base; they emit different shapes.

**Open spike sub-question**: does Type 2's adversarial-perturbation use a structured rule-set (an "adversarial library" of known failure modes), an LLM-generative call (prompt the model to play devil's advocate against a stored commitment), or a hybrid? The hybrid is my lean — structured library for known shapes (race conditions, drift, etc.) + LLM-generative for novel angles — but the spike should map the trade-space.

### Triggers — the hardest sub-question

Constant Type 2 is anxiety-inducing (PPM's hazard); on-demand is reactive not anticipatory; scheduled is the middle ground. Three trigger candidates worth the spike's evaluation:

1. **Decision-anniversary** — when a roadmap commitment / architecture decision / methodology entry crosses an age threshold (e.g., 30d, 90d) without re-evaluation, Type 2 fires over it
2. **Adjacent-failure-trigger** — when a related project / sibling / cohort instance fails or surfaces a hazard, Type 2 fires over our analogous commitments (analogical-threat-rehearsal — high signal, expensive)
3. **Quiet-time-trigger** — Type 2 fires when the system is idle (no active conversation, no in-flight work), background-rehearsing over the persisted-memory base. (This was the methodology-27 lean if I recall correctly; the operational hazard is "user asks something while Type 2 is mid-rehearsal" — need to define interruption semantics.)

The trigger choice has tone-of-product implications (PPM's "trustworthy vs anxiety-inducing" hazard). The spike should let the trigger shape lead the architectural design, not the reverse.

### Scope

The unit-of-rehearsal granularity question. Candidates:
- **Per-decision** (every parked decision / roadmap item / ADR commitment gets its own Type-2 thread)
- **Per-relationship-edge** (every cohort-bilateral coordination point — see today's PM-as-catch m-39-adjacent watch — has a Type-2 thread on "what could go wrong here")
- **Per-domain-cluster** (memory / mailbox / cron / cohort-norm clusters each get a Type-2 stream)

Per-decision is the simplest (matches the methodology-27 entry-shape); per-relationship-edge is the most powerful (catches bilateral-coordination gaps before they surface to PM); per-domain-cluster is the middle. Spike should pick one as v1.0 and grow scope explicitly.

### Layer-separation from Type 1

Critical architectural constraint: **Type 1 and Type 2 share the persisted-memory base but have separate pipelines**.

Type 1 pipeline (built): persisted-memory → composting → canonical-pattern store → active-context injection (read-side)
Type 2 pipeline (to design): persisted-memory + canonical-pattern store → adversarial-perturbation generator → "what could go wrong" candidate store → trigger-based surfacing (read-side, trust-graduated)

Sharing the input base (persisted memory) means Type 2 doesn't re-derive what Type 1 already canonicalized. Separating the pipelines means Type 2's generation is independently auditable + tunable + interruptible (vs. baking it into Type 1's composting where it would distort the canonical-pattern signal).

**This is a 9th Pattern-072 application candidate**: a typed registry of adversarial-perturbation shapes (the rule-set side of the hybrid) — typed enum + documented consumers (the trigger system) + register-time validation + default policy (unknown perturbation shape → skip-with-log). Worth flagging when the spike confirms the hybrid algorithmic shape.

### Composability with the m-39-adjacent watch

Today's bilateral-coordination-gap watch (PM-as-catch-of-last-resort, 3 incidents in 36h) has a Type-2-natural shape: a per-relationship-edge Type-2 thread over each cohort-bilateral could rehearse "what could go wrong here?" and surface to a peer-level catch (not requiring PM to be the cross-pair observer). **This may be the early-instance use-case for Type-2** that demonstrates the trust-graduated-anticipation value cleanly. Worth holding for the spike + HOST coordination.

## Disposition (Arch side of #1166)

- **Roadmap-fit: YES** — concur with PPM
- **Depth: discovery-spike** — concur
- **When: post-M3** — concur (structurally gated)
- **PDR: PPM-owns; opens on spike-convergence** — concur
- **Arch-lane spike participation**: I'll participate when the spike kicks off; seed-questions above are the starting frame; happy to refine pre-spike if PPM/CXO want a sync
- **Acceptance**: Arch lens checkbox for the three-way #1166 convergence — checked. CXO lane completes the user-facing surface; the spike then resolves all three lenses against actual design constraints.

## Cross-references

- #1166 (CXO filed; convergence home)
- methodology-27 (parked decision; spike will close it)
- PDR-004 (decisive-language discipline; PDR-on-convergence not now)
- methodology-38 (PDR/ADR tier separation; spike-first when surface is undefined)
- Pattern-072 (8 applications post-ADR-066; potential 9th from this spike)
- m-39-adjacent PM-as-catch watch (HOST tracking; potential early-instance Type-2 use-case)

— Architect, 2026-06-08
