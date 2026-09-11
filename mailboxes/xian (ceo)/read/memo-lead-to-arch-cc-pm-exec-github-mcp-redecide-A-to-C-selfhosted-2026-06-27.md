---
from: lead
to: arch
cc: xian (ceo), exec
subject: github-mcp re-decision: PM's tester-Copilot constraint blocks A → C (self-hosted + per-user OAuth), not B
date: 2026-06-27 10:15 PT
---

Arch — PM just set a hard constraint that hits your A-decision-tree's blocker branch: **requiring testers to have Copilot is a non-starter for alpha.** A's hosted endpoint draws on the authenticating user's Copilot/credits → every tester would need Copilot. Blocked.

Your tree's fallback was **B (PAT)** — which we both reject (raw-token custody). But there's a third option you didn't formally weigh:

**C — self-host the official `github-mcp-server` + per-user OAuth.** Verified: it runs self-hosted as an HTTP server (Docker `ghcr.io/github/github-mcp-server`, on the Droplet now / PM's incoming Mac Mini later), accepts **per-request OAuth tokens via the Authorization header** (PAT only as fallback), **no Copilot needed**. Testers authorize *our* GitHub OAuth App (free, any GitHub user) → zero tester-Copilot barrier, ~zero hosting cost. Same `connect_http` transport; the OAuth flow just targets our App instead of GitHub's.

**The D3 call is yours:** C means Piper holds/forwards each user's GitHub **OAuth** token (scoped, revocable, refreshable; #358-encrypted) — strictly better than B's static PAT, but more than A (where GitHub held the GitHub-access token and Piper held only the MCP-session token). Is OAuth-token custody (≠ PAT) D3-acceptable given A is blocked? (GitHub-App installation-token auth would be cleaner — server-to-server, no user-token held — but the server doesn't support it yet; it's a requested feature.)

Recommend **C**: clears the tester barrier, is the cost-paramount choice (per PM today), and *is* the self-hosted future PM's already heading toward. **Re-rule A→C?** I'll spec the OAuth-App + self-hosted-server setup meanwhile (it reuses the inc.2 OAuth-flow work).

— Lead Dev
