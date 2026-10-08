---
from: Lead
to: Exec
date: 2026-10-07 17:xx PDT
subject: "READY for PM (relay; no decision needed): alpha 99289b6690 is live with complete_todo on, and test-card rows A, C and D pass LIVE — served answers quoted. Row F is with Web. Three issues closed, two small ones filed."
---

Exec —

This is the "ready" the deploy manifest promised: deployed, then re-tested by me on the served answer.

**Alpha**: promoted today through the new workflow (run 37701277327, every step green; first successful run of that path ever). `/health` `99289b6690`; flag read on the host includes `complete_todo`.

**Row C** (PM's exact sentence; test account, its own key):
- "what reminders do I have?" → numbered, Due 1–4 and Upcoming 5–6, rendering correctly.
- "Mark the first three complete and leave the fourth one pending." → `Complete 3 reminders: "check the test card again" (2 items) and "review the pr"? Leaving "revise the pr" as is. (yes/no)`
- "yes" → `Marked 3 reminders done: • check the test card again (2 items) • review the pr / Left "revise the pr" as is.`
- The stored data matches (three completed, one pending).

**Row D**: "get issue 101" → issue #101 from the default repo (`mediajunkie/test-piper-morgan`).

**Row A**: "close issue 99999 in mediajunkie/test-piper-morgan" → confirm → `There's no issue #99999 in mediajunkie/test-piper-morgan — nothing was changed.` No more "couldn't verify".

**#1944** ("my default repo should be test-piper-morgan"): passes once the repo is registered on the account; PM's account has it.

**Closed with live evidence**: #1941, #1942, #1944 (and #1943's row-C comment). **Filed**: #1959 (the close confirm comes before checking the issue exists) and #1960 (the consent line says set-default-repo writes to connected tools; it writes Piper's own preference). Both small.

**Row F (#1913)** is with Web; it needs a fresh invite and a key from PM, routed through you (my memo to Web, cc you).

**Spend**: about 16 chat turns on the test account's key, ≈ $0.45–0.50, inside PM's $1 approval.

Verified how: live `POST /api/v1/intent` turns on alpha (replies quoted verbatim), `GET /api/v1/todos` for row C's data, `fly ssh console printenv` for the flag, `/health` for the sha. Layer: served answers + stored data on the deployed host. Denominator: rows A, C, D (and #1944); F not run by me.

— Lead
