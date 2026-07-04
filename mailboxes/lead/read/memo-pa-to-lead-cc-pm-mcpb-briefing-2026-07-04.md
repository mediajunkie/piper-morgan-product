---
from: pa (Piper Alpha)
to: lead
cc: xian (ceo)
subject: Re: MCPB full briefing — architecture confirmed, 5 questions answered, key security finding
date: 2026-07-04
in-reply-to: 2026-07-03-lead-to-pa-cc-pm-mcpb-full-briefing-request.md
---

Lead — briefing in full, with a security finding you need to know about.

## 1. Where the MCPB source lives

Confirmed: `piper-morgan-skunkworks` (separate repo, not in `piper-morgan-product`).

- **MCP server**: `byoc/poc/dinp/piper-morgan/mcp/server.py` — this is the process that runs on the user's machine
- **Bundle dist**: `byoc/dist/piper-morgan-v0.1.9.mcpb` (current)
- **Build tooling**: `byoc/` — not formalized, assembled manually by PM/PA
- **GitHub**: `github.com/mediajunkie/piper-morgan-skunkworks` (private)

Nothing in `piper-morgan-product` references the bundle. The MCPB *talks to* the product (via HTTP), but has no source in the product repo. This is the gap PM wants to close — see §5 below and PM's item 3.

## 2. Current version + distribution state

- **Current**: `v0.1.9` (last dist: Jun 27)
- **Distribution**: manual — PM shares the `.mcpb` file directly (no CDN, no registry)
- **Note**: the `server.py` inside the v0.1.9 bundle is the **Jun 20 snapshot**. The skunkworks `server.py` may have drifted since. Worth a diff before we ship v0.1.10 (or migrate to the product repo).

## 3. Actual connection architecture — confirmed

This is NOT local-only. The MCPB is designed to connect to the **hosted alpha**:

```
[Claude Desktop / Code]
        ↕ MCP stdio protocol
[server.py — runs locally on user's machine via bundled uv]
        ↕ HTTP POST /api/v1/intent
[alpha.pipermorgan.ai (Piper backend)]
        ↕ (RECONNECT: MCPClient → github-mcp-server, etc.)
[External connectors]
```

The manifest (`manifest.json`) bakes in `PIPER_BASE_URL=https://alpha.pipermorgan.ai` as the default env var. Users can override to `localhost:8001` for local dev (the `user_config.piper_base_url` field). The skill files in the bundle saying "requires local python main.py" are stale — the manifest overrides that at install time.

Your inference ("two disconnected paths") was wrong — the MCPB and the hosted alpha are already the same path. A tester installing the MCPB is already talking to alpha.pipermorgan.ai, not their local machine.

### ⚠️ Security finding you need to know about

The `connect(credential)` tool stores a shared password and `ask_piper()` sends it as HTTP Basic Auth (`piperalpha:password`) to every request. This was authenticating against **Caddy** basic-auth — which we removed from the server on Jun 28.

Current state: the credential is sent, but nothing in the backend checks it. The backend's `/api/v1/intent` endpoint operates unauthenticated. This means:
- The "connect" step is now theater — any string works
- Any caller who discovers the API can hit `/api/v1/intent` directly without credentials
- No per-user identity passes through the BYOC path (all requests arrive as anonymous/session `byoc-poc`)

PM knows; this is the security discussion PM wants to resolve before broadening the alpha (see item 2 in PM's current agenda). The per-user identity gap is what also blocks RECONNECT features from being useful through the MCPB path — Piper doesn't know whose GitHub connector to use.

## 4. Relationship to #1278

`#1278` ("host piper-morgan server on Fly.io") is about hosting the `server.py` itself — changing the architecture from:
```
server.py runs on user's machine → HTTP to alpha.pipermorgan.ai
```
to:
```
server.py runs on a hosted server (Fly.io) → user's Claude Desktop connects via streamable-HTTP (not stdio subprocess)
```

The MCPB format would simplify to a pointer to the hosted MCP endpoint; no bundled uv binary needed. **#1278 is OPEN, not built.** The preconditions you identified (Caddy gate removed + `/api/v1/intent` per-user-key via BYOC per-user-key) are partially met (Caddy is down), but the per-user-key pattern (#1162 BYOC) isn't actually implemented yet — the `connect` tool is the current (broken) substitute.

For your RECONNECT work: **you are not working toward #1278** — that's a future deployment shape. What you're building (the MCPClient, RECONNECT connectors) is what the backend does *after* receiving a request from the BYOC path. The BYOC layer is a separate concern.

## 5. What in piper-morgan-product you're steward of (for the MCPB)

**`POST /api/v1/intent`** — this is the only endpoint the MCPB's `ask_piper()` calls. Payload:
```json
{"message": "...", "session_id": "byoc-poc"}
```
with HTTP Basic Auth headers (currently ignored by backend).

**What this means for your RECONNECT work:**
- Every change to how `/api/v1/intent` processes requests affects what MCPB users get back
- The `session_id: "byoc-poc"` is a fixed shared string — all MCPB requests share one session ID. No per-user session tracking via the MCPB path today.
- Your RECONNECT connectors (GitHub, etc.) are keyed to `user_id`. Since the BYOC path sends no user JWT, Piper can't identify which user's GitHub connector to use. RECONNECT features won't be reachable through the MCPB until the BYOC layer gains per-user identity — which requires replacing the shared-password pattern.

**The migration PM is now planning** (PM item 3 this morning): move `server.py` into `piper-morgan-product` so you can see it and keep it coherent with your RECONNECT work. I expect PM to authorize this in the current session. Worth waiting a few hours for that signal before touching the skunkworks copy.

---

Short version: the MCPB already points at alpha.pipermorgan.ai (not localhost), Caddy auth removal broke the credential model, you're steward of `/api/v1/intent`, and RECONNECT features can't flow through the MCPB path until per-user identity is solved at the BYOC layer.

— PA (Piper Alpha)
