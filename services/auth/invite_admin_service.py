"""Admin invite operations behind the Invites page (#2081).

HOST's security shape (memo 2026-10-18 07:27, recorded on the issue):

- Raw codes are returned ONCE by the mint call and never again by any read;
  they are never logged and never written to audit rows (masked forms only).
- N is bounded 1..20 per request and 20 per UTC day (a hijacked admin session
  cannot mint without limit).
- The list shows the masked form (``ABCD…WXYZ``), minted-at, used-at and the
  redeeming username; a REVOKED code (``used_at`` set, ``used_by_user_id``
  empty) is its own status, never shown as a redemption.
- Revoke closes the no-revoke gap: it is the same conditional write the
  wizard's consume uses (``WHERE used_at IS NULL``), keyed on the masked form
  because the page never holds the raw value; an ambiguous mask refuses.
- One audit row per mint and per revoke: actor, count, masked forms, time.

Trust zone (unchanged since #1344): this table knows TOKENS, never who a code
was for; HOST's roster keeps that.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, time, timezone
from typing import List, Optional, Sequence
from uuid import UUID

import structlog
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.auth.invite_token_service import generate_invite_token
from services.database.models import InviteToken, User

logger = structlog.get_logger()

MAX_PER_REQUEST = 20  # the mint script's bound, kept
MAX_PER_DAY = 20  # HOST's cap
_MASK_RE = re.compile(r"^[0-9A-Z]{4}…[0-9A-Z]{4}$")


# Issue 2432 (Arch, mail 01M87QXPZZ, decisions.log 2026-11-24 13:38): a refusal carries a
# CODE and, for the daily limit, its whole numbers. It carries no sentence. The route
# picks the line through ``invite_refusal_line`` (on the guard's closed picker list), so
# nothing built at run time can reach the admin's screen.
REFUSAL_MINT_COUNT = "mint_count_out_of_range"
REFUSAL_DAILY_LIMIT = "daily_limit"
REFUSAL_NOT_MASKED = "not_a_masked_code"
REFUSAL_NO_MATCH = "no_match"
REFUSAL_AMBIGUOUS = "more_than_one_match"
REFUSAL_ALREADY_REDEEMED = "already_redeemed"
REFUSAL_ALREADY_REVOKED = "already_revoked"
REFUSAL_USED_MEANWHILE = "used_meanwhile"


class InviteAdminError(ValueError):
    """A refusal: a code and a status. ``minted``, ``limit`` and ``left`` are whole
    numbers, set only for the daily limit."""

    def __init__(
        self, code: str, status_code: int = 400, *, minted: int = 0, limit: int = 0, left: int = 0
    ):
        super().__init__(code)
        self.code = code
        self.status_code = status_code
        self.minted = minted
        self.limit = limit
        self.left = left


# The lines an admin reads (CXO, mail 01M87RB23J, 2026-11-24). The first is built once at
# import from the limit it names. "Nothing was revoked" is true: each refusal is raised
# before the write.
INVITE_MINT_COUNT_LINE = "You can create between 1 and {max} invite codes at a time.".format(
    max=int(MAX_PER_REQUEST)
)
INVITE_DAILY_LIMIT_TEMPLATE = (
    "That would go past today's limit: {used} of {limit} invite codes created, {left} left."
)
INVITE_NOT_MASKED_LINE = (
    "That doesn't look like a masked invite code. It should look like ABCD…WXYZ."
)
INVITE_NO_MATCH_LINE = "No invite code matches that masked form."
INVITE_AMBIGUOUS_LINE = (
    "More than one unused code matches that masked form, so nothing was revoked."
)
INVITE_ALREADY_REDEEMED_LINE = "That code is already redeemed, so there is nothing to revoke."
INVITE_ALREADY_REVOKED_LINE = "That code is already revoked, so there is nothing to revoke."
INVITE_USED_MEANWHILE_LINE = "That code was used in the meantime, so nothing was revoked."


def invite_refusal_line(code: str) -> Optional[str]:
    """The line for a refusal code, or None for a code with no line (the refusal then
    answers its status line). The daily limit is not here: its line carries whole
    numbers and the route builds it from ``INVITE_DAILY_LIMIT_TEMPLATE``. A picker on the
    guard's closed list (``DETAIL_PICKERS``): every return is an UPPER_CASE constant or
    None."""
    if code == REFUSAL_MINT_COUNT:
        return INVITE_MINT_COUNT_LINE
    if code == REFUSAL_NOT_MASKED:
        return INVITE_NOT_MASKED_LINE
    if code == REFUSAL_NO_MATCH:
        return INVITE_NO_MATCH_LINE
    if code == REFUSAL_AMBIGUOUS:
        return INVITE_AMBIGUOUS_LINE
    if code == REFUSAL_ALREADY_REDEEMED:
        return INVITE_ALREADY_REDEEMED_LINE
    if code == REFUSAL_ALREADY_REVOKED:
        return INVITE_ALREADY_REVOKED_LINE
    if code == REFUSAL_USED_MEANWHILE:
        return INVITE_USED_MEANWHILE_LINE
    return None


def mask(token: str) -> str:
    """The masked form every memo and roster line uses: first four, last four."""
    t = token or ""
    if len(t) < 8:
        return "…"
    return f"{t[:4]}…{t[-4:]}"


@dataclass(frozen=True)
class InviteRow:
    masked: str
    created_at: Optional[datetime]
    used_at: Optional[datetime]
    used_by: Optional[str]
    status: str  # "unused" | "redeemed" | "revoked"


def _status_of(used_at: Optional[datetime], used_by_user_id) -> str:
    if used_at is None:
        return "unused"
    # HOST ruling 4: a revoke sets used_at with no redeemer; it must never read
    # as a redemption.
    return "redeemed" if used_by_user_id is not None else "revoked"


async def _write_audit(
    session: AsyncSession,
    *,
    actor_user_id: UUID,
    action: str,
    message: str,
    masked: Sequence[str],
) -> None:
    """One audit row through the shared ``AuditLogger`` (#249); masked forms
    only (HOST ruling 5). Best effort: a failed audit write is logged and never
    blocks the operation it describes."""
    from services.security.audit_logger import audit_logger

    try:
        await audit_logger.log_event(
            event_type="admin",
            action=action,
            status="success",
            severity="info",
            message=message,
            session=session,
            user_id=actor_user_id,
            resource_type="invite_token",
            details={"count": len(masked), "masked": list(masked)},
        )
    except Exception as exc:  # silent-ok: logged; the audit row must not undo the admin's act
        logger.error("invite_admin_audit_write_failed", action=action, error=str(exc))


async def minted_today(session: AsyncSession, now: Optional[datetime] = None) -> int:
    now = now or datetime.now(timezone.utc)
    day_start = datetime.combine(now.date(), time.min, tzinfo=timezone.utc)
    result = await session.execute(
        select(func.count()).select_from(InviteToken).where(InviteToken.created_at >= day_start)
    )
    return int(result.scalar_one() or 0)


async def mint_invites(session: AsyncSession, *, count: int, actor_user_id: UUID) -> List[str]:
    """Mint ``count`` codes. Returns the RAW codes, to be shown once. Never log them."""
    if not isinstance(count, int) or count < 1 or count > MAX_PER_REQUEST:
        raise InviteAdminError(REFUSAL_MINT_COUNT, 422)
    already = await minted_today(session)
    if already + count > MAX_PER_DAY:
        left = max(0, MAX_PER_DAY - already)
        raise InviteAdminError(
            REFUSAL_DAILY_LIMIT, 429, minted=already, limit=MAX_PER_DAY, left=left
        )
    raw: List[str] = []
    for _ in range(count):
        token = generate_invite_token()
        session.add(InviteToken(token=token))
        raw.append(token)
    await session.flush()
    masked = [mask(t) for t in raw]
    await _write_audit(
        session,
        actor_user_id=actor_user_id,
        action="invite_mint",
        message=f"Minted {count} invite code(s) from the Invites page.",
        masked=masked,
    )
    logger.info("invite_admin_minted", count=count, masked=masked, actor=str(actor_user_id))
    return raw


async def list_invites(session: AsyncSession) -> List[InviteRow]:
    result = await session.execute(
        select(
            InviteToken.token,
            InviteToken.created_at,
            InviteToken.used_at,
            InviteToken.used_by_user_id,
            User.username,
        )
        .join(User, User.id == InviteToken.used_by_user_id, isouter=True)
        .order_by(InviteToken.created_at.desc())
    )
    rows: List[InviteRow] = []
    for token, created_at, used_at, used_by_user_id, username in result.all():
        rows.append(
            InviteRow(
                masked=mask(token),
                created_at=created_at,
                used_at=used_at,
                used_by=username if used_by_user_id is not None else None,
                status=_status_of(used_at, used_by_user_id),
            )
        )
    return rows


async def revoke_invite(session: AsyncSession, *, masked: str, actor_user_id: UUID) -> str:
    """Revoke ONE unused code by its masked form. Refuses when the mask matches
    no unused code (404), more than one (409: ambiguous, say so), or only a
    code already redeemed (409)."""
    if not _MASK_RE.match(masked or ""):
        raise InviteAdminError(REFUSAL_NOT_MASKED, 422)
    head, tail = masked.split("…")
    result = await session.execute(
        select(InviteToken.token, InviteToken.used_at, InviteToken.used_by_user_id).where(
            InviteToken.token.like(f"{head}%{tail}")
        )
    )
    matches = [
        (t, u, b) for (t, u, b) in result.all() if len(t) >= 8 and t[:4] == head and t[-4:] == tail
    ]
    if not matches:
        raise InviteAdminError(REFUSAL_NO_MATCH, 404)
    unused = [t for (t, u, b) in matches if u is None]
    if len(unused) > 1:
        raise InviteAdminError(REFUSAL_AMBIGUOUS, 409)
    if not unused:
        status = _status_of(matches[0][1], matches[0][2])
        raise InviteAdminError(
            REFUSAL_ALREADY_REDEEMED if status == "redeemed" else REFUSAL_ALREADY_REVOKED, 409
        )
    token = unused[0]
    now = datetime.now(timezone.utc)
    done = await session.execute(
        update(InviteToken)
        .where(InviteToken.token == token, InviteToken.used_at.is_(None))
        .values(used_at=now, used_by_user_id=None)
    )
    if done.rowcount != 1:
        raise InviteAdminError(REFUSAL_USED_MEANWHILE, 409)
    await _write_audit(
        session,
        actor_user_id=actor_user_id,
        action="invite_revoke",
        message="Revoked one unused invite code from the Invites page.",
        masked=[masked],
    )
    logger.info("invite_admin_revoked", masked=masked, actor=str(actor_user_id))
    return masked
