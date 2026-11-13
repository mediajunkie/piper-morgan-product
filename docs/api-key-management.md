# API Key Management

**Last Updated**: October 31, 2026 (rewritten against the current code, issue #1904; the first version was written for #228 in October 2025)

## Overview

Each signed-in user stores their own LLM provider key. Piper makes that user's LLM calls with that user's key and never with anyone else's. This page describes where the key lives, the REST routes that manage it, and what happens on store, delete and rotate.

Verified against: `services/security/user_api_key_service.py`, `web/api/routes/api_keys.py`, `services/infrastructure/keychain_service.py` and the `UserAPIKey` model in `services/database/models.py`, read 2026-10-31; the storage section re-read 2026-11-12 for the keychain opt-in change (#2353).

## Where the key is stored

The key is stored encrypted in the database. The OS keychain is used only if you choose it.

1. **Encrypted at rest in the database** (`user_api_keys.encrypted_secret`). The key is encrypted field by field (AES-256-GCM) with a key derived from `ENCRYPTION_MASTER_KEY`. This is the durable store on the hosted app and on a local install. A second encrypted copy goes to the `secure_credentials` table through `KeychainService`, which is the database store unless you chose the keychain.
2. **The OS keychain**, only when `PIPER_CREDENTIAL_STORE=keychain` is set. Since 2026-11-12 the app never reads or writes the OS keychain on its own: with the variable unset it uses the database store. Someone who already keeps keys in their own keychain sets the variable to go on using them. When the encrypted column is available, a keychain failure is logged and the store continues. Reads prefer the encrypted column and fall back to the `KeychainService` copy: the `secure_credentials` row, or the keychain when it was chosen.

With no `ENCRYPTION_MASTER_KEY` and no keychain choice there is nowhere secure to put a key: storing fails and says so, and reads find no key. On a local install, `python scripts/local_key_setup.py` creates the master key and stores a provider key at a hidden prompt.

The `user_api_keys` table (one row per user and provider, unique on the pair) also holds metadata: `provider`, `key_reference` (`piper_{user_id}_{provider}`), `is_active`, `is_validated`, `last_validated_at`, `previous_key_reference`, `rotated_at`.

The same table holds connector credentials too (the GitHub token at rest and `{connector}_mcp_oauth` grants). Those are managed only through their connector's Connect and Disconnect in Settings → Integrations. The key routes below refuse any provider that is not an LLM provider.

## Providers

The routes accept the providers in `LLMProvider`: `anthropic`, `openai`, `gemini`. Any other value returns 400 with a message pointing at Settings → Integrations. The private beta asks testers for an Anthropic key.

## REST routes

All routes are under `/api/v1/keys` and need an authenticated user.

| Route | Does |
|-------|------|
| `POST /store` | Stores a key. Body: `provider`, `api_key`, `validate` (default `true`). Returns `provider`, `is_validated`, a message. |
| `GET /list` | Lists the user's keys as metadata only: `provider`, `is_active`, `is_validated`, `last_validated_at`, `created_at`, `rotated_at`. The key itself is never returned. |
| `DELETE /{provider}` | Deletes the key. Removes it from the keychain (a keychain failure is logged and the delete continues), then deletes the database row, which removes the encrypted copy. |
| `POST /{provider}/validate` | Checks the stored key against the provider and returns `is_valid`. |
| `POST /{provider}/rotate` | Replaces the key. Body: `new_api_key`, `validate` (default `true`). Records `rotated_at` and keeps `previous_key_reference`. |

Store, delete and rotate write an audit log entry.

## In the app

Testers manage their key in Settings → LLM API Keys. Removing a key there deletes it from the live database. Backups keep a copy for a limited time, and the Remove dialog says so.

## Examples

```bash
# Store a key (validated by default)
curl -X POST https://<host>/api/v1/keys/store \
  -H "Authorization: Bearer <your token>" -H "Content-Type: application/json" \
  -d '{"provider": "anthropic", "api_key": "<your key>"}'

# List your keys (metadata only)
curl https://<host>/api/v1/keys/list -H "Authorization: Bearer <your token>"

# Delete
curl -X DELETE https://<host>/api/v1/keys/anthropic -H "Authorization: Bearer <your token>"
```

Never paste a real key into a document, an issue or a commit.

## Troubleshooting

- **404 on delete**: no key is stored for that provider for your user. List first. (Validate wraps every failure, a missing key included, in a 500 "Failed to validate API key".)
- **400 "This page is for AI provider keys only"**: the provider is a connector, not an LLM provider. Use Settings → Integrations.
- **Store fails on a local install**: with no `ENCRYPTION_MASTER_KEY` there is no store, because the OS keychain is used only when `PIPER_CREDENTIAL_STORE=keychain` is set. Run `python scripts/local_key_setup.py` (it creates the master key), or set that variable to use your keychain.

## Not verified here

Key validation behavior against each provider, the rotation steps beyond what the route docstrings state, and the Alembic migration history for `user_api_keys` were not re-read for this rewrite.
