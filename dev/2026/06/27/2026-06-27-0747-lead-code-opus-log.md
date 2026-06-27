# Lead Developer — Session Log 2026-06-27

**Role**: Lead Developer (role-slug: lead) · **Tool**: Claude Code · **Model**: Sonnet 4.6
**Worktree**: interesting-beaver-7ee19c (ephemeral, Model B) · Sole lead.
**START**: 07:47 PDT Sat Jun 27 — PM kicked off: close Jun 26, open today, check mail, resume RECONNECT. Jun 26 retroactively closed (busy-signal interrupts prevented a live STOP; all Jun 26 work was already on origin/main).

## Carry-in (RECONNECT Chunk 2 — the ports)
- ✅ **WS-2 (#1229) CLOSED** 6/26 — `ConnectorBinding` storage foundation. ✅ **GitHub port inc.1** — adapter connect()/status() read the binding store.
- ⚠️ **inc.2 (OAuth callback) is BLOCKED** behind the real transport: the MCP-consumer transport is simulation-only (`services/mcp/protocol/protocol_client.py:179` `NotImplementedError`) + no github-mcp-server. **#1220 (real MCP-consumer transport) is the prerequisite.**
- **▶ TODAY: build #1220 — the real MCP transport.** Buildable+testable NOW against `scripts/mcp_file_server.py` (no github-mcp-server needed for the transport itself). github-mcp-server provisioning (stdio-local vs hosted) = a later infra call. Gameplan: `dev/2026/06/26/1317-1220-mcp-ports-gameplan.md`. Exec green-lit "keep draining the ports — pre-authorized" (6/26).
- **Gated (don't touch)**: #1312 (queued AFTER alpha bundle, PM-approved timing); #1320/#1162 (Caddy-gate = PM+Arch).

## Work

- **07:47 — START.** Closed Jun 26 (DAY-CLOSED). Synced; all prior work on origin/main. Triaged the 2 Exec memos (1312-timing + keep-draining-ports) → read/. Mail clear.

- **~08:00 — #1220 investigated + gameplan written (the spine).** Investigate-before-extending on the transport: **the official MCP SDK is already a dep (`mcp==1.26.0`)** — provides `ClientSession`, `stdio_client`+`StdioServerParameters` (real subprocess transport), `create_connected_server_and_client_session` (in-memory test transport), `FastMCP` (test-server fixtures). Also found: the hand-rolled sim stack (`MCPProtocolClient`/`consumer_core` `simulation_mode:True`) is **LIVE** in `query_router.py:109`; and `scripts/mcp_file_server.py` is itself a POC sim (not real MCP). **Design decision (Lead-lane, flagging for PM/Arch): Shape B — build a NEW SDK-based `MCPClient`, don't retrofit the hand-rolled `_send_message`.** Rationale: don't hand-roll MCP JSON-RPC when the SDK is installed; the legacy sim stack is live in query_router → a new client leaves it untouched (zero regression); legacy cutover = a separate follow-up, OUT of #1220 scope. Gameplan + audit self-check: `dev/2026/06/27/1220-real-mcp-transport-gameplan.md`. **Concern to surface**: this is a notable transport-mechanism + architecture call — proceeding per Exec's keep-draining green light, but PM/Arch may want to weigh in on the legacy-cutover sequencing. Building inc.1 (the SDK `MCPClient` + in-memory round-trip test) now.
