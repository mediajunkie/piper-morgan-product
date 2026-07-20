"""#1452: the full-suite burn-down gate's own contract.

Pins the three verdicts (new-failure fails, shrink-lock fails, all-on-backlog
passes) and the blind-spot guards (no summary -> refuse; file-level collection
ERROR covers that file's backlog entries rather than reading as 'fixed')."""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO / "scripts" / "check_fullsuite_backlog.py"


def _run(tmp_path, output_text, backlog_text):
    out = tmp_path / "run.out"
    out.write_text(output_text)
    backlog = tmp_path / "backlog.tsv"
    backlog.write_text(backlog_text)
    # point the script at the temp backlog via a tiny wrapper env
    code = (
        "import sys, importlib.util, pathlib\n"
        f"spec = importlib.util.spec_from_file_location('chk', {str(SCRIPT)!r})\n"
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
        f"m.BACKLOG_FILE = pathlib.Path({str(backlog)!r})\n"
        f"sys.argv = ['chk', {str(out)!r}]\n"
        "sys.exit(m.main())\n"
    )
    return subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, cwd=REPO
    )


SUMMARY = "2 failed, 10 passed in 3.21s"


@pytest.mark.smoke
class TestFullsuiteBacklogGate:
    def test_all_failures_on_backlog_passes(self, tmp_path):
        r = _run(
            tmp_path,
            f"FAILED tests/a.py::test_x - boom\nFAILED tests/b.py::test_y\n{SUMMARY}\n",
            "tests/a.py::test_x\tfixture\ntests/b.py::test_y\ttriage\n",
        )
        assert r.returncode == 0, r.stdout + r.stderr
        assert "backlog size: 2" in r.stdout

    def test_new_failure_fails(self, tmp_path):
        r = _run(
            tmp_path,
            f"FAILED tests/a.py::test_x\nFAILED tests/c.py::test_NEW\n{SUMMARY}\n",
            "tests/a.py::test_x\tfixture\n",
        )
        assert r.returncode == 1
        assert "NEW failures" in r.stdout and "test_NEW" in r.stdout

    def test_shrink_lock_fails_when_backlog_entry_passes(self, tmp_path):
        r = _run(
            tmp_path,
            f"FAILED tests/a.py::test_x\n{SUMMARY}\n",
            "tests/a.py::test_x\tfixture\ntests/gone.py::test_fixed\ttriage\n",
        )
        assert r.returncode == 1
        assert "SHRINK-LOCK" in r.stdout and "test_fixed" in r.stdout

    def test_no_summary_refuses(self, tmp_path):
        r = _run(
            tmp_path,
            "FAILED tests/a.py::test_x\n",  # truncated: no summary line
            "tests/a.py::test_x\tfixture\n",
        )
        assert r.returncode != 0
        assert "REFUSING" in (r.stdout + r.stderr)

    def test_file_level_error_covers_backlog_entries(self, tmp_path):
        """A collection ERROR on the whole file must not read its per-test
        backlog entries as 'fixed' (they never ran)."""
        r = _run(
            tmp_path,
            f"ERROR tests/a.py - SystemExit\n1 failed, 5 passed in 1s\n",
            "tests/a.py::test_x\tfixture\ntests/a.py::test_y\tfixture\n",
        )
        assert r.returncode == 0, r.stdout + r.stderr

    def test_bad_tag_rejected(self, tmp_path):
        r = _run(
            tmp_path,
            f"FAILED tests/a.py::test_x\n{SUMMARY}\n",
            "tests/a.py::test_x\tblessed-forever\n",
        )
        assert r.returncode != 0
        assert "format error" in (r.stdout + r.stderr)
