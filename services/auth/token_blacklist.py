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

from services.auth.jwt_service import BlacklistUnavailable
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
        # #1802: `_redis_available = False` used to mean two different things
        # indistinguishably — "initialize() ran and found no Redis" and
        # "initialize() never ran at all" (e.g. a bare TestClient that skips
        # the app's startup lifespan). `_initialized` separates them so the
        # DB-fallback log line below can say which one actually happened,
        # instead of the silent default reading as a deliberate Redis check.
        self._initialized = False

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
        finally:
            # Set regardless of outcome: "initialized" means initialize() was
            # called and made a real determination, not that it succeeded.
            self._initialized = True

    def _warn_if_never_initialized(self, token_id: str, operation: str) -> None:
        """Make the silent-default DB fallback loud (#1802 AC item 2).

        Purely additive logging — does not change which branch is taken.
        `_redis_available` being False routes to the database fallback either
        way; this only tells an operator WHY, which they could not previously
        distinguish from the log alone.
        """
        if not self._initialized:
            logger.warning(
                "token_blacklist_never_initialized",
                token_id=token_id,
                operation=operation,
                detail=(
                    "TokenBlacklist.initialize() was never called before this "
                    "check — routing to the database fallback without ever "
                    "having checked Redis (not 'Redis was checked and found "
                    "down'). Expected under a bare TestClient that skips the "
                    "app's startup lifespan; if seen on a running server, "
                    "startup wiring is missing."
                ),
            )

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
                self._warn_if_never_initialized(token_id, operation="add")
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
            True if blacklisted, False if definitively not blacklisted

        Raises:
            BlacklistUnavailable: if the store could not be reached, so
                revocation status is UNKNOWN (#1792)

        Note:
            Still fails CLOSED — an unreachable store refuses the request. It
            just refuses it honestly. Returning True here used to be
            indistinguishable from a real blacklist hit, which made a store
            outage report as a mass revocation (see BlacklistUnavailable).
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
                self._warn_if_never_initialized(token_id, operation="is_blacklisted")
                return await self._check_database(token_id)

        except BlacklistUnavailable:
            # Already reported honestly by the inner check; don't re-wrap.
            raise
        except Exception as e:
            logger.error(
                "blacklist_check_unavailable",
                token_id=token_id,
                store="redis" if self._redis_available else "database",
                error=str(e),
                outcome="refused_revocation_status_unknown",
            )
            raise BlacklistUnavailable(
                f"Could not check revocation status for token {token_id}: {e}"
            ) from e

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
            True if blacklisted, False if definitively not blacklisted

        Raises:
            BlacklistUnavailable: if the database could not answer (#1792)

        Note:
            #1792 found TWO fail-closed-by-returning-True sites, not one. The
            issue cited only `is_blacklisted`'s outer handler; the live
            reproduction (200, 401, 401, 401, 401 through a bare TestClient)
            actually ran through THIS one, because `_redis_available` was
            False and the asyncpg session was bound to a dead event loop.
            Fixing only the cited site would have left the reproduced path
            still lying.

        Note (#1802): `session_scope()` draws from the global `db` singleton
        (services/database/connection.py), whose engine is bound to whatever
        event loop happened to be running the first time it was lazily
        initialized. A bare `TestClient` spins a fresh event loop per
        request, so from request 2 onward the pooled asyncpg connection
        belongs to a loop that no longer exists — "Task ... got Future ...
        attached to a different loop", then "asyncpg.InterfaceError: cannot
        perform operation: another operation is in progress". This method
        uses `session_scope_fresh()` instead: a per-call engine bound to
        whatever loop is CURRENTLY running (#442's documented manual opt-in
        for exactly this failure class — the same guard #1452 gave
        `RedisFactory.initialize` on the Redis side). The cost is a fresh
        engine per fallback check, which is acceptable here because this
        path only runs when Redis is unavailable (or never initialized);
        the Redis path remains the O(1) hot path unaffected by this change.
        """
        try:
            async with self.db_session_factory.session_scope_fresh() as session:
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
                "blacklist_check_unavailable",
                token_id=token_id,
                store="database",
                error=str(e),
                outcome="refused_revocation_status_unknown",
            )
            # Still fail closed — the request is refused. It is refused
            # honestly (503 "couldn't verify") instead of as a false
            # revocation claim (401 "Token has been revoked").
            raise BlacklistUnavailable(
                f"Could not check revocation status for token {token_id}: {e}"
            ) from e

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
