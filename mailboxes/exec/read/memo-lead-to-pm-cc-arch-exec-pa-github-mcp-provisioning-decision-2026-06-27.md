---
from: lead
to: xian (ceo)
cc: arch, exec, pa
subject: Decision needed — github-mcp-server provisioning: hosted-OAuth (D3-aligned) vs local-stdio-PAT
date: 2026-06-27 08:25 PT
---

PM / Arch — follow-through on this morning's note: the GitHub connector is now fully protocol-wired (connect/status/resolve are binding-aware + honest-degrade, riding the real `MCPClient` transport shipped today). The one thing between it and a live GitHub port is **how we run github-mcp-server**. I researched the real options today (GitHub's official server) so you can decide on grounded facts, not my guess.

## The two real options

**A — Hosted remote (recommended).** GitHub's managed endpoint `https://api.githubcopilot.com/mcp/` (GA Sept 2025). Auth is **OAuth 2.1 + PKCE**; the **server owns the token** (held server-side, not by us).
- **D3-aligned**: this is exactly ADR-070 D3 ("the MCP server owns OAuth; Piper stores bindings, never raw tokens") + ADR-058 per-user OAuth. Our `connect()` orchestrates the OAuth redirect; the callback stores a **binding** (#1229), never a token.
- **Ops**: nothing to run/patch/rotate on our Droplet (GitHub runs it).
- **Cost**: needs a **streamable-HTTP transport** added to `MCPClient` — my #1220 transport is stdio-only so far. The SDK ships the HTTP client; it's a small additive increment mirroring `connect_stdio`. Plus an external dependency on GitHub's endpoint (GitHub-run → reliable).

**B — Local stdio (Docker/binary).** `ghcr.io/github/github-mcp-server` (or the Go binary) run as `github-mcp-server stdio`, authenticated by a `GITHUB_PERSONAL_ACCESS_TOKEN` env var.
- **Fits my current transport exactly** — `connect_stdio` already spawns stdio servers (this is literally what #1220 inc.2 proved). No new transport needed.
- **But it re-introduces raw-token custody**: for multi-user, Piper would have to hold each user's **PAT** (even encrypted via #358) to inject into that user's subprocess env. That's the exact custody D3 moved us *away from*. Viable, but it works against the ADR's intent.
- **Ops**: per-user subprocess management on the Droplet.

## Recommendation
**A (hosted-OAuth).** It realizes D3/ADR-058 cleanly — the whole reason WS-2 collapsed to "bindings, not credentials" was to stop holding raw tokens, and A is what makes that real for GitHub. B is faster to wire (no new transport) but re-introduces the credential custody we just designed out. The only real cost of A is the HTTP transport increment, which is independently worth having (most hosted MCP servers use HTTP, not just GitHub).

This is your / Arch's call (the #1220 issue frames provisioning as an Arch/CIO architecture-direction decision).

## What I'll do meanwhile (not blocking on your answer)
I'll **complete `MCPClient`'s transport to support streamable-HTTP alongside stdio** — both are standard MCP transports and hosted servers are common, so this is correct *regardless* of the GitHub call (it just also de-risks option A). The GitHub-specific deployment + the inc.2 OAuth callback wait on your decision.

## Ask
**A or B?** And any constraint on taking a hosted external dependency (cost / data-policy / preferring self-hosted)? If A, I'll wire the OAuth-callback binding-creation against the hosted endpoint next; if B, I'll wire the PAT-env subprocess path (and we should pair it with the #358 encrypted store).

— Lead Dev

Sources: [github/github-mcp-server](https://github.com/github/github-mcp-server) · [GitHub Blog — practical guide to the GitHub MCP server](https://github.blog/ai-and-ml/generative-ai/a-practical-guide-on-how-to-use-the-github-mcp-server/)
