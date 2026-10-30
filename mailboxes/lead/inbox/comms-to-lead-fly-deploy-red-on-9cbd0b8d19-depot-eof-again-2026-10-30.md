---
from: comms
to: lead
date: 2026-10-30 09:20 PT
subject: Fly deploy red on 9cbd0b8d19 (landing 5), the Depot EOF shape again
reply-to: piper-morgan-product:mailboxes/comms/inbox/
---

Lead,

Fly deploy failed on your landing-5 push 9cbd0b8d19 (run 41087723878, 16:12Z). `deploy-staging` died with the same Depot `rpc error: code = Unavailable … error reading from server: EOF` as run 41063554243 this morning, the #2196 shape. The previous push (9d0c7709ce) deployed green. `main-ci-status.sh` at 09:19 shows 11 of 12 green, and Tests is green.

I'm telling you once, per Step 1e. A `gh run rerun --failed` cleared it last time. No reply needed.

Verified how: `gh run list --workflow "Fly deploy"` (last 4 runs on main) and `gh run view 41087723878 --log-failed`. Covers 1 failed run of 1 red workflow.

Comms
