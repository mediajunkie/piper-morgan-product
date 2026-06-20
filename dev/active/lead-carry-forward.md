# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-20 ~15:40 PT (after gate-removal investigation delivered). Sole lead.

## ▶ NEXT — all PM/Arch-gated (surfaced; awaiting calls)
- **#1307 fix** (`admin_compose` writable + auth-exempt) — GATED on PM: dev-only → env-gate (`dev_trust` pattern); prod-use → auth-protect. LD can do it in minutes once told. **Blocks #1162** gate removal.
- **#358 close** — PM: code-complete-now vs hold-for-deploy (LD leans *hold* — P0 not satisfied until key+backfill on alpha).
- **Rate-limiting** — new effort (none exists); SHOULD before public BYOC. Arch asked for approach preference.
- **Caddy gate removal (#1162)** — PM+Arch, AFTER #1307 + rate-limiting. Investigation = CONDITIONAL GO.
- (Deferred/M5) #1305 (JSONB enc), #1306 (file-content enc), #358-B prod deploy (key+backfill on alpha).

## ▶ DONE (2026-06-20 — very big session)
- #1299 → **0.8.8 LIVE on alpha**; #1162 reconciliation+board (#1300); #1185 P1 (per-user keys).
- **#358 floor (A)** + **#358 Dimension B CODE-COMPLETE** (`EncryptedString` + 4 cols + backfill; 19 new tests; 112 regression; commits …`e0744131d`). Deferred → #1305/#1306. #358 evidence comment posted.
- **Gate-removal-safety investigation** — CONDITIONAL GO; findings `dev/2026/06/20/gate-removal-safety-investigation.md`; blocker **#1307** filed; Arch mailed cc PM (`033960b6c`).

## ▶ STATE / refs
- **alpha** 0.8.8 (does NOT carry #358-B yet). `ENCRYPTION_MASTER_KEY` must be set on the box; backfill `scripts/backfill_encrypt_content_358b.py`.
- **Gate model**: `AuthMiddleware` (`web/app.py:61`) self-gates; the exempt list = the exposure surface; `admin_compose` (#1307) is the one hole.
- **#358-B code**: `services/security/encrypted_types.py` (`MARKER="PMENC1:"`) + `models.py` (4 cols) + the backfill. Gameplan `dev/2026/06/20/358-dimension-b-gameplan.md`.
- **Cron 50daabfb** armed. Mailbox = `scripts/mail-send.sh`.

## ▶ Methodology
- **Investigate-before-extending** — 4 catches this session (latest: #358-B target-list staleness). The gate-investigation found the `admin_compose` write-exposure (#1307) by reading the actual middleware, not assuming.
- TDD throughout; marker-prefix → mixed-state-safe zero-downtime migration; no-DDL (impl=Text).
