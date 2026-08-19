"""#1648 — floor action-fabrication, the two transcript shapes pinned e2e.

PM live 2026-08-18 (v58), two verified instances in one session:

1. **The phantom ticket**: draft armed, PM said "file as is thanks" — the
   file-command detector missed the variant, the turn fell through the
   drafted-issue seam as off-intent, and the FLOOR roleplayed the filing
   ("Filed in test-piper-morgan. The issue is in there now." — zero writes,
   no issue number).
2. **The phantom reminder**: the time-clarify ask ("When should I remind
   you?") armed NOTHING, so the answer "at 3pm" orphaned into the routing
   chain and the floor roleplayed the save ("Reminder set for 3pm today." —
   no row, no 📅 line).

Layer honesty (m-43): the e2e classes drive the REAL
``IntentService.process_intent`` with an explosive LLM — every pinned turn
must resolve deterministically (offer seam or pre-classifier), because the
live failures happened exactly when a turn escaped to the LLM lane. The
detector/discriminator classes are pure-unit. The prompt half is pinned in
test_floor_action_claims_1648.py.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.drafted_issue import (
    DRAFTED_ISSUE_KIND,
    detect_file_command,
    is_file_near_miss,
)
from services.intent_service.todo_handlers import (
    REMINDER_TIME_QUESTION_KIND,
    build_reminder_time_offer,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

GATE = "services.intent_service.collaboration_gate"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
RESOLVER = "services.integrations.github.repo_resolver.get_user_default_repo"

_USER = "3f7b8a52-1648-4b00-9e00-000000001648"

# PM's verbatim turns from the incident transcripts.
PM_FILE_AS_IS_THANKS = "file as is thanks"
PM_TIME_ANSWER = "at 3pm"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every pinned
    turn must resolve deterministically — the live fabrications happened
    when these turns escaped to the LLM lane and the floor claimed them."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1648 turns must resolve "
            "deterministically (offer seam / pre-classifier)"
        )


@pytest.fixture
def svc():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


# ---------------------------------------------------------------------------
# 1. Detector broadening (direction 3) — pure unit
# ---------------------------------------------------------------------------


class TestBroadenedFileCommandDetector:
    @pytest.mark.parametrize(
        "message",
        [
            PM_FILE_AS_IS_THANKS,  # the live miss: object-less "file as is"
            "file as is",
            "file it",
            "file it please",
            "file it, thanks!",
            "go ahead and file it",
            "yes, go ahead and file it",
            "file this as is, thank you",
            "file the draft as is thanks",
            "just file it",
            "Please file it as is",  # the #1571 originals must keep matching
            "file it as-is",
        ],
    )
    def test_accept_variants_match(self, message):
        assert detect_file_command(message) is not None, message

    def test_repo_override_still_binds(self):
        cmd = detect_file_command("file it in mediajunkie/test-piper-morgan")
        assert cmd == {"repo": "mediajunkie/test-piper-morgan"}

    @pytest.mark.parametrize(
        "message",
        [
            # Anchored: 'file' inside prose or a NEW ask must never match
            # (the #1631 lesson runs the other way here).
            "file an issue about flaky tests",
            "file a bug about the login timeout",
            "create an issue in owner/repo about testing",
            "I filed my taxes as is thanks to my accountant",
            "what should I file it under?",
            "can you file it later if I forget",
            "profile it",
            "file",  # bare verb carries no draft reference
            "no",
            "yes",
            "",
        ],
    )
    def test_non_commands_still_do_not_match(self, message):
        assert detect_file_command(message) is None, message


class TestFileNearMissDiscrimination:
    @pytest.mark.parametrize(
        "message",
        ["file the sucker", "just file that thing now", "submit the thing"],
    )
    def test_file_headed_variants_are_near_misses(self, message):
        assert is_file_near_miss(message) is True, message

    @pytest.mark.parametrize(
        "message",
        [
            "file a bug about X",  # a NEW ask with its own subject
            "file an issue about flaky tests",
            "close issue #108",  # other command families route normally
            "list my reminders",
            "no",
            "",
        ],
    )
    def test_new_asks_and_other_commands_are_not(self, message):
        assert is_file_near_miss(message) is False, message


# ---------------------------------------------------------------------------
# 2. Instance 1 e2e — "file as is thanks" files for real, never a floor claim
# ---------------------------------------------------------------------------


def _compose_intent(message="help me write a ticket about the login timeout on mobile"):
    return Intent(
        category=IntentCategory.EXECUTION,
        action="create_ticket",
        confidence=0.95,
        original_message=message,
        context={},
    )


async def _arm_draft(svc, sid):
    """Turn 1 (the compose/draft turn) at the handler seam — arms the binding
    (same harness as test_drafted_issue_1571)."""
    with (
        patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.create_issue", new=AsyncMock()),
    ):
        return await svc._handle_create_issue(
            _compose_intent(), "wf-1", sid, user_id=_USER
        )


class TestPhantomTicketEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_file_as_is_thanks_files_for_real(self, svc):
        """PM's verbatim turn now files the bound draft in one turn, with the
        REAL number from the tool result — never a roleplayed 'Filed'."""
        sid = "e2e-1648-file-thanks"
        await _arm_draft(svc, sid)
        created = {
            "number": 123,
            "html_url": "https://github.com/acme/widgets/issues/123",
            "title": "login timeout on mobile",
        }
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            result = await svc.process_intent(
                message=PM_FILE_AS_IS_THANKS, session_id=sid, user_id=_USER
            )
        w.assert_awaited_once()
        assert "#123" in result.message
        assert result.intent_data.get("issue_number") == 123
        assert "#[" not in result.message
        assert _pending_offers(svc) == {}

    async def test_near_miss_reasks_and_rearms_never_abandons(self, svc):
        """Direction 2: a file-shaped variant the detector still doesn't know
        must RE-ASK honestly and RE-ARM — the turn never reaches any
        classification surface (explosive LLM proves it), nothing files, and
        the draft survives."""
        sid = "e2e-1648-nearmiss"
        await _arm_draft(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            result = await svc.process_intent(
                message="file the sucker", session_id=sid, user_id=_USER
            )
        w.assert_not_awaited()
        # Honest: nothing filed, said plainly; the working moves are taught.
        assert "nothing has been filed" in result.message.lower()
        assert "file it as is" in result.message
        assert result.intent_data.get("drafted_issue_reasked") is True
        # The draft is still armed — the retry can file it.
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == DRAFTED_ISSUE_KIND

    async def test_near_miss_then_file_it_files_the_same_draft(self, svc):
        sid = "e2e-1648-nearmiss-retry"
        await _arm_draft(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()),
        ):
            await svc.process_intent(
                message="file the sucker", session_id=sid, user_id=_USER
            )
        created = {"number": 9, "html_url": "https://x/9", "title": "t"}
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(RESOLVER, new=AsyncMock(return_value="acme/widgets")),
        ):
            r2 = await svc.process_intent(
                message="file it", session_id=sid, user_id=_USER
            )
        w.assert_awaited_once()
        assert "#9" in r2.message
        assert _pending_offers(svc) == {}

    async def test_off_intent_command_still_routes_normally(self, svc):
        """The carrier's documented off-intent rule is untouched: an
        unrelated command abandons the draft and routes (here the
        deterministic close confirmation claims it)."""
        sid = "e2e-1648-offintent"
        await _arm_draft(svc, sid)
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            r = await svc.process_intent(
                message="close issue #108", session_id=sid, user_id=_USER
            )
        w.assert_not_awaited()
        assert "(yes/no)" in r.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"].get("kind") != DRAFTED_ISSUE_KIND


# ---------------------------------------------------------------------------
# 3. Instance 2 e2e — the 3pm path: real save with 📅, or honest inability
# ---------------------------------------------------------------------------


def _mock_todo_service(svc):
    """Swap the real DB-backed TodoManagementService for a mock that records
    the write. The seam under test is routing/binding, not persistence."""
    mock = MagicMock()
    mock.create_todo = AsyncMock(
        return_value=SimpleNamespace(id=uuid4(), text="whatever")
    )
    svc.todo_handlers.todo_service = mock
    return mock


class TestPhantomReminderEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def _ask_with_unbindable_time(self, svc, sid):
        """Turn 1: PM's reminder ask with an explicit-but-unbindable time —
        the honest clarify ask, now arming the carrier. Deterministic route:
        the pre-classifier claims 'remind me to …' (explosive LLM holds)."""
        with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
            return await svc.process_intent(
                message="remind me to review the beta notes at 25:99",
                session_id=sid,
                user_id=_USER,
            )

    async def test_clarify_ask_arms_the_time_question(self, svc):
        sid = "e2e-1648-arm"
        _mock_todo_service(svc)
        r1 = await self._ask_with_unbindable_time(svc, sid)
        assert "When should I remind you?" in r1.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
        assert stored["pending_action"]["task_text"] == "review the beta notes"

    async def test_time_answer_performs_the_real_save_with_calendar_line(self, svc):
        """PM's transcript shape, fixed: the time answer binds at the offer
        seam and the REAL save runs — the reply is the 📅 confirmation the
        genuine path prints, never an improvised 'Reminder set'."""
        sid = "e2e-1648-save"
        mock = _mock_todo_service(svc)
        await self._ask_with_unbindable_time(svc, sid)

        r2 = await svc.process_intent(
            message="at 3pm tomorrow", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_awaited_once()
        kwargs = mock.create_todo.await_args.kwargs
        assert kwargs["text"] == "review the beta notes"
        assert kwargs["reminder_date"] is not None
        assert (kwargs["reminder_date"].hour, kwargs["reminder_date"].minute) == (15, 0)
        assert "Reminder saved" in r2.message
        assert "📅" in r2.message
        assert _pending_offers(svc) == {}

    async def test_bare_at_3pm_also_saves(self, svc):
        """The verbatim live answer — bare 'at 3pm' (no date word) binds via
        the parser's next-occurrence rule and saves for real."""
        sid = "e2e-1648-save-bare"
        mock = _mock_todo_service(svc)
        await self._ask_with_unbindable_time(svc, sid)
        r2 = await svc.process_intent(
            message=PM_TIME_ANSWER, session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_awaited_once()
        assert mock.create_todo.await_args.kwargs["reminder_date"].hour == 15
        assert "Reminder saved" in r2.message
        assert "📅" in r2.message

    async def test_unrecognized_answer_reasks_and_rearms(self, svc):
        """Direction 2 on the reminder side: a turn with no parseable time
        and no command shape gets the honest re-ask — never a silent abandon,
        never a fabricated save, never the parser's tomorrow-morning default."""
        sid = "e2e-1648-reask"
        mock = _mock_todo_service(svc)
        await self._ask_with_unbindable_time(svc, sid)
        r2 = await svc.process_intent(
            message="hmm whatever works", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_not_awaited()
        assert "Nothing has been saved" in r2.message
        assert r2.intent_data.get("reminder_time_reasked") is True
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND

    async def test_still_unbindable_time_reasks_honestly(self, svc):
        """An answer whose time is explicit but unbindable re-asks (honest
        inability) and keeps the binding — never saves a guessed time."""
        sid = "e2e-1648-unbindable"
        mock = _mock_todo_service(svc)
        await self._ask_with_unbindable_time(svc, sid)
        r2 = await svc.process_intent(
            message="at 25:99", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_not_awaited()
        assert "Nothing has been saved" in r2.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND

    async def test_decline_drops_honestly(self, svc):
        sid = "e2e-1648-decline"
        mock = _mock_todo_service(svc)
        await self._ask_with_unbindable_time(svc, sid)
        r2 = await svc.process_intent(message="no", session_id=sid, user_id=_USER)
        mock.create_todo.assert_not_awaited()
        assert "Nothing was saved" in r2.message
        assert _pending_offers(svc) == {}

    async def test_full_restatement_routes_normally_with_new_task(self, svc):
        """A full restatement carries its own task AND time — it must route
        through the real handler (re-extracting both), not save the old task
        under the new time."""
        sid = "e2e-1648-restate"
        mock = _mock_todo_service(svc)
        await self._ask_with_unbindable_time(svc, sid)
        with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
            r2 = await svc.process_intent(
                message="remind me to call the vet at 3pm tomorrow",
                session_id=sid,
                user_id=_USER,
            )
        mock.create_todo.assert_awaited_once()
        assert mock.create_todo.await_args.kwargs["text"] == "call the vet"
        assert "Reminder saved" in r2.message
        assert "📅" in r2.message


# ---------------------------------------------------------------------------
# 4. The reminder_clear audit (direction 2's "look, don't assume")
# ---------------------------------------------------------------------------


class TestClearVerbQuestionHonestFallback:
    pytestmark = pytest.mark.asyncio

    def _offer(self):
        from services.intent_service.reminder_clear import (
            CLARIFY_CLEAR_VERB_WORKFLOW,
            CLEAR_VERB_QUESTION_KIND,
        )

        return {
            "workflow_type": CLARIFY_CLEAR_VERB_WORKFLOW,
            "pending_action": {
                "kind": CLEAR_VERB_QUESTION_KIND,
                "clear_verb": "clear",
                "clear_noun": "reminder",
                "clear_target_ids": ["a", "b"],
                "clear_target_texts": ["x", "y"],
                "user_id": _USER,
                "original_message": "clear my reminders",
            },
            "decline_message": "Okay — nothing has been changed.",
        }

    async def test_unrecognized_answer_reasks_and_rearms(self):
        """The same silent-abandon existed here: a non-answer non-command
        turn ('the first one') used to fall through the pop into the routing
        chain. It now re-asks honestly and re-arms."""
        from services.intent_service.reminder_clear import handle_reminder_clear_turn

        intent_service = MagicMock()
        result = await handle_reminder_clear_turn(
            self._offer(),
            "the first one",
            session_id="s-1648-rc",
            user_id=_USER,
            intent_service=intent_service,
        )
        assert result is not None
        assert "I didn't catch that as an answer" in result["message"]
        assert "nothing has been changed" in result["message"].lower()
        assert result["intent_data"].get("verb_question_reasked") is True
        intent_service.workflow_offer_service.set_pending_offer.assert_called_once()

    async def test_command_shaped_turn_still_falls_through(self):
        """The off-intent rule is untouched: a command-shaped turn returns
        None (abandons via the pop, routes normally)."""
        from services.intent_service.reminder_clear import handle_reminder_clear_turn

        intent_service = MagicMock()
        result = await handle_reminder_clear_turn(
            self._offer(),
            "list my reminders",
            session_id="s-1648-rc2",
            user_id=_USER,
            intent_service=intent_service,
        )
        assert result is None
        intent_service.workflow_offer_service.set_pending_offer.assert_not_called()

    async def test_decline_still_falls_through(self):
        from services.intent_service.reminder_clear import handle_reminder_clear_turn

        intent_service = MagicMock()
        result = await handle_reminder_clear_turn(
            self._offer(),
            "no",
            session_id="s-1648-rc3",
            user_id=_USER,
            intent_service=intent_service,
        )
        assert result is None
        intent_service.workflow_offer_service.set_pending_offer.assert_not_called()


# ---------------------------------------------------------------------------
# 5. The offer record + generic-accept landing (wiring)
# ---------------------------------------------------------------------------


class TestReminderTimeOfferWiring:
    def test_offer_record_shape(self):
        offer = build_reminder_time_offer("review the beta notes", _USER)
        assert offer["workflow_type"] == "clarify_reminder_time"
        pa = offer["pending_action"]
        assert pa["kind"] == REMINDER_TIME_QUESTION_KIND
        assert pa["task_text"] == "review the beta notes"
        assert pa["user_id"] == _USER
        assert "Nothing was saved" in offer["decline_message"]

    def test_clarify_workflow_registered_offer_seam_only(self):
        register_default_workflows()
        from services.intent_service.workflow_dispatcher import (
            get_action_workflows,
            get_registered_workflows,
        )

        registered = get_registered_workflows()
        assert "clarify_reminder_time" in registered
        # Offer-seam only: never rail-dispatchable from a classified action.
        assert "clarify_reminder_time" not in get_action_workflows()

    @pytest.mark.asyncio
    async def test_bare_yes_lands_on_reask_not_the_floor(self, svc):
        """Defense in depth: a bare 'yes' against 'when?' re-asks via the
        registered landing — it can never fall into _handle_unknown_intent
        and reach the floor."""
        sid = "e2e-1648-bare-yes"
        mock = _mock_todo_service(svc)
        with patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})):
            await svc.process_intent(
                message="remind me to review the beta notes at 25:99",
                session_id=sid,
                user_id=_USER,
            )
        r2 = await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
        mock.create_todo.assert_not_awaited()
        assert "Nothing has been saved" in r2.message
        stored = next(iter(_pending_offers(svc).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
