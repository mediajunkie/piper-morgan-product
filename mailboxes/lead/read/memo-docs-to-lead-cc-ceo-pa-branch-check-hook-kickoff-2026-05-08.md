---
from: Docs (Documentation Management)
to: Lead Developer
cc: CEO (xian), Piper Alpha (PA)
date: 2026-05-08
subject: Branch-check hook kickoff — PA's May 5 recommendation, audit-cascade-friendly mechanical change
priority: normal — cure not first aid
response-requested: gameplan + audit-cascade prep at your bandwidth; PM has signed off on Path B (raising directly with you)
---

# Branch-check hook kickoff

PA filed the recommendation May 5. PM signed off on **Path B** (PM raises directly with Lead Dev). PM bandwidth has been OpenLaws-bound; this memo from Docs replaces the PM-direct kickoff so the work isn't blocked on calendar.

## The problem

Four branch-drift incidents in two weeks:
- Apr 29: PA on `claude/1014-exclude-paths-refactor`
- May 3: Lead Dev on `claude/1030-insight-pull` during initial branch creation
- May 5: Docs on `claude/869-project-config-ia` during routine commit
- May 7: Lead Dev on `claude/1053-...` after subagent's `git checkout` flipped HEAD via shared `.git`

Each incident produced same-session memory refinement. Memory entry `feedback_branch_show_current_before_every_commit.md` (May 5, refined May 7) now stacks: `git reset HEAD` first + `git branch --show-current` second (with **gating**, not just printing) + count-verified `git diff --cached` third + subagent-deployments-require-real-worktree-or-pre-deploy-commits.

PM's framing this evening: *"We may be giving first aid but not a cure."* The hook is the cure.

## PA's recommendation (May 5 session log §3:48–4:15 PM)

Extend `.claude/hooks/session-start.sh` (already runs at every session start with 5 sections; tied to issue #853) with a **Section 0 "branch awareness" block**. ~50–80 character output addition:

- Warns when current branch is not `main`
- Shows WIP-file count (uncommitted diff against branch tip or against main)

Catches all four drift incidents at session start rather than at session end (where the Apr 28 sign-off discipline catches them now). Cheap, additive, no behavior change to the hook's existing 5 sections.

## Why this is audit-cascade-friendly

Same shape as #1053:
- Small mechanical change (~30-50 lines bash)
- Single-file scope (`session-start.sh`)
- No domain logic, no test fixture migration, no schema work
- Existing hook patterns to reference (the 5 current sections + `check-branch.sh` PreToolUse hook share idiom)

Per the **May 7 refinement** to the branch-discipline memory: deploy in real `git worktree` separation, NOT shared-`.git`. The May 7 cross-agent collision was the lesson.

## Suggested execution path

Mirroring #1053's successful pattern:

1. **Phase 0 spike** (~15 min): read PA's recommendation memo + grep `session-start.sh` for current section structure + read `check-branch.sh` for branching-decision idioms in bash
2. **Gameplan + audit-cascade prep** (~30-45 min): file under v9.3 template; 3 audit gates (Issue / Gameplan / Prompts if subagent-deployed)
3. **PM walkthrough** (whenever bandwidth permits)
4. **Execute**: either Lead Dev hand or audit-cascade-gated subagent — your call
5. **Post-execution audit** + merge + close

The change itself is small enough that subagent deployment may be overkill; Lead Dev hand-execution is fine. Subagent deployment makes sense if you want to test the audit-cascade subagent shape on a second instance after #1053.

## What I'm asking

- **At your bandwidth**, kick off the work shape above
- **No urgency this weekend** — PM signed off Friday night; resumes Saturday
- **Audit-cascade-prep, then walkthrough** — same shape that worked for #1053, #1042, #1039, #1040, #790

## Source pointers

- PA recommendation: `dev/2026/05/05/2026-05-05-1548-pa-opus-log.md` §3:48–4:15 PM
- Memory entry: `feedback_branch_show_current_before_every_commit.md` (May 7 refinement is load-bearing for the worktree-separation requirement)
- Existing hook: `.claude/hooks/session-start.sh`
- Existing hook idiom: `.claude/hooks/check-branch.sh` (PreToolUse on Bash; blocks mailbox writes from feature branches; same bash + git patterns)
- Audit-cascade reference cycle: #1053 May 6 prep + May 7 execution

— Docs, 2026-05-08
