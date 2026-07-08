"""Uploaded-file storage — the single byte-level seam (#1306).

As of #1306 (2026-07-08, Arch-ratified design), uploaded-file content is
encrypted at rest at THIS seam: every write goes through
``write_file_to_storage()`` (encrypt) and every read through
``read_file_from_storage()`` (decrypt) — the two functions below are the only
places in the codebase allowed to touch uploaded-file bytes on disk. A
grep-style enforcement test (``TestUploadedFileByteSeamEnforcement``) fails the
build if a byte-read/write of uploaded content appears anywhere else, so the
single-seam property Arch's ratification conditioned on can't silently drift.

Envelope: ``PMENC1:`` marker prefix (bytes) + AES-256-GCM via
``FieldEncryptionService.encrypt_bytes`` under the per-field HKDF context
``uploaded_files.content`` (one context for the column-equivalent, matching the
per-FIELD labeling of every #358/#1305 surface — not per-file). Marker-absent
files are legacy plaintext and read through unchanged (pre-backfill compat;
``scripts/backfill_encrypt_files_1306.py`` converts them). A marked file
without a key raises ``DecryptionError`` — fail closed, never return
ciphertext as content. No key at write time → plaintext + a warn-once (the
non-prod fallback, same as every sibling surface).
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from fastapi import UploadFile

from services.security.encrypted_types import MARKER
from services.security.field_encryption import DecryptionError, FieldEncryptionService

logger = logging.getLogger(__name__)

_FILE_CONTEXT = "uploaded_files.content"
_MARKER_BYTES = MARKER.encode("ascii")
_warned_no_key_files = False


def write_file_to_storage(file_path: Union[str, Path], content: bytes) -> None:
    """THE uploaded-file byte-write seam (#1306): encrypt-then-write.

    Every writer of uploaded-file bytes routes here (``save_file_to_storage``
    below + the upload route) — never a raw ``open(..., 'wb')`` elsewhere.
    """
    global _warned_no_key_files
    svc = FieldEncryptionService.from_env()
    if svc is None:
        if not _warned_no_key_files:
            logger.warning(
                "ENCRYPTION_MASTER_KEY unset — uploaded files stored as plaintext "
                "(non-prod fallback; the #1306 backfill refuses to run without the key)"
            )
            _warned_no_key_files = True
        data = content
    else:
        data = _MARKER_BYTES + svc.encrypt_bytes(content, _FILE_CONTEXT)
    with open(file_path, "wb") as f:
        f.write(data)


def read_file_from_storage(storage_path: Union[str, Path]) -> bytes:
    """THE uploaded-file byte-read seam (#1306): sniff-marker-then-decrypt.

    Marker-absent = legacy plaintext (pre-backfill), returned unchanged.
    Marker-present without a key raises ``DecryptionError`` (fail closed).
    """
    with open(storage_path, "rb") as f:
        data = f.read()
    if not data.startswith(_MARKER_BYTES):
        return data  # legacy plaintext (pre-backfill file)
    svc = FieldEncryptionService.from_env()
    if svc is None:
        raise DecryptionError(
            "encrypted uploaded file present but ENCRYPTION_MASTER_KEY is unset"
        )
    return svc.decrypt_bytes(data[len(_MARKER_BYTES) :], _FILE_CONTEXT)


async def save_file_to_storage(
    file: Union[UploadFile, bytes], filename: Optional[str] = None
) -> str:
    """Save uploaded file (encrypted at rest per #1306) and return storage path."""
    try:
        # Create upload directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)

        # Generate unique filename to avoid collisions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if isinstance(file, UploadFile):
            # Handle UploadFile object
            safe_filename = f"{timestamp}_{file.filename}"
            content = await file.read()
        else:
            # Handle bytes content
            safe_filename = f"{timestamp}_{filename or 'uploaded_file'}"
            content = file

        file_path = upload_dir / safe_filename

        # Save file through the #1306 encrypt seam
        write_file_to_storage(file_path, content)

        logger.info(f"File saved to storage: {file_path}")
        return str(file_path)

    except Exception as e:
        logger.error(f"Failed to save file to storage: {e}")
        raise


def delete_file_from_storage(storage_path: str) -> bool:
    """Delete file from storage"""
    try:
        file_path = Path(storage_path)
        if file_path.exists():
            file_path.unlink()
            logger.info(f"File deleted from storage: {storage_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete file from storage: {e}")
        return False


def get_file_size(storage_path: str) -> int:
    """Get file size in bytes (on-disk size — ciphertext size for encrypted files)"""
    try:
        file_path = Path(storage_path)
        if file_path.exists():
            return file_path.stat().st_size
        return 0
    except Exception as e:
        logger.error(f"Failed to get file size: {e}")
        return 0


def generate_session_id() -> str:
    """Generate a unique session ID"""
    return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.getpid()}"
