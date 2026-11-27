"""#2455: the project page reads the project's open todos.

The page said "No work items for this project" right after chat confirmed a todo
added to that project. Arch's rule (2026-11-27): a new owner-scoped route makes the
ONE call chat's "Open todos in <project>" makes (#2301), returns structured rows,
and a failed read is never an empty list. CXO's words (same day): two lines on the
page, and the Work Items section is hidden there.

Layer: the route through FastAPI's TestClient with the todo service and the project
repository replaced; and the template's source. What the page RENDERS is tested in
jsdom: tests/frontend/unit/project-page-todos-2455.test.js.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

TEMPLATE = Path("templates/project_detail.html")


@dataclass
class _Claims:
    sub: str


class _Page(list):
    capped = False


def _todo(text, priority="medium"):
    return SimpleNamespace(text=text, priority=priority, completed=False, status="pending")


def _client(user_id, project, todos=None, list_raises=None):
    from services.auth.auth_middleware import get_current_user
    from web.api.dependencies import get_project_repository
    from web.api.routes.projects import router

    repo = MagicMock()
    repo.get_by_id = AsyncMock(return_value=project)
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: _Claims(sub=user_id)
    app.dependency_overrides[get_project_repository] = lambda: repo

    service = MagicMock()
    if list_raises is not None:
        service.list_todos = AsyncMock(side_effect=list_raises)
    else:
        service.list_todos = AsyncMock(return_value=todos if todos is not None else _Page())
    return TestClient(app, raise_server_exceptions=False), repo, service


def _project(name="Launch"):
    return SimpleNamespace(id=str(uuid4()), name=name)


SERVICE = "services.todo.todo_management_service.TodoManagementService"


def test_one_open_todo_comes_back_as_one_structured_row():
    user_id, project = str(uuid4()), _project()
    client, repo, service = _client(user_id, project, _Page([_todo("send the invites")]))
    with patch(SERVICE, return_value=service):
        response = client.get(f"/api/v1/projects/{project.id}/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos": [{"text": "send the invites", "repeat": 1, "priority": None}],
        "count": 1,
        "cap_line": None,
        "project_id": project.id,
    }


def test_it_makes_the_one_call_chat_makes_and_no_other():
    """Arch: ``list_todos(user_id, include_completed=False, project_id)``, once."""
    user_id, project = str(uuid4()), _project()
    client, repo, service = _client(user_id, project)
    with patch(SERVICE, return_value=service):
        client.get(f"/api/v1/projects/{project.id}/todos")
    service.list_todos.assert_awaited_once_with(
        user_id=UUID(user_id), include_completed=False, project_id=project.id
    )
    assert [c[0] for c in service.method_calls] == ["list_todos"]


def test_ownership_is_checked_the_way_the_work_items_route_checks_it():
    user_id, project = str(uuid4()), _project()
    client, repo, service = _client(user_id, project)
    with patch(SERVICE, return_value=service):
        client.get(f"/api/v1/projects/{project.id}/todos")
    repo.get_by_id.assert_awaited_once_with(project.id, owner_id=user_id)


def test_someone_elses_project_is_a_404_and_no_todo_read_is_made():
    user_id = str(uuid4())
    client, repo, service = _client(user_id, None)
    with patch(SERVICE, return_value=service):
        response = client.get(f"/api/v1/projects/{uuid4()}/todos")
    assert response.status_code == 404
    service.list_todos.assert_not_awaited()


def test_a_failed_read_is_a_500_never_an_empty_list():
    user_id, project = str(uuid4()), _project()
    client, repo, service = _client(user_id, project, list_raises=RuntimeError("db down"))
    with patch(SERVICE, return_value=service):
        response = client.get(f"/api/v1/projects/{project.id}/todos")
    assert response.status_code == 500
    assert "todos" not in response.json()


def test_a_read_that_found_none_is_a_200_with_an_empty_list():
    user_id, project = str(uuid4()), _project()
    client, repo, service = _client(user_id, project, _Page())
    with patch(SERVICE, return_value=service):
        response = client.get(f"/api/v1/projects/{project.id}/todos")
    assert response.status_code == 200
    assert response.json()["todos"] == []
    assert response.json()["count"] == 0


def test_rows_keep_chats_order_grouping_and_priority_note():
    """The same lines ``format_todo_list_grouped`` numbers: a repeat is one row; only
    urgent and high carry a note (chat shows no note for medium or low)."""
    from services.consciousness.todo_consciousness import format_todo_list_grouped

    todos = _Page(
        [
            _todo("call the caterer", "urgent"),
            _todo("review prs", "high"),
            _todo("review prs", "high"),
            _todo("book the venue", "medium"),
            _todo("tidy the doc", "low"),
        ]
    )
    user_id, project = str(uuid4()), _project()
    client, repo, service = _client(user_id, project, todos)
    with patch(SERVICE, return_value=service):
        rows = client.get(f"/api/v1/projects/{project.id}/todos").json()["todos"]
    assert rows == [
        {"text": "call the caterer", "repeat": 1, "priority": "urgent"},
        {"text": "review prs", "repeat": 2, "priority": "high"},
        {"text": "book the venue", "repeat": 1, "priority": None},
        {"text": "tidy the doc", "repeat": 1, "priority": None},
    ]
    # The page's rows, written the way the page writes them, are chat's numbered lines.
    chat_lines = format_todo_list_grouped(todos, header="h").split("\n")[1:]
    page_lines = [
        f"{n}. {r['text']}"
        + (f" (×{r['repeat']})" if r["repeat"] > 1 else "")
        + (f" ({r['priority']})" if r["priority"] else "")
        for n, r in enumerate(rows, 1)
    ]
    assert page_lines == chat_lines


def test_a_capped_list_carries_chats_own_cap_line():
    from services.intent_service.project_status_todos import CAP_LINE

    todos = _Page([_todo("a"), _todo("b")])
    todos.capped = True
    user_id, project = str(uuid4()), _project("Launch")
    client, repo, service = _client(user_id, project, todos)
    with patch(SERVICE, return_value=service):
        data = client.get(f"/api/v1/projects/{project.id}/todos").json()
    assert data["cap_line"] == CAP_LINE.format(count=2, project="Launch")


# --- the template's source -------------------------------------------------


def _served_source() -> str:
    """The template without its Jinja comments: what can reach a browser."""
    return re.sub(r"\{#.*?#\}", "", TEMPLATE.read_text(), flags=re.S)


def test_the_page_carries_cxos_two_lines_word_for_word():
    served = _served_source()
    assert "'No open todos in this project.'" in served
    assert (
        "\"I couldn't check this project's todos just now. Reload the page to try again.\""
        in served
    )
    assert "<h2>Open todos</h2>" in served


def test_the_page_reads_the_todos_route_and_not_the_work_items_route():
    served = _served_source()
    assert "/api/v1/projects/${projectId}/todos" in served
    assert "/work-items" not in served


@pytest.mark.parametrize(
    "gone",
    [
        "Work Items",
        "No work items for this project",
        "Work items linked to this project will appear here.",
        'id="work-item-count"',
        'id="work-items-container"',
        "loadWorkItems",
        "renderWorkItems",
    ],
)
def test_the_work_items_section_is_not_served_on_the_project_page(gone):
    """CXO: hide it, don't rename it; its line promised something no person can do."""
    assert gone not in _served_source()
