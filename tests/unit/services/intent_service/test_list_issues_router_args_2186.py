"""#2186 — `_handle_list_issues_query` consumes the router's list qualifiers.

The router already emits ``milestone`` / ``label`` / ``state`` / ``repo`` and a
count (``count`` or ``limit``) in ``context["inversion_args"]`` (Lead's ×3
measurement, dev/2026/10/28/controls/2186-args-baseline-x3-main-args-2026-10-28.txt).
The handler checks each value with the #1976 honesty guard and passes it to the
search rail; the rail builds the query in code (ADR-080). A qualifier the read
can't apply is named in the reply, never dropped silently. Without router args
(the legacy path) the call and the reply are byte-identical to before.
"""

import importlib.util
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import (
    LIST_COUNT_CAP_LINE,
    LIST_REPO_UNRESOLVED_LINE,
    LIST_UNAPPLIED_LINE,
    LIST_UNAPPLIED_PART_LINE,
    IntentService,
)
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubIssuesResult
from services.shared_types import IntentCategory

_CONN = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues"
_NATIVE = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
_HITS = "services.intent.intent_service.IntentService._bare_repo_hits"


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent(message, args=None):
    context = {"original_message": message}
    if args is not None:
        context["inversion_args"] = args
    return Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        original_message=message,
        context=context,
    )


def _page(n):
    return [
        {"number": 100 + i, "title": f"Issue {i}", "labels": [{"name": "bug"}] if i == 0 else []}
        for i in range(n)
    ]


async def _run(svc, intent, issues=None, total=12):
    stub = AsyncMock(
        return_value=GitHubIssuesResult(issues=_page(5) if issues is None else issues, total=total)
    )
    with patch(_CONN, new=stub):
        res = await svc._handle_list_issues_query(intent, "wf")
    return stub, res


# (e) The legacy path: no inversion_args → the same call and the same reply as
# before #2186, byte for byte (captured from origin/main c26d199a5a's handler
# with this exact stub).
_TODAY_REPLY = (
    "You have **12 open issues** assigned to you across all your repositories.\n\nHere are the most recent:\n"
    "- **#100**: Issue 0 (bug)\n- **#101**: Issue 1\n- **#102**: Issue 2\n"
    "- **#103**: Issue 3\n- **#104**: Issue 4\n\n"
    "That's all 5 I have in front of me, out of 12."
)
_TODAY_REPO_REPLY = (
    "You have **12 open issues** in mediajunkie/piper-morgan-product.\n\n"
    "Here are the most recent:\n"
    "- **#100**: Issue 0 (bug)\n- **#101**: Issue 1\n- **#102**: Issue 2\n"
    "- **#103**: Issue 3\n- **#104**: Issue 4\n\n"
    "That's all 5 I have in front of me, out of 12."
)


@pytest.mark.asyncio
async def test_no_router_args_is_byte_identical(intent_service):
    stub, res = await _run(intent_service, _intent("show my open issues"))
    assert stub.await_args == call(None, limit=50, repository=None)
    assert res.message == _TODAY_REPLY
    assert "filters" not in res.intent_data["context"]


@pytest.mark.asyncio
async def test_no_router_args_regex_repo_still_works(intent_service):
    stub, res = await _run(
        intent_service, _intent("show open issues in mediajunkie/piper-morgan-product")
    )
    assert stub.await_args == call(None, limit=50, repository="mediajunkie/piper-morgan-product")
    assert res.message == _TODAY_REPO_REPLY


# (a) milestone
@pytest.mark.asyncio
async def test_milestone_reaches_the_rail_and_names_its_scope(intent_service):
    stub, res = await _run(
        intent_service,
        _intent("show my open issues in the MVP milestone", {"milestone": "MVP"}),
        total=3,
    )
    assert stub.await_args == call(None, limit=50, repository=None, milestone="MVP")
    assert res.message.startswith(
        'You have **3 open issues** assigned to you across all your repositories in milestone "MVP".'
    )
    assert res.intent_data["context"]["filters"] == {"milestone": "MVP"}


# (b) label
@pytest.mark.asyncio
async def test_label_reaches_the_rail_and_names_its_scope(intent_service):
    stub, res = await _run(
        intent_service,
        _intent("open bugs labeled needs-triage", {"label": "needs-triage", "state": "open"}),
        total=4,
    )
    assert stub.await_args == call(None, limit=50, repository=None, label="needs-triage")
    assert res.message.startswith(
        'You have **4 open issues** assigned to you across all your repositories labeled "needs-triage".'
    )
    assert "couldn't" not in res.message


# (c) state: closed
@pytest.mark.asyncio
async def test_closed_state_reads_closed_and_says_closed(intent_service):
    stub, res = await _run(
        intent_service, _intent("what closed issues do I have", {"state": "closed"}), total=9
    )
    assert stub.await_args == call(None, limit=50, repository=None, state="closed")
    assert res.message.startswith(
        "You have **9 closed issues** assigned to you across all your repositories."
    )


@pytest.mark.asyncio
async def test_filtered_empty_read_names_its_scope_and_skips_default_repo_count(
    intent_service,
):
    with patch.object(
        intent_service, "_default_repo_open_issue_count", new=AsyncMock()
    ) as repo_count:
        _stub, res = await _run(
            intent_service,
            _intent("show my open issues in the MVP milestone", {"milestone": "MVP"}),
            issues=[],
            total=0,
        )
    assert res.message == 'You have no open issues assigned to you in milestone "MVP".'
    repo_count.assert_not_awaited()


# (d) count, under either name
@pytest.mark.asyncio
@pytest.mark.parametrize("key", ["count", "limit"])
async def test_count_shows_the_newest_n_and_keeps_the_true_total(intent_service, key):
    stub, res = await _run(
        intent_service, _intent("show my last two new issues", {key: "2"}), total=12
    )
    assert stub.await_args == call(None, limit=50, repository=None)
    assert res.message.startswith(
        "You have **12 open issues** assigned to you across all your repositories."
    )  # total unchanged
    assert "#100" in res.message and "#101" in res.message
    assert "#102" not in res.message
    assert "That's the 2 you asked for, out of 12." in res.message
    assert "say the word" not in res.message  # no offer after a slice the user chose


@pytest.mark.asyncio
async def test_count_over_five_shows_that_many(intent_service):
    _stub, res = await _run(
        intent_service, _intent("show my last eight issues", {"count": 8}), issues=_page(10)
    )
    assert all(f"#{100 + i}" in res.message for i in range(8))
    assert "#108" not in res.message


# (f) the honesty guard
@pytest.mark.asyncio
async def test_value_the_user_did_not_say_is_ignored(intent_service):
    stub, res = await _run(
        intent_service,
        _intent("show my open issues in the MVP milestone", {"milestone": "Production"}),
    )
    assert stub.await_args == call(None, limit=50, repository=None)
    assert res.message == _TODAY_REPLY


# (g) an unhonourable qualifier is named, never dropped
@pytest.mark.asyncio
async def test_unhonourable_state_appends_the_fixed_line(intent_service):
    stub, res = await _run(
        intent_service,
        _intent("show all my issues in the MVP milestone", {"state": "all", "milestone": "MVP"}),
        total=3,
    )
    assert stub.await_args == call(None, limit=50, repository=None, milestone="MVP")
    line = LIST_UNAPPLIED_LINE.format(qualifiers='state "all"', pronoun="it")
    assert line in res.message
    # CXO: under the count header, above the list.
    assert res.message.index(line) < res.message.index("Here are the most recent:")
    assert 'in milestone "MVP"' in res.message  # the honourable one still applied
    assert res.intent_data["context"]["unhonoured_qualifiers"] == ['state "all"']


@pytest.mark.asyncio
async def test_count_over_the_cap_appends_the_fixed_line(intent_service):
    _stub, res = await _run(intent_service, _intent("show my last 80 issues", {"count": "80"}))
    # CXO 12:34: a cap, not a failed filter — its own sentence, and the first 50 shown.
    line = LIST_COUNT_CAP_LINE.format(cap=50)
    assert line in res.message
    assert "couldn't apply" not in res.message
    assert res.message.index(line) < res.message.index("Here are the most recent:")


@pytest.mark.asyncio
async def test_native_fallback_names_every_qualifier_it_cannot_apply(intent_service):
    degrade = GitHubIssuesResult(
        degradation=DegradationResponse(
            reason=DegradationReason.CONNECT_REQUIRED,
            user_message="Connect GitHub to continue.",
        )
    )
    native_router = MagicMock()
    native_router.initialize = AsyncMock()
    native_router.get_open_items_strict = AsyncMock(
        return_value=[{"number": 99, "title": "Native issue", "labels": []}]
    )
    native_router.last_open_window_full = False
    intent = _intent(
        "show my closed issues in the MVP milestone", {"milestone": "MVP", "state": "closed"}
    )
    with patch(_CONN, new=AsyncMock(return_value=degrade)):
        with patch(_NATIVE, return_value=native_router):
            res = await intent_service._handle_list_issues_query(intent, "wf")
    assert res.message.startswith(
        "You have **1 open issue**."
    )  # native read: no assignee term, so no scope phrase  # no false filter claim
    # One sentence for every unapplied qualifier, joined with "and" (CXO).
    assert (
        LIST_UNAPPLIED_LINE.format(qualifiers='milestone "MVP" and state "closed"', pronoun="them")
        in res.message
    )
    assert res.message.count("I couldn't apply") == 1


# (h) router repo vs the regex fallback
@pytest.mark.asyncio
async def test_router_repo_beats_the_regex(intent_service):
    stub, _res = await _run(
        intent_service,
        _intent(
            "show open issues in mediajunkie/piper-morgan-product, not acme/other",
            {"repo": "acme/other"},
        ),
    )
    assert stub.await_args == call(None, limit=50, repository="acme/other")


@pytest.mark.asyncio
async def test_bare_router_repo_without_a_user_is_named_not_dropped(intent_service):
    with patch(_HITS, new=AsyncMock(return_value=["mediajunkie/piper-morgan-product"])):
        stub, res = await _run(
            intent_service,
            _intent(
                "show open issues in piper-morgan-product",
                {"repo": "piper-morgan-product"},
            ),
        )
    # user_id None → no resolution attempted; the bare name is named, not dropped
    assert stub.await_args == call(None, limit=50, repository=None)
    assert LIST_REPO_UNRESOLVED_LINE.format(name="piper-morgan-product") in res.message
    assert "couldn't apply" not in res.message  # a name that didn't match is a different fact


@pytest.mark.asyncio
async def test_bare_router_repo_with_a_user_resolves(intent_service):
    uid = "11111111-1111-1111-1111-111111111111"
    with patch("services.intent.intent_service._principal_from_intent", return_value=uid):
        with patch(_HITS, new=AsyncMock(return_value=["mediajunkie/piper-morgan-product"])):
            stub, res = await _run(
                intent_service,
                _intent(
                    "show open issues in piper-morgan-product",
                    {"repo": "piper-morgan-product"},
                ),
            )
    assert stub.await_args == call(uid, limit=50, repository="mediajunkie/piper-morgan-product")
    assert "couldn't" not in res.message


@pytest.mark.asyncio
async def test_bare_router_repo_with_several_hits_is_named_not_guessed(intent_service):
    # The same lookup as #1944 (_bare_repo_hits). Two registered repos share the
    # bare name: the read must not pick one; the qualifier is named as unapplied.
    uid = "11111111-1111-1111-1111-111111111111"
    with patch("services.intent.intent_service._principal_from_intent", return_value=uid):
        with patch(
            _HITS,
            new=AsyncMock(
                return_value=["acme/piper-morgan-product", "mediajunkie/piper-morgan-product"]
            ),
        ):
            stub, res = await _run(
                intent_service,
                _intent(
                    "show open issues in piper-morgan-product",
                    {"repo": "piper-morgan-product"},
                ),
            )
    assert stub.await_args == call(uid, limit=50, repository=None)
    assert LIST_REPO_UNRESOLVED_LINE.format(name="piper-morgan-product") in res.message
    assert "couldn't apply" not in res.message  # a name that didn't match is a different fact


# ── corpus rows and the scorer (#2186 step 6) ──
_SCRIPTS = Path(__file__).resolve().parents[4] / "scripts"

_ROWS = {
    "show my last two new issues": {"count": "2"},
    "show my open issues in the MVP milestone": {"milestone": "MVP"},
    "open bugs labeled needs-triage": {"label": "needs-triage"},
    "what closed issues do I have": {"state": "closed"},
}


def test_corpus_carries_one_args_row_per_qualifier():
    sys.path.insert(0, str(_SCRIPTS))
    import inversion_phase0_baseline as p0

    rows = {r.get("phrase"): r for r in p0.load_corpus()}
    for phrase, args in _ROWS.items():
        assert rows[phrase]["expected"] == "action:list_issues_query"
        assert rows[phrase]["expected_args"] == args


def test_scorer_compares_list_qualifiers_and_count():
    path = _SCRIPTS / "inversion_phase1_shadow_score.py"
    sys.path.insert(0, str(_SCRIPTS))
    spec = importlib.util.spec_from_file_location("_score_2186", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.args_match({"milestone": "MVP"}, {"milestone": "mvp"})[0]
    assert not mod.args_match({"milestone": "MVP"}, {"milestone": "Production"})[0]
    assert mod.args_match({"label": "needs-triage"}, {"label": "needs-triage"})[0]
    assert mod.args_match({"state": "closed"}, {"state": "Closed"})[0]
    assert mod.args_match({"count": "2"}, {"count": 2, "sort": "created"})[0]
    assert mod.args_match({"count": "2"}, {"limit": "2"})[0]
    ok, note = mod.args_match({"count": "2"}, {"count": 3})
    assert not ok and note.startswith("count:")
    assert not mod.args_match({"count": "2"}, {})[0]


# ── CXO's rulings of 2026-10-28 11:21 (#2186): singulars, the joined sentence, the trailer ──


@pytest.mark.asyncio
async def test_singular_count_line_open_and_closed(intent_service):
    _, res = await _run(
        intent_service,
        _intent("show my open issues in the MVP milestone", {"milestone": "MVP"}),
        issues=_page(1),
        total=1,
    )
    assert (
        '**1 open issue** assigned to you across all your repositories in milestone "MVP".'
        in res.message
    )
    _, res = await _run(
        intent_service,
        _intent("what closed issues do I have", {"state": "closed"}),
        issues=_page(1),
        total=1,
    )
    assert "**1 closed issue**" in res.message


@pytest.mark.asyncio
async def test_empty_branch_puts_the_sentence_after_the_one_line_answer(intent_service):
    _, res = await _run(
        intent_service,
        _intent(
            "show my open issues in the MVP milestone with state all",
            {"milestone": "MVP", "state": "all"},
        ),
        issues=[],
        total=0,
    )
    assert res.message.startswith('You have no open issues assigned to you in milestone "MVP".')
    assert LIST_UNAPPLIED_LINE.format(qualifiers='state "all"', pronoun="it") in res.message


def test_compose_capped_list_count_aware_trailer_keeps_the_rest_cashable():
    from services.intent_service.list_remainder import compose_capped_list

    lines = [f"\n- item {i}" for i in range(10)]
    r = compose_capped_list(lines=lines, cap=2, asked_count=2, kind="open issues", source_total=14)
    assert r.body.endswith("That's the 2 you asked for, out of 14.")
    assert "item 1" in r.body and "item 2" not in r.body
    assert "say the word" not in r.body
    assert r.remainder is not None and len(r.remainder.lines) == 8  # "the rest" still cashes
    # Asked for more than is held: the ordinary logic (everything held is on screen).
    r2 = compose_capped_list(
        lines=lines[:3], cap=8, asked_count=8, kind="open issues", source_total=3
    )
    assert "you asked for" not in r2.body and r2.complete is not None


# ── #2186 Open 1 (Arch 12:29 10-28): an undeclared key is named, never dropped ──


@pytest.mark.asyncio
async def test_undeclared_key_is_named_alongside_the_applied_one(intent_service):
    stub, res = await _run(
        intent_service,
        _intent(
            "show my open issues in the MVP milestone from this week",
            {"milestone": "MVP", "timeframe": "this week", "sort": "created", "order": "desc"},
        ),
        total=3,
    )
    assert stub.await_args.kwargs.get("milestone") == "MVP"
    # CXO 12:34: the user's phrase, quoted; never the router's field name.
    line = LIST_UNAPPLIED_LINE.format(qualifiers='"this week"', pronoun="it")
    assert line in res.message  # the applied key is not named; sort/order are rail-satisfied
    assert res.message.index(line) < res.message.index("Here are the most recent:")
    assert "timeframe" not in res.message and "sort" not in res.message


@pytest.mark.asyncio
async def test_undeclared_key_value_the_user_did_not_say_names_the_key_only(intent_service):
    _, res = await _run(intent_service, _intent("show my open issues", {"priority": "P0"}), total=3)
    # Neither the field name nor an unsaid value is printed: the plain sentence.
    assert LIST_UNAPPLIED_PART_LINE in res.message
    assert "priority" not in res.message and "P0" not in res.message


@pytest.mark.asyncio
async def test_pr_list_names_every_router_key_it_was_given(intent_service):
    # "list my pull requests from this week" -> list_prs with timeframe="this week" (x3 on main, 10-28).
    page = [
        {"number": 7, "title": "Seven", "html_url": "https://github.com/o/r/pull/7", "labels": []},
        {"number": 6, "title": "Six", "html_url": "https://github.com/o/r/pull/6", "labels": []},
    ]
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_prs_query",
        context={
            "original_message": "list my pull requests from this week",
            "inversion_args": {"timeframe": "this week"},
        },
    )
    intent.bind_original_message("list my pull requests from this week")
    with patch(
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_prs",
        new=AsyncMock(return_value=GitHubIssuesResult(issues=page, total=2)),
    ):
        res = await intent_service._handle_list_prs_query(intent, "wf")
    line = LIST_UNAPPLIED_LINE.format(qualifiers='"this week"', pronoun="it")
    assert line in res.message
    assert "timeframe" not in res.message
    assert res.message.index(line) < res.message.index("Here are the most recent:")


@pytest.mark.asyncio
async def test_pr_list_treats_state_open_as_rail_satisfied(intent_service):
    # Arch 15:29 10-28: the PR rail reads open items; a router state "open" is satisfied, not unapplied.
    page = [
        {"number": 7, "title": "Seven", "html_url": "https://github.com/o/r/pull/7", "labels": []}
    ]
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_prs_query",
        context={
            "original_message": "list my open pull requests from this week",
            "inversion_args": {"state": "open", "timeframe": "this week"},
        },
    )
    intent.bind_original_message("list my open pull requests from this week")
    with patch(
        "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_prs",
        new=AsyncMock(return_value=GitHubIssuesResult(issues=page, total=1)),
    ):
        res = await intent_service._handle_list_prs_query(intent, "wf")
    assert LIST_UNAPPLIED_LINE.format(qualifiers='"this week"', pronoun="it") in res.message
    assert '"open"' not in res.message
