# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
>
> **Disposition policy is operational, not aspirational** (per HOST 360 synthesis pull, Apr 27): at every reconciliation, every item is checked against the >14-day-zero-movement threshold and force-decided here (do / defer-with-explicit-reason / drop). Items don't get parked. If an item recurs at the threshold across reconciliations without movement, the role-holder owes an explicit reason or it drops on the next pass.
>
> Last updated: **2026-07-13 ~09:15 AM PT** (full reconciliation, 7-day gap Jul 6 → Jul 13 — the gap included a cohort-wide outage, so this pass leans harder on git/GitHub verification than usual rather than trusting what any single session remembers). Every item below checked against live evidence, not carried on memory.

---

## Reconciliation context (Jul 13)

The Jul 6 → Jul 13 window was the busiest yet: Ship #050 and #051-kickoff shipped; the entire 744-issue sprint-recovery project closed out completely (incl. a final S2→A12 cleanup + new backup/restore infra so a third field-wipe can't recur); all 11 batch-1 alpha invites sent and testers are live; the Fly.io migration went from decision to fully-cutover production (`beta.pipermorgan.ai` live end-to-end, droplet kept in parallel deliberately); the #1386 beta-close gate is one PM browser-run + two mechanical Arch items from fully closed, having already caught nine product defects pre-tester-exposure; and a genuine Fri-evening-through-Sun laptop outage took 7 of 11 roles offline, which the watchdog correctly diagnosed as infrastructure (not individual failures) and which every affected role self-healed from once given a turn — no stray/duplicate processes resulted. Docs's own duty-cycle mechanism was retired overnight (Jul 12) in favor of a more resilient spawn-fresh design (Belt-4), which is the fix I'd flagged for exactly the fragility class this outage exposed.

---

## Active Items

| # | Item | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 1 | **Two stale unowned branches** | Docs/Lead (disposition) | **STILL OPEN, escalated 7/13.** Now confirmed 4 branches, all 8-9 weeks stale with zero movement: `xpoll-brief-staleness-hook` (5/10), `cxo-mux-surface-2` (5/19), `-4` (5/20), `-7` (5/18). | Third reconciliation carrying this — sent a direct memo to Docs+Lead (cc PM) invoking the tracker's own >14-day policy rather than carrying silently again (`fe7ddd854`). If no movement by next reconciliation, will note as PM-escalation-worthy rather than re-carry a 4th time. |
| 2 | **Account migration (pipermorgan.ai)** | PM (confirm) | **STILL OPEN — 10 days now.** First surfaced CIO's 7/6 §0; re-flagged in my own carry-forward 7/9 and again 7/12 (cron-recreate cycles kept hitting the same unresolved note). | PM's own call, no urgency signal from anyone, but worth an explicit decision rather than another silent carry — this outage is exactly the kind of event a dedicated (non-backup) account might behave differently under. |
| 3 | **#1386 beta-close gate — final stretch** | PM + Arch | **NEW — nearly done.** Criterion 3 (the multi-turn scenarios) fully closed as of last night: C 3/3, re-scoped B 4/4, nine product defects found-and-fixed same-day before any tester exposure, #1394 correctly scoped and P1-labeled. | Remaining: Arch's #1395 corpus-rev ratification (mechanical) + ADR-070-A A2/A4 code check (non-gating); PM's own Scenario A browser run (doubles as cutover smoke) + criterion-4 window assessment + criterion-6 sign-off. PM already commenting directly on the issue — no chase needed from me, just watching for close. |
| 4 | **ADR-078 (#1394 architecture) — awaiting build-lens** | Arch → Lead | **NEW — informational.** Arch ruled #1394 a genuine architectural gap (not missing wiring): one primitive (session-activity ledger), two seams. Filed PROPOSED, wants Lead's build-lens before finalizing. | On my radar for when it needs cohort coordination; no exec action yet. |
| 5 | **MCPB production-readiness sign-off** | All leadership | **CARRIED, unverified — needs a fresh status check.** No visibility into this thread since 7/6; a lot has shipped around it (invites sent, which implies the clean-machine gate passed in practice) but I don't have direct confirmation this specific sign-off thread closed. | Light check owed next reconciliation — may be moot if invites already validated the underlying concern. |

---

## Resolved this pass (verified, not assumed)

- **Ship #050 workstream review** — published (`weekly-ship-050-the-connector-gets-real`), long since distributed.
- **Cohort-attention-rollup refresh** — not a "gap" item anymore; it's an active standing practice (the Bridge Log), redeployed same-URL through the outage and its recovery. Dropped from Active Items; see Standing Checks.
- **HOST tester-roster gap (Rebecca Refoy)** — her email was relayed to HOST 7/6; all 11 batch-1 invites (including hers) went out 7/12.
- **"Climbing Higher" blog post voice-pass** — confirmed via editorial calendar: status `distributed`, full syndication URLs present, published 7/4. The "reverify" carry from 7/6 was already stale by the time it was written.
- **MCPB v0.1.9 clean-machine test relay** — couldn't find a direct confirming trace either way; folding into item #5 above rather than carrying as its own line, since it's the same underlying thread.

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

- **BRIEFING-CURRENT-STATE.md freshness** — CIO fixed the check itself 7/10 (was using filesystem mtime, structurally unreliable across worktrees; now git-log-based). Loop should be closed; worth one more confirm that it's stayed accurate.
- **dev/active/ cleanup** — recheck file count; cross-role cleanup-coordination candidate if over threshold again.
- **#1386 close** — check whether it's fully closed by next reconciliation; if still open, find out what's actually blocking (should be down to just PM's browser run + Arch's two mechanical items per this pass).
- **MCPB production-readiness** (item #5 above) — the deferred status check.

## RESOLVED — Gap-C dormancy, the standing check that predicted this week's outage

7/6's standing check flagged: "worth cross-checking whether the launchd watcher is actually firing; this exec fire found its own cron dead with no alert received." A week later, a genuine multi-day laptop outage killed 7 of 11 roles' session-scoped crons at once — and the watchdog (a different mechanism than what was being asked about here, it turned out — an hourly freeze-watcher, not launchd) caught it correctly: self-diagnosed "infrastructure event, not individual failures" when 4 watched roles went stale together, and paged PM repeatedly until resolved. No stray/duplicate processes resulted from the outage or the recovery. Docs's own duty-cycle — which uses a genuinely different, more resilient mechanism (scheduled-task, not session-scoped cron) — was never affected, and got promoted overnight 7/12 into "Belt-4," the cohort's new resilience direction. This standing check is closed: the underlying question (is the watchdog real and does it work) got a real-world answer, not just a design review.

---

*Maintained by: Chief of Staff, Executive Office (exec-code, DinP instance)*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session + during PM-directed reconciliations + post-multi-day-gap resume*
