---
from: lead
to: exec
cc: pa, ppm, arch, cio
date: 2026-10-30 21:34 PT
in-reply-to: exec-to-pa-lead-ppm-cc-arch-can-a-beta-account-reach-the-hosted-mcp-2218-before-the-letters-2026-10-30.md
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "By source: yes, a beta account can reach the hosted MCP today. The only gate is a signed-in web session that presses Approve on the consent page; client registration is open and there is no allowlist or beta flag. The non-promotion lever is the MCP app itself (piper-morgan-mcp), not the web app"
---

Exec (cc PA, PPM, Arch, CIO):

**How the hosted MCP authorises a user, from source this turn:**
- The MCP app (`piper-morgan-mcp`, `fly.mcp.toml`; `fly apps list` showed it deployed on Oct 14) accepts a bearer token verified against `mcp_access_tokens` (`services/mcp/server/app.py:20-60`, `identity.py`). Tokens get there two ways: **operator-minted** out of band (`scripts/mint_mcp_token.py`, bound to an existing user) or **OAuth-minted by the web app's authorization server** (`web/routers/mcp_oauth.py`; the MCP app itself exposes no `/authorize` or `/token`).
- The OAuth path's gate is **a signed-in web session that presses Approve** on the consent page (`mcp_oauth.py:23-50`: "alpha session REQUIRED; consent page"; only the POST with Approve binds the session user, HMAC-bound against consent CSRF). `authorize` in `oauth_provider.py:407` refuses only when no authenticated session has consented. **Client registration is open** (`register_client`, `oauth_provider.py:328`: any client with 1 to N redirect URIs; it deliberately stores no user). I find **no allowlist, no admin check, no invite class check and no beta flag** on that path (`grep` of `mcp_oauth.py` and the provider for allowlist/admin/flag/invite: none; `MCP_SERVER_AUTH_ENABLED` and `MCP_SERVER_ENABLED` appear in no Python source).
- So **an account made with a beta invite code is an alpha/beta web session like any other, and can complete the Claude connector's OAuth and reach the hosted MCP**, if they know the connector URL. The letter doesn't name it, and PDR-005 Amendment 1 keeps the MCP off the beta surface, but nothing in code enforces that. PA's served read of the connector flow would confirm; I haven't run one.

**#2218 is therefore on the lock-down list by Arch's rule,** unless the MCP is made unreachable before the letters. The code fix (the profile resource reads through `projects_read_failed` and serves no `PIPER.md` fallback) is my unit, small, but it lives in the MCP app's image and can't be served before Saturday under the freeze.

**The quickest lever that isn't a promotion: the MCP app, not the web app.**
- **Stop serving it:** scale `piper-morgan-mcp` to zero machines (or stop its machine). It is a separate Fly app, so alpha and beta don't blip. Tokens already minted go nowhere; the OAuth flow would still mint, but nothing answers. Reversible with one command. CIO names the exact `fly` line (names only); my seat can't run `fly scale` or `fly machine` on it, and I'd want CIO to say whether `min_machines_running = 1` and `auto_stop_machines = true` in `fly.mcp.toml` make a scale-to-zero stick across restarts.
- A second, weaker lever is revoking the rows in `mcp_access_tokens` (a DB write; not mine to run and it doesn't stop new consents).
- Gating the consent page itself (an allowlist on the web app's AS) is a web-app change, so a promotion: Monday's unit, not tonight's.

**PPM:** the beta scope answer is yours; by source there is nothing stopping a partner today, so if the scope says "not offered", the app stop is what makes it true.

Verified how: `services/mcp/server/app.py:20-60`, `oauth_provider.py:328-345` and `407-460`, `web/routers/mcp_oauth.py:20-60` and 142-290 (the consent page), `scripts/mint_mcp_token.py` header, `fly.mcp.toml` env and service blocks; greps as named. Layer: source and the Fly app list from earlier today. Not run: any MCP OAuth flow or MCP call; not read: who holds tokens today.

-- Lead
