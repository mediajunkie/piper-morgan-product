"""#2342 (ADR-081 D3): the cutover's data step, from the classic GitHub OAuth App to the
published GitHub App.

Arch's rulings (issue 2342, 2026-11-11 19:09 and 19:23; mail 2026-11-12 06:51):

* it is a **script in xian's hand**, not an Alembic data migration: the deploy runs
  before the App's secrets exist, a schema migration has no business holding the
  network and a client secret, and a failed revoke must be countable without failing a
  deploy;
* it **selects by grant, not by status**: every stored GitHub grant that carries no App
  marker, whatever its binding says. So it still deletes and revokes for a binding the
  resolver already marked;
* for each one: **try the revoke** at GitHub with the classic app's credentials (a
  failure is counted and never blocks), mark the binding STALE with
  ``status_reason = cutover``, and **delete the token**;
* it never resurrects an unbound row, never touches a personal token (D4), and never
  touches ``connector_configs`` (the saved repository choices stay byte-identical);
* it is **idempotent**: a second run finds no markerless grant;
* **dry run by default**. Applying is refused unless App mode is on, because marking
  grants stale before there is an App to reconnect through would strand every account.

It prints and returns counts only. No token, login, email or name leaves this module.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

import structlog
from sqlalchemy import select

from services.connectors.binding_repository import ConnectorBindingRepository
from services.database.session_factory import AsyncSessionFactory
from services.mcp.consumer.connector import ConnectorStatusState
from services.mcp.consumer.connector_grant_store import ConnectorGrantStore, _provider
from services.mcp.consumer.github_app_grant import (
    REASON_CUTOVER,
    GrantRecordDamaged,
    app_mode,
    classify,
)

logger = structlog.get_logger(__name__)

_GITHUB = "github"

COUNT_KEYS = (
    "seen",
    "marked",
    "already_marked",
    "deleted",
    "revoke_ok",
    "revoke_failed",
    "app_grants",
    "unreadable",
)


class CutoverRefused(RuntimeError):
    """Applying the cutover was refused; the message says why. Nothing was changed."""


async def _grant_owner_ids() -> List[str]:
    """Every account id with a stored GitHub OAuth grant row. The seam tests patch."""
    from services.database.models import UserAPIKey

    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(
            select(UserAPIKey.user_id).where(
                UserAPIKey.provider == _provider(_GITHUB),
                UserAPIKey.is_active == True,  # noqa: E712
            )
        )
        return [str(row[0]) for row in result.all()]


async def _read_grant(owner_id: str) -> Optional[str]:
    async with AsyncSessionFactory.session_scope() as session:
        return await ConnectorGrantStore().get_encrypted_strict(session, owner_id, _GITHUB)


def _classic_handler():
    from services.mcp.consumer.github_oauth_handler import GitHubOAuthHandler

    return GitHubOAuthHandler(classic=True)


async def run_cutover(*, apply: bool = False) -> Dict[str, int]:
    """One pass over every stored GitHub grant. See the module docstring.

    Counts: ``seen`` (markerless grants found), ``marked`` (bindings set STALE with
    ``cutover``; in a dry run, the ones that would be), ``already_marked``, ``deleted``
    (tokens removed), ``revoke_ok`` / ``revoke_failed`` (GitHub's answer; both zero in a
    dry run), ``app_grants`` (left alone), ``unreadable`` (a row that could not be read
    or is damaged: left alone, look at it by hand)."""
    if apply and not app_mode():
        raise CutoverRefused(
            "GitHub App mode is off (GITHUB_APP_CLIENT_ID and GITHUB_APP_CLIENT_SECRET are "
            "not both set). Applying now would leave every account with nothing to "
            "reconnect through. Nothing was changed."
        )
    counts = {key: 0 for key in COUNT_KEYS}
    handler = _classic_handler() if apply else None
    for owner_id in await _grant_owner_ids():
        try:
            raw = await _read_grant(owner_id)
            grant = classify(raw)
        except GrantRecordDamaged:
            counts["unreadable"] += 1
            continue
        except Exception as e:
            logger.warning("github_app_cutover_read_failed", error=type(e).__name__)
            counts["unreadable"] += 1
            continue
        if raw is None:
            continue  # the row went away since it was listed
        if grant is not None:
            counts["app_grants"] += 1
            continue
        counts["seen"] += 1
        if apply:
            # Revoke first: it needs the token, and after the delete nobody holds it.
            if handler is not None and await handler.revoke_grant(raw):
                counts["revoke_ok"] += 1
            else:
                counts["revoke_failed"] += 1
        async with AsyncSessionFactory.session_scope() as session:
            repo = ConnectorBindingRepository(session)
            row = await repo.get(owner_id, _GITHUB)
            if row is not None and row.status != ConnectorStatusState.UNBOUND.value:
                if (
                    row.status == ConnectorStatusState.STALE.value
                    and row.status_reason == REASON_CUTOVER
                ):
                    counts["already_marked"] += 1
                else:
                    counts["marked"] += 1
                    if apply:
                        await repo.set_status(
                            owner_id,
                            _GITHUB,
                            ConnectorStatusState.STALE.value,
                            reason=REASON_CUTOVER,
                        )
            if apply:
                # The mark is flushed above; the store's delete commits the session.
                if await ConnectorGrantStore().delete(session, owner_id, _GITHUB):
                    counts["deleted"] += 1
    logger.info("github_app_cutover_pass", applied=apply, **counts)
    return counts


def format_counts(counts: Dict[str, int], *, applied: bool, ran_at: Optional[str] = None) -> str:
    """The lines the script prints. Counts only, and the time the run finished (Arch
    2026-11-12 08:28: the apply prints when it ran, so the record shows it was the same
    sitting as the secrets)."""
    head = "APPLIED" if applied else "DRY RUN (nothing changed; pass --apply to change it)"
    when = ran_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [f"github app cutover: {head}", f"  ran at {when}"]
    labels = {
        "seen": "classic grants found",
        "marked": "bindings marked stale (cutover)" if applied else "bindings that would be marked",
        "already_marked": "bindings already marked",
        "deleted": "classic tokens deleted",
        "revoke_ok": "revoked at GitHub",
        "revoke_failed": "revoke failed (may stay valid at GitHub)",
        "app_grants": "GitHub App grants left alone",
        "unreadable": "rows that could not be read (left alone)",
    }
    for key in COUNT_KEYS:
        lines.append(f"  {labels[key]:<44} {counts.get(key, 0)}")
    return "\n".join(lines)
