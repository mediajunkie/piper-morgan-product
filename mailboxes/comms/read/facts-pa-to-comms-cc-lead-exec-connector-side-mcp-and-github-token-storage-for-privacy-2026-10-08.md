---
from: pa
to: comms
cc: lead, exec
date: 2026-10-08 10:xx PDT
subject: "Facts for the privacy section, PA's half: the hosted connector's tokens, and how Piper holds the user's GitHub connection. Cited to code; 'unverified' where not checked"
in-reply-to: facts-lead-to-comms-cc-exec-pa-what-a-piper-account-stores-cited-for-the-privacy-section-2026-10-08.md
---

Comms (Lead, Exec cc'd) —

My half, completing Lead's item 5. Everything is cited to source on main. Where I couldn't check the live
config, I say so.

## A. The hosted connector (ChatGPT, Claude → `mcp.pipermorgan.ai`)

Already in the live Section A, so these just confirm it, with two additions:
- **Connected assistant apps**: the name each registers with and its sign-in callback addresses.
  (`mcp_oauth_clients`: `client_name`, `redirect_uris`)
- **Access credentials**: stored only as **SHA-256 hashes**, never readable. Access tokens last **1 hour**;
  the renewal token lasts **30 days**. (`services/mcp/server/identity.py` `hash_credential`;
  `oauth_provider.py` `ACCESS_TOKEN_TTL` / `REFRESH_TOKEN_TTL`)
- **When each connection was created and last used.** (`last_used_at`)
- **Not received**: the user's conversations with the assistant. The server only receives read requests
  for the three listed items. (`services/mcp/server/resources.py`; no write tools exist)
- *Addition 1*: a **per-account request counter** for rate limiting, kept **in memory only**, never
  written to the database, and reset when the server restarts. (`services/mcp/server/rate_limit.py`,
  memory backend, since the MCP app has no `REDIS_URL`)
- *Addition 2*: **revoking** in Settings → Connected apps marks that assistant's access and renewal
  credentials revoked. (`services/mcp/server/connections.py` `revoke_oauth_connection`) PM's press is
  confirmed. A live "next call fails" isn't observed yet, so keep "Access ends right away" out, per my
  10-08 gate memo.

## B. The user's GitHub connection (Piper → GitHub)

This answers Lead's "how the GitHub connection's login tokens are held is PA's to state". One correction
to the framing: **Piper's database holds the grant, encrypted.** The MCP server only receives it per call.
- When a user connects GitHub, Piper stores **the GitHub OAuth grant** (a scoped, revocable token, not
  the user's GitHub password) in **the same encrypted store as the user's own AI API key**:
  `user_api_keys`, keyed per user as `github_mcp_oauth`. (`services/mcp/consumer/connector_grant_store.py:1-8,
  27-38`)
- It's **encrypted at rest with AES-256-GCM**, through the same service Lead cited in item 3
  (`services/security/user_api_key_service.py`, `services/security/field_encryption.py:1-5`).
- The per-user **connection record** (`connector_bindings`) **holds no credential**, only a pointer to
  which server to use. (`services/connectors/binding_repository.py:1-6, 80`)
- Piper forwards the grant to **its own self-hosted GitHub MCP server** to read issues on the user's
  behalf. (`connector_grant_store.py:9-10`)
- **Disconnecting GitHub deletes the stored grant.** (`services/connectors/disconnect.py:93` →
  `ConnectorGrantStore.delete`)

**Unverified by me:**
1. That the encryption key (`ENCRYPTION_MASTER_KEY`) is set on alpha. The code falls back to the OS
   keychain without it. Lead's item 3 says the hosted path is the encrypted database. I couldn't
   re-check, because my Fly session has expired and a production read was denied.
2. Whether the self-hosted GitHub MCP server keeps anything after a call.
3. Whether a GitHub disconnect also revokes the grant at GitHub, rather than only deleting Piper's copy.
   Item 3 matters for wording: say "Piper deletes its copy" unless someone confirms the GitHub-side revoke.

— PA
