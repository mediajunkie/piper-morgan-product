"""Connector-binding repository (RECONNECT WS-2, #1229).

Data access for `connector_bindings` — the per-user MCP-server binding store (ADR-070 D3:
Piper stores bindings only, never raw creds). Mirrors ConnectorConfigRepository (#1199): the
caller owns the transaction (this layer flushes; the session scope commits). Anchored to
`owner_id` (ADR-071 D2); credential-free (D3 — the MCP server owns OAuth/tokens).

Read/write asymmetry is deliberate: reads degrade gracefully (a None/non-UUID owner → None,
m-40), but writes are STRICT (a binding must belong to the settled identity — `owner_id` is
NOT NULL, so a write with a None/non-UUID owner raises rather than silently no-op).
"""

from __future__ import annotations

from typing import Optional, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import ConnectorBinding


def _as_uuid_or_none(value: Union[str, UUID, None]) -> Optional[UUID]:
    """Parse a principal (str | UUID | None) to UUID, or None if malformed (m-40 graceful)."""
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except (ValueError, TypeError, AttributeError):
        return None


class ConnectorBindingRepository:
    """Data access for the `connector_bindings` table (WS-2)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
        self, owner_id: Union[str, UUID, None], connector: str
    ) -> Optional[ConnectorBinding]:
        """The (owner, connector) binding row, or None.

        A None/non-UUID owner can't match a UUID `owner_id`, so it returns None
        (graceful read boundary, not an error).
        """
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            return None
        result = await self.session.execute(
            select(ConnectorBinding).where(
                ConnectorBinding.owner_id == owner,
                ConnectorBinding.connector == connector,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self,
        owner_id: Union[str, UUID, None],
        connector: str,
        *,
        mcp_server_ref: Optional[str] = None,
        status: Optional[str] = None,
        capability_profile: Optional[dict] = None,
        is_native_legacy: Optional[bool] = None,
    ) -> ConnectorBinding:
        """Insert the (owner, connector) binding, or update its fields in place.

        Idempotent by unique(owner_id, connector). The caller owns the transaction (flush here;
        commit via the session scope). Raises ValueError on a None/non-UUID owner — a binding
        MUST belong to the settled identity (`owner_id` NOT NULL, ADR-071 D2). Only the fields
        passed (non-None) are updated; omitted fields keep their existing/default value. Stores
        NO credential material (D3 — the MCP server owns OAuth/tokens).
        """
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            raise ValueError("connector binding requires a valid owner_id (UUID)")
        row = await self.get(owner, connector)
        if row is None:
            row = ConnectorBinding(owner_id=owner, connector=connector)
            self.session.add(row)
        if mcp_server_ref is not None:
            row.mcp_server_ref = mcp_server_ref
        if status is not None:
            row.status = status
        if capability_profile is not None:
            row.capability_profile = dict(capability_profile)
        if is_native_legacy is not None:
            row.is_native_legacy = is_native_legacy
        await self.session.flush()
        return row

    async def set_status(
        self, owner_id: Union[str, UUID, None], connector: str, status: str
    ) -> Optional[ConnectorBinding]:
        """Update just the binding's status (bound/unbound/unreachable/stale). Returns the row,
        or None if no binding exists for (owner, connector) — status is a no-op without a binding
        (you can't be 'bound' before connect() creates the row).
        """
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            return None
        row = await self.get(owner, connector)
        if row is None:
            return None
        row.status = status
        await self.session.flush()
        return row
