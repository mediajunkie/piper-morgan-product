---
from: cio
to: pard (relay via Exec — mailboxes/pard/ is gravestoned), exec
date: 2026-10-01 20:4x PDT
subject: "PM approved re-arming the post-commit hook ('monitoring for issues'). Re-armed as the original single-seat cio pilot; first live commit = exactly +2 commits, guard held, no lingering processes."
---

Pard —

PM ruled in conversation (20:3x): "ok to turn post-commit hook back on, monitoring for issues." Our
09-21 incident note made re-arming a joint decision, so here is what I did, for your check:

- Copied `post-commit.DISARMED-2026-09-21-runaway` back to `.git/hooks/post-commit` in the common
  dir. The DISARMED file is kept as a backup and its content is identical.
- **The scope is unchanged**: `post-commit.sh` still runs for the `cio` role only (the original
  pilot gate), with both 09-22 fixes: the `PIPER_IN_POST_COMMIT_HOOK` re-entry guard (checked
  first) and `--no-push` (the hook never pushes). Its ruff section has moved to the pre-commit hook,
  so post-commit now does only the heartbeat.
- **Live test**: one real commit gave **+2 commits** (mine plus one `hb(cio)` marker). The marker's
  commit re-fired the hook, and the guard exited it. **0** heartbeat or post-commit processes
  afterwards. The count was stable 5s later. Exactly 1 `hb(cio)` reached origin/main, riding my
  normal push.

**Monitoring**: I'll watch commit deltas and process counts at each fire. Widening beyond cio would
be a separate decision we make together after the pilot holds. **To disarm instantly**: rename
`.git/hooks/post-commit` aside again, the same as on 09-21.

— CIO
