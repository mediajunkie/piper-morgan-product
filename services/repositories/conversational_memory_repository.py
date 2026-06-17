"""
Repository for conversational memory entries.

Part of #657 MEM-ADR054-P1.
"""

from datetime import datetime
from typing import List
from uuid import UUID, uuid4

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import ConversationalMemoryEntryDB
from services.memory.conversational_memory import ConversationalMemoryEntry


def _as_uuid_or_none(user_id: str):
    """Parse a principal string to UUID, or None if malformed.

    #1252 P7: the principal is a users.id-string (a UUID per ADR-071), but a
    non-UUID identifier must NOT raise here — some consumer paths still pass
    legacy string ids during the user_id→owner_id transition. A non-UUID can't
    match a UUID owner_id, so callers treat None as "no match" (return empty).
    This is a graceful boundary guard, not the D5 degradation ternary.
    """
    try:
        return UUID(user_id)
    except (ValueError, TypeError, AttributeError):
        return None


class ConversationalMemoryRepository:
    """
    Repository for conversational memory entries.

    Provides data access for ADR-054 Layer 1 (24-hour conversational memory).
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save_entry(self, user_id: str, entry: ConversationalMemoryEntry) -> str:
        """
        Save a memory entry.

        Args:
            user_id: User ID
            entry: Memory entry to save

        Returns:
            Entry ID
        """
        entry_id = str(uuid4())

        db_entry = ConversationalMemoryEntryDB(
            id=entry_id,
            user_id=user_id,
            # #1252 P7 (ADR-071 D2): dual-write the canonical owner_id (UUID)
            # during the user_id→owner_id transition. Graceful: a non-UUID
            # principal leaves owner_id NULL rather than raising on save.
            owner_id=_as_uuid_or_none(user_id),
            conversation_id=entry.conversation_id,
            timestamp=entry.timestamp,
            topic_summary=entry.topic_summary,
            entities_mentioned=entry.entities_mentioned,
            outcome=entry.outcome,
            user_sentiment=entry.user_sentiment,
        )

        self.session.add(db_entry)
        await self.session.commit()

        return entry_id

    async def get_entries_since(
        self,
        user_id: str,
        since: datetime,
    ) -> List[ConversationalMemoryEntry]:
        """
        Get entries for user since given timestamp.

        Args:
            user_id: User ID
            since: Return entries after this timestamp

        Returns:
            List of entries ordered most recent first
        """
        # #1252 P7 (ADR-071 D2): scope by the canonical owner_id (UUID). A
        # non-UUID principal can't match a UUID owner_id → no rows (graceful).
        owner_uuid = _as_uuid_or_none(user_id)
        if owner_uuid is None:
            return []
        stmt = (
            select(ConversationalMemoryEntryDB)
            .where(ConversationalMemoryEntryDB.owner_id == owner_uuid)
            .where(ConversationalMemoryEntryDB.timestamp >= since)
            .order_by(ConversationalMemoryEntryDB.timestamp.desc())
        )

        result = await self.session.execute(stmt)
        rows = result.scalars().all()

        return [self._to_domain(row) for row in rows]

    async def delete_entries_before(self, user_id: str, before: datetime) -> int:
        """
        Delete entries older than given timestamp.

        Args:
            user_id: User ID
            before: Delete entries before this timestamp

        Returns:
            Count of deleted entries
        """
        # #1252 P7 (ADR-071 D2): scope by the canonical owner_id (UUID); a
        # non-UUID principal matches nothing → delete 0 (graceful).
        owner_uuid = _as_uuid_or_none(user_id)
        if owner_uuid is None:
            return 0
        stmt = (
            delete(ConversationalMemoryEntryDB)
            .where(ConversationalMemoryEntryDB.owner_id == owner_uuid)
            .where(ConversationalMemoryEntryDB.timestamp < before)
        )

        result = await self.session.execute(stmt)
        await self.session.commit()

        return result.rowcount

    def _to_domain(self, db_entry: ConversationalMemoryEntryDB) -> ConversationalMemoryEntry:
        """Convert database model to domain model."""
        return ConversationalMemoryEntry(
            conversation_id=db_entry.conversation_id,
            timestamp=db_entry.timestamp,
            topic_summary=db_entry.topic_summary,
            entities_mentioned=db_entry.entities_mentioned or [],
            outcome=db_entry.outcome,
            user_sentiment=db_entry.user_sentiment,
        )
