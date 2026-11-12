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
  PIPER_CREDENTIAL_STORE=db POSTGRES_PORT=5433 nohup venv/bin/python main.py > /tmp/piper-server.log 2>&1 &
```

`PIPER_CREDENTIAL_STORE=db` keeps the server out of xian's login keychain (his rule, 2026-11-11: nothing we run reads it without his permission). Provider keys come from the database store, or from a key variable you put on the command line after the `env -u` flags (which strip any inherited `ANTHROPIC_API_KEY`). If a run would need the keychain, stop and ask xian through Exec.

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

## 4. Minting an MCP server access token (#1462 unit 1)

Same operator-mint idiom as `scripts/mint_prod_invite.sh` (fixed payload committed to git, run
inside the prod container via `fly ssh console`, never a broad remote-exec permission) — see
`docs/internal/architecture/current/mcp/server-README.md` for the full identity model and
`scripts/mint_mcp_token.py`'s docstring for the DB-resolution guard.

```bash
scripts/mint_mcp_token.sh --user-email tester@example.com --label "alpha tester — claude desktop"
#   DRY RUN by default — shows the plan, writes nothing.
scripts/mint_mcp_token.sh --user-email tester@example.com --label "alpha tester — claude desktop" --apply
#   Mints one token; the raw value prints ONCE to the terminal. Deliver it the way an invite
#   token is delivered (PM ruling 2026-07-04): NEVER a mailbox memo, GH comment, or any
#   git-tracked file — in-conversation or the gitignored roster only.
```

Optional `--expires-days N` for a time-limited token. Revoke by setting `revoked_at` on the
`mcp_access_tokens` row (no script yet — direct SQL via the same `fly ssh console` pattern until
one exists).

---

*Referenced from CLAUDE.md's Progressive Loading table. Closes #1277.*

## 5. Pushing to main under contention: `scripts/push-main.sh` is the canonical wrapper (Lead, 2026-10-14)

**Why:** every seat pushes finished units to `origin/main` from its own worktree (CLAUDE.md §Git). On a busy day a plain
`git push origin HEAD:main` is rejected non-fast-forward several times an hour, and each seat was re-typing the same recovery loop by
hand. The CIO methodology audit of 2026-10-14 (R9) found five push/commit wrappers under `scripts/` with no doc. Disposition:

| script | born | verdict |
|---|---|---|
| `push-main.sh` | 2026-08-15 (Agent 360) | **canonical.** `git push origin HEAD:main`; on a race (fetch first / non-fast-forward / cannot lock ref / behind) it fetches, `git merge --no-edit origin/main`, retries, bounded (`MAX_RETRIES`, default 4). A non-race error is surfaced, never retried. A merge conflict stops it. Never force, never stash, never rebase, never checkout. |
| `safe-push.sh` | 2026-05-15 | retired. Its loop was stash → fetch → rebase → push: `git stash` is forbidden in the shared store (every worktree shares one stash stack) and a rebase of a shared branch is the wrong recovery; referenced only by May 2026 records. |
| `commit.sh` | 2025-10-15 | retired. `git add -u` stages every modified file, which the mailbox hook and the "stage in one call, your own files" rule forbid; referenced only by the P4 retrospective. |
| `pull.sh` | 2025-09-02 | retired. Not a pull: a hard-coded `git add` + commit message for PM-009. Never referenced. |
| `preserve.sh` | 2025-09-02 | retired. A one-off June 2025 preservation-branch recipe. Never referenced. |

The four retired files are in git history if a line of them is ever wanted.

**Use:** from your worktree, after committing, `scripts/push-main.sh` (or the raw command when you expect no contention; they are the
same push). Then verify on origin, whichever you used: `git fetch -q origin main && git rev-list --count origin/main..HEAD` must print
`0`. Do not decide "landed" by grepping push output for `HEAD -> main`: the rejected line carries the same text. Mail goes through
`scripts/mail-send.sh`, which has its own bounded retry; never push mailbox files with this wrapper.

**After the 2026-10-14 history rewrite:** the merge step merges the *new* `origin/main`, which is what you want. The wrapper does not
and must not merge an old branch; the pre-push guard refuses pre-rewrite history regardless.

## 6. "Is it my diff or the environment?" — the `ab-a-isolation` skill (Lead, 2026-08-15; concept recorded 2026-10-14)

**Why:** a suite that fails during your work has two candidate causes, your diff or the run's environment/history, and arguing
about it costs more than measuring it. The A/B/A experiment answers in minutes: run the failing test on **A** (your tree with the
diff set aside), **B** (your tree with the diff), then **A** again. B-only failure = your diff; A/A failure = the environment; a
flip between the two A runs = run-history (order, state, a stale container). The skill `.claude/skills/ab-a-isolation/SKILL.md`
holds the exact steps. It sets the diff aside with the tagged, apply-by-SHA stash form that the shared-stash rule allows (`git stash
push -u -m <tag>` → `git stash apply <sha>` → drop by tag), never a bare `git stash` / `stash pop`. Reach for it before you touch
code to "fix" a failure you have not attributed.

## 7. Erasing a user's account on request: `scripts/erase_user.py` (#2064, 2026-10-16)

**The promise:** /privacy says "email support@pipermorgan.ai and we'll delete your account and everything in it within
14 days". **The clock:** day 0 is the date the request email arrived; erase by day 14. **Who runs it:** xian, by hand, in
an attended session (it goes through `fly ssh console`, which asks). Agents never run the `--erase` line. Count first, then
erase with the id the count printed (`--confirm` must repeat it exactly):

```bash
fly ssh console -a piper-morgan -C "python /app/scripts/erase_user.py <email-or-username>"
fly ssh console -a piper-morgan -C "python /app/scripts/erase_user.py <email-or-username> --erase --confirm <user-id-from-the-count>"
```

All flags go inside the quotes; the prod-exec deny refuses any flag after them. The count writes nothing. It lists every
planned table, upload files, ChromaDB chunks, Redis keys, the connectors to revoke, and a live-schema census, then a
pre-flight line: `pre-flight: would erase cleanly`, or `pre-flight: would refuse at <table> (<error class>; …)`. The
pre-flight runs every database delete of the plan inside a transaction and rolls it back. If it says `would refuse`, the
erase will refuse too, with `refusing: pre-flight failed at <table> …; nothing erased anywhere`, before it touches
anything. That usually means another user's row still points at this user's data (for example their to-do in this user's
project): file it for Lead, don't work around it. The erase revokes provider grants (best effort), deletes upload files
through the storage seam, then ChromaDB chunks, then the database rows in one transaction, then Redis keys, and prints the
same counts after. Every count after should be 0. If any isn't, rerun by id (it's idempotent) and tell Lead. If the census
says `UNPLANNED`, the erase refuses: file it for Lead.

**Count again, 30 minutes later.** An access token the user already holds stays valid for up to 30 minutes after the
erase (a refresh is refused once the account row is gone, so it cannot renew), and an open tab can write rows in that
window. At least 30 minutes after the erase, run the count line again **by the user id** (the email and username no longer
resolve) and expect every count to be 0:

```bash
fly ssh console -a piper-morgan -C "python /app/scripts/erase_user.py <user-id>"
```

If any count is not 0, run `--erase --confirm <user-id>` by id again and paste both outputs into the record.

**No allow line, for either form.** Both lines stay under the ask on `fly ssh console`, by xian's hand. A prefix allow on
the count line would also match the erase line, because `--erase --confirm …` rides after the same prefix as argv (Arch,
2026-10-16).

**What to record:** a private request record (designinproduct `docs/mail/`, with `-private-` in the filename, never this
repo). It holds the date received, the due date (received + 14 days), the user id, both pasted outputs, the date erased and
who ran it, and the second count's output and time. The output carries only the id and sha256 fingerprints, never the email. Logs that Fly keeps hold fingerprints
only and are out of scope (#2064).

## 8. Invite codes: one code, one account, spent at "Create Account" (Lead, 2026-10-18)

**The lesson (xian, 2026-10-18, after three seats spent memos on a spent code):** an invite code is consumed
the moment `create-user` succeeds, by one conditional `UPDATE … WHERE used_at IS NULL`
(`services/auth/invite_token_service.py`, `consume_invite_token`). It is spent **even when the wizard then
fails** (the #2078 shape: the account exists, the code is gone, step 5 shows "Setup Failed"). A code that was
used to create any account cannot be redeemed again; the wizard says "invalid or already used invite token"
at step 3.

So, before any run that needs a fresh sign-up:

1. **Assume every saved code is spent unless its owner says otherwise.** A file in `~/.piper-shared/` with a
   mint date is not evidence the code is unused; a sign-up on or after that date with no second mint means it
   is spent.
2. **One fresh mint per fresh account.** `scripts/mint_prod_invite.sh --apply` (xian's hand, or HOST's seat
   when its rule allows); the raw value prints once; save it under a `-credential-` name so the read-deny
   covers it; HOST records the masked form (first four and last four) on the roster.
3. **Record the spend.** When a code is used, the roster line gets "spent <date> on <account label>"; the
   file can then be deleted, since it holds nothing redeemable.
4. **Agents never hold a code** (PA included): a runner is xian or Web in an isolated browser context.
5. **A masked form that reaches any seat goes to HOST the same hour**, whatever the sender says about having sent it already (2026-10-17: xian told Lead "gave to HOST" in the same breath as the masked form; HOST had nothing until the next day). Relay, then confirm the roster line exists.

Verified how: `consume_invite_token` read from source on main 2026-10-18; the 10-17 sequence (mint 16:06,
sign-up 16:09 consumed it and `/setup/complete` 403'd, file saved 16:10) reconstructed by PA from Lead's log.

## 9. Local served fault run: `scripts/served_fault_run.py` (#2232, Lead, 2026-11-11)

For a failure branch that cannot be forced on alpha (Arch, 2026-10-30: no fault switch in served code,
no forced upstream failure on the host partners use). The script starts `main.py` from the tree on a
scratch database (`piper_fault_run`, local Postgres 5433, dropped afterwards), points one upstream at a
failing stub, sends the HTTP request a browser sends, and prints the reply with the server's own log
line for the branch reached. It never touches the dev database and changes no served code.

```bash
venv/bin/python scripts/served_fault_run.py                 # every row (none needs a real LLM key)
venv/bin/python scripts/served_fault_run.py --rows 2154     # one row
```

Rows today: `2125-store` (wrong-length `ENCRYPTION_MASTER_KEY`), `2125-check` (the provider unreachable:
an HTTPS proxy stub answering 502), `2154` (SELECT on `connector_configs` revoked from the app's role),
`955` (a chat turn, "forget my clear preference", with UPDATE on `users.preferences` revoked),
`2337` (the repositories route on a connected account, same revoke as `2154`).
Two rules from Arch's 11-10 ruling hold for any database row: the app connects as a non-superuser role
(the compose role `piper` is a superuser and ignores grants), and a probe proves the denial before the
request, or the row reports NOT RUN. The layer is the local server's HTTP reply: not alpha, and not the
rendered page. Evidence goes on #2231 under the row.

A chat row runs on a scripted model (Arch, decisions.log 2026-11-11 06:55): `ANTHROPIC_BASE_URL` points
the server at a local stub, and the request carries a throwaway string in `X-User-Api-Key`. Three
conditions: the stub's answers are copied from a served trace of the same phrasing and the row cites it;
the row proves the stub was the model (no key anywhere, stub hits above 0, no request to the real
provider, no unscripted request); and the row says "routing scripted from <trace>", so nobody reads it
as a check of partner phrasing. The server runs with the mirror of alpha's live router flag kept in
`scripts/inversion_phase3_deletion_gate.py`. Where no served trace exists, the row needs a real key
through Exec instead.

The page half of `2154` (`--hold-2154 FILE` keeps the failed-read state up for a browser; deleting FILE
ends it). A settings page loads its preferences only after the provider answers (status, then the
repository or channel list), and those calls use `aiohttp` at hard-coded hosts, so no local server can
reach that state by itself. The 11-11 check scripted those two answers in the browser (an init script
wrapping `fetch` for `GET …/github` and `GET …/github/repositories`) and let every other request reach
the local server, so the 503 on `…/github/preferences` was the server's own. Say "provider legs
scripted in the browser" wherever that evidence is quoted.

A row that needs a connected GitHub account (`2337`, Arch, decisions.log 2026-11-11 10:19): the
connection is seeded by calling `persist_github_connection` with a fake grant, in a child process that
has the server's environment (never SQL; say "OAuth exchange not run" on the row), and
`GITHUB_MCP_SERVER_URL` points the server at a local MCP stub whose one tool answers the fixture
payload from `tests/unit/services/mcp/consumer/test_github_repositories_1327.py`. The row proves the
stub was the source: its tool was called with `user:@me`, every request carried the seeded grant, and
the healthy read returned the stub's list before the revoke. A connected-but-degraded connector answers
502, so the 503 is the saved-selection read. `--hold-2337 FILE` holds that state for a browser, and the
page needs no scripting (the status routes answer connected from the binding). The route's
`source=connector` info line is not emitted at the served log level, so don't cite it.

The driver starts `main.py` with `--no-browser`. Without it every server start opens a tab in the
default browser of the machine it runs on (it did, on 2026-11-11, until this was added).

Limit of the outbound sink: `aiohttp.ClientSession()` ignores the proxy environment, so the sink
neither refuses nor records those calls. It covers httpx and the Anthropic SDK only.

## 10. A step only xian can run because he holds the secrets: one command with hidden prompts (CIO, 2026-11-11, #2341)

xian, 11-11, running #2174's refresh check by hand: "I find this process super tedious and wish we could
script it all somehow so I'm not a human copy/paste machine." So a seat that needs xian to run something
with secrets only he holds (a GitHub App's client secret, a refresh token, a Fly secret, a provider key)
gives him one command instead of a list of steps with placeholders to edit. The rules for that command:

1. **It asks for each secret once, with the input hidden:** `getpass` in Python, `read -rs` in a shell
   script. It never reads them from his keychain. He types them; the keychain stays off-limits (his
   ruling of 11-11).
2. **No secret goes in argv, which `ps` shows.** It is never echoed, logged, written to a file or saved
   in shell history. A child process gets a secret through its environment or stdin.
3. **It does every step itself,** including starting and stopping helpers such as `fly proxy`, and it
   stops them on every path, failures included. If a step fails, it prints the error and stops before
   the next one.
4. **It prints one marked block to paste back,** and nothing secret is in that block. If any step ever
   prints a value the run holds, that value is replaced with `[hidden]`.
5. **If the procedure replaces a secret** (a GitHub refresh replaces the refresh token), the script
   shows the new one once, only when he answers yes, and outside the block.
6. **Unit tests pin rules 2 to 4:** no secret in argv or in the block, helpers stopped on every path,
   and a failed first step stops the run. xian's first run is the served check, and no seat can stand in
   for it.
7. **The seat that needs the result writes the script.** The issue or memo that asks xian gives him the
   one command line, and never asks him to paste a secret into a session, memo, issue or chat.
8. **He runs it in a real terminal, and the script refuses without one.** Its first line of work checks
   `sys.stdin.isatty()` (in a shell, `[ -t 0 ]`) and, if that is false, stops before any check or prompt
   with: "run this in a real terminal (Terminal.app), not through Claude Code's ! prefix". The command
   line given to him says "in Terminal". Why: the `!` prefix has no terminal, so `getpass` can't hide
   the input and warns that it "may be echoed". On 11-12 xian's first run of the second instance went
   through `!`. The first prompt got end-of-input and the run stopped with nothing typed and nothing set
   (Exec 01M78T4M9N). That was safe only by luck: a prompt that might echo must never be reached. The
   `!` prefix is still right for commands that take no secret.

First instance: `scripts/github_app_refresh_check.py` (Lead, #2341, ADR-081 D3's refresh check).
Second: `scripts/github_app_cutover_sitting.py` (Lead, #2343), section 11's sitting. It also sets Fly
secrets, which go to `fly secrets import` on standard input.

This rule does not cover how a provider key reaches a seat for its own runs. That is open with xian
through Exec (Arch, decisions.log 2026-11-11 18:43, #2340).

## 11. The GitHub App cutover sitting: register, promote, set the secrets, run the cutover (#2342, Lead, 2026-11-12)

ADR-081 D3 moves GitHub connect from the classic OAuth App to one published GitHub App. The code is on
main and does nothing until the App's two variables are set on the main app. This is the order for the
sitting in which xian turns it on. Every step is his hand. Steps 3 and 4 are one sitting, not two days
(Arch, 2026-11-12 08:28): once the secrets are set, a classic token is refused by the main app but
stays valid at GitHub, and still serves the Claude connector, until the script in step 4 has run.

**Before the sitting**

1. **Register the published App** with HOST's settings on issue 2342: the four permissions, "Expire
   user authorization tokens" on, no private key, webhook off. Callback URL, exact, one per hosted
   origin that should connect: `<origin>/api/v1/settings/integrations/github/callback`, where
   `<origin>` is that host's `PIPER_BASE_URL` (beta: `https://beta.pipermorgan.ai`). If
   `GITHUB_OAUTH_REDIRECT_URI` is set on a host, the callback is that value instead; the App and the
   classic app use the same one. No seat can read either value.
   **Settled 2026-11-12 13:12 (Arch, HOST; Lead for the source):** the owner is org `pipermorgan`,
   install scope "Only on this account", and the served rows run on a test repository in that org
   (not the product repo; the rows write). List both the beta and the alpha callback, since a host
   sends one and no seat can read which. Leave "Request user authorization (OAuth) during
   installation" and "Enable Device Flow" unticked: the callback refuses a request without our
   `state`, and device flow is unused.
2. **Promote a build that carries the code**, at or after main `7f17d1a841`. It carries the migration
   `u2342reason` (one nullable column), so it needs xian's explicit word, not the standing grant. With
   the secrets unset the build behaves as the classic app does.
   **Done 2026-11-12 11:52 PT:** beta serves `d4fd55e6c5` (run 43294075652, on xian's "Yes, promote.").
   "Beta" is the Fly app `piper-morgan`; the deploy input is still named `promote_to_alpha`.
2a. **Deploy the MCP app from main too** (PA, 2026-11-12 12:05). The MCP app (`piper-morgan-mcp`) is
   its own image and isn't moved by step 2. At 11:57 it served `28911350bb` (11-05), which has none of
   #2342's code. That build sends whatever is stored as the bearer (`Bearer {grant}` in
   `_grant_headers_or_raise`), so once one account reconnects through the App it would forward the
   whole grant record, refresh token included, the defect Lead fixed in unit 4 (`7e32d63f68`). Run
   `git fetch -q origin main && git merge -q --ff-only origin/main && scripts/deploy-mcp.sh` from a
   clean worktree, then check `https://mcp.pipermorgan.ai/health` serves a sha at or after `7e32d63f68`.
   With the App values unset it behaves as today. **Don't start step 3 until it does.**
   **Done 2026-11-12 13:12:** the MCP app serves `4666e38493` (xian's deploy; Exec's and Lead's reads).

**The sitting**

Steps 3 and 4 are one command (issue 2343). Run it in Terminal, from a clean worktree where `fly` is
signed in, never through Claude Code's `!` prefix (section 10 rule 8; it refuses without a terminal):

```
python3 scripts/github_app_cutover_sitting.py
```

It checks first (step 2a's MCP build among the checks) and changes nothing until two typed `yes` answers: one before the values are set, one
before `--apply`. It asks GitHub whether the client ID and secret belong together before setting
them. It prints one block for issue 2342. If it stops after the main app's values are set, it says so
and gives the line that finishes the job with nothing to type (`--cutover-only`). Not yet run against
the hosts by anyone; xian's first run is the check. What it does, and the by-hand form if it fails:

3. **Set the values.** On the main app (`piper-morgan`): `GITHUB_APP_CLIENT_ID`,
   `GITHUB_APP_CLIENT_SECRET`, `GITHUB_APP_SLUG`. On the MCP app (`piper-morgan-mcp`):
   `GITHUB_APP_SLUG` only (CXO, 08:28). The client ID and secret never go on the MCP app (Arch, PA;
   the note is in `fly.mcp.toml`). One alone on the main app leaves App mode off, and the startup log
   names the missing one. The client secret must not be typed into a command line or pasted into a
   session. By hand, the form that keeps it off the command line is `fly secrets import -a <app>`,
   which reads `NAME=VALUE` lines from standard input.
4. **Run the cutover, in the main app's container.** The form is the one already used for every
   script xian runs there (section 7's `erase_user.py`, the 10-18 password-reset mint): one
   `fly ssh console -a piper-morgan -C "<command>"` per run, with the script's full path, since the
   image's working directory is `/app` and it carries `scripts/` (`Dockerfile`: `WORKDIR /app`,
   `COPY . .`). Settled from that record by Lead on 2026-11-12, not a question for xian (Exec, 11:44);
   issue 2343's one command uses the same form. The three runs:
   `fly ssh console -a piper-morgan -C "python /app/scripts/github_app_cutover.py"` (a dry run: it
   prints what it would do), then the same line with `--apply` after the script name, then the dry
   run again, which should find no classic grant. None of the three carries a secret: the script
   reads the App's values from the container's environment. It prints counts and the time it ran, never a token. `--apply` is refused unless both App
   variables are set. Put the three outputs on issue 2342. A revoke that failed is counted and does not
   stop the run.
5. **Check it took.** The main app's startup log reads "GitHub connect mode: GitHub App". On beta,
   Settings, Integrations, GitHub: an account that was connected before reads CXO's cutover line and
   offers Reconnect.

**After**

6. The served acceptance rows on issue 2342 (Web's browser, PA's connector turns, CXO's judgment).
7. When they pass: widen who can install the App, and retire the classic app's client secret. Until
   then the classic `GITHUB_OAUTH_CLIENT_ID` and secret stay set, because the script's revoke and the
   disconnect of a classic grant read them.

**To turn it off again:** unset the two App variables on the main app. Connect returns to the classic
app. Accounts already moved keep their App grant, which then serves only until its access token
expires (8 hours) and cannot be refreshed; accounts the script marked stay stale until they reconnect.
So this is a way back for new connections, not an undo of the cutover.

## Promotion checklist: read staging's sha from staging, not from the deploy-run list (Lead, 2026-10-16)

**Why:** the 10:51 dispatch under the standing grant was refused by the promote gate. The gate reads the sha staging's
machines are RUNNING (`fly-deploy.yml`, "Read the image AND the sha currently running on staging"); Lead's pre-dispatch
checklist had read "staging's sha" from the newest fly-deploy push run's head. Those were different: while Tests was red on
main, the known-broken guard skipped the deploy step of each push (the run still concludes success), so staging kept
serving the last sha deployed before the red (0e30760c79), whose Tests had failed.

**Recipe:** before any dispatch, `curl -s https://piper-morgan-staging.fly.dev/health` and use its `git_sha` as the sha to
probe (`SHA=<that full sha> GITHUB_REPOSITORY=mediajunkie/piper-morgan-product bash <gate probe>`); never the run list.
After a red→green on main, remember that staging does not redeploy until a push touching deployable paths lands.

**Which paths deploy (Lead, 2026-10-19):** `fly-deploy.yml` ignores `.claude/**`, `.github/**`, `**/*.log`, `deploy/fly/**`,
`dev/**`, `mailboxes/**`, `node_modules/**`, `tests/**`, `venv/**`. So a session log, a mailbox memo, a carry-forward, a
`decisions.log` line or a test-only commit never moves staging. On 2026-10-19 Tests went green at 10:44 and ten pushes
from six seats over the next twenty minutes were all of those kinds, so staging kept serving the red build's code and the
promotion gate (rightly) refused. To move staging after a red→green, land something under `docs/` (not `*.log`),
`services/`, `web/`, `scripts/` or `alembic/`, or wait for the next such push; then re-read staging's `/health` sha.

## Google Calendar for a hosted deployment (PM ruling 2026-10-01)

The Google OAuth **app** (client ID/secret) is deployment plumbing, set once by the operator as
Fly secrets — users never configure it; they only connect their own calendar. Env wins over the
admin-UI store (`oauth_handler.py`: env > IntegrationConfigService), and the settings page hides
the app-credential card from non-admins.

```
fly secrets set -a piper-morgan \
  GOOGLE_CLIENT_ID="<id>.apps.googleusercontent.com" \
  GOOGLE_CLIENT_SECRET="<secret>" \
  GOOGLE_SETTINGS_REDIRECT_URI="https://alpha.pipermorgan.ai/api/v1/settings/integrations/calendar/callback"
```
(`GOOGLE_SETTINGS_REDIRECT_URI` is the one the Settings → Calendar "Connect" flow uses —
`settings_integrations.py:1148`. **Set it explicitly.** If it's unset, the code falls back to `PIPER_BASE_URL`, which on alpha gives `https://piper-morgan.fly.dev/…`. On 10-15, Google refused that address with `redirect_uri_mismatch` (Web's step-C run). Better: set `PIPER_BASE_URL=https://alpha.pipermorgan.ai`. Every OAuth fallback builds on it (calendar, both Slack redirects, the Slack link URL), and nothing depends on the fly.dev form (Lead, 10-15). **But an explicit per-provider redirect secret overrides it.** On 10-15, alpha held explicit `GOOGLE_SETTINGS_REDIRECT_URI`, `SLACK_REDIRECT_URI`, `SLACK_SETTINGS_REDIRECT_URI` and `GITHUB_OAUTH_REDIRECT_URI` secrets, so setting `PIPER_BASE_URL` alone left calendar on fly.dev. Check `fly secrets list` and set the provider's own variable. An earlier note here said alpha already carried the value, and that was wrong. `GOOGLE_CALENDAR_REDIRECT_URI` is the
older setup-wizard flow's; since #2043 (10-16) its default derives from `PIPER_BASE_URL` with the router's real path,
`{base}/api/v1/setup/calendar/oauth/callback` (the old default was localhost and lacked `/api/v1`), so it needs no secret;
register that URL in Google Cloud only if the wizard is in use.) The
callback URL must be listed under Authorized redirect URIs on the OAuth client in Google Cloud
Console.

**Which redirect secrets a hosted deployment still needs (Lead, 2026-10-16, after #2043):** none, provided `PIPER_BASE_URL` is the
public host and each provider's console lists the base-derived callback (GitHub settings `…/api/v1/settings/integrations/github/callback`;
Slack settings `…/api/v1/settings/integrations/slack/callback` and wizard `…/api/v1/setup/slack/oauth/callback`; calendar settings
`…/api/v1/settings/integrations/calendar/callback` and wizard as above). Every default now derives from the base. An explicit per-provider
secret (`GITHUB_OAUTH_REDIRECT_URI`, `SLACK_REDIRECT_URI`, `SLACK_SETTINGS_REDIRECT_URI`, `SLACK_SETUP_REDIRECT_URI`,
`GOOGLE_SETTINGS_REDIRECT_URI`, `GOOGLE_CALENDAR_REDIRECT_URI`) overrides the base and is the one way a flow can still point at another
host; the proposal to unset them on alpha, provider by provider, is on #1852 (xian's hand). After the restart,
Settings → Calendar shows "Connect" for every user. The admin UI path remains as a fallback for self-hosters without
env access.
