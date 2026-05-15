"""
Tests for user history service.

Part of #663 MEM-ADR054-P3.

Tests cover:
- ConversationSummary dataclass
- UserHistoryPage dataclass
- ConversationDetail dataclass
- InMemoryUserHistoryRepository
- UserHistoryService methods:
  - get_history (pagination)
  - search_history
  - mark_private / unmark_private
  - get_conversation_detail
"""

from datetime import datetime, timedelta, timezone

import pytest

from services.memory.user_history import (
    ConversationDetail,
    ConversationSummary,
    InMemoryUserHistoryRepository,
    UserHistoryPage,
    UserHistoryService,
)

# =============================================================================
# Test Fixtures
# =============================================================================


def make_summary(
    conversation_id: str = "conv-1",
    title: str = "Test Conversation",
    hours_ago: float = 0,
    turn_count: int = 5,
    topics: list = None,
    preview: str = "Hello, how can I help?",
    is_private: bool = False,
) -> ConversationSummary:
    """Helper to create test conversation summaries."""
    now = datetime.now(timezone.utc)
    return ConversationSummary(
        conversation_id=conversation_id,
        title=title,
        started_at=now - timedelta(hours=hours_ago + 1),
        last_activity=now - timedelta(hours=hours_ago),
        turn_count=turn_count,
        topics=topics or [],
        preview=preview,
        is_private=is_private,
    )


def make_detail(
    conversation_id: str = "conv-1",
    title: str = "Test Conversation",
    hours_ago: float = 0,
    is_private: bool = False,
    topics: list = None,
    turns: list = None,
) -> ConversationDetail:
    """Helper to create test conversation details."""
    now = datetime.now(timezone.utc)
    return ConversationDetail(
        conversation_id=conversation_id,
        title=title,
        started_at=now - timedelta(hours=hours_ago + 1),
        last_activity=now - timedelta(hours=hours_ago),
        is_private=is_private,
        topics=topics or [],
        turns=turns
        or [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ],
    )


@pytest.fixture
def repository():
    """Fresh in-memory repository for each test."""
    return InMemoryUserHistoryRepository()


@pytest.fixture
def service(repository):
    """Service with in-memory repository."""
    return UserHistoryService(repository=repository)


# =============================================================================
# Test: ConversationSummary
# =============================================================================


class TestConversationSummary:
    """Tests for ConversationSummary dataclass."""

    def test_creates_with_all_fields(self):
        """Summary can be created with all fields."""
        summary = make_summary(
            conversation_id="conv-123",
            title="API Discussion",
            topics=["api", "design"],
        )
        assert summary.conversation_id == "conv-123"
        assert summary.title == "API Discussion"
        assert summary.topics == ["api", "design"]
        assert summary.is_private is False

    def test_to_dict(self):
        """Summary serializes to dictionary."""
        summary = make_summary()
        d = summary.to_dict()

        assert "conversation_id" in d
        assert "title" in d
        assert "started_at" in d
        assert "last_activity" in d
        assert "topics" in d
        assert "is_private" in d

    def test_default_not_private(self):
        """Summaries are not private by default."""
        summary = make_summary()
        assert summary.is_private is False


# =============================================================================
# Test: UserHistoryPage
# =============================================================================


class TestUserHistoryPage:
    """Tests for UserHistoryPage dataclass."""

    def test_creates_with_conversations(self):
        """Page can be created with conversations."""
        convos = [make_summary(conversation_id=f"conv-{i}") for i in range(3)]
        page = UserHistoryPage(
            conversations=convos,
            total_count=10,
            page=1,
            page_size=3,
            has_more=True,
        )

        assert len(page.conversations) == 3
        assert page.total_count == 10
        assert page.has_more is True

    def test_total_pages_calculation(self):
        """Total pages calculated correctly."""
        page = UserHistoryPage(
            conversations=[],
            total_count=25,
            page=1,
            page_size=10,
            has_more=True,
        )
        assert page.total_pages == 3  # ceil(25/10) = 3

    def test_total_pages_exact_division(self):
        """Total pages correct for exact division."""
        page = UserHistoryPage(
            conversations=[],
            total_count=20,
            page=1,
            page_size=10,
            has_more=False,
        )
        assert page.total_pages == 2

    def test_total_pages_zero_page_size(self):
        """Total pages handles zero page size."""
        page = UserHistoryPage(
            conversations=[],
            total_count=10,
            page=1,
            page_size=0,
            has_more=False,
        )
        assert page.total_pages == 0


# =============================================================================
# Test: ConversationDetail
# =============================================================================


class TestConversationDetail:
    """Tests for ConversationDetail dataclass."""

    def test_creates_with_turns(self):
        """Detail includes conversation turns."""
        turns = [
            {"role": "user", "content": "Question"},
            {"role": "assistant", "content": "Answer"},
        ]
        detail = make_detail(turns=turns)

        assert len(detail.turns) == 2
        assert detail.turns[0]["role"] == "user"


# =============================================================================
# Test: InMemoryUserHistoryRepository
# =============================================================================


class TestInMemoryUserHistoryRepository:
    """Tests for in-memory repository."""

    @pytest.mark.asyncio
    async def test_get_conversations_empty(self, repository):
        """Returns empty for new user."""
        convos, total = await repository.get_conversations(
            user_id="new-user", offset=0, limit=10, include_private=False
        )
        assert convos == []
        assert total == 0

    @pytest.mark.asyncio
    async def test_add_and_retrieve(self, repository):
        """Can add and retrieve conversations."""
        repository.add_conversation("user-1", make_summary(conversation_id="c1"))
        repository.add_conversation("user-1", make_summary(conversation_id="c2"))

        convos, total = await repository.get_conversations(
            user_id="user-1", offset=0, limit=10, include_private=False
        )
        assert len(convos) == 2
        assert total == 2

    @pytest.mark.asyncio
    async def test_excludes_private_by_default(self, repository):
        """Private conversations excluded when not requested."""
        repository.add_conversation("user-1", make_summary(conversation_id="c1", is_private=False))
        repository.add_conversation("user-1", make_summary(conversation_id="c2", is_private=True))

        convos, total = await repository.get_conversations(
            user_id="user-1", offset=0, limit=10, include_private=False
        )
        assert len(convos) == 1
        assert convos[0].conversation_id == "c1"

    @pytest.mark.asyncio
    async def test_includes_private_when_requested(self, repository):
        """Private conversations included when requested."""
        repository.add_conversation("user-1", make_summary(conversation_id="c1", is_private=False))
        repository.add_conversation("user-1", make_summary(conversation_id="c2", is_private=True))

        convos, total = await repository.get_conversations(
            user_id="user-1", offset=0, limit=10, include_private=True
        )
        assert len(convos) == 2

    @pytest.mark.asyncio
    async def test_pagination(self, repository):
        """Pagination works correctly."""
        for i in range(5):
            repository.add_conversation(
                "user-1", make_summary(conversation_id=f"c{i}", hours_ago=i)
            )

        # First page
        convos, total = await repository.get_conversations(
            user_id="user-1", offset=0, limit=2, include_private=False
        )
        assert len(convos) == 2
        assert total == 5

        # Second page
        convos, total = await repository.get_conversations(
            user_id="user-1", offset=2, limit=2, include_private=False
        )
        assert len(convos) == 2

    @pytest.mark.asyncio
    async def test_sorted_by_last_activity(self, repository):
        """Results sorted by last_activity descending."""
        repository.add_conversation("user-1", make_summary(conversation_id="old", hours_ago=10))
        repository.add_conversation("user-1", make_summary(conversation_id="new", hours_ago=1))

        convos, _ = await repository.get_conversations(
            user_id="user-1", offset=0, limit=10, include_private=False
        )
        assert convos[0].conversation_id == "new"
        assert convos[1].conversation_id == "old"

    @pytest.mark.asyncio
    async def test_search_by_title(self, repository):
        """Search finds by title."""
        repository.add_conversation(
            "user-1", make_summary(conversation_id="c1", title="API Design Discussion")
        )
        repository.add_conversation(
            "user-1", make_summary(conversation_id="c2", title="Random Chat")
        )

        results = await repository.search_conversations("user-1", "API", limit=10)
        assert len(results) == 1
        assert results[0].conversation_id == "c1"

    @pytest.mark.asyncio
    async def test_search_by_preview(self, repository):
        """Search finds by preview content."""
        repository.add_conversation(
            "user-1",
            make_summary(conversation_id="c1", preview="Help with authentication"),
        )

        results = await repository.search_conversations("user-1", "auth", limit=10)
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_search_by_topics(self, repository):
        """Search finds by topics."""
        repository.add_conversation(
            "user-1",
            make_summary(conversation_id="c1", topics=["python", "testing"]),
        )

        results = await repository.search_conversations("user-1", "python", limit=10)
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_search_excludes_private(self, repository):
        """Search never includes private conversations."""
        repository.add_conversation(
            "user-1",
            make_summary(conversation_id="c1", title="Secret Project", is_private=True),
        )

        results = await repository.search_conversations("user-1", "Secret", limit=10)
        assert len(results) == 0

    @pytest.mark.asyncio
    async def test_set_private(self, repository):
        """Can set conversation as private."""
        repository.add_conversation("user-1", make_summary(conversation_id="c1"))

        result = await repository.set_private("user-1", "c1", True)
        assert result is True

        convos, _ = await repository.get_conversations("user-1", 0, 10, include_private=False)
        assert len(convos) == 0

    @pytest.mark.asyncio
    async def test_set_private_not_found(self, repository):
        """Returns False for non-existent conversation."""
        result = await repository.set_private("user-1", "nonexistent", True)
        assert result is False

    @pytest.mark.asyncio
    async def test_get_detail(self, repository):
        """Can retrieve conversation detail."""
        summary = make_summary(conversation_id="c1")
        detail = make_detail(conversation_id="c1")
        repository.add_conversation("user-1", summary, detail)

        result = await repository.get_detail("user-1", "c1")
        assert result is not None
        assert result.conversation_id == "c1"
        assert len(result.turns) == 2

    @pytest.mark.asyncio
    async def test_get_detail_wrong_user(self, repository):
        """Returns None for wrong user."""
        summary = make_summary(conversation_id="c1")
        detail = make_detail(conversation_id="c1")
        repository.add_conversation("user-1", summary, detail)

        result = await repository.get_detail("user-2", "c1")
        assert result is None


# =============================================================================
# Test: UserHistoryService.get_history
# =============================================================================


class TestGetHistory:
    """Tests for get_history method."""

    @pytest.mark.asyncio
    async def test_returns_page_for_user(self, service, repository):
        """Returns paginated history for user."""
        for i in range(5):
            repository.add_conversation("user-1", make_summary(conversation_id=f"c{i}"))

        page = await service.get_history("user-1", page=1, page_size=3)

        assert isinstance(page, UserHistoryPage)
        assert len(page.conversations) == 3
        assert page.total_count == 5
        assert page.has_more is True

    @pytest.mark.asyncio
    async def test_page_defaults(self, service, repository):
        """Default page is 1 with default page size."""
        for i in range(5):
            repository.add_conversation("user-1", make_summary(conversation_id=f"c{i}"))

        page = await service.get_history("user-1")

        assert page.page == 1
        assert page.page_size == 20  # Default

    @pytest.mark.asyncio
    async def test_max_page_size_enforced(self, service, repository):
        """Page size capped at maximum."""
        page = await service.get_history("user-1", page_size=500)
        assert page.page_size == 100  # Max

    @pytest.mark.asyncio
    async def test_excludes_private_by_default(self, service, repository):
        """Private excluded unless explicitly included."""
        repository.add_conversation("user-1", make_summary(conversation_id="c1", is_private=False))
        repository.add_conversation("user-1", make_summary(conversation_id="c2", is_private=True))

        page = await service.get_history("user-1")
        assert len(page.conversations) == 1

    @pytest.mark.asyncio
    async def test_includes_private_when_requested(self, service, repository):
        """Private included when requested."""
        repository.add_conversation("user-1", make_summary(conversation_id="c1", is_private=True))

        page = await service.get_history("user-1", include_private=True)
        assert len(page.conversations) == 1


# =============================================================================
# Test: UserHistoryService.search_history
# =============================================================================


class TestSearchHistory:
    """Tests for search_history method."""

    @pytest.mark.asyncio
    async def test_finds_matching_conversations(self, service, repository):
        """Finds conversations matching query."""
        repository.add_conversation("user-1", make_summary(title="Python API Design"))
        repository.add_conversation("user-1", make_summary(title="JavaScript Basics"))

        results = await service.search_history("user-1", "Python")
        assert len(results) == 1

    @pytest.mark.asyncio
    async def test_empty_query_returns_empty(self, service, repository):
        """Empty query returns no results."""
        repository.add_conversation("user-1", make_summary())

        results = await service.search_history("user-1", "")
        assert results == []

    @pytest.mark.asyncio
    async def test_whitespace_query_returns_empty(self, service, repository):
        """Whitespace-only query returns no results."""
        results = await service.search_history("user-1", "   ")
        assert results == []

    @pytest.mark.asyncio
    async def test_respects_limit(self, service, repository):
        """Respects the limit parameter."""
        for i in range(10):
            repository.add_conversation("user-1", make_summary(title=f"Python Topic {i}"))

        results = await service.search_history("user-1", "Python", limit=3)
        assert len(results) == 3


# =============================================================================
# Test: UserHistoryService.mark_private
# =============================================================================


class TestMarkPrivate:
    """Tests for mark_private and unmark_private methods."""

    @pytest.mark.asyncio
    async def test_mark_private_success(self, service, repository):
        """Can mark conversation as private."""
        repository.add_conversation("user-1", make_summary(conversation_id="c1"))

        result = await service.mark_private("user-1", "c1")
        assert result is True

        # Verify it's now private
        page = await service.get_history("user-1", include_private=False)
        assert len(page.conversations) == 0

    @pytest.mark.asyncio
    async def test_mark_private_not_found(self, service, repository):
        """Returns False for non-existent conversation."""
        result = await service.mark_private("user-1", "nonexistent")
        assert result is False

    @pytest.mark.asyncio
    async def test_unmark_private(self, service, repository):
        """Can remove private flag."""
        repository.add_conversation("user-1", make_summary(conversation_id="c1", is_private=True))

        # Verify it's private
        page = await service.get_history("user-1", include_private=False)
        assert len(page.conversations) == 0

        # Unmark
        result = await service.unmark_private("user-1", "c1")
        assert result is True

        # Verify it's now visible
        page = await service.get_history("user-1", include_private=False)
        assert len(page.conversations) == 1


# =============================================================================
# Test: UserHistoryService.get_conversation_detail
# =============================================================================


class TestGetConversationDetail:
    """Tests for get_conversation_detail method."""

    @pytest.mark.asyncio
    async def test_returns_detail(self, service, repository):
        """Returns full conversation detail."""
        summary = make_summary(conversation_id="c1")
        detail = make_detail(conversation_id="c1")
        repository.add_conversation("user-1", summary, detail)

        result = await service.get_conversation_detail("user-1", "c1")

        assert result is not None
        assert result.conversation_id == "c1"
        assert len(result.turns) >= 1

    @pytest.mark.asyncio
    async def test_returns_none_for_wrong_user(self, service, repository):
        """Returns None when user doesn't own conversation."""
        summary = make_summary(conversation_id="c1")
        detail = make_detail(conversation_id="c1")
        repository.add_conversation("user-1", summary, detail)

        result = await service.get_conversation_detail("user-2", "c1")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_for_nonexistent(self, service, repository):
        """Returns None for non-existent conversation."""
        result = await service.get_conversation_detail("user-1", "nonexistent")
        assert result is None


class TestGetHistorySummary:
    """Tests for the get_history_summary method (Issue #1021 Phase 2.4)."""

    @pytest.mark.asyncio
    async def test_returns_none_for_user_with_no_history(self, service):
        """No conversations → None so callers can skip the field."""
        result = await service.get_history_summary(user_id="nobody")
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_summary_with_recency_phrase(self, service, repository):
        """Summary always begins with a 'Last active …' phrase."""
        summary = make_summary(conversation_id="c1", hours_ago=2)
        repository.add_conversation("user-1", summary)

        result = await service.get_history_summary(user_id="user-1")

        assert result is not None
        assert "Last active" in result
        assert "ago" in result

    @pytest.mark.asyncio
    async def test_includes_topics_when_present(self, service, repository):
        """Topics from recent conversations appear in the summary."""
        summary = make_summary(
            conversation_id="c1",
            hours_ago=1,
            topics=["roadmap", "onboarding"],
        )
        repository.add_conversation("user-1", summary)

        result = await service.get_history_summary(user_id="user-1")

        assert "Recent topics:" in result
        assert "roadmap" in result
        assert "onboarding" in result

    @pytest.mark.asyncio
    async def test_includes_count_when_more_than_one(self, service, repository):
        """Summary mentions total count when user has 2+ conversations."""
        for i in range(3):
            repository.add_conversation(
                "user-1",
                make_summary(conversation_id=f"c{i}", hours_ago=i + 1),
            )

        result = await service.get_history_summary(user_id="user-1")

        assert "3 prior conversations" in result

    @pytest.mark.asyncio
    async def test_excludes_private_from_summary(self, service, repository):
        """Private conversations don't contribute to the summary."""
        repository.add_conversation(
            "user-1",
            make_summary(conversation_id="c1", hours_ago=1, is_private=True),
        )

        result = await service.get_history_summary(user_id="user-1")
        assert result is None

    @pytest.mark.asyncio
    async def test_dedupes_topics_across_conversations(self, service, repository):
        """A topic that recurs in multiple conversations appears once."""
        for i in range(3):
            repository.add_conversation(
                "user-1",
                make_summary(
                    conversation_id=f"c{i}",
                    hours_ago=i + 1,
                    topics=["roadmap"],
                ),
            )

        result = await service.get_history_summary(user_id="user-1")

        # "roadmap" should only show once after the colon
        topics_segment = result.split("Recent topics:")[-1]
        assert topics_segment.count("roadmap") == 1

    @pytest.mark.asyncio
    async def test_caps_topics_at_five(self, service, repository):
        """Summary surfaces at most 5 topic strings."""
        topics = [f"topic-{i}" for i in range(20)]
        repository.add_conversation(
            "user-1",
            make_summary(conversation_id="c1", hours_ago=1, topics=topics),
        )

        result = await service.get_history_summary(user_id="user-1")

        topics_segment = result.split("Recent topics:")[-1]
        assert topics_segment.count("topic-") == 5
