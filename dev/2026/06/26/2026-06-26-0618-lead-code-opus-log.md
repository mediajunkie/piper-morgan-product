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
