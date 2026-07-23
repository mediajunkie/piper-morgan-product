# Lead Dev carry-forward (rewritten 2026-07-23 ~08:55 PT)

## Session/env
- Worktree: `.claude/worktrees/lead-1452-harness`; session cron e1106eb5 (`17 6,9,12,15,18,21 * * *`, session-only — re-arm after any re-attach, Gap-C).
- Beta at v27; main==production lockstep (fe890b82e + pending push). No deploy owed — lazy-init fix only changes keyless behavior.

## #1452 burn-down — live state (Thursday 7/23 morning)
- **CI GREEN at c0a10e40f (~08:35)** — first green under the gate; PM notified. Waves 19-25 pushed since (CI arbitration of that batch in flight at 2e7bff1f5).
- Backlog on disk: 182. Arc: 634→182. Waves today: 15 execution_analysis fix; 16 llm-marks (classification_accuracy+direct_interface); 17 benchmarks DI fix; 18 standup async/refresh fixes (9 ride flaky — full-sweep-only oscillation); 19 configuration_regression mock-theatre cut to 1 real test; 20 error_message_enhancement rewritten to degradation contract; 21 llm-marks (clarification_edge_cases+api_query); 22 integrations_dashboard JWT claims; 23 mcp_error_scenarios per #1436 ruling (4 dead-premise cut, breaker+resolver fixed); 24-25 todo suites (real UUID owners + selectin_polymorphic product fix in item_service, latent).
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
