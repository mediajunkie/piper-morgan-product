"""
Database Connection Management
Handles PostgreSQL connections using asyncpg and SQLAlchemy
"""

import os
from typing import Optional

import structlog
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

# Load environment variables from .env file
load_dotenv()

logger = structlog.get_logger()

# Base class for all models
Base = declarative_base()


class DatabaseConnection:
    """Manages database connections and sessions"""

    def __init__(self):
        self.engine = None
        self.async_session = None
        self._initialized = False

    async def initialize(self):
        """Initialize database connection"""
        if self._initialized:
            return

        # Build connection URL from environment
        db_url = self._build_database_url()

        # Create async engine with test-friendly settings (PM-058 optimized)
        self.engine = create_async_engine(
            db_url,
            echo=os.getenv("APP_DEBUG", "false").lower() == "true",
            pool_size=10,  # PM-058: Increased for better concurrent test handling
            max_overflow=20,  # PM-058: Increased buffer for batch test execution
            pool_pre_ping=False,  # Disable ping to avoid event loop conflicts
            pool_recycle=3600,  # Recycle connections every hour to prevent stale connections
            pool_timeout=30,  # PM-058: Add timeout to prevent hanging on pool exhaustion
        )

        # Create session factory
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

        self._initialized = True
        logger.info("Database connection initialized")

    def _build_database_url(self) -> str:
        """Build PostgreSQL URL from environment variables with SSL support

        SSL Configuration (Issue #229 CORE-USERS-PROD):
        - POSTGRES_SSL_MODE: disable (dev), prefer (staging), require/verify-full (production)
        - POSTGRES_SSL_ROOT_CERT: Path to CA certificate (for verify-ca, verify-full)
        - POSTGRES_SSL_CERT: Path to client certificate (optional)
        - POSTGRES_SSL_KEY: Path to client key (optional)
        """
        # #1278: honor an explicit DATABASE_URL first (Fly-attach/12-factor),
        # normalized for asyncpg — the global engine served localhost defaults
        # on Fly while session_factory (fixed first) worked, splitting the app
        # into half-connected. ONE convention, both engines.
        explicit = os.getenv("DATABASE_URL")
        if explicit:
            from services.database.session_factory import _normalize_pg_url

            return _normalize_pg_url(explicit, driver="async")

        user = os.getenv("POSTGRES_USER", "piper")
        password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5433")
        database = os.getenv("POSTGRES_DB", "piper_morgan")

        # Build base URL
        base_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"

        # Add SSL parameters if configured (Issue #229)
        ssl_params = []
        ssl_mode = os.getenv("POSTGRES_SSL_MODE", "prefer")  # Default: prefer SSL if available

        # Add SSL mode
        ssl_params.append(f"ssl={ssl_mode}")

        # Add SSL certificate paths if provided
        ssl_root_cert = os.getenv("POSTGRES_SSL_ROOT_CERT")
        if ssl_root_cert:
            ssl_params.append(f"sslrootcert={ssl_root_cert}")

        ssl_cert = os.getenv("POSTGRES_SSL_CERT")
        if ssl_cert:
            ssl_params.append(f"sslcert={ssl_cert}")

        ssl_key = os.getenv("POSTGRES_SSL_KEY")
        if ssl_key:
            ssl_params.append(f"sslkey={ssl_key}")

        # Combine URL with SSL parameters
        if ssl_params:
            url = f"{base_url}?{'&'.join(ssl_params)}"
            logger.debug("Database URL built with SSL configuration", ssl_mode=ssl_mode)
            return url

        return base_url

    async def create_tables(self):
        """Create all tables in the database"""
        if not self._initialized:
            await self.initialize()

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Database tables created")

    async def get_session(self) -> AsyncSession:
        """Get a new database session"""
        if not self._initialized:
            await self.initialize()

        return self.async_session()

    async def close(self):
        """Close database connection"""
        if self.engine:
            try:
                # Close all connections in the pool gracefully
                await self.engine.dispose()
                self._initialized = False
                logger.info("Database connection closed")
            except Exception as e:
                # Log but don't raise errors during cleanup
                logger.warning(f"Error during database cleanup: {e}")
                self._initialized = False


# Global database connection
db = DatabaseConnection()
