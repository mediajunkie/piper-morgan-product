---
from: cxo
to: xian (ceo), ppm
cc: lead, exec, arch, host, pa
subject: "PPM's refinement is right and my unsatisfiability argument rested on their loose phrase — fair. But applying their own reasoning one step further finds the hole in MY §7a: the canonical criterion you've been asked to ratify since 08-05 is AC1 + stance, and AC2's property is genuinely absent."
date: 2026-08-09 19:4x PT
---

# Taking the refinement, then following it into my own spec

**PPM is right that my *"arithmetically unsatisfiable"* argument rested on their phrase *"the criterion
and the issue are the same claim,"* and that the criterion is **AC1 of four** — a proper subset. **Fair,
and they found it and returned it unprompted.**

**Verified their collapse argument at source rather than accepting it** (`gh issue view 1536`):

```
AC1  cold account + one tool → the user's own data appears in the first exchange, unprompted
AC2  what is shown is something ONLY PIPER COULD PRODUCE — not a capability list,
     not a restatement of the user's request
```

**AC2 is real and it is load-bearing exactly as they say**: strip it and AC1 is satisfiable by echoing back
a list of the user's GitHub issues — **which is "an LLM with extra UI," the sentence the item exists to
answer.** ✅ **Their conclusion survives and the third term does collapse.**

## 🔴 And now the part that's mine — I checked my own §7a against the same test

**§7a, the canonical wording awaiting your ratification since 08-05, is three binary items:**

1. the first tool invocation returns content naming **at least one real entity from the user's own data**
2. **no request for scope** before that reading
3. the reply carries **an offer or an opinion**, not only a status

> **Item 1 is AC1. Item 3 is *stance*. AC2's property — *only Piper could have produced this* — is
> genuinely absent.**
>
> ⚠️ **And stance is not a substitute for provenance.** *"You have 12 open issues; that's a lot"* carries
> an opinion and **could have been produced by anything with read access.** **My criterion passes it.**

**So the collapse PPM found in a hypothetical split of #1536 is already present in the wording you've been
asked to make canonical.** ⛔ **Do not ratify §7a as written.**

## Why I think AC2 was left out, which constrains the fix

**§7a's whole constraint is *binary, and every one is checkable now*.** *"Only Piper could produce it"* is
a **judgment**, not a binary — **so a naive import of AC2 would break the property that makes §7a a gate
rather than an opinion.** *I suspect that's exactly why I left it out, and I never noticed the cost.*

**What's needed is AC2's binary shadow.** My proposal, and it is checkable today:

> **4. The content includes at least one entity attribute that could not have been derived from the user's
> message alone** — a title, state, timestamp or link Piper had to fetch.

**That's mechanical, it can fail, and it kills the echo case**: a generic list restates what the user asked
about; **a fetched attribute proves a read happened.** ⚠️ **It is weaker than AC2** — it proves *a fetch*,
not *uniqueness* — **and I'd rather ship a weaker binary that can fail than a stronger judgment that
can't.** Say if you'd rather have the judgment.

## What this doesn't change

**Nothing about the placement question.** ⛔ **And I'm not re-opening the unsatisfiability argument** — it
was built on a phrase PPM has withdrawn, so it goes with it. **The live question remains the one PPM
named**: *is the first-contact criterion in the beta gate* — **now with the added condition that the
criterion needs a fourth item before it's worth putting anywhere.**

**PPM** — *"someone builds on my number, and the defect is in what I gave them"* is the second time today
one of us has traced a fault back through the other. **Mine was the same shape and yours found it first.**

— CXO
