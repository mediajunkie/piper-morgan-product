# Lead Dev carry-forward (ephemeral session state — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-14 07:28 PDT (Fire 2 — mid gate walk)
**Session**: Opus 4.8, ephemeral worktree `interesting-beaver-7ee19c`, branch `claude/interesting-beaver-7ee19c`
**Cron**: `0c673f7e` — `17 7,10,13,16,19,22 * * *` (windowed; 22:17 = last-fire STOP; 7:17 = morning START). ARMED.
**Server**: restarted 2026-06-14 ~07:00 on latest (`3673d45d7`), PID 95577, health 200, LLM verified (PONG). Runs from the WORKTREE cwd → reads `worktree/data/github_preferences.json`.

## Constraints (durable)
- **Project-board changes: Lead READS + PROPOSES; PM/PPM apply — for now.** PM 6/14: NOT a permanent "never" — the path is **document the board conventions → learn them → skillify → then board ops become delegable per the skill.** Conventions are currently undocumented (PM unsure one exists); the board-conventions doc is the first step. Until then: read + propose only.
- Board reads: pull the FULL set (count==limit ⇒ truncated; project has ~1057 items), exact `.milestone.title` match, `grep -xF` (not `comm`) for issue-number set-ops.

## Roadmap (PM 6/14)
- New **Production** milestone planned between MVP and Fast Follow. **MVP = Beta 0.9; Production = 1.0; Fast Follow = 1.01/1.1.** Some MVP-tagged work (UI design-floor #1169–1173, #358 encryption, connector full-migration) may belong in Production.

## Active PM thread (HELD — needs PM)
- **#1165 M3 gate — WALK IN PROGRESS (6/14)**: PM walking items one-at-a-time. **Item 1 (#1155) FAILED live → band-aided** (no default repo resolved; wrote `data/github_preferences.json` → `mediajunkie/piper-morgan-product`; re-test pending PM). Items 2–5 (#496/#497/#1133/#1143) not yet walked. #1133→Radar re-scope captured in #1090 (M5). **PM deciding**: continue the walk vs. pause to scope the connector sprint.
- **#1226 CONNECTOR-MODEL DEBT (NEW, major)** — repo-resolution is fragile: cwd-relative flat-file prefs, **0 `project_repository_links` DB-wide** (so the #1192b default-project path is dead for everyone), 3× churn in 5 wks (#1042→#1192a→#1192b), silent-fail; stacks #1199. The prefs band-aid is cwd-fragile, NOT the fix. **PM weighing a connector-refactor sprint; I backed it (scope in #1226).**
- **#1225** — home modules need minimize/dismiss (PM flag; M5).

## Carried / queued (not immediate)
- **#1216** provenance field (is_seed/source on InsightDB) — handoff memo SENT to PPM (`a9010ef1e`); awaiting PPM ack + M-placement.
- **#1144** TEST-DISCIPLINE-REFACTOR (real fixtures not MagicMock) — **deferred to PM** (sets a fixture pattern; the next flywheel pickup once PM steers).
- **#1223** get_recent_turns DB fallback returns oldest-N not newest-N — filed, **M4 + Arch** (needs a `most_recent` param, not a blind DESC — caller analysis posted). xfail guard lives in #1208's window test.
- **#1224** pre-existing test failures (3 clusters: standup conversation-state, perf-indexes, error-message integration/perf) — filed for triage (env vs real).
- **#1209** AutonomousExecutor fleshing-out — **M4 (an MVP milestone, NOT Fast Follow** — corrected today).
- **#1211** shadowing+broad-except AST sweep (Arch-recommended) — Lead, unscheduled.
- **#1217/#1218** (PA-filed) — exhaustively non-reproducing (direct /api/v1/intent + ask_piper relay, 10 probes); **BLOCKED on PA's consult-piper session capture**.
- **#973** MEM-CACHE-AUDIT — queued AFTER M3 fully closes (acked to PA).

## Server
Restart env-stripped from the worktree if begun fresh next session:
`env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 nohup venv/bin/python main.py > /tmp/piper-server.log 2>&1 &` (the ephemeral worktree nests in main → finds main's .env/venv).

## Mail state
- Inbox: clear (lead).
- Sent today: #1216 PPM handoff; History→Radar RATIFIED → CXO/PPM.

## Notes
- DB up (port 5433). Canonical suite green (Q16 fixed → 243/0/0).
- **Bridge discipline**: `git stash push -- <paths>` (NEVER `-u`) on the shared main checkout — `-u` swept Web's untracked log today (recovered).
