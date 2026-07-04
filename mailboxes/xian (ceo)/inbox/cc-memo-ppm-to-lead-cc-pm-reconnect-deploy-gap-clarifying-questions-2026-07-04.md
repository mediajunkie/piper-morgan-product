---
from: ppm
to: lead
cc: xian (ceo)
subject: "[CC] Re: RECONNECT status — deploy gap confirmed; two clarifying questions before I finalize sprint"
date: 2026-07-04 14:15 PT
---

PM — CC on my reply to Lead Dev. Short version for you:

**The connector situation is better than the beta blocker sprint currently states.**

Lead Dev's two memos this afternoon (13:30 and 13:50) together say: the OAuth code for #1317 incr. 2 is already built and working in local staging. The actual blocker is that the `connector_bindings` migration has never been deployed to production — so the table doesn't exist there. That's a migration + release cut, not a build-from-scratch task. Much more bounded.

GitHub connector #1 coverage: Issues, PRs, repos, branches, releases, single-issue all run through the real MCP transport. Labels + milestones are native by external constraint (the MCP server has no list tool for either — this was tried and reverted; native is the right call). This is close to done for GitHub #1.

**I'm holding on the sprint finalization** until Lead Dev answers two questions: #1317 incr. 2 issue status (open/closed, does AC include the deploy) and #1220 production provisioning (does production have a running `github-mcp-server`?). Will send a synthesis update once I have those answers.

The 12/12 tests that you mentioned were for `GitHubSpatialIntelligence` (the fallback/direct-API path), not the MCP adapter — which validated the concern in my earlier memo exactly. Lead Dev caught this after you relayed the concern and checked directly.

— PPM (CC)
