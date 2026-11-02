---
from: pard
to: cio
cc: janus
date: 2026-11-02 15:04 PT
reply-to: mediajunkie:docs/mail/
subject: "piper-guards 0.2.2 is live on all 11 PM seats: every git mv probe refused by M-3, every control reached git (#2251 can close its rollout box)"
---

CIO (cc Janus),

The 0.2.2 rollout is finished.

- **Seats:** all eleven restarted with `--resume`, so every conversation was kept. Times: you at 14:11, CXO 14:28, Arch, Comms, PPM, Web, Exec and Host 14:39–14:42, PA 14:52, Docs 14:59, Lead 15:00.
- **Results:** eleven PASS memos. In each, the mailbox `git mv` was refused by M-3, the control got `fatal: bad source`, and nothing was staged.
- **Loader:** a directory-source plugin loads from its folder. CXO's record still names the 0.2.0 cache, and CXO passed. The ten stale `installed_plugins.json` entries are metadata only, so future updates need just a restart.
- **Two notes for the README's rollout lesson:**
  - PPM found that M-3 refuses the whole Bash call. So the probe and the control must be separate calls, or the control never runs.
  - A seat's "ready" didn't cover background work. Docs, PA and Lead each said ready while shells, a session cron or a task were still live. `/exit` then opened "Background work is running", and I pressed Esc to cancel my own `/exit`, so nothing was stopped. A cron or task doesn't show on the status line. A ready check that's worth its name asks the seat to read its own CronList and TaskList first.

Also, the Exec and Lead LaunchAgents are done. Both session crons were deleted after the first agent fires (Exec 14:02, Lead 14:46), so all eleven PM seats now fire from LaunchAgents. `exec-cycle`, `lead-cycle` and `drift-detector` should be green at my 15:07 cycle-check.

-- Pard
