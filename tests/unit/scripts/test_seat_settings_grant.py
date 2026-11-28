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


def test_show_says_why_the_self_deny_is_absent(seat, monkeypatch, capsys):
    """Exec 01M8CJW0EX (2026-11-26): add-allow alone leaves the self-deny out, which is correct for
    a file with no seat key; the summary has to say so, and has to say MISSING if a key is there."""
    mod = _load()
    root, path = seat
    rule = "Bash(scripts/seat_session.py --account seat-github-1)"
    assert mod.main(["--root", str(root), "add-allow", "--seat", "lead", "--rule", rule]) == 0
    out = capsys.readouterr().out
    assert "self-deny present: False (not needed: no seat key in this file" in out
    data = json.loads(path.read_text())
    data["env"] = {"PIPER_SEAT_ANTHROPIC_KEY": DUMMY}
    path.write_text(json.dumps(data))
    assert mod.main(["--root", str(root), "show", "--seat", "lead"]) == 0
    out = capsys.readouterr().out
    assert DUMMY not in out
    assert "self-deny present: False. MISSING: this file holds a seat key" in out


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


def test_fleet_deny_adds_its_rules_and_changes_nothing_else(tmp_path, capsys):
    mod = _load()
    shared = tmp_path / "settings.json"
    before = {
        "cleanupPeriodDays": 3650,
        "env": {"FLY_NO_UPDATE_CHECK": "1"},
        "permissions": {"allow": ["Bash(x)"]},
    }
    shared.write_text(json.dumps(before, indent=2) + "\n")
    shared.chmod(0o644)
    assert mod.main(["fleet-deny", "--shared-settings", str(shared)]) == 0
    after = json.loads(shared.read_text())
    assert after["permissions"]["deny"] == list(mod.FLEET_DENIES)
    assert after["permissions"]["allow"] == ["Bash(x)"] and after["env"] == before["env"]
    assert after["cleanupPeriodDays"] == 3650
    assert stat.S_IMODE(shared.stat().st_mode) == 0o644  # the shared file keeps its mode
    assert f"added {len(mod.FLEET_DENIES)} deny rule(s)" in capsys.readouterr().out
    # a second run adds nothing and keeps existing denies
    assert mod.main(["fleet-deny", "--shared-settings", str(shared)]) == 0
    assert json.loads(shared.read_text())["permissions"]["deny"] == list(mod.FLEET_DENIES)
    assert "added 0 deny rule(s)" in capsys.readouterr().out


def test_fleet_deny_keeps_an_existing_deny_and_refuses_a_missing_or_broken_file(tmp_path):
    mod = _load()
    shared = tmp_path / "settings.json"
    shared.write_text(json.dumps({"permissions": {"deny": ["Read(~/.cloudflare/**)"]}}))
    assert mod.main(["fleet-deny", "--shared-settings", str(shared)]) == 0
    assert json.loads(shared.read_text())["permissions"]["deny"] == [
        "Read(~/.cloudflare/**)",
        *mod.FLEET_DENIES,
    ]
    with pytest.raises(SystemExit):
        mod.main(["fleet-deny", "--shared-settings", str(tmp_path / "absent.json")])
    shared.write_text("{ not json")
    with pytest.raises(SystemExit):
        mod.main(["fleet-deny", "--shared-settings", str(shared)])
    assert shared.read_text() == "{ not json"


def test_fleet_deny_keeps_the_file_as_it_was_beside_it(tmp_path, capsys):
    mod = _load()
    shared = tmp_path / "settings.json"
    original = json.dumps({"env": {"FLY_NO_UPDATE_CHECK": "1"}}, indent=4) + "\n"
    shared.write_text(original)
    assert mod.main(["fleet-deny", "--shared-settings", str(shared)]) == 0
    backup = tmp_path / "settings.json.before-fleet-deny"
    assert backup.read_text() == original  # byte for byte, so the undo is one mv
    out = capsys.readouterr().out
    assert str(backup) in out and "to undo: mv" in out
    # a second run changes nothing and does not replace the first copy
    backup_before = backup.read_text()
    assert mod.main(["fleet-deny", "--shared-settings", str(shared)]) == 0
    assert backup.read_text() == backup_before
    assert "to undo" not in capsys.readouterr().out


@pytest.fixture
def tty(monkeypatch):
    """Tests run without a terminal; the tool's own check is the seam."""
    return lambda mod, value=True: monkeypatch.setattr(mod, "is_terminal", lambda: value)


def _shared(tmp_path):
    shared = tmp_path / "shared-settings.json"
    shared.write_text(json.dumps({"env": {"FLY_NO_UPDATE_CHECK": "1"}}, indent=2) + "\n")
    return shared


def test_grant_key_does_all_four_steps_in_order_when_the_reads_were_refused(
    seat, tmp_path, monkeypatch, capsys, tty
):
    mod = _load()
    tty(mod)
    root, path = seat
    shared = _shared(tmp_path)
    seen = {}

    def answer(prompt):
        # at the wait, the denies are in and no key is in the seat's file
        seen["deny_at_wait"] = json.loads(path.read_text())["permissions"]["deny"]
        seen["env_at_wait"] = json.loads(path.read_text()).get("env")
        seen["shared_at_wait"] = json.loads(shared.read_text())["permissions"]["deny"]
        return "refused refused refused"

    monkeypatch.setattr("builtins.input", answer)
    monkeypatch.setattr(mod.getpass, "getpass", lambda prompt: DUMMY)
    rc = mod.main(
        [
            "--root",
            str(root),
            "grant-key",
            "--seat",
            "lead",
            "--name",
            "PIPER_SEAT_ANTHROPIC_KEY",
            "--shared-settings",
            str(shared),
        ]
    )
    assert rc == 0
    assert mod.SELF_DENY in seen["deny_at_wait"] and seen["env_at_wait"] is None
    assert seen["shared_at_wait"] == list(mod.FLEET_DENIES)
    assert json.loads(path.read_text())["env"]["PIPER_SEAT_ANTHROPIC_KEY"] == DUMMY
    assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert (tmp_path / "shared-settings.json.before-fleet-deny").exists()
    out = capsys.readouterr()
    assert DUMMY not in out.out and DUMMY not in out.err
    assert "WAITING FOR READ TESTS on seat lead" in out.out


@pytest.mark.parametrize(
    "reply",
    [
        "",
        "no",
        "yes",
        "refused",
        "refused refused",
        "refused refused read",
        "not refused refused refused",
    ],
)
def test_grant_key_stops_before_the_key_unless_he_types_refused(
    seat, tmp_path, monkeypatch, capsys, tty, reply
):
    mod = _load()
    tty(mod)
    root, path = seat
    shared = _shared(tmp_path)
    monkeypatch.setattr("builtins.input", lambda prompt: reply)

    def no_key(prompt):
        raise AssertionError("the key prompt must not be reached")

    monkeypatch.setattr(mod.getpass, "getpass", no_key)
    rc = mod.main(
        [
            "--root",
            str(root),
            "grant-key",
            "--seat",
            "lead",
            "--name",
            "PIPER_SEAT_ANTHROPIC_KEY",
            "--shared-settings",
            str(shared),
        ]
    )
    assert rc == 2
    assert "env" not in json.loads(path.read_text())
    assert "Stopped before any key" in capsys.readouterr().out


def test_grant_key_refuses_without_a_terminal_and_changes_nothing(seat, tmp_path, monkeypatch):
    mod = _load()
    root, path = seat
    shared = _shared(tmp_path)
    before_seat, before_shared = path.read_text(), shared.read_text()
    monkeypatch.setattr(mod, "is_terminal", lambda: False)
    with pytest.raises(SystemExit):
        mod.main(
            [
                "--root",
                str(root),
                "grant-key",
                "--seat",
                "lead",
                "--name",
                "PIPER_SEAT_ANTHROPIC_KEY",
                "--shared-settings",
                str(shared),
            ]
        )
    assert path.read_text() == before_seat and shared.read_text() == before_shared


def test_grant_key_refuses_a_broken_seat_file_before_touching_the_shared_one(
    seat, tmp_path, monkeypatch, tty
):
    mod = _load()
    tty(mod)
    root, path = seat
    shared = _shared(tmp_path)
    before_shared = shared.read_text()
    path.write_text("{ not json")
    with pytest.raises(SystemExit):
        mod.main(
            [
                "--root",
                str(root),
                "grant-key",
                "--seat",
                "lead",
                "--name",
                "PIPER_SEAT_ANTHROPIC_KEY",
                "--shared-settings",
                str(shared),
            ]
        )
    assert shared.read_text() == before_shared
    assert not (tmp_path / "shared-settings.json.before-fleet-deny").exists()


def test_every_add_allow_line_in_the_steps_file_is_accepted_as_written(tmp_path):
    """The commands xian pastes (ADR-084 steps file) must be ones the tool takes."""
    import re
    import shlex

    steps = (ROOT / "docs" / "internal" / "operations" / "adr-084-one-time-steps.md").read_text()
    lines = [
        line.strip()
        for line in steps.splitlines()
        if line.strip().startswith("scripts/seat_settings_grant.py add-allow")
    ]
    assert len(lines) >= 2, lines
    mod = _load()
    for line in lines:
        words = shlex.split(line)
        seat, rule = words[words.index("--seat") + 1], words[words.index("--rule") + 1]
        # One fixed command each: a helper for a named account, plus at most one closed
        # tail. Each tail is an exact literal, never a slot, so a new shape is a diff HOST
        # reads: the fixed redirect_uri reads (issue 2282 step 5; HOST's land
        # 2026-11-16; the /setup calendar start, issue 2282 box 4, 2026-11-24); the counter read, the one path on seat_read.ALLOWED_PATHS (#2388
        # row 4; HOST 2026-11-24); --save-key and --remove-key for anthropic (#2406, HOST's
        # reads 2026-11-22 and 11-23). No other path or flag.
        assert re.fullmatch(
            r"Bash\(scripts/seat_[a-z_]+\.py --account [a-z0-9-]+"
            r"( --redirect-uri (github|calendar|setup-calendar)"
            r"| /api/v1/admin/floored-actions"
            r"| --save-key anthropic"
            r"| --remove-key anthropic)?\)",
            rule,
        ), rule
        folder = tmp_path / seat / ".claude"
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / "settings.local.json"
        if not path.exists():
            path.write_text(json.dumps({"permissions": {"allow": [], "deny": []}}))
        assert mod.main(["--root", str(tmp_path), *words[1:]]) == 0
        assert rule in json.loads(path.read_text())["permissions"]["allow"]
        script = rule[len("Bash(") :].split()[0]
        assert (ROOT / script).is_file(), script


def test_fleet_deny_rerun_adds_only_the_piper_shared_rules_and_keeps_the_first_copy(tmp_path):
    """2026-11-22: a shared file already holding Step A's two denies gains only the new ones."""
    mod = _load()
    shared = tmp_path / "settings.json"
    step_a = list(mod.FLEET_DENIES[:2])
    shared.write_text(json.dumps({"permissions": {"deny": step_a}}, indent=2) + "\n")
    backup = tmp_path / "settings.json.before-fleet-deny"
    backup.write_text("first copy\n")
    assert mod.main(["fleet-deny", "--shared-settings", str(shared)]) == 0
    deny = json.loads(shared.read_text())["permissions"]["deny"]
    assert deny == list(mod.FLEET_DENIES)
    assert backup.read_text() == "first copy\n"


def test_fleet_denies_cover_a_browser_profile_folder_and_its_contents():
    """The deny that Web's seat lacked: a file inside seat-browser-credential-profile-<seat>."""
    mod = _load()
    assert "Read(~/.piper-shared/*credential*)" in mod.FLEET_DENIES
    assert "Read(~/.piper-shared/*credential*/**)" in mod.FLEET_DENIES
    for name in ("token", "secret"):
        assert f"Read(~/.piper-shared/*{name}*)" in mod.FLEET_DENIES
        assert f"Read(~/.piper-shared/*{name}*/**)" in mod.FLEET_DENIES


def test_a_rerun_prints_an_undo_that_reverts_only_that_run(tmp_path, capsys):
    """Arch, 2026-11-22: after Step A, the printed mv must not drop Step A's two denies."""
    mod = _load()
    shared = tmp_path / "settings.json"
    step_a = list(mod.FLEET_DENIES[:2])
    after_step_a = json.dumps({"permissions": {"deny": step_a}}, indent=2) + "\n"
    shared.write_text(after_step_a)
    first = tmp_path / "settings.json.before-fleet-deny"
    first.write_text("the copy from Step A\n")
    assert mod.main(["fleet-deny", "--shared-settings", str(shared)]) == 0
    out = capsys.readouterr().out
    undo = [line for line in out.splitlines() if line.startswith("to undo: mv ")]
    assert len(undo) == 1
    named = Path(undo[0].split("'")[1])
    assert named != first and named.name.startswith("settings.json.before-fleet-deny.")
    assert json.loads(named.read_text())["permissions"]["deny"] == step_a
    assert first.read_text() == "the copy from Step A\n"


# ADR-084 line 22: no seat runs `fly`. Exec 01M8G038V2 (2026-11-27), after PA's seat ran `fly releases`
# and `fly status` with no rule refusing them. fnmatch stands in for Claude Code's matcher here (the
# real matcher is read by a seat's refused `fly version`); it pins which strings the rules name.
def _denied(mod, command):
    import fnmatch

    return any(fnmatch.fnmatchcase(command, rule[len("Bash(") : -1]) for rule in mod.FLY_DENIES)


@pytest.mark.parametrize(
    "command",
    [
        "fly releases -a piper-morgan-mcp",
        "fly status -a piper-morgan-mcp",
        "fly secrets list -a piper-morgan",
        "flyctl deploy",
        "fly",
        "/opt/homebrew/bin/fly status",
        "/opt/homebrew/bin/flyctl ssh console -a piper-morgan",
        "env fly status",
        "env FLY_API_TOKEN=x fly status",
        "env -u ANTHROPIC_API_KEY flyctl logs",
        "command fly status",
        "FLY_API_TOKEN=x fly status -a piper-morgan",
        "FLY_ACCESS_TOKEN=x FLY_NO_UPDATE_CHECK=1 flyctl secrets list",
        "fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES'",
    ],
)
def test_fly_denies_name_every_fly_command_a_seat_types(command):
    assert _denied(_load(), command)


@pytest.mark.parametrize(
    "command",
    [
        "ls deploy/fly",
        "cat deploy/fly/github-mcp.fly.toml",
        "grep -n 'bin/fly ' scripts/seat_settings_grant.py",
        "git commit -m 'deny fly on every seat'",
        "gh workflow run fly-deploy.yml -R mediajunkie/piper-morgan-product --ref main -f promote_to_alpha=true",
        "scripts/deploy-mcp.sh --dry-run",
        "python3 scripts/gen-fly-permissions.py --check",
        "flyway migrate",
        "FLY_NO_UPDATE_CHECK=1 python3 scripts/gen-fly-permissions.py --check",
    ],
)
def test_fly_denies_leave_other_commands_alone(command):
    assert not _denied(_load(), command)


def test_fly_denies_are_in_the_fleet_set_and_keep_an_existing_fly_allow(tmp_path):
    """The shared file already carries one fly allow (the live-set read); the run is additive and
    leaves it, and a deny beats an allow, so after the run it no longer lets a seat through."""
    mod = _load()
    assert set(mod.FLY_DENIES) <= set(mod.FLEET_DENIES)
    assert all(not rule.startswith("Bash(*") for rule in mod.FLY_DENIES)
    allow = "Bash(fly ssh console -a piper-morgan -C 'printenv PIPER_INVERSION_LIVE_CATEGORIES')"
    shared = tmp_path / "settings.json"
    shared.write_text(
        json.dumps({"permissions": {"allow": [allow], "deny": list(mod.FLEET_DENIES[:8])}})
    )
    added = mod.fleet_deny(shared)
    assert added == list(mod.FLY_DENIES)
    after = json.loads(shared.read_text())["permissions"]
    assert after["allow"] == [allow] and after["deny"] == list(mod.FLEET_DENIES)
