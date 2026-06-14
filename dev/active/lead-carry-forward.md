# Lead Dev carry-forward (ephemeral session state — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-14 15:1x PDT (Fire 13 — RECONNECT decomposition + D1 build order)
**Session**: Opus 4.8, ephemeral worktree `interesting-beaver-7ee19c`, branch `claude/interesting-beaver-7ee19c`
**Cron**: `0c673f7e` — `17 22,7,10,13,16,19 * * *` (windowed; 22:17 = last-fire STOP; 7:17 = morning START). ARMED (verified Fire 13).
**Server**: restarted 2026-06-14 ~07:00 on latest (`3673d45d7`), PID 95577, health 200, LLM verified (PONG). Runs from the WORKTREE cwd → reads `worktree/data/github_preferences.json`.

## Constraints (durable)
- **Project-board changes: Lead may apply them WHEN PM AUTHORIZES (per-instance); default is READ + PROPOSE.** PM 6/14 refinement: "you can do these things when I authorize." Propose by default; on explicit PM go-ahead for a specific board op, do it. Path to *standing* delegation: **document conventions → learn → skillify** (conventions now documented at `docs/internal/planning/sprint-board-structure.md`); until skillified, board ops are per-authorization, not autonomous.
- Board reads: pull the FULL set (count==limit ⇒ truncated; project has **1061** items as of 6/14 — verified-good, not truncated), exact `.milestone.title` match, `grep -xF` (not `comm`) for issue-number set-ops.
- **WRITE TO WORKTREE PATHS** (`…/.claude/worktrees/interesting-beaver-7ee19c/…`), never bare main paths — Fire 13 lost 3 edits to the main checkout via bare paths (the shared main tree also actively reverts files). One-glance check: does the path contain `/.claude/worktrees/`?

## Roadmap (PM 6/14)
- New **Production** milestone planned between MVP and Fast Follow. **MVP = Beta 0.9; Production = 1.0; Fast Follow = 1.01/1.1.** Some MVP-tagged work (UI design-floor #1169–1173, #358 encryption, connector full-migration) may belong in Production.

## CURRENT STATE: M3 DONE; sprint order = D1 → RECONNECT → M4 → M5 (PM-agreed 6/14)
M3 closed (PM declared). Connector decision RATIFIED: **MCP, not native** (scope doc §0). Sprint plan & order all PM-agreed 6/14. We do **D1 now** (unblocked) while Arch designs the RECONNECT ADR (gates the connector build + M4's identity-dependent items).

### RECONNECT (Connector Refactor) — decomposed; FILING ADR-GATED
- **7 issues in RECONNECT** (PM moved 6/14): #1226 (trigger/WS-1), #1199 (WS-1/3), #1220 (WS-8 MCP anchor), #1109/#1110 (WS-7), #1201 (WS-6), #1227 (discrete output bug).
- **Decomposition done** → appended as §10 of `docs/internal/architecture/connector-refactor-sprint-scope-2026-06-14.md`. Existing 7 cover WS-1/6/7/8 (+3/9 seeded). **NEW issues needed for WS-2 (creds), WS-4 (honest-degrade contract), WS-5 (MCP-consumer contract = ADR output), WS-9 (identity unify)** — PROPOSED, **file AFTER Arch's ADR** (MCP decision reshapes WS-1/2/5). PM nudging Arch.
- **#1227 is the one ADR-independent quick win** (Slack mrkdwn rendering) — shippable anytime.

### D1 (Beta design quality) — 10 issues, PROPOSED build order (awaiting PM bless to make durable / board-reflect)
- **Track A — quick wins (start now, parallelizable):** #1223 (recent-turns oldest→newest, backend correctness, highest-value; tiny Arch param-confirm on `most_recent`), #1225 (home module minimize/dismiss), #1228 (typing/thinking indicator). #1225/#1228 zero-dependency frontend.
- **Track B — design-floor (sequential, under #1169 epic):** tokens (#1172a) → Dialog/Modal (#1170) → page-shell (#1171) → chat-page conformance (#1173) → CI-lint-gate (#1172b, enforcement LAST — can't gate-green a non-conforming tree). *Recommend splitting #1172 into 1172a-tokens / 1172b-gate.*
- **Track C — parked/flag:** #1218 (#NNN→close_issue trigger) BLOCKED on PA consult-piper capture; #1174 (proactive-presence discovery) reads as **M4-flavored** — recommend parallel discovery or move to M4 (PM's call).

## Carried / queued (not immediate)
- **#1216** provenance field (is_seed/source on InsightDB) — handoff memo SENT to PPM (`a9010ef1e`); PM moved to **M4**.
- **#1144** TEST-DISCIPLINE-REFACTOR (real fixtures not MagicMock) — **deferred to PM** (sets a fixture pattern; next flywheel pickup once PM steers).
- **#1224** pre-existing test failures (3 clusters: standup conversation-state, perf-indexes, error-message integration/perf) — filed for triage (env vs real); PM moved to **M5**.
- **#1209** AutonomousExecutor fleshing-out — **M4** (an MVP milestone, NOT Fast Follow — corrected 6/13).
- **#1211** shadowing+broad-except AST sweep (Arch-recommended) — Lead, unscheduled.
- **#1090** #1133→Radar re-scope captured here — **M5** polish.
- **#973** MEM-CACHE-AUDIT — queued (M3 now closed; can pick up when D1 leaves room; acked to PA).

## Server
Restart env-stripped from the worktree if begun fresh next session:
`env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 nohup venv/bin/python main.py > /tmp/piper-server.log 2>&1 &` (the ephemeral worktree nests in main → finds main's .env/venv).

## Mail state
- Inbox: clear (lead).
- Sent today: #1216 PPM handoff; History→Radar RATIFIED → CXO/PPM.

## Notes
- DB up (port 5433). Canonical suite green (Q16 fixed → 243/0/0).
- **Bridge discipline**: `git stash push -- <paths>` (NEVER `-u`) on the shared main checkout — `-u` swept Web's untracked log today (recovered).
- **GitHub prefs band-aid** (`data/github_preferences.json`, untracked runtime) keeps the GitHub floor working post-#1042; it is NOT the fix → deleted by RECONNECT WS-1. Two identities mapped: web `a25db09c…` + Slack `009afc8c…`.
