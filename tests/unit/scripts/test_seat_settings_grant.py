"""seat_settings_grant.py (ADR-084): the value is never printed, the file ends at 0600, denies only grow."""

import importlib.util
import json
import stat
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
DUMMY = "dummy-not-a-key-0123456789abcdef"


def _load():
    spec = importlib.util.spec_from_file_location(
        "seat_settings_grant", ROOT / "scripts" / "seat_settings_grant.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def seat(tmp_path):
    folder = tmp_path / "lead" / ".claude"
    folder.mkdir(parents=True)
    path = folder / "settings.local.json"
    path.write_text(
        json.dumps({"permissions": {"allow": ["Bash(git status:*)"], "deny": ["Read(**/.env)"]}})
    )
    path.chmod(0o644)
    return tmp_path, path


def test_add_key_stores_the_value_and_never_prints_it(seat, monkeypatch, capsys):
    mod = _load()
    root, path = seat
    monkeypatch.setattr(mod.getpass, "getpass", lambda prompt: DUMMY)
    assert (
        mod.main(
            ["--root", str(root), "add-key", "--seat", "lead", "--name", "PIPER_SEAT_ANTHROPIC_KEY"]
        )
        == 0
    )
    out = capsys.readouterr()
    assert DUMMY not in out.out and DUMMY not in out.err
    assert f"{len(DUMMY)} chars, sha256 " in out.out
    data = json.loads(path.read_text())
    assert data["env"]["PIPER_SEAT_ANTHROPIC_KEY"] == DUMMY
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    # the earlier deny is kept and the self-deny is added; the earlier allow is untouched
    assert data["permissions"]["deny"] == ["Read(**/.env)", mod.SELF_DENY]
    assert data["permissions"]["allow"] == ["Bash(git status:*)"]


def test_add_key_refuses_a_provider_variable_name(seat, monkeypatch):
    mod = _load()
    root, path = seat
    before = path.read_text()
    monkeypatch.setattr(mod.getpass, "getpass", lambda prompt: DUMMY)
    with pytest.raises(SystemExit):
        mod.main(["--root", str(root), "add-key", "--seat", "lead", "--name", "ANTHROPIC_API_KEY"])
    assert path.read_text() == before


@pytest.mark.parametrize("bad", ["", "has space", " leading", "trailing\n"])
def test_add_key_refuses_an_empty_or_spaced_value(seat, monkeypatch, bad):
    mod = _load()
    root, path = seat
    before = path.read_text()
    monkeypatch.setattr(mod.getpass, "getpass", lambda prompt: bad)
    with pytest.raises(SystemExit):
        mod.main(
            ["--root", str(root), "add-key", "--seat", "lead", "--name", "PIPER_SEAT_ANTHROPIC_KEY"]
        )
    assert path.read_text() == before


def test_a_broken_settings_file_is_left_alone(seat, monkeypatch):
    mod = _load()
    root, path = seat
    path.write_text("{ not json")
    monkeypatch.setattr(mod.getpass, "getpass", lambda prompt: DUMMY)
    with pytest.raises(SystemExit):
        mod.main(
            ["--root", str(root), "add-key", "--seat", "lead", "--name", "PIPER_SEAT_ANTHROPIC_KEY"]
        )
    assert path.read_text() == "{ not json"


def test_add_allow_is_exact_only_and_idempotent(seat, capsys):
    mod = _load()
    root, path = seat
    rule = "Bash(venv/bin/python scripts/seat_session.py --account seat-plain)"
    assert mod.main(["--root", str(root), "add-allow", "--seat", "lead", "--rule", rule]) == 0
    assert mod.main(["--root", str(root), "add-allow", "--seat", "lead", "--rule", rule]) == 0
    data = json.loads(path.read_text())
    assert data["permissions"]["allow"].count(rule) == 1
    assert data["permissions"]["deny"] == ["Read(**/.env)"]
    with pytest.raises(SystemExit):
        mod.main(["--root", str(root), "add-allow", "--seat", "lead", "--rule", "Bash(python3:*)"])


def test_show_and_remove_key(seat, monkeypatch, capsys):
    mod = _load()
    root, path = seat
    monkeypatch.setattr(mod.getpass, "getpass", lambda prompt: DUMMY)
    mod.main(
        ["--root", str(root), "add-key", "--seat", "lead", "--name", "PIPER_SEAT_ANTHROPIC_KEY"]
    )
    capsys.readouterr()
    assert mod.main(["--root", str(root), "show", "--seat", "lead"]) == 0
    out = capsys.readouterr().out
    assert DUMMY not in out and "self-deny present: True" in out and "mode: 0o600" in out
    assert (
        mod.main(
            [
                "--root",
                str(root),
                "remove-key",
                "--seat",
                "lead",
                "--name",
                "PIPER_SEAT_ANTHROPIC_KEY",
            ]
        )
        == 0
    )
    data = json.loads(path.read_text())
    assert "env" not in data
    assert mod.SELF_DENY in data["permissions"]["deny"]  # a deny is never removed


def test_check_env_reads_the_environment_only(monkeypatch, capsys):
    mod = _load()
    monkeypatch.setenv("PIPER_SEAT_ANTHROPIC_KEY", DUMMY)
    assert mod.main(["check-env", "--name", "PIPER_SEAT_ANTHROPIC_KEY"]) == 0
    out = capsys.readouterr().out
    assert DUMMY not in out and "set, " in out
    monkeypatch.delenv("PIPER_SEAT_ANTHROPIC_KEY")
    assert mod.main(["check-env", "--name", "PIPER_SEAT_ANTHROPIC_KEY"]) == 1


def test_an_unknown_seat_is_refused(tmp_path):
    mod = _load()
    with pytest.raises(SystemExit):
        mod.main(["--root", str(tmp_path), "show", "--seat", "nobody"])


def test_check_env_refuses_a_name_that_is_not_a_seat_key(monkeypatch, capsys):
    mod = _load()
    monkeypatch.setenv("ANTHROPIC_API_KEY", DUMMY)
    with pytest.raises(SystemExit):
        mod.main(["check-env", "--name", "ANTHROPIC_API_KEY"])
    out = capsys.readouterr()
    assert "sha256" not in out.out and "sha256" not in out.err


@pytest.mark.parametrize(
    "rule",
    ["Read(~/.piper-shared/anything.txt)", "Edit(scripts/foo.py)", "WebFetch(domain:example.com)"],
)
def test_add_allow_takes_bash_rules_only(seat, rule):
    mod = _load()
    root, path = seat
    before = path.read_text()
    with pytest.raises(SystemExit):
        mod.main(["--root", str(root), "add-allow", "--seat", "lead", "--rule", rule])
    assert path.read_text() == before


def test_prepare_adds_the_deny_and_the_mode_with_no_key(seat, capsys):
    mod = _load()
    root, path = seat
    assert mod.main(["--root", str(root), "prepare", "--seat", "lead"]) == 0
    data = json.loads(path.read_text())
    assert "env" not in data
    assert data["permissions"]["deny"] == ["Read(**/.env)", mod.SELF_DENY]
    assert data["permissions"]["allow"] == ["Bash(git status:*)"]
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert "no key was added" in capsys.readouterr().out
    # running it twice changes nothing
    assert mod.main(["--root", str(root), "prepare", "--seat", "lead"]) == 0
    assert json.loads(path.read_text())["permissions"]["deny"].count(mod.SELF_DENY) == 1
