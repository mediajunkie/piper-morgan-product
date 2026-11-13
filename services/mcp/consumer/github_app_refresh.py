"""#2342 (ADR-081 D3): what the one GitHub credential resolver does with a stored grant in
App mode: serve it, refresh it first, or say why it can't be served.

Rulings this implements (Arch, issue 2342, 2026-11-11 19:09, 19:11, 19:23 and
2026-11-12 06:51):

* a grant **without the App marker never serves** in App mode. It is a classic grant by
  definition, so the verdict is ``cutover``;
* a **damaged** record is a read failure, never classic;
* a token with under five minutes left is **refreshed before serving**, and two
  concurrent requests **spend the refresh token once**: an in-process lock per owner,
  and on Postgres ``pg_advisory_xact_lock`` on a key namespaced to this use, taken in the
  transaction that re-reads the grant, refreshes only if it is still due, and writes the
  new pair;
* a **rejected** refresh re-reads the store once. A newer pair written by a concurrent
  request serves; otherwise the verdict is ``refresh_rejected``. The dead pair is left
  in the store;
* a refresh that **could not complete** (timeout, connection failure, 5xx, an
  unclassifiable answer) leaves the store exactly as it was. The current token serves
  if it has not actually expired; otherwise the verdict is unreachable;
* a **scoped** process (the MCP app: decrypt-only, #1982) never attempts a refresh. It
  can neither write the new pair nor hold the App's client secret;
* so the **main app refreshes in the background** (Arch 2026-11-12 06:52):
  ``background_refresh_pass`` runs every 30 minutes in App mode and refreshes every
  App-marked grant on a BOUND binding with under two hours left, under the same lock. A
  person who uses Piper only through the Claude connector then nearly always finds a
  live token in the MCP app.

The write is the LAST step under the lock: ``store_user_key`` commits inside the call
and ``pg_advisory_xact_lock`` releases at commit, so nothing after the write may assume
the lock is still held.

No token appears in any log line here.
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import time
from dataclasses import dataclass
from typing import Dict, Optional

import structlog
from sqlalchemy import select, text

from services.database.session_factory import AsyncSessionFactory
from services.infrastructure.logging.evidence import evidence  # noqa: E402 (#2350)
from services.security.field_encryption import ENV_SCOPED_SUBKEYS

from .connector_grant_store import ConnectorGrantStore
from .github_app_grant import (
    REASON_CUTOVER,
    REASON_REFRESH_REJECTED,
    REFRESH_SKEW_SECONDS,
    GitHubAppGrant,
    GrantRecordDamaged,
    app_mode,
    classify,
)

logger = structlog.get_logger(__name__)

_GITHUB = "github"
_LOCK_NAMESPACE = "github_grant_refresh:"

#: The background pass refreshes a grant with less than this left (Arch: 2 hours).
BACKGROUND_DUE_WITHIN_SECONDS = 2 * 3600
#: How often the background pass runs (Arch: every 30 minutes).
BACKGROUND_INTERVAL_SECONDS = 30 * 60

# One asyncio lock per owner, for requests inside this process. The Postgres advisory
# lock covers other processes and machines; this one also covers the SQLite unit layer.
_OWNER_LOCKS: Dict[str, asyncio.Lock] = {}


@dataclass(frozen=True)
class AppGrantVerdict:
    """Exactly one of: ``token`` (serve with it), ``stale_reason`` (the binding goes
    STALE with that reason; ``None``-reason staleness is ``absent``), ``read_failed``
    (the store could not be read: UNREACHABLE, never absence), or ``unreachable`` (the
    refresh could not complete and the token has expired; the store is untouched)."""

    token: Optional[str] = None
    stale_reason: Optional[str] = None
    absent: bool = False
    read_failed: bool = False
    unreachable: bool = False
    # What happened, for the background pass's one log line: "fresh", "refreshed",
    # "could_not_complete", "rejected", "raced" or "" (not a refresh result).
    event: str = ""

    def __repr__(self) -> str:  # never a token
        return (
            f"AppGrantVerdict(serves={self.token is not None}, "
            f"stale_reason={self.stale_reason!r}, absent={self.absent}, "
            f"read_failed={self.read_failed}, unreachable={self.unreachable})"
        )


def process_can_refresh() -> bool:
    """False in a scoped (decrypt-only) process, which can never write a new pair."""
    return not os.getenv(ENV_SCOPED_SUBKEYS)


def advisory_lock_key(owner_id) -> int:
    """The signed 64-bit key for ``pg_advisory_xact_lock``: a hash of the namespace and
    the owner, so no other advisory lock can collide with this use."""
    digest = hashlib.sha256(f"{_LOCK_NAMESPACE}{owner_id}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big", signed=True)


async def _take_advisory_lock(session, owner_id) -> None:
    bind = session.get_bind()
    if getattr(getattr(bind, "dialect", None), "name", "") != "postgresql":
        return
    await session.execute(
        text("SELECT pg_advisory_xact_lock(:key)"), {"key": advisory_lock_key(owner_id)}
    )


def _classify_or_failed(raw: Optional[str]):
    """(grant, verdict): a grant to work with, or the verdict that ends the read."""
    if raw is None:
        return None, AppGrantVerdict(absent=True)
    try:
        grant = classify(raw)
    except GrantRecordDamaged:
        logger.warning("github_app_grant_record_damaged")
        return None, AppGrantVerdict(read_failed=True)
    if grant is None:
        return None, AppGrantVerdict(stale_reason=REASON_CUTOVER)
    return grant, None


async def _read_grant(owner_id) -> Optional[str]:
    """The stored value, from the encrypted row only. The seam tests patch."""
    async with AsyncSessionFactory.session_scope() as session:
        return await ConnectorGrantStore().get_encrypted_strict(session, str(owner_id), _GITHUB)


def _new_handler():
    from .github_oauth_handler import GitHubOAuthHandler

    return GitHubOAuthHandler()


async def app_grant_verdict(owner_id, raw: Optional[str]) -> AppGrantVerdict:
    """The resolver's verdict for a BOUND binding's stored value in App mode."""
    grant, verdict = _classify_or_failed(raw)
    if verdict is not None:
        return verdict
    if not grant.refresh_due():
        return AppGrantVerdict(token=grant.access_token, event="fresh")
    if not process_can_refresh() or not app_mode():
        # A scoped process can't write a new pair; a process without App mode holds no
        # client secret. Neither may spend the refresh token.
        if grant.access_expired():
            logger.warning(
                "github_app_grant_expired_where_it_cannot_be_refreshed",
                scoped=not process_can_refresh(),
                app_mode=app_mode(),
            )
            return AppGrantVerdict(unreachable=True)
        return AppGrantVerdict(token=grant.access_token)
    return await _refresh_under_lock(owner_id)


def _due(grant: GitHubAppGrant, due_within: int) -> bool:
    return time.time() >= grant.access_expires_at - due_within


async def _refresh_under_lock(
    owner_id, *, due_within: int = REFRESH_SKEW_SECONDS
) -> AppGrantVerdict:
    lock = _OWNER_LOCKS.setdefault(str(owner_id), asyncio.Lock())
    async with lock:
        rejected_pair: Optional[GitHubAppGrant] = None
        try:
            async with AsyncSessionFactory.session_scope() as session:
                await _take_advisory_lock(session, owner_id)
                store = ConnectorGrantStore()
                raw = await store.get_encrypted_strict(session, str(owner_id), _GITHUB)
                current, verdict = _classify_or_failed(raw)
                if verdict is not None:
                    return verdict
                if not _due(current, due_within):
                    # Another request refreshed while this one waited for the lock.
                    return AppGrantVerdict(token=current.access_token, event="fresh")
                outcome = await _new_handler().refresh_grant(current.refresh_token)
                if outcome.refreshed:
                    # One write, both tokens: the old refresh token is already spent.
                    # LAST step under the lock: this call commits, which releases it.
                    try:
                        await store.store_app_grant(session, str(owner_id), _GITHUB, outcome.grant)
                    except Exception as e:
                        # Arch 2026-11-12 07:24: GitHub has already spent the old refresh
                        # token, so the next refresh will be rejected and the person told
                        # to reconnect. Its own event, so that later ``refresh_rejected``
                        # can be explained from the log.
                        logger.error(
                            "github_app_grant_refreshed_write_failed",
                            owner_id=str(owner_id),
                            error=type(e).__name__,
                        )
                        return AppGrantVerdict(read_failed=True, event="could_not_complete")
                    evidence("github_app_grant_refreshed", owner_id=str(owner_id))
                    return AppGrantVerdict(token=outcome.grant.access_token, event="refreshed")
                if outcome.could_not_complete:
                    # Nothing is written back and the binding is not marked.
                    if current.access_expired():
                        return AppGrantVerdict(unreachable=True, event="could_not_complete")
                    return AppGrantVerdict(token=current.access_token, event="could_not_complete")
                rejected_pair = current
        except Exception:
            logger.warning("github_app_grant_refresh_read_failed", exc_info=True)
            return AppGrantVerdict(read_failed=True)
        # Rejected. Re-read once, in a fresh session, before calling it stale (Arch
        # 2026-11-11 19:11): a pair written by a concurrent request that this lock did
        # not cover must serve, never send a person to reconnect a working connection.
        try:
            newer, verdict = _classify_or_failed(await _read_grant(owner_id))
        except Exception:
            logger.warning("github_app_grant_reread_failed", exc_info=True)
            return AppGrantVerdict(read_failed=True)
        if (
            newer is not None
            and newer.refresh_token != rejected_pair.refresh_token
            and not newer.access_expired()
        ):
            evidence("github_app_grant_refresh_raced_served_newer", owner_id=str(owner_id))
            return AppGrantVerdict(token=newer.access_token, event="raced")
        return AppGrantVerdict(stale_reason=REASON_REFRESH_REJECTED, event="rejected")


async def _bound_github_owners() -> list:
    """Owner ids of every BOUND GitHub binding. The seam tests patch."""
    from services.database.models import ConnectorBinding

    from .connector import ConnectorStatusState

    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(
            select(ConnectorBinding.owner_id).where(
                ConnectorBinding.connector == _GITHUB,
                ConnectorBinding.status == ConnectorStatusState.BOUND.value,
            )
        )
        return [row[0] for row in result.all()]


async def background_refresh_pass(
    *, due_within: int = BACKGROUND_DUE_WITHIN_SECONDS
) -> Dict[str, int]:
    """#2342 (Arch 2026-11-12 06:52): one pass of the main app's background refresh.

    Only in App mode and never in a scoped process. Takes only App-marked grants whose
    binding is BOUND and that have under ``due_within`` left; a STALE or UNBOUND binding
    is never refreshed, and a classic grant is left for the resolver and the cutover
    script. A rejected refresh marks the binding STALE with ``refresh_rejected``; one
    that can't complete writes nothing, and the next pass retries it. Writes one log
    line with the counts and returns them. Never raises."""
    counts = {
        "seen": 0,
        "refreshed": 0,
        "already_fresh": 0,
        "rejected": 0,
        "could_not_complete": 0,
    }
    if not app_mode() or not process_can_refresh():
        return counts
    try:
        owners = await _bound_github_owners()
    except Exception:
        logger.warning("github_app_background_refresh_list_failed", exc_info=True)
        return counts
    for owner_id in owners:
        try:
            grant = classify(await _read_grant(owner_id))
        except Exception:  # an unreadable or damaged row: not this pass's to judge
            logger.warning("github_app_background_refresh_read_failed", owner_id=str(owner_id))
            continue
        if grant is None:
            continue  # absent or classic: not an App-marked grant
        counts["seen"] += 1
        if not _due(grant, due_within):
            counts["already_fresh"] += 1
            continue
        verdict = await _refresh_under_lock(owner_id, due_within=due_within)
        if verdict.event == "refreshed":
            counts["refreshed"] += 1
        elif verdict.event in ("fresh", "raced"):
            counts["already_fresh"] += 1
        elif verdict.event == "rejected":
            counts["rejected"] += 1
            await _mark_refresh_rejected(owner_id)
        else:
            counts["could_not_complete"] += 1
    evidence("github_app_background_refresh_pass", **counts)
    return counts


async def _mark_refresh_rejected(owner_id) -> None:
    """STALE with ``refresh_rejected``, through the adapter's one stale-writing function
    (only over BOUND, best-effort)."""
    from .github_adapter import GitHubCredential, GitHubMCPSpatialAdapter

    await GitHubMCPSpatialAdapter._mark_oauth_binding_stale(
        GitHubCredential(owner_id=owner_id, mcp_server_ref=_GITHUB, token=None, leg="oauth"),
        reason=REASON_REFRESH_REJECTED,
    )
