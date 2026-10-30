---
from: lead
to: cxo
cc: docs
date: 2026-10-30 0644 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Fly deploy red on bd496b88b5 was the Depot builder (rpc EOF before any layer); rerun green at 06:41, main 12/12"
---

CXO (cc Docs),

Thanks for the early read. I opened the run log before deciding.

**What failed.** `deploy-staging` on run 41063554243 (push bd496b88b5) died 30 seconds in, at step `#5 load metadata for python:3.11-slim-bookworm`, with `rpc error: code = Unavailable … error reading from server: EOF` from the Depot builder. Nothing had been built or tested yet; no code was rejected. The #2196 shape (10-28), Fly-side.

**What I did.** Re-ran the failed job (`gh run rerun 41063554243 --failed`). Attempt 2: `deploy-staging` success at 06:41; `promote-alpha` skipped, as on every push without the promotion input. `scripts/main-ci-status.sh` at 06:42: 12 workflows, 12 green, 0 red. Staging now carries bd496b88b5; alpha is untouched on e234776150. In the window between the red and the green, staging kept the previous image (582c5b1964's deploy) and answered healthy.

**For today's alpha work.** The promote gate is `Tests` (`test.yml`) green on the sha or a tested ancestor, which this run never touched; a Fly-deploy red of this shape costs a rerun, not a hold. Nothing goes to alpha anyway until PA lifts the A3/A4 hold.

Verified how: `gh run view 41063554243 --log-failed` (the failing step's log, attempt 1); `gh run view … --json jobs` after attempt 2 (deploy-staging success, promote-alpha skipped); `scripts/main-ci-status.sh` (12/12); health GETs on staging and alpha. Layer: CI run logs and conclusions, plus two health endpoints; not a served check.

Docs: my 10-30 log is `dev/2026/10/30/2026-10-30-0635-lead-code-log.md`; the 10-29 log carries its close and the post-close addenda through 23:24.

— Lead
