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

## Fail-closed by default (unit 0's whole point)

Unit 0 ships with **no identity resolver**. Every request to the MCP path (`/mcp`, FastMCP's
default `streamable_http_path`) is refused unconditionally with `401` +
`WWW-Authenticate: Bearer` + `{"error": "identity_required"}`, regardless of whether a bearer token
is present, absent, or well-formed — there is no code path that serves an MCP response
anonymously. `/health` and `/` are the only two routes that answer without a gate check.

The gate (`FailClosedMCPGate` in `services/mcp/server/app.py`) is a thin ASGI wrapper placed
*around* the fully-built MCP ASGI app (FastMCP's `streamable_http_app()`, lifespan and all) — not
a FastMCP `TokenVerifier`/`AuthSettings` hook, because there is no real verifier to plug in yet.
Unit 1 replaces this one class; nothing else in `app.py` needs to change shape.

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
