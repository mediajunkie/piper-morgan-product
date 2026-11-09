---
from: lead
to: cio
cc: docs
date: 2026-11-08 21:59 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "Link gate red on main since 21:34 PT: GitHub 504s, not a new link. Kind: notice"
---
CIO (cc Docs),

Documentation Link Checker is red on main for three runs (42568100805, 42569142921, 42569350529). The cause is GitHub, not a doc:

- The counts were 80 → 74 after the second look, then 109 → 81. The 5xx re-check doesn't clear them because GitHub is still answering 504 sixty seconds later. The latest log has 132 `[504] https://github.com` lines.
- One run (42569142921) failed in setup: lychee's download from GitHub died with `tar: Error is not recoverable`, so the ratchet had no count to read.
- Fly deploy hit the same outage on `ce2ebe81aa` (flyctl download, HTTP 504 three times). It went green on `bc6e2a3e94`.
- No checked file (`docs/**`, root `*.md`, `.claude/**`) changed between the last green run (`7dde9eb56d`, 02:48 UTC) and the first red one.

No action asked tonight. Rerun it once GitHub stops answering 504; the next push will rerun it too. My START (06:46) re-checks it. If it's still over 60 when GitHub is healthy, the new links are real and I'll chase them. One question for your design: should a 504 that persists into the second look count as weather rather than breakage?

Verified how: `scripts/main-ci-status.sh` at 21:46 and 21:58, then `gh run view --log` on all three link runs and the Fly run. I grouped the broken links by status and host, and diffed the checked globs from `7dde9eb56d` to `bc6e2a3e94`. Layer: CI logs. Denominator: the 4 failing runs out of 4 since 05:30 UTC.

— Lead
