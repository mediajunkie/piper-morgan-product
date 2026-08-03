"""Slack-account linking service (#1466 — Slack user → Piper user principal mapping).

The mint-in-Piper/redeem-in-Slack handshake, ratified 2026-08-03 (Lead memo,
Arch ratification with three binding conditions, CXO flow spec): the
AUTHENTICATED side (a logged-in Piper user, from settings) mints a short-lived
6-digit code; the unauthenticated side (a Slack caller) redeems it with
``/link <code>``, proving control of both accounts. Slack never holds a Piper
credential.

Token idiom: third member of the single-use-token family. Redemption REUSES
the ``consume_invite_token`` atomic-UPDATE shape — a SINGLE conditional UPDATE
(``WHERE code = ? AND used_at IS NULL AND expires_at > now``), never
check-then-write (TOCTOU double-spend; see invite_token_service.py). The code
is user-BOUND at mint (redemption returns the minting user's id — the redeemer
never chooses the target account) and short-TTL, which are exactly
PasswordResetToken's two deliberate differences from identity-blind
invite_tokens — hence a sibling table (slack_link_codes), not a ``kind``
column on invite_tokens (whose documented trust-zone contract is "validates
TOKENS only, never identities").

Arch condition 1 (BINDING): a 6-digit code is ~20 bits redeemed over an
unauthenticated channel, so redemption attempts are BOUNDED — per
slack_user_id AND per slack_team_id within a rolling window, fail-closed
(a ledger error also declines). Every redemption call is counted, hit or miss.

Arch condition 2 (BINDING): a second redemption for an already-linked Slack
identity FAILS CLOSED — the UNIQUE(slack_user_id, slack_team_id) violation is
CAUGHT (savepoint + IntegrityError) and answered with the already-linked
outcome; never a silent no-op, never an owner overwrite (account-takeover
shape). Because the consume and the identity INSERT share the savepoint, a
conflicted redemption also leaves the code unspent — after an unlink, the same
still-fresh code redeems cleanly.

ADR-079: slack_identities is owner-bearing; every read here is owner-scoped
except ``resolve_slack_principal``, which is keyed by the Slack identity pair
and SELECTs owner_id — it IS the principal resolution the boundary exists for.
"""

import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import List, Optional
from urllib.parse import quote, urlencode
from uuid import UUID

from sqlalchemy import delete, func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import SlackIdentity, SlackLinkAttempt, SlackLinkCode

CODE_LENGTH = 6
CODE_TTL_MINUTES = 10

# Arch condition 1 bounds: 5 attempts / 10 min per Slack user (the ratified
# example); the per-team bound is wider so one guesser exhausting their own
# budget doesn't lock a whole workspace out, while still capping the team-wide
# online-guessing rate.
ATTEMPT_WINDOW_MINUTES = 10
MAX_ATTEMPTS_PER_SLACK_USER = 5
MAX_ATTEMPTS_PER_TEAM = 20

# Ledger hygiene: attempt rows older than this are opportunistically purged.
ATTEMPT_RETENTION_HOURS = 24

_MINT_COLLISION_RETRIES = 8

# Redemption outcomes
LINKED = "linked"
INVALID_CODE = "invalid_code"
ALREADY_LINKED = "already_linked"
RATE_LIMITED = "rate_limited"


@dataclass
class RedeemOutcome:
    status: str  # one of LINKED / INVALID_CODE / ALREADY_LINKED / RATE_LIMITED
    owner_id: Optional[UUID] = None


def generate_link_code() -> str:
    """A cryptographically random 6-digit code (zero-padded)."""
    return f"{secrets.randbelow(10 ** CODE_LENGTH):0{CODE_LENGTH}d}"


def normalize_code(raw: str) -> str:
    """Digits only — testers may paste with spaces/dashes; cosmetic, never load-bearing."""
    return "".join(c for c in (raw or "").strip() if c.isdigit())


def build_link_deep_url(
    slack_user_id: Optional[str] = None, slack_team_id: Optional[str] = None
) -> str:
    """Deep link to the settings link section (CXO §2 — a one-click path, not
    an instruction), carrying the caller's Slack context as opaque query params
    so post-login the section renders "Link this Slack account" with the code
    pre-minted. Degrades gracefully to the plain section link when the inbound
    surface didn't carry both ids.

    The params are not credentials and nothing is stored pre-link — everything
    here was already in the inbound Slack event (CXO §2 / Arch Q3).
    """
    base = os.getenv("PIPER_BASE_URL", "http://localhost:8001").rstrip("/")
    path = f"{base}/settings/integrations/slack"
    if slack_user_id and slack_team_id:
        params = urlencode(
            {"slack_user_id": slack_user_id, "slack_team_id": slack_team_id}, quote_via=quote
        )
        return f"{path}?{params}#link-slack"
    return f"{path}#link-slack"


async def mint_link_code(
    session: AsyncSession, owner_id: UUID, ttl_minutes: int = CODE_TTL_MINUTES
) -> tuple[str, datetime]:
    """Mint a fresh single-use link code bound to owner_id.

    One outstanding code per user (a re-mint supersedes); expired codes and
    stale attempt-ledger rows are purged opportunistically. Retries on the
    (rare, ~outstanding/10^6) natural-key collision.
    """
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=ttl_minutes)

    # Opportunistic hygiene — keeps the 6-digit code space effectively empty.
    await session.execute(delete(SlackLinkCode).where(SlackLinkCode.expires_at <= now))
    # One outstanding code per user: a re-mint supersedes prior codes (owner-scoped).
    await session.execute(delete(SlackLinkCode).where(SlackLinkCode.user_id == owner_id))
    await session.execute(
        delete(SlackLinkAttempt).where(
            SlackLinkAttempt.attempted_at < now - timedelta(hours=ATTEMPT_RETENTION_HOURS)
        )
    )

    for _ in range(_MINT_COLLISION_RETRIES):
        code = generate_link_code()
        try:
            async with session.begin_nested():
                session.add(SlackLinkCode(code=code, user_id=owner_id, expires_at=expires_at))
                await session.flush()
            return code, expires_at
        except IntegrityError:
            continue  # active-code collision — draw again
    raise RuntimeError("could not mint a unique link code")  # pragma: no cover


async def redeem_link_code(
    session: AsyncSession, raw_code: str, slack_user_id: str, slack_team_id: str
) -> RedeemOutcome:
    """Atomically redeem a link code for a Slack identity, writing the mapping.

    Order is load-bearing:
    1. Identity present? Both ids required — else invalid (fail-closed).
    2. Rate limit FIRST (Arch condition 1): record this attempt, then bound the
       windowed count per slack_user_id AND per slack_team_id. Fail-closed —
       a ledger error declines rather than proceeding unmetered.
    3. Consume + link inside ONE savepoint: the consume is the invite-token
       atomic-UPDATE idiom; the identity INSERT hits
       UNIQUE(slack_user_id, slack_team_id) if already linked, which is CAUGHT
       and answered (Arch condition 2) — and the shared savepoint un-burns the
       code so it survives an unlink-then-retry within its TTL.

    The caller commits (the attempt row must persist even on a miss).
    """
    if not slack_user_id or not slack_team_id:
        return RedeemOutcome(INVALID_CODE)

    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=ATTEMPT_WINDOW_MINUTES)

    # -- Arch condition 1: bounded attempts, fail-closed --
    try:
        session.add(
            SlackLinkAttempt(
                slack_user_id=slack_user_id, slack_team_id=slack_team_id, attempted_at=now
            )
        )
        await session.flush()
        user_attempts = await session.scalar(
            select(func.count())
            .select_from(SlackLinkAttempt)
            .where(
                SlackLinkAttempt.slack_user_id == slack_user_id,
                SlackLinkAttempt.attempted_at >= window_start,
            )
        )
        team_attempts = await session.scalar(
            select(func.count())
            .select_from(SlackLinkAttempt)
            .where(
                SlackLinkAttempt.slack_team_id == slack_team_id,
                SlackLinkAttempt.attempted_at >= window_start,
            )
        )
    except Exception:
        # Fail-closed: if we cannot meter, we do not redeem.
        return RedeemOutcome(RATE_LIMITED)

    # Counts include the attempt just recorded, so "> MAX" allows exactly MAX
    # attempts per window.
    if user_attempts > MAX_ATTEMPTS_PER_SLACK_USER or team_attempts > MAX_ATTEMPTS_PER_TEAM:
        return RedeemOutcome(RATE_LIMITED)

    code = normalize_code(raw_code)
    if len(code) != CODE_LENGTH:
        return RedeemOutcome(INVALID_CODE)

    # -- consume + link, one savepoint --
    try:
        async with session.begin_nested():
            result = await session.execute(
                update(SlackLinkCode)
                .where(
                    SlackLinkCode.code == code,
                    SlackLinkCode.used_at.is_(None),
                    SlackLinkCode.expires_at > now,
                )
                .values(used_at=now)
                .returning(SlackLinkCode.user_id)
            )
            owner_id = result.scalar_one_or_none()
            if owner_id is None:
                return RedeemOutcome(INVALID_CODE)
            session.add(
                SlackIdentity(
                    owner_id=owner_id,
                    slack_user_id=slack_user_id,
                    slack_team_id=slack_team_id,
                    linked_at=now,
                )
            )
            await session.flush()
    except IntegrityError:
        # Arch condition 2: already-linked → fail-closed, honest, unlink-first.
        return RedeemOutcome(ALREADY_LINKED)

    return RedeemOutcome(LINKED, owner_id=owner_id)


async def resolve_slack_principal(
    session: AsyncSession, slack_user_id: str, slack_team_id: str
) -> Optional[UUID]:
    """Resolve a Slack identity to its Piper owner_id, or None (never a default).

    Keyed by the full (slack_user_id, slack_team_id) pair — the UNIQUE
    constraint guarantees at most one owner. This read is the principal
    resolution itself (ADR-079 note in the module docstring).
    """
    if not slack_user_id or not slack_team_id:
        return None
    result = await session.execute(
        select(SlackIdentity.owner_id).where(
            SlackIdentity.slack_user_id == slack_user_id,
            SlackIdentity.slack_team_id == slack_team_id,
        )
    )
    return result.scalar_one_or_none()


async def list_links_for_owner(session: AsyncSession, owner_id: UUID) -> List[SlackIdentity]:
    """Owner-scoped: the settings surface lists only the acting user's links."""
    result = await session.execute(
        select(SlackIdentity)
        .where(SlackIdentity.owner_id == owner_id)
        .order_by(SlackIdentity.linked_at)
    )
    return list(result.scalars().all())


async def unlink_slack_identity(
    session: AsyncSession, owner_id: UUID, slack_user_id: str, slack_team_id: str
) -> bool:
    """Owner-scoped unlink (the Arch-condition-2 unlink-first path).

    The owner_id predicate means a user can only ever unlink their OWN link —
    a well-formed request naming someone else's Slack identity deletes nothing.
    """
    result = await session.execute(
        delete(SlackIdentity).where(
            SlackIdentity.owner_id == owner_id,
            SlackIdentity.slack_user_id == slack_user_id,
            SlackIdentity.slack_team_id == slack_team_id,
        )
    )
    return bool(result.rowcount)
