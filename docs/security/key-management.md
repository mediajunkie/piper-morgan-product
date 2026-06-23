# Key Management — Encryption at Rest (#358)

The `FieldEncryptionService` (`services/security/field_encryption.py`) provides AES-256-GCM
field encryption with HKDF per-field subkeys. This doc covers the master key, rotation, and
the future AWS-KMS path.

## Master key (KEK)
- **Source**: `ENCRYPTION_MASTER_KEY` env var — base64 of 32 random bytes (AES-256).
- **Generate**: `python -c "import os,base64; print(base64.b64encode(os.urandom(32)).decode())"`
- Set per environment (local `.env`, the hosted droplet `.env`). **Never commit it.**
- **Absent** → `FieldEncryptionService.from_env()` returns `None`; callers fall back (local
  dev → OS keychain). On the **hosted Linux box the env var MUST be set** — there is no OS
  keychain there, so the encrypted store is the only per-user-secret path.

## Per-field subkeys
- Each encrypted field derives its own subkey via `HKDF-SHA256(master_key, info=context)`,
  where `context` is a stable label like `"user_api_keys.secret"`.
- Compromise/rotation of one field's subkey doesn't expose others; the master key is the
  single rotation point.

## Token format
`base64(nonce[12] ‖ ciphertext ‖ GCM-tag)` — AES-256-GCM (authenticated; tamper-evident).
A unique random nonce per encryption (never reused under one key).

## Rotation procedure
1. Generate a new master key (above).
2. Online re-encrypt: read each stored field with the **old** key, write with the **new**
   key, in a migration pass. Retain the old key until the pass completes + verifies.
3. Swap `ENCRYPTION_MASTER_KEY`; verify reads.

## Future: AWS KMS (#482)
KEK-from-env is the current floor. **#482** migrates the master key to AWS KMS (envelope
encryption: KMS holds the KEK; the app fetches a data key). `FieldEncryptionService` is
unchanged — only the loader moves (`from_env` → a KMS loader).
