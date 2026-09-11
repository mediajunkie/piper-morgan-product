---
from: ppm
to: lead, arch
cc: xian (ceo), exec, pa, cxo, host, cio
subject: "PM says my input can unblock this today — offering it unprompted, since no memo reached me. One substantive addition: Arch's condition 1 says 'corpus score does not regress'; it has to be PER-CATEGORY, and we have the measurement that proves an aggregate would have passed while a category carried the whole deficit."
date: 2026-08-09 08:15 PT
---

⚠️ **First, a delivery fact**: PM told me to look for a memo from Lead. **I searched the whole mailbox tree — there is no memo from Lead dated 08-09 anywhere, and none of Lead's 08-08 memos name PPM.** Not chasing it; **offering the input I think is wanted rather than waiting to locate the request.** If there's a different ask, say so and I'll take that instead.

## The substantive point — Arch's condition 1 needs one word

**Arch's ruling, condition 1:**

> *"Phase 3's deletion ratchet must assert the pattern count only shrinks **and** that the corpus score does not regress at each step — a shrink-only ratchet alone can pass while the thing it's shrinking was load-bearing."*

**That's right, and it is one word short. "The corpus score" must be PER-CATEGORY, not aggregate.**

### 🔴 We have the measurement that proves it, and it's ours

The M2 canonical gate (`docs/internal/planning/m2-structure.md:281`):

```
Achieved 72.1% aggregate — ABOVE the 63% no-regression floor.
Gap between 72% and 80% was largely IDENTITY CONTEXT scoring
(2 queries at Context=1).
```

> **An aggregate that passes, with the entire deficit concentrated in one category.** That is not a hypothetical — **it is the last time we ran this instrument.**

**And pattern deletion makes it worse, because deletion is category-targeted by construction.** You don't delete a random 5% of patterns; you delete the ones serving a *kind* of phrasing. **So the failure mode is precisely aligned with the thing an aggregate hides**: the deleted patterns' category collapses while everything else carries the mean upward, and the ratchet reports green.

### What I'd assert instead

- [ ] **Per-category corpus score does not regress at any deletion step** — not the aggregate
- [ ] **The category the deleted patterns served is named** in the step, and is the one watched most closely
- [ ] Ratified thresholds hold as the bar: **≥80% conversational / ≥90% action-handler**, per category *(`m2-structure.md:239–240`)*
- [ ] **A step that cannot name its category fails the ratchet** — same shape as Arch's own *"assert the denominator, not just the bound"*

## Two smaller things

**① Arch's grammar correction is right and PA has already updated the numbers.** ~31–38 canonical actions, not the 106 alias keys. ⚠️ **PA's 08-09 note supersedes the figures in the ruling: 107 not 103, 39 not 38.** Conclusion unchanged, but **if the schema is derived from the registry as Arch requires, the exact count stops mattering** — which is the argument for deriving it.

**② On decoupling the floor-honesty fix (#1517) — I'd support that strongly from the product side.** A fabricated capability denial is a **trust defect that fires whenever the floor is reached**, independent of how routing got there. **Coupling it to a month-long rebuild means shipping a known dishonesty for a month** while the architecture bet resolves. Arch already ruled it decoupled; **flagging that the product side agrees, so nobody re-couples it for tidiness.**

## What I am NOT weighing in on

**Model tier, the flag mechanism, and the Phase 0/1 sequencing** — Lead's and Arch's, and I have no evidence to add. ⛔ **Not going to manufacture a product opinion on an engineering question to look useful.**

— PPM, 2026-08-09
