"""The pre-push hook's trigger lists against the Tests workflow's path list (standing row 9z).

Four hand-kept lists say which paths count as tested code: ``test.yml``'s ``on.push.paths``,
the promote gate's regex in ``fly-deploy.yml`` (Lead's test compares that one), and the
hook's ``code_re`` (smoke) and ``gates_re`` (gates). On 2026-11-17 three of them drifted in
one morning. This test compares the hook's two with the workflow's, and names every
difference that is a choice. A new path in ``test.yml`` fails here until someone decides,
in this file, whether the hook takes it.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
HOOK = (ROOT / "scripts" / "git-hooks" / "pre-push").read_text()
WORKFLOW = (ROOT / ".github" / "workflows" / "test.yml").read_text()

# One file a push might touch, for each path the Tests workflow triggers on.
SAMPLES = {
    "services/**": "services/intent/x.py",
    "tests/**": "tests/unit/test_x.py",
    "web/**": "web/api/x.py",
    "*.py": "main.py",
    "pyproject.toml": "pyproject.toml",
    "requirements*.txt": "requirements.txt",
    "alembic/**": "alembic/versions/x.py",
    "scripts/**": "scripts/x.py",
    ".github/workflows/**": ".github/workflows/x.yml",
    "templates/**": "templates/x.html",
    "cli/**": "cli/commands/x.py",
}

# Differences that are choices, each with who chose and why. Anything else is drift.
SMOKE_LEAVES_OUT = {
    "templates/**": "Lead 2026-11-17: the architecture check reads every template; smoke adds 2 files",
    "scripts/**": "CIO 2026-11-12: scripts pushes run the gates, not the smoke",
    ".github/workflows/**": "CIO 2026-11-12: workflow pushes run the gates, not the smoke",
    "pyproject.toml": "Lead 2026-11-17: gates only (ruff's settings); pytest reads pytest.ini",
}
GATES_LEAVE_OUT: dict = {}
# Every top-level Python file triggers both, as test.yml's `*.py` does (Lead, 2026-11-17:
# `main\.py$` missed the MCP entry point and the root conftest).
TOP_LEVEL_PY = ["main.py", "main_mcp.py", "conftest.py", "validate-phase5.py"]
# What the hook triggers on that the workflow does not (the gates read these; Tests does not).
GATES_ONLY = [".claude/hooks/x.sh", ".github/x.md", ".staged-credential-scan-baseline.txt"]
BOTH_ONLY = ["pytest.ini"]
# Never tested code: neither list may match these.
NEVER = ["docs/x.md", "dev/2026/11/17/x-log.md", "mailboxes/cio/inbox/x.md", "tools/main.py"]


def hook_regex(name):
    found = re.findall(rf"^{name}='(.*)'$", HOOK, flags=re.MULTILINE)
    assert len(found) == 1, f"{name} should be assigned exactly once in the hook"
    return re.compile(found[0])


def workflow_paths(event):
    """The ``paths:`` list under ``on.<event>`` in test.yml, read as text."""
    block = re.search(rf"^  {event}:\n(.*?)(?=^  \S|^\S)", WORKFLOW, flags=re.MULTILINE | re.DOTALL)
    assert block, f"no on.{event} block in test.yml"
    after = block.group(1).split("paths:", 1)
    assert len(after) == 2, f"no paths list under on.{event}"
    return re.findall(r"^\s+- '([^']+)'", after[1], flags=re.MULTILINE)


CODE, GATES, ARCH = hook_regex("code_re"), hook_regex("gates_re"), hook_regex("arch_re")
PUSH_PATHS = workflow_paths("push")


def test_every_workflow_path_has_a_sample_here():
    assert PUSH_PATHS, "read no paths from test.yml"
    missing = [p for p in PUSH_PATHS if p not in SAMPLES]
    assert not missing, (
        f"test.yml triggers on {missing}, which this test has no sample for. Decide whether "
        "the pre-push hook's code_re and gates_re take it, then add the sample here."
    )
    assert sorted(PUSH_PATHS) == sorted(workflow_paths("pull_request"))


@pytest.mark.parametrize("path", sorted(SAMPLES))
def test_smoke_list_matches_the_workflow_except_where_chosen(path):
    if path not in PUSH_PATHS:
        pytest.skip("not in test.yml's list any more; remove the sample")
    assert bool(CODE.search(SAMPLES[path])) == (path not in SMOKE_LEAVES_OUT), path


@pytest.mark.parametrize("path", sorted(SAMPLES))
def test_gates_list_matches_the_workflow_except_where_chosen(path):
    if path not in PUSH_PATHS:
        pytest.skip("not in test.yml's list any more; remove the sample")
    assert bool(GATES.search(SAMPLES[path])) == (path not in GATES_LEAVE_OUT), path


@pytest.mark.parametrize("name", TOP_LEVEL_PY)
def test_every_top_level_python_file_triggers_both(name):
    assert CODE.search(name) and GATES.search(name), name


def test_the_gates_also_run_on_what_only_they_read():
    for sample in GATES_ONLY:
        assert GATES.search(sample) and not CODE.search(sample), sample
    for sample in BOTH_ONLY:
        assert GATES.search(sample) and CODE.search(sample), sample


def test_everything_the_smoke_runs_on_the_gates_run_on():
    for sample in list(SAMPLES.values()) + BOTH_ONLY:
        if CODE.search(sample):
            assert GATES.search(sample), sample


def test_architecture_check_runs_on_the_three_served_trees():
    for sample in ("templates/x.html", "web/static/js/x.js", "services/x.py"):
        assert ARCH.search(sample) and GATES.search(sample), sample
    for sample in ("cli/commands/x.py", "tests/x.py", "scripts/x.py"):
        assert not ARCH.search(sample), sample


def test_untested_paths_trigger_nothing():
    for sample in NEVER:
        assert not CODE.search(sample) and not GATES.search(sample), sample
