# #1317 inc.2 — GitHub connector OAuth (option C: self-hosted + per-user OAuth) gameplan

**Author**: Lead Dev · **2026-06-27** · **Decision**: C (Arch re-ruled A→C); token-custody CONFIRMED (binding → encrypted grant in `user_api_keys`, binding holds a reference). decisions.log + carry-forward.

## Clarification (corrects the carry-forward "OAuthClientProvider/PKCE" note)
Option C's GitHub auth is a **plain GitHub OAuth App authorization-code flow** (mirror `services/integrations/calendar/oauth_handler.py`, pointed at GitHub endpoints) — NOT the MCP-protocol PKCE/`OAuthClientProvider` (that was option A's hosted-endpoint OAuth). We get the **user's GitHub OAuth token** and forward it to our self-hosted `github-mcp-server` via the `Authorization` header.

## Endpoints (GitHub OAuth App)
- authorize: `https://github.com/login/oauth/authorize`
- token: `https://github.com/login/oauth/access_token` (send `Accept: application/json`)
- user: `https://api.github.com/user` (identity for logging)
- scopes (requested in-flow): `repo` (confirm minimal set; GitHub requests at authorize, not registration)

## Slices (TDD, each committed)
- **A — `GitHubOAuthHandler`** (`services/mcp/consumer/github_oauth_handler.py`): mirror the calendar handler — `generate_authorization_url(user_id)` (state=user_id+nonce, CSRF/#734), `verify_state`, `handle_oauth_callback(code,state)` → exchange code → `GitHubOAuthTokens(access, refresh?, expires_at?)`. **Tests**: state gen/verify (no network); code-exchange with mocked aiohttp. ← FIRST
- **B — grant storage**: store the user's GitHub token (encrypted) via `user_api_key_service` (provider="github_mcp", per-user); the #1229 binding references it (status=bound). **Tests**: store→retrieve round-trip; binding upsert refs the secret.
- **C — `MCPClient.connect_http` auth header**: re-add header support via the SDK's `create_mcp_http_client(headers=...)` → `streamable_http_client(url, http_client=...)`, so the user token reaches the self-hosted server. **Tests**: header passed (against the http fixture).
- **D — web routes** (`web/api/routes/settings_integrations.py`): `/github/connect` (redirect to authorize) + `/github/callback` (verify→exchange→store grant→create binding→redirect). **Tests**: callback creates a bound binding (mocked handler).
- **E — github adapter wiring**: `connect()` unbound → ConnectRequired(action_hint=`/api/v1/settings/integrations/github/connect`); `_mcp_client_ctx` → `connect_http(<self-hosted-url>, token)`; `_server_params_for` retired for github (HTTP not stdio). **Tests**: connect() returns the connect URL; resolve() uses the http client.

## AC
- [ ] GitHub OAuth handler (authorize-url + state CSRF + code-exchange), TDD.
- [ ] Grant stored encrypted (`user_api_keys`); binding references it (no token in the binding row — D3).
- [ ] `connect_http` carries the user token (auth header) to the self-hosted server.
- [ ] `/github/connect` + `/github/callback` wired; callback creates a bound binding.
- [ ] adapter connect()/status()/resolve() reflect the live flow; consumer suite green; no regression.
- [ ] LIVE deps (PM-gated, not code): OAuth App registered (callback `…/github/callback`), Docker server deployed, client_id/secret in keychain.

## Security / audit self-check
- State CSRF + user_id-bound (mirror #734); single-use; expiry. · Token NEVER logged (log presence/length only). · Grant encrypted-at-rest (`user_api_keys`); binding holds a reference, never the token (D3). · client_secret from keychain/env, never committed. · Token-exchange failures degrade honestly (no silent success). · End-state #1325 (GitHub-App installation-token) supersedes per-user-token custody when supported.
