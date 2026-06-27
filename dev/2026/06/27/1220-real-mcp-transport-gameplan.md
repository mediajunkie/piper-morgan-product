# #1220 (WS-8) — the real MCP-consumer transport — gameplan

**Author**: Lead Dev · **Date**: 2026-06-27 · **Issue**: #1220 (RECONNECT WS-8, the spine prerequisite for the #1317 github port's connect/resolve).
**Design source**: ADR-070 (D5 Connector protocol; OQ-1 Anthropic-published MCP servers) + the #1232 `Connector` protocol (shipped) + #1229 `ConnectorBinding` storage (shipped). Higher-drift (net-new integration) → gameplan + audit gate before building; small TDD increments.

## Problem statement
Piper's MCP-consumer transport is **simulation-only**: `services/mcp/protocol/protocol_client.py:179` `_send_message` raises `NotImplementedError("Real transport not yet implemented")`, and `consumer_core` runs `simulation_mode: True`. So no connector can actually talk to a real MCP server — the #1317 github port's `connect()`/`resolve()` (inc.2-3) have nothing real to speak to. #1220 builds the real transport.

## Root-cause / what exists (investigated 2026-06-27)
- The official **MCP SDK is already a dependency** (`mcp==1.26.0`). It provides: `ClientSession` (`initialize`/`list_resources`/`read_resource`/`list_tools`/`call_tool`); `mcp.client.stdio.stdio_client` + `StdioServerParameters` (real subprocess transport); `mcp.shared.memory.create_connected_server_and_client_session` (in-memory client↔server transport for tests); `mcp.server.fastmcp.FastMCP` (trivial real test-server fixtures).
- The hand-rolled `MCPProtocolClient` + `consumer_core` (`simulation_mode:True`) stack is **live** — `services/queries/query_router.py:109` default-instantiates `MCPConsumerCore()`. Query routing depends on its simulated responses today.
- `scripts/mcp_file_server.py` is itself a **POC simulation** (its docstring says so) — NOT a real MCP stdio server. So the real test target is an SDK FastMCP fixture, not the file-server.

## Design decision (Lead-lane; recorded for PM/Arch visibility, not gating)
**Build a NEW, small, SDK-based `MCPClient` (Shape B)** — do NOT retrofit the hand-rolled `MCPProtocolClient._send_message` (Shape A).
- **Why SDK, not hand-roll**: hand-rolling MCP JSON-RPC framing/lifecycle when the official SDK (`mcp==1.26.0`) is installed would be wrong — duplicate + unmaintained. OQ-1 already leans Anthropic-published; the Anthropic SDK is the matching client.
- **Why a new client, not retrofit-legacy**: the legacy `MCPProtocolClient`/`consumer_core` sim stack is **live** in `query_router` on `simulation_mode:True`. A new client leaves that live path untouched → **zero regression risk** to query routing. Retiring/cutting-over the legacy stack to the real client is a separate, larger effort (its own issue), explicitly **out of #1220 scope**.
- **Consumer**: the connector adapters (#1317 github `resolve()`) use `MCPClient`. The binding (#1229) supplies the server ref/params.

## Increments (TDD; each shippable + tested)
1. **`MCPClient` over the SDK `ClientSession` — the in-memory-proven real transport.** `services/mcp/consumer/mcp_client.py`: an async client exposing `list_resources()`, `read_resource(uri)`, `list_tools()`, `call_tool(name, args)`, backed by a real `ClientSession`. A `connect_stdio(StdioServerParameters)` async-context factory for production (spawns the server subprocess, `initialize()`s, yields the client). **Tests** (in-memory transport via `create_connected_server_and_client_session` against a `FastMCP` fixture with one known resource + one known tool): real round-trip — list/read the resource, list/call the tool, assert real protocol responses. ← **FIRST BUILD**
2. **stdio subprocess integration.** Prove `connect_stdio` against a real MCP server *process* (a minimal FastMCP fixture script spawned via `StdioServerParameters`) — round-trip over real stdio, not in-memory. Marked integration (slower); guards the production transport path. (No github-mcp-server needed — the fixture server proves the transport.)
3. **(hands off to #1317 inc.3)** github `resolve()` wires `MCPClient` (via `connect_stdio` using the binding's server ref) → `ResourceHandle | ResolveMiss`. github-mcp-server provisioning (stdio-local vs hosted) = the infra call surfaced when inc.3 starts.

## Test strategy
- **Unit (inc.1)**: in-memory SDK transport + FastMCP fixture — real MCP protocol round-trips with no subprocess (fast, deterministic). Asserts list_resources/read_resource/list_tools/call_tool return real server data.
- **Integration (inc.2)**: spawn a fixture MCP server subprocess via stdio; one round-trip. Proves the real OS-level transport.
- **No regression**: the legacy sim stack is untouched → existing `tests/.../mcp/consumer` (78) + query-router tests stay green. Run the consumer suite after inc.1.

## Rollback
Pure addition (new module + new tests; no edits to live paths). Rollback = delete the new module/tests. Nothing in the live query path changes, so there is no runtime rollback surface.

## Dependencies
- `mcp==1.26.0` (present). #1232 protocol (shipped). #1229 binding storage (shipped, supplies server ref for inc.3). No Arch gate (ADR-070 D5 already rules the protocol; this is implementation).

## AC (for #1220)
- [ ] `MCPClient` exists, backed by the real SDK `ClientSession` (no simulation, no `NotImplementedError`).
- [ ] `connect_stdio(StdioServerParameters)` async-context factory spawns + initializes a real MCP server connection.
- [ ] In-memory round-trip test (inc.1) green: real list/read resource + list/call tool against a FastMCP fixture.
- [ ] stdio subprocess integration test (inc.2) green: real round-trip over OS stdio.
- [ ] Legacy sim stack untouched; consumer suite + query-router tests green (no regression).
- [ ] Legacy-stack cutover explicitly tracked as a separate follow-up (filed), not silently dropped.

## Audit-cascade self-check (GAMEPLAN gate)
- **Template reqs covered**: issue ref ✅ · problem statement ✅ · root-cause/what-exists ✅ · design decision + rationale ✅ · success criteria/AC ✅ · test strategy ✅ · increments w/ scope ✅ · rollback ✅ · dependencies ✅.
- **Drift risks**: (a) touching the live legacy stack → mitigated by Shape B (new client, legacy untouched); (b) subprocess test flake → mitigated by in-memory as the primary unit path, stdio as a separate integration test; (c) scope creep into the legacy cutover → explicitly OUT, filed as a follow-up.
- **No requirement marked N/A without note.** The legacy-cutover follow-up (AC last box) prevents the "minimal deliverable with no fleshing-out plan" trap.
