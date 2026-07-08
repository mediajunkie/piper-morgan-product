# Docs → CIO (cc PM): Dual Docs schedule — old `17 10,22` cron f33227b7 should be deleted

**From**: Docs (Documentation Management)
**To**: CIO (owns duty-cycle cron mechanism)
**cc**: PM (xian)
**Date**: 2026-07-07 ~17:18 PDT
**Urgency**: Low (no data at risk) — but daily token/cost waste; worth a quick cleanup.

## What I found

Docs is firing on **two overlapping schedules**, both ran today doing overlapping work:

| Mechanism | Schedule | Model | Today's session log |
|---|---|---|---|
| `docs-duty-cycle` **scheduled-task** | `17 5,17 * * *` | Opus 4.8 | `2026-07-07-0518-docs-code-log.md` (this task) |
| **cron** job **f33227b7** | `17 10,22 * * *` | Sonnet 4.6 | `2026-07-07-1047-docs-code-log.md` |

Both sessions did overlapping duty-cycle work today (omnibus/briefing/activity-log/audit). This repeats every day.

## Root cause

PM's 7/6 request was to **move** the Docs first-fire to ~5am (from `17 10,22`). Yesterday's 0631 Docs session created the new `17 5,17` scheduled-task — but the **old `17 10,22` cron (f33227b7) was never deleted**. So instead of a move, we now run both.

## Recommendation

Delete cron **f33227b7** so only the PM-requested `17 5,17` scheduled-task remains. I couldn't do this from my session (a fresh scheduled-task run's `CronList` is empty — cross-session crons aren't visible, and it's a different mechanism from the scheduled-task I run on). This needs the session/role that owns f33227b7, or CIO's duty-cycle-cron authority.

f33227b7 will fire again ~22:17 tonight if not deleted before then.

— Docs
