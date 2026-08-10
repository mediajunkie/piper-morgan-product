"""#1578 [SECURITY] — stored XSS in templates/todos.html client-side rendering.

renderTodos() interpolated ``${todo.text}`` (and a sweep found many sibling
fields) unescaped into ``container.innerHTML``. Todos are shareable (Share
button, shared-with-me route), so a crafted title shared to another account is
stored XSS running in the victim's session.

LAYER (named honestly): these tests verify the JS SOURCE escapes, not the
runtime DOM. The escaping happens client-side inside a JS template literal, so
a Jinja render proves only what the shipped script says — assertions here are
string/regex pins on the rendered page source. The runtime-DOM half lives in
the jsdom harness: tests/frontend/unit/todos-page-xss.test.js renders hostile
todos through the real extracted script and asserts no element injection.

Two contexts, two rules pinned here:
- HTML text/attribute contexts -> escapeHtml()/escapeAttr() on every
  interpolation (the sweep tests ratchet this: any future bare ``${...}`` in
  the render path fails).
- JS-string-inside-onclick context -> HTML-escaping CANNOT protect it (the
  HTML parser decodes entities before the JS engine parses the handler), so
  user-authored text must never appear there at all. The Share button used to
  pass ``'${todo.text}'`` into onclick — the title now travels via the
  currentTodos state lookup and only server-generated ids cross that boundary.
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


def _fn_body(rendered, signature):
    """Extract a top-level inline-script function body (two-space indent)."""
    m = re.search(rf"{re.escape(signature)}\(.*?\n  \}}\n", rendered, re.DOTALL)
    assert m, f"{signature}() not found in rendered page"
    return m.group(0)


# --- the helper itself --------------------------------------------------------


def test_escape_html_helper_exists_and_covers_the_metacharacters(rendered):
    """A single escapeHtml() source of truth; escapeAttr stays as the named
    attribute-context variant (the #1568 edit input already uses it)."""
    body = _fn_body(rendered, "function escapeHtml")
    for ch, entity in [
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ('"', "&quot;"),
        ("'", "&#39;"),
    ]:
        assert entity in body, f"escapeHtml() does not escape {ch!r} -> {entity}"
    assert "function escapeAttr" in rendered, (
        "escapeAttr() (attribute-context variant, #1568) went missing"
    )


# --- the headline hole: todo.text ---------------------------------------------


def test_raw_todo_text_interpolation_is_gone_everywhere(rendered):
    """The stored-XSS vector itself: ``${todo.text}`` must never appear bare —
    every surviving use goes through escapeHtml()/escapeAttr()."""
    assert "${todo.text}" not in rendered, (
        "todo.text is interpolated unescaped — a shared todo titled "
        "'<img src=x onerror=...>' executes in the recipient's session"
    )


def test_plain_title_row_escapes_todo_text(rendered):
    assert "${escapeHtml(todo.text)}" in rendered, (
        "the non-editing title branch does not escape todo.text"
    )


def test_share_button_no_longer_passes_title_through_onclick_js_string(rendered):
    """HTML-escaping cannot protect a JS string inside onclick (entities are
    decoded before the JS parses), so the title must not cross that boundary
    at all — only the server-generated id does."""
    assert not re.search(r"shareTodo\('\$\{[^}]*\}',\s*'\$\{[^}]*\}'\)", rendered), (
        "Share button still passes a second (text) argument through the "
        "onclick JS-string context — unprotectable by HTML escaping"
    )
    assert "shareTodo('${escapeAttr(todo.id)}')" in rendered, (
        "Share button should pass only the escaped id"
    )
    # and shareTodo() resolves the title from state instead
    body = _fn_body(rendered, "function shareTodo")
    assert "currentTodos" in body, (
        "shareTodo() must resolve the title from currentTodos state, not from "
        "an onclick-interpolated argument"
    )


# --- the sweep: every interpolation in the render path -------------------------

# Composed sub-template variables whose leaves are escaped where they are built.
_ALLOWED_COMPOSED = {
    "titleArea",
    "priorityChip",
    # #1569: static literal, no user data (pinned static in
    # test_todos_reminder_identity_1569.py::test_chip_label_is_static...)
    "reminderChip",
    "lifecycleIndicator",
    "actionButtons",
    "ownerIndicator",
}

_INNERMOST_INTERP = re.compile(r"\$\{([^{}]*)\}")


def _assert_all_escaped(body, fn_name, allowed=()):
    allowed = set(allowed)
    for expr in _INNERMOST_INTERP.findall(body):
        expr = expr.strip()
        ok = (
            expr.startswith("escapeHtml(")
            or expr.startswith("escapeAttr(")
            or expr in allowed
        )
        assert ok, (
            f"unescaped interpolation in {fn_name}(): ${{{expr}}} — every "
            "dynamic value in the render path goes through escapeHtml()/"
            "escapeAttr() (or is a composed, already-escaped fragment)"
        )


def test_every_interpolation_in_renderTodos_is_escaped_or_composed(rendered):
    """Ratchet: a future bare ``${...}`` added to renderTodos fails here.
    (Innermost interpolations only — outer conditional wrappers contain braces
    and are covered via their nested literals.)"""
    _assert_all_escaped(
        _fn_body(rendered, "function renderTodos"),
        "renderTodos",
        allowed=_ALLOWED_COMPOSED,
    )


def test_every_interpolation_in_renderCurrentShares_is_escaped(rendered):
    """Same ratchet for the share-modal list (share.user_email is another
    account's self-chosen string — hostile-capable)."""
    _assert_all_escaped(
        _fn_body(rendered, "function renderCurrentShares"),
        "renderCurrentShares",
    )


# --- named field sites (the sweep proves coverage; these name the fields) ------


@pytest.mark.parametrize(
    "site",
    [
        # owner indicator (another user's self-chosen username)
        "${escapeHtml(todo.owner_username || todo.owner_id)}",
        # lifecycle: stage attr + phrase (attr and text uses)
        '${escapeAttr(todo.lifecycle_state)}',
        "${escapeAttr(phrase)}",
        "${escapeHtml(phrase)}",
        # priority chip: class attr + label text
        "priority-${escapeAttr(priority)}",
        "${escapeHtml(priority)}",
        # role badge
        "${escapeAttr(getRoleBadgeClass(role))}",
        "${escapeHtml(roleDisplay)}",
        # status line + due date (formatDueDate falls back to the raw value)
        "${escapeHtml(todo.status || 'pending')}",
        "${escapeHtml(formatDueDate(todo.due_date))}",
        # edit-mode input (the #1568 escaping, kept)
        'value="${escapeAttr(todo.text)}"',
        # share list: email/id, role badge, role label
        "${escapeHtml(share.user_email || share.user_id)}",
        "${escapeAttr(getRoleBadgeClass(share.role))}",
        "${escapeHtml(formatRole(share.role))}",
    ],
)
def test_field_site_is_escaped(rendered, site):
    assert site in rendered, f"expected escaped interpolation site missing: {site}"


def test_share_modal_content_escapes_its_onclick_ids(rendered):
    """openShareModal's form content builds an onclick too — ids/types are
    server-generated, but the HTML-attribute layer still gets escaped."""
    assert "addShare('${escapeAttr(resourceType)}', '${escapeAttr(resourceId)}')" in rendered
    # The modal TITLE (`Share ${resourceName}`) carries todo.text but feeds
    # Dialog.show(config.title), a textContent sink (web/static/js/dialog.js:78)
    # — safe by sink, pinned behaviorally in tests/frontend/unit/dialog.test.js.


def test_1568_behavior_untouched(rendered):
    """The fix must not disturb the same-day #1568 work: inline edit, priority
    chip, humanized dates. (Their own suite pins details; this is a canary.)"""
    assert "saveTodoTitle" in rendered
    assert "priority-chip" in rendered
    assert "formatDueDate(todo.due_date)" in rendered
