# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-12 ~4:15 PM PT (Fire 2, duty-cycle-tick)
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Sprint-recovery: S2→A12 bulk-move (19 issues)** | ✅ Executed + verified — PM go-ahead received | Done. S2 now empty on the board |
| **Sprint-recovery: Group 3 (19 true-zero-evidence issues)** | ✅ Built and published; PM reviewing next | Await PM's read — this is the last open piece of the whole 7/5 recovery effort |
| **#1386/#1394 Scenario B re-scope** | ✅ CXO+PPM joint sign-off FINAL as of this fire — folded into #1386 body, #1394 labeled `priority: high` | Watch for Lead's re-execution of rescoped B3/B4; CXO owns the TESTER-QUICKSTART line once Lead's #1394 scope-read lands |
| **#1278 Fly cutover** | PM appears to be executing DNS cutover (per Lead's 7/12 memo) | Watch for completion + criterion-2 Run 15 results |
| **#1397 (discovered this fire)** | Filed: `regenerate-mailbox-manifests.py` + duty-cycle-tick Step 2 assume local-disk-matches-origin, false under Option-B ephemeral worktrees | No PPM action needed — flagged for a maintainer; affects the whole cohort, not just PPM |

## PM-attention / escalation items (residual home since 6/17 fold)

- None outstanding as of this fire.

## Parked (no current trigger)

- Pre-7/5-crisis entity-model lane (#1237/#1238/#1239/#683/#967/#1185/#5/PDR-005/ADR-071-anchoring) — status unverified since 6/18, preserved in `ppm-standing-items.md` under a "needs revalidation" heading. Don't assume current without a fresh check.
- Roadmap v18.1/v19 fold — owed since 6/15, never actioned; likely superseded by the beta-blockers/Fly work since.
- Ship #048 kickoff memo — status unknown, not touched since 6/18.

## Known process notes for future fires

- **`/private/tmp` scratchpad does not survive across cron-triggered fires** — each fire may start with an empty scratch dir even mid-conversation. Don't treat prior-fire scratch files as available; the durable source of truth for sprint-recovery specifically is `docs/internal/planning/sprint-recovery-decisions-log.md` on `origin/main`, not scratch JSON.
- **duty-cycle-tick Step 2 (git checkout + merge) does not apply as written** — this session runs Model B (ephemeral worktree, temp-index-direct-to-main), not the Model A dedicated cycle-branch the skill assumes. Substitute a plain `git fetch`. See #1397.
- **Always re-verify "applied" claims against the live board before trusting a prior log entry as fact** — #234 this fire is the concrete proof case: logged as applied, wasn't. The decisions log records intent/history well; it is not itself proof of current board state.

## Cron

Current job: `52 6,9,12,15,18,21`, confirmed still armed via `CronList` at the end of this fire (never deleted — Rule 1 says substantive work >2min should CronDelete first; this fire didn't, noting the miss rather than fixing retroactively). **Known limitation, told to PM**: session-only, no durable persistence — dies on reboot or session end without a human or surviving fire re-arming it.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
