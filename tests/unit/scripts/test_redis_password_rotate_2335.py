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
        self.second_address = None
        self.serves_redis_field = False
        self.mcp_status = "healthy"

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
            if self.second_address:
                line += f"  Public URL = {self.second_address}\n"
            return 0, f"Redis\n  Name = {argv[3]}\n{line}"
        if argv[:3] == ["fly", "redis", "reset"]:
            if key in self.fail:
                return 1, "Error: timeout"  # failed and changed nothing
            if self.reset_changes:
                self.password = NEW_PW
            code = 1 if "reset exits 1 after changing" in self.fail else 0
            return code, f"Your Redis database {argv[3]} was reset: {_url(self.password)}"
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
        services = {"uptime_seconds": up}
        if self.serves_redis_field:
            answering = self.app_has.get(rr.MAIN_APP) == self.password
            services["redis"] = "ok" if answering else "unavailable"
            services["revocation_source"] = "redis" if answering else "database"
        return {"status": "healthy", "services": services}

    def mcp_health(self):
        return {"status": self.mcp_status}

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
            mcp_health=self.mcp_health,
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
    assert code == 0 and "RESULT: DONE\n" in text + "\n"
    assert "NOT verified" not in text
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


def test_a_failure_after_the_reset_names_the_half_state():
    w = World(fail={f"import {rr.MAIN_APP}"})
    code, text = w.go()
    assert code == 1 and rr.HALF_STATE in text
    assert _leaks(text) == []


def test_a_reset_that_failed_and_changed_nothing_is_not_called_a_reset():
    """HOST 2026-11-12: e.g. `fly redis reset` asks a question and gets no input."""
    w = World(fail={"fly redis reset"})
    code, text = w.go()
    assert code == 1 and w.password == OLD_PW
    assert "did not change the password" in text and "Nothing was changed" in text
    assert rr.HALF_STATE not in text
    assert not any("import" in a for a in w.argvs())


def test_a_reset_that_changed_the_password_counts_even_if_fly_exits_nonzero():
    w = World(fail={"reset exits 1 after changing"})
    code, text = w.go()
    assert code == 0 and "RESULT: DONE" in text
    assert "exited 1 although the password changed" in text
    assert w.app_has[rr.MAIN_APP] == NEW_PW


def test_two_addresses_stop_the_run_before_the_reset_and_neither_is_printed():
    """HOST's change 2 and CIO's: never pick one of two, and scrub both."""
    w = World()
    other_pw = "made-up-public-word"
    w.second_address = f"rediss://default:{other_pw}@fly-example-db-public.upstash.io:6379"
    code, text = w.go()
    assert code == 1 and "will not pick one" in text
    assert not any("reset" in a.split()[2:3] or "import" in a for a in w.argvs())
    assert _leaks(text) == [] and other_pw not in text and "public.upstash" not in text


def test_a_second_address_in_a_failing_command_is_scrubbed_from_the_tail():
    w = World()
    other = "rediss://default:made-up-public-word@fly-other.upstash.io:6379"
    real = w.runner

    def noisy(argv, stdin):
        code, out = real(argv, stdin)
        if argv[:3] == ["fly", "secrets", "import"]:
            return 1, f"Error\nold {_url(OLD_PW)}\nalso {other}\n{stdin}"
        return code, out

    w.runner = noisy
    code, text = w.go()
    assert code == 1
    assert _leaks(text) == [] and "made-up-public-word" not in text and "[hidden]" in text


def test_the_block_names_the_scheme_and_nothing_else_of_the_address():
    w = World()
    _, text = w.go()
    assert "address scheme: redis" in text
    assert HOST.split(":")[0] not in text


def test_an_mcp_holder_must_read_healthy_afterwards():
    w = World(holders=(rr.MAIN_APP, rr.MCP_APP))
    _, text = w.go()
    assert f"{rr.MCP_APP} reads healthy" in text
    w2 = World(holders=(rr.MAIN_APP, rr.MCP_APP))
    w2.mcp_status = "degraded"
    code, text = w2.go()
    assert code == 1 and "did not read healthy" in text and rr.HALF_STATE in text


def test_a_reset_that_did_not_change_the_password_stops_before_setting_anything():
    w = World()
    w.reset_changes = False
    code, text = w.go()
    assert code == 1 and "did not change the password" in text
    assert not any("import" in a for a in w.argvs())
    assert rr.HALF_STATE not in text


def test_a_503_after_the_restart_is_a_failure():
    w = World()
    w.probe = lambda url: 503
    code, text = w.go()
    assert code == 1 and "answered 503" in text and rr.HALF_STATE in text


def test_after_reset_skips_the_reset_and_asks_nothing():
    w = World(answers=())
    w.password = NEW_PW  # already reset by hand; the app still holds the old one
    code, text = w.go(["--after-reset"])
    assert code == 0
    # HOST's change 1: this mode cannot compare passwords, so it must not claim it did.
    assert "RESULT: DONE (address set; change of password NOT verified by this run)" in text
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
    two = "redis://a:pw-one@h1:6379 and redis://a:pw-two@h2:6379 and redis://a:pw-one@h1:6379"
    assert rr.find_url(two) is None and len(rr.find_urls(two)) == 2
    tls = f"rediss://default:{NEW_PW}@fly-x.upstash.io:6379"
    assert rr.find_url(f"| Private URL | {tls} |") == tls
    assert rr.redis_names("NAME\tORG\nmy-db\tpersonal\n\n") == ["my-db"]


def test_a_build_that_serves_the_redis_field_is_read_for_the_confirmation():
    """#2348: /health says redis ok and which store revocations use."""
    w = World()
    w.serves_redis_field = True
    code, text = w.go()
    assert code == 0
    assert "/health reads redis: ok, revocation_source: redis" in text
    older = World()
    _, text = older.go()
    assert "does not serve a redis field" in text


def test_health_reading_redis_unavailable_after_the_restart_is_a_failure():
    w = World()
    w.serves_redis_field = True
    w.probe = lambda url: 200  # the page loads, yet the record says Redis is not answering
    real = w.runner

    def wrong_value(argv, stdin):
        code, out = real(argv, stdin)
        if argv[:3] == ["fly", "secrets", "import"]:
            w.app_has[rr.MAIN_APP] = "something-else"
        return code, out

    w.runner = wrong_value
    code, text = w.go()
    assert code == 1 and "/health reads redis: unavailable" in text and rr.HALF_STATE in text
