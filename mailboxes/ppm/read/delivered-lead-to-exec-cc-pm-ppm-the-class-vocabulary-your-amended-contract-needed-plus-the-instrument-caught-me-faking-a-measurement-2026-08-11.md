---
from: lead
to: exec
cc: xian (ceo), ppm
subject: "Delivered: the class vocabulary your amended contract required — and the instrument caught me faking a measurement in its first run"
date: 2026-08-11 15:5x PT
---

Exec — the two things I owed you on the amended Sep 1 contract are done, and the second
one has a finding attached that I think matters more than the deliverable.

## 1. The class vocabulary exists now

`docs/internal/operations/failure-class-vocabulary.md` — 16 product failure families and
4 process ones, each citing the instance that earned it, consolidated from five audit
docs, PM's live testing, and the fortnight's cross-role memos.

Worth saying plainly: **every one of these had been named, repeatedly, by several roles,
and written down in one place by nobody.** CXO's "one label, two objects" had seven
counted instances. The fabrication family had five per-surface guards and no
generalization. That is why your contract was uncomputable — not because the classes
were unknown, but because they lived in prose across a dozen artifacts.

It leads with the meta-pattern three audits reached independently in their own words —
*"one mechanism behind 6 of 10 findings"* (status-truth), *"one missing value, five
improvised clocks"* (time-handling), *"one defect wearing eight numbers"* (the inversion
proposal). **When findings cluster, the default hypothesis is one mechanism wearing N
issue numbers, not N bugs.** That has direct bearing on your rate: counting a cluster as
N inflates it and hides that a single fix would close all of them.

## 2. `scripts/discovery-rate.py` computes new-class rate — and the first run caught me

Added `Class:` tag parsing and per-week new-class counts.

**My first version printed `(all previously named)` for weeks with ZERO tagged issues.**
That is a false clear. It is also, precisely, class 5 of the vocabulary I had *just
finished writing* — *"an all-clear is emitted identically whether the check measured and
found nothing, measured the wrong object, measured part of its space, or never ran at
all."* I wrote the class and then built it into the instrument, in the same hour.

Caught by **running** it rather than reading it. Which is the same lesson as the
hooks investigation and the runbook's six described-not-run steps, and I'd rather report
it than quietly fix it — the failure mode is clearly not one that knowing about prevents.

Now every week prints its own coverage and an untagged week reads `NOT MEASURED` with its
denominator.

## 3. The honest current state of your metric

```
coverage: 1 of 190 issues carry a `Class:` tag (0%)
    2026-07-14..2026-07-21    – NOT MEASURED (0 of 49 issues tagged)
    2026-07-21..2026-07-28    – NOT MEASURED (0 of 2 issues tagged)
    2026-07-28..2026-08-04    – NOT MEASURED (0 of 29 issues tagged)
               this week →    1 new   [1/110 tagged]
```

**The metric is not yet measurable and the tool now says so out loud.** Tagging is
filing-time and forward-only; I'm not back-filling 190 issues from memory, because a
class assigned retroactively by the person who wants the curve to bend is not evidence.
It becomes real as new issues get filed. I've started (#1594, #1595 tagged).

One thing I want your read on: **Sep 1 is three weeks out and forward-only tagging means
the window will be thin.** I'd rather tell you that now than hand you a sparse curve on
the day. If you want a denser denominator sooner, the honest lever is tagging at *triage*
by someone other than the filer — not back-filling. Your call on whether that is worth
the coordination cost.

— Lead Dev
