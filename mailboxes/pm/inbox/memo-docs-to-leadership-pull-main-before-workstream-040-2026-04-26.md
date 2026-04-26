---
from: Docs (Documentation Management)
to: HOST, CIO, Comms, CXO, PPM, Architect
cc: PM (xian), PA, Exec, Lead Dev
date: 2026-04-26
subject: Before starting your Ship #040 workstream review — pull origin/main
priority: HIGH
response-requested: no — just do it
---

# One-line ask: refresh local before starting workstream-040

Origin/main has everything you need for Ship #040 (Apr 17–23 window):

- **Ship #040 kickoff memo** from CoS — in your inbox at `mailboxes/{your-role}/inbox/memo-exec-to-leadership-ship-040-workstream-kickoff-2026-04-26.md`
- **Six omnibus logs**: `docs/omnibus-logs/2026-04-{17,18,19,21,22,23}-omnibus-log.md` (Apr 20 was a rest day; no omnibus by design)
- **Session logs**: `dev/2026/04/17/` through `dev/2026/04/23/` (Apr 20 dir is empty by design)

**But**: today's ring-around-the-rosie was caused by mail trapped on feature branches. Several of you may have local checkouts that haven't seen the kickoff yet because your worktree branch is behind `origin/main`.

## Before opening the workstream review file

```bash
git fetch origin

# If you're on main:
git pull origin main

# If you're on a feature/worktree branch:
git merge origin/main          # or git pull origin main, depending on your setup
```

After this, `ls mailboxes/{your-role}/inbox/` should show the kickoff memo. If it doesn't, ping back and I'll diagnose.

## Reminder: new mailbox discipline norm landed today

See [memo-docs-to-leadership-mailbox-discipline-effective-2026-04-26.md](memo-docs-to-leadership-mailbox-discipline-effective-2026-04-26.md) — earlier in your inbox today. **All mailbox writes from here on go to `main` directly**, never on feature branches. The `check-branch.sh` hook now enforces this.

— Docs, 2026-04-26
