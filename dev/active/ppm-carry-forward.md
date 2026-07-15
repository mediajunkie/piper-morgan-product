# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-14 ~10:25 PM PT (day-close)
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Sprint-recovery + Production-milestone triage + backup infra** | ✅✅✅ All fully complete (7/12), folded into `roadmap.md` v18.6 and `BRIEFING-CURRENT-STATE.md` (7/14) | None — closed lanes |
| **#1386 criterion 3 (scenarios)** | ✅ Fully closed (C 3/3, re-scoped B 4/4, both PASS 7/12) | None |
| **#1394 / ADR-078** | ✅ **ACCEPTED v0.2** (7/14 ~10:05 PM) — Lead's feasibility read corrected D1 to a dedicated `session_activity` ledger; Arch added owner-scoping (D1a) as non-negotiable; Lead cleared to build B4 | Watch only — Arch/Lead/HOST's to build and close |
| **#1386 overall gate** | As of 7/14 evening: #1394 closed out of the open list (ADR accepted, build not yet done — watch whether Lead treats the issue itself as still-open pending B4/B3 build). Remaining open: #1278 (Fly cutover), #1386 itself, #1393 (scaffolding-leak), #1395 (corpus-rev), **#1400 + #1401 (hosted-audit: connector prefs + tester uploads both lost on every Fly deploy)** | Watch only. #1400/#1401 worth a glance next fire given proximity to invites |
| **Workstream #051** | Submitted late 7/14, named honestly — Exec folded it into the actual Ship #051 draft same day, so it landed despite the lateness | Closed, no further action expected |
| **BRIEFING-CURRENT-STATE** | Refreshed 7/14 with verified data (was drifting on dates + had a materially wrong Beta-Blockers count) | Keep current going forward — don't let it drift back into "last touched weeks ago" |
| **Docs omnibus-gap memo** | Sent 7/14 — precisely scoped (only Jul 6 needs a backfill; Jul 7-8 are correctly blank) with a ready-made commit timeline for Docs to use | Watch for Docs' response; not urgent |
| **#1397** | Filed 7/12 (duty-cycle tooling assumes local-disk-matches-origin) | No PPM action — flagged for a maintainer |
| **Docs-tree audit** | Plan delivered 7/13, PM-gated | Watch for PM's review/approval |

## PM-attention / escalation items
- None outstanding.

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18, see `ppm-standing-items.md`.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found (worth a future check)
- A canonical `ROLE-PORTFOLIO` doc for PPM (other roles, e.g. HOST, have one — `ROLE-PORTFOLIO-HOST.md`). Referenced by the Workstream #051 kickoff format but not found this session; used the general PPM mandate instead. Not urgent, but worth confirming whether it exists and I missed it, or genuinely doesn't exist yet.

## Known process notes for future fires
- **`/private/tmp` scratchpad does not survive across cron-triggered fires.** Durable source of truth for sprint-recovery is `docs/internal/planning/sprint-recovery-decisions-log.md`.
- **duty-cycle-tick Step 2 (git checkout + merge) doesn't apply** — Model B session, use a plain `git fetch`. See #1397.
- **Re-verify "applied"/"missing"/count claims against live sources, not a prior log entry or a single-page query.** Three real instances this week: #234 (logged applied, wasn't), the missing-files claim (wrong path, not actually missing), the Beta-Blockers count (single-page GraphQL undercounted 7→0).
- **When mail sits unread across multiple fires, actually open it — don't just note the filename in a scan.** Workstream-051's kickoff was the concrete cost of skipping this once.
- **Step 0 self-heal actually works** — used for real this week (7/13's retroactive close) for the first time, not just as documented procedure. Reconstructing a day-arc from its own commit trail is reliable when the day's commits were properly made even if the log was never formally wrapped.

## Cron

Current job: `52 6,9,12,15,18,21`, confirmed armed at day-close. Survived a >1-day idle gap this week without dying (idle ≠ killed; only a hard reboot/session-end actually kills it). Leaving armed per STOP convention — this is a day-close ritual, not a cron-teardown.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
