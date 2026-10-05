"""Piper Morgan MCP server — per-caller-identity rate limiting (#1458 AC: rate limiting).

#1458 (Arch's rescoped ruling, 2026-10-05 — see
``mailboxes/pa/inbox/rule-arch-to-pa-cc-exec-1458-gates-listing-rescoped-to-mcp-reachable-
code-three-acs-already-met-2026-10-05.md``) required rate limiting on ``/mcp`` keyed per
token identity, not per process or per IP-only, before the server is listed for a second
tenant. No such limiter existed anywhere under ``services/mcp/server/`` (confirmed: no
``rate.?limit``/``throttle``/``429`` hit in that tree before this file; see #1458 PR
report for the exact grep). This module adds the minimal mechanism, keyed on the SAME
verified identity ``identity.py`` already resolves — never on IP, never on a shared
"anonymous" bucket.

Design, and why it is placed where it is
-----------------------------------------
The obvious place to check a per-caller limit is *after* identity is resolved — i.e.
inside a resource/tool handler, via ``current_user_id()``. That placement was rejected:
an exception raised inside a FastMCP resource/tool handler is caught by the SDK's own
dispatch (``mcp/server/lowlevel/server.py``) and turned into a JSON-RPC
``isError``/``ErrorData`` response — still **HTTP 200**, not the HTTP 429 this AC asks
for. Verified by reading that dispatch path directly, not assumed.

So this is raw ASGI middleware, sitting on the ``/mcp`` path only, INSIDE
:class:`~services.mcp.server.app.MCPPathGate` (which still owns deny-by-default for
every other path) but OUTSIDE FastMCP's own auth stack (``AuthenticationMiddleware`` +
``RequireAuthMiddleware``, wired by ``mcp.streamable_http_app()`` itself — see
``identity.py``'s module docstring). That auth stack has no public seam to insert a
middleware BETWEEN "identity resolved" and "route dispatched" (Starlette's own
``add_middleware`` always inserts OUTERMOST, i.e. BEFORE auth, not after — verified by
reading ``streamable_http_app()``'s construction), so this module resolves identity a
SECOND time, independently, using the SAME :class:`~services.mcp.server.identity.
MCPTokenVerifier` the real auth path uses:

- No/garbled/unresolvable bearer → this middleware does nothing and passes the request
  through unchanged. It never originates a 401 and never changes today's refusal
  semantics — that stays entirely FastMCP's ``RequireAuthMiddleware``'s job (identity.py).
  This also means a flood of garbage tokens cannot consume a shared "unauthenticated"
  rate-limit bucket — there is no such bucket; an unresolvable token is simply not rate
  limited by identity (it is still refused by auth, same as before this change).
- A bearer that resolves → keyed by ``access_token.client_id`` (the verified user_id,
  identical to what ``current_user_id()`` would return for this same request). Over the
  limit → this middleware answers 429 itself, with ``Retry-After``, and never calls into
  FastMCP's auth/routing at all for that request.

The cost of the second verification is one extra indexed DB lookup (by ``token_hash``,
the same query ``MCPTokenVerifier._verify_token`` already runs) plus a redundant
``last_used_at`` touch, on every MCP request. Accepted: correctness (a real HTTP 429,
keyed on the real identity) over micro-optimizing away a cheap indexed read.

Backing store: Redis via :class:`~services.cache.redis_factory.RedisFactory` — reusing
the fixed-window INCR+EXPIRE shape ``web/middleware/usage_cap_middleware.py`` already
uses for ADR-076 (same pattern, not re-derived), because it is the repo's existing
shared, cross-process-safe counter (Arch's instruction: prefer an existing shared
limiter utility over a new in-memory one). This matters concretely here: `fly.mcp.toml`
sets ``min_machines_running = 1`` with ``auto_start_machines = true`` — i.e. the MCP app
can and does run a second ("burst") machine under load, not just the one always-on
machine. An in-process counter is per-machine and a caller split across two machines by
Fly's load balancer would get roughly double the intended limit; Redis is shared across
every machine this app runs, so that gap does not exist here.

Fail-closed vs. fail-open on the rate limiter's OWN backend (deliberate, asymmetric
with identity.py): identity resolution is fail-closed by contract (no identity, no
read — see identity.py). This limiter is fail-OPEN specifically on a Redis error: a
request whose rate-limit check itself cannot be completed is let through unmetered
(logged at ERROR), never refused. Rationale, stated plainly: whether ``REDIS_URL`` is
provisioned as a secret on the ``piper-morgan-mcp`` Fly app specifically (a SEPARATE app
from the alpha web app that DOES have it — see ``fly.toml`` vs. ``fly.mcp.toml``) is NOT
verifiable from this repo and was not asserted as fact anywhere in this change. Shipping
fail-closed here means a missing/misconfigured Redis secret on THIS app would 503 every
MCP request the moment this code deploys — turning a live, already-functioning,
read-only informational endpoint into a hard outage over an infra gap unrelated to
identity correctness. Fail-open means the worst case of that same gap is "temporarily
unmetered," i.e. no worse than before this file existed. This is a considered reversal
of ADR-076's fail-closed choice for the *same* INCR+EXPIRE shape, not an oversight — see
the #1458 PR report for the full reasoning, and flip ``MCP_RATE_LIMIT_FAIL_CLOSED=true``
once Redis is confirmed live on that app if a stricter posture is wanted.
"""

from __future__ import annotations

import os

import structlog
from starlette.responses import JSONResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from services.cache.redis_factory import RedisFactory
from services.mcp.server.identity import MCPTokenVerifier

logger = structlog.get_logger(__name__)

# Conservative default: this gates read-only resource/tool traffic from a handful of
# alpha testers, not bulk API consumption. Env-configurable (Arch's instruction) so PA/
# HOST can retune for beta without a code change — same convention
# ``usage_cap_middleware.py`` uses for its own thresholds.
DEFAULT_LIMIT_PER_MINUTE = 30
WINDOW_SECONDS = 60

RATE_KEY_PREFIX = "mcp_rl:"


def _limit_per_minute() -> int:
    return int(os.environ.get("MCP_RATE_LIMIT_PER_MINUTE", str(DEFAULT_LIMIT_PER_MINUTE)))


def _fail_closed() -> bool:
    """Opt-in stricter posture once Redis is confirmed provisioned on this app
    (see module docstring) — default False (fail-open on backend errors)."""
    return os.environ.get("MCP_RATE_LIMIT_FAIL_CLOSED", "false").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def _bearer_token(scope: Scope) -> str | None:
    """Raw bearer token from the ASGI ``headers`` list, or ``None`` if absent/
    malformed. ASGI header names are lower-cased bytes per spec; this does not
    assume FastMCP/Starlette have parsed anything yet (this middleware runs
    before that parsing)."""
    for name, value in scope.get("headers") or ():
        if name.lower() != b"authorization":
            continue
        try:
            decoded = value.decode("latin-1")
        except UnicodeDecodeError:  # silent-ok: malformed header -> no token, not a crash
            return None
        if not decoded.lower().startswith("bearer "):
            return None
        return decoded[7:].strip() or None
    return None


def _rate_limited_response(retry_after: int, limit: int) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limited",
            "message": f"Rate limit: {limit} requests/minute per identity. Retry in {retry_after}s.",
            "retry_after_seconds": retry_after,
        },
        headers={"Retry-After": str(retry_after)},
    )


def _backend_unavailable_response(retry_after: int = 5) -> JSONResponse:
    """Only reachable when ``MCP_RATE_LIMIT_FAIL_CLOSED`` is set — see module
    docstring for why the default posture never reaches this."""
    return JSONResponse(
        status_code=503,
        content={
            "error": "capacity_check_unavailable",
            "message": "Temporarily unable to verify rate-limit capacity. Please retry shortly.",
            "retry_after_seconds": retry_after,
        },
        headers={"Retry-After": str(retry_after)},
    )


class MCPRateLimitMiddleware:
    """Per-verified-identity rate limit for the MCP path only.

    Placed BETWEEN :class:`~services.mcp.server.app.MCPPathGate` (outermost,
    deny-by-default for every path) and FastMCP's own auth+routing app
    (innermost): see module docstring for why this layer, not a handler-level
    check, is what can actually answer HTTP 429.
    """

    def __init__(
        self,
        app: ASGIApp,
        mcp_path: str,
        *,
        verifier: MCPTokenVerifier | None = None,
    ) -> None:
        self._app = app
        self._mcp_path = mcp_path.rstrip("/") or "/"
        # Lazily constructed on first use unless injected, mirroring
        # MCPTokenVerifier's own test-injection seam (identity.py) — a fresh
        # instance here if none is given, built from the CURRENT
        # AsyncSessionFactory.session_scope at first-use time, not at
        # __init__ time, so a test that monkeypatches the session factory
        # before calling build_asgi_app() still takes effect (same ordering
        # identity.py's own verifier already relies on).
        self._injected_verifier = verifier

    def _verifier_instance(self) -> MCPTokenVerifier:
        return self._injected_verifier or MCPTokenVerifier()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        path = scope["path"].rstrip("/") or "/"
        if path != self._mcp_path:
            await self._app(scope, receive, send)
            return

        token = _bearer_token(scope)
        if token is None:
            # No/garbled bearer: not our refusal to make. Let RequireAuthMiddleware
            # 401 it exactly as it would have before this middleware existed.
            await self._app(scope, receive, send)
            return

        try:
            access_token = await self._verifier_instance().verify_token(token)
        except Exception as e:  # silent-ok: identity check itself failed -> treat as unresolved, let real auth handle it
            logger.error("mcp_rate_limit_identity_check_failed", error=str(e))
            access_token = None

        if access_token is None:
            # Invalid/revoked/expired per OUR check too: let the real auth stack
            # produce the identical refusal it already would. We never originate
            # a distinguishable response for an unresolvable token.
            await self._app(scope, receive, send)
            return

        identity = access_token.client_id
        limit = _limit_per_minute()
        key = f"{RATE_KEY_PREFIX}{identity}"

        try:
            async with RedisFactory.redis_scope() as redis_client:
                count = await redis_client.incr(key)
                if count == 1:
                    await redis_client.expire(key, WINDOW_SECONDS)
                if count > limit:
                    ttl = await redis_client.ttl(key)
                    retry_after = ttl if ttl and ttl > 0 else WINDOW_SECONDS
                    logger.warning("mcp_rate_limited", identity=identity, count=count, limit=limit)
                    response = _rate_limited_response(retry_after, limit)
                    await response(scope, receive, send)
                    return
        except Exception as e:
            logger.error("mcp_rate_limit_backend_unavailable", identity=identity, error=str(e))
            if _fail_closed():
                response = _backend_unavailable_response()
                await response(scope, receive, send)
                return
            # Fail-open default: see module docstring. The request proceeds
            # unmetered rather than the whole endpoint 503ing on a Redis gap.

        await self._app(scope, receive, send)
