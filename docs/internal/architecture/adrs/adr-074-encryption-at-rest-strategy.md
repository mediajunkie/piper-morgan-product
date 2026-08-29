# ADR-074: Encryption at Rest Strategy

**Status**: ACCEPTED (documenting already-shipped work) — written 2026-07-05 (Lead Dev) as part of #358's closure, retroactively recording the design + decisions behind work implemented 2026-06-20 and live-verified on alpha 2026-06-25. No new decision is made here; this is the durable record #358 asked for.

**Date of original implementation**: 2026-06-20 (Dimension A + B code); 2026-06-25 (Dimension B live-verified on alpha)

**Author**: Lead Developer

**Related**: #358 (SEC-ENCRYPT-ATREST, the originating issue), #1305 (JSON/JSONB structured-column encryption, deferred sibling), #1306 (uploaded-file content-at-rest, deferred sibling), #1185 (per-user LLM keys — the hosted multi-tenant floor this ADR's Dimension A enables), ADR-058 (multi-tenancy isolation, composes at the credential layer)

---

## Context

Piper stores two categories of sensitive data in Postgres that need protection against a database-level compromise:

1. **User secrets** — API keys / integration credentials (Dimension A). Originally kept exclusively in the macOS Keychain, which does not exist on the hosted Linux droplet — a hard blocker for #1185 (per-user LLM keys on a hosted, multi-tenant instance).
2. **Content fields** — free-text conversation/artifact data that could contain PII (Dimension B). The originating issue's field list (written Nov 2025) predated several schema changes and named columns that no longer exist (`conversations.content`, `uploaded_files.content`, `conversation_turns.user_content`) — the real schema was reconciled during implementation (2026-06-20).

## Decision

### The primitive: AES-256-GCM with per-field HKDF subkeys

One reusable service, `FieldEncryptionService` (`services/security/field_encryption.py`), used by both dimensions:

- **AES-256-GCM** — authenticated encryption (confidentiality + tamper-detection via the GCM tag; a wrong key or tampered ciphertext raises, never silently returns garbage).
- **Per-field subkeys via HKDF-SHA256** — one master key (`ENCRYPTION_MASTER_KEY`, base64-encoded 32 bytes, sourced from the environment) derives an independent subkey per `context` label (e.g. `"user_api_keys.secret"`, `"conversations.preview"`), so compromise or rotation of one field's subkey doesn't cross-contaminate others.
- **Unique random nonce per encryption** — never reused under one key.
- Master key, derived subkeys, nonces, and plaintext are never logged (`__repr__` is key-safe by construction).

### Dimension A — user-secret store (the #1185 enabling floor)

`user_api_keys.encrypted_secret` (additive column, migration `a358encsecret`) + `UserAPIKeyService` (`services/security/user_api_key_service.py`):

- **Write**: dual-write — stores to the OS keychain (when available, e.g. local dev) AND to `encrypted_secret` (when a master key is configured), so the same code path works on a dev Mac and the keychain-less Linux droplet.
- **Read**: prefers `encrypted_secret` (decrypt via `FieldEncryptionService`) when both a stored value and a master key are present; falls back to the keychain otherwise (legacy rows, or a key-less local-dev environment).
- No master key configured → keychain-only, unchanged from pre-#358 behavior (graceful, not a hard failure).

### Dimension B — content-field encryption

`EncryptedString`, a SQLAlchemy `TypeDecorator` (`services/security/encrypted_types.py`), applied to 4 real free-text columns (the reconciled, actual schema — not the stale Nov-2025 list): `conversation_turns.user_message`, `conversation_turns.assistant_response`, `artifacts.content`, `conversations.preview`.

- **Version-marker prefix** (`PMENC1:`) distinguishes encrypted values from legacy plaintext — a column is safe to read during a backfill (mixed plaintext + ciphertext rows) and behaves strictly once every row carries the marker (an unmarked value is legacy plaintext; a *marked* but undecryptable value is a real error, never silently returned).
- **No master key configured** → plaintext passthrough on write (logged once), so pre-key/local-dev environments keep working unmodified. The backfill script (`scripts/backfill_encrypt_content_358b.py`) refuses to run without a key, so production can never silently persist plaintext *under* the encrypted marker.
- No DDL changes — the column type stays `Text`; encryption is transparent at the ORM boundary.

### What's explicitly out of scope here (deferred, PM-approved 2026-06-20)

- **JSON/JSONB structured columns** (`conversations.context`/`topics`, `conversation_turns.entities`/`references`/`context_used`/`turn_metadata`, `patterns.pattern_data`) — whole-column encryption breaks queryability (e.g. the `topics` GIN index). Needs its own design decision (selective-field encryption vs. accept-queryability-loss vs. searchable encryption) → **#1305**.
- **On-disk uploaded-file content** — a storage-layer problem (files live at a `storage_path` on disk, not in a DB column), needing its own architecture decision (local envelope encryption vs. S3-style SSE vs. full-disk encryption) → **#1306**.

## Consequences

### Positive
- One encryption primitive serves both the credential store and content fields — no duplicated crypto code.
- The hosted/multi-tenant floor (#1185) is unblocked: user secrets can be stored durably without depending on a host-specific OS keychain.
- Zero-downtime, backward-compatible rollout for both dimensions (dual-write / marker-prefix passthrough) — no environment without the master key configured breaks.

### Negative / tradeoffs
- Dimension A is a dual-write (keychain + encrypted column) during the transition window, not yet a clean cutover — acceptable since the keychain path remains a safe fallback, not a liability.
- Structured/JSON data and file content are explicitly not covered by this ADR's scope (see #1305/#1306) — a reader auditing "is everything encrypted?" must check those separately.

## Verification evidence

- **Dimension A**: 9 unit/integration tests pass (`tests/security/test_user_api_key_service.py`), including a real encrypt-then-decrypt round-trip test and a keychain-fallback test, run against real Postgres. Re-verified 2026-07-05 (Lead Dev) with a freshly-generated master key.
- **Dimension B**: 22 unit tests (`tests/unit/services/security/test_field_encryption.py` + `test_encrypted_types_358b.py`), plus **live verification on the alpha droplet** (2026-06-25): `ENCRYPTION_MASTER_KEY` present, `FieldEncryptionService.from_env()` round-trips, `EncryptedString`'s save-path produces `PMENC1:`-marked ciphertext and its load-path restores plaintext — confirmed in-container against the live key (no secrets logged during verification).
- **Performance**: ~15µs/field decrypt overhead, sub-millisecond per realistic read (2026-06-20 benchmark) — well within the issue's <5%/<10% read/write overhead targets.
- **Dimension A live-alpha verification**: NOT yet done as of this ADR's writing — dimension B was verified live on the droplet 2026-06-25; dimension A's equivalent live check (confirming a real user's key round-trips via `encrypted_secret` on the actual hosted instance, not just locally) is the one remaining item, requiring droplet access.

## What this ADR is NOT

- Not a commitment to encrypt JSON/JSONB columns or file content — those are #1305/#1306's separate design decisions.
- Not a multi-tenancy ADR — composes with ADR-058 at the credential layer but doesn't alter it.
- Not evidence that dimension A has been proven on the live hosted instance — only dimension B has that specific verification as of this writing.
