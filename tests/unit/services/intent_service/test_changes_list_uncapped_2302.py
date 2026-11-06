"""#2302 (PA's #2275 preview, 11-06): "What changed in my tasks and projects this
week?" said "Tasks (7)" over three names. The changes reply listed ``created[:3]``
under a count of all of them, with nothing saying the list was partial. CXO's ruling:
every item, repeats grouped as the #2219 todo list groups them.

Reuses #2140's harness: the real ``_handle_changes_query`` with its three reads
(audit, todos, projects) stubbed at the session scope.
"""

import pytest

from tests.unit.services.intent_service.test_changes_query_fail_closed_2140 import (  # noqa: F401
    _intent,
    _project,
    _run,
    _todo,
    intent_service,
)


@pytest.mark.asyncio
async def test_every_created_item_is_listed_and_repeats_are_grouped(intent_service):
    todos = [
        _todo("audit the current navigation", 70),
        _todo("interview five current users", 60),
        _todo("review prs", 50),
        _todo("review prs", 40),
        _todo("review prs", 30),
        _todo("draft the launch checklist", 20),
        _todo("call the dentist", 10),
    ]
    result, _ = await _run(intent_service, _intent(), [], todos, [])
    message = result.message
    assert "**Tasks** (7):" in message and "Created: 7" in message
    for name in (
        "audit the current navigation",
        "interview five current users",
        "draft the launch checklist",
        "call the dentist",
    ):
        assert f"    - {name}" in message
    assert "    - review prs (×3)" in message
    assert message.count("review prs") == 1


@pytest.mark.asyncio
async def test_every_project_under_the_count_is_listed(intent_service):
    projects = [_project(f"Project {i}", 10 + i) for i in range(7)]
    result, _ = await _run(intent_service, _intent(), [], [], projects)
    assert "**Projects** (7):" in result.message
    for i in range(7):
        assert f"Project {i}" in result.message
