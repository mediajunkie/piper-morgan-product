"""Arch 2026-11-17: a push that changes only a template or only the CLI must run the
Tests workflow, and a template or shared-script change must run Architecture
Enforcement, whose escape-helper test reads them.

On 2026-11-17 a template change turned main red, and its fix did not re-run
Architecture Enforcement, because neither workflow's trigger named ``templates/**``.

Layer: the workflow files' text. Nothing is run on GitHub.
"""

from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[2]


def _paths(workflow: str, event: str):
    data = yaml.safe_load((ROOT / ".github" / "workflows" / workflow).read_text(encoding="utf-8"))
    triggers = data.get("on") or data.get(True)  # YAML reads a bare ``on`` as True
    return triggers[event]["paths"]


@pytest.mark.parametrize("event", ("push", "pull_request"))
@pytest.mark.parametrize("path", ("templates/**", "cli/**", "services/**", "web/**", "tests/**"))
def test_the_tests_workflow_runs_on_every_tested_tree_in_the_image(event, path):
    assert path in _paths("test.yml", event)


@pytest.mark.parametrize("event", ("push", "pull_request"))
@pytest.mark.parametrize("path", ("templates/**", "web/static/js/**"))
def test_architecture_enforcement_runs_when_what_its_escape_test_reads_changes(event, path):
    assert path in _paths("architecture-enforcement.yml", event)


# --- the promote gate's own list (Arch 2026-11-17) --------------------------------------
#
# fly-deploy.yml's promote gate accepts "the nearest tested ancestor is green and no
# tested file changed since". Its idea of a tested file is a regex kept by hand beside
# test.yml's path list. If the regex lacks a path Tests runs on, a change there counts
# as "nothing tested changed" and the gate accepts a run that never saw it.

import re  # noqa: E402

_SAMPLE = {
    "services/**": "services/a/b.py",
    "tests/**": "tests/unit/test_x.py",
    "web/**": "web/app.py",
    "templates/**": "templates/integrations.html",
    "cli/**": "cli/commands/keys.py",
    "*.py": "main.py",
    "pyproject.toml": "pyproject.toml",
    "requirements*.txt": "requirements-dev.txt",
    "alembic/**": "alembic/versions/x.py",
    "scripts/**": "scripts/x.sh",
    ".github/workflows/**": ".github/workflows/test.yml",
}


def _gate_regex() -> "re.Pattern[str]":
    text = (ROOT / ".github" / "workflows" / "fly-deploy.yml").read_text(encoding="utf-8")
    found = re.findall(r"TESTED_PATHS_RE='([^']+)'", text)
    assert len(found) == 1, "the promote gate should define TESTED_PATHS_RE exactly once"
    return re.compile(found[0])


def test_every_path_tests_runs_on_has_a_sample_file_here():
    """A path added to test.yml must be added to _SAMPLE too, or this fails: that is
    what makes the comparison below cover it."""
    assert set(_paths("test.yml", "push")) == set(_SAMPLE)
    assert _paths("test.yml", "push") == _paths("test.yml", "pull_request")


@pytest.mark.parametrize("pattern", sorted(_SAMPLE))
def test_the_promote_gate_counts_every_path_tests_runs_on_as_tested(pattern):
    assert _gate_regex().search(_SAMPLE[pattern]), pattern


@pytest.mark.parametrize(
    "path", ("docs/x.md", "dev/2026/11/17/log.md", "mailboxes/lead/inbox/x.md", "a/main.py")
)
def test_the_promote_gate_does_not_count_untested_paths(path):
    assert not _gate_regex().search(path)
