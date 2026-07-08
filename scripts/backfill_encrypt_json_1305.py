"""#1305 backfill — encrypt existing plaintext JSON/JSONB rows (zero-downtime).

Sibling of scripts/backfill_encrypt_content_358b.py, adapted for JSON columns:

- **Full-value columns** (6): a plaintext row is any JSON value that is NOT a
  marker-prefixed JSON string; it becomes ``to_jsonb('PMENC1:<token>'::text)``
  — the exact shape ``EncryptedJSON.process_bind_param`` writes, so ORM reads
  decrypt transparently mid-run (the mixed state is safe throughout).
- **Leaf-split column** (``patterns.pattern_data``): a plaintext row is a JSON
  object without a marker-prefixed ``_enc`` leaf; it becomes
  ``{<whitelisted keys>: <original>, _enc: 'PMENC1:<token of the rest>'}`` —
  default-encrypt with the ratified plaintext whitelist, matching the ORM type.

Idempotent + resumable: encrypted rows stop matching the plaintext filter, so
batches advance without OFFSET and re-runs are no-ops. **No DDL** (the one
schema change, the topics-GIN drop, is migration f1305encjson).

REFUSES to run without ``ENCRYPTION_MASTER_KEY`` (would stamp the marker over
plaintext). Run:

    ENCRYPTION_MASTER_KEY=<base64-32B> POSTGRES_PORT=5433 \
        venv/bin/python -m scripts.backfill_encrypt_json_1305
"""

from __future__ import annotations

import asyncio
import json
import os
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from services.security.encrypted_types import MARKER
from services.security.field_encryption import FieldEncryptionService

# (table, column, context-label) — MUST mirror EncryptedJSON contexts in models.py.
# NOTE: conversation_turns' ORM attribute is turn_metadata but the DB column is "metadata".
FULL_VALUE_TARGETS = [
    ("conversations", "context", "conversations.context"),
    ("conversations", "topics", "conversations.topics"),
    ("conversation_turns", "entities", "conversation_turns.entities"),
    ("conversation_turns", "references", "conversation_turns.references"),
    ("conversation_turns", "context_used", "conversation_turns.context_used"),
    ("conversation_turns", "metadata", "conversation_turns.metadata"),
]

# Leaf-split target: whitelisted keys stay plaintext; the remainder encrypts under _enc.
LEAF_TABLE, LEAF_COLUMN, LEAF_CONTEXT = "learned_patterns", "pattern_data", "patterns.pattern_data"
LEAF_WHITELIST = ("action_type",)
ENC_KEY = "_enc"


def require_encryptor() -> FieldEncryptionService:
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


async def backfill_full_value(conn, table, column, context, encryptor, batch=500) -> int:
    """Encrypt whole-value plaintext rows in one column. Returns rows encrypted.

    Plaintext filter (Postgres): a row is ALREADY encrypted iff the JSON value
    is a string whose text starts with the marker — i.e.
    ``jsonb_typeof(col::jsonb) = 'string' AND (col::jsonb #>> '{}') LIKE 'PMENC1:%'``.
    Everything else non-NULL (objects, arrays, non-marker strings) is plaintext.
    """
    total = 0
    while True:
        rows = (
            await conn.execute(
                text(
                    f'SELECT id, "{column}"::text FROM {table} '
                    f'WHERE "{column}" IS NOT NULL AND NOT ('
                    f"  jsonb_typeof(\"{column}\"::jsonb) = 'string' "
                    f"  AND (\"{column}\"::jsonb #>> '{{}}') LIKE :marker"
                    f") LIMIT :lim"
                ),
                {"marker": MARKER + "%", "lim": batch},
            )
        ).fetchall()
        if not rows:
            break
        for rid, raw_json_text in rows:
            value = json.loads(raw_json_text)
            token = MARKER + encryptor.encrypt(json.dumps(value, default=str), context)
            await conn.execute(
                text(
                    f'UPDATE {table} SET "{column}" = to_jsonb(CAST(:v AS text)) WHERE id = :id'
                ),
                {"v": token, "id": rid},
            )
        await conn.commit()
        total += len(rows)
    return total


async def backfill_leaf_split(conn, encryptor, batch=500) -> int:
    """Encrypt pattern_data rows into the leaf-split shape. Returns rows encrypted.

    Plaintext filter: a row is ALREADY split iff it's an object whose ``_enc``
    leaf is a marker-prefixed string. Non-object values (legacy anomalies) get
    full-value treatment falls under the object branch too via the ORM's read
    passthrough — here we split objects and full-encrypt non-objects.
    """
    total = 0
    while True:
        rows = (
            await conn.execute(
                text(
                    f'SELECT id, "{LEAF_COLUMN}"::text FROM {LEAF_TABLE} '
                    f'WHERE "{LEAF_COLUMN}" IS NOT NULL AND NOT ('
                    f"  jsonb_typeof(\"{LEAF_COLUMN}\"::jsonb) = 'object' "
                    f"  AND COALESCE((\"{LEAF_COLUMN}\"::jsonb ->> '{ENC_KEY}') LIKE :marker, false)"
                    f") LIMIT :lim"
                ),
                {"marker": MARKER + "%", "lim": batch},
            )
        ).fetchall()
        if not rows:
            break
        for rid, raw_json_text in rows:
            value = json.loads(raw_json_text)
            if isinstance(value, dict):
                plain = {k: v for k, v in value.items() if k in LEAF_WHITELIST}
                rest = {k: v for k, v in value.items() if k not in LEAF_WHITELIST}
                plain[ENC_KEY] = MARKER + encryptor.encrypt(
                    json.dumps(rest, default=str), LEAF_CONTEXT
                )
                new_json = json.dumps(plain)
                await conn.execute(
                    text(
                        f'UPDATE {LEAF_TABLE} SET "{LEAF_COLUMN}" = CAST(:v AS json) '
                        f"WHERE id = :id"
                    ),
                    {"v": new_json, "id": rid},
                )
            else:
                # Non-object anomaly: full-value encrypt (the ORM read handles both shapes).
                token = MARKER + encryptor.encrypt(json.dumps(value, default=str), LEAF_CONTEXT)
                await conn.execute(
                    text(
                        f'UPDATE {LEAF_TABLE} SET "{LEAF_COLUMN}" = '
                        f"to_jsonb(CAST(:v AS text))::json WHERE id = :id"
                    ),
                    {"v": token, "id": rid},
                )
        await conn.commit()
        total += len(rows)
    return total


async def _main() -> None:
    encryptor = require_encryptor()
    engine = create_async_engine(_database_url(), pool_size=1, max_overflow=0)
    try:
        async with engine.connect() as conn:
            for table, column, context in FULL_VALUE_TARGETS:
                n = await backfill_full_value(conn, table, column, context, encryptor)
                print(f"{table}.{column}: encrypted {n} rows")
            n = await backfill_leaf_split(conn, encryptor)
            print(f"{LEAF_TABLE}.{LEAF_COLUMN}: leaf-split {n} rows")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(_main())
