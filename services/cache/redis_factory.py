"""
Redis Connection Factory - Following AsyncSessionFactory Pattern
Provides Redis client management with connection pooling and health monitoring
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

import redis.asyncio as redis
import structlog

from services.health.integration_health_monitor import health_monitor

logger = structlog.get_logger()


class RedisFactory:
    """Redis client factory following AsyncSessionFactory pattern"""

    _redis_pool: Optional[redis.ConnectionPool] = None
    _pool_loop_id: Optional[int] = None

    @classmethod
    async def initialize(cls) -> None:
        """Initialize Redis connection pool.

        #1452: the pool's connections bind to the event loop they were created
        on. A cached pool that outlives its loop throws "Event loop is closed"
        on every use — which made the usage-cap middleware fail-closed with
        503 capacity_check_unavailable (the Redis twin of the #1193 poisoned
        DB-pool class). Detect loop change and rebuild.
        """
        import asyncio

        loop_id = id(asyncio.get_running_loop())
        if cls._redis_pool is not None and cls._pool_loop_id != loop_id:
            try:
                await cls._redis_pool.disconnect()
            except Exception:
                pass  # the old loop is gone; the pool is unusable either way
            cls._redis_pool = None

        if cls._redis_pool is None:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
            cls._redis_pool = redis.ConnectionPool.from_url(
                redis_url,
                max_connections=20,
                retry_on_timeout=True,
                decode_responses=False,  # Keep bytes for JSON serialization
            )

            cls._pool_loop_id = loop_id
            logger.info("Redis connection pool initialized", redis_url=redis_url)

    @classmethod
    async def create_client(cls) -> redis.Redis:
        """Create Redis client from pool"""
        await cls.initialize()
        client = redis.Redis(connection_pool=cls._redis_pool)

        # Test connection
        try:
            await client.ping()
            health_monitor.record_success("redis_connection", 5.0, {"status": "connected"})
        except Exception as e:
            health_monitor.record_failure("redis_connection", str(e))
            logger.error(f"Redis connection test failed: {e}")

        return client

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
