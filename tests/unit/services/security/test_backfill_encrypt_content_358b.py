"""#358-B Phase 3 — backfill tests: idempotent encrypt, scope-guard, key-refusal."""

from __future__ import annotations

import base64
import os

import pytest

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import text  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from scripts.backfill_encrypt_content_358b import (  # noqa: E402
    TARGETS,
    backfill_column,
    require_encryptor,
)
from services.database.models import ConversationTurnDB  # noqa: E402
from services.security.encrypted_types import MARKER  # noqa: E402
from services.security.field_encryption import FieldEncryptionService  # noqa: E402


def test_targets_cover_exactly_the_four_approved_columns():
    # Scope guard: the backfill touches exactly the 4 PM-approved free-text columns.
    assert set(TARGETS) == {
        ("conversation_turns", "user_message", "conversation_turns.user_message"),
        ("conversation_turns", "assistant_response", "conversation_turns.assistant_response"),
        ("artifacts", "content", "artifacts.content"),
        ("conversations", "preview", "conversations.preview"),
    }


def test_require_encryptor_refuses_without_key(monkeypatch):
    monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)
    with pytest.raises(SystemExit):
        require_encryptor()


@pytest.mark.asyncio
async def test_backfill_column_encrypts_unmarked_idempotently(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda sc: ConversationTurnDB.__table__.create(sc, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Seed plaintext via the ORM with NO key (passthrough writes plaintext to the raw row).
    monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)
    async with SessionLocal() as s:
        for i in range(3):
            s.add(
                ConversationTurnDB(
                    id=f"t{i}",
                    conversation_id="c",
                    turn_number=i,
                    user_message=f"plain user {i}",
                    assistant_response=f"plain asst {i}",
                )
            )
        await s.commit()

    # Configure a key and backfill user_message only.
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(os.urandom(32)).decode())
    svc = FieldEncryptionService.from_env()
    ctx = "conversation_turns.user_message"
    async with engine.connect() as conn:
        n = await backfill_column(conn, "conversation_turns", "user_message", ctx, svc)
    assert n == 3

    # Raw row is now marked ciphertext that decrypts back.
    async with engine.connect() as conn:
        raw = (
            await conn.execute(text("SELECT user_message FROM conversation_turns WHERE id='t0'"))
        ).scalar()
    assert raw.startswith(MARKER) and "plain user 0" not in raw
    assert svc.decrypt(raw[len(MARKER) :], ctx) == "plain user 0"

    # ORM reads it back as plaintext; the un-backfilled column reads as legacy plaintext
    # (mixed plaintext+ciphertext state reads correctly).
    async with SessionLocal() as s:
        turn = await s.get(ConversationTurnDB, "t0")
        assert turn.user_message == "plain user 0"
        assert turn.assistant_response == "plain asst 0"  # not backfilled → legacy passthrough

    # Idempotent re-run → 0 newly encrypted; row count preserved.
    async with engine.connect() as conn:
        n2 = await backfill_column(conn, "conversation_turns", "user_message", ctx, svc)
        cnt = (await conn.execute(text("SELECT COUNT(*) FROM conversation_turns"))).scalar()
    assert n2 == 0
    assert cnt == 3

    await engine.dispose()
