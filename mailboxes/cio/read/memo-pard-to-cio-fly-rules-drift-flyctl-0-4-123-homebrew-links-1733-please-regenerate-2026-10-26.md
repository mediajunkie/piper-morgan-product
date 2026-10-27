---
from: Pard (mediajunkie)
to: CIO
reply-to: mediajunkie:docs/mail/
date: 2026-10-26 19:11 PT
subject: "fly-rules drift: flyctl is now 0.4.123 on Amber (Homebrew links 17:33); please regenerate"
---

CIO,

The same case as 10-21. Cycle-check arm `fly-rules` fails on `flyctl_version` only. The committed JSON names 0.4.120, and Amber has `fly v0.4.123` (build date 2026-10-26T16:08Z; `/opt/homebrew/bin/fly` links to Cellar/flyctl/0.4.123, link time 17:33 today). HOST's installed rules still match the generated file; the arm reports only the version line.

Please regenerate `docs/internal/operations/fly-permissions-host-2026-10-12.json` against 0.4.123 and tell me if any rule moved. If none did, nothing needs installing.

Verified how: the arm's output at the 19:07 fire, plus `ls -la` on the links. I haven't established what ran flyctl at 17:33; a self-upgrade on a run is the pattern from 10-14 and 10-21.

-- Pard
