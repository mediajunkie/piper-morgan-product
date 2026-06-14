"""#1180 — ConversationRepository context-state REAL-DB round-trip (in-memory SQLite).

#953 added ``save_context_state`` / ``load_context_state`` but could only be
tested against a *mocked* session (see ``test_conversation_context_state_953.py``),
because ``ConversationDB`` used Postgres-only JSONB DDL that wouldn't compile on
in-memory SQLite. #1180 made ``ConversationDB`` SQLite-testable
(``postgresql.JSONB().with_variant(JSON(), "sqlite")``), so this exercises the
genuine persistence round-trip: write through the repo, read back through a
*fresh* session, and assert the JSON serialized and deserialized intact — the
thing the mock could not prove.

Mirrors the #1035 InsightRepository in-memory-SQLite pattern.
"""

from __future__ import annotations

import pytest
import pytest_asyncio

# Skip module if aiosqlite missing (parallel to #1035 / #1018 pattern).
aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import ConversationDB  # noqa: E402
from services.database.repositories import ConversationRepository  # noqa: E402

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def session_factory():
    """In-memory SQLite with the conversations table created; yields a session
    factory so each step can use its own session (proving real persistence)."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConversationDB.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    yield SessionLocal
    await engine.dispose()


async def _seed_conversation(SessionLocal, conv_id, *, context=None):
    async with SessionLocal() as s:
        s.add(
            ConversationDB(
                id=conv_id,
                user_id="alpha",
                session_id=conv_id,
                title="t",
                context=context if context is not None else {},
            )
        )
        await s.commit()


class TestContextStateRoundTrip1180:
    async def test_save_then_load_roundtrips_through_a_fresh_session(self, session_factory):
        """The real test the mock could not do: persist, then read back via a
        SEPARATE session, proving the JSONB/JSON column actually serialized."""
        await _seed_conversation(session_factory, "conv-rt")
        state = {
            "lens_stack": ["issues", "calendar"],
            "last_offer": None,
            "nested": {"counts": [1, 2, 3], "flag": True},
        }

        async with session_factory() as s:
            ok = await ConversationRepository(s).save_context_state("conv-rt", state)
            assert ok is True

        async with session_factory() as s:  # fresh session → real DB read
            loaded = await ConversationRepository(s).load_context_state("conv-rt")
        assert loaded == state

    async def test_save_preserves_other_context_keys_real_db(self, session_factory):
        await _seed_conversation(session_factory, "conv-keep", context={"existing": "keep me"})

        async with session_factory() as s:
            await ConversationRepository(s).save_context_state("conv-keep", {"lens_stack": ["x"]})

        async with session_factory() as s:
            row = await s.get(ConversationDB, "conv-keep")
        assert row.context["existing"] == "keep me"
        assert row.context["layer4_state"] == {"lens_stack": ["x"]}

    async def test_overwrite_replaces_prior_state_real_db(self, session_factory):
        await _seed_conversation(session_factory, "conv-ow")
        async with session_factory() as s:
            await ConversationRepository(s).save_context_state("conv-ow", {"lens_stack": ["a"]})
        async with session_factory() as s:
            await ConversationRepository(s).save_context_state("conv-ow", {"lens_stack": ["b"]})
        async with session_factory() as s:
            loaded = await ConversationRepository(s).load_context_state("conv-ow")
        assert loaded == {"lens_stack": ["b"]}

    async def test_missing_conversation_save_false_load_none(self, session_factory):
        async with session_factory() as s:
            assert await ConversationRepository(s).save_context_state("nope", {"x": 1}) is False
        async with session_factory() as s:
            assert await ConversationRepository(s).load_context_state("nope") is None

    async def test_legacy_row_without_state_loads_none(self, session_factory):
        """Row predating #953 (context has no layer4_state key) → None, not KeyError."""
        await _seed_conversation(session_factory, "conv-legacy", context={"other": "x"})
        async with session_factory() as s:
            assert await ConversationRepository(s).load_context_state("conv-legacy") is None
