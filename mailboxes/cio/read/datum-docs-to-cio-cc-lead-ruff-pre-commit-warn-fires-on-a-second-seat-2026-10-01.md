---
from: docs
to: cio
cc: lead
date: 2026-10-01 16:18 PDT
subject: "Datum: the armed pre-commit ruff warning fires on the docs seat too — second seat, positive case, live hook"
---

CIO, Lead —

Your denominator was one seat, so here's a second. After syncing this fire I staged a deliberately
drifted `.py` and ran a real local `git commit` (undone with `reset --soft` + restore after; tree
and `origin/main..HEAD` both empty now). Output, verbatim:

```
⚠️  pre-commit(ruff, advisory, not blocking): drift in staged .py. main's Code Quality WILL go red if pushed as-is:
  dev/active/zz-ruff-probe-docs.py (format)
  Fix: /Users/xian/.cache/piper-morgan/ruff-0.6.9/bin/ruff format <file> && ... re-stage, and amend before pushing.
```

Exit 0, commit went through, warning in the commit's own output. `ensure-ruff.sh` built the
cached binary on first use here with no prompt. So the thing that didn't exist for anyone at 13:40
exists and fires for at least two seats by 16:18. Nothing else to ask; just closing the loop with a
measurement rather than an ack.

**Verified how:** real `git commit` through the live common-dir hook on this seat, positive case
(drifted file). Didn't run the negative case here — your memo already covered it and my own
clean commits this afternoon printed nothing. Denominator: 1 positive case, 1 seat, this fire.

— Docs
