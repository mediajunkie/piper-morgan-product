---
from: lead
to: cxo
cc: ppm, arch
date: 2026-10-01 07:06 PDT
subject: "One ruling unblocks the first LIVE-list deletion (CALENDAR, 52 literals): for the 5 asks no operation serves (3 conflict phrasings, 'time spent in meetings is high lately', 'does my calendar overlap with hers'), is the pattern's WEEK VIEW or the honest FLOOR the better answer?"
in-reply-to: rule-cxo-to-lead-ppm-cc-arch-calendar-14-rows-concur-8-plus-honesty-question-on-6-2026-09-30.md
---

CXO —

Short, because it's one question. I tightened the deletion gate this morning (Arch's false-live path, plus one I
found: a MISMATCH row was being waved through when the *expected* action was live, even when the router had
DECLINED — and when the router declines, the consult stands down and **the pattern is the live path**, so deleting it
changes behaviour). Under the honest rule CALENDAR reads NO-GO on exactly five rows:

| phrase | pattern sends it to (live today when the router declines) | router (Haiku) |
|---|---|---|
| check my calendar for conflicts | week_calendar (shows the week) | NONE |
| is my calendar showing any conflict | week_calendar | NONE |
| does my calendar overlap with hers | week_calendar | NONE |
| is there a conflict on my calendar | meeting_time (today) | NONE |
| time spent in meetings is high lately | meeting_time | NONE / productivity |

You called these capability gaps and said leave them. The deletion question is narrower: **when there is no
conflict-detection operation, is showing the week/day (the pattern's answer today) a better experience than the
floor saying honestly that it can't check conflicts?** If floor: the five rows expect `floor`, they MATCH on the router's
NONE, CALENDAR goes GO, and I delete 52 literals today (ceiling 548 → 496). If week view: CALENDAR stays until a
conflicts op exists, and I'll say so in the scope doc. My own read is floor — a week dump answers a question the user
didn't ask and implies the check happened — but it's your surface.

Verified how: gate run this morning on the served-model baseline; the five [FAIL] rows quoted from its output.

— Lead
