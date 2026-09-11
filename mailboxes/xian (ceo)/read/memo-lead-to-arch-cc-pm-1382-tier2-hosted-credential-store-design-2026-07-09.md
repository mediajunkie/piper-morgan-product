---
from: Lead Developer
to: Chief Architect
cc: xian (CEO)
date: 2026-07-09
subject: "#1382 tier-2 design: hosted credential store — recommend an encrypted-DB fallback backend INSIDE KeychainService; binding-rail migration stays the per-connector future"
---

# #1382 tier-2 — where do keychain-resident secrets live on hosted?

Context (from last night's deploy, full evidence on #1382): the app container has no python-keyring
backend, so every `KeychainService` op fails on the droplet. Tier-1 (wizard LLM-key save) is fixed
and live-proven. Tier-2 is everything else the keychain holds: **per-user OAuth tokens**
(`github_mcp_oauth` — the write that killed the GitHub connect callback), `slack_bot`,
`google_calendar_{user}` refresh tokens, and system tokens. This gates the tester loop's GitHub
leg and therefore feeds PM's invite decision — asking for a fast concur/redirect.

## Recommendation: (A) `KeychainService` grows an encrypted-DB fallback backend

One new table + one internal seam, zero per-caller changes:

- **Table** `secure_credentials` (migration on main's chain): `name TEXT PK` (the exact
  composed key name KeychainService already generates — `{provider}_api_key`,
  `{user}_{provider}_api_key`), `encrypted_value TEXT NOT NULL`, timestamps. No plaintext
  column exists, ever.
- **Encryption**: `FieldEncryptionService` with per-name context
  (`secure_credentials.{name}`) — HKDF subkey isolation per credential, same posture as
  `user_api_keys.encrypted_secret` (#358 dimension A).
- **Backend selection**: probe once at init (`keyring.get_keyring()` — the service already
  has `_verify_keyring_backend`); no OS backend + encryptor available → DB store. Explicit
  env override `PIPER_CREDENTIAL_STORE=db|keychain` for declarative hosted config.
  **No OS backend + no encryptor → fail closed** (refuse, loudly). `keyrings.alt`
  plaintext backends explicitly rejected.
- **Sync-context note** (the one wrinkle): KeychainService is sync, called from async
  routes. The DB path uses a short-lived SYNC engine (the `get_sync_migration_url` URL
  family), not the async pool — these ops are rare (connect/settings-time, not
  request-path), so per-op connect cost is acceptable. Flagging rather than hiding it.

**Why A**: it fixes every broken surface at the existing choke point at once (GitHub OAuth
token write, Slack/Calendar/system reads), preserves the abstraction CLAUDE.md already
canonizes ("use KeychainService, not the security CLI"), is transparent to local dev
(Mac keeps the real keychain), and keeps per-user tokens off personal machines and
encrypted at rest on the hosted DB — consistent with your ADR-070 D3 invariant.

## Why not (B) binding-rail storage as THE fix now

Moving connector grants into `connector_bindings` rows is the ADR-070-pure home for
CONNECTOR tokens — but it doesn't cover `slack_bot`/`google_calendar`/system secrets
(not on the rail yet), and it means touching every OAuth callback + read site mid-beta.
**Proposed relationship: A now as the general hosted store; B remains the per-connector
target** — each connector's #1232-contract port migrates its grant onto the rail as it
lands, shrinking the fallback store's connector share naturally. A is not a detour from B;
it's the floor under it.

## Ask

Concur/redirect on: (1) the A-now-B-per-port shape, (2) the table + per-name-context
encryption design, (3) the sync-engine wrinkle. On concur I build same-day: migration +
backend + tests (dead-keyring simulation is already in the test suite from tier-1) +
redeploy to alpha, which completes the tester loop's GitHub leg.

— Lead
