"""
JWT Token Blacklist Storage

Implements secure token invalidation using Redis with database fallback.
Provides O(1) blacklist lookups with automatic TTL expiration.

Usage:
    blacklist = TokenBlacklist(redis_factory, db_session_factory)
    await blacklist.initialize()

    # Add token to blacklist
    await blacklist.add(token_id="abc123", reason="logout", expires_at=datetime.now(timezone.utc) + timedelta(hours=1))

    # Check if blacklisted
    is_blocked = await blacklist.is_blacklisted("abc123")
"""

import json
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator, Optional
from uuid import UUID

import structlog

from services.cache.redis_factory import RedisFactory
from services.database.session_factory import AsyncSessionFactory
from services.utils.datetime_utils import ensure_utc, utc_now

logger = structlog.get_logger(__name__)


class TokenBlacklist:
    """
    Manages blacklisted JWT tokens for secure invalidation.

    Uses Redis for O(1) lookups with automatic TTL expiration.
    Falls back to database if Redis unavailable.

    Performance: <5ms for blacklist checks
    Storage: Token ID only (not full token)
    """

    def __init__(
        self,
        redis_factory: RedisFactory,
        db_session_factory: AsyncSessionFactory,
    ):
        """
        Initialize token blacklist.

        Args:
            redis_factory: Redis factory for connection management
            db_session_factory: Database session factory for fallback storage
        """
        self.redis_factory = redis_factory
        self.db_session_factory = db_session_factory
        self._redis_available = False

    async def initialize(self) -> None:
        """
        Initialize Redis connection and verify availability.

        Checks Redis connectivity. If unavailable, falls back to database storage.
        """
        try:
            redis = await self.redis_factory.create_client()
            await redis.ping()
            self._redis_available = True
            logger.info("TokenBlacklist: Redis available")
        except Exception as e:
            logger.warning(
                "TokenBlacklist: Redis unavailable, using database fallback",
                error=str(e),
            )
            self._redis_available = False

    async def add(
        self,
        token_id: str,
        reason: str,
        expires_at: datetime,
        user_id: Optional[UUID] = None,
    ) -> bool:
        """
        Add token to blacklist.

        Args:
            token_id: Unique token identifier (JTI claim)
            reason: Reason for blacklist (logout, security, admin)
            expires_at: Token expiration time (for TTL calculation)
            user_id: Optional user ID for audit trail

        Returns:
            True if successfully blacklisted
        """
        try:
            # Calculate TTL (seconds until expiration)
            # Use naive UTC for consistent timezone handling (Issue #769)
            now = utc_now()
            expires_at_naive = ensure_utc(expires_at)
            ttl = max(int((expires_at_naive - now).total_seconds()), 0)

            if ttl == 0:
                logger.info(
                    "Token already expired, skipping blacklist",
                    token_id=token_id,
                )
                return True

            if self._redis_available:
                # Redis: O(1) with automatic expiration
                redis = await self.redis_factory.create_client()
                key = f"blacklist:jwt:{token_id}"
                value = json.dumps(
                    {
                        "reason": reason,
                        "user_id": user_id,
                        "blacklisted_at": now.isoformat(),
                    }
                )
                await redis.setex(key, ttl, value)
                logger.info(
                    "Token blacklisted via Redis",
                    token_id=token_id,
                    reason=reason,
                    ttl=ttl,
                )
                return True
            else:
                # Database fallback
                return await self._add_to_database(token_id, reason, expires_at, user_id)

        except Exception as e:
            logger.error("Failed to blacklist token", token_id=token_id, error=str(e))
            return False

    async def is_blacklisted(self, token_id: str) -> bool:
        """
        Check if token is blacklisted.

        Args:
            token_id: Token identifier to check

        Returns:
            True if blacklisted, False otherwise

        Note:
            Fails closed (returns True) on errors for security
        """
        try:
            if self._redis_available:
                # Redis: O(1) lookup
                redis = await self.redis_factory.create_client()
                key = f"blacklist:jwt:{token_id}"
                exists = await redis.exists(key)
                return bool(exists)
            else:
                # Database fallback
                return await self._check_database(token_id)

        except Exception as e:
            logger.error(
                "Failed to check blacklist, failing closed",
                token_id=token_id,
                error=str(e),
            )
            # Fail closed: assume blacklisted on error for security
            return True

    async def remove_expired(self) -> int:
        """
        Clean up expired blacklist entries.

        Redis entries expire automatically via TTL.
        This method only cleans database fallback entries.

        Returns:
            Number of entries removed (0 for Redis)
        """
        if self._redis_available:
            # Redis handles expiration automatically
            logger.debug("Redis auto-expires, no cleanup needed")
            return 0
        else:
            # Database cleanup
            return await self._cleanup_database()

    async def revoke_user_tokens(self, user_id: UUID, reason: str = "security") -> int:
        """
        Revoke all active tokens for a user (security incident response).

        Note: Requires token registry to track user tokens.
        This is a placeholder for future implementation.

        Args:
            user_id: User whose tokens to revoke
            reason: Revocation reason

        Returns:
            Number of tokens revoked
        """
        logger.error(
            "revoke_user_tokens called but NOT implemented - needs token registry",
            user_id=user_id,
            reason=reason,
        )
        # #1436 F4 (Arch: security no-ops must fail LOUD): the silent `return 0`
        # was success-shaped — an incident responder calling this would believe
        # tokens were revoked when nothing happened. Raise until the token
        # registry exists.
        raise NotImplementedError(  # nie-ok: Arch-ruled loud security stub (#1436 F4) — silent 0 was the defect
            "revoke_user_tokens requires a per-user token registry (not yet built); "
            "no tokens were revoked"
        )

    async def _add_to_database(
        self,
        token_id: str,
        reason: str,
        expires_at: datetime,
        user_id: Optional[UUID],
    ) -> bool:
        """
        Database fallback for token blacklist.

        Args:
            token_id: Token identifier
            reason: Blacklist reason
            expires_at: Token expiration
            user_id: Optional user ID

        Returns:
            True if successful
        """
        try:
            async with self.db_session_factory.session_scope() as session:
                # Import here to avoid circular dependencies
                from services.database.models import TokenBlacklist as DBTokenBlacklist

                entry = DBTokenBlacklist(
                    token_id=token_id,
                    reason=reason,
                    user_id=user_id,
                    expires_at=ensure_utc(expires_at),
                    created_at=utc_now(),
                )
                session.add(entry)
                await session.commit()

                logger.info(
                    "Token blacklisted via database",
                    token_id=token_id,
                    reason=reason,
                )
                return True

        except Exception as e:
            logger.error(
                "Database blacklist failed",
                token_id=token_id,
                error=str(e),
            )
            return False

    async def _check_database(self, token_id: str) -> bool:
        """
        Check database for blacklisted token.

        Args:
            token_id: Token identifier to check

        Returns:
            True if blacklisted, False otherwise
        """
        try:
            async with self.db_session_factory.session_scope() as session:
                from sqlalchemy import select

                from services.database.models import TokenBlacklist as DBTokenBlacklist

                query = select(DBTokenBlacklist).where(
                    DBTokenBlacklist.token_id == token_id,
                    DBTokenBlacklist.expires_at > utc_now(),
                )
                result = await session.execute(query)
                entry = result.scalar_one_or_none()

                return entry is not None

        except Exception as e:
            logger.error(
                "Database check failed, failing closed",
                token_id=token_id,
                error=str(e),
            )
            # Fail closed for security
            return True

    async def _cleanup_database(self) -> int:
        """
        Remove expired entries from database.

        Returns:
            Number of entries removed
        """
        try:
            async with self.db_session_factory.session_scope() as session:
                from sqlalchemy import delete

                from services.database.models import TokenBlacklist as DBTokenBlacklist

                query = delete(DBTokenBlacklist).where(DBTokenBlacklist.expires_at <= utc_now())
                result = await session.execute(query)
                await session.commit()

                count = result.rowcount
                logger.info("Cleaned up expired blacklist entries", count=count)
                return count

        except Exception as e:
            logger.error("Database cleanup failed", error=str(e))
            return 0
