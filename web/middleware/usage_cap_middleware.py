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
access. Fail-visibly (D5): every rejection is a JSON body with a machine-parseable
``error`` field + ``retry_after_seconds``, never a silent hang or bare string.
"""

import os
import time
from typing import List, Optional

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

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


def _rate_limited_response(retry_after: int) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "error": "rate_limited",
            "message": f"Rate limit: {RATE_LIMIT_PER_MINUTE} requests/minute. Retry in {retry_after}s.",
            "retry_after_seconds": retry_after,
        },
        headers={"Retry-After": str(retry_after)},
    )


def _at_capacity_response(current: int, limit: int) -> JSONResponse:
    return JSONResponse(
        status_code=503,
        content={
            "error": "at_capacity",
            "message": f"Instance at capacity ({current}/{limit} active sessions). Try again shortly.",
            "retry_after_seconds": 30,
        },
        headers={"Retry-After": "30"},
    )


def _redis_unavailable_response() -> JSONResponse:
    """D4 fail-closed: a Redis outage denies rather than silently allowing
    unbounded access. Distinct message from the two above — this is "we
    couldn't verify your capacity," not "you are over your limit.\""""
    return JSONResponse(
        status_code=503,
        content={
            "error": "capacity_check_unavailable",
            "message": "Temporarily unable to verify usage capacity. Please retry shortly.",
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
                    logger.warning(
                        "usage_cap_rate_limited", principal=principal, count=count
                    )
                    return _rate_limited_response(retry_after)

                # --- Mechanism 2: concurrency cap (ZSET gauge, TTL-pruned) ---
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
                        return _at_capacity_response(current_count, MAX_CONCURRENT_SESSIONS)
                # Register/refresh this principal's last-active timestamp —
                # whether newly admitted or already an active member.
                await redis.zadd(CONCURRENCY_GAUGE_KEY, {principal: now})
        except Exception as e:
            # D4: fail-closed. Anything that prevents verifying capacity
            # (connection refused, timeout, auth failure) denies rather than
            # silently falling through to unbounded access.
            logger.error("usage_cap_redis_unavailable", error=str(e), principal=principal)
            return _redis_unavailable_response()

        return await call_next(request)
