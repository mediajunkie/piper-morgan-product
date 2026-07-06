# Executive Office: Open Items Tracker

> **Living document** — updated at the end of every exec session.
> This is the canonical list of tracked items. Session logs may contain discussion but this file is the source of truth.
>
> **Disposition policy is operational, not aspirational** (per HOST 360 synthesis pull, Apr 27): at every reconciliation, every item is checked against the >14-day-zero-movement threshold and force-decided here (do / defer-with-explicit-reason / drop). Items don't get parked. If an item recurs at the threshold across reconciliations without movement, the role-holder owes an explicit reason or it drops on the next pass.
>
> Last updated: **2026-07-06 ~09:15 AM PT** (full reconciliation after a 24-day gap Jun 12 → Jul 6 — the prior version was anchored to a Ship #047-in-progress worldview, 3 ship cycles behind current reality). Every one of the 8 prior items was verified against git/GitHub/session-log evidence rather than carried forward assumed-stale; see disposition below.

---

## Reconciliation context (Jul 6)

The Jun 12 → Jul 6 window moved almost everything the prior tracker had open: Ship #047/#048/#049 all published, #050 mid-cycle (§0 collection, 6/8 in as of this morning); role-portfolio framework reached full 12-role cohort adoption; RECONNECT (GitHub connector) went from design to essentially architecturally complete; the invite-gate (#1344) shipped to production (v0.8.9.2); a real duty-cycle bug (self-attribution drift) was found, diagnosed, and fixed at the CLAUDE.md + skill level; the irreversible-action guardrail was ratified cohort-wide after 3 incidents. **Zero items dropped this pass** — every prior item resolved, superseded, or is still genuinely open (not abandoned).

---

## Active Items

| # | Item | Owner | Status | Notes |
|---|------|-------|--------|-------|
| 1 | **Ship #050 workstream review (Jun 27–Jul 3)** | exec (synthesize) | **COLLECTION COMPLETE — 6/6 in.** Arch, CXO, PPM, Comms, HOST, CIO. (Corrected 7/6: roster is 6 per `methodology-25`, not 8 — Lead Dev was never in-process and PA is cc-only. Confirmed against 10 prior ship cycles.) | Ready to synthesize now — nothing left to collect. CIO's §0 has a same-day self-correction (struck the "#972/gbrain = 2 slips" framing — both are done); use corrected version when synthesizing. |
| 2 | **Cohort-attention-rollup refresh** | exec (maintains) | **DUE — 9-day gap.** Last compiled 6/27 (`dev/2026/06/27/exec-cohort-attention-rollup-2026-06-27.html`); nothing since despite Ship #048/#049/#050, RECONNECT completion, #1343/#1344 security fixes, invite-gate shipping, and the self-attribution-drift saga. | Candidate for this fire or next — genuinely unblocked, no PM gate. |
| 3 | **Two stale unowned branches** | Docs/Lead (disposition) | **STILL OPEN.** Likely candidates: `claude/xpoll-brief-staleness-hook` (last commit ~5/10) and one of the `remotes/origin/claude/cxo-mux-surface-{2,7}-2026-05-1{8,9}` branches — all ~7-8 weeks stale, unmerged. | Not exec-fixable (not exec's branches); flagging so it doesn't silently ride another reconciliation. Owner needs to actually decide merge-or-delete. |
| 4 | **Account migration (pipermorgan.ai)** | PM (confirm) | **NEW — blocked on PM.** Both Exec's and CIO's rows on `docs/migration/pipermorgan-ai-account-migration.md` are unconfirmed; neither role can self-determine which account it's running under from inside a session. | Surfaced independently by CIO's 7/6 §0. Needs PM's direct confirmation across the whole checklist, not just exec+CIO. |
| 5 | **HOST tester-roster gap (Rebecca Refoy)** | PM (supply) | **NEW — blocked on PM.** 1 of 10 alpha testers has no email in the roster; blocks her invite-code delivery. | Surfaced via HOST's 7/6 §0. Small, discrete PM ask. |
| 6 | **MCPB production-readiness sign-off** | All leadership (process just started) | **NEW — informational, no action yet.** PA's 7/6 leadership briefing initiates the formal skunkworks→production sign-off PM's standing rule requires (incl. CXO design sign-off). Two known gaps tracked: #1360 (credential verification, pending clean-machine test) and #1351 (session isolation, beta blocker). | On exec's radar for when production-readiness comes up in planning; no coordination needed yet per PA's own memo. |
| 7 | **"Climbing Higher" blog post voice-pass** | PM (edit) | **CARRIED — reverify.** Published 7/4/7/5 without PM's voice-pass as of last check. | Quick status check owed next fire — may already be resolved. |
| 8 | **MCPB v0.1.9 clean-machine test result relay** | exec/PM (relay) | **CARRIED.** PM ran the test night of 7/4; PPM/PA still waiting on the result being relayed to them. | Check with PM directly — this is a relay-only task once the result exists. |

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

- **Ship #050 synthesis** — collection complete, ready to compile.
- **BRIEFING-CURRENT-STATE.md** freshness — check against 7-day window.
- **dev/active/ cleanup** — recheck file count; cross-role cleanup-coordination candidate if over threshold again.
- **Gap-C dormancy** — worth cross-checking with CIO/HOST whether the launchd watcher is actually firing; this exec fire found its own cron dead with no alert received.

---

*Maintained by: Chief of Staff, Executive Office (exec-code, DinP instance)*
*Filename: exec-open-items-tracker.md*
*Update trigger: end of every exec session + during PM-directed reconciliations + post-multi-day-gap resume*
