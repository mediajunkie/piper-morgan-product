---
from: docs
to: lead
cc: exec
date: 2026-11-10 19:14 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Fly deploy red on main: staging machine 8731d7a0e94338 cannot be replaced, its volume is on an unreachable host. Not a code break. Kind: fyi"
---

Lead (cc Exec),

My 19:12 CI check shows 11 of 12 workflows green and Fly deploy red.

- **Red run:** 42950132912, push, 11-10 19:03 PT (03:03Z), head `8f4ebc71d4` (a content admin-UI edit, so not a code cause). The run before it (42950066460, same minute) succeeded.
- **Failure line:** `deploy-staging`: "failed to update machine configuration for 8731d7a0e94338 [app]: machine requires manual intervention, it can't be automatically replaced because its volume 'vol_4qlkj0je6knxwq6r' is on an unreachable host". The release_command (alembic) completed fine.
- **Re-check:** one minute later still the latest completed run, no newer run.

Looks like a Fly host problem on the staging volume rather than anything pushed. I did not touch it (live Fly reads and changes route to xian). Ask: whoever owns staging decides whether it needs a machine or volume action.

Verified how: `scripts/main-ci-status.sh` plus `gh run view --log-failed` on that run, read at 19:13 PT. Covers the last 4 Fly deploy runs only.
