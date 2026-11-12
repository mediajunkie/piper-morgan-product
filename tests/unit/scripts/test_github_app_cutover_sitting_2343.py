"""#2343: the GitHub App cutover sitting as one command with hidden prompts.

Pins rules 2 to 4 of canonical-ops-recipes.md section 10: no value in argv or in the
block, a failed step stops the run, and the half-set state is named.

Every "secret" in this file is a made-up string, not a credential.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
_spec = importlib.util.spec_from_file_location(
    "github_app_cutover_sitting", ROOT / "scripts" / "github_app_cutover_sitting.py"
)
cs = importlib.util.module_from_spec(_spec)
sys.modules["github_app_cutover_sitting"] = cs
_spec.loader.exec_module(cs)

CLIENT_ID = "fake-client-id-value"
CLIENT_SECRET = "fake-client-secret-value"
SLUG = "piper-test-app"
VALUES = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "slug": SLUG}
SHA = "d4fd55e6c56413e5affe3e80ee942cb962667f6f"


def _counts(found, applied=False):
    head = "APPLIED" if applied else "DRY RUN (nothing changed; pass --apply to change it)"
    return (
        f"github app cutover: {head}\n"
        "  ran at 2026-11-12T20:00:00Z\n"
        f"  classic grants found                         {found}\n"
        f"  classic tokens deleted                       {found if applied else 0}\n"
    )


class World:
    """A fake Fly, git, GitHub and beta. Records every command and its standard input."""

    def __init__(self, fail=None, github="bad_verification_code", answers=("yes", "yes")):
        self.fail = fail or set()
        self.github_answer = github
        self.answers = list(answers)
        self.calls = []
        self.printed = []
        self.grants = 3
        self.t = 0.0
        self.restarted_at = None
        self.mcp_sha = "5a87cce789" + "0" * 30

    def runner(self, argv, stdin):
        self.calls.append((list(argv), stdin))
        key = " ".join(argv[:3])
        if argv[:3] == ["fly", "secrets", "import"]:
            key = f"import {argv[4]}"
            if key not in self.fail and argv[4] == cs.MAIN_APP:
                self.restarted_at = self.t
            # A flyctl that echoed what it was given must still not leak.
            return (1 if key in self.fail else 0), f"Updating {argv[4]}\n{stdin}"
        if argv[:3] == ["fly", "ssh", "console"]:
            apply = argv[-1].endswith("--apply")
            # dry0 is the run before anything is set, dry1 the one after, dry2 the last.
            earlier = [c for c, _ in self.calls[:-1] if c[:3] == argv[:3]]
            dry_runs = sum(1 for c in earlier if not c[-1].endswith("--apply"))
            key = "apply" if apply else f"dry{dry_runs}"
            if key in self.fail:
                return 1, "Error: host unavailable"
            if apply:
                found, self.grants = self.grants, 0
                return 0, _counts(found, applied=True)
            return 0, "Connecting to fdaa:0:1...\n" + _counts(self.grants)
        if key in self.fail:
            return 1, "failed"
        return 0, ""

    def health(self):
        up = 99999 if self.restarted_at is None else self.t - self.restarted_at
        return {"status": "healthy", "git_sha": SHA, "services": {"uptime_seconds": up}}

    def mcp_health(self):
        return {"status": "healthy", "git_sha": self.mcp_sha} if self.mcp_sha else {}

    def github(self, client_id, client_secret):
        assert (client_id, client_secret) == (CLIENT_ID, CLIENT_SECRET)
        return self.github_answer

    def confirm(self, prompt):
        return self.answers.pop(0)

    def sleep(self, seconds):
        self.t += seconds

    def clock(self):
        self.t += 1.0
        return self.t

    def sitting(self):
        return cs.Sitting(
            runner=self.runner,
            health=self.health,
            mcp_health=self.mcp_health,
            github=self.github,
            confirm=self.confirm,
            sleep=self.sleep,
            clock=self.clock,
            out=self.printed.append,
        )

    def go(self, cutover_only=False):
        s = self.sitting()
        orig = s.run_all
        s.run_all = lambda only: orig(only, ask=lambda: dict(VALUES))
        code = cs.main(["--cutover-only"] if cutover_only else [], sitting=s)
        return code, "\n".join(self.printed)

    def argvs(self):
        return [" ".join(c) for c, _ in self.calls]


def test_a_full_run_sets_the_values_and_applies_the_cutover():
    w = World()
    code, text = w.go()
    assert code == 0
    assert "RESULT: DONE" in text
    assert cs.HALF_STATE not in text
    order = [a for a in w.argvs() if a.startswith("fly secrets") or a.startswith("fly ssh")]
    dry = f"fly ssh console -a {cs.MAIN_APP} -C python {cs.CUTOVER_IN_IMAGE}"
    assert order == [
        dry,
        f"fly secrets import -a {cs.MCP_APP}",
        f"fly secrets import -a {cs.MAIN_APP}",
        dry,
        dry + " --apply",
        dry,
    ]


def test_no_value_is_ever_in_argv():
    w = World()
    w.go()
    for argv, _ in w.calls:
        joined = " ".join(argv)
        assert CLIENT_ID not in joined
        assert CLIENT_SECRET not in joined


def test_the_values_reach_fly_on_standard_input_and_only_the_slug_reaches_the_mcp_app():
    w = World()
    w.go()
    stdin = {argv[4]: given for argv, given in w.calls if argv[:3] == ["fly", "secrets", "import"]}
    assert stdin[cs.MCP_APP] == f"GITHUB_APP_SLUG={SLUG}\n"
    assert stdin[cs.MAIN_APP] == (
        f"GITHUB_APP_CLIENT_ID={CLIENT_ID}\n"
        f"GITHUB_APP_CLIENT_SECRET={CLIENT_SECRET}\n"
        f"GITHUB_APP_SLUG={SLUG}\n"
    )


def test_nothing_printed_carries_a_value_even_when_fly_echoes_it():
    w = World(fail={f"import {cs.MAIN_APP}"})
    code, text = w.go()
    assert code == 1
    assert CLIENT_ID not in text
    assert CLIENT_SECRET not in text
    assert "[hidden]" in text


@pytest.mark.parametrize(
    "fail, last_step",
    [
        ("fly auth whoami", "whoami"),
        ("git cat-file -e", "cat-file"),
        ("git merge-base --is-ancestor", "merge-base"),
        ("dry0", "ssh"),
    ],
)
def test_a_failed_check_stops_before_any_value_is_asked_for_or_set(fail, last_step):
    w = World(fail={fail})
    code, text = w.go()
    assert code == 1
    assert "STOPPED" in text and "RESULT: NOT FINISHED" in text
    assert not any(a.startswith("fly secrets") for a in w.argvs())
    assert last_step in w.argvs()[-1]
    assert cs.HALF_STATE not in text


def test_a_pair_github_refuses_stops_before_anything_is_set():
    w = World(github="incorrect_client_credentials")
    code, text = w.go()
    assert code == 1
    assert "incorrect_client_credentials" in text
    assert not any(a.startswith("fly secrets") for a in w.argvs())


def test_without_a_typed_yes_nothing_is_set():
    w = World(answers=("y", "yes"))
    code, text = w.go()
    assert code == 1
    assert not any(a.startswith("fly secrets") for a in w.argvs())


def test_a_failed_mcp_step_leaves_the_main_app_untouched():
    w = World(fail={f"import {cs.MCP_APP}"})
    code, text = w.go()
    assert code == 1
    assert f"fly secrets import -a {cs.MAIN_APP}" not in w.argvs()
    assert cs.HALF_STATE not in text


@pytest.mark.parametrize("fail", [f"import {cs.MAIN_APP}", "dry1", "apply", "dry2"])
def test_a_failure_after_the_main_app_is_set_names_the_half_state(fail):
    w = World(fail={fail})
    code, text = w.go()
    assert code == 1
    assert "RESULT: NOT FINISHED" in text
    assert cs.HALF_STATE in text


def test_declining_the_apply_names_the_half_state_and_applies_nothing():
    w = World(answers=("yes", "no"))
    code, text = w.go()
    assert code == 1
    assert not any(a.endswith("--apply") for a in w.argvs())
    assert cs.HALF_STATE in text


def test_the_apply_prompt_says_how_many_tokens_it_deletes():
    w = World()
    _, text = w.go()
    assert "revokes and deletes 3 classic GitHub token(s)" in text


def test_classic_grants_left_after_the_apply_is_a_failure():
    w = World()
    real = w.runner

    def sticky(argv, stdin):
        code, out = real(argv, stdin)
        if argv[-1].endswith("--apply"):
            w.grants = 1
        return code, out

    w.runner = sticky
    code, text = w.go()
    assert code == 1
    assert "still finds classic grants (1)" in text
    assert cs.HALF_STATE in text


def test_cutover_only_asks_for_nothing_and_sets_nothing():
    w = World(answers=("yes",))
    code, text = w.go(cutover_only=True)
    assert code == 0 and "RESULT: DONE" in text
    assert not any(a.startswith("fly secrets") for a in w.argvs())
    assert sum(1 for a in w.argvs() if a.endswith("--apply")) == 1


def test_the_block_holds_the_three_cutover_outputs_with_their_times():
    w = World()
    _, text = w.go()
    block = text.split(cs.BLOCK_START)[1].split(cs.BLOCK_END)[0]
    assert block.count("github app cutover: DRY RUN") == 3
    assert block.count("github app cutover: APPLIED") == 1
    assert block.count("ran at ") == 4
    assert "Connecting to" not in block


def test_the_wait_needs_an_uptime_younger_than_the_set():
    w = World()
    s = w.sitting()
    w.restarted_at = None  # beta never restarted: uptime stays large
    with pytest.raises(cs.Stop):
        s.wait_for_restart(w.clock(), limit_s=60)


def test_hidden_prompts_and_value_shape():
    asked = []

    def hidden(prompt):
        asked.append(prompt)
        return CLIENT_ID if "ID" in prompt else CLIENT_SECRET

    assert cs.ask_values(hidden, lambda p: f" {SLUG.upper()} ") == VALUES
    assert len(asked) == 2 and all("input hidden" in a for a in asked)
    with pytest.raises(cs.Stop):
        cs.ask_values(lambda p: "has a space", lambda p: SLUG)
    with pytest.raises(cs.Stop):
        cs.ask_values(hidden, lambda p: "not/a/slug")


def test_the_command_takes_no_value_argument():
    with pytest.raises(SystemExit):
        cs.main(["--client-secret", CLIENT_SECRET])


def test_an_mcp_app_that_cannot_be_read_stops_before_anything_is_set():
    w = World()
    w.mcp_sha = ""
    code, text = w.go()
    assert code == 1
    assert "recipe 11, step 2a" in text
    assert not any(a.startswith("fly secrets") or a.startswith("fly ssh") for a in w.argvs())


def test_the_mcp_check_asks_git_about_the_bearer_fix_and_the_served_sha():
    w = World()
    w.go()
    assert f"git merge-base --is-ancestor {cs.MCP_NEEDS_COMMIT} {w.mcp_sha}" in w.argvs()
    assert len(cs.MCP_NEEDS_COMMIT) == 40


def test_cutover_only_warns_about_an_old_mcp_app_and_still_finishes():
    w = World(fail={"git merge-base --is-ancestor"}, answers=("yes",))
    code, text = w.go(cutover_only=True)
    assert code == 0 and "RESULT: DONE" in text
    assert "WITHOUT the bearer fix" in text


@pytest.mark.parametrize("word", ["REFUSED", "ERROR"])
@pytest.mark.parametrize("which", ["apply", "dry"])
def test_a_refused_or_error_line_stops_the_run_even_with_exit_zero(word, which):
    w = World()
    real = w.runner
    seen = {"dry": 0}

    def lying(argv, stdin):
        code, out = real(argv, stdin)
        if argv[:3] == ["fly", "ssh", "console"]:
            is_apply = argv[-1].endswith("--apply")
            if not is_apply:
                seen["dry"] += 1
            if (which == "apply" and is_apply) or (which == "dry" and seen["dry"] == 2):
                return 0, f"github app cutover: {word}. Nothing was changed."
        return code, out

    w.runner = lying
    code, text = w.go()
    assert code == 1
    assert f"the cutover script answered {word}" in text
    assert "RESULT: NOT FINISHED" in text and cs.HALF_STATE in text
    if which == "dry":
        assert not any(a.endswith("--apply") for a in w.argvs())


def test_an_apply_that_prints_a_dry_run_line_is_not_taken_as_applied():
    w = World()
    real = w.runner

    def wrong(argv, stdin):
        if argv[:3] == ["fly", "ssh", "console"] and argv[-1].endswith("--apply"):
            return 0, _counts(3)
        return real(argv, stdin)

    w.runner = wrong
    code, text = w.go()
    assert code == 1
    assert "no 'github app cutover: APPLIED' line" in text


def test_an_unexpected_exception_after_the_set_still_prints_the_block_and_the_half_state():
    w = World()
    real = w.health

    def breaks():
        if w.restarted_at is not None:
            raise RuntimeError(f"connection reset while sending {CLIENT_SECRET}")
        return real()

    w.health = breaks
    code, text = w.go()
    assert code == 1
    assert "STOPPED: unexpected RuntimeError" in text
    assert cs.BLOCK_START in text and cs.HALF_STATE in text
    assert CLIENT_SECRET not in text and "connection reset" not in text


def test_the_block_carries_the_client_id_masked_and_never_whole():
    w = World()
    _, text = w.go()
    assert f"client ID (masked): {CLIENT_ID[:4]}…{CLIENT_ID[-4:]}" in text
    assert CLIENT_ID not in text
    assert cs.masked("short") == "(too short to mask)"


def test_unreadable_rows_after_the_apply_get_a_note_in_the_block():
    w = World()
    real = w.runner

    def with_unreadable(argv, stdin):
        code, out = real(argv, stdin)
        if argv[:3] == ["fly", "ssh", "console"]:
            out += "  rows that could not be read (left alone)     2\n"
        return code, out

    w.runner = with_unreadable
    code, text = w.go()
    assert code == 0
    assert "NOTE: 2 row(s) could not be read" in text
