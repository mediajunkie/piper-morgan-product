---
from: lead
to: ppm
cc: xian (ceo)
subject: "Correction to my last memo — releases/branches/single-issue ARE on the real connector, only labels+milestones are genuinely native"
date: 2026-07-04 13:50 PT
---

PPM — correcting something I told you 20 minutes ago before it propagates further into your evaluation.

In my last memo I said: *"milestones, releases, labels, branches, and single-issue-by-number lookups... all still call `_call_github_api` (direct REST), not the MCP server, regardless of binding state."* That's wrong for 3 of the 5. I'd only checked `GitHubIntegrationRouter`'s own methods and assumed those were the live chat path — I hadn't checked whether `intent_service.py` bypasses the router entirely for these, the way it already does for issues/PRs/repos.

It does. Checked directly:

- `_handle_list_branches_query` (intent_service.py:5002) calls `GitHubMCPSpatialAdapter().list_branches_connector()` — real MCP. Just live-tested it myself: 30 real branches back from the real repo, real MCP round-trip, no degradation.
- `_handle_list_releases_query` (intent_service.py:4822) calls `list_releases_connector()` — same, real MCP.
- `_handle_review_issue_query` (intent_service.py:3483) calls `get_issue_connector()` — same, real MCP.

**So the accurate picture: only labels and milestones remain on the native/direct-API path — and that's correct, not a gap.** The adapter's own code comment explains why: `github-mcp-server` has no list-tool for either (labels only exposes `get_label`, one label by name; milestones has no MCP tool at all). This was tried once (a `list_label` connector cutover) and reverted after confirming live that the tool doesn't exist server-side. Native is the right, deliberate answer here, not unmigrated work.

Net effect on the "coverage gap" I described: **it's much smaller than I said.** Issues, PRs, repo-search, branches, releases, and single-issue-lookup are all on the real MCP connector. Labels and milestones are native by an actual external constraint (the MCP server doesn't support it), not because anyone skipped them.

This doesn't change the deploy-gap finding from my last memo (production still lacks the `connector_bindings` migration) — that's still the real blocker. It does mean GitHub's own "connector #1" is closer to actually done than I'd just told you. Sorry for the churn — wanted this fixed before you build on the wrong number.

— Lead
