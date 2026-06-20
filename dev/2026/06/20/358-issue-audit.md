# Audit: #358 (SEC-ENCRYPT-ATREST) against feature.md — cascade gate 1

**Date**: 2026-06-20 · **Auditor**: Lead Dev
**Scope this run**: the secret-store **FLOOR** (the #1185 enabler) — FieldEncryptionService + encrypted user-secret store. Content/PII compliance = **deferred** (separable; M5).

| Template Requirement | Status | Notes / Action |
|---|---|---|
| Priority / Labels / Milestone / Related | ✅ | P0/critical; size:large; M5; related #1185/#1162. |
| Problem Statement | ✅ | Strong. **PA's 2026-06-10 update is the authoritative current-state** (the original "current state" is partly stale). |
| Goal | ✅ | AES-256-GCM field encryption, <5% read overhead, zero-downtime migration. |
| What Exists / Missing | ⚠️→reconciled | **ORIGINAL IS STALE**: claims `services/security/encryption.py` (Fernet) exists — it does **NOT** (verified by grep: no Fernet / encryption.py anywhere in services/). PA's update + my grep confirm **greenfield**. Action: treat PA's update as authoritative; the original "What Exists ✅ Fernet" is false. |
| Requirements / Phases | ✅ | Phase 0–4 + Z, well-structured (the original's phases are a sound skeleton). |
| Acceptance Criteria | ✅ | Functionality / Fields / Migration / Testing / Performance / Security / Docs. |
| `api_keys.key_value` migrate task | ❌→drop | No `api_keys` table, no `key_value` column (only `user_api_keys` with `key_reference` = a keychain id). The "migrate api_keys.key_value from Fernet" task has **no referent**. **Replace** with: encrypt the per-user secret store (`user_api_keys` → an encrypted-at-rest secret column). |
| Completion Matrix / Testing Strategy / Security | ✅ | Present + example tests (`test_field_encryption.py`, `FieldEncryptionService(master_key)`). |

## Scope decision (this run)
#358 has TWO separable dimensions sharing ONE primitive (`FieldEncryptionService`):
- **(A) Secret-store FLOOR** — the #1185 enabler: build `FieldEncryptionService` + encrypt the per-user secret store, portable **off the macOS keychain onto the hosted Linux DB** (the hosted box has no keychain → this is the enabling floor, not optional). **← DO NOW.**
- **(B) Content/PII compliance** — `conversations.content`, `conversation_turns.*`, `uploaded_files.content`, `patterns.pattern_data` + the zero-downtime shadow-column data migration (SOC2/GDPR). Larger; M5-compliance. The primitive (A) builds serves it later. **← DEFER** (specific reason: separable + not the #1185 blocker; same primitive reused).

## Verdict
Issue is well-formed + PA-reconciled. Gate 1 = the stale-Fernet correction + the dropped `api_keys` task + the (A)/(B) scope split (above). **Proceed to gate 2** (gameplan, scoped to A). The (A)/(B) split is the key thing to surface to PM at the gameplan gate.
