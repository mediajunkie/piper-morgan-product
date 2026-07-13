# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-13 ~7:20 AM PT
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Sprint-recovery effort (7/5 field wipe)** | ✅✅✅ **FULLY COMPLETE** as of 2026-07-12 — HIGH/MEDIUM/LOW/S2-correction/Group 3 all applied+verified | None. Closed. See decisions-log final entry if this needs revisiting later |
| **#1386 criterion 3 (scenarios)** | ✅ FULLY CLOSED — C 3/3, re-scoped B 4/4, both PASS live beta 2026-07-12 evening | None. #1394 stays open/tracked as intended, `priority: high` already set |
| **#1386 overall gate** | Criteria 1/2/4/5/6 still open — Arch (corpus-rev #1395, ADR-070-A check) and PM (Scenario A browser run, criterion-4 window, criterion-6 sign-off) own what's left | Watch only — nothing in PPM's lane remains on this issue |
| **#1278 Fly cutover** | PM appears to be executing DNS cutover (per Lead's 7/12 memo) | Watch for completion + criterion-2 Run 15 results |
| **#1397 (discovered 7/12)** | Filed: `regenerate-mailbox-manifests.py` + duty-cycle-tick Step 2 assume local-disk-matches-origin, false under Option-B ephemeral worktrees | No PPM action needed — flagged for a maintainer |
| **#1394** | Arch: ARCHITECTURAL GAP determination (one ledger primitive, two seams); ADR-078 PROPOSED, gated on Lead's feasibility read. CXO's TESTER-QUICKSTART disclosure draft delivered — PPM acked on-issue 7/13 | Watch only — Lead integrates the disclosure text and gives the feasibility read |
| **Production-milestone triage** | ✅✅ **FULLY COMPLETE, 99/99** — 20 new issues into PROD-* sprints + #1358/#1374 into Ongoing/FLYWHEEL (PM-agreed); roadmap.md folded to v18.6 | None |
| **Docs-tree audit request** | Memo sent to Docs (cc PM) per PM directive, with 3 concrete starting data points | Watch for Docs' audit + cleanup plan — not PPM's to execute |
| **Sprint-field backup/restore infra** | ✅ Built + tested: `scripts/restore-sprint-field-from-snapshot.py`, wired into CLAUDE.md's wipe warning | None — this is now standing infrastructure. Keep running `snapshot-project-board.sh` after batches so the backup stays fresh |

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
