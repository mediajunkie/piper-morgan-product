"""#2335: rotating the hosted Redis password as one command.

Pins section 10's rules: no address or password in argv or in anything printed, a
failed step stops the run, the unreadable-address case stops BEFORE the reset, and the
half-state after a reset is named.

Every address and password here is made up.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location(
    "redis_password_rotate", ROOT / "scripts" / "redis_password_rotate.py"
)
rr = importlib.util.module_from_spec(_spec)
sys.modules["redis_password_rotate"] = rr
_spec.loader.exec_module(rr)

OLD_PW = "made-up-old-word"
NEW_PW = "made-up-new-word"
HOST = "fly-example-db.upstash.io:6379"
DB = "example-db"


def _url(pw):
    return f"redis://default:{pw}@{HOST}"


class World:
    """A fake Fly and a fake beta. Records every command and its standard input."""

    def __init__(self, fail=None, answers=("yes",), holders=(rr.MAIN_APP,), dbs=(DB,)):
        self.fail = fail or set()
        self.answers = list(answers)
        self.holders = set(holders)
        self.dbs = list(dbs)
        self.calls = []
        self.printed = []
        self.password = OLD_PW
        self.app_has = {a: OLD_PW for a in self.holders}
        self.t = 0.0
        self.restarted_at = None
        self.status_shows_url = True
        self.reset_changes = True

    def runner(self, argv, stdin):
        self.calls.append((list(argv), stdin))
        key = " ".join(argv[:3])
        if argv[:3] == ["fly", "secrets", "list"]:
            if key in self.fail:
                return 1, "Error: unauthorized"
            rows = "NAME\tDIGEST\tCREATED AT\nDATABASE_URL\tabc\t1d ago\n"
            if argv[4] in self.holders:
                rows += "REDIS_URL\tdef\t30d ago\n"
            return 0, rows
        if argv[:3] == ["fly", "redis", "list"]:
            body = "NAME\tORG\tPLAN\tREGION\n" + "".join(
                f"{d}\tpersonal\tFree\tsjc\n" for d in self.dbs
            )
            return (1 if key in self.fail else 0), body
        if argv[:3] == ["fly", "redis", "status"]:
            if key in self.fail:
                return 1, "Error: not found"
            line = f"  Private URL = {_url(self.password)}\n" if self.status_shows_url else ""
            return 0, f"Redis\n  Name = {argv[3]}\n{line}"
        if argv[:3] == ["fly", "redis", "reset"]:
            if key in self.fail:
                return 1, "Error: timeout"
            if self.reset_changes:
                self.password = NEW_PW
            return 0, f"Your Redis database {argv[3]} was reset: {_url(self.password)}"
        if argv[:3] == ["fly", "secrets", "import"]:
            app = argv[4]
            if f"import {app}" in self.fail:
                return 1, f"Error updating {app}\n{stdin}"
            self.app_has[app] = stdin.strip().split("=", 1)[1].split(":")[2].split("@")[0]
            if app == rr.MAIN_APP:
                self.restarted_at = self.t
            return 0, f"Secrets are staged\n{stdin}"
        return (1 if key in self.fail else 0), ""

    def health(self):
        up = 99999 if self.restarted_at is None else self.t - self.restarted_at
        return {"status": "healthy", "services": {"uptime_seconds": up}}

    def probe(self, url):
        return 200 if self.app_has.get(rr.MAIN_APP) == self.password else 503

    def confirm(self, prompt):
        return self.answers.pop(0)

    def sleep(self, seconds):
        self.t += seconds

    def clock(self):
        self.t += 1.0
        return self.t

    def rotation(self):
        return rr.Rotation(
            runner=self.runner,
            health=self.health,
            probe=self.probe,
            confirm=self.confirm,
            sleep=self.sleep,
            clock=self.clock,
            out=self.printed.append,
        )

    def go(self, argv=()):
        code = rr.main(list(argv), rotation=self.rotation(), terminal=lambda: True)
        return code, "\n".join(self.printed)

    def argvs(self):
        return [" ".join(c) for c, _ in self.calls]


def _leaks(text):
    return [w for w in (OLD_PW, NEW_PW, _url(OLD_PW), _url(NEW_PW)) if w in text]


def test_a_full_run_resets_then_sets_the_new_address_on_the_holder():
    w = World()
    code, text = w.go()
    assert code == 0 and "RESULT: DONE" in text
    assert w.app_has[rr.MAIN_APP] == NEW_PW
    changing = [a for a in w.argvs() if "reset" in a or "import" in a]
    assert changing == [f"fly redis reset {DB}", f"fly secrets import -a {rr.MAIN_APP}"]
    assert rr.HALF_STATE not in text


def test_no_address_or_password_is_ever_in_argv_or_in_anything_printed():
    w = World()
    _, text = w.go()
    assert _leaks(text) == []
    for argv, _ in w.calls:
        assert _leaks(" ".join(argv)) == []


def test_the_new_address_reaches_fly_on_standard_input_only():
    w = World()
    w.go()
    given = [s for argv, s in w.calls if argv[:3] == ["fly", "secrets", "import"]]
    assert given == [f"REDIS_URL={_url(NEW_PW)}\n"]


def test_only_apps_that_hold_the_secret_are_set():
    w = World(holders=(rr.MAIN_APP, rr.MCP_APP))
    code, _ = w.go()
    assert code == 0
    assert w.app_has == {rr.MAIN_APP: NEW_PW, rr.MCP_APP: NEW_PW}
    w2 = World(holders=(rr.MAIN_APP,))
    w2.go()
    assert f"fly secrets import -a {rr.MCP_APP}" not in w2.argvs()


def test_an_address_this_command_cannot_read_stops_before_the_reset():
    w = World()
    w.status_shows_url = False
    code, text = w.go()
    assert code == 1
    assert not any("reset" in a or "import" in a for a in w.argvs())
    assert rr.HALF_STATE not in text and w.password == OLD_PW


@pytest.mark.parametrize(
    "fail", ["fly auth whoami", "fly redis list", "fly secrets list", "fly redis status"]
)
def test_a_failed_check_changes_nothing(fail):
    w = World(fail={fail})
    code, text = w.go()
    assert code == 1 and "RESULT: NOT FINISHED" in text
    assert not any("reset" in a or "import" in a for a in w.argvs())
    assert rr.HALF_STATE not in text


def test_without_a_typed_yes_nothing_is_reset():
    w = World(answers=("y",))
    code, _ = w.go()
    assert code == 1 and w.password == OLD_PW
    assert not any("reset" in a for a in w.argvs())


def test_no_holder_means_nothing_to_rotate():
    w = World(holders=())
    code, text = w.go()
    assert code == 1 and "nothing to rotate" in text
    assert not any("reset" in a for a in w.argvs())


def test_two_databases_need_a_name_and_a_named_one_is_used():
    w = World(dbs=(DB, "other-db"))
    code, text = w.go()
    assert code == 1 and "--redis NAME" in text
    w2 = World(dbs=(DB, "other-db"))
    code, _ = w2.go(["--redis", DB])
    assert code == 0 and f"fly redis reset {DB}" in w2.argvs()
    w3 = World()
    code, text = w3.go(["--redis", "missing"])
    assert code == 1 and "no Redis database named missing" in text


@pytest.mark.parametrize("fail", ["fly redis reset", f"import {rr.MAIN_APP}"])
def test_a_failure_from_the_reset_on_names_the_half_state(fail):
    w = World(fail={fail})
    code, text = w.go()
    assert code == 1 and rr.HALF_STATE in text
    assert _leaks(text) == []


def test_a_reset_that_did_not_change_the_password_stops_before_setting_anything():
    w = World()
    w.reset_changes = False
    code, text = w.go()
    assert code == 1 and "same password as before" in text
    assert not any("import" in a for a in w.argvs())


def test_a_503_after_the_restart_is_a_failure():
    w = World()
    w.probe = lambda url: 503
    code, text = w.go()
    assert code == 1 and "answered 503" in text and rr.HALF_STATE in text


def test_after_reset_skips_the_reset_and_asks_nothing():
    w = World(answers=())
    w.password = NEW_PW  # already reset by hand; the app still holds the old one
    code, text = w.go(["--after-reset"])
    assert code == 0 and "RESULT: DONE" in text
    assert not any("reset" in a.split()[2] for a in w.argvs() if a.startswith("fly redis"))
    assert w.app_has[rr.MAIN_APP] == NEW_PW


def test_an_unexpected_exception_after_the_reset_still_prints_the_half_state():
    w = World()
    real = w.health

    def breaks():
        if w.password == NEW_PW:
            raise RuntimeError(f"boom {_url(NEW_PW)}")
        return real()

    w.health = breaks
    code, text = w.go()
    assert code == 1
    assert "STOPPED: unexpected RuntimeError" in text and rr.HALF_STATE in text
    assert _leaks(text) == []


def test_without_a_terminal_it_refuses_before_any_check(capsys):
    w = World()
    code = rr.main([], rotation=w.rotation(), terminal=lambda: False)
    assert code == 2 and w.calls == []
    assert rr.NO_TERMINAL in capsys.readouterr().out


def test_the_command_takes_no_address_argument():
    with pytest.raises(SystemExit):
        rr.main(["--url", _url(NEW_PW)], terminal=lambda: True)


def test_find_url_wants_a_password_and_reads_tls_addresses():
    assert rr.find_url("Public URL = redis://fly-x.upstash.io:6379") is None
    tls = f"rediss://default:{NEW_PW}@fly-x.upstash.io:6379"
    assert rr.find_url(f"| Private URL | {tls} |") == tls
    assert rr.redis_names("NAME\tORG\nmy-db\tpersonal\n\n") == ["my-db"]
