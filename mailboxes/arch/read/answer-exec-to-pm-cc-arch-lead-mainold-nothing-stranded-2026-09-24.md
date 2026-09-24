---
from: exec
to: xian (ceo)
cc: arch, lead
reply-to: piper-morgan-product/mailboxes/exec/inbox/
date: 2026-09-24
subject: "main-old review COMPLETE: nothing critical stranded. 501 of 503 commits already on main by content; the only 2 absent are the obsolete 2025 sprint-creation scripts."
---

PM —

Your ask (09-23, via Janus) is answered, with the full report at
`dev/2026/09/24/mainold-503-review-2026-09-24.md` on `origin/main`.

**Bottom line: no missing cog.** Of the 503 commits on `main-old` that `main` lacks:

- **494 are content-identical** (patch-id equivalence via `git cherry`) to commits already in
  main's own history — they reached main by a different path, they were never stranded.
- **7 merge commits** individually inspected — none adds content beyond its constituents.
- **Exactly 2 commits are genuinely absent**: the October-2025 manual sprint-creation workflow
  (`HOW-TO-CREATE-A-NEW-SPRINT.md`, `create_sprint.sh`, `new-sprint`). Fully superseded — current
  sprint tracking is the Projects-v2 field with its own mature tooling (`sprint-truth.py`, the
  restore-snapshot script, the assign-sprint-safely skill), a generation past what those scripts did.
- The 19 scariest-sounding commits (JWT, keychain, migrations, Docker) all hand-cross-referenced:
  every one already on main. Named subsystems (spatial, intent stack, MCP adapters) all have larger
  active successors on main — nothing silently depends on main-old.

**Method note**: subagent-executed (Sonnet, per your ask for a subagent), then I spot-checked the
headline claims myself before committing — cherry counts reproduced exactly, both absent commits
confirmed, all three named paths verified absent from main. Not relayed on faith.

**What this unblocks, decision yours, not made here**: `main-old` can now be left frozen
indefinitely at zero risk, or deleted whenever you like — its own branch protection would need
removing first, and nothing on main would notice either way.

— Exec
