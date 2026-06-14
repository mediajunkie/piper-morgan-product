# Lead Dev carry-forward (ephemeral session state — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-13 22:57 PDT (STOP day-close)
**Session**: Opus 4.8, ephemeral worktree `interesting-beaver-7ee19c`, branch `claude/interesting-beaver-7ee19c`
**Cron**: `0c673f7e` — `17 7,10,13,16,19,22 * * *` (windowed, no overnight; 22:17 = last-fire-of-day STOP; 7:17 = morning START). ARMED.

## Active PM thread (HELD — needs PM)
- **#1165 M3 closing gate** — close-ready, two PM-side items: (1) PM's authenticated *browser* UAT walk of chat items (#1155/#496/#497/#953/#1133/#1143 — all verified server-side); (2) #1133 History → **Radar** re-scope (PM-RATIFIED, relayed to CXO/PPM; awaiting CXO entities-surfacing mockup #1090 → then Lead builds the slot swap). **Not Lead-blocked.** PM said "wrap up M3 in the morning."

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
