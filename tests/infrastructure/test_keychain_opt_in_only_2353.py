"""#2353 (Arch, 2026-11-12): the OS keychain is opt-in only.

With PIPER_CREDENTIAL_STORE unset, the keyring module is never called, even with a live
backend. Only PIPER_CREDENTIAL_STORE=keychain reaches it.
"""

import base64

import keyring
import pytest
from keyring.backend import KeyringBackend

from services.infrastructure import keychain_service as ks


class RecordingKeyring(KeyringBackend):
    """A live backend that records every call."""

    priority = 1  # type: ignore[assignment]

    def __init__(self):
        super().__init__()
        self.calls = []
        self.items = {}

    def get_password(self, service, username):
        self.calls.append(("get", username))
        return self.items.get(username)

    def set_password(self, service, username, password):
        self.calls.append(("set", username))
        self.items[username] = password

    def delete_password(self, service, username):
        self.calls.append(("delete", username))
        self.items.pop(username, None)


class FakeDbStore:
    def __init__(self):
        self.rows = {}

    def store(self, name, value):
        self.rows[name] = value

    def get(self, name):
        return self.rows.get(name)

    def delete(self, name):
        return self.rows.pop(name, None) is not None


@pytest.fixture
def live_keyring(monkeypatch):
    """A live, recording backend, with the test run's own process default removed."""
    backend = RecordingKeyring()
    previous = keyring.get_keyring()
    keyring.set_keyring(backend)
    monkeypatch.setattr(ks, "_process_default_store", None)
    monkeypatch.delenv(ks.STORE_ENV_VAR, raising=False)
    looked_up = []
    real = keyring.get_keyring
    monkeypatch.setattr(keyring, "get_keyring", lambda: looked_up.append(1) or real())
    backend.looked_up = looked_up
    yield backend
    keyring.set_keyring(previous)


@pytest.fixture
def db_store(monkeypatch):
    store = FakeDbStore()
    monkeypatch.setattr(
        "services.infrastructure.secure_credential_store.EncryptedDBCredentialStore",
        lambda *a, **k: store,
    )
    return store


@pytest.mark.parametrize("value", [None, "", "db", "DB", "auto", "anything"])
def test_unset_or_anything_else_never_touches_the_keyring(
    live_keyring, db_store, monkeypatch, value
):
    if value is not None:
        monkeypatch.setenv(ks.STORE_ENV_VAR, value)
    svc = ks.KeychainService()
    svc.store_api_key("anthropic", "fake-value")
    assert svc.get_api_key("anthropic") == "fake-value"
    assert svc.read_secret("openai").is_verified_absent
    svc.delete_api_key("anthropic")
    svc.list_stored_keys()
    assert live_keyring.calls == [] and live_keyring.looked_up == []
    assert svc._db_store is db_store


def test_unset_with_no_master_key_is_no_store_and_never_the_keyring(live_keyring, monkeypatch):
    monkeypatch.delenv("ENCRYPTION_MASTER_KEY", raising=False)
    monkeypatch.delenv("ENCRYPTION_SCOPED_SUBKEYS", raising=False)
    svc = ks.KeychainService()
    assert svc._db_store is None and svc._no_secure_store
    assert svc.get_api_key("anthropic") is None
    with pytest.raises(RuntimeError) as err:
        svc.store_api_key("anthropic", "fake-value")
    text = str(err.value)
    assert "ENCRYPTION_MASTER_KEY" in text and "PIPER_CREDENTIAL_STORE=keychain" in text
    assert "local_key_setup.py" in text and "fake-value" not in text
    assert live_keyring.calls == [] and live_keyring.looked_up == []


@pytest.mark.parametrize("value", ["keychain", " Keychain "])
def test_keychain_is_used_when_chosen(live_keyring, monkeypatch, value):
    monkeypatch.setenv(ks.STORE_ENV_VAR, value)
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", base64.b64encode(b"k" * 32).decode())
    svc = ks.KeychainService()
    assert svc._db_store is None and svc._no_secure_store is None
    svc.store_api_key("anthropic", "fake-value")
    assert svc.get_api_key("anthropic") == "fake-value"
    assert ("set", "anthropic_api_key") in live_keyring.calls
    assert ("get", "anthropic_api_key") in live_keyring.calls


def test_the_environment_wins_over_the_process_default(live_keyring, db_store, monkeypatch):
    monkeypatch.setattr(ks, "_process_default_store", "keychain")
    assert ks.selected_store() == "keychain"
    monkeypatch.setenv(ks.STORE_ENV_VAR, "db")
    assert ks.selected_store() == "db"
    ks.KeychainService().get_api_key("anthropic")
    assert live_keyring.calls == []


def test_the_process_default_is_not_an_environment_variable():
    """A child process inherits os.environ; the test run's opt-in must not travel."""
    src = open("tests/conftest.py").read()
    assert "_process_default_store" in src
    assert 'os.environ["PIPER_CREDENTIAL_STORE"] = "keychain"' not in src
    assert 'setdefault("PIPER_CREDENTIAL_STORE", "keychain")' not in src
