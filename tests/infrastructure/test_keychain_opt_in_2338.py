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
that product modules imported by other tests never construct a KeychainService;
the in-memory swap (last three tests) is what keeps such a service off the OS keyring.
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


# ── no test reads or writes the OS keyring either ──────────────────────────────


class _FakeOSKeyring:
    """A live-looking OS backend (its module name has no "fail" in it) that must
    never be reached once the default configure has run."""

    def __init__(self):
        self.calls = []

    def get_password(self, service, username):
        self.calls.append(("get", service, username))
        return "a-real-secret"

    def set_password(self, service, username, password):
        self.calls.append(("set", service, username))

    def delete_password(self, service, username):
        self.calls.append(("delete", service, username))


@pytest.fixture
def fake_os_keyring():
    import keyring
    from keyring.backend import KeyringBackend

    class FakeOS(_FakeOSKeyring, KeyringBackend):
        priority = 1

        def __init__(self):
            KeyringBackend.__init__(self)
            _FakeOSKeyring.__init__(self)

    before = keyring.get_keyring()
    fake = FakeOS()
    keyring.set_keyring(fake)
    try:
        yield fake
    finally:
        keyring.set_keyring(before)


def test_default_configure_swaps_a_live_os_keyring_for_an_in_memory_one(
    env_without_keys, fake_os_keyring
):
    import keyring

    conftest_mod = _load_root_conftest()
    conftest_mod.pytest_configure(config=None)

    assert getattr(keyring.get_keyring(), "piper_test_in_memory", False) is True
    keyring.set_password("piper-morgan", "slack_bot", "xoxb-test-token")
    assert keyring.get_password("piper-morgan", "slack_bot") == "xoxb-test-token"
    assert keyring.get_password("piper-morgan", "anthropic") is None
    keyring.delete_password("piper-morgan", "slack_bot")
    assert fake_os_keyring.calls == []


def test_opted_in_reads_first_then_swaps_so_nothing_is_written(env_without_keys, fake_os_keyring):
    """Arch 11:39: the opt-in grants reading, not writing."""
    import keyring

    os.environ[_OPT_IN] = "1"
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
    assert os.environ["ANTHROPIC_API_KEY"] == "real-anthropic"  # read happened first
    assert getattr(keyring.get_keyring(), "piper_test_in_memory", False) is True
    keyring.set_password("piper-morgan", "slack_bot", "xoxb-test-token")
    assert [c for c in fake_os_keyring.calls if c[0] in ("set", "delete")] == []


def test_a_dead_backend_is_not_replaced(env_without_keys):
    """CI's keyring is the fail backend; the database fallback must stay in charge."""
    import keyring
    from keyring.backends.fail import Keyring as FailKeyring

    before = keyring.get_keyring()
    dead = FailKeyring()
    keyring.set_keyring(dead)
    try:
        conftest_mod = _load_root_conftest()
        assert conftest_mod._use_in_memory_keyring() is False
        assert keyring.get_keyring() is dead
    finally:
        keyring.set_keyring(before)


# ── an app process a test starts never reads the keychain either ───────────────


def test_child_app_env_forces_the_database_store_by_default(env_without_keys):
    os.environ.pop("PIPER_CREDENTIAL_STORE", None)
    conftest_mod = _load_root_conftest()
    env = conftest_mod.child_app_env()
    assert env["PIPER_CREDENTIAL_STORE"] == "db"
    assert "PIPER_CREDENTIAL_STORE" not in os.environ  # the parent keeps the swap


def test_child_app_env_keeps_an_explicit_store_and_a_given_base(env_without_keys):
    conftest_mod = _load_root_conftest()
    env = conftest_mod.child_app_env({"PIPER_CREDENTIAL_STORE": "keychain", "X": "1"})
    assert env == {"PIPER_CREDENTIAL_STORE": "keychain", "X": "1"}


def test_child_app_env_forces_the_database_store_when_opted_in_too(env_without_keys):
    """Arch 11:51: read-not-write holds in child processes; keys go by environment."""
    os.environ.pop("PIPER_CREDENTIAL_STORE", None)
    os.environ[_OPT_IN] = "1"
    os.environ["ANTHROPIC_API_KEY"] = "loaded-by-the-opt-in"
    conftest_mod = _load_root_conftest()
    env = conftest_mod.child_app_env()
    assert env["PIPER_CREDENTIAL_STORE"] == "db"
    assert env["ANTHROPIC_API_KEY"] == "loaded-by-the-opt-in"


def _load_live_conftest():
    path = Path(__file__).resolve().parents[1] / "live" / "conftest.py"
    spec = importlib.util.spec_from_file_location("_live_conftest_2338", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_live_harness_strips_an_empty_anthropic_key_but_passes_a_real_one():
    live = _load_live_conftest()
    poison = {
        "ANTHROPIC_API_KEY": "",
        "ANTHROPIC_BASE_URL": "http://shell-proxy",
        "ANTHROPIC_AUTH_TOKEN": "t",
        "ANTHROPIC_CUSTOM_HEADERS": "h",
        "KEEP": "1",
    }
    assert live.scrub_child_env(dict(poison)) == {"KEEP": "1"}
    assert live.scrub_child_env({"ANTHROPIC_API_KEY": "   "}) == {}
    real = live.scrub_child_env({"ANTHROPIC_API_KEY": "a-real-key", "ANTHROPIC_BASE_URL": "x"})
    assert real == {"ANTHROPIC_API_KEY": "a-real-key"}


def test_every_test_harness_that_starts_main_py_uses_child_app_env():
    """Any test file that starts ``main.py`` as a child must build the child's
    environment through ``app_child_env`` (the two known today, and any new one)."""
    tests_root = Path(__file__).resolve().parents[1]
    starters = []
    for path in tests_root.rglob("*.py"):
        if path == Path(__file__).resolve():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if 'sys.executable, "main.py"' in text or '"python", "main.py"' in text:
            starters.append(path)
    assert sorted(p.relative_to(tests_root).as_posix() for p in starters) == [
        "integration/test_startup.py",
        "live/conftest.py",
    ]
    for path in starters:
        assert "app_child_env" in path.read_text(encoding="utf-8"), path
