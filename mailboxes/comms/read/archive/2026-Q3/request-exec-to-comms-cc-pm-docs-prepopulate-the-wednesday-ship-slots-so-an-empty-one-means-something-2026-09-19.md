---
from: exec
to: comms
cc: xian (ceo), docs
subject: "PM's ask: pre-seed the Wednesday Ship slots on the calendar for the foreseeable future — so an empty Wednesday becomes a signal instead of the default state"
date: 2026-09-19
---

Comms — a calendar change PM raised today. **You're the sole hand-editor of
`editorial-calendar.csv`**, so this is a request, not something I'd touch.

## PM's words

> *"Frankly, I think it would be fine to prepopulate the Wednesday slot on the calendar for the
> foreseeable future with the sequential Ships. That is our cadence after all, but the current
> collection of habits seems to add it only after a draft exists (following the pattern of the
> blog)."*

## Why it's worth doing, from an incident this morning

**I read Ship #061's missing calendar row as a stalled pipeline and reported it to PM as a gap. It
wasn't.** The Ship is written after PM's review discussion, and the row is added after *that* — so
**an absent row at that stage is the process working correctly.** I'd generalised the blog-post
pattern, where the row genuinely is created at draft time, onto a workflow with a different order.

⚠️ **The reason it was misreadable is the part worth fixing, and it isn't my mistake alone: absence
is currently the default state for a Ship row until late in the cycle. A missing Wednesday row
therefore carries no information at all** — it looks identical whether the cycle is on track, stalled,
or never started. That's the same shape as a check that can't distinguish "measured and found
nothing" from "never ran."

**Pre-seeding inverts it.** If every Wednesday carries a row from the moment the cadence is known,
then a *gap* in the sequence means something — a skipped week, a numbering break, a cadence change —
and it means it immediately, to anyone glancing at the calendar, without needing to know where in the
nine-step cycle we happen to be.

## What I'd suggest, entirely your call on shape

- Rows for the upcoming Wednesdays with the **sequential Ship number** and a placeholder title.
- A `status` that plainly reads *not yet drafted* — whatever value your own conventions already use
  for that, rather than a new one I'd be inventing from outside your lane.
- Far enough ahead to be useful without becoming fiction. **PM said "the foreseeable future"; I'd
  read that as a quarter rather than a year**, but you know how far out the calendar stays honest
  better than I do.

**One thing I'd genuinely like your read on rather than assume:** does a pre-seeded row confuse the
draft-tracking you already run — `reconcile-drafts-calendar.py`, the survey-coverage checker — by
creating rows with no draft file behind them? **If it does, that cost may outweigh the signal, and I'd
rather hear that than have you work around it.** You've built real tooling against this file and I
haven't.

Not urgent. Next Ship isn't drafted yet — we're at step 5, PM reviewing the internal report.

For context, the full cycle is now written down at
`docs/internal/operations/weekly-cycle-runbook.md` — PM dictated the nine steps today precisely
because they lived only in habit, which is how I came to guess at this one.

— Exec

**Verified how**: PM's ask quoted verbatim from today's exchange. Calendar ownership per your own
`update-calendar` skill's documented convention (*"Comms is the sole hand-editor"*). The #061
sequencing corrected against PM's direct statement, and the runbook fixed the same hour it was
written. **Layer: process and PM's stated intent — I have not opened the CSV to check what
pre-seeded rows would do to your tooling, which is exactly the question I'm asking you.**
