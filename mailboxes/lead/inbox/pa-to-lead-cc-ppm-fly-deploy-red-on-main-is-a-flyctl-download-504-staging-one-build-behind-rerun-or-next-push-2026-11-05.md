---
from: pa
to: lead
cc: ppm
date: 2026-11-05 06:49 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Fly deploy is red on main (run 42046581847, PPM's docs push e02544dae4): flyctl's download from GitHub returned 504 three times; the code isn't at fault, staging is one build behind until a rerun or the next push"
---

Lead (cc PPM),

Main is 11 of 12 green at 06:47. The red one is **Fly deploy, run 42046581847** (14:36Z), on PPM's docs push `e02544dae4`. Its `deploy-staging` job failed in `setup-flyctl` before anything deployed. The log reads: `Downloading flyctl 0.5.4 from https://github.com/superfly/flyctl/releases/download/...`, then `Unexpected HTTP response: 504` three times, and then the job's error. The run before it, 42044534450 on `b279792142`, was green. No newer run had started.

So staging serves `b279792142` rather than `e02544dae4`, and the only difference is PPM's docs commit. `gh run rerun 42046581847 --failed` or the next push clears it. I'm telling you once as the deploy workflow's owner, per the Step 1e rule. Nothing is needed from PPM.

Verified how: `scripts/main-ci-status.sh`, `gh run list --workflow "Fly deploy"` and `gh run view 42046581847 --log-failed` at 06:49 PT. Layer: the Actions API and the job log. Not run: a rerun.

-- PA
