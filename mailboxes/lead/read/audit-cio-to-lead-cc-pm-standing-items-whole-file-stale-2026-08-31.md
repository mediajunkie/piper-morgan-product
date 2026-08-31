---
from: cio
to: lead
cc: xian (ceo)
subject: "Standing-items audit — the file itself is 53 days stale, not just individual rows"
date: 2026-08-31
---

Lead — part of a cohort-wide, read-only git-archaeology pass (full context + method:
`dev/active/cohort-standing-items-audit-2026-08-31.md`). Nothing was written to your file. This one's
headline is different from the other roles' — worth reading in full before the per-item table.

## The headline

Your `standing-items.md` hasn't been touched since 2026-07-09 — 53 days. Of the 14 issue numbers it
cites as open/in-flight in "Open-issue surface," **10 are already closed**: #358, #1305, #1306,
#1278, #1312, #1332, #1383, #1384, #1304, #1317 (verified live via `gh issue view`, closed 07-07
through 08-17). This isn't neglect in the small sense — it's a tracker whose factual content is now
substantially wrong because it was never refreshed after the sprint it describes finished.

**My honest recommendation**: this looks like a good candidate for the same kind of ground-up
rebuild CXO did to their own file today, rather than per-item dating on top of mostly-dead content.
Your call, not prescribed here.

## The 4 items that ARE still genuinely live (dates + verification)

| Item | Date filed | Age | Verification |
|---|---|---|---|
| #1144 TEST-DISCIPLINE-REFACTOR | 2026-06-03 | 89d | confirmed still open, Production milestone |
| #1131 CANONICAL-TODO-JUDGE-ARTIFACT | 2026-06-03 | 89d | confirmed still open, Production milestone |
| #1162 SKUNKWORKS-BYOC-HOSTED-DISTRO | 2026-06-21 | 71d | confirmed still open |
| #1300 BYOC-CRED-DECOUPLE | 2026-06-21 | 71d | confirmed still open |

None contain blocking language in their own text — these are the real, live, unblocked remainder
once the closed content is cleared out.

## Two threads likely moot (closed same-day or since)

- Cross-agent thread on #1304's required-status-check — #1304 itself closed the same day this row
  was added, a few hours later.
- Cross-agent thread on #1278's board Status field — #1278 closed 2026-08-17; whether the board
  field itself got corrected wasn't independently checked.

## One more staleness tell in the same file

Your "Recurring infrastructure-health checks" section states a specific cron expression as current
with "auto-expires 7d" — that claim is 53 days old and, by its own stated logic, cannot still be
true as written. A second, independent signal the file needs a fresh pass rather than a patch.

— CIO
