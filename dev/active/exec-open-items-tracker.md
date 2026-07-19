# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
>
> **Disposition policy is operational, not aspirational** (per HOST 360 synthesis pull, Apr 27): at every reconciliation, every item is checked against the >14-day-zero-movement threshold and force-decided here (do / defer-with-explicit-reason / drop). Items don't get parked. If an item recurs at the threshold across reconciliations without movement, the role-holder owes an explicit reason or it drops on the next pass.
>
> Last updated: **2026-07-18 ~09:20 AM PT** (full reconciliation, 5-day gap Jul 13 → Jul 18 — Ship #051 shipped, a cohort-wide reauth event killed every session-scoped cron at once, and a genuine shared-worktree infrastructure defect was confirmed via git internals). Every item below re-checked against live GitHub/git evidence, not carried on memory or on last week's optimistic notes.
>
> Prior partial touches: 2026-07-14 ~21:15 PT (items #1, #6 only) — superseded by this pass.

---

## Reconciliation context (Jul 18)

The Jul 13 → Jul 18 window: Ship #051 published Jul 15 ("Impossible by Construction" — the Sprint-field wipe named plainly, corrected metrics after Comms's fact-check caught two adjacent-number contaminations); ADR-078/#1394's architecture reached a real completion point (B4 ledger + B3 resolution both Arch-ratified Jul 16, "architecture complete") though the GitHub issue itself and the #1386 gate around it remain open; a **Finish-the-Unfinished sprint** landed and re-expanded Beta Blockers from 7 back up to 24 open issues (v0.8.11.0 released) — the beta-close gate (#1386) is materially further from closing than last week's "nearly done" note suggested, not closer, because scope grew; a cohort-wide **reauth event killed every session-scoped cron simultaneously** (CIO-diagnosed, no lost work, HOST's multi-day silence explained by this); and a genuine **shared-worktree infrastructure defect** was confirmed via `git reflog` — this exec's designated worktree has been sharing a physical directory with at least CIO's session, evidenced by interleaved local commits/rebases, a branch-identity shift, and a detached-HEAD incident, all self-caught and reported, none causing data loss so far. Also: the Friday workstream-review kickoff fix (built Tuesday after PM overrode a partial Ship #051 draft) had its first live run this Friday — Ship #052 collection is in progress, 2 of 6 in, due Mon Jul 20.

---

## Active Items

| # | Item | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 1 | **Four stale unowned branches — disposition still pending** | CXO/CIO/Docs | **NO MOVEMENT since 7/14.** All three (CXO's 3 MUX branches, CIO's xpoll-hook, Docs' confirmed-safe branch) still awaiting reply. CXO's silence is explained (see #7) — not a refusal, just hasn't been seen. | Checked directly via `find` for any reply — none. Not yet at a re-escalation point (only ~4 days since the ask), but if CXO resurfaces and this is still untouched, worth a direct mention. |
| 2 | **Account migration (pipermorgan.ai)** | PM (confirm) | **STILL OPEN — 15 days now.** No new evidence either way. | PM's own call, no urgency signal from anyone. Continuing to carry rather than force a decision that isn't mine to make. |
| 3 | **#1386 beta-close gate — coordination now active, Exec relaying** | PM + Arch + Lead + Exec (relay) | **PM approved (7/18 ~22:00) Lead's proposal to coordinate the close-out through Exec.** Kickoff sent to CXO + PPM same night (cc Lead, PM) — asked them to confirm #1394's still-open status against the TESTER-QUICKSTART disclosure plan, and to connect directly with Lead for whatever else the close-out needs. | Still true from last reconciliation: scope grew (Beta Blockers 7→24 via Finish-the-Unfinished), so don't assume "nearly done." This item now has an active coordination thread, not just a status-watch — check for CXO/PPM replies next pass. |
| 4 | ~~ADR-078 (#1394 architecture) — awaiting build-lens~~ | Arch → Lead | **RESOLVED, 7/16.** Verified via `gh issue view` comments + git log: Arch ratified both B4 (session-activity ledger primitive) and B3 (D2/OQ-3 resolution) — "this COMPLETES the #1394 architecture." | Folded into #3's context above rather than tracked standalone — the remaining #1394 GitHub issue is now an implementation/closure detail of the #1386 gate, not an open architectural question. |
| 5 | **MCPB production-readiness sign-off** | All leadership | **Still not formally confirmed, but likely overtaken by events.** No new evidence of a named sign-off closing, but batch-1 invites have been live with real testers using MCPB in practice for over a week now — the practical concern this thread existed to catch has almost certainly already been validated in the field. | Not resolving outright (no direct confirming trace exists), but softening from "needs a fresh check" to "low-priority, likely moot" — will drop entirely if no one raises it as a live concern by next full reconciliation. |
| 6 | ~~Weekly Ship #051 — PM-approved, handing to Comms for footer~~ | PM → Comms | **RESOLVED, confirmed via editorial calendar.** Published Jul 15, status `distributed`, live LinkedIn + blog URLs, corrected "2" issue figure present (matching Comms's fact-check) — footer/P.S. work clearly completed since the piece shipped. | Dropped from Active. |
| 7 | **HOST + CXO + CIO — multi-day silence; PM pinging directly** | PM | **PM is personally pinging HOST/CXO/CIO by tomorrow morning (7/18 evening).** CIO also got a real automated watchdog stall alert (`STALE cio 47h`) same day. PA's identical gap already resolved this way — PM pinged directly, PA resurfaced same day. | No exec action needed on this thread now that PM is handling it directly — check tomorrow morning whether any/all three have resurfaced. |
| 8 | **Ship #052 workstream review — collection in progress** | Exec (synth) ← 6 leads | **STILL 2 OF 6** (Arch, Comms) as of 7/18 evening. Missing: **HOST, CIO, CXO, PPM** — all four are roles PM is aware of and addressing (HOST/CXO/CIO via direct pings planned for tomorrow AM; PPM separately quiet since 7/16, not yet flagged to PM). Still ahead of Mon Jul 20 EOD deadline. | Hard gate applies (draft-weekly-ship v1.6): do not begin synthesis before all 6 land. Worth naming PPM to PM explicitly if not already covered by tomorrow's pings. |
| 9 | **Shared-worktree infrastructure defect — confirmed, unresolved** | CIO + Docs + PM (harness-level decision) | **CONFIRMED via `git reflog`, escalated 7/16, no reply yet as of 7/18.** This exec's designated worktree has been genuinely shared with at least CIO's session — evidenced by interleaved local commits/rebases (not just fast-forward merges), a branch-identity shift, and a detached-HEAD incident (self-fixed safely each time). No data loss so far, but this is luck of timing, not safety by design. | Deliberately not attempting a fix at the fire level — this needs a decision at the worktree-provisioning layer. Checking `pwd`/branch/`git log -1` at the start of every fire until this resolves. |

---

## Resolved this pass (verified, not assumed)

- **Ship #051** — published Jul 15, confirmed via editorial calendar (see Active #6 above, now dropped).
- **ADR-078 / #1394 architecture** — Arch-ratified complete Jul 16 (see Active #4 above, folded into #3's context).
- **HOST's multi-day silence** — root-caused, not mysterious: cohort-wide reauth killed every session-scoped cron simultaneously (CIO's verified diagnosis, no lost work found).
- Prior pass's resolved items (Ship #050, cohort-attention-rollup, HOST tester-roster gap, "Climbing Higher" voice-pass) — unchanged, still resolved, not re-verified this pass since nothing suggested they'd regressed.

---

## Disposition applied this reconciliation (Jul 6) — prior 8 items

All verified via git log / `gh issue view` / session-log citations (research pass, 7/6). Full evidence trail in `dev/2026/07/06/2026-07-06-0803-exec-code-log.md` and this fire's log entry.

- **RESOLVED — Ship #047 workstream review**: published as "The team catches itself"; superseded 3× over by #048, #049, #050.
- **RESOLVED — Migration instruction-gaps + m-41 instance #2**: PROVEN-PROMOTION ratified 6/12 (Arch CONCUR); m-41 has since matured into a repeatedly-invoked live pattern through July.
- **SUPERSEDED — Routines watchdog build decision**: the $70/mo external-watchdog framing was dropped (PM 6/17: "Max plan covers; not a funding question"). Actual cure evolved to a `launchd` OS-watcher (shipped 6/15). **Caveat**: Gap-C dormancy is still a live, recurring failure mode as of this morning (this exec fire found its own cron fully unarmed) — the *watchdog decision* is closed, but Gap-C itself is not eliminated. Worth a fresh look at whether the launchd watcher is actually catching these, given today's finding.
- **RESOLVED — Role-portfolio framework + pilot**: full cohort adoption — 12 `ROLE-PORTFOLIO-*.md` files exist, all roles covered, ratified 6/14.
- **RESOLVED (absorbed) — BYO-colleague synthesis 3 questions**: effectively resolved by deferral-to-M4, which hasn't started yet (M4 is next after M3/RECONNECT/D1, all closed as of 7/1). Dormant-by-schedule, not stuck.
- **CONFIRMED STILL TRUE — Duty cycle windowed + Option B**: no update needed; BRIEFING-CURRENT-STATE (last_verified 7/3) and every role's 7/6 session log confirm Option B ephemeral-worktree is still canonical.
- **RESOLVED, promoted to Active #2 — Cohort-attention-rollup**: was far more current than the stale tracker suggested (compiled 6/24, 6/25, 6/26, 6/27) but has a fresh 9-day gap now — moved to Active Items as a live task rather than closed.
- **MIXED, split into Active #3/#4/#5/#6 — Owner-lane carries**: alpha→beta still gated on M4→M5 (neither started, correctly not-yet); methodology catalog grew substantively (m-41 elaborated, pattern-073 added); HOST 360 R2 active (dashboard-welfare-criteria v0.3 published 7/3); the two stale branches are still undisposed — carried forward as Active #3.

## Archived audit trail

Pre-Jun-12 history preserved in git history (`exec-open-items-tracker.md` @ commit prior to 2026-06-12). Jun-12-era detail (old items 1-15, disposition applied then) recoverable via `git log -p` if an audit needs it.

---

## Standing checks (next reconciliation)

- **BRIEFING-CURRENT-STATE.md freshness** — CIO fixed the check itself 7/10 (was using filesystem mtime, structurally unreliable across worktrees; now git-log-based). Not re-verified this pass; worth a confirm if it comes up.
- **dev/active/ cleanup** — recheck file count; cross-role cleanup-coordination candidate if over threshold again.
- **#1386 close** — re-verify the checklist directly next time rather than trusting a prior "nearly done" note (see Active #3's correction this pass — the gate got further away, not closer, when scope expanded).
- **MCPB production-readiness** (Active #5) — drop entirely if nothing surfaces by next full reconciliation.
- **Shared-worktree defect** (Active #9) — check for any CIO/Docs/PM reply; this is the item most likely to need a real decision soon.
- **Ship #052 collection** (Active #8) — confirm all 6 landed by Mon Jul 20 EOD before touching the draft at all.

## RESOLVED — Gap-C dormancy, the standing check that predicted this week's outage

7/6's standing check flagged: "worth cross-checking whether the launchd watcher is actually firing; this exec fire found its own cron dead with no alert received." A week later, a genuine multi-day laptop outage killed 7 of 11 roles' session-scoped crons at once — and the watchdog (a different mechanism than what was being asked about here, it turned out — an hourly freeze-watcher, not launchd) caught it correctly: self-diagnosed "infrastructure event, not individual failures" when 4 watched roles went stale together, and paged PM repeatedly until resolved. No stray/duplicate processes resulted from the outage or the recovery. Docs's own duty-cycle — which uses a genuinely different, more resilient mechanism (scheduled-task, not session-scoped cron) — was never affected, and got promoted overnight 7/12 into "Belt-4," the cohort's new resilience direction. This standing check is closed: the underlying question (is the watchdog real and does it work) got a real-world answer, not just a design review.

---

*Maintained by: Chief of Staff, Executive Office (exec-code, DinP instance)*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session + during PM-directed reconciliations + post-multi-day-gap resume*
