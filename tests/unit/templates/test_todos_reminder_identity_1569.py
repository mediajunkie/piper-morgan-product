"""#1569 — /todos visual identity for reminders (reminders ARE todos).

Reminders share storage with todos (unified model, PM-ratified); the page
previously rendered them as indistinguishable rows. #1569 gives them a
legible identity: (a) a "⏰ reminder" chip on the row (same chip pattern as
the #1568 priority chip), and (b) client-side grouping — reminder rows
cluster under their own "Reminders" heading, an empty group rendering
nothing. The signal is the payload's reminder_date field (threaded through
GET /api/v1/todos by #1569 — see
tests/unit/web/api/routes/test_todos_reminder_field_1569.py), never title
text.

LAYER (named honestly, the #1568/#1578 pattern): real Jinja
template.render() through the app_shell; the page builds rows in inline JS,
so JS assertions are string/regex pins on the rendered page source — they
prove the shipped script carries the behavior, not that a browser executed
it (that's the E2E layer). CSS assertions are on CSS source, not pixels.

Escaping: the chip label is a static literal (no user data), and the row
interpolates it as a composed fragment — covered by the #1578 ratchet
(_ALLOWED_COMPOSED) in test_todos_xss_escaping_1578.py.
"""

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

REPO = Path(__file__).resolve().parents[3]
TEMPLATES = REPO / "templates"

_USER = {"username": "xian", "user_id": "u1", "is_admin": False}


@pytest.fixture(scope="module")
def rendered():
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    return env.get_template("todos.html").render(trust_stage=1, user=_USER)


def _render_fn(rendered):
    m = re.search(r"function renderTodos\(.*?\n  \}\n", rendered, re.DOTALL)
    assert m, "renderTodos() not found in rendered page"
    return m.group(0)


# --- (a) the reminder chip ----------------------------------------------------


def test_reminder_rows_get_a_reminder_chip(rendered):
    body = _render_fn(rendered)
    assert "reminder-chip" in body, (
        "no reminder chip in the row markup — reminder rows are visually "
        "indistinguishable from plain todos"
    )
    assert "⏰ reminder" in body, "chip does not carry the '⏰ reminder' label"


def test_chip_is_keyed_off_reminder_date_not_title_text(rendered):
    """The identity signal is the threaded payload field — a todo titled
    'reminder to buy milk' must NOT grow a chip."""
    body = _render_fn(rendered)
    assert re.search(
        r"todo\.reminder_date\s*\?[^:]*reminder-chip", body, re.DOTALL
    ), "chip is not conditional on todo.reminder_date"
    assert (
        "todo.text.includes" not in body and "todo.text.match" not in body
    ), "reminder identity must never be inferred from title text"


def test_chip_reuses_the_priority_chip_pattern(rendered):
    """Same chip pattern as #1568's priority chip: shared .priority-chip base
    class for the shape, a .reminder-chip modifier for the identity color."""
    body = _render_fn(rendered)
    assert re.search(
        r'class="priority-chip reminder-chip"', body
    ), "reminder chip does not reuse the .priority-chip base pattern"
    assert ".reminder-chip" in rendered, "no CSS rule for the reminder chip"


def test_chip_label_is_static_no_user_data_interpolated(rendered):
    """The chip literal must contain no ${...} — its leaves are static, which
    is what qualifies it as a composed fragment under the #1578 ratchet."""
    body = _render_fn(rendered)
    m = re.search(r"`(<span class=\"priority-chip reminder-chip\">[^`]*)`", body)
    assert m, "reminder chip literal not found"
    assert "${" not in m.group(1), (
        "reminder chip interpolates dynamic data — it is pinned as a " "static composed fragment"
    )


# --- (b) grouping: Reminders cluster under their own heading -------------------


def test_reminders_cluster_under_their_own_heading(rendered):
    body = _render_fn(rendered)
    assert "Reminders</h2>" in body, (
        "no 'Reminders' group heading — reminder rows stay interleaved with " "plain todos"
    )
    assert re.search(
        r"todos\.filter\(\s*t\s*=>\s*t\.reminder_date\s*\)", body
    ), "no client-side reminder grouping keyed off reminder_date"
    assert re.search(
        r"todos\.filter\(\s*t\s*=>\s*!t\.reminder_date\s*\)", body
    ), "plain todos are not separated from reminder rows"


def test_empty_reminder_group_renders_nothing(rendered):
    """No reminders -> no heading: the section is gated on the group having
    rows (a heading over nothing is clutter, not identity)."""
    body = _render_fn(rendered)
    assert re.search(r"reminderTodos\.length\s*===\s*0\s*\?\s*''", body) or re.search(
        r"reminderTodos\.length\s*\?", body
    ), "the Reminders section is not gated on the group being non-empty"


def test_group_note_teaches_the_unified_model_on_the_page_too(rendered):
    """Explanation-first (PM's #1569 priority order) carries to the page: the
    group carries a one-line note on where reminders live and how they
    surface."""
    body = _render_fn(rendered)
    assert (
        "Reminders live with your todos" in body
    ), "no on-page explanation of the reminders-are-todos relationship"


# --- canary: same-day #1568/#1578 work stays intact ---------------------------


def test_1568_and_1578_behavior_untouched(rendered):
    assert "saveTodoTitle" in rendered
    assert "priority-chip priority-${" in rendered
    assert "formatDueDate(todo.due_date)" in rendered
    assert "${escapeHtml(todo.text)}" in rendered
