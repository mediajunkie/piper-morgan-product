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
    """A live, recording backend in keyring's global, with the test run's own backend
    seam removed, so the service behaves as it does in a real process."""
    backend = RecordingKeyring()
    previous = keyring.get_keyring()
    keyring.set_keyring(backend)
    monkeypatch.setattr(ks, "_test_keyring_backend", None)
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


def test_an_explicit_db_wins_over_the_test_backend(live_keyring, db_store, monkeypatch):
    seam = RecordingKeyring()
    monkeypatch.setattr(ks, "_test_keyring_backend", seam)
    assert ks.selected_store() == "keychain"  # unset + a test backend
    monkeypatch.setenv(ks.STORE_ENV_VAR, "db")
    assert ks.selected_store() == "db"
    ks.KeychainService().get_api_key("anthropic")
    assert seam.calls == [] and live_keyring.calls == []


@pytest.mark.parametrize("store", [None, "keychain"])
def test_with_the_seam_set_nothing_reaches_keyrings_global(live_keyring, monkeypatch, store):
    """Arch's pin. The seam carries the backend: with it set, a read, a write and a
    delete touch only it, whatever keyring's global holds (here a recorder standing in
    for a real keyring that a test replaced or a reload restored), and the global is
    never even looked up. True with the store unset and with it set to keychain."""
    seam = RecordingKeyring()
    monkeypatch.setattr(ks, "_test_keyring_backend", seam)
    if store:
        monkeypatch.setenv(ks.STORE_ENV_VAR, store)
    svc = ks.KeychainService()
    assert svc._db_store is None and svc._no_secure_store is None
    svc.store_api_key("anthropic", "fake-value")
    assert svc.get_api_key("anthropic") == "fake-value"
    assert svc.read_secret("anthropic").is_present
    assert svc.delete_api_key("anthropic") is True
    assert {c[0] for c in seam.calls} == {"set", "get", "delete"}
    assert live_keyring.calls == [] and live_keyring.looked_up == []


def test_nothing_outside_tests_assigns_the_test_backend():
    """Arch's ratchet: the seam is set by tests/ only. Production code may read it in
    keychain_service.py and nowhere assigns it a value other than its ``None`` default."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    assign = re.compile(r"_test_keyring_backend\s*(?::[^=\n]*)?=(?!=)")
    offenders = []
    for folder in ("services", "web", "cli", "scripts", "config"):
        for path in (root / folder).rglob("*.py"):
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if assign.search(line) or "setattr" in line and "_test_keyring_backend" in line:
                    offenders.append(f"{path.relative_to(root)}:{n}: {line.strip()}")
    offenders += [
        f"main.py:{n}"
        for n, line in enumerate((root / "main.py").read_text().splitlines(), 1)
        if "_test_keyring_backend" in line
    ]
    assert offenders == [
        "services/infrastructure/keychain_service.py:"
        + str(
            next(
                n
                for n, line in enumerate(
                    (root / "services/infrastructure/keychain_service.py").read_text().splitlines(),
                    1,
                )
                if line.startswith("_test_keyring_backend: Optional[Any] = None")
            )
        )
        + ": _test_keyring_backend: Optional[Any] = None"
    ], offenders


def test_the_seam_is_not_an_environment_variable():
    """A child process inherits os.environ; the test run's opt-in must not travel."""
    src = open("tests/conftest.py").read()
    assert "_test_keyring_backend = backend" in src
    assert 'os.environ["PIPER_CREDENTIAL_STORE"] = "keychain"' not in src
    assert 'setdefault("PIPER_CREDENTIAL_STORE", "keychain")' not in src
