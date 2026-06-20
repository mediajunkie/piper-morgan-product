# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-19 STOP (~00:20 PDT 6/20, after the alpha 0.8.8 deploy attempt). Sole lead.

## ▶ TOMORROW'S OPENERS (priority order)
1. **RECONNECT Phase-0 reconciliation** — fold PA's BYOC near-term map (`docs/internal/architecture/current/diagrams/byoc-nearterm-work-2026-06-19.html` + `byoc-stack-2026-06-19.html`) + the ratified identity model (UUID-bearer-MVP → email+magic-link-1.0) into the RECONNECT WS issues + scope doc (`connector-refactor-sprint-scope-2026-06-14.md`). Settle the RECONNECT-vs-M5 boundary — the BYOC backend foundation (#1162 cred-decoupling, #1278 Fly, #1185 BYO-KEY) is NOT in RECONNECT's scope → **loop Architect** (ADR-070). 9 WS: WS1 #1226/#1199 · WS2 #1229 · WS3 #1230 · WS4 #1231 · WS5 #1232(ADR-070 build target) · WS6 #1201 · WS7 #1109/#1110 · WS8 #1220 · WS9 #1233.
2. **#1299 — fix the 0.8.8 alpha-deploy blockers** + redeploy: (a) restore `; sys_platform=="darwin"` markers on the 3 pyobjc lines in the REPO requirements.txt; (b) real blocker = chromadb needs sqlite3>=3.35, image too old → pysqlite3-binary swap OR pin chromadb OR upgrade base-image sqlite3. Redeploy via the runbook. **alpha healthy on 0.8.7 now.**

## ▶ STATE
- **D1 CLOSED** (#1297, 3 gates, 32/32). 0.8.8 cut (PA) but NOT live (#1299). Sequence: RECONNECT → M4 → M5 → 0.9.0.
- **alpha** = DO droplet 146.190.151.63 / root@piper-alpha; docker-compose /opt/piper; Caddy→app:8001 (gate → /health 401); deploy = `/opt/piper/deploy.sh`. Healthy on **0.8.7**. Rollback assets: `/root/alpha-deploy-backup-20260620-0633` + `piper-morgan-stable-app:rollback-20260619`. Runbook: `docs/internal/operations/alpha-deployment-runbook.md`.
- #1289 standup-skill swap → PA (adapter spec in #1289). #1296 mail-send residue (CIO #1259 follow-on).
- **Cron 50daabfb** armed (`17 22,7,10,13,16,19`). Mailbox = `scripts/mail-send.sh` (push-to-ref).

## ▶ Methodology this session
- Deploy = outward-facing → confirm before irreversible; back up config + rollback-tag the image + snapshot code BEFORE deploying; verify-and-rollback when it crash-loops.
- requirements.txt platform-marker discipline — a Mac `pip freeze` leaks pyobjc → Linux build fails.
