# Disposal record — #1499 Class 2: six unmounted routers + shadow files (2026-09-23)

**Authority**: Arch's Rule-0 ruling, 2026-09-23 —
`mailboxes/lead/read/rule-arch-to-lead-cc-pm-1863-1499-both-GO-verified-2026-09-23.md`,
replying to Lead's ask
`mailboxes/lead/sent/ask-lead-to-arch-cc-pm-1499-class-2-rule-0-six-unmounted-routers-and-the-backup-shadow-files-disposal-ruling-requested-2026-09-23.md`.
GO on all six named routers + the shadow-file sweep, conditioned on (1) extracting
`deploy_identity()` out of `staging_health.py` before deleting it, and (2) a fresh sweep at
cut time (the audit was six weeks old).

**Executed by**: Coding Agent (prog), Sonnet, dispatched by Lead. Session log:
`dev/2026/09/23/2026-09-23-1603-prog-code-1499c2-log.md`.

---

## Outcome summary (fresh sweep found the six-router premise had already shifted)

| # | Target | Outcome | Why |
|---|---|---|---|
| 1 | `services/api/health/staging_health.py` | **DELETED** (after extraction) | Router genuinely dark; `deploy_identity()` extracted first |
| 2 | `services/api/feedback_api.py` | **DELETED** | Router genuinely dark; same-prefix collision twin of a mounted router |
| 3 | `web/api/routes/loading_demo.py` | **DELETED** | Router genuinely dark, unreferenced |
| 4 | `web/api/routes/conversation_context_demo.py` | **DELETED** | Router genuinely dark, unreferenced |
| 5 | `services/api/slack_monitoring.py` | **ALREADY GONE** | Deleted 2026-08-30 in an earlier, unrelated disposal batch (`6729d39521`) — before this audit's six-week-old cut date |
| 6 | `services/integrations/slack/webhook_router.py` (`SlackWebhookRouter`) | **NOT DELETED — member strip done (2026-09-23, follow-up)** | Class is LIVE — only its FastAPI router mount was dead. Full-file deletion would have broken live Slack slash commands. A narrower follow-up (same day) stripped the confirmed-dead members while leaving the live slash-command surface untouched — 1736 → 655 lines. See below. |

Plus the six shadow files (all six deleted, see below).

**The fresh-sweep condition Arch asked for did its job**: two of the six candidates were not
what the six-week-old audit said they were. One (`slack_monitoring.py`) had already been
disposed of by a different agent in the meantime. The other (`webhook_router.py`) turned out
to carry live business logic the audit's own framing ("HTTP surface dead, handlers live via
Socket Mode, #1496") already hinted at but the ruling's action item ("GO on all six") read as
a flat instruction to delete. Both are exactly the kind of drift Rule-0's "re-verify before
cutting" step exists to catch.

---

## 1–4. The four routers actually deleted

### `services/api/health/staging_health.py` — 11 routes

Router (`staging_health_router = APIRouter(prefix="/health", ...)`) mounted by no app.
Re-verified at cut time via `tests/test_completion_ratchets.py::test_unmounted_routers_ratchet`
(still in the allowlist, still dark) and a fresh `grep -rn` for importers.

**`deploy_identity()` extraction (Arch's condition 1)**: `web/api/routes/admin.py` imports
`deploy_identity` at two live call sites — `/health` (route at `admin.py:56`, the served
health check every deploy-infra healthcheck polls) and `/api/v1/version` (`admin.py:120`, the
UI footer's version fetch). `deploy_identity()` plus its three private helpers
(`_deployed_version`, `_deployed_git_sha`, `_deployed_environment`) were moved verbatim,
docstrings included, into a new module `services/api/health/deploy_identity.py`. Both
`admin.py` import sites repointed. Verified: `tests/unit/web/api/routes/test_health_deploy_identity_1839.py`
(6 tests) and `tests/unit/web/api/routes/test_version_route_1499.py` (7 tests) — all pass
against the new module, including the cross-surface identity test
(`test_shares_deploy_identity_with_the_served_health`).

References fixed in the same pass:
- `tests/unit/web/api/routes/test_health_deploy_identity_1839.py` — docstring no longer credits
  `staging_health.py`'s module as covering the shared-helper claim (the module is gone; the
  cross-surface coverage is `test_version_route_1499.py` now).
- `tests/unit/web/api/routes/test_version_route_1499.py` — file-path citation repointed to
  `deploy_identity.py`.
- `tests/infrastructure/test_mcp_error_scenarios.py` — a docstring named
  `staging_health._check_mcp_health` as tracking the Family-6 MCP error-coverage follow-up;
  corrected to note the follow-up is still open but no longer tracked in that (deleted)
  docstring.
- `scripts/migrate_personal_data.py` — a comment cited `PIPER.md.backup-20251101` (a shadow
  file, see below) as the historical source of a hardcoded data dict; the script never reads
  that path at runtime (the data was extracted once, Nov 2025, issue #280), so no functional
  break — comment corrected to note the file's deletion and that the citation is provenance,
  not a live read.
- `docs/internal/architecture/current/web-routes-conventions.md` — the `/health` exception
  section rewritten: previously said disposal was "pending an Arch ruling"; now says deleted,
  with the extraction noted.

### `services/api/feedback_api.py` — 6 routes

Router (`feedback_router = APIRouter(prefix="/api/v1/feedback", ...)`) mounted by no app.

⚠️ **The landmine, flagged per Arch's explicit ask**: this router sat on the *exact same
prefix* (`/api/v1/feedback`) as `web/api/routes/feedback.py`'s `router`, which IS mounted
(`web/app.py:286`, `RouterInitializer.mount_router(app, "web.api.routes.feedback", "router",
"Feedback API")`). Two routers, same prefix, only one ever wired — a collision waiting to
happen if anyone had ever wired the dead one without checking. No functional overlap was
actually live (FastAPI mounts whichever is registered; only `feedback.py`'s ever was), but the
next person who "fixes" an unmounted router by mounting it would have shipped a silent route
shadow/duplicate. Confirmed no other importer of `services.api.feedback_api` exists.

### `web/api/routes/loading_demo.py` — 8 routes, `web/api/routes/conversation_context_demo.py` — 6 routes

Both pedagogical demo routers (`/loading`, `/conversation` prefixes), mounted by no app,
referenced by no template/JS. Confirmed zero non-allowlist importers of either module or its
symbols. No dedicated test files existed for either (nothing to excise).

---

## 5. `services/api/slack_monitoring.py` — already deleted, six weeks before this audit's cut

Fresh sweep found `slack_monitoring.py` does not exist. `git log --all --diff-filter=D --
"*slack*monitor*"` shows it was deleted 2026-08-30 in commit `6729d39521`
("refactor(disposal): Batch-2 family P4 — dead debugging package + unmounted
slack_monitoring rider"), an unrelated earlier disposal batch that predates the 2026-08-07
audit's cut date having any bearing here — the audit was run before that deletion and never
saw it happen. `docs/internal/development/planning/plans/pm078-tdd-implementation-plan.md`
already carries an accurate dated historical note from that prior disposal; no further doc
correction needed. Nothing to do here beyond recording that the fresh sweep is what caught it.

---

## 6. `services/integrations/slack/webhook_router.py` — NOT deleted (discovered live)

**This is the load-bearing finding of this pass.** The Lead's ask memo and Arch's ruling both
characterized `SlackWebhookRouter` as "HTTP surface dead (#1496), handlers live via Socket
Mode" — accurate framing that the ruling's action item ("GO on all six ... SlackWebhookRouter")
did not carry through into an equally scoped instruction. A full `git rm` of this file would
have deleted live production functionality:

- `services/integrations/slack/socket_mode_runner.py:124-126` **instantiates
  `SlackWebhookRouter()` live** and calls `self._slash_router._process_slash_command(payload)`
  to process `/piper`, `/standup`, and `/link` Slack slash commands arriving over Socket Mode
  (the comment at `socket_mode_runner.py:101-106` names this explicitly: *"the HTTP mount for
  SlackWebhookRouter was removed in the Oct 2025 CORE-GREAT-2D refactor... Route the
  socket-delivered payload through the existing tested `_process_slash_command`; command logic
  stays in webhook_router"*).
- `tests/test_slack_identity_binding_guard.py` pins `SLACK_CALLER_HOME =
  "services/integrations/slack/webhook_router.py"` as the **sole sanctioned caller** of
  `redeem_link_code` — a #1466 security invariant (the `/link` identity-binding guard).
  Deleting the file would have deleted the file this security test requires to exist and be
  the caller-of-record.
- `tests/unit/services/integrations/test_slack_subcommand_intents_1436.py` imports
  `SlackWebhookRouter` directly (`SlackWebhookRouter.__new__(SlackWebhookRouter)`) to test its
  subcommand-processing methods.

**What is actually dead** is narrower than "the router": `self.router = APIRouter(prefix="/slack", ...)`,
the `_register_routes()` method (registers 6 HTTP endpoints — `/webhooks/events`,
`/oauth/callback`, `/webhooks/interactive`, `/webhooks/commands`, `/oauth/authorize`,
`/webhooks/health`), the TDD-compatibility wrapper `register_webhook_routes()`, `get_router()`,
and `get_webhook_urls()`. Nothing mounts this FastAPI router (confirmed via
`tests/test_completion_ratchets.py`'s own documented KNOWN BLIND SPOT: class-scoped routers
like this one were never in that census's denominator, by design — see the comment at
`test_completion_ratchets.py:163-167`, written before this session). The class's business-logic
methods (`_process_slash_command`, `_handle_piper_command`, `_handle_standup_command`,
`_handle_link_command`, the event-processing methods, the signature-verification helpers) are
live and tested.

**Action taken**: file left untouched. No edit, no deletion. This is a hard stop per
CLAUDE.md's "Infrastructure doesn't match gameplan assumptions" STOP condition — deleting
live, security-guarded, production-serving code on the strength of a six-week-old audit's
characterization (even a broadly-accurate one) is not a call a coding agent should make
unilaterally mid-batch.

**Recommended follow-up** (not executed here — flagged for Lead/Arch to scope as its own,
smaller task): a surgical extraction removing only the confirmed-dead FastAPI mount members
(`self.router`, `_register_routes`, `register_webhook_routes`, `get_router`,
`get_webhook_urls`, and the now-unused `APIRouter`/`Request`/`JSONResponse`/`HTTPException`/
`status` imports if nothing else in the file still needs them) while keeping the class and its
live-called methods intact. This is a different, more delicate unit of work than "delete this
file" — it touches a security-invariant-guarded class — and deserves its own review pass
rather than being folded into a dark-router batch deletion.

**Member strip — done (2026-09-23, follow-up)**. Executed by a Coding Agent (prog, Sonnet,
dispatched by Lead). Full method-by-method reachability was re-derived by grepping every
member name across `services/`, `web/`, and `tests/` (not just the six FastAPI names the
paragraph above named) — the earlier framing above turned out to be too narrow in one
important way, corrected here:

**The earlier framing said the event-processing methods and signature-verification helpers
were "live and tested." They are not live. "Tested" was standing in for "live."** Every one of
`_process_event_callback` and everything under it (`_process_message_event`,
`_process_mention_event`, `_process_reaction_event`, `_process_channel_join_event`,
`_process_event_callback_with_observability`, `_unfurl_notion_refs`), plus
`handle_slack_events`, `_process_interactive_component`, `_verify_slack_signature`, and
`_compute_and_verify_signature`, has a caller set that traces back ONLY to the unmounted
`_handle_events_webhook`/`_handle_interactive_webhook` FastAPI routes or to `handle_slack_events`
itself — and `handle_slack_events` is called only by `SlackDomainService.handle_slack_events`
(`services/domain/slack_domain_service.py:58`), which in turn has ZERO callers anywhere in the
tree (`grep -rn "\.handle_slack_events\b" services/ web/ tests/` returns only its own
definition and the one dead call site). `SlackSocketModeRunner._handle_event`
(`services/integrations/slack/socket_mode_runner.py:141`) handles Socket Mode's `events_api`
envelopes entirely on its own — it talks to `intent_service.process_intent` directly and never
calls into `SlackWebhookRouter` at all. Direct unit tests existed for this whole tree
(`tests/integration/test_complete_integration_flow.py`,
`tests/integration/test_slack_spatial_adapter_integration.py`) — that is what made it look
live; a unit test calling a private method directly is not evidence of a production caller.

**Member table** (LIVE = has a real caller; DEAD = removed):

| Member | Status | Caller evidence |
|---|---|---|
| `__init__` (config_service/oauth_handler/spatial_mapper/integration_router/response_handler/spatial_adapter DI, `self.router = APIRouter(...)`, `_register_routes()`) | DEAD as written | Constructed with **zero** args everywhere live (`socket_mode_runner.py:126: SlackWebhookRouter()`) and by every surviving test fixture; none of the injected deps is read by any live method (verified: every `self.config_service`/`self.oauth_handler`/`self.spatial_mapper`/`self.integration_router`/`self.response_handler`/`self.spatial_adapter`/`self.router` reference in the file was inside a method later found dead). Replaced with no `__init__` — the class holds no instance state. |
| `_get_connector_user_id` | DEAD | Only read inside dead methods (`_verify_webhook_signature`, `_process_message_event`, `_process_mention_event`, `_process_reaction_event`, `_get_oauth_authorization_url`, `_webhook_health_check`, `_verify_slack_signature`); zero references outside the file except the deleted test. |
| `handle_slack_events` | DEAD | Sole caller `SlackDomainService.handle_slack_events` (`services/domain/slack_domain_service.py:58`) itself has zero callers. |
| `_register_routes`, `register_webhook_routes`, `get_router`, `get_webhook_urls` | DEAD | Named in Arch's original framing; confirmed no callers anywhere (`get_router`/`get_webhook_urls` had zero, `register_webhook_routes` only in the deleted `test_ngrok_webhook_flow.py`). |
| `_handle_events_webhook`, `_handle_oauth_callback`, `_handle_interactive_webhook`, `_get_oauth_authorization_url`, `_webhook_health_check` | DEAD | Bodies of the six unmounted FastAPI routes; unreachable now the routes are gone. `_get_oauth_authorization_url` independently confirmed dead by `tests/unit/web/api/routes/test_slack_oauth_route_collapse_1499.py`'s own docstring ("`webhook_router.py:184` sits on an unmounted router"). |
| `_handle_commands_webhook` | DEAD (wrapper only) | The FastAPI wrapper around `_process_slash_command` is itself unreachable — Socket Mode calls `_process_slash_command` directly (`socket_mode_runner.py:127`), bypassing this wrapper entirely. The inner call is the live/shared part; see next row. |
| `_verify_slack_signature`, `_compute_and_verify_signature`, `_verify_webhook_signature` | DEAD | Called only by the three dead HTTP handlers above (`_handle_events_webhook`, `_handle_interactive_webhook`, `_handle_commands_webhook`) and each other. Confirmed `socket_mode_runner.py` does not call any of these — Slack SDK's `SocketModeClient` handles its own auth over the websocket/app-token, no per-request HMAC check needed. |
| `_validate_event`, `_log_webhook_event`, `_collect_metrics`, `_validate_config`, `_process_event_queue`, `set_webhook_url`, `process_webhook_event` | DEAD | Zero callers anywhere except the deleted `test_ngrok_webhook_flow.py` (which mocked/tested them in isolation, several against methods/attrs — `_check_rate_limit`, `self.event_handler` — that never existed on the class at all). |
| `_process_event_callback_with_observability`, `_process_event_callback`, `_unfurl_notion_refs`, `_process_message_event`, `_process_mention_event`, `_process_reaction_event`, `_determine_emotional_valence`, `_process_channel_join_event`, `_process_interactive_component` | DEAD | Full Events-API pipeline; caller chain traces only to the two unreached entry points above. Directly unit-tested in `tests/integration/test_complete_integration_flow.py` and `tests/integration/test_slack_spatial_adapter_integration.py` (both trimmed, see below) but never called by production code. |
| `_process_slash_command` | **LIVE** | `services/integrations/slack/socket_mode_runner.py:127`: `response = await self._slash_router._process_slash_command(payload)`. |
| `_handle_piper_command`, `_handle_calendar_subcommand`, `_handle_status_subcommand`, `_handle_priority_subcommand`, `_build_help_response` | **LIVE** | Reached from `_process_slash_command`'s `/piper` branch; calendar/status/priority also directly unit-tested (`tests/unit/services/integrations/test_slack_subcommand_intents_1436.py`). |
| `_handle_standup_command`, `_resolve_todo_principal`, `_get_completed_since_yesterday`, `_get_today_priorities`, `_get_blockers` | **LIVE** | Reached from `_process_slash_command`'s `/standup` branch. |
| `_handle_link_command` | **LIVE** | Reached from `_process_slash_command`'s `/link` branch. Also the sole sanctioned caller of `redeem_link_code` per `tests/test_slack_identity_binding_guard.py` (#1466 binding invariant) — unchanged, still passes. |

**Result**: 1736 → 655 lines (1081 removed). Imports pruned to exactly what the live code uses
(`logging`, `datetime`/`timedelta`/`timezone`, `typing.Any`/`Dict`/`Optional`, `uuid.UUID`,
`sqlalchemy.select`) — every FastAPI, signature-verification, and Slack-service-DI import
(`APIRouter`, `HTTPException`, `Request`, `status`, `JSONResponse`, `hashlib`, `hmac`, `json`,
`os`, `time`, `SlackAuthFailedError`, `task_manager`, `ProcessingStage`, `SlackPipelineMetrics`,
`correlation_id`, `slack_event_id`, `SlackConfigService`, `SlackOAuthHandler`,
`SlackResponseHandler`, `SlackIntegrationRouter`, `SlackSpatialMapper`) removed as unused.

**Tests**: deleted `tests/unit/services/integrations/slack/test_ngrok_webhook_flow.py` (entirely
dead-HTTP-surface coverage: route registration, event validation, signature verification via a
positional `config_service` arg the new `__init__` doesn't have, health check, metrics, config
validation, event queueing — all against methods now removed) and
`tests/unit/services/integrations/slack/test_webhook_oauth_url_1339.py` (entirely
`_get_oauth_authorization_url` coverage). Trimmed `TestCompleteIntegrationFlow` and
`TestSpatialAdapterRegistryIntegration` out of `tests/integration/test_complete_integration_flow.py`
(kept `TestResponseHandlerIntegration`, which tests `SlackResponseHandler` directly and never
touched `SlackWebhookRouter`). Trimmed `TestWebhookRouterIntegration` out of
`tests/integration/test_slack_spatial_adapter_integration.py` (kept the adapter-only and
registry-only classes). Added
`tests/unit/services/integrations/slack/test_webhook_router_socket_mode_only_1499.py`, pinning
(a) the FastAPI surface can't silently regrow and (b) the Socket Mode → `_process_slash_command`
path still resolves and answers a real `/piper` and `/standup` payload with the #1466 identity
seam patched. `tests/test_slack_identity_binding_guard.py` passes unchanged — verbatim, no edits.

**Verification**: `tests/test_slack_identity_binding_guard.py`,
`tests/unit/services/integrations/slack/test_slash_commands.py`,
`tests/unit/services/integrations/slack/test_slack_linking_1466.py`,
`tests/unit/services/integrations/slack/test_socket_slash_transport_1496.py`,
`tests/unit/services/integrations/test_slack_subcommand_intents_1436.py`, and the new pinning
test all pass. `tests/test_completion_ratchets.py` + `tests/test_architecture_enforcement.py`:
63 passed. `scripts/run-sweep.sh smoke`: 527 passed, 1 skipped. Full collection: 14257 tests,
0 collection errors. `ruff check .` / `ruff format --check .`: clean tree-wide.
`scripts/principal_threading_lint.py`: exit 0. `scripts/check_silent_death.py --count`: 192
(matches ceiling, unchanged). Per-file mypy (`mypy-gate.ini`) on the touched file alone:
10 arg-type + 1 assignment + 1 func-returns-value (before) → 4 arg-type + 0 + 0 (after) — pure
shrinkage, 0 attr-defined/call-arg in either version. `scripts/run-sweep.sh ratchets` shrank
`mypy_arg_type`/`mypy_assignment`/`mypy_func_returns_value`/`mypy_union_attr` below their
ceilings (consistent with the deletions here) but read `mypy_attr_defined` 142 (ceiling 141) and
`mypy_call_arg` 17 (ceiling 16) — both **not attributable to this file**: the isolated per-file
check above shows `webhook_router.py` contributes zero attr-defined/call-arg errors before or
after this strip, and the full-tree gate scans all of `services/`+`web/`, not just this file.
Pre-existing drift elsewhere in the tree; reported per instructions, ceilings not edited.

---

## Shadow files — all six deleted

Per `SHADOW_FILE_ALLOWLIST` in `tests/test_completion_ratchets.py` (#1499 Class 5 / #1522):

- `config/PIPER.md.backup-20251101`
- `services/integrations/slack/webhook_router.py.security-fix-backup`
- `backup_before_phase2_20251104_104652.sql`
- `backup_before_phase2_20251104_110227.sql`
- `backup_before_phase2_20251104_110245.sql`
- `backup_before_phase2_20251104_110300.sql`

All six confirmed still tracked and present at cut time. No live code path opens any of them
at runtime (backup files by construction); the one historical-provenance citation found
(`scripts/migrate_personal_data.py`, see above) was corrected in place. `UNMOUNTED_ROUTER_ALLOWLIST`
and `SHADOW_FILE_ALLOWLIST` in `tests/test_completion_ratchets.py` are now both empty sets
(kept as typed empty sets, not removed, so a NEW dark router or shadow file fails the ratchet
loudly instead of needing a re-add).

---

## Ceiling changes (measured, `scripts/ratchet_ceilings.json`)

| Ceiling | Before | After | Measured via |
|---|---|---|---|
| `unmounted_routers` | 4 | 0 | `pytest tests/test_completion_ratchets.py -k unmounted` |
| `shadow_files` | 6 | 0 | `pytest tests/test_completion_ratchets.py -k shadow` |
| `mypy_arg_type` | 372 | 371 | `scripts/run-sweep.sh ratchets` (venv-mypy-gate) |
| `mypy_assignment` | 231 | 229 | same |
| `mypy_attr_defined` | 148 | 141 | same |
| `mypy_index` | 37 | 10 | same |
| `mypy_union_attr` | 156 | 151 | same |

The five mypy drops are attributed to the ~2,100 lines removed across the four deleted Python
modules (`staging_health.py` 1069, `feedback_api.py` 164, `loading_demo.py` 221,
`conversation_context_demo.py` 257) — deleted code cannot carry mypy debt. Attribution caveat,
stated per the ceilings file's own established discipline: this worktree had other lanes'
uncommitted work present at measurement time (`services/database/repositories.py`,
`services/intent_service/todo_handlers.py`, `services/onboarding/portfolio_service.py`,
`tests/test_architecture_enforcement.py` — none of which this disposal touched), so the exact
mypy delta is not re-isolated in a clean throwaway worktree; the direction (down, not up) and
rough magnitude are consistent with deleting ~2,100 lines of routed API code with several
loosely-typed dict/subscript patterns (`staging_health.py` in particular had many
`.get()`/dict-subscript health-check payloads). If precise per-file attribution matters later,
re-measure in a clean worktree at this commit.

---

## ⚠️ Commit-attribution incident, same worktree, same session

The ten `git rm` deletions (four Python modules + six shadow files) landed in the repository
not through a commit this agent made — this agent does not commit — but were **accidentally
swept into an unrelated commit** by whatever process staged and committed
`dev/2026/09/23/2026-09-23-0940-lead-code-log.md`:

```
commit 1eb7c946ff11069707abc2be0cbd37cc5fefb428
    docs(lead): 1758/1729 closed, 1855 dispatched — log

 backup_before_phase2_20251104_104652.sql        |    0
 backup_before_phase2_20251104_110227.sql        |    0
 backup_before_phase2_20251104_110245.sql        |    1 -
 backup_before_phase2_20251104_110300.sql        | 2254 -----
 config/PIPER.md.backup-20251101                 |  195 -
 dev/2026/09/23/2026-09-23-0940-lead-code-log.md |   13 +
 services/api/feedback_api.py                    |  164 -
 services/api/health/staging_health.py           | 1069 -----
 .../slack/webhook_router.py.security-fix-backup |  857 -----
 web/api/routes/conversation_context_demo.py     |  257 -
 web/api/routes/loading_demo.py                  |  221 -
 11 files changed, 13 insertions(+), 5018 deletions(-)
```

This is the shared-worktree hazard CLAUDE.md's "commit only own files" discipline exists to
prevent: this session had already run `git rm` on all ten paths (staging the deletions), and a
concurrent process's session-log commit — intended to touch exactly one file — evidently used a
broad staging call (`git add -A` / `git commit -a` or equivalent) that swept in this session's
already-staged deletions too. **Net effect is functionally correct** (the ten paths are
genuinely gone, as intended, on the shared branch) **but the commit message misattributes
them** to issues #1758/#1729/#1855 rather than #1499 Class 2. Flagging here per Rule 0's own
"when a sweep surprises you mid-execution, flag it in the execution memo" precedent, and
because a future `git log`/`git blame` archaeology on these paths would otherwise be misled by
the commit message. This record is the authoritative account of what actually happened and
why; no history rewrite was attempted (out of scope for a coding agent, and the commit had
already propagated into subsequent merges by the time it was noticed).

The remaining changes in this batch — the `deploy_identity.py` extraction, the `admin.py`
repoint, the test-docstring corrections, the `web-routes-conventions.md` rewrite, the
allowlist/ceiling updates, and this record itself — were made and verified AFTER that commit,
against the tree it produced, and are Lead's to commit under the correct #1499 Class 2
attribution.

---

## Verification (`Verified how:`)

- **Method**: `grep -rn` per file across `web/`, `services/`, `tests/`, `docs/`, `scripts/`
  (excluding `venv/`, `node_modules/`, `dev/`, `mailboxes/` as historical/non-live surfaces),
  plus `git log --all --diff-filter=D` for the already-deleted `slack_monitoring.py`, plus
  running each affected test file directly before and after each edit.
- **Layer**: static import/reference sweep + live test execution (real `TestClient` /
  `pytest`), not just grep — the `deploy_identity` extraction was verified by running the
  actual route tests against the new module, not just by inspection.
- **Denominator**: all six named routers + all six named shadow files re-verified at cut time
  (2 of 6 routers found to have a materially different disposal status than the six-week-old
  audit claimed: 1 already gone, 1 live-and-not-deletable); every importer/reference found by
  the sweep was fixed or explained, none left dangling.

Full gate results: `tests/test_completion_ratchets.py` + `tests/test_architecture_enforcement.py`
(63 passed), `tests/unit/web/api/routes/test_version_route_1499.py` +
`test_health_deploy_identity_1839.py` + `test_admin_cache_routes_gated_1508.py` (13 passed),
`scripts/run-sweep.sh smoke` (539 passed, 1 skipped), `scripts/run-sweep.sh ratchets` (63
passed + 5 mypy ceilings lowered as above), full collection (14,247 tests, no ImportError).
