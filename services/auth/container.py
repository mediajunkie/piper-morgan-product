"""
Authentication Service Container - Dependency Injection for Auth Services

Provides singleton instances of authentication-related services with proper
dependency injection for testing and configuration flexibility.

Issue: #258 CORE-AUTH-CONTAINER
"""

from typing import Optional

import structlog

from services.auth.jwt_service import JWTService
from services.auth.token_blacklist import TokenBlacklist
from services.cache.redis_factory import RedisFactory
from services.database.session_factory import AsyncSessionFactory

logger = structlog.get_logger(__name__)


class AuthContainer:
    """
    Dependency injection container for authentication services.

    Provides singleton instances to avoid multiple initializations and
    enable proper dependency injection for testing.

    Usage:
        # Get JWT service
        jwt_service = AuthContainer.get_jwt_service()

        # Get token blacklist
        blacklist = AuthContainer.get_token_blacklist()

        # Reset for testing
        AuthContainer.reset()

    #936 (May 9 2026): get_user_service / _user_service removed. UserService
    was dead code; never populated in production. See dev/2026/05/09/936-issue-audit.md.
    """

    _jwt_service: Optional[JWTService] = None
    _token_blacklist: Optional[TokenBlacklist] = None
    _initialized: bool = False

    @classmethod
    def get_jwt_service(cls) -> JWTService:
        """
        Get singleton JWT service instance.

        Returns:
            Configured JWTService instance
        """
        if cls._jwt_service is None:
            logger.info("Initializing JWT service singleton")

            # Get token blacklist for JWT service
            blacklist = cls.get_token_blacklist()

            # Create JWT service with defaults (reads from environment)
            # JWTService handles JWT_SECRET_KEY from env with secure fallback
            cls._jwt_service = JWTService(blacklist=blacklist)

            logger.info("JWT service singleton created")

        return cls._jwt_service

    @classmethod
    def get_token_blacklist(cls) -> TokenBlacklist:
        """
        Get singleton token blacklist instance.

        Returns:
            Configured TokenBlacklist instance
        """
        if cls._token_blacklist is None:
            logger.info("Initializing token blacklist singleton")

            # Create factories for Redis and database
            redis_factory = RedisFactory()
            db_session_factory = AsyncSessionFactory()

            # Create token blacklist with dual storage
            cls._token_blacklist = TokenBlacklist(
                redis_factory=redis_factory, db_session_factory=db_session_factory
            )

            logger.info("Token blacklist singleton created")

        return cls._token_blacklist

    @classmethod
    def is_initialized(cls) -> bool:
        """
        Check if container has been initialized.

        Returns:
            True if any service has been created
        """
        return cls._initialized or (
            cls._jwt_service is not None or cls._token_blacklist is not None
        )

    @classmethod
    def reset(cls) -> None:
        """
        Reset all singletons (FOR TESTING ONLY).

        This allows tests to create fresh service instances with mocked dependencies.
        """
        logger.warning("Resetting AuthContainer (testing mode)")

        cls._jwt_service = None
        cls._token_blacklist = None
        cls._initialized = False

        logger.info("AuthContainer reset complete")

    @classmethod
    def initialize(cls) -> None:
        """
        Eagerly initialize all services.

        Useful for application startup to catch configuration errors early.
        """
        if cls._initialized:
            logger.info("AuthContainer already initialized")
            return

        logger.info("Initializing AuthContainer eagerly")

        # Initialize all services
        cls.get_token_blacklist()
        cls.get_jwt_service()

        cls._initialized = True

        logger.info("AuthContainer initialization complete")


# Singleton instance for backward compatibility
auth_container = AuthContainer()
