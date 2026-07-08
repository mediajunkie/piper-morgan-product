"""#1305 — EncryptedJSON TypeDecorator (full-value + leaf-split modes).

Unit-level: exercises process_bind_param / process_result_value directly (no DB),
mirroring test_encrypted_types_358b.py; all tests inject the encryptor. The
real-Postgres proof (the server-side ``pattern_data -> 'action_type'`` query
surviving the leaf-split, and the backfill) lives in
tests/unit/services/security/test_encrypted_json_pg_1305.py.
"""

import os

import pytest

from services.security.encrypted_types import MARKER, EncryptedJSON
from services.security.field_encryption import DecryptionError, FieldEncryptionService


def _svc():
    return FieldEncryptionService(os.urandom(32))


# --- full-value mode ---------------------------------------------------------


def test_full_value_dict_round_trip():
    col = EncryptedJSON(context="t.col", encryptor=_svc())
    original = {"user": "xian", "notes": ["a", "b"], "n": 3}
    stored = col.process_bind_param(original, None)
    assert isinstance(stored, str) and stored.startswith(MARKER)
    assert col.process_result_value(stored, None) == original


def test_full_value_list_round_trip():
    col = EncryptedJSON(context="t.col", encryptor=_svc())
    original = ["topic-a", "topic-b"]
    stored = col.process_bind_param(original, None)
    assert isinstance(stored, str) and stored.startswith(MARKER)
    assert col.process_result_value(stored, None) == original


def test_none_passes_through_both_directions():
    col = EncryptedJSON(context="t.col", encryptor=_svc())
    assert col.process_bind_param(None, None) is None
    assert col.process_result_value(None, None) is None


def test_legacy_plaintext_dict_and_list_pass_through_on_read():
    """Pre-backfill rows: raw dicts/lists (no marker anywhere) must read as-is."""
    col = EncryptedJSON(context="t.col", encryptor=_svc())
    assert col.process_result_value({"legacy": True}, None) == {"legacy": True}
    assert col.process_result_value(["legacy"], None) == ["legacy"]
    assert col.process_result_value("plain string", None) == "plain string"


def test_no_encryptor_bind_passes_through_plaintext():
    col = EncryptedJSON(context="t.col", encryptor=None)
    assert col.process_bind_param({"a": 1}, None) == {"a": 1}


def test_no_encryptor_read_of_marked_value_raises_not_silent_token():
    svc = _svc()
    writer = EncryptedJSON(context="t.col", encryptor=svc)
    stored = writer.process_bind_param({"secret": 1}, None)
    keyless = EncryptedJSON(context="t.col", encryptor=None)
    with pytest.raises(DecryptionError):
        keyless.process_result_value(stored, None)


def test_per_context_isolation():
    svc = _svc()
    a = EncryptedJSON(context="t.a", encryptor=svc)
    b = EncryptedJSON(context="t.b", encryptor=svc)
    stored = a.process_bind_param({"x": 1}, None)
    with pytest.raises(DecryptionError):
        b.process_result_value(stored, None)


def test_empty_context_rejected():
    with pytest.raises(ValueError):
        EncryptedJSON(context="")


# --- leaf-split mode (Arch's ratified condition: DEFAULT-encrypt) -------------


def _leaf_col(svc=None):
    return EncryptedJSON(
        context="patterns.pattern_data",
        plaintext_whitelist=("action_type",),
        encryptor=svc or _svc(),
    )


def test_leaf_split_keeps_whitelisted_key_plaintext_and_encrypts_rest():
    col = _leaf_col()
    original = {"action_type": "create_issue", "user_note": "PII here", "count": 2}
    stored = col.process_bind_param(original, None)
    # The stored shape: whitelisted key readable, everything else under _enc.
    assert stored["action_type"] == "create_issue"
    assert "user_note" not in stored
    assert "count" not in stored
    assert stored["_enc"].startswith(MARKER)
    # Round-trip restores the full object.
    assert col.process_result_value(stored, None) == original


def test_leaf_split_default_encrypts_a_NEW_unanticipated_key():
    """THE load-bearing Arch condition: a future PII field added to the payload
    must land encrypted BY DEFAULT — nobody updates any list. This is the
    injected-drift proof: 'ssn' was never anticipated anywhere."""
    col = _leaf_col()
    stored = col.process_bind_param(
        {"action_type": "x", "ssn": "000-00-0000"}, None
    )
    assert "ssn" not in stored  # not a plaintext leaf
    assert "000-00-0000" not in str(stored)  # value nowhere in the stored shape
    assert stored["_enc"].startswith(MARKER)


def test_leaf_split_read_of_legacy_unsplit_object_passes_through():
    """Pre-backfill pattern_data rows: plain objects without _enc read as-is."""
    col = _leaf_col()
    legacy = {"action_type": "x", "old_field": "still plaintext in DB"}
    assert col.process_result_value(legacy, None) == legacy


def test_leaf_split_keyless_read_of_split_row_raises():
    svc = _svc()
    writer = _leaf_col(svc)
    stored = writer.process_bind_param({"action_type": "x", "secret": 1}, None)
    keyless = EncryptedJSON(
        context="patterns.pattern_data",
        plaintext_whitelist=("action_type",),
        encryptor=None,
    )
    with pytest.raises(DecryptionError):
        keyless.process_result_value(stored, None)


def test_leaf_split_legacy_dict_with_non_marker_enc_key_passes_through():
    """A legacy object that HAPPENS to have an _enc key (not ours — no marker)
    must pass through, not be misparsed as ciphertext."""
    col = _leaf_col()
    odd = {"action_type": "x", "_enc": "just a weird field"}
    assert col.process_result_value(odd, None) == odd
