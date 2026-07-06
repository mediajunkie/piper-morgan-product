"""Repository for knowledge-base documents (ADR-071 P2, #1238).

Owner-anchoring for the ChromaDB doc store: the `documents` table is the
canonical relational row each ChromaDB document needs (the store itself is
ChromaDB-only). This repo upserts a row per ingested document and answers the
read-authorization question — which documents a principal may read — as a set of
`chromadb_base_id`s the caller intersects with ChromaDB query results (the
`is_global_pm_domain` marker lives on the row, not in ChromaDB metadata — Arch
ruling 2026-06-16).
"""

from __future__ import annotations

import os
from typing import List, Optional, Set, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import DocumentDB, User


def _as_uuid_or_none(value: Union[str, UUID, None]) -> Optional[UUID]:
    """Parse a principal (str | UUID | None) to UUID, or None if malformed.

    #1252 P7 / ADR-071: the principal is a users.id UUID, but a non-UUID legacy
    identifier must NOT raise — it simply can't match a UUID owner_id, so the
    caller treats None as "no owner match" (→ global-only reads). Graceful
    boundary guard, not the D5 degradation ternary.
    """
    if isinstance(value, UUID):
        return value
    try:
        return UUID(value)
    except (ValueError, TypeError, AttributeError):
        return None


async def resolve_pm_owner_id(session: AsyncSession) -> Optional[UUID]:
    """Resolve the configured PM's users.id — the doc-store owner for CLI ingest + backfill.

    Resolution order (#1260, ADR-071 D7 prerequisite — replaces the old hardcoded
    ``username == 'xian'`` literal with server-owned config, ADR-066 D7):
      1. env ``PIPER_PM_USER_ID`` (explicit override), if a valid UUID
      2. the user named by ``PiperConfigLoader.load_pm_identity_config()`` (the
         "PM Identity" section of ``PIPER.user.md`` — single-tenant shape today;
         ADR-071 D7 names the evolution to a tenant principal, same config seam)
      3. None — graceful. ``owner_id`` is provenance; reads still work via
         ``is_global_pm_domain``, so an unresolved PM never breaks readability.
    """
    override = os.environ.get("PIPER_PM_USER_ID")
    parsed = _as_uuid_or_none(override) if override else None
    if parsed is not None:
        return parsed

    from services.configuration.piper_config_loader import piper_config_loader

    username = piper_config_loader.load_pm_identity_config()
    if not username:
        return None
    result = await session.execute(select(User.id).where(User.username == username))
    return _as_uuid_or_none(result.scalar_one_or_none())


class DocumentRepository:
    """Data access for the `documents` anchor table (#1238)."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_document(
        self,
        chromadb_base_id: str,
        owner_id: Union[str, UUID, None] = None,
        is_global_pm_domain: bool = False,
        title: Optional[str] = None,
        source: Optional[str] = None,
    ) -> DocumentDB:
        """Insert a document row, or update it in place if the base_id exists.

        Idempotent by ``chromadb_base_id`` (safe for re-ingest + backfill re-runs).
        Caller owns the transaction (flush here; commit via session_scope()).
        """
        owner_uuid = _as_uuid_or_none(owner_id)
        row = await self.get_by_base_id(chromadb_base_id)
        if row is None:
            row = DocumentDB(chromadb_base_id=chromadb_base_id)
            self.session.add(row)
        row.owner_id = owner_uuid
        row.is_global_pm_domain = bool(is_global_pm_domain)
        if title is not None:
            row.title = title
        if source is not None:
            row.source = source
        await self.session.flush()
        return row

    async def get_by_base_id(self, chromadb_base_id: str) -> Optional[DocumentDB]:
        result = await self.session.execute(
            select(DocumentDB).where(DocumentDB.chromadb_base_id == chromadb_base_id)
        )
        return result.scalar_one_or_none()

    async def get_readable_base_ids(self, principal_owner_id: Union[str, UUID, None]) -> Set[str]:
        """Return the set of chromadb_base_ids the principal may read.

        Readable = ``is_global_pm_domain`` is true (D1 exemption — preserves
        PM-domain shared-reasoning-context reads) OR ``owner_id == principal``.
        A None/non-UUID principal sees global-only (m-40 graceful — a non-UUID
        can't match a UUID owner). The caller intersects this set with ChromaDB
        query results.
        """
        principal = _as_uuid_or_none(principal_owner_id)
        stmt = select(DocumentDB.chromadb_base_id)
        if principal is None:
            stmt = stmt.where(DocumentDB.is_global_pm_domain.is_(True))
        else:
            stmt = stmt.where(
                (DocumentDB.is_global_pm_domain.is_(True)) | (DocumentDB.owner_id == principal)
            )
        result = await self.session.execute(stmt)
        return set(result.scalars().all())

    async def list_for_owner(self, principal_owner_id: Union[str, UUID, None]) -> List[DocumentDB]:
        """The principal's OWN documents (owner == principal), newest-first.

        For the personal Radar surface (#1238 "the user's documents") — owner-scoped,
        intentionally NOT including is_global_pm_domain docs (those are shared
        reasoning-context for the reads, not personal-radar items; a user's Radar shows
        their own docs, not the global PM knowledge base). None/non-UUID principal → []
        (m-40 graceful — a non-UUID can't own anything).
        """
        principal = _as_uuid_or_none(principal_owner_id)
        if principal is None:
            return []
        result = await self.session.execute(
            select(DocumentDB)
            .where(DocumentDB.owner_id == principal)
            .order_by(DocumentDB.updated_at.desc())
        )
        return list(result.scalars().all())
