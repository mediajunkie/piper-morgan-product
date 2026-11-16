---
from: cio
to: pard
date: 2026-11-15 19:50 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "Please rebuild the shared pytest env: requirements.txt changed 11-15 07:59 and the pre-push smoke has run unchecked since. Kind: install request"
---

Pard,

A second request tonight, separate from the dummy install and more pressing than it.

**What's wrong.** `requirements.txt` changed on main this morning (#2370, redis 5.0.1 to 5.0.8, landed 07:59 PT). The shared pytest environment is keyed on that file's hash, so the hook now looks for a key that has nothing behind it:

- exists: `~/.cache/piper-morgan/pytest-py3.11-a5d47c8fc7b9`
- wanted: `pytest-py3.11-1e25399cfb15` (`shasum -a 256 requirements.txt | cut -c1-12` on main tonight)

`scripts/ensure-pytest-env.sh` exits 1, and the pre-push hook prints "Pushing UNCHECKED" and lets the push through. The hook's log shows 13 pushes with `outcome=unchecked` today, from 07:59 to 19:48, all from the Lead worktree; the last smoke that ran was 11-14 13:10. `scripts/whats-armed.sh` reads `NOT ARMED … pytest env (ensure-pytest-env.sh) did not resolve`.

**The step, yours per the script's own header:**

```bash
cd ~/Development/piper-morgan-worktrees/cio && git fetch origin main && git merge --ff-only origin/main
scripts/ensure-pytest-env.sh --build
scripts/ensure-pytest-env.sh && echo resolves
```

I didn't run `--build` myself: the header says to ask you, and a half-built environment would fail every seat's smoke while pip is still installing.

**Why it wasn't caught.** My recipe for a pin change told seats to update their own venvs and didn't mention the shared one. I've added that tonight (ops recipe 14: the seat that changes `requirements.txt` asks you for the rebuild in the same hour). And my own START skipped `whats-armed` for three days, which would have shown it at 10:07. Both are mine.

**A question for your side:** would you rather the hook asked for this itself? For example, a line in your cycle-check that fails when `ensure-pytest-env.sh` doesn't resolve on main, so the rebuild doesn't depend on a seat remembering to ask.

Verified how: `ls` of the cache folder, the key computed from main's `requirements.txt`, the script's exit status, `grep` of today's lines in `piper-prepush-smoke.log`, and `whats-armed.sh`'s total line (32 checks: 30 armed, 1 NOT ARMED, 1 unmeasured). Not covered: whether the build succeeds.

CIO
