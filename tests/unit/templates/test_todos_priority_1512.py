"""#1512 — the /todos Add form must offer priority; due-date absence must be visible.

Findings behind this suite:
- The DB and API fully support priority, and the Slack /standup "Today"
  bucket selects todos where priority == "high"
  (services/integrations/slack/webhook_router.py) — but the page's Add form
  had NO priority control, so every page-created todo was stuck at the
  "medium" default and Today could never populate from the UI.
- Due dates rendered only when set (`${todo.due_date ? ... : ''}`), so a todo
  with no due date gave no signal that a due date was even a thing.

Layer: real Jinja template.render() through the app_shell (the UI-fix
discipline — a curl-200 proves nothing about what the page does). The page
builds its rows and requests in inline JS, so JS assertions here are
string-presence pins on the rendered HTML: they prove the shipped script
carries priority, not that a browser executed it (that's the E2E layer).

The allowed priority values are read from the REAL enum
(services.shared_types.TodoPriority) — the select must offer exactly the
.value strings the String-typed DB column stores (#1472 banned raw-enum
comparisons; the wire format is the .value string).
"""

import re
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

from services.shared_types import TodoPriority

REPO = Path(__file__).resolve().parents[3]
TEMPLATES = REPO / "templates"

_USER = {"username": "xian", "user_id": "u1", "is_admin": False}


@pytest.fixture(scope="module")
def rendered():
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    return env.get_template("todos.html").render(trust_stage=1, user=_USER)


# --- priority control in the Add form ---------------------------------------


def test_add_form_has_a_priority_select(rendered):
    assert "new-todo-priority" in rendered, (
        "Add form has no priority control — #1512: page-created todos are "
        "stuck at 'medium' and /standup's Today bucket can never populate "
        "from the UI"
    )


def test_priority_select_offers_the_real_enum_values(rendered):
    """Options must be the TodoPriority .value strings — not guessed labels."""
    m = re.search(
        r'<select id="new-todo-priority".*?</select>', rendered, re.DOTALL
    )
    assert m, "priority select not found in Add form"
    select = m.group(0)
    for p in TodoPriority:
        assert f'value="{p.value}"' in select, (
            f"priority select is missing the real enum value '{p.value}'"
        )
    # No invented values beyond the enum
    offered = set(re.findall(r'value="([^"]+)"', select))
    assert offered == {p.value for p in TodoPriority}


def test_priority_select_defaults_to_medium(rendered):
    """The API/DB default is 'medium'; the form should say so, not imply blank."""
    m = re.search(
        r'<select id="new-todo-priority".*?</select>', rendered, re.DOTALL
    )
    assert m
    assert re.search(r'value="medium"[^>]*selected', m.group(0)), (
        "medium is the server-side default and should be preselected"
    )


def test_create_js_threads_priority_into_the_request(rendered):
    """String-presence pin on the inline script (see module docstring for the
    layer caveat): the create fetch body must carry priority."""
    assert re.search(
        r"getElementById\('new-todo-priority'\)", rendered
    ), "createNewTodo() never reads the priority select"
    assert "priority: priority" in rendered, (
        "create request body does not carry priority — the select would be "
        "decoration (#1541's due_date lesson: a field the page doesn't send "
        "can never persist)"
    )


def test_standup_today_value_is_offerable(rendered):
    """/standup's Today bucket filters on the literal string 'high'
    (webhook_router: _priority(t) == 'high') — the UI must be able to send it."""
    assert 'value="high"' in rendered


# --- due-date visibility -----------------------------------------------------


def test_todo_without_due_date_shows_an_affordance_not_nothing(rendered):
    """Rows must render an always-visible due-date slot: 'No due date' when
    unset, instead of silently omitting the line."""
    assert "No due date" in rendered, (
        "no visible affordance for todos without a due date — #1512 "
        "readability half"
    )
    # The empty-string branch (render nothing when unset) must be gone
    assert not re.search(r"todo\.due_date\s*\?[^:]+:\s*''", rendered), (
        "due-date render still collapses to '' when unset"
    )
