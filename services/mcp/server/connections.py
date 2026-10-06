"""Owner-scoped read/revoke of a user's MCP credentials, for the Settings
"Connected apps" surface (#1918).

Two credential families share the identity boundary unit 1/4 built
(``services/mcp/server/identity.py`` / ``oauth_provider.py``):

- OAuth-issued access tokens carry ``label = "oauth:{client_id}"``
  (``OAUTH_LABEL_PREFIX``) and are paired with a ``mcp_oauth_refresh_tokens``
  row for the same ``(user_id, client_id)``. These are what "Connected apps"
  shows grouped by client.
- Operator-minted (manually-minted) bearer tokens carry any OTHER label.
  They have no refresh-token counterpart and are listed individually.

Every read and write here takes ``user_id`` as an explicit argument and
filters by it — there is no code path in this module that can read or
revoke another user's credential. The router (``web/api/routes/
mcp_connections.py``) is the ONLY caller, and it sources ``user_id`` from
the authenticated session (``get_current_user``), never from a request
parameter.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import MCPAccessToken, MCPOAuthClient, MCPOAuthRefreshToken
from services.mcp.server.oauth_provider import OAUTH_LABEL_PREFIX


def _as_aware_utc(value: Optional[datetime]) -> Optional[datetime]:
    """Same normalization as ``identity.py``/``oauth_provider.py``: SQLite
    (the unit tests' in-memory DB) drops tzinfo on read-back; every value
    this module ever wrote was already UTC, so a naive value read back is
    safely re-attached to UTC, not guessed at."""
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value


def _is_active(
    expires_at: Optional[datetime], revoked_at: Optional[datetime], now: datetime
) -> bool:
    if revoked_at is not None:
        return False
    expires = _as_aware_utc(expires_at)
    if expires is not None and expires <= now:
        return False
    return True


@dataclass
class OAuthConnection:
    client_id: str
    client_name: Optional[str]
    connected_at: datetime
    last_used_at: Optional[datetime]
    active: bool


@dataclass
class ManualToken:
    label: str
    connected_at: datetime
    last_used_at: Optional[datetime]
    active: bool


@dataclass
class MCPConnections:
    oauth_connections: list[OAuthConnection]
    manual_tokens: list[ManualToken]


async def list_user_connections(session: AsyncSession, user_id: uuid.UUID) -> MCPConnections:
    """This user's OAuth client grants (grouped) + manually-minted tokens
    (individually). Never returns a token hash or raw token — only the
    metadata columns (label, timestamps, active)."""
    now = datetime.now(timezone.utc)

    access_rows = (
        (
            await session.execute(
                # owner-scoped: user_id is the authenticated caller's id (#1918)
                select(MCPAccessToken).where(MCPAccessToken.user_id == user_id)
            )
        )
        .scalars()
        .all()
    )

    refresh_rows = (
        (
            await session.execute(
                # owner-scoped: user_id is the authenticated caller's id (#1918)
                select(MCPOAuthRefreshToken).where(MCPOAuthRefreshToken.user_id == user_id)
            )
        )
        .scalars()
        .all()
    )

    oauth_groups: dict[str, list[MCPAccessToken]] = {}
    manual_tokens: list[ManualToken] = []
    for row in access_rows:
        label = row.label or ""
        if label.startswith(OAUTH_LABEL_PREFIX):
            client_id = label[len(OAUTH_LABEL_PREFIX) :]
            oauth_groups.setdefault(client_id, []).append(row)
        else:
            manual_tokens.append(
                ManualToken(
                    label=label,
                    connected_at=_as_aware_utc(row.created_at) or now,
                    last_used_at=_as_aware_utc(row.last_used_at),
                    active=_is_active(row.expires_at, row.revoked_at, now),
                )
            )

    refresh_by_client: dict[str, list[MCPOAuthRefreshToken]] = {}
    for refresh_row in refresh_rows:  # own name: `row` above is an MCPAccessToken (mypy, 1947)
        refresh_by_client.setdefault(refresh_row.client_id, []).append(refresh_row)

    client_ids = set(oauth_groups) | set(refresh_by_client)

    client_names: dict[str, Optional[str]] = {}
    if client_ids:
        # global-ok: mcp_oauth_clients names an APPLICATION, not a user's row
        # (same distinction oauth_provider.py's MCPOAuthClient docstring draws) —
        # there is no user_id column to scope by.
        client_rows = (
            (
                await session.execute(
                    select(MCPOAuthClient).where(MCPOAuthClient.client_id.in_(client_ids))
                )
            )
            .scalars()
            .all()
        )
        client_names = {c.client_id: c.client_name for c in client_rows if c.client_id}

    oauth_connections: list[OAuthConnection] = []
    for client_id in client_ids:
        access_group = oauth_groups.get(client_id, [])
        refresh_group = refresh_by_client.get(client_id, [])

        connected_candidates = [
            ts
            for ts in (
                [_as_aware_utc(r.created_at) for r in access_group]
                + [_as_aware_utc(r.created_at) for r in refresh_group]
            )
            if ts is not None
        ]
        connected_at = min(connected_candidates) if connected_candidates else now

        last_used_candidates = [
            ts for ts in (_as_aware_utc(r.last_used_at) for r in access_group) if ts is not None
        ]
        last_used_at = max(last_used_candidates) if last_used_candidates else None

        active = any(_is_active(r.expires_at, r.revoked_at, now) for r in access_group) or any(
            _is_active(r.expires_at, r.revoked_at, now) for r in refresh_group
        )

        oauth_connections.append(
            OAuthConnection(
                client_id=client_id,
                client_name=client_names.get(client_id),
                connected_at=connected_at,
                last_used_at=last_used_at,
                active=active,
            )
        )

    oauth_connections.sort(key=lambda c: c.connected_at, reverse=True)
    manual_tokens.sort(key=lambda t: t.connected_at, reverse=True)

    return MCPConnections(oauth_connections=oauth_connections, manual_tokens=manual_tokens)


async def revoke_oauth_connection(
    session: AsyncSession, user_id: uuid.UUID, client_id: str
) -> bool:
    """Revoke ALL of this user's access tokens labelled ``oauth:{client_id}``
    AND all of this user's refresh tokens for ``client_id``, in the caller's
    transaction (commit happens on the caller's session-scope exit).

    Returns ``False`` when this user never had any credential (revoked or
    not) for this ``client_id`` — the router turns that into a 404 WITHOUT
    revealing whether the client_id exists for some other user. Idempotent:
    a repeat call for a client_id this user DID connect still returns
    ``True`` even though every matching row is already revoked (re-stamping
    an already-revoked row is a no-op `UPDATE ... WHERE revoked_at IS NULL`).
    """
    label = f"{OAUTH_LABEL_PREFIX}{client_id}"

    existing_access = (
        await session.execute(
            # owner-scoped: user_id is the authenticated caller's id (#1918)
            select(MCPAccessToken.id)
            .where(MCPAccessToken.user_id == user_id, MCPAccessToken.label == label)
            .limit(1)
        )
    ).first()
    existing_refresh = (
        await session.execute(
            # owner-scoped: user_id is the authenticated caller's id (#1918)
            select(MCPOAuthRefreshToken.id)
            .where(
                MCPOAuthRefreshToken.user_id == user_id,
                MCPOAuthRefreshToken.client_id == client_id,
            )
            .limit(1)
        )
    ).first()
    if existing_access is None and existing_refresh is None:
        return False

    now = datetime.now(timezone.utc)
    await session.execute(
        update(MCPAccessToken)
        .where(
            # owner-scoped: user_id is the authenticated caller's id (#1918)
            MCPAccessToken.user_id == user_id,
            MCPAccessToken.label == label,
            MCPAccessToken.revoked_at.is_(None),
        )
        .values(revoked_at=now)
    )
    await session.execute(
        update(MCPOAuthRefreshToken)
        .where(
            # owner-scoped: user_id is the authenticated caller's id (#1918)
            MCPOAuthRefreshToken.user_id == user_id,
            MCPOAuthRefreshToken.client_id == client_id,
            MCPOAuthRefreshToken.revoked_at.is_(None),
        )
        .values(revoked_at=now)
    )
    return True
