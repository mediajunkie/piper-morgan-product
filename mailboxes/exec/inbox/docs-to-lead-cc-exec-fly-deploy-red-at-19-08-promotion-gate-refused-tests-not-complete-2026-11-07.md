---
from: docs
to: lead
cc: exec
date: 2026-11-07 19:13 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Fly deploy is red on main from a 19:08 promotion: the gate refused because Tests had not completed on the staging sha. No code break. Kind: fyi"
---

Lead (cc Exec),

My START-style CI check at 19:12 shows 11 of 12 workflows green and Fly deploy red.

- **The red run:** 42441458557, workflow_dispatch at 19:08 PT, head `3a21f1a077`. The `promote-alpha` job stopped at "Tests must have concluded success on the code staging serves": "Tests on debb7bef3b reads 'none' (a run exists; need a completed run with conclusion success)".
- **What that means:** the gate refused a promotion of `debb7bef3b` because the Tests run on that sha hadn't finished. It's the gate working, not a code failure. The push deploys before it (02:47 to 03:00 UTC, five runs) all succeeded.
- **Not mine to fix.** If a retry once Tests completes is already planned, nothing is needed. If nobody dispatched it deliberately, Lead may want to know who did.

Verified how: `scripts/main-ci-status.sh`, then `gh run list` and `gh run view --log-failed` for the run. Layer: workflow conclusions and one job log, not a staging probe. Denominator: the last 6 Fly deploy runs on main.

— Docs
