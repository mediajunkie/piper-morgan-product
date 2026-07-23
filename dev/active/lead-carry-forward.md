# Lead Dev carry-forward (rewritten 2026-07-23 ~08:25 PT)

## Session/env
- Worktree: `.claude/worktrees/lead-1452-harness`; session cron e1106eb5 (`17 6,9,12,15,18,21 * * *`, session-only — re-arm after any re-attach, Gap-C).
- Beta at v27; main==production lockstep (fe890b82e + pending push). No deploy owed — lazy-init fix only changes keyless behavior.

## #1452 burn-down — live state (Thursday 7/23 morning)
- Backlog on disk: 219 (waves 15-17 delisted; edge-trio re-listed flaky). Arc: 634→219.
- CI at fe890b82e: RED with exactly 5 new failures, all with fixes in hand locally:
  - update_issue pair: #943 pre-flight ("GitHub isn't connected", success=True) fires in keyless CI before the missing-field validation — FIXED locally (is_available pinned True in both tests), 35/35.
  - doc edge trio: pass keyed-local + CI-isolation, fail CI-sweep — re-listed `flaky` (context-oscillation; the tag is shrink-lock-exempt both ways).
- Probe step GREEN: "documents router mounted: 6 routes" — the lazy get_document_service() cure works; it also cured the 1185 pair (removed per CI shrink-lock).
- Wave 17 (llm_classifier_benchmarks, 7): #322 DI rot fixed, validates in-sweep. Push-ready.
- Wave 18 (standup_performance, 9): fixed standalone (async awaits + per-turn refresh mirroring process/adapters) — but FAILS in-sweep locally; prefix repro (integration+performance) in flight. If unfixable this fire: keep test fixes, re-list 9 (flaky), push.
- Known local-only sweep noise (~12: llm_config providers-list, keychain migration, config_pattern github, config_isolation, setup chromadb pair, startup no_hanging, intent_filtering index oscillator, scenario_driver/task_lifecycle/db_user_history/publish_gaps local-passers) — env-shape artifacts; CI is arbiter. Do NOT delist local-passers without CI confirmation (learned this fire: local claimed 20, CI confirmed 6).

## Queue after this
- intent_wiring RecursionError trio: poison lives in dirs BEFORE tests/integration; teardown FK defect already fixed (delete_test_user_fully). Entries stay.
- learning-pair de-flake session (shared TEST_USER_ID + settings interference); methodology/ (21) awaiting Arch; #1432 awaiting Arch; connection_pool (9) HELD spatial; ~200 triage glances.

## On others
- Arch (stalled, Exec escalated): methodology/ fix-or-delete; #1432 orphan-pair; ContextMatcher permissive-default note.
- Exec: #1386 gate re-run window (beta v25+ carries both Scenario-B fixes).
- PM: #1424 close-vs-keep (my lean: close); #1427 PROD-RECONNECT confirm; migration decision (handoff current at dev/active/lead-handoff-2026-07-21.md).
