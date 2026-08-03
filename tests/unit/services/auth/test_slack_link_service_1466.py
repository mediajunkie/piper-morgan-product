"""#1466 — Slack↔Piper link service: mint / redeem / resolve / unlink.

The load-bearing properties (Arch ratification 2026-08-03, three binding
conditions):
1. Bounded redemption attempts per slack_user_id AND per slack_team_id,
   fail-closed — a 6-digit code is ~20 bits over an unauthenticated channel.
2. Re-link of an already-linked Slack identity FAILS CLOSED — the unique
   constraint violation is caught and answered, never silent no-op, never
   owner overwrite.
3. Redemption reuses the consume_invite_token atomic-UPDATE idiom
   (WHERE code=? AND used_at IS NULL AND expires_at > now — never
   check-then-write).

DB-backed via the shared db_session fixture (real Postgres, port 5433 —
run `alembic upgrade head` first for l1466slack).
"""

import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import select

from services.auth.slack_link_service import (
    ALREADY_LINKED,
    CODE_LENGTH,
    INVALID_CODE,
    LINKED,
    MAX_ATTEMPTS_PER_SLACK_USER,
    MAX_ATTEMPTS_PER_TEAM,
    RATE_LIMITED,
    build_link_deep_url,
    generate_link_code,
    mint_link_code,
    normalize_code,
    redeem_link_code,
    resolve_slack_principal,
    unlink_slack_identity,
)
from services.database.models import SlackLinkCode, User


def _make_user() -> User:
    suffix = uuid.uuid4().hex[:8]
    return User(
        id=uuid.uuid4(), username=f"u_{suffix}", email=f"{suffix}@test.invalid", is_alpha=True
    )


def _slack_user() -> str:
    return f"U{uuid.uuid4().hex[:10].upper()}"


def _slack_team() -> str:
    return f"T{uuid.uuid4().hex[:10].upper()}"


# ---- generation / normalization ----


def test_generate_link_code_is_six_digits():
    for _ in range(20):
        code = generate_link_code()
        assert len(code) == CODE_LENGTH
        assert code.isdigit()  # zero-padded, never shorter


def test_normalize_code_strips_cosmetic_characters():
    assert normalize_code(" 123-456 ") == "123456"
    assert normalize_code("12 34 56") == "123456"
    assert normalize_code("") == ""
    assert normalize_code(None) == ""


# ---- deep link (CXO §2 — one-click path with opaque Slack context) ----


def test_build_link_deep_url_carries_opaque_slack_params():
    url = build_link_deep_url("U123ABC", "T999XYZ")
    assert "/settings/integrations/slack" in url
    assert "slack_user_id=U123ABC" in url
    assert "slack_team_id=T999XYZ" in url
    assert url.endswith("#link-slack")


def test_build_link_deep_url_degrades_gracefully_without_ids():
    url = build_link_deep_url(None, None)
    assert "/settings/integrations/slack" in url
    assert "slack_user_id" not in url
    assert url.endswith("#link-slack")


# ---- mint → redeem → resolve happy path (DB-backed) ----


@pytest.mark.asyncio
async def test_mint_redeem_resolve_happy_path(db_session):
    user = _make_user()
    db_session.add(user)
    await db_session.commit()

    code, expires_at = await mint_link_code(db_session, user.id)
    assert len(code) == CODE_LENGTH and code.isdigit()

    su, st = _slack_user(), _slack_team()
    outcome = await redeem_link_code(db_session, code, su, st)
    await db_session.commit()

    assert outcome.status == LINKED
    assert outcome.owner_id == user.id

    resolved = await resolve_slack_principal(db_session, su, st)
    assert resolved == user.id

    # The code is burned (single-use, atomic conditional UPDATE)
    row = (
        await db_session.execute(select(SlackLinkCode).where(SlackLinkCode.code == code))
    ).scalar_one_or_none()
    assert row is None or row.used_at is not None


@pytest.mark.asyncio
async def test_code_is_single_use(db_session):
    user = _make_user()
    db_session.add(user)
    await db_session.commit()

    code, _ = await mint_link_code(db_session, user.id)
    first = await redeem_link_code(db_session, code, _slack_user(), _slack_team())
    assert first.status == LINKED

    second = await redeem_link_code(db_session, code, _slack_user(), _slack_team())
    assert second.status == INVALID_CODE
    await db_session.commit()


@pytest.mark.asyncio
async def test_expired_code_declines(db_session):
    user = _make_user()
    db_session.add(user)
    await db_session.commit()

    code, _ = await mint_link_code(db_session, user.id, ttl_minutes=-1)  # born expired
    outcome = await redeem_link_code(db_session, code, _slack_user(), _slack_team())
    assert outcome.status == INVALID_CODE
    await db_session.commit()


@pytest.mark.asyncio
async def test_remint_supersedes_prior_code(db_session):
    """One outstanding code per user — a re-mint invalidates the previous one."""
    user = _make_user()
    db_session.add(user)
    await db_session.commit()

    first_code, _ = await mint_link_code(db_session, user.id)
    second_code, _ = await mint_link_code(db_session, user.id)

    stale = await redeem_link_code(db_session, first_code, _slack_user(), _slack_team())
    if first_code != second_code:  # (equal draws are possible in principle)
        assert stale.status == INVALID_CODE

    fresh = await redeem_link_code(db_session, second_code, _slack_user(), _slack_team())
    assert fresh.status == LINKED
    await db_session.commit()


# ---- Arch condition 2: re-link conflict fails CLOSED ----


@pytest.mark.asyncio
async def test_already_linked_identity_fails_closed_never_overwrites(db_session):
    user_a, user_b = _make_user(), _make_user()
    db_session.add_all([user_a, user_b])
    await db_session.commit()

    su, st = _slack_user(), _slack_team()

    code_a, _ = await mint_link_code(db_session, user_a.id)
    assert (await redeem_link_code(db_session, code_a, su, st)).status == LINKED
    await db_session.commit()

    # B tries to claim the SAME Slack identity with their own valid code.
    code_b, _ = await mint_link_code(db_session, user_b.id)
    outcome = await redeem_link_code(db_session, code_b, su, st)
    await db_session.commit()

    assert outcome.status == ALREADY_LINKED  # caught, answered — not ORM noise
    # Never owner overwrite: A still owns the identity.
    assert await resolve_slack_principal(db_session, su, st) == user_a.id

    # Unlink-first path works, and B's code survived the conflict (savepoint
    # un-burns it), so the retry within TTL redeems cleanly.
    assert await unlink_slack_identity(db_session, user_a.id, su, st) is True
    await db_session.commit()
    retry = await redeem_link_code(db_session, code_b, su, st)
    await db_session.commit()
    assert retry.status == LINKED
    assert await resolve_slack_principal(db_session, su, st) == user_b.id


# ---- two-workspace isolation ----


@pytest.mark.asyncio
async def test_two_workspace_isolation(db_session):
    """The same Slack user id in two workspaces resolves to two distinct owners."""
    user_a, user_b = _make_user(), _make_user()
    db_session.add_all([user_a, user_b])
    await db_session.commit()

    su = _slack_user()  # same U… id in both teams
    team_1, team_2 = _slack_team(), _slack_team()

    code_a, _ = await mint_link_code(db_session, user_a.id)
    assert (await redeem_link_code(db_session, code_a, su, team_1)).status == LINKED
    code_b, _ = await mint_link_code(db_session, user_b.id)
    assert (await redeem_link_code(db_session, code_b, su, team_2)).status == LINKED
    await db_session.commit()

    assert await resolve_slack_principal(db_session, su, team_1) == user_a.id
    assert await resolve_slack_principal(db_session, su, team_2) == user_b.id
    # An unlinked third workspace resolves to None — never a default owner.
    assert await resolve_slack_principal(db_session, su, _slack_team()) is None


# ---- Arch condition 1: bounded redemption attempts, fail-closed ----


@pytest.mark.asyncio
async def test_rate_limit_per_slack_user_exhaustion(db_session):
    su, st = _slack_user(), _slack_team()

    for _ in range(MAX_ATTEMPTS_PER_SLACK_USER):
        outcome = await redeem_link_code(db_session, "000000", su, st)
        assert outcome.status == INVALID_CODE  # metered, not yet bounded out

    exhausted = await redeem_link_code(db_session, "000000", su, st)
    assert exhausted.status == RATE_LIMITED
    await db_session.commit()


@pytest.mark.asyncio
async def test_rate_limit_per_team_exhaustion(db_session):
    """Distinct Slack users can't pool unlimited guesses against one team."""
    st = _slack_team()

    statuses = []
    for _ in range(MAX_ATTEMPTS_PER_TEAM + 1):
        outcome = await redeem_link_code(db_session, "000000", _slack_user(), st)
        statuses.append(outcome.status)
    await db_session.commit()

    assert statuses[-1] == RATE_LIMITED
    assert all(s == INVALID_CODE for s in statuses[:MAX_ATTEMPTS_PER_TEAM])


@pytest.mark.asyncio
async def test_rate_limited_caller_cannot_redeem_even_a_valid_code(db_session):
    user = _make_user()
    db_session.add(user)
    await db_session.commit()
    code, _ = await mint_link_code(db_session, user.id)

    su, st = _slack_user(), _slack_team()
    for _ in range(MAX_ATTEMPTS_PER_SLACK_USER):
        await redeem_link_code(db_session, "999999", su, st)

    outcome = await redeem_link_code(db_session, code, su, st)
    await db_session.commit()
    assert outcome.status == RATE_LIMITED
    assert await resolve_slack_principal(db_session, su, st) is None


@pytest.mark.asyncio
async def test_rate_limit_fails_closed_on_ledger_error():
    """If the attempt ledger cannot be written/read, redemption DECLINES —
    it never proceeds unmetered (Arch condition 1 fail-closed)."""
    session = MagicMock()
    session.add = MagicMock()
    session.flush = AsyncMock(side_effect=RuntimeError("ledger down"))

    outcome = await redeem_link_code(session, "123456", _slack_user(), _slack_team())
    assert outcome.status == RATE_LIMITED


@pytest.mark.asyncio
async def test_missing_identity_fields_decline(db_session):
    assert (await redeem_link_code(db_session, "123456", "", _slack_team())).status == INVALID_CODE
    assert (await redeem_link_code(db_session, "123456", _slack_user(), "")).status == INVALID_CODE


# ---- unlink is owner-scoped (ADR-079) ----


@pytest.mark.asyncio
async def test_unlink_is_owner_scoped(db_session):
    user_a, user_b = _make_user(), _make_user()
    db_session.add_all([user_a, user_b])
    await db_session.commit()

    su, st = _slack_user(), _slack_team()
    code, _ = await mint_link_code(db_session, user_a.id)
    assert (await redeem_link_code(db_session, code, su, st)).status == LINKED
    await db_session.commit()

    # B cannot unlink A's identity, however well-formed the request.
    assert await unlink_slack_identity(db_session, user_b.id, su, st) is False
    assert await resolve_slack_principal(db_session, su, st) == user_a.id

    assert await unlink_slack_identity(db_session, user_a.id, su, st) is True
    await db_session.commit()
    assert await resolve_slack_principal(db_session, su, st) is None
