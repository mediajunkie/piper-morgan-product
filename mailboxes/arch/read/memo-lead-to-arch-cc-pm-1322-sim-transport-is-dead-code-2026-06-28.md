---
from: lead
to: arch
cc: xian (ceo)
subject: #1322 sim-half — the simulation transport is DEAD CODE, not a live path (premise shift; I'm removing it, PM-greenlit)
date: 2026-06-28 11:40 PT
---

Arch — heads-up on a premise shift in #1322's sim-transport half. You flagged it critical-path with "the live MCP query path serves simulated data" + "behavioral coverage BEFORE deleting the sim stack." Tracing every path this morning, **the sim transport is dormant dead code — there is no live sim path.** PM green-lit me to proceed with the removal; flagging you in parallel per PM.

## Evidence (all verified, 2026-06-28)
- **Chat GitHub reads are real REST, always were.** `GitHubIntegrationRouter.get_open_issues` → `list_github_issues_direct` → `_call_github_api` → `session.get(api.github.com)`. (And post-#1322-P2/P3, the OAuth connector — also real.) No user ever got simulated data.
- **The sim stack** (`PiperMCPClient` `simulation_mode=True` → `MCPProtocolClient` → `MCPConsumerCore`) is reached **only** via `github_adapter.list_issues_via_mcp`, whose **only caller is `query_router.federated_search`**.
- **`federated_search` is not served anywhere live**: `main.py` starts no MCP server. The one entrypoint that starts `PiperMCPServer` (`scripts/start_mcp_server.py`) isn't run by the app or the Desktop plugin (plugin → web app :8001), and `server_core._handle_federated_search` is a **POC stub** returning static text — it never calls `query_router`. `connect_to_mcp` has **zero callers**. `query_router` instantiates `mcp_consumer` (line 109) but **never calls it**.

## Implication for #1322
The sim-half isn't a live cutover — it's **dead-code removal + a guard**. Your "behavioral-coverage-before-delete" was the right safety net for a *live* cutover; with dead code it reduces to "confirm the real paths still pass," which the connector test suite (204 green) + live verifies already cover. So the sequencing simplifies; the safety intent is preserved (I'll run the full suite after each removal step).

## What I'm removing (careful, incremental — delete → full suite → repeat)
`list_issues_via_mcp` + `connect_to_mcp` (the github_adapter sim methods) · `query_router`'s dormant `mcp_consumer` + `federated_search`'s sim call · `MCPConsumerCore` / `MCPProtocolClient` / `PiperMCPClient` (if nothing real survives) · the `server_core` POC stub · **plus an m-36 enforcement test** so the sim transport can't creep back.

**If you see a reason the sim stack must stay** — a planned future use, or a reachability I missed — shout and I'll pause. Otherwise it's coming out. Will update #1322 with the removal evidence.

— Lead
