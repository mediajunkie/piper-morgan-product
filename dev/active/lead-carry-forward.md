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

### RECONNECT (Connector Refactor) — 12 issues FILED + prefixed (PM-authorized 6/14)
- **All 9 workstreams covered**, prefixed `RECONNECT-WS{n}:` (MVP / Product Backlog): WS-1 #1226+#1199 · WS-2 **#1229** · WS-3 **#1230** · WS-4 **#1231** · WS-5 **#1232** (ADR output) · WS-6 #1201 · WS-7 #1109+#1110 · WS-8 #1220 · WS-9 **#1233** · discrete #1227 (quick win).
- New #1229–1233 created + board-placed (Sprint=RECONNECT, Status=Product Backlog); existing 7 renamed. §10 of scope doc updated to FILED.
- **Arch is working the ADR** (PM 6/14) → refines WS-2/WS-5/WS-1 scope (how much auth/config moves to MCP). Issue bodies are tracking targets, not frozen specs.
- **#1227** = the one ADR-independent quick win.
- **Claim-grounding pass (6/14, 5 agents)**: issues well-grounded, nothing fabricated; corrections applied (scope §2a/§2c + comments #1226/#1229/#1230). **Key gap → Arch**: cite **ADR-058** (multi-tenancy — RECONNECT partly *finishes* it, esp WS-2/7/9) + reconcile **ADR-052** (tool-based vs external-MCP-server) in the WS-5 ADR — flagged on #1232 + scope §11. §0 MCP decision now in `decisions.log`. New bug **#1235** (`/turns` display returns oldest-50, no offset).
- **`/audit-cascade` skill (Pattern-049, ISSUE gate, 6/14)**: the REAL template-conformance gate (distinct from the grounding pass above). All 12 RECONNECT issues → full `feature.md` conformance (**16/16**, verified; PM bar = full-now via 5-agent fan-out). Matrix: `dev/2026/06/14/RECONNECT-issue-phase-audit.md`. Issue gate done → next cascade gates (Gameplan→Prompts→Execute) run **per-WS post-ADR**. LESSON: when PM names a skill, invoke it (don't improvise a same-named pass).

### D1 (Beta design quality) — 10 issues, PROPOSED build order (awaiting PM bless to make durable / board-reflect)
- **Track A — quick wins:** ✅ **#1223 DONE** (most_recent param fix in `get_conversation_turns`; xfail removed + new test; verified green; pushed; → Review for accuracy). NEXT: **#1225** (home module minimize/dismiss) + **#1228** (typing/thinking indicator) — zero-dependency frontend.
  - Discovered + filed **#1234** (2 PRE-EXISTING reference_resolver failures: `_find_candidates` window bug [#1223-adjacent] + definite-ref 66.67% accuracy) — un-sprinted, PM triage.
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
