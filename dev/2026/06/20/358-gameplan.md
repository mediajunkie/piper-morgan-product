# Gameplan — #358 SEC-ENCRYPT-ATREST (secret-store FLOOR — the #1185 enabler)

**Issue**: #358 · **Scope this run**: **(A)** the secret-store floor — `FieldEncryptionService` + encrypted user-secret store. **(B)** content/PII compliance = **DEFERRED** (separable; M5; same primitive reused).
**Author**: Lead Dev · **Date**: 2026-06-20 · **Security-critical (P0)** — careful TDD; getting crypto wrong is worse than no crypto.

## ⭐ Reconciled state (gate 1)
No encryption-at-rest exists (no `encryption.py`, no Fernet, no KEK). Per-user secrets live in the macOS Keychain (`KeychainService`/`keyring`), keyed by user_id — **laptop-only; cannot work on the hosted Linux droplet.** So #358 is the *enabling floor* for hosted BYO-key (#1185), not compliance polish. The original body's "Fernet exists" + "api_keys.key_value" claims have no referent (PA's 2026-06-10 update corrects them).

## Phase -1 / 0 — Infra (verified)
- `cryptography==46.0.5` present → `AESGCM` + `HKDF` in `cryptography.hazmat`. ✅
- `user_api_keys.key_reference` (String, keychain id) — the column to supplement with an encrypted secret. ✅
- No `ENCRYPTION_MASTER_KEY` / KEK infra yet → Phase 1 establishes it. ✅
- **PROCEED.**

## Security design (load-bearing decisions)
- **AES-256-GCM** (authenticated encryption — confidentiality + tamper-detection via the GCM tag), via `cryptography.hazmat.primitives.ciphers.aead.AESGCM`. Don't hand-roll.
- **Per-field subkeys via HKDF-SHA256**: derive a subkey from `master_key` + a context label (`f"{table}.{field}"`) → leak/rotation of one context doesn't cross-contaminate.
- **Master key** from `ENCRYPTION_MASTER_KEY` env (32 bytes, base64). KEK-from-env now; **AWS-KMS path is #482** (documented, not built here).
- **Per-encryption random 12-byte nonce**; stored token = base64(nonce ‖ ciphertext+tag). Never reuse a nonce under one key.
- **Never log** master key, subkeys, plaintext, or nonce-with-key.

## Phases

### Phase 1 — FieldEncryptionService (the primitive; security-critical)
**Objective**: a reusable AES-256-GCM field encryptor with HKDF per-field subkeys.
**TDD (write first)**:
- [ ] round-trip: `decrypt(encrypt(pt, ctx), ctx) == pt`.
- [ ] tamper-detection: flipping a ciphertext byte → raises (GCM tag), never returns garbage.
- [ ] per-field isolation: ciphertext for ctx "a" won't decrypt under ctx "b".
- [ ] nonce-uniqueness: two encrypts of the same pt → different tokens.
- [ ] missing/short master key → clear init error (no silent weak key).
- [ ] no-leak: master key / plaintext never in `repr` / logs.
**Build**: `services/security/field_encryption.py` → `FieldEncryptionService(master_key)` with `encrypt(plaintext, context)` / `decrypt(token, context)`.
**Deliverables**: service + `tests/unit/services/security/test_field_encryption.py` (20+) + `docs/security/key-management.md` (rotation + KMS path).

### Phase 2 — Encrypted user-secret store (the #1185 floor)
**Objective**: per-user secrets encrypted-at-rest in Postgres, portable to the hosted box.
**Tasks**:
- [ ] Additive Alembic migration: `encrypted_secret` (Text, nullable) on `user_api_keys` (keep `key_reference` for back-compat/transition).
- [ ] `UserAPIKeyService.store_user_key`: encrypt secret (ctx `user_api_keys.secret`) → `encrypted_secret`; keychain still written during transition (or config-gated).
- [ ] `retrieve_user_key`: prefer `encrypted_secret` (decrypt) → fall back to keychain (local dev / pre-migration).
- [ ] No master key configured (local dev) → fall back to keychain; honest, don't 500.
**TDD**:
- [ ] store → row's `encrypted_secret` is not plaintext; retrieve → original.
- [ ] cross-user isolation preserved (existing `UserAPIKeyService` tests still green).
- [ ] keychain fallback when `encrypted_secret` absent.
- [ ] wiring: `retrieve_user_key` → the #1185 resolver gets the decrypted key.
**Deliverables**: migration + service updates + tests.

### DEFERRED — dimension (B): content/PII compliance
`conversations.content`, `conversation_turns.*`, `uploaded_files.content`, `patterns.pattern_data` + the zero-downtime shadow-column migration (SOC2/GDPR). Reuses the Phase-1 primitive. **Defer reason**: separable + not the #1185 blocker; the M5-compliance bulk. Tracked on #358.

## Conditional phases (template 0.5 / 0.6 / 0.7 / 0.8)
- **0.5 FE-BE Contract** — N/A this run (backend-only; no new UI/fetch). The hosted "configure your key" UX rides #1300/#1185's `/connect`, separately.
- **0.6 Data Flow** (multi-layer): **store** = `UserAPIKeyService.store_user_key(user_id, provider, secret)` → `FieldEncryptionService.encrypt(secret, ctx="user_api_keys.secret")` → `user_api_keys.encrypted_secret`. **retrieve** = `retrieve_user_key` → `encrypted_secret` present? decrypt : keychain-fallback. **master key** = `ENCRYPTION_MASTER_KEY` env → absent ⇒ keychain-only (local dev). Subkey = HKDF(master, ctx). `user_id` flows in from the #1185 resolver (already wired).
- **0.7 Conversation Design** — N/A.
- **0.8 Post-Completion side-effects** — after Phase 2: a stored key has a non-null `encrypted_secret`; `retrieve_user_key` prefers it; on the hosted box (no keychain) the encrypted path is the ONLY path. Migration is additive (`key_reference` retained) → reversible; no plaintext-key loss.

## Phase Z — Handoff & close
- [ ] ADR-043 (Encryption at Rest Strategy) created/updated; `docs/security/key-management.md` (rotation + #482 KMS path).
- [ ] Update #358: floor (A) done + tested; content/PII (B) deferred with reason; evidence. PM closes (or keeps open for B).
- [ ] Note in #1185 that its hosted-safety encrypt-at-rest gate is now satisfiable.
- [ ] Session log + decisions note.

## STOP conditions (security)
- `cryptography`'s AESGCM/HKDF behaving unexpectedly in a test → STOP (don't hand-roll).
- Master key would be logged anywhere → STOP.
- Migration risks plaintext-key loss → STOP (additive-only; no destructive drop this run).
- Weak/short master key accepted silently → STOP (must error).

## Effort
**Medium.** Phase 1 = careful primitive (small code, many security tests). Phase 2 = small (additive column + service wiring). (B deferred.)

## Subagent decision
**Solo TDD** — security-critical + the two phases share `field_encryption.py` + `user_api_key_service.py`. No fan-out.

## Refs
#358 body + PA 2026-06-10 update · #1185 (the consumer) · #482 (AWS-KMS — the later KEK path) · `cryptography` lib.
