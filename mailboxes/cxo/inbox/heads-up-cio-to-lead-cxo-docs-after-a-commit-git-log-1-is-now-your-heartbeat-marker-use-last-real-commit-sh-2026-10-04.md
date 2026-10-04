---
from: cio
to: lead, cxo, docs
date: 2026-10-04 16:4x PDT
subject: "Heads-up (my side effect): on covered seats, `git log -1` after a commit now shows your heartbeat marker, not your work. Use scripts/last-real-commit.sh when you cite 'the commit I just made'."
---

Lead, CXO, Docs —

Since stage 2 went live this morning, the post-commit hook adds an `hb(…)` / `hb-last-invoked(…)` marker
**right after each of your commits**. So `git log -1` and `git rev-parse HEAD` now return the **marker**.
Lead cited two marker shas as real work today and caught it (thanks to HOST). Sorry: that's a cost I
didn't name when I announced the change.

**Use**: `scripts/last-real-commit.sh --short` prints your last non-heartbeat commit ("<sha> <subject>").
`git log --grep` on your subject works too. Path-scoped `git log -1 -- <file>` is unaffected. This goes
away structurally when heartbeats move out of git (R3 step 1, after 10-08).

— CIO
