# Lead Dev carry-forward (ephemeral — read at fire-time, not frozen in the prompt)

**Updated**: 2026-06-28 ~13:00 PT. Sole lead. Session log: `dev/2026/06/28/2026-06-28-0823-lead-code-opus-log.md` (continues 06-27).
**Mode**: PM away most of 6/28, maybe until 6/29 — authorized autonomous RECONNECT work. **RUN LEAN (KEEP tier, 3×/day cron) through Wed Jul-1 ~9pm** (PM quota throttle, Exec memo).

## ▶ AUTONOMOUS QUEUE — what to advance each fire (in order, all unblocked, no PM needed)

**1. #1322 sim-transport retirement — increments 2–5 (PM-greenlit, Arch-flagged; dead-code removal).**
Executable plan + proof on **#1322 comment 4827173746**. The sim transport (`PiperMCPClient simulation_mode=True` / `MCPProtocolClient` / `MCPConsumerCore`) is DEAD CODE (chat GitHub = real REST always; sim reached only via an unserved `__main__` demo). **Arch CONCURRED 6/28 ("remove it", owns the live-path overstatement; strongly endorses the m-36 guard).** **Increments 1–2 DONE** (inc.1 `d61987a70`: `query_router_spatial_migration.py` + 8 federation/pm033c integration tests; inc.2: `query_router.federated_search` + dormant `mcp_consumer` wiring [import/param/2 init lines] + `test_pm033c_mcp_server_config.py` removed — 176 green, integration collects 890 clean). **Remaining (delete → full suite → commit, each its own increment):**
  - ~~inc.2~~ ✅ DONE.
  - **inc.3 (SCOPED 6/29 — bigger than first thought; github_adapter has ~6 `mcp_consumer` sites)**: remove the import (`from .consumer_core import MCPConsumerCore`, L41) + the attr (`self.mcp_consumer = MCPConsumerCore()`, L97) + the **caller-less dead methods** `connect_to_mcp` (L915), `list_issues_via_mcp` (L1119), `get_issue_via_mcp` (L1202) [verified: zero real callers]; and remove **only the mcp_consumer reference lines** inside `get_mapping_stats` (L1267 — the `"mcp_connected": self.mcp_consumer.is_connected()` key) + `disconnect` (L1289 — the `await self.mcp_consumer.disconnect()` line) — **keep those two methods, they do other things**. + delete tests `tests/unit/services/mcp/consumer/test_github_adapter_demo_fallback_1088.py` + `tests/integration/test_mcp_consumer_demo.py`. Re-verify `get_issue_via_mcp`/`get_mapping_stats`/`disconnect` have no real callers at execution time. (The #1088 demo-fallback fixture was already removed earlier — see L1157 comment; just the method shell remains.)
  - **inc.4**: the now-orphaned sim classes — `MCPConsumerCore` (`consumer_core.py`), `MCPProtocolClient` (`protocol/protocol_client.py` + `protocol/__init__.py` + `service_discovery.py`), `PiperMCPClient` (`client.py`), `PiperMCPServer` (`server/server_core.py`) + `scripts/start_mcp_server.py` (+ `test_dual_mode.py` + any remaining sim test). Verify each is import-orphaned first.
  - **inc.5**: m-36 enforcement test (`test_architecture_enforcement.py`) — sim transport / `simulation_mode=True` can't re-enter the live import graph.
  - **Safety**: run `pytest tests/unit/services/mcp/consumer/ tests/unit/services/intent_service/test_github_query_handlers.py` + `pytest tests/integration/ --collect-only` after each delete (the collect-only catches orphaned importers — it caught the pm033c runner straggler in inc.1).

**2. #1327 default-repo mechanism (PM Q2 6/28) — the foundation that unblocks repo-scoped reads + writes.**
Build on the live `_resolve_from_user_default` path (#1226/#1199, reads `default_repository` from DB). Needs: (a) a way to SET the default repo — **the set-default UX may want CXO/PM input → flag before building UI; the backend (service method + endpoint) is buildable**; (b) wire the repo-scoped read handlers (branches/labels/milestones/releases/review-issue) to resolve via it through the connector + honest-degrade when unset (#1231). This is also the hierarchy's step-4 default (#1327).

## ▶ PM-GATED (do NOT do autonomously — need PM/CXO)
- **Writes cutover (close/comment) — #1322 Q3 DECIDED "cut over", but the live write needs PM.** Path is capable (grant has `repo` scope; `issue_write`/`add_issue_comment` exist). Build the handlers (connector write, TDD vs fixture) AFTER #1327 (writes are repo-scoped). **First REAL write = PM picks a target during testing / a clearly-marked throwaway — never an unsolicited write to a live issue.**
- **set-default-repo UX** — coordinate w/ CXO if it's user-facing UI.
- **Alpha release** (main→production, 536 commits behind, v0.8.9) — PM-gated, NOT now. The connector ships in a future release.

## ▶ STATE (end 6/28) — the connector WORKS in local staging
- **GitHub MCP connector LIVE (local staging, decoupled from any release).** OAuth connect → binding BOUND → reads PM's real GitHub via `connect_http` + the #358-encrypted grant: `get_me`→mediajunkie, `search_issues`→179, `search_pull_requests`→2. inc.2 (OAuth flow) code-complete + the "Connect with GitHub" button + the `/github/oauth-status` badge all shipped.
- **Chat reads cut over (#1322 P2/P3, verified live):** `_handle_list_issues_query` (179), `_handle_list_prs_query` (2), `_handle_stale_prs` (2 found) — connector-first, native-PAT fallback only if not OAuth-connected, honest-degrade otherwise; count by `total_count` (the 30-vs-179 fix). Semantics = user-wide (`assignee:@me`/`author:@me`) = the #1327 get-all default.
- **Staging stack UP** for PM testing: `github-mcp-server` container `piper-ghmcp` :8082 + app :8001 (latest code). PM binding bound (user `a25db09c-6d79-41e4-8d82-87b6a005bbb0`). PM's browser JWT expires → re-login before UI testing. **Test plan delivered**: `dev/2026/06/28/reconnect-github-test-plan-2026-06-28.html`.
- **PM decisions 6/28**: Q1 resolution hierarchy (explicit→infer+trust→ask→default) + Q2 default-repo → **#1327**; Q3 writes cut over → **#1322 comment 4828041009**.

## ▶ STATE / refs
- **Restart staging app** (from worktree, picks up code): `env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS POSTGRES_PORT=5433 GITHUB_MCP_SERVER_URL=http://localhost:8082/mcp nohup /Users/xian/Development/piper-morgan/piper-morgan-product/venv/bin/python main.py > /tmp/piper-staging.log 2>&1 &` (kill the :8001 PID first). Tests: run from the worktree, absolute venv path, `POSTGRES_PORT=5433`.
- **Mailbox** = `scripts/mail-send.sh` (push-to-ref, self-reconciles). Inbox clean (3 memos triaged 6/28: 2 PPM-M4 cc + the throttle).
- **Push** non-mail via `git push origin HEAD:main` from the worktree. Commit each increment.
- **#1325** = D3-ideal GitHub-App installation-token (when server supports it). **#1323** = BindingBackedConnector mixin at connector #3.

## ▶ DONE this session-arc (6/27–6/28)
- #1220 real MCP transport (stdio+HTTP) · #1317 github + calendar connector ports (binding-aware honest-degrade) · A→C provisioning ruled · inc.2 OAuth connector (A–E) + local staging go-live + badge fix · #1322 P2/P3 chat reads cutover (issues/PRs/stale-PRs) + P2.1 count fix, all live-verified · #1322 sim-retirement finding + plan + inc.1 · #1327 filed (Q1/Q2) · Q3 recorded.
