"""#2338: a test run reads the developer's keychain only when asked to.

xian's ruling (decisions.log 2026-11-11 11:12): nothing we run on his machine may
read his login keychain without his permission. ``tests/conftest.py`` used to copy
his OpenAI, Anthropic and GitHub credentials from the OS keyring into the
environment on every pytest run (#742, #914), and fall back to ``gh auth token``
(gh keeps its token in the login keychain on macOS). Arch's mechanism (11:16): off
by default, on only when ``PIPER_TESTS_USE_KEYCHAIN`` is set.

Layer: these call the real ``pytest_configure`` hook and the real
``_dev_keychain_or_none`` helper from ``tests/conftest.py`` with the keyring, the
keychain service and ``subprocess.run`` replaced by tripwires. They do not prove
that product modules imported by other tests never construct a KeychainService.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from unittest.mock import patch

import pytest

pytestmark = [pytest.mark.unit, pytest.mark.smoke]

_ROOT_CONFTEST = Path(__file__).resolve().parents[1] / "conftest.py"
_KEY_VARS = ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GITHUB_TOKEN")
_OPT_IN = "PIPER_TESTS_USE_KEYCHAIN"


def _load_root_conftest():
    spec = importlib.util.spec_from_file_location("_root_conftest_2338", _ROOT_CONFTEST)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tripwire(name):
    def _raise(*args, **kwargs):
        raise AssertionError(f"{name} was called without the #2338 opt-in")

    return _raise


@pytest.fixture
def env_without_keys():
    env = {k: v for k, v in os.environ.items() if k not in _KEY_VARS + (_OPT_IN,)}
    with patch.dict(os.environ, env, clear=True):
        yield


class _Keyring:
    """Stands in for an OS-keyring-backed KeychainService that holds real keys."""

    _db_store = None
    _no_secure_store = None

    def __init__(self):
        self.asked = []

    def get_api_key(self, provider, username=None):
        self.asked.append(provider)
        return f"real-{provider}"


@pytest.mark.parametrize("value", [None, "", "0", "false", "no", "off"])
def test_default_configure_never_touches_the_keyring_or_gh(env_without_keys, value):
    if value is not None:
        os.environ[_OPT_IN] = value
    conftest_mod = _load_root_conftest()
    with (
        patch("keyring.get_password", side_effect=_tripwire("keyring.get_password")) as get_pw,
        patch(
            "services.infrastructure.keychain_service.get_keychain_service",
            side_effect=_tripwire("get_keychain_service"),
        ) as get_service,
        patch("subprocess.run", side_effect=_tripwire("subprocess.run (gh auth token)")) as run,
    ):
        conftest_mod.pytest_configure(config=None)
    assert get_pw.call_count == 0
    assert get_service.call_count == 0
    assert run.call_count == 0
    assert [v for v in _KEY_VARS if os.environ.get(v)] == []


def test_keys_already_in_the_environment_are_left_alone(env_without_keys):
    os.environ["ANTHROPIC_API_KEY"] = "from-shell"
    conftest_mod = _load_root_conftest()
    with patch(
        "services.infrastructure.keychain_service.get_keychain_service",
        side_effect=_tripwire("get_keychain_service"),
    ):
        conftest_mod.pytest_configure(config=None)
    assert os.environ["ANTHROPIC_API_KEY"] == "from-shell"


@pytest.mark.parametrize("value", ["1", "true", "YES"])
def test_opted_in_the_load_works_as_before(env_without_keys, value):
    os.environ[_OPT_IN] = value
    service = _Keyring()
    conftest_mod = _load_root_conftest()
    with (
        patch(
            "services.infrastructure.keychain_service.get_keychain_service",
            return_value=service,
        ),
        patch("subprocess.run", side_effect=FileNotFoundError("gh disabled in pin")),
    ):
        conftest_mod.pytest_configure(config=None)
    assert service.asked == ["openai", "anthropic", "github_token"]
    assert os.environ["OPENAI_API_KEY"] == "real-openai"
    assert os.environ["ANTHROPIC_API_KEY"] == "real-anthropic"
    assert os.environ["GITHUB_TOKEN"] == "real-github_token"


def test_live_llm_fixture_gets_no_keychain_without_the_opt_in(env_without_keys):
    conftest_mod = _load_root_conftest()
    with patch(
        "services.infrastructure.keychain_service.KeychainService",
        side_effect=_tripwire("KeychainService()"),
    ) as ctor:
        assert conftest_mod._dev_keychain_or_none() is None
    assert ctor.call_count == 0


def test_live_llm_fixture_gets_the_keychain_when_opted_in(env_without_keys):
    os.environ[_OPT_IN] = "1"
    conftest_mod = _load_root_conftest()
    sentinel = object()
    with patch("services.infrastructure.keychain_service.KeychainService", return_value=sentinel):
        assert conftest_mod._dev_keychain_or_none() is sentinel
