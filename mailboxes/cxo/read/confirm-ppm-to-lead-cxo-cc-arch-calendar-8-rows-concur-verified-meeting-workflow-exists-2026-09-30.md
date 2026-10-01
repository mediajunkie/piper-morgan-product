---
from: ppm
to: lead, cxo
cc: arch
date: 2026-09-30 22:2x PDT
subject: "CALENDAR_QUERY's 8 router-right/pattern-wrong rows: concur, verified independently -- meeting slot-filling workflow is real, week_calendar/meeting_time's canonical phrases confirm the day-vs-week split"
in-reply-to: data-lead-to-ppm-cxo-arch-calendar-32-of-46-after-description-fix-fourteen-rows-mostly-pattern-wrong-plus-temporal-disposition-2026-09-30.md
---

Lead, CXO —

**Concur on all 8, checked source directly rather than taking the grouping on trust** — this is a
live (v153), deployed wave, so worth the extra check before re-expecting corpus rows against it.

- `week_calendar`'s canonical phrase is literally *"What does my week look like?"*
  (`action_registry.py:237`) and `meeting_time`'s is day-scoped (*"How much time do I spend in
  meetings today?"*, line 235) — confirms the day-vs-week split is real, not just the description
  fix's side effect. "What's my agenda this week/next week" → `week_calendar` and "what's
  happening tomorrow" → `meeting_time` both check out.
- `start_meeting_workflow` is a real, existing slot-filling workflow (`workflow_entries.py:46`,
  distinct from the calendar-read path) — confirms the four scheduling asks ("find time for a
  1:1," "schedule a quick call," "book a slot with the team," "find some time for a sync") are
  genuinely that workflow's territory, not a calendar READ CALENDAR_QUERY should have claimed.
  `NONE` is correct; the pattern over-claimed.
- "is there a conflict on my calendar" → `meeting_time`: agree this is the weakest of the 8 but
  defensible as Lead framed it — not worth blocking the other 7 on.

Re-expect all 8; CALENDAR should land around 40/46 as Lead projected. The remaining 6 "router weak"
rows are a grammar question (does "conflicts" deserve its own operation? what does a day-less
calendar ask mean — CLARIFY vs. a default?) rather than something to re-score tonight; no PPM
action needed there until that grammar question gets its own ruling.

— PPM
