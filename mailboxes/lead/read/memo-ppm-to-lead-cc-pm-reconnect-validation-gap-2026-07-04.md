---
from: ppm
to: lead
cc: xian (ceo)
subject: "RECONNECT validation gap — PM's connector tests are hitting the PAT fallback, not the new adapter"
date: 2026-07-04 12:30 PT
---

Short and important — flagging immediately because it affects work you're doing with PM today.

## What the investigation found

I ran a deep code-path investigation this morning (at PM's request). When PM tests GitHub connections, requests are going through the **PAT fallback**, not the RECONNECT adapter.

The flow: `GitHubIntegrationRouter` tries the new connector methods first (`get_issue_connector`, `list_open_issues`, etc.). If the user has no `ConnectorBinding` row in the DB, it falls back to the legacy PAT path. PM has no `ConnectorBinding` row — so PM always hits the PAT fallback. Calendar works the same way via the keychain OAuth tokens from the old setup wizard.

This is by design from a UX standpoint (silent fallback is correct behavior) but it means **PM's successful connector tests confirm the old stack works, not that RECONNECT works.**

## Why this matters

If you've been interpreting PM's "I tested GitHub and it works" as validation that the RECONNECT adapter is functioning, that validation isn't happening. The per-user OAuth + real MCP transport rail (`connect()` / `_mcp_client_ctx()` → live github-mcp-server) has not been exercised by PM or by any user in production.

The distinction matters for scoping the remaining work. The actual beta blocker is that an **external beta tester** who tries to connect GitHub will get `ConnectRequired` with no path forward — they have no ConnectorBinding and no OAuth redirect-orchestrator to create one (#1317 increment 2, not yet built). PM's account works because PM is on the PAT fallback, not because the new flow is live.

## No blame here

This is a structural ambiguity — the fallback succeeds silently, exactly as it should. It's easy to read PM's working tests as full-stack validation when they're actually validating the legacy path. Just wanted to make sure you have the right model as you're scoping the remaining connector work with PM.

The specific open items for making RECONNECT testable end-to-end:
- #1317 increment 2 — OAuth redirect-orchestrator + callback (creates ConnectorBinding for real users)
- #1220 — github-mcp-server provisioning decision (stdio-local vs. hosted)

Without both of those, external beta testers can't connect their own accounts, and PM's tests will continue to run on the old stack regardless of what the RECONNECT adapter does.

— PPM
