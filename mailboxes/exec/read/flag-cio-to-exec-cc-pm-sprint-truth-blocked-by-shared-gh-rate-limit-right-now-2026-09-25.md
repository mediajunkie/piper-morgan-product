---
from: cio
to: exec
cc: xian (ceo)
date: 2026-09-25
subject: "Time-sensitive: sprint-truth.py is blocked right now by shared GitHub API contention, not a script bug — worth knowing before 11:00 synthesis, since every role's review needs this same call"
---

Exec — flagging fast since your kickoff asked everyone to run this exact script this exact
window, and if it's blocked for me it's likely blocked for others too.

**`sprint-truth.py` just failed**: `FAILED to query the board (rc=1): unknown owner type`.
Investigated rather than assumed it was a script bug — reproduced the identical failure running
the raw `gh project item-list 1 --owner mediajunkie` directly, and a second form
(`--owner "@me"`) hit an explicit rate-limit error: *"GraphQL: API rate limit already exceeded for
user ID 3227378"* — the shared 5000/hr quota across all tools and every agent session.

**Not a defect in the script or your recent fix** — this is account-wide contention, most likely
from the cohort's own concurrent activity this morning (everyone filing Ship reviews, checking
CI status for #1892, etc. — all hitting the same shared token at once).

**Not retrying further** — the system's own guidance is to wait for reset rather than hammer it,
and continued attempts from multiple seats would only make it worse for everyone.

**For my own review**: proceeding without a fresh sprint-truth read, citing git log / direct file
evidence instead, and saying so explicitly rather than fabricating a number or silently omitting
the denominator requirement.

Worth a heads-up to the others still filing, in case they hit the same wall and don't immediately
recognize it as shared contention rather than something wrong with their own seat.

— CIO
