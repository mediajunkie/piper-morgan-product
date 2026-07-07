"""Password-reset token service (#441 Phase 3 / #1261 — beta password recovery).

The beta auth model's equivalent of email-based reset: the product has no mailer,
so PM/HOST mint a reset code on request (scripts/mint_password_reset_token.py)
and hand it to the tester over the same channel that already distributes #1344
invite codes. Faithful sibling of invite_token_service.py — same Crockford
format (I/L/O/U excluded for readability), same normalization, and the same
load-bearing atomicity rule: consumption is a SINGLE conditional UPDATE
(`WHERE used_at IS NULL AND expires_at > now`), never check-then-write, so two
concurrent resets presenting the same token cannot both succeed (TOCTOU
double-spend — see invite_token_service.py's docstring for the full argument).

Two deliberate differences from invites: a reset token is BOUND to a user at
mint time (consumption returns that user_id — the caller never chooses the
target account), and it EXPIRES (default 72h).
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.invite_token_service import (
    CROCKFORD_ALPHABET,
    TOKEN_LENGTH,
    normalize_token,
)
from services.database.models import PasswordResetToken

DEFAULT_TTL_HOURS = 72


def generate_reset_token() -> str:
    """A cryptographically random 24-char Crockford Base32 token (invite format)."""
    import secrets

    return "".join(secrets.choice(CROCKFORD_ALPHABET) for _ in range(TOKEN_LENGTH))


def default_expiry(now: Optional[datetime] = None) -> datetime:
    return (now or datetime.now(timezone.utc)) + timedelta(hours=DEFAULT_TTL_HOURS)


async def consume_reset_token(session: AsyncSession, raw_token: str) -> Optional[UUID]:
    """Atomically validate-and-consume a reset token.

    Returns the bound user_id iff the token was valid, unused, AND unexpired —
    else None. Call this INSIDE the same transaction as the password-hash
    UPDATE it authorizes, so a burned token and a failed password write commit
    or roll back together (the invite-service atomicity contract, applied to
    resets).
    """
    token = normalize_token(raw_token)
    if not token:
        return None
    now = datetime.now(timezone.utc)
    result = await session.execute(
        update(PasswordResetToken)
        .where(
            PasswordResetToken.token == token,
            PasswordResetToken.used_at.is_(None),
            PasswordResetToken.expires_at > now,
        )
        .values(used_at=now)
        .returning(PasswordResetToken.user_id)
    )
    return result.scalar_one_or_none()
