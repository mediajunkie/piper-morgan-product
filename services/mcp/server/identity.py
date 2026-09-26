"""Piper Morgan MCP server — fail-closed caller identity (Phase C unit 1, #1462).

Companion docs: ``docs/internal/architecture/current/mcp/phase-c-build-plan-2026-09-25.md``
(unit 1) and ``phase-c-minimal-alpha-slice-2026-09-25.md`` (Arch's condition 1:
"no identity, no read; never default to anonymous"). Unit 0
(``services/mcp/server/app.py``) shipped with no identity resolver at all —
every MCP request was refused unconditionally. This module is what unit 0's
docstring named as its own replacement: a real bearer-token verifier backed
by the ``mcp_access_tokens`` table (operator-minted, hashed-at-rest, never
storing the raw token — see ``scripts/mint_mcp_token.py``).

Two properties are load-bearing and tested (``tests/unit/services/mcp/server/
test_identity_unit1.py``):

1. **No code path serves an MCP response with a default/anonymous identity.**
   Every failure mode of :meth:`MCPTokenVerifier.verify_token` — no such
   hash, revoked, expired — returns ``None``, identically. The SDK's own
   ``RequireAuthMiddleware`` (``mcp.server.auth.middleware.bearer_auth``)
   turns a ``None`` into a 401 before any resource handler runs; there is no
   branch in this module that resolves a missing/invalid token to a real
   user.
2. **Caller A can never produce caller B's identity.** ``client_id`` on the
   returned :class:`AccessToken` is sourced ONLY from the DB row the
   token's own hash matched — never from a header, a query parameter, or a
   default. :func:`current_user_id` reads that identity back out of the
   SDK's own request-scoped contextvar
   (``mcp.server.auth.middleware.auth_context.get_access_token``), which the
   SDK populates only after ``verify_token`` has already succeeded for THIS
   request — so a resource handler calling :func:`current_user_id` gets
   exactly the identity this request's own bearer resolved to, or an
   exception, never someone else's.
"""

from __future__ import annotations

import enum
import hashlib
from datetime import datetime, timezone
from typing import AsyncContextManager, Callable

import structlog
from mcp.server.auth.provider import AccessToken, TokenVerifier
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import MCPAccessToken
from services.database.session_factory import AsyncSessionFactory

SessionScopeFactory = Callable[[], AsyncContextManager[AsyncSession]]

logger = structlog.get_logger(__name__)

# The one scope every minted MCP token carries. Unit 1 ships resources-only
# (Arch's slice: zero tools) — a single scope is enough; a tool-bearing scope
# would be a unit-2+/condition-3 decision, not this one's to invent.
RESOURCE_READ_SCOPE = "resources:read"

TOKEN_PREFIX = "mcp_"


class _RefusalReason(str, enum.Enum):
    """Named so the one log line unit 1 emits on refusal is grep-able —
    never surfaced to the caller (the SDK's 401 body is identical for all
    three; see module docstring property 1)."""

    NOT_FOUND = "not_found"
    REVOKED = "revoked"
    EXPIRED = "expired"


def _hash(raw_token: str) -> str:
    """Same irreversible-hash convention as ``services/security/
    key_leak_detector.py``'s API-key comparison — SHA-256 hex digest."""
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def _as_aware_utc(value: datetime | None) -> datetime | None:
    """Normalize to a tz-aware UTC datetime.

    PostgreSQL's ``DateTime(timezone=True)`` round-trips tzinfo faithfully;
    SQLite (the in-memory DB the unit tests use — no ``TIMESTAMPTZ`` type)
    silently drops it on read-back, producing a naive datetime that raises
    ``TypeError`` when compared against an aware one. Every value this
    module ever WRITES is already UTC (``datetime.now(timezone.utc)``), so a
    naive value read back is safely re-attached to UTC, not guessed at.
    """
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def mask_token(raw_token: str) -> str:
    """``mcp_…WXYZ`` — safe to log or paste; never the raw token itself."""
    if len(raw_token) <= 4:
        return "…"
    return f"{TOKEN_PREFIX}…{raw_token[-4:]}"


class MCPTokenVerifier(TokenVerifier):
    """Resolves a bearer token to a real ``user_id``, or refuses.

    ``session_scope`` is injectable (defaults to
    :meth:`AsyncSessionFactory.session_scope`) so tests can supply an
    in-memory-SQLite-backed context manager without touching the real DB
    connection — see ``test_identity_unit1.py``.
    """

    def __init__(self, session_scope: SessionScopeFactory | None = None) -> None:
        self._session_scope: SessionScopeFactory = (
            session_scope or AsyncSessionFactory.session_scope
        )

    async def verify_token(self, token: str) -> AccessToken | None:
        token_hash = _hash(token)
        masked = mask_token(token)

        async with self._session_scope() as session:
            # ADR-079 D4/D6: this lookup RESOLVES the owner — user_id is the
            # OUTPUT of identity resolution here, not a known input to scope
            # by (same shape as D2a's "credential lookup without a known
            # principal yet"). token_hash is UNIQUE, so it's a single-row
            # lookup by the credential itself.
            row = (
                await session.execute(
                    select(MCPAccessToken).where(  # global-ok: resolves owner, see above
                        MCPAccessToken.token_hash == token_hash
                    )
                )
            ).scalar_one_or_none()

            if row is None:
                logger.warning(
                    "mcp_identity_refused", token=masked, reason=_RefusalReason.NOT_FOUND.value
                )
                return None

            now = datetime.now(timezone.utc)

            if row.revoked_at is not None:
                logger.warning(
                    "mcp_identity_refused", token=masked, reason=_RefusalReason.REVOKED.value
                )
                return None

            if (expires_at := _as_aware_utc(row.expires_at)) is not None and expires_at <= now:
                logger.warning(
                    "mcp_identity_refused", token=masked, reason=_RefusalReason.EXPIRED.value
                )
                return None

            # session_scope() commits on clean exit (#1193 contract) — no
            # explicit commit() needed here.
            await session.execute(
                update(MCPAccessToken).where(MCPAccessToken.id == row.id).values(last_used_at=now)
            )

            return AccessToken(
                token=token,
                client_id=str(row.user_id),
                scopes=[RESOURCE_READ_SCOPE],
            )


def current_user_id() -> str:
    """The verified caller's ``user_id`` for the CURRENT MCP request — and
    nothing else.

    Sourced ONLY from the SDK's own request-scoped :class:`AccessToken`
    (``mcp.server.auth.middleware.auth_context.get_access_token()``, set by
    ``AuthContextMiddleware`` after :class:`MCPTokenVerifier` has already
    resolved THIS request's bearer). Never a header, never a query
    parameter, never a default. Raises if called with no verified identity
    on the request context — that is a bug in whatever called it (a resource
    read should never execute without identity already having been enforced
    by ``RequireAuthMiddleware`` upstream), not a runtime condition to
    silently paper over.
    """
    from mcp.server.auth.middleware.auth_context import get_access_token

    access_token = get_access_token()
    if access_token is None:
        raise RuntimeError(
            "current_user_id() called with no verified MCP identity on the request "
            "context. There is no anonymous fallback — this indicates a resource "
            "handler ran without RequireAuthMiddleware's bearer check having "
            "succeeded first, which should be structurally impossible."
        )
    return access_token.client_id
