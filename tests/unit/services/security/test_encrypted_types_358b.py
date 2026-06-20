"""#358-B Phase 1 — EncryptedString TypeDecorator tests (TDD).

Unit-level: exercises process_bind_param / process_result_value directly (no DB).
All tests inject the encryptor so behavior is deterministic regardless of the test
environment's ENCRYPTION_MASTER_KEY.
"""
import os

import pytest

from services.security.encrypted_types import MARKER, EncryptedString
from services.security.field_encryption import DecryptionError, FieldEncryptionService


def _svc():
    return FieldEncryptionService(os.urandom(32))


def test_round_trip_bind_then_result():
    svc = _svc()
    col = EncryptedString(context="t.col", encryptor=svc)
    stored = col.process_bind_param("hello secret", None)
    assert stored != "hello secret"
    assert stored.startswith(MARKER)
    assert col.process_result_value(stored, None) == "hello secret"


def test_none_passes_through_both_directions():
    col = EncryptedString(context="t.col", encryptor=_svc())
    assert col.process_bind_param(None, None) is None
    assert col.process_result_value(None, None) is None


def test_bind_writes_marker_prefixed_ciphertext():
    col = EncryptedString(context="t.col", encryptor=_svc())
    stored = col.process_bind_param("plaintext-value", None)
    assert stored.startswith(MARKER)
    assert "plaintext-value" not in stored


def test_result_on_unmarked_value_is_legacy_plaintext_passthrough():
    col = EncryptedString(context="t.col", encryptor=_svc())
    assert col.process_result_value("legacy plaintext", None) == "legacy plaintext"


def test_result_on_marked_but_tampered_raises():
    svc = _svc()
    col = EncryptedString(context="t.col", encryptor=svc)
    stored = col.process_bind_param("secret", None)
    tampered = stored[:-2] + ("AA" if not stored.endswith("AA") else "BB")
    with pytest.raises(DecryptionError):
        col.process_result_value(tampered, None)


def test_no_encryptor_bind_passes_through_plaintext():
    col = EncryptedString(context="t.col", encryptor=None)
    assert col.process_bind_param("plain", None) == "plain"


def test_no_encryptor_result_on_unmarked_passes_through():
    col = EncryptedString(context="t.col", encryptor=None)
    assert col.process_result_value("plain", None) == "plain"


def test_no_encryptor_result_on_marked_raises_not_silent_token():
    real = EncryptedString(context="t.col", encryptor=_svc())
    stored = real.process_bind_param("secret", None)
    keyless = EncryptedString(context="t.col", encryptor=None)
    with pytest.raises(DecryptionError):
        keyless.process_result_value(stored, None)


def test_per_context_isolation():
    svc = _svc()
    a = EncryptedString(context="t.cola", encryptor=svc)
    b = EncryptedString(context="t.colb", encryptor=svc)
    stored = a.process_bind_param("secret", None)
    with pytest.raises(DecryptionError):
        b.process_result_value(stored, None)


def test_cache_ok_is_true():
    assert EncryptedString.cache_ok is True


def test_empty_context_rejected():
    with pytest.raises(ValueError):
        EncryptedString(context="", encryptor=_svc())


def test_uninjected_column_resolves_from_env(monkeypatch):
    import base64

    key = base64.b64encode(os.urandom(32)).decode()
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", key)
    col = EncryptedString(context="t.col")  # no injection → resolves from_env per call
    stored = col.process_bind_param("secret", None)
    assert stored.startswith(MARKER)
    assert col.process_result_value(stored, None) == "secret"


def test_uninjected_column_without_key_passes_through(monkeypatch):
    monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)
    col = EncryptedString(context="t.col")
    assert col.process_bind_param("plain", None) == "plain"
