"""#358-B Phase 2 — content columns encrypt-at-rest (real ORM round-trip + wiring).

Real round-trip against in-memory async SQLite (the #952/#1035 pattern). Proves the 4
target columns are wired to EncryptedString and that, with a master key configured,
the value is ciphertext at rest (raw SQL) but plaintext through the ORM.
"""
from __future__ import annotations

import base64
import os

import pytest

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import text as sa_text  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import (  # noqa: E402
    ArtifactDB,
    ConversationDB,
    ConversationTurnDB,
)
from services.security.encrypted_types import MARKER, EncryptedString  # noqa: E402


@pytest.fixture(autouse=True)
def _master_key(monkeypatch):
    # A real key so the columns actually encrypt during these tests.
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(os.urandom(32)).decode())


def test_target_columns_are_encrypted_string_with_per_field_context():
    """Wiring (#490 learning): the real model columns are EncryptedString with the
    correct per-field context — proves the decorator is wired, not just unit-correct."""
    expected = {
        ConversationTurnDB.__table__.c.user_message: "conversation_turns.user_message",
        ConversationTurnDB.__table__.c.assistant_response: "conversation_turns.assistant_response",
        ArtifactDB.__table__.c.content: "artifacts.content",
        ConversationDB.__table__.c.preview: "conversations.preview",
    }
    for col, ctx in expected.items():
        assert isinstance(col.type, EncryptedString)
        assert col.type._context == ctx


@pytest.mark.asyncio
async def test_turn_content_encrypted_at_rest_round_trips():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sc: ConversationTurnDB.__table__.create(sc, checkfirst=True)
        )
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        s.add(
            ConversationTurnDB(
                id="t1",
                conversation_id="c1",
                turn_number=1,
                user_message="my secret message",
                assistant_response="secret reply",
            )
        )
        await s.commit()
    # raw read → ciphertext at rest
    async with engine.connect() as conn:
        raw = (
            await conn.execute(
                sa_text(
                    "SELECT user_message, assistant_response FROM conversation_turns WHERE id='t1'"
                )
            )
        ).first()
    assert raw[0].startswith(MARKER) and "my secret message" not in raw[0]
    assert raw[1].startswith(MARKER) and "secret reply" not in raw[1]
    # ORM read → plaintext
    async with SessionLocal() as s:
        turn = await s.get(ConversationTurnDB, "t1")
        assert turn.user_message == "my secret message"
        assert turn.assistant_response == "secret reply"
    await engine.dispose()


@pytest.mark.asyncio
async def test_artifact_content_encrypted_at_rest_round_trips():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda sc: ArtifactDB.__table__.create(sc, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        s.add(
            ArtifactDB(
                id="a1", owner_id="u1", content="sensitive doc body", source_type="generated"
            )
        )
        await s.commit()
    async with engine.connect() as conn:
        raw = (
            await conn.execute(sa_text("SELECT content FROM artifacts WHERE id='a1'"))
        ).scalar()
    assert raw.startswith(MARKER) and "sensitive doc body" not in raw
    async with SessionLocal() as s:
        art = await s.get(ArtifactDB, "a1")
        assert art.content == "sensitive doc body"
    await engine.dispose()
