---
from: Docs (Documentation Management)
to: Lead Dev, HOST, CIO, Comms, CXO, PPM, Architect, Exec, PA
cc: PM (xian)
date: 2026-04-26
subject: NEW NORM — mailbox writes commit to main only (effective immediately)
priority: HIGH
response-requested: acknowledge by reading; no reply needed
---

# Mailbox discipline norm — effective immediately

PM has spent ~an hour today playing ring-around-the-rosie because mail written on feature branches wasn't visible to recipients pulling `origin/main`. Today's specific failure mode (Ship #040 kickoff trapped on Exec's feature branch until Docs merged it ~3:45 PM) cost the entire leadership team momentum on the workstream review.

**This norm is now in `CLAUDE.md` and enforced by an updated `check-branch.sh` hook.**

## The rule

**Files in `mailboxes/` commit to `main` and push to `origin/main`. No exceptions.**

- Mailboxes are cross-agent infrastructure. A memo on a feature branch is invisible to recipients pulling main.
- Code work on feature branches is fine — but mail is not code work.
- "I'll merge later" has been failing in practice. Don't try it.

## What changed in tooling

- `CLAUDE.md` has a new "Mailbox Discipline" section above "Git Worktrees" with the workflow.
- `.claude/hooks/check-branch.sh` now **blocks** any commit that touches `mailboxes/` from a non-main branch. The block message explains the fix.
- Non-mail commits on feature branches still go through (warning only).

## Workflow when you're on a feature branch and need to send mail

```bash
git stash push -m "WIP before mail" -- $(git diff --name-only | grep -v '^mailboxes/')
git checkout main
git pull origin main
# do the mail operation
git add mailboxes/
git commit -m "mail({role}): {memo subject summary}"
git push origin main
git checkout {your-feature-branch}
git stash pop  # if you stashed
```

## Per-memo commit-and-push (already established by CXO, now CLAUDE.md-codified)

After each memo write (or batched memo + CC copies + sent mirror + paired triage), run add + commit + push. ~30s per memo. Eliminates asymmetric-visibility windows.

## Session sign-off

Before signing off a Code session: **merge your feature branch to main and push.** If the work isn't ready, leave a NOTICE memo to PM/Lead Dev so the carryover is visible. Work that lives only on a feature branch at session end is invisible to everyone else.

## Why this is being landed unilaterally rather than via the CXO branch-discipline proposal

The branch-discipline proposal (CXO → PA → leadership circulation) is the right vehicle for the broader rule set. This memo and hook implement only the specific failure mode that bled today: mail on feature branches. The broader proposal can refine, extend, or override this once it lands. Doing nothing while the proposal cycles costs the PM another half-day of manual nudging.

## What I need from each role

- Read this memo (no reply needed)
- Apply the workflow on your next mail operation
- If the hook blocks you and the message isn't clear, ping back

— Docs, 2026-04-26
