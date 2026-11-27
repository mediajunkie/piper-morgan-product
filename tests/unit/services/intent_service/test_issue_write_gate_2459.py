"""2459 part 2: one gate in front of every GitHub issue write that takes a number.

Arch's rule: a number typed in this message is accepted as today; otherwise only the
session's created head (owner- and session-scoped), when it is the session's
referent, with the same repository. Anything else gets the existing ask for a number
(CXO's named ask when the only candidate referent is a single SHOWN issue), and
nothing is armed, recorded or sent. The gate reads the words and the ledger in code;
it never trusts router args.

Writes gated: update_issue (handler + its #2304 write ask), close_issue and
reopen_issue (handlers + the #1959 confirm builder), comment_issue (handler).
"""

import uuid
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.issue_write_gate import (
    CLOSE_ISSUE_NUMBER_ASK,
    COMMENT_ISSUE_NUMBER_ASK,
    REOPEN_ISSUE_NUMBER_ASK,
    UPDATE_ISSUE_NUMBER_ASK,
    gate_issue_write,
    issue_number_arg,
    typed_issue_candidates,
    typed_issue_number,
)
from services.intent_service.shown_issue import (
    LEDGER_UNREADABLE,
    SHOWN_ISSUE_WHICH_ASK,
    record_shown_issues,
)
from services.shared_types import IntentCategory

LEDGER = "services.intent_service.session_activity_read.list_session_activities"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
EXTRACT = "services.slot_filling.slot_extractor.extract_slots"

USER = "3f7b8a52-2459-4b00-9e00-0000000a2459"
SHOWN_REPO = "pipermorgan/piper-test"
HEAD_REPO = "acme/widgets"

# The asks as they are on main, typed out here so a drift in the constants shows.
MAIN_UPDATE_ASK = (
    "I couldn't find an issue number in your request. Please specify an issue number "
    "(e.g., 'update issue #123')."
)
MAIN_COMMENT_ASK = (
    "I couldn't find an issue number in your request. Please specify an issue number "
    "(e.g., 'comment on issue #123 saying...')."
)
MAIN_CLOSE_ASK = (
    'I can close a particular issue if you give me its number, like "close #123". '
    "I don't search for finished issues or close them in bulk yet."
)
MAIN_REOPEN_ASK = (
    'I can reopen a particular issue if you give me its number, like "reopen #123". '
    "I don't search for closed issues or reopen them in bulk yet."
)
NAMED_1 = 'I just showed #1 in pipermorgan/piper-test. If that\'s the one you mean, say "#1".'


def test_the_constants_are_mains_words():
    assert UPDATE_ISSUE_NUMBER_ASK == MAIN_UPDATE_ASK
    assert COMMENT_ISSUE_NUMBER_ASK == MAIN_COMMENT_ASK
    assert CLOSE_ISSUE_NUMBER_ASK == MAIN_CLOSE_ASK
    assert REOPEN_ISSUE_NUMBER_ASK == MAIN_REOPEN_ASK
    assert SHOWN_ISSUE_WHICH_ASK.format(number=1, repository=SHOWN_REPO) == NAMED_1


# ---------------------------------------------------------------------------
# Fixtures and helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def svc():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            service = IntentService()
    service.llm_client = MagicMock()
    return service


@pytest.fixture
def sid():
    return f"s-2459-gate-{uuid.uuid4()}"


def _now():
    return datetime.now(timezone.utc)


def _row(number: int, at: datetime, repo: str = HEAD_REPO):
    return SimpleNamespace(
        action_type="issue_created", target_ref=f"{repo}#{number}", target_title=None, created_at=at
    )


def _intent(action: str, message: str, **ctx) -> Intent:
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        original_message=message,
        confidence=0.9,
        context={"original_message": message, "user_id": USER, **ctx},
    )


def _router():
    router = MagicMock()
    router.initialize = AsyncMock()
    router.is_available = AsyncMock(return_value=True)
    router.config_service.is_configured.return_value = True
    router.update_issue = AsyncMock(
        return_value={"number": 22, "title": "T", "state": "open", "html_url": "u"}
    )
    router.add_comment = AsyncMock(return_value={"html_url": "https://github.com/o/r/issues/1#c"})
    router.get_issue = AsyncMock(return_value={"number": 1, "title": "T", "state": "open"})
    return router


def _shown_only(sid):
    record_shown_issues(sid, USER, [(SHOWN_REPO, 1)])
    return []


def _created_then_shown(sid):
    rows = [_row(22, _now() - timedelta(seconds=5))]
    record_shown_issues(sid, USER, [(SHOWN_REPO, 1)])
    return rows


def _shown_then_created(sid):
    record_shown_issues(sid, USER, [(SHOWN_REPO, 1)])
    return [_row(22, _now() + timedelta(seconds=5))]


async def _run(svc, sid, action, intent, rows, extracted=None):
    """One handler turn; returns (result, router). The ledger read is the rows."""
    router = _router()
    handler = {
        "update_issue": lambda: svc._handle_update_issue(
            intent, "wf", session_id=sid, user_id=USER
        ),
        "close_issue": lambda: svc._handle_close_issue_query(intent, "wf", session_id=sid),
        "reopen_issue": lambda: svc._handle_reopen_issue_query(intent, "wf", session_id=sid),
        "comment_issue": lambda: svc._handle_comment_issue_query(intent, "wf", session_id=sid),
    }[action]
    with (
        patch(LEDGER, new=AsyncMock(return_value=rows)),
        patch(ROUTER, return_value=router),
        patch(EXTRACT, new=AsyncMock(return_value=extracted or {})),
    ):
        result = await handler()
    return result, router


def _assert_nothing_done(svc, sid, router, result):
    router.update_issue.assert_not_awaited()
    router.add_comment.assert_not_awaited()
    assert svc.workflow_offer_service._pending_offers.get(sid) is None
    data = result.intent_data or {}
    assert not data.get("retitled_activity")
    assert not data.get("created_activity")
    assert result.success is False
    assert result.requires_clarification is True


# The "it" turn for each write, shaped as each write's own sources would carry a
# session referent: update's context number (B3's shape, or a router arg copied in),
# close/reopen (words only, so nothing), comment (the extractor's reading).
def _it_turn(action: str, number=None):
    if action == "update_issue":
        ctx = {"title": "Test issue two"}
        if number is not None:
            ctx.update(issue_number=number, repository=HEAD_REPO if number == 22 else SHOWN_REPO)
        return _intent(action, "rename it to Test issue two", **ctx), None
    if action == "close_issue":
        return _intent(action, "close it"), None
    if action == "reopen_issue":
        return _intent(action, "reopen it"), None
    extracted = {"issue_number": None if number is None else str(number), "comment_text": "ok"}
    return _intent(action, "comment on it saying ok"), extracted


WRITES = ["update_issue", "close_issue", "reopen_issue", "comment_issue"]
PLAIN = {
    "update_issue": MAIN_UPDATE_ASK,
    "close_issue": MAIN_CLOSE_ASK,
    "reopen_issue": MAIN_REOPEN_ASK,
    "comment_issue": MAIN_COMMENT_ASK,
}


# ---------------------------------------------------------------------------
# The normaliser and the typed check
# ---------------------------------------------------------------------------


class TestNormaliser:
    @pytest.mark.parametrize(
        "mapping, expected",
        [
            ({"issue_number": 1}, 1),
            ({"issue": 1}, 1),
            ({"issue": "#7"}, 7),
            ({"issue_number": "12"}, 12),
            ({"issue_number": "one"}, None),
            ({"issue": 1.5}, None),
            ({"issue_number": True}, None),
            ({"issue_number": 0}, None),
            ({}, None),
            (None, None),
        ],
    )
    def test_both_keys_map_to_one_int(self, mapping, expected):
        assert issue_number_arg(mapping) == expected

    def test_typed_reads_the_2460_forms(self):
        assert typed_issue_candidates("set title to v2 on issue #108", True) == {108}
        assert typed_issue_candidates("set title to v2 on issue #108", False) == {2, 108}
        assert typed_issue_candidates("rename it to Test issue two", True) == set()

    async def test_a_non_integer_key_gets_the_plain_ask_even_with_a_shown_issue(self, svc, sid):
        _shown_only(sid)
        intent = _intent("update_issue", "rename it to X", title="X", issue="one")
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_the_handler_reads_the_issue_key_too(self, svc, sid):
        """A created-head number under ``issue`` binds like ``issue_number``."""
        intent = _intent(
            "update_issue", "rename it to X", title="X", issue="22", repository=HEAD_REPO
        )
        result, router = await _run(svc, sid, "update_issue", intent, [_row(22, _now())])
        assert router.update_issue.await_args.kwargs["issue_number"] == 22


# ---------------------------------------------------------------------------
# Rule 5, for each write
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("action", WRITES)
class TestEachWrite:
    async def test_no_referent_keeps_mains_ask_byte_for_byte(self, svc, sid, action):
        intent, extracted = _it_turn(action)
        result, router = await _run(svc, sid, action, intent, [], extracted)
        assert result.message == PLAIN[action]
        _assert_nothing_done(svc, sid, router, result)

    async def test_shown_issue_only_gets_the_named_ask_and_nothing_armed(self, svc, sid, action):
        rows = _shown_only(sid)
        intent, extracted = _it_turn(action, number=1)
        result, router = await _run(svc, sid, action, intent, rows, extracted)
        assert result.message == NAMED_1
        _assert_nothing_done(svc, sid, router, result)

    async def test_created_then_shown_gets_the_named_ask(self, svc, sid, action):
        rows = _created_then_shown(sid)
        intent, extracted = _it_turn(action, number=22)
        result, router = await _run(svc, sid, action, intent, rows, extracted)
        assert result.message == NAMED_1
        _assert_nothing_done(svc, sid, router, result)

    async def test_typed_number_binds_it(self, svc, sid, action):
        rows = _created_then_shown(sid)
        if action == "update_issue":
            intent = _intent(
                action, "change the title of #1 to X", title="X", repository=SHOWN_REPO
            )
            extracted = None
        elif action == "comment_issue":
            intent = _intent(action, f"comment on #1 in {SHOWN_REPO} saying ok")
            extracted = {"issue_number": "#1", "comment_text": "ok"}
        else:
            verb = "close" if action == "close_issue" else "reopen"
            intent = _intent(action, f"yes, {verb} #1 in {SHOWN_REPO}")
            extracted = None
        result, router = await _run(svc, sid, action, intent, rows, extracted)
        if action == "comment_issue":
            assert router.add_comment.await_args.args[0] == 1
        else:
            kw = router.update_issue.await_args.kwargs
            args = router.update_issue.await_args.args
            assert kw.get("issue_number", args[0] if args else None) == 1


class TestShownThenCreated:
    async def test_update_binds_the_created_issue(self, svc, sid):
        rows = _shown_then_created(sid)
        intent, _ = _it_turn("update_issue", number=22)
        result, router = await _run(svc, sid, "update_issue", intent, rows)
        kw = router.update_issue.await_args.kwargs
        assert (kw["issue_number"], kw["owner"], kw["repo_name"]) == (22, "acme", "widgets")
        assert result.success is True

    async def test_comment_binds_the_created_issue_in_its_repository(self, svc, sid):
        rows = _shown_then_created(sid)
        intent, extracted = _it_turn("comment_issue", number=22)
        _, router = await _run(svc, sid, "comment_issue", intent, rows, extracted)
        assert router.add_comment.await_args.args[0] == 22
        assert router.add_comment.await_args.kwargs.get("owner") == "acme"

    @pytest.mark.parametrize("action", ["close_issue", "reopen_issue"])
    async def test_close_and_reopen_have_no_session_referent_source(self, svc, sid, action):
        """Pinned as on main: close/reopen take a number only from the words, so
        "close it" after a create still gets the plain ask (no source to bind; this
        is reported, not built)."""
        rows = _shown_then_created(sid)
        intent, _ = _it_turn(action)
        result, router = await _run(svc, sid, action, intent, rows)
        assert result.message == PLAIN[action]
        _assert_nothing_done(svc, sid, router, result)


# ---------------------------------------------------------------------------
# The named ask: from the slot's data, binds nothing, a typed "#1" then proceeds
# ---------------------------------------------------------------------------


class TestNamedAsk:
    async def test_names_the_slot_not_the_router_args(self, svc, sid):
        record_shown_issues(sid, USER, [("other/place", 9)])
        intent = _intent(
            "update_issue",
            "rename it to X",
            title="X",
            inversion_args={"issue_number": 1, "repo": SHOWN_REPO},
        )
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message == SHOWN_ISSUE_WHICH_ASK.format(number=9, repository="other/place")
        _assert_nothing_done(svc, sid, router, result)
        # The named ask's issue comes from the slot, never the args.
        verdict = await gate_issue_write(
            intent,
            None,
            has_free_text_field=True,
            repository=None,
            user_id=USER,
            session_id=sid,
            created_head=AsyncMock(return_value=None),
        )
        assert verdict.accepted is False and verdict.shown == ("other/place", 9)

    @pytest.mark.parametrize("arrange", ["shown_only", "created_then_shown"])
    async def test_the_verdict_names_the_shown_issue_for_the_named_ask(self, sid, arrange):
        rows = _shown_only(sid) if arrange == "shown_only" else _created_then_shown(sid)
        head = None
        if rows:
            head = SimpleNamespace(
                repository=HEAD_REPO, number=22, created_at=rows[0].created_at, unreadable=False
            )
        number = 1 if arrange == "shown_only" else 22
        verdict = await gate_issue_write(
            _intent("update_issue", "rename it"),
            number,
            has_free_text_field=True,
            repository=None,
            user_id=USER,
            session_id=sid,
            created_head=AsyncMock(return_value=head),
        )
        assert verdict.accepted is False and verdict.shown == (SHOWN_REPO, 1)

    async def test_no_shown_issue_names_nothing(self, sid):
        verdict = await gate_issue_write(
            _intent("update_issue", "rename it"),
            None,
            has_free_text_field=True,
            repository=None,
            user_id=USER,
            session_id=sid,
            created_head=AsyncMock(return_value=None),
        )
        assert verdict.shown is None

    async def test_flags_match_the_plain_ask(self, svc, sid):
        plain, _ = await _run(svc, sid, "update_issue", _it_turn("update_issue")[0], [])
        _shown_only(sid)
        named, _ = await _run(svc, sid, "update_issue", _it_turn("update_issue")[0], [])
        assert (named.success, named.requires_clarification, named.clarification_type) == (
            plain.success,
            plain.requires_clarification,
            plain.clarification_type,
        )
        assert named.intent_data == plain.intent_data

    async def test_a_typed_hash_one_after_the_named_ask_proceeds_as_today(self, svc, sid):
        _shown_only(sid)
        named, _ = await _run(svc, sid, "update_issue", _it_turn("update_issue")[0], [])
        assert named.message == NAMED_1
        # The handler's normal typed form, and a bare "#1" (no field: today's line).
        typed = _intent(
            "update_issue", "change the title of #1 to X", title="X", repository=SHOWN_REPO
        )
        _, router = await _run(svc, sid, "update_issue", typed, [])
        assert router.update_issue.await_args.kwargs["issue_number"] == 1
        bare, router = await _run(
            svc, sid, "update_issue", _intent("update_issue", "#1", repository=SHOWN_REPO), []
        )
        assert bare.message.startswith("Tell me what to change on #1")
        router.update_issue.assert_not_awaited()


# ---------------------------------------------------------------------------
# Refusals that keep the plain ask; a failed ledger read is never a pass
# ---------------------------------------------------------------------------


class TestPlainRefusals:
    async def test_repository_mismatch_is_refused_with_the_plain_ask(self, svc, sid):
        intent = _intent(
            "update_issue", "rename it to X", title="X", issue_number=22, repository="other/repo"
        )
        result, router = await _run(svc, sid, "update_issue", intent, [_row(22, _now())])
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_a_failed_ledger_read_refuses_the_created_head(self, svc, sid):
        intent, _ = _it_turn("update_issue", number=22)
        router = _router()
        with (
            patch(LEDGER, new=AsyncMock(side_effect=RuntimeError("db down"))),
            patch(ROUTER, return_value=router),
        ):
            result = await svc._handle_update_issue(intent, "wf", session_id=sid, user_id=USER)
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_a_not_single_read_newer_than_the_create_refuses(self, svc, sid):
        rows = [_row(22, _now() - timedelta(seconds=5))]
        record_shown_issues(sid, USER, [(SHOWN_REPO, 1), (SHOWN_REPO, 2)])
        intent, _ = _it_turn("update_issue", number=22)
        result, router = await _run(svc, sid, "update_issue", intent, rows)
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_another_user_or_session_created_head_is_not_this_ones(self, svc, sid):
        intent = _intent(
            "update_issue",
            "rename it to X",
            title="X",
            issue_number=22,
            repository=HEAD_REPO,
            user_id="someone-else",
        )
        ledger = AsyncMock(return_value=[])
        router = _router()
        with patch(LEDGER, new=ledger), patch(ROUTER, return_value=router):
            result = await svc._handle_update_issue(intent, "wf", session_id=sid, user_id=None)
        ledger.assert_awaited_once_with("someone-else", sid)
        assert result.message == MAIN_UPDATE_ASK


class TestGateUnit:
    async def test_unreadable_head_is_no_head(self):
        intent = _intent("update_issue", "rename it")
        verdict = await gate_issue_write(
            intent,
            22,
            has_free_text_field=True,
            repository=None,
            user_id=USER,
            session_id="s",
            created_head=AsyncMock(return_value=LEDGER_UNREADABLE),
        )
        assert verdict.accepted is False

    async def test_router_args_are_never_a_source(self):
        """A number only in router args is not what the handler acts on; the gate
        takes the candidate the handler gives it (here: none)."""
        intent = _intent("update_issue", "rename it", inversion_args={"issue_number": 22})
        verdict = await gate_issue_write(
            intent,
            None,
            has_free_text_field=True,
            repository=None,
            user_id=USER,
            session_id="s",
            created_head=AsyncMock(return_value=None),
        )
        assert verdict.accepted is False


# ---------------------------------------------------------------------------
# Issue 2460 (Arch): what counts as a TYPED issue number for a write
# ---------------------------------------------------------------------------


class TestTypedIssueNumber2460:
    """Arch's rule 1 as amended: on a free-text write, a MARKED number (``#N`` or
    ``issue N``) outside the field value being written; ``#N`` only when the value
    is not in the message; bare digits never. Close/reopen: one distinct number."""

    @pytest.mark.parametrize(
        "message, free_text, values, expected",
        [
            # The amended "So:" list.
            ("change the title of issue 108 to Draft 3", True, ["Draft 3"], 108),
            ("rename it to Test issue 2", True, ["Test issue 2"], None),
            ("change the title of issue #2 to Draft 3", True, ["Draft 3"], 2),
            ("comment on #4: see #9", True, ["see #9"], 4),
            # Two distinct marked numbers, both outside the value: the ask.
            ("change the title of #2 and #3 to Draft", True, ["Draft"], None),
            ("change the title of issue 2 and issue 3 to Draft", True, ["Draft"], None),
            # One number repeated is ONE distinct number.
            ("set #2 to Draft, yes #2", True, ["Draft"], 2),
            # The value is not in the message: only "#N" counts.
            ("change the title of issue 108 to Draft", True, ["Something else"], None),
            ("change the title of #108 to Draft", True, ["Something else"], 108),
            ("rename issue 108 please", True, [], None),
            # Bare digits never count on a free-text write.
            ("change the title of 108 to Draft", True, ["Draft"], None),
            # The forms of "issue N" accepted, and the ones not.
            ("change the title of Issue #108 to Draft", True, ["Draft"], 108),
            ("change the title of issue  108 to Draft", True, ["Draft"], 108),
            ("change the title of ISSUE 108 to Draft", True, ["Draft"], 108),
            ("change the title of issues 3 to Draft", True, ["Draft"], None),
            ("change the title of issue-108 to Draft", True, ["Draft"], None),
            ("change the title of issue108 to Draft", True, ["Draft"], None),
            ("change the title of reissue 5 to Draft", True, ["Draft"], None),
            # A number overlapping ANY occurrence of the value is excluded.
            ("Draft 3: set issue 7 to Draft 3", True, ["Draft 3"], 7),
            # The first "issue 7" is outside the value, the second inside: 7 counts.
            ("set issue 7 to Draft issue 7", True, ["Draft issue 7"], 7),
            # A partial overlap with the value excludes the number.
            ("set issue 7 to Draft", True, ["7 to Draft"], None),
            ("set it to Draft #7 now", True, ["Draft #7"], None),
            ("change #0 to X", True, ["X"], None),
            ("change # to X", True, ["X"], None),
            # Arch's three normalisations when locating the value (and nothing else).
            ("change the title of issue 8 to DRAFT Three", True, ["Draft three"], 8),
            ("change the title of issue 8 to Draft   three", True, ["Draft three"], 8),
            ("change the title of issue 8 to Draft three", True, ['"Draft three"'], 8),
            ("change the title of issue 8 to Draft three", True, ["\u2018Draft three\u2019"], 8),
            ('change the title of issue 8 to "Draft three"', True, ['"Draft three"'], 8),
            # A changed word or punctuation is not found: only "#N" counts.
            ("change the title of issue 8 to Draft three", True, ["Draft 3"], None),
            ("change the title of issue 8 to Draft three", True, ["Draft, three"], None),
            ("change the title of #8 to Draft three", True, ["Draft 3"], 8),
            # Spans map back to the ORIGINAL message across collapsed whitespace.
            ("change the title of issue  8 to Test  issue 2", True, ["Test issue 2"], 8),
            ("rename it to Test  issue  2", True, ["Test issue 2"], None),
            # Every field value takes part: labels, milestone (Arch's adjustment).
            ("add label v2 to issue 5", True, ["v2"], 5),
            ("add label 2024 to it", True, ["2024"], None),
            ("set the milestone of issue 9 to Sprint 3", True, ["Sprint 3"], 9),
            ("add label issue 4 to issue 5", True, ["issue 4"], 5),
            # Close/reopen (no free-text field) are unaffected by rule 1.
            ("close issue 5", False, [], 5),
            ("close issue 5", False, ["issue 5"], 5),
            ("close issue 5, it duplicates 7", False, [], None),
            ("close #5", False, [], 5),
            ("reopen 5", False, [], 5),
            ("close #5 and #5", False, [], 5),
            ("close #0", False, [], None),
            ("close #", False, [], None),
        ],
    )
    def test_the_rule(self, message, free_text, values, expected):
        assert typed_issue_number(message, free_text, values) == expected

    async def test_field_digit_with_no_head_gets_the_ask(self, svc, sid):
        intent = _intent(
            "update_issue", "rename it to Test issue 2", title="Test issue 2", repository=SHOWN_REPO
        )
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_field_digit_with_a_created_head_binds_the_head(self, svc, sid):
        intent = _intent("update_issue", "rename it to Test issue 2", title="Test issue 2")
        _, router = await _run(svc, sid, "update_issue", intent, [_row(22, _now())])
        kw = router.update_issue.await_args.kwargs
        assert (kw["issue_number"], kw["owner"], kw["repo_name"]) == (22, "acme", "widgets")

    async def test_issue_n_outside_the_title_targets_it_1411_kept(self, svc, sid):
        intent = _intent(
            "update_issue",
            "change the title of issue 108 to Draft 3",
            title="Draft 3",
            repository=SHOWN_REPO,
        )
        _, router = await _run(svc, sid, "update_issue", intent, [])
        assert router.update_issue.await_args.kwargs["issue_number"] == 108

    async def test_marked_number_beside_a_field_digit_targets_the_marked_one(self, svc, sid):
        intent = _intent(
            "update_issue",
            "change the title of issue #2 to Draft 3",
            title="Draft 3",
            repository=SHOWN_REPO,
        )
        _, router = await _run(svc, sid, "update_issue", intent, [])
        assert router.update_issue.await_args.kwargs["issue_number"] == 2

    async def test_two_marked_numbers_outside_the_title_get_the_ask(self, svc, sid):
        intent = _intent(
            "update_issue",
            "change the title of #2 and #3 to Draft",
            title="Draft",
            repository=SHOWN_REPO,
        )
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_a_bare_number_gets_the_existing_ask(self, svc, sid):
        """CXO's bare-number line is not shipped: on an imperative update no confirm
        stands in front of the write (1509's imperative pin), so "I'll ask you to
        confirm" would not be true. The existing ask stands, byte for byte."""
        intent = _intent(
            "update_issue", "change the title of 108 to Draft", title="Draft", repository=SHOWN_REPO
        )
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_a_shown_issue_and_a_bare_number_say_the_shown_statement(self, svc, sid):
        _shown_only(sid)
        intent = _intent(
            "update_issue", "change the title of 108 to Draft", title="Draft", repository=SHOWN_REPO
        )
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message == NAMED_1
        _assert_nothing_done(svc, sid, router, result)

    async def test_the_classifiers_no_hash_explicit_number_targets_it(self, svc, sid):
        """B3's 1411 explicit path puts 108 in context from "issue 108"; it is a
        marked number outside the new title, so it is typed."""
        message = "change the title of issue 108 to test new regressions"
        intent = _intent(
            "update_issue",
            message,
            issue_number=108,
            b3_resolved=True,
            b3_explicit=True,
            repository=SHOWN_REPO,
        )
        _, router = await _run(svc, sid, "update_issue", intent, [])
        assert router.update_issue.await_args.kwargs["issue_number"] == 108

    async def test_a_state_only_update_takes_one_bare_number(self, svc, sid):
        """No title or body is written, so rule 2 (one distinct number) applies."""
        intent = _intent(
            "update_issue", "close issue 31", state="closed", issue_number=31, repository=HEAD_REPO
        )
        _, router = await _run(svc, sid, "update_issue", intent, [])
        assert router.update_issue.await_args.kwargs["issue_number"] == 31

    async def test_a_changed_word_in_the_title_gets_the_ask(self, svc, sid):
        """The title the handler will write ("Draft 3") is not in the words ("Draft
        three"), so only "#N" counts and "issue 8" does not."""
        intent = _intent(
            "update_issue",
            "change the title of issue 8 to Draft three",
            title="Draft 3",
            repository=SHOWN_REPO,
        )
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_a_label_value_is_excluded_and_issue_n_outside_it_targets(self, svc, sid):
        intent = _intent(
            "update_issue", "add label v2 to issue 5", labels=["v2"], repository=SHOWN_REPO
        )
        _, router = await _run(svc, sid, "update_issue", intent, [])
        assert router.update_issue.await_args.kwargs["issue_number"] == 5

    async def test_a_digit_label_with_no_head_gets_the_ask(self, svc, sid):
        intent = _intent(
            "update_issue", "add label 2024 to it", labels=["2024"], repository=SHOWN_REPO
        )
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message == MAIN_UPDATE_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_a_digit_label_with_a_created_head_binds_the_head(self, svc, sid):
        intent = _intent("update_issue", "add label 2024 to it", labels=["2024"])
        _, router = await _run(svc, sid, "update_issue", intent, [_row(22, _now())])
        kw = router.update_issue.await_args.kwargs
        assert (kw["issue_number"], kw["labels"]) == (22, ["2024"])

    async def test_move_it_to_milestone_3_with_no_field_value_targets_3_and_writes_nothing(
        self, svc, sid
    ):
        """Pinned under Arch's adjustment: the update handler has no milestone slot, so
        this turn writes no field value; rule 2 then counts the one bare number (3). No
        field to change, so the handler's own "tell me what to change" line, no write."""
        intent = _intent("update_issue", "move it to milestone 3", repository=SHOWN_REPO)
        result, router = await _run(svc, sid, "update_issue", intent, [])
        assert result.message.startswith("Tell me what to change on #3")
        router.update_issue.assert_not_awaited()

    async def test_a_context_number_beside_a_field_digit(self, svc, sid):
        intent = _intent(
            "update_issue",
            "move it to milestone 3",
            title="X",
            issue_number=22,
            repository=HEAD_REPO,
        )
        _, router = await _run(svc, sid, "update_issue", intent, [_row(22, _now())])
        assert router.update_issue.await_args.kwargs["issue_number"] == 22

    async def test_args_differing_from_the_typed_number_write_the_typed_number(self, svc, sid):
        intent = _intent(
            "update_issue",
            "change the title of #5 to X",
            title="X",
            repository=SHOWN_REPO,
            inversion_args={"issue_number": 1},
        )
        _, router = await _run(svc, sid, "update_issue", intent, [])
        assert router.update_issue.await_args.kwargs["issue_number"] == 5

    @pytest.mark.parametrize("verb", ["close", "reopen"])
    async def test_close_and_reopen_take_a_single_bare_number(self, svc, sid, verb):
        action = f"{verb}_issue"
        intent = _intent(action, f"yes, {verb} issue 5 in {SHOWN_REPO}")
        _, router = await _run(svc, sid, action, intent, [])
        kw = router.update_issue.await_args.kwargs
        args = router.update_issue.await_args.args
        assert kw.get("issue_number", args[0] if args else None) == 5

    @pytest.mark.parametrize("verb", ["close", "reopen"])
    async def test_two_numbers_on_close_or_reopen_get_the_ask(self, svc, sid, verb):
        """No title-search match (mocked), so the plain ask; nothing armed or written.
        Before 2460 the first number (5) was taken."""
        action = f"{verb}_issue"
        intent = _intent(action, f"{verb} issue 5, it duplicates 7")
        router = _router()
        router.get_open_issues = AsyncMock(return_value=[])
        router.get_closed_issues = AsyncMock(return_value=[])
        with patch(LEDGER, new=AsyncMock(return_value=[])), patch(ROUTER, return_value=router):
            handler = (
                svc._handle_close_issue_query if verb == "close" else svc._handle_reopen_issue_query
            )
            result = await handler(intent, "wf", session_id=sid)
        assert result.message == PLAIN[action]
        _assert_nothing_done(svc, sid, router, result)

    async def test_a_marked_number_inside_the_comment_body_is_not_the_target(self, svc, sid):
        intent = _intent("comment_issue", f"comment on #4 in {SHOWN_REPO}: see #9")
        extracted = {"issue_number": "#4", "comment_text": "see #9"}
        _, router = await _run(svc, sid, "comment_issue", intent, [], extracted)
        assert router.add_comment.await_args.args[0] == 4

    async def test_the_extractor_picking_the_body_number_gets_the_ask(self, svc, sid):
        intent = _intent("comment_issue", "comment on #4: see #9")
        extracted = {"issue_number": "#9", "comment_text": "see #9"}
        result, router = await _run(svc, sid, "comment_issue", intent, [], extracted)
        assert result.message == MAIN_COMMENT_ASK
        _assert_nothing_done(svc, sid, router, result)

    async def test_issue_n_on_a_comment_counts(self, svc, sid):
        intent = _intent("comment_issue", f"comment on issue 4 in {SHOWN_REPO}: looks good")
        extracted = {"issue_number": "4", "comment_text": "looks good"}
        _, router = await _run(svc, sid, "comment_issue", intent, [], extracted)
        assert router.add_comment.await_args.args[0] == 4

    async def test_a_bare_comment_number_gets_the_ask(self, svc, sid):
        intent = _intent("comment_issue", "comment on 4: looks good")
        extracted = {"issue_number": "4", "comment_text": "looks good"}
        result, router = await _run(svc, sid, "comment_issue", intent, [], extracted)
        assert result.message == MAIN_COMMENT_ASK
        _assert_nothing_done(svc, sid, router, result)

    def test_the_close_confirm_builders_read_the_same_rule(self):
        from services.intent_service.destructive_confirm import _issue_number_from

        assert _issue_number_from(_intent("close_issue", "close issue 5")) == 5
        assert _issue_number_from(_intent("close_issue", "close issue 5, it duplicates 7")) is None

    def test_the_read_keeps_its_own_parse(self):
        """Rule 3: review_issue_query still reads the first number, as on main."""
        import inspect

        src = inspect.getsource(IntentService._handle_review_issue_query)
        assert 're.search(r"#?(\\d+)", original_message)' in src


# ---------------------------------------------------------------------------
# The #2304 write ask and the #1959 close/reopen builder: gated before arming
# ---------------------------------------------------------------------------


class TestAskTimeGate:
    async def test_update_write_ask_passes_a_refused_number_through_unarmed(self, sid):
        from services.intent_service.write_confirm_words import (
            WRITE_ASK_BOUND_KEY,
            WriteAskRequest,
            update_issue_write_ask,
        )

        _shown_only(sid)
        intent = _intent(
            "update_issue", "rename it to X", title="X", issue_number=1, repository=SHOWN_REPO
        )
        service = SimpleNamespace(_issue_referent_from_ledger=AsyncMock(return_value=None))
        ask = await update_issue_write_ask(
            WriteAskRequest(
                intent=intent,
                message="rename it to X",
                intent_service=service,
                session_id=sid,
                user_id=USER,
            )
        )
        assert ask.passthrough is True and ask.words is None
        assert WRITE_ASK_BOUND_KEY not in intent.context

    async def test_close_builder_gates_before_arming(self):
        from services.intent_service import destructive_confirm as dc

        intent = _intent("close_issue", "close #4")
        with patch(
            "services.intent_service.issue_write_gate.gate_issue_write",
            new=AsyncMock(return_value=SimpleNamespace(accepted=False)),
        ):
            gate = await dc.build_close_reopen_confirmation(intent, MagicMock(), "wf")
        assert gate.offer is None and gate.passthrough_result is None


# ---------------------------------------------------------------------------
# The full two-turn flow on update_issue: created head, ask, "yes", the write
# ---------------------------------------------------------------------------


class TestTwoTurnYes:
    """Turn 1 runs the rail's own pieces (the entry's write ask and the #1190 consent
    carrier); turn 2 runs the #1190 confirm workflow the "yes" seam dispatches. Driven
    below process_intent so no database row is written by the turn's other seams."""

    async def test_created_head_question_then_yes_writes_the_created_issue(self, svc, sid):
        from services.intent_service import consent_gate
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import (
            register_default_workflows,
            run_confirm_pending_action_workflow,
        )

        register_default_workflows()
        message = "the title of it ought to say New name"
        b3_shape = _intent(
            "update_issue", message, issue_number=22, repository=HEAD_REPO, title="New name"
        )
        router = _router()
        with (
            patch(LEDGER, new=AsyncMock(return_value=[_row(22, _now())])),
            patch(ROUTER, return_value=router),
            patch(
                "services.mcp.consumer.github_adapter.github_app_write_refusal_line",
                new=AsyncMock(return_value=None),
            ),
        ):
            ask = await svc._resolve_rail_write_ask(
                get_action_workflows()["update_issue"], b3_shape, message, USER, sid, USER
            )
        assert ask.words.question == "Change the title of issue #22 in acme/widgets? (yes/no)"
        check = consent_gate.build_consent_check_offer(b3_shape, ask.words)
        svc.workflow_offer_service.set_pending_offer(sid, check.offer, user_id=USER)
        router.update_issue.assert_not_awaited()

        offer = svc.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=USER)
        assert offer is not None
        # The "yes" is not gated again: a ledger that now fails does not refuse it.
        with (
            patch(LEDGER, new=AsyncMock(side_effect=RuntimeError("db down"))),
            patch(ROUTER, return_value=router),
        ):
            done = await run_confirm_pending_action_workflow(
                sid,
                USER,
                context={"pending_action": offer["pending_action"], "intent_service": svc},
            )
        router.update_issue.assert_awaited_once()
        kw = router.update_issue.await_args.kwargs
        assert (kw["issue_number"], kw["owner"], kw["repo_name"], kw["title"]) == (
            22,
            "acme",
            "widgets",
            "New name",
        )
        assert "Updated issue #22" in str(done)

    async def test_a_shown_issue_question_is_never_armed(self, svc, sid):
        """The same turn with the number taken from a shown issue: no question, the
        rail passes through to the handler, which says the named ask."""
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        _shown_only(sid)
        message = "the title of it ought to say New name"
        shown_shape = _intent(
            "update_issue", message, issue_number=1, repository=SHOWN_REPO, title="New name"
        )
        with patch(LEDGER, new=AsyncMock(return_value=[])):
            ask = await svc._resolve_rail_write_ask(
                get_action_workflows()["update_issue"], shown_shape, message, USER, sid, USER
            )
        assert ask.passthrough is True and ask.words is None
        result, router = await _run(svc, sid, "update_issue", shown_shape, [])
        assert result.message == NAMED_1
        _assert_nothing_done(svc, sid, router, result)


# ---------------------------------------------------------------------------
# Rule 1(a): the snapshot's RECENT ISSUE is fed by choose_issue_referent
# ---------------------------------------------------------------------------


class TestSnapshotRecentIssue:
    @pytest.fixture
    def quiet_reads(self, monkeypatch):
        from services.intent_service import collaboration_gate, verified_inference
        from services.process.registry import ProcessRegistry

        async def _load(user_id):
            return {}

        monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
        monkeypatch.setattr(
            verified_inference, "get_verified_inference", AsyncMock(return_value=None)
        )
        ProcessRegistry.reset_instance()
        yield
        ProcessRegistry.reset_instance()

    async def _snap(self, sid, rows):
        from services.intent_service.snapshot_assembly import assemble_session_snapshot
        from services.intent_service.soft_invocation import WorkflowOfferService

        stub = SimpleNamespace(workflow_offer_service=WorkflowOfferService())
        with patch(LEDGER, new=AsyncMock(return_value=rows)):
            return await assemble_session_snapshot(sid, USER, stub)

    async def test_a_newer_single_show_is_the_recent_issue(self, sid, quiet_reads):
        from services.intent_service.session_snapshot import serialize_for_prompt

        snap = await self._snap(sid, _created_then_shown(sid))
        assert (snap.recent_issue_number, snap.recent_issue_repo) == (1, SHOWN_REPO)
        assert (
            "RECENT ISSUE: #1 in pipermorgan/piper-test (bare 'it'/'that issue' likely refers here)"
            in serialize_for_prompt(snap)
        )

    async def test_a_newer_create_is_the_recent_issue(self, sid, quiet_reads):
        snap = await self._snap(sid, _shown_then_created(sid))
        assert (snap.recent_issue_number, snap.recent_issue_repo) == (22, HEAD_REPO)

    async def test_a_newer_multi_read_leaves_no_recent_issue(self, sid, quiet_reads):
        rows = [_row(22, _now() - timedelta(seconds=5))]
        record_shown_issues(sid, USER, [(SHOWN_REPO, 1), (SHOWN_REPO, 2)])
        snap = await self._snap(sid, rows)
        assert snap.recent_issue_number is None and snap.recent_issue_repo is None

    async def test_created_only_is_unchanged(self, sid, quiet_reads):
        snap = await self._snap(sid, [_row(22, _now())])
        assert (snap.recent_issue_number, snap.recent_issue_repo) == (22, HEAD_REPO)

    def test_the_slot_read_creates_no_context(self, sid):
        """The slot read the snapshot adds is read-only (the offer peek already in
        the snapshot is a separate read, not changed here)."""
        from services.intent_service import conversation_context as cc
        from services.intent_service.shown_issue import last_shown_issue

        assert last_shown_issue(sid, USER) is None
        assert cc._context_key(sid, USER) not in cc._conversation_contexts
