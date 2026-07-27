# Lead Dev carry-forward (rewritten 2026-07-23 ~11:10 PT)

## Session/env
- Worktree: `.claude/worktrees/lead-1452-harness`; session cron e1106eb5 (`17 6,9,12,15,18,21 * * *`, session-only — re-arm after any re-attach, Gap-C).
- **Beta at v28** (health 200) — masking fix + loop-aware Redis pool + lazy doc-init + polymorphic eager-load. main==production lockstep at 91e878a95; PM local synced.

## #1452 — state after the Thursday-morning marathon
- **CI GREEN and holding** (3 consecutive green batches; first green ~08:35, PM notified). Progress comment on #1452 records the milestone + composition.
- Backlog: **119** (arc 634→119; today 264→119, waves 15-42). All removals CI-arbitrated. **The accessible triage tail is DRAINED** — everything remaining is parked/gated: ~40 methodology (Arch), 16 spatial-held, 12 learning complex (dedicated session; incl. manual/test_learning_handler_phase1 with the hardcoded shared TEST_USER_ID), 16 flaky, ~12 env-oscillators, 3 load tests (need a quiet box), ~20 misc gated.
- Remaining composition: ~40 methodology (Arch fix-or-delete, LARGEST cluster), 9 connection_pool (HELD spatial), 7 spatial-adapter integration (parked, held cascade — complete_integration_flow + slack_spatial), 9 learning-cycle (dedicated de-flake session), ~13 flaky context-oscillators, ~8 env-oscillators (radar/publish_gaps — do NOT delist without CI confirmation), ~45 small glances.
- Discipline notes that earned their keep today: CI-confirms-shrink-lock (local claimed 20, CI said 6); waves validate in-sweep (wave 18 caught); push-pausing so CI runs can complete; flaky tag = context-oscillators, shrink-lock-exempt both ways.

## Queue next
- Learning-complex de-flake (dedicated session; quality-banked to a fresh session deliberately — 12 entries: cycle pair, phase3/4 perf, manual phase1 script; root causes: shared TEST_USER_ID + settings interference).
- Load tests (3) on a quiet box.
- Full-sweep-poison chase for the standup-flaky 9 (earlier-dirs source; the config-rewriting teardown removal may already have helped — retest in a dedicated sweep).
- On Arch (Exec escalated): methodology ruling now gates ~30% of remaining backlog; #1432 orphan pair; ContextMatcher note.
- On Exec: #1386 gate re-run window (beta v25+ carries both Scenario-B fixes).
- On PM: #1424 close-vs-keep (lean: close), #1427 PROD-RECONNECT confirm, migration decision (handoff at dev/active/lead-handoff-2026-07-21.md).

## Note 2026-07-25 day-close
- sync-pm-local no-op'd at day-close (PM checkout has local commits/WIP — designed behavior, PM's work wins; likely Saturday-evening drafting). Next successful sync catches up; re-check next START.
- Backlog 94 (learning complex drained + validated 7/25). Methodology-math memo with Arch (38-of-94 lever). Cohort roll to Amber authorized; my migration queued after the 5 idle roles.

## Amber-migration notes (2026-07-26, from the seat-roll probe burst)
- **2a-bis probe on my first Amber fire must use COMPOUND command shape** (the shape agents actually commit with) — standalone commits pass 4/4 while compound bypasses; Web's index-state mechanism explains it, validated on four seats (PA's amendment to v1.15; ask for the current skill rev at migration).
- sync-pm-local hard-codes the laptop checkout and no-ops on Amber (PA found; CIO/Pard own the fix) — expect the post-push PM-sync step to change shape there.
- Arch confirmed my methodology execution received ("the 43% lever already pulled").
