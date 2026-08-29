"""#1568 — finish the /todos page: real inline edit, visible priority, human dates.

PM live-tested the page (2026-08-10):
- Edit was still a "coming soon" toast stub while PUT /api/v1/todos/{id}
  WORKS (#1548 fixed it against the real repo signature). The page must
  offer inline title editing wired to that route.
- Priority never displayed — a High todo's card showed Status + Due only,
  even though the API payload carries `priority` on every row.
- Due dates printed raw ISO ("Due: 2026-08-08T15:00:00+00:00"). The
  audit-endorsed pattern (docs/internal/operations/time-handling-audit-
  2026-08-10.md, the 23-correct-sites pattern) is aware-ISO from the server,
  browser-side toLocale* rendering in the USER's timezone.

CALL-SHAPE NOTE (the load-bearing contract): the real PUT route declares
`title` as a QUERY parameter — there is no Pydantic body model on it. A
JSON body {"title": ...} would be silently dropped by FastAPI, the route
would build an empty updates dict, and the page would toast success while
changing nothing — exactly the #1541 delete lie in a new shape. So the
page must send `?title=` on the PUT. The route side of this contract is
pinned in tests/unit/web/api/routes/test_todos_put_call_shape_1568.py.

Layer: real Jinja template.render() through the app_shell (the UI-fix
discipline — a curl-200 proves nothing about what the page does). The page
builds its rows and requests in inline JS, so JS assertions here are
string-presence pins on the rendered HTML: they prove the shipped script
carries the behavior, not that a browser executed it (that's the E2E layer).
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


def _save_fn(rendered):
    """The saveTodoTitle() block of the inline script."""
    m = re.search(r"async function saveTodoTitle\(.*?\n  \}\n", rendered, re.DOTALL)
    assert m, "saveTodoTitle() not found in rendered page"
    return m.group(0)


# --- edit: the stub must be gone, replaced by a real inline flow -------------


def test_coming_soon_edit_stub_is_gone(rendered):
    assert "coming_soon" not in rendered, (
        "editTodo() is still the 'coming soon' toast stub while the PUT "
        "route works (#1548) — #1568 finding (1)"
    )


def test_edit_renders_inline_input_with_save_and_cancel(rendered):
    """Edit swaps the title for an input prefilled with the current title,
    plus Save/Cancel controls."""
    assert "edit-title-input" in rendered, "no inline edit input in the row markup"
    assert "saveTodoTitle" in rendered, "no save handler wired"
    assert "cancelEditTodo" in rendered, "no cancel handler wired"
    assert re.search(r"save-edit-btn[^>]*>\s*Save", rendered), "no Save button"
    assert re.search(r"cancel-edit-btn[^>]*>\s*Cancel", rendered), "no Cancel button"
    # The input must be prefilled with the todo's current title
    assert re.search(
        r'edit-title-input[^>]*value="\$\{', rendered
    ), "edit input is not prefilled with the current title"


def test_edit_put_sends_title_as_query_param_matching_the_real_route(rendered):
    """The real route takes `title` as a QUERY param (no body model) — a JSON
    body would be silently dropped and the toast would lie (#1541 pattern).
    Route half of the contract: test_todos_put_call_shape_1568.py."""
    body = _save_fn(rendered)
    assert "method: 'PUT'" in body, "saveTodoTitle() does not PUT"
    assert re.search(r"\?title=\$\{encodeURIComponent\(", body), (
        "PUT does not carry title as an encoded query param — the shape the "
        "real route actually reads"
    )
    assert "JSON.stringify" not in body, (
        "saveTodoTitle() sends a JSON body — the PUT route has no body model, "
        "so the title would be silently dropped (success toast, no change)"
    )


def test_edit_failure_is_an_honest_error_toast(rendered):
    """Failing-first: success toast only after response.ok; refusal surfaces
    as an error toast — never success-toast-then-nothing (#1541's lie)."""
    body = _save_fn(rendered)
    ok_pos = body.find("response.ok")
    toast_pos = body.find("ToastMessages.success('todo_updated')")
    assert ok_pos != -1, "saveTodoTitle() never checks response.ok"
    assert toast_pos != -1, "saveTodoTitle() has no success toast"
    assert ok_pos < toast_pos, "success toast fires before/without checking the response"
    assert (
        "ToastMessages.error('update_error'" in body
    ), "no honest error toast when the API refuses the update"


# --- priority chip -----------------------------------------------------------


def test_row_renders_a_priority_chip(rendered):
    assert (
        "priority-chip" in rendered
    ), "cards render Status + Due but never priority — #1568 finding (2)"
    # The chip's modifier class must be driven by the todo's actual priority
    assert re.search(
        r"priority-chip priority-\$\{", rendered
    ), "priority chip class is not driven by todo.priority"


def _css_rules(rendered):
    """selector-text -> declaration-text for every rule in the page styles."""
    return {sel.strip(): decl for sel, decl in re.findall(r"([^{}]+)\{([^{}]*)\}", rendered)}


def test_priority_css_covers_every_real_enum_value(rendered):
    """The four classes must be the TodoPriority .value strings — not guessed."""
    for p in TodoPriority:
        assert (
            f".priority-{p.value}" in rendered
        ), f"no chip styling for the real enum value '{p.value}'"


def test_high_and_urgent_are_visually_distinct_from_low_and_medium(rendered):
    """Layer: CSS source, not pixels — we assert high/urgent get declarations
    different from the subtle low/medium rule (a browser-visual check is E2E)."""
    rules = _css_rules(rendered)

    def decl_for(cls):
        matches = [d for s, d in rules.items() if cls in s]
        assert matches, f"no CSS rule for {cls}"
        return " ".join(matches)

    low = decl_for(".priority-low")
    assert decl_for(".priority-medium") == low or ".priority-medium" in str(
        [s for s in rules if ".priority-low" in s]
    ), "low/medium should share the subtle treatment"
    assert (
        decl_for(".priority-high") != low
    ), ".priority-high styled identically to low — not visually distinct"
    assert (
        decl_for(".priority-urgent") != low
    ), ".priority-urgent styled identically to low — not visually distinct"


# --- humanized due dates ------------------------------------------------------


def test_due_date_renders_through_the_local_formatter_not_raw_iso(rendered):
    assert "formatDueDate(todo.due_date)" in rendered, (
        "due date is not routed through a formatter — raw ISO reaches the user "
        "(#1568 finding (3))"
    )
    assert not re.search(
        r"Due:\s*\$\{todo\.due_date\}", rendered
    ), "row still interpolates the raw ISO string into 'Due:'"


def test_formatter_uses_browser_local_toLocale_rendering(rendered):
    """The audit-endorsed pattern: aware-ISO from the server, browser renders
    in the USER's timezone via toLocale*."""
    assert "toLocaleDateString" in rendered, "no browser-local date rendering"
    assert "toLocaleTimeString" in rendered, "no browser-local time rendering for timed due dates"


def test_midnight_utc_all_day_values_render_date_only(rendered):
    """Midnight-UTC values are all-day-ish (the <input type=date> create path
    stores YYYY-MM-DD → 00:00:00+00:00): the time is meaningless, and the
    calendar date must be read in UTC so the picked day never shifts."""
    m = re.search(r"function formatDueDate\(.*?\n  \}\n", rendered, re.DOTALL)
    assert m, "formatDueDate() not found in rendered page"
    body = m.group(0)
    assert (
        "getUTCHours() === 0" in body
    ), "formatter never distinguishes midnight-UTC all-day values"
    assert "timeZone: 'UTC'" in body, (
        "all-day branch must read the calendar date in UTC — otherwise the "
        "picked day shifts for any user west of UTC"
    )
