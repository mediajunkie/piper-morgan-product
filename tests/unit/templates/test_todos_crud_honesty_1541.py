"""#1541 — the /todos page's CRUD surface must be real, not theater.

PM live-tested the page (2026-08-09):
- Delete showed "Done / Todo removed" and the row survived refresh. Root:
  deleteTodo()'s API call was COMMENTED OUT ("// TODO: Call API to delete")
  while the success toast fired unconditionally — a client-side lie, no
  request ever left the browser.
- No complete-task control existed at all (Edit was a coming-soon stub, so
  the only real controls were Remove [fake] and Share).

Real template.render() through the app_shell (the UI-fix discipline —
curl-200 proves nothing about what the page does), plus source-level pins on
the inline script, which is where both lies lived.
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


# --- delete honesty ---------------------------------------------------------


def test_delete_actually_calls_the_delete_api(rendered):
    """The DELETE fetch must be live code, not a comment."""
    assert "// TODO: Call API to delete" not in rendered, (
        "deleteTodo() still has the API call commented out — the page claims "
        "deletion while sending no request (#1541 root cause)"
    )
    # A real fetch with method DELETE against the todo resource
    assert re.search(
        r"fetch\(`/api/v1/todos/\$\{todoId\}`,\s*\{[^}]*method:\s*'DELETE'", rendered
    ), "no live DELETE fetch found in deleteTodo()"


def test_delete_success_toast_is_gated_on_response_ok(rendered):
    """The 'todo_deleted' toast may only fire after checking the response."""
    m = re.search(r"function deleteTodo\(.*?\n  \}\n", rendered, re.DOTALL)
    assert m, "deleteTodo() not found in rendered page"
    body = m.group(0)
    ok_pos = body.find("response.ok")
    toast_pos = body.find("ToastMessages.success('todo_deleted')")
    assert ok_pos != -1, "deleteTodo() never checks response.ok"
    assert toast_pos != -1, "deleteTodo() lost its success toast"
    assert ok_pos < toast_pos, (
        "success toast fires before/without checking the response — the "
        "claimed-success lie in a new shape"
    )
    assert "delete_error" in body, "no honest error path when the API refuses"


# --- complete control (did not exist) ---------------------------------------


def test_page_has_a_complete_control(rendered):
    assert "completeTodo(" in rendered, (
        "no complete-task control on the page — #1541 finding (1)"
    )
    assert "complete-btn" in rendered


def test_complete_calls_the_completion_route_and_checks_outcome(rendered):
    m = re.search(r"async function completeTodo\(.*?\n  \}\n", rendered, re.DOTALL)
    assert m, "completeTodo() not found in rendered page"
    body = m.group(0)
    assert re.search(
        r"fetch\(`/api/v1/todos/\$\{todoId\}/complete`,\s*\{[^}]*method:\s*'POST'", body
    ), "completeTodo() does not POST to the completion route"
    assert "response.ok" in body, "completeTodo() never checks the response"
    ok_pos = body.find("response.ok")
    toast_pos = body.find("ToastMessages.success('todo_completed')")
    assert toast_pos != -1 and ok_pos < toast_pos, (
        "completion success toast must be gated on response.ok"
    )


def test_completed_todos_do_not_offer_the_complete_button(rendered):
    """The button is built only for not-yet-completed todos."""
    m = re.search(r"function renderTodos\(.*?function createNewTodo", rendered, re.DOTALL)
    assert m, "renderTodos() not found"
    body = m.group(0)
    # The complete-button branch must consult completion state
    btn = body.find("complete-btn")
    assert btn != -1
    guard = re.search(r"if \(canEdit\(todo\) && !isCompleted\)", body)
    assert guard, "complete button is not guarded on completion state"


def test_toast_catalog_carries_the_completed_key():
    src = (REPO / "web/static/js/toast-messages.js").read_text()
    assert "todo_completed" in src, (
        "completeTodo() toasts 'todo_completed' but the catalog has no such key "
        "(showToastMessage would render an empty/unknown toast)"
    )


# --- due date wiring --------------------------------------------------------


def test_create_dialog_still_sends_due_date(rendered):
    """The page's half of the due-date chain (API half pinned in
    tests/unit/web/api/routes/test_todos_crud_1541.py)."""
    assert "new-todo-due-date" in rendered
    assert "due_date: dueDate" in rendered
