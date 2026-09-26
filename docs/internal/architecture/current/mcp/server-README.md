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

## Resources (unit 2, #1462)

`register_resources(app: FastMCP)` in `services/mcp/server/app.py` (the seam unit 0 shipped as a
no-op, called inside `build_mcp_server()` before capability trimming) now delegates to
`services/mcp/server/resources.py:register_resources` — the resource functions and their
`@app.resource(...)` registrations live there so they're independently testable without pulling
in this module's ASGI-wiring concerns. Three resources, all read-only, all owner-scoped to the
caller `current_user_id()` resolves (unit 1) — no fallback, no anonymous read path. Every read
that can fail is caught INSIDE the resource: a failure becomes a structured honest-empty (or
connector-specific honest-degrade) JSON payload, never a bare exception surfaced to the client
and never a fabricated result.

### `piper://me/profile`

The caller's organization, active projects (+ `projects_source`: `database` / `preferences` /
`config`, so the client can see where the list came from), and stated priorities — read via
`services/user_context_service.py:get_user_context`, the same service the chat surface uses.

```json
{"available": true, "organization": "Org A", "projects": ["project-a"],
 "projects_source": "database", "priorities": ["priority-a"]}
```

Read failure (never an exception to the client):

```json
{"available": false, "reason": "profile_read_failed"}
```

### `piper://me/colleague-model`

Per CXO's Q2 ruling (`mailboxes/lead/read/rule-cxo-to-lead-arch-cc-ppm-exec-pm-mcp-q2-colleague-model-referent-plus-rubric-staleness-correction-2026-09-25.md`):
every entry in the #1510 verified-inference store
(`services/intent_service/verified_inference.py`) for this user that has actually gone through
the read-back-and-confirm loop — never a raw, unconfirmed inference — plus the user's own
hand-authored PIPER.md priorities. Deliberately **not** #1735's personalization/learning-loop
stores (that issue's own body: three of its four stores are disconnected or a silent no-op).
There is no "list all confirmed entries" helper in `verified_inference.py`, so this resource
reads the same `collaboration_gate._load_preferences` seam that module's own
`get_verified_inference` reads internally, rather than inventing a new shared-module function
for a single consumer.

```json
{"verified": [{"key": "reminder_clear_verb:done", "value": "complete",
               "verified_at": "2026-09-01T00:00:00+00:00"}],
 "priorities": ["priority-a"]}
```

Nothing confirmed yet (the honest-empty shape, not a failure):

```json
{"verified": [], "priorities": [], "note": "nothing confirmed yet"}
```

### `piper://me/github/issues`

The caller's own open GitHub issues (`assignee:@me`), read via
`services/mcp/consumer/github_adapter.py:GitHubMCPSpatialAdapter.list_open_issues` — the user's
bound GitHub connector, resolved via a logical-key binding (ADR-070 Amendment A). Page capped at
`GITHUB_ISSUES_PAGE_CAP` (50, mirroring the chat surface's own default); `capped_at` is always
stated so a client can tell a short list from a truncated one (#1762 render-whole discipline).

```json
{"available": true, "issues": [{"number": 1, "title": "A's issue"}], "count": 1, "capped_at": 50}
```

Unbound — the connector's own honest `ConnectRequired` degradation passed through as a
structured payload, never an exception and never an empty list pretending to be "no issues":

```json
{"available": false, "connector": "github", "reason": "connect_required",
 "message": "Connect GitHub to continue."}
```

Any other connector degradation (stale token, unreachable, misconfigured, …) uses the same
shape with `reason` set to that `DegradationReason`'s value and `message` to its
`user_message`.

## Tests

`tests/unit/services/mcp/server/test_skeleton_unit0.py` — `/health` + `/` stay open, the MCP path
fails closed unconditionally (GET and POST), the real `create_initialization_options()` capability
object has `resources` and not `tools`/`prompts`; `register_resources()` is now confirmed to
register unit 2's three resources (amended from unit 0's original "registers nothing yet").

`tests/unit/services/mcp/server/test_resources_unit2.py` — `resources/list` returns exactly the
three URIs and nothing else; each resource, read through a real MCP client with two synthetic
users' tokens, returns only that caller's data (the read surfaces are mocked per-user and the
`user_id` each stub receives is asserted against the token's own owner); the profile
honest-empty payload on a read failure; the colleague-model honest-empty shape when nothing is
confirmed; the GitHub resource's `connect_required` payload when unbound and its
`count`/`capped_at` payload when bound; the capability set is re-asserted resources-only now
that resources are actually registered.
