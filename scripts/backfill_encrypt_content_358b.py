"""#358-B Phase 3 — zero-downtime backfill: encrypt existing plaintext content rows.

Raw-reads unmarked, non-empty values from the 4 target columns, encrypts each
(``MARKER + FieldEncryptionService.encrypt(value, context)`` — the SAME marker + context
the ``EncryptedString`` ORM type uses, so subsequent ORM reads decrypt transparently),
and raw-writes them back.

Idempotent + resumable: the ``WHERE ... NOT LIKE 'PMENC1:%'`` filter skips already-encrypted
rows, so a re-run is a no-op and a partial run resumes cleanly. **No DDL** → zero downtime;
the read path tolerates the mixed plaintext+ciphertext state throughout the run.

REFUSES to run without ``ENCRYPTION_MASTER_KEY`` — otherwise it would "succeed" while
storing plaintext under the encryption marker.

Run (with the key + DB env set, ANTHROPIC_* stripped per CLAUDE.md is NOT needed here —
this script makes no LLM calls):

    ENCRYPTION_MASTER_KEY=<base64-32B> POSTGRES_PORT=5433 \
        venv/bin/python -m scripts.backfill_encrypt_content_358b
"""
from __future__ import annotations

import asyncio
import os
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from services.security.encrypted_types import MARKER
from services.security.field_encryption import FieldEncryptionService

# (table, column, context-label) — MUST mirror the EncryptedString contexts in models.py.
TARGETS = [
    ("conversation_turns", "user_message", "conversation_turns.user_message"),
    ("conversation_turns", "assistant_response", "conversation_turns.assistant_response"),
    ("artifacts", "content", "artifacts.content"),
    ("conversations", "preview", "conversations.preview"),
]


def require_encryptor() -> FieldEncryptionService:
    """Return the env-configured encryptor, or exit non-zero (never run keyless)."""
    enc = FieldEncryptionService.from_env()
    if enc is None:
        print(
            "ERROR: ENCRYPTION_MASTER_KEY unset — refusing to run "
            "(would store plaintext under the encryption marker).",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return enc


def _database_url() -> str:
    user = os.getenv("POSTGRES_USER", "piper")
    password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    database = os.getenv("POSTGRES_DB", "piper_morgan")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


async def backfill_column(conn, table, column, context, encryptor, batch=500) -> int:
    """Encrypt unmarked, non-empty values in one column. Returns rows encrypted.

    Each batch re-queries ``NOT LIKE marker``; encrypted rows then match the marker and
    drop out, so the loop advances without OFFSET and is safe to resume.
    """
    total = 0
    while True:
        rows = (
            await conn.execute(
                text(
                    f"SELECT id, {column} FROM {table} "
                    f"WHERE {column} IS NOT NULL AND {column} <> '' "
                    f"AND {column} NOT LIKE :marker LIMIT :lim"
                ),
                {"marker": MARKER + "%", "lim": batch},
            )
        ).fetchall()
        if not rows:
            break
        for rid, val in rows:
            enc = MARKER + encryptor.encrypt(val, context)
            await conn.execute(
                text(f"UPDATE {table} SET {column} = :v WHERE id = :id"),
                {"v": enc, "id": rid},
            )
        await conn.commit()
        total += len(rows)
    return total


async def backfill_all(conn, encryptor) -> dict:
    results = {}
    for table, column, context in TARGETS:
        results[f"{table}.{column}"] = await backfill_column(
            conn, table, column, context, encryptor
        )
    return results


async def _main() -> None:
    encryptor = require_encryptor()
    engine = create_async_engine(_database_url(), pool_size=1, max_overflow=0)
    try:
        async with engine.connect() as conn:
            results = await backfill_all(conn, encryptor)
        for key, n in results.items():
            print(f"{key}: encrypted {n} rows")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(_main())
