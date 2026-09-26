# 2026-09-26 06:50 — prog (Coding Agent) — MCP Phase C unit 0

**Model**: Sonnet 5
**Dispatched by**: Lead Developer
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`) — NOT committing; Lead owns the commit.
**Task**: Build unit 0 of MCP Phase C — skeleton FastMCP server, resources-only capability set, fail-closed 401 gate on all MCP traffic (identity resolver is unit 1, not built here), `main_mcp.py` entrypoint, `fly.mcp.toml`, tests, docs.

## Context read
- `docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md` (Lead's plan)
- `docs/internal/architecture/current/mcp/phase-c-minimal-alpha-slice-2026-09-25.md` (Arch's scope: resources only, zero tools, fail-closed identity)
- ADR-070 §D3, `main.py`, `Dockerfile`, `fly.toml`, installed `mcp` SDK (`fastmcp/server.py`, `streamable_http_manager.py`)
- `services/mcp/` — confirmed `consumer/` + `protocol/` exist, no `server/` (from scratch)

## Work log

Built unit 0 exactly per the Lead's plan and Arch's slice doc, deployable dark:

- `services/mcp/server/__init__.py`, `services/mcp/server/app.py` — `FastMCP("piper-morgan")` over
  streamable HTTP. Key design decisions (see docstrings for full rationale):
  1. FastMCP unconditionally wires tools/prompts handlers even with none registered, so
     `_restrict_to_resources_only()` pops the four handler entries (`ListToolsRequest`,
     `CallToolRequest`, `ListPromptsRequest`, `GetPromptRequest`) from
     `mcp._mcp_server.request_handlers` right after construction — the only way to make the real
     `initialize` capability set actually be resources-only.
  2. Fail-closed gate (`FailClosedMCPGate`) is a raw ASGI wrapper around the finished
     `streamable_http_app()` output (lifespan intact), not a FastMCP `TokenVerifier` — there's no
     verifier to plug in until unit 1. Rejects every request to the MCP path unconditionally
     (bearer present or not) with 401 + `WWW-Authenticate: Bearer` +
     `{"error":"identity_required"}`.
  3. `/health` and `/` registered via FastMCP's `custom_route` (SDK's own no-auth escape hatch),
     living inside the same Starlette app/lifespan as the MCP endpoint — avoids the
     sub-app-mount lifespan-propagation trap entirely.
  4. `/health` reuses `services.api.health.deploy_identity.deploy_identity()` (same helper alpha's
     `/health`/`/api/v1/version` use) rather than re-parsing pyproject/VERSION a second time.
  5. `register_resources(app)` — documented no-op seam for unit 2.
- `main_mcp.py` (repo root, ~30 lines) — uvicorn entrypoint, `$PORT` (default 8080), reuses
  `services.infrastructure.logging.config`'s structlog setup via import side effect (same as every
  other Piper entrypoint) rather than reconfiguring.
- `fly.mcp.toml` — app `piper-morgan-mcp`, same Dockerfile, `[experimental] cmd` override (mirrors
  `deploy/fly/github-mcp.fly.toml`'s idiom) rather than editing the Dockerfile CMD; internal port
  8080; `/health` HTTP check; no secrets; `min_machines_running = 0` (dark, no live tester yet,
  unlike alpha's pinned-warm `fly.toml`).
- `tests/unit/services/mcp/server/test_skeleton_unit0.py` (8 tests) — `/health`/`/` open + 4
  fields; MCP path fails closed on GET and POST `initialize` (no bearer); the REAL
  `create_initialization_options()` capability object has `resources` and not `tools`/`prompts`
  (plus a handler-table check as belt-and-suspenders); `register_resources()` confirmed no-op via
  `await server.list_resources() == []`.
- `docs/internal/architecture/current/mcp/server-README.md` — what runs where, local run, deploy
  command, fail-closed default, unit 1/2 seams.

### Gates run
- `ruff format` + `ruff check --fix` on all 5 touched files: clean, 0 changes needed.
- `tests/unit/services/mcp/server/test_skeleton_unit0.py`: **8 passed**.
- `tests/unit/services/mcp/ -q` (consumer + server, untouched consumer/protocol dirs not modified):
  **235 passed**, 4 pre-existing warnings (unrelated `pytest.mark.asyncio` on sync tests in
  `test_github_write_not_found_1858.py`, not touched this session).
- `tests/test_architecture_enforcement.py`: **63 passed, 1 xfailed**.
- `scripts/run-sweep.sh ratchets` (canonical invocation — uses `venv-mypy-gate/bin/python`, the
  CI-faithful pinned venv; `venv/bin/python` over-reports per the script's own header comment):
  `73 passed, 1 xfailed` on the ratchet pytest files, then
  `mypy gate: all 24 ratcheted codes at ceiling (total=1121; ...)` — **PASS**, exit 0.
- Isolated `venv-mypy-gate/bin/python -m mypy --config-file mypy-gate.ini services/mcp/server
  main_mcp.py`: 5 errors, all attributed to `services/infrastructure/logging/url_redaction.py`,
  `services/infrastructure/logging/config.py`, `services/mcp/client.py` — three pre-existing,
  git-clean (unmodified) files reached only transitively via imports. **Zero errors in any new
  file.** (First attempt used `venv/bin/python`, the over-reporting dev venv per the script's own
  warning — re-ran with `venv-mypy-gate/bin/python` for the accurate number.)

### Discovered work
None filed — the pre-existing mypy ratchet drift visible under the dev venv is explained by the
repo's own documented dev-vs-gate-venv discrepancy (`scripts/run-sweep.sh` comment, `#1436`), not a
new finding; the canonical gate invocation passes clean.

## Memory & briefing surfaces referenced this session

**Referenced**:
- `docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md` — unit 0 scope, exact
  deliverable list.
- `docs/internal/architecture/current/mcp/phase-c-minimal-alpha-slice-2026-09-25.md` — fail-closed
  identity standard, resources-only/zero-tools condition.
- `services/api/health/deploy_identity.py` — reused directly for `/health`.
- `deploy/fly/github-mcp.fly.toml` — mirrored for the `fly.mcp.toml` CMD-override idiom.
- `services/infrastructure/logging/config.py` — reused (import side effect) for structlog setup.

**Loaded but not referenced**: ADR-070 §D3 (read for context; no direct decision needed at unit 0
since auth/OAuth transport is Q1/unit 4's concern, not unit 0's).

**Wanted but not found**: nothing — the two Phase C docs were sufficiently complete for unit 0.

## Sign-off
Not applicable — prog subagent, no commit/push authority per dispatch instructions. Reporting back
to Lead via SubagentHandback for Lead to review/commit.
