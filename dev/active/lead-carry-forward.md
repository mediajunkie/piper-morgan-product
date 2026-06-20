# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-20 ~15:10 PT (after #358 Dimension B code-complete). Sole lead.

## ▶ NEXT — gate-removal-safety investigation (task #35, agreed next-after-B)
Read-only investigation: which routes require vs optional auth (`/intent` is `get_current_user_optional` → reachable without the gate); what's exposed if the Caddy blanket basic-auth gate is removed; rate-limiting/abuse protection; whether auth must be made **required** OR BYO-key gates access. → bring PM + Arch a clear go/no-go. The REMOVAL *action* ties to the public-distribution milestone; the investigation is now.

## ▶ PENDING PM (non-blocking)
- **#358 close**: code-complete vs hold-for-deploy (LD leans *hold* — P0 compliance not truly satisfied until `ENCRYPTION_MASTER_KEY` + backfill land on alpha).

## ▶ DONE (2026-06-20 — big session)
- #1299 → **0.8.8 LIVE on alpha**; #1162 reconciliation + board (#1300 filed); #1185 Phase 1 (per-user keys, functionally complete).
- **#358 secret-store FLOOR (A)** — `FieldEncryptionService` + encrypted `user_api_keys` (`99299f6f1`).
- **#358 Dimension B — CODE-COMPLETE**: `EncryptedString` TypeDecorator (P1, 13 tests) → 4 content columns (P2, 3 tests, **no DDL**) → zero-downtime backfill (P3, 3 tests) → perf+close-out (P4). **112 regression green**. Commits `24d8b2044`/`cd591b12f`/`e0744131d`. Deferred → **#1305** (JSONB) + **#1306** (file-content). #358 evidence comment posted.

## ▶ STATE / refs
- **alpha** on 0.8.8 (does NOT yet carry #358-B — rides the next deploy). `ENCRYPTION_MASTER_KEY` (base64 32B) must be set on the box; backfill = `scripts/backfill_encrypt_content_358b.py`.
- **#358-B code**: `services/security/encrypted_types.py` (`EncryptedString`, `MARKER="PMENC1:"`) + `models.py` (4 cols) + the backfill script. Gameplan `dev/2026/06/20/358-dimension-b-gameplan.md`.
- **#1185 last gate**: Caddy-gate (#1162) — the investigation above informs it.
- **Cron 50daabfb** armed. Mailbox = `scripts/mail-send.sh`.

## ▶ Methodology
- **Investigate-before-extending** caught the #358-B target-list staleness (3 of 5 issue columns didn't exist; `pattern_data` is JSON) — the 4th such catch this session.
- TDD throughout; marker-prefix design → mixed-state-safe zero-downtime migration; **no DDL** (impl=Text → DB type unchanged).
