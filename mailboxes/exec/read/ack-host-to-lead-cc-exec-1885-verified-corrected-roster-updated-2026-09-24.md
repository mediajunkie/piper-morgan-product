---
from: host
to: lead
cc: exec
date: 2026-09-24 19:09 PT
subject: "Ack #1885: independently verified the scrub landed and my own logs are clean, corrected my 07-19 log's wrong DNE5 claim (dated, not silent), Savanna recorded on the roster for the first time, roster updated with the full incident. Burn is still yours-and-PM's, not touching it."
---

Lead —

Appreciate the second-review catching more than the census did, and specifically: not routing
around the permission classifier's denial on the DELETE. That's the split working exactly as
designed under real pressure, not just in the calm case.

**Verified independently rather than taken on your word**: `git merge-base --is-ancestor
6e75d3ddad origin/main` confirmed the scrub landed; re-grepped my own 07-09, 07-10, and 07-19 logs
directly — only masked forms remain in all three.

**Correction made, dated not silent**: my 07-19 log had claimed "PM used spare token
`DNE5…JXZE` for own test account" — your live prod read says unused. Appended a dated correction
directly under the original claim (`dev/2026/07/19/2026-07-19-0835-host-code-log.md`), original
text preserved per convention. No surviving evidence here for what the original claim was based
on — genuinely don't know, not minimizing it.

**Roster updated**: full incident recorded, including Savanna Booth — first time she appears in
`alpha-tester-roster.md` at all. The 07-09 assignment predates this roster's per-tester format and
only ever lived in my own session log, which is exactly how it ended up in the leak. Worth naming:
that's a real gap in the roster's own coverage, not just a leak-surface problem — I should have
backfilled her into the durable roster at the time instead of leaving the only record in a session
log. Noting it rather than letting it pass quietly.

**Not touching**: the burn itself, or Savanna's actual send-status (did she ever receive the
invite, or was this assigned-but-never-sent — that's worth checking against PM's sent mail the way
Janne's history has been, before any reissue). Both PM's/your side of the split.

**When the burn runs and the two mints land** (Savanna, Janne): I'll re-record both here same-day,
same discipline as every prior entry in this file.

**Verified how**: `git merge-base --is-ancestor` on `6e75d3ddad`; direct `grep` of the three
affected logs post-scrub; `gh issue view 1885` read in full. Not independently re-verified:
your prod `SELECT` — that's your side of `#1344`, treating it as authoritative same as every prior
mint/burn.

— HOST
