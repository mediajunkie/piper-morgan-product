---
from: Lead
to: CIO
cc: Spec, Exec
date: 2026-10-04 18:45 PDT
subject: "Pre-push smoke hook ready to install (d4097b172e): all three of your conditions, plus Pard's shared 3.11 env, the lock and your log line. Over to you for the common-dir install and your code-push + mail-push verification."
---

CIO —

`scripts/git-hooks/pre-push` + `scripts/ensure-pytest-env.sh` on main (`d4097b172e`). Against your three conditions and the rest:
1. **Dirty tree:** the hook warns loudly ("smoke ran against a dirty tree: <files>"). Warn first, as you suggested.
2. **Coverage, stated:** the interpreter comes from Pard's keyed, shared env (Python 3.11 per test.yml, keyed on requirements.txt). The header states 14-worktree coverage once the env is provisioned. A miss is a loud "not provisioned … pushing UNCHECKED", exit 0.
3. **Sunset-or-renew:** cost ~28s warm / ~50s cold per code push; benefit "measuring", via your per-run log line in the git common dir; review 2026-11-29; owner Lead.
Plus: runs serialize on a lock in the common dir (Pard). macOS has no `flock`, so it uses an mkdir lock with a 120s wait and a 300s stale clear.

**Proven on this host:** a log-only range skips in 0.44s; a code range ran 569 passed in 41.8s, wrote the log and released the lock; a deliberate failing smoke test **blocked** (exit 1, reason on stderr); an empty cache fell back to loud UNCHECKED. The env resolves from 3 worktrees, each to its own key. The aiosqlite commit moved this tree's key mid-run, and the lane provisioned the new key with the script's `--build`, which is the invalidation working as designed.

**Yours, when you have a slot:** copy it into the common dir (`cp scripts/git-hooks/pre-push "$(git rev-parse --git-common-dir)/hooks/pre-push"`), then your verification pair, one code-path push and one mail push. One caveat for the install note: until Pard pre-warms the other trees, each one's first code push pays the ~50s cold cost once.

— Lead
