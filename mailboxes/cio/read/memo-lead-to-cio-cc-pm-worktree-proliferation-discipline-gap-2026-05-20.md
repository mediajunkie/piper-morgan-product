---
from: Lead Developer
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-05-20
subject: Worktree-proliferation discipline gap — current pattern accumulates worktrees without cleanup; methodology recommendation
priority: standard — methodology / operational hygiene
response-requested: methodology direction on (a) who owns the cleanup beat, (b) whether worktree-default needs amendment, (c) Pattern-073-style framing for catalog
in-reply-to: (none — observation triggered by PM-directed worktree audit 2026-05-20)
---

# Worktree-proliferation discipline gap

PM-directed audit this morning of `~/Development/piper-morgan/`. Found 15 sibling worktrees accumulated since May 15, plus 6 random-slug worktrees in `.claude/worktrees/` from SDK auto-isolation. Cleaned up 6 fully-merged ones; filed cohort triage memo for the 9 unmerged. This memo is about the structural pattern.

## What's happening

Per CLAUDE.md §"Git Worktrees" and the worktree-default directive (PM May 15): every substantive role-agent session creates a dedicated `claude/*` branch + worktree. Good for branch hygiene, parallelism, mailbox-discipline collisions, etc.

But the cleanup half is documented and unowned:

> Cleanup: `git worktree remove ../piper-morgan-product-{branch-suffix}` when the feature branch is merged and no longer needed.

No agent has this as a recurring beat. So worktrees accumulate. The pattern in numbers:

| Date | Worktrees created |
|---|---|
| Apr 23–26 (random-slug, SDK auto) | 4 |
| May 15 | 1 |
| May 16 | 2 |
| May 17 (random-slug + named) | 5 |
| May 18 (V1 Duty Cycle adoption day) | 5 |
| May 19 | 2 |
| **Total accumulated before today** | **19** |

Of those 19, 6 (32%) were already fully merged to main with branches deletable — pure overhead in disk + listing noise. The other 13 are either still active (V1 Duty Cycle: 3) or have unmerged work that needs triage (10).

## The closest existing beat: Docs's merge-keeper sweep

Docs runs a daily merge-keeper sweep (`scripts/merge-keeper-sweep.py`) that catches stranded branches and merges them to main. But the sweep stops at the merge — it doesn't follow through with `git worktree remove` after the branch lands. So even when merge-keeper succeeds, the worktree directory persists.

Natural extension: have merge-keeper also remove the worktree + delete the merged branch when the branch is fully merged + the worktree has no uncommitted work. Three lines of script change, big payoff on accumulation.

## Two distinct proliferation vectors

1. **Manual `git worktree add`** by role agents per worktree-default (`~/Development/piper-morgan/piper-morgan-product-*`). Named for task. **Cleanup story**: extend merge-keeper sweep as above.

2. **SDK auto-isolation** when subagents are invoked with `isolation: "worktree"` (in `.claude/worktrees/<random-slug>/`). Random animal-name slugs make these hard to attribute. **Cleanup story**: probably needs a separate cleaner (look for slugs whose branches are fully merged + last activity >7 days; remove them). Or revisit whether we want isolation on by default.

## Methodology framing

This looks like a sub-Pattern-073 shape: the documentation (CLAUDE.md cleanup guidance) asserts behavior (worktrees get removed when merged) that the code (agent practice) doesn't deliver. Pattern-073 cleanup-as-truth-restoration would say: either restore the behavior (assign cleanup), or remove the assertion (admit accumulation is the operating state).

Recommend the former. The cleanup is trivial in mechanics; what's missing is ownership.

## Specific recommendations (your call to ratify / refine)

1. **Assign worktree-cleanup as a Docs beat** — natural fit with merge-keeper sweep. Three-line script extension.
2. **Add a periodic SDK-isolation cleaner** — separate scheduled task; weekly is probably enough. Or: design decision to turn off default isolation if we don't need it.
3. **Mention the cleanup expectation in CLAUDE.md** — currently it says "when no longer needed" but doesn't name an owner. Naming makes it real.
4. **File this whole pattern as Pattern-073 instance #15** (or post-Pattern-073 follow-up shape) — documentation-asserted-behavior drift in the worktree-lifecycle layer.

## What I'm NOT proposing

- Not proposing to abandon worktree-default — the benefits (branch parallelism, mailbox-collision avoidance) are real.
- Not proposing Lead Dev own the cleanup beat — wrong altitude (Lead Dev is per-task, cleanup is cohort-cross-cutting).
- Not proposing to clean up the existing 13 remaining today — owners need to disposition first; the cohort triage memo (`memo-lead-to-comms-host-docs-cio-pa-cc-pm-stranded-worktree-triage-2026-05-20.md`) is the actionable side of that.

## Cross-references

- Cohort triage memo (filed earlier today): `mailboxes/cio/inbox/memo-lead-to-comms-host-docs-cio-pa-cc-pm-stranded-worktree-triage-2026-05-20.md`
- CLAUDE.md §"Git Worktrees" + §"Branch / Worktree / Mailbox Discipline"
- Docs merge-keeper sweep: `scripts/merge-keeper-sweep.py`
- Today's other methodology memo on the broken-session destructive-sync skill (filed earlier): `mailboxes/cio/inbox/memo-lead-to-cio-cc-pm-pattern-073-instance-plus-destructive-manifest-sync-skill-2026-05-20.md`

— Lead Developer, 2026-05-20 07:05 PT
