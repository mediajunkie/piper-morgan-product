"""F1 #1170 Part B — native-dialog → Dialog/Toast migration (content assertions).

The `scripts/native_dialog_lint.py` gate (baseline at zero) enforces the NEGATIVE
("no native confirm/alert/prompt reachable"). These assertions guard the POSITIVE —
that each migrated caller now routes through the design-floor `Dialog.*` primitive
or `Toast`/`ToastMessages` — so a future edit can't satisfy the lint by simply
deleting the user-facing notification, and so the insights.html asset wiring
(which loads dialog.js) can't silently regress (Dialog would be undefined).
"""
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


def _read(*parts: str) -> str:
    return (ROOT.joinpath(*parts)).read_text()


@pytest.fixture
def insights() -> str:
    return _read("templates", "insights.html")


@pytest.fixture
def home() -> str:
    return _read("templates", "home.html")


# --- insights.html: confirm + 2 prompts + alert, plus the asset include --------

def test_insights_loads_dialog_assets(insights):
    # Self-contained Dialog.open needs dialog.js (+ css); insights.html doesn't
    # include the #confirmation-dialog partial, so these are the only requirement.
    assert "/static/js/dialog.js" in insights, "insights.html must load dialog.js"
    assert "/static/css/dialog.css" in insights, "insights.html must load dialog.css"


def test_insights_delete_uses_dialog_confirm(insights):
    assert "await Dialog.confirm(" in insights
    assert "Remove this insight?" in insights


def test_insights_reset_uses_dialog_prompt_with_validate(insights):
    assert "await Dialog.prompt(" in insights
    # the RESET gate is preserved as a validate() rule
    assert "validate:" in insights
    assert "'RESET'" in insights


def test_insights_why_uses_dialog_alert(insights):
    assert "await Dialog.alert(" in insights


def test_insights_handlers_are_async(insights):
    assert "async function handleDelete(" in insights
    assert "async function handleReset(" in insights


# --- home.html: 3 toast errors + 1 dialog confirm ------------------------------

def test_home_delete_uses_dialog_confirm(home):
    assert "await Dialog.confirm(" in home
    assert "Delete this conversation?" in home


def test_home_errors_use_toast_messages(home):
    assert "ToastMessages.error('update_error'" in home
    assert "ToastMessages.error('archive_error'" in home
    assert "ToastMessages.error('delete_error'" in home


# --- the other migrated files --------------------------------------------------

def test_insight_card_uses_dialog_confirm():
    card = _read("templates", "components", "insight_card.html")
    assert "async function handleDelete(" in card
    assert "await Dialog.confirm(" in card


def test_navigation_uses_toast_not_alert():
    nav = _read("templates", "components", "navigation.html")
    assert "Toast.error('Logout failed'" in nav


def test_learning_dashboard_uses_dialog_confirm():
    ld = _read("templates", "learning-dashboard.html")
    assert "await Dialog.confirm(" in ld


def test_chat_save_error_uses_toast_messages():
    chat = _read("web", "static", "js", "chat.js")
    assert "ToastMessages.error('save_error')" in chat


# --- the new toast key + the gate baseline is at zero --------------------------

def test_archive_error_toast_key_exists():
    tm = _read("web", "static", "js", "toast-messages.js")
    assert "archive_error:" in tm


def test_native_dialog_baseline_is_zero():
    baseline = _read(".native-dialog-lint-baseline.txt")
    # zeroed: no non-blank signature lines remain
    assert [ln for ln in baseline.splitlines() if ln.strip()] == []
