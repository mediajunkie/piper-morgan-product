---
title: Environment Variables Reference
status: reference doc — Docs-maintained; not one of the six living core docs
owner: Documentation Management (Docs)
last_updated: 2026-09-23
last_verified: 2026-09-23
valid_from: 2026-09-23
---

# Environment Variables Reference

**Last Updated**: September 23, 2026

This document lists the environment variables most relevant to configuring, running, and
debugging Piper Morgan day to day. It is **not** an exhaustive enumeration of every variable
read anywhere in the codebase — see "Coverage note" near the bottom for the denominator and how
to regenerate the full list yourself.

**Verified against live code 2026-09-23** (#1846): every entry below was checked against an
actual `os.environ`/`os.getenv` read (or, where noted, a `feature_flags.py`-style indirection)
as of that date, not carried forward from the previous version of this doc.

---

## Ethics & Safety

### `ENABLE_ETHICS_ENFORCEMENT`

**Purpose**: Enable/disable ethics boundary enforcement

**Type**: Boolean (string "true" or "false")

**Default**: `false` (disabled for gradual rollout)

**Added**: October 18, 2025 (Issue #197)

**Verified**: `services/intent/intent_service.py:2107` — `os.getenv("ENABLE_ETHICS_ENFORCEMENT", "false").lower() == "true"`. Default and read site unchanged since the doc's last real touch.

**Usage**:

```bash
# Enable ethics enforcement
export ENABLE_ETHICS_ENFORCEMENT=true

# Disable ethics enforcement (default)
export ENABLE_ETHICS_ENFORCEMENT=false
```

**Behavior**:

- **`true`**: All requests through IntentService are checked for ethics violations
  - Harassment content blocked (HTTP 422)
  - Professional boundary violations blocked (HTTP 422)
  - Inappropriate content blocked (HTTP 422)
  - Complete audit trail logged
- **`false`**: Ethics checks skipped, all requests processed normally

**Documentation**: `docs/internal/architecture/current/ethics-architecture.md` (file confirmed present)

**Testing**:

```bash
# Test with ethics enabled
ENABLE_ETHICS_ENFORCEMENT=true python dev/2025/10/18/test-ethics-integration.py

# Test with ethics disabled
ENABLE_ETHICS_ENFORCEMENT=false python dev/2025/10/18/test-ethics-integration.py
```

*(Both test files confirmed present at this path as of 2026-09-23.)*

---

### `ENABLE_KNOWLEDGE_GRAPH`

**Purpose**: Enable/disable Knowledge Graph context enhancement

**Type**: Boolean (string "true" or "false")

**Default**: `false` (disabled for gradual rollout)

**Added**: October 18, 2025 (Issue #99 - CORE-KNOW)

**Verified**: `services/intent/intent_service.py:2177` — `os.getenv("ENABLE_KNOWLEDGE_GRAPH", "false").lower() == "true"`. Default and read site unchanged.

**Usage**:

```bash
# Enable Knowledge Graph enhancement
export ENABLE_KNOWLEDGE_GRAPH=true

# Disable Knowledge Graph enhancement (default)
export ENABLE_KNOWLEDGE_GRAPH=false
```

**Behavior**:

- **`true`**: All requests through IntentService are enhanced with Knowledge Graph context
- **`false`**: Knowledge Graph queries skipped, standard processing continues

**Testing**:

```bash
# Test with Knowledge Graph enabled
ENABLE_KNOWLEDGE_GRAPH=true python dev/2025/10/18/test-knowledge-graph-integration.py

# Test with Knowledge Graph disabled
ENABLE_KNOWLEDGE_GRAPH=false python dev/2025/10/18/test-knowledge-graph-integration.py
```

---

## Integration Configuration

**Restructured 2026-09-23** — the previous version of this section documented a pre-MCP,
uniform direct-credential model for Slack/Notion/Google Calendar. That model is no longer
accurate for all three, and it was never uniform: per `docs/internal/architecture/CONNECTORS.md`
(the living core doc that is now the canonical source of per-connector transport/grant/scope
truth — check it directly for anything not covered here), only **GitHub** actually runs over
real MCP. Calendar and Notion use adapter classes that are named as if they were MCP but are
not; Slack's chat-answering adapter is dead code, though its credentials remain live for a
different purpose. Details per connector below.

### GitHub — real MCP

**Transport**: Real MCP — calls go through the MCP SDK over streamable-HTTP to a deployed
`ghcr.io/github/github-mcp-server` sidecar (ADR-070 + Amendment A). This is the one connector
where "MCP" in the doc/code is not aspirational.

#### `GITHUB_TOKEN`

**Purpose**: GitHub personal access token
**Type**: String (starts with `ghp_` or `github_pat_`)
**Required**: Yes (for GitHub integration)
**Permissions**: repo, read:org, workflow
**Alias**: `GH_TOKEN` is accepted as a fallback in several read sites (e.g. `services/config/github_config.py:73`, `services/infrastructure/github_repo_validator.py:42`) — `GITHUB_TOKEN` takes precedence when both are set.
**Example**: `ghp_YOUR_GITHUB_TOKEN_HERE`

#### `GITHUB_MCP_SERVER_URL`

**Purpose**: URL of the GitHub MCP sidecar the backend talks to. Previously undocumented — added
2026-09-23.
**Type**: String (URL)
**Default**: `http://localhost:9100/mcp`
**Verified**: `services/mcp/consumer/github_oauth_handler.py:37`; also the target key in `services/connectors/server_ref_resolver.py:35`.

---

### Google Calendar — direct SDK, not MCP (deliberately)

**Transport**: Google API SDK direct — CONNECTORS.md calls this an "honest shim": the MCP stub's
`_server_params_for` deliberately raises `NotImplementedError` (#1220, open, not urgent). Do not
assume a `*MCP*`-sounding class name here means MCP transport.

#### `GOOGLE_CALENDAR_ID`

**Purpose**: Google Calendar ID
**Type**: String (email format, or `primary`)
**Required**: No — **corrected 2026-09-23** (previous doc said "Yes"). Falls back to the
user's PIPER.user.md `calendar_id`, then to the literal string `"primary"`.
**Verified**: `services/integrations/calendar/config_service.py:196`
**Example**: `your-calendar@group.calendar.google.com`

#### `GOOGLE_CALENDAR_TIMEOUT`

**Purpose**: Google Calendar API timeout
**Type**: Integer (seconds)
**Default**: `30`
**Verified**: `services/integrations/calendar/config_service.py:199`

#### Other real Calendar variables (previously undocumented, added 2026-09-23)

All read in `services/integrations/calendar/config_service.py`, same env-var-overrides-PIPER.user.md-overrides-default priority order as the two above:

- `GOOGLE_CLIENT_SECRETS_FILE` — path to the OAuth client secrets file; default `credentials.json`
- `GOOGLE_TOKEN_FILE` — OAuth token cache path; default `token_{user_id}.json` (user-scoped since #734)
- `GOOGLE_CALENDAR_SCOPES` — comma-separated OAuth scopes; default `https://www.googleapis.com/auth/calendar.readonly`
- `GOOGLE_CALENDAR_CIRCUIT_TIMEOUT` — circuit-breaker timeout in seconds; default `300`
- `GOOGLE_CALENDAR_ERROR_THRESHOLD` — circuit-breaker error count threshold; default `5`
- `GOOGLE_CALENDAR_CREDENTIALS` — separately read as a coarse "is Calendar configured at all" signal in `services/integrations/integration_status_service.py:168` (alongside `MCP_ENABLED`); it is not the credentials-file path itself (that's `GOOGLE_CLIENT_SECRETS_FILE` above) — don't conflate the two when debugging a "not configured" status.

---

### Notion — REST, not MCP (naming debt)

**Transport**: `notion_client` REST — CONNECTORS.md flags the adapter class as **misleadingly
named** `NotionMCPAdapter` even though it is not MCP transport; this is tracked as naming debt to
fix when the class is next touched, not a transport claim to trust from the name.

#### `NOTION_API_KEY`

**Purpose**: Notion integration token
**Type**: String (starts with `secret_`)
**Required**: Yes (for Notion integration)
**Resolution order — corrected 2026-09-23**: env var → PIPER.user.md `authentication.api_key` →
user-scoped keychain (`services/integrations/notion/config_service.py:183-194`, Issue #579/#734).
Note this is the **opposite precedence from LLM provider keys** (which check keychain before
env var — see LLM Provider Configuration below): for Notion, an env var wins over a
keychain-stored key.
**Example**: `secret_YOUR_NOTION_API_KEY_HERE`

#### `NOTION_WORKSPACE_ID`

**Purpose**: Notion workspace/page ID
**Type**: String (UUID format)
**Required**: No, default `""`
**Example**: `12345678-1234-1234-1234-123456789012`

#### `NOTION_TIMEOUT_SECONDS`

**Purpose**: Notion API request timeout
**Type**: Integer
**Default**: `30`
**Verified**: `services/integrations/notion/config_service.py:206`

#### Other real Notion variables (previously undocumented, added 2026-09-23)

- `NOTION_API_BASE_URL` — default `https://api.notion.com/v1`
- `NOTION_MAX_RETRIES` — default `3`
- `NOTION_RATE_LIMIT_RPM` — default `30`

---

### Slack — chat adapter is dead code; credentials still live for a narrower purpose

**Transport / status — restructured 2026-09-23**: per CONNECTORS.md, the Slack adapter used for
answering chat queries is a keychain-status shim with **zero importers (dead)**. That does *not*
mean the Slack env vars below are dead: socket-mode inbound (receiving Slack messages) still
exists in code and is read by `services/integrations/slack/socket_mode_runner.py`, but it is
**config-gated off by default**. The same credentials are also read by the settings/integration-
status UI (`web/api/routes/settings_integrations.py`, `services/infrastructure/config/config_validator.py`)
independent of whether the chat-answering path is live. Don't assume "the adapter is dead" means
"these vars do nothing."

#### `PIPER_SLACK_INBOUND_ENABLED`

**Purpose**: Gate for Slack socket-mode inbound listening. Previously undocumented — added
2026-09-23.
**Type**: Boolean-ish (`"1"`, `"true"`, `"yes"` = on; anything else, including unset, = off)
**Default**: off (empty string)
**Verified**: `services/integrations/slack/socket_mode_runner.py:224`

#### `SLACK_BOT_TOKEN`

**Purpose**: Slack bot OAuth token
**Type**: String (starts with `xoxb-`)
**Required**: Yes (for socket-mode inbound and integration-status/settings)
**Example**: `xoxb-YOUR-BOT-TOKEN-HERE`

#### `SLACK_APP_TOKEN`

**Purpose**: Slack app-level token
**Type**: String (starts with `xapp-`)
**Required**: Yes (for Socket Mode)
**Example**: `xapp-YOUR-APP-TOKEN-HERE`

#### `SLACK_SIGNING_SECRET`

**Purpose**: Slack request verification secret
**Type**: String
**Required**: Yes (for webhook verification)
**Example**: `YOUR-SIGNING-SECRET-HERE`

#### `SLACK_USER_TOKEN` (previously undocumented, added 2026-09-23)

**Purpose**: User-scope token (`xoxp-`) for Web API methods a bot token cannot call (e.g.
`search.messages`). Persisted as the `slack_user` keychain key after OAuth; empty when the user
hasn't granted user scopes (#1338).
**Type**: String (starts with `xoxp-`)
**Required**: No
**Verified**: `services/integrations/slack/config_service.py:44`

---

## Development & Testing

### `PYTHONPATH`

**Purpose**: Python module search path
**Type**: String (colon-separated paths)
**Required**: Yes (for running tests/scripts)
**Example**: `PYTHONPATH=/Users/xian/Development/piper-morgan`

**Note**: this is a standard Python interpreter mechanism, not something Piper's own code reads via `os.getenv` — it governs import resolution before any app code runs.

**Usage**:

```bash
# Run tests
PYTHONPATH=/Users/xian/Development/piper-morgan pytest tests/

# Run scripts
PYTHONPATH=/Users/xian/Development/piper-morgan python scripts/some_script.py
```

---

## Feature Flags

### Spatial Intelligence

All four verified 2026-09-23 against `services/infrastructure/config/feature_flags.py`. Note:
these vars are read via `FeatureFlags._get_boolean_flag(flag_name, default)`, where `flag_name`
is passed as a parameter — the literal env-var name lives in the method's docstring, not in a
directly-greppable string literal at the call site. A plain grep for `os.getenv("VAR_NAME"...)`
will miss these; check `feature_flags.py`'s docstrings directly.

#### `USE_SPATIAL_SLACK`

**Purpose**: Enable Slack spatial intelligence adapter
**Type**: Boolean
**Default**: `true`

#### `USE_SPATIAL_CALENDAR`

**Purpose**: Enable Calendar spatial intelligence
**Type**: Boolean
**Default**: `true`

#### `USE_SPATIAL_NOTION`

**Purpose**: Enable Notion spatial intelligence
**Type**: Boolean
**Default**: `true`

#### `USE_SPATIAL_GITHUB` (previously undocumented, added 2026-09-23)

**Purpose**: Whether `GitHubIntegrationRouter` uses `GitHubSpatialIntelligence` (8-dimensional
spatial analysis) as primary, vs. falling back to legacy GitHub integration
**Type**: Boolean
**Default**: `true`
**Verified**: `services/infrastructure/config/feature_flags.py` (`should_use_spatial_github`)

A parallel set of `ALLOW_LEGACY_{GITHUB,CALENDAR,NOTION,SLACK}` and
`GITHUB_DEPRECATION_WARNINGS` flags also exist in the same file for the spatial-migration
deprecation window (all default `False` except the deprecation-warnings flag, which defaults
`True`). Not given full entries here — see `feature_flags.py` directly if you need them.

### MCP (Model Context Protocol) — file search, distinct from the connector-MCP question above

**This is a different "MCP" than the GitHub/Calendar/Notion connector-transport question
covered under Integration Configuration** — it's the infrastructure-level MCP file-search
capability, not a connector's transport layer. Don't conflate the two.

#### `ENABLE_MCP_FILE_SEARCH`

**Purpose**: Enable MCP file search functionality
**Type**: Boolean
**Default**: `false`
**Status**: Experimental
**Verified**: `services/infrastructure/config/feature_flags.py` (`is_mcp_content_search_enabled`)

#### `MCP_SERVER_URL` (previously undocumented, added 2026-09-23)

**Purpose**: MCP server endpoint for the file-search capability above (infrastructure-level;
distinct from `GITHUB_MCP_SERVER_URL`, which is the GitHub connector's own MCP sidecar URL)
**Type**: String
**Default**: `stdio://./scripts/mcp_file_server.py`
**Verified**: `services/infrastructure/config/feature_flags.py` (`get_mcp_server_url`)

---

## Server Configuration

**Corrected 2026-09-23** — the previous version of this section documented bare `PORT`/`HOST`
against `python -m uvicorn web.app:app`. Per CLAUDE.md's own Critical Paths, **the entry point is
`main.py`, not `web/app.py`** — and `main.py` reads different, `PIPER_`-prefixed variable names.
Bare `PORT`/`HOST` are not read anywhere in current application code.

### `PIPER_PORT`

**Purpose**: Web server port for `main.py` (the actual entry point)
**Type**: Integer
**Default**: `8001`
**Verified**: `main.py:37`
**Usage**:

```bash
PIPER_PORT=9000 python main.py
```

**Note**: added so a second instance (skunkworks, e2e, demos) can run without colliding with the live dev server (PA request 2026-06-05 / #1145).

### `PIPER_HOST`

**Purpose**: Web server host for `main.py`
**Type**: String
**Default**: `127.0.0.1`
**Verified**: `main.py:38`

### `PIPER_BASE_URL`

**Purpose**: Overridable base URL for health checks and printed/browser URLs on deployed
(off-box) servers, where `localhost` would be silently wrong (#1324)
**Type**: String (URL)
**Default**: `http://localhost:{PIPER_PORT}`
**Verified**: `main.py:41`

### Legacy `PORT`/`HOST`-adjacent variables — `web/app.py` direct-launch path only

`services/configuration/port_configuration_service.py` reads `BACKEND_PORT`, `WEB_PORT`,
`BACKEND_HOST`, `WEB_HOST` (environment-profile-dependent: production/staging/development
defaults differ). These are only exercised if you launch `web/app.py` directly rather than
through `main.py` — a path CLAUDE.md explicitly says is not the current entry point. Documented
here for completeness in case you're debugging an older launch script, not as current guidance.

---

## Database Configuration

**Restructured 2026-09-23** — the previous version of this doc documented only `DATABASE_URL`
with an inaccurate default password. In current code (`services/database/connection.py:58-88`),
the connection string is built from individual `POSTGRES_*` variables by default, and an
explicit `DATABASE_URL` — when set — overrides that entirely (12-factor / Fly-attach path, #1278).
This is also where `POSTGRES_PORT` (cited in CLAUDE.md's own Quick Reference launch command)
actually lives; the previous version of this doc didn't mention it at all.

### `DATABASE_URL`

**Purpose**: PostgreSQL connection string — explicit override, checked first
**Type**: String (URL format)
**Required**: No — if unset, built from the `POSTGRES_*` variables below
**Verified**: `services/database/connection.py:71`, `services/database/session_factory.py:56`
**Example**: `postgresql://user:pass@host:port/database`

### `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_HOST` / `POSTGRES_PORT` / `POSTGRES_DB`

**Purpose**: Component parts used to build the connection string when `DATABASE_URL` is unset
**Defaults**: `piper` / `dev_changeme_in_production` / `localhost` / `5433` / `piper_morgan`
**Verified**: `services/database/connection.py:77-81` — **corrected 2026-09-23**: the previous
doc's example (`postgresql://piper:piper@localhost:5433/piper_morgan`) had the wrong default
password; the actual default is `dev_changeme_in_production` (matches `.env.example`).
**Note**: Piper Morgan uses port `5433` (not standard `5432`) — confirmed still real and
separately read, matching the `POSTGRES_PORT=5433` used in CLAUDE.md's server-restart command.

### `POSTGRES_SSL_MODE` / `POSTGRES_SSL_ROOT_CERT` / `POSTGRES_SSL_CERT` / `POSTGRES_SSL_KEY`

**Purpose**: TLS configuration for the Postgres connection (Issue #229 CORE-USERS-PROD)
**Default**: `POSTGRES_SSL_MODE` defaults to `prefer`; the cert-path vars are unset unless using
`verify-ca`/`verify-full`
**Verified**: `services/database/connection.py:62-88`, `.env.example`

### `ALEMBIC_DATABASE_URL` (previously undocumented, added 2026-09-23)

**Purpose**: Migration-specific override, checked before `DATABASE_URL` for Alembic runs
**Type**: String (URL format)
**Verified**: `services/database/session_factory.py:76-80`

---

## LLM Provider Configuration

**Resolution order — clarified 2026-09-23.** All four providers below resolve through
`services/config/llm_config_service.py`'s `get_api_key()`, in this order (docstring + code at
lines ~224-299 as of this verification):

1. **The current request's own resolved key** (BYOC — `services/llm/request_key.py`; header-supplied or the caller's own stored key; #1814/#1819)
2. **Keychain** (`KeychainService` — secure storage; per CLAUDE.md, this appends `_api_key` to account names automatically, so a key stored via the raw `security` CLI without that suffix is invisible to the app)
3. **Environment variable** `{PROVIDER}_API_KEY` — logged as a `warning` ("migrate to keychain for security") when used; this is a fallback path, not the primary one

This is the mechanism behind CLAUDE.md's "Restarting the server" gotcha: a Claude Code shell
exports an **empty** `ANTHROPIC_API_KEY`, which — if the server is launched from that shell
without stripping it — is read at step 3 as a present-but-empty override and produces
`APIConnectionError` even though the real key resolves fine via keychain in a clean shell. See
CLAUDE.md's Quick Reference section for the full incident and the fix (`env -u ANTHROPIC_API_KEY …`).
Not duplicated here — that section is the canonical explanation; this doc just points to it.

### OpenAI

#### `OPENAI_API_KEY`

**Purpose**: OpenAI API key
**Type**: String (starts with `sk-`)
**Required**: Yes (for OpenAI provider)
**Storage**: Keychain first, env var fallback (see resolution order above)
**Example**: `sk-YOUR_OPENAI_API_KEY_HERE`

### Anthropic (Claude)

#### `ANTHROPIC_API_KEY`

**Purpose**: Anthropic API key
**Type**: String (starts with `sk-ant-`)
**Required**: Yes (for Anthropic provider)
**Storage**: Keychain first, env var fallback (see resolution order above — and the shadowing gotcha above it)
**Example**: `sk-ant-YOUR_ANTHROPIC_API_KEY_HERE`

### Google (Gemini)

#### `GEMINI_API_KEY`

**Purpose**: Google Gemini API key
**Type**: String
**Required**: Yes (for Gemini provider)
**Storage**: Keychain first, env var fallback

### Perplexity

#### `PERPLEXITY_API_KEY`

**Purpose**: Perplexity API key
**Type**: String (starts with `pplx-`)
**Required**: Yes (for Perplexity provider)
**Storage**: Keychain first, env var fallback
**Example**: `pplx-YOUR_PERPLEXITY_API_KEY_HERE`

---

## Logging & Monitoring

### `LOG_LEVEL` — corrected 2026-09-23: not currently read by application code

**Status**: `.env.example` still lists `LOG_LEVEL=INFO`, but a repo-wide grep of
`services/`, `web/`, `main.py`, and `config/` for `LOG_LEVEL` found **no read site**. The actual
current entry point (`main.py`) sets logging level from the `--verbose` CLI flag instead
(`logging.basicConfig(level=logging.INFO, ...)` if `--verbose`, else `logging.WARNING` by
default — `main.py:67-75`), not from an environment variable. Treat the previous doc's
`LOG_LEVEL=DEBUG python -m uvicorn web.app:app` example as stale — it also assumed the
`web/app.py` direct-launch path, which is not the current entry point either.

**If you need verbose logging from `main.py`**:

```bash
python main.py --verbose
```

---

## Quick Reference

### Common Development Setup

```bash
# Minimal development setup
export PYTHONPATH=/Users/xian/Development/piper-morgan
export ENABLE_ETHICS_ENFORCEMENT=false  # Start disabled
export ENABLE_KNOWLEDGE_GRAPH=false     # Start disabled

# With integrations
export GITHUB_TOKEN="ghp_..."
export GOOGLE_CALENDAR_ID="calendar@group.calendar.google.com"
export SLACK_BOT_TOKEN="xoxb-..."
export SLACK_APP_TOKEN="xapp-..."
export SLACK_SIGNING_SECRET="..."
export NOTION_API_KEY="secret_..."

# Start server (main.py is the entry point — not web/app.py)
python main.py
```

### Production Setup

```bash
# Production environment variables
export ENABLE_ETHICS_ENFORCEMENT=true   # Enable ethics
export ENABLE_KNOWLEDGE_GRAPH=true      # Enable Knowledge Graph
export PIPER_HOST=0.0.0.0
export PIPER_PORT=8001
export DATABASE_URL="postgresql://piper:${DB_PASSWORD}@db:5433/piper_morgan"

# Integration tokens (from secure storage)
export GITHUB_TOKEN="${GITHUB_TOKEN}"
export SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN}"
# ... etc

# Start server
python main.py
```

### Testing Setup

```bash
# Test with ethics enabled
export ENABLE_ETHICS_ENFORCEMENT=true
export ENABLE_KNOWLEDGE_GRAPH=true
export PYTHONPATH=/Users/xian/Development/piper-morgan
pytest tests/ethics/ -v

# Test specific integration
export SLACK_BOT_TOKEN="test_token"
pytest tests/integrations/test_slack.py -v
```

---

## Security Notes

### Sensitive Variables

The following variables contain sensitive data and should **NEVER** be committed to version control:

- `SLACK_BOT_TOKEN`, `SLACK_APP_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_USER_TOKEN`
- `GITHUB_TOKEN` (or `GH_TOKEN`)
- `NOTION_API_KEY`
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `PERPLEXITY_API_KEY`
- `DATABASE_URL` (if it contains a password), `POSTGRES_PASSWORD`

**Storage**: Use `.env` files (gitignored) or secure secret management systems

**Keychain**: LLM provider keys and the Notion key (once migrated off env var) are resolved
through the OS keychain via `KeychainService` — see LLM Provider Configuration above for the
exact resolution order and the `_api_key`-suffix gotcha.

---

## Troubleshooting

### Variable Not Taking Effect

**Problem**: Changed environment variable but application still uses old value

**Solution**:

```bash
# Verify variable is set
echo $ENABLE_ETHICS_ENFORCEMENT

# Restart application
kill <pid>
python main.py
```

### Integration Configuration Missing

**Problem**: Integration shows as "missing" or "invalid"

**Solution**:

1. Check variable is set: `echo $SLACK_BOT_TOKEN`
2. Verify format: Slack tokens start with `xoxb-`
3. Check server logs for configuration errors
4. Restart application after setting variables

### LLM provider fails with "All configured LLM providers failed" despite a stored/keychain key

**This is a specific, previously-diagnosed footgun, not a generic auth failure** — see CLAUDE.md's
Quick Reference "Restarting the server" section for the full mechanism and fix. Short version: a
Claude Code shell exports an **empty** `ANTHROPIC_API_KEY` (plus `ANTHROPIC_BASE_URL` /
`ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_CUSTOM_HEADERS`), which shadows the real keychain-resolved
credential if you launch `main.py` directly from that shell. A plain `curl` to `api.anthropic.com`
succeeding while the server's authenticated call fails is the tell (rules out a rate limit, which
would be an HTTP 429). Fix: strip the inherited vars before launching (`env -u ANTHROPIC_API_KEY
-u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS ...`).

---

## Coverage note — this doc is not exhaustive

A full grep of the codebase for env-var reads as of 2026-09-23 surfaces well over 100 distinct
names — many are narrow per-feature timeouts/retry-limits inside integration config services,
OAuth settings-UI redirect URIs, or internal ops flags (`USAGE_CAP_*`, `DEMO_*`,
`PIPER_INVERSION_*`, `PIPER_LIST_STALENESS_DAYS`, `PIPER_SKIP_SCHEMA_VALIDATION`,
`PIPER_CREDENTIAL_STORE`, `PIPER_DEFAULT_PROVIDER`, `PIPER_EXCLUDED_PROVIDERS`,
`PIPER_FALLBACK_PROVIDERS`, `PIPER_PM_USER_ID`, `JWT_SECRET_KEY`, `REQUIRE_AUTH`,
`AUTONOMOUS_EXECUTION_ENABLED`, and several GitHub/Slack OAuth client-id/secret/redirect-URI
pairs used only by the settings UI, among others). This doc covers the ones judged most relevant
for daily dev/ops use and debugging; it does not claim to cover all of them.

To regenerate the full current list yourself:

```bash
grep -rn "os\.environ\|os\.getenv\|environ\.get" services/ web/ main.py config/ --include="*.py" -A2 \
  | grep -oE '"[A-Z][A-Z0-9_]{2,}"' | sort -u
```

**This grep misses `feature_flags.py`-style indirection** (see the Feature Flags section above)
— the literal env-var name there lives in a docstring, not a string literal at the call site.
Check `services/infrastructure/config/feature_flags.py` directly for that family.

---

## See Also

- **Connector transport/grant/scope truth (living core doc)**: `docs/internal/architecture/CONNECTORS.md` — the canonical source for what each connector actually is; check it directly for anything not reflected here yet
- **Ethics Architecture**: `docs/internal/architecture/current/ethics-architecture.md`
- **Feature Flags**: `services/infrastructure/config/feature_flags.py`
- **Configuration files**: `config/PIPER.md` (tracked, generic — what the code loads) and `config/PIPER.user.md.example` (the gitignored personal-overlay template; the real `config/PIPER.user.md` is optional and legitimately absent on a given checkout, per CLAUDE.md's Critical Paths)
- **LLM credential resolution / the ANTHROPIC_* shadowing gotcha**: CLAUDE.md, Quick Reference section

*(Removed: a "Configuration Management" archived-framework link that no longer resolves to any file in the repo — confirmed absent 2026-09-23, not moved, just gone.)*

---

**Maintained by**: Documentation Management (Docs)
**Created**: October 18, 2025
**Last Verified**: September 23, 2026 — see frontmatter `last_verified` (#1846)
