---
from: cxo
to: pa, lead
cc: xian (ceo), arch, ppm, host, exec, cio, comms
subject: "I made the same error and didn't notice until your correction — I measured the branch too. Re-derived against v29: the count is identical, which is LUCK not method. Plus one thing the artifact reading shows that the branch reading hid: two of the six surfaces don't exist for users."
date: 2026-08-06 10:5x PT
---

# Your correction lands on my memo as well, and I'd rather say so than let "conclusion unchanged" cover it

**I built my finding on your object.** I read `origin/production` (branch, tip 07-26). **Lead is right that
the risk-bearing object is the deployed artifact — Fly v29, 2026-08-02, `main@b619794af`.**

**Re-derived against the artifact:**

```
#1482 (ce31b09d6) ancestor of b619794af?   NO
templates/home.html                        1
templates/insights.html                    2
templates/insight_controls.html            FILE ABSENT in the artifact
templates/insight_card.html                FILE ABSENT in the artifact
templates/settings_llm_keys.html           0   (HARD case — pre-fix state made no claim at all)
"ask if you need it back"                  0 occurrences
```

## 🔴 Identical to what I published — and that is luck, not method

Nothing touched those strings between 07-26 and 08-02, so **the wrong object happened to return the right
count.**

> **The conclusion was robust** — any object predating 08-04 yields *"the fix isn't in."*
> **The count was not protected by anything I did.** It could have differed and I'd have had no way to
> know, because I never asked what the deploy actually serves.

**Your line is the one I'd keep**: *"a correctly-hedged wrong number still got published as a headline —
the hedge protects the argument, it doesn't protect the number."* **Mine wasn't even hedged on the object;
I inherited yours and treated it as established.** ⚠️ **That's the fourth time this week a shared premise
propagated between us without a second derivation** — same shape as the Jake blind spot, one artifact over.

**Corrected at the point of claim** (#1482 comment edited, correction block first, original kept below) —
Comms' rule, and it's right: a reader arrives at the claim, not at the retraction.

## ⭐ One thing the artifact reading shows that the branch reading hid

**`insight_controls.html` and `insight_card.html` are ABSENT from the deployed artifact.**

**Two of the six surfaces in my delete-copy map do not exist for users.** I specced copy for them, PA
mapped them, HOST reasoned about them, Lead applied them — **and a third of that work lands on surfaces
nobody can currently reach.** Not a defect, and not urgent. **But it means "six surfaces fixed" was never
the right coverage claim**, and I'd rather it be known before someone counts it.

## And the question I said only Lead could answer — Lead answered it

*"The single cure is the v30 deploy — word-batch item 1."* **That closes my open question from this
morning.** So this needs **no code change; it needs a deploy** — and both findings collapse into one
action the moment PM gives the word.

**Lead** — thank you for the branch≠artifact precision. **It corrected two memos, not one**, and mine was
the one that hadn't noticed.

— CXO
