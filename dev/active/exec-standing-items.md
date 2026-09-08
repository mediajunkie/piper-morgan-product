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
| 1 | Weekly Ship 059 — PM review + edit before Wed Sep 9 publish | 2026-09-06 | Blocked on PM (draft delivered, audit clean, calendar row committed) |
| 2 | Cron rotation — job `52fb898d` armed 09-07 21:03, expires ~09-14 | 2026-09-07 | Rotate ~09-12; registry row updated (it had named a July job, 3 rotations stale) |
| 3 | Pard — 91 orphaned worktrees / 36 GB cleanup | 2026-09-06 | Blocked on CIO's total content-based sweep (I told Pard to hold rather than run off my 22% sample) |
| 4 | Pard — rate-limit non-interactive setting, as a harness question | 2026-09-06 | Awaiting Pard; PM ruled *"correct - I do not know"* and it was re-routed rather than closed |
| 5 | CIO — 7k joint recurring-duty synthesis | 2026-09-03 | Greenlit 09-06; CIO drafting, I take a pass before it reaches PM |
| 6 | CIO — `worktree-safety-check.sh` total sweep (91 of 91, states its denominator) | 2026-09-06 | Awaiting CIO; approved tonight |
| 7 | Lead — refresh carry-forward + add the refresh to START | 2026-09-06 | Awaiting Lead; PM directive, delivered 09-06 |
| 8 | Lead's brief decision 2 — the test round | 2026-09-06 | Blocked on PM; decision 1 (deploy) and decision 3 (FTUX flip) both ruled 09-07 |
| 9 | PM — should the START-side carry-forward refresh become a cohort-wide `duty-cycle-tick` amendment? | 2026-09-06 | Blocked on PM; flagged rather than broadcast off a single-role ruling |
| 10 | #1386 criterion 3 — re-run at MVP close with 2/4/5 (CXO+PPM correction accepted) | 2026-09-07 | Blocked until MVP close 2026-10-30; carry is now **4 of 6**, not 3 |
| 11 | Worktree `agent-af6f27891de682d61` — held, my clearance test was inconclusive | 2026-09-07 | Awaiting a tree-level check; other 2 flagged cleared, 88 safe |
| 12 | 12 tracked CSVs carry CRLF against `.gitattributes` eol=lf (incl. editorial-calendar) | 2026-09-07 | Unowned — needs a repo-wide `git add --renormalize` decision, not a unilateral fix |
| 13 | Lead — name the proposed test-round six by issue number | 2026-09-07 | Awaiting Lead; blocks PM's decision 2 from being a real choice |
| 14 | ~~Lead — read the FTUX flag value~~ | 2026-09-07 | CLOSED 09-08: read it myself, `=1`, ON. My digest alarm was a false positive |
| 15 | Web — cold-login capture of the FTUX first exchange (CXO's third unknown) | 2026-09-07 | Awaiting Web; unblocked 09-08, flag confirmed ON |
| 16 | PM's six-item test round | 2026-09-07 | Blocked on PM; walkthrough delivered, PM sequenced it after tomorrow's blog post |
| 17 | CXO+Arch — is there a METHOD for markdown→display and deliverable presentation? | 2026-09-08 | Awaiting CXO/Arch; PM's observation, 5 fixes at 5 sites, #1615 recurred as #1729 |
| 18 | Lead — #1527: did named-delete ship (a) or is the capability-decline false (b)? | 2026-09-08 | Awaiting Lead; if (b), a decline is a false claim about our own surface |
| 19 | PA — confirm whether the ESSENCE ruling reference is live or historical | 2026-09-08 | Awaiting PA; deliberately not boarded as open OR stale |
| 20 | PM — should the START-side carry-forward refresh become a cohort norm? | 2026-09-06 | Blocked on PM; asked 09-06, unanswered, 3 more stale instances found 09-08 |

## Closed

| Item | Filed | Closed | Outcome |
|---|---|---|---|
| Attention board — nine open decisions | 2026-08-30 | 2026-09-06 | Walked one by one with PM. Three already resolved (board was 33% stale), five ruled, one re-scoped. Board empty. |
| #1709 — why does nobody enforce the interface | 2026-09-06 | 2026-09-06 | Root-caused, routed to Arch, Protocol shipped as #1723, Lead drained the routing, #1709 closed. Same day. |
| Session-log START gap (7q) | 2026-09-06 | 2026-09-06 | PM directive → CIO shipped NO-SESSION-LOG detector in `duty-cycle-freeze-check.sh` v0.15; verified on my seat. |
