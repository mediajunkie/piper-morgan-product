# #1322 cutover — chat GitHub reads → per-user OAuth connector (gameplan)

**Date**: 2026-06-27 · **Role**: Lead Dev · **Issue**: #1322 (RECONNECT consumer cutover)
**Foundation**: #1317 OAuth connector shipped + proven live (get_me + search_issues→179 + list_issues). Connector rail (binding-aware honest-degrade + `_mcp_client_ctx` connect_http) in `services/mcp/consumer/github_adapter.py`.

## What the cutover redirects
Chat GitHub reads run through intent handlers (`services/intent/intent_service.py`):
`_handle_list_issues_query` → `GitHubIntegrationRouter().get_open_issues()` → **native PAT** (`GitHubConfigService.get_authentication_token(user_id or "system")`). Handlers **already thread `user_id`** (`initialize(user_id=_user_id)`, #891) → no D4 threading work needed. Siblings: `_handle_close_issue_query`, `_handle_comment_issue_query`, list_prs/branches/labels/milestones/releases.

## Product decision flagged for PM
The native path is **repo-scoped** (resolve_repo → one repo's open issues). The connector path uses **`search_issues("assignee:@me is:open is:issue")` — user-wide, your assigned issues across all repos** (no repo resolution → sidesteps the vestigial `resolve_repo`/#1230, per PM "don't polish vestigial pathways"). This is a **semantic improvement** ("your issues" vs "one repo's issues") but a behavior change. Proceeding on user-wide; flagging for PM override.

## Phases (TDD, additive, zero-regression)
- **P1 — connector fetch primitive** (this slice): `GitHubMCPSpatialAdapter.list_open_issues(user_id, limit)` → `GitHubIssuesResult(issues | degradation)`. Mirrors `resolve()`'s rail: no binding → CONNECT_REQUIRED degrade (+ connect link); non-bound → honest reason; bound → `_mcp_client_ctx` → `search_issues` → parse → issues; failure → UNREACHABLE. TDD vs a FastMCP `search_issues` fixture. **No handler change yet → zero regression.**
- **P2 — wire `_handle_list_issues_query`**: prefer the connector when the user has a binding; on CONNECT_REQUIRED degrade → honest message + connect link; **fall back to native PAT only if no binding** (transitional, layer-then-migrate D6). Real-path test.
- **P3 — siblings**: extend to close/comment/list_prs/etc. (each its own small slice).
- **P4 — retire native** (D6): once all read paths cut over + a beta of confidence, drop the PAT fallback + `GitHubConfigService` native token. Separate, later.

## AC (this pass = P1+P2)
- "How many open issues?" in chat, for an OAuth-connected user, answers from the **connector** (binding + grant + search_issues), not the PAT.
- Not connected → honest "Connect GitHub" message + the connect link (never silent-empty, #1231).
- Existing PAT users unaffected (fallback) until P4.
- Tests: P1 fixture rail (hit + 3 degrade reasons + empty) ; P2 handler prefers connector / degrades / falls back.
