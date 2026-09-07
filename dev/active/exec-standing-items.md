# Exec (Chief of Staff) — standing items

**Created 2026-09-06.** Exec was the only role of eleven with no standing-items file. Ten roles had
one; `scripts/aging-standing-items.sh` reported *"10 standing-items files, 5 readable"* and Exec was
not in either number — **not an unreadable file, an absent one.** That is strictly worse than the
coverage gap the script already names, and it is the same shape as CLAUDE.md's rule about the
freeze-watchdog registry: *no row at all is worse than a parked one, because absent means the
mechanism is structurally incapable of noticing.*

Found by running the checker against my own seat immediately after directing Lead to fix a staleness
problem in theirs. Mine was worse: Lead's carry-forward was two days stale, mine was three, and Lead
at least had a standing-items file.

**Date format**: the `Filed` column is what `aging-standing-items.sh` parses. Keep it `YYYY-MM-DD`.
A row with no blocker and a `Filed` date ≥21 days old will be flagged — that is the point.

| # | Item | Filed | Status |
|---|---|---|---|
| 1 | Ship #059 — PM review + edit before Wed Sep 9 publish | 2026-09-06 | Blocked on PM (draft delivered, audit clean, calendar row committed) |
| 2 | Cron rotation — job `5a59f399` armed 09-03, expires ~09-10 | 2026-09-03 | Rotate ~09-08 per the ~48h-before-expiry rule |
| 3 | Pard — 91 orphaned worktrees / 36 GB cleanup | 2026-09-06 | Blocked on CIO's total content-based sweep (I told Pard to hold rather than run off my 22% sample) |
| 4 | Pard — rate-limit non-interactive setting, as a harness question | 2026-09-06 | Awaiting Pard; PM ruled *"correct - I do not know"* and it was re-routed rather than closed |
| 5 | CIO — 7k joint recurring-duty synthesis | 2026-09-03 | Greenlit 09-06; CIO drafting, I take a pass before it reaches PM |
| 6 | CIO — `worktree-safety-check.sh` total sweep (91 of 91, states its denominator) | 2026-09-06 | Awaiting CIO; approved tonight |
| 7 | Lead — refresh carry-forward + add the refresh to START | 2026-09-06 | Awaiting Lead; PM directive, delivered 09-06 |
| 8 | Lead's brief decisions 2 and 3 — short test round, #1688 closer-call | 2026-09-06 | Blocked on PM; deploy (decision 1) approved 09-06, these two explicitly not covered |
| 9 | PM — should the START-side carry-forward refresh become a cohort-wide `duty-cycle-tick` amendment? | 2026-09-06 | Blocked on PM; flagged rather than broadcast off a single-role ruling |

## Closed

| Item | Filed | Closed | Outcome |
|---|---|---|---|
| Attention board — nine open decisions | 2026-08-30 | 2026-09-06 | Walked one by one with PM. Three already resolved (board was 33% stale), five ruled, one re-scoped. Board empty. |
| #1709 — why does nobody enforce the interface | 2026-09-06 | 2026-09-06 | Root-caused, routed to Arch, Protocol shipped as #1723, Lead drained the routing, #1709 closed. Same day. |
| Session-log START gap (7q) | 2026-09-06 | 2026-09-06 | PM directive → CIO shipped NO-SESSION-LOG detector in `duty-cycle-freeze-check.sh` v0.15; verified on my seat. |
