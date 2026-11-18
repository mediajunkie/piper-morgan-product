"""scripts/guide_keyed_steps_run.py (issue 2404, ADR-084 D2): the bounds Arch and CIO read
the driver against, pinned without Docker, a key or a provider.

Every key-shaped value here is made up at run time. Nothing starts a server.
"""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
SEAT_VALUE = "made-up-seat-value-" + "2404" * 6
INHERITED_VALUE = "made-up-inherited-value-" + "9f1c" * 6


def _load():
    name = "guide_keyed_steps_run"
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def g():
    return _load()


PARENT = {
    "PATH": "/usr/bin",
    "HOME": "/home/someone",
    "PIPER_SEAT_ANTHROPIC_KEY": SEAT_VALUE,
    "PIPER_SEAT_OPENAI_KEY": SEAT_VALUE,
    "ANTHROPIC_API_KEY": INHERITED_VALUE,
    "ANTHROPIC_BASE_URL": "http://inherited.invalid",
    "OPENAI_API_KEY": INHERITED_VALUE,
    "DATABASE_URL": "postgresql://piper:pw@localhost:5433/piper_morgan",
    "ALEMBIC_DATABASE_URL": "postgresql://piper:pw@localhost:5433/piper_morgan",
    "POSTGRES_DB": "piper_morgan",
    "REDIS_URL": "redis://localhost:6379",
    "ENCRYPTION_MASTER_KEY": "inherited-master",
    "PIPER_CREDENTIAL_STORE": "keychain",
    "JWT_SECRET_KEY": "inherited-jwt",
    "HTTPS_PROXY": "http://inherited-proxy.invalid",
    "LOG_LEVEL": "WARNING",
}
RUN_DB_URL = "postgresql://piper_guide_app_0a1b2c3d:pw@localhost:5433/piper_guide_run_0a1b2c3d"


# ── Arch 1 and 3, CIO 2: the environment every started process gets ─────────


@pytest.mark.parametrize("which", ["child", "server-real", "server-stub"])
def test_no_key_or_default_store_reaches_a_started_process(g, which):
    if which == "child":
        env = g.child_env(PARENT, db_url=RUN_DB_URL, master_key="run-master")
    else:
        stub = which == "server-stub"
        env = g.server_env(
            PARENT,
            db_url=RUN_DB_URL,
            master_key="run-master",
            port=61000,
            stub_url="http://127.0.0.1:61001" if stub else None,
            sink_url="http://127.0.0.1:61002" if stub else None,
        )
    assert not any(k.startswith("PIPER_SEAT_") for k in env)
    assert SEAT_VALUE not in env.values() and INHERITED_VALUE not in env.values()
    for name in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "ALEMBIC_DATABASE_URL", "POSTGRES_DB"):
        assert name not in env
    assert env["DATABASE_URL"] == RUN_DB_URL  # by name, never the default database
    assert "piper_morgan" not in env["DATABASE_URL"].rsplit("/", 1)[-1]
    assert env["PIPER_CREDENTIAL_STORE"] == "db"
    assert env["ENCRYPTION_MASTER_KEY"] == "run-master"
    assert env["PYTHON_DOTENV_DISABLED"] == "1"
    assert env["REDIS_URL"] == f"redis://localhost:6379/{g.REDIS_DB}"
    if which == "server-real":
        assert "ANTHROPIC_BASE_URL" not in env
        assert "HTTPS_PROXY" not in env and "https_proxy" not in env
        assert env["LOG_LEVEL"] == "INFO"  # the llm_usage lines COST is read from
        assert env["JWT_SECRET_KEY"] != "inherited-jwt"
    if which == "server-stub":
        assert env["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:61001"
        assert env["HTTPS_PROXY"] == env["https_proxy"] == "http://127.0.0.1:61002"


def test_redis_database_is_not_the_shared_default(g):
    assert g.REDIS_DB != 0


def test_master_key_is_made_for_the_run(g):
    import base64

    a, b = g.new_master_key(), g.new_master_key()
    assert a != b and len(base64.b64decode(a)) == 32


def test_run_names_are_the_runs_own(g):
    db, role = g.run_names("0a1b2c3d")
    assert db == "piper_guide_run_0a1b2c3d" and role == "piper_guide_app_0a1b2c3d"
    with pytest.raises(ValueError):
        g.run_names("piper_morgan")


def test_leftovers_are_named_by_the_runs_prefixes_only(g):
    dbs, roles = g.leftover_names(
        "piper_morgan\npiper_guide_run_aa11bb22\npiper_fault_run",
        "piper\npiper_guide_app_aa11bb22\npiper_fault_app",
    )
    assert dbs == ["piper_guide_run_aa11bb22"] and roles == ["piper_guide_app_aa11bb22"]


# ── Arch 2: no .env, by two separate means ───────────────────────────────────


def test_python_dotenv_honours_the_switch_the_run_sets(tmp_path, monkeypatch):
    from dotenv import load_dotenv

    env_file = tmp_path / ".env"
    env_file.write_text("GUIDE_RUN_2404_PROBE=loaded\n")
    monkeypatch.delenv("GUIDE_RUN_2404_PROBE", raising=False)
    monkeypatch.setenv("PYTHON_DOTENV_DISABLED", "1")
    load_dotenv(env_file)
    assert "GUIDE_RUN_2404_PROBE" not in os.environ


def test_requirements_pin_a_python_dotenv_with_the_switch():
    pins = [
        ln.split("==")[1].strip()
        for ln in (ROOT / "requirements.txt").read_text().splitlines()
        if ln.startswith("python-dotenv==")
    ]
    assert pins, "python-dotenv is not pinned in requirements.txt"
    major, minor = (int(x) for x in pins[0].split(".")[:2])
    assert (major, minor) >= (1, 1)  # PYTHON_DOTENV_DISABLED arrived in 1.1


def test_run_folder_links_the_tree_but_not_data_or_env(g, tmp_path):
    root, run_dir = tmp_path / "root", tmp_path / "run"
    root.mkdir()
    run_dir.mkdir()
    (root / "config").mkdir()
    (root / "data" / "chromadb").mkdir(parents=True)
    (root / "main.py").write_text("")
    (root / ".env").write_text("NOT_READ=1\n")
    assert g.make_run_folder(root, run_dir) == [".env", "data"]
    assert (run_dir / "config").is_symlink() and (run_dir / "main.py").is_symlink()
    assert not (run_dir / ".env").exists()
    assert (run_dir / "data").is_dir() and not (run_dir / "data").is_symlink()
    assert list((run_dir / "data").iterdir()) == []


def test_the_driver_never_opens_env_itself():
    source = (ROOT / "scripts" / "guide_keyed_steps_run.py").read_text()
    assert 'os.environ["PYTHON_DOTENV_DISABLED"] = "1"' in source
    for call in ("load_dotenv(", "dotenv_values(", 'open(".env"', '/ ".env"'):
        assert call not in source


# ── Arch 1 and 7: the key's one door ─────────────────────────────────────────


def test_real_key_comes_from_its_environment_name_only(g):
    assert g.key_from_env({g.KEY_VAR: SEAT_VALUE}) == SEAT_VALUE
    with pytest.raises(g.Refused) as refused:
        g.key_from_env({"ANTHROPIC_API_KEY": INHERITED_VALUE})
    assert INHERITED_VALUE not in str(refused.value)


def test_seed_takes_the_key_on_stdin_and_uses_step_5s_call(g):
    assert g.seed_command()[-1] == g.PROVIDER  # argv names the provider and nothing else
    assert "sys.stdin.readline()" in g.SEED
    assert "KeychainService()" in g.SEED and "store_api_key(provider, key)" in g.SEED
    assert 'selected_store() != "db"' in g.SEED
    assert "INSERT" not in g.SEED.upper() and "execute(" not in g.SEED


def test_made_up_key_is_new_each_time(g):
    assert g.made_up_key() != g.made_up_key()


def test_leak_check_finds_the_key_anywhere(g):
    assert g.leak_found(SEAT_VALUE, ["a", f"prefix {SEAT_VALUE} suffix"])
    assert not g.leak_found(SEAT_VALUE, ["a", "b"])
    assert not g.leak_found("", ["anything"])


def test_invite_code_is_masked(g):
    from tests.utils.made_up_credentials import invite_code

    code = invite_code("2404 masked in the step 8 block")
    assert g.mask_codes(f"line {code}", [code]) == f"line {code[:4]}…{code[-4:]}"


# ── Arch 4: COST from the provider's own counts ──────────────────────────────

CONSOLE = (
    "2026-11-18 06:57:10 [info     ] llm_usage                      cache_read_tokens=None "
    "cache_write_tokens=0 completion_tokens=7 model=claude-haiku-4-5-20251001 "
    "prompt_tokens=11 provider=anthropic"
)
JSONLINE = (
    '{"event": "llm_usage", "provider": "anthropic", "model": "claude-sonnet-4-6", '
    '"prompt_tokens": 1000, "completion_tokens": 100, "cache_write_tokens": 2000, '
    '"cache_read_tokens": 4000}'
)


def test_usage_lines_are_read_in_both_log_formats(g):
    calls = g.usage_calls([CONSOLE, "unrelated line", JSONLINE])
    assert [c["model"] for c in calls] == ["claude-haiku-4-5-20251001", "claude-sonnet-4-6"]
    assert calls[0]["input_tokens"] == 11 and calls[0]["output_tokens"] == 7
    assert calls[0]["cache_read_input_tokens"] == 0  # "None" counts as none
    assert calls[1]["cache_creation_input_tokens"] == 2000


def test_cost_is_priced_from_the_one_price_table(g):
    total, lines = g.priced(g.usage_calls([CONSOLE, JSONLINE]))
    haiku = (11 * 1.00 + 7 * 5.00) / 1_000_000
    sonnet = (1000 * 3.00 + 2000 * 3.00 * 1.25 + 4000 * 3.00 * 0.10 + 100 * 15.00) / 1_000_000
    assert total == pytest.approx(haiku + sonnet)
    assert len(lines) == 2


def test_a_model_with_no_price_is_named_not_guessed(g):
    total, lines = g.priced(
        [
            {
                "model": "some-unpriced-model",
                "input_tokens": 5,
                "output_tokens": 5,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
            }
        ]
    )
    assert total == 0 and "NO RECORDED PRICE" in lines[0]


def test_startup_check_bound_is_small_and_positive(g):
    assert 0 < g.startup_check_bound() < 0.001


def test_turns_are_bounded_before_anything_starts(g, monkeypatch):
    monkeypatch.setattr(g, "remove_leftovers", lambda: pytest.fail("started"))
    with pytest.raises(g.Refused):
        g.Run("stub", g.MAX_TURNS + 1, {}, out=lambda s: None).execute()


def test_real_run_without_the_key_starts_nothing(g, monkeypatch):
    monkeypatch.setattr(g, "remove_leftovers", lambda: pytest.fail("started"))
    with pytest.raises(g.Refused):
        g.Run("real", 1, {"ANTHROPIC_API_KEY": INHERITED_VALUE}, out=lambda s: None).execute()


# ── CIO 3, Arch 5: teardown on every exit path ───────────────────────────────


def _wire(g, monkeypatch, calls, *, claim_fails=False):
    monkeypatch.setattr(g, "remove_leftovers", lambda: [])

    def claim(run_id):
        if claim_fails:
            raise g.Refused("database in use")
        calls.append("claim")
        return []

    def create(db, role, environ):
        raise g.Refused("a step failed")

    monkeypatch.setattr(g, "claim_redis", claim)
    monkeypatch.setattr(g, "create_db_and_role", create)
    monkeypatch.setattr(g, "release_redis", lambda: calls.append("release") or ["released"])
    monkeypatch.setattr(
        g, "drop_db_and_role", lambda db, role: calls.append(("drop", db, role)) or ["dropped"]
    )


def test_teardown_runs_when_a_step_fails(g, monkeypatch):
    calls, out = [], []
    _wire(g, monkeypatch, calls)
    run = g.Run("stub", 1, {}, out=out.append, run_id="0a1b2c3d")
    with pytest.raises(g.Refused):
        run.execute()
    assert "release" in calls
    assert ("drop", "piper_guide_run_0a1b2c3d", "piper_guide_app_0a1b2c3d") in calls
    assert any(line.startswith("TEARDOWN:") and "run folder" in line for line in out)


def test_redis_not_claimed_is_not_touched(g, monkeypatch):
    calls, out = [], []
    _wire(g, monkeypatch, calls, claim_fails=True)
    with pytest.raises(g.Refused):
        g.Run("stub", 1, {}, out=out.append, run_id="0a1b2c3d").execute()
    assert "release" not in calls
    assert any("not claimed by this run" in line for line in out)


# ── CIO / Arch 6: the run's own Redis database ───────────────────────────────


class FakeRedis:
    def __init__(self, keys):
        self.keys = dict.fromkeys(keys, "v")
        self.commands = []

    def __call__(self, *args):
        self.commands.append(args)
        if args[0] == "--scan":
            out = "\n".join(self.keys)
        elif args[0] == "DEL":
            self.keys.pop(args[1], None)
            out = "1"
        elif args[0] == "SET":
            self.keys[args[1]] = args[2]
            out = "OK"
        else:
            out = ""
        return subprocess.CompletedProcess(args, 0, out, "")


def test_claim_on_an_empty_database_sets_the_marker(g):
    r = FakeRedis([])
    assert g.claim_redis("0a1b2c3d", r) == []
    assert r.keys == {g.REDIS_MARKER: "0a1b2c3d"}


def test_claim_stops_on_keys_without_the_marker_and_changes_nothing(g):
    r = FakeRedis(["someone:else"])
    with pytest.raises(g.Refused):
        g.claim_redis("0a1b2c3d", r)
    assert r.keys == {"someone:else": "v"}
    assert not [c for c in r.commands if c[0] in ("DEL", "SET", "FLUSHDB", "FLUSHALL")]


def test_claim_removes_an_earlier_runs_leftovers_by_name(g):
    r = FakeRedis([g.REDIS_MARKER, "usage_cap:rate:ip:127.0.0.1"])
    said = g.claim_redis("0a1b2c3d", r)
    assert "2" in said[0] and r.keys == {g.REDIS_MARKER: "0a1b2c3d"}


def test_release_deletes_exactly_the_listed_keys_and_masks_ids(g):
    long_id = "a1b2c3d4e5f6a7b8c9d0"
    r = FakeRedis([g.REDIS_MARKER, f"usage_cap:{long_id}", "usage_cap:rate:ip:127.0.0.1"])
    said = g.release_redis(r)
    assert r.keys == {}
    assert not [c for c in r.commands if c[0] in ("FLUSHDB", "FLUSHALL")]
    assert long_id not in " ".join(said) and "usage_cap:<id>" in said[0]
    assert "0 left" in said[1]


def test_listing_change_names_each_difference(g):
    before = {"a": (1, 1), "b": (2, 2)}
    after = {"b": (2, 3), "c": (1, 1)}
    assert g.listing_change(before, after) == ["added c", "removed a", "changed b"]
    assert g.listing_change(before, dict(before)) == []


# ── the guide's lines stay the app's lines ───────────────────────────────────


def test_step_7_and_9_lines_are_still_what_the_app_shows(g):
    setup_py = (ROOT / "web" / "api" / "routes" / "setup.py").read_text()
    assert 'f"Using the {provider_display_name(req.provider)} key you already saved."' in setup_py
    assert '"anthropic": "Anthropic"' in setup_py
    assert "Using the Anthropic key you already saved." in g.GUIDE["7"]["expected"]
    page = (ROOT / "templates" / "setup.html").read_text()
    for text in (
        "<h2>Setup Complete</h2>",
        "You're all set. You're signed in, and Piper is ready to help.",
        ">Open Piper</a",
    ):
        assert text in page


def test_parent_environment_setting_never_reaches_the_run(g):
    env = g.server_env(
        {"PIPER_ENVIRONMENT": "production", "FLY_APP_NAME": "piper-morgan"},
        db_url=RUN_DB_URL,
        master_key="run-master",
        port=61000,
    )
    assert "PIPER_ENVIRONMENT" not in env and "FLY_APP_NAME" not in env


def test_cost_lines_go_through_the_key_search_before_printing():
    source = (ROOT / "scripts" / "guide_keyed_steps_run.py").read_text()
    assert "rendered = cost_lines + [" in source
    assert "def _cost(self, server: Server) -> List[str]:" in source
