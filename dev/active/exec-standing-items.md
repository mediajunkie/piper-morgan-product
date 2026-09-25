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
| 1 | ~~Weekly Ship 059 — PM review + edit before Wed Sep 9 publish~~ | 2026-09-06 | **CLOSED 09-18** (12d stale): #059 published, and #060 has since published 09-16. Row outlived its subject by two Ships. |
| 2 | Cron rotation — nightly delete-then-create at STOP; current job `399cc524` armed 09-24, expires ~10-01 | 2026-09-07 | Ongoing ritual until cascade LaunchAgent verified for this seat (then retired); row refreshed 09-24 after sitting 3 rotations stale — same defect it was filed about |
| 3 | Pard — 91 orphaned worktrees / 36 GB cleanup | 2026-09-06 | Blocked on CIO's total content-based sweep (I told Pard to hold rather than run off my 22% sample) |
| 4 | Pard — rate-limit non-interactive setting, as a harness question | 2026-09-06 | Awaiting Pard; PM ruled *"correct - I do not know"* and it was re-routed rather than closed |
| 5 | CIO — 7k joint recurring-duty synthesis | 2026-09-03 | Greenlit 09-06; CIO drafting, I take a pass before it reaches PM |
| 6 | CIO — `worktree-safety-check.sh` total sweep (91 of 91, states its denominator) | 2026-09-06 | Awaiting CIO; approved tonight |
| 7 | Lead — refresh carry-forward + add the refresh to START | 2026-09-06 | Awaiting Lead; PM directive, delivered 09-06 |
| 8 | ~~Lead's brief decision 2 — the test round~~ | 2026-09-06 | ✅ **CLOSED — WAS NEVER BLOCKED ON PM AFTER 09-08.** PM ran the round 09-08 05:14 on v70 with per-item verdicts + screenshots. **This row sat stale 12 days and I boarded it to PM twice as 'blocked on PM'.** |
| 9 | ~~PM — should the START-side carry-forward refresh become a cohort-wide `duty-cycle-tick` amendment?~~ | 2026-09-06 | **CLOSED 09-18 — WAS NEVER BLOCKED ON PM AFTER 09-08.** CIO ruled AND shipped it: `mailboxes/cio/sent/shipped-cio-to-exec-...-both-amendments-shipped-...-2026-09-08.md`. Found by applying my own Step-2.0 rule (check the recipient's `sent/`) to my own file for the first time. **Duplicate of row 20.** |
| 10 | #1386 criterion 3 — re-run at MVP close with 2/4/5 (CXO+PPM correction accepted) | 2026-09-07 | Blocked until MVP close 2026-10-30; carry is now **4 of 6**, not 3 |
| 11 | Worktree `agent-af6f27891de682d61` — held, my clearance test was inconclusive | 2026-09-07 | Awaiting a tree-level check; other 2 flagged cleared, 88 safe |
| 12 | 12 tracked CSVs carry CRLF against `.gitattributes` eol=lf (incl. editorial-calendar) | 2026-09-07 | Unowned — needs a repo-wide `git add --renormalize` decision, not a unilateral fix |
| 13 | Lead — name the proposed test-round six by issue number | 2026-09-07 | Awaiting Lead; blocks PM's decision 2 from being a real choice |
| 14 | ~~Lead — read the FTUX flag value~~ | 2026-09-07 | CLOSED 09-08: read it myself, `=1`, ON. My digest alarm was a false positive |
| 15 | Web — cold-login capture of the FTUX first exchange (CXO's third unknown) | 2026-09-07 | Awaiting Web; unblocked 09-08, flag confirmed ON |
| 16 | ~~PM's six-item test round~~ | 2026-09-07 | ✅ **CLOSED — PM COMPLETED IT 2026-09-08, 4 pass / 2 fail.** #1656 (upload), #1657 (summarize), #1572 (timezone) closed on PM's live verdict; #1717 passed. **Stale 12 days; my error, not PM's silence.** |
| 17 | CXO+Arch — is there a METHOD for markdown→display and deliverable presentation? | 2026-09-08 | **Re-verified 09-22, still open — blocker updated.** `aging-standing-items.sh` flagged this as stale because the originally-cited #1615 is closed; checked directly rather than trust the flag: #1615 closing was one instance, the underlying recurrence is **#1729 (still OPEN)**. Updated citation, row stays open — the METHOD question is real, not resolved. |
| 18 | ~~Lead — #1527: did named-delete ship (a) or is the capability-decline false (b)?~~ | 2026-09-08 | ✅ **CLOSED 09-22 — answer was (b).** Verified from #1527's own close comments (2026-09-12, `78e325c9e`/`95839e7aa`, Lead): named-target delete HAD shipped (v67); the decline was false because the verb-shim had no DELETE cell for reminder/todo phrasings, so real classifier emissions fell through to a generic "not built yet." Fixed at the registry layer, re-verified against 88/88 new tests + a 4049-case sweep. Found by running `aging-standing-items.sh` against my own file and checking the flagged closed-blocker rather than assuming it was stale noise. |
| 19 | PA — confirm whether the ESSENCE ruling reference is live or historical | 2026-09-08 | Awaiting PA; deliberately not boarded as open OR stale |
| 20 | ~~PM — should the START-side carry-forward refresh become a cohort norm?~~ | 2026-09-06 | **CLOSED 09-18 — duplicate of row 9, same question filed twice, both stale for 10 days.** Resolved by CIO 09-08; see row 9. ⚠️ The irony is the finding: **the very amendment CIO shipped mandates a three-surface re-check per PM-gated row — and it lands on carry-forward rows, not standing-items rows, so this file never got it applied.** |
| 21 | ~~REMIND PM to review PA's Cross-Piper synthesis~~ | 2026-09-19 | ✅ **CLOSED same day** — PM read it, called it "excellent as usual", supports observations and recommendations, apologised for the 16-day delay. Relayed to PA. Reminder never needed. |

## Closed

| Item | Filed | Closed | Outcome |
|---|---|---|---|
| Attention board — nine open decisions | 2026-08-30 | 2026-09-06 | Walked one by one with PM. Three already resolved (board was 33% stale), five ruled, one re-scoped. Board empty. |
| #1709 — why does nobody enforce the interface | 2026-09-06 | 2026-09-06 | Root-caused, routed to Arch, Protocol shipped as #1723, Lead drained the routing, #1709 closed. Same day. |
| Session-log START gap (7q) | 2026-09-06 | 2026-09-06 | PM directive → CIO shipped NO-SESSION-LOG detector in `duty-cycle-freeze-check.sh` v0.15; verified on my seat. |
| 22 | ~~★ REMIND PM: check Vercel Deployment Storage~~ | 2026-09-19 | ✅ **CLOSED 09-25 — PM checked and shared screenshots: Deployment Storage 527.23 MB / 10 GB (down from ~20 GB peak; the 09-19 retention setting visibly took effect after Sep 22), Functions 80.72 MB / 10 GB. Both healthy, trend confirmed by the charts, nothing further owed.** |
| 23 | ~~★ MONDAY 10:00 — usage reassessment with PM~~ | 2026-09-20 | **CLOSED 2026-09-21 — superseded, far exceeded.** PM raised it directly mid-morning (62% at 48% through the week, hotter than the 40%/33% baseline) before my scheduled 10:38 check-in. Full transcript-based audit run instead of an estimate: `docs/internal/operations/weekly-usage-audit-2026-09-21.md`, 3 addenda. Root cause found (95.8% context re-read, not Fable/team-size), both PM hypotheses tested and both negative, model-tier corrections made in real time as CIO/Janus/Pard/Arch surfaced them. Four-workstream reduction plan sent to CIO same day. This is the most any single standing-item row has ever actually delivered against its own ask. |
| 24 | ★★ **CONTEXT-FLOOR PLAN — check progress at EVERY fire, not just when reminded.** PM, 09-22: *"stay on top of the context-floor plan, as it may be our biggest lever now (aside from more frequent clearing)."* Four items (CLAUDE.md/briefing audit — Docs; tick-skill refactor + registry efficiency — CIO; carry-forward spring-clean — fleet, directed by me). `git log` each item's paths every fire. **If zero movement persists past ~09-22 14:38, escalate beyond a repeat nudge** — ask directly whether CIO's two items are blocked (hook-incident cleanup is the likely real reason, not neglect) rather than nudging into silence twice. | 2026-09-22 | **Open — daily until all four items close, then review whether it stays a standing check or becomes an event-driven one.** |
