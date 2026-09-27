# Piper Morgan MCP server — what runs where (Phase C, #1462)

Companion to the Lead's build plan (`phase-c-build-plan-2026-09-25.md`) and Arch's slice doc
(`phase-c-minimal-alpha-slice-2026-09-25.md`), same directory. This file documents unit 0 (the
skeleton), the seams unit 1/2 land in, and unit 4's authorization server — it is not a
re-statement of either plan.

## What runs where

- **Alpha web app**: `main.py` → `web.app:app`, Fly app `piper-morgan`, `fly.toml`. Unchanged by
  units 0–2. **Unit 4 adds one thing to it: the OAuth authorization server** (six routes, no
  behavior change to any existing route) — see "Two hosts, one identity" below.
- **MCP server**: `main_mcp.py` → `services/mcp/server/app.py:build_asgi_app()`, Fly app
  `piper-morgan-mcp`, `fly.mcp.toml`. Same Docker image as alpha, same DB and bindings, a
  **separate process/entrypoint** — the Fly config overrides the container CMD
  (`[experimental] cmd`), the Dockerfile itself is untouched, so a bad MCP deploy can't take alpha
  down. It is a **pure resource server**: it verifies tokens, it never issues them.

## Two hosts, one identity (unit 4, #1462 — the OAuth 2.1 authorization server)

The authorization server runs in **alpha**, not in the MCP server, because alpha is the only host
that holds the user's login session (cookie + JWT, `services/auth/auth_middleware.py`). The MCP
server has no session, no login page, and no business growing one. RFC 9728 exists precisely to
let a resource server name a *separate* issuer.

```
                       alpha.pipermorgan.ai                    mcp.pipermorgan.ai
                       (session + consent + AS)                (resources only, RS)
 ┌─────────┐                    │                                       │
 │ ChatGPT │──1─ GET /mcp ──────┼───────────────────────────────────────▶│  401 + WWW-Authenticate:
 │         │                    │                                       │  resource_metadata=…
 │         │──2─ GET /.well-known/oauth-protected-resource ─────────────▶│  { authorization_servers:
 │         │                    │                                       │    [".../mcp/oauth"] }
 │         │──3─ GET /.well-known/oauth-authorization-server/mcp/oauth ─▶│ (on ALPHA)
 │         │                    │  { authorization_endpoint, token_endpoint, registration_endpoint }
 │         │──4─ POST /mcp/oauth/register ─────▶ (RFC 7591 dynamic client registration)
 │         │                    │
 │ browser │──5─ GET /mcp/oauth/authorize ─────▶ AuthMiddleware: session? ──no──▶ 302 /login?next=…
 │         │                    │                        │ yes
 │         │                    │                 consent page ──Approve──▶ code bound to THAT user
 │         │◀───────────────────┼── 302 redirect_uri?code=…&state=…
 │         │──6─ POST /mcp/oauth/token (code + PKCE verifier) ──▶ access token + refresh token
 │         │                    │                                       │
 │         │──7─ GET /mcp  Authorization: Bearer <access token> ───────▶│  reads as that user
 └─────────┘                                                            │
```

**What the tester configures in ChatGPT: the MCP URL, and nothing else.** Steps 2–6 are
discovery and are automatic for any client that speaks OAuth 2.1 + dynamic client registration +
PKCE. There is no bearer field to paste, no client id to create by hand, no secret to deliver
out-of-band. (That was the whole reason unit 4 exists — Q1 in the build plan: ChatGPT's connector
UI offers no bearer header field, so unit 1's operator-minted token could not be presented by it.)

**What PA can tell the tester, verbatim-safe:**

> Add a connector pointing at `https://mcp.pipermorgan.ai/mcp`. You'll be sent to Piper Morgan to
> sign in (if you aren't already) and then asked to approve read-only access to your profile, your
> colleague model, and your GitHub issues. Approve it and you're connected. Nothing you approve can
> change anything — all three are reads — and it only ever sees your own data.

**Unit 1's operator-minted bearer tokens still work.** OAuth adds a second way to *obtain* a
credential, not a second credential format: an OAuth exchange writes an `mcp_access_tokens` row
(label `oauth:<client_id>`, ~1 h expiry) and `MCPTokenVerifier` was not changed at all. One
verifier, one boundary, two ways in. A Claude Desktop/Code tester passing `--header` still works
exactly as documented under "Minting a token" below.

### The identity binding (Arch's unit-4 review condition)

Arch's condition: *the minted token must be bound to the SAME identity that authenticated at the
authorize step, throughout — the failure shape being `exchange_authorization_code` minting a token
for a different (or unresolved) identity than the one that consented.* Four structural facts, all
of which would have to fail:

1. **No identity → no code, ever.** `/mcp/oauth/authorize` is deliberately **not** auth-exempt, so
   alpha's own `AuthMiddleware` requires a session and redirects an unauthenticated browser to
   `/login?next=<the authorize URL>`. The route re-checks independently
   (`_session_user_id`), so the property doesn't depend on middleware registration order.
2. **Consent is a real step.** GET renders a consent page naming the three resource URIs and the
   signed-in account, and writes nothing. Only a POST carrying **Approve plus an HMAC consent
   token bound to (user_id, client_id, code_challenge)** proceeds — which also closes
   consent-CSRF: a forged cross-site approve cannot produce a token for a victim's user id.
3. **The code row is the only carrier of identity** (`mcp_oauth_codes.user_id`, NOT NULL), written
   only from that consenting session via the `consenting_user()` binding. The provider's
   `authorize()` refuses outright if that binding is absent — its contextvar defaults to `None`, so
   forgetting to set it is a refusal, never an anonymous mint.
4. **The exchange mints for the STORED row's `user_id`**, read back after the code is atomically
   claimed — never for the value on the `AuthorizationCode` object the SDK handler passed in. If
   the two disagree, that is a tamper signal and the exchange refuses rather than picking a side
   (`_refuse_code`, a pure function — the one place "may this code be exchanged, and for whom?"
   is decided).

Also enforced: PKCE S256 (mandatory), redirect_uri match, single-use codes (atomic conditional
UPDATE) with **revocation of the first exchange's tokens on any replay** (OAuth 2.1 §4.1.2.5), and
refresh-token rotation. Codes/access tokens/refresh tokens are SHA-256-hashed at rest via the same
`hash_credential()` the verifier uses; the one exception is `mcp_oauth_clients.client_secret`
(encrypted, not hashed — the SDK's `ClientAuthenticator` does the comparison and needs the value;
the model docstring carries the full reasoning).

⚠️ **Three implementation facts a future reader will otherwise re-discover the hard way:**

- **The SDK's OAuth error types are frozen dataclasses.** Raising a `TokenError` inside an
  `async with self._scope()` block fails with `FrozenInstanceError`, because `contextlib`'s
  async-CM exit assigns `exc.__traceback__`. Every refusal in `oauth_provider.py` is therefore
  raised *outside* any session scope. Found by test, not by reading.
- **The transaction split is load-bearing, not stylistic.** `_scope()` rolls back on any exception
  (#1193), so claiming a code, revoking a replay's tokens, and minting must be **separate**
  transactions — one shared scope would mean raising `invalid_grant` for a replay rolls back the
  very revocation the spec requires. A fail-open dressed as a refusal.
- **`MCPPathGate` was blocking RFC 9728 discovery.** FastMCP registers
  `/.well-known/oauth-protected-resource` whenever `resource_server_url` is set, and the 401 on
  the MCP path *points at it* — but unit 1's gate answered it with a 401, so a client had no way
  to find the issuer. Unit 4 adds that one path to `OPEN_PATHS` (it is public by design: it names
  the issuer and the scopes, and carries no user data).

### Files

| Concern | File |
|---|---|
| Provider (protocol impl, minting, refusals) | `services/mcp/server/oauth_provider.py` |
| HTTP surface, session gate, consent page, mounting | `web/routers/mcp_oauth.py` |
| Mount call | `web/app.py` (after the router block, before static mounts) |
| Tables | `mcp_oauth_clients`, `mcp_oauth_codes`, `mcp_oauth_refresh_tokens` — migration `alembic/versions/o1462oaut_mcp_oauth_as.py` |
| Route conventions exception | `docs/internal/architecture/current/web-routes-conventions.md` §"Deliberate exceptions" 4 |
| Tests | `tests/unit/services/mcp/server/test_oauth_as_unit4.py` |

### Config

| Env var | Default | Notes |
|---|---|---|
| `MCP_OAUTH_ISSUER_URL` | `https://alpha.pipermorgan.ai/mcp/oauth` | Read by **both** hosts. Must match on both or discovery breaks. |
| `MCP_RESOURCE_SERVER_URL` | `https://mcp.pipermorgan.ai` | RS identifier (RFC 9728). |
| `MCP_OAUTH_CONSENT_SECRET` | *(falls back to `JWT_SECRET_KEY`)* | HMAC key for the consent token. One fewer secret to provision by default. |

The `/mcp/oauth` path prefix itself is **not** configurable: it is baked into the issuer
identifier a client validates, so an env knob would let the two hosts disagree silently.

⚠️ **The migration must be applied before the AS can serve.** Until
`alembic upgrade head` runs, `/mcp/oauth/register` 500s on `relation "mcp_oauth_clients" does not
exist` — confirmed live on a local dev DB 2026-09-26, which is exactly what it will look like in
prod if the deploy skips the migration.

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

`tests/unit/services/mcp/server/test_oauth_as_unit4.py` — the authorization server, 21 tests.
The full happy path runs across BOTH hosts in one test: dynamic registration → authorize as
session user A → consent Approve → PKCE exchange → the minted token presented to the *resource
server* through a real MCP client reads `piper://me/profile` **as A**, asserted via the same
per-user read spy unit 2's tests use (the `user_id` the resource read actually received). Plus:
no session → no code and zero rows written; three adversarial identity-crossing constructions,
each refused with nothing minted; PKCE mismatch; code replay → refused AND the first token
revoked (re-read from the store, because the bug guarded against is a rollback); refresh
rotation; discovery resolved hop by hop from what the RS advertises; the RS's 401 behavior
unchanged; consent-CSRF and Deny; and the exempt-list shape that `/authorize` depends on.
**No live client was exercised** — nothing here is a claim about ChatGPT's behavior, only about
our endpoints and their metadata.

`tests/unit/services/mcp/server/test_resources_unit2.py` — `resources/list` returns exactly the
three URIs and nothing else; each resource, read through a real MCP client with two synthetic
users' tokens, returns only that caller's data (the read surfaces are mocked per-user and the
`user_id` each stub receives is asserted against the token's own owner); the profile
honest-empty payload on a read failure; the colleague-model honest-empty shape when nothing is
confirmed; the GitHub resource's `connect_required` payload when unbound and its
`count`/`capped_at` payload when bound; the capability set is re-asserted resources-only now
that resources are actually registered.
