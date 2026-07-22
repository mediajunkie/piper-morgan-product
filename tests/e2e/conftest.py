"""
Shared fixtures for E2E (end-to-end) HTTP tests.

E2E tests hit REAL HTTP endpoints with REAL services and REAL database.
No mocking of business logic — only database session isolation via cleanup.

Pattern (from #490 onboarding E2E):
1. Create test user directly in database (committed so app can see it)
2. Boot real FastAPI app with lifespan via ASGI transport
3. Hit real endpoints, assert real responses
4. Clean up test data after each test

Requirements:
- PostgreSQL running on port 5433 (docker compose up -d)
- Database migrations current (alembic upgrade head)
- No external API keys required for core flows

Issue: #352 TEST-SMOKE-E2E
"""

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4

import httpx
import pytest
from httpx import ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Database URL — same as production app uses locally
E2E_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def e2e_db_session():
    """
    Create database session for E2E tests.

    Commits are real (so the app's separate connection can see them),
    but tests clean up after themselves in teardown.
    """
    engine = create_async_engine(E2E_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def e2e_test_user(e2e_db_session):
    """
    Create a test user with NO projects.

    Returns (user_id, username, password) tuple.
    Cleans up the user (and any projects) after the test.
    """
    from services.auth.password_service import PasswordService

    user_id = str(uuid4())
    username = f"e2e_test_{user_id[:8]}"
    email = f"{username}@test.example.com"
    password = "testpass123"

    ps = PasswordService()
    password_hash = ps.hash_password(password)

    await e2e_db_session.execute(
        text(
            """
            INSERT INTO users (id, username, email, password_hash, is_active, is_verified,
                               created_at, updated_at, role, is_alpha)
            VALUES (:id, :username, :email, :password_hash, true, true, :now, :now, 'user', true)
        """
        ),
        {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": password_hash,
            "now": datetime.now(timezone.utc),
        },
    )
    await e2e_db_session.commit()

    yield user_id, username, password

    # Cleanup: remove dependent rows in FK order, then user.
    # #927/#963: todo_items.owner_id → users.id (direct FK, not through lists)
    # Must delete todo_items by owner_id BEFORE deleting user.
    await e2e_db_session.execute(
        text("DELETE FROM todo_items WHERE owner_id = CAST(:uid AS uuid)"),
        {"uid": user_id},
    )
    await e2e_db_session.execute(
        text(
            "DELETE FROM items WHERE list_id IN "
            "(SELECT id FROM lists WHERE owner_id = CAST(:uid AS uuid))"
        ),
        {"uid": user_id},
    )
    await e2e_db_session.execute(
        text("DELETE FROM items WHERE id NOT IN (SELECT id FROM todo_items)"),
    )
    await e2e_db_session.execute(
        text("DELETE FROM lists WHERE owner_id = CAST(:uid AS uuid)"),
        {"uid": user_id},
    )
    from tests.conftest import delete_test_user_fully

    await delete_test_user_fully(e2e_db_session, user_id)


@pytest.fixture
async def e2e_client():
    """
    HTTP client backed by the REAL FastAPI app with full lifespan.

    Boots the real app with all middleware, routes, services, and database
    connections exactly as production. Uses ASGI transport (in-process,
    no actual network call needed).
    """
    from web.app import app

    @asynccontextmanager
    async def lifespan_wrapper():
        async with app.router.lifespan_context(app):
            yield

    async with lifespan_wrapper():
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.fixture
async def e2e_auth_headers(e2e_client, e2e_test_user):
    """
    Convenience fixture: login and return auth cookies/headers.

    Returns a dict with 'cookies' key for use in subsequent requests.
    """
    _, username, password = e2e_test_user

    login_response = await e2e_client.post(
        "/api/v1/auth/login",
        data={"username": username, "password": password},
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"

    yield {"cookies": login_response.cookies}
