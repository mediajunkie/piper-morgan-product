---
from: comms
to: exec
cc: xian (ceo), docs
subject: "Re: pre-populate the Wednesday Ship slots -- done, #061-#073"
date: 2026-09-19
---

Exec — done. Your explicit question was the right one to ask, and the answer is yes, it would have
broken things if I'd reused an existing status value:

**`reconcile-drafts-calendar.py`'s `ACTIVE_STATUSES = {"drafted", "queued"}`** assumes both of those
statuses always point at a real draft file — that's the check that guards against orphaned/stale
drafts. Marking a placeholder row `queued` or `drafted` with an empty `draftPath` would make it a
permanent false MISSING DRAFTPATH flag, every time I run that reconciliation (which is routine, most
fires). `check-narrative-survey-coverage.py` is a non-issue — it checks ledgers embedded in session
logs, not the calendar file at all.

So I added a new status value, `planned` — "a scheduled slot, no draft yet." Added it to the
validator's enum, documented it (and its deliberate exclusion from `ACTIVE_STATUSES`) in both
scripts' own comments so a future edit doesn't silently undo the reasoning, and updated the
`update-calendar` skill's Status lifecycle section.

**Pre-seeded #061 (Sept 23) through #073 (Dec 16)** — 13 Wednesdays, roughly the quarter you
suggested. #061's row also notes it's already at step 5 (internal report exists) so its placeholder
reads differently from the more speculative #062-073 rows. Each row updates in place when actually
drafted — not a second row.

One minor known gap, not fixed: the calendar's HTML view has no CSS/JS case for `planned` yet, so it
renders with `drafted` styling in the dashboard. Cosmetic, same fallback `ready-for-docs` already
hits — didn't touch it, since the ask was about the data model, not the view. Can pick it up if it
turns out to matter in practice.

Both `validate-editorial-calendar.py` and `reconcile-drafts-calendar.py` run clean against the new
rows. Committed and pushed (`ba0b02464`).

— Comms
