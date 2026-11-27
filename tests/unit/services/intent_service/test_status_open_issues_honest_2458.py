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
from uuid import uuid4

import pytest

from services.integrations.github.priority_labels import (
    HIGH_PRIORITY_LABELS,
    is_high_priority,
    priority_rank,
)
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


# --- the one rule ---------------------------------------------------------------


def test_the_label_set_is_ppms_union_of_nine():
    assert set(HIGH_PRIORITY_LABELS) == {
        "p0",
        "p1",
        "priority-high",
        "high-priority",
        "priority: high",
        "urgent",
        "priority: urgent",
        "critical",
        "priority: critical",
    }
    assert len(HIGH_PRIORITY_LABELS) == 9


@pytest.mark.parametrize("label", HIGH_PRIORITY_LABELS)
def test_each_label_in_the_set_counts_whatever_its_case_or_shape(label):
    assert is_high_priority([label])
    assert is_high_priority([label.upper()])
    assert is_high_priority([{"name": label}])  # the dict shape some reads return


@pytest.mark.parametrize(
    "labels",
    [
        [],
        None,
        ["bug", "docs"],
        ["priority: low"],
        ["p10"],  # no substrings
        ["not-urgent"],
        ["high"],
        ["priority"],
        [{"name": "enhancement"}],
        [None, 3],
    ],
)
def test_no_label_or_a_near_miss_is_not_high_priority(labels):
    assert not is_high_priority(labels)


def test_rank_is_critical_then_urgent_then_high_then_unlabelled():
    assert (
        priority_rank(["p0"])
        < priority_rank(["urgent"])
        < priority_rank(["high-priority"])
        < priority_rank(["bug"])
    )
    assert priority_rank(["bug"]) == priority_rank([]) == len(HIGH_PRIORITY_LABELS)


#: Files under services/ and web/ that spell a priority label and are NOT readers of
#: the one rule. Arch 2026-11-27: named, keyed by file, each with its reason and the
#: condition that clears it. The test fails if a new file appears, and fails if an
#: exception stops matching (so a stale entry cannot sit here; the 2420 shape).
_OWN_LABEL_LITERAL_EXCEPTIONS = {
    "services/integrations/spatial/github_spatial.py": (
        "sets an internal attention level; never said to a person; spatial is "
        "protected. Clears: joins the one rule if it ever renders a priority word."
    ),
    "services/domain/work_item_extractor.py": (
        "WRITES the label priority-high onto an extracted work item; it decides "
        "nothing about a GitHub issue, and has no caller. Clears: joins the one rule "
        "if it ever reads a label to decide priority."
    ),
}
_THE_ONE_RULE = "services/integrations/github/priority_labels.py"


def test_every_path_that_says_high_priority_reads_the_one_rule():
    """Arch's condition 1. The priority read, the project scoring, the status gather
    and the floor's rows call the predicate, and no file under services/ or web/
    spells a priority label of its own except the rule and the named exceptions."""
    import re
    from pathlib import Path

    handlers = Path("services/intent_service/canonical_handlers.py").read_text()
    assembler = Path("services/intent_service/context_assembler.py").read_text()
    floor = Path("services/intent_service/conversational_floor.py").read_text()
    assert handlers.count('is_high_priority(issue.get("labels", []))') == 2
    assert 'priority_rank(issue.get("labels"))' in assembler
    assert 'is_high_priority(it.get("labels"))' in floor

    literal = re.compile(
        r"""["'](p0|p1|priority-high|high-priority|priority: (high|urgent|critical))["']""",
        re.IGNORECASE,
    )
    spelling = set()
    for root in ("services", "web"):
        for path in Path(root).rglob("*.py"):
            if "/tests/" in str(path) or path.name.startswith("test_"):
                continue
            if literal.search(path.read_text(errors="ignore")):
                spelling.add(str(path))
    assert _THE_ONE_RULE in spelling
    assert spelling - {_THE_ONE_RULE} == set(_OWN_LABEL_LITERAL_EXCEPTIONS), (
        "a file spells its own priority label, or a named exception no longer does: "
        f"{sorted(spelling - {_THE_ONE_RULE})}"
    )


@pytest.mark.asyncio
async def test_the_priority_read_filters_by_the_one_rule():
    """The count line's number (``urgent_items``) comes from this list's length."""
    from services.intent_service.canonical_handlers import CanonicalHandlers

    issues = [
        {"number": 1, "title": "a", "labels": ["priority: urgent"]},  # was not in the six
        {"number": 2, "title": "b", "labels": ["P1"]},
        {"number": 3, "title": "c", "labels": ["bug"]},
        {"number": 4, "title": "d", "labels": []},
    ]
    handlers = CanonicalHandlers.__new__(CanonicalHandlers)
    service = MagicMock()
    service.get_connection_status = MagicMock(return_value={"connected": True})
    service.get_open_issues = AsyncMock(return_value=issues)
    status = MagicMock()
    status.is_configured = AsyncMock(return_value=True)
    with (
        patch(
            "services.integrations.integration_status_service.IntegrationStatusService",
            return_value=status,
        ),
        patch("services.domain.github_domain_service.GitHubDomainService", return_value=service),
        patch(
            "services.integrations.github.repo_resolver.get_user_default_repo",
            new=AsyncMock(return_value="o/r"),
        ),
    ):
        got = await handlers._get_priority_metadata(user_id=str(uuid4()))
    assert [i["number"] for i in got["high_priority_issues"]] == [1, 2]
    assert got["total_open_issues"] == 4


# --- what the floor is told ----------------------------------------------------


def _context(issues, **extra):
    return {"high_priority_issues": issues, "open_issue_count": len(issues), **extra}


def _issue(number, title, labels, repository="pipermorgan/piper-test"):
    return {"number": number, "title": title, "labels": labels, "repository": repository}


def test_the_beta_case_one_unlabelled_issue_carries_no_priority_word():
    """The served turn: one open issue, no priority label. The only "high priority"
    in the block is the heading's own sentence saying when the mark applies."""
    out = _lines(_context([_issue(1, "Test issue for Piper", [])]))
    assert "High-priority open issues" not in out
    row = next(line for line in out.split("\n") if "#1" in line)
    assert row.strip() == "• #1: Test issue for Piper"
    assert "priority" not in row.lower()


def test_the_heading_is_cxos_words_and_names_the_repository_as_github_does():
    out = _lines(_context([_issue(1, "Test issue for Piper", [])]))
    assert (
        "- Open issues in pipermorgan/piper-test (1 open; top 1 shown), "
        "priority-labelled first, then newest. "
        'Marked "high priority" only where the issue carries a priority label.'
    ) in out


def test_a_labelled_issue_is_marked_with_the_one_phrase_never_its_raw_label():
    out = _lines(
        _context(
            [
                _issue(3, "Fix login", ["bug", "priority: critical"]),
                _issue(5, "Ship it", ["P1"]),
                _issue(2, "Tidy docs", ["docs"]),
            ]
        )
    )
    assert "• #3 [high priority]: Fix login" in out
    assert "• #5 [high priority]: Ship it" in out
    assert "• #2: Tidy docs" in out
    assert "priority: critical" not in out
    assert "[P1]" not in out


def test_the_count_line_is_cxos_words():
    out = _lines({"priorities": {"urgent_items": 2}})
    assert "- Open issues marked high priority: 2" in out
    assert "- High-priority issues:" not in out


def test_an_old_cached_entry_with_no_repository_names_none():
    """Arch's condition 2: the cache key lives five minutes, and an entry written
    before this change has rows with no ``repository``. It renders under the new
    heading without a repository, never as if one were known."""
    old_shape = [
        {"number": 1, "title": "Test issue for Piper", "labels": [], "url": "u", "updated_at": "d"}
    ]
    out = _lines(_context(old_shape))
    assert "- Open issues (1 open; top 1 shown), priority-labelled first" in out
    assert "Open issues in " not in out


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


def test_an_empty_list_adds_no_block():
    out = _lines(_context([]))
    assert "Open issues" not in out


def test_the_not_configured_line_is_unchanged():
    out = _lines({"github_repo_unconfigured": True, "high_priority_issues": []})
    assert "GitHub repository: not configured for this user" in out


def test_the_provenance_of_the_count_says_the_rule_it_is_counted_by():
    """Arch 2026-11-27: evidence events described ``urgent_items`` as filtered by
    "priority:high", which is not a label in the set."""
    import inspect

    from services.intent_service import context_assembler

    source = inspect.getsource(context_assembler)
    assert '"filter": "state:open, label in HIGH_PRIORITY_LABELS"' in source
    assert "priority:high" not in source.replace('say "priority:high"', "")
