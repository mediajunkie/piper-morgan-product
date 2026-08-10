# Session Log — 2026-08-10 07:56 — Coding Agent (prog) — Time-Handling Class Audit

**Role**: Coding Agent (prog), isolated worktree `worktree-agent-ae88394db2a98e100`
**Model**: Fable 5 (claude-fable-5)
**Task**: PM-directed time-handling class audit (AUDIT ONLY, no fixes). Deliverable:
`docs/internal/operations/time-handling-audit-2026-08-10.md` in the style of the
principal-dropping (08-08) and status-truth (08-09) class audits.
**Constraints**: commit locally only — NO push, NO mailboxes/, NO `gh`.

## Plan
1. Read the two prior class audits for method/format (m-43 rigor: stated method,
   denominators, ranked findings, root cause, canonical model).
2. Enumerate 5 scopes: PARSE anchors, STORAGE, DISPLAY, COMPARISON/roll rules,
   user-tz infrastructure. Static analysis + cheap env-stripped probes.
3. Verify PM's implied root finding: user-typed clock times interpreted on the
   SERVER clock (UTC on fly) absent per-user tz.
4. Write audit doc; commit doc + log locally.

## Work

- 08:00 — Read both prior class audits (format locked). Read temporal_utils.py in full
  (418 lines): every parse anchors `datetime.now().astimezone()` = server clock.
- 08:02 — STORAGE swept directly: 83 DateTime columns in services/database/models.py +
  2 in services/persistence/models.py, **all** `DateTime(timezone=True)`, zero naive.
  services/utils/datetime_utils.py (#750) exists: utc_now/ensure_utc/utc_now_naive.
- 08:05 — Found THREE existing per-user/config tz sources, none wired to parse/display:
  (1) PersonalizationContextRepository context["timezone"] (ADR-075 D1) — read only by
  `_current_time_for_user` flourish (context_assembler.py:23-66, #1381);
  (2) UserPreferenceManager.get/set_reminder_timezone (IANA-validated, default
  America/Los_Angeles) — used only by standup_reminder_job.py:187;
  (3) piper_config_loader standup timing timezone (file config). Plus Slack workspace tz
  (spatial_mapper.py:130). parse_relative_date's user_timezone param: dead (never passed;
  sole caller intent_service.py:5622 omits it).
- 08:07 — Dispatched 3 Explore agents: DISPLAY sites, COMPARISON/parse-anchor sweep,
  user-tz infra corroboration.
- 08:59 UTC probe (TZ=UTC, lead venv python) CONFIRMS root finding: "at 4:30pm today"
  → 16:30Z = 9:30 AM PT (fires 7h early); "9:41am today" honest-ask fires while time is
  still in user's future; "in two hours" correct instant, UTC face unlabeled (#1535);
  calendar "today" = UTC day boundaries. Probe: scratchpad/tz_probe.py.
- 08:12 — Sweep agents 2+3 returned. Headlines beyond my direct findings:
  (a) UserPreferenceManager is IN-MEMORY only (user_preference_manager.py:195) — the
  reminder-tz preference has NO production writer and always returns the
  America/Los_Angeles default; even google_calendar_adapter.py:494-512's "per-user"
  day boundary is really the hardcoded default for everyone.
  (b) LIVE bug: context_assembler.py:124-125 naive now vs aware due_date → TypeError
  swallowed at :1048-1050 → pending_todos block silently dropped from floor context
  for any user with a due-dated todo (same shape as #1491 v30, one function over).
  (c) Naive residual: 233 naive datetime.now() sites / 62 files (most in-memory-safe);
  utcnow() down to 3 sites in slack/oauth_handler.py (self-consistent naive-UTC pair).
  (d) TWO different "today"s inside google_calendar_adapter (user-tz-ish vs server).
  (e) document_service.py "yesterday" = rolling 24h window, not calendar day; two
  functions default differently (:241 last week vs :352 yesterday).
  (f) No tz column in any of 79 migrations; browser-tz capture ABSENT; Slack users.info
  tz fields never read; parse_relative_date user_timezone param dead (0/2 callers).
- 08:20 — Display sweep returned: 50 render sites classified — 13 UTC/server unlabeled,
  10 raw ISO, 1 UTC-labeled, 3 config-tz labeled, 23 browser-local correct. All four
  seed incidents located exactly (todo_handlers.py:265 = #1535; todos.html:233 raw ISO;
  todo_handlers.py:425 = #1521 "3:00 PM UTC"; standup.py:339/404/468 naive strftime).
  Corrected the brief's issue mapping: #1521 is the reminder LIST query (closed 8/9),
  NOT the standup anchor — verified via action_registry.py:127 + lead log 8/9. The
  standup/agenda UTC anchor has no issue number → new-issue list.
- 08:25 — Verified F5 swallow (context_assembler.py:1048-1050) and todos.html:233 raw
  render at first hand before committing (m-44: not on subagent testimony alone).
- 08:27 — Wrote docs/internal/operations/time-handling-audit-2026-08-10.md (root cause:
  per-user tz supply 0% / consumption ~80% built → five improvised clocks; F1-F7 ranked;
  bare-clock answer: roll is legitimate only on the user's clock and visibly labeled;
  canonical model: capture→store UTC→parse user-tz→display user-tz labeled→compare aware;
  7 new-issue titles for Lead). Committed locally (no push per constraints).

## Discovered issues filed
None filed (no `gh` per constraints) — 7 new-issue titles listed in the audit doc for
Lead to file; F5 (deadline-proximity TypeError swallow) flagged urgent.

## Memory & briefing surfaces referenced this session
- **Referenced**: CLAUDE.md (m-43/m-44 discipline, evidence rules, env-stripped probe
  guidance, session-log protocol); principal-dropping-audit-2026-08-08.md +
  status-truth-audit-2026-08-09.md (format/method template);
  feedback_verify_at_the_right_layer (drove first-hand F5 verification);
  feedback_no_superlatives_without_verification (denominator phrasing).
- **Loaded but not referenced**: memory index bulk; mailbox/worktree discipline sections
  (no mailbox writes this session); Amber hooks investigation.
- **Wanted but not found**: an in-repo issue-body mirror for #1521/#1535/#1562 (no `gh`
  allowed — reconstructed from code comments and dev logs; adequate but slow).

## Wrap
Working tree: audit doc + this log committed locally on worktree branch. No push, no
mailbox writes, no `gh`, no code changes — per constraints. Probe script in scratchpad
(session-ephemeral, intentionally not committed).
