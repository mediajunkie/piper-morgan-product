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

Backend: Redis-if-configured, in-memory otherwise — NOT Redis-always (PA review finding,
2026-10-05, corrected from this file's first revision)
-----------------------------------------------------------------------------------------
The first revision of this module assumed Redis was always reachable and failed OPEN
(unmetered) on any Redis error, reasoning that ``REDIS_URL`` provisioning on the
``piper-morgan-mcp`` Fly app was merely *unverified*. PA then actually ran ``fly secrets
list -a piper-morgan-mcp`` and found exactly one secret, ``DATABASE_URL`` — no
``REDIS_URL``, on either ``fly.mcp.toml`` or ``fly.toml``. :class:`~services.cache.
redis_factory.RedisFactory` defaults an unset ``REDIS_URL`` to
``redis://localhost:6379``, which does not exist on that Fly app's machine — so in
production every ``INCR`` would error, and the fail-OPEN default meant the limiter
would enforce **nothing**, silently, while every test here (which mocks or runs against
a local dev Redis) stayed green. That is exactly the "all clear" that measured the wrong
thing (m-44) — unverified was being treated as probably-fine when it was actually
checkable and false. Fixed as follows:

1. **Backend selection is gated on ``REDIS_URL`` being SET, not on trying and catching.**
   :func:`_redis_url_configured` checks the env var directly. If unset, this module never
   attempts Redis at all — it goes straight to the in-memory counter every time. This
   matters specifically because local dev DOES have a Redis running on
   ``RedisFactory``'s hardcoded default (``docker compose``), so "try Redis, catch on
   failure" would have silently used Redis in every local/test run while production (no
   local Redis, no ``REDIS_URL``) silently got nothing — the exact false-clear PA found.
   Gating on the env var means the DECISION matches production's actual topology instead
   of whatever happens to be listening on ``localhost:6379`` wherever the process runs.
2. **If ``REDIS_URL`` IS set but a request's Redis call still errors** (outage, not
   missing config), this middleware falls back to the SAME in-memory counter for THAT
   request, logs a single WARNING (not one per request — see
   :meth:`MCPRateLimitMiddleware._warn_redis_fallback_once`), and still ENFORCES the
   limit via memory. It never goes fully unmetered on a transient Redis failure anymore.
3. :data:`MCP_RATE_LIMIT_FAIL_CLOSED` remains as a last-resort opt-in (503 instead of
   proceeding) for the case where the rate-limit check raises an exception the fallback
   itself can't absorb (the in-memory path is pure-Python dict arithmetic and should not
   raise in practice — this is defensive, not the expected path).
4. One INFO line is logged once per process, on the first ``/mcp`` request, naming the
   backend this process is actually using (``"redis"`` or ``"memory"``) — see
   :meth:`MCPRateLimitMiddleware._log_active_backend_once` — so a deploy's logs show
   which one is live without reading source.

In-memory backend: per-machine, explicit caveat (unchanged concern from the first
revision, now the ACTUAL default on ``piper-morgan-mcp`` rather than a hypothetical)
----------------------------------------------------------------------------------------
:class:`_InMemoryFixedWindow` is a plain per-process dict keyed by identity — it does
NOT share state across machines. ``fly.mcp.toml`` sets ``auto_start_machines = true``
with no explicit concurrency cap, so this app can and does run more than the one
always-on machine under load (a "burst" machine). A caller split across N machines by
Fly's load balancer gets an effective limit of roughly N × ``MCP_RATE_LIMIT_PER_MINUTE``,
not exactly the configured number. This is EXPLICITLY ACCEPTED for the current
alpha/probe stage (a handful of named testers, abuse-resistance rather than hard
metering) and is NOT silent: this paragraph, the module's log line (point 4 above), and
the #1458 PR report all name it. If Redis is provisioned on this app later (the
genuinely-shared, cross-machine-correct backend this module already supports), the
caveat disappears automatically — no code change needed, just set ``REDIS_URL``.
"""

from __future__ import annotations

import os
import time

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
    """Opt-in last-resort posture (503) if the rate-limit check itself raises
    something even the in-memory fallback can't absorb — see module
    docstring point 3. Default False."""
    return os.environ.get("MCP_RATE_LIMIT_FAIL_CLOSED", "false").strip().lower() in (
        "1",
        "true",
        "yes",
    )


def _redis_url_configured() -> bool:
    """Whether ``REDIS_URL`` is actually SET — the backend-selection gate
    (module docstring point 1). Deliberately NOT "try Redis and see": an
    unset ``REDIS_URL`` must never silently fall through to
    ``RedisFactory``'s ``redis://localhost:6379`` default, which is reachable
    in local dev (docker compose) but does not exist on the production MCP
    Fly app — that mismatch is exactly what produced the false "all tests
    green, nothing enforced in prod" clear this revision fixes."""
    return bool(os.environ.get("REDIS_URL", "").strip())


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
    """Only reachable when ``MCP_RATE_LIMIT_FAIL_CLOSED`` is set AND the
    in-memory fallback itself raised — see module docstring point 3; this is
    a defensive last resort, not the expected path."""
    return JSONResponse(
        status_code=503,
        content={
            "error": "capacity_check_unavailable",
            "message": "Temporarily unable to verify rate-limit capacity. Please retry shortly.",
            "retry_after_seconds": retry_after,
        },
        headers={"Retry-After": str(retry_after)},
    )


class _InMemoryFixedWindow:
    """A plain per-process fixed-window counter — the fallback/default
    backend (module docstring: per-machine, caveat stated there). Pure dict
    arithmetic with no ``await`` between read and write, so it is safe
    without an explicit lock under asyncio's cooperative scheduling (no
    other coroutine can run between the read and the write)."""

    def __init__(self) -> None:
        self._windows: dict[str, tuple[int, float]] = {}  # key -> (count, expires_at)

    def increment(self, key: str, window_seconds: int) -> tuple[int, int]:
        """Returns ``(count_after_increment, retry_after_seconds_if_over)``."""
        now = time.monotonic()
        count, expires_at = self._windows.get(key, (0, 0.0))
        if now >= expires_at:
            count = 0
            expires_at = now + window_seconds
        count += 1
        self._windows[key] = (count, expires_at)
        retry_after = max(1, int(expires_at - now))
        return count, retry_after


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
        self._memory = _InMemoryFixedWindow()
        # "Once per process" flags — instance-scoped, which is equivalent to
        # process-scoped in production (main_mcp.py builds this app exactly
        # once) and resets per-test here, which is the right unit for a test.
        self._backend_logged = False
        self._redis_fallback_warned = False

    def _verifier_instance(self) -> MCPTokenVerifier:
        return self._injected_verifier or MCPTokenVerifier()

    def _log_active_backend_once(self) -> None:
        if self._backend_logged:
            return
        self._backend_logged = True
        backend = "redis" if _redis_url_configured() else "memory"
        logger.info("mcp_rate_limit_backend_active", backend=backend)

    def _warn_redis_fallback_once(self, error: Exception) -> None:
        if self._redis_fallback_warned:
            return
        self._redis_fallback_warned = True
        logger.warning("mcp_rate_limit_redis_unavailable_falling_back_to_memory", error=str(error))

    async def _check_and_increment(self, identity: str) -> tuple[int, int]:
        """``(count_after_increment, retry_after_seconds_if_over)``, via
        Redis if configured and reachable, else the in-memory fallback (see
        module docstring points 1-2)."""
        key = f"{RATE_KEY_PREFIX}{identity}"

        if _redis_url_configured():
            try:
                async with RedisFactory.redis_scope() as redis_client:
                    count = await redis_client.incr(key)
                    if count == 1:
                        await redis_client.expire(key, WINDOW_SECONDS)
                        retry_after = WINDOW_SECONDS
                    else:
                        ttl = await redis_client.ttl(key)
                        retry_after = ttl if ttl and ttl > 0 else WINDOW_SECONDS
                    return count, retry_after
            except Exception as e:
                self._warn_redis_fallback_once(e)
                # fall through to memory below — NEVER fail fully open here.

        return self._memory.increment(key, WINDOW_SECONDS)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self._app(scope, receive, send)
            return

        path = scope["path"].rstrip("/") or "/"
        if path != self._mcp_path:
            await self._app(scope, receive, send)
            return

        self._log_active_backend_once()

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

        try:
            count, retry_after = await self._check_and_increment(identity)
        except Exception as e:
            # Defensive last resort only — see module docstring point 3; the
            # in-memory path should never actually raise.
            logger.error(
                "mcp_rate_limit_check_failed_unexpectedly", identity=identity, error=str(e)
            )
            if _fail_closed():
                response = _backend_unavailable_response()
                await response(scope, receive, send)
                return
            await self._app(scope, receive, send)
            return

        if count > limit:
            logger.warning("mcp_rate_limited", identity=identity, count=count, limit=limit)
            response = _rate_limited_response(retry_after, limit)
            await response(scope, receive, send)
            return

        await self._app(scope, receive, send)
