"""#2078: the setup wizard's per-user writes take their principal from the session.

Before this, ``/api/v1/setup/complete`` and ``/api/v1/setup/projects`` sat behind
the #1504 instance lockout and took a body ``user_id``. On any initialized server
(alpha since day one) the lockout refused every invited tester right after
``create-user`` had made the account, so the wizard ended in "Setup Failed" with
the key never stored. Arch's rule (2026-10-17): ``create-user`` signs the new
account in with the same cookie pair login sets; ``/complete`` and ``/projects``
require that session and write only for it; a body ``user_id`` that differs is
403, no session is 401; ``/slack-credentials`` (instance-wide) keeps the lockout.

Layers: the principal helper directly; the routes through the app's TestClient
(HTTP plumbing: cookie read, 401/403, nothing written); and the three handlers in
sequence against the real scratch database (create → complete → projects as the
new user, with the cookie create-user issued).
"""

from __future__ import annotations

import base64
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException, Request, Response
from fastapi.testclient import TestClient
from sqlalchemy import select

from services.auth.container import AuthContainer
from services.auth.invite_token_service import generate_invite_token
from services.database.models import InviteToken, ProjectDB, User
from web.api.routes import setup as setup_routes
from web.api.routes.setup import (
    CreateUserRequest,
    SetupCompleteRequest,
    SetupProjectRequest,
    _setup_principal,
    complete_setup,
    create_setup_project,
    create_user,
)
from web.app import app


def _claims(user_id: str):
    return SimpleNamespace(sub=user_id)


def _token_for(user_id: str) -> str:
    return AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.UUID(user_id), user_email="u2078@example.com", scopes=["user"]
    )


def _http_request() -> Request:
    return Request({"type": "http", "method": "POST", "headers": [], "scheme": "http", "path": "/"})


# ---------------------------------------------------------------- the rule itself


class TestPrincipalRule:
    def test_session_is_the_principal_when_body_is_silent(self):
        uid = str(uuid.uuid4())
        assert _setup_principal(_claims(uid), None) == uid

    def test_matching_body_user_id_is_accepted(self):
        uid = str(uuid.uuid4())
        assert _setup_principal(_claims(uid), uid) == uid

    def test_mismatched_body_user_id_is_refused_not_overridden(self):
        uid, other = str(uuid.uuid4()), str(uuid.uuid4())
        with pytest.raises(HTTPException) as exc:
            _setup_principal(_claims(uid), other)
        assert exc.value.status_code == 403


# ---------------------------------------------------------------- HTTP plumbing


@pytest.fixture(scope="module")
def client():
    return TestClient(app, follow_redirects=False)


class TestRoutesOverHttp:
    def test_complete_without_a_session_is_401(self, client):
        with patch.object(setup_routes, "AsyncSessionFactory") as factory:
            r = client.post("/api/v1/setup/complete", json={"anthropic_key": None})
        assert r.status_code == 401
        factory.session_scope_fresh.assert_not_called()

    def test_projects_without_a_session_is_401(self, client):
        with patch.object(setup_routes, "AsyncSessionFactory") as factory:
            r = client.post("/api/v1/setup/projects", json={"project_name": "Atlas"})
        assert r.status_code == 401
        factory.session_scope_fresh.assert_not_called()

    def test_complete_with_another_users_id_in_the_body_is_403_and_writes_nothing(self, client):
        me, other = str(uuid.uuid4()), str(uuid.uuid4())
        client.cookies.set("auth_token", _token_for(me))
        try:
            with patch.object(setup_routes, "AsyncSessionFactory") as factory:
                r = client.post(
                    "/api/v1/setup/complete",
                    json={"user_id": other, "anthropic_key": "sk-ant-not-stored"},
                )
        finally:
            client.cookies.delete("auth_token")
        assert r.status_code == 403
        factory.session_scope_fresh.assert_not_called()

    def test_projects_with_another_users_id_in_the_body_is_403_and_writes_nothing(self, client):
        me, other = str(uuid.uuid4()), str(uuid.uuid4())
        client.cookies.set("auth_token", _token_for(me))
        try:
            with patch.object(setup_routes, "AsyncSessionFactory") as factory:
                r = client.post(
                    "/api/v1/setup/projects", json={"user_id": other, "project_name": "Atlas"}
                )
        finally:
            client.cookies.delete("auth_token")
        assert r.status_code == 403
        factory.session_scope_fresh.assert_not_called()

    def test_slack_credentials_keeps_the_instance_lockout(self, client):
        with patch.object(
            setup_routes, "_completed_setup_exists", new=AsyncMock(return_value=True)
        ):
            r = client.post(
                "/api/v1/setup/slack-credentials",
                json={"client_id": "x", "client_secret": "y"},
            )
        assert r.status_code == 403


# ---------------------------------------------------------------- create-user signs in


class TestCreateUserIssuesTheSession:
    @pytest.mark.asyncio
    async def test_direct_call_without_request_sets_no_cookie(self, db_session):
        token = generate_invite_token()
        db_session.add(InviteToken(token=token))
        await db_session.commit()
        name = f"u2078_{uuid.uuid4().hex[:8]}"
        resp = await create_user(
            CreateUserRequest(
                username=name,
                email=f"{name}@test.invalid",
                password="A-fine-passw0rd!",
                password_confirm="A-fine-passw0rd!",
                invite_token=token,
            )
        )
        assert resp.success is True  # unchanged contract for direct callers

    @pytest.mark.asyncio
    async def test_http_call_sets_both_session_cookies_for_the_new_user(self, db_session):
        token = generate_invite_token()
        db_session.add(InviteToken(token=token))
        await db_session.commit()
        name = f"u2078_{uuid.uuid4().hex[:8]}"
        response = Response()
        resp = await create_user(
            CreateUserRequest(
                username=name,
                email=f"{name}@test.invalid",
                password="A-fine-passw0rd!",
                password_confirm="A-fine-passw0rd!",
                invite_token=token,
            ),
            _http_request(),
            response,
        )
        assert resp.success is True
        cookies = response.headers.getlist("set-cookie")
        names = {c.split("=", 1)[0] for c in cookies}
        assert names == {"auth_token", "refresh_token"}, cookies
        assert all("HttpOnly" in c for c in cookies)
        auth = next(c for c in cookies if c.startswith("auth_token="))
        jwt = auth.split("=", 1)[1].split(";", 1)[0]
        claims = await AuthContainer.get_jwt_service().validate_token(jwt)
        assert str(claims.sub) == resp.user_id


# ---------------------------------------------------------------- the wizard's own order


class TestWizardSequenceAsTheNewUser:
    @pytest.mark.asyncio
    async def test_create_then_complete_then_projects_as_the_new_user(
        self, db_session, monkeypatch
    ):
        """An initialized instance (the scratch DB already holds completed users
        from other tests, and this test doesn't care): create-user → complete →
        projects, every write for the new user only, in the wizard's own order."""
        monkeypatch.setenv("PIPER_CREDENTIAL_STORE", "db")
        # a valid 32-byte key, base64 (test fixture, not a secret)
        monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(b"2078" * 8).decode())
        token = generate_invite_token()
        db_session.add(InviteToken(token=token))
        await db_session.commit()
        name = f"u2078_{uuid.uuid4().hex[:8]}"
        response = Response()
        created = await create_user(
            CreateUserRequest(
                username=name,
                email=f"{name}@test.invalid",
                password="A-fine-passw0rd!",
                password_confirm="A-fine-passw0rd!",
                invite_token=token,
            ),
            _http_request(),
            response,
        )
        auth = next(
            c for c in response.headers.getlist("set-cookie") if c.startswith("auth_token=")
        )
        jwt = auth.split("=", 1)[1].split(";", 1)[0]
        claims = await AuthContainer.get_jwt_service().validate_token(jwt)

        # the wizard sends the user_id it was given; it matches the session
        done = await complete_setup(
            SetupCompleteRequest(user_id=created.user_id, default_llm_provider=None), claims
        )
        assert done.success is True
        assert done.redirect_url == "/"
        user = (
            await db_session.execute(select(User).where(User.id == uuid.UUID(created.user_id)))
        ).scalar_one()
        await db_session.refresh(user)
        assert user.setup_complete is True

        made = await create_setup_project(
            SetupProjectRequest(user_id=created.user_id, project_name="Atlas 2078"), claims
        )
        assert made.success is True
        project = (
            await db_session.execute(select(ProjectDB).where(ProjectDB.id == made.project_id))
        ).scalar_one()
        assert str(project.owner_id) == created.user_id
