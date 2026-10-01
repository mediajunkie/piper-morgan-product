"""#1912 — clicking Remove on a project showed a success toast while the
project stayed listed (and the chat duplicate-check still saw it, because
the project was never actually deleted server-side).

ROOT CAUSE (found by reading the whole `deleteProject()` handler in
`templates/projects.html`, not a fragment of it): the fetch to the DELETE
endpoint was commented out as a TODO stub. The confirm dialog fired, the
success toast fired unconditionally, and `loadProjects()` re-fetched the
same still-present project from the server — the exact "success toast over
a no-op" shape #1824 names. The backend route
(`web/api/routes/projects.py::delete_project`) and repository
(`services/database/repositories.py::BaseRepository.delete`) were already
correct — owner-scoped hard delete, honest 404 on not-found/not-owned
(#1464 already fixed the un-awaited `session.delete` bug there). This is a
template-only fix; route behavior is pinned separately in
`tests/unit/web/api/routes/test_projects.py::TestDeleteProjectRoute1912`.

LAYER (m-43): this file is a SOURCE PIN on the shipped template, in the
same style as `test_setup_wizard_step1_honest_1875.py` — it does not spin
up a browser to execute the inline JS (no DOM/fetch harness in this
suite), so it cannot prove runtime behavior; it proves the shipped source
no longer contains the stub, calls the real endpoint, and gates the
success toast on reading the response BODY (not just `response.ok`).

DENOMINATOR: covers `templates/projects.html`'s `deleteProject()` handler
only. Does not cover `components/project_config_panel.html` (repo-unlink /
integration-remove — different, already-wired DELETE calls, out of scope
for #1912) or a live-browser click-through.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
PROJECTS_HTML = REPO_ROOT / "templates" / "projects.html"


def _delete_project_handler() -> str:
    js = PROJECTS_HTML.read_text()
    start = js.index("function deleteProject(")
    end = js.index("function shareProject(")
    assert start < end
    return js[start:end]


def test_todo_stub_is_gone():
    handler = _delete_project_handler()
    assert "TODO" not in handler, "the commented-out stub must not come back"


def test_handler_calls_the_real_delete_endpoint():
    handler = _delete_project_handler()
    assert "method: 'DELETE'" in handler
    assert "fetch(`/api/v1/projects/${projectId}`" in handler
    assert "credentials: 'include'" in handler


def test_success_toast_is_gated_on_the_response_body_not_status_alone():
    """The bug was a success toast fired with NO check at all. The fix
    must not merely add a `response.ok` check (a 2xx with an unconfirmed
    body is still not proof of deletion) — it must read the JSON body and
    gate on its `status` field before reporting success."""
    handler = _delete_project_handler()

    fetch_at = handler.index("fetch(`/api/v1/projects/${projectId}`")
    ok_at = handler.index("if (!response.ok)")
    json_at = handler.index("response.json()")
    body_check_at = handler.index("data.status !== 'deleted'")
    success_at = handler.index("ToastMessages.success('project_deleted')")

    assert fetch_at < ok_at < json_at < body_check_at < success_at, (
        "success must be reported only after fetch -> ok-check -> body "
        "read -> body-confirms-deletion, in that order"
    )


def test_not_found_or_not_owned_is_handled_distinctly_and_resyncs_the_list():
    """A 404 (not found, or owned by someone else — the route can't tell
    those apart and 404s either way) must not be silently swallowed into
    the generic error path, and must refresh state from the server rather
    than leaving a stale row."""
    handler = _delete_project_handler()
    assert "response.status === 404" in handler
    not_found_branch = handler[handler.index("response.status === 404") :]
    await_reload_at = not_found_branch.index("await loadProjects()")
    return_at = not_found_branch.index("return;")
    assert (
        await_reload_at < return_at
    ), "the 404 branch must refresh the list from the server before returning"


def test_every_outcome_branch_refreshes_from_the_server():
    """Never just hide the row client-side — every terminal branch that
    believes it knows the new state must re-fetch from the server."""
    handler = _delete_project_handler()
    assert handler.count("await loadProjects()") >= 3, (
        "success, 404, and unconfirmed-2xx branches must each resync " "from the server"
    )
