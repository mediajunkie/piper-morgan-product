"""
Integration test fixtures and configuration.

These tests use REAL database connections with transaction rollback
for isolation. No mocking - tests verify actual system behavior.

Issue #292 - CORE-ALPHA-AUTH-INTEGRATION-TESTS
"""

from datetime import datetime, timezone
from uuid import UUID

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Mark all tests in integration/ as integration tests
pytestmark = pytest.mark.integration


def create_test_user_fn(session: AsyncSession):
    """
    Factory function to create a test user creator for a specific session.

    Returns a callable that creates users in the given session.
    Ensures FK constraints are satisfied for tests.
    """

    async def _create_user(user_id: str, username: str = None, email: str = None):
        """Create a test user with minimal required fields"""
        if username is None:
            username = f"test_user_{user_id[:8]}"
        if email is None:
            email = f"{username}@example.com"

        # Insert user directly using raw SQL
        # This bypasses any domain validation and ensures the user exists for FK constraints
        await session.execute(
            text(
                """
                INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                                   created_at, updated_at, role, is_alpha)
                VALUES (:id, :username, :email, '', true, false, :created_at, :updated_at, 'user', true)
                ON CONFLICT (id) DO NOTHING
            """
            ),
            {
                "id": user_id,
                "username": username,
                "email": email,
                "created_at": datetime.now(timezone.utc),
                "updated_at": datetime.now(timezone.utc),
            },
        )
        await session.flush()

    return _create_user


@pytest.fixture
async def create_test_user(integration_db: AsyncSession):
    """
    Fixture to create a test user in the database.

    Returns a callable that creates users with the given UUID.
    Ensures FK constraints are satisfied for tests.
    """
    return create_test_user_fn(integration_db)


@pytest.fixture(scope="session")
def integration_db_url():
    """Use test database for integration tests"""
    return "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def integration_db(integration_db_url):
    """
    Database connection with transaction rollback.

    Each test runs in a transaction that's rolled back after completion,
    ensuring complete test isolation without manual cleanup.

    Architecture Decision: Transaction rollback strategy
    - Fast and deterministic
    - No test pollution
    - Natural fit with FastAPI TestClient
    """
    engine = create_async_engine(integration_db_url)

    async with engine.begin() as conn:
        # Start a nested transaction
        async with conn.begin_nested() as transaction:
            # Create session factory
            async_session_factory = sessionmaker(conn, class_=AsyncSession, expire_on_commit=False)

            async with async_session_factory() as session:
                yield session

            # Rollback transaction (automatic cleanup)
            await transaction.rollback()

    await engine.dispose()


@pytest.fixture
async def real_client(integration_db):
    """
    HTTP client using real database.

    This client uses the actual application with real database connections,
    not mocked dependencies. Perfect for integration testing.

    Architecture Decision: Real sessions via database connection override
    - Overrides db.get_session() to use integration_db
    - Maintains transaction isolation
    - Tests actual production code paths
    """
    from services.database.connection import db
    from web.app import app

    # Store original get_session method
    original_get_session = db.get_session

    # Override db.get_session to return integration_db
    async def override_get_session():
        return integration_db

    db.get_session = override_get_session

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    # Restore original method after test
    db.get_session = original_get_session


@pytest.fixture
def test_client():
    """
    Synchronous HTTP test client for integration tests.

    Issue #590: Some integration tests use sync TestClient pattern.
    This fixture provides a simple sync client for API testing.

    Note: For tests requiring database isolation, use `real_client` instead.
    """
    from fastapi.testclient import TestClient

    from web.app import app

    with TestClient(app) as client:
        yield client
