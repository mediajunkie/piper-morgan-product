# #358 Dimension B — Content/PII Encryption-at-Rest — Gameplan

**Issue**: #358 (SEC-ENCRYPT-ATREST), dimension B (content/PII). Dimension A (secret-store floor) shipped 2026-06-20 (`99299f6f1`).
**Date**: 2026-06-20. **Author**: Lead Dev. **PM scope-approved**: 2026-06-20.

## Problem
Real user content sits in the DB as plaintext-at-rest (alpha already has live conversation data). Compliance gap for hosted beta. Dimension A built the AES-256-GCM primitive (`FieldEncryptionService`) + encrypted the user-secret store; B applies that primitive to the free-text content columns.

## Scope (PM-approved 2026-06-20, corrected against the real schema)
**Verify-before-extending finding**: the issue's "Fields Encrypted" list was ~60% stale — `conversations.content`, `uploaded_files.content`, and `conversation_turns.user_content`/`assistant_content` **don't exist**; `pattern_data` is JSON. Corrected targets below.

**IN scope — the free-text Text columns (the clear PII):**
1. `conversation_turns.user_message` (Text) — user messages
2. `conversation_turns.assistant_response` (Text) — AI responses
3. `artifacts.content` (Text) — generated/document content
4. `conversations.preview` (Text) — conversation preview snippet

**DEFERRED (separate follow-ups, each its own tradeoff — PM-confirmed):**
- **JSONB/JSON structured columns** (`conversations.context`/`topics`, `conversation_turns.entities`/`references`/`context_used`/`turn_metadata`, `patterns.pattern_data`) — encrypting breaks GIN-index queryability. → its own issue.
- **On-disk file content** (`uploaded_files.storage_path` → disk) — storage-layer encryption, not a DB-column problem. → its own issue.

**Safe to encrypt transparently**: confirmed no raw text-search (ILIKE/ts_query/.contains) on the target columns → an ORM-layer `TypeDecorator` won't break any query path.

## Mechanism — `EncryptedString(TypeDecorator)`
A SQLAlchemy `TypeDecorator` (`impl=Text`) reusing `FieldEncryptionService`:
- `process_bind_param` (save): `MARKER + service.encrypt(value, context)`; `None` → `None`; no encryptor (key unset) → plaintext passthrough (log once).
- `process_result_value` (load): marker present → `service.decrypt(stripped, context)` (`DecryptionError` → **RAISE**: tamper/wrong-key); marker absent → plaintext passthrough (pre-migration row).
- **Marker prefix** (`PMENC1:`) distinguishes ciphertext from plaintext → **mixed-state safe** during migration + **auto-strict** post-migration (no code-flip needed: once every row is marked, an unmarked/undecryptable value is a real error). Collision with genuine plaintext starting with the marker is astronomically unlikely; the backfill reads RAW (bypasses the decorator) to avoid a round-trip; residual risk documented.
- `cache_ok = True`. Per-column `context` (e.g. `"conversation_turns.user_message"`) → per-field HKDF subkey (cross-field ciphertext isn't swappable).

## Phases (TDD)
**Phase 1 — `EncryptedString` TypeDecorator** (`services/security/encrypted_types.py`, NEW): the decorator + marker logic. Tests: round-trip; None-safe; plaintext-passthrough (unmarked); marked-tamper→raise; no-encryptor→passthrough; per-context isolation; cache_ok. (~9 tests)

**Phase 2 — Apply to the 4 columns**: change `Column(Text...)` → `Column(EncryptedString(context=...))` on the 4 targets. **NO Alembic schema migration** (impl stays Text — DB DDL unchanged). Tests: ORM save→load round-trip per column writes ciphertext to the raw row + returns plaintext to the app; raw-SQL read shows marker+ciphertext. **Wiring test (#490 learning)**: real import of `EncryptedString` into the model columns + real `FieldEncryptionService` (no mock) — proves the decorator is actually wired, not just unit-correct in isolation.

**Phase 3 — Zero-downtime data backfill** (`scripts/backfill_encrypt_content_358b.py`, NEW): per target table, raw-read unmarked rows → encrypt → raw-write (marked), batched + idempotent (skip already-marked) + resumable. **NO downtime** (no DDL; read-path tolerates mixed state). Validate on a test DB with seeded plaintext. Tests: idempotent (re-run = no-op); mixed-state read; row count preserved.

**Phase 4 — Perf validation + regression + close-out**: measure read overhead (<5% target) on a representative query; **regression gate** — existing `conversation` / `conversation_turn` / `artifact` test suites stay green post-change; close #358 dimension B properly (description checkboxes + evidence); file the 2 deferred follow-up issues (JSONB, file-content).

## Post-completion side-effects (Phase 0.8)
- Existing target rows → ciphertext-at-rest (after backfill); raw row = `PMENC1:`+base64. App layer unchanged (sees plaintext).
- No downstream feature-state change (no `setup_complete`-style flag) — encryption is transparent to all readers.
- `ENCRYPTION_MASTER_KEY` becomes **load-bearing for reads** of encrypted rows: lose it → marked rows are unrecoverable. Key custody is the operational dependency (`docs/security/key-management.md`; #482 = AWS-KMS path).

## STOP conditions
- `ENCRYPTION_MASTER_KEY` unset → encryption silently no-ops (passthrough). The **backfill MUST refuse to run without the key** (else it'd "succeed" writing plaintext). HARD STOP.
- Backfill not idempotent/resumable → STOP (live data).
- Perf >5% read overhead → STOP, surface to PM.
- Any target column turns out to be searched via raw SQL (re-verify before Phase 2) → STOP.

## Rollback
- Column stays Text + marker distinguishes ciphertext → rollback = stop encrypting (revert the Column types); existing marked rows still decrypt on read as long as the key is present. Full reverse = a decrypt-all backfill (mirror of Phase 3).

## Success criteria
- The 4 columns encrypt-at-rest (raw row = marker+ciphertext; app sees plaintext).
- Existing rows backfilled; mixed-state safe throughout.
- No query path broken; <5% read overhead.
- 2 deferred follow-ups filed.
- #358 dimension B closed with evidence.
