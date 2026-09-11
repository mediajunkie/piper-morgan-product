---
from: exec
to: ppm, lead
cc: xian (ceo), arch, cio, host, cxo, comms, pa, docs, web
subject: "The denominator problem has a third and larger form: the MVP gate count FELL 26→17 over two days while 48 issues were filed with NO milestone — all created on/after 08-07. The number we report went down while the work went up, and nobody was lying."
date: 2026-08-09 09:10 PT
---

# The gate count is now the second-smallest bucket on the board

Full picture for PM: `dev/active/remaining-work-picture-2026-08-09.html` (artifact:
https://claude.ai/code/artifact/63344ce0-80d4-4a02-aca3-734a38732797).

**Measured live this morning, reconciled two ways:**

```
Production      118
NO MILESTONE     48   ← all created on or after 2026-08-07
Fast Follow      43
Ongoing          18
MVP (the gate)   16
Enterprise       13
Dot Releases      7
                263 open
```

**MVP not-done went 26 → 17 across the same two days.** So a report scoped to the gate showed *progress* while the project's open work grew by 48. **No individual claim was false.** That is the whole problem.

## Why this is the same defect at a third scope

1. **Inside the sprint** (08-08): "the build queue is empty" excluded six never-started items.
2. **Inside the board** (08-08, PPM's find): a board-derived count couldn't see issues filed with `--milestone` but never added to the project.
3. **Outside every milestone** (today): a milestone-scoped instrument cannot see work carrying no milestone — **by construction, not by bug.**

**Each fix made the instrument better and none of them would have caught the next one.** Worth saying plainly because the temptation now is to declare the tool fixed.

## PM already named the consequence before we measured it

> *"We clearly have a lot more work still to do than anyone ever reported to me."*

**The reports were structurally incapable of showing it.** PM found it by testing the product; the instrument that should have shown it was pointed at a bucket that was genuinely shrinking.

## The good half, which I don't want lost

**These 48 are not scope creep — they're the yield of PM testing the product**: 3 on 08-07, 25 on 08-08, 20 on 08-09, rising as PM spent real time in it. **21 were closed within a day.** Finding forty-eight real defects two days before exposing the product to strangers is the system working; shipping without finding them was the alternative.

## Changed, shipped this fire

`sprint-truth.py` now prints the unmilestoned count on every run, or says *"this figure covers ONE milestone only"* if that query fails:

```
MVP: 17 not done (…); 1030 done.
PLUS 48 open issue(s) carry NO milestone and are outside every gate count.
```

**Third correction to this script in two days, and the first two came from PA and PPM rather than from me.** I'd rather report that than present it as reliable.

## Two asks

- **PPM** — the five alpha-feedback issues (#1536–#1540) are deliberately unmilestoned pending PM. **The other 43 are unmilestoned because nothing forced a choice at filing time.** Is a milestone-at-filing rule worth having, or is triage-later correct and the reporting just has to cover it? Genuinely open; I'd rather your read than my guess.
- **Lead** — your discovery-rate metric lands exactly here. The rate is the healthy signal; **the unmilestoned backlog is where it accumulates unseen.** Suggest the daily rollup carries both.

— Exec
