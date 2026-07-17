# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-16 ~5:20 PM PT (post Gap-C recovery)
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **Sprint-recovery + Production-milestone triage + backup infra** | ✅ Fully complete (7/12) | None — closed lane |
| **#1394 / ADR-078** | ✅ **Architecture COMPLETE** (B4 7/14 + B3 7/16, both Arch-ratified) | Watch only — one non-blocking D5 live-probe left, rides the next canonical-retest cycle |
| **#1411 / #1412** (update_issue / create_issue reachability) | ✅ Both built + ratified 7/15-16 | None |
| **Beta Blockers sprint** | 🔺 Grew **7→24 open** (7/16) via the new Finish-the-Unfinished census (#1424) — real, not scope creep. Full list in the 7/16 briefing entry | Watch — this is now the dominant open-work surface, worth checking progress each fire |
| **Finish-the-Unfinished epic (#1424)** | PM-ratified in-conversation with Lead (7/16). Phase 0 census done, Phase 1 (guards) + Phase 2 (HIGH fixes) underway — several already closed same-day | Watch only — Lead/Arch driving; plan at `docs/internal/operations/finish-the-unfinished-sprint-2026-07-16.md` |
| **Production 1.0 GATE** (new, 7/16) | Defined: 4 core connectors (GitHub/GCal/Slack/Notion) must complete during beta to close Production milestone #9. RECONNECT R2 epic #1440 (+#1441 GCal, #1442 Notion) seeded | Watch — this is a new PPM-relevant thread, track connector-completion progress |
| **roadmap.md / BRIEFING-CURRENT-STATE.md** | Both folded forward to reflect the above (v18.7 / 7/16 refresh) same-session as this catch-up | Keep current — don't let another gap re-stale them |
| **#1397** (local-disk-vs-origin drift) | Filed 7/12, confirmed on 3 surfaces now (duty-cycle-tick, manifest-regen, SessionStart hook) | No PPM action — flagged for a maintainer |
| **Docs-tree audit** | Plan delivered 7/13, PM-gated | Watch for PM's review/approval |
| **Docs omnibus-gap memo (Jul 6 backfill)** | Docs completed the backfill (confirmed via commit `3819eba89`) | Closed |

## PM-attention / escalation items
- None requiring PM action right now beyond what PM already knows from this conversation.

## Situational awareness (not PPM's lane, just watching)
- **HOST 3-day silence** — Exec already escalated to PM during the gap (commit `007831804`). Not re-investigating; already has an owner.
- **CIO worktree-identity discrepancy** — CIO flagged to Exec during the gap (commit `c4361f56c`). Not re-investigating; already has an owner.
- **CIO duty-cycle stalls** (recurring across 7/15-16) — same pattern as before, still Exec's lane.

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18, see `ppm-standing-items.md`.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found (worth a future check)
- A canonical `ROLE-PORTFOLIO-PPM` doc. Still not found; still not urgent.

## Known process notes for future fires
- **`/private/tmp` scratchpad does not survive across cron-triggered fires.** Durable source of truth for sprint-recovery is `docs/internal/planning/sprint-recovery-decisions-log.md`.
- **duty-cycle-tick Step 2 (git checkout + merge) doesn't apply** — Model B session, use a plain `git fetch`. See #1397.
- **Re-verify "applied"/"missing"/count claims against live sources, not commit messages or a prior log entry.** Latest instance (7/16): the Beta Blockers count wasn't "some new issues got added" — it was a full 7→24 jump, only visible via a live paginated GraphQL pull. Commit-message tallies undercounted badly.
- **CronList can come back completely empty (Gap-C), not just report a stale/idle job.** 7/16: a ~22hr gap with zero fires meant the session-scoped cron had actually died, not just gone quiet. Always run `CronList` explicitly after any gap longer than a few hours — don't assume "armed at last check" still holds.
- **When PPM goes dark, PM routes product/sprint decisions directly to another role (usually Lead) rather than wait.** This is the correct fallback, not a violation — but it means planning docs (`roadmap.md`, `BRIEFING-CURRENT-STATE.md`) drift from real decisions during the gap. First move on any resume-from-gap fire: check whether new product/sprint decisions happened without PPM in the loop, and fold them forward same-session.
- **ADR-077 (Routing Integrity Contract) vs ADR-078 (Session Activity Ledger + Pre-Classifier Reference Resolution) are different ADRs** — both touched by the #1394/#1411/#1412 thread, easy to conflate from commit-message shorthand.
- **"cc-pm" in mailbox filenames means `xian (ceo)`, not `ppm`.** Different slugs.
- **Step 0 self-heal works for full-day AND multi-fire gaps** — used successfully for a stale-but-not-dead gap (7/13) and now a fully-dead-cron gap (7/15→16). The reconstruction quality depends on having the actual session log content to summarize, not just commits, when available.

## Cron

Current job: `61944f35`, `52 6,9,12,15,18,21`, re-armed 2026-07-16 ~5:10 PM PT after confirming the prior job (`192e3d47`) had died during the gap. Watch for another Gap-C on the next long silence — don't assume "was armed last time I checked" still holds after any multi-hour gap.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
