"""#953 CONTEXT-PERSIST Phase 3 — ConversationManager context-state wiring.

Verifies the async persist/load wiring added to ConversationManager:
- _save_turn_to_database persists context_state via the same-session
  repo.save_context_state (after save_turn / ensure_conversation_exists).
- load_context_state delegates to repo.load_context_state; best-effort on error.

Mocks AsyncSessionFactory (patched where it's USED — module-level in
conversation_manager) + ConversationRepository (local import → patched at source).
Tests _save_turn_to_database directly to isolate the new logic from the rest of
save_conversation_turn's call graph. The repo methods + (de)serialize round-trip
are covered by the foundation tests.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.conversation.conversation_manager import ConversationManager

# AsyncSessionFactory is module-level in conversation_manager → patch it there.
_FACTORY_TARGET = "services.conversation.conversation_manager.AsyncSessionFactory"
# ConversationRepository is locally imported inside the methods → patch at source.
_REPO_TARGET = "services.database.repositories.ConversationRepository"


def _mock_factory():
    factory = MagicMock()
    factory.session_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
    factory.session_scope.return_value.__aexit__ = AsyncMock(return_value=None)
    return factory


def _mock_repo():
    repo = MagicMock()
    repo.save_turn = AsyncMock()
    repo.save_context_state = AsyncMock()
    repo.load_context_state = AsyncMock()
    return repo


class TestSaveTurnPersistsContextState:
    @pytest.mark.asyncio
    async def test_context_state_persisted_in_same_session_as_turn(self):
        mgr = ConversationManager()
        repo = _mock_repo()
        turn = MagicMock(conversation_id="conv-1")
        state = {"lens_stack": ["issues"], "last_offer": None}

        with patch(_FACTORY_TARGET, _mock_factory()), patch(_REPO_TARGET, return_value=repo):
            await mgr._save_turn_to_database(turn, user_id="user-1", context_state=state)

        repo.save_turn.assert_awaited_once()
        repo.save_context_state.assert_awaited_once_with("conv-1", state)

    @pytest.mark.asyncio
    async def test_no_context_state_skips_save_context_state(self):
        mgr = ConversationManager()
        repo = _mock_repo()
        turn = MagicMock(conversation_id="conv-1")

        with patch(_FACTORY_TARGET, _mock_factory()), patch(_REPO_TARGET, return_value=repo):
            await mgr._save_turn_to_database(turn, user_id="user-1")  # context_state=None

        repo.save_turn.assert_awaited_once()
        repo.save_context_state.assert_not_awaited()


class TestLoadContextState:
    @pytest.mark.asyncio
    async def test_load_delegates_to_repo(self):
        mgr = ConversationManager()
        repo = _mock_repo()
        state = {"lens_stack": ["calendar"], "last_response_was_floor": True}
        repo.load_context_state = AsyncMock(return_value=state)

        with patch(_FACTORY_TARGET, _mock_factory()), patch(_REPO_TARGET, return_value=repo):
            got = await mgr.load_context_state("conv-1")

        assert got == state
        repo.load_context_state.assert_awaited_once_with("conv-1")

    @pytest.mark.asyncio
    async def test_load_returns_none_on_error(self):
        """DB hiccup → None (best-effort), never raises into the floor path."""
        mgr = ConversationManager()
        factory = MagicMock()
        factory.session_scope.side_effect = RuntimeError("db down")
        with patch(_FACTORY_TARGET, factory):
            assert await mgr.load_context_state("conv-1") is None

    @pytest.mark.asyncio
    async def test_save_turn_swallows_errors(self):
        """_save_turn_to_database is best-effort — a context-state write failure
        must not propagate (persistence never blocks the response)."""
        mgr = ConversationManager()
        repo = _mock_repo()
        repo.save_context_state = AsyncMock(side_effect=RuntimeError("boom"))
        turn = MagicMock(conversation_id="conv-1")
        with patch(_FACTORY_TARGET, _mock_factory()), patch(_REPO_TARGET, return_value=repo):
            # must not raise
            await mgr._save_turn_to_database(turn, user_id="u", context_state={"lens_stack": []})
