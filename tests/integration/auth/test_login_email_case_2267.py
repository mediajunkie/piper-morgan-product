"""#2267 (PA's served repro, 11-06 10:57): signing in with an email whose case differs
from the stored one got a 401, and the 401 said "Your session may have expired",
the sentence for an expired session, not a wrong credential.

Real database, real login route and the real app's 401 handler (the
test_auth_integration.py idiom: committed users, cascade-deleted at teardown).
"""

from uuid import uuid4

import pytest

from services.auth.password_service import PasswordService
from services.database.models import User
from web.api.routes.auth import BAD_CREDENTIALS_DETAIL

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"
_PASSWORD = "TestPass123!"


@pytest.fixture
async def db_session():
    from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
    from sqlalchemy.orm import sessionmaker

    engine = create_async_engine(_DB_URL)
    maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with maker() as session:
        yield session
    await engine.dispose()


@pytest.fixture
async def user(db_session):
    from tests.conftest import delete_test_user_fully

    uid = uuid4().hex[:8]
    row = User(
        username=f"case2267_{uid}",
        email=f"case2267_{uid}@example.com",
        password_hash=PasswordService().hash_password(_PASSWORD),
    )
    db_session.add(row)
    await db_session.commit()
    await db_session.refresh(row)
    yield row
    await delete_test_user_fully(db_session, row.id)
    await db_session.commit()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_an_email_in_another_case_signs_in(real_client, user):
    mixed = user.email[0].upper() + user.email[1:].replace("example.com", "Example.COM")
    assert mixed != user.email
    response = await real_client.post(
        "/api/v1/auth/login", data={"username": mixed, "password": _PASSWORD}
    )
    assert response.status_code == 200, response.text


@pytest.mark.integration
@pytest.mark.asyncio
async def test_a_wrong_password_says_so_not_session_expired(real_client, user):
    response = await real_client.post(
        "/api/v1/auth/login", data={"username": user.email, "password": "wrong-one"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == BAD_CREDENTIALS_DETAIL
    assert "expired" not in response.text


@pytest.mark.integration
@pytest.mark.asyncio
async def test_an_unknown_email_gets_the_same_line(real_client):
    response = await real_client.post(
        "/api/v1/auth/login",
        data={"username": f"nobody_{uuid4().hex[:8]}@example.com", "password": _PASSWORD},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == BAD_CREDENTIALS_DETAIL


@pytest.mark.asyncio
async def test_any_other_401_keeps_the_expired_session_sentence():
    """The app's own HTTPException handler: only the login's line is kept."""
    import json

    from fastapi import HTTPException
    from starlette.requests import Request

    from web.app import app

    handler = app.exception_handlers[HTTPException]
    request = Request({"type": "http", "method": "GET", "path": "/x", "headers": []})
    generic = await handler(request, HTTPException(status_code=401, detail="Not authenticated"))
    login = await handler(request, HTTPException(status_code=401, detail=BAD_CREDENTIALS_DETAIL))
    assert json.loads(generic.body)["detail"] == (
        "Let's try logging in again. Your session may have expired."
    )
    assert json.loads(login.body)["detail"] == BAD_CREDENTIALS_DETAIL
