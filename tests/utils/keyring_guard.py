"""A guard for tests that construct ``KeychainService`` under the keychain store.

xian's rule (2026-11-11): nothing a seat runs reads or writes his login keychain. The
root conftest keeps to it by handing the service an in-memory keyring for the whole run.
HOST (2026-11-17) asked that a test which relies on that swap check it first, so a run
with conftests disabled can't reach an OS keyring by accident.

A test may run when either holds:
- the service's test backend is the conftest's in-memory one; or
- this host has no OS keyring at all (hosted Linux CI: keyring's "fail" backend), where
  there is nothing to reach and the database store is in charge.
Otherwise it skips.
"""

import keyring
import pytest


def a_real_keyring_could_be_reached() -> bool:
    from services.infrastructure import keychain_service

    if getattr(keychain_service._test_keyring_backend, "piper_test_in_memory", False):
        return False
    # Asks which backend class is installed; reads no secret.
    return "fail" not in keyring.get_keyring().__class__.__module__


def skip_if_a_real_keyring_could_be_reached() -> None:
    if a_real_keyring_could_be_reached():
        pytest.skip(
            "the in-memory keyring is not in place and this host has an OS keyring; "
            "this test never runs against a real keychain"
        )
