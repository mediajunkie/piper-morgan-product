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
