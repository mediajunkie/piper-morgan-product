# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-21 ~13:15 PT. Sole lead. Session log: `dev/2026/06/21/2026-06-21-0615-lead-code-opus-log.md`

## ▶ NEXT (draining in priority order)
- ✅ **PA Redis prod-fix DONE** (PM-approved 2026-06-21) — 6379 now `127.0.0.1`-only on the alpha Droplet (was `0.0.0.0`+IPv6); redis recreated, app unaffected (Up 26h healthy; app→redis ping True), public 401. Backup `/opt/piper/docker-compose.yml.bak-2026-06-21-redis-bind`. Tracked+closed **#1311**; PA confirmed. Plugin-wave Redis blocker cleared.
- **CXO #1286 D2 design-system** — **Slice 1 (tokens/baseline/grid `8f8f9a67d`) + Slice 3 (responsive shell + mobile hamburger drawer `af7cba06b`) SHIPPED** — render+lint-verified; **CXO conformance + PM phone-UAT pending** (can't headless-verify the responsive/drawer visuals). **Slice 2 (radar tiling) HELD for CXO** — spec's dense `.radar-entity-item`/pill tiling ≠ the roomy production `.radar-card`; memo'd CXO 3 options (`e6decb14f`). Can't close #1286 until Slice 2 + the UATs.
- **RECONNECT Phase-1 — WS-1 FUNCTIONAL CORE COMPLETE (P0→P3), all on origin/main** (`7436d1bef`…`946c5f66c`). The scattered connector config now has a DB-backed home + every surface reads/writes it. Guide: `dev/2026/06/21/1226-ws1-config-store-gameplan.md`.
  - **P0** WS-9 identity collapse → canonical `owner_id` = m1-test `009afc8c`. **P1** `connector_configs` table (model + migration `000baa96d800`, 7 tests). **P2** `ConnectorConfigRepository`+`ConnectorConfigService` (`services/connectors/`, 12 tests). **P3a** backfill json→DB; **P3b** settings writer dual-writes the DB; **P3c** `repo_resolver` reads DB-first+json-fallback (the canonical chat path); **P3d** `UserPreferenceManager.get_default_repo` DB-first → **standup always-None bug FIXED**. ~90 tests green across the touched suites.
  - **P4 (retire flat/in-memory) DONE** — clean cutover (PM-directed 2026-06-21: pre-prod + no users = zero-risk window; deferring inverts the risk). DB is now the SOLE github-config store: settings + resolver + UPM + feed_factory all DB-only; `github_username` also DB-backed; flat-file + in-memory machinery DELETED (net −314 lines). Verified: touched suites green + full unit+domain smoke **8003 passed / 19 pre-existing fails only** (zero new regressions). #1199 "exactly one store" AC now MET. **P5** evidence comments on #1199 + #1226; **both OPEN, PM close-decision pending** — #1199 now ~95%+ (only a single e2e test + docs remain).
  - **Discovered + filed**: DB↔model drift `task_59a7a442` (autogenerate unusable); 9-test datetime-tz bug in standup `task_640ecba1` (pre-existing, proven orthogonal). #1185 parked (sibling).

## ▶ PENDING PM / Arch
- ~~PM: Redis prod-fix go~~ — DONE 2026-06-21 (#1311).
- ~~Arch: #1232 ratify + build-order~~ — **DONE 2026-06-21**: Arch RATIFIED the shapes (Open-Q-4 closed) + ruled WS-1-now-independent-of-#1185 (order WS-9-collapse→WS-1→ports; multi-tenant-READY per m-40). Now building (see NEXT). Open-Q-5 (handoff-vs-orchestrate) still deferred to the ports' MCP-connect-flow.
- #358 close: hold-for-deploy (PM-confirmed); deploy = set `ENCRYPTION_MASTER_KEY` on the box + run the backfill.
- **PM: WS-1 close decision** — #1199 (~90%, functional unification done) + #1226 (umbrella): close-now-with-follow-up, or hold for retire + e2e-test + docs? Both have evidence comments; both currently open.

## ▶ DONE this session (06-21)
- Cron reshaped → 05:05 morning (PM-requested); `cbe956dc` (`5 5,8,11,14,17,20`).
- **WS-9 identity call resolved** (PM): m1-test + xian = same human, unify; PM sole human → single-identity, multi-tenant deferrable (ADR-070 OQ-3). #1233 + decisions.log; `2b47b652b`.
- **#1232 contract refined to Arch's 5 constraints**: sum types (`Binding|ConnectRequired`, `ResourceHandle|ResolveMiss`) + m-41 no-credential guard; 72 consumer tests green; `e485cca9a`. Looped Arch for ratify (`44e505456`).
- **#1286 Slice 1 + Slice 3 shipped**: token foundation (`8f8f9a67d`) + responsive shell/mobile-nav drawer (`af7cba06b`); 36 render/regression tests + token_lint green. CXO memo (`e6decb14f`) holds Slice 2.

## ▶ DONE 06-20 (carry)
- #1299 → 0.8.8 alpha; #1162 reconciliation; #1185 P1 (parked); #358 floor + Dimension B (code-complete; #1305/#1306 deferred).
- Security gap closed: **#1307** admin_compose removed + **#1308** exempt-list lint (m-41). #1162 gate-removal ready for M5.
- **#1232 WS-5 contract** shipped (now refined, above). #1309 filed (stale onboarding test).

## ▶ STATE / refs
- **#1232**: `services/mcp/consumer/connector.py` (sum types) + `github_adapter.py` + `test_connector_protocol_1232.py` + `test_connector_contract_1232.py` (no-cred guard). ADR-070 governs.
- **#1308**: `AUTH_EXEMPT_JUSTIFIED` in `auth_middleware.py` + `test_exempt_list_boundary_1308.py`.
- **alpha** 0.8.8 (no #358-B/#1232/#1307/#1308 yet — next deploy). `ENCRYPTION_MASTER_KEY` needed for #358-B.
- **Cron cbe956dc** armed — `5 5,8,11,14,17,20` (05:05 morning, 20:05 day-close). Session-only, auto-expires 7d → re-arm on the cycle.
- **Mailbox** = `scripts/mail-send.sh` (push-to-ref) — **RECONCILE residue immediately after each send**: drop local copies (identical on origin/main) + FF-merge. Worked cleanly this session.

## ▶ Methodology
- **Investigate-before-extending**: WS-9 — pulled the live users table (480 rows, 478 test) before framing the decision; #1232 — checked shipped types vs Arch's 5 constraints (3 already met) before refactoring.
- **m-41 mechanism**: the #1232 no-credential guard auto-discovers all connector dataclasses (impossible-by-construction, not vigilance); #1308 lint; #1232 AST-guard.
