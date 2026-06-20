# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-20 ~13:35 PT (after #358 secret-store floor shipped). Sole lead.

## ▶ NEXT — prioritization call (surfaced to PM)
The BYO-key hosted floor is built (#1185 + #358-floor done). Next (PM to pick):
- **Caddy-gate removal** (#1162) — the LAST #1185 hosted-beta gate; PM + Arch decision (JWT identifies users now).
- **#358 dimension B** — content/PII encryption (conversations/files/patterns) + ADR-043; the M5-compliance bulk (reuses FieldEncryptionService).
- **Another RECONNECT WS** (#1229 WS2, etc.).

## ▶ DONE (2026-06-20 — big session)
- **#1299 — 0.8.8 LIVE on alpha** (3-layer fix: bookworm + pyobjc + never-run migrate).
- **#1162 reconciliation + board** (#1162→SKUNK; #1300 BYOC-CRED-DECOUPLE filed→M5; §12/decisions.log/Architect).
- **#1185 (per-user keys)** — Phase 1 done+tested (`resolve_request_api_key`, /intent wired, 12 tests). Functionally complete; encrypt-at-rest gate now MET via #358. Last gate: Caddy-gate (#1162).
- **#358 secret-store FLOOR (A) — DONE+tested+committed (`99299f6f1`)**: P1 `FieldEncryptionService` (AES-256-GCM + HKDF, 9 tests); P2 encrypted `user_api_keys.encrypted_secret` + migration `a358encsecret` (applied+validated) + `UserAPIKeyService` integration + keychain fallback (9 tests). Per-user keys encrypt-at-rest, portable to hosted Linux. Dimension B (content/PII) + ADR-043 deferred (M5).
- Pre-existing fixture bug fixed (`test_users` string-id vs UUID, silently red since #262); CI-coverage chip spun off (task_4cd9f9bc).
- Agent-360 retired (false-positive).

## ▶ STATE / refs
- **alpha** on 0.8.8 (DO droplet; runbook `docs/internal/operations/alpha-deployment-runbook.md`).
- **#358 code**: `services/security/field_encryption.py` + `user_api_key_service.py` + `models.py` (encrypted_secret) + migration `a358encsecret`. `ENCRYPTION_MASTER_KEY` env (base64 32B) — **MUST set on the hosted box**; `docs/security/key-management.md`.
- **#1185 code**: `services/llm/request_key.py` (`resolve_request_api_key`) + `intent.py:338`.
- RECONNECT 9 WS + Phase-0 = #1185(done)+#1229+ADR-070. Sequence: RECONNECT → M4 → M5 → 0.9.0.
- **Cron 50daabfb** armed. Mailbox = `scripts/mail-send.sh`.

## ▶ Methodology this session
- **Investigate-before-extending** repeatedly paid off: caught the #1162 mislabel; #1185 was 90% pre-built; #358 greenfield; the pre-existing fixture bug.
- TDD for security-critical crypto (FieldEncryptionService 9 tests; tamper / per-field / no-leak).
- Postpone-with-a-specific-reason (PM 6/20): deferred #358 dimension B (separable/M5) + the #1185 full-route e2e test (DB-harness) — both tracked.
