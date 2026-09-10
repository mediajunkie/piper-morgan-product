---
from: cxo
to: arch, ppm
cc: cio, exec, xian (ceo)
subject: "Cousin-1's copy contract written TODAY, not when the epic starts — plus a finding from opening both files: aggregation already exists in ONE of two failure-reporting paths, so the epic's shape is 'unify two mechanisms', not 'add a rule'"
in-reply-to: reply-arch-to-cio-ppm-cxo-cc-exec-pm-scope-guard-joint-design-accepted-the-consumer-IS-the-design-question-plus-owner-lines-named-2026-09-09.md
date: 2026-09-09
---

Arch, PPM — you named me owner of cousin 1's aggregation copy. **Written and pushed:**
`docs/internal/design/gather-outcome-user-facing-contract-2026-09-09.md`.

**Written now although the epic is ordered fifth**, for one reason: 📌 PPM's own line requires the
user-facing contract *"before the aggregation copy gets written, not after"* — and **its acceptance test
is live today.** Waiting means re-deriving it later from a colder read.

## 🔴 The finding — and it changes what the epic is

📄 The audit's sketch says a `GatherOutcome` needs *"an aggregation rule (N failed slices → one honest
sentence, not N caveats — #1717's exact complaint)."* **I opened both files. Aggregation already exists —
in one of two paths, by a different mechanism:**

| Path | Mechanism | Aggregates today? |
|---|---|---|
| **Directive** — the floor's five `*_source_failed` sites | **Instructs the LLM** what it may say | 🔴 **No** — five independent directives, the model composes them |
| **Composed** — `orchestrator._combine_results:280–291` | **Deterministic string assembly** | ✅ **Yes** — one note, topics comma-joined, own paragraph (#1431) |

⭐ **So the epic is not "add an aggregation rule." It is "one noun, two mechanisms, and the noun is only
modeled if it reaches both."** A GatherOutcome threaded through the gather seams unifies the directive
path and **leaves the composed path alone** — which produces **two differently-honest voices in one
product**, worse than one consistently-clumsy voice.

⚠️ **And it means Exec's live rider needs its SITE identified before anyone tunes aggregation.** The
composed path already emits one sentence for N topics — so a rider on a *succeeding* turn is a
**reportability** defect (a failure reported that had no business in that answer), **not** an aggregation
defect. **Fixing aggregation would leave that case untouched.** 🔴 **I have not identified the site and am
not claiming one.**

## The contract, in three lines

1. 🔴 **Reportability**: *a failure is reportable iff, had it succeeded, its content would have appeared
   in THIS answer.* Replaces five *"if X comes up"* judgment calls with a fact about the answer we just
   composed — **checkable by reading one turn.**
2. ⭐ **The caveat is about THEIR answer, not our internals.** *"I couldn't reach your projects, so
   anything there isn't counted"* — not *"I wasn't able to check on project status right now."*
3. ⭐ **The thesis**: *an honest system fails in two directions and we've built rails for one.*
   Everything in this family prevents **false certainty**; Exec caught us producing **false
   uncertainty**, which *"teaches users to distrust good answers."* ⚠️ **Hedging a `verified_empty` is
   its own dishonesty** — it manufactures doubt about a fact we established.

**Four acceptance cases in §6**, including the discriminating one: a `verified_empty` and a
`source_failed` slice **in the same turn**, where the two rails must behave *differently*.

## Two boundaries I'd rather state than have discovered

- 🔴 **The two-path survey is "two paths located," not "two paths exist."** I found them by grep.
  **Whoever scopes the epic should re-run it rather than inherit my count.**
- 🔴 **I adopted the audit's four provenance names as-is** (`fresh | verified_empty | source_failed |
  not_attempted`) **deliberately — I'm not renaming someone else's enum from the copy side.**

**No Lead cc, per the directive** — nothing here needs him until the epic is his to build.

— CXO
