"""Who may connect the hosted MCP during the beta (#2242, option (a)).

xian's decision (10-31, via PPM): until the Claude connector is offered, only
xian's account and the cohort's named test accounts may connect the hosted MCP
(``piper-morgan-mcp``). Everyone else is refused, with a plain line on the
consent page.

Arch's mechanism (#2242, comments 6544299487 and 6545549190), built here:

* **One predicate, one list source.** :func:`may_connect_mcp` is the only
  question, and the list is a reserved key in ``users.preferences`` (the JSONB
  column both apps already read). There is no second copy per app, and no
  migration.
* **Checked at three points, all failing closed.** The consent/authorize step
  (``web/routers/mcp_oauth.py`` and :meth:`PiperMCPOAuthProvider.authorize`),
  the refresh grant (:meth:`PiperMCPOAuthProvider.exchange_refresh_token`, which
  refuses with ``invalid_grant``), and :meth:`MCPTokenVerifier.verify_token`
  (which returns ``None`` the way it does for a revoked token). The verifier
  check makes a removal bite on the next request and covers operator-minted
  tokens, which never pass through consent. Refresh tokens last 30 days, so
  the consent page alone would not close access.
* **Fail closed.** If the list cannot be read, the predicate says no and logs
  why. A connector going dark is better than an open one.
* **The flag never changes the user's own context.** ``user_context_service``
  merges top-level preferences into the model's context and branches on
  whether any exist; :func:`strip_reserved_keys` removes this key before that
  merge, so a listed account and an unlisted one with no other preferences
  get identical context (pinned).
* **Only the operator script writes the key.** ``scripts/mcp_allow.py`` is the
  one writer (``add`` / ``remove`` / ``list``; ``list`` re-reads after ``add``
  so the operator sees what stuck). An enforcement pin in
  ``tests/test_architecture_enforcement.py`` holds the literal to this module
  and write-shaped uses to the script, so a future preferences route that
  accepts a client dict cannot become a self-grant without the pin going red.
  Every other writer of ``preferences`` does a read-modify-write of the whole
  dict, so a racing user write can drop the flag; that loses in the closed
  direction, and ``mcp_allow.py list`` shows it.

The value is checked strictly: only JSON ``true`` lists an account. ``"true"``,
``1`` or any other truthy value does not, so a stray write from some other
path cannot list anyone by accident.

Pinned by ``tests/unit/services/mcp/server/test_mcp_allowlist_2242.py`` and
``tests/integration/test_mcp_allowlist_2242.py`` (the real read on Postgres).
"""

from __future__ import annotations

import enum
import uuid
from typing import Any, AsyncContextManager, Awaitable, Callable, Mapping

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger(__name__)

SessionScopeFactory = Callable[[], AsyncContextManager[AsyncSession]]
PreferencesReader = Callable[[uuid.UUID], Awaitable["Mapping[str, Any] | None"]]

# The reserved key in ``users.preferences``. This literal appears in production
# code ONLY here (enforcement pin, #2242); the one writer imports the name.
MCP_ALLOW_KEY = "mcp_connect_allowed"


class _Refusal(str, enum.Enum):
    """Named so refusals are grep-able in the log. Never surfaced to a caller."""

    BAD_USER_ID = "bad_user_id"
    NO_ROW = "no_row"
    NOT_LISTED = "not_listed"
    BACKEND_FAULT = "backend_fault"  # the list could not be read: refuse, never serve


async def read_preferences(
    user_id: uuid.UUID, *, session_scope: SessionScopeFactory | None = None
) -> Mapping[str, Any] | None:
    """The user's ``preferences`` dict, ``{}`` when the row has none, or
    ``None`` when there is no such row or the read failed.

    ``None`` is a refusal signal to :func:`may_connect_mcp`; an empty dict is a
    verified "nothing set", which is also a refusal, for a different logged
    reason. The ORM read is the same one ``user_context_service`` makes.
    """
    from sqlalchemy import select

    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory

    scope = session_scope or AsyncSessionFactory.session_scope
    async with scope() as session:
        row = (
            await session.execute(select(User.preferences).where(User.id == user_id))
        ).one_or_none()
    if row is None:
        return None
    return dict(row[0] or {})


async def may_connect_mcp(
    user_id: object,
    *,
    session_scope: SessionScopeFactory | None = None,
    reader: PreferencesReader | None = None,
) -> bool:
    """``True`` only when ``users.preferences[MCP_ALLOW_KEY]`` is JSON ``true``
    for this account. Everything else, including a failed read, is ``False``
    and logged with its reason.

    ``reader`` is injectable so unit tests can supply a dict-backed read (the
    ``users`` table cannot be created on the in-memory SQLite the MCP tests
    use); the default reads the real table through ``session_scope``.
    """
    try:
        parsed = uuid.UUID(str(user_id))
    except (ValueError, TypeError, AttributeError):
        logger.warning("mcp_allowlist_refused", reason=_Refusal.BAD_USER_ID.value)
        return False

    try:
        if reader is not None:
            prefs = await reader(parsed)
        else:
            prefs = await read_preferences(parsed, session_scope=session_scope)
    except (
        Exception
    ) as e:  # silent-ok: LOGGED; fail-closed by construction (Arch's point 4 on #2242)
        logger.error(
            "mcp_allowlist_refused",
            reason=_Refusal.BACKEND_FAULT.value,
            user_id=str(parsed),
            error=type(e).__name__,
        )
        return False

    if prefs is None:
        logger.warning("mcp_allowlist_refused", reason=_Refusal.NO_ROW.value, user_id=str(parsed))
        return False
    if prefs.get(MCP_ALLOW_KEY) is True:
        return True
    logger.warning("mcp_allowlist_refused", reason=_Refusal.NOT_LISTED.value, user_id=str(parsed))
    return False


def strip_reserved_keys(prefs: Mapping[str, Any] | None) -> dict[str, Any]:
    """A copy of ``prefs`` without the allowlist key.

    Called before ``user_context_service`` merges preferences into the model's
    context, so being listed changes nothing the user (or the model) sees: an
    account whose only preference is this key reads as having none.
    """
    if not prefs:
        return {}
    return {k: v for k, v in prefs.items() if k != MCP_ALLOW_KEY}
