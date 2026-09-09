# Canonical Ops Recipes

Three copy-pasteable procedures that otherwise get reconstructed from tacit knowledge every
session (per MEM-EVAL corpus analysis #1272; filed as #1277). These are command patterns and
gotchas, not full docs — each links out to the fuller explanation where one already exists.

---

## 1. Restarting the app server from a Claude Code shell

**Full explanation**: CLAUDE.md, Quick Reference section (search for `ANTHROPIC_API_KEY`). Don't
duplicate that reasoning here — this is just the command.

**The command** (verified current against CLAUDE.md as of this writing):

```bash
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
  POSTGRES_PORT=5433 nohup venv/bin/python main.py > /tmp/piper-server.log 2>&1 &
```

**Why the `env -u` flags**: a Claude Code Bash shell exports `ANTHROPIC_API_KEY=` (empty) plus
`ANTHROPIC_BASE_URL` / `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_CUSTOM_HEADERS` for its own use. Launching
`main.py` directly from that shell inherits the empty key, which shadows the env-var fallback in the
credential resolution order (Keychain first, then env — `services/config/llm_config_service.py:213`)
and every LLM call fails with a connection error that masquerades as a rate limit. Full diagnosis and
the Amber-specific "Keychain entries are simply absent" wrinkle: CLAUDE.md, same callout box.

**Gotcha on Amber specifically**: stripping the env vars is necessary but may not be sufficient. If
the Keychain has no `anthropic`/`openai`/`github_token` entries under service `piper-morgan` for this
seat, the server will still fail LLM calls after a clean restart — that's an unprovisioned-credential
problem, not an env-shadowing one, and this command doesn't fix it. Provision via `KeychainService`
(see Recipe 2 below for the naming convention), not the `security` CLI.

**Sanity check the server actually came up**:

```bash
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8001/health
tail -f /tmp/piper-server.log
```

---

## 2. Integrations connect-flow map (Slack, GitHub, Notion)

Canonical status logic lives in one place: `services/integrations/integration_status_service.py`
(#1547) — read that file first if this table doesn't answer your question, it hoists the
already-correct internals of `GET /api/v1/integrations/health` (`web/api/routes/integrations.py`).
`KNOWN_INTEGRATIONS = ("github", "slack", "calendar", "notion")` there is the user-facing set; the
`Demo` plugin is structurally excluded.

All three below ultimately go through `KeychainService` (`services/infrastructure/keychain_service.py`,
service name `"piper-morgan"`). Its key-naming rule (`_get_key_name`, line 290): `{provider}_api_key`
unscoped, or `{username}_{provider}_api_key` when a `username` (user_id) is passed. **Verified from
source, not the CLAUDE.md summary** — CLAUDE.md's claim that KeychainService "appends `_api_key` to
account names automatically" checks out exactly.

| Integration | Auth pattern | Keychain / store naming | Env-var fast path | Code path |
|---|---|---|---|---|
| **Slack** | OAuth 2.0 app-install flow (bot token issued on install) | provider `"slack_bot"` → keychain entry `{user_id}_slack_bot_api_key` (or unscoped `slack_bot_api_key`) | `SLACK_BOT_TOKEN` | `services/integrations/slack/oauth_handler.py` (`SlackOAuthHandler`); ADR-058 |
| **GitHub** | **Two paths, checked in order**: (1) OAuth via a bound MCP connector (#1329/ADR-070 C) — a `ConnectorBindingRepository` row with `status == ConnectorStatusState.BOUND`; (2) legacy personal-access-token (PAT) fallback | connector binding has no keychain entry (DB-backed, `services/connectors/binding_repository.py`); PAT path uses provider `"github_token"` → keychain entry `{user_id}_github_token_api_key` | `GITHUB_TOKEN` or `GITHUB_ACCESS_TOKEN` | `services/mcp/consumer/connector.py` (`ConnectorStatusState`), `services/mcp/consumer/github_oauth_handler.py`; PAT validation in `services/integrations/github/token_validator.py` (`verify_github_token`) |
| **Notion** | Static internal-integration API key (**not OAuth** — no `oauth_handler.py` exists under `services/integrations/notion/`, confirmed by directory listing) | provider `"notion"`, stored via `UserAPIKeyService` (`services/security/user_api_key_service.py`, #1337) — DB metadata row (`UserAPIKey` table) + the actual secret still lands in `KeychainService` under the same `{user_id}_notion_api_key` naming (`UserAPIKeyService.store_user_key` calls `self._keychain.store_api_key(provider, api_key, username=user_id)` at line 198) | `NOTION_API_TOKEN` or `NOTION_API_KEY` | `services/integrations/notion/config_service.py` (`NotionConfigService`) |

`integration_status_service.py`'s `via` field distinguishes these at read time: `"oauth_binding"`
(GitHub connector), `"keychain"` (Slack, GitHub PAT, calendar), `"user_secret_store"` (Notion, via
`UserAPIKeyService`), `"env"` (any of them via the env-var fast path).

**How to verify a connection is actually live — not just that a key exists:**

The key-exists check (`get_config_status` in `integration_status_service.py`) only tells you
something is *configured*. To confirm the credential still *works*, hit the live-test endpoints —
each makes a real API call:

```bash
# Aggregate health (all integrations, cached where a test has already run) — requires a valid JWT
curl -s -H "Authorization: Bearer $TOKEN" http://localhost:8001/api/v1/integrations/health | jq

# Force a live test of one integration (actually calls the provider's API)
curl -s -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8001/api/v1/integrations/test/slack | jq
curl -s -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8001/api/v1/integrations/test/github | jq
curl -s -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8001/api/v1/integrations/test/notion | jq

# All three (plus calendar) in one call
curl -s -X POST -H "Authorization: Bearer $TOKEN" http://localhost:8001/api/v1/integrations/test-all | jq
```

Both routes require an authenticated user (`Depends(get_current_user)`) — there's no anonymous
health check. What each live test actually does, per `web/api/routes/integrations.py`:

- **Slack** (`_test_slack`, line 495): `GET https://slack.com/api/auth.test` with the stored bot
  token; `data.get("ok")` is the pass/fail signal.
- **GitHub** (`_test_github`, line 537): if OAuth-bound, reports success without a network call
  (the binding *is* the health signal per #1329); otherwise `GET https://api.github.com/user` with
  the PAT — 200 = valid, else `token_invalid`.
- **Notion** (`_test_notion`, line 450): `GET https://api.notion.com/v1/users/me` with the stored
  key — 200 = valid.

GitHub also has a narrower, dependency-free PAT-only check: `verify_github_token()` in
`services/integrations/github/token_validator.py` does the same `GET /user` call and returns
`{"authenticated": bool, "username": str|None, "error": str|None}` — useful if you want to validate
a token without going through the full router. There's also a dedicated
`GET /api/v1/settings/integrations/github/oauth-status` route (`web/api/routes/settings_integrations.py:1331`)
for the connector-binding state specifically.

**What I could not verify**: I did not find a GitHub-App-installation-token pattern anywhere in
`services/integrations/github/` or `services/mcp/consumer/` — GitHub auth here is OAuth-connector-or-PAT,
not a GitHub App installation grant. If a GitHub App flow exists elsewhere in the repo, I didn't find
it in the integrations/connectors code I searched.

---

## 3. GitHub Actions scheduling debug

### Cron syntax gotchas specific to `schedule:` triggers

- Standard 5-field cron (`min hour dom month dow`), UTC only — no timezone field. Every
  `schedule:` block in this repo is written in UTC; e.g. `.github/workflows/weekly-docs-audit.yml`
  uses `7 16 * * 1` (Mondays 16:07 UTC = 9:07am PT).
- **GitHub explicitly documents scheduled runs as best-effort** — they can be delayed or dropped
  under platform load. This is a real, documented platform property, not a bug in this repo's
  config. Don't spend time debugging workflow YAML for a symptom that's actually GitHub's scheduler
  queue.
- **This repo has lived evidence of both delay and outright no-fire**, not just the general
  disclaimer:
  - Delay: `gh run list --workflow=weekly-docs-audit.yml` shows the `7 16 * * 1` cron (16:07 UTC)
    firing anywhere from 15 minutes to **5+ hours** late across recent weeks (checked 2026-09-09:
    2026-08-31 run fired at 21:26 UTC, 5h19m after schedule).
  - Outright no-fire: `docs/internal/operations/staggered-audit-calendar-2026.md` references issue
    #1713, a real incident where both `weekly-docs-audit.yml` and `monthly-housekeeping-audit.yml`
    (both scheduled for the same Monday 9am PT slot) had zero runs 4.5 hours past their scheduled
    time, while push-triggered workflows fired normally in the same window. Confirmed via the Actions
    API directly (`gh api repos/{owner}/{repo}/actions/workflows/{id}/runs`), not just `gh run list`'s
    default view.
  - Known mitigation, not a fix: moving a cron off `:00` (e.g. `weekly-docs-audit.yml`'s commit
    `94bbdb9f6` moved `0 16 * * 1` → `7 16 * * 1` to dodge the top-of-hour stampede). #1713 shows
    this reduces but does not eliminate the failure mode.
- Multiple workflows in this repo deliberately avoid `:00`/common minutes for this reason —
  `ci-liveness.yml` uses `23 14 * * 2` with an inline comment ("off the :00 stampede").

### Checking recent runs of a specific workflow

```bash
gh run list --workflow=<workflow-file>.yml --limit 10
```

Verified working invocation against this repo, e.g.:

```bash
gh run list --workflow=ci-liveness.yml --limit 5
gh run list --workflow=weekly-docs-audit.yml --limit 8
```

Output columns: `status  conclusion  name  workflow  branch  event  run-id  duration  timestamp`.
The `event` column is the fastest way to tell trigger types apart — look for `schedule` vs
`workflow_dispatch` vs `push`.

For a lower-level view (needed when `gh run list` seems to be missing something — see the #1713
incident, where the team went to the raw API to rule out a client-side filtering artifact):

```bash
gh api "repos/<owner>/<repo>/actions/workflows/<workflow_id>/runs?status=success&per_page=1" \
  --jq '.workflow_runs[0].created_at // ""'
```

(`<workflow_id>` comes from `gh api repos/<owner>/<repo>/actions/workflows | jq '.workflows[] | {id,name}'`.)

### Telling "never fired this occurrence" apart from "fired and failed"

- **Fired and failed**: shows up in `gh run list` with `conclusion: failure` (or `cancelled`,
  `timed_out`) and a `run-id` you can inspect with `gh run view <run-id> --log-failed`.
- **Never fired**: the expected occurrence is simply **absent** from `gh run list` output — there is
  no failed run to find, no error anywhere, nothing to click on in the Actions UI. This is the
  actually-dangerous case because it produces no signal by default; #1713 was only caught because
  someone happened to check `gh run list` directly 4.5 hours after the expected time. Confirm by
  checking the `event: schedule` runs specifically and comparing their timestamps against the cron
  expression — if the most recent `schedule` run is older than one full period, that occurrence
  didn't fire (or hasn't yet — check platform delay first before concluding it's a genuine miss).

### Related but distinct tool: `scripts/ci_liveness_check.sh`

This script (verified present, wired up in `.github/workflows/ci-liveness.yml`, weekly cron
`23 14 * * 2` + `workflow_dispatch`) answers a **different** question: "for every *active* workflow
in the repo, how long since its last **success**?" — a chronic-staleness detector, not a
this-occurrence-fired-or-not check. It flags a workflow if `age_days > MAX_AGE_DAYS` (default 10),
maintains an explicit `DORMANT_OK` allowlist-with-reasons for intentionally low-frequency workflows
(quarterly/monthly jobs), and fails loudly (exit 2) if the GitHub API itself doesn't answer — it
never reports "all clear" from a measurement that didn't run. Use it to catch "workflow has been
silently red/dead for weeks"; use the `gh run list` pattern above to debug "did this specific
Monday's occurrence fire."

---

*Referenced from CLAUDE.md's Progressive Loading table. Closes #1277.*
