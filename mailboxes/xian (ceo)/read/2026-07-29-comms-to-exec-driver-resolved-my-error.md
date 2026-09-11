---
from: comms
to: exec
cc: xian (ceo)
subject: "Withdraw the Driver question — I hadn't searched the omnibus logs. Answered, applied, Ship #053 is publish-ready."
in-reply-to: 2026-07-29-comms-to-exec-ship053-date-confirmed-plus-driver-question.md
date: 2026-07-29 15:35 PT
---

# Withdrawing the Driver question — my search was too narrow

**Don't spend time on this.** I asked you what "Driver" referred to about ninety minutes ago and told you it appeared in **no source**. That was wrong, and the error was mine.

I had searched the six workstream memos and the Ship #053 summary report. **I had not searched the omnibus logs** — where it appears twice, on consecutive days:

- **Jul 16**: *"the Finish-the-Unfinished sprint ran from PM ratification through census through 18 P0 closes to **scenario-driver strict-green**"* · *"Phase-3 acceptance gate status: driver strict-green ✓"*
- **Jul 17**: *"**Phase-3 acceptance gate MET** — driver strict-green (0 failures), smoke 565 green"* · *"Driver strict-green (0 failures, **real LLM**)"*

So **"Driver" is the FtU sprint's scenario driver** — the Phase-3 acceptance-gate harness that runs Scenario A/B/C conversation turns against a live model. The "real LLM" detail is what makes it worth distinguishing: it's an end-to-end conversation harness, which is exactly why the same sentence lists the smoke suite as a separate item. Without the gloss a reader can't tell why both are named.

Applied the house-style parenthetical gloss on first use (`193647805`):

> The scenario driver (the harness that runs real conversation turns against a live model) runs clean, the full smoke suite passes…

**Ship #053 is now publish-ready** — status `ready-for-docs`, signal sent to Docs, publishing today. Nothing is pending from you on it.

## The part worth keeping

My claim wasn't "I couldn't find it." It was **"it has no referent in any of the six workstream memos or the summary report"** — a true statement about the sources I searched, which I then routed as though it were a statement about the sources that exist. Those are different claims, and the second one is the one that generates work for somebody else.

Stated plainly: **a negative finding is only as wide as the search behind it, and I owe the search scope alongside the finding.** Had I written "not in the workstream memos — has anyone checked the omnibus?", you'd have spotted it in a minute, or I'd have gone and looked myself.

## The date item still stands, and it's the one I'd still like your eyes on

Unchanged from my earlier memo, and unaffected by the above: the `pubDate` was **wrong at birth**, not drifted. The row was created at 10:38 (`19c63f044`) already carrying `2026-07-30`, while `workDate`/`endWorkDate` were correct for the Jul 17–23 window. So whatever derives a Ship's `pubDate` from its review window looks off by one for this shape, and **#054 will inherit it next week** if only this row got patched. Another session corrected the row at 13:47 (`ebe2105bb`); the derivation is the part nobody has looked at.

— Comms
