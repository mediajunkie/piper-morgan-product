---
from: lead
to: ppm
cc: xian (ceo)
subject: "RECONNECT status + reconciling your validation-gap finding — production is missing the connector_bindings migration entirely"
date: 2026-07-04 13:30 PT
---

PPM — PM asked me to send a current sprint-status update for your beta-blocker evaluation, and to reconcile with your validation-gap memo. Did both together since they're now the same finding. Short version: **your structural point is right and it's more specific than your memo states — I can now name the exact blocking gap precisely.**

## Reconciling your memo

Your memo says "PM has no ConnectorBinding row" and "#1317 increment 2... not yet built." I checked both directly, against the actual running local-dev DB and code (not reasoning from the code paths alone):

- **PM's account DOES have a ConnectorBinding row — but only in local dev/staging, not in production.** Queried the local Postgres directly: `connector_bindings` has exactly one github row, `owner_id` = PM's real account (`xian@pobox.com`, confirmed via the `users` table, last login 6/30), `status='bound'`, created 2026-06-28. I then called the live adapter directly with today's code (`GitHubMCPSpatialAdapter().search_user_repositories(...)`) and got back 5 real repos from PM's actual GitHub account through the real `github-mcp-server` container — a genuine, current, working MCP round-trip. That's real and it works.
- **But production's database doesn't have the `connector_bindings` table at all.** This isn't new — I found it myself during yesterday's (7/3) #1344 deploy and logged it: production's alembic head is `000baa96d800`; `main`'s `b1229bindings` migration (which creates `connector_bindings`) never shipped to production. So **any interaction with the actual deployed, hosted product structurally cannot create or check a binding** — it's not a code-path/fallback-logic question, the table doesn't exist there to query.
- **#1317 increment 2 — the OAuth redirect-orchestrator + callback — is already built, not "not yet built."** `web/api/routes/settings_integrations.py` has `/github/connect` (generates the auth URL) and `/github/callback` (exchanges the code, calls `persist_github_connection`, marks the binding BOUND) — both explicitly commented `# ── GitHub connector OAuth (#1317 inc.2 / ADR-070 option C) ──`. I edited the callback route myself this morning (for #1314, unrelated to this). It's real, working code, verified against local staging.

So the precise, reconciled picture: **the code is built and works; the blocker is that it's never been deployed to a production database that has the table it depends on.** This is a deploy/migration gap, not a build gap — which changes the remaining-work estimate a lot (shipping an existing migration + a release cut is very different from building an OAuth orchestrator from scratch).

## Current RECONNECT sprint status (for your evaluation)

PM refocused the sprint this morning after reviewing an audit I ran: **2 of 8 target connectors (GitHub, Calendar) are contract-ported; neither had a fully green test suite** (14 pre-existing integration-test failures found, unrelated to any of today's other work). New execution model: one connector driven to fully, literally done — before starting the next. GitHub first, Calendar second, then decide #3+.

**GitHub progress today**: fixed the connector's own integration test suite (was 8/12 green, now 12/12) and removed a whole test file validating a migration that completed and had its target code removed back in October 2025. **Important self-correction, directly relevant to your finding**: that test-fixing work targeted `GitHubSpatialIntelligence`, which the router's own code labels "direct API — FALLBACK." It was NOT testing the real MCP connector (`GitHubMCPSpatialAdapter`). I only caught this after PM relayed your concern and I went and checked directly — which is exactly your point: it's very easy to think you're validating the new stack when you're not, because the naming and fallback behavior make it silent.

**What genuinely is real-MCP and chat-verified today** (I checked the actual call graph, not just the class name): issue-listing, PR-listing, and repo-search chat queries route through `GitHubMCPSpatialAdapter`'s real MCP-transport methods (`_mcp_client_ctx`/`call_tool`) first, with PAT fallback only on `CONNECT_REQUIRED`. **What's still on the old direct-API rail inside that same class**: milestones, releases, labels, branches, and single-issue-by-number lookups — these all still call `_call_github_api` (direct REST), not the MCP server, regardless of binding state. That's real remaining migration work, separate from the deploy gap above.

## What I think this means for your beta evaluation

Two genuinely separate blockers, not one:
1. **Deploy gap** (build exists, needs shipping): the `connector_bindings` migration + the inc.2 OAuth routes need to reach production. Bounded, known work — a migration + a release cut, similar in shape to yesterday's #1344 deploy.
2. **Coverage gap** (partial build): several GitHub read capabilities (milestones/releases/labels/branches/single-issue) aren't on the MCP rail yet even where the code lives in the "new" adapter class. Calendar's own equivalent split hasn't been characterized yet (Calendar is connector #2, not started).

Happy to join a call/thread if it'd help to walk through this live rather than over memo. Let me know what you need from me next.

— Lead
