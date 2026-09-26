# 2026-09-26 0755 — prog (Coding Agent), MCP Phase C unit 2

**Model**: Sonnet 5. **Dispatched by**: Lead Developer, for MCP Phase C unit 2 (three named
resources). **Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch
`claude/lead-cycle`) — no commits/staging by me; Lead reviews and commits.

## Task

Build unit 2 of the MCP Phase C build plan: three read-only, owner-scoped resources
(`piper://me/profile`, `piper://me/colleague-model`, `piper://me/github/issues`) registered
via `register_resources(mcp)` in `services/mcp/server/app.py`. Honest-empty / connect-required
payloads, never exceptions. Colleague-model referent per CXO's ruling: #1510's verified-inference
store (never #1735).

## Reading done (in full, before writing code)

- `docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md` (Lead's unit
  breakdown)
- `docs/internal/architecture/current/mcp/phase-c-minimal-alpha-slice-2026-09-25.md` (Arch's
  scope: resources-only, escalation trigger on any mutation)
- `mailboxes/lead/read/rule-cxo-to-lead-arch-cc-ppm-exec-pm-mcp-q2-colleague-model-referent-plus-rubric-staleness-correction-2026-09-25.md`
  (CXO's Q2 ruling)
- `docs/internal/architecture/current/mcp/server-README.md` (unit 0/1 shape, unit 2 seam)
- `services/mcp/server/app.py`, `services/mcp/server/identity.py` (seam + `current_user_id()`)
- `services/user_context_service.py` (`UserContext`, `get_user_context`)
- `services/intent_service/verified_inference.py` (#1510 rail — found there is no "list all"
  helper; the actual keys currently stored are `reminder_clear_verb:<verb>` provenance keys via
  `services/intent_service/reminder_clear.py:inference_key()` — not literally "working mode" or
  "standup preferences", which are NOT wired through this store. Read generically: whatever is
  actually confirmed, via the same `_load_preferences` seam `get_verified_inference` itself uses.)
- `services/mcp/consumer/connector.py` (`Connector` protocol, `ConnectRequired`,
  `DegradationResponse`)
- `services/mcp/consumer/github_adapter.py` (`GitHubMCPSpatialAdapter.list_open_issues` — the
  established call convention, confirmed via grep of existing callers in
  `services/intent/intent_service.py`)
- `tests/unit/services/mcp/server/test_identity_unit1.py` (real-MCP-client idiom:
  `streamable_http_client` + `ClientSession` over `httpx.ASGITransport`, seeded
  `mcp_access_tokens` via in-memory SQLite + `StaticPool`)
- `tests/unit/services/mcp/server/test_skeleton_unit0.py` (confirmed the "existing 21 tests"
  count: 9 in unit0 + 12 in unit1 = 21; also confirmed `TestRegisterResourcesSeam`'s
  unit-0 no-op assertion (`list_resources() == []`) necessarily needs amending once unit 2
  actually registers resources — same amendment pattern unit 1 already applied to
  `TestMCPPathFailsClosed`)

## Escalation-trigger check (Arch's condition)

None of the three resources needed a write. Confirmed none.

## Work log

- Read all of the above, in full, before writing any code.
- Implemented `services/mcp/server/resources.py`: three resource functions
  (`_read_profile`, `_read_colleague_model`, `_read_github_issues`) + `register_resources(app)`.
  Every external read wrapped so a failure/absence becomes a structured honest payload, never
  an exception.
- Wired `app.py`'s `register_resources` seam (unchanged name/location, per the README's
  documented seam) to delegate to `resources.py`'s implementation.
- Wrote `tests/unit/services/mcp/server/test_resources_unit2.py` (8 tests) using the real-MCP-
  client idiom from `test_identity_unit1.py`. Had to build the FastMCP instance + `MCPPathGate`
  by hand (rather than `build_asgi_app()`) so each test could enter
  `mcp.session_manager.run()` itself — `httpx.ASGITransport` never sends ASGI lifespan events,
  and a real multi-request `ClientSession` needs the session manager's task group running
  explicitly (same reason `test_identity_unit1.py`'s two-caller-isolation test does this).
- Amended `test_skeleton_unit0.py`'s `TestRegisterResourcesSeam` — its unit-0 assertion
  (`register_resources` registers nothing) necessarily breaks once unit 2 actually registers
  three resources; replaced with an assertion that the seam produces exactly 3, same amendment
  pattern unit 1 already applied there for `TestMCPPathFailsClosed`.
- mypy gate: my two `get_user_context(session_id=None, ...)` calls tripped `[arg-type]`
  (ceiling 364 -> 366) — `session_id` is typed plain `str`, not `Optional[str]`, even though
  other call sites in the codebase pass `None` there (pre-existing, already priced into the
  ceiling). Fixed by passing a synthetic `f"mcp:{user_id}"` session_id instead of `None` — the
  cache-key/logging use of session_id is functionally moot when user_id is provided, so this
  doesn't change behavior. Ceiling restored to 364; gate back to EXIT 0.
- Extended `docs/internal/architecture/current/mcp/server-README.md` with the three URIs, their
  payload shapes, honest-empty/connect-required contracts, and the unit-2 test list.
- Ran and confirmed green: `tests/unit/services/mcp/` (256 passed), `test_architecture_
  enforcement.py` (63 passed, 1 xfailed), `scripts/run-sweep.sh ratchets` (73 passed, 1 xfailed;
  mypy gate all 24 codes at ceiling, EXIT 0), `venv-mypy-gate/.../mypy services/mcp/server`
  (zero errors in services/mcp/server itself — the 853 remaining errors are all pre-existing,
  in `services/intent/intent_service.py`, pulled in transitively), bearer lint over docs/dev
  (OK, no new hits).
- Handed back to Lead via SubagentHandback.

## Escalation-trigger re-check at completion

None of the three resources needed a write at any point during implementation. Confirmed: none.

## Memory & briefing surfaces referenced this session

- **Referenced**: CLAUDE.md dispatch instructions (prog role, session log location/format);
  Lead's build plan + Arch's slice doc + CXO's Q2 ruling (all task-defining, read in full per
  dispatch instructions).
- **Loaded but not referenced**: none beyond the dispatch prompt's own reading list.
- **Wanted but not found**: a "list all verified inferences for a user" helper in
  `verified_inference.py` — doesn't exist; built the read generically off the existing
  `_load_preferences` seam instead of inventing a new shared-module function, to keep the
  diff scoped to `resources.py` as instructed.
