"""#1532 F3 — chat-path conversation persistence must enforce ownership.

The audit (docs/internal/operations/principal-dropping-audit-2026-08-08.md)
found the three chat-path persistence reads (``get_recent_turns`` /
``load_context_state`` / ``hydrate_turns_from_db``) had NO principal parameter,
and ``ensure_conversation_exists`` returned early on existing rows with no
owner comparison — so authenticated user B posting user A's session UUID
hydrated A's turns into B's floor prompt AND appended B's turns to A's row.
The REST surface (conversations.py:173) enforces exactly the check the chat
path skipped.

Contract pinned here (the safe not-found contract, both directions):
- owner mismatch on READ → behave as not-found (empty list / None) + warning
  with both ids; turn content is never leaked.
- owner mismatch on APPEND → ConversationOwnershipError at the data layer.
- anonymous-owned rows (owner None) stay readable/appendable by the anonymous
  path ONLY; an authenticated principal hitting an anonymous-owned id is
  treated as not-found.
- principal omitted entirely (legacy sentinel) → unscoped m-40 shim, WARNs
  (mirrors ConversationRepository.get_by_id's #1252 D3 shim).

Mocked-session pattern (the #953/#1030 house pattern) so these run without
aiosqlite; the end-to-end DB shape is exercised by the repro evidence in the
#1532 session record and by the route tests.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.conversation.conversation_manager import (
    ConversationManager,
    _owner_matches,
)
from services.database.repositories import (
    ConversationOwnershipError,
    ConversationRepository,
)

_FACTORY_TARGET = "services.conversation.conversation_manager.AsyncSessionFactory"
_REPO_TARGET = "services.database.repositories.ConversationRepository"

USER_A = "user-a-1111"
USER_B = "user-b-2222"
CONV = "conv-of-user-a"


def _factory_with_row(row):
    """Mock AsyncSessionFactory whose session.get returns ``row`` (the
    conversation row the ownership probe sees)."""
    session = MagicMock()
    session.get = AsyncMock(return_value=row)
    factory = MagicMock()
    factory.session_scope.return_value.__aenter__ = AsyncMock(return_value=session)
    factory.session_scope.return_value.__aexit__ = AsyncMock(return_value=None)
    return factory, session


def _repo_with_turns(turns):
    repo = MagicMock()
    repo.get_conversation_turns = AsyncMock(return_value=turns)
    repo.load_context_state = AsyncMock(return_value={"lens_stack": ["issues"]})
    return repo


A_TURNS = [SimpleNamespace(user_message="A's private note", assistant_response="ok")]


class TestOwnerMatchContract:
    """The pinned ownership rule itself (shared read/append contract)."""

    def test_owner_reads_own_row(self):
        assert _owner_matches(USER_A, USER_A) is True

    def test_cross_principal_is_mismatch(self):
        assert _owner_matches(USER_A, USER_B) is False

    def test_anonymous_cannot_read_owned_row(self):
        assert _owner_matches(USER_A, None) is False

    def test_authenticated_on_anonymous_owned_row_is_not_found(self):
        """PINNED safe contract: an authenticated user hitting an
        anonymous-owned conversation id is treated as not-found."""
        assert _owner_matches(None, USER_B) is False

    def test_anonymous_path_keeps_anonymous_owned_rows(self):
        """PINNED: anonymous-owned rows remain readable by the anonymous path."""
        assert _owner_matches(None, None) is True

    def test_string_comparison_not_identity(self):
        """Mirrors the REST rule's str() comparison (UUID vs str inputs)."""
        from uuid import UUID

        uid = "12345678-1234-5678-1234-567812345678"
        assert _owner_matches(uid, UUID(uid)) is True


class TestGetRecentTurnsOwnership:
    @pytest.mark.asyncio
    async def test_cross_principal_read_is_empty_and_never_touches_turns(self):
        """F3 READ half: B reading A's session gets [] — the turns query is
        never even issued for a mismatched principal."""
        factory, _ = _factory_with_row(SimpleNamespace(user_id=USER_A))
        repo = _repo_with_turns(A_TURNS)
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            got = await ConversationManager().get_recent_turns(CONV, user_id=USER_B)
        assert got == []
        repo.get_conversation_turns.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_owner_read_returns_turns(self):
        factory, _ = _factory_with_row(SimpleNamespace(user_id=USER_A))
        repo = _repo_with_turns(A_TURNS)
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            got = await ConversationManager().get_recent_turns(CONV, user_id=USER_A)
        assert got == A_TURNS

    @pytest.mark.asyncio
    async def test_anonymous_principal_cannot_read_owned_row(self):
        factory, _ = _factory_with_row(SimpleNamespace(user_id=USER_A))
        repo = _repo_with_turns(A_TURNS)
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            got = await ConversationManager().get_recent_turns(CONV, user_id=None)
        assert got == []

    @pytest.mark.asyncio
    async def test_anonymous_principal_reads_anonymous_owned_row(self):
        """PINNED: the anonymous path keeps working against anonymous rows."""
        factory, _ = _factory_with_row(SimpleNamespace(user_id=None))
        repo = _repo_with_turns(A_TURNS)
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            got = await ConversationManager().get_recent_turns(CONV, user_id=None)
        assert got == A_TURNS

    @pytest.mark.asyncio
    async def test_missing_row_scoped_read_returns_empty_not_error(self):
        """A scoped read of a nonexistent conversation stays a clean empty
        read (anonymous sessions with no persisted row keep working)."""
        factory, _ = _factory_with_row(None)
        repo = _repo_with_turns([])
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            got = await ConversationManager().get_recent_turns(CONV, user_id=USER_B)
        assert got == []

    @pytest.mark.asyncio
    async def test_unscoped_legacy_call_still_reads(self):
        """m-40 shim PIN: omitting the principal entirely (sentinel) stays
        unscoped + WARNs — non-breaking for legacy/internal callers while
        Guard 1/3 push callers to thread it."""
        factory, session = _factory_with_row(SimpleNamespace(user_id=USER_A))
        repo = _repo_with_turns(A_TURNS)
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            got = await ConversationManager().get_recent_turns(CONV)
        assert got == A_TURNS

    @pytest.mark.asyncio
    async def test_ownership_probe_failure_fails_closed(self):
        """DB down during the probe → empty (fail-closed), never a leak."""
        factory = MagicMock()
        factory.session_scope.side_effect = RuntimeError("db down")
        with patch(_FACTORY_TARGET, factory):
            got = await ConversationManager().get_recent_turns(CONV, user_id=USER_B)
        assert got == []


class TestLoadContextStateOwnership:
    @pytest.mark.asyncio
    async def test_cross_principal_state_read_is_none(self):
        factory, _ = _factory_with_row(SimpleNamespace(user_id=USER_A))
        repo = _repo_with_turns([])
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            got = await ConversationManager().load_context_state(CONV, user_id=USER_B)
        assert got is None
        repo.load_context_state.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_owner_state_read_returns_state(self):
        factory, _ = _factory_with_row(SimpleNamespace(user_id=USER_A))
        repo = _repo_with_turns([])
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            got = await ConversationManager().load_context_state(CONV, user_id=USER_A)
        assert got == {"lens_stack": ["issues"]}


def _repo_with_conversation_row(row):
    session = AsyncMock()
    session.get = AsyncMock(return_value=row)
    session.add = MagicMock()
    session.commit = AsyncMock()
    repo = ConversationRepository(session)
    return repo, session


class TestEnsureConversationExistsOwnership:
    @pytest.mark.asyncio
    async def test_cross_principal_append_raises(self):
        """F3 APPEND half: appending B's turns to A's row is impossible."""
        repo, session = _repo_with_conversation_row(SimpleNamespace(user_id=USER_A))
        with pytest.raises(ConversationOwnershipError):
            await repo.ensure_conversation_exists(CONV, user_id=USER_B)
        session.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_anonymous_append_to_owned_row_raises(self):
        repo, _ = _repo_with_conversation_row(SimpleNamespace(user_id=USER_A))
        with pytest.raises(ConversationOwnershipError):
            await repo.ensure_conversation_exists(CONV, user_id=None)

    @pytest.mark.asyncio
    async def test_authenticated_append_to_anonymous_owned_row_raises(self):
        """PINNED: no adoption of anonymous-owned rows by authenticated users."""
        repo, _ = _repo_with_conversation_row(SimpleNamespace(user_id=None))
        with pytest.raises(ConversationOwnershipError):
            await repo.ensure_conversation_exists(CONV, user_id=USER_B)

    @pytest.mark.asyncio
    async def test_owner_append_passes(self):
        repo, session = _repo_with_conversation_row(SimpleNamespace(user_id=USER_A))
        await repo.ensure_conversation_exists(CONV, user_id=USER_A)  # no raise
        session.add.assert_not_called()  # row exists; nothing created

    @pytest.mark.asyncio
    async def test_anonymous_on_anonymous_owned_row_passes(self):
        repo, _ = _repo_with_conversation_row(SimpleNamespace(user_id=None))
        await repo.ensure_conversation_exists(CONV, user_id=None)  # no raise

    @pytest.mark.asyncio
    async def test_save_turn_propagates_ownership_refusal(self):
        """The sole production caller: save_turn must refuse, not append."""
        repo, session = _repo_with_conversation_row(SimpleNamespace(user_id=USER_A))
        turn = MagicMock(conversation_id=CONV)
        with pytest.raises(ConversationOwnershipError):
            await repo.save_turn(turn, user_id=USER_B)
        session.add.assert_not_called()
        session.commit.assert_not_awaited()


class TestHydrateTurnsPrincipalThreading:
    @pytest.mark.asyncio
    async def test_hydrate_threads_principal_to_manager_read(self):
        from services.intent_service.conversation_context import (
            ConversationContext,
            hydrate_turns_from_db,
        )

        ctx = ConversationContext()
        manager = MagicMock()
        manager.get_recent_turns = AsyncMock(return_value=[])
        await hydrate_turns_from_db(ctx, manager, "sess-1", user_id=USER_B)
        manager.get_recent_turns.assert_awaited_once_with(
            "sess-1", limit=ctx.max_turns, user_id=USER_B
        )

    @pytest.mark.asyncio
    async def test_hydrate_legacy_call_stays_unscoped(self):
        """3-arg legacy shape forwards NO user_id kwarg (manager shim decides)."""
        from services.intent_service.conversation_context import (
            ConversationContext,
            hydrate_turns_from_db,
        )

        ctx = ConversationContext()
        manager = MagicMock()
        manager.get_recent_turns = AsyncMock(return_value=[])
        await hydrate_turns_from_db(ctx, manager, "sess-1")
        manager.get_recent_turns.assert_awaited_once_with("sess-1", limit=ctx.max_turns)

    @pytest.mark.asyncio
    async def test_cross_principal_hydration_backfills_nothing(self):
        """End-to-end through the real manager: B hydrating A's session id
        gets an EMPTY working state — A's turns never reach B's floor."""
        from services.intent_service.conversation_context import (
            ConversationContext,
            hydrate_turns_from_db,
        )

        factory, _ = _factory_with_row(SimpleNamespace(user_id=USER_A))
        repo = _repo_with_turns(A_TURNS)
        ctx = ConversationContext()
        with patch(_FACTORY_TARGET, factory), patch(_REPO_TARGET, return_value=repo):
            backfilled = await hydrate_turns_from_db(
                ctx, ConversationManager(), CONV, user_id=USER_B
            )
        assert backfilled is False
        assert ctx.turns == []
