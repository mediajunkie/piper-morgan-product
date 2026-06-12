"""
AAXT (Automated Agent-Experience Testing) fixtures.

These tests hit the REAL app with REAL services and evaluate quality
via LLM-as-judge using our Colleague Test rubric.

Issue: #929 AAXT Golden Scenarios
Requires: AAXT_ENABLED=true (skipped by default for cost control)
"""

import json
import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4

import httpx
import pytest
from httpx import ASGITransport
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

AAXT_ENABLED = os.getenv("AAXT_ENABLED", "false").lower() == "true"
AAXT_JUDGE_MODEL = os.getenv("AAXT_JUDGE_MODEL", "claude-sonnet-4-6")

E2E_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


def pytest_collection_modifyitems(config, items):
    """Skip all AAXT tests unless AAXT_ENABLED=true."""
    if not AAXT_ENABLED:
        skip = pytest.mark.skip(reason="AAXT_ENABLED not set (cost control)")
        for item in items:
            if "aaxt" in item.nodeid:
                item.add_marker(skip)


@pytest.fixture(scope="module")
async def aaxt_db_session():
    """Database session for AAXT tests."""
    engine = create_async_engine(E2E_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await engine.dispose()


@pytest.fixture(scope="module")
async def aaxt_test_user(aaxt_db_session):
    """Create a test user for AAXT scenarios. Cleaned up after module."""
    from services.auth.password_service import PasswordService

    user_id = str(uuid4())
    username = f"aaxt_test_{user_id[:8]}"
    password = "testpass123"

    ps = PasswordService()
    password_hash = ps.hash_password(password)

    await aaxt_db_session.execute(
        text(
            "INSERT INTO users (id, username, email, password_hash, is_active, is_verified, "
            "created_at, updated_at, role, is_alpha) "
            "VALUES (:id, :username, :email, :password_hash, true, true, :now, :now, 'user', true)"
        ),
        {
            "id": user_id,
            "username": username,
            "email": f"{username}@test.example.com",
            "password_hash": password_hash,
            "now": datetime.now(timezone.utc),
        },
    )
    await aaxt_db_session.commit()

    yield user_id, username, password

    # Cleanup
    for table in ["todo_items", "items", "lists", "conversations", "projects", "users"]:
        try:
            if table == "users":
                await aaxt_db_session.execute(
                    text(f"DELETE FROM {table} WHERE id = :uid"), {"uid": user_id}
                )
            else:
                await aaxt_db_session.execute(
                    text(f"DELETE FROM {table} WHERE owner_id = CAST(:uid AS uuid)"),
                    {"uid": user_id},
                )
        except Exception:
            pass
    await aaxt_db_session.commit()


@pytest.fixture(scope="module")
async def aaxt_client():
    """ASGI-backed HTTP client with full app lifespan."""
    from web.app import app

    @asynccontextmanager
    async def lifespan_wrapper():
        async with app.router.lifespan_context(app):
            yield

    async with lifespan_wrapper():
        transport = ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.fixture(scope="module")
async def aaxt_auth(aaxt_client, aaxt_test_user):
    """Login and return auth cookies."""
    _, username, password = aaxt_test_user
    resp = await aaxt_client.post("/api/v1/auth/login", data={"username": username, "password": password})
    assert resp.status_code == 200, f"AAXT login failed: {resp.text}"
    return {"cookies": resp.cookies}


@pytest.fixture(scope="module")
def judge_client():
    """LLM client for quality judging."""
    try:
        from anthropic import Anthropic

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            return Anthropic(api_key=api_key)
    except ImportError:
        pass
    pytest.skip("No Anthropic client for AAXT judge")
