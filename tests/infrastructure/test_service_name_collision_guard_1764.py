"""#1764 — the DB credential store has no service_name namespace; guard it loudly.

The defect (found by the #1748 lane): the OS keyring namespaces credentials by
(service_name, account); ``EncryptedDBCredentialStore`` keys rows by bare composed name.
A ``KeychainService(service_name='anything-else')`` routed to the DB store therefore
reads and writes the DEFAULT namespace's rows — silent cross-namespace collision, the
honest-empty family's silent-mask shape at the credential layer.

Until namespace parity exists (migration plan on #1764 — non-trivial because the
encryption context binds the bare name, so renaming rows means decrypt/re-encrypt),
the contract is: **a non-default service_name may not use the DB backend.** These tests
pin the guard from both sides.
"""

import pytest

from services.infrastructure.keychain_service import SERVICE_NAME, KeychainService


class TestServiceNameCollisionGuard:
    def test_custom_service_name_refuses_db_store(self, monkeypatch):
        """Forcing the DB store with a custom namespace raises loudly at construction."""
        monkeypatch.setenv("PIPER_CREDENTIAL_STORE", "db")
        with pytest.raises(RuntimeError, match="1764"):
            KeychainService(service_name="piper-somewhere-else")

    def test_default_service_name_still_reaches_db_store_path(self, monkeypatch):
        """The default namespace takes the DB path exactly as before (no regression).

        Construction either succeeds with the DB store engaged (ENCRYPTION_MASTER_KEY
        present, e.g. CI) or degrades to the no-secure-store state (key absent, e.g. a
        bare dev shell) — both are the pre-guard behaviors; the guard must introduce
        no third outcome for the default name.
        """
        monkeypatch.setenv("PIPER_CREDENTIAL_STORE", "db")
        svc = KeychainService()  # default service_name — must NOT raise the 1764 guard
        assert (svc._db_store is not None) or (svc._no_secure_store is not None)

    def test_custom_service_name_on_forced_keyring_unaffected(self, monkeypatch):
        """The #1711 pattern (custom namespace + forced OS keyring) stays legal."""
        monkeypatch.setenv("PIPER_CREDENTIAL_STORE", "keychain")
        svc = KeychainService(service_name="piper-test-1764-keyring")
        assert svc._db_store is None
