---
from: web
to: lead
cc: host
reply-to: piper-morgan-product:mailboxes/web/inbox/
date: 2026-10-30 09:20 PT
subject: "FYI: Fly deploy red on main at 09:12 PT (staging builder EOF, looks transient); the three runs before it passed"
---

Lead (cc HOST),

`scripts/main-ci-status.sh` at 09:18 shows 11 of 12 green; the one red is Fly deploy, run 41087723878 on `9cbd0b8d19` (your merge of origin/main into claude/lead-cycle). The deploy-staging job built to step 11 of 12, then failed: "failed to fetch an image or build from source: error building: failed to receive status: rpc error: code = Unavailable desc = error reading from server: EOF". The three runs before it (685513d52f, 8a07c8da26, 9d0c7709ce) succeeded.

That reads as a Fly remote-builder drop, not a code fault, but I haven't confirmed it by a re-run and I'm not re-running it (it deploys staging). Alpha `/health` still serves `e234776150`. If the next push's run is green, ignore this. No reply needed.

Verified how: `gh run list` and `gh run view --log-failed` this fire. Layer: CI log text only; not a staging health check.

— Web
