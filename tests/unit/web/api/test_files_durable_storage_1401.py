"""#1401 durable uploads + #1450 download decrypt.

Three properties pinned:
- ``get_upload_base()`` reads UPLOAD_DIR at call time (hosted deploys point it
  at the Fly volume; local dev keeps the relative ``uploads/`` default), and
  ``save_file_to_storage`` writes under it.
- ``download_file`` reads through the #1306 decrypt seam (#1450: FileResponse
  streamed raw disk bytes — PMENC1: ciphertext on any key-bearing deploy).
- ``download_file`` on a DB row whose bytes are gone (pre-volume upload wiped
  by a deploy) returns an honest 410 with a re-upload message, not a confusing
  404/500 (the #1401 read-side AC).

Download tests are DB-backed on the dev Postgres (B15/#1421 house pattern):
real users + uploaded_files rows, route function called directly.
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.file_context.storage import (
    get_upload_base,
    save_file_to_storage,
    write_file_to_storage,
)
from web.api.routes.files import download_file

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"

# Any 32-byte urlsafe-b64 key is a valid FieldEncryptionService master key.
_TEST_KEY = "x" * 43 + "="


class TestGetUploadBase:
    def test_default_is_relative_uploads(self):
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("UPLOAD_DIR", None)
            assert get_upload_base() == Path("uploads")

    def test_env_override_wins(self):
        with patch.dict(os.environ, {"UPLOAD_DIR": "/data/uploads"}):
            assert get_upload_base() == Path("/data/uploads")

    @pytest.mark.asyncio
    async def test_save_writes_under_env_base(self, tmp_path):
        base = tmp_path / "vol" / "uploads"
        with patch.dict(os.environ, {"UPLOAD_DIR": str(base)}):
            stored = await save_file_to_storage(b"hello volume", filename="probe.txt")
        assert Path(stored).is_file()
        assert Path(stored).parent == base  # created parents included


@pytest.fixture
async def file_owner():
    """One user row; yields (factory, user_id); cleans up rows it made."""
    engine = create_async_engine(_DB_URL, echo=False)
    factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    uid = str(uuid4())
    now = datetime.now(timezone.utc)
    async with factory() as s:
        await s.execute(
            text(
                "INSERT INTO users (id, username, email, is_active, is_verified, "
                "created_at, updated_at, role, is_alpha) "
                "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
            ),
            {"id": uid, "u": f"f1401_{uid[:8]}", "e": f"f1401_{uid[:8]}@test.example.com", "now": now},
        )
        await s.commit()
    try:
        yield factory, uid
    finally:
        async with factory() as s:
            await s.execute(
                text("DELETE FROM uploaded_files WHERE owner_id = CAST(:u AS uuid)"), {"u": uid}
            )
            await s.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid})
            await s.commit()
        await engine.dispose()


async def _insert_file_row(factory, uid: str, storage_path: str, filename: str) -> str:
    fid = f"file_{uuid4().hex[:12]}"
    async with factory() as s:
        await s.execute(
            text(
                "INSERT INTO uploaded_files (id, owner_id, filename, file_type, "
                "file_size, storage_path, upload_time) "
                "VALUES (:id, CAST(:o AS uuid), :fn, 'text/plain', 12, :sp, :now)"
            ),
            {
                "id": fid,
                "o": uid,
                "fn": filename,
                "sp": storage_path,
                "now": datetime.now(timezone.utc),
            },
        )
        await s.commit()
    return fid


class TestDownloadFile:
    @pytest.mark.asyncio
    async def test_download_decrypts_at_rest_ciphertext(self, file_owner, tmp_path):
        """#1450: with a master key set, disk holds PMENC1: ciphertext but the
        download must return the user's original bytes."""
        factory, uid = file_owner
        plaintext = b"the original document body"
        blob = tmp_path / "doc.txt"
        with patch.dict(os.environ, {"ENCRYPTION_MASTER_KEY": _TEST_KEY}):
            write_file_to_storage(blob, plaintext)
            assert blob.read_bytes().startswith(b"PMENC1:")  # really encrypted at rest
            fid = await _insert_file_row(factory, uid, str(blob), "doc.txt")
            request = SimpleNamespace(state=SimpleNamespace(user_id=uid, is_admin=False))
            resp = await download_file(fid, request=request)
        assert resp.body == plaintext
        assert 'filename="doc.txt"' in resp.headers["content-disposition"]

    @pytest.mark.asyncio
    async def test_missing_blob_is_honest_410(self, file_owner):
        """#1401 read-side AC: row survived, bytes didn't — say so plainly."""
        factory, uid = file_owner
        fid = await _insert_file_row(
            factory, uid, "uploads/ghost/20260701_gone.txt", "gone.txt"
        )
        request = SimpleNamespace(state=SimpleNamespace(user_id=uid, is_admin=False))
        with pytest.raises(HTTPException) as exc:
            await download_file(fid, request=request)
        assert exc.value.status_code == 410
        assert "upload it again" in exc.value.detail
