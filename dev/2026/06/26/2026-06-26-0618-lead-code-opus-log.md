# Lead Developer — Session Log 2026-06-26

**Role**: Lead Developer (role-slug: lead) · **Tool**: Claude Code · **Model**: Sonnet 4.6
**Worktree**: interesting-beaver-7ee19c (ephemeral, Model B) · Sole lead.
**START**: 06:18 PDT Fri Jun 26 — PM kicked off the morning cycle: "let's get back to working on RECONNECT." Jun 25 closed cleanly (DAY-CLOSED verified). Overnight 03:35 WATCH was quiet (inbox empty; only CIO liveness-model + Docs WATCH overnight).

## Carry-in (from `dev/active/lead-carry-forward.md`)
- **RECONNECT is today's focus.** PM delegated sprint chunking to Lead (6/25) + ratified the plan. Sequencing principle: order by Lead's context-coherence, not external urgency (tester count too low to drive order). Plan: `dev/2026/06/25/reconnect-sprint-chunking-proposal-2026-06-25.md`.
- **Today's first moves**: (1) fire the **Arch WS-2 design-decision** question (does MCP-server-binding storage shrink #1229?) — the one gate on the spine; (2) start **#1229 (credential model)** — prep is unblocked now (read `user_api_keys` + Keychain path + ADR-058), build to Arch's answer.
- **Decided 6/25**: #1230 + #1231 both FOLD into the per-connector ports (#1232 contract + m-41 guard enforce honest-degrade as each ports). #1283 + ADR-073 → M5. Slack (#1109/#1110) → later ("Slack can wait"). #1162 keep-the-gate. Spine order: #1229 → #1220/#1317 ports → #1314/#1315 → #1316/#865.
- **Parked (not-RECONNECT, PM hold/delegate/do call):** #1287 (CIO GO'd full coordinator removal, ready), CXO setup intro-panel copy fix + copy-debt, #1320 double-login follow-up.

## Work

- **06:18 — START.** Verified Jun 25 DAY-CLOSED (no self-heal); synced; inbox empty; today's dir ready. Beginning RECONNECT per the ratified plan.

- **~06:35 — #1229 investigation → Arch-gate ALREADY CLEARED + issue is stale (no Arch-wait needed).** Planned first move was "fire the Arch WS-2 design-Q (raw creds vs MCP bindings?)." Investigate-before-extending: read ADR-070 fully — **D3 already rules it**: "MCP server owns OAuth; Piper stores bindings only"; "the four-conventions credential model collapses to one convention: server-binding-by-user"; line 152 "WS-2 collapses to server-binding storage per D3." Arch-authored + PM-ratified-direction. So asking would re-litigate a settled ADR. The one genuinely-open WS-2-adjacent item is OQ-5 (does Piper retain OAuth-handshake state, or is `connect()` a pure redirect-orchestrator?) — but that affects the WS-5 **connect() flow in the ports**, NOT the binding-storage schema → doesn't block #1229. **Net: #1229 fully unblocked, no Arch dependency.**
  - **#1229 issue body is STALE vs ADR-070 D3**: its Phase-1/2 (unify 4 raw-cred keychain conventions, typed OAuth-app/token/PAT wrapper) is exactly what D3 supersedes. **Real scope = the per-user MCP-server-binding storage foundation** (the ports consume/populate it). Per-connector cred cleanups (stale `get_api_key("github")` phantom-readers at intent_service.py:6254/:6416; Notion dual-scope) fold into each connector's port (context-coherence), like #1230/#1231.
  - **Build shape (mirrors WS-1 #1199 `connector_configs`)**: a `connector_bindings` table — `id` + `owner_id` (FK users.id, ADR-071 D2) + `tenant_id` (ADR-071 D7) + `connector` + binding fields per D3/D4 (mcp_server_ref/endpoint, capability_profile, status, `is_native_legacy`) + UniqueConstraint(owner_id, connector) + `TimestampMixin`; additive Alembic migration; `ConnectorBindingRepository` (get/upsert/status) mirroring `ConnectorConfigRepository`. ADR-058 user-scoping. Building now (gameplan → TDD).

- **~06:40 — #1229 WS-2 binding-storage foundation BUILT + verified (commit `88a168aff`).** Gameplan `dev/2026/06/26/1229-binding-storage-gameplan.md` (low-drift mirror of #1199). Shipped: `ConnectorBinding` model (10 cols, owner-stamped, no creds), additive migration `b1229bindings`, `ConnectorBindingRepository` (get/upsert/set_status), 8 unit tests. **Verified**: migration applies + reverses clean on real Postgres (`\d connector_bindings` confirms all cols/defaults/indexes/FK); 27/27 connectors suite green (no regressions). Re-scoped #1229 (raw-cred unification superseded by D3; per-connector cleanups → #1317). Next: track the folds on #1317 + close #1229.

- **~07:30 — GitHub port inc.2 BLOCKED → sequencing correction: #1220 (real transport) is the prerequisite.** Went to build inc.2 (OAuth callback); investigate-before-extending caught a hard blocker: the **MCP-consumer transport is simulation-only** (`protocol_client.py:179` `NotImplementedError("Real transport not yet implemented")`; `consumer_core` `simulation_mode: True`) + **no github-mcp-server configured**. So inc.2-3 (github connect/resolve) can't talk to anything real — would be building vapor against an absent external contract. **Corrected the gameplan**: #1220 (WS-8, the real MCP-consumer transport) is the true prerequisite, not parallel; inc.1 worked only because it's pure binding-storage. **#1220 is buildable+testable NOW** against the existing `scripts/mcp_file_server.py` (no github-mcp-server needed for the transport itself); github-mcp-server provisioning (stdio-local vs hosted) is a later infra call for inc.2. **Pivoting to #1220.** (Mirrors the day's pattern — investigate-first caught it before building wrong.)
- **~07:45 — #1312 timing CONFIRMED queued-after-alpha (Exec memo, PM-approved).** Personality-Base collapse stays in its agreed slot (after the alpha MCPB gate), NOT pulled forward; fully specced (Arch ruling (a) UUID-everywhere + delete dead sentinel; invariant-lint skeleton; the one TDD risk = response_enhancer user_id UUID-castability). No action until alpha clears. Memo → read/.

- **~07:00 — Chunk 2 entered: gameplan + GitHub port increment 1 (commit `2be6ecbf5`).** Investigated the MCP-consumer surface (connector.py protocol + github_adapter stubs + MCPProtocolClient plumbing). Resolved the 2 Lead-Dev design calls: OQ-1 → github-mcp-server; OQ-5 → MCP owns OAuth, connect()=redirect-orchestrator, binding created on the callback. Wrote the ports gameplan (`dev/2026/06/26/1317-1220-mcp-ports-gameplan.md`, GitHub-first, 5 TDD increments). **Increment 1 shipped**: github adapter connect()/status() now read the #1229 `ConnectorBinding` store (status→ConnectorStatus; connect→Binding-if-bound-else-ConnectRequired), via session_scope. 6 new tests; 78/78 mcp/consumer suite green (the #1232 contract + no-credential-leak guards still pass). Next: increment 2 (the OAuth callback that creates the binding).

- **~06:45 — #1229 CLOSED properly (WS-2 done).** Status banner on the description (raw-cred phases N/A:superseded-by-D3) + closing comment with evidence; per-connector cred-cleanup folds tracked on #1317 (`comment 4810106920`). **RECONNECT WS-2 complete** — the credential-model foundation. Sprint: 10 of ~23 done (WS-1/5/9/2 + quick-wins + security). Next per the ratified chunking: **Chunk 2 — the MCP spine + ports (#1220 WS-8 + #1317 WS-5)**, the bulk. Two Lead-Dev design calls open it (ADR-070 OQ-1 MCP-server-selection-per-connector; OQ-5 OAuth-handshake-state) before the first port (github).

---

## Session Wrap (STOP — 2026-06-26, 06:18 → ~10:30 PDT; retroactive close 06-27 07:47)

**Day arc:** Back on RECONNECT per PM. **Closed WS-2 (#1229)** — the credential-model foundation: investigate-first found ADR-070 D3 had already cleared the Arch-gate (no wait) + superseded the issue's raw-cred phases → re-scoped to the binding-storage foundation; built + verified + closed (`ConnectorBinding` model + migration applying/reversing on real Postgres + repository + 8 tests; 27/27 connectors green). **Entered Chunk 2 (the bulk):** ports gameplan (OQ-1 → github-mcp-server, OQ-5 → MCP-owns-OAuth); shipped **GitHub port inc.1** (adapter connect()/status() read the binding store; 6 tests; 78/78 consumer suite). **inc.2 blocked → key discovery:** the MCP-consumer transport is simulation-only (`protocol_client.py:179` `NotImplementedError`) + no github-mcp-server → **#1220 (real MCP transport) is the true prerequisite** for the github connect/resolve; recorded the sequencing correction. Exec green-lit "keep draining the ports, you're pre-authorized." #1312 confirmed queued-after-alpha. Net: a workstream closed + the bulk's first increment shipped + the real next step (#1220) identified.

**Discipline win of the day:** investigate-before-extending paid off three times — caught the ADR-070 D3 Arch-gate clearance (saved a round-trip), the stale #1229 issue (avoided building superseded raw-cred work), and the simulation-only transport (avoided building a vapor OAuth flow against a non-existent server).

## Memory & briefing surfaces referenced this session
**Referenced**: ADR-070 (D3/D5 + OQ-1/4/5 — the load-bearing find of the day); the WS-1 #1199 `connector_configs` pattern (mirrored for bindings); the #1232 `Connector` protocol; `duty-cycle-tick` (START); `close-issue-properly` (#1229 close); CLAUDE.md (alembic/cross-dialect migration + session-scope patterns).
**Loaded but not referenced**: cross-pollination brief; BRIEFING-CURRENT-STATE.
**Wanted but not found**: an at-a-glance statement that the MCP-consumer transport was still simulation-only — I discovered it by reading `protocol_client.py`; a note in ADR-070 / the scope doc ("real transport = #1220, not yet built") would have surfaced the #1220-prerequisite before I started down inc.2.

## Sign-off
```
git log HEAD..origin/main: empty (all work pushed — #1229, inc.1, gameplan, sequencing-correction docs)
```

<!-- DAY-CLOSED: 2026-06-26 -->
