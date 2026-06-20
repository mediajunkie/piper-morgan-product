# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-20 ~09:45 PT (post #1162 reconciliation + board correction). Sole lead.

## ▶ NEXT (RECONNECT Phase-0 — now unblocked)
The #1162 reconciliation is RESOLVED (below). RECONNECT Phase-0 foundation = **#1185 (identity core)** + **#1229 (WS2 cred-model)** + Architect's **ADR-070**. Next build (PM to pick / confirm sequencing):
- **#1185 identity core** — prep DONE (gap verified: `user_api_keys` `models.py:190` covers Anthropic → no schema change; core change = user_id-aware key resolution in `services/llm/clients.py` / `LLMConfigService`). Needs a gameplan + audit-cascade gate before building. May split (identity → RECONNECT vs per-user-LLM-key → hosted-beta) — confirm scope with PM.
- **#1229 WS2** — unified connector credential model (RECONNECT-native).
- WS5 (#1232) waits on Architect's ADR-070.

## ▶ DONE THIS SESSION (2026-06-20)
- **#1299 — 0.8.8 LIVE on alpha** (version 0.8.8, sqlite 3.40.1, schema at head `a1273coretables`, /health 200). 3-layer fix: pyobjc markers + Dockerfile bullseye→bookworm + the never-run migrate (alembic.ini hardcodes localhost:5433 → (a)+(b) folded into #1299, OPEN). Fix on main + production (`5401a139c`). PA notified (`940837b1c`). Runbook corrected.
- **#1162 reconciliation RESOLVED + board corrected (PM-approved)**: #1162 (hosted-distro exploration, NOT cred-decoupling) → SKUNK; filed **#1300 (BYOC-CRED-DECOUPLE)** → M5 (the real decouple work, PA option-a); #1185 stays RECONNECT; #1278 stays M5. Corrected scope-§12 (CORRECTION block) + decisions.log + re-pinged Architect (`f8f49c61e` — ADR-070 Phase-0 = #1185+#1229, drop #1162). M5 refactor deferred ("when we get to M5" — PM).
- Agent-360 owed-item retired (false-positive — Lead already responded Jun 4).

## ▶ STATE / refs
- **alpha** = DO droplet 146.190.151.63 / root@piper-alpha; docker-compose /opt/piper; deploy = `/opt/piper/deploy.sh`. On **0.8.8**. Runbook: `docs/internal/operations/alpha-deployment-runbook.md`.
- RECONNECT 9 WS: WS1 #1226/#1199 · WS2 #1229 · WS3 #1230 · WS4 #1231 · WS5 #1232(ADR-070) · WS6 #1201 · WS7 #1109/#1110 · WS8 #1220 · WS9 #1233. Scope: `connector-refactor-sprint-scope-2026-06-14.md` (§12 corrected). Sprint = Projects-v2 **Sprint** field (project 1 "Building Piper Morgan").
- Sequence: RECONNECT → M4 → M5 → 0.9.0.
- **Cron 50daabfb** armed (`17 22,7,10,13,16,19`). Mailbox = `scripts/mail-send.sh` (push-to-ref).

## ▶ Methodology this session
- Deploy = outward-facing → confirm before irreversible; back up + rollback-tag + snapshot first; verify-and-rollback on crash-loop.
- alembic.ini hardcodes localhost:5433 → in-container migrate silently fails every deploy (#1299 (a)). Run migrate with the app's real engine URL (runbook footgun).
- **Investigate-before-extending caught the #1162 mislabel** before building on it (read the issue, not the label). The label propagated from PA's BYOC diagrams → §12 → carry-forward — fixed at all three.
