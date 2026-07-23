# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
>
> **Disposition policy is operational, not aspirational** (per HOST 360 synthesis pull, Apr 27): at every reconciliation, every item is checked against the >14-day-zero-movement threshold and force-decided here (do / defer-with-explicit-reason / drop). Items don't get parked. If an item recurs at the threshold across reconciliations without movement, the role-holder owes an explicit reason or it drops on the next pass.
>
> Last updated: **2026-07-20 ~09:15 AM PT** (full reconciliation, 2-day gap Jul 18 → Jul 20 — a genuinely eventful two days: Ship #052 drafted end-to-end, PM roused the full cohort and worked AFK-coordinated-through-Exec for a day, a live worktree-collision incident got investigated in real time and confirmed isolated, and a laptop crash was survived cleanly). Every item below re-checked against live GitHub/git evidence.
>
> Prior partial touches: 2026-07-14 ~21:15 PT (items #1, #6 only) — superseded.

---

## Reconciliation context (Jul 20)

The Jul 18 → Jul 20 window: **Ship #052 fully drafted** ("The Mechanism, Not the Memory" — all 6 workstream memos collected, all 7 omnibus logs read, routed to PM, awaiting fact-check/voice-pass). **HOST, CXO, CIO all resurfaced Jul 19** (confirmed via fresh session logs), closing out the prior window's multi-day-silence watch entirely. **The worktree-collision defect moved from "flagged risk" to "confirmed and detection-fixed"**: CIO's fleet audit found it isolated to one directory (21 of 22 others correctly paired, not a cohort problem), shipped a same-fire detection check into `duty-cycle-tick`, and PM is actively planning to end one of the colliding sessions — the only remaining cure. A separate, initially-alarming data-loss report turned out to be an unrelated, already-fixed bug in PPM's own retry logic, not an escalation of the collision itself. **#1386 (beta gate) accidentally auto-closed via a commit-message keyword coincidence, caught and reopened by PPM same day.** **Lead had a very productive Jul 19**: the "testers lose data every deploy" bug class fully retired (#1400/#1401), CI's smoke gate green for the first time in 40+ runs, #1394 root-caused to the classifier layer (Arch stopped Lead's first fix design as ADR-078-violating, redirected to a re-probe — still pending as of this morning). A laptop crash mid-afternoon Jul 19 was survived with zero work lost (push-routinely discipline held). PA's MCPB→hosted-MCP pivot (PDR-006) is real and moving — #1360/#1351 closed as superseded per PM's ruling.

---

## Active Items

| # | Item | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 1 | **Six stale unowned branches — disposition still pending, deletion-claim corrected** | Docs | **CORRECTED 7/22**: Janus relayed (via a PM conversation) that Docs deleted 5 of 6 on 7/21 "confirmed via git ls-remote" — checked directly, this is inaccurate: all 6 branches (4 CXO MUX, CIO's `xpoll-brief-staleness-hook`, `claude/fix-docker-migration-setup`) are still on `origin`. Sent Docs a memo (cc PM) with the exact list, asking them to execute now that authorization apparently already exists (per Janus, PM already approved 5 of 6, holding only `fix-docker-migration-setup` for explicit go-ahead) or clarify the blocker. | 8 days silent as of the original finding, now further complicated by an inaccurate "mostly resolved" claim reaching PM. Awaiting Docs' reply — don't assume this is close to done just because PM was told it was. |
| 2 | **Account migration (pipermorgan.ai)** | PM (confirm) | **STILL OPEN — 17 days now.** No new evidence either way. | PM's own call, no urgency signal from anyone. Continuing to carry. |
| 3 | **#1386 beta-close gate — UNBLOCKED 7/20, gate-run now Lead+CXO+PPM's to schedule** | Lead + CXO + PPM | **Resolved past the hold, 7/20 ~21:00**: Arch ruled, Lead built and shipped the fix — beta v25 live with both Scenario-B fix candidates (#1393 scaffolding leak + #1394 turn-3 referent resolution, now actually wired on the live chat path). One gate re-run verifies both. Notified CXO+PPM directly that the wait is over — nothing left for them to hold on. | No exec action needed now — handed the ball to Lead/CXO/PPM to schedule directly. Gate itself still has the other criteria unverified (canonical suite fresh-run, #1278 scope call, PM go/no-go) — don't assume close is imminent just because the scenario blocker cleared. |
| 5 | ~~MCPB production-readiness sign-off~~ | — | **RESOLVED (by supersession), 7/19.** PM confirmed MCPB is dead and pivoted PA to a hosted-MCP + Claude-plugin + ChatGPT-integration architecture (PDR-006). #1360 + #1351 (the MCPB-specific security issues this thread existed to track) closed as superseded per PM's ruling, verified via git log. | Dropped from Active — the underlying question this item tracked no longer has a referent. |
| 7 | ~~HOST + CXO + CIO — multi-day silence~~ | — | **RESOLVED, 7/19.** All three resurfaced with fresh session logs (verified via `find` this pass) and filed their Ship #052 workstream memos same day. | Dropped from Active. |
| 8 | ~~Ship #052 workstream review — collection~~ | — | **RESOLVED, 7/19 morning.** All 6 memos landed; Ship fully drafted same day, routed to PM. | Dropped from Active — see new item #10 for the draft's own status. |
| 9 | **Shared-worktree infrastructure defect — confirmed + detection-fixed, cure in progress** | CIO + PM (harness-level decision) | **Materially advanced 7/19**: CIO's full fleet audit (all 22 worktree directories) confirmed this is isolated to the one directory Exec+CIO share — not a cohort discipline problem. A real-time incident (a live rebase conflict caught mid-fire) further confirmed it's an active, ongoing risk, not historical. Detection fix shipped into `duty-cycle-tick` (Step 2a, checks dir/branch pairing every fire) so a recurrence is caught same-fire. **PM is actively planning to end one of the colliding sessions** — the only remaining cure — as of last night. | Check whether the restart happened overnight; if this session is still in `mystifying-lumiere-8bebd3` next pass with no new pairing mismatch, the cure likely landed on CIO's or PPM's side instead. |
| 10 | **Weekly Ship #052 draft — awaiting PM fact-check/voice-pass** | PM | **NEW, 7/19.** Theme "The Mechanism, Not the Memory." Drafted with all 6 memos, all 7 omnibus logs, editorial calendar verified, issues-closed count GitHub-verified. Two self-caught errors fixed before finalizing (an inaccurate "months-old" framing on #1394; an unverified "first" superlative on the CLAUDE.md trim). ~1790 words, flagged as comparable density to #051's approved overage. | Do not touch the draft again until PM has read it and responded — same discipline as #051. |
| 11 | **Lead Dev's #1424/#1427 decisions — still awaiting PM** | PM | **NO MOVEMENT since 7/18.** #1424 (close the Finish-the-Unfinished epic as sprint-complete, or keep it open as a ratchet-backlog tracker) and #1427 (confirm PROD-RECONNECT as the right bucket) — both briefed with grounded evidence 7/18, no PM answer yet. | Not blocking anything else; carrying quietly. |

---

## Resolved this pass (verified, not assumed)

- **Ship #052 workstream collection** — all 6 memos landed 7/19, Ship fully drafted, routed to PM (see Active #10 for the draft's own still-open status).
- **HOST + CXO + CIO's multi-day silence** — all three resurfaced 7/19, verified via fresh session logs.
- **MCPB production-readiness sign-off** — resolved by supersession, not by the sign-off it was originally waiting on: PM confirmed MCPB dead, pivoted to hosted-MCP (PDR-006), the specific issues this thread tracked closed as superseded.
- Prior pass's resolved items (Ship #051, ADR-078/#1394 architecture, Ship #050, cohort-attention-rollup, HOST tester-roster gap, "Climbing Higher" voice-pass) — unchanged, still resolved, not re-verified this pass since nothing suggested regression.

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

- **BRIEFING-CURRENT-STATE.md freshness** — CIO fixed the check itself 7/10 (was using filesystem mtime, structurally unreliable across worktrees; now git-log-based). Not re-verified since; worth a confirm if it comes up.
- **dev/active/ cleanup** — recheck file count; cross-role cleanup-coordination candidate if over threshold again.
- **#1386 close** — re-verify the checklist directly next time, not from memory. Lead's re-probe result (Active #3) is the immediate blocker to even scheduling the next real step.
- **Stale branches** (Active #1) — now 6 days silent despite owners being active; the next reconciliation is a natural point for a light second touch if still untouched.
- **Shared-worktree defect** (Active #9) — check whether PM's planned session-restart happened; this is the item most likely to actually resolve by next pass.
- **Ship #052 draft** (Active #10) — check for PM's fact-check/voice-pass response before touching the file again.

## RESOLVED — Gap-C dormancy, the standing check that predicted this week's outage

7/6's standing check flagged: "worth cross-checking whether the launchd watcher is actually firing; this exec fire found its own cron dead with no alert received." A week later, a genuine multi-day laptop outage killed 7 of 11 roles' session-scoped crons at once — and the watchdog (a different mechanism than what was being asked about here, it turned out — an hourly freeze-watcher, not launchd) caught it correctly: self-diagnosed "infrastructure event, not individual failures" when 4 watched roles went stale together, and paged PM repeatedly until resolved. No stray/duplicate processes resulted from the outage or the recovery. Docs's own duty-cycle — which uses a genuinely different, more resilient mechanism (scheduled-task, not session-scoped cron) — was never affected, and got promoted overnight 7/12 into "Belt-4," the cohort's new resilience direction. This standing check is closed: the underlying question (is the watchdog real and does it work) got a real-world answer, not just a design review.

---

*Maintained by: Chief of Staff, Executive Office (exec-code, DinP instance)*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session + during PM-directed reconciliations + post-multi-day-gap resume*
