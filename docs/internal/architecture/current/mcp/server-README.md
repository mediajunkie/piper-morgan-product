# Piper Morgan MCP server — what runs where (Phase C, #1462)

Companion to the Lead's build plan (`phase-c-build-plan-2026-09-25.md`) and Arch's slice doc
(`phase-c-minimal-alpha-slice-2026-09-25.md`), same directory. This file documents unit 0 (the
skeleton) and the seams unit 1/2 land in — it is not a re-statement of either plan.

## What runs where

- **Alpha web app**: `main.py` → `web.app:app`, Fly app `piper-morgan`, `fly.toml`. Unchanged by
  this work.
- **MCP server**: `main_mcp.py` → `services/mcp/server/app.py:build_asgi_app()`, Fly app
  `piper-morgan-mcp`, `fly.mcp.toml`. Same Docker image as alpha, same DB and bindings, a
  **separate process/entrypoint** — the Fly config overrides the container CMD
  (`[experimental] cmd`), the Dockerfile itself is untouched, so a bad MCP deploy can't take alpha
  down.

## Run locally

```bash
PORT=8080 venv/bin/python main_mcp.py
# GET http://localhost:8080/health   -> {"status":"healthy","service":"piper-morgan-mcp",...}
# GET http://localhost:8080/         -> plain-text pointer
# any request to /mcp                -> 401 {"error":"identity_required"} (see below)
```

## Deploy

```bash
fly deploy -c fly.mcp.toml -a piper-morgan-mcp --remote-only \
  --build-arg PIPER_GIT_SHA=$(git rev-parse HEAD)
```

DNS (`mcp.pipermorgan.ai`) and the TLS cert are already issued (Phase B, Pard, 2026-09-24). Fly
serves no TLS for a machine-less app, so the endpoint reads as dark (`curl` → connection refused/000)
until the first deploy of `fly.mcp.toml` — expected, not broken.

## Fail-closed identity (unit 1, #1462)

Unit 0 shipped with **no identity resolver** — every MCP request was refused unconditionally.
Unit 1 replaces that with a real bearer-token verifier
(`services/mcp/server/identity.py:MCPTokenVerifier`), wired into FastMCP's own auth hook
(`FastMCP(auth=AuthSettings(...), token_verifier=MCPTokenVerifier())` in
`build_mcp_server()`). The fail-closed property still holds, by a different mechanism:

- **No anonymous read path, ever.** `MCPTokenVerifier.verify_token()` returns `None` for a
  missing hash, a revoked token, and an expired token — identically, so a caller can't learn
  *why* a token failed. FastMCP's own `RequireAuthMiddleware` turns any `None` into a `401` before
  the request ever reaches a resource handler. There is no branch anywhere that resolves a
  missing/invalid/expired token to a real user.
- **`MCPPathGate`** (`services/mcp/server/app.py`, née `FailClosedMCPGate` in unit 0) still denies
  by default at the raw ASGI layer — but only for paths nobody has explicitly gated (a typo, a
  future route someone forgets to protect). The MCP path itself is now let through to the inner
  app, because that inner app enforces its own real identity check via `RequireAuthMiddleware`;
  "let through to a fail-closed check" is not the same thing as "served anonymously."
- **Caller isolation.** `client_id` on the resolved `AccessToken` comes only from the DB row the
  token's own SHA-256 hash matched. `services/mcp/server/identity.py:current_user_id()` (unit 2's
  seam for reading the verified identity inside a resource handler) reads it back out of the
  SDK's own request-scoped contextvar (`mcp.server.auth.middleware.auth_context`) — never a
  header, a query parameter, or a default — so caller A's token can never produce caller B's
  identity. Tested with two synthetic users even though only one real tester exists
  (`tests/unit/services/mcp/server/test_identity_unit1.py::TestTwoCallerIsolation`).

### The `mcp_access_tokens` table

One row per minted bearer credential: `user_id` (FK `users.id`, NOT NULL — there is no row that
resolves to an anonymous owner), `token_hash` (SHA-256 hex digest, UNIQUE — the raw token is
**never** stored, logged, or written to an exception, anywhere), `label`, `created_at`,
`expires_at` (nullable — NULL means never expires), `revoked_at` (nullable — set once, never
unset), `last_used_at` (updated by the verifier on every successful resolution). Migration:
`alembic/versions/n1462mcpt_mcp_access_tokens.py`.

### Minting a token

`scripts/mint_mcp_token.py` (+ `scripts/mint_mcp_token.sh`, the `fly ssh console` wrapper mirroring
`scripts/mint_prod_invite.sh`'s idiom exactly — same fixed-payload-in-git rationale, same
prod-vs-dev DB-resolution guard). Generates a 32-byte URL-safe random token (`mcp_` prefix),
stores only its hash, and prints the raw value to stdout **exactly once** with a warning that it
will not be shown again. Dry-run by default; `--apply` to actually insert.

```bash
scripts/mint_mcp_token.sh --user-email tester@example.com --label "alpha tester — claude desktop" --apply
```

Delivery is out-of-band, exactly like an invite token (#1344, PM ruling 2026-07-04): **never** a
mailbox memo, a GH comment, or any git-tracked file — in-conversation or the gitignored roster
only. Revoke by setting `revoked_at` on the row (no dedicated script yet).

### Tests that pin the fail-closed guarantee

`tests/unit/services/mcp/server/test_identity_unit1.py` — an unresolvable identity (monkeypatched
verifier) gets 401 on `initialize`; a real valid token gets 200; a revoked token gets 401; an
expired token gets 401; `MCPTokenVerifier` unit-level tests pin each refusal condition directly;
`TestTwoCallerIsolation` proves caller A's token can never produce caller B's identity, and a
garbage token reads nothing — via a real MCP client (`mcp.client.streamable_http` +
`ClientSession`) round-tripping `initialize` + `resources/read` over an in-process ASGI transport,
against a resource stub that calls `current_user_id()`.

## Capability set: resources only, zero tools, zero prompts

FastMCP's constructor unconditionally wires `list_tools`/`call_tool`/`list_prompts`/`get_prompt`
handlers onto its low-level `Server`, whether or not anything is registered under them — so an
unmodified `FastMCP()` instance always advertises `tools` and `prompts` capabilities in the
`initialize` handshake even with zero of each. `_restrict_to_resources_only()` in
`services/mcp/server/app.py` pops those four handler entries immediately after construction, so
the real `initialize` response advertises `resources` and nothing else. See that function's
docstring before changing anything here.

## The seams for unit 1 and unit 2

- **Unit 1 (identity)**: replace `FailClosedMCPGate` (or extend its `__call__`) with real bearer
  resolution. `build_asgi_app()`'s shape doesn't need to change.
- **Unit 2 (three named resources)**: `register_resources(app: FastMCP)` in
  `services/mcp/server/app.py` is a documented no-op seam — add `@app.resource(...)`
  registrations there. It's already called (before capability trimming, which doesn't care about
  resource count) inside `build_mcp_server()`, so unit 2 doesn't restructure this file.

## Tests

`tests/unit/services/mcp/server/test_skeleton_unit0.py` — `/health` + `/` stay open, the MCP path
fails closed unconditionally (GET and POST), the real `create_initialization_options()` capability
object has `resources` and not `tools`/`prompts`, and `register_resources()` is confirmed to
register nothing yet.
