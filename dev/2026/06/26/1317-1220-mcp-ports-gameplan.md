# Chunk 2 — MCP spine + ports (#1220 WS-8 + #1317 WS-5) gameplan

**Author**: Lead Dev · **Date**: 2026-06-26 · **Design source**: ADR-070 (D3/D5/D6) + the #1232 `Connector` protocol (shipped) + #1229 `ConnectorBinding` storage (shipped).
**This is the bulk** ("heavy two-thirds"). Higher-drift than #1229 (net-new integration + OAuth + external dependency) → real gameplan + audit-cascade gate before building; build in small TDD increments, GitHub first.

## Two Lead-Dev design calls (ADR-070 flagged these for Lead-consultation, not Arch-gated) — RESOLVED
- **OQ-1 (MCP server per connector)** → **github-mcp-server (Anthropic-published) for the GitHub port.** Per the ADR lean (published servers where available; community/build-own at gaps). Revisit per-connector at each port; GitHub is the canonical first.
- **OQ-5 (OAuth-handshake state)** → **the MCP server owns all OAuth state; Piper's `connect()` is a pure redirect-orchestrator.** Piper never stores raw tokens (D3). The binding is created on the **callback** (after the MCP server authorizes), not inside `connect()`.

## What exists (investigated 2026-06-26)
- `services/mcp/consumer/connector.py` — the `Connector` protocol + sum types (`Binding | ConnectRequired`, `ResourceHandle | ResolveMiss`, `ConnectorStatus`, `DegradationResponse`). Shipped #1232.
- `services/mcp/consumer/github_adapter.py` — `GitHubMCPSpatialAdapter` with the 4 protocol methods as **honest stubs** (`degrade()` is fully real; connect/status/resolve degrade-with-"not wired yet"). `IMPLEMENTS_CONNECTOR=True` (m-41 guard).
- `services/mcp/consumer/consumer_core.py` + `services/mcp/protocol/protocol_client.py` (`MCPProtocolClient`) — MCP-client plumbing.
- `services/connectors/binding_repository.py` — `ConnectorBindingRepository` (get/upsert/set_status) — #1229, the storage `connect()`/callback writes + `status()`/`resolve()` read.

## ⚠️ SEQUENCING CORRECTION (found building inc.2, 2026-06-26)
Going to build inc.2 (the OAuth callback), I hit a hard blocker: **Piper's MCP-consumer transport is simulation-only** — `services/mcp/protocol/protocol_client.py:179` `_send_message` raises `NotImplementedError("Real transport not yet implemented")`; `consumer_core` runs `simulation_mode: True`. And **no github-mcp-server is configured** (only the local file-server stdio default). So the github port's connect/resolve (inc.2-3) have nothing real to talk to.

**The real prerequisite is #1220 (WS-8) — building the REAL MCP-consumer transport.** My original ordering (inc.1 then the github connect-flow) was wrong: inc.1 worked because it's pure binding-storage (no transport); inc.2-3 need the transport. So the corrected sequence is: **#1220 real transport FIRST → then github port inc.2-3 on top of it.**

**#1220 is buildable + testable NOW** against the existing local MCP server (`scripts/mcp_file_server.py`, the default `stdio://` target) — it does NOT need github-mcp-server to prove the real stdio transport works. **github-mcp-server provisioning is a later infra decision** (for when the github port actually connects, inc.2-3): how we run it — stdio-local-process (lean; mirrors the file-server pattern) vs hosted-http. Surface that when inc.2 resumes.

## Increments (TDD, GitHub first; each shippable + tested)
**(Revised order: #1220 real transport precedes github inc.2-3.)**
1. **`status()` + `connect()` ↔ binding storage (the D3 read seam).** `status(user_id)` reads the `ConnectorBinding` (owner, "github") → maps stored status → `ConnectorStatus` (no binding → UNBOUND). `connect(user_id)` returns `Binding(id)` if already bound, else `ConnectRequired` (with the connect action-hint). Uses the #1229 repo via the session-scope pattern (mirror `ConnectorConfigService`). **No external server / OAuth yet** — pure storage seam. Tests: bound binding → Binding/BOUND; none → ConnectRequired/UNBOUND. ← **NEXT BUILD**
2. **The connect callback + binding creation.** A web route (the redirect-orchestrator per OQ-5): initiate → github-mcp-server auth → callback creates the `ConnectorBinding(owner, "github", mcp_server_ref, status="bound")`. `connect()` returns `ConnectRequired(action_hint=<connect_url>)` when unbound. Tests: callback creates a bound binding; status flips UNBOUND→BOUND.
3. **`resolve()` via the MCP client.** Wire `resolve(user_id, ResourceQuery("default_repo"))` through `MCPProtocolClient` against github-mcp-server using the binding → `ResourceHandle` | `ResolveMiss`. Folds in **#1230** (resolution) + **#1231** (honest-degrade — replace the canonical_handlers.py silent `return {}` for the GitHub path) + the **#1229 per-connector cleanups** (stale `get_api_key("github")` readers). Tests: resolve hit → handle; miss → ResolveMiss; unbound → degrade.
4. **Cut the live GitHub chat path over to the adapter** behind a marker; retire the native `services/integrations/github` path as parity reaches (ADR-070 D6 m-40 collapse; `is_native_legacy`).
5. **Repeat per connector** (calendar → slack → notion), folding each one's #1230/#1231/#1229-cleanup as it ports.

## Audit-cascade self-check (GAMEPLAN gate)
- Design ruled (ADR-070 D3/D5) + protocol shipped (#1232) + storage shipped (#1229) → the contract + storage are fixed points; drift risk is in the OAuth flow + the live cutover (increments 2 + 4) — gated by tests + the marker.
- Each increment is independently testable + shippable; GitHub-first proves the pattern before the other three.
- m-41 guard already enforces the 4 methods; honest-degrade is structural (no silent-empty).
- Out: the other connectors' MCP-server selection (revisit per port, OQ-1); #1185 multi-tenant (separate beta track).

## AC (for #1317 GitHub port)
- [ ] GitHub adapter's connect/status/resolve wired (no stubs) — connect orchestrates OAuth (MCP-owned), callback creates a binding, status/resolve read it.
- [ ] #1230 (GitHub resolution) + #1231 (GitHub honest-degrade) folded in + verified (no silent `return {}`).
- [ ] Live GitHub chat path cut to the adapter behind a marker; native path retire-ready (D6).
- [ ] Tests per increment; canonical regression green; #1229 per-connector cleanups done.
