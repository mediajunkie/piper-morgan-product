# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-14 ~8:35 PM PT
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Sprint-recovery + Production-milestone triage + backup infra** | ✅✅✅ All fully complete (as of 7/12). Folded into `roadmap.md` v18.6 and `docs/briefing/BRIEFING-CURRENT-STATE.md` (7/14 refresh). | None — closed lanes |
| **#1386 criterion 3 (scenarios)** | ✅ Fully closed (C 3/3, re-scoped B 4/4, both PASS 7/12) | None |
| **#1386 overall gate** | Live count as of 7/14 (verified full-board pull, corrected the briefing's stale "2 open"): **7 open** — #1278 (Fly final cutover), #1386 itself, #1393 (floor scaffolding-leak, found via #1386 testing), #1394 (continuity gap, ADR-078 PROPOSED), #1395 (corpus-rev, needs Arch ratification), **#1400 + #1401 (hosted-audit: connector prefs + tester uploads both lost on every Fly deploy — significant, newly surfaced)** | Watch only — all Arch/Lead/PM's to close. Worth a glance next fire on #1400/#1401 specifically given how close to invites this is |
| **#1394 / ADR-078** | Lead's ledger-feasibility read landed 7/14 (thorough, code-grounded) — recommends a dedicated `session_activity` table over reusing the protected #1312 tables; Arch to finalize ADR-078 ACCEPTED | Watch only |
| **Workstream #051** | Submitted late 7/14 (missed the 7/13 EOD deadline — a real miss, named honestly in the submission) — sourced from verified commit history given the 7/6-7/8 session-log gap | None further unless Exec/PM follow up |
| **BRIEFING-CURRENT-STATE** | Refreshed 7/14 (was drifting: frontmatter said 7/10, prose said 7/13, Beta-Blockers count was stale at "2 open" vs actual 7) | None — keep this current going forward rather than letting it drift again |
| **#1397** | Filed 7/12 (duty-cycle tooling assumes local-disk-matches-origin, false under Option B) | No PPM action — flagged for a maintainer |
| **Docs-tree audit** | Plan delivered 7/13, PM-gated for execution; small cc-delivery gap flagged to Docs | Watch for PM's review/approval |

## PM-attention / escalation items

- None outstanding.

## Parked (no current trigger)

- Pre-7/5-crisis entity-model lane — unverified since 6/18, see `ppm-standing-items.md`.
- Roadmap v18.1/v19 fold line-item — superseded by v18.6 (7/12); stale reference, not real work.
- Ship #048 kickoff memo — status unknown, unverified.

## Known process notes for future fires

- **`/private/tmp` scratchpad does not survive across cron-triggered fires.** Durable source of truth for sprint-recovery is `docs/internal/planning/sprint-recovery-decisions-log.md`, not scratch JSON.
- **duty-cycle-tick Step 2 (git checkout + merge) doesn't apply** — this session runs Model B (temp-index-direct-to-main). Use a plain `git fetch`. See #1397.
- **Re-verify "applied" claims against the live board, not a prior log entry.** #234 (7/12) was the proof case: logged as applied, wasn't.
- **A "days since 2026-06-18" staleness hook message doesn't necessarily mean the file's actually that stale** — BRIEFING-CURRENT-STATE's own frontmatter and prose dates had already drifted from each other and from the hook's number. Read the file before assuming the hook's day-count is the ground truth.
- **When "unread" mail sits across multiple fires, actually open it, don't just note its filename in a scan.** The workstream-051 kickoff sat visible-but-unread for days this week before its own deadline passed — the miss wasn't a delivery failure, it was scanning a filename list without reading content.
- **A single non-paginated GraphQL board query undercounts.** Caught this fire: an initial `items(first: 100)` Beta-Blockers check said "0 open," full pagination said 7. Always paginate for anything board-wide.

## Cron

Current job: `52 6,9,12,15,18,21`, confirmed armed. Survived a >1-day stale gap this week (7/13 afternoon → 7/14 evening) without dying — the underlying object persists through an idle/unattended session, distinct from a hard reboot which does kill it. `SessionStart:resume` is the wake signal in the survives-but-idle case.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
