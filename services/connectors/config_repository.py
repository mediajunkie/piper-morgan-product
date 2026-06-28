"""Connector-config repository (RECONNECT WS-1, #1226 / #1199).

Data access for `connector_configs` — the DB-backed connector-config home (ADR-070 D4).
Mirrors the DocumentRepository async pattern (#1238): the caller owns the transaction
(this layer flushes; the session scope commits). Anchored to `owner_id` (ADR-071 D2);
credential-free (D3 — creds stay in the keychain, never in the config blob).

Read/write asymmetry is deliberate: reads degrade gracefully (a None/non-UUID owner →
None, m-40), but writes are STRICT (config must belong to the settled identity — `owner_id`
is NOT NULL, so `upsert` with a None/non-UUID owner raises rather than silently no-op).
"""

from __future__ import annotations

from typing import Optional, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import ConnectorConfig


def _as_uuid_or_none(value: Union[str, UUID, None]) -> Optional[UUID]:
    """Parse a principal (str | UUID | None) to UUID, or None if malformed (m-40 graceful)."""
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except (ValueError, TypeError, AttributeError):
        return None


class ConnectorConfigRepository:
    """Data access for the `connector_configs` table (WS-1)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
        self, owner_id: Union[str, UUID, None], connector: str
    ) -> Optional[ConnectorConfig]:
        """The (owner, connector) config row, or None.

        A None/non-UUID owner can't match a UUID `owner_id`, so it returns None
        (graceful read boundary, not an error).
        """
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            return None
        result = await self.session.execute(
            select(ConnectorConfig).where(
                ConnectorConfig.owner_id == owner,
                ConnectorConfig.connector == connector,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(
        self, owner_id: Union[str, UUID, None], connector: str, config: dict
    ) -> ConnectorConfig:
        """Insert the (owner, connector) row, or replace its config blob in place.

        Idempotent by the unique(owner_id, connector). The caller owns the transaction
        (flush here; commit via the session scope). Raises ValueError on a None/non-UUID
        owner — config MUST belong to the settled identity (`owner_id` NOT NULL, D2).
        Replace-semantics (not merge): the config blob is owned by the caller, which
        read-modify-writes the whole dict (e.g. the service's `set_default_repo`).
        """
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            raise ValueError("connector config requires a valid owner_id (UUID)")
        row = await self.get(owner, connector)
        if row is None:
            row = ConnectorConfig(owner_id=owner, connector=connector, config={})
            self.session.add(row)
        row.config = dict(config or {})  # reassign → SQLAlchemy tracks the change
        await self.session.flush()
        return row
