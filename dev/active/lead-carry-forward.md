# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-25 ~21:55 PT (day-close STOP). Sole lead. Session log: `dev/2026/06/25/2026-06-25-0635-lead-code-opus-log.md`

## ▶ TOMORROW AM — PLAN READY TO GO (read first)
**PM removed the sequencing gate (6/25 eve): Lead chunks the RECONNECT sprint myself — PM will ratify or flag concerns.** Plan written: `dev/2026/06/25/reconnect-sprint-chunking-proposal-2026-06-25.md` (STATUS: PROPOSED). **Tomorrow AM, execute it unless PM objects:**
1. **First (no code)**: fire the **Arch WS-2 design-decision** question (does MCP-binding storage shrink #1229?) — unblocks the critical path (Chunk 1 → Chunk 2 spine/ports).
2. **Then dive into Chunk 1 (#1229)** — prep/investigation is unblocked even before Arch answers (read `user_api_keys` + Keychain path + ADR-058 cred model; scope binding-vs-raw-cred); build per Arch's answer. Small fallback if Arch is slow: **#1110** (self-contained Slack `_make_request` user_id bug). **NOTE: #1283 → M5 (PM 6/25)** — no longer the starter; it + ADR-073 are M5 polish (routing gaps fall to the floor safely already).
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
