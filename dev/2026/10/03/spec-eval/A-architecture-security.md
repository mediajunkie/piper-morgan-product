# Workstream A — Architecture as found + Security/Privacy

Snapshot: product `a191856164351cf59ba033d7dbc4a34f036c6122`, code-only export `/home/user/snapshot-code` (no docs/dev/mailboxes/*.md read). Git history was used only for the secret scan.
Scripts (all in `spec-eval/metrics/`): `A-depgraph.py` (import graph, cycles, reachability, function sizes → `A-depgraph.out.json`, `A-dead.out.json`), `A-dupes.py` (duplicate basenames and identical function bodies), `A-secretscan.py` (regex secret scan of the tree and the history, values masked → `A-secretscan-tree.out`, `A-secretscan-history.out`), `A-routes.py` (static route list and auth-exempt surface → `A-routes.out`), `A-tenancy.py` (heuristic check that queries are scoped to a user → `A-tenancy-flagged.txt`).

## 1. Architecture as found (concise map)

**Size.** Production Python covers 530 modules and **191,044 LOC**: `services/` has 464 files and 164.7k LOC, `web/` has 52 files and 22.7k, `cli/` has 11 files and 3.6k. Tests are 1,115 files and 278k LOC. Scripts are 138 files and 35k LOC. The front end is about 12k LOC of JS/HTML/CSS under `web/static` and `web/templates`.

**Entry points.**
- `main.py` (442 LOC) is the CLI launcher. It runs uvicorn on `"web.app:app"` and has setup, status, preferences and rotate-key sub-modes.
- `web/app.py` and `web/startup.py` form the FastAPI app. Startup runs phased init: container, plugin discovery (filesystem scan of `services/integrations/*/*_plugin.py`), and router mounting through `RouterInitializer.mount_router("web.api.routes.X")` string imports.
- `main_mcp.py` (35 LOC) is a separate MCP server process (`services/mcp/server/app.py`, run with `fly.mcp.toml`).
- `cli/commands/*.py` are standalone scripts. Only `keys` is imported by `main.py`.
- Two more channels feed the same pipeline: Slack inbound (`socket_mode_runner.py:174`, `response_handler.py:688`) calls `IntentService.process_intent`. The Slack runner is gated by `PIPER_SLACK_INBOUND_ENABLED` (default off).

**Request path.** Middleware runs UsageCap (Redis rate limit), then Auth (deny-by-default JWT with an exempt list), then EnhancedError, then IntentEnforcement. The chat route is `POST /api/v1/intent` (`web/api/routes/intent.py:471`), which calls `IntentService.process_intent` (`services/intent/intent_service.py:801`), which calls `_process_intent_internal` (line 1207, **1,949 lines**).

**Heaviest subsystems (LOC).**

| Package | LOC |
|---|---|
| `services/intent_service` (52 files) | 38.3k |
| `web/api` | 18.7k |
| `services/integrations` | 18.5k |
| `services/intent` (one file: `intent_service.py`) | 16.7k |
| `services/mcp` | 8.6k |
| `services/mux` | 8.2k |
| `services/database` | 7.1k |
| `services/domain` | 6.4k |
| `services/infrastructure` | 5.4k |
| `services/standup` | 4.1k |
| `services/consciousness` | 3.6k |

**Intent routing alone (`services/intent` plus `services/intent_service`) is 55k LOC, 29% of all production code** and three times the size of every integration combined.

**Dependency graph** (`A-depgraph.out.json`):
- **Package level.** One strongly-connected component holds **43 packages**: essentially all of `services.*` plus `web.utils`. There is no layering at package granularity.
- **Module level.** There are 5 cycles. The largest has **46 modules**: `services.container`, `conversation_handler`, `intent.intent_service` and about 40 `intent_service.*` modules.
- **Fan-out leaders.** `services.intent.intent_service` imports 77 internal modules. Next are `canonical_handlers` (30), `settings_integrations` route (27) and `workflow_entries` (23).
- **Fan-in leaders.** `database.session_factory` (72), `domain.models` (72), `shared_types` (54), `database.models` (51), `auth.jwt_service` (31).

**Largest functions.**

| Function | Location | Lines |
|---|---|---|
| `_process_intent_internal` | `services/intent/intent_service.py` | 1,949 |
| `register_default_workflows` | `services/intent_service/workflow_entries.py` | 1,252 |
| `_format_domain_context` | `services/intent_service/conversational_floor.py` | 710 |
| `pre_classify_with_pattern_list` | `services/intent_service/pre_classifier.py` | 679 |
| `_handle_portfolio_query` | `services/intent_service/canonical_handlers.py` | 466 |

46 of 4,879 functions exceed 200 lines.

## 2. Findings

Schema: id · claim · layer · denominator · evidence · confidence · implication.

### Security and privacy (highest priority)

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| A-S1 | **Unauthenticated `POST /api/v1/setup/complete` trusts a `user_id` from the request body.** For that user it overwrites stored OpenAI, Anthropic and Notion keys (`validate=False`), the authorized-provider consent list and the default provider. It also sets `setup_complete` and mints and stores a 90-day CLI token. Anyone who knows or obtains a user's UUID can swap that user's LLM key, or deny service by planting a bad key. | static | 1 of 13 unauthenticated write routes read in full | `web/api/routes/setup.py:961-1120`. The route is exempt via the `/api/v1/setup` prefix (`services/auth/auth_middleware.py:112`), justified only by the blanket entry `"/api/v1/setup/": "setup wizard, pre-account-creation"` (line ~235). There is no session, invite or setup-state check in the handler. | high (static); live exploitability unverified | **Change now.** Require the auth cookie, or a setup-scoped token bound to the user just created by `create-user`, on every `/api/v1/setup/*` write except `create-user`. |
| A-S2 | **Unauthenticated `POST /api/v1/setup/slack-credentials` overwrites the instance-wide Slack app client_id and secret.** The authenticated sibling route exists; the auth module's own comment says the write siblings "still require auth", but this setup copy bypasses that. | static | as A-S1 | `setup.py:803-845` calls `IntegrationConfigService().store_slack_credentials(...)` with no user scope. | high | Integrity and DoS of Slack OAuth for every user. Same fix as A-S1. |
| A-S3 | **Unauthenticated `POST /api/v1/setup/projects` creates projects with `owner_id=req.user_id`.** This lets anyone inject content into another user's workspace. | static | as A-S1 | `setup.py:1171-1200` (docstring: "does NOT require JWT auth — uses user_id from the request") | high | Same fix as A-S1. |
| A-S4 | **The auth-exempt "justified writes" ratchet is satisfied by a blanket prefix**, so it did not catch A-S1 to A-S3. 42 of 255 statically found routes match the exempt list. 13 of those are write methods, and 7 of the 13 are `/api/v1/setup/*`. | static | 255 routes found by AST (decorated routers; MCP Starlette routes not covered) | `A-routes.out`; `AUTH_EXEMPT_JUSTIFIED` in `auth_middleware.py:229-262` | high | The control reports "clear" while measuring a prefix, not the routes. Require one justification entry per exact route; ban prefix keys for write methods. |
| A-S5 | **The production web app is internet-facing with no perimeter in front of it.** Fly `http_service` sets `PIPER_HOST=0.0.0.0` and `force_https`, with no Caddy or auth proxy in the Fly config. App-layer auth is therefore the whole perimeter. | static (config) | `fly.toml` and `docker-compose.yml` | `fly.toml:[env]`, `[http_service]` | med (the live topology is not observed) | Raises the severity of A-S1 to A-S3. |
| A-S6 | **A Google (Gemini) API key was committed in a public repo.** It is in `dev/2025/10/16/server-startup.log` (`AIza…9HUc`; the log line shows HTTP 200, so the key was live then). It sat at the tip from 2025-10-16 to 2026-09-24, when it was masked at the tip (`6e75d3dd`). **It is still in history.** | git-history | full `git log -p a1918561` over 31,314 commits; 14 regex families | `metrics/A-secretscan-history.out` (commits `ffa19a94`, `f0abb152`) | high that it was exposed; rotation unverified | If the key was not rotated, rotate it now. Masking the tip is not remediation. |
| A-S7 | **No other likely-real secrets were found outside tests**, in the tree or in history. The remaining "LIKELY-REAL" hits are synthetic test fixtures (`ghp_…FFFF`, `sk-t…`), a fake key in an old CI workflow, a filename false positive (`…prefix-is-sk-p…`) and committed `venv/` library code. | static, git-history | tree: all files under 3 MB; history: added lines only | `A-secretscan-tree.out`, `A-secretscan-history.out` | med | The scan is regex-based. App-specific invite codes and other bearer tokens are not covered by generic patterns (see Unobservables). |
| A-S8 | **The JWT is accepted from a `?token=` query parameter on every route**, alongside the header and cookie. URL tokens leak through access logs, history and Referer. A redactor exists for logs, but browser and Referer exposure remain. | static | 1 extractor | `auth_middleware.py:~468` (`request.query_params.get("token")`); `services/infrastructure/logging/url_redaction.py` | high | Restrict query-param tokens to the WebSocket path, or remove them. |
| A-S9 | **A hardcoded JWT dev-fallback secret exists in the public source.** Only `PIPER_ENVIRONMENT=production` refuses it. Any staging or alpha host running with another env name signs tokens with a key that anyone can read. | static | 1 | `services/auth/jwt_service.py:158-190` | med (live env name unobservable) | Fail closed whenever `JWT_SECRET_KEY` is unset outside tests. |
| A-S10 | **Encryption at rest is partial.** The AES-256-GCM/HKDF field encryption (`EncryptedString`) covers 5 columns: conversation turns (user and assistant), the conversation preview, artifact content, and the MCP client secret. About 19 other content or PII columns are plaintext. Without `ENCRYPTION_MASTER_KEY`, writes fall back to plaintext outside prod. Credentials go to the OS keyring, or to an encrypted-DB store when the keyring is dead. | static | 48 models, 36 with a user or owner column | `services/database/models.py` (5 `EncryptedString(context=…)` sites); `services/security/encrypted_types.py:96-104`; `keychain_service.py:171-212` | med | The design is sound; extend coverage to todos, lists, memory and feedback text if those count as user content. |
| A-S11 | **Multi-tenant isolation is deliberate in the repositories I sampled.** They use `owner_id` filter lists, raise `ValueError` when `owner_id` is missing, and annotate 21 exceptions with `# global-ok`. A naive heuristic flagged 95 of 207 statements on user-owned models; the 2 of 2 I sampled were false positives (filters built before the call). | static (heuristic + sample) | 207 statements; 2 hand-checked | `A-tenancy-flagged.txt`; `todo_repository.py:40-75`; `universal_list_repository.py:55-90` | low-med | Not a finding of leakage. Remaining coverage is unverified (see Unobservables). The real tenancy hole is A-S1 and A-S3: body-supplied `user_id` on unauthenticated routes. |
| A-S12 | **67 places in `web/` return `str(e)` or `{e}` to the client** in `detail=`, `message=` or `error=`, so internal error text and stack details leak to callers. | static | regex over `web/` and `services/` | grep count 81 overall, 67 in `web/` (e.g. `setup.py` complete_setup 500 path) | med | Low-severity information disclosure. Standardize on the existing `internal_error()` helper. |
| A-S13 | **Public-repo hygiene.** The tip tracks an 85 MB PostgreSQL data directory (`data/postgres/`, 2,119 files, `pg_hba.conf` set to `trust`, one SCRAM role hash, no user emails found), 4 Chroma sqlite stores, 29 `.log` files and 46 test PDFs in `uploads/`. History contains a committed `venv/` (`de126a66`). | git-history / static | full tracked list (35,840 paths) | `git ls-tree -r a1918561`; email/bcrypt byte scan of `data/postgres` (1 email-like hit, `temporal.io`; 0 bcrypt) | high | No PII found, but this is risk-shaped. `.gitignore` and `git rm --cached` would remove data dirs, logs and uploads. |
| A-S14 | **Login brute-force protection is only the generic per-IP limit** (UsageCap, 100 requests/min per principal, Redis). There is no login-specific lockout. | static | auth route and middleware | `web/middleware/usage_cap_middleware.py:7-20,50`; no attempt or lockout logic in `web/api/routes/auth.py` | med | Add a login-specific limit. Lower priority than A-S1. |
| A-S15 | **Some user content is logged at INFO**, e.g. `markdown_formatter.py:198` logs 500 characters of message text and `preference_extractor.py:144` logs the user message. | static | single-line logger calls only (9 hits) | grep | low-med | Privacy hygiene; downgrade to DEBUG or remove. |

### Architecture, routing, dead code, consistency, complexity

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| A-R1 | **Intent routing is layered accretion, not a coherent dispatcher.** `_process_intent_internal` is a single 1,949-line function with at least 25 ordered interception points before and after classification: collaboration gate, verified-inference, reminder-clear, drafted-issue, reminder time/task turns, FTUX interview, repo clarification, destructive-confirm, acceptance, standup prefs/todo-offer, early `dispatch_workflow`, guided-process, pending-resume, standup conversation, ethics boundary, conversational floor, KG enhancement, inversion-live, multi-intent inversion, `classify_multiple`/orchestrator, `classify` (pre-classifier then LLM), learning capture/suggestions, automation autoexec, floor-with-context, `canonical_handlers`, action rail, then 6 category handlers. | static | 1 function; call sites listed by grep | `intent_service.py:1251-3106` (awaited-call inventory); 614 comment lines and 110 `if`/`elif` in the function | high | Each new behavior adds an interceptor. Ordering is the real routing logic and is implicit. This is the main cost centre for change. |
| A-R2 | **Routing mechanisms counted.** 35 `*_PATTERNS` lists and 473 raw-regex literals in `pre_classifier.py` (2,808 LOC); 865 raw-string literals and 84 `re.compile` across `intent*`/`conversation`; 34 `WorkflowEntry` registrations (action rail); 71 `_handle_*` handlers (48 in `intent_service.py`); 27 `IntentCategory` members; 1 surviving `if intent.action in` chain. | static | `services/intent`, `services/intent_service`, `services/conversation` | grep counts (section 2 commands) | high (counts); med (raw strings ≠ all regex) | Pattern-based routing is the dominant mechanism; the LLM classifier is one stage among many. |
| A-R3 | **About 3.2k LOC of alternative routing is behind default-off flags**, none of which is set in `fly.toml` or `docker-compose`: `inversion_live` (1,254), `inversion_router` (685), `inversion_shadow` (460), `preclaim_shadow` (377), plus `_maybe_dispatch_multi_intent_inversion` (388) (`PIPER_INVERSION_LIVE_CATEGORIES` empty by default, `PIPER_INVERSION_SHADOW` ""). The KG enhancement (`ENABLE_KNOWLEDGE_GRAPH`, default false) is also unset in deploy config. | static | deploy configs in repo; live env unobservable | `inversion_live.py:20,190`; `intent_service.py:2234`; `fly.toml` | med | A second routing architecture is shipped dark alongside the first. Decide: promote it or delete it. Maintaining both doubles cost. |
| A-D1 | **Dead or unreachable code.** 56 production modules (**10.6k LOC**) are not reachable from any entry point by static plus string-literal imports (excluding filesystem-discovered plugins and standalone CLI scripts). 15 modules (2.0k LOC) are imported by nothing and mentioned nowhere. Notable: `integrations/slack/workspace_navigator` (809), `slack/event_handler` (540), `mux/metadata` (544), `mux/pull_mode` (484), `conversation/context_tracker` (478), `infrastructure/config/methodology_configuration` (460), two separate `spatial_intent_classifier.py` (429 + 191, both unreachable), `repositories/workflow_repository_legacy_removed` (100). `services/mux` has 15 unreachable modules (2.6k LOC). | static | 530 production modules | `metrics/A-dead.out.json`, `A-depgraph.py` | med-high (dynamic `getattr`/`__import__` beyond string literals is not modelled) | About 5.5% of production code is removable. Low risk, moderate payoff. |
| A-D2 | **Fabricated or stub endpoint.** `GET /api/v1/workflows/{id}` always returns `status:"processing"`, empty tasks and `now()` timestamps without looking anything up. It is also auth-exempt. | static | 1 | `web/api/routes/intent.py:428-462` | high | Small, but it is UI-placating fake state. Delete it or make it real. |
| A-D3 | **Duplication is mostly structural, not copy-paste.** 11 groups and 47 functions have identical bodies (530 redundant lines), mostly the per-integration `config_service`/`*_plugin` boilerplate. 22 basenames are duplicated, including 6 `models.py`, two `action_registry.py`, two `notion_adapter.py`, two `spatial_adapter.py`, two `conversation_handler.py`/`conversation_manager.py`, and the config split `services/config` vs `services/configuration` vs `services/infrastructure/config`. Persistence is split into `services/database/repositories.py` (3.1k LOC), `services/repositories/` and `services/persistence/` (the last unreachable). | static | all production files | `metrics/A-dupes.py` output | high | Parallel homes for the same concern make "where does X live" ambiguous for agents. |
| A-C1 | **Consistency.** DB access is uniformly async SQLAlchemy (496 `AsyncSession` refs; sync engines only in the migration checker, credential store and CLI). It goes through two session scopes, `session_scope` (142) and `session_scope_fresh` (98, added to work around an event-loop mismatch per call site). 9 of 31 route files execute SQL directly, bypassing repositories (e.g. raw `text("UPDATE users …")` in `setup.py`). Errors: 1,095 `except Exception`, 0 bare `except`, 27 handlers that swallow on the next line. Logging is mixed: structlog in 144 files, stdlib `logging` in 93; 677 f-string log calls vs 317 structured; 161 `print(` in `services/` and `web/`. Config: 117 distinct env vars read via `os.getenv` in 54 files, plus a `FeatureFlags` class and several config loaders. | static | all production code | grep counts (commands in this run) | high | No single convention per concern. The `_fresh` session split suggests an unresolved event-loop or engine-lifecycle bug papered over 98 times. |
| A-C2 | **TODO/FIXME density is near zero** (16 in 191k LOC), while the code carries 19.4k comment lines and **793 distinct issue references**; `intent_service.py` alone has 1,022 refs to 199 issues. | static | all production code | grep | high | The history of decisions lives in inline comments (archaeology in code). That increases read cost per change, especially for agents. |
| A-X1 | **The complexity budget is skewed to routing.** 55k LOC of intent routing against about 18.5k for every integration (GitHub, Slack, Notion, Calendar) suggests most engineering goes into deciding *what* a message means rather than into capabilities. Speculative subsystems are also present: `mux` (8.2k, 15 modules unreachable), `consciousness` (3.6k), `ethics` (2.4k; enforcement on in fly), `trust` (2.8k), `knowledge_graph` (1.1k; off by default). | static | package LOC | section 1 table | med (judgement) | Freezing interceptor growth in `process_intent` and consolidating the routing surfaces is the highest-leverage architectural change. |

## Appendix (low bearing on the guiding question)

- Plugins are discovered by filesystem scan, so `*_plugin.py` modules look unreachable statically; I excluded them from A-D1.
- All 31 `web/api/routes/*.py` modules are mounted, so there are no unmounted route files.
- CORS middleware was not found in `web/*.py`. The app is same-origin, so this is not a finding.
- Auth cookies are `httponly`, `samesite=lax`, and `secure` only on HTTPS.
- 65 of 255 routes have no route-level auth dependency and rely solely on the global middleware. This is by design (deny-by-default).

## Unobservables

| What | Why not observed | How to observe |
|---|---|---|
| Whether A-S1 to A-S3 are exploitable on the live hosts (Fly app, pipermorgan.ai) | No live probing was in scope; a proxy, firewall or different deployed commit could change this | Probe the routes against a staging copy with a test UUID; confirm the deployed commit |
| Whether user UUIDs are discoverable by an unauthenticated or other-tenant party (precondition for A-S1/A-S3) | Would need a full read of the API response surface and the front end | Grep responses and templates for `user_id`; probe with a second account |
| Whether the Google key in A-S6 was rotated or revoked | External provider state | Check the GCP console or the key's API response |
| Live env vars (`PIPER_ENVIRONMENT`, inversion flags, `ENABLE_KNOWLEDGE_GRAPH`, `ENCRYPTION_MASTER_KEY`, `JWT_SECRET_KEY`) | Fly secrets and Amber env are not in the repo | `fly secrets list`; inspect the host env |
| Application-specific bearer tokens (invite codes, reset codes) in history | Generic regexes don't match the Crockford invite format | Run `scripts/mailbox_bearer_lint.py` patterns over full history |
| Full tenancy coverage | The heuristic has a high false-positive rate; only 2 of 95 flagged statements were hand-checked | Enable SQL logging in a two-tenant integration test, or do a proper AST dataflow review of the 95 flagged statements |
| Runtime routing distribution (which of the ~25 interceptors actually fire) | Static only | Per-stage counters or traces on live traffic |
| MCP server (Starlette) route auth | `A-routes.py` parses FastAPI decorators only | Enumerate `build_asgi_app` routes |

## Pre-registered top 5

1. **Close the unauthenticated `/api/v1/setup/*` write routes** (complete, projects, slack-credentials, use-keychain and validate-key). `setup/complete` lets anyone overwrite any user's stored API keys and consent list given their UUID, on an internet-facing app (A-S1–A-S3, A-S5).
2. **Replace the prefix-based auth-exempt justification with one entry per exact route for every write**, because the current ratchet reports clear while not measuring the routes (A-S4).
3. **Confirm the Gemini key leaked in history (2025-10 to 2026-09, public repo) was rotated**, and make history-wide scans part of the bearer-credential gate (A-S6).
4. **Stop adding interceptors to the 1,949-line `_process_intent_internal`.** Resolve the dark second routing architecture (inversion/preclaim, about 3.2k LOC) by promoting or deleting it, and make stage ordering explicit (A-R1–A-R3, A-X1).
5. **Remove the JWT query-param token path and the public hardcoded JWT fallback secret, then delete the about 10.6k LOC of unreachable modules** (A-S8, A-S9, A-D1).
