"""#1665 + #1664 — arm sites store their rendered ask; is_confirm derives from kind.

Two Phase-2.2 prerequisites for the LIVE SessionSnapshot (issue 1595 lane;
gate doc caveats), tested at the honest layer:

- **#1665 anti-drift pin, per arm site**: every #846 arm site stores the
  QUESTION COPY it just rendered — ``offer["question"]`` — and the pin is
  EQUALITY with (or verbatim containment in) the user-visible message of the
  SAME turn. The stored string is the already-rendered copy: each test drives
  the real arming function and compares the stored record against the
  returned message, so a site that re-renders (or drifts) fails here.

- **#1664 confirm-kind table**: ``destructive_confirm.offer_is_confirm`` is
  the ONE derivation home. True for exactly the #1650 confirm kinds
  (destructive confirms, reminder-clear delete confirms, consent checks, the
  unmapped-status close confirm, the drafted-issue FILE confirm state, the
  closed-default repo bind) and FALSE for the open repo question and the
  clear-verb question (the AC's pinned negatives — the literal 1664 defect
  was the open repo question rendering "(yes/no confirm)"). The kind-literal
  drift pins keep the derivation's string literals honest against their
  source constants (they are literals because the source modules import
  destructive_confirm — importing back would be circular).
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from services.domain.models import Intent
from services.intent_service import reminder_clear as rc
from services.intent_service.collaboration_gate import (
    build_collaboration_response,
    draft_open_question,
)
from services.intent_service.consent_gate import (
    CONSENT_CHECK_KIND,
    build_consent_check_offer,
)
from services.intent_service.destructive_confirm import (
    DESTRUCTIVE_CONFIRM_KIND,
    build_confirmation_offer,
    offer_is_confirm,
)
from services.intent_service.drafted_issue import (
    _DRAFT_RETAINED_LINE,
    _NEAR_ACCEPT_ASK,
    _POST_BIND_ASK,
    DRAFTED_ISSUE_KIND,
    build_drafted_issue_offer,
    handle_drafted_issue_turn,
)
from services.intent_service.repo_clarification import (
    REPO_QUESTION_KIND,
    build_repo_question_offer,
    handle_repo_question_turn,
    open_repo_question,
)
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.standup_preferences import (
    INVITE_AFTER_REPORT,
    INVITE_EMPTY_LEAD,
    INVITE_KIND,
    build_interview_invitation,
)
from services.intent_service.standup_todo_offer import (
    STANDUP_TODO_OFFER_KIND,
    build_overdue_todo_offer,
)
from services.intent_service.todo_handlers import (
    _TIME_REASK_TAIL,
    REMINDER_TASK_QUESTION_KIND,
    REMINDER_TIME_QUESTION_KIND,
    TodoIntentHandlers,
    build_reminder_time_offer,
    handle_reminder_time_turn,
)
from services.intent_service.verified_inference import (
    VERIFY_INFERENCE_KIND,
    build_read_back_offer,
)
from services.shared_types import EffectClass, IntentCategory

_USER = "3f7b8a52-1665-4b00-9e00-000000001665"
_SESSION = "sess-1665-rendered-ask"


def _intent(message, action="create_issue", category=IntentCategory.EXECUTION):
    return Intent(
        category=category,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )


def _fake_service(todo_service=None):
    """The slice the arm seams touch: a REAL offer store + a todo boundary."""
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(),
        todo_handlers=SimpleNamespace(todo_service=todo_service),
    )


def _stored(svc):
    offer = svc.workflow_offer_service.peek_pending_offer(_SESSION, user_id=_USER)
    assert offer is not None, "arm site stored nothing"
    return offer


def _todo(text="pay the invoice"):
    return SimpleNamespace(
        id=uuid4(),
        text=text,
        reminder_date=datetime.now(timezone.utc),
        due_date=datetime(2026, 8, 1, tzinfo=timezone.utc),
        completed=False,
    )


@pytest.fixture
def mem_prefs(monkeypatch):
    """In-memory users.preferences double at the ONE persistence seam
    (the #1510 idiom — collaboration_gate._load_preferences)."""
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        store.setdefault(str(user_id), {})[key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store


# ---------------------------------------------------------------------------
# #1665 — builder-level sites where the arm site RETURNS builder.question
# verbatim as the turn's message: stored == said is builder-internal equality.
# ---------------------------------------------------------------------------


class TestBuilderCarriedAsks:
    def test_destructive_confirm_stores_its_question(self):
        """The rail seam returns ``ConfirmationOffer.question`` as the turn's
        message; the record now carries the same string (one render)."""
        offer = build_confirmation_offer(_intent("close issue #108", "close_issue"))
        assert offer.question == "Close issue #108? (yes/no)"
        assert offer.offer["question"] == offer.question
        assert offer.offer["pending_action"]["kind"] == DESTRUCTIVE_CONFIRM_KIND

    def test_consent_check_stores_its_question(self):
        offer = build_consent_check_offer(
            _intent("update issue #108", "update_issue"), EffectClass.WRITE
        )
        assert offer.offer["question"] == offer.question
        assert "(yes/no)" in offer.question

    def test_read_back_offer_stores_its_question(self):
        rb = build_read_back_offer(_USER, "standup_mode", "report", "that you want brief standups")
        assert rb.offer["question"] == rb.question
        assert "Did I get that right? (yes/no)" in rb.question

    def test_standup_todo_offer_stores_its_question(self):
        built = build_overdue_todo_offer(_USER, _SESSION, _todo(), more_overdue=0)
        assert built.offer["question"] == built.question
        assert "Want me to mark that overdue todo done? (yes/no)" in built.question

    def test_interview_invitation_stores_caller_rendered_lead(self):
        """The two invitation surfaces render DIFFERENT leads; the caller
        passes the one it renders (INVITE_EMPTY_LEAD / INVITE_AFTER_REPORT)."""
        empty = build_interview_invitation(_USER, _SESSION, question=INVITE_EMPTY_LEAD)
        after = build_interview_invitation(_USER, _SESSION, question=INVITE_AFTER_REPORT)
        assert empty["question"] == INVITE_EMPTY_LEAD
        assert after["question"] == INVITE_AFTER_REPORT

    def test_reminder_time_offer_stores_given_question(self):
        offer = build_reminder_time_offer(
            "check the oven", _USER, question="When should I remind you?"
        )
        assert offer["question"] == "When should I remind you?"

    def test_repo_question_offer_stores_given_question(self):
        q = open_repo_question(108)
        offer = build_repo_question_offer(
            _intent("update issue #108", "update_issue"), 108, _USER, question=q
        )
        assert offer["question"] == q


# ---------------------------------------------------------------------------
# #1665 — drafted issue: the stored ask is the SAME function's output the
# response copy embeds (one source), plus the re-arm seams' state updates.
# ---------------------------------------------------------------------------


class TestDraftedIssueAsks:
    @pytest.mark.parametrize(
        "subject,body",
        [
            ("Fix login", "Steps: open the app"),  # ready to file → file confirm
            ("Fix login", None),  # body ask
            (None, "Steps: open the app"),  # title ask (#1649 partial)
            (None, None),  # "What's it about?" (#1630)
        ],
    )
    def test_open_question_is_verbatim_substring_of_response(self, subject, body):
        """The anti-drift pin at the source: the stored ask (draft_open_question)
        appears VERBATIM in build_collaboration_response for every state —
        they share one function, so this pins the sharing."""
        question = draft_open_question(subject, body, draft_bound=True)
        message = build_collaboration_response(
            subject=subject, repository=None, draft_bound=True, body=body
        )
        assert question in message

    def test_builder_stores_the_open_question(self):
        question = draft_open_question("Fix login", None)
        offer = build_drafted_issue_offer(
            _intent("help me write a ticket about login"),
            "Fix login",
            question=question,
        )
        assert offer["question"] == question

    async def test_body_bind_rearms_with_post_bind_ask(self):
        """#1627 bind turn: the reply closes with _POST_BIND_ASK and the
        re-armed record's question IS that string."""
        svc = _fake_service()
        offer = build_drafted_issue_offer(
            _intent("help me write a ticket"),
            None,
            question=draft_open_question(None, None),
        )
        prose = (
            "Add a guard so that deleting a project always asks for explicit "
            "confirmation before anything is removed, because right now a "
            "single ambiguous phrase can trigger a destructive operation."
        )
        result = await handle_drafted_issue_turn(
            offer, prose, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert result is not None
        assert _POST_BIND_ASK in result["message"]
        assert _stored(svc)["question"] == _POST_BIND_ASK

    async def test_near_accept_rearms_with_its_reask(self):
        """#1650 near-accept ("sure, whatever you think"): neither files nor
        drops — the re-ask copy is stored on the re-armed record."""
        svc = _fake_service()
        offer = build_drafted_issue_offer(
            _intent("help me write a ticket about login"),
            "Fix login",
            question=draft_open_question("Fix login", None),
        )
        result = await handle_drafted_issue_turn(
            offer,
            "sure, whatever you think",
            session_id=_SESSION,
            user_id=_USER,
            intent_service=svc,
        )
        assert result is not None
        assert _NEAR_ACCEPT_ASK in result["message"]
        assert _stored(svc)["question"] == _NEAR_ACCEPT_ASK

    async def test_file_near_miss_rearms_with_its_moves(self):
        """#1648 near-miss ("file the sucker"): the re-ask names the moves —
        and the stored question is exactly the moves line the reply contains."""
        svc = _fake_service()
        offer = build_drafted_issue_offer(
            _intent("help me write a ticket about login"),
            "Fix login",
            question=draft_open_question("Fix login", None),
        )
        result = await handle_drafted_issue_turn(
            offer,
            "file the sucker",
            session_id=_SESSION,
            user_id=_USER,
            intent_service=svc,
        )
        assert result is not None
        stored_q = _stored(svc)["question"]
        assert stored_q in result["message"]
        assert 'Say "file it as is" to file it' in stored_q

    def test_retained_line_constant_matches_rearm_question(self):
        """The failure-retention re-arm stores _DRAFT_RETAINED_LINE — pin the
        constant's phrasing (the copy the retention replies embed)."""
        assert _DRAFT_RETAINED_LINE == (
            'Your draft is still here — say "file it" to try again, ' 'or "no" to drop it.'
        )


# ---------------------------------------------------------------------------
# #1665 — reminder-clear: every variant's arm stores the exact rendered ask.
# Driven through the REAL maybe_handle_clear_family / turn handlers, with the
# prefs seam double and a fake todo boundary.
# ---------------------------------------------------------------------------


class _FakeTodoService:
    def __init__(self, todos):
        self._todos = todos
        self.completed = []

    async def list_todos(self, user_id, include_completed=False):
        return list(self._todos)

    async def complete_todo(self, todo_id, user_id):
        self.completed.append(todo_id)
        return True


async def _run_clear(svc, message="clear my reminders", effect=EffectClass.WRITE):
    return await rc.maybe_handle_clear_family(
        svc,
        _intent(message, "complete_todo"),
        _SESSION,
        _USER,
        UUID(_USER),
        effect,
    )


class TestReminderClearAsks:
    async def test_variant_one_arm_stores_the_ratified_ask(self, mem_prefs):
        svc = _fake_service(_FakeTodoService([_todo()]))
        result = await _run_clear(svc)
        assert result.message == rc.variant_one_question("clear", "reminder")
        assert _stored(svc)["question"] == result.message

    async def test_variant_three_arm_stores_the_confirm_ask(self, mem_prefs):
        from services.intent_service.verified_inference import (
            VERIFIED_INFERENCES_PREF_KEY,
        )

        mem_prefs[_USER][VERIFIED_INFERENCES_PREF_KEY] = {
            rc.inference_key("clear"): {"value": "delete", "source": "user_verified"}
        }
        svc = _fake_service(_FakeTodoService([_todo()]))
        result = await _run_clear(svc)
        assert result.message == rc.variant_three_question(1, "clear", "reminder")
        assert _stored(svc)["question"] == result.message

    async def test_always_ask_arm_stores_the_leading_question(self, mem_prefs):
        from services.intent_service.verified_inference import (
            VERIFICATION_META_PREF_KEY,
            VERIFIED_INFERENCES_PREF_KEY,
        )

        mem_prefs[_USER][VERIFIED_INFERENCES_PREF_KEY] = {
            rc.inference_key("clear"): {"value": "complete", "source": "user_verified"}
        }
        mem_prefs[_USER][VERIFICATION_META_PREF_KEY] = {"mode": "always_ask"}
        svc = _fake_service(_FakeTodoService([_todo()]))
        result = await _run_clear(svc)
        assert result.message == rc.variant_two_always_ask_question()
        assert _stored(svc)["question"] == result.message

    async def test_correction_window_stores_the_standing_invitation(self, mem_prefs):
        """Variant-2 auto-apply arms the correction window; its open question
        is CORRECTION_WINDOW_ASK — the exact sentence the disclosure renders."""
        from services.intent_service.verified_inference import (
            VERIFIED_INFERENCES_PREF_KEY,
        )

        mem_prefs[_USER][VERIFIED_INFERENCES_PREF_KEY] = {
            rc.inference_key("clear"): {"value": "complete", "source": "user_verified"}
        }
        svc = _fake_service(_FakeTodoService([_todo()]))
        result = await _run_clear(svc)
        assert rc.CORRECTION_WINDOW_ASK in result.message
        assert _stored(svc)["question"] == rc.CORRECTION_WINDOW_ASK

    def test_correction_window_ask_is_the_disclosure_sentence(self):
        """Drift guard: the ratified variant-2 disclosure ends with the same
        sentence the correction offer stores (one meaning, two surfaces)."""
        assert rc.CORRECTION_WINDOW_ASK in rc.variant_two_disclosure("clear")

    async def test_correction_claim_arms_delete_confirm_with_its_ask(self):
        todo = _todo()
        svc = _fake_service(_FakeTodoService([todo]))
        result = await rc.handle_reminder_clear_turn(
            {
                "workflow_type": rc.CLEAR_CORRECTION_WORKFLOW,
                "pending_action": {
                    "kind": rc.CLEAR_CORRECTION_KIND,
                    "user_id": _USER,
                    "clear_verb": "clear",
                    "clear_noun": "reminder",
                    "clear_target_ids": [str(todo.id)],
                    "clear_target_texts": [todo.text],
                },
            },
            "I meant delete",
            _SESSION,
            _USER,
            svc,
        )
        assert result is not None
        assert result["message"] == "Got it — delete this reminder instead? (yes/no)"
        assert _stored(svc)["question"] == result["message"]

    async def test_unrecognized_answer_rearm_stores_the_reask(self):
        todo = _todo()
        svc = _fake_service(_FakeTodoService([todo]))
        result = await rc.handle_reminder_clear_turn(
            {
                "workflow_type": rc.CLARIFY_CLEAR_VERB_WORKFLOW,
                "pending_action": {
                    "kind": rc.CLEAR_VERB_QUESTION_KIND,
                    "user_id": _USER,
                    "clear_verb": "clear",
                    "clear_noun": "reminder",
                    "clear_target_ids": [str(todo.id)],
                    "clear_target_texts": [todo.text],
                },
            },
            "the blue one perhaps",
            _SESSION,
            _USER,
            svc,
        )
        assert result is not None
        stored_q = _stored(svc)["question"]
        assert stored_q == "For these reminders: mark them done, or delete them?"
        assert stored_q in result["message"]


# ---------------------------------------------------------------------------
# #1665 — reminder time question (#1648 carrier): the honest asks + re-asks.
# ---------------------------------------------------------------------------


class TestReminderTimeAsks:
    async def test_unbindable_time_arm_stores_the_when_ask(self):
        svc = _fake_service()
        handlers = TodoIntentHandlers()
        message = await handlers.handle_create_reminder(
            _intent("remind me to check the oven at 25:99", "create_reminder"),
            _SESSION,
            UUID(_USER),
            intent_service=svc,
        )
        stored_q = _stored(svc)["question"]
        assert stored_q == (
            "When should I remind you? " "(For example: 'at 3pm tomorrow' or 'in 2 hours'.)"
        )
        assert stored_q in message
        assert _stored(svc)["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND

    async def test_reask_rearm_stores_the_reask_tail(self):
        svc = _fake_service()
        offer = build_reminder_time_offer(
            "check the oven", _USER, question="When should I remind you?"
        )
        result = await handle_reminder_time_turn(
            offer,
            "banana banana",
            session_id=_SESSION,
            user_id=_USER,
            intent_service=svc,
        )
        assert result is not None
        assert _TIME_REASK_TAIL in result["message"]
        assert _stored(svc)["question"] == _TIME_REASK_TAIL


# ---------------------------------------------------------------------------
# #1665 — repo question: the re-ask seam stores the exact per-status copy.
# ---------------------------------------------------------------------------


class TestRepoQuestionAsks:
    async def test_name_unresolved_rearm_stores_the_exact_copy(self, monkeypatch):
        from services.intent_service import repo_clarification as rq

        async def _not_found(user_id, name):
            return rq.RepoNameResolution(status="not_found")

        monkeypatch.setattr(rq, "resolve_repo_name", _not_found)
        svc = _fake_service()
        offer = build_repo_question_offer(
            _intent("change the title of issue 108", "update_issue"),
            108,
            _USER,
            question=open_repo_question(108),
        )
        result = await handle_repo_question_turn(
            offer,
            "banana",
            session_id=_SESSION,
            user_id=_USER,
            intent_service=svc,
        )
        assert result is not None
        assert _stored(svc)["question"] == result["message"]
        assert "couldn't find one called 'banana'" in result["message"]


# ---------------------------------------------------------------------------
# #1665 — the IntentService-hosted arm sites, driven through the REAL methods
# (the LLM boundary stays explosive: none of these turns may consult it).
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def live_service():
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier

    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


class TestIntentServiceArmSites:
    async def test_open_repo_question_arm_stores_what_it_says(self, live_service):
        result = await live_service._ask_for_repository(
            _intent("change the title of issue 108", "update_issue"),
            108,
            _SESSION,
            _USER,
        )
        assert result is not None
        stored = live_service.workflow_offer_service.peek_pending_offer(_SESSION)
        assert stored["question"] == result.message == open_repo_question(108)
        assert offer_is_confirm(stored) is False  # AC pin: open repo question

    async def test_closed_default_repo_arm_stores_what_it_says(self, live_service, monkeypatch):
        from services.integrations.github import repo_resolver
        from services.intent_service.repo_clarification import (
            RepoNameResolution,
            repo_resolution_question,
        )

        async def _default(uid):
            return "mediajunkie/test-piper-morgan"

        monkeypatch.setattr(repo_resolver, "get_user_default_repo", _default)
        resolution = RepoNameResolution(status="not_found")
        result = await live_service._ask_for_repository(
            _intent("change the title of issue 108", "update_issue"),
            108,
            _SESSION,
            _USER,
            asked_name="banana",
            resolution=resolution,
        )
        assert result is not None
        expected = repo_resolution_question("banana", resolution, "mediajunkie/test-piper-morgan")
        stored = live_service.workflow_offer_service.peek_pending_offer(_SESSION)
        assert stored["question"] == result.message == expected
        assert "say 'yes' to use your default" in expected
        assert offer_is_confirm(stored) is True  # closed-default bind

    async def test_unmapped_status_value_arm_stores_what_it_says(self, live_service):
        result = live_service._offer_status_close_clarification(
            _intent("change the status of issue #108 to Done", "update_issue"),
            "change the status of issue #108 to Done",
            108,
            _SESSION,
            _USER,
        )
        assert result is not None
        stored = live_service.workflow_offer_service.peek_pending_offer(_SESSION)
        assert stored["question"] == result.message
        assert result.message == ("By 'Done' do you mean close issue #108? (yes/no)")
        assert offer_is_confirm(stored) is True

    async def test_collaborate_arm_stores_the_per_state_ask(self, live_service, mem_prefs):
        """The #1571/#1630 collaborate turn: the armed record's question is
        draft_open_question's output, verbatim inside the rendered reply."""
        result = await live_service._handle_create_issue(
            _intent("help me write a ticket", "create_issue"),
            None,
            _SESSION,
            _USER,
        )
        assert result.intent_data.get("collaboration_gate") is True
        stored = live_service.workflow_offer_service.peek_pending_offer(_SESSION)
        assert stored["question"] == draft_open_question(None, None, draft_bound=True)
        assert stored["question"] in result.message
        assert offer_is_confirm(stored) is False  # mid-compose, not a yes/no


# ---------------------------------------------------------------------------
# #1665 — assembly reads the stored ask (extending the 1595 per-field tests).
# ---------------------------------------------------------------------------


class TestAssemblyPicksUpStoredAsk:
    async def test_snapshot_carries_the_arm_sites_rendered_copy(self, mem_prefs):
        from services.intent_service.snapshot_assembly import (
            assemble_session_snapshot,
        )

        svc = _fake_service(_FakeTodoService([_todo()]))
        result = await _run_clear(svc)
        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.pending_offer_question == result.message
        assert snap.pending_offer_kind == rc.CLEAR_VERB_QUESTION_KIND
        assert snap.pending_offer_is_confirm is False  # AC pin: verb question


# ---------------------------------------------------------------------------
# #1664 — is_confirm derives from the offer KIND (one home; #1650's table).
# ---------------------------------------------------------------------------


class TestIsConfirmKindTable:
    def test_destructive_confirm_true(self):
        offer = build_confirmation_offer(_intent("close issue #108", "close_issue")).offer
        assert offer_is_confirm(offer) is True

    def test_delete_confirm_true(self):
        offer = rc._delete_confirmation_offer(
            _USER, "clear", "reminder", [str(uuid4())], ["x"], "clear my reminders"
        )
        assert offer_is_confirm(offer) is True

    def test_consent_check_true(self):
        offer = build_consent_check_offer(
            _intent("update issue #108", "update_issue"), EffectClass.WRITE
        ).offer
        assert offer_is_confirm(offer) is True

    def test_unmapped_status_value_close_confirm_true(self):
        """The #1411 clarify-first ask is a destructive close confirm by
        another name — its copy is literally '...? (yes/no)'."""
        offer = {
            "workflow_type": "confirm_pending_action",
            "pending_action": {"kind": "unmapped_field_value_clarification"},
        }
        assert offer_is_confirm(offer) is True

    def test_open_repo_question_false_the_1664_defect(self):
        """THE pinned negative: the open which-repo ask rides the confirm
        carrier but is NOT a yes/no — 1664's literal defect was rendering
        '(yes/no confirm)' on it."""
        offer = build_repo_question_offer(
            _intent("change the title of issue 108", "update_issue"),
            108,
            _USER,
            question=open_repo_question(108),
        )
        assert offer["workflow_type"] == "confirm_pending_action"  # the trap
        assert offer_is_confirm(offer) is False

    def test_closed_default_repo_bind_true(self):
        """With a default on offer, a crisp 'yes' binds it and FIRES the held
        update (#1650) — that state IS a confirm."""
        offer = build_repo_question_offer(
            _intent("change the title of issue 108", "update_issue"),
            108,
            _USER,
            asked_name="banana",
            default_repo="mediajunkie/test-piper-morgan",
        )
        assert offer_is_confirm(offer) is True

    def test_verb_question_false_pinned(self):
        """THE other pinned negative: the either/or verb question is not a
        yes/no (a bare 'yes' re-asks; it never fires)."""
        offer = rc._verb_question_offer(
            _USER,
            "clear",
            "reminder",
            [],
            [],
            "clear my reminders",
            question=rc.variant_one_question(),
        )
        assert offer_is_confirm(offer) is False

    def test_correction_window_false(self):
        offer = rc._correction_offer(_USER, "clear", "reminder", [], [], "clear my reminders")
        assert offer_is_confirm(offer) is False

    def test_drafted_issue_mid_compose_false_ready_to_file_true(self):
        mid = build_drafted_issue_offer(_intent("help me write a ticket"), "Fix login")
        ready = build_drafted_issue_offer(
            _intent("help me write a ticket"), "Fix login", body="Steps: open the app"
        )
        assert offer_is_confirm(mid) is False
        assert offer_is_confirm(ready) is True

    def test_generic_yes_no_offers_stay_false(self):
        """The standup todo offer / invitation / read-back phrase a yes-no but
        take the GENERIC detector, not the #1650 strict one — is_confirm's
        contract comment ('rides the strict #1650 detector if True') keeps
        them out of the set."""
        todo_offer = build_overdue_todo_offer(_USER, _SESSION, _todo()).offer
        invite = build_interview_invitation(_USER, _SESSION, question=INVITE_EMPTY_LEAD)
        rb = build_read_back_offer(_USER, "standup_mode", "report", "desc").offer
        assert offer_is_confirm(todo_offer) is False
        assert offer_is_confirm(invite) is False
        assert offer_is_confirm(rb) is False

    def test_no_offer_and_kindless_carrier_fallback(self):
        assert offer_is_confirm(None) is False
        assert offer_is_confirm({}) is False
        # Documented fallback: a kindless carrier record (the pre-1664
        # destructive builder's shape) still reads as a confirm.
        legacy = {
            "workflow_type": "confirm_pending_action",
            "pending_action": {"action": "close_issue", "summary": "close issue #108"},
        }
        assert offer_is_confirm(legacy) is True


class TestKindLiteralDriftPins:
    """The derivation's literals must equal their source constants — the
    modules can't import each other (circularity), so THIS is the guard."""

    def test_literals_match_source_constants(self):
        from services.intent_service import destructive_confirm as dc

        assert rc.CLEAR_DELETE_CONFIRMATION_KIND in dc._CONFIRM_KINDS
        assert CONSENT_CHECK_KIND in dc._CONFIRM_KINDS
        assert DESTRUCTIVE_CONFIRM_KIND in dc._CONFIRM_KINDS
        assert "unmapped_field_value_clarification" in dc._CONFIRM_KINDS
        assert dc._DRAFTED_ISSUE_KIND == DRAFTED_ISSUE_KIND
        assert dc._REPO_QUESTION_KIND == REPO_QUESTION_KIND
        # The pinned negatives are NOT in the always-confirm set.
        assert rc.CLEAR_VERB_QUESTION_KIND not in dc._CONFIRM_KINDS
        assert rc.CLEAR_CORRECTION_KIND not in dc._CONFIRM_KINDS
        assert REMINDER_TIME_QUESTION_KIND not in dc._CONFIRM_KINDS
        assert REMINDER_TASK_QUESTION_KIND not in dc._CONFIRM_KINDS  # #1654
        assert STANDUP_TODO_OFFER_KIND not in dc._CONFIRM_KINDS
        assert INVITE_KIND not in dc._CONFIRM_KINDS
        assert VERIFY_INFERENCE_KIND not in dc._CONFIRM_KINDS

    def test_unmapped_kind_literal_matches_arm_site(self):
        """The intent_service arm site writes its kind as a literal too —
        grep-level pin so a rename there breaks here."""
        import inspect

        from services.intent import intent_service as isvc

        src = inspect.getsource(isvc.IntentService._offer_status_close_clarification)
        assert '"unmapped_field_value_clarification"' in src
