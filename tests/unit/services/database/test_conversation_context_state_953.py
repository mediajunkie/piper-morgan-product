"""#953 CONTEXT-PERSIST — Phase 2: ConversationRepository context-state methods.

Verifies the logic of save_context_state / load_context_state (namespace merge
under "layer4_state", missing-row → False/None, overwrite, legacy backward-compat)
using a mocked AsyncSession — the established #1030 unit pattern. These remain a
fast, fine-grained logic layer.

Note: ConversationDB is now SQLite-testable (#1180 added
``postgresql.JSONB().with_variant(JSON(), "sqlite")``), so the genuine
persistence round-trip — write, then read back through a *fresh* session — lives
in ``test_conversation_context_state_roundtrip_1180.py``. These mocked tests
complement it (logic edges without DB-setup cost).
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from services.database.repositories import ConversationRepository


def _repo_with_row(row):
    """Build a ConversationRepository whose session.get returns ``row`` (or None)
    and records commit calls."""
    session = AsyncMock()
    session.get = AsyncMock(return_value=row)
    session.commit = AsyncMock()
    repo = ConversationRepository(session)
    return repo, session


class TestSaveContextState953:
    @pytest.mark.asyncio
    async def test_save_writes_namespaced_state_and_commits(self):
        row = SimpleNamespace(context={})
        repo, session = _repo_with_row(row)
        state = {"lens_stack": ["issues"], "last_offer": None}

        ok = await repo.save_context_state("conv-1", state)

        assert ok is True
        assert row.context["layer4_state"] == state
        session.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_save_does_not_clobber_other_context_keys(self):
        row = SimpleNamespace(context={"some_other_key": "keep me"})
        repo, _ = _repo_with_row(row)

        await repo.save_context_state("conv-2", {"lens_stack": ["x"]})

        assert row.context["some_other_key"] == "keep me"
        assert row.context["layer4_state"] == {"lens_stack": ["x"]}

    @pytest.mark.asyncio
    async def test_save_handles_none_existing_context(self):
        row = SimpleNamespace(context=None)  # defensive: never None in prod, but guard
        repo, _ = _repo_with_row(row)
        ok = await repo.save_context_state("conv-x", {"lens_stack": []})
        assert ok is True
        assert row.context["layer4_state"] == {"lens_stack": []}

    @pytest.mark.asyncio
    async def test_save_returns_false_for_missing_conversation(self):
        repo, session = _repo_with_row(None)  # session.get → None
        ok = await repo.save_context_state("nope", {"lens_stack": []})
        assert ok is False
        session.commit.assert_not_awaited()  # no write attempted

    @pytest.mark.asyncio
    async def test_overwrite_replaces_prior_state(self):
        row = SimpleNamespace(context={})
        repo, _ = _repo_with_row(row)
        await repo.save_context_state("conv-3", {"lens_stack": ["a"]})
        await repo.save_context_state("conv-3", {"lens_stack": ["b"]})
        assert row.context["layer4_state"] == {"lens_stack": ["b"]}


class TestLoadContextState953:
    @pytest.mark.asyncio
    async def test_load_returns_persisted_state(self):
        state = {"lens_stack": ["issues", "calendar"], "last_response_was_floor": True}
        row = SimpleNamespace(context={"layer4_state": state})
        repo, _ = _repo_with_row(row)
        assert await repo.load_context_state("conv-1") == state

    @pytest.mark.asyncio
    async def test_load_returns_none_for_missing_conversation(self):
        repo, _ = _repo_with_row(None)
        assert await repo.load_context_state("nope") is None

    @pytest.mark.asyncio
    async def test_load_returns_none_for_legacy_row_without_state(self):
        """Row predating #953 (no layer4_state key) → None, not KeyError."""
        row = SimpleNamespace(context={"some_other_key": "x"})
        repo, _ = _repo_with_row(row)
        assert await repo.load_context_state("conv-legacy") is None

    @pytest.mark.asyncio
    async def test_load_handles_none_context(self):
        row = SimpleNamespace(context=None)
        repo, _ = _repo_with_row(row)
        assert await repo.load_context_state("conv-x") is None
