# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-15 ~7:01 PM PT

**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Sprint-recovery + Production-milestone triage + backup infra** | ✅✅✅ All fully complete (7/12) | None — closed lanes |
| **#1386 criterion 3 (scenarios)** | ✅ Fully closed (7/12) | None |
| **#1394 / ADR-078 — B4** | ✅ Built + ratified (7/14, 37-test suite run) | None |
| **#1394 / ADR-078 — B3** | 🔄 Design essentially settled (7/15 ~7pm): surface-1, OQ-2 deterministic, message-rewrite+raw-preserve, and now **OQ-3 ruled emit-directly** (B3 emits `action=update_issue` straight, never back through the classifier — closes the create_issue-duplicate hazard by construction). D5 corpus rows pending #1411. Next: Lead builds B3 TDD | Watch only — Arch/Lead's to build and close |
| **#1411** (ADR-077 conformance fix, not ADR-078) | Built + merged same-day (`5475410da`), Lead pinged Arch, Arch's reply already confirms direction | **Downgraded from "needs PM sprint call"** (4:01pm note) — this is self-resolving via normal Arch/Lead ratify-and-close, likely closes without ever entering sprint planning. Watch for close; re-flag only if it stalls |
| **#1386 overall gate** | Remaining open besides #1394 — #1278 (Fly cutover), #1386 itself, #1393 (scaffolding-leak), #1395 (corpus-rev), **#1400 + #1401 (hosted-audit: connector prefs + tester uploads lost on every Fly deploy)** | Watch only. #1400/#1401 still just "worth a glance," not yet investigated |
| **Workstream #051** | Closed 7/14 | None |
| **BRIEFING-CURRENT-STATE** | Refreshed 7/14; confirmed 7/15 still correct on origin/main (a SessionStart-hook false-positive claimed otherwise — local-disk drift, see process notes) | Keep current going forward |
| **Docs omnibus-gap memo** | Sent 7/14 | Watch for Docs' response; not urgent |
| **#1397** | Filed 7/12 | No PPM action. Confirmed 7/15 it also explains the SessionStart hook false-positive — same root cause |
| **Docs-tree audit** | Plan delivered 7/13, PM-gated | Watch for PM's review/approval |

## PM-attention / escalation items
- None requiring PM action right now. (#1411's sprint-placement question from 4:01pm is downgraded — see table.)

## Situational awareness (not PPM's lane, just watching)
- **CIO duty-cycle stall, recurring**: 4th "⚠️ duty-cycle stall — cio" watchdog alert today as of 7:01pm fire, no CIO session log exists for today. Not escalating myself — Exec owns operational-health monitoring and the cohort has watchdog+freeze-registry infrastructure for exactly this. Flagging here so it's visible if it's still unresolved next check.

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18, see `ppm-standing-items.md`.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found (worth a future check)
- A canonical `ROLE-PORTFOLIO` doc for PPM (other roles, e.g. HOST, have one). Not found this session; used the general PPM mandate instead.

## Known process notes for future fires
- **`/private/tmp` scratchpad does not survive across cron-triggered fires.** Durable source of truth for sprint-recovery is `docs/internal/planning/sprint-recovery-decisions-log.md`.
- **duty-cycle-tick Step 2 (git checkout + merge) doesn't apply** — Model B session, use a plain `git fetch`. See #1397.
- **Re-verify "applied"/"missing"/count claims against live sources, not a prior log entry or a single-page query.** Real instances: #234, the missing-files claim, the Beta-Blockers count, and the SessionStart hook's "BRIEFING STALE" false positive (7/15) — all local-disk-vs-origin drift, same root cause (#1397), now confirmed across three different surfaces (duty-cycle-tick, manifest-regen, SessionStart hook).
- **PPM inbox's MANIFEST.md is not the unread-tracking source of truth** — empty stub on origin/main even with a full inbox. Don't hand-edit it. The reliable action is moving read files from `inbox/` to `read/` directly.
- **ADR-077 (Routing Integrity Contract) vs ADR-078 (Session Activity Ledger + Pre-Classifier Reference Resolution) are different ADRs** — both touched by the #1394/#1411 thread today, easy to conflate from commit-message shorthand alone. #1394/B3/B4 = ADR-078. #1411 (elif-only dispatch reachability) = ADR-077 conformance.
- **"cc-pm" in mailbox filenames means `xian (ceo)`, not `ppm`.** Different slugs, easy to misread — checked a file that turned out not to be addressed to my inbox at all because of this.
- **When mail sits unread across multiple fires, actually open it — don't just note the filename in a scan.** Workstream-051's kickoff was the concrete cost of skipping this once.
- **Step 0 self-heal actually works** — used for real 7/13 (retroactive close), not just as documented procedure.

## Cron

Current job: `52 6,9,12,15,18,21`, confirmed armed (7/15 ~7pm check, job `192e3d47` unchanged). Next scheduled fire 21:52 — not the last fire of the day, no STOP this cycle. Leaving armed.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
