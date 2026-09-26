# Session log — prog (Coding Agent), MCP Phase C unit 1

**Role**: Coding Agent (prog), dispatched by Lead Developer
**Model**: Sonnet 5 (claude-sonnet-5)
**Date**: 2026-09-26
**Task**: MCP Phase C unit 1 — fail-closed caller identity for the MCP server (#1462)
**Worktree**: `/Users/xian/Development/piper-morgan-worktrees/lead` (branch `claude/lead-cycle`)
**Constraint**: do NOT commit/stage/touch the git index — Lead owns the commit. No deploys, no Fly, no network, no LLM. Usage throttle in effect: read what's needed, no sweeps.

## Reading (before writing any code)

- `docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md` — unit 1 scope
- `docs/internal/architecture/current/mcp/phase-c-minimal-alpha-slice-2026-09-25.md` — Arch's condition 1 (no identity, no read; never default to anonymous)
- `docs/internal/architecture/current/mcp/server-README.md` — unit 0 seams
- `services/mcp/server/app.py` — unit 0: `FailClosedMCPGate`, `register_resources` seam
- `venv/lib/python3.11/site-packages/mcp/server/auth/provider.py` — `TokenVerifier`, `AccessToken`
- `venv/lib/python3.11/site-packages/mcp/server/auth/settings.py` — `AuthSettings`
- `venv/lib/python3.11/site-packages/mcp/server/fastmcp/server.py` — how `FastMCP(auth=, token_verifier=)` wires `RequireAuthMiddleware`/`BearerAuthBackend`/`AuthContextMiddleware`
- `venv/lib/python3.11/site-packages/mcp/server/auth/middleware/bearer_auth.py` + `auth_context.py` — the request-scoped contextvar (`get_access_token()`)
- `services/database/models.py` — `User`, `UserAPIKey`, `InviteToken`, `PasswordResetToken`, `SlackIdentity`, `CrossDialectUUID`
- `services/security/field_encryption.py` — confirmed NOT applicable (token_hash is a one-way SHA-256 digest, not a reversible secret; precedent is `key_leak_detector.py`'s `hashlib.sha256(...).hexdigest()`)
- `scripts/mint_prod_invite.sh` + `scripts/mint_invite_tokens.py` — operator-mint precedent (`_engine()` idiom, prod-vs-dev DB resolution, dry-run default)
- `services/database/session_factory.py` — `AsyncSessionFactory.session_scope()` (commit-on-clean-exit contract, #1193)
- `alembic/versions/m1797drop_dead_persistence_twin_tables.py` (current head) + `l1466slack_...py` (shape precedent)
- `tests/unit/services/mcp/server/test_skeleton_unit0.py` — unit 0 test idiom
- `tests/unit/services/database/test_document_model_1238.py` — in-memory SQLite test fixture pattern
- `scripts/mailbox_bearer_lint.py` — confirmed placeholder-token rules for docs/tests

## Plan

1. `MCPAccessToken` model (`services/database/models.py`) + alembic migration `n1462mcpt` (down_revision `m1797drop`, the verified head).
2. `services/mcp/server/identity.py` — `MCPTokenVerifier(TokenVerifier)`, `current_user_id()`.
3. `scripts/mint_mcp_token.py` + `scripts/mint_mcp_token.sh`.
4. Wire `services/mcp/server/app.py`: `FastMCP(auth=AuthSettings(...), token_verifier=MCPTokenVerifier())`; replace `FailClosedMCPGate`'s unconditional-401 MCP-path behavior with "MCP path passes through to the SDK's bearer auth; unknown paths still denied by default."
5. Tests: `tests/unit/services/mcp/server/test_identity_unit1.py` (SQLite fixture); update `test_skeleton_unit0.py` where behavior changed.
6. Docs: `server-README.md` + `canonical-ops-recipes.md` mint one-liner.
7. Gates: ruff format/check, pytest (mcp unit dir + architecture enforcement), sweep ratchets, mypy-gate.

## Work log

### Built (unit 1: fail-closed caller identity)

1. **Model**: `MCPAccessToken` (`services/database/models.py`) — `id`, `user_id` (FK `users.id`,
   NOT NULL, CASCADE, indexed), `token_hash` (SHA-256 hex, UNIQUE, raw token never stored),
   `label`, `created_at`, `expires_at`/`revoked_at`/`last_used_at` (nullable). Used
   `CrossDialectUUID()` (not `postgresql.UUID`) so the model works under the in-memory-SQLite
   unit-test pattern.
2. **Migration**: `alembic/versions/n1462mcpt_mcp_access_tokens.py`, down_revision `m1797drop`
   (verified current head via `alembic/versions/*.py` revision/down_revision scan). Additive,
   reversible. Loads and parses cleanly (verified via direct module exec — no live DB touched
   per the no-network/no-deploy constraint).
3. **Verifier**: `services/mcp/server/identity.py` — `MCPTokenVerifier(TokenVerifier)`:
   hash → lookup → refuse (None) on not-found/revoked/expired, identically, one
   `mcp_identity_refused` log line with masked token + reason enum, no user id ever logged on
   refusal. `current_user_id()` reads the SDK's own request-scoped `AccessToken` contextvar
   (`mcp.server.auth.middleware.auth_context.get_access_token()`) — raises if absent, never a
   default. Found and fixed a real bug while writing tests: SQLite drops tzinfo on
   `DateTime(timezone=True)` round-trip, so the expired-token comparison raised
   `TypeError: can't compare offset-naive and offset-aware datetimes` under the SQLite test
   fixture (Postgres round-trips tzinfo fine) — added `_as_aware_utc()` to normalize before
   comparing.
4. **Wired into `services/mcp/server/app.py`**: `build_mcp_server()` now passes
   `auth=AuthSettings(issuer_url=..., resource_server_url=..., required_scopes=["resources:read"])`
   + `token_verifier=MCPTokenVerifier()` to `FastMCP(...)`. No `auth_server_provider` — no live
   OAuth AS, no `/authorize`/`/token` routes; issuer/resource URLs are RFC 9728 metadata only
   (documented in `_auth_settings()`'s docstring), overridable via `MCP_OAUTH_ISSUER_URL` /
   `MCP_RESOURCE_SERVER_URL`. `FailClosedMCPGate` renamed `MCPPathGate`: still deny-by-default
   for any path nobody has gated, but the MCP path now passes through to the SDK's own
   `RequireAuthMiddleware` instead of being denied unconditionally.
5. **Mint script**: `scripts/mint_mcp_token.py` (+ `scripts/mint_mcp_token.sh`, the `fly ssh
   console` wrapper mirroring `mint_prod_invite.sh`'s exact idiom — fixed payload in git, same
   prod-vs-dev DB-resolution guard duplicated from `mint_invite_tokens.py`, never imported, so no
   import-time coupling). `mcp_` + `secrets.token_urlsafe(32)`; stores only the SHA-256 hash;
   prints the raw token ONCE with a masked-reference line; dry-run by default.
6. **Tests**: `tests/unit/services/mcp/server/test_identity_unit1.py` (20 assertions across the
   401/200/revoked/expired ASGI-layer matrix, direct `MCPTokenVerifier` unit tests, and
   two-caller isolation via a REAL MCP client — `mcp.client.streamable_http.streamable_http_client`
   + `ClientSession` — round-tripping `initialize`/`resources/read` over an in-process ASGI
   transport against a resource stub that calls `current_user_id()`). Updated
   `test_skeleton_unit0.py`'s two MCP-path-401 tests to assert the invariant (401 + a
   `WWW-Authenticate` challenge) rather than unit 0's now-superseded exact body shape.
7. **Docs**: extended `server-README.md` (identity model, mint procedure, table shape, test
   coverage) and added a mint one-liner recipe to `canonical-ops-recipes.md`.

### Debugging detours (both resolved, both worth keeping as notes)

- **False "hang"**: several early test iterations appeared to hang for 30s+. Root cause (found via
  `faulthandler.dump_traceback_later` thread dumps): Starlette `TestClient`'s default
  `base_url="http://testserver"` fails FastMCP's auto-enabled DNS-rebinding Host check (`421`,
  not a hang) for any request that gets PAST `RequireAuthMiddleware` (unauthenticated requests
  never reach that check, so the 401 tests were unaffected) — and because the assertion failure
  happened before `engine.dispose()`, aiosqlite's non-daemon worker thread kept the whole process
  alive. Fixed by (a) using `base_url="http://localhost:8080"` — matches FastMCP's default
  `allowed_hosts=["127.0.0.1:*","localhost:*","[::1]:*"]` — and (b) moving DB engine
  creation/disposal into a `pytest_asyncio` fixture so teardown runs regardless of test outcome.
- **Cross-test contamination**: running the two `TestTwoCallerIsolation` tests together with the
  earlier ASGI-layer tests raised `RuntimeError: ... bound to a different event loop` from
  `sse_starlette.sse.AppStatus.should_exit_event` — a process-global singleton bound to whichever
  asyncio loop first touched it, colliding with pytest-asyncio's per-test event loop. Fixed with
  an autouse fixture resetting `AppStatus.should_exit`/`should_exit_event` before each test in
  the file.
- Also switched from the now-`@deprecated` `streamablehttp_client` to `streamable_http_client`
  (the SDK's own replacement) once the deprecation warning surfaced, and fixed a genuine
  `unscoped_repo_reads` ratchet regression (36→37): `MCPAccessToken` is now an ADR-079
  D3-owner-bearing model (has `user_id`), and the identity-resolution lookup in
  `verify_token()` legitimately has no owner predicate (the owner is the query's OUTPUT, not a
  known input) — added a `# global-ok:` annotation per D4/D6, ceiling back to 36.

### Gate results (all commands, quoted verbatim)

- `venv/bin/python -m pytest tests/unit/services/mcp/server/ -q` → **20 passed** (both new
  unit-1 files together, no cross-test interference).
- `venv/bin/python -m pytest tests/unit/services/mcp/ -q` → **247 passed, 4 warnings** (pre-existing
  warnings, unrelated to this change).
- `venv/bin/python -m pytest tests/test_architecture_enforcement.py -q` → **63 passed, 1 xfailed**.
- `scripts/run-sweep.sh ratchets` → **73 passed, 1 xfailed**; mypy per-code gate: *"all 24
  ratcheted codes at ceiling (total=1121 ...)"* — unchanged from before this work (confirmed via
  the `unscoped_repo_reads` regression being caught and fixed back to ceiling 36 first).
- `venv-mypy-gate/bin/python -m mypy --config-file mypy-gate.ini services/mcp/server main_mcp.py
  scripts/mint_mcp_token.py` → 359 errors reported, **zero attributable to the 4 new/changed
  files** (all in pre-existing transitively-imported files: `repositories.py`,
  `audit_logger.py`, `config_repository.py`, etc. — grepped explicitly for lines starting with
  `services/mcp/server/app.py:`, `services/mcp/server/identity.py:`, `main_mcp.py:`,
  `scripts/mint_mcp_token.py:` and found none).
- `venv/bin/python -m ruff format <changed files>` → 3 reformatted, then `ruff check --fix` →
  clean; final `ruff check <changed files>` → **All checks passed!**
- `venv/bin/python scripts/mailbox_bearer_lint.py --roots mailboxes docs dev --baseline
  .mailbox-bearer-lint-baseline.txt` (the CI invocation, per `.github/workflows/lint.yml`) →
  **OK — no new bearer credential** (46 baselined historical hits, unrelated to this work; the
  bare no-baseline invocation surfaces the full historical backlog and is not the gate CI runs).

### Discovered work / follow-ups (not filed as GH issues — reporting to Lead per dispatch scope)

- No token-revocation script exists yet (documented as "direct SQL via fly ssh console" in the
  ops recipe) — a `revoke_mcp_token.sh` would be a natural, small follow-up, not built here since
  out of unit 1's stated scope.
- Unit 2 (three named resources) is the next build-plan unit; `register_resources()` remains the
  unit-2 seam, unit 1 doesn't touch it.

## Verified how

**Method**: every gate command above was actually run this session and its output quoted
verbatim, not recalled from an earlier check. **Layer**: unit-level SQLite-backed tests +
real-ASGI-layer tests (Starlette `TestClient` / httpx `ASGITransport`, the same protocol surface
uvicorn serves) exercising FastMCP's actual `RequireAuthMiddleware`/`BearerAuthBackend` wiring —
not a mocked verifier standing in for the SDK's auth path; the two-caller isolation proof uses a
real MCP client library round-trip, not a direct function call into the resource. **Denominator**:
covers unit 1 (identity boundary) in full, per the build plan's own scope — does not cover unit 2
(resources), unit 3 (deploy), or unit 4 (OAuth AS), none of which are built here. No live Fly
deploy, no real Postgres, no LLM calls were made (per dispatch constraints); the migration was
verified to load/parse/chain correctly but was not applied against a live database.

## Memory & briefing surfaces referenced this session

**Referenced**: the two MCP Phase C planning docs (build plan + slice doc) — scoped unit 1
precisely; `server-README.md` — gave the exact seam (`FailClosedMCPGate`, `register_resources`)
to extend; `services/database/models.py`'s existing token-family models (`InviteToken`,
`PasswordResetToken`, `SlackIdentity`) — gave the natural-key-vs-surrogate-key shape decision and
the `CrossDialectUUID` SQLite-compat convention; `scripts/mint_prod_invite.sh` +
`mint_invite_tokens.py` — gave the operator-mint `_engine()`/dry-run idiom verbatim;
`services/database/session_factory.py`'s `session_scope()` docstring — gave the commit-on-clean-
exit contract (#1193) the verifier and test fixture both had to match; ADR-079's
`check_unscoped_reads.py` docstring — gave the exact `# global-ok:` annotation mechanism once the
ratchet caught a real regression.

**Loaded but not referenced**: `services/security/field_encryption.py` (confirmed NOT applicable —
token_hash is a one-way digest, not a reversible secret — but didn't otherwise shape the work).

**Wanted but not found**: no existing precedent in the repo for testing a real MCP
bearer-auth-protected resource end-to-end (unit 0's tests only exercised the pre-auth 401 paths);
had to work out the `streamable_http_client` + `ClientSession` + `session_manager.run()` +
DNS-rebinding-host + sse_starlette-singleton mechanics from the SDK source directly. A short
"testing an authenticated MCP resource" recipe would have saved real time if it had existed —
flagging as a gap for whoever builds unit 2's resource tests next.
