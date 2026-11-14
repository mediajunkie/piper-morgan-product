"""scripts/check-deploy-trigger-parity.sh: two directions, a run-time exemption, the file-glob mapping.

Issue 2369 (CIO's placement, Arch's ruling, 2026-11-13). The deploy trigger's `paths-ignore` mirrors
`.dockerignore`. The check blocks only the dangerous direction (the trigger ignores a path the image
contains), warns on the harmless one, and exempts a harmless row that git cannot see change: no
tracked file under it and `.gitignore` ignores it.

Each test copies the script into a throwaway git repo and runs it there.
"""

import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "scripts" / "check-deploy-trigger-parity.sh"

WORKFLOW = """name: deploy
on:
  push:
    branches: [main]
    paths-ignore:
{rows}
  workflow_dispatch:
jobs: {{}}
"""


def _git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def _repo(tmp_path, *, dockerignore, paths_ignore, gitignore="", tracked=()):
    root = tmp_path / "r"
    (root / "scripts").mkdir(parents=True)
    (root / ".github" / "workflows").mkdir(parents=True)
    shutil.copy(SCRIPT, root / "scripts" / SCRIPT.name)
    (root / ".dockerignore").write_text("\n".join(dockerignore) + "\n")
    rows = "\n".join(f"      - '{p}'" for p in paths_ignore)
    (root / ".github" / "workflows" / "fly-deploy.yml").write_text(WORKFLOW.format(rows=rows))
    (root / ".gitignore").write_text(gitignore)
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "t@example.com")
    _git(root, "config", "user.name", "t")
    for rel in tracked:
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("x\n")
        _git(root, "add", "-f", rel)
    return root


def _run(root, *args):
    return subprocess.run(
        ["bash", str(root / "scripts" / SCRIPT.name), *args], capture_output=True, text=True
    )


BASE_DI = [".git", ".github", "dev/", "*.log", ".dockerignore"]
BASE_PI = [".github/**", "dev/**", "**/*.log"]


def test_an_exact_mirror_is_ok(tmp_path):
    r = _run(_repo(tmp_path, dockerignore=BASE_DI, paths_ignore=BASE_PI))
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK — paths-ignore mirrors .dockerignore (3 patterns, 0 exempt)" in r.stdout


def test_a_file_glob_row_maps_to_itself_not_to_a_directory(tmp_path):
    """CIO's find: `config/*.user.md` was expected as `config/*.user.md/**`, which matches nothing."""
    root = _repo(
        tmp_path,
        dockerignore=BASE_DI + ["config/*.user.md"],
        paths_ignore=BASE_PI + ["config/*.user.md"],
    )
    r = _run(root, "--strict")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "config/*.user.md/**" not in r.stdout
    assert "(4 patterns, 0 exempt)" in r.stdout


def test_a_trigger_pattern_missing_from_dockerignore_blocks(tmp_path):
    """The dangerous direction: such a push can change the image and would not deploy."""
    root = _repo(tmp_path, dockerignore=BASE_DI, paths_ignore=BASE_PI + ["docs/**"])
    r = _run(root)
    assert r.returncode == 1
    assert "DANGEROUS" in r.stdout and "    docs/**" in r.stdout


def test_the_dangerous_direction_is_never_exempted(tmp_path):
    """Even when the path is gitignored and untracked, a trigger-only pattern still blocks."""
    root = _repo(
        tmp_path,
        dockerignore=BASE_DI,
        paths_ignore=BASE_PI + ["data/redis/**"],
        gitignore="data/redis/\n",
    )
    r = _run(root)
    assert r.returncode == 1
    assert "DANGEROUS" in r.stdout and "    data/redis/**" in r.stdout
    assert "exempt —" not in r.stdout


def test_a_harmless_row_warns_and_passes_and_strict_fails(tmp_path):
    """A tracked directory in .dockerignore the trigger does not ignore: an unneeded deploy."""
    kw = dict(dockerignore=BASE_DI + ["tests/"], paths_ignore=BASE_PI, tracked=["tests/t.py"])
    root = _repo(tmp_path, **kw)
    r = _run(root)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "WARNING" in r.stdout and "    tests/**" in r.stdout
    assert "OK with warnings" in r.stdout
    strict = _run(root, "--strict")
    assert strict.returncode == 1
    assert "DRIFT (--strict)" in strict.stdout


def test_untracked_gitignored_rows_are_exempt_by_name(tmp_path):
    """Main's shape on 2026-11-13: a file glob and two data directories, all gitignored."""
    root = _repo(
        tmp_path,
        dockerignore=BASE_DI + ["config/*.user.md", "data/postgres/", "data/redis/"],
        paths_ignore=BASE_PI,
        gitignore="*.user.md\ndata/postgres/\ndata/redis/\n",
    )
    r = _run(root, "--strict")
    assert r.returncode == 0, r.stdout + r.stderr
    for row in ("    config/*.user.md", "    data/postgres/**", "    data/redis/**"):
        assert row in r.stdout
    assert "(3 patterns, 3 exempt)" in r.stdout
    assert "WARNING" not in r.stdout


def test_the_exemption_lapses_when_a_file_is_force_added(tmp_path):
    """Arch: a force-added file under an exempt path makes the row harmless drift again."""
    root = _repo(
        tmp_path,
        dockerignore=BASE_DI + ["data/redis/"],
        paths_ignore=BASE_PI,
        gitignore="data/redis/\n",
        tracked=["data/redis/dump.rdb"],
    )
    r = _run(root)
    assert r.returncode == 0
    assert "WARNING" in r.stdout and "    data/redis/**" in r.stdout
    assert "exempt —" not in r.stdout
    assert _run(root, "--strict").returncode == 1


def test_an_untracked_row_that_is_not_gitignored_is_not_exempt(tmp_path):
    """Both conditions are needed: a file could be committed there by an ordinary push."""
    root = _repo(tmp_path, dockerignore=BASE_DI + ["scratch/"], paths_ignore=BASE_PI)
    r = _run(root)
    assert r.returncode == 0
    assert "WARNING" in r.stdout and "    scratch/**" in r.stdout
    assert "exempt —" not in r.stdout


def test_an_unknown_argument_is_refused(tmp_path):
    r = _run(_repo(tmp_path, dockerignore=BASE_DI, paths_ignore=BASE_PI), "--stirct")
    assert r.returncode == 2


def test_main_is_ok_under_strict_and_code_quality_runs_the_check():
    r = subprocess.run(["bash", str(SCRIPT), "--strict"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    lint = (REPO / ".github" / "workflows" / "lint.yml").read_text()
    assert "./scripts/check-deploy-trigger-parity.sh" in lint
    assert lint.count("- '.dockerignore'") == 2  # a push or PR that edits it runs the check
