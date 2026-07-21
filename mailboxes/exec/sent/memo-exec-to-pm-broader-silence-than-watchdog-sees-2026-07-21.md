---
from: exec
to: xian (ceo)
subject: "Broader than the watchdog alert: 9 of 10 other roles haven't fired since Jul 19, not just Arch"
date: 2026-07-21 09:15 PT
---

PM — you've likely already seen this morning's watchdog alert flagging Arch (41h stale). Worth knowing it's actually part of a bigger pattern the automated system can't see, since it only monitors 4 roles (arch/lead/cio/exec).

**Checked the full roster directly this morning**: every role's last session log is Jul 19, except Lead (fired this morning, 06:47) and me. That's Arch, CIO, Comms, CXO, Docs, HOST, PA, PPM, and Web — 9 of 10 other roles, all quiet through the entirety of Jul 20.

**What I don't know**: whether this is one cause (a cohort-wide cron-kill, same shape as the Jul 13 reauth event or the Sunday laptop crash) or several unrelated ones. I haven't found a "cohort-wide" watchdog alert for it — just the narrower Arch-specific one, since the other 6 quiet roles fall outside what's automatically monitored.

**Ask**: if you haven't already, worth a broad re-prod/wake pass rather than treating this as an Arch-specific stall — the same fix that resolves one session-scoped cron death usually resolves all of them from the same cause. Not urgent-urgent (nothing appears to have broken from the silence itself), but the scope is bigger than the one alert you've seen suggests.

— Exec
