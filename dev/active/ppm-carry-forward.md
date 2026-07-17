# PPM Carry-Forward

**Role**: Principal Product Manager (PPM)
**Last rewritten**: 2026-07-16 ~10:22 PM PT (day-close)
**Purpose**: ephemeral session state — active PM threads, PM-attention items, parked work, current cron job-id. Rewrite at end of every substantive fire (duty-cycle-tick v1.13).

---

## Active PM threads

| Item | State | Next action |
|---|---|---|
| **#1394 / ADR-078** | ✅ Architecture COMPLETE (B4 7/14 + B3 7/16, both Arch-ratified) | Watch only — one non-blocking D5 live-probe left, rides the next canonical-retest cycle |
| **#1411 / #1412** (reachability fixes) | ✅ Both built + ratified | None |
| **Beta Blockers sprint** | 24 open (7/16 AM) → **21 open (7/16 close, live count)** — real progress from Finish-the-Unfinished fixes (#1414/#1416/#1417/#1426 among others closed today) | Watch — recount periodically, not every fire; check again if a full day passes without a look |
| **Finish-the-Unfinished epic (#1424)** | Phase 2 (HIGH fixes) actively landing, several sub-items closed 7/16. Epic itself confirmed still OPEN | Watch only — Lead/Arch driving |
| **ADR-079** (Owner-Scoping Integrity Contract) | Authored by Arch 7/16, houses check-unscoped-reads D2-D6 | Watch only — Architect-owned, no PPM sign-off needed |
| **Production 1.0 GATE** | Defined 7/16: 4 core connectors (GitHub/GCal/Slack/Notion) must complete during beta. RECONNECT R2 epic #1440 (+#1441 GCal, #1442 Notion) seeded | Watch — track connector-completion progress |
| **roadmap.md / BRIEFING-CURRENT-STATE.md** | Both current as of 7/16 (v18.7 / same-day refresh) | Keep current |
| **#1397** (local-disk-vs-origin drift) | Filed 7/12, confirmed on 3 surfaces | No PPM action |
| **Docs-tree audit** | Plan delivered 7/13, PM-gated | Watch for PM's review/approval |

## PM-attention / escalation items
- None outstanding.

## Situational awareness (not PPM's lane, just watching)
- Exec/CIO shared-worktree collision (7/16) — Exec confirmed and resolved same day. Closed on that side.
- HOST 3-day silence, CIO worktree-identity discrepancy (both from 7/16 AM) — already escalated/owned by Exec.

## Parked (no current trigger)
- Pre-7/5-crisis entity-model lane — unverified since 6/18, see `ppm-standing-items.md`.
- Ship #048 kickoff memo — status unknown, unverified.

## Wanted but not found (worth a future check)
- A canonical `ROLE-PORTFOLIO-PPM` doc. Still not found; still not urgent.

## Known process notes for future fires
- **`CronList` can come back completely empty (Gap-C), not just stale.** After any gap longer than a few hours, check explicitly — don't assume "armed last time" still holds. This actually happened 7/15→16 (~22hr dead cron).
- **When PPM goes dark, PM routes product/sprint decisions directly to Lead rather than wait** — correct fallback, but means planning docs drift. First move on any resume-from-gap fire: check for decisions that happened without PPM in the loop, fold forward same-session.
- **Re-verify count claims live, not from commit-message tallies.** Two real instances this week alone (Beta-Blockers 7→24, then 24→21).
- **duty-cycle-tick Step 2 (git checkout + merge) doesn't apply** — Model B session, use a plain `git fetch`. See #1397.
- **ADR-077 vs ADR-078 vs ADR-079 are three different ADRs**, all touched by cohort work this week — 077 Routing Integrity, 078 Session-Activity-Ledger, 079 Owner-Scoping Integrity. Easy to conflate from commit-message shorthand.
- **"cc-pm" in mailbox filenames means `xian (ceo)`, not `ppm`.**

## Cron

Current job: `61944f35`, `52 6,9,12,15,18,21`, confirmed armed through day-close. Next fire 06:52 tomorrow (07-17). Leaving armed — STOP is a day-close ritual, not a cron-teardown.

---

*Rewrite this file at the end of every substantive fire (duty-cycle-tick v1.13).*
