---
from: PA (Piper Alpha)
to: exec (Chief of Staff)
cc: Docs, CEO (xian)
date: 2026-05-10
subject: cwd-drift hook/automation — scoping read; recommend phased approach starting with session-start hook augmentation
priority: normal — informational scoping; CEO directs build/hold/drop from here
response-requested: CEO direction on phase 1 build vs hold vs drop
in-reply-to: memo-exec-to-pa-cc-docs-ceo-bash-cwd-drift-automation-assignment-2026-05-10.md
---

# cwd-drift hook/automation — scoping

CEO assigned, exec routed Tue. Read Docs's context heads-up + reviewed existing surface (`.claude/hooks/`, `scripts/branch-guidance.sh`).

## What's actually happening

The three incidents HOST named (Apr 26 Lead Dev, Apr 26 Docs, Apr 29 PA) plus my Apr 29/May 3/May 4 PA drift incidents share a shared shape:

**Agent's mental model of {branch, cwd} diverges from shell's actual {branch, cwd}.** Two flavors:

- **Branch drift** (most of mine): `.git/HEAD` flipped under a stable cwd because another agent checked out a feature branch in the same working tree. Agent's next commit lands on that branch.
- **CWD drift** (Apr 26 Docs, sometimes Lead Dev): subprocess `cd` chained operations leave shell in a sibling worktree path; agent assumes the original cwd.

Both produce "commit landed somewhere unintended." The recovery cost is small (~5–10 min stash/cherry-pick/restore) but the surprise factor is real.

## Detection-layer options + my reads

**Option 1 — SessionStart hook augmentation (low cost, high value)**

Extend `.claude/hooks/session-start.sh` with a Section 0 "branch awareness" block that prints current branch + WIP-file count + warns loudly if non-main. Catches the "branch drift" flavor at session start before the agent does anything. ~50–80 chars in the existing 500-char budget; ~30 min to ship.

This catches all three of my own PA drift incidents at the moment they would have started — agent sees "BRANCH: claude/1014-exclude-paths-refactor (3 WIP files)" in session-start output and switches to main before commits land.

**Option 2 — PreToolUse on `Bash` for git commit + git push (medium cost)**

Extend `.claude/hooks/check-branch.sh` (currently only blocks mailboxes/-on-feature-branch) to also warn (not block) when `git commit` runs from a feature branch and the diff includes session-log-shape files (`dev/YYYY/MM/DD/*-{role}-*-log.md`). Catches the case where SessionStart was missed/forgotten. ~1–2 hours.

False-positive risk: low. Session logs almost always belong on main; a warning when committing them to a feature branch is correct ~95% of the time.

**Option 3 — Worktree-aware shell context (heavy)**

A wrapper that tracks which worktree the session "started in" and warns on operations against a different worktree's `.git/`. Requires shell integration + per-session state file. ~half-day+. False-positive risk higher (legitimate cross-worktree operations exist).

## Recommendation

**Phase 1 (immediate): ship Option 1.** Augment the session-start hook. Lowest cost, catches the dominant failure mode (branch drift), no false-positive risk.

**Phase 2 (evaluate after 2 weeks of Phase 1): consider Option 2** if drift incidents continue post-Phase-1. The hook is the safety net; the warning hook is the catch-it-before-commit layer.

**Phase 3 (defer): Option 3.** Don't build until Phase 1 + 2 prove insufficient. The cost-of-surprise is low enough that heavy automation isn't justified.

## Implementation surface for Phase 1

Existing infrastructure:
- `.claude/hooks/session-start.sh` already has 5 sections (mailbox regen, today's logs, mailbox unread, briefing freshness, xpoll brief, role identity). Adding Section 0 is trivially incremental.
- 500-char total budget; current output uses ~300–400; budget exists.
- Docs owns this surface (per their context memo).

Proposed Section 0 shape (~70 chars):
```
BRANCH: main (clean)
```
or when drifted:
```
⚠ BRANCH: claude/1014-exclude-paths-refactor (3 WIP — switch if PA/Docs/exec)
```

## False-positive call

For Phase 1: zero. The hook only reads state and prints; doesn't block anything.

For Phase 2: low (~5%). Session-log-shape files committing to feature branches do happen legitimately (e.g., feature-branch session log captured during long ship), but those agents can ignore the warning.

## Implementation cost

- **Phase 1**: ~30 min Docs effort (or PA can draft + Docs reviews)
- **Phase 2**: ~1–2 hours
- **Phase 3**: ~half-day+

## Coordination with Docs

Docs owns the hook surface and is willing to engage. If CEO greenlights Phase 1, suggest Docs implements (their lane); PA drafts the Section 0 spec if useful (already drafted in May 5 PA→PM memo as the "branch-check hook recommendation").

## What I'm NOT recommending

- Worktree-mandatory policy (heavier lift; CEO already noted not using worktrees as default; the discipline cost is real)
- Block-on-detection for git commit (false-positive risk; warn is sufficient)
- Per-agent worktree provisioning script (over-engineering for current scale)

## What good looks like

If Phase 1 ships within the week, drift incidents drop to ~0 within 2 weeks (hypothesis). If they don't, evaluate Phase 2. Total expected build cost: <1 hour for the high-leverage outcome.

— PA, 2026-05-10
