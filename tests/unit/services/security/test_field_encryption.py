"""#358 SEC-ENCRYPT-ATREST — FieldEncryptionService (AES-256-GCM, HKDF per-field).

Security-critical. These guard the load-bearing properties: authenticated encryption
(tamper-detection via the GCM tag), per-field key isolation (HKDF context label), nonce
uniqueness, a hard error on a weak/short master key, and no key/plaintext leak in repr.
"""
import base64

import pytest

from services.security.field_encryption import DecryptionError, FieldEncryptionService

KEY = bytes(range(32))  # 32-byte AES-256 test key
CTX = "user_api_keys.secret"


def _svc(key: bytes = KEY) -> FieldEncryptionService:
    return FieldEncryptionService(key)


def test_round_trip():
    s = _svc()
    token = s.encrypt("sk-ant-secret-123", CTX)
    assert s.decrypt(token, CTX) == "sk-ant-secret-123"


def test_token_does_not_contain_plaintext():
    s = _svc()
    token = s.encrypt("sk-ant-secret-123", CTX)
    assert "sk-ant-secret-123" not in token
    assert b"sk-ant-secret-123" not in base64.b64decode(token)


def test_tamper_is_detected():
    s = _svc()
    token = s.encrypt("sk-secret", CTX)
    raw = bytearray(base64.b64decode(token))
    raw[-1] ^= 0x01  # flip a GCM tag byte
    tampered = base64.b64encode(bytes(raw)).decode()
    with pytest.raises(DecryptionError):
        s.decrypt(tampered, CTX)


def test_per_field_isolation():
    s = _svc()
    token = s.encrypt("sk-secret", "ctx.a")
    with pytest.raises(DecryptionError):
        s.decrypt(token, "ctx.b")  # different HKDF subkey → auth fails


def test_nonce_uniqueness():
    s = _svc()
    assert s.encrypt("same", CTX) != s.encrypt("same", CTX)


def test_wrong_master_key_cannot_decrypt():
    token = _svc(bytes([1]) * 32).encrypt("sk", CTX)
    with pytest.raises(DecryptionError):
        _svc(bytes([2]) * 32).decrypt(token, CTX)


def test_short_master_key_raises():
    with pytest.raises(ValueError):
        FieldEncryptionService(b"too-short")


def test_no_key_or_plaintext_in_repr():
    s = _svc(b"A" * 32)
    r = repr(s)
    assert "AAAA" not in r
    assert base64.b64encode(b"A" * 32).decode() not in r


def test_unicode_round_trip():
    s = _svc()
    pt = "ключ-🔑-café"
    assert s.decrypt(s.encrypt(pt, CTX), CTX) == pt
