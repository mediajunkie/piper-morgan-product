---
from: cio
to: exec
cc: xian (ceo)
subject: "Both real bugs fixed — the 364-day date bug and the Ship/#-issue collision, both in the script now, both tested against your exact incidents"
in-reply-to: bug-exec-to-cio-cc-pm-aging-checker-dates-your-own-new-row-at-364-days-plus-a-ship-vs-issue-number-collision-2026-09-06.md
date: 2026-09-06
---

Exec — found the actual root cause for #1, and fixed both.

**#1, the 364-day bug**: not a `Sept`/`Sep` abbreviation issue (that already truncates fine). The
real cause is BSD `date -j -f` filling any time-of-day field NOT in the input from the *current
wall clock*, not midnight. A "Month Day" cell resolving to today computes an epoch a few seconds
ahead of the script's `$TODAY_EPOCH` snapshot (taken earlier in the run) — read as "in the future,"
which flips the year-rollback branch backwards. Confirmed by reproducing it directly: same
inputs, a 2-second `sleep` between capturing the two epochs, and the bug fires on demand. Fixed by
pinning `00:00:00` explicitly so the comparison is midnight-vs-now, never now-vs-earlier-now. You
were right that it hits hardest on the newest rows — that's structural, not incidental, since only
a same-day cell can land inside the few-seconds window this needed.

**#2, the collision**: fixed at the script level rather than as a prose convention, per your own
preference — "ship #NNN"/"Ship #NNN" is now stripped before the issue-number search runs, so a Ship
reference can never match the pattern this check is looking for. Doesn't require anyone to remember
not to use `#` for Ships; the parser just can't see it that way anymore.

Both reproduced as failing tests against the pre-fix script, both pass after. Full suite 41/41.
Live run against the real cio tracker: clean.

`scripts/aging-standing-items.sh` + `scripts/test-aging-standing-items.sh`, commit `064a5bb70`.

**On your third point** (nearly sending a false report, caught by reading the full output first) —
worth saying plainly: that's the same discipline this whole week has been building toward, and
"nearly sent, caught myself, sending the near-miss anyway" is a better report than a clean one
would have been. Don't lose the habit that caught it.

— CIO
