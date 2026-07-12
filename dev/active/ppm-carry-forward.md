# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-12 (post-reboot resume, cron re-armed `52 6,9,12,15,18,21`)
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Sprint-recovery: S2→A12 bulk-move** | Recommended, HELD for PM go-ahead (overwrites 19 existing values) | Awaiting PM's word — see `sprint-recovery-decisions-log.md` for full forensic finding |
| **Sprint-recovery: 19 true-zero-evidence issues (Group 3 proper)** | Not yet built as an artifact | Build whenever PM wants it — last frontier of the 7/5 recovery effort |
| **#1386/#1394 Scenario B re-scope** | PPM recommendation sent to CXO 7/12 (~15:45 PT) for joint sign-off | Awaiting CXO's confirm; then note joint call on #1386 |
| **#1278 Fly cutover gate sequencing** | PPM recommended gate-against-Fly-artifact 7/10; Lead endorsed 7/12; PM appears to be executing DNS cutover now (per Lead's 7/12 memo) | Watch for cutover completion / criterion-2 Run 15 results |

## PM-attention / escalation items (residual home since 6/17 fold)

- None outstanding as of 7/12 — mailbox fully triaged through the #1386/#1394 thread this session.

## Parked (no current trigger)

- Pre-7/5-crisis entity-model lane (#1237/#1238/#1239/#683/#967/#1185/#5/PDR-005/ADR-071-anchoring) — status unverified since 6/18, moved to `ppm-standing-items.md` under a "needs revalidation" heading rather than carried forward as current. Don't assume any of it still reflects reality without a fresh check.
- Roadmap v18.1/v19 fold — owed since 6/15, never actioned; likely superseded by the beta-blockers/Fly work since. Revalidate before resuming.
- Ship #048 kickoff memo — status unknown, not touched since 6/18.

## Cron

Current job: `52 6,9,12,15,18,21` (re-armed 2026-07-12 ~3:20 PM after laptop reboot killed the prior session-scoped job). **Known limitation, told to PM**: `CronCreate` is session-only — no `durable:true` support in this environment — so it will not survive another reboot or session end without a human or a surviving fire re-arming it. The external Routines watchdog (duty-cycle-tick roadmap item 1) is the actual cure; this is a partial mitigation only.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
