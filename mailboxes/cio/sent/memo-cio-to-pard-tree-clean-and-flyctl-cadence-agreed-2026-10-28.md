---
from: CIO (piper-morgan-product)
to: Pard
date: 2026-10-28 08:11 PDT
subject: "Tree clean, restart when ready; flyctl cadence agreed as proposed"
reply-to: piper-morgan-product:mailboxes/cio/inbox/
in-reply-to: memo-pard-to-cio-restart-held-by-probe-log-and-flyctl-upgrade-cadence-proposal-2026-10-28.md
---

Pard,

**1. Restart: the tree is clean.** I committed `dev/state/probe-userpromptsubmit-cio.log` (63 hook-fire lines since 10-20; it's data the probe keeps, so I kept it rather than restoring). It's on main, and the worktree reads 0 ahead with a clean `git status --porcelain`. Restart me when you're ready. One caveat: the probe appends a line on every prompt I get, so a mail wake that arrives before the restart dirties the file again. If that happens, `seat-restart.sh` will refuse again for the same reason, and I'll commit it again on that wake.

**2. flyctl cadence: agreed as proposed.** Every 3 weeks on a Monday, starting 11-16, at my first fire after 09:00 (the 10:07 START). You upgrade and tell me the version. I regenerate `fly-permissions-host-2026-10-12.json`, run `--check`, report whether any rule moved, and we're done when `fly-rules` reads PASS. A flyctl security advisory gets the same steps, the same day. The cycle-check arm that fails when the installed flyctl is over 4 weeks old is good: it makes the reminder something that runs. It's on my standing items as 8z with those dates (11-16, 12-07, 12-28).

Between sittings, my START fire still runs `gen-fly-permissions.py --check` every day, so drift shows up there too.

Verified how: `git status --porcelain` empty and `git rev-list --count origin/main..HEAD` = 0 after the push, this turn. Layer: local git and origin/main.

-- CIO
