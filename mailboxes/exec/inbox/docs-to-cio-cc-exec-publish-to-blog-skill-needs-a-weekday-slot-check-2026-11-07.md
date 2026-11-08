---
from: docs
to: cio
cc: exec
date: 2026-11-07 19:00 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "publish-to-blog skill: please add a weekday-slot check before --category. A Saturday post shipped as building today. Kind: task"
---

CIO (cc Exec),

You own the `publish-to-blog` skill, so I'm asking you for the edit instead of making it.

**What happened (11-07):** "At Long Last, Beta" was created on 11-04 as a building row for Saturday 11-07. Comms' memos called it building, I passed `--category building`, and it published that way. xian caught it: weekends are insights. The skill says to take the category from the calendar (line 313) and check "category alignment with calendar" (line 77), and the calendar was the thing that was wrong. Nothing in the skill compares the category to the weekday.

**The ask:** in the pre-flight, before `--category`, add: read the slot table from `docs/briefing/BRIEFING-ESSENTIAL-DOCS.md` (section "Publishing Slots and Syndication") and confirm the row's `theme` matches its pubDate's weekday. Stop and ask Comms if it doesn't.

**What I already did, in my lane:**
- `scripts/validate-editorial-calendar.py` now warns on any open row (planned, drafted, queued, ready-for-docs) whose theme breaks the slot table. Tested: it flags the 11-07 row when reverted, and 0 open rows warn today. History is not checked, because 167 distributed rows predate the current cadence.
- The slot table and syndication targets are now in my briefing. Before this they lived only in shared memory, which is why xian's question, "how can we expect long-established cadences to be in your memory", has no good answer except putting them where the action happens.

Verified how: ran the validator on the real calendar and on a reverted copy, and counted the weekday mismatches across all rows with a pubDate. Layer: script output, not a live publish. Denominator: all 475 rows.

— Docs
