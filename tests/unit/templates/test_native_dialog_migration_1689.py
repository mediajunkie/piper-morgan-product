"""#1689 — the two post-baseline native-dialog callers migrate to Dialog (F1 #1170).

The `scripts/native_dialog_lint.py` gate (baseline at zero) enforces the NEGATIVE.
These assertions guard the POSITIVE — that both migrated callers now route through
the design-floor `Dialog.*` primitive — so a future edit can't satisfy the lint by
deleting the user-facing notification. Mirrors
tests/unit/templates/test_native_dialog_migration_1170.py.

Layer note (m-43): the asset-reachability tests RENDER each page through the
app_shell layout (the layer that actually loads dialog.js/css), not curl-200 and
not source-scanning the child template — Dialog.alert/confirm are undefined at
runtime unless the shell's includes reach the rendered page.
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[3]


def _read(*parts: str) -> str:
    return (ROOT.joinpath(*parts)).read_text()


def _render(template_name: str) -> str:
    env = Environment(loader=FileSystemLoader(str(ROOT / "templates")), autoescape=True)
    return env.get_template(template_name).render(
        user={"username": "xian", "user_id": "u1", "is_admin": False}
    )


@pytest.fixture
def github() -> str:
    return _read("templates", "settings_github.html")


@pytest.fixture
def llm_keys() -> str:
    return _read("templates", "settings_llm_keys.html")


# --- settings_github.html: OAuth-start failure alert ---------------------------


def test_settings_github_renders_with_dialog_assets():
    html = _render("settings_github.html")
    assert "/static/js/dialog.js" in html, "settings_github must load dialog.js (via app_shell)"
    assert "/static/css/dialog.css" in html, "settings_github must load dialog.css (via app_shell)"


def test_settings_github_oauth_error_uses_dialog_alert(github):
    assert "await Dialog.alert(" in github
    assert "Could not start GitHub OAuth" in github, "error copy went missing"


def test_settings_github_has_no_native_dialogs(github):
    assert "window.alert(" not in github
    assert "window.confirm(" not in github


# --- settings_llm_keys.html: hard-delete confirm -------------------------------


def test_settings_llm_keys_renders_with_dialog_assets():
    html = _render("settings_llm_keys.html")
    assert "/static/js/dialog.js" in html, "settings_llm_keys must load dialog.js (via app_shell)"
    assert "/static/css/dialog.css" in html, "settings_llm_keys must load dialog.css (via app_shell)"


def test_settings_llm_keys_delete_uses_dialog_confirm(llm_keys):
    # Promise style (F1 #1170) — the handler is async and gates on the result.
    assert "await Dialog.confirm(" in llm_keys
    assert "if (!confirmed) return;" in llm_keys


def test_settings_llm_keys_delete_copy_preserved(llm_keys):
    # #1482 honesty set rides along unchanged (its own pins live in
    # test_delete_copy_honesty_1482.py; this is the migration-local guard).
    assert "really is gone" in llm_keys
    assert "destroy our copy" in llm_keys
    assert "until you revoke it there" in llm_keys


def test_settings_llm_keys_has_no_native_dialogs(llm_keys):
    assert "window.confirm(" not in llm_keys
    assert "window.alert(" not in llm_keys


# --- the gate itself goes quiet ------------------------------------------------


def test_native_dialog_gate_is_quiet():
    """Run the EXACT CI invocation (.github/workflows/lint.yml:102) from repo
    root — must exit 0 (zero NEW native dialog calls against the baseline)."""
    import subprocess
    import sys

    proc = subprocess.run(
        [
            sys.executable,
            "scripts/native_dialog_lint.py",
            "--baseline",
            ".native-dialog-lint-baseline.txt",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, f"native-dialog gate would fail CI:\n{proc.stdout}{proc.stderr}"
