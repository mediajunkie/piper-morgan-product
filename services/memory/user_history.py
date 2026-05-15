"""
User history service for conversation archive access.

Part of #663 MEM-ADR054-P3 (ADR-054 Phase 3: User History Enhancements).

This module provides:
- ConversationSummary: Summary of a conversation for history display
- UserHistoryPage: Paginated conversation history
- UserHistoryRepository: Abstract repository for history access
- UserHistoryService: Service for managing user's conversation history

Layer 2 of ADR-054's memory model - all past conversations accessible
and searchable, with privacy mode support.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Protocol

# =============================================================================
# Domain Models
# =============================================================================


@dataclass
class ConversationSummary:
    """
    Summary of a conversation for history display.

    Provides enough information to display in a history list
    without loading full conversation content.
    """

    conversation_id: str
    title: str
    started_at: datetime
    last_activity: datetime
    turn_count: int
    topics: List[str]
    preview: str  # First user message or summary
    is_private: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "conversation_id": self.conversation_id,
            "title": self.title,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "turn_count": self.turn_count,
            "topics": self.topics,
            "preview": self.preview,
            "is_private": self.is_private,
        }


@dataclass
class UserHistoryPage:
    """
    Paginated conversation history.

    Supports browsing through large conversation archives
    with standard pagination controls.
    """

    conversations: List[ConversationSummary]
    total_count: int
    page: int
    page_size: int
    has_more: bool

    @property
    def total_pages(self) -> int:
        """Calculate total number of pages."""
        if self.page_size <= 0:
            return 0
        return (self.total_count + self.page_size - 1) // self.page_size


@dataclass
class ConversationDetail:
    """
    Full conversation with all turns.

    Used when displaying a single conversation's complete history.
    """

    conversation_id: str
    title: str
    started_at: datetime
    last_activity: datetime
    is_private: bool
    topics: List[str]
    turns: List[Dict[str, Any]]  # List of {role, content, timestamp}


# =============================================================================
# Repository Protocol
# =============================================================================


class UserHistoryRepository(ABC):
    """
    Abstract repository for user history operations.

    Implementations can be database-backed or in-memory for testing.
    """

    @abstractmethod
    async def get_conversations(
        self,
        user_id: str,
        offset: int,
        limit: int,
        include_private: bool,
    ) -> tuple[List[ConversationSummary], int]:
        """
        Get conversations for a user with pagination.

        Returns:
            Tuple of (conversations, total_count)
        """
        pass

    @abstractmethod
    async def search_conversations(
        self,
        user_id: str,
        query: str,
        limit: int,
    ) -> List[ConversationSummary]:
        """Search conversations by content/title/topics."""
        pass

    @abstractmethod
    async def set_private(
        self,
        user_id: str,
        conversation_id: str,
        is_private: bool,
    ) -> bool:
        """Set privacy flag on a conversation."""
        pass

    @abstractmethod
    async def get_detail(
        self,
        user_id: str,
        conversation_id: str,
    ) -> Optional[ConversationDetail]:
        """Get full conversation detail."""
        pass


# =============================================================================
# In-Memory Repository (for testing)
# =============================================================================


class InMemoryUserHistoryRepository(UserHistoryRepository):
    """
    In-memory implementation for testing.

    Stores conversations in a dictionary keyed by user_id.
    """

    def __init__(self):
        self._conversations: Dict[str, List[ConversationSummary]] = {}
        self._details: Dict[str, ConversationDetail] = {}

    def add_conversation(
        self,
        user_id: str,
        summary: ConversationSummary,
        detail: Optional[ConversationDetail] = None,
    ) -> None:
        """Add a conversation for testing."""
        if user_id not in self._conversations:
            self._conversations[user_id] = []
        self._conversations[user_id].append(summary)

        if detail:
            self._details[summary.conversation_id] = detail

    async def get_conversations(
        self,
        user_id: str,
        offset: int,
        limit: int,
        include_private: bool,
    ) -> tuple[List[ConversationSummary], int]:
        """Get conversations with pagination."""
        all_convos = self._conversations.get(user_id, [])

        # Filter private if needed
        if not include_private:
            all_convos = [c for c in all_convos if not c.is_private]

        # Sort by last_activity descending
        all_convos = sorted(all_convos, key=lambda c: c.last_activity, reverse=True)

        total = len(all_convos)
        paginated = all_convos[offset : offset + limit]

        return paginated, total

    async def search_conversations(
        self,
        user_id: str,
        query: str,
        limit: int,
    ) -> List[ConversationSummary]:
        """Search by title, preview, or topics."""
        all_convos = self._conversations.get(user_id, [])
        query_lower = query.lower()

        matching = []
        for conv in all_convos:
            if conv.is_private:
                continue  # Never include private in search

            if (
                query_lower in conv.title.lower()
                or query_lower in conv.preview.lower()
                or any(query_lower in topic.lower() for topic in conv.topics)
            ):
                matching.append(conv)

        # Sort by relevance (title match first, then last_activity)
        matching.sort(
            key=lambda c: (
                0 if query_lower in c.title.lower() else 1,
                -c.last_activity.timestamp(),
            )
        )

        return matching[:limit]

    async def set_private(
        self,
        user_id: str,
        conversation_id: str,
        is_private: bool,
    ) -> bool:
        """Set privacy flag."""
        convos = self._conversations.get(user_id, [])
        for conv in convos:
            if conv.conversation_id == conversation_id:
                # Create new summary with updated privacy (dataclass is frozen-ish)
                idx = convos.index(conv)
                convos[idx] = ConversationSummary(
                    conversation_id=conv.conversation_id,
                    title=conv.title,
                    started_at=conv.started_at,
                    last_activity=conv.last_activity,
                    turn_count=conv.turn_count,
                    topics=conv.topics,
                    preview=conv.preview,
                    is_private=is_private,
                )
                return True
        return False

    async def get_detail(
        self,
        user_id: str,
        conversation_id: str,
    ) -> Optional[ConversationDetail]:
        """Get conversation detail."""
        # Verify user owns this conversation
        convos = self._conversations.get(user_id, [])
        owns = any(c.conversation_id == conversation_id for c in convos)

        if not owns:
            return None

        return self._details.get(conversation_id)


# =============================================================================
# User History Service
# =============================================================================


class UserHistoryService:
    """
    Manages user's conversation history.

    Provides paginated access, search, privacy controls,
    and full conversation retrieval.
    """

    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    def __init__(self, repository: UserHistoryRepository):
        """
        Initialize with repository.

        Args:
            repository: Implementation of UserHistoryRepository
        """
        self.repository = repository

    async def get_history(
        self,
        user_id: str,
        page: int = 1,
        page_size: Optional[int] = None,
        include_private: bool = False,
    ) -> UserHistoryPage:
        """
        Get paginated conversation history.

        Args:
            user_id: User to get history for
            page: Page number (1-indexed)
            page_size: Items per page (default: 20, max: 100)
            include_private: Include private conversations

        Returns:
            UserHistoryPage with conversations and pagination info
        """
        # Normalize pagination params
        page = max(1, page)
        if page_size is None:
            page_size = self.DEFAULT_PAGE_SIZE
        page_size = min(max(1, page_size), self.MAX_PAGE_SIZE)

        offset = (page - 1) * page_size

        conversations, total_count = await self.repository.get_conversations(
            user_id=user_id,
            offset=offset,
            limit=page_size,
            include_private=include_private,
        )

        has_more = (offset + len(conversations)) < total_count

        return UserHistoryPage(
            conversations=conversations,
            total_count=total_count,
            page=page,
            page_size=page_size,
            has_more=has_more,
        )

    async def search_history(
        self,
        user_id: str,
        query: str,
        limit: int = 10,
    ) -> List[ConversationSummary]:
        """
        Search conversation history by content.

        Args:
            user_id: User to search history for
            query: Search query
            limit: Maximum results to return

        Returns:
            List of matching ConversationSummary
        """
        if not query or not query.strip():
            return []

        limit = min(max(1, limit), self.MAX_PAGE_SIZE)

        return await self.repository.search_conversations(
            user_id=user_id,
            query=query.strip(),
            limit=limit,
        )

    async def mark_private(
        self,
        user_id: str,
        conversation_id: str,
    ) -> bool:
        """
        Mark conversation as private.

        Private conversations are:
        - Excluded from memory/learning
        - Excluded from search results
        - Excluded from history unless explicitly requested

        Args:
            user_id: User who owns the conversation
            conversation_id: Conversation to mark private

        Returns:
            True if successful, False if conversation not found
        """
        return await self.repository.set_private(
            user_id=user_id,
            conversation_id=conversation_id,
            is_private=True,
        )

    async def unmark_private(
        self,
        user_id: str,
        conversation_id: str,
    ) -> bool:
        """
        Remove private flag from conversation.

        Args:
            user_id: User who owns the conversation
            conversation_id: Conversation to unmark

        Returns:
            True if successful, False if conversation not found
        """
        return await self.repository.set_private(
            user_id=user_id,
            conversation_id=conversation_id,
            is_private=False,
        )

    async def get_conversation_detail(
        self,
        user_id: str,
        conversation_id: str,
    ) -> Optional[ConversationDetail]:
        """
        Get full conversation with all turns.

        Args:
            user_id: User who owns the conversation
            conversation_id: Conversation to retrieve

        Returns:
            ConversationDetail if found, None otherwise
        """
        return await self.repository.get_detail(
            user_id=user_id,
            conversation_id=conversation_id,
        )

    async def get_history_summary(
        self,
        user_id: str,
        max_conversations: int = 5,
    ) -> Optional[str]:
        """
        Compact text summary of the user's recent conversation history.

        Per ADR-054 Layer 3 / PDR-002 adaptive greetings: returns a
        short prompt-injectable string suitable for the floor's
        ``persistent_memory`` field — e.g. "Last active 2 hours ago.
        3 prior conversations; recent topics: roadmap, onboarding."

        Returns ``None`` when the user has no prior conversations, so
        callers can skip the field cleanly.

        Args:
            user_id: User to summarize history for
            max_conversations: How many recent conversations to inspect

        Returns:
            One-line summary string, or None if no history exists.
        """
        page = await self.get_history(
            user_id=user_id,
            page=1,
            page_size=max(1, min(max_conversations, self.MAX_PAGE_SIZE)),
            include_private=False,
        )

        if not page.conversations:
            return None

        most_recent = page.conversations[0]

        topic_pool: List[str] = []
        seen: set = set()
        for conv in page.conversations:
            for topic in conv.topics or []:
                key = topic.strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    topic_pool.append(topic.strip())
                if len(topic_pool) >= 5:
                    break
            if len(topic_pool) >= 5:
                break

        delta = datetime.now(timezone.utc) - most_recent.last_activity
        seconds = max(0, int(delta.total_seconds()))
        if seconds < 60:
            when = "moments ago"
        elif seconds < 3600:
            when = f"{seconds // 60} minute{'s' if seconds // 60 != 1 else ''} ago"
        elif seconds < 86400:
            when = f"{seconds // 3600} hour{'s' if seconds // 3600 != 1 else ''} ago"
        else:
            days = seconds // 86400
            when = f"{days} day{'s' if days != 1 else ''} ago"

        parts = [f"Last active {when}."]
        if page.total_count > 1:
            parts.append(f"{page.total_count} prior conversations.")
        if topic_pool:
            parts.append(f"Recent topics: {', '.join(topic_pool)}.")

        return " ".join(parts)
