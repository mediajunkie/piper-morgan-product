"""#1382 tier-2 — hosted credential store: KeychainService's encrypted-DB fallback.

The failure this guards: hosted Linux has no OS keyring backend (python-keyring
resolves to ``keyring.backends.fail.Keyring``), which killed OAuth token storage
and every keychain read on alpha (found live 2026-07-08). The fix routes
KeychainService through ``EncryptedDBCredentialStore`` when the OS backend is
dead — these tests pin the selection logic and the store's crypto behavior.

Store round-trip tests run against the REAL local Postgres (house pattern for
the encryption family — #358/#1305 proof layers) with unique-prefixed names and
teardown deletes; SQLite can't host the store (Postgres upsert + now()).
"""

import uuid
from unittest.mock import patch

import pytest

from services.security.field_encryption import FieldEncryptionService


class _DeadBackend:
    """Stands in for keyring.backends.fail.Keyring (module name carries 'fail')."""

    __module__ = "keyring.backends.fail"


class _AliveBackend:
    __module__ = "keyring.backends.macOS"


def _fresh_service(**env):
    """Construct KeychainService with a controlled keyring backend + env."""
    import os

    from services.infrastructure import keychain_service as mod

    with patch.dict(os.environ, env, clear=False):
        return mod.KeychainService()


class TestStoreSelection:
    def test_alive_backend_keeps_os_keychain(self):
        with patch("keyring.get_keyring", return_value=_AliveBackend()):
            svc = _fresh_service(PIPER_CREDENTIAL_STORE="")
        assert svc._db_store is None

    def test_dead_backend_with_encryptor_routes_to_db(self, monkeypatch):
        monkeypatch.setenv("ENCRYPTION_MASTER_KEY", "S" * 43 + "=")
        with patch("keyring.get_keyring", return_value=_DeadBackend()):
            svc = _fresh_service(PIPER_CREDENTIAL_STORE="")
        assert svc._db_store is not None

    def test_dead_backend_without_encryptor_fails_closed(self, monkeypatch):
        monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)
        with patch("keyring.get_keyring", return_value=_DeadBackend()):
            with pytest.raises(RuntimeError, match="secure credential store"):
                _fresh_service(PIPER_CREDENTIAL_STORE="")

    def test_forced_keychain_keeps_legacy_behavior_even_when_dead(self):
        with patch("keyring.get_keyring", return_value=_DeadBackend()):
            svc = _fresh_service(PIPER_CREDENTIAL_STORE="keychain")
        assert svc._db_store is None  # legacy path, legacy failure mode preserved


class TestEncryptedDBStoreRoundTrip:
    """Against real local Postgres (secure_credentials exists at head g1382creds)."""

    @pytest.fixture
    def store(self):
        from services.infrastructure.secure_credential_store import (
            EncryptedDBCredentialStore,
        )

        s = EncryptedDBCredentialStore(encryptor=FieldEncryptionService(b"T" * 32))
        self._names = []
        yield s
        for n in self._names:
            s.delete(n)

    def _name(self):
        n = f"test1382_{uuid.uuid4().hex[:12]}_api_key"
        self._names.append(n)
        return n

    def test_round_trip_and_ciphertext_at_rest(self, store):
        from sqlalchemy import text

        name = self._name()
        store.store(name, "sk-super-secret-value")
        assert store.get(name) == "sk-super-secret-value"
        with store._get_engine().connect() as c:
            raw = c.execute(
                text("SELECT encrypted_value FROM secure_credentials WHERE name=:n"),
                {"n": name},
            ).scalar()
        assert "sk-super-secret" not in raw

    def test_upsert_overwrites(self, store):
        name = self._name()
        store.store(name, "first")
        store.store(name, "second")
        assert store.get(name) == "second"

    def test_missing_returns_none_and_delete_semantics(self, store):
        name = self._name()
        assert store.get(name) is None
        store.store(name, "v")
        assert store.delete(name) is True
        assert store.delete(name) is False

    def test_context_isolation_between_names(self, store):
        # Ciphertext written under one name's HKDF context must not decrypt
        # under another name (per-name subkeys — same posture as #358).
        from sqlalchemy import text

        a, b = self._name(), self._name()
        store.store(a, "value-for-a")
        with store._get_engine().begin() as c:
            ct = c.execute(
                text("SELECT encrypted_value FROM secure_credentials WHERE name=:n"),
                {"n": a},
            ).scalar()
            c.execute(
                text(
                    "INSERT INTO secure_credentials (name, encrypted_value) "
                    "VALUES (:n, :v)"
                ),
                {"n": b, "v": ct},
            )
        with pytest.raises(Exception):
            store.get(b)

    def test_keyless_construction_refuses(self, monkeypatch):
        from services.infrastructure.secure_credential_store import (
            EncryptedDBCredentialStore,
        )

        monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)
        with pytest.raises(RuntimeError, match="ENCRYPTION_MASTER_KEY"):
            EncryptedDBCredentialStore()
