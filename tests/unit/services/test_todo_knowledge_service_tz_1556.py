"""#1556: naive-local datetime class in TodoKnowledgeService.

Discovered by the #1493 audit's class sweep (2026-08-09) beyond the audited
todo-layer scope: `TodoKnowledgeService` used naive LOCAL `datetime.now()`
in two spots —
  - update_todo_relationships (:280) stamps a KG edge's metadata with
    `datetime.now().isoformat()` — a WRITE, just not against a SQL
    timestamptz column: it lands in a JSONB metadata blob, but the same
    server-offset drift applies once it's read back and parsed.
  - get_todo_recommendations (:220) computes `current_hour =
    datetime.now().hour` to bucket time-of-day recommendation patterns —
    server-local hour instead of a UTC-anchored one.

These tests pin aware-UTC behavior WITHOUT wall-clock assertions. An AST
guard pins the file at zero bare `datetime.now()` calls, with the
denominator (files checked) asserted per m-44. Idiom matched from
tests/unit/services/repositories/test_todo_repository_tz_1493.py.
"""

import ast
import os
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

from services.todo.todo_knowledge_service import TodoKnowledgeService


async def test_update_todo_relationships_writes_aware_utc_created_at():
    """RED-FIRST (write site): the KG edge metadata's created_at is written
    via datetime.now().isoformat() — a naive isoformat string has no UTC
    offset suffix; parsing it back must yield an aware datetime."""
    svc = TodoKnowledgeService.__new__(TodoKnowledgeService)
    svc.knowledge_graph = AsyncMock()
    svc.semantic_indexer = None

    related_node = MagicMock()
    related_node.id = "node-2"
    related_node.metadata = {"todo_id": "todo-2"}
    svc.knowledge_graph.get_nodes_by_type = AsyncMock(return_value=[related_node])
    svc.knowledge_graph.create_edge = AsyncMock()

    todo = MagicMock()
    todo.knowledge_node_id = "node-1"
    todo.id = "todo-1"
    todo.owner_id = "owner-1"

    await svc.update_todo_relationships(todo=todo, related_todo_ids=["todo-2"])

    svc.knowledge_graph.create_edge.assert_awaited_once()
    metadata = svc.knowledge_graph.create_edge.await_args.kwargs["metadata"]
    created_at = metadata["created_at"]
    parsed = datetime.fromisoformat(created_at)
    assert parsed.tzinfo is not None, (
        f"update_todo_relationships created_at is a NAIVE isoformat string "
        f"({created_at!r}) — the #1493/#1556 class: no UTC offset survives "
        f"a round trip, so a reader can't tell which timezone produced it"
    )


class TestNoNaiveDatetimeNowInTodoKnowledgeService1556:
    """AST guard: zero bare `datetime.now()` (no tz argument) in
    services/todo/todo_knowledge_service.py — covers both #1556 sites
    (:220 current_hour, :280 created_at), including :220 which can't be
    pinned behaviorally once reduced to a bare int via `.hour`."""

    FILES = ["services/todo/todo_knowledge_service.py"]

    @staticmethod
    def _is_bare_now(node) -> bool:
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "now"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "datetime"
            and not node.args
            and not node.keywords
        )

    def test_no_bare_datetime_now(self):
        violations = []
        files_checked = 0
        for rel in self.FILES:
            assert os.path.exists(rel), (
                f"{rel} missing — the #1556 guard's denominator is wrong; "
                f"update FILES rather than letting the scan go vacuous (m-44)"
            )
            files_checked += 1
            tree = ast.parse(open(rel, encoding="utf-8").read(), filename=rel)
            for node in ast.walk(tree):
                if self._is_bare_now(node):
                    violations.append(f"{rel}:{node.lineno}")

        assert (
            files_checked == len(self.FILES) == 1
        ), f"guard checked {files_checked} files, expected 1 (denominator)"
        assert not violations, (
            f"bare naive-local datetime.now() in todo_knowledge_service.py "
            f"(#1556) — use services.utils.datetime_utils.utc_now(): {violations} "
            f"(checked {files_checked} files)"
        )
