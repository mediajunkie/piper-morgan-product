"""#2157's restore drill as one command (HOST design v2, Arch 11-12; section 10's rules).

Layer: the script's own logic with every outside call stubbed (fly, the proxy, HTTP). Not
a run against Fly: xian's first run is the served check, and no seat stands in for it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import restore_drill_2157 as d  # noqa: E402

KEY = "MASTER-KEY-VALUE-xyz"
R_PASSWORD = "r-password-value"
DB_PASSWORD = "db-superuser-pw-123"
TOKEN = "jwt-token-for-r"
STAMP = "20261120-1400"
APP = f"pm-restore-drill-{STAMP}"


class Fly:
    """Answers fly commands; records every argv and stdin."""

    def __init__(self, fail_on=None, image=None):
        self.calls = []
        self.fail_on = fail_on
        self.apps = set()
        self.image = image or {"Registry": "registry.fly.io", "Repository": "piper-morgan",
                               "Digest": "sha256:abc"}  # fmt: skip

    def __call__(self, argv, stdin=None):
        self.calls.append((argv, stdin))
        joined = " ".join(argv)
        if self.fail_on and self.fail_on in joined:
            return 1, "Error: something refused"
        if argv[:3] == ["fly", "auth", "whoami"]:
            return 0, "xian@example\n"
        if argv[:3] == ["fly", "volumes", "list"]:
            if "piper-morgan-db" == argv[4]:
                return 0, json.dumps([{"id": "vol_src", "size_gb": 3}])
            return 0, json.dumps([{"id": "vol_copy"}]) if argv[4] in self.apps else "[]"
        if argv[:4] == ["fly", "volumes", "snapshots", "list"]:
            if argv[4] == "vol_src":
                return 0, json.dumps(
                    [
                        {"id": "vs_old", "created_at": "2026-11-18T00:00:00Z"},
                        {"id": "vs_new", "created_at": "2026-11-19T00:00:00Z"},
                    ]  # fmt: skip
                )
            return 0, "[]"
        if argv[:3] == ["fly", "image", "show"]:
            return 0, json.dumps(self.image)
        if argv[:3] == ["fly", "apps", "list"]:
            return 0, json.dumps(
                [{"Name": n} for n in sorted(self.apps)] + [{"Name": "piper-morgan"}]
            )
        if argv[:3] == ["fly", "postgres", "create"]:
            self.apps.add(argv[argv.index("--name") + 1])
            return 0, f"Creating...\n  Username:    postgres\n  Password:    {DB_PASSWORD}\n"
        if argv[:3] == ["fly", "apps", "create"]:
            self.apps.add(argv[3])
            return 0, "New app created"
        if argv[:3] == ["fly", "apps", "destroy"]:
            self.apps.discard(argv[3])
            return 0, "Destroyed"
        if argv[:3] == ["fly", "ssh", "console"]:
            return 0, "Connecting...\nok\n"
        return 0, ""


class FakeProxy:
    instances = []

    def __init__(self, app):
        self.app, self.started, self.stopped = app, False, False
        FakeProxy.instances.append(self)

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True

    def alive(self):
        return self.started and not self.stopped


def ok_http(method, url, form=None, bearer=None):
    if url.endswith("/health"):
        return 200, {}
    if url.endswith("/login"):
        return 200, {"token": TOKEN}
    if url.endswith("/me"):
        return (200, {}) if bearer == TOKEN else (401, {})
    return 404, {}


def drill(fly, request=ok_http, keep=False, confirm=None, out=None, free=lambda: True):
    clock = iter(range(0, 10_000, 5))
    return d.Drill(
        org="personal",
        keep=keep,
        runner=fly,
        request=request,
        proxy_factory=FakeProxy,
        values=lambda: (KEY, "r-user", R_PASSWORD),
        confirm=confirm or (lambda prompt: APP),
        sleep=lambda s: None,
        clock=lambda: next(clock),
        out=out or (lambda line: None),
        stamp=STAMP,
        free=free,
    )


def run(dr):
    printed = []
    dr.out = printed.append
    code = d.main(["--org", "personal"], drill=dr, terminal=lambda: True)
    return code, "\n".join(printed)


SECRETS = (KEY, R_PASSWORD, DB_PASSWORD, TOKEN)


def test_a_full_run_passes_1_2_5_and_says_proof_3_waits():
    fly = Fly()
    code, printed = run(drill(fly))
    assert "PROOF 1 PASS" in printed and "PROOF 2 PASS: stored key decrypts: ok" in printed
    assert "PROOF 3 NOT RUN" in printed and "PROOF 5 PASS" in printed
    assert "RESULT: PROOFS 1, 2, 5 PASSED; proof 3 waits on #2158" in printed
    assert "RESULT: DONE" not in printed and code == 0
    assert not fly.apps & {APP, f"{APP}-db", f"{APP}-redis"}


def test_no_secret_in_any_argv_and_none_printed():
    """Section 10 rules 2 and 4."""
    fly = Fly()
    _, printed = run(drill(fly))
    for argv, _ in fly.calls:
        for value in SECRETS:
            assert all(value not in part for part in argv)
    for value in SECRETS:
        assert value not in printed


def test_the_copy_gets_exactly_the_allowlist_through_stdin():
    fly = Fly()
    run(drill(fly))
    ((argv, stdin),) = [(a, s) for a, s in fly.calls if a[:3] == ["fly", "secrets", "import"]]
    assert argv[-2:] == [APP, "--stage"] or "--stage" in argv
    given = dict(line.split("=", 1) for line in stdin.strip().splitlines())
    assert set(given) == {"DATABASE_URL", "ENCRYPTION_MASTER_KEY", "JWT_SECRET_KEY",
                          "REDIS_URL", "PIPER_CREDENTIAL_STORE"}  # fmt: skip
    assert given["ENCRYPTION_MASTER_KEY"] == KEY and given["PIPER_CREDENTIAL_STORE"] == "db"
    assert f"{APP}-db.flycast" in given["DATABASE_URL"] and DB_PASSWORD in given["DATABASE_URL"]
    assert given["REDIS_URL"].startswith(f"redis://{APP}-redis.internal")
    for word in ("GITHUB", "SLACK", "GOOGLE", "CALENDAR", "SMTP", "ANTHROPIC", "SUBKEY"):
        assert not any(word in name for name in given)


def test_everything_is_made_on_the_runs_own_network_never_production():
    fly = Fly()
    run(drill(fly))
    creates = [a for a, _ in fly.calls if a[:3] in (["fly", "postgres", "create"],
                                                   ["fly", "apps", "create"])]  # fmt: skip
    assert len(creates) == 3
    for argv in creates:
        assert argv[argv.index("--network") + 1] == APP
    made = [
        a
        for a, _ in fly.calls
        if a[:2] == ["fly", "machine"] or a[:3] == ["fly", "apps", "destroy"]
    ]
    for argv in made:
        assert "piper-morgan" not in argv and "piper-morgan-db" not in argv
    machine = [a for a, _ in fly.calls if a[:3] == ["fly", "machine", "run"] and "-e" in a][0]
    assert f"{d.DRILL_COPY_ENV}=yes" in machine and "--port" not in machine


@pytest.mark.parametrize(
    "fail_on",
    ["machine run redis", "apps create " + APP + " --org", "secrets import", "ssh console"],
)
def test_a_failed_step_still_destroys_every_app_it_made(fail_on):
    """HOST: a failed drill must not leave a copy of everyone's data standing."""
    fly = Fly(fail_on=fail_on.strip())
    code, printed = run(drill(fly))
    assert not fly.apps - {"piper-morgan"}
    assert "destroy " in printed


def test_a_failed_create_destroys_the_half_made_database():
    fly = Fly(fail_on="postgres create")
    code, printed = run(drill(fly))
    destroyed = [a[3] for a, _ in fly.calls if a[:3] == ["fly", "apps", "destroy"]]
    assert destroyed == [f"{APP}-db"] and code == 1 and "RESULT: NOT FINISHED" in printed


def test_the_proxy_is_stopped_on_a_failure():
    FakeProxy.instances.clear()
    fly = Fly(fail_on="ssh console")
    run(drill(fly))
    assert FakeProxy.instances and all(p.stopped for p in FakeProxy.instances)


def test_the_copy_that_never_answers_is_still_destroyed():
    FakeProxy.instances.clear()
    fly = Fly()
    code, printed = run(drill(fly, request=lambda *a: (0, {})))
    assert "didn't answer 200" in printed and code == 1
    assert not fly.apps - {"piper-morgan"} and FakeProxy.instances[-1].stopped


def test_a_wrong_name_at_the_confirm_creates_nothing():
    fly = Fly()
    code, printed = run(drill(fly, confirm=lambda p: "yes"))
    assert code == 1 and "nothing was created" in printed
    assert not [a for a, _ in fly.calls if "create" in a]


def test_an_existing_name_stops_before_anything_is_made():
    fly = Fly()
    fly.apps.add(f"{APP}-redis")
    code, printed = run(drill(fly))
    assert code == 1 and "already exists" in printed
    assert not [a for a, _ in fly.calls if "create" in a or "destroy" in a]


def test_keep_destroys_nothing_and_names_what_to_destroy():
    fly = Fly()
    code, printed = run(drill(fly, keep=True))
    assert not [a for a, _ in fly.calls if a[:3] == ["fly", "apps", "destroy"]]
    assert "REMINDER" in printed and f"{APP}-db" in printed and "RESULT: NOT FINISHED" in printed


def test_a_failed_decrypt_is_not_finished():
    class Bad(Fly):
        def __call__(self, argv, stdin=None):
            if argv[:3] == ["fly", "ssh", "console"]:
                self.calls.append((argv, stdin))
                return 0, "fail:1\n"
            return super().__call__(argv, stdin)

    code, printed = run(drill(Bad()))
    assert "PROOF 2 FAIL: stored key decrypts: fail:1" in printed
    assert "RESULT: NOT FINISHED" in printed and code == 1


def test_proof_2_runs_the_drill_mode_inside_the_copy_never_beta():
    fly = Fly()
    run(drill(fly))
    (argv,) = [a for a, _ in fly.calls if a[:3] == ["fly", "ssh", "console"]]
    assert argv[argv.index("-a") + 1] == APP and "--own-database-in-drill-copy" in argv[-1]


def test_without_a_terminal_it_refuses_before_anything(capsys):
    fly = Fly()
    assert d.main(["--org", "x"], drill=drill(fly), terminal=lambda: False) == 2
    assert "real terminal" in capsys.readouterr().out and fly.calls == []


def test_the_newest_snapshot_is_the_one_restored():
    fly = Fly()
    run(drill(fly))
    (argv,) = [a for a, _ in fly.calls if a[:3] == ["fly", "postgres", "create"]]
    assert argv[argv.index("--snapshot-id") + 1] == "vs_new"
    assert int(argv[argv.index("--volume-size") + 1]) >= 3


@pytest.mark.parametrize(
    "shown,ref",
    [
        ({"Registry": "r", "Repository": "p", "Digest": "sha256:1"}, "r/p@sha256:1"),
        ({"Registry": "r", "Repository": "p", "Tag": "t"}, "r/p:t"),
        (
            [
                {"Registry": "r", "Repository": "p", "Tag": "a"},
                {"Registry": "r", "Repository": "p", "Tag": "b"},
            ],
            None,
        ),  # fmt: skip
        ({"Registry": "r"}, None),
    ],
)
def test_image_ref(shown, ref):
    assert d.image_ref(shown) == ref


def test_a_value_with_white_space_is_refused_before_it_is_set():
    with pytest.raises(d.Stop):
        d.secrets_stdin({"ENCRYPTION_MASTER_KEY": "two words"})


# --- the reads of 11-18: HOST, CIO, Arch ------------------------------------------------


def test_the_block_holds_no_email_address():
    """HOST: whoami prints the account's email; the block goes on a public issue."""
    fly = Fly()
    _, printed = run(drill(fly))
    block = printed[printed.index(d.BLOCK_START) : printed.index(d.BLOCK_END)]
    import re

    assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", block)  # no email address
    assert "xian@example" not in block and "fly signed in: yes" in block


@pytest.mark.parametrize("where", ["machine run redis", "health"])
def test_an_interrupt_mid_run_still_destroys_everything_and_stops_the_proxy(where):
    """CIO, rule 3: a hang-up or kill takes the Ctrl-C path; the cleanup still runs."""
    FakeProxy.instances.clear()

    class Interrupting(Fly):
        def __call__(self, argv, stdin=None):
            if where in " ".join(argv):
                self.calls.append((argv, stdin))
                raise KeyboardInterrupt
            return super().__call__(argv, stdin)

    def request(method, url, form=None, bearer=None):
        if where == "health" and url.endswith("/health"):
            raise KeyboardInterrupt
        return ok_http(method, url, form, bearer)

    fly = Interrupting()
    code, printed = run(drill(fly, request=request))
    assert code == 1 and "STOPPED: interrupted" in printed
    assert not fly.apps - {"piper-morgan"}
    assert all(p.stopped for p in FakeProxy.instances)
    assert "If this stops, destroy these by hand" in printed


def test_a_taken_port_stops_before_the_password_is_sent():
    sent = []

    def request(method, url, form=None, bearer=None):
        sent.append(form)
        return ok_http(method, url, form, bearer)

    fly = Fly()
    code, printed = run(drill(fly, request=request, free=lambda: False))
    assert "is in use" in printed and code == 1
    assert not any(f and R_PASSWORD in f.values() for f in sent)
    assert not fly.apps - {"piper-morgan"}


def test_a_dead_proxy_gets_no_password():
    class DeadProxy(FakeProxy):
        def alive(self):
            return False

    sent = []

    def request(method, url, form=None, bearer=None):
        sent.append(form)
        return ok_http(method, url, form, bearer)

    fly = Fly()
    dr = drill(fly, request=request)
    dr.proxy_factory = DeadProxy
    code, printed = run(dr)
    assert "R's password was not sent" in printed
    assert not any(f and R_PASSWORD in f.values() for f in sent)


def test_a_failed_create_that_printed_the_password_keeps_it_out_of_the_block():
    """CIO: hold the password before the exit code is read."""

    class Leaky(Fly):
        def __call__(self, argv, stdin=None):
            if argv[:3] == ["fly", "postgres", "create"]:
                self.calls.append((argv, stdin))
                self.apps.add(argv[argv.index("--name") + 1])
                return 1, f"  Password: {DB_PASSWORD}\npostgres://postgres:{DB_PASSWORD}@x\n"
            return super().__call__(argv, stdin)

    fly = Leaky()
    code, printed = run(drill(fly))
    assert DB_PASSWORD not in printed and "[hidden]" in printed and code == 1
    assert not fly.apps - {"piper-morgan"}


def test_one_apps_cleanup_failure_does_not_stop_the_others():
    class Broken(Fly):
        def __call__(self, argv, stdin=None):
            if argv[:3] == ["fly", "volumes", "list"] and argv[4] == f"{APP}-db":
                raise OSError("broken pipe")
            return super().__call__(argv, stdin)

    fly = Broken()
    code, printed = run(drill(fly, request=lambda *a: (0, {})))
    assert f"destroy {APP}-db: stopped (OSError)" in printed
    assert f"destroy {APP}-redis: exit 0" in printed and f"destroy {APP}: exit 0" in printed


def test_nothing_without_the_drill_prefix_is_ever_destroyed():
    fly = Fly()
    dr = drill(fly)
    dr.attempted = ["piper-morgan"]
    dr.cleanup()
    assert not [a for a, _ in fly.calls if a[:3] == ["fly", "apps", "destroy"]]


def test_the_allowlist_and_env_carry_arch_s_closed_comment():
    source = (Path(d.__file__)).read_text()
    assert "allowlist is CLOSED" in source and "GITHUB_APP_" in source
    assert "PIPER_SLACK_INBOUND_ENABLED" in source


def test_printing_survives_a_closed_terminal(monkeypatch):
    def broken(*a, **k):
        raise OSError("EIO")

    monkeypatch.setattr("builtins.print", broken)
    d.safe_print("still going")  # must not raise


def test_the_decrypt_script_and_the_drill_agree_on_the_prefix():
    import verify_stored_credential_decrypt as v

    assert v.DRILL_APP_PREFIX == d.PREFIX and d.names(STAMP)["app"].startswith(d.PREFIX)
