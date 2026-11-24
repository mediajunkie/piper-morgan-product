"""
Usage-Cap Enforcement Middleware (ADR-076)

Two independent mechanisms, both Redis-backed (never in-process — the #1109
lesson: per-worker counters silently multiply by worker count):

1. Rate limit — a per-principal fixed-window counter (Redis INCR+EXPIRE,
   atomic natively, no Lua needed). ADR-076 D1 names sliding-window/token-bucket
   as the reference shapes; a fixed window is the simplest member of that family
   and sufficient for an alpha-stage welfare backstop (the ADR's own consequences
   section: "the numbers are product... the shape is the durable architecture").
2. Concurrency cap — an instance-wide gauge of DISTINCT recently-active
   principals, implemented as a Redis sorted set (score = last-seen timestamp).
   TTL-pruned via ZREMRANGEBYSCORE before each check, so an abandoned session
   releases its slot automatically without an explicit decrement — matching
   "concurrent SESSIONS" (a period of activity) rather than "concurrent
   in-flight requests" (one HTTP call).

Principal = ``request.state.user_id`` (set by AuthMiddleware) when authenticated,
else client IP. Both mechanisms key on the same principal so an unauthenticated
caller can't dodge one dimension of the cap by lacking the other.

Placement (verified empirically, not assumed): Starlette's ``add_middleware``
inserts at position 0 of the internal stack, so LATER calls become MORE OUTER
(execute first on request). AuthMiddleware must resolve ``request.state.user_id``
before this middleware reads it, so this middleware's own ``add_middleware`` call
must happen BEFORE AuthMiddleware's in web/app.py, not after.

Fail-closed (D4): a Redis outage denies rather than silently allowing unbounded
access. Fail-visibly (D5): every rejection to a background request is a JSON body with
a machine-parseable ``error`` field + ``retry_after_seconds``, never a silent hang or bare
string. Issue 2431: a page load (``services.api.refusal_pages.wants_a_page``) gets a plain
page with the same sentence instead, and the same status and ``Retry-After``.
"""

import os
import time
from typing import List, Optional

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from services.api.errors import (
    PIPER_CANT_TAKE_REQUESTS_MESSAGE,
    PIPER_IS_FULL_MESSAGE,
    RATE_LIMITED_MESSAGE,
)
from services.api.refusal_pages import refusal_page, wants_a_page
from services.cache.redis_factory import RedisFactory

logger = structlog.get_logger(__name__)

# Thresholds are config, not hardcoded (ADR-076 consequences) — PM/HOST can
# retune for beta without a code change. Defaults match the PM-ratified
# alpha thresholds (2026-07-04, via HOST).
RATE_LIMIT_PER_MINUTE = int(os.getenv("USAGE_CAP_RATE_PER_MINUTE", "100"))
MAX_CONCURRENT_SESSIONS = int(os.getenv("USAGE_CAP_MAX_CONCURRENT", "10"))
# How long a principal is considered "recently active" for the concurrency
# gauge after its last request — NOT the same as the 60s rate-limit window.
# A chat session spans many requests over a period of use; this is the idle
# timeout after which a quiet session releases its slot.
CONCURRENT_SESSION_IDLE_SECONDS = int(os.getenv("USAGE_CAP_IDLE_SECONDS", "600"))

RATE_KEY_PREFIX = "usage_cap:rate:"
CONCURRENCY_GAUGE_KEY = "usage_cap:active_sessions"

# D6: rate-exempt routes are an explicit, justified allowlist (same discipline
# as #1307/#1308's auth-exempt list) — an unrecorded exemption is an abuse
# surface. Health checks are monitoring/uptime infrastructure, not user load;
# same justification AuthMiddleware's EXEMPT_HEALTH_PATHS uses, reproduced
# explicitly here rather than imported, since the two lists are exempt for
# different reasons and could legitimately diverge later.
RATE_EXEMPT_PATHS: List[str] = [
    "/health",
    "/api/v1/health",
    # Static files are not the spend this cap guards (ADR-076: API/LLM abuse), and
    # one page load fans out ~32 of them — three navigations in a minute blew the
    # 100/min budget and the fourth page came back half-rendered as 429s (#1874).
    "/static/",
    "/assets/",
]


def _resolve_principal(request: Request) -> str:
    """The identity both mechanisms key on: authenticated user_id, else client IP.

    Falls back to IP (not a shared "anonymous" bucket) so one unauthenticated
    caller can't exhaust a pool shared by every other unauthenticated caller —
    the same per-principal welfare rationale ADR-076 D3 states for authenticated
    users.
    """
    user_id = getattr(request.state, "user_id", None)
    if user_id:
        return f"user:{user_id}"

    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        ip = forwarded_for.split(",")[0].strip()
    else:
        ip = request.client.host if request.client else "unknown"
    return f"ip:{ip}"


def _rate_limited_response(request: Request, retry_after: int) -> Response:
    """429 (issue 2431, CXO's words): a page for a page load, the sentence as ``message``
    otherwise. The per-minute number is gone from the words; the seconds stay, put in by
    the one shape the guard allows (Arch, mail 01M87EY4N7): ``.format(seconds=int(...))``.
    The spoken number is never below 2 (CXO, mail 01M87GHNFX), so the line never says
    "1 seconds"; the ``Retry-After`` header and ``retry_after_seconds`` keep the real value."""
    if wants_a_page(request):
        return refusal_page(
            RATE_LIMITED_MESSAGE.format(seconds=int(max(2, retry_after))), 429, retry_after
        )
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limited",
            "message": RATE_LIMITED_MESSAGE.format(seconds=int(max(2, retry_after))),
            "retry_after_seconds": retry_after,
        },
        headers={"Retry-After": str(retry_after)},
    )


def _at_capacity_response(request: Request) -> Response:
    """503 at capacity (issue 2431, CXO's words). The session counts are logged at the
    call site and never sent: operator numbers that say how many other people are on."""
    if wants_a_page(request):
        return refusal_page(PIPER_IS_FULL_MESSAGE, 503, 30)
    return JSONResponse(
        status_code=503,
        content={
            "error": "at_capacity",
            "message": PIPER_IS_FULL_MESSAGE,
            "retry_after_seconds": 30,
        },
        headers={"Retry-After": "30"},
    )


def _redis_unavailable_response(request: Request) -> Response:
    """D4 fail-closed: a Redis outage denies rather than silently allowing
    unbounded access. Distinct from the two above: "we couldn't verify your
    capacity," not "you are over your limit."

    Issue 2431 (Arch's ruling): a page load gets a plain page with CXO's sentence and a
    reload link, never JSON and never a redirect; everything else keeps JSON, with the
    sentence as ``message`` and ``capacity_check_unavailable`` kept for code and the log."""
    if wants_a_page(request):
        return refusal_page(PIPER_CANT_TAKE_REQUESTS_MESSAGE, 503, 5)
    return JSONResponse(
        status_code=503,
        content={
            "error": "capacity_check_unavailable",
            "message": PIPER_CANT_TAKE_REQUESTS_MESSAGE,
            "retry_after_seconds": 5,
        },
        headers={"Retry-After": "5"},
    )


class UsageCapMiddleware(BaseHTTPMiddleware):
    """ADR-076: per-principal rate limit + instance-wide concurrency cap."""

    def __init__(self, app, rate_exempt_paths: Optional[List[str]] = None):
        super().__init__(app)
        self.rate_exempt_paths = rate_exempt_paths or list(RATE_EXEMPT_PATHS)

    def _is_exempt(self, path: str) -> bool:
        return any(path.startswith(exempt) for exempt in self.rate_exempt_paths)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if self._is_exempt(request.url.path):
            return await call_next(request)

        principal = _resolve_principal(request)

        try:
            async with RedisFactory.redis_scope() as redis:
                # --- Mechanism 1: rate limit (fixed-window, atomic INCR) ---
                rate_key = f"{RATE_KEY_PREFIX}{principal}"
                count = await redis.incr(rate_key)
                if count == 1:
                    await redis.expire(rate_key, 60)
                if count > RATE_LIMIT_PER_MINUTE:
                    ttl = await redis.ttl(rate_key)
                    retry_after = ttl if ttl and ttl > 0 else 60
                    logger.warning("usage_cap_rate_limited", principal=principal, count=count)
                    return _rate_limited_response(request, retry_after)

                # --- Mechanism 2: concurrency cap (ZSET gauge, TTL-pruned) ---
                # #1390: AUTHENTICATED principals only. The gauge measures live
                # user sessions (ADR-076's LLM-cost protection); unauthenticated
                # requests 401 at auth and never reach an LLM — they are not
                # session load. Found live on beta day one: ten scanner IPs
                # filled the 10-slot gauge and starved real users. ip:*
                # principals remain fully covered by mechanism 1's per-IP rate
                # limit above.
                # #1452: the gauge block is guarded (not an early
                # `return await call_next(...)` inside this try) so DOWNSTREAM
                # handler exceptions can never be swallowed here and
                # misreported as capacity 503s — that masking bug made a
                # template-init error on "/" read as capacity_check_unavailable.
                if principal.startswith("user:"):
                    now = time.time()
                    await redis.zremrangebyscore(
                        CONCURRENCY_GAUGE_KEY, "-inf", now - CONCURRENT_SESSION_IDLE_SECONDS
                    )
                    is_active = await redis.zscore(CONCURRENCY_GAUGE_KEY, principal) is not None
                    if not is_active:
                        current_count = await redis.zcard(CONCURRENCY_GAUGE_KEY)
                        if current_count >= MAX_CONCURRENT_SESSIONS:
                            logger.warning(
                                "usage_cap_at_capacity",
                                principal=principal,
                                current_count=current_count,
                            )
                            return _at_capacity_response(request)
                    # Register/refresh this principal's last-active timestamp —
                    # whether newly admitted or already an active member.
                    await redis.zadd(CONCURRENCY_GAUGE_KEY, {principal: now})
        except Exception as e:
            # D4: fail-closed. Anything that prevents verifying capacity
            # (connection refused, timeout, auth failure) denies rather than
            # silently falling through to unbounded access.
            logger.error("usage_cap_redis_unavailable", error=str(e), principal=principal)
            return _redis_unavailable_response(request)

        return await call_next(request)
