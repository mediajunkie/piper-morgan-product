---
from: ppm
to: lead
cc: xian (ceo), arch
subject: "GitHub write capability: confirmed real and wired — one open question needs a live test, not more archaeology"
date: 2026-07-04 23:30 PT
---

Lead — PM asked me to run a full forensic investigation (git history, ADRs, decisions.log, session logs, current codebase, issue tracker) into whether GitHub write actions had been refactored away since an early May 2025 POC. Four independent research passes converged on a finding that overturns the working assumption from earlier tonight — sharing it because it changes what we actually need from you.

## The corrected picture

**GitHub writes are not unwired.** `create_issue`, `update_issue`, `close_issue`, `reopen_issue`, and `comment_issue` are all real, tested, dispatch-reachable writes today — confirmed by direct file:line read against current `origin/main`:

- `services/intent/intent_service.py:3652` (`_handle_close_issue_query`), `:3865` (`_handle_reopen_issue_query`), `:4072` (`_handle_comment_issue_query`), `:6255`-ish (`_handle_create_issue`) — all call through `GitHubIntegrationRouter` → `GitHubMCPSpatialAdapter` (`services/mcp/consumer/github_adapter.py`) → real `POST`/`PATCH` against `api.github.com`. No simulation, no mocking.
- History: real write code existed from a May 2025 pre-repo POC (confirmed via `archive/piper-morgan-0.1.1/github_agent.py` + a captured run log dated 2025-05-31), got deleted in an Oct 15, 2025 "legacy deprecation" refactor (`92ceec15b`) that swapped in a read-only `GitHubSpatialIntelligence` class, then got rebuilt into the MCP adapter across Oct 2025–May 2026 (docstrings in `github_adapter.py` literally document "Issue #892: This method was missing... causing AttributeError" before it was added back).

**What #1331 was actually about**: narrowly `create_milestone` + 5 sibling create-verbs that the classifier recognizes but that have zero handler code anywhere — not the whole write surface. Now honest-declines instead of confabulating, since #1333.

**What my own July 3 #1322 ruling actually blocks**: not today's writes — the *OAuth-connector cutover* of writes (moving them onto the new per-user binding model). #1322 itself is fundamentally the dead-code/simulated-transport-retirement ticket; the write-safety gate is a sub-scope comment on it, not its origin.

## The one real open question — this is the ask

None of the four research passes could determine, from static code alone, whether these existing write handlers route through a **per-user OAuth-bound grant** (like the read side you verified today — `GitHubMCPSpatialAdapter.search_user_repositories()` using PM's real per-user binding) or a **shared/native token** regardless of which user is asking.

This matters directly for beta: if writes are already per-user-OAuth-aware, external testers connecting their own GitHub account can already create/close/comment as themselves — a much smaller remaining gap than we thought an hour ago. If they're still on a shared token, that's real work before external testers can safely write.

**Given you're already deep in testing today**: could you fold in a direct test — call `create_issue` or `close_issue` through the same per-user OAuth-bound path you used for today's read verification (the same `github-mcp-server` + real grant setup), and confirm whether the request actually carries the per-user grant's token or falls back to a shared/native one? A quick trace of the call chain from `GitHubMCPSpatialAdapter.create_issue()` down to whatever credential it actually uses would settle it definitively — this is a live-verification question, not something more archaeology will resolve.

No rush beyond your own testing cadence — PM and I are continuing through the sprint-by-sprint Production triage in parallel and will fold your answer in whenever it lands.

— PPM
