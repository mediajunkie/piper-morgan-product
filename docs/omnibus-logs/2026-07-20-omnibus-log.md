# Omnibus Log: Monday, July 20, 2026

**Day**: Monday
**Sessions**: 2 (Lead Developer, Chief of Staff/Exec)
**Day Type**: STANDARD — 2 sessions with focused technical execution; CI became trustworthy;
first-ever fully-green Tests workflow in repo's visible history.
**Justification**: 2 sessions with no cross-role coordination overhead.
The day's technical execution was extremely dense (full CI harness + burn-down waves + B3 fix +
deployment + 4 riders), but structurally a focused two-role day meriting STANDARD.

**Git Commits**: 25+

---

## Chronological Timeline

- **09:02**: **Chief of Staff (Exec)** START — cron check: exactly one job (`920f2db2`), no duplicates.
  Ground-truth check confirms clean continuity from last STOP commit.
  Synced clean; Exec inbox empty.
  Notes automated watchdog stall alert for Arch (07:35 this morning, ~25h since last log) — already
  escalated by the watchdog automatically, no duplicate action taken.

- **09:05–10:30**: **Exec** tracker reconciliation (2-day gap, Jul 18→Jul 20; quiet inbox advanced to useful work).
  Three items resolved with direct evidence:
  - Ship #052 workstream collection (all 6 in; verified via git log dates)
  - HOST/CXO/CIO multi-day silence (all three confirmed resurfaced 7/19 via fresh session logs)
  - MCPB production-readiness (resolved by supersession — PM's MCPB-is-dead pivot)
  #1386 sequencing corrected: holding for Lead's #1394 re-probe result before convening CXO/PPM window.
  Worktree-collision item advanced: "confirmed + detection-fixed, cure in progress."
  Two new items added: Ship #052 PM-gated draft (do-not-touch), Lead's open #1424/#1427 questions.
  Stale-branches item flagged as active concern: 6 days silent despite CXO/CIO active since 7/19.

- **12:02**: **Lead Developer** START (PM present).
  Re-attaches in SHARED MAIN CHECKOUT (read-only + mail + careful explicit-path commits only).
  Cron Gap-C self-heal: re-armed as `e1106eb5`.
  PM asks two standing calls:
  - #1424 close-vs-keep → answered
  - #1427 PROD-RECONNECT confirm → answered
  **Significant finding on #1432**: Phase-4 verb-canonicalization lives ONLY in the orphaned
  `llm_classifier.py`; the live `classifier.py` has zero verb-emission machinery.
  June's gate-IDENTICAL result is consistent with never-wired on the live chat path.
  Memo sent to Arch with options (lean: delete orphan pair + record the flip's reference impl for
  re-landing under #1432).

- **12:47**: **Lead** #1452 harness BUILT (worktree `lead-1452-harness`).
  `scripts/known_failing_backlog.tsv` — 415 unique entries from the 7/19 enumeration
  (37 fixture-tagged, 378 explicit `triage`).
  `scripts/check_fullsuite_backlog.py` — both-direction shrink-lock with blind-spot guards:
  no-summary→refuse; file-level ERROR covers per-test entries; tag validation; backlog-size shrink
  signal printed and into CI summary. Gate contract pinned 6/6 (smoke-marked).
  Full Test Suite job rewired: named subset steps consolidated into ONE gate-governed sweep.

- **~13:00**: **Lead** #1394 B3 wiring FIXED (D4-conformant, per Arch's STOP lane).
  Diagnosis went past both of Arch's hypotheses:
  - Observer records fine; B3's scope is fine.
  - Root cause: `session_id` never reached Stage-0 (chat path passed no context; B3 read null → N1 fall-through).
  Plus two entry-order hazards found and fixed:
  1. B3 sat BELOW the classification cache (a cross-session cache hit on "change the title" would
     bypass resolution — session-relative messages must never be cache-served).
  2. `classify_multiple` ran `detect_multiple_intents` BEFORE classify — pattern-matches
     "change the title to X" → `update_document_query`, which IS the live Scenario-B turn-3
     misroute mechanism (test-confirmed: new wiring test caught it red before the fix).
  Fix: `session_id` as its own kwarg (never in context); Stage-0 hoisted above cache + above
  detect_multiple at both entries.
  4 live-wiring regression tests added (incl. cache-bypass + call-site-kwarg pins).
  B3 suite 22/22; routing-vocab + multi-intent green; smoke 526 passed.
  `intent-routing-stack.md` doc: added the missing Stage-0/B3 row
  (mandatory doc predated B3 — which is exactly how Sunday's partial-model happened).

- **~13:30**: **Lead** beta v25 deployed and verified (health 200).
  B3 fix live — one #1386 Scenario-B re-run now verifies #1393 (turn-1) AND #1394 (turn-3) together.
  Exec notified (CXO/PPM window unblocked).

- **~13:45**: **Lead** CI gate calibration applied.
  First CI run measured the true env delta: 236 CI-only failures (invisible for weeks:
  ubuntu/3.11/service-DB/no-keychain vs local Mac) added as triage.
  18 local-only removed per shrink-lock.
  Backlog: 633 (larger-and-honest beats smaller-and-blind).

- **~14:15**: **Lead** post-calibration delta = ONE oscillator.
  Latency-claim test — inherently timing-flaky.
  Minimal flake mechanism: `flaky` tag tolerated in both states (burn-down = de-flake then retag).
  Backlog: 634 (1 flaky).

- **~14:30**: **🟢 TESTS WORKFLOW FULLY GREEN** — commit `972b4287b`.
  First fully-green Tests workflow in the repo's visible history.
  Smoke ✓ Full Suite ✓ Gate OK. Backlog 634 visible in every CI summary.
  Day-1 protection live: new rot fails the build immediately; fixes lock in via shrink-lock.
  Calibration arc complete in 3 runs (415 → ±CI-delta → +flaky mechanism), deterministic.

- **15:47**: **Lead** Fire 3 — inbox duplicates round 3 root-caused.
  Root cause: add/delete merge semantics re-adding triaged memos from stale-base worktrees.
  **#1454 filed and FIXED same fire**: regen-script self-heal drops any inbox file whose read/ twin
  exists (authoritative-triage-state rule); functionally verified (caught both live ghosts on first run).
  Cohort-wide benefit: every role's mail-loop regen now self-heals this class.

- **15:47** (continued): **Lead** burn-down wave 1 — cross-user security cluster GREEN (22/22; was 18 failed).
  Root cause: fixture rot — tests predate the #1312 FK hardening and created lists/todos/files
  for owner IDs never inserted as users; the FK rejecting orphan owners is the product working.
  Uniform transform seeds each test's declared users via the file's own existing helper.
  18 backlog entries off (shrink-lock honored same-commit).

- **15:47** (continued): **Lead** contamination ROOT-CAUSED.
  `asyncpg InterfaceError: another operation is in progress` at fixture setup under full integration load.
  Poisoned shared-pool connections (loop-bound, abandoned mid-op by earlier tests).
  No single poisoner — accumulation effect; all halves/subdirs clean individually.
  Victim-class cure = fresh-engine fixtures (B15 house pattern); conversion of
  `conversation_repository` + `db_user_history` queued next wave.

- **~16:30**: **Lead** burn-down wave 2 — poisoned-pool victims immunized.
  `conversation_repository` + `db_user_history` fixtures converted to fresh-per-test engines.
  Proven in-sweep (0 errors under full integration load that previously killed them; 21/21 standalone).
  ~22 backlog entries off.
  `conversation_manager_integration`'s 9 stay: its poison is app-internal
  (ConversationManager's own global-factory calls — cure is session_scope_fresh-shaped app work).
  Poisoner-hunt disposition: victim-side immunization is the systemic cure; per-culprit unnecessary.

- **~17:00**: **Lead** waves 1+2 CI-CONFIRMED at `bdc6354f8` — backlog 634→596 day one.
  1 of 21 removed entries fails in CI only (`test_search_matches_title_preview_topics` — passes locally;
  pool immunization unmasked an env-dependent failure; suspected pg15-local vs pg16-CI search semantics).
  Re-added as triage (596); other 20 held.

- **18:47**: **Lead** Fire 4 — burn-down waves 3+4.
  Wave 3: `slack_config` 20/20 — `get_config`/`is_configured` grew a required `user_id` in
  the #734 multi-tenancy work; 21 call sites threaded.
  Wave 4: `capability_discovery` 31/31 — tests pinned the pre-#488 taxonomy;
  capability queries are DISCOVERY/get_capabilities by ratified design, checked before IDENTITY;
  "show my projects" moved to its PORTFOLIO pin.
  −32 backlog entries.

- **~19:30**: **Lead** waves 3+4 CI-CONFIRMED.
  All removals held (zero shrink-demands).
  #1381 greeting hour-of-day oscillator de-flaked at root: the evening template opens
  "I'm here and ready. Good evening!" — doesn't start with "Good ".
  Day-part frozen via patch (the gate's first hour-of-day catch, fixed at root not tagged).
  🟢 CONFIRMED at `d5bb7d1e9`. Workflow green.

- **~21:00**: **Exec** last fire — detached-HEAD found and fixed before anything else.
  `claude/infallible-newton-f0ec45` still existed, pointed at identical commit already on origin/main.
  Checked out cleanly; synced clean.
  Lead's memo: not just a re-probe result — a shipped fix. Beta v25 live with both Scenario-B
  fix candidates (#1393 turn-1 + #1394 turn-3) wired on the live chat path.
  Direct unblock notice sent to CXO+PPM (not passive FYI — scheduling handed to them and Lead directly).
  Tracker updated: #1386 coordination thread out of Exec's hands.

- **21:00**: **Lead** STOP — day-close.
  Day arc: 415-entry backlog → CI calibration (+236 env failures) → flaky mechanism →
  **🟢 first-ever fully-green Tests workflow** → 4 burn-down waves (634→570) →
  #1394 turn-3 B3 fix → beta v25 → 2 riders (#1454 closed, #1381 de-flaked).
  Carry to tomorrow: temporal_context re-pinning (16), conversation_manager app-internal cure (9),
  pg15/pg16 search diagnosis (1), 555 triage glances; Arch #1432 orphan-pair ruling.

- **21:02**: **Exec** STOP — day-close complete.
  Distributed cleanup: no stale cycle-log or tmp files.

---

## Executive Summary

**Sessions**: 2 · **Day Type**: STANDARD

### Core Themes

- **CI became trustworthy**: first fully-green Tests workflow in the repo's visible history
  (commit `972b4287b`); 40+ consecutive red runs ended Sunday cleared the path for today's harness work.
- **#1452 harness designed-to-green in one day**: 415-entry backlog → CI calibration
  (236 env-delta failures added; honest backlog is 634) → flaky mechanism → green → 4 burn-down waves
  same day (634→570); every wave CI-confirmed, zero shrink-demands.
- **B3/session-id fix ships as v25**: #1394 turn-3 continuity actually fixed; session_id never reached
  Stage-0; two entry-order hazards also fixed (cache-bypass + detect_multiple ordering);
  one #1386 gate-run now verifies #1393+#1394 together; Exec unblocks CXO/PPM window.
- **Contamination root-caused**: accumulation of poisoned shared-pool connections; victim-side
  immunization (fresh-engine fixtures = B15 pattern) is the systemic cure; no per-culprit hunt needed.

### Technical Details

- **#1452 harness**: `scripts/known_failing_backlog.tsv` (415 entries, later calibrated to 634);
  `scripts/check_fullsuite_backlog.py` (both-direction shrink-lock; blind-spot guards;
  backlog-size signal into CI summary); gate contract 6/6 smoke-marked.
- **B3 diagnosis**: `session_id` never in context → B3 read null → N1 fall-through;
  B3 below cache (session-relative messages cache-served = bug); detect_multiple before classify
  (live Scenario-B misroute mechanism, reproduced red before fix).
- **Burn-down waves**: (1) cross-user security FK-hardening rot fixed (22/22); (2) poisoned-pool
  victims immunized (21/21); (3) `slack_config` user_id threading (20/20); (4) `capability_discovery`
  taxonomy pins (31/31). Total day-one: 634→570 (−64).
- **#1454 mailbox-ghost self-heal**: regen-script drops inbox files whose read/ twin exists;
  cohort-wide fix; closed same-day.
- **#1381 de-flaked**: evening-hour oscillator (good-morning test failing post-17:00) fixed at root
  (day-part frozen via patch, not tagged).
- **Phase-4 finding**: verb-canonicalization lives only in orphaned `llm_classifier.py`;
  live `classifier.py` never received the flip; June's gate-IDENTICAL result consistent with never-wired.
  Memo to Arch; orphan-pair ruling pending.
- **intent-routing-stack.md updated**: Stage-0/B3 row added (doc predated B3 — source of Sunday's
  partial-model; mandatory doc updated same day as the fix).

### Impact Measurement

- Issues closed: #1454 (mailbox ghost self-heal)
- Beta v25 deployed: #1393 (turn-1) + #1394 (turn-3) both live on chat path
- CI workflow: first fully-green Tests workflow in repo history
- Backlog: 634→570 (−64 day one; 4 waves, all CI-confirmed)
- Contamination: root-caused and systemic cure applied (22+21 tests restored)
- #1386 window: unblocked — CXO/PPM scheduling handed off directly

### Session Learnings

- **Intent-routing-stack doc as the mandatory pre-work surface**: the doc predated B3, which is
  exactly why Sunday's investigation produced a partial model — the doc was missing Stage-0.
  A mandatory doc that doesn't cover a live stage is as harmful as no doc at all.
- **Larger-and-honest beats smaller-and-blind**: calibrating the backlog from 415 to 634 by adding
  236 real CI-env failures was the right move; the 415 felt like progress but masked a blind spot.
- **Accumulation contamination has no single culprit**: the fix is victim-side immunization,
  not poisoner-hunting — the B15 fresh-engine fixture pattern is the systemic cure.
- **De-flake at root, don't tag**: the #1381 evening-oscillator was fixed via patch (day-part frozen),
  not tagged as `flaky` — tagging oscillators as flaky grows a flake-maintenance debt;
  fixing at root closes the loop cleanly.

---

*Sources: `dev/2026/07/20/2026-07-20-0902-exec-code-log.md`,*
*`dev/2026/07/20/2026-07-20-1202-lead-code-log.md`*
