"""#1344 — create_user requires a valid, unused invite token (Arch's Gap-A closure).

The route previously had zero auth and zero app-layer gate (open registration since
the Jun 29 Caddy perimeter removal). These tests exercise the real handler against the
real DB — including the atomicity property under actual concurrency, since that's the
one non-negotiable requirement (Arch): two simultaneous registrations presenting the
same token must not both succeed.
"""

import asyncio
import uuid

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import select

from services.auth.invite_token_service import generate_invite_token
from services.database.models import InviteToken, User
from web.api.routes.setup import CreateUserRequest, create_user


def _req(token: str, username: str | None = None) -> CreateUserRequest:
    # Email is genuinely required as of #1348's fix (2026-07-07): the request
    # model now matches the DB's NOT NULL + unique constraint (and #1261 made
    # email a login identifier + the password-reset mint key).
    name = username or f"u_{uuid.uuid4().hex[:10]}"
    return CreateUserRequest(
        username=name,
        email=f"{name}@test.invalid",
        password="a-fine-password",
        password_confirm="a-fine-password",
        invite_token=token,
    )


@pytest.fixture
async def unused_token(db_session):
    token = generate_invite_token()
    db_session.add(InviteToken(token=token))
    await db_session.commit()
    return token


def test_invite_token_is_required_on_the_request_model():
    with pytest.raises(ValidationError):
        CreateUserRequest(
            username="someone",
            password="a-fine-password",
            password_confirm="a-fine-password",
        )


@pytest.mark.asyncio
async def test_valid_token_creates_user_and_burns_token(db_session, unused_token):
    resp = await create_user(_req(unused_token))

    assert resp.success is True
    row = (
        await db_session.execute(select(InviteToken).where(InviteToken.token == unused_token))
    ).scalar_one()
    assert row.used_at is not None
    assert str(row.used_by_user_id) == resp.user_id


@pytest.mark.asyncio
async def test_unknown_token_rejected_and_no_user_created(db_session):
    username = f"u_{uuid.uuid4().hex[:10]}"
    with pytest.raises(HTTPException) as exc_info:
        await create_user(_req("NOTAREALTOKEN0000000000", username=username))

    assert exc_info.value.status_code == 400
    row = (await db_session.execute(select(User).where(User.username == username))).scalar_one_or_none()
    assert row is None  # #1344: no orphaned account on a rejected token


@pytest.mark.asyncio
async def test_already_used_token_rejected_second_time(db_session, unused_token):
    first = await create_user(_req(unused_token, username=f"u_{uuid.uuid4().hex[:10]}"))
    assert first.success is True

    second_username = f"u_{uuid.uuid4().hex[:10]}"
    with pytest.raises(HTTPException) as exc_info:
        await create_user(_req(unused_token, username=second_username))

    assert exc_info.value.status_code == 400
    row = (
        await db_session.execute(select(User).where(User.username == second_username))
    ).scalar_one_or_none()
    assert row is None  # the second attempt created nothing


@pytest.mark.asyncio
async def test_concurrent_registrations_cannot_both_consume_the_same_token(db_session, unused_token):
    """The load-bearing property (Arch, 2026-07-03): a non-atomic check-then-burn lets two
    concurrent requests both pass validity before either burns the token (double-spend).
    Exactly one of these two simultaneous calls must succeed."""
    req_a = _req(unused_token, username=f"ua_{uuid.uuid4().hex[:10]}")
    req_b = _req(unused_token, username=f"ub_{uuid.uuid4().hex[:10]}")

    results = await asyncio.gather(create_user(req_a), create_user(req_b), return_exceptions=True)

    successes = [r for r in results if not isinstance(r, Exception)]
    failures = [r for r in results if isinstance(r, Exception)]
    assert len(successes) == 1, f"expected exactly one success, got: {results}"
    assert len(failures) == 1
    assert isinstance(failures[0], HTTPException) and failures[0].status_code == 400


# ---------------------------------------------------------------------------
# #1348 — email is required (matches the NOT NULL + unique DB constraint);
# duplicates name the right field. Fixed 2026-07-07.
# ---------------------------------------------------------------------------


def test_email_is_required_on_the_request_model_1348():
    """A missing email must be a clean 422 at the model layer — never a
    Postgres NotNullViolation leaking through as a confusing 500."""
    with pytest.raises(ValidationError):
        CreateUserRequest(
            username="someone",
            password="a-fine-password",
            password_confirm="a-fine-password",
            invite_token="SOMETOKEN",
        )


async def test_duplicate_email_400_names_the_email_field_1348(db_session, unused_token):
    """Two accounts, same email, different usernames → the 400 must blame the
    EMAIL (previously it said "Username 'x' already exists" for email dupes)."""
    from services.auth.invite_token_service import generate_invite_token

    email = f"dupe_{uuid.uuid4().hex[:8]}@test.invalid"
    first = CreateUserRequest(
        username=f"u_{uuid.uuid4().hex[:10]}",
        email=email,
        password="a-fine-password",
        password_confirm="a-fine-password",
        invite_token=unused_token,
    )
    await create_user(first)

    token2 = generate_invite_token()
    db_session.add(InviteToken(token=token2))
    await db_session.commit()
    second = CreateUserRequest(
        username=f"u_{uuid.uuid4().hex[:10]}",  # different username
        email=email,  # SAME email
        password="a-fine-password",
        password_confirm="a-fine-password",
        invite_token=token2,
    )
    with pytest.raises(HTTPException) as exc:
        await create_user(second)
    assert exc.value.status_code == 400
    assert "Email" in exc.value.detail
    assert email in exc.value.detail
