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

Next: RECONNECT **#1162** (cred-decoupling — the Phase-0 foundation, ADR-independent). *[corrected below — #1162 turned out to be mislabeled.]*

## RECONNECT #1162 reconciliation — referent mismatch found, surfaced to PM (07:51 PT)

Started to build the "#1162 cred-decoupling foundation" — but reading #1162 + #1185 first (investigate-before-extending) revealed **#1162 is hosted-distro EXPLORATION** ("explore hosting MCP/plugins/marketplace", parent epic #1145 CLOSED), NOT cred-decoupling. My §12 + carry-forward had propagated the mislabel. Verified-from-GitHub:
- #1162 = hosted-distro exploration · #1282 = plugin packaging/distribution · #1278 = Fly hosting → all **distribution-lane**.
- #1185 = BYO-KEY-MULTI-TENANT (per-user keys + per-user auth/identity) — the identity half is WS-9's actual dependency.
- #1229 = RECONNECT-WS2 cred model — already RECONNECT-native.

Decision-a kept #1278 OUT (hosting=distribution-lane); #1162 is hosting too → by that same logic it belongs with #1278, not in RECONNECT. **Corrected mapping surfaced to PM** (RECONNECT Phase-0 = #1185-identity + #1229; distribution = #1162+#1282+#1278) — awaiting confirm before building #1185 + fixing §12 + re-pinging Architect. Gap flagged: the buildable cred-decoupling work (PA option-a plan) appears to have no own issue.

Duty-cycle tick fired 07:17 mid-conversation — cron 50daabfb armed (1 job, Gap-C OK); sync clean; inbox empty; the 1 delta memo already actioned. Presence-aware hold on the #1162 thread; carry-forward rewritten to current state.

**Unblocked housekeeping while #1162 awaits PM:**
- **Agent-360 owed-item retired** (false-positive). Verified Lead already responded (in the 9/9 by Jun 4; HOST quotes Lead's §9.5 in the Jun-10 synthesis to PM). The standing-items "OWED" predated my Jun-4 response. Retired from standing-items + carry-forward; flagged the standing-items doc as broadly stale (M2/M3 era). (`e581b0768`)
- **#1185 prep** (de-risking the build #1162 gates — decision-independent, #1185 is the identity foundation either way): verified the open-Q — `user_api_keys` (`services/database/models.py:190`, `UniqueConstraint(user_id, provider)`) **already covers Anthropic** (provider field: "openai, anthropic, github, etc") → **NO schema change** needed for the per-user LLM key. Gap confirmed exactly as #1185 states: `services/llm/clients.py` → `LLMConfigService.get_api_key("anthropic")` (instance-level, no `user_id`) → `llm_config_service` reads env/keychain, no per-user resolution. Core change = a `user_id`-aware key resolution (read `user_api_keys` first, instance fallback). **Open for PM:** #1185 may itself split — identity (per-user auth → RECONNECT) vs per-user-LLM-key (hosted-beta) — the #1162 mapping clarifies. Gameplan + audit-cascade gate await PM's confirm.

## RECONNECT #1162 reconciliation RESOLVED + board corrected (PM-approved, ~09:45 PT)

PM approved the correction ("apply the recommended board changes; when we get to M5 we can decide if that sprint needs refactoring"). Actions applied + verified:
- **Filed #1300** (BYOC-CRED-DECOUPLE — the real plugin-cred decouple from PA's option-a plan, which had no tracking issue). Body faithful to the plan (3-part design, 6 work items, near-term/end-state, PM open-Qs).
- **Board** (Projects-v2 Sprint field, project 1; verified via item-list): #1162 (hosted-distro exploration) RECONNECT → **SKUNK** (+ status In Progress → Product Backlog); #1300 added → **M5**; #1185 stays RECONNECT; #1278 stays M5.
- **Records**: scope-§12 CORRECTION block (decision-a retained for history, marked superseded where conflicting); decisions.log correction line (right after the (a) line); #1300 body lane → M5 confirmed.
- **Architect re-pinged** (`memo-lead-to-arch-cc-pm-1162-correction`, `f8f49c61e`) — ADR-070 Phase-0 = #1185 + #1229, drop #1162; WS-9 reframe unchanged.
- M5 refactor (consolidate #1282, etc.) **deferred** to "when we get to M5" (PM).

RECONNECT now clean: 9 WS + #1185 (identity) + connector-adjacent (#441/#865/#1227/#1283). Phase-0 foundation = #1185 + #1229 (+ ADR-070). **Next:** gameplan #1185 (or #1229) — PM to pick/sequence.

## #1185 audit cascade (gates 1–2) DONE — COMPLETE-THE-PATTERN, ~70% built (midday)

PM: "do whole, one coherent effort; run the audit cascade." Ran it:
- **Gate 1 (Issue)**: audited #1185 vs feature.md → fleshed feature-complete (Goal/AC/Testing/Effort/Deps; Open-Q-1 resolved). `dev/2026/06/20/1185-issue-audit.md`. (78fe3a84c)
- **Gate 2 (Gameplan + audit)**: `dev/2026/06/20/1185-gameplan.md` + `1185-gameplan-audit.md`.
- **Gate 3 (Prompts)**: N/A — **solo TDD** (shared files `request_key.py`/`intent.py` → parallel subagents would collide).

**KEY FINDING — #1185 is ~70% built (Medium, not Large):** three pieces exist separately, just unwired:
1. Per-request key rail — `services/llm/request_key.py` (ContextVar + `request_api_key` CM + `anthropic_client_for_request`); `clients.py:_anthropic_complete` already uses it; `complete()` takes `user_id`.
2. Stored keys — `UserAPIKeyService.retrieve_user_key(session, user_id, provider)`; `user_api_keys` covers anthropic (no schema change).
3. Auth — `/intent` resolves `user_id` from JWT (#455/#490: `current_user.sub`).
**The gap**: `intent.py:338` binds ONLY the header (`X-User-Api-Key`, Desktop BYOC), never the stored key (hosted web). **Open-Q-2 (token vs account/login) RESOLVED → JWT (token), already in place.**

Gameplan: P1 DB-fallback at the binding (small) · P2 extend beyond /intent + confirm JWT covers hosted testers (the unknown; possible STOP) · P3 capture at /connect (#1300) · P4 encrypt (#358). Subagent decision: solo. **Next: Phase 1 TDD.**

### Phase 1 DONE — DB-resolved key binding (10:30, TDD green)
- `resolve_request_api_key(header_key, user_id, fetch_stored)` in `services/llm/request_key.py` — **pure** (DB fetch injected); priority header > stored > None.
- `intent.py:338` wired: `X-User-Api-Key` header (Desktop BYOC) → authed user's STORED key (`UserAPIKeyService.retrieve_user_key`, session via `AsyncSessionFactory.session_scope_fresh()`) → server key. Rides the existing #1162 ContextVar rail.
- Tests: `tests/unit/services/llm/test_request_key_resolve_1185.py` (6 — resolver matrix + rail-wiring proving a stored key reaches a real Anthropic client). **12 passed** (incl. #1162 regression). `intent.py` imports clean.
- STOP-check (session availability) resolved: session via AsyncSessionFactory at the binding site.
- Next: Phase 2 — extend the binding beyond /intent (2a) + investigate JWT-issuance-for-hosted-testers / Caddy-gate (2b, surface for PM+Arch — #1162 gate territory).

### Phase 2 investigation — core essentially done; 2 decisions remain (midday)
- **2a (extend beyond /intent): NO-OP.** `/intent` is the ONLY LLM-invoking route; every other `LLMClient` use (floor, intent_service, analyzers) runs *under* `process_intent` → already on Phase-1's binding. `setup.py` only *stores* keys (line ~867); the LLMClient mention there is a comment, not a call.
- **2b (auth): EXISTS.** `web/api/routes/auth.py` — full JWT: `/login`→`generate_access_token`→`auth_token` cookie, `/refresh`, `/logout`. The "no token flow" STOP is moot.
- **Phase 3 (capture): partly exists.** `setup.py` stores the user's anthropic key at setup-complete. #1300 `/connect` = the *plugin* equivalent (separate).
- **Net**: per-user keys resolve end-to-end for the hosted-web path; Phase 1 was the load-bearing change.
- **Remaining**: (1) **Caddy-gate removal** — PM/Arch decision (#1162 gate); (2) **encrypt-at-rest (#358)** — keys via `KeychainService` (OS keychain on Mac); the *hosted-Linux* backend is the open question; in-#1185-now vs #358-lane = scope call; (3) **end-to-end integration test** (buildable). Next: integration test (unblocked); (1)+(2) surfaced for PM.

### Phase 4/#358 finding — encrypt-at-rest is a REAL hosted-beta gate (midday)
`KeychainService` uses Python `keyring` (macOS Keychain locally → encrypted). On the **hosted Linux droplet** (headless, no secret service), `keyring`'s default backend is NOT guaranteed encrypted — fail-backend (raises) or a plaintext/file fallback depending on what's installed; `_verify_keyring_backend` raises on init failure. So **per-user keys resolve (Phase 1) but are not safe at rest on the hosted box until #358** (a deliberate encrypted backend / DB-column encryption). → **#358 is a hard dependency for the hosted-beta cutover, not optional**; it's its own substantial SEC build; #1185 depends on it.

**Definition-of-done (#1185)**: resolution + wiring = **functionally complete + tested** (Phase 1). Hosted-beta SAFETY gated on **#358** (encrypt-at-rest) + **Caddy-gate-removal** decision (#1162, PM/Arch). Full-route integration test = tracked (pieces individually tested; e2e needs the test-DB harness). All three surfaced to PM.

## #358 SEC-ENCRYPT-ATREST — cascade (gates 1–2), scoped to the secret-store floor (PM picked it)
PM: "proceed with #358." Investigated → it's a **true greenfield SEC build** (no `encryption.py`/Fernet/KEK exist — confirmed by grep; PA's 2026-06-10 update is authoritative; the original body's "Fernet exists" + "api_keys.key_value" claims have no referent).
- **Gate 1 (issue audit)**: `dev/2026/06/20/358-issue-audit.md`. Reconciled the stale original; scoped **(A) secret-store FLOOR** (the #1185 enabler) vs **(B) content/PII compliance bulk** (defer; M5; same primitive).
- **Gate 2 (gameplan + audit)**: `358-gameplan.md` + `358-gameplan-audit.md`. **Phase 1** = `FieldEncryptionService` (AES-256-GCM + HKDF per-field subkeys + `ENCRYPTION_MASTER_KEY` env); **Phase 2** = encrypted user-secret store (`encrypted_secret` column on `user_api_keys` + `UserAPIKeyService` integration + keychain fallback). Security design: authenticated encryption, per-field subkeys, random nonce, no-leak, additive-only migration. KEK-env now / #482 KMS later.
- **Gate 3 (prompts)**: N/A — solo (security-critical + shared files).
- Tasks #31–34. Next: **Phase 1 TDD** (FieldEncryptionService).
