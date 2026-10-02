"""``what_piper_knows_about_me`` — the composite read-only tool (PM ruling + Arch
no-objection, 2026-10-01). Pins Arch's condition 1 (compose the resource handlers,
never re-implement) and its honest-degrade property: one failing section reads
``available: false`` for that section, never a failed tool call."""

from __future__ import annotations

import json

import pytest

from services.mcp.server import resources

pytestmark = pytest.mark.asyncio


async def test_composes_the_three_resource_handlers(monkeypatch) -> None:
    async def profile():
        return json.dumps({"available": True, "organization": "Org"})

    async def colleague():
        return json.dumps({"verified": [], "priorities": [], "note": "nothing confirmed yet"})

    async def issues():
        return json.dumps({"available": True, "issues": [], "count": 0, "capped_at": 50})

    monkeypatch.setattr(resources, "_read_profile", profile)
    monkeypatch.setattr(resources, "_read_colleague_model", colleague)
    monkeypatch.setattr(resources, "_read_github_issues", issues)

    out = await resources.what_piper_knows_about_me()

    assert out == {
        "profile": {"available": True, "organization": "Org"},
        "colleague_model": {"verified": [], "priorities": [], "note": "nothing confirmed yet"},
        "github_issues": {"available": True, "issues": [], "count": 0, "capped_at": 50},
    }


async def test_one_failing_section_degrades_alone(monkeypatch) -> None:
    async def profile():
        return json.dumps({"available": True, "organization": "Org"})

    async def boom():
        raise RuntimeError("github adapter exploded")

    async def colleague():
        return json.dumps({"verified": [], "priorities": []})

    monkeypatch.setattr(resources, "_read_profile", profile)
    monkeypatch.setattr(resources, "_read_colleague_model", colleague)
    monkeypatch.setattr(resources, "_read_github_issues", boom)

    out = await resources.what_piper_knows_about_me()

    assert out["profile"]["available"] is True
    assert out["github_issues"] == {"available": False, "reason": "read_failed"}


def test_tool_module_imports_no_llm_client() -> None:
    """Arch's condition 3, mechanically: no LLM client is reachable from the
    tool's module namespace."""
    names = set(vars(resources))
    assert not any(n.lower() in {"anthropic", "openai", "llm_client", "llmclient"} for n in names)
