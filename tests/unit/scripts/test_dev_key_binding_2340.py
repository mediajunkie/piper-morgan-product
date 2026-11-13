"""#2340: the shared developer-key binder stays out of the OS keychain, binds only the
provider a run names, and refuses before the first call.

Arch's ruling (2026-11-11 18:28 PT, issuecomment-6812602076) with one variance found at
build time: the store must be set even when a key is named in the environment, because
with ``PIPER_CREDENTIAL_STORE`` unset the app's own provider selection reads the OS
keychain during a call.

Every key in this file is a made-up string, not a credential.
"""

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dev_key_binding as binder  # noqa: E402

BINDER_USERS = (
    "ethics_gate_run_2364.py",
    "inversion_phase0_baseline.py",
    "inversion_phase1_shadow_score.py",
    "inversion_phase2_gate.py",
    "inversion_phase3_surface2_floor_probe.py",
    "inversion_router_control.py",
    "probe_milestone_resolver.py",
    "router_batch.py",
    "routing_probe_1283.py",
    "run_probe_set_v0_1.py",
    "surface1_counterfactual_probe_1283.py",
)


class _RecordingStore:
    """Stands in for KeychainService; records which providers were asked for."""

    def __init__(self, keys=None):
        self.keys = keys or {}
        self.asked = []

    def get_api_key(self, provider):
        self.asked.append(provider)
        return self.keys.get(provider)


@pytest.fixture
def clean_env(monkeypatch):
    for var in ("PIPER_CREDENTIAL_STORE", "ANTHROPIC_API_KEY", "OPENAI_API_KEY"):
        monkeypatch.delenv(var, raising=False)
    return monkeypatch


@pytest.fixture
def no_store(monkeypatch):
    """Any credential-store lookup fails the test."""

    def _forbidden():
        raise AssertionError("the binder asked for the credential store")

    import services.infrastructure.keychain_service as ks

    monkeypatch.setattr(ks, "get_keychain_service", _forbidden)


@pytest.fixture
def store(monkeypatch):
    rec = _RecordingStore({"anthropic": "fake-db-anthropic", "openai": "fake-db-openai"})
    import services.infrastructure.keychain_service as ks

    monkeypatch.setattr(ks, "get_keychain_service", lambda: rec)
    return rec


def test_unset_store_refuses_without_touching_any_store(clean_env, no_store):
    with pytest.raises(SystemExit) as exc:
        with binder.developer_keys_bound(providers=("anthropic",)):
            pytest.fail("the block ran")
    assert "PIPER_CREDENTIAL_STORE" in str(exc.value)
    assert "Do not use the keychain" in str(exc.value)


def test_unset_store_refuses_even_with_a_key_in_the_environment(clean_env, no_store):
    clean_env.setenv("ANTHROPIC_API_KEY", "fake-env-anthropic")
    with pytest.raises(SystemExit):
        with binder.developer_keys_bound(providers=("anthropic",)):
            pytest.fail("the block ran")


def test_db_store_with_environment_key_binds_it_and_asks_no_store(clean_env, no_store):
    clean_env.setenv("PIPER_CREDENTIAL_STORE", "db")
    clean_env.setenv("ANTHROPIC_API_KEY", "fake-env-anthropic")
    with binder.developer_keys_bound(providers=("anthropic",)) as keys:
        assert keys == {"anthropic": "fake-env-anthropic"}


def test_db_store_without_environment_key_reads_only_the_named_provider(clean_env, store):
    clean_env.setenv("PIPER_CREDENTIAL_STORE", "db")
    with binder.developer_keys_bound(providers=("anthropic",)) as keys:
        assert keys == {"anthropic": "fake-db-anthropic"}
    assert store.asked == ["anthropic"]


def test_db_store_with_no_key_anywhere_refuses(clean_env, monkeypatch):
    clean_env.setenv("PIPER_CREDENTIAL_STORE", "db")
    import services.infrastructure.keychain_service as ks

    monkeypatch.setattr(ks, "get_keychain_service", lambda: _RecordingStore())
    with pytest.raises(SystemExit) as exc:
        with binder.developer_keys_bound(providers=("openai",)):
            pytest.fail("the block ran")
    assert "OPENAI_API_KEY" in str(exc.value)


def test_no_provider_named_refuses(clean_env, no_store):
    clean_env.setenv("PIPER_CREDENTIAL_STORE", "db")
    clean_env.setenv("ANTHROPIC_API_KEY", "fake-env-anthropic")
    with pytest.raises(SystemExit) as exc:
        with binder.developer_keys_bound(providers=binder.providers_from_flag(None)):
            pytest.fail("the block ran")
    assert "--provider" in str(exc.value)


def test_only_the_named_provider_is_bound_so_the_other_refuses_before_spend(clean_env, no_store):
    """Ask 2: a run asked for Anthropic stops, unbound, on a call that lands on OpenAI."""
    from services.llm.request_key import UnboundLLMKeyError, request_spend_key

    clean_env.setenv("PIPER_CREDENTIAL_STORE", "db")
    clean_env.setenv("ANTHROPIC_API_KEY", "fake-env-anthropic")
    clean_env.setenv("OPENAI_API_KEY", "fake-env-openai")
    with binder.developer_keys_bound(providers=("anthropic",)) as keys:
        assert set(keys) == {"anthropic"}
        assert request_spend_key("anthropic") == "fake-env-anthropic"
        with pytest.raises(UnboundLLMKeyError):
            request_spend_key("openai")


def test_dry_run_looks_nothing_up(clean_env, no_store):
    with binder.developer_keys_bound(providers=(), require=False) as keys:
        assert keys == {}


def test_planned_calls_line_names_count_and_provider():
    line = binder.planned_calls_line(120, ("anthropic",), "router calls")
    assert "120 router calls" in line and "anthropic" in line


def test_pop_provider_flag():
    argv = ["prog", "--provider", "openai", "out.md"]
    assert binder.pop_provider_flag(argv) == "openai"
    assert argv == ["prog", "out.md"]
    argv = ["prog", "--provider=anthropic"]
    assert binder.pop_provider_flag(argv) == "anthropic"
    assert argv == ["prog"]
    assert binder.pop_provider_flag(["prog"]) is None


def test_binder_itself_never_names_the_keyring_or_sets_the_store():
    src = (SCRIPTS / "dev_key_binding.py").read_text()
    assert "import keyring" not in src
    assert not re.search(r"os\.environ\[[\"']PIPER_CREDENTIAL_STORE[\"']\]\s*=", src)
    assert 'setdefault("PIPER_CREDENTIAL_STORE"' not in src


@pytest.mark.parametrize("name", BINDER_USERS)
def test_every_binder_user_names_its_providers(name):
    src = (SCRIPTS / name).read_text()
    calls = re.findall(r"developer_keys_bound\(([^)]*(?:\([^)]*\)[^)]*)*)\)", src)
    assert calls, f"{name} no longer uses the binder; update BINDER_USERS"
    for args in calls:
        assert "providers=" in args, f"{name}: developer_keys_bound({args}) names no provider"


def test_binder_user_list_is_complete():
    users = sorted(
        p.name
        for p in SCRIPTS.glob("*.py")
        if p.name != "dev_key_binding.py" and "developer_keys_bound" in p.read_text()
    )
    assert users == sorted(BINDER_USERS)


@pytest.mark.parametrize(
    "name",
    ("inversion_router_control.py", "inversion_phase1_shadow_score.py", "inversion_phase2_gate.py"),
)
def test_usage_text_no_longer_sends_keys_through_the_keychain(name):
    assert "keys resolve via Keychain" not in (SCRIPTS / name).read_text()


@pytest.mark.parametrize(
    "name", ("inversion_router_control.py", "inversion_phase1_shadow_score.py")
)
def test_the_two_screens_print_the_plan_before_the_first_call(name):
    src = (SCRIPTS / name).read_text()
    assert "planned_calls_line(" in src
    first_call = "route_all(rows, router_fn)" if "phase1" in name else "asyncio.run(_control("
    assert src.index("planned_calls_line(") < src.index(first_call)
