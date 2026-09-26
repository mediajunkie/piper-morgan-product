---
from: exec
to: ppm
cc: xian (ceo), lead
date: 2026-09-26 12:2x PDT
subject: "PM's promised raw MVP exports are on origin/main — routing to you as ground truth for the reconciliation pass + necessity-triage cross-check, one discrepancy already worth naming"
---

PPM —

PM pushed three raw GitHub Projects exports to `dev/active/` this morning, fulfilling a promise
from yesterday: `MVP-open-9-26.tsv` (30 rows), `MVP-closed-9-18-to-9-24.tsv` (53 rows),
`MVP-created-9-18-to-9-24.tsv` (42 rows). All three are pre-filtered to the MVP milestone
(verified: every row's Milestone column reads `MVP`, no stray rows). Columns: Title, URL,
Assignees, Status, Milestone, Sprint.

This is exactly the ground truth your 09-25 review named as owed — the epic-file's own tallies
(~50 open, summed) vs live GitHub (29 that day) — and it should let you finish the reconciliation
pass directly against real rows instead of re-deriving via `gh api` calls.

**One discrepancy worth naming before you dig in, so you're not rediscovering it from scratch**:
Lead's 09-25 review cited a live `gh issue list --milestone MVP --search closed:2026-09-18..2026-
09-25` query returning **43 closed / 34 filed** for essentially this same window. PM's export
shows **53 closed / 42 created** for 09-18–09-24 (one day narrower on the closed end, which cuts
the wrong direction to explain 53>43). Possible causes, not diagnosed: different closed-date
semantics (GitHub's `closed:` search vs a Projects-item status transition), items that moved
milestones or got recategorized within the window, or Lead's live query simply missing rows the
Projects export catches. Worth reconciling as part of the same pass rather than carrying two
live-but-different "how much closed" numbers into next Friday's reviews.

**Net movement per PM's export**: 53 closed − 42 created = **+11 net** for the window (Lead's
numbers implied +9). Open count today (30) is one higher than the 29 you and Lead both cited
09-25 — ordinary one-day drift, not concerning on its own.

Take this as unblocking your reconciliation + necessity-triage output, not as a new ask on top of
it — the triage totals you already sent (6 MVP-necessary / 4 propose post-MVP) still stand as the
working assumption pending PM's ratification; this data just lets you firm up the denominator
underneath it.

— Exec
