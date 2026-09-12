"""#1748 pin — test-written DB-store credentials must never become "real" keys.

The defect class this pins shut: in CI the runner's OS keyring is dead, so
``KeychainService`` routes to the #1382 ``EncryptedDBCredentialStore`` backed
by the shared per-job Postgres. That table is provisioned EMPTY every job, so
the only writers it can ever have had are tests — any credential found there
is test residue (``sk-test`` etc.), not a real key. But ``tests/conftest.py``'s
session-start key load (#742, "load developer keys from macOS Keychain") went
through the same ``KeychainService`` seam, so it happily retrieved the residue
and exported it as ``ANTHROPIC_API_KEY`` — un-skipping llm-marked tests and
handing garbage to live calls → 401s that read as product failures.

Observed live (Tests workflow run 34639901479, 2026-09-11, ubuntu runner):
    [info] Keychain service initialized backend=EncryptedDBCredentialStore
    [conftest] Loaded ANTHROPIC_API_KEY from keychain
The writer that run was the pre-fix #1711 suite: ``store_api_key("anthropic",
"sk-test")`` expected a raise, but auto-routed to the DB store and SUCCEEDED,
with no cleanup (fixed same day by forcing PIPER_CREDENTIAL_STORE=keychain in
its ``_isolate`` fixture — but the CLASS remained open for any future writer).

The rule these tests pin (read-side, closes the class for every writer):
conftest may treat ONLY a positively-confirmed OS-keyring-backed
KeychainService as a source of developer keys. DB-store-backed, degraded
(no-secure-store), and unrecognizable service shapes are all refused —
fail-safe, so an internals rename can only make tests skip, never make
residue load.

Layer note (m-43): these tests exercise the real ``pytest_configure`` hook
from ``tests/conftest.py`` against controlled fake KeychainService shapes and
a controlled env — no DB writes, no keyring calls. The store-selection logic
itself (dead backend → DB store) is pinned separately in
``tests/security/test_secure_credential_store_1382.py``. Deliberately NO
fake credential is ever written to a real shared store here: a pin that
polluted the store it guards would be the defect wearing a test's name.
"""

import importlib.util
import os
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.infrastructure.keychain_service import KeychainService

_ROOT_CONFTEST = Path(__file__).resolve().parents[1] / "conftest.py"

_KEY_VARS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN", "GH_TOKEN")

FAKE_RESIDUE = "sk-test-residue-from-a-prior-test"


def _load_root_conftest():
    """Import tests/conftest.py as a plain module (tests/ is not a package)."""
    spec = importlib.util.spec_from_file_location("_root_conftest_1748", _ROOT_CONFTEST)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _db_backed_service(value=FAKE_RESIDUE):
    """A KeychainService in the exact CI shape: routed to the #1382 DB store.

    Built via __new__ so no keyring/DB is touched; the fake store answers
    every name — the way a polluted secure_credentials table would.
    """
    svc = KeychainService.__new__(KeychainService)
    svc.service_name = "piper-morgan"
    svc._no_secure_store = None
    svc._db_store = SimpleNamespace(
        get=lambda name: value,
        store=lambda name, v: None,
        delete=lambda name: False,
    )
    return svc


def _os_backed_service(anthropic_key="sk-ant-real-from-os-keyring"):
    """A KeychainService in the local-dev shape: real OS keyring selected."""
    svc = KeychainService.__new__(KeychainService)
    svc.service_name = "piper-morgan"
    svc._no_secure_store = None
    svc._db_store = None
    # Shadow the method on the instance: the OS-keyring read path itself
    # (bounded _keyring_call etc.) is #1711's layer, not this pin's.
    svc.get_api_key = lambda provider, username=None: (
        anthropic_key if provider == "anthropic" else None
    )
    return svc


def _degraded_service():
    """The no-secure-store degraded state (dead backend, no master key)."""
    svc = KeychainService.__new__(KeychainService)
    svc.service_name = "piper-morgan"
    svc._db_store = None
    svc._no_secure_store = "no secure credential store (#1382)"
    # Real semantics already return None here; the pin asserts the guard
    # refuses BEFORE consulting the service at all, so answer loudly.
    svc.get_api_key = lambda provider, username=None: "must-never-be-exported"
    return svc


@pytest.fixture
def clean_env():
    """Run with the key env vars absent and restore everything after."""
    env = {k: v for k, v in os.environ.items() if k not in _KEY_VARS}
    with patch.dict(os.environ, env, clear=True):
        yield


@pytest.fixture
def no_gh_cli():
    """Keep conftest's `gh auth token` fallback from touching the real CLI."""
    with patch("subprocess.run", side_effect=FileNotFoundError("gh disabled in pin")):
        yield


def _run_configure_with(service, conftest_mod):
    with patch(
        "services.infrastructure.keychain_service.get_keychain_service",
        return_value=service,
    ):
        conftest_mod.pytest_configure(config=None)


class TestDBStoreResidueNeverBecomesReal:
    """The #1748 class itself: DB-store contents are not developer keys."""

    def test_db_store_backed_key_is_not_exported(self, clean_env, no_gh_cli):
        """A fresh resolution pass over a polluted DB store exports NOTHING.

        This is the survival pin the issue asks for: the fake store answers
        every composed name (openai_api_key, anthropic_api_key,
        github_token_api_key) exactly like a polluted secure_credentials
        table — and none of them may reach the environment.
        """
        conftest_mod = _load_root_conftest()
        _run_configure_with(_db_backed_service(), conftest_mod)
        for var in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN"):
            assert os.environ.get(var) is None, (
                f"{var} was exported from the #1382 DB store — test residue "
                "just became a 'real' credential (#1748 regression)"
            )

    def test_degraded_service_is_not_consulted(self, clean_env, no_gh_cli):
        """No-secure-store shape: refused by the guard, not by luck of None."""
        conftest_mod = _load_root_conftest()
        _run_configure_with(_degraded_service(), conftest_mod)
        for var in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN"):
            assert os.environ.get(var) is None

    def test_unrecognizable_service_shape_fails_safe(self, clean_env, no_gh_cli):
        """A service missing the store-selection attrs is NOT presumed OS-backed.

        Fail-safe direction: if KeychainService internals are renamed, the
        guard must degrade to 'skip loading' (tests skip, visibly), never to
        'assume OS keyring' (residue loads, silently).
        """
        conftest_mod = _load_root_conftest()
        stranger = SimpleNamespace(
            get_api_key=lambda provider, username=None: "sk-should-never-load"
        )
        _run_configure_with(stranger, conftest_mod)
        for var in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN"):
            assert os.environ.get(var) is None


class TestOSKeyringPathStillWorks:
    """Guard must not overcorrect: #742's dev-seat convenience stays intact."""

    def test_os_backed_key_still_loads(self, clean_env, no_gh_cli):
        conftest_mod = _load_root_conftest()
        _run_configure_with(_os_backed_service(), conftest_mod)
        assert os.environ.get("ANTHROPIC_API_KEY") == "sk-ant-real-from-os-keyring"
        assert os.environ.get("OPENAI_API_KEY") is None  # keyring had none

    def test_env_var_precedence_unchanged(self, clean_env, no_gh_cli):
        """A key already in the env is never overwritten by any store."""
        conftest_mod = _load_root_conftest()
        os.environ["ANTHROPIC_API_KEY"] = "sk-from-shell"
        _run_configure_with(_os_backed_service(), conftest_mod)
        assert os.environ["ANTHROPIC_API_KEY"] == "sk-from-shell"
