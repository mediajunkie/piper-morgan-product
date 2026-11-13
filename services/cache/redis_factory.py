"""
Redis Connection Factory - Following AsyncSessionFactory Pattern
Provides Redis client management with connection pooling and health monitoring
"""

import asyncio
import os
import time
import weakref
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from urllib.parse import urlsplit

import redis.asyncio as redis
import structlog

from services.health.integration_health_monitor import health_monitor
from services.infrastructure.logging.evidence import evidence  # noqa: E402 (#2350)

logger = structlog.get_logger()

# #2336: create_client used to PING on every client it handed out, an extra round
# trip on every Redis read (each authenticated request's revocation check). The
# ping gates nothing (a failure only logs); it feeds the redis_connection health
# record. So it runs on a new pool's first client, then at most once per interval.
_HEALTH_PING_INTERVAL_S = 30.0


def _redis_host(redis_url: str) -> str:
    """host:port of a Redis URL, for logs; drops the scheme, user and password."""
    parts = urlsplit(redis_url)
    return f"{parts.hostname}:{parts.port or 6379}"


class RedisFactory:
    """Redis client factory following AsyncSessionFactory pattern"""

    _redis_pool: Optional[redis.ConnectionPool] = None
    _last_health_ping: Optional[float] = None  # time.monotonic(); None = never on this pool
    # #2348: the outcome of the most recent health ping, for /health. None = no ping yet in
    # this process. /health reads it and never pings (the #2336 lesson: it is hit too often).
    _last_ping_ok: Optional[bool] = None
    _last_ping_recorded_at: Optional[float] = None  # time.monotonic() of that outcome
    # A weak reference, not id(loop): a collected loop's id() can be handed to
    # the next loop, which then inherited the dead loop's pool (found 11-09 by
    # the 2334 rebuild pin failing only in the full suite).
    _pool_loop_ref: Optional["weakref.ReferenceType[asyncio.AbstractEventLoop]"] = None

    @classmethod
    async def initialize(cls) -> None:
        """Initialize Redis connection pool.

        #1452: the pool's connections bind to the event loop they were created
        on. A cached pool that outlives its loop throws "Event loop is closed"
        on every use — which made the usage-cap middleware fail-closed with
        503 capacity_check_unavailable (the Redis twin of the #1193 poisoned
        DB-pool class). Detect loop change and rebuild.
        """
        loop = asyncio.get_running_loop()
        pool_loop = cls._pool_loop_ref() if cls._pool_loop_ref is not None else None
        if cls._redis_pool is not None and pool_loop is not loop:
            try:
                await cls._redis_pool.disconnect()
            except Exception:
                pass  # the old loop is gone; the pool is unusable either way
            cls._redis_pool = None

        if cls._redis_pool is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            # #2334: a plain ConnectionPool RAISES "Too many connections" once all 20
            # are checked out, so a burst of >20 concurrent requests failed closed in
            # the token blacklist. The blocking pool waits up to `timeout` for a free
            # slot instead (redis-py 5.0.1 defaults that wait to 20 s, hence explicit).
            # The socket timeouts bound reaching a dead or blackholed Redis, which the
            # pool timeout doesn't cover; from_url leaves both unset. Size stays 20
            # until Upstash's per-plan connection limit is read (Arch 11-09 10:31).
            cls._redis_pool = redis.BlockingConnectionPool.from_url(
                redis_url,
                max_connections=20,
                timeout=2,
                socket_connect_timeout=2,
                socket_timeout=5,
                retry_on_timeout=True,
                decode_responses=False,  # Keep bytes for JSON serialization
            )

            cls._pool_loop_ref = weakref.ref(loop)
            cls._last_health_ping = None
            # #2335: never log the URL itself; an Upstash REDIS_URL carries the password.
            evidence("Redis connection pool initialized", redis_host=_redis_host(redis_url))

    @classmethod
    async def create_client(cls) -> redis.Redis:
        """Create Redis client from pool"""
        await cls.initialize()
        client = redis.Redis(connection_pool=cls._redis_pool)

        now = time.monotonic()
        if cls._last_health_ping is None or now - cls._last_health_ping >= _HEALTH_PING_INTERVAL_S:
            cls._last_health_ping = now
            try:
                await client.ping()
                latency_ms = (time.monotonic() - now) * 1000
                health_monitor.record_success(
                    "redis_connection", latency_ms, {"status": "connected"}
                )
                cls._last_ping_ok = True
                cls._last_ping_recorded_at = time.monotonic()
            except Exception as e:
                cls._last_ping_ok = False
                cls._last_ping_recorded_at = time.monotonic()
                health_monitor.record_failure("redis_connection", str(e))
                logger.error(f"Redis connection test failed: {e}")

        return client

    @classmethod
    def recorded_health(cls) -> str:
        """``ok`` or ``unavailable``: the recorded outcome of the last health ping (#2348).

        Never pings and never raises. No ping yet in this process reads ``unavailable``,
        since nothing has shown Redis answering. The ping runs when a client is taken
        and at most every 30 s, so on a quiet host the record is as old as the last
        request that used Redis.
        """
        return "ok" if cls._last_ping_ok is True else "unavailable"

    @classmethod
    def recorded_health_age_s(cls) -> Optional[int]:
        """Whole seconds since the recorded ping, or None when there has been none."""
        if cls._last_ping_ok is None or cls._last_ping_recorded_at is None:
            return None
        return max(0, int(time.monotonic() - cls._last_ping_recorded_at))

    @classmethod
    @asynccontextmanager
    async def redis_scope(cls) -> AsyncGenerator[redis.Redis, None]:
        """Redis client context manager following AsyncSessionFactory pattern"""
        client = await cls.create_client()
        try:
            yield client
        finally:
            await client.close()

    @classmethod
    async def close_pool(cls) -> None:
        """Close Redis connection pool"""
        if cls._redis_pool:
            await cls._redis_pool.disconnect()
            cls._redis_pool = None
            logger.info("Redis connection pool closed")
