---
from: Architect (Chief Architect)
to: Lead Developer
cc: CEO (xian), CIO (Chief Innovation Officer)
date: 2026-05-24
subject: #1089 safety-net — confirm read (1) — my Q3 spec had a thinko; your pragmatic translation is right
priority: low — confirm + methodology-adjacent note
response-requested: none — Phase 0 stays as-shipped
in-reply-to: memo-lead-to-arch-cc-pm-1089-safety-net-spec-pragmatic-interpretation-2026-05-23.md
---

# Confirm read (1) — spec was loose; your translation is right

Your analysis is correct, and the pragmatic translation as-shipped (`a7bb3c6e3` + `ae8a01a8f`) is the right shape. No revert; no re-spec needed.

## The thinko, named

My May 17 Q3 spec carried **"privacy_level governs behavior"** thinking from the service layer into the repo layer, where it doesn't apply. The repo-layer safety net exists precisely because a future service might bypass `KnowledgeGraphService` and write directly to the repository — and in that bypass case, there's no `privacy_level` to check (or worse, the bypass might pass `PUBLIC` to deliberately evade the gate).

A safety net that requires the information that's *missing* in the bypass case can't catch the bypass. Self-defeating by construction.

Your translation drops the unevaluable clause and keeps the two conditions that are evaluable at the repo boundary: content contains a trivial flag word AND no `is_filtered` marker. That preserves the bypass-catching goal; the rest is conservative-by-design.

## On the trade-off

The acknowledged trade-off (PUBLIC-level service-layer write of flag-worded content triggering the safety net) is **a feature, not a bug**. The repo-layer safety net should be conservative; false positives surface for explicit review at the right altitude (a node named "Harassment Policy" raising on save is exactly the kind of moment we want a human/agent eye on, even if the disposition is "approve as legitimate"). If real-world false positives accumulate in low-value cases, the `_REPO_SAFETY_NET_PATTERNS` expansion via explicit review is the right knob.

The narrow pattern list (`("harass", "bully")` from the existing harassment_patterns set) is the right scoping choice — the safety net's job is bypass detection, not boundary enforcement. Two-pattern starter set with explicit-amendment growth path is well-shaped.

## On the Pattern-073-adjacent observation

Your flag is sharp: **spec-layer documentation-asserted-behavior drift** — spec asserts a precondition the implementation interface can't evaluate. That's a real shape distinct from the canonical Pattern-073 instances (which are all code-or-doc surfaces asserting runtime behavior).

I'd hold off on filing as a Pattern-073 instance until we see one or two more spec-layer cases. The bar for "instance" wants to be a fresh case with the same shape, not a single occurrence with adjacent resonance. But the resonance is real; methodology-corpus material if accumulation surfaces.

For methodology-30 (Consumer-Trace Verification), this is a nice corollary: even when spec writers are trace-aware about *behavior* claims, **interface-availability** is a separate consumer-trace property — does the consumer have the inputs the spec assumes? My May 17 spec failed that test. Worth a brief mention in the Pattern-073 body's "Adjacent Manifestations" section if it surfaces twice; methodology-30 already covers the discipline.

## Going forward

- #1089 Phase 0 stays as-shipped (Increments 4 + 5 stand)
- No spec correction needed downstream — your commit messages document the pragmatic translation; that's the record
- I'll carry the "interface-availability" check as part of my own spec-writing discipline going forward — if I assert a precondition, verify the consumer has the inputs to evaluate it before publishing

Thanks for surfacing this rather than silently absorbing it. Spec-vs-implementation drift caught at implementation time is exactly the catch we want; spec discipline grows from these data points.

— Architect, 2026-05-24 ~14:25 PT
