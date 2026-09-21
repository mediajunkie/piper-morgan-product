"""
Tests for JWT Token Blacklist

Tests the blacklist implementation for secure token revocation.
Covers TokenBlacklist operations, JWT service integration, and middleware enforcement.

Test Coverage:
- Blacklist operations (add, check, cleanup)
- JWT service integration (validate with blacklist, revoke)
- Middleware exception handling
- Security fail-closed behavior
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from services.auth.jwt_service import (
    BlacklistUnavailable,
    JWTService,
    TokenExpired,
    TokenInvalid,
    TokenRevoked,
)
from services.auth.token_blacklist import TokenBlacklist

# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture(scope="function")
def mock_redis():
    """Mock Redis client for testing with stateful blacklist"""
    redis = AsyncMock()
    redis.ping = AsyncMock(return_value=True)
    redis.setex = AsyncMock(return_value=True)
    redis.close = AsyncMock()

    # Use a dictionary to track blacklisted tokens
    blacklisted_tokens = set()

    async def mock_setex(key, ttl, value):
        blacklisted_tokens.add(key)
        return True

    async def mock_exists(key):
        return 1 if key in blacklisted_tokens else 0

    redis.setex = mock_setex
    redis.exists = mock_exists

    return redis


@pytest.fixture(scope="function")
def mock_redis_factory(mock_redis):
    """Mock RedisFactory for testing"""
    factory = MagicMock()

    # Ensure create_client returns the SAME mock_redis instance each time
    # (with shared stateful blacklisted_tokens set)
    async def create_client():
        return mock_redis

    factory.create_client = create_client
    return factory


@pytest.fixture(scope="function")
def mock_db_session_factory():
    """Mock database session factory.

    #1808: initialize() now SEEDS Redis from the DB (session_scope_fresh +
    an async execute whose result iterates), and add() write-throughs to the
    DB first — the mock supports both with an empty table by default.
    """
    factory = MagicMock()

    session = MagicMock()
    empty_result = MagicMock()
    empty_result.scalars.return_value = []
    empty_result.rowcount = 0

    async def _execute(*a, **k):
        return empty_result

    session.execute = _execute
    session.add = MagicMock()

    async def _commit():
        return None

    session.commit = _commit

    scope = MagicMock()

    async def _aenter(*a, **k):
        return session

    async def _aexit(*a, **k):
        return False

    scope.__aenter__ = _aenter
    scope.__aexit__ = _aexit
    factory.session_scope_fresh.return_value = scope
    factory.session_scope.return_value = scope
    factory._session = session  # test hook
    return factory


@pytest.fixture(scope="function")
async def blacklist(mock_redis_factory, mock_db_session_factory):
    """Create TokenBlacklist instance for testing"""
    bl = TokenBlacklist(mock_redis_factory, mock_db_session_factory)
    await bl.initialize()
    return bl


@pytest.fixture
def jwt_service(blacklist):
    """Create JWT service with blacklist for testing"""
    return JWTService(
        secret_key="test-secret-key",
        blacklist=blacklist,
    )


# ============================================================================
# Test TokenBlacklist Operations
# ============================================================================


@pytest.mark.asyncio
@pytest.mark.integration  # Skip conftest auto-mock of is_blacklisted
class TestTokenBlacklistOperations:
    """Test token blacklist basic operations"""

    @pytest.mark.smoke
    async def test_initialize_with_redis_available(
        self, mock_redis_factory, mock_db_session_factory
    ):
        """Should initialize with Redis when available"""
        bl = TokenBlacklist(mock_redis_factory, mock_db_session_factory)
        await bl.initialize()

        assert bl._redis_available is True

    @pytest.mark.smoke
    async def test_initialize_with_redis_unavailable(
        self, mock_redis_factory, mock_db_session_factory
    ):
        """Should fallback to database when Redis unavailable"""
        # Make Redis fail
        mock_redis_factory.create_client = AsyncMock(
            side_effect=Exception("Redis connection failed")
        )

        bl = TokenBlacklist(mock_redis_factory, mock_db_session_factory)
        await bl.initialize()

        assert bl._redis_available is False

    @pytest.mark.smoke
    async def test_add_to_blacklist_redis(self, blacklist):
        """Should add token to Redis blacklist"""
        token_id = "test-token-123"
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        success = await blacklist.add(token_id=token_id, reason="logout", expires_at=expires_at)

        assert success is True

        # Verify token is now in blacklist
        is_blacklisted = await blacklist.is_blacklisted(token_id)
        assert is_blacklisted is True

    @pytest.mark.smoke
    async def test_add_expired_token_skipped(self, blacklist):
        """Should skip adding already-expired tokens"""
        token_id = "expired-token"
        expires_at = datetime.now(timezone.utc) - timedelta(hours=1)

        success = await blacklist.add(token_id=token_id, reason="logout", expires_at=expires_at)

        # Should return True (no-op for expired)
        assert success is True

    @pytest.mark.smoke
    async def test_is_blacklisted_true(self, blacklist):
        """Should detect blacklisted tokens"""
        token_id = "blacklisted-token"
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        # Add token to blacklist first
        await blacklist.add(token_id=token_id, reason="test", expires_at=expires_at)

        result = await blacklist.is_blacklisted(token_id)

        assert result is True

    @pytest.mark.smoke
    async def test_is_blacklisted_false(self, blacklist):
        """Should allow non-blacklisted tokens"""
        token_id = "valid-token"

        # Don't add to blacklist
        result = await blacklist.is_blacklisted(token_id)

        assert result is False

    @pytest.mark.smoke
    async def test_security_fail_closed_on_error(self, mock_redis_factory, mock_db_session_factory):
        """Should still fail closed on errors — now by RAISING, not returning True.

        #1792 changed the signal, not the posture. Returning `True` was
        indistinguishable from a real blacklist hit, so a store outage reported
        as "Token has been revoked" to every active user. `BlacklistUnavailable`
        refuses exactly as before while saying what is actually true.

        Fail-closed is asserted here as the ABSENCE of a `False` return: no
        caller can read this outcome as "not blacklisted, proceed".
        """
        # Mock db_session_factory.session_scope to raise an error when used.
        # #1802: `_check_database` now opens its session via
        # `session_scope_fresh()` (the #442 same-loop-safe opt-in), not
        # `session_scope()` — stub both so this test still exercises the
        # failure path regardless of which one production calls.
        failing_context = MagicMock()
        failing_context.__aenter__ = AsyncMock(side_effect=Exception("Database connection failed"))
        failing_context.__aexit__ = AsyncMock(return_value=False)

        mock_db_session_factory.session_scope = MagicMock(return_value=failing_context)
        mock_db_session_factory.session_scope_fresh = MagicMock(return_value=failing_context)

        bl = TokenBlacklist(mock_redis_factory, mock_db_session_factory)
        bl._redis_available = False  # Simulate no Redis

        with pytest.raises(BlacklistUnavailable):
            await bl.is_blacklisted("any-token")

    @pytest.mark.smoke
    async def test_remove_expired_cleans_db_even_in_redis_mode(self, blacklist):
        """#1808 AMENDMENT (was: Redis mode -> cleanup no-op): the DB is ALWAYS
        written now (write-through contract), so cleanup always runs against it;
        Redis entries still TTL-expire on their own. Should be no-op for Redis (auto-expires via TTL)"""
        count = await blacklist.remove_expired()
        assert count == 0


# ============================================================================
# Test JWT Service Integration
# ============================================================================


@pytest.mark.asyncio
@pytest.mark.integration  # Skip conftest auto-mock for blacklist integration tests
class TestJWTServiceIntegration:
    """Test blacklist integration with JWT service"""

    @pytest.mark.smoke
    async def test_validate_token_checks_blacklist(self, jwt_service, blacklist):
        """Should check blacklist during token validation"""
        # Create a valid token
        user_id = uuid4()  # Issue #262
        token = jwt_service.generate_access_token(
            user_id=user_id,
            user_email="user@example.com",
            scopes=["read", "write"],
        )

        # Initially valid (not blacklisted)
        claims = await jwt_service.validate_token(token)
        assert claims is not None
        assert claims.user_id == str(user_id)

        # Blacklist the token
        await jwt_service.revoke_token(token, reason="test")

        # Should now raise TokenRevoked
        with pytest.raises(TokenRevoked):
            await jwt_service.validate_token(token)

    @pytest.mark.smoke
    async def test_revoke_token_adds_to_blacklist(self, jwt_service):
        """Should add token to blacklist on revocation"""
        token = jwt_service.generate_access_token(
            user_id=uuid4(),  # Issue #262
            user_email="test@example.com",
            scopes=["read"],
        )

        # Revoke the token
        success = await jwt_service.revoke_token(token, reason="logout")
        assert success is True

        # Token should now be blacklisted
        with pytest.raises(TokenRevoked):
            await jwt_service.validate_token(token)

    @pytest.mark.smoke
    async def test_revoke_token_without_blacklist(self):
        """Should fail gracefully when blacklist not configured"""
        # Create service without blacklist
        service = JWTService(secret_key="test-key")

        token = service.generate_access_token(
            user_id=uuid4(),  # Issue #262
            user_email="test@example.com",
            scopes=["read"],
        )

        # Should return False (no blacklist configured)
        success = await service.revoke_token(token)
        assert success is False

    @pytest.mark.smoke
    async def test_validate_token_with_expired_signature(self, jwt_service):
        """Should raise TokenExpired for expired tokens"""
        # Create token with very short expiration
        service = JWTService(
            secret_key="test-secret-key",  # Same key as jwt_service fixture
            access_token_expire_minutes=-1,  # Already expired
        )

        token = service.generate_access_token(
            user_id=uuid4(),  # Issue #262
            user_email="test@example.com",
            scopes=["read"],
        )

        # Should raise TokenExpired
        with pytest.raises(TokenExpired):
            await service.validate_token(token)  # Use same service for validation

    @pytest.mark.smoke
    async def test_validate_token_with_invalid_token(self, jwt_service):
        """Should raise TokenInvalid for malformed tokens"""
        # Should raise TokenInvalid
        with pytest.raises(TokenInvalid):
            await jwt_service.validate_token("not-a-valid-token")


# ============================================================================
# Test Middleware Integration
# ============================================================================


@pytest.mark.asyncio
class TestMiddlewareIntegration:
    """Test middleware handling of token exceptions"""

    @pytest.mark.smoke
    async def test_middleware_rejects_revoked_token(self, jwt_service):
        """Should reject revoked tokens with 401"""
        # This would be tested with actual middleware
        # For now, we verify the exceptions are properly defined
        assert TokenRevoked is not None
        assert TokenExpired is not None
        assert TokenInvalid is not None

        # Verify exceptions can be raised and caught
        try:
            raise TokenRevoked("Token revoked")
        except TokenRevoked as e:
            assert "revoked" in str(e).lower()


# ============================================================================
# Test Edge Cases
# ============================================================================


@pytest.mark.asyncio
@pytest.mark.integration  # Skip conftest auto-mock for edge case tests
class TestEdgeCases:
    """Test edge cases and error handling"""

    @pytest.mark.smoke
    async def test_blacklist_token_without_jti(self, jwt_service):
        """Should handle tokens without JTI claim"""
        # This is a malformed scenario that shouldn't happen with our JWT service
        # but we test the error handling
        pass  # JWTService always adds JTI

    @pytest.mark.smoke
    async def test_concurrent_blacklist_operations(self, blacklist, mock_redis):
        """Should handle concurrent operations safely"""
        import asyncio

        token_ids = [f"token-{i}" for i in range(10)]
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)

        # Add multiple tokens concurrently
        tasks = [
            blacklist.add(token_id=tid, reason="test", expires_at=expires_at) for tid in token_ids
        ]

        results = await asyncio.gather(*tasks)

        # All should succeed
        assert all(results)

    @pytest.mark.smoke
    async def test_refresh_access_token_with_blacklist(self, jwt_service):
        """Should check blacklist when refreshing tokens"""
        # Create refresh token
        refresh_token = jwt_service.generate_refresh_token(
            user_id=uuid4(),  # Issue #262
            user_email="test@example.com",
        )

        # Should work initially
        new_token = await jwt_service.refresh_access_token(refresh_token)
        assert new_token is not None

        # Revoke refresh token
        await jwt_service.revoke_token(refresh_token, reason="logout")

        # Should fail after revocation
        new_token = await jwt_service.refresh_access_token(refresh_token)
        assert new_token is None


# ============================================================================
# #1808 — the activation contract: DB is the record, Redis is a seeded
# write-through cache. These are the properties that make it SAFE to finally
# call initialize() (which was dead code — Redis configured, wired, never used).
# ============================================================================


def _db_factory_with_rows(rows):
    """A session factory whose seed query returns `rows` and which records
    every ORM add() (the write-through's durable half)."""
    factory = MagicMock()
    session = MagicMock()
    result = MagicMock()
    result.scalars.return_value = rows
    result.rowcount = 0

    async def _execute(*a, **k):
        return result

    session.execute = _execute
    session.added = []
    session.add = lambda entry: session.added.append(entry)

    async def _commit():
        return None

    session.commit = _commit

    scope = MagicMock()

    async def _aenter(*a, **k):
        return session

    async def _aexit(*a, **k):
        return False

    scope.__aenter__ = _aenter
    scope.__aexit__ = _aexit
    factory.session_scope_fresh.return_value = scope
    factory.session_scope.return_value = scope
    factory._session = session
    return factory


def _db_row(token_id, minutes_left=60):
    from datetime import timedelta

    from services.utils.datetime_utils import utc_now

    row = MagicMock()
    row.token_id = token_id
    row.reason = "logout"
    row.user_id = None
    row.expires_at = utc_now() + timedelta(minutes=minutes_left)
    row.created_at = utc_now()
    return row


@pytest.mark.asyncio
@pytest.mark.integration
class TestActivationContract1808:
    async def test_initialize_seeds_redis_from_unexpired_db_rows(
        self, mock_redis_factory, mock_redis
    ):
        """THE switch-on safety pin: a token revoked into the DB BEFORE this
        process started must be honored by Redis-mode reads — otherwise
        activating Redis un-revokes every historical revocation."""
        factory = _db_factory_with_rows([_db_row("historic-revocation-1")])
        bl = TokenBlacklist(mock_redis_factory, factory)
        await bl.initialize()

        assert bl._redis_available is True
        # The seeded entry is now visible on the Redis read path:
        assert await bl.is_blacklisted("historic-revocation-1") is True

    async def test_seed_failure_degrades_to_database_only(self, mock_redis_factory):
        """A Redis that couldn't be seeded must NOT serve reads — it silently
        lacks historical revocations. Database-only is slower, never wrong."""
        factory = MagicMock()
        scope = MagicMock()

        async def _aenter(*a, **k):
            raise RuntimeError("db unreachable during seed")

        async def _aexit(*a, **k):
            return False

        scope.__aenter__ = _aenter
        scope.__aexit__ = _aexit
        factory.session_scope_fresh.return_value = scope

        bl = TokenBlacklist(mock_redis_factory, factory)
        await bl.initialize()

        assert bl._redis_available is False
        assert bl._initialized is True

    async def test_add_writes_the_database_even_in_redis_mode(self, mock_redis_factory, mock_redis):
        """Write-through: the DB is the durable record. A Redis-era revocation
        must survive a restart into database-only mode (the flap hazard)."""
        from datetime import timedelta

        from services.utils.datetime_utils import utc_now

        factory = _db_factory_with_rows([])
        bl = TokenBlacklist(mock_redis_factory, factory)
        await bl.initialize()
        assert bl._redis_available is True

        ok = await bl.add("jti-flap", "logout", utc_now() + timedelta(hours=1))

        assert ok is True
        assert len(factory._session.added) == 1  # durable half
        assert await bl.is_blacklisted("jti-flap") is True  # cache half

    async def test_redis_write_failure_downgrades_but_revocation_stands(
        self, mock_redis_factory, mock_redis
    ):
        """A cache write that fails must not lose the revocation NOR leave a
        Redis in service that would report the token as valid."""
        from datetime import timedelta

        from services.utils.datetime_utils import utc_now

        factory = _db_factory_with_rows([])
        bl = TokenBlacklist(mock_redis_factory, factory)
        await bl.initialize()

        async def _boom(*a, **k):
            raise RuntimeError("redis died mid-write")

        mock_redis.setex = _boom

        ok = await bl.add("jti-degrade", "logout", utc_now() + timedelta(hours=1))

        assert ok is True  # the DB took it — the revocation IS recorded
        assert bl._redis_available is False  # and the lossy cache is out of service
        assert len(factory._session.added) == 1

    async def test_db_write_failure_fails_the_revocation_loudly(
        self, mock_redis_factory, mock_redis
    ):
        """The durable half is REQUIRED: no DB write, no success claim — a
        Redis-only revocation would silently evaporate on the next restart."""
        from datetime import timedelta

        from services.utils.datetime_utils import utc_now

        factory = _db_factory_with_rows([])

        async def _commit_boom():
            raise RuntimeError("db down")

        factory._session.commit = _commit_boom

        bl = TokenBlacklist(mock_redis_factory, factory)
        await bl.initialize()

        ok = await bl.add("jti-dbfail", "logout", utc_now() + timedelta(hours=1))
        assert ok is False


@pytest.mark.asyncio
class TestStartupPhase1808:
    async def test_phase_initializes_the_container_blacklist(self):
        from unittest.mock import patch

        from web.startup import TokenBlacklistInitPhase

        bl = AsyncMock()
        with patch("services.auth.container.AuthContainer.get_token_blacklist", return_value=bl):
            await TokenBlacklistInitPhase.startup(app=MagicMock())
        bl.initialize.assert_awaited_once()

    async def test_phase_never_raises(self):
        from unittest.mock import patch

        from web.startup import TokenBlacklistInitPhase

        with patch(
            "services.auth.container.AuthContainer.get_token_blacklist",
            side_effect=RuntimeError("container exploded"),
        ):
            await TokenBlacklistInitPhase.startup(app=MagicMock())  # must not raise

    def test_phase_is_in_the_startup_sequence(self):
        """The whole #1808 defect was a phase that EXISTED nowhere — pin its
        membership so it can't quietly fall out of the list."""
        from web.startup import StartupManager, TokenBlacklistInitPhase

        manager = StartupManager(app=MagicMock())
        assert TokenBlacklistInitPhase in manager.phases
