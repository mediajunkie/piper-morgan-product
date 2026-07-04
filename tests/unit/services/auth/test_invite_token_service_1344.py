"""#1344 — invite token generation + atomic validate-and-consume.

Atomicity is the load-bearing property (Arch, 2026-07-03): consume_invite_token()
must be a single conditional UPDATE, never check-then-write, or a TOCTOU race lets
two concurrent registrations both burn the same token (double-spend).
"""

import uuid

import pytest
from sqlalchemy import select

from services.auth.invite_token_service import (
    CROCKFORD_ALPHABET,
    TOKEN_LENGTH,
    consume_invite_token,
    generate_invite_token,
    normalize_token,
)
from services.database.models import InviteToken, User


def _make_user() -> User:
    suffix = uuid.uuid4().hex[:8]
    return User(id=uuid.uuid4(), username=f"u_{suffix}", email=f"{suffix}@test.invalid", is_alpha=True)


# ---- generation ----


def test_generate_invite_token_shape():
    token = generate_invite_token()
    assert len(token) == TOKEN_LENGTH
    assert all(c in CROCKFORD_ALPHABET for c in token)


def test_generate_invite_token_excludes_ambiguous_characters():
    # Crockford Base32 excludes I, L, O, U for visual clarity.
    for c in "ILOU":
        assert c not in CROCKFORD_ALPHABET


def test_generate_invite_token_is_random():
    tokens = {generate_invite_token() for _ in range(50)}
    assert len(tokens) == 50  # no collisions in 50 draws


# ---- normalization ----


def test_normalize_token_uppercases():
    assert normalize_token("abcd1234efgh5678ijkl9012") == "ABCD1234EFGH5678IJKL9012"


def test_normalize_token_strips_dashes_and_whitespace():
    assert normalize_token("  ABCD-1234-EFGH-5678  ") == "ABCD1234EFGH5678"


def test_normalize_token_empty_stays_empty():
    assert normalize_token("   ") == ""


# ---- atomic consume (real DB, the load-bearing behavior) ----


@pytest.mark.asyncio
async def test_consume_valid_unused_token_succeeds(db_session):
    token = generate_invite_token()
    db_session.add(InviteToken(token=token))
    await db_session.commit()

    user = _make_user()
    db_session.add(user)  # uncommitted — same txn as the consume, mirrors create_user

    consumed = await consume_invite_token(db_session, token, user.id)
    await db_session.commit()

    assert consumed is True
    row = (
        await db_session.execute(select(InviteToken).where(InviteToken.token == token))
    ).scalar_one()
    assert row.used_at is not None
    assert row.used_by_user_id == user.id


@pytest.mark.asyncio
async def test_consume_already_used_token_fails(db_session):
    token = generate_invite_token()
    db_session.add(InviteToken(token=token))
    await db_session.commit()

    user1 = _make_user()
    db_session.add(user1)
    assert await consume_invite_token(db_session, token, user1.id) is True
    await db_session.commit()

    user2 = _make_user()
    db_session.add(user2)
    consumed_again = await consume_invite_token(db_session, token, user2.id)
    await db_session.rollback()  # mirrors create_user's failure path: no double-spend committed

    assert consumed_again is False


@pytest.mark.asyncio
async def test_consume_unknown_token_fails(db_session):
    user = _make_user()
    db_session.add(user)
    consumed = await consume_invite_token(db_session, "NOTAREALTOKEN000000000A", user.id)
    await db_session.rollback()
    assert consumed is False


@pytest.mark.asyncio
async def test_consume_accepts_lowercase_and_dash_formatted_input(db_session):
    token = generate_invite_token()
    db_session.add(InviteToken(token=token))
    await db_session.commit()

    user = _make_user()
    db_session.add(user)
    dashed = f"{token[:6]}-{token[6:12]}-{token[12:18]}-{token[18:]}".lower()

    consumed = await consume_invite_token(db_session, dashed, user.id)
    await db_session.commit()

    assert consumed is True


@pytest.mark.asyncio
async def test_consume_empty_token_fails_without_querying(db_session):
    user = _make_user()
    db_session.add(user)
    consumed = await consume_invite_token(db_session, "   ", user.id)
    await db_session.rollback()
    assert consumed is False
