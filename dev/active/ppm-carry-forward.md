# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-15 ~4:01 PM PT
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Sprint-recovery + Production-milestone triage + backup infra** | ✅✅✅ All fully complete (7/12), folded into `roadmap.md` v18.6 and `BRIEFING-CURRENT-STATE.md` (7/14) | None — closed lanes |
| **#1386 criterion 3 (scenarios)** | ✅ Fully closed (C 3/3, re-scoped B 4/4, both PASS 7/12) | None |
| **#1394 / ADR-078 — B4** | ✅ Built + ratified (7/14 ~10:05 PM, 37-test suite run) — ledger primitive done | None |
| **#1394 / ADR-078 — B3** | 🔄 In active design (7/15 ~4pm): Arch ratified Lead's plan (surface-1, OQ-2 deterministic, message-rewrite+raw-preserve) but flagged a capability-gap finding; Lead's build-lens investigation corrected it — `_handle_update_issue` exists, elif-only dispatched (reachability fragility, not missing capability) — filed **#1411**. Arch's OQ-3 (emit resolved intent directly vs. rewrite-and-hope) still open | Watch only — Arch/Lead's to rule + build TDD |
| **#1411** (new, filed 7/15 by Lead) | Zero project-board membership (no milestone/sprint/status). Non-blocking/complementary per Lead's own note | **Flagged for PM** — natural sprint destination unclear (PROD-TECHDEBT vs. unsprinted-in-MVP pending B3 resolution); didn't assign unilaterally, fresh triage not wipe-recovery |
| **#1386 overall gate** | As of 7/14 evening: remaining open besides #1394 — #1278 (Fly cutover), #1386 itself, #1393 (scaffolding-leak), #1395 (corpus-rev), **#1400 + #1401 (hosted-audit: connector prefs + tester uploads both lost on every Fly deploy)** | Watch only. #1400/#1401 still just "worth a glance," not yet investigated |
| **Workstream #051** | Submitted late 7/14, named honestly — Exec folded it into the actual Ship #051 draft same day | Closed, no further action expected |
| **BRIEFING-CURRENT-STATE** | Refreshed 7/14 with verified data; confirmed 7/15 that origin/main still correctly shows it (a SessionStart-hook false-positive claimed otherwise — see process notes) | Keep current going forward |
| **Docs omnibus-gap memo** | Sent 7/14 — precisely scoped, ready-made commit timeline included | Watch for Docs' response; not urgent |
| **#1397** | Filed 7/12 (duty-cycle tooling assumes local-disk-matches-origin) | No PPM action — flagged for a maintainer. Now confirmed to also affect the SessionStart hook's staleness check (7/15), not just duty-cycle-tick/manifest regen — same root cause, no new issue needed |
| **Docs-tree audit** | Plan delivered 7/13, PM-gated | Watch for PM's review/approval |

## PM-attention / escalation items
- **#1411** — new, real, but low-urgency: needs a sprint-triage call (see table above). Not blocking anything; surfacing so it doesn't sit invisible.

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18, see `ppm-standing-items.md`.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found (worth a future check)
- A canonical `ROLE-PORTFOLIO` doc for PPM (other roles, e.g. HOST, have one — `ROLE-PORTFOLIO-HOST.md`). Referenced by the Workstream #051 kickoff format but not found this session; used the general PPM mandate instead.

## Known process notes for future fires
- **`/private/tmp` scratchpad does not survive across cron-triggered fires.** Durable source of truth for sprint-recovery is `docs/internal/planning/sprint-recovery-decisions-log.md`.
- **duty-cycle-tick Step 2 (git checkout + merge) doesn't apply** — Model B session, use a plain `git fetch`. See #1397.
- **Re-verify "applied"/"missing"/count claims against live sources, not a prior log entry or a single-page query.** Instances this week: #234 (logged applied, wasn't), the missing-files claim (wrong path), the Beta-Blockers count (single-page GraphQL undercounted 7→0), and (7/15) the SessionStart hook's "BRIEFING STALE (27 days)" — false positive from reading frozen local disk instead of origin/main.
- **The local-disk-vs-origin drift (#1397) isn't limited to duty-cycle-tick/manifest-regen** — 7/15 confirmed it also feeds the SessionStart hook's staleness check. Any tool/hook reading this worktree's local disk (frozen ~June 18) rather than `git show origin/main:<path>` will misreport. Always verify staleness/count claims against origin/main directly before acting on a hook signal.
- **When mail sits unread across multiple fires, actually open it — don't just note the filename in a scan.** Workstream-051's kickoff was the concrete cost of skipping this once.
- **Step 0 self-heal actually works** — used for real 7/13 (retroactive close) for the first time, not just as documented procedure.
- **PPM inbox's MANIFEST.md is not the unread-tracking source of truth** — it's an empty stub on origin/main even with 19 files sitting in inbox/. Whatever computes the SessionStart hook's per-mailbox unread count isn't reading this file; don't hand-edit it to "fix" a count. The reliable, precedented action is moving read files from `inbox/` to `read/` directly (matches Docs' own mailbox-hygiene pattern, e.g. commit `f27dd2e09`).

## Cron

Current job: `52 6,9,12,15,18,21`, confirmed armed (7/15 ~4pm check, job `192e3d47` unchanged). Survived a >1-day idle gap this week without dying (idle ≠ killed; only a hard reboot/session-end actually kills it). Leaving armed — this is a day-close ritual, not a cron-teardown.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
