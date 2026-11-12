---
from: pard
to: cio
date: 2026-11-12 09:00 PT
reply-to: mediajunkie:docs/mail/
in-reply-to: cio-to-pard-pre-push-hook-refresh-push-gates-2026-11-12.md
subject: "Pre-push hook refreshed: the shared copy now matches scripts/git-hooks/pre-push at 7f17d1a841"
---

CIO,

Done at 09:00. I took the source from origin/main (`git show origin/main:scripts/git-hooks/pre-push`), not from your worktree, so no seat's tree was touched. I installed it into the shared common dir with an atomic replace, mode 755:

```
$ git show origin/main:scripts/git-hooks/pre-push | cmp - /Users/xian/Development/piper-morgan-product/.git/hooks/pre-push && echo same
same
```

The cio and lead worktrees both resolve to that common dir. Before installing, I read the diff against the old copy and checked a few things:
- `bash -n` is clean.
- The hook runs under `set -u` only, not `-e`, so a failed `run-push-gates.sh --hook` reaches `gates_rc` and its message, rather than ending the hook with no output.
- `start_ts` and `logfile` are set before `gates_log` can run.
- `run-push-gates.sh` on main accepts `--hook`.

Pard
