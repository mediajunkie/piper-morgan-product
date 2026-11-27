"""#2458: a connected status read names its repository and claims priority only
from a label.

Served on beta 2026-11-27 (Path A, Web): "what's going on in my github?" answered
"one open issue right now, #1: Test issue for Piper, and it's flagged as high
priority", and never said which repository. The trace: the floor was handed the top
open issues of ANY priority under the heading "High-priority open issues", with no
repository in the data.

Layer: unit. The read's row shape, the gather's rows and the floor's context lines.
Not covered here: what the floor's model then writes (judged on Web's rerun).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversational_floor import (
    ConversationalFloor,
    open_issues_heading,
)


def _row(number, title, labels, repository="pipermorgan/piper-test"):
    return {
        "number": number,
        "title": title,
        "labels": labels,
        "updated_at": f"2026-11-{number:02d}",
        "uri": f"https://github.test/{number}",
        "repository_full_name": repository,
    }


def _patch_router(open_issues):
    router = MagicMock()
    router.initialize = AsyncMock(return_value=None)
    router.get_open_issues = AsyncMock(return_value=open_issues)
    return patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
        return_value=router,
    )


def _lines(context):
    return ConversationalFloor(llm_client=MagicMock())._format_domain_context(context)


# --- the read ------------------------------------------------------------------


@pytest.mark.asyncio
async def test_the_strict_read_says_which_repository_it_read():
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    router = GitHubIntegrationRouter.__new__(GitHubIntegrationRouter)
    router._user_id = "u"
    router.mcp_adapter = MagicMock()
    router.mcp_adapter.list_open_issues = AsyncMock(
        return_value=MagicMock(
            degradation=None,
            issues=[{"number": 1, "title": "Test issue for Piper", "state": "open", "labels": []}],
        )
    )
    rows = await router._open_issues_via_connector("pipermorgan", "piper-test", 100)
    assert rows[0]["repository_full_name"] == "pipermorgan/piper-test"
    assert rows[0]["repository"] == "piper-test"  # the older field is unchanged


# --- the gather ----------------------------------------------------------------


@pytest.mark.asyncio
async def test_each_row_carries_the_repository_the_read_was_made_against():
    with _patch_router([_row(1, "Test issue for Piper", [])]):
        result = await ContextAssembler()._compute_high_priority_issues("uid")
    assert result["high_priority_issues"][0]["repository"] == "pipermorgan/piper-test"
    assert result["high_priority_issues"][0]["labels"] == []


@pytest.mark.asyncio
async def test_a_row_from_a_read_that_names_no_repository_carries_none():
    row = _row(1, "t", [])
    del row["repository_full_name"]
    with _patch_router([row]):
        result = await ContextAssembler()._compute_high_priority_issues("uid")
    assert result["high_priority_issues"][0]["repository"] is None


# --- what the floor is told ----------------------------------------------------


def _context(issues, **extra):
    return {"high_priority_issues": issues, "open_issue_count": len(issues), **extra}


def _issue(number, title, labels, repository="pipermorgan/piper-test"):
    return {"number": number, "title": title, "labels": labels, "repository": repository}


def test_the_beta_case_one_unlabelled_issue_is_not_called_high_priority():
    """The served turn: one open issue, no priority label."""
    out = _lines(_context([_issue(1, "Test issue for Piper", [])]))
    block = out[out.index("- Open issues") :].split("\n- ")[0]
    assert "High-priority" not in out
    assert "high priority" not in block.lower()
    assert "• #1 [no priority label]: Test issue for Piper" in block


def test_the_heading_names_the_repository():
    out = _lines(_context([_issue(1, "Test issue for Piper", [])]))
    assert "- Open issues in pipermorgan/piper-test (1 open; top 1 shown" in out


def test_a_labelled_issue_shows_its_own_label_and_an_unlabelled_one_says_none():
    out = _lines(
        _context(
            [
                _issue(3, "Fix login", ["bug", "priority: critical"]),
                _issue(2, "Tidy docs", ["docs"]),
            ]
        )
    )
    assert "• #3 [priority: critical]: Fix login" in out
    assert "• #2 [no priority label]: Tidy docs" in out


def test_the_count_and_the_capped_plus_are_unchanged():
    out = _lines(
        _context(
            [_issue(1, "a", [])],
            open_issue_count=100,
            open_issue_count_capped=True,
        )
    )
    assert "(100+ open; top 1 shown" in out


@pytest.mark.parametrize(
    "issues",
    [
        [{"number": 1, "title": "a", "labels": []}],  # a row with no repository
        [
            _issue(1, "a", [], repository="o/one"),
            _issue(2, "b", [], repository="o/two"),
        ],  # two repositories
        [_issue(1, "a", []), {"number": 2, "title": "b", "labels": []}],  # one row unnamed
    ],
)
def test_no_repository_is_named_unless_every_row_names_the_same_one(issues):
    heading = open_issues_heading(issues, len(issues))
    assert heading.startswith(f"- Open issues ({len(issues)} open;")
    assert " in " not in heading.split("(")[0]


def test_an_empty_list_adds_no_block():
    out = _lines(_context([]))
    assert "Open issues" not in out


def test_the_not_configured_line_is_unchanged():
    out = _lines({"github_repo_unconfigured": True, "high_priority_issues": []})
    assert "GitHub repository: not configured for this user" in out
