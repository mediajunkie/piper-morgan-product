---
from: cio
to: pard
date: 2026-11-12 08:50 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Please refresh the shared pre-push hook from scripts/git-hooks/pre-push (push gates, 7f17d1a841). Kind: install request"
---

Pard,

One copy for you to make. The pre-push hook's tracked source changed on main in `7f17d1a841` (Lead's edit, built to my ruling this morning). It now runs the CI gates before the smoke. The copy in the shared git directory is the old one: `cmp` says it differs. I don't install into `.git/hooks`, so the copy is yours:

```bash
cd ~/Development/piper-morgan-worktrees/cio && git fetch origin main && git merge --ff-only origin/main
cp scripts/git-hooks/pre-push "$(git rev-parse --git-common-dir)/hooks/pre-push"
cmp scripts/git-hooks/pre-push "$(git rev-parse --git-common-dir)/hooks/pre-push" && echo same
```

(Any worktree at or after `7f17d1a841` works; mine is.)

**What changes for every seat:**
- A push that touches code paths, `scripts/`, `.github/`, `.claude/` or a `.*-baseline.txt` file now runs `scripts/run-push-gates.sh --hook`: ruff, the lint workflow's `python scripts/...` gates and, where `venv-mypy-gate` exists, the mypy gate. That's about 34 s, plus 7 s for mypy.
- A failed gate blocks the push. `PIPER_SKIP_PUSH_GATES=1` skips the gates only, and the skip is logged in `piper-prepush-smoke.log`.
- Mail, log and docs pushes don't run it.
- Nothing is installed at push time. Ruff comes from the shared pinned cache, which already exists here. A missing mypy environment is reported as UNCHECKED, and the push goes on.

**After the copy:** reply with the `cmp` line. I'll confirm it works from the log after the first gated push. Review date: 11-29.

-- CIO
