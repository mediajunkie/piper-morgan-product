"""#2098 — "change the title to X" on a pending issue draft (Arch's shape, 2026-10-19).

Web's #1386 scenario B3 on alpha e801b1a309: with a draft pending, "Actually, change the
title to '<new>'" was appended to the body and the title stayed. The first fix (a marker
list) was a binder and retitled on body prose ("we should call it out in the release
notes" → "out in the release notes"); reverted at f260d8ed5b. This is the replacement: the
carrier consults the router on the held turn through ``classify_armed_reply`` with
``update_issue`` as its answering operation. Only a BIND naming ``update_issue`` with a
non-empty ``title`` retitles; ``none``, CONFIRM, RELEASE, a title-less bind and a consult
failure all continue down today's path (the #1627 body bind).

LAYER: ``handle_drafted_issue_turn`` with the real offer store and the consult stubbed.
DENOMINATOR: the five consult outcomes, the no-LLM failure path, Arch's three misfire
strings, the filing path's title read, the binder's absence.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import drafted_issue as mod
from services.intent_service.armed_turn_consult import ArmedReplyDecision, ArmedReplyOutcome
from services.intent_service.classifier import IntentClassifier
from services.intent_service.drafted_issue import DRAFTED_ISSUE_KIND, handle_drafted_issue_turn
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

CONSULT = "services.intent_service.armed_turn_consult.classify_armed_reply"
_USER = "3f7b8a52-2098-4b00-9e00-000000002098"
OLD_TITLE = "Add search functionality to navigation bar"
NEW_TITLE = "Implement full-text search across nav and global search bar"
BODY = "Users can't find pages from the nav; search should cover nav items and content."
TITLE_TURN = f"Actually, change the title to '{NEW_TITLE}'"
PROSE_TURN = "Also we should call it out in the release notes"
# A body answer long enough to read as prose at the seam (the #1627 length floor), so the
# "every other outcome binds to the body" pins exercise the bind rather than the fall-through.
PROSE_LONG = (
    "Also we should call it out in the release notes and mention the keyboard shortcut that "
    "opens search, since support keeps getting asked about it every week."
)
ARCH_MISFIRES = [
    PROSE_TURN,
    "Add that users name it as their top pain",
    "Please make the title shorter",
]


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def svc():
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _offer():
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="create_issue",
        confidence=0.95,
        original_message=f"draft an issue about {OLD_TITLE}",
        context={"title": OLD_TITLE, "description": BODY, "repository": "octo/repo"},
    )
    return {
        "kind": DRAFTED_ISSUE_KIND,
        "question": mod._POST_BIND_ASK,
        "pending_action": {
            "action": "create_issue",
            "intent": intent,
            "draft": {"title": OLD_TITLE, "body": BODY, "repository": "octo/repo"},
            "summary": f"Issue in octo/repo: {OLD_TITLE}",
        },
    }


def _walk_offers(store):
    """The offer store's shape is the service's own; find every offer dict in it."""
    if isinstance(store, dict):
        if "pending_action" in store:
            yield store
        else:
            for v in store.values():
                yield from _walk_offers(v)
    elif isinstance(store, (list, tuple)):
        for v in store:
            yield from _walk_offers(v)


def _decision(outcome, operation=None, **args):
    return ArmedReplyDecision(outcome=outcome, operation=operation, confidence=0.9, args=args)


async def _turn(svc, message, decision=None, sid="s-2098"):
    offer = _offer()
    if decision is None:
        return offer, await handle_drafted_issue_turn(
            offer, message, session_id=sid, user_id=_USER, intent_service=svc
        )
    stub = AsyncMock(return_value=decision)
    with patch(CONSULT, new=stub):
        result = await handle_drafted_issue_turn(
            offer, message, session_id=sid, user_id=_USER, intent_service=svc
        )
    return offer, result, stub


class TestBindRetitles:
    @pytest.mark.asyncio
    async def test_update_issue_bind_with_title_retitles_keeps_body_and_rearms(self, svc):
        offer, result, stub = await _turn(
            svc, TITLE_TURN, _decision(ArmedReplyOutcome.BIND, "update_issue", title=NEW_TITLE)
        )
        assert result["message"].startswith(
            "Updated the title. Nothing is filed yet. Here's the draft:"
        )
        assert f"**Title**: {NEW_TITLE}" in result["message"]
        assert BODY in result["message"]
        assert result["intent_data"]["drafted_issue_retitled"] is True
        assert result["requires_clarification"] is True
        draft = offer["pending_action"]["draft"]
        assert draft["title"] == NEW_TITLE and draft["body"] == BODY
        # the create rail reads intent.context["title"] first: "file it as is" files the new one
        assert offer["pending_action"]["intent"].context["title"] == NEW_TITLE
        assert offer["pending_action"]["intent"].context["description"] == BODY
        # re-armed in the store with the retitled draft
        store = svc.workflow_offer_service._pending_offers
        stored = [
            o
            for o in _walk_offers(store)
            if (o.get("pending_action") or {}).get("draft", {}).get("title") == NEW_TITLE
        ]
        assert stored, f"retitled draft not re-armed in the store: {list(store)}"
        # the consult saw the message with update_issue as this carrier's answering operation
        kwargs = stub.await_args.kwargs
        assert stub.await_args.args[0] == TITLE_TURN
        assert kwargs["answering_operations"] == frozenset({"update_issue"})

    @pytest.mark.asyncio
    async def test_title_value_is_stripped(self, svc):
        offer, result, _ = await _turn(
            svc,
            TITLE_TURN,
            _decision(ArmedReplyOutcome.BIND, "update_issue", title=f"  {NEW_TITLE}  "),
        )
        assert offer["pending_action"]["draft"]["title"] == NEW_TITLE


class TestEverythingElseIsTodaysPath:
    @pytest.mark.parametrize(
        "decision",
        [
            _decision(ArmedReplyOutcome.BIND, None),  # router none → body prose
            _decision(ArmedReplyOutcome.CONFIRM, None),  # uncertain → never a silent retitle
            _decision(ArmedReplyOutcome.RELEASE, "list_projects"),  # the #1627 hold stays
            _decision(ArmedReplyOutcome.BIND, "update_issue"),  # named, but no title value
            _decision(ArmedReplyOutcome.BIND, "update_issue", title="   "),
        ],
        ids=["none", "confirm", "release", "no-title-arg", "blank-title"],
    )
    @pytest.mark.asyncio
    async def test_non_title_outcomes_bind_prose_to_the_body(self, svc, decision):
        offer, result, _ = await _turn(svc, PROSE_LONG, decision)
        assert result["message"].startswith("Added to the draft — nothing is filed yet.")
        draft = offer["pending_action"]["draft"]
        assert draft["title"] == OLD_TITLE
        assert draft["body"].endswith(PROSE_LONG)
        assert "drafted_issue_retitled" not in result["intent_data"]

    # #2098 reopened (Arch's remedy ruling 2026-11-02): the "confirm" row moved out of
    # this pin. A CONFIRM on a held draft now ASKS (TestConfirmAsks below); only the
    # router's ``none`` and a title-less update_issue BIND keep the fall-through.
    @pytest.mark.parametrize(
        "decision",
        [
            _decision(ArmedReplyOutcome.BIND, None),
            _decision(ArmedReplyOutcome.BIND, "update_issue"),
        ],
        ids=["none", "no-title-arg"],
    )
    @pytest.mark.asyncio
    async def test_command_shaped_title_turn_without_a_title_falls_through_never_retitles(
        self, svc, decision
    ):
        """Arch's shape, point 3: with no router value there is nothing to confirm, so the
        turn takes today's path. "Actually, change the title to …" is command-shaped (the
        execute framing reads through the lead-in since this row), and a command-shaped
        turn on a held draft falls through to the generic flow, as it did before #2098.
        The one thing that must never happen is a retitle on a guess."""
        offer, result, _ = await _turn(svc, TITLE_TURN, decision)
        assert result is None
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE

    @pytest.mark.parametrize("prose", ARCH_MISFIRES)
    @pytest.mark.asyncio
    async def test_arch_misfire_strings_on_a_none_verdict_go_to_the_body(self, svc, prose):
        offer, result, _ = await _turn(svc, prose, _decision(ArmedReplyOutcome.BIND, None))
        # The title never moves on a none verdict. Where the turn goes next is today's
        # path (a long answer binds to the body; a short one re-asks or falls through).
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE
        assert "Updated the title" not in ((result or {}).get("message") or "")
        if result is not None and result.get("intent_data", {}).get("drafted_issue_body_bound"):
            assert offer["pending_action"]["draft"]["body"].endswith(prose)

    @pytest.mark.asyncio
    async def test_consult_without_an_llm_asks_not_a_crash(self, svc):
        """The real consult against the explosive LLM: its failure path is CONFIRM
        (consult_exception), so prose binds to the body and, since Arch's remedy ruling
        (2026-11-02), the command-shaped title turn ASKS case 2 instead of falling
        through to the classifier."""
        offer, result = await _turn(svc, PROSE_LONG)
        assert result["message"].startswith("Added to the draft — nothing is filed yet.")
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE
        offer, result = await _turn(svc, TITLE_TURN)
        assert result["message"] == mod.TITLE_QUESTION_NO_TITLE
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE

    @pytest.mark.asyncio
    async def test_accept_and_decline_never_reach_the_consult(self, svc):
        stub = AsyncMock(side_effect=AssertionError("consulted"))
        with patch(CONSULT, new=stub):
            offer = _offer()
            assert (
                await handle_drafted_issue_turn(
                    offer, "no, drop it", session_id="s-d", user_id=_USER, intent_service=svc
                )
                is None
            )
        assert stub.await_count == 0


class TestNoBinderCameBack:
    def test_marker_list_and_extractor_are_gone(self):
        assert not hasattr(mod, "_TITLE_CHANGE_MARKERS")
        assert not hasattr(mod, "extract_title_change")

    def test_corpus_carries_both_rows(self):
        import yaml

        rows = yaml.safe_load(open("tests/fixtures/inversion_corpus_phase0.yaml"))["corpus"]
        by_phrase = {r["phrase"]: r for r in rows}
        assert by_phrase[TITLE_TURN]["expected"] == "action:update_issue"
        assert by_phrase[TITLE_TURN]["expected_args"] == {"title": NEW_TITLE}
        assert by_phrase[PROSE_TURN]["expected"] == "floor"


# ---------------------------------------------------------------------------
# #2098 reopened (2026-11-02): a CONFIRM asks. Arch's remedy ruling; CXO's words as
# amended 19:21. LAYER: ``handle_drafted_issue_turn`` with the real offer store, the
# consult stubbed, the next turn handed the record the store holds (the seam's pop);
# one served class drives ``process_intent``. DENOMINATOR: the three CONFIRM reasons
# (sub_threshold with a title, router_clarify, consult_exception), RELEASE, the
# misfire control, the answer turn's six shapes (yes, no, a declining exit, a title,
# a non-answer, a yes with no title) and "file it as is" after yes / no / ignore.
# ---------------------------------------------------------------------------

DOCUMENTS_LINE = "I can't update documents from chat yet"
QUOTED_TITLE = 'Fix the "save" button\'s lag'
WORKFLOW = "services.intent_service.workflow_entries.run_confirm_pending_action_workflow"
# At/above soft_invocation.PROSE_LENGTH_FLOOR (160): prose by shape, never a title answer.
PROSE_OVER_FLOOR = PROSE_LONG + " It needs a docs page too."


def _confirm(reason, **args):
    return ArmedReplyDecision(
        outcome=ArmedReplyOutcome.CONFIRM, confidence=0.5, reason=reason, args=args
    )


def _stored(svc, sid):
    """What the seam pops on the next turn."""
    return svc.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER)


async def _next(svc, sid, message, decision=None):
    offer = _stored(svc, sid)
    assert offer is not None, "the draft was not left armed"
    if decision is None:
        result = await handle_drafted_issue_turn(
            offer, message, session_id=sid, user_id=_USER, intent_service=svc
        )
    else:
        with patch(CONSULT, new=AsyncMock(return_value=decision)):
            result = await handle_drafted_issue_turn(
                offer, message, session_id=sid, user_id=_USER, intent_service=svc
            )
    return offer, result


async def _file(svc, sid):
    """ "file it as is" with the create rail stubbed; returns the title it filed."""
    seen = {}

    async def _run(*, session_id, user_id, context):
        seen["title"] = context["pending_action"]["intent"].context["title"]
        return {"message": "Created issue #7 in octo/repo", "intent_data": {"issue_number": 7}}

    offer = _stored(svc, sid)
    with patch(WORKFLOW, new=_run):
        result = await handle_drafted_issue_turn(
            offer, "file it as is", session_id=sid, user_id=_USER, intent_service=svc
        )
    assert result["intent_data"]["issue_number"] == 7
    return seen["title"]


class TestCxoStrings:
    def test_the_four_strings_by_text(self):
        assert (
            mod.TITLE_QUESTION_WITH_TITLE
            == 'Do you want the draft\'s title changed to "{title}"? Nothing is filed yet.'
        )
        assert mod.TITLE_QUESTION_NO_TITLE == (
            "I couldn't tell what you wanted changed. What should the draft's title be? "
            "Nothing is filed yet, and the draft keeps its current title until you say."
        )
        assert mod.TITLE_CHANGED_LINE == (
            'The draft\'s title is now "{title}". Nothing is filed yet. '
            'Say "file it as is" when it\'s ready, or tell me a different title.'
        )
        assert mod.TITLE_KEPT_LINE == (
            'Okay, I\'m keeping "{title}". Nothing is filed yet. '
            'Say "file it as is" when it\'s ready.'
        )


class TestConfirmAsks:
    @pytest.mark.asyncio
    async def test_sub_threshold_with_a_title_asks_case_1_and_keeps_the_old_title(self, svc):
        offer, result, _ = await _turn(svc, TITLE_TURN, _confirm("sub_threshold", title=NEW_TITLE))
        assert result["message"] == (
            f'Do you want the draft\'s title changed to "{NEW_TITLE}"? Nothing is filed yet.'
        )
        assert result["intent_data"]["drafted_issue_title_question"] is True
        stored = _stored(svc, "s-2098")
        pa = stored["pending_action"]
        assert pa["draft"]["title"] == OLD_TITLE and pa["draft"]["body"] == BODY
        assert pa["intent"].context["title"] == OLD_TITLE  # display only until the yes
        assert pa[mod.TITLE_QUESTION_KEY] == {"old_title": OLD_TITLE, "proposed_title": NEW_TITLE}
        assert stored["question"] == result["message"]  # #1665: what's stored is what's said

    @pytest.mark.parametrize("reason", ["router_clarify", "consult_exception"])
    @pytest.mark.asyncio
    async def test_confirm_without_a_title_asks_case_2(self, svc, reason):
        offer, result, _ = await _turn(svc, TITLE_TURN, _confirm(reason))
        assert result["message"] == mod.TITLE_QUESTION_NO_TITLE
        stored = _stored(svc, "s-2098")
        assert stored["pending_action"]["draft"]["title"] == OLD_TITLE
        assert stored["pending_action"][mod.TITLE_QUESTION_KEY]["proposed_title"] is None
        assert DOCUMENTS_LINE not in result["message"]

    @pytest.mark.asyncio
    async def test_release_falls_through_exactly_as_today(self, svc):
        offer, result, _ = await _turn(
            svc,
            TITLE_TURN,
            ArmedReplyDecision(
                outcome=ArmedReplyOutcome.RELEASE, operation="list_projects", confidence=0.95
            ),
        )
        assert result is None
        assert mod.TITLE_QUESTION_KEY not in offer["pending_action"]
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE

    @pytest.mark.asyncio
    async def test_misfire_control_still_binds_the_body_no_question(self, svc):
        offer, result, _ = await _turn(svc, PROSE_TURN, _confirm("router_clarify"))
        assert result["message"].startswith("Added to the draft — nothing is filed yet.")
        assert offer["pending_action"]["draft"]["body"].endswith(PROSE_TURN)
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE
        assert mod.TITLE_QUESTION_KEY not in offer["pending_action"]

    @pytest.mark.asyncio
    async def test_bare_exit_on_a_confirm_still_drops_through_the_generic_flow(self, svc):
        offer, result, _ = await _turn(svc, "cancel", _confirm("router_clarify"))
        assert result is None
        assert mod.TITLE_QUESTION_KEY not in offer["pending_action"]


class TestTheAnswerTurn:
    @pytest.mark.asyncio
    async def test_case_1_yes_applies_the_title_and_file_files_the_new_one(self, svc):
        await _turn(svc, TITLE_TURN, _confirm("sub_threshold", title=NEW_TITLE))
        offer, result = await _next(svc, "s-2098", "yes")
        assert result["message"] == (
            f'The draft\'s title is now "{NEW_TITLE}". Nothing is filed yet. '
            'Say "file it as is" when it\'s ready, or tell me a different title.'
        )
        assert offer["pending_action"]["draft"]["body"] == BODY
        assert mod.TITLE_QUESTION_KEY not in offer["pending_action"]
        assert await _file(svc, "s-2098") == NEW_TITLE

    @pytest.mark.parametrize("answer", ["no", "never mind"])
    @pytest.mark.asyncio
    async def test_case_1_decline_keeps_the_old_title_and_file_files_it(self, svc, answer):
        await _turn(svc, TITLE_TURN, _confirm("sub_threshold", title=NEW_TITLE))
        stub = AsyncMock(side_effect=AssertionError("a decline never consults"))
        with patch(CONSULT, new=stub):
            offer, result = await _next(svc, "s-2098", answer)
        assert result["message"] == mod.TITLE_KEPT_LINE.format(title=OLD_TITLE)
        # Arch's condition (20:21): the stored ask is exactly the line shown, and
        # it carries the file prompt, so a bare yes next answers a filing ask.
        assert offer["question"] == result["message"]
        assert 'Say "file it as is" when it\'s ready.' in offer["question"]
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE
        assert await _file(svc, "s-2098") == OLD_TITLE

    @pytest.mark.asyncio
    async def test_case_2_free_text_title_is_taken_verbatim(self, svc):
        await _turn(svc, TITLE_TURN, _confirm("router_clarify"))
        offer, result = await _next(
            svc, "s-2098", QUOTED_TITLE, ArmedReplyDecision(outcome=ArmedReplyOutcome.BIND)
        )
        assert result["message"] == mod.TITLE_CHANGED_LINE.format(title=QUOTED_TITLE)
        assert f'"{QUOTED_TITLE}"' in result["message"]  # the stored title, verbatim
        assert offer["pending_action"]["draft"]["title"] == QUOTED_TITLE
        assert offer["pending_action"]["draft"]["body"] == BODY
        assert await _file(svc, "s-2098") == QUOTED_TITLE

    @pytest.mark.asyncio
    async def test_case_1_renders_a_quoted_title_unchanged(self, svc):
        _, result, _ = await _turn(svc, TITLE_TURN, _confirm("sub_threshold", title=QUOTED_TITLE))
        assert result["message"] == (
            f'Do you want the draft\'s title changed to "{QUOTED_TITLE}"? Nothing is filed yet.'
        )

    @pytest.mark.asyncio
    async def test_a_non_answer_is_not_stored_as_the_title(self, svc):
        """CXO's amendment 4: "the one I said" is decided by the idiom's own
        classification (the router CONFIRMs: not a value), never a phrase list."""
        await _turn(svc, TITLE_TURN, _confirm("router_clarify"))
        offer, result = await _next(svc, "s-2098", "the one I said", _confirm("router_clarify"))
        assert result["message"] == mod.TITLE_QUESTION_NO_TITLE
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE
        assert await _file(svc, "s-2098") == OLD_TITLE

    @pytest.mark.asyncio
    async def test_confirm_re_asks_once_then_keeps_the_old_title(self, svc):
        """Arch's confirmation (2026-11-02 19:3x): CONFIRM re-asks ONCE. A second
        unclear answer keeps the old title and says so; the draft stays armed."""
        await _turn(svc, TITLE_TURN, _confirm("router_clarify"))
        _, first = await _next(svc, "s-2098", "the one I said", _confirm("router_clarify"))
        assert first["message"] == mod.TITLE_QUESTION_NO_TITLE
        offer, second = await _next(svc, "s-2098", "you know", _confirm("router_clarify"))
        assert second["message"] == mod.TITLE_KEPT_LINE.format(title=OLD_TITLE)
        assert offer["question"] == second["message"]
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE
        assert mod.TITLE_QUESTION_KEY not in offer["pending_action"]
        assert await _file(svc, "s-2098") == OLD_TITLE

    @pytest.mark.asyncio
    async def test_case_2_yes_names_no_title_and_asks_again(self, svc):
        await _turn(svc, TITLE_TURN, _confirm("router_clarify"))
        offer, result = await _next(svc, "s-2098", "yes")
        assert result["message"] == mod.TITLE_QUESTION_NO_TITLE
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE

    @pytest.mark.asyncio
    async def test_ignored_question_then_file_files_the_old_title(self, svc):
        await _turn(svc, TITLE_TURN, _confirm("sub_threshold", title=NEW_TITLE))
        assert await _file(svc, "s-2098") == OLD_TITLE

    @pytest.mark.asyncio
    async def test_update_issue_bind_on_the_answer_uses_its_title_arg(self, svc):
        await _turn(svc, TITLE_TURN, _confirm("router_clarify"))
        offer, result = await _next(
            svc,
            "s-2098",
            f"make it '{NEW_TITLE}'",
            _decision(ArmedReplyOutcome.BIND, "update_issue", title=NEW_TITLE),
        )
        assert result["message"] == mod.TITLE_CHANGED_LINE.format(title=NEW_TITLE)

    @pytest.mark.asyncio
    async def test_release_on_the_answer_routes_normally(self, svc):
        await _turn(svc, TITLE_TURN, _confirm("router_clarify"))
        offer, result = await _next(
            svc,
            "s-2098",
            "close issue #108",
            ArmedReplyDecision(
                outcome=ArmedReplyOutcome.RELEASE, operation="close_issue", confidence=0.95
            ),
        )
        assert result is None
        # Arch (19:3x): the generic path takes the command; the draft keeps its old
        # title and stays armed, the question closed.
        stored = _stored(svc, "s-2098")
        assert stored is not None
        assert stored["pending_action"]["draft"]["title"] == OLD_TITLE
        assert stored["pending_action"]["draft"]["body"] == BODY
        assert mod.TITLE_QUESTION_KEY not in stored["pending_action"]
        assert stored["question"] == mod._POST_BIND_ASK

    @pytest.mark.asyncio
    async def test_long_prose_on_the_answer_binds_the_body_not_the_title(self, svc):
        await _turn(svc, TITLE_TURN, _confirm("router_clarify"))
        stub = AsyncMock(side_effect=AssertionError("prose never consults"))
        with patch(CONSULT, new=stub):
            offer, result = await _next(svc, "s-2098", PROSE_OVER_FLOOR)
        assert result["message"].startswith("Added to the draft — nothing is filed yet.")
        assert offer["pending_action"]["draft"]["body"].endswith(PROSE_OVER_FLOOR)
        assert offer["pending_action"]["draft"]["title"] == OLD_TITLE
        assert mod.TITLE_QUESTION_KEY not in offer["pending_action"]


class TestServedTurnNeverReachesTheClassifier:
    @pytest.mark.asyncio
    async def test_process_intent_asks_and_never_classifies(self, svc):
        sid = "s-2098-served"
        intent = _offer()["pending_action"]["intent"]
        armed = mod.build_drafted_issue_offer(
            intent, OLD_TITLE, "octo/repo", body=BODY, question=mod._POST_BIND_ASK
        )
        svc.workflow_offer_service.set_pending_offer(sid, armed, user_id=_USER)
        classify = AsyncMock(side_effect=AssertionError("classifier reached"))
        with (
            patch.object(svc.intent_classifier, "classify", new=classify),
            patch(CONSULT, new=AsyncMock(return_value=_confirm("router_clarify"))),
        ):
            r = await svc.process_intent(message=TITLE_TURN, session_id=sid, user_id=_USER)
        assert r.message == mod.TITLE_QUESTION_NO_TITLE
        assert DOCUMENTS_LINE not in r.message
        classify.assert_not_awaited()
        stored = svc.workflow_offer_service.peek_pending_offer(sid, user_id=_USER)
        assert stored["pending_action"]["draft"]["title"] == OLD_TITLE
