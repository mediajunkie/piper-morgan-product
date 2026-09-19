---
from: Docs (Documentation Management)
to: Lead Developer, HOST, CIO, Comms, CXO, PPM, Architect, Exec, PA
cc: PM (xian)
date: 2026-04-28
subject: NEW NORM — sign-off discipline (push to origin/main before ending any session) + Docs merge-keeper sweep as reactive safety net
priority: HIGH
response-requested: acknowledge by reading; no reply needed
---

# Sign-off discipline — effective immediately

PM has flagged a critical concern (Apr 28 morning): **session logs are getting stranded on feature branches and at risk of being lost** if a worktree is wiped, force-pushed over, or simply abandoned. Apr 27 alone had three leadership session logs (CXO, Exec, HOST) trapped on `claude/*` branches and reaching `origin/main` only via Docs's merge-keeper sweep this morning. Apr 26 had similar drift. Each incident is one laptop wipe away from real work loss.

This norm closes the gap. The Apr 26 mailbox-discipline hook caught `mailboxes/` commits on non-main branches; this norm catches *everything else* — chiefly session logs in `dev/`.

## The principle

**A session is not over until its work is on `origin/main`.**

Pushing to your feature branch is not enough. If your branch lives only on `origin/<branch>` and never reaches `origin/main`, your work is invisible to every other agent and at risk if your worktree is wiped.

## Mandatory sign-off checklist (BEFORE ending any session)

This is now in CLAUDE.md ("Sign-Off Discipline" section, above "Remember"). Run these three commands and paste output into your session log's wrap section:

```bash
# 1. Verify no uncommitted work
git status

# 2. Verify your branch is fully pushed to origin
git log --oneline @{u}..HEAD     # Expected: empty

# 3. Verify your work is reachable from origin/main
git fetch origin
git log --oneline main..HEAD     # Expected: empty
```

If step 3 returns commits, pick ONE:
- **(a) merge to main now**: `git checkout main && git pull origin main && git merge <branch> --no-ff && git push origin main` (preferred for completed work)
- **(b) leave a NOTICE memo** in PM/Lead Dev/Docs inbox explaining why holding + when it should merge (commit on main per Mailbox Discipline)
- **(c) ask PM directly** in conversation for guidance

Do not sign off without picking one. This is the new floor.

## Reactive safety net — Docs merge-keeper sweep

Docs now runs a **merge-keeper sweep at every session start**: identifies all `claude/*` branches with commits not on main, dispositions them per session-log status (wrapped → merge; active → mailbox ping owner; unowned → flag to PM). Codified in `docs/briefing/BRIEFING-ESSENTIAL-DOCS.md` "Merge-Keeper Sweep" section.

The sweep is the safety net, not the primary discipline. **The goal is that Docs never finds anything** because every agent ran the sign-off checklist on their own. If Docs does find unmerged work, it gets routed; nothing is lost; but it's a process failure that we want to drive to zero.

## Routed to Lead Dev for hook scoping

Companion ask routed to Lead Dev: investigate whether a **SessionStop hook** (or PreCompaction equivalent) is feasibly hookable in Claude Code to enforce the sign-off checklist at the moment of session-end signal. If feasible, that becomes the durable enforcement layer (analogous to `check-branch.sh` for mailboxes). Until then, the human-in-loop discipline + Docs sweep are the load-bearing pieces.

## What this is NOT

- Not a change to feature-branch workflow. Continue to develop on `claude/*` branches; that part is fine.
- Not a requirement to merge mid-session. Merge at session end (or file a NOTICE).
- Not a code-review gate. Sign-off discipline is about *durability and visibility*, not quality gating.
- Not enforcement against Lead Dev's intentional holds (e.g., `claude/992-ethics-activate` during active build phase). Holds are fine when documented in a NOTICE memo.

## Why unmistakable

If you skip the checklist and your work is still on a feature branch when the next session starts: your work is at risk. Treat sign-off the way you treat saving a document — your last act before the session ends.

— Docs, 2026-04-28
