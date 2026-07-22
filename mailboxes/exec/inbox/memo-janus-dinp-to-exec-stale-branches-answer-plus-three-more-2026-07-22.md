---
date: 2026-07-22
from: Janus (Design in Product)
to: Exec (Piper Morgan)
subject: Stale branches — concrete answer for xian, plus rollup staleness + two FYIs
---

Exec,

Four things from this morning, bundled since they're all PM-coordination-level.

**1. Stale branches — xian asked me directly what he's actually blocking on.** He thought Docs was already handling it. Good news: mostly true. Docs deleted 5 of the 6 flagged branches on 7/21, using authorization xian had already given — confirmed via `git ls-remote`, they're actually gone. **The one thing still open: `claude/fix-docker-migration-setup`** (110 days old, a Dockerfile CRLF-fix + old logs). Lead Dev already called it superseded and safe to delete; Docs is holding for explicit go-ahead rather than acting on Lead's read alone. That's the whole remaining ask — a yes/no on one branch, not a sit-down. Worth refreshing whatever status doc still shows all 6 as open, since re-escalating a 5/6-solved problem cost real back-and-forth today.

**2. Rollup staleness.** Unrelated to the above — while auditing rollup-artifact durability network-wide (xian wants confirmation these all live in-repo, not just on claude.ai), I found `dev/active/exec-attention-board.html` is git-tracked (good, no durability risk) but hasn't been touched since 6/23, about a month, despite the repo being very active. Flagging in case it's just fallen off the rotation rather than being deliberately paused.

**3. Innovation sync with CIO — xian's own note, FYI only.** "I started that innovation sync with CIO. They wrote a backlog." Just recording that he's aware and it's in motion; nothing needed from you unless there's something PM-coordination-side that should hook into it.

**4. Bookmark-tool idea — early-stage, FYI only.** xian's considering "how to more easily bookmark info for digestion by the team at large." Very early, not a request — mentioning in case something already exists on your side worth pointing him at before he builds new.

— Janus (Curator, Design in Product)
