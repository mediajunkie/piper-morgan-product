# Session log — Coding Agent (prog), 2026-09-23

**Role**: Coding Agent (prog)
**Model**: Sonnet (dispatched by Lead, tier stated)
**Issue**: #1499 Class 2 — `SlackWebhookRouter` member strip
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`) — no commits/pushes made; Lead reviews and commits the explicit file set below.

## Task

Follow-up to `docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md`
§6: `services/integrations/slack/webhook_router.py`'s `SlackWebhookRouter` class is LIVE
(`socket_mode_runner.py` instantiates it to process `/piper`/`/standup`/`/link` over Socket
Mode; `tests/test_slack_identity_binding_guard.py` pins it as the #1466 sanctioned caller of
`redeem_link_code`), but its FastAPI surface was mounted nowhere (#1496 retired the HTTP
webhook path). Narrow surgery: build a full member table, remove the confirmed-dead members,
keep the live slash-command tree, update tests and docs.

## What I found

Reachability grep across `services/`, `web/`, `tests/` for every member name showed the dead
surface was BROADER than the disposal record's original framing. The record said the
event-processing methods (`_process_message_event` etc.) and signature-verification helpers
were "live and tested" — they are directly unit-tested but have **zero production callers**:
their only paths in were the unmounted `_handle_events_webhook`/`_handle_interactive_webhook`
FastAPI routes, or `handle_slack_events` (itself called only by
`SlackDomainService.handle_slack_events`, which nothing calls). Socket Mode's own event
handling (`SlackSocketModeRunner._handle_event`) talks to `intent_service` directly and never
calls into `SlackWebhookRouter` at all — only the slash-command path
(`_process_slash_command`) does. "Tested" was standing in for "live."

Every `self.config_service`/`self.oauth_handler`/`self.spatial_mapper`/`self.integration_router`/
`self.response_handler`/`self.spatial_adapter`/`self.router` reference in the file traced back
to a method later found dead — so `__init__`'s entire DI setup was dead too, and the class needs
no `__init__` at all (it holds no instance state; every live method does its own local lookups).

## What shipped

- `services/integrations/slack/webhook_router.py`: 1736 → 655 lines. Removed: `self.router`/
  `APIRouter` construction, `_register_routes`, `register_webhook_routes`, `get_router`,
  `get_webhook_urls`, the six HTTP route handlers, the full Events-API pipeline
  (`_process_event_callback` + everything under it), `_verify_slack_signature`/
  `_compute_and_verify_signature`/`_verify_webhook_signature`, `_get_connector_user_id`,
  `handle_slack_events`, and the now-unused `__init__` DI wiring + imports (`APIRouter`,
  `HTTPException`, `Request`, `status`, `JSONResponse`, `hashlib`, `hmac`, `json`, `os`, `time`,
  `SlackAuthFailedError`, `task_manager`, `ProcessingStage`, `SlackPipelineMetrics`,
  `correlation_id`, `slack_event_id`, `SlackConfigService`, `SlackOAuthHandler`,
  `SlackResponseHandler`, `SlackIntegrationRouter`, `SlackSpatialMapper`). Kept verbatim:
  `_process_slash_command`, `_handle_piper_command`, `_handle_calendar_subcommand`,
  `_handle_status_subcommand`, `_handle_priority_subcommand`, `_build_help_response`,
  `_handle_standup_command`, `_resolve_todo_principal`, `_handle_link_command`,
  `_get_completed_since_yesterday`, `_get_today_priorities`, `_get_blockers`. Docstring rewritten
  to describe what the class is now and what/why was removed.
- Deleted `tests/unit/services/integrations/slack/test_ngrok_webhook_flow.py` and
  `test_webhook_oauth_url_1339.py` — exclusively dead-HTTP-surface coverage.
- Trimmed `TestCompleteIntegrationFlow` + `TestSpatialAdapterRegistryIntegration` out of
  `tests/integration/test_complete_integration_flow.py` (kept `TestResponseHandlerIntegration`,
  unrelated to `SlackWebhookRouter`).
- Trimmed `TestWebhookRouterIntegration` out of `tests/integration/test_slack_spatial_adapter_integration.py`.
- Added `tests/unit/services/integrations/slack/test_webhook_router_socket_mode_only_1499.py`
  pinning the FastAPI surface's absence and the live Socket Mode → `_process_slash_command` path.
- Updated the stale "class-scoped router" comment/allowlist note in `tests/test_completion_ratchets.py`.
- Updated the disposal record (§6, full member table + verification evidence) and
  `docs/internal/architecture/current/web-routes-conventions.md`.

## Verification

- Full named test list (slack tests, `test_slack_identity_binding_guard.py`, ratchets,
  architecture enforcement, etc.): pass, except 4 **pre-existing** failures confirmed by
  running the identical assertions against the unmodified files from `HEAD` (same failure,
  same error, before my edits): `TestResponseHandlerIntegration::test_response_handler_with_mock_dependencies`,
  `::test_response_handler_no_context_found`, `TestSlackSpatialAdapter::test_map_slack_timestamp_to_position`,
  `::test_create_spatial_event_from_slack`, `TestSpatialAdapterRegistryIntegration::test_map_through_registry`.
  Not caused by this work.
- `tests/test_completion_ratchets.py` + `tests/test_architecture_enforcement.py`: 63 passed.
- `scripts/run-sweep.sh smoke`: 527 passed, 1 skipped.
- Full collection: 14257 tests, 0 errors.
- `ruff check .` / `ruff format --check .`: clean tree-wide.
- `scripts/principal_threading_lint.py`: exit 0.
- `scripts/check_silent_death.py --count`: 192 (== ceiling, unchanged).
- Per-file mypy (`mypy-gate.ini`) on `webhook_router.py` alone: 10 arg-type + 1 assignment +
  1 func-returns-value (before, via `git show HEAD:...`) → 4 arg-type + 0 + 0 (after). Pure
  shrinkage; 0 attr-defined/call-arg in either version.
- `scripts/run-sweep.sh ratchets`: shrank arg_type/assignment/func_returns_value/union_attr
  below ceiling (consistent with the deletions). Read `mypy_attr_defined` 142 (ceiling 141) and
  `mypy_call_arg` 17 (ceiling 16) over — **not attributable to this file** per the isolated
  per-file check above (0 in both before/after); pre-existing drift elsewhere in the
  services/+web/ tree the full gate scans. Reported per instructions; `ratchet_ceilings.json`
  not edited.

**Verified how**: ran every command above in this worktree this turn and quoted its actual
output (not remembered from an earlier check); measured the touched-file mypy delta against
`git show HEAD:...` content, not the ceiling file's prose; the pre-existing-failure claims are
backed by re-running the identical test against the unmodified `HEAD` copy, not assumed.
Denominator: the full named test list in the brief, the two required enforcement suites, both
sweep tiers, full collection, tree-wide ruff (both check and format), the two script gates, and
a before/after mypy diff on the one touched service file — all run, all reported above.

## Discovered issues (report only, not filed as GH issues — flagging for Lead)

1. `services/domain/slack_domain_service.py:58` (`SlackDomainService.handle_slack_events`)
   calls `self._webhook_router.handle_slack_events(event_data)`, a method that no longer
   exists on `SlackWebhookRouter` after this strip. This is latent (nothing calls
   `SlackDomainService.handle_slack_events` either — confirmed via the same reachability grep),
   so nothing breaks today, but it's a landmine: if anything ever calls it, it's an
   `AttributeError`. Out of scope for this narrow surgery (different file, different class);
   flagging rather than fixing.
2. `services/integrations/mcp/skills/standup_workflow_skill.py:104` constructs
   `SlackDomainService()` and later calls `self.slack_service.post_message(...)` — but
   `SlackDomainService` has no `post_message` method (checked; it has `handle_slack_events`,
   `get_webhook_router`, `handle_spatial_event`, `get_response_handler`,
   `get_connection_status`, `get_service_health`). Pre-existing, unrelated to this task —
   surfaced only because I was tracing `SlackWebhookRouter`'s reachability through
   `SlackDomainService`.
3. `services/integrations/slack/tests/` (note: NOT `tests/unit/services/integrations/slack/`)
   is a stale, out-of-date duplicate test directory not collected by pytest
   (`pytest.ini testpaths = tests`) — confirmed via diff against the canonical
   `tests/unit/services/integrations/slack/` copies of `test_ngrok_webhook_flow.py` and
   `test_spatial_system_integration.py`, which have diverged. Out of scope; left untouched.

## Memory & briefing surfaces referenced this session

**Referenced**:
- `docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md` — source of the task, target of the update.
- `docs/internal/architecture/current/web-routes-conventions.md` — updated per task instructions.
- `tests/test_slack_identity_binding_guard.py` — verified unchanged/still-passing per its own stated invariant (caller-set == webhook_router.py).
- CLAUDE.md sign-off/mailbox discipline — not applicable, this session does not commit/push (Lead reviews and commits the explicit file set).

**Loaded but not referenced**: role table, worktree model sections, general session-start protocol (dispatched directly with role/log path pre-specified by Lead).

**Wanted but not found**: none — the disposal record and existing tests gave complete caller context.

## Files touched (for Lead's review/commit)

- `services/integrations/slack/webhook_router.py`
- `tests/unit/services/integrations/slack/test_ngrok_webhook_flow.py` (deleted)
- `tests/unit/services/integrations/slack/test_webhook_oauth_url_1339.py` (deleted)
- `tests/unit/services/integrations/slack/test_webhook_router_socket_mode_only_1499.py` (new)
- `tests/integration/test_complete_integration_flow.py`
- `tests/integration/test_slack_spatial_adapter_integration.py`
- `tests/test_completion_ratchets.py`
- `docs/internal/architecture/design-records/disposal-record-1499-class-2-dark-routers-2026-09-23.md`
- `docs/internal/architecture/current/web-routes-conventions.md`
