"""Personalization-context repository (ADR-075 Component B, #1366).

Data access for `personalization_contexts` — the DB-backed, owner_id-scoped home
for per-user system-prompt personalization (ADR-075 D2). Mirrors
`ConnectorConfigRepository`'s async pattern (#1226/#1199): the caller owns the
transaction (this layer flushes; the session scope commits). Anchored to
`owner_id` (ADR-071 D2).

Read/write asymmetry is deliberate: reads degrade gracefully (a None/non-UUID
owner → None, m-40), but writes are STRICT (context must belong to the settled
identity — `owner_id` is NOT NULL, so `upsert` with a None/non-UUID owner
raises rather than silently no-op) — same discipline as connector_configs.
"""

from __future__ import annotations

from typing import Optional, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import PersonalizationContext


def _as_uuid_or_none(value: Union[str, UUID, None]) -> Optional[UUID]:
    """Parse a principal (str | UUID | None) to UUID, or None if malformed (m-40 graceful)."""
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except (ValueError, TypeError, AttributeError):
        return None


class PersonalizationContextRepository:
    """Data access for the `personalization_contexts` table (ADR-075 Component B)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, owner_id: Union[str, UUID, None]) -> Optional[PersonalizationContext]:
        """The owner's personalization row, or None.

        A None/non-UUID owner can't match a UUID `owner_id`, so it returns None
        (graceful read boundary, not an error — matches D4's "must degrade,
        never crash" invariant at the resolution layer above this one).
        """
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            return None
        result = await self.session.execute(
            select(PersonalizationContext).where(PersonalizationContext.owner_id == owner)
        )
        return result.scalar_one_or_none()

    async def upsert(
        self,
        owner_id: Union[str, UUID, None],
        context: dict,
        is_seeded_default: bool = False,
    ) -> PersonalizationContext:
        """Insert the owner's row, or replace its context blob in place.

        Idempotent by the unique `owner_id`. The caller owns the transaction
        (flush here; commit via the session scope). Raises ValueError on a
        None/non-UUID owner — context MUST belong to the settled identity
        (`owner_id` NOT NULL, D2). Replace-semantics (not merge): the context
        blob is owned by the caller, which read-modify-writes the whole dict.

        `is_seeded_default` defaults to False here (an explicit upsert is, by
        definition, not the lazy-seed path — see `get_or_seed_default` below
        for that path specifically).
        """
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            raise ValueError("personalization context requires a valid owner_id (UUID)")
        row = await self.get(owner)
        if row is None:
            row = PersonalizationContext(owner_id=owner, context={})
            self.session.add(row)
        row.context = dict(context or {})  # reassign → SQLAlchemy tracks the change
        row.is_seeded_default = is_seeded_default
        await self.session.flush()
        return row

    async def get_or_seed_default(
        self, owner_id: Union[str, UUID, None], default_context: dict
    ) -> Optional[PersonalizationContext]:
        """The owner's row if one exists; otherwise seed one with `default_context`
        and return the newly-created row (ADR-075 OQ-3 / HOST's "real seeded
        record, not implicit empty fall-through" requirement).

        None/non-UUID owner returns None without seeding anything (m-40
        graceful — matches `get`'s degradation boundary; there is no
        identity to seed a row for).
        """
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            return None
        existing = await self.get(owner)
        if existing is not None:
            return existing
        return await self.upsert(owner, default_context, is_seeded_default=True)

    async def mark_notice_seen(self, owner_id: Union[str, UUID, None]) -> None:
        """Mark the first-response personalization notice as shown for this
        owner (ADR-075 OQ-3) — one-time, never shown again regardless of
        whether the user goes on to customize their profile. A no-op if the
        owner is malformed or has no row (nothing to mark)."""
        owner = _as_uuid_or_none(owner_id)
        if owner is None:
            return
        row = await self.get(owner)
        if row is None:
            return
        row.has_seen_personalization_notice = True
        await self.session.flush()
