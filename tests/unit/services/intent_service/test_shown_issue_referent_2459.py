"""2459: an issue a read showed alone is the referent of a bare "it".

Served: a status reply named exactly one GitHub issue ("#1: Test issue for Piper")
and offered to pull up its details; the person took the offer and nothing was
fetched, because the one-issue read knew only the issue this session CREATED (2114).

Arch's rule (issue 2459): a code read that hands the person exactly one issue records
it as the session's last-shown issue (owner- and session-scoped, from the read's data,
outside the activity ledger). With no number in the words, the one-issue read takes
the NEWER of the created head and that slot; neither, or a newest read that showed
several, keeps the ask for a number. CXO's words for a failed read of the resolved
referent: ``I couldn't pull up that issue just now.``

The route ("pull up the full details on it" → review_issue_query) is a corpus row and
is not tested here; these tests call the handler the route reaches.
"""

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import shown_issue as shown_mod
from services.intent_service.context_assembler import ContextAssembler
from services.intent_service.conversation_context import ShownIssue, get_or_create_context
from services.intent_service.shown_issue import (
    REFERENT_READ_FAILED_LINE,
    CreatedIssueRef,
    choose_issue_referent,
    record_shown_issues,
)
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubIssuesResult
from services.shared_types import IntentCategory

LEDGER = "services.intent_service.session_activity_read.list_session_activities"
ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"
LIST_CONN = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues"

USER = "3f7b8a52-2459-4b00-9e00-000000002459"
OTHER_USER = "3f7b8a52-2459-4b00-9e00-00000000beef"
REPO = "pipermorgan/piper-test"

# Today's ask, byte for byte (the 2114 handler's no-number reply).
ASK = (
    "I couldn't find an issue number in your request. Please specify an issue number "
    "(e.g., 'show me issue #123')."
)

ISSUE_1 = {
    "number": 1,
    "title": "Test issue for Piper",
    "state": "open",
    "labels": [],
    "body": "",
    "html_url": f"https://github.com/{REPO}/issues/1",
}


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


@pytest.fixture
def sid():
    return f"s-2459-{uuid.uuid4()}"


@pytest.fixture
def quiet_gather(monkeypatch):
    """gather_context's own clock and first-contact reads are not what these pin."""
    import services.intent_service.context_assembler as ca
    from services.intent_service import first_contact

    monkeypatch.setattr(ca, "_current_time_and_date_for_user", AsyncMock(return_value=(None, None)))
    monkeypatch.setattr(first_contact, "is_first_exchange", lambda *a, **k: False)


def _review(message: str = "pull up the full details on it", user_id: str | None = USER):
    ctx = {"original_message": message}
    if user_id:
        ctx["user_id"] = user_id
    return Intent(category=IntentCategory.QUERY, action="review_issue_query", context=ctx)


def _list_intent(user_id: str = USER):
    return Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        context={"original_message": "show my open issues", "user_id": user_id},
    )


def _adapter_returning(item):
    adapter = MagicMock()
    adapter.get_issue_connector = AsyncMock(
        return_value=SimpleNamespace(item=item, degradation=None, resolved_repo=REPO)
    )
    return adapter


def _created_row(ref: str, at: datetime | None) -> SimpleNamespace:
    return SimpleNamespace(
        action_type="issue_created", target_ref=ref, target_title=None, created_at=at
    )


async def _status_turn(sid: str, rows: list, count: int | None = None, user_id: str = USER):
    gathered = {
        "high_priority_issues": rows,
        "open_issue_count": len(rows) if count is None else count,
    }

    async def _fake(self, user_id=None):
        return dict(gathered)

    with patch.object(ContextAssembler, "_gather_status_priority_context", _fake):
        return await ContextAssembler().gather_context(
            intent_category="STATUS", user_id=user_id, session_id=sid
        )


def _row(number: int, repository: str | None = REPO) -> dict:
    row = {"number": number, "title": f"Issue {number}", "labels": [], "url": None}
    if repository is not None:
        row["repository"] = repository
    return row


async def _read_it(
    service, sid, message="pull up the full details on it", ledger=None, user_id=USER
):
    adapter = _adapter_returning(ISSUE_1)
    with (
        patch(LEDGER, new=AsyncMock(return_value=ledger or [])),
        patch(ADAPTER, return_value=adapter),
    ):
        result = await service._handle_review_issue_query(
            _review(message, user_id=user_id), "wf", session_id=sid
        )
    return result, adapter


# ---------------------------------------------------------------------------
# The served scenario: one issue shown, then "it"
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestOneIssueShownIsTheReferent:
    async def test_one_issue_status_read_then_it_reads_that_issue(
        self, intent_service, sid, quiet_gather
    ):
        await _status_turn(sid, [_row(1)])
        result, adapter = await _read_it(intent_service, sid)
        adapter.get_issue_connector.assert_awaited_once_with(
            USER, issue_number=1, explicit_repo=REPO
        )
        assert result.success is True
        assert "Test issue for Piper" in result.message

    async def test_one_issue_listing_then_it_reads_that_issue(self, intent_service, sid):
        page = GitHubIssuesResult(
            issues=[{**ISSUE_1, "repository_url": f"https://api.github.com/repos/{REPO}"}],
            total=1,
        )
        with patch(LIST_CONN, new=AsyncMock(return_value=page)):
            listed = await intent_service._handle_list_issues_query(
                _list_intent(), "wf", session_id=sid
            )
        assert listed.success is True
        result, adapter = await _read_it(intent_service, sid)
        adapter.get_issue_connector.assert_awaited_once_with(
            USER, issue_number=1, explicit_repo=REPO
        )
        assert result.success is True

    async def test_a_status_row_without_a_repository_records_no_issue(
        self, intent_service, sid, quiet_gather
    ):
        """Main's gathered rows carry no repository yet: never guessed, so the ask."""
        await _status_turn(sid, [_row(1, repository=None)])
        result, adapter = await _read_it(intent_service, sid)
        assert result.message == ASK
        adapter.get_issue_connector.assert_not_awaited()


# ---------------------------------------------------------------------------
# Several shown, or nothing: the ask stands, byte for byte
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestTheAskStands:
    async def test_two_issue_status_read_then_it_asks_for_a_number(
        self, intent_service, sid, quiet_gather
    ):
        await _status_turn(sid, [_row(1), _row(2)])
        result, adapter = await _read_it(intent_service, sid)
        assert result.message == ASK
        assert result.requires_clarification is True
        adapter.get_issue_connector.assert_not_awaited()

    async def test_one_row_of_several_open_is_not_a_single(self, intent_service, sid, quiet_gather):
        await _status_turn(sid, [_row(1)], count=3)
        result, _ = await _read_it(intent_service, sid)
        assert result.message == ASK

    async def test_a_multi_issue_read_after_a_single_clears_the_single(
        self, intent_service, sid, quiet_gather
    ):
        await _status_turn(sid, [_row(1)])
        await _status_turn(sid, [_row(1), _row(2)])
        result, adapter = await _read_it(intent_service, sid)
        assert result.message == ASK
        adapter.get_issue_connector.assert_not_awaited()

    async def test_two_issue_listing_then_it_asks_for_a_number(self, intent_service, sid):
        page = GitHubIssuesResult(
            issues=[
                {**ISSUE_1, "repository_url": f"https://api.github.com/repos/{REPO}"},
                {**ISSUE_1, "number": 2, "repository_url": f"https://api.github.com/repos/{REPO}"},
            ],
            total=2,
        )
        with patch(LIST_CONN, new=AsyncMock(return_value=page)):
            await intent_service._handle_list_issues_query(_list_intent(), "wf", session_id=sid)
        result, _ = await _read_it(intent_service, sid)
        assert result.message == ASK

    async def test_a_failed_listing_after_a_single_clears_the_single(self, intent_service, sid):
        record_shown_issues(sid, USER, [(REPO, 1)])
        degraded = GitHubIssuesResult(
            degradation=DegradationResponse(
                reason=DegradationReason.UNREACHABLE,
                user_message="GitHub's MCP server is unreachable right now.",
            )
        )
        with patch(LIST_CONN, new=AsyncMock(return_value=degraded)):
            await intent_service._handle_list_issues_query(_list_intent(), "wf", session_id=sid)
        result, _ = await _read_it(intent_service, sid)
        assert result.message == ASK

    async def test_no_issue_at_all_keeps_todays_ask(self, intent_service, sid):
        result, adapter = await _read_it(intent_service, sid)
        assert result.success is False
        assert result.requires_clarification is True
        assert result.message == ASK
        adapter.get_issue_connector.assert_not_awaited()


# ---------------------------------------------------------------------------
# Newest wins between the created head (2114) and the shown slot
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestNewestWins:
    async def test_a_create_after_a_show_resolves_to_the_create(self, intent_service, sid):
        record_shown_issues(sid, USER, [(REPO, 1)])
        later = datetime.now(timezone.utc) + timedelta(seconds=5)
        ledger = [_created_row("acme/widgets#22", later)]
        _, adapter = await _read_it(intent_service, sid, ledger=ledger)
        adapter.get_issue_connector.assert_awaited_once_with(
            USER, issue_number=22, explicit_repo="acme/widgets"
        )

    async def test_a_show_after_a_create_resolves_to_the_show(self, intent_service, sid):
        earlier = datetime.now(timezone.utc) - timedelta(seconds=5)
        ledger = [_created_row("acme/widgets#22", earlier)]
        record_shown_issues(sid, USER, [(REPO, 1)])
        _, adapter = await _read_it(intent_service, sid, ledger=ledger)
        adapter.get_issue_connector.assert_awaited_once_with(
            USER, issue_number=1, explicit_repo=REPO
        )

    async def test_a_multi_read_after_a_create_asks(self, intent_service, sid):
        earlier = datetime.now(timezone.utc) - timedelta(seconds=5)
        ledger = [_created_row("acme/widgets#22", earlier)]
        record_shown_issues(sid, USER, [(REPO, 1), (REPO, 2)])
        result, adapter = await _read_it(intent_service, sid, ledger=ledger)
        assert result.message == ASK
        adapter.get_issue_connector.assert_not_awaited()

    async def test_a_create_after_a_multi_read_resolves_to_the_create(self, intent_service, sid):
        record_shown_issues(sid, USER, [(REPO, 1), (REPO, 2)])
        later = datetime.now(timezone.utc) + timedelta(seconds=5)
        ledger = [_created_row("acme/widgets#22", later)]
        _, adapter = await _read_it(intent_service, sid, ledger=ledger)
        assert adapter.get_issue_connector.await_args.kwargs["issue_number"] == 22

    async def test_a_number_in_the_words_wins_over_both(self, intent_service, sid):
        record_shown_issues(sid, USER, [(REPO, 1)])
        ledger = AsyncMock(return_value=[_created_row("acme/widgets#22", None)])
        adapter = _adapter_returning({**ISSUE_1, "number": 7, "title": "Seven"})
        with patch(LEDGER, new=ledger), patch(ADAPTER, return_value=adapter):
            await intent_service._handle_review_issue_query(
                _review("show me issue #7"), "wf", session_id=sid
            )
        ledger.assert_not_awaited()
        adapter.get_issue_connector.assert_awaited_once_with(
            USER, issue_number=7, explicit_repo=None
        )


class TestChooseIssueReferent:
    """The pure rule, including the cases code cannot order (never a guess)."""

    NOW = datetime(2026, 11, 27, 16, 0, tzinfo=timezone.utc)

    def test_neither(self):
        assert choose_issue_referent(None, None) is None

    def test_created_only(self):
        assert choose_issue_referent(CreatedIssueRef("o/r", 3, None), None) == ("o/r", 3)

    def test_shown_only(self):
        assert choose_issue_referent(None, ShownIssue("o/r", 4, self.NOW)) == ("o/r", 4)

    def test_not_single_only(self):
        assert choose_issue_referent(None, ShownIssue(None, None, self.NOW)) is None

    def test_unorderable_pair_is_not_guessed(self):
        shown = ShownIssue("o/r", 4, self.NOW)
        assert choose_issue_referent(CreatedIssueRef("o/r", 3, None), shown) is None
        assert choose_issue_referent(CreatedIssueRef("o/r", 3, self.NOW), shown) is None

    def test_naive_ledger_time_is_read_as_utc(self):
        shown = ShownIssue("o/r", 4, self.NOW)
        naive_later = (self.NOW + timedelta(seconds=1)).replace(tzinfo=None)
        assert choose_issue_referent(CreatedIssueRef("o/r", 3, naive_later), shown) == ("o/r", 3)


# ---------------------------------------------------------------------------
# Scope: owner and session
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestScope:
    async def test_another_user_does_not_see_the_shown_issue(self, intent_service, sid):
        record_shown_issues(sid, USER, [(REPO, 1)])
        result, adapter = await _read_it(intent_service, sid, user_id=OTHER_USER)
        assert result.message == ASK
        adapter.get_issue_connector.assert_not_awaited()

    async def test_another_session_does_not_see_the_shown_issue(self, intent_service, sid):
        record_shown_issues(sid, USER, [(REPO, 1)])
        result, adapter = await _read_it(intent_service, f"{sid}-other")
        assert result.message == ASK
        adapter.get_issue_connector.assert_not_awaited()

    async def test_no_principal_records_nothing(self, sid):
        record_shown_issues(sid, None, [(REPO, 1)])
        assert get_or_create_context(sid, user_id=None).last_shown_issue is None

    async def test_the_slot_is_not_written_to_the_activity_ledger(
        self, intent_service, sid, quiet_gather
    ):
        """Showing an issue is not something done: no ledger write on either read."""
        with patch(
            "services.database.repositories.SessionActivityRepository.record",
            create=True,
            new=AsyncMock(),
        ) as ledger_write:
            await _status_turn(sid, [_row(1)])
        ledger_write.assert_not_awaited()
        assert get_or_create_context(sid, user_id=USER).last_shown_issue.single is True


# ---------------------------------------------------------------------------
# Best-effort: a failed slot write never blocks or changes the reply
# ---------------------------------------------------------------------------


def _break_the_slot(monkeypatch):
    """Make only the slot write raise (the record is built inside the write's try)."""

    def _boom(*a, **k):
        raise RuntimeError("slot store down")

    monkeypatch.setattr("services.intent_service.conversation_context.ShownIssue", _boom)


@pytest.mark.asyncio
class TestFailedSlotWrite:
    async def test_a_failed_slot_write_never_blocks_the_listing_reply(
        self, intent_service, sid, monkeypatch
    ):
        page = GitHubIssuesResult(issues=[dict(ISSUE_1)], total=1)
        with patch(LIST_CONN, new=AsyncMock(return_value=page)):
            baseline = await intent_service._handle_list_issues_query(
                _list_intent(), "wf", session_id=f"{sid}-base"
            )
        _break_the_slot(monkeypatch)
        with patch(LIST_CONN, new=AsyncMock(return_value=page)):
            result = await intent_service._handle_list_issues_query(
                _list_intent(), "wf", session_id=sid
            )
        assert result.success is True
        assert result.message == baseline.message
        assert get_or_create_context(sid, user_id=USER).last_shown_issue is None

    async def test_a_failed_slot_write_never_blocks_the_status_gather(
        self, sid, quiet_gather, monkeypatch
    ):
        _break_the_slot(monkeypatch)
        ctx = await _status_turn(sid, [_row(1)])
        assert ctx["high_priority_issues"][0]["number"] == 1
        assert ctx["open_issue_count"] == 1

    async def test_a_failed_slot_read_is_nothing_shown(self, sid, monkeypatch):
        record_shown_issues(sid, USER, [(REPO, 1)])

        def _boom(*a, **k):
            raise RuntimeError("context store down")

        monkeypatch.setattr(
            "services.intent_service.conversation_context.get_or_create_context", _boom
        )
        assert shown_mod.last_shown_issue(sid, USER) is None


# ---------------------------------------------------------------------------
# CXO's words: a failed read of the resolved referent
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestFailedReadOfTheReferent:
    async def test_unreachable_read_of_the_shown_issue_says_the_constant(self, intent_service, sid):
        record_shown_issues(sid, USER, [(REPO, 1)])
        adapter = MagicMock()
        adapter.get_issue_connector = AsyncMock(
            return_value=SimpleNamespace(
                item=None,
                resolved_repo=REPO,
                degradation=DegradationResponse(
                    reason=DegradationReason.UNREACHABLE,
                    user_message="GitHub's MCP server is unreachable right now.",
                ),
            )
        )
        with patch(LEDGER, new=AsyncMock(return_value=[])), patch(ADAPTER, return_value=adapter):
            result = await intent_service._handle_review_issue_query(
                _review(), "wf", session_id=sid
            )
        assert result.success is False
        assert (
            result.message == REFERENT_READ_FAILED_LINE == "I couldn't pull up that issue just now."
        )

    async def test_a_raised_read_of_the_shown_issue_says_the_constant(self, intent_service, sid):
        record_shown_issues(sid, USER, [(REPO, 1)])
        adapter = MagicMock()
        adapter.get_issue_connector = AsyncMock(side_effect=RuntimeError("socket closed"))
        with patch(LEDGER, new=AsyncMock(return_value=[])), patch(ADAPTER, return_value=adapter):
            result = await intent_service._handle_review_issue_query(
                _review(), "wf", session_id=sid
            )
        assert result.success is False
        assert result.message == REFERENT_READ_FAILED_LINE

    async def test_an_explicit_number_keeps_the_connector_line(self, intent_service, sid):
        """Only a session-resolved referent takes the constant; a number in the words
        keeps today's degrade line."""
        adapter = MagicMock()
        adapter.get_issue_connector = AsyncMock(
            return_value=SimpleNamespace(
                item=None,
                resolved_repo=REPO,
                degradation=DegradationResponse(
                    reason=DegradationReason.UNREACHABLE,
                    user_message="GitHub's MCP server is unreachable right now.",
                ),
            )
        )
        with patch(ADAPTER, return_value=adapter):
            result = await intent_service._handle_review_issue_query(
                _review("show me issue #1"), "wf", session_id=sid
            )
        assert result.message == "GitHub's MCP server is unreachable right now."
