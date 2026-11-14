"""The promote gate's tested-ancestor walk covers every parent of the served commit (issue 2363).

Seats push merge commits to main whose FIRST parent is the seat's branch line and whose SECOND
parent is main. Tests runs exist only for main heads, so a first-parent walk (`${SHA}^`) looked
down the wrong line and refused green code (run 43366687006, 2026-11-12). The step now walks
`${SHA}^@`. These tests run the step's own bash against a small graph of that shape, with a
stand-in `gh` that answers from a file of "sha conclusion" rows.

Acceptance is unchanged and pinned here too: a tested-path change since the chosen ancestor, or
an ancestor whose Tests is not success, still refuses.
"""

import os
import stat
import subprocess
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "fly-deploy.yml"
STEP = "Tests must have concluded success on the code staging serves"

FAKE_GH = r"""#!/usr/bin/env bash
# Stand-in for `gh api <url> -q <filter>`: answers the three reads the step makes from $FAKE_RUNS.
url="$2"; filter="$4"
case "$url" in
  *head_sha=*)
    sha="${url#*head_sha=}"; sha="${sha%%&*}"
    conc="$(awk -v s="$sha" '$1==s {print $2}' "$FAKE_RUNS")"
    if [[ "$filter" == *length* ]]; then
      if [ -n "$conc" ]; then echo 1; else echo 0; fi
    else
      echo "${conc:-none}"
    fi ;;
  *branch=main*) awk '{print $1}' "$FAKE_RUNS" ;;
  *) echo "unexpected gh call: $*" >&2; exit 2 ;;
esac
"""


def _run_block():
    steps = yaml.safe_load(WORKFLOW.read_text())["jobs"]["promote-alpha"]["steps"]
    return next(s for s in steps if s.get("name") == STEP)["run"]


_CLOCK = [1_700_000_000]


def _git(cwd, *args):
    # Each commit gets its own second, as on main: `git rev-list` orders by commit date, and
    # commits made inside one second here would tie and come back in no fixed order.
    _CLOCK[0] += 60
    stamp = f"{_CLOCK[0]} +0000"
    env = dict(os.environ, GIT_AUTHOR_DATE=stamp, GIT_COMMITTER_DATE=stamp)
    r = subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True, env=env)
    return r.stdout.strip()


def _commit(repo, path, text, msg):
    f = repo / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)
    _git(repo, "add", path)
    _git(repo, "commit", "-q", "-m", msg)
    return _git(repo, "rev-parse", "HEAD")


def _graph(tmp_path, *, tested_path_after_green=False):
    """main: init -> green (code) -> [code2?] -> docs ; seat: init -> seat-log ; head = merge(seat, main)."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "t")
    old = _commit(repo, "services/a.py", "a = 1\n", "init (old tested head)")
    _git(repo, "branch", "seat")
    green = _commit(repo, "services/a.py", "a = 2\n", "code on main, Tests green")
    if tested_path_after_green:
        _commit(repo, "services/b.py", "b = 1\n", "code on main, no Tests run yet")
    _commit(repo, "docs/note.md", "n\n", "docs on main")
    _git(repo, "checkout", "-q", "seat")
    _commit(repo, "dev/log.md", "l\n", "seat log")
    _git(repo, "merge", "-q", "--no-ff", "-m", "Merge main into seat", "main")
    head = _git(repo, "rev-parse", "HEAD")
    # The shape of the 11-12 refusal: first parent is the seat line, second parent is main.
    assert _git(repo, "rev-parse", "HEAD^1") != _git(repo, "rev-parse", "main")
    assert _git(repo, "rev-parse", "HEAD^2") == _git(repo, "rev-parse", "main")
    assert (
        subprocess.run(["git", "merge-base", "--is-ancestor", green, "HEAD^1"], cwd=repo).returncode
        == 1
    )  # the green commit is NOT on the first-parent line
    return repo, head, old, green


def _run(tmp_path, repo, head, runs):
    bindir = tmp_path / "bin"
    bindir.mkdir()
    gh = bindir / "gh"
    gh.write_text(FAKE_GH)
    gh.chmod(gh.stat().st_mode | stat.S_IEXEC)
    runs_file = tmp_path / "runs.txt"
    runs_file.write_text("".join(f"{sha} {conc}\n" for sha, conc in runs))
    env = dict(os.environ)
    env.update(
        PATH=f"{bindir}{os.pathsep}{env['PATH']}",
        FAKE_RUNS=str(runs_file),
        SHA=head,
        GITHUB_REPOSITORY="o/r",
        GH_TOKEN="not-a-real-value",
    )
    return subprocess.run(
        ["bash", "-e", "-c", _run_block()], cwd=repo, capture_output=True, text=True, env=env
    )


def test_the_step_walks_every_parent_and_says_why():
    run = _run_block()
    assert 'git rev-list --max-count=2000 "${SHA}^@"' in run
    assert '"${SHA}^")' not in run  # the first-parent-only walk is gone
    assert "issue 2363" in run and "EVERY parent" in run  # Arch: the comment says why it is ^@
    assert "${{" not in run  # values arrive by env, not by expression substitution


def test_a_merge_head_with_the_green_commit_on_its_second_parent_is_accepted(tmp_path):
    repo, head, old, green = _graph(tmp_path)
    r = _run(tmp_path, repo, head, [(green, "success"), (old, "success")])
    assert r.returncode == 0, r.stdout + r.stderr
    assert f"Tests concluded success on {green}" in r.stdout
    assert "differs from it only outside Tests' trigger paths" in r.stdout


def test_a_tested_path_changed_since_the_green_commit_still_refuses(tmp_path):
    repo, head, old, green = _graph(tmp_path, tested_path_after_green=True)
    r = _run(tmp_path, repo, head, [(green, "success"), (old, "success")])
    assert r.returncode == 1
    assert "Tests never ran on the code staging serves" in r.stdout
    assert "services/b.py" in r.stdout
    assert "searched from every parent" in r.stdout  # the refusal names the line it searched


def test_a_nearest_tested_ancestor_that_is_not_green_still_refuses(tmp_path):
    repo, head, old, green = _graph(tmp_path)
    r = _run(tmp_path, repo, head, [(green, "failure"), (old, "success")])
    assert r.returncode == 1
    assert "Tests not green on the staging code" in r.stdout
    assert "searched from every parent" in r.stdout


def test_no_tested_ancestor_at_all_refuses_and_names_the_search(tmp_path):
    repo, head, _old, _green = _graph(tmp_path)
    r = _run(tmp_path, repo, head, [("0" * 40, "success")])
    assert r.returncode == 1
    assert "No Tests run found" in r.stdout
    assert "searched from every parent, not the first only" in r.stdout


def test_a_run_on_the_served_commit_itself_is_read_first(tmp_path):
    repo, head, _old, green = _graph(tmp_path)
    r = _run(tmp_path, repo, head, [(head, "success"), (green, "failure")])
    assert r.returncode == 0, r.stdout + r.stderr
    assert f"Tests concluded success on {head}" in r.stdout
