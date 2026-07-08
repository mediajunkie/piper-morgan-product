"""#1306 — the uploaded-file byte seam (encrypt-on-write, decrypt-on-read).

The drift guard itself lives in tests/test_architecture_enforcement.py
(TestUploadedFileByteSeamEnforcement, injected-regression-proven); this file
covers the seam's behavior + the backfill's in-place conversion.
"""

import base64
import os

import pytest

from services.file_context.storage import read_file_from_storage, write_file_to_storage
from services.security.encrypted_types import MARKER
from services.security.field_encryption import DecryptionError

_MARKER_BYTES = MARKER.encode("ascii")


@pytest.fixture
def keyed_env(monkeypatch):
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(os.urandom(32)).decode())


@pytest.fixture
def keyless_env(monkeypatch):
    monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)


def test_write_then_read_round_trips_binary(keyed_env, tmp_path):
    p = tmp_path / "doc.pdf"
    content = b"%PDF-1.4 " + os.urandom(2048) + b"\x00\xff"
    write_file_to_storage(p, content)
    on_disk = p.read_bytes()
    assert on_disk.startswith(_MARKER_BYTES)
    assert content not in on_disk  # ciphertext at rest
    assert read_file_from_storage(p) == content


def test_legacy_plaintext_file_reads_through(keyed_env, tmp_path):
    p = tmp_path / "legacy.pdf"
    content = b"%PDF-1.4 legacy plaintext"
    p.write_bytes(content)  # pre-#1306 file, raw on disk
    assert read_file_from_storage(p) == content


def test_keyless_read_fails_closed(monkeypatch, tmp_path):
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(os.urandom(32)).decode())
    p = tmp_path / "doc.pdf"
    write_file_to_storage(p, b"secret bytes")
    monkeypatch.delenv("ENCRYPTION_MASTER_KEY")
    with pytest.raises(DecryptionError):
        read_file_from_storage(p)


def test_keyless_write_stores_plaintext_nonprod_fallback(keyless_env, tmp_path):
    p = tmp_path / "doc.pdf"
    write_file_to_storage(p, b"local dev content")
    assert p.read_bytes() == b"local dev content"
    assert read_file_from_storage(p) == b"local dev content"


def test_backfill_converts_legacy_in_place_idempotently(monkeypatch, tmp_path):
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(os.urandom(32)).decode())
    from scripts.backfill_encrypt_files_1306 import encrypt_file_in_place, require_encryptor

    enc = require_encryptor()
    p = tmp_path / "legacy.pdf"
    p.write_bytes(b"legacy plaintext bytes")
    assert encrypt_file_in_place(p, enc) == "encrypted"
    assert p.read_bytes().startswith(_MARKER_BYTES)
    assert read_file_from_storage(p) == b"legacy plaintext bytes"
    assert encrypt_file_in_place(p, enc) == "already"  # idempotent
    assert encrypt_file_in_place(tmp_path / "gone.pdf", enc) == "missing"
