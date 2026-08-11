# Session Log — 2026-08-10 19:21 PDT — Coding Agent (prog), first-contact + greeting diagnosis

**Role**: Coding Agent (prog)
**Model**: claude-opus-5
**Worktree**: `/Users/xian/Development/piper-morgan-product/.claude/worktrees/agent-a5e5b2b42a6f63b5e` (branch `worktree-agent-a5e5b2b42a6f63b5e`)
**Constraints**: commit locally only; NO push, NO `mailboxes/`, NO `gh`.

## Assignment

Diagnose two defects observed by PM at 19:08 PT (02:08Z) against v48 on Fly:

- **A** — the #1536 first-contact demonstration block did not appear.
- **B** — the calendar greeting claimed a clear day (PM has 4 events) and rendered
  "focus time between 2:09 am and 6:00 pm".

## Evidence gathered

### Deployment / observability

- `fly status -a piper-morgan` → machine `2869e7ec495248`, **version 48**, last updated
  `2026-08-11T02:03:23Z`. PM's test at 02:08–02:09Z is on v48. Fly machines run **UTC**.
- `fly logs -a piper-morgan --no-tail` → 100-line buffer covering 02:08:37Z–02:11:56Z
  (saved to scratchpad). Log level: `main.py:75` sets stdlib root to **WARNING** in
  non-verbose mode, and structlog uses `structlog.stdlib.filter_by_level` +
  `LoggerFactory` (`services/infrastructure/logging/config.py:18-33`), so it inherits
  the same threshold. **INFO lines are not observable in production logs; WARNING and
  above are.** (m-43: naming the layer I could actually measure.)

### A — which gate fired

Repeated at 02:08:37Z (x4), 02:08:45Z (x4), 02:11:56Z (x2):

```
GitHub general-query: no repo could be resolved
(no user default_repo, no PIPER_DEFAULT_REPO env var). Returning empty result. (Issue #1042)
```

Source: `services/integrations/github/github_integration_router.py:536` — a
`logger.warning` inside `except UnresolvedRepoError` in `_resolve_default_repo`.

Each burst immediately precedes `GET /api/v1/radar ... 200 OK` from PM's client
(172.16.25.2). The Radar work-item path is
`radar.py:_build_feed → feed_factory.WorkItemProvider.list_for_user`, which at
`services/radar/feed_factory.py:92` returns `[]` **before** constructing the router
unless `IntegrationStatusService().is_configured(user_id, "github")` is True.

Therefore, for the account PM tested, in the same minute as the greeting:

1. `is_configured(user_id, "github")` → **True** (gate 2 passes; proven by the fact
   that the resolver warning is only reachable past that early return).
2. `resolve_repo(user_id=…)` → **raises `UnresolvedRepoError`** (gate 3 fires).

`first_contact._compute_first_contact_github` makes the *same* `resolve_repo` call and
returns `None` on `UnresolvedRepoError` → `gather_first_contact_demo` returns `{}` →
`render_first_contact_block(None)` → `""` → no demo block.

**Gate 3 confirmed. Gates 2 and 4 eliminated. Gate 1 not eliminable from logs** (its
only log line, `first_contact_newness_check_error`, is a WARNING and is *absent*, which
rules out the exception path but not a plain `False`); tested directly instead — see
below.

### B — window, timezone, and the two sub-defects

- `conversation_handler._get_calendar_summary` calls
  `calendar_router.get_temporal_summary()` **with no user_id**, and
  `CalendarIntegrationRouter.get_temporal_summary` (unlike its sibling
  `get_todays_events`) does **not** fall back to `self._user_id`. So the adapter runs
  with `user_id=None`.
- `google_calendar_adapter.get_todays_events` → `_get_user_timezone(None)` → the
  hardcoded fallback **`America/Los_Angeles`**. Day window = local midnight→midnight in
  that zone, converted to UTC for the API.
  **So the events window was NOT a UTC-day window** — the hypothesis in my brief is
  refuted. On 2026-08-10 at 19:09 PT the window was Aug 10 00:00–24:00 PT, which does
  contain all four of PM's events.
- `get_free_time_blocks` uses a **third** clock: `datetime.now().astimezone()` =
  **server-local = UTC on Fly**, and its no-meetings branch returns
  `now → now.replace(hour=18)`. That is 02:09Z → 18:00Z. `_format_time` renders the
  bare clock face → **"2:09 am" and "6:00 pm"**. Exact match to PM's copy, and 02:09Z
  is the timestamp of the `POST /api/v1/intent` that produced the greeting.
- The free-block sentence only appears via that no-meetings branch, so
  `get_todays_events` returned **[]** for that call. `get_todays_events` returns `[]`
  identically for circuit-open, auth failure, and any exception — indistinguishable
  from a genuine zero. `get_temporal_summary` then reports
  `stats.total_meetings=0, success=True`, and `_build_calendar_narrative` asserts
  **"a clear day ahead"** from it. That is the m-44 / #1425 defect.

### A — direct execution (the part logs could not settle)

`is_first_exchange` returns True or False with no WARNING either way, so the log
cannot distinguish "fresh conversation" from "already had turns". Probed the real
code with a realistic fixture (`scratchpad/gate_probe.py`, `is_configured`→True,
`resolve_repo`→`UnresolvedRepoError`):

```
GATE1 is_first_exchange(fresh conversation) = True
GATE2 is_configured awaited: 1x -> True
GATE3 resolve_repo awaited: 1x -> UnresolvedRepoError
RESULT demo_block = ''  (empty => no demonstration appended)
first_contact_no_repo_resolved  ... "level": "info"
```

The last line is the corroboration that matters: the no-repo path logs at **INFO**,
so its absence from the production log is *expected*, not counter-evidence.

**What I could not eliminate**: whether gate 1 passed on PM's specific request.
Gate 1 short-circuits before gate 3, so if it had returned False the demo would
have been skipped one step earlier and left no trace. Circumstantially it passed
(`GET /?new=1` at 02:08:44Z, `POST /api/v1/conversations` at 02:08:45Z, then the
greeting turn at 02:09:02Z — a conversation created 17 seconds before its first
message). Either way, gate 3 is *sufficient*, present, and confirmed for this
account: fixing gate 1 alone would not have produced a demonstration.

## Fixes

Two-sided honesty fix + one plumbing fix; the full per-user timezone work is #1572.

1. `google_calendar_adapter.py` — `_fetch_todays_events()` returns
   `(events, established)`; `get_todays_events()` delegates (contract unchanged).
   `TemporalSummaryResult.events_read_established` + `to_dict()`.
   `get_free_time_blocks` returns `[]` on an unestablished read and drops the
   `end <= start` block. `_now_server_local()` names the server-clock seam.
2. `conversation_consciousness.py` — `_build_calendar_narrative` gates the
   *zero* claim on `events_read_established`, returns None when nothing can be
   said (no stranded attribution), and routes free blocks through
   `_format_free_block`: synthetic whole-day blocks never render, server-derived
   ones render only zone-labeled, event-derived gaps render as before. Also fixed
   the `nice!.` double-punctuation PM quoted.
3. `calendar_integration_router.get_temporal_summary` — `user_id or self._user_id`,
   matching its sibling. `conversation_handler._get_calendar_summary` passes it too.

### Test evidence

Failing-first: **14 failed, 4 passed** across the three new files before the fix
(the 4 passing were deliberate controls). After: **18 passed**. The existing
`test_greeting_with_empty_calendar` also failed as predicted — its fixture encoded
the defect; updated with the establishment flag and paired with a new test pinning
PM's actual shape.

Regression run (`-m "not llm" -p no:cacheprovider`):
`tests/unit/services/ + tests/unit/services/intent_service/ + tests/unit/services/conversation/ + tests/test_architecture_enforcement.py`
→ **7632 passed, 1 failed, 228 skipped, 14 deselected**.

The single failure is `tests/unit/services/place/test_place_service.py::TestGitHubPlace::test_github_place_has_name`
— **verified pre-existing**, not assumed: stashed my four source edits and it failed
identically at HEAD (`1 failed, 25 passed`). `services/place/` last changed under
#1042 and imports nothing I touched. Same method applied to the 6 failures in
`tests/intent/` (outside the required scope): all 6 fail identically at HEAD.

## Fire log

- 19:21 — session start, log created.
- 19:22–19:28 — evidence gathering: code read, `fly status` (v48 confirmed),
  `fly logs --no-tail`, log-level analysis, gate probe.
- 19:29–19:45 — failing-first tests, implementation, regression runs, baselining
  the pre-existing failures by stash-and-rerun.
