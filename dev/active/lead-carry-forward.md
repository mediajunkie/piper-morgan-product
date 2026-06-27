# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-25 ~21:55 PT (day-close STOP). Sole lead. Session log: `dev/2026/06/25/2026-06-25-0635-lead-code-opus-log.md`

## ▶ TOMORROW AM — PLAN READY TO GO (read first)
**PM removed the sequencing gate (6/25 eve): Lead chunks the RECONNECT sprint myself — PM will ratify or flag concerns.** Plan written: `dev/2026/06/25/reconnect-sprint-chunking-proposal-2026-06-25.md` (STATUS: PROPOSED). **Tomorrow AM, execute it unless PM objects:**
**Sequencing principle (PM 6/25):** order by *Lead's process / context-coherence*, not external urgency (alpha tester count is too low for tester-facing urgency to drive order). So: stay on the dependency spine, minimize context-switching, do everything-for-a-connector in one pass.

**✅ DONE 6/26: Chunk 1 / WS-2 (#1229) — binding-storage foundation CLOSED** (`88a168aff`). `ConnectorBinding` model + migration `b1229bindings` (applies+reverses on PG) + repository + 8 tests; 27/27 connectors green. Arch-gate was already cleared by ADR-070 D3 (no Arch-wait). Per-connector cred cleanups folded to #1317.

**▶ Chunk 2 — MCP spine + ports. STATUS 6/27:**
- ✅ **GitHub port inc.1 DONE** (`2be6ecbf5`): adapter connect()/status() read the #1229 `ConnectorBinding` store. OQ-1 (github-mcp-server) + OQ-5 (MCP owns OAuth) resolved. Gameplan `dev/2026/06/26/1317-1220-mcp-ports-gameplan.md`.
- ✅ **Real MCP transport DONE (6/27)** — `MCPClient` over the official MCP SDK (`mcp==1.26.0`) `ClientSession`: `services/mcp/consumer/mcp_client.py`; `connect_stdio()` production factory; 6 tests (in-memory round-trip + real stdio subprocess); commits `69fc4f8de`+`40b8b1821`; 84/84 consumer + 11/11 queries green (Shape B — legacy sim stack untouched, zero regression). Supersedes the `protocol_client.py:179` `NotImplementedError`. Gameplan `dev/2026/06/27/1220-real-mcp-transport-gameplan.md`.
- ⚠️ **#1220 is the UMBRELLA, not "the transport" — kept OPEN** (read its full body 6/27): §0 anchor for the connection/auth → MCP migration; closes when the per-connector auth migrates + bespoke OAuth flows retire. Transport = infra shipped *under* it (progress comment posted). Hard-blockers cleared (#1232 ✅, ADR-070 ✅). **#1322 filed** = legacy sim-transport cutover (migrate query_router off simulation_mode → MCPClient).
- ✅ **MCPClient transport COMPLETE (stdio + HTTP)** — `connect_stdio` (local process) + `connect_http` (hosted streamable-HTTP) both shipped + integration-tested (`a231d6275`). 92/92 consumer + 108 MCP-tree/arch-enforcement green.
- ✅ **#1317 github inc.3 DONE (`ee1b9b457`)** — `resolve()` is binding-aware with the full honest-degrade rail (folds #1231): no-binding/stale/unreachable/server-down → matching ResolveMiss; bound+reachable → real MCP round-trip → ResourceHandle. **GitHub connector fully protocol-wired** (all 4 methods). Transport seam isolates the 2 provisioning-gated points.
- 🚦 **GATE: github-mcp-server provisioning — DECISION-MEMO sent to PM cc Arch (`64f3bfaec`).** Option A hosted-OAuth (D3-aligned; HTTP transport now pre-built) [recommended] vs B local-stdio-PAT (re-introduces raw-token custody). **All remaining github-port LIVE work (inc.2 OAuth callback, #1230 concrete resolution, live cutover) waits on this A/B decision.** Don't pre-build the OAuth flow until ratified.
- ✅ **#1317 CALENDAR port DONE (`1458c4cc6`)** — connector #2 on the binding-aware honest-degrade rail (all 4 methods; `_CALENDAR="calendar"`; m-41 guard covers it; 7 tests; 115 passed). **#1231 honest-degrade is now connector-WIDE for github + calendar.**
- **✅ ARCH RULED (6/27 08:30): provisioning = A (hosted-OAuth, D3-realizing)** + Shape-B ratified + **#1322 elevated to CRITICAL-PATH** (memos in `lead/read/`; my ack `8da17e768`). Decisions.log recorded.
- **✅ A→C RE-RULED (Arch 6/27 13:45): provisioning = C (self-hosted + per-user OAuth).** A is out — PM: requiring testers to have Copilot is a non-starter (A's hosted endpoint draws on each tester's Copilot/credits). B (PAT) rejected. **C = self-host the official `github-mcp-server` (Docker, Droplet→Mac Mini) + testers OAuth our free GitHub App (no Copilot, ~zero cost).** Same `connect_http` transport. decisions.log records C supersedes A.
- **🔑 TOKEN-CUSTODY MODEL — CONFIRMED (Arch):** D3 precised = "Piper holds NO raw vendor PAT/API-key; scoped/revocable/refreshable OAuth grants ARE permitted, #358-encrypted, the #1229 binding holds a REFERENCE (pointer), never the secret." C fits exactly (extends the Calendar-OAuth precedent #529/#843). **D3-ideal end-state = GitHub-App installation-token (Piper holds NO user token) — tracked #1325, adopt when the server supports it (m-36 ratchet).**
- **▶ inc.2 plan (C-targeted; UNBLOCKED, Arch nod on the #1229-schema part):** connect()=OAuth redirect-orchestrator (our GitHub App) → web callback route → token exchange (SDK `mcp.client.auth.OAuthClientProvider`, PKCE) → store grant in the #358 encrypted secret store → create #1229 binding (status=bound, refs the secret) → github adapter `_mcp_client_ctx` → `connect_http(<self-hosted-server-URL>)`. **Build against fixtures/mocks now** (live test needs the deploy + App below). Mirror `services/integrations/calendar/oauth_handler.py` + `/setup/calendar/oauth/callback`.
- **PM/infra deps for LIVE (NOT for the code build):** (1) **PM registers a GitHub OAuth App** — I supply the exact callback URL + scopes once the callback route exists; (2) deploy `ghcr.io/github/github-mcp-server` Docker on the Droplet; (3) store the App client_id/secret via `KeychainService`.
- **🧭 Ports thread at a clean rule-of-two boundary** (github + calendar rails done; honest-degrade now connector-wide).
- **⚠️ #1322 is critical-path, NOT cleanup** (Arch verified): `MCPConsumerCore.simulation_mode` is hardcoded `True` (`services/mcp/client.py:93`, a Pattern-073) → the live MCP **query path serves SIMULATED data today**. #1322 = what makes #1220's real transport reach query routing. Sequence as the **deliberate close of #1220's umbrella**: behavioral coverage (canonical-retest asserts real MCP data, not sim) BEFORE deleting the sim stack + the m-36 sim-test-only guard (sim unreachable from a production config). Its full cutover needs a real server connected → rides the same PM checkpoint (after github-live).
- **▶ NEXT (in order, on PM's checkpoint clear):** (1) **github inc.2** — connect() as OAuth redirect-orchestrator + callback stores the binding, against `api.githubcopilot.com/mcp/` via `connect_http` (the github adapter's `_mcp_client_ctx`/`_server_params_for` switch from the stdio stub to HTTP-to-hosted); (2) concrete #1230 github resolution tool against the real server; (3) **#1322** the query_router cutover + sim-test-only guard (the umbrella close); (4) **#1323** mixin extraction at connector #3 (notion). If PM's checkpoint stays pending, all of these are gated — everything buildable without it is shipped.
- **#1312** personality-Base collapse — PM-approved timing = **queued AFTER the alpha bundle** (Exec memo 6/26), NOT pulled forward; fully specced (Arch (a) UUID-everywhere + delete dead sentinel; invariant-lint skeleton; TDD risk = response_enhancer user_id UUID-castability). No action until alpha clears.

1. **First (no code)**: fire the **Arch WS-2 design-decision** question (does MCP-binding storage shrink #1229?) — the one gate on the spine.
2. **Then Chunk 1 (#1229) — the credential-model foundation.** Prep is unblocked now (read `user_api_keys` + Keychain path + ADR-058 cred model; scope binding-vs-raw); build to Arch's answer when it lands. Stay here rather than context-switch to filler.
3. **Then Chunk 2 (#1220 spine + #1317 ports).** **Both #1230 AND #1231 fold in per-connector** (PM ratified #1230 fold 6/25; #1231 also folds — no tester-urgency + context-coherence: do each connector's resolution + honest-degrade *while in that connector's port*, one context-load, not a separate canonical_handlers.py pass that gets re-touched at port time). The #1232 contract + m-41 guard enforce honest-degrade as each connector ports.
- **#1283 → M5** (PM 6/25). **Slack (Chunk 4 #1109/#1110) → later** (PM 6/25: "Slack can wait"). Then #1314/#1315 (data/first-run) → #1316/#865 (cleanup). #1185 beta track gated.
Chunks: 1=#1229 (cred model, needs Arch Q first) → 2=#1220+#1317 spine/ports (bulk; #1230/#1231 fold in) → 3=connect-UX (#1201/#1314/#1315) → 4=Slack robustness (#1109/#1110) → 5=independents (#865/#1316/#1283). Beta track #1185 gated on #1162 follow-on.

**Still-PM (the not-RECONNECT queue — hold/delegate/do):** #1287 (CIO GO'd, ready), CXO copy fix + debt, #1320 double-login. Surfaced; don't absorb more not-sprint work unilaterally beyond starting RECONNECT per the plan above.

## ▶ READY-TO-EXECUTE (unblocked, but held pending PM's focus call)
- **#1287 Multi-Agent Coordinator removal — CIO GO'd the full pass (option 1, expand into methodology/).** Removal set = services/-side (multi_agent_coordinator, chain_of_draft, kind_communication, integration/ dir, api/orchestration/ dir, 2 scripts, the dead `query_learning_loop.optimize_workflow_via_experiments` method) + methodology/-side (integration/{orchestration_bridge,enhanced_orchestration_bridge}.py, integration/__init__ re-exports, testing/integration_runner.py, **assess real_scenarios.py at deletion**) + ~10 test files. Execute whole pass → run suite (only removed tests should fail) → close #1287. Verify-first per file at deletion (third trace caught methodology/; do a whole-repo trace, not services/-scoped). NOT done tonight (day-close + PM focus signal). CIO memo `read/`.
- **CXO setup-copy: intro-panel fix** (`templates/setup.html` ~line 348, `.piper-description`) — replace the capability-list copy with CXO's collegial version; recommended **before the alpha tester wave**. 1-line change. + **copy debt** (low-pri, file an issue): step-1 error state in `setup.js` ~129 ("Run: docker compose up -d" → softer local-only phrasing). CXO memo `read/`.
- **#1320 double-login follow-up** — PM hit "log in twice" on the hosted UI (Caddy gate once + app login again after a refresh = app session-cookie didn't stick first try; likely the #857 cookie/refresh-token flow on the hosted domain). File a small bug; not chased tonight.

## ▶ RECONNECT — next-move (PM to pick; both are real sprint progress)
- **#1229 (WS-2 credential model)** — the foundation next step; needs a quick **Arch design-decision first** (does storing MCP-server *bindings* vs raw creds shrink it?).
- **#1283 (routing-integrity audit)** — sprint-tagged (corrected: it IS in the RECONNECT sprint), unblocked, no deps; Arch staged to author ADR-073 from its gap-list output. Bounded; delegable.
- Bulk ahead: **#1220 (MCP spine) + #1317 (ports)** = the heavy two-thirds; **#1230/#1231 fold into #1317** (re-scope, don't build as written). Full board reconciliation given to PM 6/25 eve (sequencing doc `dev/2026/06/22/reconnect-remainder-sequencing-2026-06-22.md`).

## ▶ GATED (PM/Arch/CXO — not Lead-unblocked)
- **#1312 collapse** — Arch RULED the user_id-contract (option a: UUID-everywhere, retire dead `get_default("default_user")` sentinel; **the "trust service ×7" callers are a DIFFERENT repo — `UserTrustProfileRepository`, already UUID — collapse never touches them**; so it's SMALLER than first flagged). Bounded plan in Arch memo (`read/`) + decisions.log. Awaiting **PM execution-sequencing** (slots after alpha MCPB gate). Includes an invariant-lint (AST single-Base guard → `test_architecture_enforcement.py`).
- **#1162 Caddy-gate removal** — DECIDED: **keep the gate for now** (it's the alpha invite mechanism — `create_user` has no registration gating; removing = open public registration). Real removal pairs with #1185 + app-layer invite control + RBAC (#357/#1312). decisions.log 6/25.
- **MCPB clean-machine test** (PM+PA) — the one remaining pre-alpha-email gate. PM said likely tomorrow.
- **#1286 Slice 2** (CXO radar tiling).

## ▶ DONE this session (06-25) — productive day
- #1318 + #1319 (alpha onboarding blockers) — fixed, 16 tests, deployed, **PM-UAT'd**, closed.
- #358 encryption deploy verified live; **PM ran the UI chat smoke test → encrypted write path exercised end-to-end** (the pending #358 UI item — now satisfied).
- #1310 (mail-send self-reconcile) — fixed + T6 + closed. #1309 (onboarding test) — fixed + closed.
- #1320 filed + side-bug #1 (check-keychain /api/v1 prefix) fixed+deployed+guard-tested.
- #1287 verify-first caught the methodology/ boundary → handed to CIO → CIO GO'd option 1.
- Caddy password rotated to `piperalpha`/`crispy` (PM request). Gate verified working.
- Decisions recorded (decisions.log): #1162 keep-gate; (+ Arch's #1312 contract ruling, merged).

## ▶ STATE / refs
- **alpha** 0.8.9 live + hardened. Deploy: `scp` changed files to `/opt/piper/...` + `docker compose ... restart app` (volume-mounted `.:/app`; restart picks up code; `deploy.sh` = slow full rebuild, only for dep changes).
- **Mailbox** = `scripts/mail-send.sh` — self-reconciles (#1310); no manual post-send cleanup.
- **Encryption**: key on Droplet; `services/security/field_encryption.py` + `encrypted_types.py` (`PMENC1:` marker). Cols: artifacts.content, conversations.preview, conversation_turns.{user_message,assistant_response}.

## ▶ Methodology (this session's wins)
- **Verify-first on deletes**: #1287 — whole-repo trace (not services/-scoped) caught a methodology/ consumer layer BOTH prior traces missed → paused + surfaced to CIO's lane instead of blind-delete or unilateral-expand.
- **Verify at the user's layer**: nothing "done" until live curl + PM UAT (#1318/#1319) / in-container round-trip on the real key (#358) / browser repro of the actual loop (#1320).
- **Correct myself on new data**: #1283 "not RECONNECT" → board shows it IS sprint-tagged → corrected to PM; #1162 "just remove the gate" → registration-is-open finding → corrected to "gate is the invite mechanism, keep it."
