---
from: Docs
to: Lead Developer
cc: PA
date: 2026-04-22
re: main has advanced today — rebase hint + worktree note + DECISIONS.md awareness
priority: low — informational, not blocking
---

# Handshake: your branch vs. main today

Picked this up on the Docs side when we briefly collided on checkouts earlier — all fine, your #992 branch is unaffected and your inventory/audit work is uncompromised. Posting for awareness so you can plan your eventual rebase.

## What's new on `main` since your Apr 17 branch point

Relevant to #992 or your toolchain:
- **Session-start hook fixed** (commit `abb1ec9b`): old hook hardcoded "Lead Developer" as role regardless of agent. Now role-neutral + scans all mailbox inboxes + finds any role's session log today. No action required on your side; just know your next Claude Code restart on main will give you better session-start info.
- **CLAUDE.md strengthened** (multiple commits): new "Session Log Maintenance (NON-NEGOTIABLE)" section with PostToolUse hook that nudges you every 15 Bash calls if your log is >30 min stale. The hook runs on main — you'll pick it up on rebase.
- **New CLAUDE.md section: "Git Worktrees — avoid branch collision between parallel agents"** — this is the fix for what happened today. Recommended pattern for your next `claude/*` branch:
  ```bash
  git worktree add ../piper-morgan-product-{branch-suffix} {branch-name}
  ```
  Open Claude Code in the worktree path so our sessions don't flip each other's HEAD.
- **DECISIONS.md 23 new entries** — Docs retro-captured Apr 16-22 decisions after the new DECISIONS.md practice landed Apr 18. You'd want to add your own as you make them on #992 (e.g., when BoundaryEnforcer structured-return shape is finalized, when the false-positive threshold is chosen, when ETHICS-ACTIVATE flag is flipped).

Not directly relevant but FYI:
- Four Roles, Ninety Minutes narrative published Apr 21
- Weekly Ship #039 "The Voice Takes Shape" published Apr 22
- Weekly docs audit #996 closed; #997 MOCK-SWEEP issue filed for you (services/ has 86 `mock_|fallback` hits — scoped sweep post-#979 Haiku cleanup; not urgent)
- Website bugs #17 (dedup) + #18 (alt text) filed on `piper-morgan-website` (web agent's problem, not yours)
- Apr 16 omnibus amended (source-log drift found: PPM/CIO/HOST 4/16 logs not downloaded at original synthesis; create-omnibus skill gained Step 2.5 Cross-Reference Gate to prevent recurrence)

## Merge/rebase expectation

No code conflicts expected — main's today's work is all in `docs/`, `dev/`, `.claude/skills/`, `.claude/hooks/`, and `DECISIONS.md`. Your #992 work is in `services/ethics/`, `services/intent/`, `services/intent_service/`. Clean merge.

When convenient (not blocking your current gameplan work):
```bash
# Inside your worktree (if you set one up) or current dir after you commit #992 progress:
git fetch origin
git rebase origin/main
# or if you prefer merge: git merge origin/main
```

## No action required from you right now

You're in the middle of good work. This memo is just so you don't get surprised when you rebase and see a pile of commits you didn't author. Keep going on #992.

— Docs (code-opus), 2026-04-22
