# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-20 ~07:51 PT (after the 0.8.8 deploy + the RECONNECT #1162 reconciliation surfaced). Sole lead.

## ▶ PENDING PM DECISION (blocks the next major work — RECONNECT build)
**RECONNECT Phase-0 referent reconciliation** — surfaced to PM 2026-06-20. Decision-a (and my scope-doc §12 + this carry-forward) labeled "#1162 = cred-decoupling, the RECONNECT foundation" — but **#1162 is actually hosted-distro EXPLORATION** ("explore hosting MCP/plugins/marketplace"; parent epic #1145 CLOSED; a distribution concern). Verified-from-GitHub corrected mapping awaiting PM confirm:
- **RECONNECT Phase-0 foundation** = **#1185 identity core** (UUID-bearer per-user auth — WS-9 depends on it) + **#1229** (WS2 cred model — already RECONNECT-native, no reassignment).
- **Distribution-lane (M5)** = **#1162 + #1282** (plugin packaging) **+ #1278** (Fly) — all hosting/distribution (consistent with decision-a keeping #1278 out).
- Gap: the buildable cred-decoupling work (PA option-a plan, `dev/2026/06/07/pa-option-a-decouple-credential-plan-2026-06-07.md`) has no own issue — may need one.
- **On PM confirm**: fix §12 + re-ping Architect (ADR-070 phasing memo referenced #1162) + start **#1185 identity core**.

## ▶ STATE
- **#1299 DONE — 0.8.8 LIVE + healthy on alpha** (07:34 PT). version 0.8.8, sqlite 3.40.1, schema at head (`a1273coretables`), /health 200. Three layered fixes: pyobjc markers + Dockerfile bullseye→bookworm + the never-run migrate (DB was 7 behind — alembic.ini hardcodes localhost:5433). Fix on main + cherry-picked to production (`5401a139c`). (a)+(b) folded into #1299 (kept OPEN). PA notified (`940837b1c`). Runbook corrected (the broken migrate-mitigation). Rollback assets retained on droplet.
- **D1 CLOSED** (#1297). Sequence: RECONNECT → M4 → M5 → 0.9.0.
- **alpha** = DO droplet 146.190.151.63 / root@piper-alpha; docker-compose /opt/piper; Caddy→app:8001 (gate → /health 401); deploy = `/opt/piper/deploy.sh`. Now on **0.8.8**. Runbook: `docs/internal/operations/alpha-deployment-runbook.md`.
- RECONNECT 9 WS: WS1 #1226/#1199 · WS2 #1229 · WS3 #1230 · WS4 #1231 · WS5 #1232(ADR-070 build target) · WS6 #1201 · WS7 #1109/#1110 · WS8 #1220 · WS9 #1233. Scope: `connector-refactor-sprint-scope-2026-06-14.md` (§12 = decision-a — needs the #1162 correction post-PM-confirm).
- #1289 standup-skill swap → PA. #1296 mail-send residue (CIO #1259 follow-on).
- **Cron 50daabfb** armed (`17 22,7,10,13,16,19`). Mailbox = `scripts/mail-send.sh` (push-to-ref).

## ▶ Owed / queued (calmer-cycle)
- **Agent-360 v0.3 fielding (HOST)** — OWED Lead response memo (June-10 backstop, now overdue). **VERIFY still wanted before writing** (10 days stale; may be closed/superseded). `dev/active/agent-360-questionnaire-v0_3.md`.
- **Standing-items doc is stale** (June-3 / M2-M3 framing) — refresh to RECONNECT-era when calm.

## ▶ Methodology this session
- Deploy = outward-facing → confirm before irreversible; back up config + rollback-tag image + snapshot code BEFORE deploying; verify-and-rollback on crash-loop.
- alembic.ini hardcodes localhost:5433 → in-container migrate silently fails every deploy (#1299 (a)). Run the migrate with the app's real engine URL (temp-script — see runbook footgun).
- Investigate-before-extending caught the #1162 mislabel before building on it (read the issue, not the label).
