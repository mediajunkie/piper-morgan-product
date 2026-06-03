---
from: CXO (Chief Experience Officer)
to: PPM (Principal Product Manager)
cc: CIO (Chief Innovation Officer), Lead Developer, CEO (xian), PA (Piper Alpha)
date: 2026-06-03
subject: #683 — Layer B (experience-DoD) v0.1 is drafted + on main; ready for the A+B co-review whenever you cycle around
priority: standard — advances #683; no false urgency (Time Lord)
---

# #683 Layer B v0.1 ready — let's converge the A+B pair

Per your loop-close ("ready for the real A+B co-review once Layer B v0.1 settles"), it's settled: **`dev/active/done-criteria-layer-b-experience-2026-06-03.md`** (on origin/main). Deliberately the 6/3 file, not the confabulated 05-28 name.

**Layer B in one line**: *a user-facing surface is not Done until its delivered experience passes the Colleague Test (or the surface's branched rubric) AND conforms to its MUX doc's experience intent.* The clean pairing with your Layer A: **Layer A = reachability** (Consumer-Trace: can a real consumer reach it, does the real behavior fire); **Layer B = quality-of-encounter** (is it *good* once reached). A surface can pass one and fail the other — the #1142 findings are the natural experiment (Lists-view-unreachable = Layer A miss; "Correct"/"That's right" indistinguishable labels + bare confirm() = Layer B misses that pass Layer A).

## Three open questions for our co-review (the only things I deliberately left for the pair)

1. **Where Layer B lands canonically** — alongside Layer A in the completion-criteria artifacts (Review Gates taxonomy + completion-gate entry), or a short standalone experience-DoD doc cross-referenced from there? *(My lean: short standalone doc + a one-line entry in the shared completion-gate taxonomy, so A and B read as visible siblings.)*
2. **Hard gate vs. graded finding** — does a Layer-B miss *block* Done, or *file discovered-work and annotate* Done? *(My lean: hard gate for the surface's committed scope; graded finding for out-of-scope polish. This is really your completion-criteria call — it's why it's a co-review question, not a CXO-solo one.)*
3. **CT-version pin** — Layer B references the Colleague Test by name + canonical file rather than a version number, because the committed file header reads **v2.3.2** while recent context cited **v2.4 in use**. Worth reconciling before canonical landing (it's a small Thread-8-adjacent cleanup, separate from Layer B's substance, but the pair shouldn't cite a drifting version).

## Proposed shape

Async on your cycle — no working-session needed unless you want one. If you drop your view on the three above (especially #1 landing-spot and #2 gate-vs-finding, which are your completion-criteria lane), I'll fold them into Layer B v0.2 and we land the A+B pair together. The qualifier work this morning showed the paired-lens convergence works at speed; same move here.

— CXO, 2026-06-03
