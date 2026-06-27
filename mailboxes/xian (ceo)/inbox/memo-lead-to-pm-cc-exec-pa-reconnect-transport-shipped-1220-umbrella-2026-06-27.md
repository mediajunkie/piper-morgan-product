---
from: lead
to: xian (ceo)
cc: exec, pa
subject: RECONNECT — real MCP transport shipped (the 6/26 blocker); #1220 is the umbrella, kept open
date: 2026-06-27 08:15 PT
---

PM — two linked updates from this morning's RECONNECT drain, one a milestone, one a scope correction you'll want for sprint accounting.

## 1. Milestone: the real MCP transport is shipped (this was yesterday's hard blocker)

Yesterday I found the GitHub port's connect/resolve was blocked because Piper's MCP-consumer transport was **simulation-only** (`protocol_client.py` raised `NotImplementedError("Real transport not yet implemented")`). That's now fixed:

- **`MCPClient`** (`services/mcp/consumer/mcp_client.py`) over the official MCP SDK (`mcp==1.26.0`, already a dependency) — real `list_resources`/`read_resource`/`list_tools`/`call_tool` + a `connect_stdio()` production factory.
- 6 tests: real protocol round-trip via the SDK's in-memory transport against a FastMCP fixture, **and** a real stdio-subprocess round-trip. 84/84 consumer + 11/11 query-router (the live path) green — **zero regression** (built as a new client, left the live simulated path untouched).

This is the spine every connector port needs. The GitHub port's `resolve()` rides on it next.

## 2. Scope correction: #1220 is the UMBRELLA, not "the transport" — I kept it open

Going to close #1220, I read its full body first (close-issue-properly) and caught that our carry-forward/chunking had compressed it. **#1220 is the §0 anchor/umbrella for the whole connection/auth → MCP migration** — its AC are "bespoke OAuth flows retired," "per-user scoping preserved," "Arch cross-validation." It is not closeable by building a transport.

So I:
- **Kept #1220 OPEN** and posted a progress comment (hard-blockers #1232 + ADR-070 now cleared; transport infra shipped; remaining = the per-connector auth migration + bespoke-flow retirement).
- **Filed #1322** for the genuine follow-on (migrate the live `query_router` off the simulated stack onto `MCPClient`, retire the dead sim transport).
- Recorded the transport as infrastructure *under* the umbrella.

**What this means for the board**: the transport is progress *within* #1220, not a new closed WS — so it doesn't change the RECONNECT "done" count. #1220 (umbrella) closes behind #1317 (the ports), which are the real Chunk-2 bulk. The chunking still holds; only the "#1220 = transport, build-and-close" framing was wrong.

## Next (continuing the drain per Exec's keep-draining-ports green light)
**#1317 GitHub inc.3 — `resolve()` via `MCPClient`** (fold in #1230/#1231/#1229 per-connector cleanups). Buildable + tested now against a FastMCP fixture. **One infra decision ahead** (flagging early, not blocking): the *live* GitHub hookup needs **github-mcp-server** provisioning — stdio-local-process (lean, mirrors the fixture) vs hosted-http. The fixture proves the `resolve()` logic without it; I'll bring you the options when the live hookup is the actual next step.

No reply needed unless you see the #1220-umbrella read differently, or want the transport tracked as its own closeable sub-issue rather than #1220-progress (my default: leave it as #1220-progress).

— Lead Dev
