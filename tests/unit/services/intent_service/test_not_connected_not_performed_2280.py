"""#2280 (Arch 2026-11-04 18:34, the #2188 rule): the house not-connected reply is an
operation not performed. Every chat site that returns it answers ``success=False`` with
``intent_data["not_performed"] = "not_connected"``, and the text is unchanged.

Denominator, by the reply text in ``services/intent/intent_service.py``: 14
``IntentProcessingResult`` calls whose message says "isn't connected yet", plus the list
helper ``_github_list_read_failed``'s never-connected branch (its message is a variable).
Excluded and why: the standup's calendar source line ("meetings aren't included") sits
inside an answer that was given, and the canonical connection-status reply answers the
question that was asked.
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from services.intent_service.not_performed import (
    NOT_PERFORMED_KEY,
    NOT_PERFORMED_KINDS,
    NotPerformed,
    mark_not_performed,
    was_not_performed,
)

ROOT = Path(__file__).resolve().parents[4]
SRC = ROOT / "services/intent/intent_service.py"
REPLY = "isn't connected yet"


def _strings(node: ast.AST) -> str:
    return "".join(
        n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)
    )


def _reply_sites():
    tree = ast.parse(SRC.read_text(encoding="utf-8"))
    sites = []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call) and getattr(node.func, "id", "") == "IntentProcessingResult"
        ):
            continue
        kw = {k.arg: k.value for k in node.keywords}
        if "message" in kw and REPLY in _strings(kw["message"]):
            sites.append((node.lineno, kw))
    return sorted(sites, key=lambda s: s[0])


SITES = _reply_sites()


def test_the_denominator():
    assert len(SITES) == 14, [line for line, _ in SITES]


@pytest.mark.parametrize("line, kw", SITES, ids=[f"line{line}" for line, _ in SITES])
def test_each_site_is_not_performed(line, kw):
    success = kw.get("success")
    assert isinstance(success, ast.Constant) and success.value is False, f"line {line}"
    data = kw.get("intent_data")
    assert isinstance(data, ast.Dict), f"line {line}"
    marked = [
        v
        for k, v in zip(data.keys, data.values)
        if isinstance(k, ast.Name) and k.id == "NOT_PERFORMED_KEY"
    ]
    assert len(marked) == 1, f"line {line}"
    assert ast.unparse(marked[0]) == "NotPerformed.NOT_CONNECTED", f"line {line}"


def test_the_reply_text_is_unchanged():
    src = SRC.read_text(encoding="utf-8")
    assert src.count("GitHub isn't connected yet. Connect it in Settings → Integrations, ") == 10
    assert "Google Calendar isn't connected yet, so I can't see your meetings. " in src


def test_the_kind_is_one_of_the_set():
    assert NotPerformed.NOT_CONNECTED == "not_connected"
    assert NotPerformed.NOT_CONNECTED in NOT_PERFORMED_KINDS
    data = mark_not_performed({"action": "x"}, NotPerformed.NOT_CONNECTED)
    assert data[NOT_PERFORMED_KEY] == "not_connected"
    assert was_not_performed(SimpleNamespace(intent_data=data))


def _helper():
    from services.intent.intent_service import IntentService

    svc = IntentService.__new__(IntentService)
    svc.logger = SimpleNamespace(warning=lambda *a, **k: None)
    return svc._github_list_read_failed


def test_the_list_helper_marks_never_connected():
    from services.integrations.github.read_failed import GitHubReadFailed

    rf = GitHubReadFailed("no credential", None, detail="no_credential")
    result = _helper()(rf, "list_issues_query", "issues")
    assert result.success is False
    assert result.intent_data[NOT_PERFORMED_KEY] == NotPerformed.NOT_CONNECTED
    assert result.message == (
        "GitHub isn't connected yet. Connect it in Settings → Integrations, "
        "and I can list its issues."
    )


def test_the_list_helpers_other_branches_keep_their_shape():
    from services.integrations.github.read_failed import GitHubReadFailed
    from services.mcp.consumer.connector import DegradationReason

    rf = GitHubReadFailed("down", DegradationReason.UNREACHABLE, repo="o/r", detail="x")
    result = _helper()(rf, "list_issues_query", "issues")
    assert result.success is False
    assert NOT_PERFORMED_KEY not in result.intent_data
