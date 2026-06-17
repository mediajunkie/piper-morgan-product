# Auth architecture for a hosted, publicly distributed Piper Morgan plugin — Research R2

**Date**: 2026-06-12  
**By**: PA research agent (Claude Code, Sonnet 4.6)  
**Feeds**: Phase 2 skunkworks scope decision  
**Prior research**: `pa-plugin-marketplace-hosting-research-2026-06-07.md`  
**Prior internal design**: `pa-1185-multi-tenant-byo-key-investigation-2026-06-10.md`  
**Sources**: codebase inspection, skunkworks priors, prior research files, recent memos

---

## Context recap (from R1 + recent memos)

The hosted endpoint (`alpha.pipermorgan.ai`) is already deployed — DigitalOcean droplet, Caddy TLS
+ shared basic-auth, v0.8.7. **No new infra needed to prove marketplace mechanics.** The blocker for
distributing to more than one user is multi-tenancy auth: the alpha uses a single shared credential
(Caddy basic-auth + a shared password in `PIPER_BASE_URL`). Issue #1185 tracks multi-tenant per-user
auth (M5 milestone). Lead Dev confirmed this in a 2026-06-12 memo ratifying Phase 2.

The plugin's MCP server (`mcp/server.py`, line 29) reads:

```python
PIPER_BASE = os.environ.get("PIPER_BASE_URL", "http://localhost:8001")
```

The current hosted credential is embedded as a basic-auth URL in `.mcp.json`:

```json
"PIPER_BASE_URL": "https://piperalpha:ddb78e1a6f3f7181f4cc44ef8cb49184@alpha.pipermorgan.ai"
```

This is the credential that can't be in a public repo.

---

## B2 — Auth approaches for a publicly distributed hosted MCP plugin

### Option (a): User-supplied env var

**Mechanism**: the plugin ships without the credential. The tester sets an env var before or during
install — either in their shell profile, or as part of a `meet-piper`-style setup step. The MCP
server reads it at launch.

**Implementation on the plugin side** (small, verified from codebase):

1. Replace the hardcoded URL with a token env var. Two sub-forms:
   - **Sub-form A (embed the base URL, add a token separately)**: `.mcp.json` ships with
     `"PIPER_BASE_URL": "https://alpha.pipermorgan.ai"` (no credential) plus
     `"PIPER_AUTH_TOKEN": "${PIPER_AUTH_TOKEN}"`. `server.py` attaches
     `Authorization: Bearer <token>` to httpx calls. ~15 minutes of code.
   - **Sub-form B (URL includes user-specific credentials)**: each tester gets their own credentials
     embedded in the URL (a per-user password or key). Tester substitutes the URL. Works but
     is awkward — URL is a single string to paste.

2. The Caddy (or app-layer) validates the token. Today: Caddy shared basic-auth. For per-user: either
   (i) Caddy validates against a static list (works for a tiny trusted set; doesn't scale), or
   (ii) the app's own `/api/v1/auth/login` JWT system handles it (the app already has per-user
   identity via CORE-USERS-API #228 — this is Gap C in #1185, which is unbuilt but designed).

**UX for tester**:
1. Install `uv`
2. `/plugin marketplace add mediajunkie/dinp-plugins` (or install from file/URL)
3. Set env var: `export PIPER_AUTH_TOKEN=<token-we-give-them>` (or add to `~/.zshrc`)
   — OR — run `meet-piper` which includes a setup step asking for the token and storing it in
   `~/.claude/plugins/config/...` via the MCP server's file-write capability
4. `/plugin install piper-morgan@dinp` and run `/piper-morgan:ask-piper`

**Friction points**: the env var step is the seam. If the tester doesn't set it before Claude Desktop
starts, the MCP server launches with no token and every call fails. The `meet-piper` skill could
surface the error and walk them through the fix, but the initial setup is manual. For a tiny trusted
cohort (Beatrice + a handful of others), this is low friction with a good quickstart.

**What the MCP server needs**: a small code change — add `PIPER_AUTH_TOKEN = os.environ.get("PIPER_AUTH_TOKEN")` and attach it as a Bearer header in `ask_piper`'s httpx call. The existing
`except httpx.ConnectError` failure-mode tagging handles bad credentials badly (it would likely return
HTTP-401 or 403 and be surfaced as `[ask_piper: HTTP-401]`). Consider adding a clear "auth token not
configured" check at startup.

**Confidence**: High. This is the pattern Zoom uses (export bearer tokens before install; see Zoom
plugin README). It requires a small server-side change to accept the token.

---

### Option (b): Per-user API keys issued by Piper

**Mechanism**: before installing the plugin, the tester registers at a Piper page (or is manually
issued a key by PM). They receive a per-user API key (like Anthropic's API — a static, revocable,
opaque string). The plugin ships with `PIPER_API_KEY: "${PIPER_API_KEY}"` in `.mcp.json`. The server
validates the key per-request.

**What the product already has**: the `UserAPIKeyService` + `/api/v1/keys/store|list|validate|rotate`
infrastructure (`web/api/routes/api_keys.py`) manages *third-party* API keys *for* users (GitHub,
Notion, Anthropic, etc.). There is **no existing infrastructure** for issuing API keys *to* external
callers from Piper. This is a different use-case — you'd be building an API-key-issuance system
(registration, key generation, key validation middleware) from scratch.

**What needs to be built**:
1. A registration flow (web page or manual PM step) to create a tester account
2. A key-issuance endpoint (generate an opaque key per user, store it)
3. Server-side middleware to validate the key per-request and map it to a `user_id`
4. Key revocation / rotation endpoints

None of this exists. The app's per-user JWT system (login → JWT → `current_user`) is the closest
analogue, but it uses session cookies / JWTs, not opaque API keys.

**UX for tester**: same as (a) — set `PIPER_API_KEY=<my-issued-key>` before install. The user
experience is nearly identical to (a). The difference is on the server side (we manage keys, not
just a shared secret).

**Confidence**: Medium. Technically straightforward, but requires non-trivial server-side build that
doesn't exist and isn't on the current roadmap. The existing UserAPIKeyService is for *storing*
external keys, not *issuing* keys to external callers.

---

### Option (c): OAuth 2.1 (browser-based authorization flow)

**Mechanism**: the plugin initiates an OAuth flow to grant the tester access. The tester authorizes
in their browser; the MCP server exchanges the auth code for a token. This is how Slack, Apollo,
Notion, and Atlassian handle plugin auth in the prior art (see `customer-support/.mcp.json`:
`"oauth": {"clientId": "...", "callbackPort": 3118}`).

**MCP protocol support**: Claude Code / Cowork has first-class OAuth support in `.mcp.json` via the
`oauth` key (type `http` server with `oauth.clientId` + `oauth.callbackPort`). When configured, the
Claude app handles the OAuth dance natively — opening the browser, capturing the redirect, storing
the token. The tester sees a "Authenticate with Piper" browser window rather than a token to paste.

**What the product already has**: the app has OAuth *callback* routes (Slack OAuth, GitHub OAuth,
Google Calendar — `EXEMPT_OAUTH_CALLBACK_PATHS` in `auth_middleware.py`). These are *inbound* OAuth
flows where Piper is the *resource server* (tester grants Piper access to their GitHub/Slack). They
do **not** implement an outbound OAuth server (where Piper is the *authorization server* issuing tokens
to the plugin).

**What needs to be built**: a full OAuth 2.1 authorization server:
1. An authorization endpoint (`/oauth/authorize`) that renders a consent page
2. A token endpoint (`/oauth/token`) that exchanges codes for tokens
3. Client registration (or a static `clientId`)
4. PKCE support (required by OAuth 2.1)
5. Token storage and validation
6. Refresh token handling

This is the most complete solution — no credential to paste, auto-renew, revocable per-user — but it
is also the most implementation work. Nothing in the current product implements the *server* side of
OAuth.

**UX for tester**:
1. Install plugin (no env vars needed)
2. Claude Desktop shows "Authenticate with Piper Morgan" — click opens browser
3. Log in (or create account) on `alpha.pipermorgan.ai`
4. Redirect back to Claude Desktop
5. Done — no credentials to manage

This is the cleanest tester UX, and it matches what Slack and Apollo do in the partner-built plugins.

**Confidence**: Medium. The build is substantial (full OAuth server), but the *Claude Code plugin
side* is fully supported — `"type": "http"` + `"oauth": { "clientId": "...", "callbackPort": ... }`
is in the prior art (Slack, Apollo). The gap is entirely on the Piper server side.

---

## B2 Recommendation: Option (a), Sub-form A — user-supplied env var, with `meet-piper` as the setup UX

**Reasoning**:

1. **Fastest path to proving marketplace mechanics.** R1's conclusion held: the credential-decoupling
   is the gating design decision, not the auth mechanism sophistication. Option (a) decouples the
   credential from the plugin (public repo safe) with ~15 minutes of server-side code and a small
   `.mcp.json` change. Options (b) and (c) require building new server infrastructure.

2. **Converges with the #1185 roadmap.** The converged design (PM-ratified 2026-06-10) calls for a
   4-rung key-resolution chain culminating in per-user keys. Option (a) is a step on that chain —
   specifically, it's what a "BYO (a) — key passed per-request, not stored" rung looks like from the
   plugin's perspective. Nothing thrown away when #1185 lands.

3. **`meet-piper` absorbs the friction.** The main UX rough edge is the token setup step. `meet-piper`
   already has a Part 6 (Integrations) where it asks about connected tools. Adding a "let me store your
   Piper auth token" step — calling the MCP server's existing `save_profile`-style file-write — turns
   the env-var step into a guided skill step. The token would live in `~/.claude/plugins/config/dinp/`
   and be read by `server.py` on startup. This avoids the shell-profile-edit entirely for most testers.

4. **OAuth is the right long-term answer, but not for this experiment.** When the marketplace listing
   is ready to onboard dozens of testers without hand-holding, OAuth is worth the build (zero-friction
   install, browser-native UX, auto-renew, revocable). That's a Phase 3 / post-#1185 decision.
   For a Phase 2 alpha with a small trusted cohort, (a) is proportionate.

5. **What other plugins do**: Zoom uses env-var tokens (export before install) for their hosted MCP
   surfaces; Slack and Apollo use OAuth for their hosted MCPs. The pattern splits on how many users you
   expect and how "self-serve" the install needs to be. Our alpha is closer to Zoom's case (small, known
   testers).

**Minimum build for Option (a)**:
- `server.py`: add `PIPER_AUTH_TOKEN = os.environ.get("PIPER_AUTH_TOKEN")` and attach as Bearer in
  `ask_piper`'s httpx call (and optionally the profile read/write calls).
- `server.py`: clear error message if token is missing (don't let it silently fail as HTTP-401).
- Caddy/app: validate the bearer token. For the alpha, a shared static token read from the Caddy
  config is sufficient. Per-user validation (Gap C in #1185) comes later.
- `.mcp.json`: replace the embedded basic-auth URL with clean URL + `"PIPER_AUTH_TOKEN": ""` (empty
  default that the tester fills in, or that `meet-piper` populates).
- `meet-piper` skill: add a setup step in Part 6 asking for the token and storing it.

---

## B3 — Additional API surface needed at the hosted endpoint

### What the MCP protocol imposes on transport/auth

The MCP plugin uses a **stdio transport** (not HTTP) — the MCP server is a local process launched by
`uv run server.py`, communicating with Claude Desktop over stdin/stdout. The auth question is therefore
about the **outbound HTTP calls** from `server.py` to the Piper API, not about Claude Desktop's
protocol-level connection to the MCP server.

**Implication**: MCP stdio transport has no protocol-level auth requirement. The credential question
is entirely about how `server.py` authenticates to `alpha.pipermorgan.ai`. Basic-auth (embedded in
URL) works today; Bearer token is the upgrade. The MCP protocol itself is neutral.

**The `type: "http"` OAuth pattern** (Slack, Apollo) is a *different* MCP transport mode — where Claude
Desktop connects to a remote HTTP MCP endpoint directly, and the OAuth flow authorizes that connection.
Our plugin uses stdio (local subprocess); the remote Piper is just an HTTP API the subprocess calls.
If we ever switch to a remote HTTP MCP endpoint (where `alpha.pipermorgan.ai` *is* the MCP server, not
just a backing API), then OAuth at the MCP level becomes relevant. That's a bigger architectural shift.

**Confidence**: High. Verified from `server.py` structure (command: uv, args: run server.py) and the
MCP auth docs pattern in the priors.

### What already exists vs. what needs to be added

| Surface | Status | Notes |
|---|---|---|
| `/api/v1/intent` (the plugin's main call) | ✅ EXISTS — optional auth (`auto_error=False`) | Accepts unauthenticated OR JWT. Per the `EXEMPT_OPTIONAL_AUTH_PATHS` list, auth is optional and handled inline. Works today for the single-tenant case. |
| `/api/v1/auth/login` (user login → JWT) | ✅ EXISTS | Full username/password → JWT + refresh token. Not currently used by the plugin. |
| Per-user JWT validation in `/intent` | ✅ EXISTS | `current_user` derived from Bearer JWT if present; `None` if not. The user_id is already threaded through when auth is present. |
| Bearer token validation middleware | ✅ EXISTS | `auth_middleware.py` + `JWTService.validate_token` — full JWT validation for routes that require it. |
| Static API key validation (for option a short-term) | ❌ NOT EXISTS | No static API key validation middleware. Caddy basic-auth is the only shared-secret gate today. |
| Per-user hosted auth (Gap C, #1185) | ❌ NOT EXISTS | Deploying the app's real per-user auth as the hosted entry gate. App machinery exists; deployment decision unresolved. |
| OAuth authorization server | ❌ NOT EXISTS | No `/oauth/authorize` or `/oauth/token` endpoints. Third-party OAuth (Slack, GitHub, Google) exists as *inbound* resource server, not as an outbound auth server. |

**For Option (a) alpha**: the minimal new surface is a bearer-token check at the Caddy layer (one
static token for the alpha cohort). Nothing in the app layer needs to change — the intent endpoint
already accepts unauthenticated calls and works fine. The token is just a gate to prevent open access.

**For Option (a) multi-user (post-#1185)**: the tester's token becomes a user JWT. The plugin calls
`/intent` with `Authorization: Bearer <jwt>`. The existing `get_current_user_optional` dependency
picks up the user_id. Gap C (#1185) = surfacing the app's login as the Caddy gate replacement.

**What basic-auth doesn't satisfy**: basic-auth works for a single shared gate. It doesn't distinguish
users, can't be revoked per-user, and requires the plain password to travel in every request URL (as it
does now). Bearer tokens at the app layer replace this cleanly. The MCP protocol itself doesn't care
either way — this is all in the httpx call from `server.py`.

---

## B4 — End-user install flow for a GitHub-hosted marketplace listing

**Assumed setup**: marketplace at `github.com/mediajunkie/dinp-plugins`, auth via Option (a)
(user-supplied token, meet-piper guided setup). Auth NOT yet solved (the alpha friction baseline).

### Step-by-step flow

**One-time prerequisite**:
```
install uv:  curl -LsSf https://astral.sh/uv/install.sh | sh
```
This is already in the tester quickstart. Required because the plugin runs via `uv run server.py`.
Friction: low for developers, moderate for non-technical PMs (requires terminal use).

**Add the marketplace**:
```
/plugin marketplace add mediajunkie/dinp-plugins
```
Or, if PM ships `extraKnownMarketplaces` in a project `.claude/settings.json`, it's pre-configured.
The tester never runs this command.

**Install the plugin**:
```
/plugin install piper-morgan@dinp
```
This clones the plugin from GitHub and runs it locally. No file download, no zip.

**Set the auth token** (the friction seam):

Without `meet-piper` guidance:
- PM sends the tester a token out-of-band (email, Slack DM)
- Tester sets `export PIPER_AUTH_TOKEN=<token>` in their shell profile
- Restarts Claude Desktop for the env var to be picked up
- Friction: 2-3 minutes for a developer; potentially a support call for a non-technical PM

With `meet-piper` guidance (the better path):
- Tester runs `/piper-morgan:meet-piper` after install
- `meet-piper` walks through the PM profile interview (the existing 10-minute flow)
- Part 6 / Integrations includes: "To connect to the hosted Piper, you need an access token. Paste
  yours here." — skill stores it via the MCP server's file-write
- On next Claude Desktop restart (or immediate, if the server reads config live), the token is active
- Friction: absorbed into the meet-piper flow, which the tester was doing anyway

**Use the plugin**:
```
/piper-morgan:ask-piper what should I focus on today?
/piper-morgan:consult-piper what should I focus on today?
```

**Auto-updates** (the "doesn't need to manually update" goal from R1):
- Requires `autoUpdate: true` on the marketplace entry + `plugin.json` version bumping
- With this enabled, Claude prompts to reload when a new version is detected
- No re-install needed

### Friction points summary

| Friction point | Severity | Mitigation |
|---|---|---|
| `uv` install required | Medium (terminal use) | Include in quickstart; consider bundling uv in the plugin (`mcp/bin/uv`) to eliminate this (noted in runbook) |
| Auth token setup (env var) | High if manual, Low if via meet-piper | Make meet-piper the canonical setup step; include token in the welcome email with exact instructions |
| Shell profile edit + Desktop restart | Medium | meet-piper can store token via MCP server file-write; only need restart, not shell edit |
| `meet-piper` is 10-15 min | Low (by design) | Already the norm; skip if returning user |
| `uv run` cold-start lag | Low | ~3 seconds on first call while uv bootstraps; subsequent calls are instant |

### Which auth approach requires least friction for an alpha tester?

**Option (a) with meet-piper guidance** — the tester gets a token from PM (one-time, out-of-band),
runs `meet-piper`, and is done. No OAuth flow to debug, no browser redirect, no callback port to open.
For a small cohort of trusted, technically-capable PMs, this is proportionate.

**Option (c) OAuth** would be lower friction at install time (click-to-authorize) but requires the
OAuth authorization server to be built. It's the right answer for open/self-serve distribution.

---

## Summary

| Question | Finding | Confidence |
|---|---|---|
| B2: Cleanest auth for distributed plugin | Option (a) user-supplied env var + meet-piper guidance, minimum code change (~15 min), converges with #1185 roadmap | High |
| B2: What other plugins do | Zoom: env-var Bearer tokens; Slack/Apollo/Notion: OAuth via `"type":"http"` + `"oauth"` in .mcp.json; Intercom/HubSpot/Atlassian: no auth in .mcp.json (auth presumably at provider side) | High |
| B3: MCP protocol imposes on auth | Nothing — plugin uses stdio transport; auth is in the httpx call from server.py to the Piper API; basic-auth works but doesn't scale to per-user | High |
| B3: What needs to be added vs. exists | Intent route, JWT validation, per-user app identity all EXIST. Static bearer-token gate (alpha) needs ~15-min Caddy/app change. Per-user auth at hosted edge (Gap C, #1185) is designed but unbuilt. OAuth server doesn't exist. | High |
| B4: Where is the friction | `uv` install + token setup seam; meet-piper absorbs the token step if it's part of the onboarding; auto-update is achievable with marketplace config | High |
