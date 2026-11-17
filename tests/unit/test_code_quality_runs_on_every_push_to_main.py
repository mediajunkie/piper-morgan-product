"""Code Quality runs on every push to main, whatever the push changed.

Issue 2392's credential-shape step reads every tracked text file outside mail, docs and
logs. On 2026-11-16 the workflow's push trigger still had a path filter, and 307 tracked
files sat outside it (alembic/, config/, .claude/, the root's docker-compose.yml and
fly.toml among them). A key pasted into one of those, in a push that touched nothing
else, would have run no gate in CI.
"""

from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[2] / ".github" / "workflows" / "lint.yml"


def _triggers():
    loaded = yaml.safe_load(WORKFLOW.read_text())
    # PyYAML reads the bare key ``on`` as the boolean True.
    return loaded.get("on") or loaded.get(True)


def test_a_push_to_main_has_no_path_filter():
    push = _triggers()["push"]
    assert push["branches"] == ["main"]
    assert "paths" not in push and "paths-ignore" not in push


def test_the_credential_shape_step_is_in_the_workflow():
    text = WORKFLOW.read_text()
    assert "scripts/staged_credential_scan.py --tracked --baseline" in text
    assert "scripts/mailbox_bearer_lint.py --roots mailboxes docs dev" in text
