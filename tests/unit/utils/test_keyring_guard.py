"""HOST 2026-11-17: the guard that keeps keychain-store tests off a real keychain.

These tests never construct ``KeychainService`` and never call a keyring's get, set or
delete. They set which backend object is installed and read the guard's answer.
"""

import keyring
import pytest
from keyring.backend import KeyringBackend
from keyring.backends.fail import Keyring as FailKeyring

from services.infrastructure import keychain_service
from tests.utils import keyring_guard


class _InMemory:
    piper_test_in_memory = True


class _LooksLikeAnOSKeyring(KeyringBackend):
    priority = 1  # type: ignore[assignment]

    def get_password(self, service, username):  # pragma: no cover - never called
        raise AssertionError("the guard must not read a secret")

    def set_password(self, service, username, password):  # pragma: no cover
        raise AssertionError("the guard must not write a secret")

    def delete_password(self, service, username):  # pragma: no cover
        raise AssertionError("the guard must not delete a secret")


@pytest.fixture
def installed(monkeypatch):
    """Install a keyring backend object for one test and put the old one back."""
    before = keyring.get_keyring()

    def install(backend):
        keyring.set_keyring(backend)

    yield install
    keyring.set_keyring(before)


def test_with_the_in_memory_backend_in_place_nothing_real_can_be_reached(monkeypatch, installed):
    monkeypatch.setattr(keychain_service, "_test_keyring_backend", _InMemory())
    installed(_LooksLikeAnOSKeyring())
    assert keyring_guard.a_real_keyring_could_be_reached() is False


def test_with_no_swap_and_a_live_os_keyring_the_test_is_skipped(monkeypatch, installed):
    monkeypatch.setattr(keychain_service, "_test_keyring_backend", None)
    installed(_LooksLikeAnOSKeyring())
    assert keyring_guard.a_real_keyring_could_be_reached() is True
    with pytest.raises(pytest.skip.Exception):
        keyring_guard.skip_if_a_real_keyring_could_be_reached()


def test_with_no_swap_and_no_os_keyring_the_test_runs_as_in_ci(monkeypatch, installed):
    monkeypatch.setattr(keychain_service, "_test_keyring_backend", None)
    installed(FailKeyring())
    assert keyring_guard.a_real_keyring_could_be_reached() is False
    keyring_guard.skip_if_a_real_keyring_could_be_reached()  # does not skip


@pytest.mark.parametrize(
    "name", ("test_service_name_collision_guard_1764.py", "test_keychain_opt_in_only_2353.py")
)
def test_the_two_files_that_rely_on_the_swap_carry_the_guard(name):
    from pathlib import Path

    source = (Path(__file__).resolve().parents[2] / "infrastructure" / name).read_text()
    assert "autouse=True" in source and "skip_if_a_real_keyring_could_be_reached()" in source
