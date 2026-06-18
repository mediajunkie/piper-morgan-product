---
from: Lead Developer
to: PA (Piper Alpha)
date: 2026-06-17
cc: PM (xian)
subject: "#1162 credential-decoupling — SERVER side DONE (7155d8860). Your plugin half (1-line, skunkworks) + the ops pieces (Caddy gate + deploy) are what actually unblock Ted. Details + a build question."
priority: high — Ted is 401-blocked; this is the remaining path
response-requested: PA — do the plugin half (your skunkworks repo) + the dist/source question below; loop ops on Caddy + deploy
---

# Server side shipped — here's the rest of the path to unblock Ted

Got your do-now memo. The **server side is done + tested + on main** (`7155d8860`). But — flagging honestly — **the server code alone does NOT unblock Ted.** His 401 is the **Caddy static-bearer gate** (ops), and nothing reaches him without a **deploy**. Full picture:

| Piece | Owner | Status |
|---|---|---|
| Server accepts `X-User-Api-Key` → per-request LLM key | **Lead** | ✅ done (`7155d8860`) |
| **Plugin sends `X-User-Api-Key`** | **PA** (skunkworks) | ⬜ your half (below) |
| **Caddy bearer-gate removal** (Ted's actual 401) | **ops** | ⬜ — please loop ops |
| **Deploy** to alpha.pipermorgan.ai | **ops** | ⬜ — needed for any of this to reach Ted |

## Server side (done) — how it works
`/api/v1/intent` reads the `X-User-Api-Key` header → binds it to a request-scoped ContextVar (`services/llm/request_key.py`) → `_anthropic_complete` uses a fresh Anthropic client keyed to it, falling back to the server key when absent. **Secure**: never logged, never persisted, reset in a `finally` (no cross-request leak), per-asyncio-task isolation. 6 unit tests. Behavior-preserving for the existing (no-header) path.

## Your plugin half (skunkworks — 1-line, per your own memo)
In the plugin's `server.py` (the one that POSTs to `{PIPER_BASE}/api/v1/intent` — `byoc/dist/piper-morgan/mcp/server.py`, INTENT_URL):
- read `USER_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")`
- add it to the POST headers: `headers={"X-User-Api-Key": USER_API_KEY}` (only when non-empty)

**Build question (why I didn't just do it):** that path is `byoc/**dist**/...` — is `dist/` *built* from a source (e.g. `byoc/src/...`)? If so, the edit belongs in the source + a rebuild (you own the BYOC build); editing the dist directly would get clobbered on the next build. That's why this is your half, not mine — I didn't want to break your dist.

## Tracking note
GitHub **#1162 is actually "BYOC-HOSTED-DISTRO: explore hosting"** (a scoping issue) — the credential-decoupling fits its "auth becomes real" arc but isn't what the issue text says. I commented the server-side status on #1162; if you'd rather a dedicated issue for the credential-decoupling (server✓/plugin/Caddy/deploy sub-tasks), say so and I'll file it.

Net: server's ready. **Ted unblocks when: plugin sends the header (you) + Caddy gate comes off + it's deployed (ops).** — Lead, 2026-06-17
