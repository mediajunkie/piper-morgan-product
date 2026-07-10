"""
Async Session Factory
Provides standardized session management with automatic resource cleanup

Issue #442 Fix: Creates fresh engines per-request to avoid event loop mismatch.
The global `db` singleton may be initialized in a different event loop than
HTTP request handlers, causing "Future attached to a different loop" errors.
"""

import os
from contextlib import asynccontextmanager
from typing import AsyncContextManager, Optional, Tuple

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .connection import db


def _normalize_pg_url(url: str, *, driver: str) -> str:
    """Normalize an externally-supplied Postgres URL for our engines (#1278).

    Hosted platforms (Fly attach, Heroku-style) hand out ``postgres://`` —
    a scheme SQLAlchemy 2.x no longer aliases — often with ``?sslmode=``,
    which asyncpg rejects as a connect kwarg. Map the scheme onto the
    requested driver and translate/drop sslmode for the async driver
    (private-network defaults need no TLS; ``require``-class modes become
    asyncpg's ``ssl=true``).
    """
    for prefix in ("postgres://", "postgresql://", "postgresql+asyncpg://"):
        if url.startswith(prefix):
            url = ("postgresql://" if driver == "sync" else "postgresql+asyncpg://") + url[
                len(prefix) :
            ]
            break
    if driver == "async" and "sslmode=" in url:
        import re as _re

        mode = _re.search(r"[?&]sslmode=([a-z-]+)", url)
        url = _re.sub(r"[?&]sslmode=[a-z-]+", "", url)
        if mode and mode.group(1) in ("require", "verify-ca", "verify-full"):
            url += ("&" if "?" in url else "?") + "ssl=true"
        url = url.rstrip("?&").replace("?&", "?")
    return url


def _get_database_url() -> str:
    """Build PostgreSQL URL from environment variables.

    Duplicated from connection.py to avoid importing the global db instance
    for fresh engine creation.

    #1278: honors an explicit ``DATABASE_URL`` first (the Fly-attach/12-factor
    convention), normalized for asyncpg; else builds from ``POSTGRES_*`` with
    local-dev defaults preserved.
    """
    explicit = os.getenv("DATABASE_URL")
    if explicit:
        return _normalize_pg_url(explicit, driver="async")
    user = os.getenv("POSTGRES_USER", "piper")
    password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    database = os.getenv("POSTGRES_DB", "piper_morgan")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


def get_sync_migration_url() -> str:
    """The SYNC PostgreSQL URL for Alembic migrations, resolved from the ENVIRONMENT.

    #1299(a): alembic.ini hardcoded `...@localhost:5433`, so the in-container migrate
    connected to localhost:5433 (wrong — postgres is at `postgres:5432` there) and failed
    silently on every deploy (root cause of the hollow 0.8.8). `alembic/env.py` uses this
    so the migrate works in any context — container, local, CI.

    Mirrors ``_get_database_url`` but with alembic's SYNC driver (no ``+asyncpg``). Honors
    an explicit ``ALEMBIC_DATABASE_URL`` / ``DATABASE_URL`` override (async URLs normalized
    to sync); else builds from ``POSTGRES_*`` with the local-dev defaults (localhost:5433)
    PRESERVED so local dev is unaffected.
    """
    explicit = os.getenv("ALEMBIC_DATABASE_URL") or os.getenv("DATABASE_URL")
    if explicit:
        return _normalize_pg_url(explicit, driver="sync")  # #1278: postgres:// et al.
    user = os.getenv("POSTGRES_USER", "piper")
    password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    database = os.getenv("POSTGRES_DB", "piper_morgan")
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"


class AsyncSessionFactory:
    """Factory for creating async database sessions with automatic resource management

    Note on Event Loop Handling (#442):
        This factory provides two modes:
        1. Default: Uses global db singleton (fast, for normal app code)
        2. Fresh engine: Creates new engine per-request (for setup wizard endpoints
           where the global engine may be bound to a different event loop)

        Use session_scope_fresh() when you need to avoid event loop mismatch errors.
    """

    @staticmethod
    async def create_session() -> AsyncSession:
        """Create a new async session using global db singleton

        Returns:
            AsyncSession: New database session

        Note:
            Caller is responsible for closing the session.
            Prefer using session_scope() context manager for automatic cleanup.
            For setup endpoints, use session_scope_fresh() instead.
        """
        return await db.get_session()

    @staticmethod
    def _create_fresh_engine_and_session() -> Tuple[any, AsyncSession]:
        """Create a fresh engine and session bound to current event loop.

        Returns:
            Tuple of (engine, session) - caller must dispose engine after use.
        """
        engine = create_async_engine(
            _get_database_url(),
            echo=False,
            pool_pre_ping=False,  # Avoid event loop conflicts
            pool_size=1,  # Minimal pool for single-use
            max_overflow=0,
        )
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        return engine, session_factory()

    @staticmethod
    @asynccontextmanager
    async def session_scope() -> AsyncContextManager[AsyncSession]:
        """Context manager for automatic session lifecycle management.

        CONTRACT (#1193): COMMITS on clean exit; rolls back on exception. The
        docstring always promised "automatic commit" but the implementation
        never committed — so every write that relied on it was flushed and then
        silently discarded on close (silent write-loss; bit #1079 standup and
        #1143 composting independently, plus user corrections via
        web/api/routes/insights.py). A 133-call-site audit (2026-06-12,
        Arch-ratified Option A) confirmed zero callers depend on no-commit
        semantics, so behavior now conforms to the documented contract
        (Pattern-073: conform behavior to spec). Committing a read-only or
        already-committed session is a no-op, so existing correct callers are
        unaffected. Enforced by test_architecture_enforcement.py
        (TestSessionScopeCommitContract).

        Yields:
            AsyncSession: Database session with automatic commit and cleanup

        Example:
            async with AsyncSessionFactory.session_scope() as session:
                repo = ExampleRepository(session)
                result = await repo.operation()
                # Automatic commit and cleanup
        """
        session = await AsyncSessionFactory.create_session()
        try:
            yield session
            # #1193: honor the documented contract — commit on clean exit.
            await session.commit()
        except Exception:
            try:
                await session.rollback()
            except Exception:
                # Ignore rollback errors during cleanup
                pass
            raise
        finally:
            try:
                await session.close()
            except Exception:
                # Ignore close errors during cleanup
                pass

    @staticmethod
    @asynccontextmanager
    async def session_scope_fresh() -> AsyncContextManager[AsyncSession]:
        """Context manager that creates a fresh engine bound to current event loop.

        Use this for endpoints that may run in a different event loop than
        the app startup (e.g., setup wizard endpoints).

        Issue #442: Fixes "Future attached to a different loop" errors.

        Yields:
            AsyncSession: Database session with fresh engine

        Example:
            async with AsyncSessionFactory.session_scope_fresh() as session:
                # Safe to use even when global db was initialized in different loop
                await session.execute(text("SELECT 1"))
        """
        engine, session = AsyncSessionFactory._create_fresh_engine_and_session()
        try:
            yield session
        except Exception:
            try:
                await session.rollback()
            except Exception:
                pass
            raise
        finally:
            try:
                await session.close()
            except Exception:
                pass
            try:
                await engine.dispose()
            except Exception:
                pass

    @staticmethod
    @asynccontextmanager
    async def transaction_scope() -> AsyncContextManager[AsyncSession]:
        """Context manager for explicit transaction management

        Yields:
            AsyncSession: Database session within transaction context

        Example:
            async with AsyncSessionFactory.transaction_scope() as session:
                repo = ExampleRepository(session)
                await repo.operation()
                # Explicit transaction commit on success, rollback on exception
        """
        session = await AsyncSessionFactory.create_session()
        try:
            async with session.begin():
                yield session
        finally:
            try:
                await session.close()
            except Exception:
                # Ignore close errors during cleanup
                pass
