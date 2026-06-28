# #1317 — GitHub MCP connector go-live deploy plan (alpha Droplet)

**Author**: Lead Dev · 2026-06-27 · Informed by the local de-risk of `ghcr.io/github/github-mcp-server` v1.5.0.

## De-risk findings (verified against the real server, locally)
- **HTTP mode**: `server http` → listens on `/mcp` (default port 8082; `--listen-host`, `--base-url`, `--read-only`).
- **Auth**: every request needs `Authorization: Bearer <github-token>` (401 + OAuth-protected-resource metadata otherwise). → **Piper forwards the user's OAuth grant as the Bearer header** (exactly `MCPClient.connect_http(headers=...)`, slice C). The server needs **no server-level token** — per-request auth.
- **OAuth scopes** (for our OAuth App): **`repo` + `read:org`** (default toolset). `--read-only` reduces write scopes.
- **Tools**: GitHub-specific (`get_me`, `issue_read`, `search_*`, …) — resolve() needs real-tool mapping (the #1230 follow-up; `_RESOLVE_TOOL` placeholder is not real). Full list captured at round-trip.

## Deploy steps (Droplet) — review before I execute
1. **Add the server as a docker-compose service** (internal-only; Piper reaches it, not the public):
   ```yaml
   github-mcp-server:
     image: ghcr.io/github/github-mcp-server:latest
     command: ["http", "--listen-host", "0.0.0.0", "--port", "8082"]
     restart: unless-stopped
     # no ports: exposed publicly — only the app network reaches it
   ```
2. **Piper env** (on the Droplet):
   - `GITHUB_MCP_SERVER_URL=http://github-mcp-server:8082/mcp` (compose service DNS)
   - `GITHUB_OAUTH_REDIRECT_URI=https://alpha.pipermorgan.ai/api/v1/settings/integrations/github/callback`
   - `GITHUB_OAUTH_CLIENT_ID` = the App's client id
3. **Store the new client secret** on the Droplet (getpass, never in shell history):
   `python -c "from services.infrastructure.keychain_service import KeychainService; import getpass; KeychainService().store_api_key('github_oauth_client_secret', getpass.getpass())"`
4. **Deploy the inc.2 code** (push main → pull on Droplet, or scp changed files) + `docker compose up -d github-mcp-server` + restart app.
5. **"Connect GitHub" UI**: confirm/add the button in Settings → Integrations that calls `GET /api/v1/settings/integrations/github/connect` then redirects to the returned `auth_url`. (Backend routes done; UI button likely needs adding — small slice.)
6. **Browser round-trip** (PM): Settings → Connect GitHub → authorize → redirected back, binding BOUND.
7. **Real-tool mapping** (#1230): replace `_RESOLVE_TOOL` with the actual tool(s) per ResourceQuery.kind, using the round-trip's tool list.

## Open items
- UI "Connect GitHub" button (step 5) — verify if present; add if not.
- resolve()'s real-tool mapping (step 7 / #1230) — needs the round-trip tool list.
- Confirm the OAuth App's callback URL matches step 2 exactly (GitHub matches it strictly).
