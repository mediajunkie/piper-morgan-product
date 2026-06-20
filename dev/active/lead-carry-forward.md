# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-20 ~10:46 PT (after #1185 Phase 1 + the def-of-done reframe). Sole lead.

## ▶ PENDING PM DECISION (next-priority pick)
#1185's core is done (below). Next is a fresh prioritization — surfaced to PM, awaiting pick:
- **#358 encrypt-at-rest** (Lead rec) — the HARD blocker for safe hosted BYO-key (`keyring` isn't encrypted on the headless droplet). Its own substantial SEC build → own audit-cascade.
- **Caddy-gate removal** (#1162) — PM + Arch architectural decision (JWT now identifies users; the static gate can come off).
- **Another RECONNECT WS** (e.g. #1229 WS2 cred-model).

## ▶ DONE THIS SESSION (2026-06-20)
- **#1299 — 0.8.8 LIVE on alpha** (3-layer fix: Dockerfile bullseye→bookworm + pyobjc markers + the never-run migrate). (a)+(b) folded into #1299 (OPEN). PA notified. Runbook corrected (the broken migrate-mitigation).
- **#1162 reconciliation + board corrected**: #1162→SKUNK (was mislabeled cred-decoupling; it's hosted-distro exploration), #1300 (BYOC-CRED-DECOUPLE, the real decouple) filed→M5, #1185 stays RECONNECT. §12 CORRECTION + decisions.log + Architect re-pinged.
- **#1185 audit cascade (gates 1-2) + Phase 1 DONE**: per-user key resolution (`resolve_request_api_key`, header>stored>server) wired at /intent on the #1162 rail; 12 tests. **Reframe: #1185 was ~90% pre-built** (JWT auth + setup.py web-capture existed; only /intent calls LLM → 2a no-op). Def-of-done: #1185 resolution = complete+tested; hosted-beta SAFETY gated on #358 (encrypt — hard dep) + the Caddy-gate decision. Full-route e2e test tracked.
- Agent-360 owed-item retired (false-positive).

## ▶ STATE / refs
- **alpha** on **0.8.8** (DO droplet; deploy=`/opt/piper/deploy.sh`; runbook: `docs/internal/operations/alpha-deployment-runbook.md`).
- #1185 code: `services/llm/request_key.py` (`resolve_request_api_key`), `web/api/routes/intent.py:338` (binding). Tests: `tests/unit/services/llm/test_request_key_resolve_1185.py`. Gameplan: `dev/2026/06/20/1185-gameplan.md`.
- **#358 finding**: `KeychainService` uses Python `keyring` (macOS Keychain locally → encrypted; the *headless-Linux* backend is NOT guaranteed encrypted → the hosted gate).
- RECONNECT 9 WS + Phase-0 = #1185(done)+#1229+ADR-070. Scope: `connector-refactor-sprint-scope-2026-06-14.md` (§12 corrected). Sequence: RECONNECT → M4 → M5 → 0.9.0.
- **Cron 50daabfb** armed (`17 22,7,10,13,16,19`). Mailbox = `scripts/mail-send.sh`.

## ▶ Methodology this session
- **Investigate-before-extending** repeatedly paid off: caught the #1162 mislabel; found #1185 was 90% pre-built (read the code, not the issue's 4-part framing); found #358 is a real hosted gate (the keyring backend).
- Deploy = outward-facing → confirm + back up + verify-and-rollback. `alembic.ini` hardcodes localhost:5433 (#1299 a) → migrate silently failed every deploy.
- Transient SSH port-22 blip on a verify-fetch (10:46) — push had already landed; SSH-over-443 workaround in CLAUDE.md if it recurs.
