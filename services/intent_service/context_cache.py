"""
ContextCache — Redis TTL cache for ContextAssembler gather methods (#984).

Cache-aside pattern with graceful fallback: on any Redis error, the cache
returns None (treated as miss) or False (treated as write-failure) and the
caller falls through to the source of truth. The system works the same with
Redis down as it does with Redis up — just slower.

Key namespace (PM-approved 2026-05-12): `context:{method}:{user_id}`.

Usage:
    cache = ContextCache()
    result = await cache.get_or_compute(
        key=f"context:calendar:{user_id}",
        ttl_seconds=60,
        compute_fn=lambda: self._compute_calendar_context(user_id),
    )
"""

import json
from typing import Any, Awaitable, Callable, Optional

import structlog

from services.cache.redis_factory import RedisFactory

logger = structlog.get_logger()


class ContextCache:
    """TTL cache for context_assembler gather methods.

    Graceful fallback: any Redis error → cache miss (returns None / False
    from set). Callers MUST handle None by computing the value from source.
    """

    def __init__(self, redis_factory: Optional[type] = None):
        """Initialize cache.

        Args:
            redis_factory: Override RedisFactory class (used by tests).
        """
        self._redis_factory = redis_factory or RedisFactory
        self._warned_unavailable = False

    async def _get_client(self):
        """Acquire a Redis client. Returns None if Redis is unavailable.

        Logs a single WARN on first unavailability so we don't spam logs.
        """
        try:
            return await self._redis_factory.create_client()
        except Exception as e:
            if not self._warned_unavailable:
                logger.warning(
                    "context_cache_unavailable",
                    error=str(e),
                    note="Falling through to source-of-truth for all cache ops",
                )
                self._warned_unavailable = True
            return None

    async def get(self, key: str) -> Optional[Any]:
        """Get a cached value. Returns None on miss or any error."""
        client = await self._get_client()
        if client is None:
            return None
        try:
            raw = await client.get(key)
            if raw is None:
                return None
            return json.loads(raw.decode() if isinstance(raw, bytes) else raw)
        except Exception as e:
            logger.warning("context_cache_get_error", key=key, error=str(e))
            return None

    async def set(self, key: str, value: Any, ttl_seconds: int) -> bool:
        """Store a value with TTL. Returns True on success, False on error.

        Errors are logged but never raise — the cache layer must never
        prevent the caller from returning its computed value.
        """
        client = await self._get_client()
        if client is None:
            return False
        try:
            payload = json.dumps(value)
            await client.setex(key, ttl_seconds, payload)
            return True
        except (TypeError, ValueError) as e:
            logger.warning(
                "context_cache_set_serialize_error",
                key=key,
                error=str(e),
                note="Value not JSON-serializable; caller still gets correct result",
            )
            return False
        except Exception as e:
            logger.warning("context_cache_set_error", key=key, error=str(e))
            return False

    async def get_or_compute(
        self,
        key: str,
        ttl_seconds: int,
        compute_fn: Callable[[], Awaitable[Any]],
    ) -> Any:
        """Cache-aside helper. Returns cached value on hit, else computes,
        stores, and returns. On any cache error, falls through to compute_fn
        without attempting to cache its result.
        """
        cached = await self.get(key)
        if cached is not None:
            return cached
        value = await compute_fn()
        if value is not None:
            await self.set(key, value, ttl_seconds)
        return value

    async def invalidate(self, key: str) -> bool:
        """Delete a key. Returns True if key was deleted, False otherwise
        (miss, error, or Redis unavailable). Logged either way.
        """
        client = await self._get_client()
        if client is None:
            return False
        try:
            deleted = await client.delete(key)
            logger.info(
                "context_cache_invalidated",
                key=key,
                deleted=bool(deleted),
            )
            return bool(deleted)
        except Exception as e:
            logger.warning("context_cache_invalidate_error", key=key, error=str(e))
            return False

    async def invalidate_prefix(self, prefix: str) -> int:
        """Delete all keys matching `{prefix}*`. Returns count of keys
        deleted (0 on miss / error / unavailable). Uses SCAN for production-
        safe iteration.
        """
        client = await self._get_client()
        if client is None:
            return 0
        try:
            cursor = 0
            total_deleted = 0
            pattern = f"{prefix}*"
            while True:
                cursor, keys = await client.scan(cursor=cursor, match=pattern, count=100)
                if keys:
                    total_deleted += await client.delete(*keys)
                if cursor == 0:
                    break
            logger.info(
                "context_cache_prefix_invalidated",
                prefix=prefix,
                count=total_deleted,
            )
            return total_deleted
        except Exception as e:
            logger.warning(
                "context_cache_invalidate_prefix_error",
                prefix=prefix,
                error=str(e),
            )
            return 0
