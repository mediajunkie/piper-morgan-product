"""#1305 — real-Postgres proofs for EncryptedJSON.

What the unit file can't prove: (1) the ONE surviving server-side SQL query
(``pattern_data -> 'action_type'``, learning_handler.py:396) still works against
leaf-split rows written through the real ORM type; (2) full-value ciphertext
round-trips through real JSONB columns; (3) the #1305 backfill converts
pre-existing plaintext rows in place, idempotently, to shapes the ORM then
reads transparently.

Uses the shared db_session fixture (real Postgres) + a session-injected
encryptor via ENCRYPTION_MASTER_KEY monkeypatching where needed. Rows are
created and deleted per test.
"""

import base64
import json
import os
import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import String, cast, select, text

from services.database.models import ConversationDB, LearnedPattern
from services.security.encrypted_types import MARKER
from services.security.field_encryption import FieldEncryptionService

pytestmark = pytest.mark.usefixtures("_master_key_env")


@pytest.fixture
def _master_key_env(monkeypatch):
    """A real env master key so the (env-resolving) column types encrypt."""
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(os.urandom(32)).decode())


async def _mk_user(db_session):
    from services.auth.password_service import PasswordService
    from services.database.models import User

    name = f"enc_{uuid.uuid4().hex[:10]}"
    u = User(
        id=uuid.uuid4(),
        username=name,
        email=f"{name}@test.invalid",
        password_hash=PasswordService().hash_password("Xx-test-pass-1!"),
        is_active=True,
    )
    db_session.add(u)
    await db_session.commit()
    return u.id


def _mk_conversation(user_id, **kw):
    base = dict(
        id=str(uuid.uuid4()),
        user_id=user_id,
        session_id=f"s_{uuid.uuid4().hex[:8]}",
        title="t",
        context={"purpose": "secret plans", "client": "acme"},
        topics=["alpha", "beta"],
    )
    base.update(kw)
    return ConversationDB(**base)


class TestFullValueThroughRealPostgres:
    async def test_orm_round_trip_and_ciphertext_at_rest(self, db_session):
        uid = await _mk_user(db_session)
        conv = _mk_conversation(str(uid))  # conversations.user_id is VARCHAR
        db_session.add(conv)
        await db_session.commit()
        cid = conv.id

        # ORM read: transparent decrypt.
        row = (
            await db_session.execute(select(ConversationDB).where(ConversationDB.id == cid))
        ).scalar_one()
        assert row.context == {"purpose": "secret plans", "client": "acme"}
        assert row.topics == ["alpha", "beta"]

        # Raw read: ciphertext at rest (a marker-prefixed JSON string).
        raw_ctx, raw_topics = (
            await db_session.execute(
                text(
                    "SELECT context::text, topics::text FROM conversations WHERE id = :id"
                ),
                {"id": cid},
            )
        ).one()
        assert MARKER in raw_ctx and "secret plans" not in raw_ctx
        assert MARKER in raw_topics and "alpha" not in raw_topics

        await db_session.execute(
            text("DELETE FROM conversations WHERE id = :id"), {"id": cid}
        )
        await db_session.execute(text("DELETE FROM users WHERE id = :id"), {"id": uid})
        await db_session.commit()


class TestLeafSplitThroughRealPostgres:
    async def test_action_type_sql_query_survives_the_split(self, db_session):
        """The learning_handler.py:396 query shape — ``pattern_data ->
        'action_type'`` — must keep working against a leaf-split row."""
        from services.shared_types import PatternType

        uid = await _mk_user(db_session)
        pat = LearnedPattern(
            id=uuid.uuid4(),
            user_id=uid,
            pattern_type=PatternType.USER_WORKFLOW,
            pattern_data={
                "action_type": "create_issue",
                "sensitive_note": "user works odd hours",
            },
            confidence=0.5,
        )
        db_session.add(pat)
        await db_session.commit()
        pid = pat.id

        # The EXACT production query shape (learning_handler.py:396): -> then
        # cast(String). `->` on a json column with a text key yields the JSON
        # representation, so the comparand carries the JSON quotes.
        found = (
            await db_session.execute(
                select(LearnedPattern).where(
                    LearnedPattern.pattern_data.op("->")("action_type").cast(String)
                    == '"create_issue"',
                    LearnedPattern.id == pid,
                )
            )
        ).scalar_one_or_none()
        assert found is not None

        # ORM read restores the full object.
        assert found.pattern_data["sensitive_note"] == "user works odd hours"

        # Raw read: the sensitive value is NOT plaintext at rest; action_type IS.
        raw = (
            await db_session.execute(
                text("SELECT pattern_data::text FROM learned_patterns WHERE id = :id"), {"id": pid}
            )
        ).scalar_one()
        assert "odd hours" not in raw
        assert "create_issue" in raw
        assert MARKER in raw

        await db_session.execute(text("DELETE FROM learned_patterns WHERE id = :id"), {"id": pid})
        await db_session.execute(text("DELETE FROM users WHERE id = :id"), {"id": uid})
        await db_session.commit()


class TestBackfill1305:
    async def test_backfill_encrypts_plaintext_rows_idempotently(self, db_session):
        """Plant a raw plaintext row (pre-#1305 shape), run the backfill fns,
        verify ciphertext at rest + transparent ORM read + no-op re-run."""
        from scripts.backfill_encrypt_json_1305 import (
            backfill_full_value,
            backfill_leaf_split,
        )

        uid = await _mk_user(db_session)
        cid = str(uuid.uuid4())
        pid = str(uuid.uuid4())
        # Raw plaintext rows, bypassing the ORM type (the legacy state).
        await db_session.execute(
            text(
                "INSERT INTO conversations (id, user_id, session_id, title, context, topics, "
                "is_active, lifecycle_state, created_at, updated_at, preview, is_private, turn_count) "
                "VALUES (:id, :uid, 's', 't', CAST(:ctx AS jsonb), CAST(:top AS jsonb), "
                "true, 'active', now(), now(), '', false, 0)"
            ),
            {
                "id": cid,
                "uid": str(uid),  # VARCHAR column
                "ctx": json.dumps({"legacy": "plaintext-secret"}),
                "top": json.dumps(["legacy-topic"]),
            },
        )
        await db_session.execute(
            text(
                "INSERT INTO learned_patterns (id, user_id, pattern_type, pattern_data, confidence, "
                "usage_count, success_count, failure_count, enabled, created_at, updated_at) "
                "VALUES (:id, :uid, 'USER_WORKFLOW', CAST(:pd AS json), 0.4, 0, 0, 0, true, now(), now())"
            ),
            {"id": pid, "uid": uid, "pd": json.dumps({"action_type": "x", "note": "legacy-pii"})},
        )
        await db_session.commit()

        from sqlalchemy.ext.asyncio import create_async_engine

        from scripts.backfill_encrypt_json_1305 import _database_url

        enc = FieldEncryptionService.from_env()
        # The backfill batch-commits internally (zero-downtime design), so it
        # needs its own connection — NOT the test session's (committing a
        # session-borrowed connection kills the session transaction).
        engine = create_async_engine(_database_url(), pool_size=1, max_overflow=0)
        try:
            async with engine.connect() as conn:
                n_ctx = await backfill_full_value(
                    conn, "conversations", "context", "conversations.context", enc, batch=50
                )
                n_top = await backfill_full_value(
                    conn, "conversations", "topics", "conversations.topics", enc, batch=50
                )
                n_leaf = await backfill_leaf_split(conn, enc, batch=50)
        finally:
            await engine.dispose()
        assert n_ctx >= 1 and n_top >= 1 and n_leaf >= 1

        # At rest: ciphertext; plaintext gone.
        raw_ctx = (
            await db_session.execute(
                text("SELECT context::text FROM conversations WHERE id = :id"), {"id": cid}
            )
        ).scalar_one()
        assert MARKER in raw_ctx and "plaintext-secret" not in raw_ctx
        raw_pd = (
            await db_session.execute(
                text("SELECT pattern_data::text FROM learned_patterns WHERE id = :id"), {"id": pid}
            )
        ).scalar_one()
        assert MARKER in raw_pd and "legacy-pii" not in raw_pd and "action_type" in raw_pd

        # ORM reads decrypt transparently post-backfill.
        conv = (
            await db_session.execute(select(ConversationDB).where(ConversationDB.id == cid))
        ).scalar_one()
        assert conv.context == {"legacy": "plaintext-secret"}
        pat = (
            await db_session.execute(select(LearnedPattern).where(LearnedPattern.id == pid))
        ).scalar_one()
        assert pat.pattern_data["note"] == "legacy-pii"

        # Idempotent: a re-run touches nothing.
        engine2 = create_async_engine(_database_url(), pool_size=1, max_overflow=0)
        try:
            async with engine2.connect() as conn2:
                assert (
                    await backfill_full_value(
                        conn2, "conversations", "context", "conversations.context", enc, batch=50
                    )
                    == 0
                )
                assert await backfill_leaf_split(conn2, enc, batch=50) == 0
        finally:
            await engine2.dispose()

        await db_session.execute(text("DELETE FROM conversations WHERE id = :id"), {"id": cid})
        await db_session.execute(text("DELETE FROM learned_patterns WHERE id = :id"), {"id": pid})
        await db_session.execute(text("DELETE FROM users WHERE id = :id"), {"id": uid})
        await db_session.commit()
