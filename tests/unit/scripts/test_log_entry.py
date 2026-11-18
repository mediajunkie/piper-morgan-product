"""scripts/log-entry.sh (the clock rule, xian's yes 2026-11-18): appends a heading with the clock's
time to today's log for the role, never creates a log, and refuses an unclear role or log."""

import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "log-entry.sh"


@pytest.fixture
def repo(tmp_path):
    top = tmp_path / "cio"
    top.mkdir()
    subprocess.run(["git", "init", "-q", str(top)], check=True)
    return top


def todays_dir(top):
    day = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    d = top / "dev" / day[:4] / day[5:7] / day[8:10]
    d.mkdir(parents=True)
    return d, day


def run(top, *args):
    return subprocess.run(["bash", str(SCRIPT), *args], cwd=top, capture_output=True, text=True)


def test_appends_a_clock_heading_to_todays_log(repo):
    d, day = todays_dir(repo)
    log = d / f"{day}-0744-cio-code-log.md"
    log.write_text("# log\n")
    r = run(repo, "Mail wake: Exec")
    assert r.returncode == 0, r.stderr
    assert re.fullmatch(r"# log\n\n## \d{2}:\d{2} Mail wake: Exec\n\n", log.read_text())


def test_level_and_role_options(repo):
    d, day = todays_dir(repo)
    log = d / f"{day}-0900-exec-code-log.md"
    log.write_text("")
    r = run(repo, "--role", "exec", "--level", "3", "Step A")
    assert r.returncode == 0, r.stderr
    assert re.search(r"^### \d{2}:\d{2} Step A$", log.read_text(), re.M)


def test_no_log_for_today_is_refused_and_nothing_is_created(repo):
    r = run(repo, "START")
    assert r.returncode == 2 and "no session log" in r.stderr
    assert not (repo / "dev").exists()


def test_two_logs_for_today_are_refused(repo):
    d, day = todays_dir(repo)
    (d / f"{day}-0744-cio-code-log.md").write_text("")
    (d / f"{day}-1200-cio-code-log.md").write_text("")
    r = run(repo, "START")
    assert r.returncode == 2 and "more than one" in r.stderr


@pytest.mark.parametrize("args", [[], ["--level", "5", "x"], ["--role", "Ci/o", "x"]])
def test_bad_usage_is_refused(repo, args):
    assert run(repo, *args).returncode == 2
