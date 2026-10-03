# Workstream C — The product as built: what can a user actually do?

**Snapshot**: code from `/home/user/snapshot-code` (export of a1918561); running server at `127.0.0.1:8001` (version 0.8.14.0), Postgres 16 :5433, Redis. No LLM key, no ChromaDB, Temporal, GitHub OAuth app, Slack/Calendar/Notion OAuth, or `ENCRYPTION_MASTER_KEY`.
**Method**: code-first enumeration with scripts, then drove the running app with Playwright (Chromium) and httpx as a brand-new invitee. I read no docs, dev, mailboxes or briefings.
**Scripts / artifacts**: `spec-eval/metrics/C-*` (listed in the appendix). There are 40 screenshots in `spec-eval/metrics/C-screens/`.

> ⚠️ **Environment interference (read before trusting any DB-touching result).** Between about 18:28 and 18:30 UTC, another workstream's pytest run wiped the shared scratch DB. `invite_tokens` went from 9 to 0, and my user `evalc` disappeared from `users`. Two failures I first saw after that point (file upload and feedback POST both returned a 500 with a `users` FK violation) were caused by the wipe, not by the product. I re-created an account (`evalc3`), re-ran both, and they **worked**. They are classified below as working. Every other result here comes from before the wipe or was re-run after it.

---

## 1. Capability inventory (from code + live OpenAPI)

| Surface | Count | How counted |
|---|---|---|
| HTTP operations mounted (live) | **255 ops on 220 paths** | `GET /openapi.json` → `metrics/C-openapi-live.json` |
| Route decorators in code | 269 matches. 257 are matched live. The other 12 are 7 docstring examples (auth_middleware, container, plugin_interface, dependencies) and 5 `learning/controls/*` routes that are **commented out** | `metrics/C-routes.py` → `C-routes.txt` |
| `/api/v1/*` prefixes | 31 (biggest: settings 38 ops, setup 15, learning 9, projects 9, lists 8) | live OpenAPI |
| `/api/admin/*` (unversioned) | 8 ops (cache metrics/clear, intent monitoring). Return 403 to a normal user | live OpenAPI + GET sweep |
| HTML page routes | 29 GET pages (+ `/health`, `/health/config`) | live OpenAPI |
| Page templates | 32 top-level + 30 components. **4 top-level are never rendered by any route**: `404.html`, `500.html`, `documents.html`, `network-error.html` | grep for template name in `web/`, `services/`, `main.py` |
| Chat: pre-classifier (category, action) pairs | 56 (6 canonical / 37 workflow / 13 floor) | `ACTION_REGISTRY` → `metrics/C-action-registry.json` |
| Chat: workflow-registry keys | 144 (133 action-triggered, mostly aliases) | `register_default_workflows()` |
| **Chat: unique wired actions** | **53** | `wired_chat_actions()` (the product's own canonical list) |
| CLI | `main.py`: 6 commands (setup, status, preferences, migrate-user, keys, rotate-key). `cli/commands/`: 27 subcommands across 6 non-empty modules (cal 3, documents 5, issues 6, notion 8, personality 4, publish 1) | grep `add_parser` / `.command(` |
| MCP server (`main_mcp.py`, separate process) | 3 resources (`piper://me/profile`, `/colleague-model`, `/github/issues`) + 1 read-only tool (`what_piper_knows_about_me`). OAuth-gated | `services/mcp/server/resources.py:48-50,238` |
| Integrations | 4 user-facing in the health page (Notion, Slack, GitHub, Google Calendar). Plus local_git and MCP connections (`/settings/connected-apps`). Code dirs: calendar, github, notion, slack, local_git, mcp, spatial, demo, resolution | `services/integrations/` |

**The 53 wired chat actions, grouped by what they depend on** (my judgment from handler names and registry descriptions, medium confidence):

| Dependency | n | Actions |
|---|---|---|
| Piper DB only (could be deterministic) | 19 | create/complete/delete/list/next todo, list_todos_query, create_reminder, list_reminders_query, get_current_time, set_timezone, get/set_default_repo, list_projects, list_archived_projects, session_activity_query, show_standup, attention_query, productivity, changes_query |
| GitHub | 15 | create/update/close/reopen/comment/review issue, list issues/prs/milestones/releases/labels/branches, stale_prs, shipped_this_week, analyze_commits |
| Local git | 1 | local_git_status_query |
| Google Calendar | 3 | meeting_time, recurring_meetings, week_calendar |
| Notion | 3 | search_documents, analyze_document, update_document |
| LLM-required (generation or floor) | 12 | get_capabilities, explain_trust, get_memory, pull_insights, analyze_blockers, generate_content, generate_report, analyze_data, prioritize, strategic_planning, learn_pattern, summarize_document |

---

## 2. What happened when I ran it

### First-run narrative (new invitee, timings from `metrics/C-firstrun.py`)

1. **0 → 3.4 s**: `/` redirects to `/login`. The login page says "Have an invite code? Create your account". That's clear.
2. **4.8 s**: `/setup` opens with a friendly intro: "Hi, I'm Piper Morgan… tracking tasks, managing GitHub issues, prepping for standups, calendar".
3. **9.2 s, blocked at step 1 of 5 ("System")**. The wizard checks the server's infrastructure (Docker, PostgreSQL, Redis, ChromaDB, Temporal) and hides "Continue" unless every required service is up. ChromaDB was down here, so the only button was "Retry Check" (`fr03-step1.png`). The toast is well written: "on a hosted instance, tell the person who runs it". Still, an end user is being asked to pass an operator's infrastructure check.
4. **Step 2 is a hard gate too.** "Continue" stays `disabled` until an OpenAI or Anthropic key validates (`web/static/js/setup.js:270-278`), and step 3 is where the account actually gets created. **A new invitee without their own LLM key cannot create an account through the UI at all.** A malformed key gets a jargon-heavy message: "Key too short (minimum 100 characters for anthropic) | Key too weak: entropy 43% (required: 70%)".
5. **Workaround (legitimate dev path)**:
   - I minted a token with `scripts/mint_invite_tokens.py 1 --apply`. The script hard-codes `load_dotenv("/Users/xian/...")`, which is harmless here. The pre-existing invite tokens were not usable because their raw strings are only printed at mint time and are not readable in plaintext afterwards.
   - I then POSTed `/api/v1/setup/create-user`, the same endpoint step 3 calls. It succeeded.
   - Reusing the token was correctly refused: "Invalid or already-used invite token".
6. **Login through the UI**: worked. It lands on home: chat, a left rail of chats, and a Radar panel.
7. **First chat message ("hello")**: reply in about 2.9 s: *"Hello — good to meet you. Piper runs on an LLM key of your own… Add an OpenAI or Anthropic key in Settings."* Every later message (8 more probes) got the same sentence: *"I need an LLM key of your own before I can help…"* (`chat_after.png`).
8. **Saving a key from Settings fails in this environment.** The message is: "Keychain storage failed: No OS keyring backend AND the encrypted-DB fallback is unavailable (… #1382) — no secure credential store; refusing the operation (#1382)." This is correct to fail closed, but it shows internal issue numbers to the user. So in this deployment the chat gate can never be passed.
9. **First useful thing**: to-dos, projects, lists, work items and documents all work. They are reached through the **username dropdown at the bottom of the rail** ("Your work"), not the visible nav (`templates/components/nav_rail.html:55-65`). "Check in" (standup) is hidden until trust stage 3 (`nav_rail.html:40`). A new user who stays in chat never learns these exist, because chat refuses to tell them (see C-01).

### Page crawl (30 routes, logged in; `metrics/C-crawl.py` → `C-crawl.json`)

- **30/30 returned HTTP 200 and rendered.** Empty states are friendly (e.g. todos: "All caught up! Your todo list is clear").
- **Problems found:**
  - `/settings/integrations/github`: 502 from `/api/v1/settings/integrations/github/repositories`, shown as "I couldn't load your repositories".
  - `/personality-preferences`: uncaught page error `KeyboardShortcuts is not defined`.
  - `/`: two console "Failed to fetch" errors (conversation load and Radar). Low confidence; this may be my navigation aborting the requests.
- **Integration Health page**: a brand-new user is greeted with a red ❌ "Multiple Issues — 0 of 4 integrations healthy" and a "Disconnect All" button. GitHub shows "Status: unknown" with **Disconnect** and **Test** buttons even though this user never connected GitHub. The server process has a `GITHUB_TOKEN` env var; the cause was not traced (unverified).
- **Dead links**: 30 unique internal hrefs; none dead. `/login` returns 302 when logged in, which is expected. `/docs` (Swagger) is linked from the learning dashboard and is reachable **unauthenticated**.
- **Unknown URL**: returns raw JSON `{"detail":"Not Found"}`. The 404/500/network-error templates exist but are never served.

### Non-LLM features run end-to-end

| Feature | UI | API | Result |
|---|---|---|---|
| Todos | Create via dialog → visible after reload | create / get / complete / delete OK | works. API `PUT` with a JSON body returns 200 and **silently changes nothing**: the route takes query params. The client works around this (`templates/todos.html:474-476` comment) |
| Projects | Create → visible after reload | CRUD OK. Same silent-PUT behavior | works |
| Lists + items | Create → visible after reload | list / items OK | works |
| Work items | page renders | create / list OK | works |
| Sharing | share modal fetches `/api/v1/{type}/{id}/shares` → **404**, so the "current shares" list is silently empty | `/todos/shared-with-me` and `/lists/shared-with-me` → **404**: they are declared after `/{id}` and get swallowed by it (`todos.py:176` vs `:906`; `lists.py:151` vs `:772`) | partial |
| Files | (page renders) | upload `.md` with `text/markdown` → list → preview OK. The same file sent as `application/octet-stream` is rejected (MIME type comes from the client) | works |
| Feedback | — | POST (query params) OK | works |
| Timezone | — | PUT / GET OK | works |
| Standup | page renders | `generate` / `today` OK but empty: "Nothing to show yet — as you work in connected tools…". The user's own Piper todos are not included (whether that is intended is unverified) | works (degraded) |
| Conversations / Radar | chat history rail OK | create / list OK. Radar shows a raw ISO timestamp ("last activity 2026-10-03T18:24:34.160168+00:00") | works |

**GET sweep, all 77 parameter-free `/api` GETs while authenticated** (`C-api-exercise.json`):
- 58 → 200
- 6 → 403 (admin and transparency stats)
- 3 → 302 (OAuth callbacks)
- 2 → 422
- 2 → 404 (`shared-with-me`)
- 2 → 502 (GitHub repositories, Slack channels)
- 2 → 503 (GitHub / Calendar connect)
- 2 → 401 (Calendar calendars, Notion databases)

**UI → API contract audit** (`metrics/C-fetch-audit.py`): 108 literal `/api/...` URLs in templates and static JS. 9 did not match a live route. After removing interpolation and docstring artifacts, the real misses are the `/shares` call (2 templates) and the commented-out `learning/controls` routes. No UI calls those controls routes, so it is a dead feature, not a broken button.

### Chat without an LLM (what the user sees)

- All 9 probes went through the real UI. Each returned HTTP 200 in about 2.8–3.1 s with `intent: {type: unknown, action: clarify}` and an `error` field that duplicates the message.
- **The gate fires before classification** (`web/api/routes/intent.py:232-290`, #1807/#1818). That means deterministic handlers (greeting, `mark todo 1 done`, session activity) are refused too. This is deliberate and documented in the code. The copy is honest, and the first refusal of a session is warmer than later ones.
- **Even with the gate lifted, chat is mostly LLM-dependent.** I ran the deterministic `PreClassifier` on 15 everyday phrasings (`metrics/C-preclassify.py`). Only 6 matched:
  - `hello`, `thanks`, `what can you do?`, `mark todo 1 done`, `what did we create this session`, `show my projects`.
  - 3 of those (`thanks`, `what can you do?` and the `PORTFOLIO:manage_portfolio` match) route to the LLM floor anyway, per the registry.
  - These all returned `None` and need the LLM classifier: `add a todo: …`, `show my todos`, `what time is it?`, `what's my next todo`, `set my timezone to …`, `remind me …`, `list open issues`, `what's on my calendar today?`.
- Document summarize also degrades honestly: "This needs an LLM key of your own… Nothing was charged."

### Other surfaces

- **`python main.py status`**: the integrations check crashes (`'Depends' object has no attribute 'sub'`, because a FastAPI route function is called directly). The command **still prints "✓ All systems operational!"** It also reports on an arbitrary user (`scen_380a2514`).
- **MCP server**: the ASGI app builds. `/health` returns 200 (`version 0.8.14.0`). `/mcp tools/list` returns 401 `invalid_token`, and `/.well-known/oauth-authorization-server` returns 401 `identity_required`. It fails closed as designed; its content cannot be observed without OAuth.

---

## 3. Classification

The denominator is 32 capability groups derived from the §1 inventory. Each HTTP route belongs to one group; the 53 chat actions are one group (row 26), broken down in §1.

| # | Capability | Class | Evidence |
|---|---|---|---|
| 1 | Invite-gated signup (API) | works | create-user 200; reuse → 400 |
| 2 | Signup via UI wizard | partial (blocked: infra check + required validated LLM key before the account step) | `C-firstrun.json`, `fr03`/`fr05` screens |
| 3 | Login / logout / me | works (wrong-password copy is wrong, C-03) | UI + API |
| 4 | Password reset | unobservable (needs mail) | — |
| 5 | Todos CRUD | works | UI + API |
| 6 | Projects CRUD | works | UI + API |
| 7 | Lists + items | works | UI + API |
| 8 | Work items | works | API + page |
| 9 | Sharing (todos/lists/projects) | partial | `/shares` 404, `shared-with-me` 404 |
| 10 | Files upload / list / preview | works | API (re-run post-wipe) |
| 11 | Document analyze / summarize / Q&A / compare | unobservable (LLM; honest gate) | summarize response |
| 12 | Conversations / history / Radar | works | API + UI |
| 13 | Preferences / timezone | works | API |
| 14 | Feedback | works | API (re-run post-wipe) |
| 15 | Standup generate / today | works (empty without integrations) | API + page |
| 16 | Insights / learning dashboard | partial: page renders, content depends on LLM or learning data | crawl |
| 17 | Transparency / audit | partial: page renders; `/transparency/stats` and `/health` return 403 to the owner | GET sweep |
| 18 | Personality preferences | partial (JS page error) | crawl |
| 19 | LLM key management | fails in this env (no secure store; fails closed) | `/keys/store` response |
| 20 | Integration health page | works (alarming tone for a new user) | screenshot |
| 21–24 | GitHub / Slack / Calendar / Notion connect | unobservable (OAuth apps not configured). GitHub connect returns 503, shown to the user as a generic message | server log vs response |
| 25 | Connected apps (MCP connections) | unobservable | page renders |
| 26 | **Chat: 53 wired actions** | **unobservable** (keyless gate). From code: 19 DB-only, 22 need external integrations, 12 need an LLM | §1, §2 |
| 27 | Admin cache / monitoring | unobservable (403 to user) | sweep |
| 28 | CLI `main.py status` | partial (false "operational") | run output |
| 29 | Other CLI (setup, keys, cal, notion, issues, documents, personality, publish) | not exercised (unverified) | — |
| 30 | MCP server | unobservable (fails closed without OAuth) | ASGI probe |
| 31 | 404 / 500 / network-error pages | stub (templates exist, never served) | curl → JSON |
| 32 | Learning controls (enable / disable / privacy / export) | stub (routes commented out, `learning.py:73-299`) | `C-routes.txt` |

**Totals (n = 32)**:

| Class | Count |
|---|---|
| works | 12 (1, 3, 5, 6, 7, 8, 10, 12, 13, 14, 15, 20) |
| partial | 6 (2, 9, 16, 17, 18, 28) |
| stub | 2 |
| fails | 1 (environment-caused) |
| unobservable | 10 (counting 21–24 as one row; 13 if counted individually) |
| not exercised | 1 |

**Pages: 30/30 render. 27 are clean and 3 have errors** (one of those is low confidence).

**Reading of the totals**: everything a user can do without an LLM is plain CRUD organisation (todos, projects, lists, files). It mostly works and is reasonably polished. Everything that makes Piper a PM *assistant* (chat, GitHub/Calendar/Notion actions, document intelligence, standup content, insights) cannot be observed without a BYO LLM key plus per-integration OAuth apps.

---

## 4. Findings (schema: id · claim · layer · denominator · evidence · confidence · implication)

| id | claim | layer | denominator | evidence | conf | implication |
|---|---|---|---|---|---|---|
| C-01 | All chat is refused before classification when the user has no LLM key, including deterministic handlers (greeting, complete_todo, session activity). | ran-server + static | 9/9 UI chat probes | `C-crawl.json` chat; `web/api/routes/intent.py:232-290` | high | A keyless first-run gets zero value from the headline surface. Letting DB-only deterministic actions through the gate would let new users experience Piper before they pay for a key. |
| C-02 | Even without the gate, deterministic routing covers few everyday phrasings: 6/15 pre-classified, and 3 of those route to the LLM floor anyway. "add a todo", "show my todos", "what time is it?" all need the LLM classifier. | static + ran (in-process) | 15 probe phrasings | `metrics/C-preclassify.py` / `.json` | med (probe set is mine) | Chat is effectively 100% LLM-dependent. Product cost, latency and failure modes all hinge on the LLM path. |
| C-03 | Wrong password on the login page shows "Let's try logging in again. Your session may have expired." | ran-server | UI + API | `login_wrong_password.png`; curl | high | Wrong copy at the first trust moment. One string covers different states, the same shape the code comments already warn about for the chat gate. |
| C-04 | The UI signup wizard needs every required infrastructure service up and a validated LLM key before the account step. There is no UI path to an account without a key. | ran-server + static | 1 flow, 5 steps | `setup.js:145-148, 270-278`; `fr03-step1.png` | high | Biggest first-run blocker for hosted alpha. Decouple account creation from key and infrastructure validation. |
| C-05 | Errors with a known cause are flattened to "Something went wrong on my end". Example: GitHub connect 503, where the server logs "GitHub OAuth not configured (missing OAuth App client_id/secret)". Conversely, key-store errors leak internal "#1382" references. | ran-server | 3 integration endpoints + key store | server.log vs response bodies | high | Error-copy quality is inconsistent. Route operator-config errors to an honest "not set up on this server" message. |
| C-06 | `main.py status` prints "All systems operational!" right after its integrations check crashed. | ran | 1 CLI run | output in §2 | high | A false clear in the product itself (m-44 shape). The health tooling should fail loud. |
| C-07 | API contract drift is patched in clients rather than fixed: PUT todos/projects silently ignore JSON bodies (200, unchanged); the share modal calls a nonexistent `/shares` route (404 → empty); `shared-with-me` is unreachable because of route order. | ran-server + static | 108 UI API URLs audited; 77 GETs swept | `C-fetch-audit.json`, `C-api-exercise.json`, `todos.py:176/906` | high | Add contract tests (the fetch-audit script is a seed) and make unknown body fields an error, not a silent 200. |
| C-08 | A new user's Integration Health page shows a red "Multiple Issues — 0 of 4 healthy". GitHub shows "unknown" plus Disconnect for a user who never connected it. | ran-server | 1 page, 4 integrations | `pg_settings_integrations.png`; `/integrations/health` | med (GitHub cause unverified, possibly the env `GITHUB_TOKEN`) | Not-configured is shown as unhealthy, which alarms new users. It also needs checking whether an operator token is being shown as the user's own connection. |
| C-09 | Core CRUD (todos, projects, lists, work items, files) works end-to-end in both UI and API, with friendly empty states. It lives under the username dropdown, and standup is trust-gated to stage 3. | ran-server | 5 features, 3 via UI dialogs | `C-ui-crud.json`; `nav_rail.html:40,55-65` | high | The working value is hard to find. Surface it in the nav or have chat point to it when keyless. |
| C-10 | Unknown URLs return raw JSON `{"detail":"Not Found"}`. The 404, 500 and network-error templates are never served. | ran-server + static | 4 unreferenced of 32 templates | curl; grep | high | Small polish gap, and dead templates. |
| C-11 | The product surface is large relative to what can be observed: 255 HTTP ops, 53 chat actions, 27 CLI subcommands, an MCP server. About 40% of the 32 capability groups cannot be observed without external credentials. | static + live | full inventory | §1 | high | Most product behaviour can only be verified with keys and OAuth. A seeded harness (fake LLM provider plus stub integrations) would make it checkable. |

### Appendix: minor findings not tied to the guiding question

- `/docs` and `/openapi.json` are public (unauthenticated).
- The 8 `/api/admin/*` routes lack the `/v1` prefix the repo convention requires.
- The page header uses the user-preference timezone while message timestamps use browser time.
- Radar shows a raw ISO timestamp.
- `mint_invite_tokens.py` hard-codes a `/Users/xian` `.env` path.
- Upload rejects `.md` sent as `application/octet-stream` because it trusts the client MIME type.
- A `/health/config` 401 for a never-logged-in caller says "your session may have expired".
- **Eval-environment issue**: concurrent pytest runs wipe the shared scratch DB. Other workstreams' runtime results may be affected too.

---

## Unobservables

| What | Why not observed | How a tester or harness could observe it |
|---|---|---|
| All 53 chat actions, including the LLM classifier and floor | No LLM key; key storage impossible without `ENCRYPTION_MASTER_KEY` | Set `ENCRYPTION_MASTER_KEY`, store a real key via `/settings/llm-keys`, replay the probe set in `C-crawl.py`. Better: point the provider at a recorded or fake LLM server for deterministic replays |
| GitHub / Slack / Calendar / Notion actions and settings | No OAuth app client IDs or secrets; no tokens | Configure test OAuth apps and a sandbox org/workspace, then run the integration settings pages and chat probes ("list open issues", "what's on my calendar today") |
| Document intelligence (summarize / analyze / Q&A / compare) | LLM-gated | As above, with a fixture PDF/MD |
| Insights / learning content, standup with real content | Needs history plus integrations or LLM | Seed a user with a week of activity (fixtures), then view `/insights`, `/learning`, `/standup` |
| MCP server tools and resources | OAuth identity required | Run `main_mcp.py`, complete the OAuth flow with a test client (e.g. MCP inspector), call `what_piper_knows_about_me` |
| Signup wizard steps 3–5 in the UI | Blocked by ChromaDB and the key gate | Run ChromaDB and supply a valid key, then rerun `C-firstrun.py` to the end |
| Password reset | Needs mail delivery | Use a mail catcher (MailHog) with the reset flow |
| Remaining CLI subcommands (27) | Not exercised; most need integrations | Script each with `--help` and dry-runs under a seeded user |
| Real-browser MIME behaviour for `.md` upload | API-only test | Upload via the `/files` page in Playwright using a file chooser |
| Admin endpoints | 403 for a normal user | Promote a test user to admin and sweep |

## Pre-registered top 5

1. **Chat has no keyless value at all.** The gate refuses even deterministic actions, and the pre-classifier only routes about 6 of 15 everyday phrasings deterministically. Decide whether DB-only actions should pass the gate (C-01, C-02).
2. **There is no UI path to an account without a validated LLM key and a full infrastructure check.** Decouple signup from key and infrastructure validation (C-04).
3. **Error copy is wrong at trust-critical moments.** Wrong password reads as "session expired"; known config causes become "something went wrong"; internal issue numbers leak to users (C-03, C-05).
4. **API contract drift is papered over in clients.** Silent no-op PUTs, a 404 shares route, unreachable `shared-with-me`. Add UI↔API contract tests (C-07).
5. **The health tooling gives false clears and false alarms.** `status` says "operational" after a crash; Integration Health shows red for a new user (C-06, C-08).

---
**Scripts** (`spec-eval/metrics/`):
- `C-routes.py` / `C-routes.txt`: route inventory vs live
- `C-actions.py` / `C-action-registry.json`: chat registry
- `C-openapi-live.json`
- `C-firstrun.py` / `.json`
- `C-api-exercise.py` / `.json`
- `C-crawl.py` / `.json`: pages, links, chat
- `C-ui-crud.py` / `.json`
- `C-preclassify.py` / `.json`
- `C-fetch-audit.py` / `.json`
- `C-screens/` (40 PNGs)

**Verified how**: ran scripts against live OpenAPI and code (static), then Playwright and httpx against the running server (ran-server) · layers: static, ran-server, in-process pre-classifier · denominator: 255 ops / 30 pages / 53 chat actions / 32 capability groups / 108 UI API URLs / 77 GETs / 9 chat probes / 15 pre-classifier probes.
