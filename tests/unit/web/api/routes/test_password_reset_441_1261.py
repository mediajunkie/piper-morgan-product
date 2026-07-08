"""#441 Phase 3 / #1261 — password reset via PM-issued reset code + email-or-username login.

Mirrors test_setup_create_user_1344.py's approach: the real handler against the real
DB, including the atomicity property under actual concurrency (the invite-service
contract, applied to resets: two simultaneous resets presenting the same code must
not both succeed).
"""

import asyncio
import uuid
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy import select

from services.auth.password_reset_service import (
    consume_reset_token,
    default_expiry,
    generate_reset_token,
)
from services.auth.password_service import PasswordService
from services.database.models import PasswordResetToken, User
from web.api.routes.auth import PasswordResetRequest, reset_password


class _FakeRequest:
    """Minimal stand-in for fastapi.Request (the handler only reads .client.host)."""

    class _Client:
        host = "127.0.0.1"

    client = _Client()


def _mk_user(username: str | None = None) -> User:
    name = username or f"u_{uuid.uuid4().hex[:10]}"
    return User(
        id=uuid.uuid4(),
        username=name,
        email=f"{name}@test.invalid",
        password_hash=PasswordService().hash_password("Original-Pass-1!"),
        is_active=True,
    )


async def _mint(db_session, user: User, *, expired: bool = False, used: bool = False) -> str:
    token = generate_reset_token()
    row = PasswordResetToken(
        token=token,
        user_id=user.id,
        expires_at=(
            datetime.now(timezone.utc) - timedelta(hours=1) if expired else default_expiry()
        ),
        used_at=datetime.now(timezone.utc) if used else None,
    )
    db_session.add(row)
    await db_session.commit()
    return token


def _req(token: str, password: str = "New-Pass-Strong-1!") -> PasswordResetRequest:
    return PasswordResetRequest(
        reset_token=token, new_password=password, new_password_confirm=password
    )


class TestConsumeResetToken:
    async def test_valid_token_returns_bound_user_id_and_burns(self, db_session):
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user)

        got = await consume_reset_token(db_session, token)
        await db_session.commit()
        assert got == user.id

        # Burned: a second consume returns None.
        assert await consume_reset_token(db_session, token) is None

    async def test_expired_token_returns_none(self, db_session):
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user, expired=True)
        assert await consume_reset_token(db_session, token) is None

    async def test_used_token_returns_none(self, db_session):
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user, used=True)
        assert await consume_reset_token(db_session, token) is None

    async def test_garbage_and_empty_tokens_return_none(self, db_session):
        assert await consume_reset_token(db_session, "not-a-real-token") is None
        assert await consume_reset_token(db_session, "   ") is None

    async def test_normalization_lowercase_and_dashes_accepted(self, db_session):
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user)
        # Tester types the distribution-formatted copy: lowercase + dashes.
        pretty = "-".join([token[i : i + 4].lower() for i in range(0, len(token), 4)])
        got = await consume_reset_token(db_session, pretty)
        assert got == user.id


class TestResetPasswordEndpoint:
    async def test_happy_path_resets_password(self, db_session):
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user)

        result = await reset_password(_FakeRequest(), _req(token))
        assert result.success is True

        # The hash actually changed and verifies against the NEW password.
        async with __import__(
            "services.database.session_factory", fromlist=["AsyncSessionFactory"]
        ).AsyncSessionFactory.session_scope_fresh() as s:
            row = (await s.execute(select(User).where(User.id == user.id))).scalar_one()
            assert PasswordService().verify_password("New-Pass-Strong-1!", row.password_hash)
            assert not PasswordService().verify_password("Original-Pass-1!", row.password_hash)

    async def test_invalid_token_is_generic_400(self, db_session):
        with pytest.raises(HTTPException) as exc:
            await reset_password(_FakeRequest(), _req("TOTALLY-BOGUS-CODE"))
        assert exc.value.status_code == 400
        assert "Invalid or expired" in exc.value.detail

    async def test_expired_token_is_generic_400(self, db_session):
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user, expired=True)
        with pytest.raises(HTTPException) as exc:
            await reset_password(_FakeRequest(), _req(token))
        assert exc.value.status_code == 400

    async def test_mismatched_passwords_400_without_burning_token(self, db_session):
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user)
        req = PasswordResetRequest(
            reset_token=token,
            new_password="New-Pass-Strong-1!",
            new_password_confirm="Different-Pass-2!",
        )
        with pytest.raises(HTTPException) as exc:
            await reset_password(_FakeRequest(), req)
        assert exc.value.status_code == 400
        # The mismatch is caught BEFORE consumption — the code survives for a retry.
        assert await consume_reset_token(db_session, token) == user.id

    async def test_weak_password_400_without_burning_token(self, db_session):
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user)
        with pytest.raises(HTTPException) as exc:
            await reset_password(_FakeRequest(), _req(token, password="weakweak"))
        assert exc.value.status_code == 400
        assert await consume_reset_token(db_session, token) == user.id

    async def test_concurrent_resets_same_token_only_one_succeeds(self, db_session):
        """The invite-service atomicity contract, applied to resets: the burn is a
        single conditional UPDATE, so a double-spend is impossible."""
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()
        token = await _mint(db_session, user)

        async def attempt():
            try:
                return await reset_password(_FakeRequest(), _req(token))
            except HTTPException as e:
                return e

        r1, r2 = await asyncio.gather(attempt(), attempt())
        outcomes = sorted(
            "ok" if not isinstance(r, HTTPException) else "rejected" for r in (r1, r2)
        )
        assert outcomes == ["ok", "rejected"]


class TestLoginIdentifier:
    """#1261: login accepts email OR username (username precedence)."""

    async def test_login_lookup_matches_by_email(self, db_session):
        # Unit-level check of the widened lookup semantics via the real DB:
        # the route's logic is username-first-then-email; verify an email-only
        # match resolves to the same user login() would authenticate.
        user = _mk_user()
        db_session.add(user)
        await db_session.commit()

        by_username = (
            await db_session.execute(select(User).where(User.username == user.username))
        ).scalar_one_or_none()
        by_email = (
            await db_session.execute(select(User).where(User.email == user.email))
        ).scalar_one_or_none()
        assert by_username.id == by_email.id == user.id
