"""
Invite Token Service (#1344 — alpha-registration gate)

Generates and atomically consumes single-use invite tokens for account creation.
Validates TOKENS only — never tester identities (HOST owns the roster mapping
token -> identity in a gitignored file outside this DB; trust-zone separation
agreed with HOST/Arch 2026-07-03).

Token format: 24-char Crockford Base32 (excludes I/L/O/U to avoid visual
ambiguity when a tester reads or types a code), normalized to uppercase for
comparison so lowercase input still matches.

Atomicity (Arch, load-bearing): consume_invite_token() is a SINGLE conditional
UPDATE (`WHERE used_at IS NULL`), never a separate check-then-write. A
non-atomic pair has a TOCTOU race: two concurrent registrations presenting the
same token can both pass a validity check before either burns it, producing a
double-spend — exactly the "forwarded invite link creates extra accounts"
threat single-use tokens exist to prevent.
"""

import re
import secrets
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import InviteToken

# Crockford Base32 — excludes I, L, O, U (visual ambiguity with 1, 1, 0, V).
CROCKFORD_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
TOKEN_LENGTH = 24


def generate_invite_token() -> str:
    """A cryptographically random 24-char Crockford Base32 token."""
    return "".join(secrets.choice(CROCKFORD_ALPHABET) for _ in range(TOKEN_LENGTH))


def normalize_token(raw: str) -> str:
    """Uppercase + strip non-alphanumeric characters.

    Testers may type lowercase or a dash-formatted distribution copy
    (e.g. "abcd-efgh-..."); dashes/spaces are cosmetic only, never load-bearing.
    """
    return re.sub(r"[^0-9A-Z]", "", raw.strip().upper())


async def consume_invite_token(session: AsyncSession, raw_token: str, user_id: UUID) -> bool:
    """Atomically validate-and-consume a token. Returns True iff it was valid and unused.

    Call this INSIDE the same transaction as the user INSERT it gates (never a
    separate call/endpoint) — so a token burn and a failed account creation
    commit or roll back together, and a spent token can never outlive its account.
    """
    token = normalize_token(raw_token)
    if not token:
        return False
    result = await session.execute(
        update(InviteToken)
        .where(InviteToken.token == token, InviteToken.used_at.is_(None))
        .values(used_at=datetime.now(timezone.utc), used_by_user_id=user_id)
        .returning(InviteToken.token)
    )
    return result.scalar_one_or_none() is not None
