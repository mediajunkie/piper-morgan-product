# Lead Dev — 2026-06-20 (Saturday)

**Role**: Lead Developer · **Tool**: Claude Code · **Model**: Opus 4.8 (1M)
**Cron**: 50daabfb (`17 22,7,10,13,16,19`) · **Worktree**: interesting-beaver-7ee19c · sole lead

## START (06:08 PT)
- 06-19 closed OK (`DAY-CLOSED: 2026-06-19` ✓). Synced clean. Cron armed (one job, correct expr — Gap-C OK).
- Inbox: PA's `alpha-deploy-runbook-gap` memo — **already actioned last night** (runbook written + reply sent + #1299 filed) → moved to read/.
- alpha healthy on **0.8.7** (clean rollback last night; 0.8.8 deferred to #1299).

## Today (PM-engaged — weekend prime time)
1. **RECONNECT sprint dive** (PM diving in when settled). Phase-0 reconciliation: fold PA's BYOC near-term map (`byoc-nearterm-work-2026-06-19.html` + `byoc-stack`) + the ratified identity model (UUID-bearer-MVP → email+magic-link-1.0) into the RECONNECT WS issues + scope doc (`connector-refactor-sprint-scope-2026-06-14.md`); settle the RECONNECT-vs-M5 boundary (BYOC backend foundation #1162/#1278/#1185 not in RECONNECT scope) — loop Architect (ADR-070). 9 WS map in carry-forward.
2. **#1299** — 0.8.8 alpha-deploy fix (pyobjc reqs markers in repo + chromadb/sqlite3 Dockerfile) → redeploy via the runbook. PM: "sort it today." Offered PA the pyobjc part.

## Fire (06:23, RECONNECT dive) — Phase-0 reconciliation done
PM dove into RECONNECT. Reconciled it vs PA's BYOC Phase-2a (the byoc-stack/nearterm diagrams + the ratified UUID-bearer identity). **Decision (a) — PM-ratified:** pull #1162 (cred-decoupling) + #1185 (identity core) INTO RECONNECT as Phase-0/1 foundation (PM reassigning the issues); #1278 (Fly) stays distribution-lane. WS-9 reframed (key connector config to the BYOC identity, not a legacy UUID merge). Captured: scope-doc §12 (`eff741438`) + decisions.log; Architect looped (`b12b80141`, ADR-070 phasing fold-in). Next: PM's pick — #1162 (RECONNECT foundation, ADR-independent) or #1299 (0.8.8 deploy fix).

## #1299 — 0.8.8 deploy FIXED + live on alpha (07:34 PT)

PM picked #1299 first ("go with your rec"). Root-caused + fixed the 0.8.8 deploy; **0.8.8 is now live + healthy on alpha** (version 0.8.8, sqlite 3.40.1, schema at head `a1273coretables`, internal `/health` 200; external 401 = Caddy gate as designed).

**Three layered issues (not the two #1299 first guessed):**
1. pyobjc markers lost in `requirements.txt` → Linux build fail. Restored (`requirements.txt:226-230`).
2. Dockerfile drift `slim-bullseye`→`slim-bookworm` (sqlite 3.34.1→3.40.1; chromadb needs ≥3.35). The #1299 pysqlite3/pin-chromadb guesses were red herrings (chromadb same 0.4.22 throughout). `Dockerfile:6-10`.
3. **The migrate had never run** — droplet DB was **7 migrations behind** (entire D1/RECONNECT schema: documents/#1238, owner_id/#1252, project_integrations/#1267, intents/workflows/tasks/stakeholders/#1273). Cause: `alembic.ini:87` hardcodes `localhost:5433` → in-container migrate connects to the wrong host, has silently failed every deploy. Ran it manually with the app's real engine URL; DB → head; restarted app for a clean init. App was "healthy" but hollow before this.

Fix on `main` + cherry-picked to `production` (`5401a139c`). Deploy ran via the runbook's safe procedure (archive production → /opt/piper → restore config → deploy.sh → verify); rollback assets retained on droplet.

**Per PM (this fire):**
- Folded **(a)** alembic.ini env-driven URL + **(b)** deploy.sh migrate hardening into **#1299** (kept OPEN; body + title + evidence-comment updated per close-issue-properly).
- Notified PA (`memo-lead-to-pa-cc-pm-0.8.8-now-live-on-alpha`, `940837b1c`) — flagged (a) as a RECONNECT "config has no stable home" instance for PA's connector/config lane.
- Corrected the runbook footgun: the documented mitigation (`re-run alembic upgrade head`) was itself broken (same localhost:5433 bug); replaced with the real-URL temp-script mitigation.

Next: RECONNECT **#1162** (cred-decoupling — the Phase-0 foundation, ADR-independent).
