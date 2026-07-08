"""#1306 backfill — encrypt existing plaintext uploaded files on disk (zero-downtime).

Iterates uploaded_files rows' storage_paths (DB-known files only — orphans on
disk are unreachable through the product and are reported, not touched),
sniffs the marker, and encrypts unmarked files in place with the exact envelope
write_file_to_storage uses, so reads decrypt transparently mid-run.

Idempotent: marked files are skipped. REFUSES to run keyless.

    ENCRYPTION_MASTER_KEY=<base64-32B> POSTGRES_PORT=5433 \
        venv/bin/python -m scripts.backfill_encrypt_files_1306
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from services.security.encrypted_types import MARKER
from services.security.field_encryption import FieldEncryptionService

_CONTEXT = "uploaded_files.content"
_MARKER_BYTES = MARKER.encode("ascii")


def require_encryptor() -> FieldEncryptionService:
    enc = FieldEncryptionService.from_env()
    if enc is None:
        print("ERROR: ENCRYPTION_MASTER_KEY unset — refusing to run.", file=sys.stderr)
        raise SystemExit(1)
    return enc


def _database_url() -> str:
    user = os.getenv("POSTGRES_USER", "piper")
    password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    database = os.getenv("POSTGRES_DB", "piper_morgan")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


def encrypt_file_in_place(path: Path, encryptor: FieldEncryptionService) -> str:
    """Returns 'encrypted' | 'already' | 'missing'."""
    if not path.exists():
        return "missing"
    data = path.read_bytes()
    if data.startswith(_MARKER_BYTES):
        return "already"
    path.write_bytes(_MARKER_BYTES + encryptor.encrypt_bytes(data, _CONTEXT))
    return "encrypted"


async def _main() -> None:
    encryptor = require_encryptor()
    engine = create_async_engine(_database_url(), pool_size=1, max_overflow=0)
    counts = {"encrypted": 0, "already": 0, "missing": 0}
    try:
        async with engine.connect() as conn:
            rows = (
                await conn.execute(
                    text("SELECT storage_path FROM uploaded_files WHERE storage_path IS NOT NULL")
                )
            ).fetchall()
        for (storage_path,) in rows:
            counts[encrypt_file_in_place(Path(storage_path), encryptor)] += 1
    finally:
        await engine.dispose()
    print(f"uploaded files: {counts['encrypted']} encrypted, {counts['already']} already, {counts['missing']} missing-on-disk")


if __name__ == "__main__":
    asyncio.run(_main())
