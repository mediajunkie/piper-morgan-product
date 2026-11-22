"""#2413: "show me the todos in the Launch project" asks which project, then shows it.

Arch 2026-11-22 (01M82907VE, 01M82A8RX0), CXO (01M829VZ5X, 01M82AGXFK), PPM
(01M82986YX). The classifier's ``list_project_todos`` / ``list_todos_by_project``
land on one router-hidden READ entry. No model supplies a project on these turns, so
the handler asks (armed, every active project bound) and never reads a name from the
person's words; the answer turn shows 2301's block. Nothing is ever written.

LAYER: the entry point, the answer turn and the re-ask landing through their own
functions, with the project read and the todo service replaced at one seam each; the
pop seam and the generic decline/accept through the real ``process_intent`` with the
classification stubbed. The router's and the classifier's requests pinned by sha256.
No router call, no model call, no database.
DENOMINATOR: first turn (1 project, 6 projects, none, a failed read, cannot arm, no
principal) for both names; the binding; the answer (exact, other case, trailing
"project", unmatched, decline, bare yes, several then a number, gone, failed todo
read, failed project re-check, principal mismatch, a foreign kind); nothing written in
any case; no "added" wording; the registry, the grammar and both request pins.
"""

import ast
import hashlib
import json
import types
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from sqlalchemy.exc import OperationalError

from services.domain.models import Intent
from services.intent_service import project_status_todos as pst
from services.intent_service import project_todos_read as ptr
from services.intent_service import todo_project_attach as attach
from services.intent_service import workflow_entries
from services.intent_service.todo_handlers import TodoIntentHandlers
from services.shared_types import IntentCategory

REPO = Path(__file__).resolve().parents[4]
USER = "24130000-0000-4000-8000-000000002413"
OTHER = "24139999-0000-4000-8000-000000002413"
ASK_1 = "show me the todos in the Launch project"
ASK_2 = "which todos are under Website Refresh?"
BOTH = list(ptr.CLASSIFIER_ACTION_NAMES)


def _project(pid, name, created=None):
    return types.SimpleNamespace(id=pid, name=name, created_at=created)


def _todo(tid, text, priority="medium"):
    return types.SimpleNamespace(
        id=tid, text=text, priority=priority, completed=False, status="pending"
    )


def _handlers(by_project=None, fail=None):
    """The real 2301 render with the todo service stubbed. Every write the todo
    handlers could make is an AsyncMock, so a test can assert none was called."""
    h = TodoIntentHandlers.__new__(TodoIntentHandlers)
    reads = []

    async def list_todos(**kwargs):
        reads.append(kwargs)
        if fail is not None:
            raise fail
        return (by_project or {}).get(kwargs.get("project_id"), [])

    h.todo_service = MagicMock()
    h.todo_service.list_todos = AsyncMock(side_effect=list_todos)
    h._remember_todo_list_lines = MagicMock()
    h.create_titles_in_project = AsyncMock()
    h.create_titles_without_project = AsyncMock()
    h._reads = reads
    return h


def _assert_nothing_written(h):
    for name in ("create_todo", "update_todo", "delete_todo", "complete_todo"):
        getattr(h.todo_service, name).assert_not_called()
    h.create_titles_in_project.assert_not_called()
    h.create_titles_without_project.assert_not_called()


def _service(handlers=None, store=True):
    svc = types.SimpleNamespace(todo_handlers=handlers or _handlers())
    if store:
        svc.workflow_offer_service = MagicMock()
    return svc


def _intent(action, message=ASK_1):
    return Intent(
        original_message=message,
        category=IntentCategory.QUERY,
        action=action,
        confidence=0.9,
        context={"original_message": message},
    )


@pytest.fixture
def projects(monkeypatch):
    """The person's active projects by user id: the one seam for the project read."""
    table = {USER: []}

    async def _active(user_id):
        rows = table.get(str(user_id), [])
        if isinstance(rows, Exception):
            raise rows
        return list(rows)

    monkeypatch.setattr(attach, "_active_projects", _active)
    return table


async def _first(action, svc, user=USER, session="s1", message=ASK_1):
    return await ptr.run_list_project_todos_workflow(
        session, user, {"intent": _intent(action, message), "intent_service": svc}
    )


def _armed(svc):
    """The record armed on the (mocked) store, or None."""
    calls = svc.workflow_offer_service.set_pending_offer.call_args_list
    return calls[-1].args[1] if calls else None


async def _answer(record, text, svc, user=USER, session="s1"):
    return await ptr.handle_project_todos_pick_turn(
        record, text, session_id=session, user_id=user, intent_service=svc
    )


# -- the first turn -----------------------------------------------------------------


class TestFirstTurn:
    @pytest.mark.parametrize("action", BOTH)
    async def test_one_project_asks_and_arms(self, projects, action):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service()
        result = await _first(action, svc)
        assert result.message == (
            "Which project's todos do you want? Your projects: Launch. "
            "Tell me the name and I'll show them."
        )
        assert result.requires_clarification is True
        assert result.intent_data[ptr.PICK_PENDING_FLAG] is True
        record = _armed(svc)
        assert record["question"] == result.message
        assert record["pending_action"]["kind"] == ptr.PROJECT_TODOS_PICK_KIND
        assert record["pending_action"]["answer"] == attach.ANSWER_NAME
        assert record["pending_action"]["user_id"] == USER
        assert record["decline_message"] == "Okay, I haven't shown any todos."
        _assert_nothing_written(svc.todo_handlers)
        assert svc.todo_handlers._reads == []

    @pytest.mark.parametrize("action", BOTH)
    async def test_six_projects_list_five_and_bind_all_six(self, projects, action):
        names = ["Launch", "Website Refresh", "Mobile Redesign", "Hiring", "Budget", "Offsite"]
        projects[USER] = [_project(f"p{i}", n) for i, n in enumerate(names, 1)]
        svc = _service()
        result = await _first(action, svc)
        assert result.message == (
            "Which project's todos do you want? Your projects: Launch, Website Refresh, "
            "Mobile Redesign, Hiring, Budget, and 1 more. Tell me the name and I'll show them."
        )
        payload = _armed(svc)["pending_action"]
        assert payload["pick_ids"] == ["p1", "p2", "p3", "p4", "p5", "p6"]
        assert payload["pick_names"] == names
        _assert_nothing_written(svc.todo_handlers)

    @pytest.mark.parametrize("action", BOTH)
    async def test_no_projects_says_so_and_arms_nothing(self, projects, action):
        svc = _service()
        result = await _first(action, svc)
        assert result.message == (
            "I don't see any projects on your account, so there are no project todos to show."
        )
        assert result.requires_clarification is False
        svc.workflow_offer_service.set_pending_offer.assert_not_called()
        _assert_nothing_written(svc.todo_handlers)

    @pytest.mark.parametrize("action", BOTH)
    @pytest.mark.parametrize("raised", [OperationalError("x", {}, Exception()), OSError("down")])
    async def test_a_failed_project_read_says_so_and_nothing_else(self, projects, action, raised):
        projects[USER] = raised
        svc = _service()
        result = await _first(action, svc)
        assert result.message == "I couldn't check your projects just now."
        svc.workflow_offer_service.set_pending_offer.assert_not_called()
        _assert_nothing_written(svc.todo_handlers)

    @pytest.mark.parametrize("action", BOTH)
    async def test_no_store_shows_no_question(self, projects, action):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service(store=False)
        result = await _first(action, svc)
        assert result.message == ptr.NOT_ARMED_LINE
        assert "Which project" not in result.message
        assert result.requires_clarification is False
        _assert_nothing_written(svc.todo_handlers)

    @pytest.mark.parametrize("action", BOTH)
    async def test_no_session_shows_no_question(self, projects, action):
        projects[USER] = [_project("p1", "Launch")]
        svc = _service()
        result = await _first(action, svc, session=None)
        assert result.message == ptr.NOT_ARMED_LINE
        svc.workflow_offer_service.set_pending_offer.assert_not_called()

    async def test_no_principal_reads_nothing(self, monkeypatch):
        monkeypatch.setattr(attach, "_active_projects", AsyncMock(side_effect=AssertionError))
        result = await _first(BOTH[0], _service(), user=None)
        assert result.success is False
        assert result.error_type == "AuthenticationRequired"

    async def test_the_message_is_never_read_for_a_name(self, projects):
        """The words name "Launch", and a project called Launch exists: it still asks,
        exactly as for a message that names nothing."""
        projects[USER] = [_project("p1", "Launch"), _project("p2", "Website Refresh")]
        named, plain = _service(), _service()
        a = await _first(BOTH[0], named, message=ASK_1)
        b = await _first(BOTH[0], plain, message="show me project todos")
        assert a.message == b.message
        assert _armed(named) == _armed(plain)
        assert named.todo_handlers._reads == []


# -- the answer turn ----------------------------------------------------------------


async def _asked(projects, rows, svc=None):
    projects[USER] = rows
    svc = svc or _service(_handlers({"p1": [_todo("a", "book the venue")]}))
    await _first(BOTH[0], svc)
    return svc, _armed(svc)


class TestAnswer:
    @pytest.mark.parametrize("text", ["Launch", "launch", "LAUNCH", "Launch project", "Launch."])
    async def test_a_listed_name_shows_its_todos(self, projects, text):
        svc, record = await _asked(projects, [_project("p1", "Launch"), _project("p2", "Hiring")])
        turn = await _answer(record, text, svc)
        assert turn["message"] == "Open todos in Launch:\n1. book the venue"
        assert svc.todo_handlers._reads[0]["project_id"] == "p1"
        svc.todo_handlers._remember_todo_list_lines.assert_called_once()
        _assert_nothing_written(svc.todo_handlers)

    async def test_the_header_names_the_stored_project(self, projects):
        svc, record = await _asked(projects, [_project("p1", "Launch")])
        turn = await _answer(record, "LAUNCH project", svc)
        assert turn["message"].startswith("Open todos in Launch:")

    async def test_a_project_with_no_open_todos_names_the_stored_project(self, projects):
        """CXO 01M82H9S53: standing alone, "it" would point at nothing."""
        svc, record = await _asked(projects, [_project("p1", "Launch"), _project("p2", "Hiring")])
        turn = await _answer(record, "Hiring", svc)
        assert turn["message"] == "Hiring has no open todos."

    @pytest.mark.parametrize("text", ["Laun", "the Launch", "Launch stuff", "something else"])
    async def test_an_unmatched_answer_is_none_and_nothing_is_shown(self, projects, text):
        svc, record = await _asked(projects, [_project("p1", "Launch")])
        assert await _answer(record, text, svc) is None
        assert svc.todo_handlers._reads == []

    @pytest.mark.parametrize("text", ["no", "nope", "yes", "sure"])
    async def test_decline_and_bare_yes_are_left_to_the_generic_seam(self, projects, text):
        svc, record = await _asked(projects, [_project("p1", "Launch")])
        assert await _answer(record, text, svc) is None
        assert svc.todo_handlers._reads == []

    async def test_a_project_named_no_is_not_reached_by_no(self, projects):
        svc, record = await _asked(projects, [_project("p1", "No")])
        assert await _answer(record, "no", svc) is None

    async def test_two_projects_sharing_the_name_ask_by_number_then_show_one(self, projects):
        rows = [
            _project("p1", "Launch", datetime(2026, 11, 3)),
            _project("p2", "launch", datetime(2026, 11, 5)),
            _project("p3", "Hiring"),
        ]
        svc = _service(_handlers({"p2": [_todo("b", "print the badges")]}))
        svc, record = await _asked(projects, rows, svc)
        turn = await _answer(record, "launch", svc)
        assert turn["message"] == (
            "I found more than one project that could be the one you mean: "
            "1. Launch (created 3 Nov) 2. launch (created 5 Nov). "
            "Which one's todos do you want? Say the number."
        )
        assert turn["requires_clarification"] is True
        numbered = _armed(svc)
        assert numbered["pending_action"]["answer"] == attach.ANSWER_NUMBER
        assert numbered["pending_action"]["pick_ids"] == ["p1", "p2"]
        assert numbered["decline_message"] == ptr.DECLINE_LINE
        assert svc.todo_handlers._reads == []
        shown = await _answer(numbered, "2", svc)
        assert shown["message"] == "Open todos in launch:\n1. print the badges"
        assert svc.todo_handlers._reads[0]["project_id"] == "p2"
        _assert_nothing_written(svc.todo_handlers)

    @pytest.mark.parametrize("text", ["3", "the second one please now", "Launch"])
    async def test_the_numbered_question_takes_only_a_short_in_range_number(self, projects, text):
        rows = [_project("p1", "Launch"), _project("p2", "launch")]
        svc, record = await _asked(projects, rows)
        numbered_turn = await _answer(record, "Launch", svc)
        assert numbered_turn["requires_clarification"] is True
        assert await _answer(_armed(svc), text, svc) is None

    async def test_the_numbered_question_unarmed_shows_no_question(self, projects):
        rows = [_project("p1", "Launch"), _project("p2", "launch")]
        svc, record = await _asked(projects, rows)
        turn = await _answer(record, "Launch", _service(svc.todo_handlers, store=False))
        assert turn["message"] == ptr.NOT_ARMED_LINE

    async def test_a_project_gone_at_answer_time(self, projects):
        svc, record = await _asked(projects, [_project("p1", "Launch")])
        projects[USER] = []
        turn = await _answer(record, "Launch", svc)
        assert turn["message"] == (
            "I couldn't find that project anymore, so I haven't shown any todos."
        )
        assert svc.todo_handlers._reads == []

    async def test_a_failed_project_recheck_says_the_read_failed(self, projects):
        svc, record = await _asked(projects, [_project("p1", "Launch")])
        projects[USER] = OSError("down")
        turn = await _answer(record, "Launch", svc)
        assert turn["message"] == ptr.PROJECTS_READ_FAILED_LINE

    @pytest.mark.parametrize("raised", [OperationalError("x", {}, Exception()), RuntimeError("x")])
    async def test_a_failed_todo_read_says_2301s_line(self, projects, raised):
        svc = _service(_handlers(fail=raised))
        svc, record = await _asked(projects, [_project("p1", "Launch")], svc)
        turn = await _answer(record, "Launch", svc)
        assert (
            turn["message"] == pst.TODOS_READ_FAILED_LINE == "I couldn't check its todos just now."
        )

    async def test_a_principal_mismatch_shows_nothing(self, projects):
        svc, record = await _asked(projects, [_project("p1", "Launch")])
        turn = await _answer(record, "Launch", svc, user=OTHER)
        assert turn["message"] == attach.PRINCIPAL_MISMATCH_LINE
        assert turn["intent_data"]["principal_mismatch"] is True
        assert svc.todo_handlers._reads == []

    async def test_a_foreign_record_kind_is_ignored(self, projects):
        svc, record = await _asked(projects, [_project("p1", "Launch")])
        foreign = {**record, "pending_action": {**record["pending_action"], "kind": "x"}}
        assert await _answer(foreign, "Launch", svc) is None
        twentynine = {"pending_action": {"kind": attach.TODO_PROJECT_PICK_KIND}}
        assert await _answer(twentynine, "Launch", svc) is None


class TestReAsk:
    async def test_the_landing_reasks_the_same_text_and_rearms(self, projects):
        names = ["Launch", "Website Refresh", "Mobile Redesign", "Hiring", "Budget", "Offsite"]
        svc, record = await _asked(projects, [_project(f"p{i}", n) for i, n in enumerate(names)])
        again = await ptr.run_clarify_project_todos_pick_workflow(
            "s1",
            USER,
            {"pending_action": record["pending_action"], "intent_service": svc},
        )
        assert again["message"] == record["question"]
        assert again["requires_clarification"] is True
        rearmed = _armed(svc)
        assert rearmed["pending_action"] == record["pending_action"]
        assert rearmed["decline_message"] == ptr.DECLINE_LINE
        _assert_nothing_written(svc.todo_handlers)

    async def test_the_landing_refuses_a_foreign_payload(self):
        svc = _service()
        out = await ptr.run_clarify_project_todos_pick_workflow(
            "s1", USER, {"pending_action": {"kind": "x"}, "intent_service": svc}
        )
        assert out is None
        svc.workflow_offer_service.set_pending_offer.assert_not_called()


class TestWording:
    def test_no_string_in_the_module_says_added(self):
        tree = ast.parse((REPO / "services/intent_service/project_todos_read.py").read_text())
        strings = [
            n.value
            for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
        ]
        assert strings
        assert not [s for s in strings if "added" in s.lower()]

    def test_the_provisional_lines(self):
        assert ptr.DECLINE_LINE == "Okay, I haven't shown any todos."
        assert ptr.NOT_ARMED_LINE == (
            "I can't ask which project you mean right now, so I haven't shown any todos."
        )
        assert ptr.PROJECT_GONE_READ_LINE == (
            "I couldn't find that project anymore, so I haven't shown any todos."
        )
        assert ptr.NO_OPEN_TODOS_STANDALONE_LINE == "{project} has no open todos."


# -- through process_intent: the pop seam and the generic seam ----------------------


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service(monkeypatch):
    from unittest.mock import patch

    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier

    workflow_entries.register_default_workflows()
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            svc = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))
    svc.todo_handlers = _handlers({"p1": [_todo("a", "book the venue")]})
    return svc


def _classify_as(monkeypatch, service, category, action):
    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        intent = Intent(
            category=category,
            action=action,
            original_message=msg,
            confidence=0.95,
            context={"original_message": msg},
        )
        return types.SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)


async def _turn(service, monkeypatch, sid, message, action, category=IntentCategory.QUERY):
    _classify_as(monkeypatch, service, category, action)
    return await service.process_intent(message=message, session_id=sid, user_id=USER)


class TestThroughProcessIntent:
    @pytest.mark.parametrize("action,ask", [(BOTH[0], ASK_1), (BOTH[1], ASK_2)])
    async def test_ask_then_name_shows_the_todos(self, projects, service, monkeypatch, action, ask):
        projects[USER] = [_project("p1", "Launch"), _project("p2", "Website Refresh")]
        sid = f"ptr-{uuid4().hex[:8]}"
        first = await _turn(service, monkeypatch, sid, ask, action)
        assert first.message.startswith("Which project's todos do you want?")
        reply = await _turn(
            service, monkeypatch, sid, "launch", "small_talk", IntentCategory.CONVERSATION
        )
        assert reply.message == "Open todos in Launch:\n1. book the venue"
        assert service.workflow_offer_service._pending_offers.get(sid) is None
        _assert_nothing_written(service.todo_handlers)

    async def test_no_declines_with_the_records_line(self, projects, service, monkeypatch):
        projects[USER] = [_project("p1", "Launch")]
        sid = f"ptr-{uuid4().hex[:8]}"
        await _turn(service, monkeypatch, sid, ASK_1, BOTH[0])
        reply = await _turn(
            service, monkeypatch, sid, "no", "small_talk", IntentCategory.CONVERSATION
        )
        assert reply.message == "Okay, I haven't shown any todos."
        assert service.todo_handlers._reads == []

    async def test_bare_yes_reasks_the_same_question(self, projects, service, monkeypatch):
        projects[USER] = [_project("p1", "Launch")]
        sid = f"ptr-{uuid4().hex[:8]}"
        first = await _turn(service, monkeypatch, sid, ASK_1, BOTH[0])
        again = await _turn(
            service, monkeypatch, sid, "yes", "small_talk", IntentCategory.CONVERSATION
        )
        assert again.message == first.message
        offer = service.workflow_offer_service._pending_offers.get(sid)
        assert offer["pending_action"]["kind"] == ptr.PROJECT_TODOS_PICK_KIND
        assert service.todo_handlers._reads == []


# -- the registry and the two request pins -----------------------------------------


class TestRegistryAndPins:
    def test_both_names_are_one_hidden_read_entry(self):
        from services.intent_service.workflow_dispatcher import (
            EffectClass,
            Outwardness,
            get_action_workflows,
        )

        workflow_entries.register_default_workflows()
        wf = get_action_workflows()
        a, b = wf[BOTH[0]], wf[BOTH[1]]
        assert a is b
        assert a.effect == EffectClass.READ and a.outwardness == Outwardness.PRIVATE
        assert a.router_visible is False and a.action_triggered is True
        assert a.flip_group is None

    def test_the_reask_landing_is_offer_only_and_reads(self):
        from services.intent_service.workflow_dispatcher import (
            EffectClass,
            get_action_workflows,
            get_registered_workflows,
        )

        workflow_entries.register_default_workflows()
        landing = get_registered_workflows()[ptr.PROJECT_TODOS_PICK_WORKFLOW]
        assert landing.effect == EffectClass.READ
        assert landing.action_triggered is False
        assert ptr.PROJECT_TODOS_PICK_WORKFLOW not in get_action_workflows()

    def test_the_router_never_saw_them_and_its_request_is_mains(self):
        """The hash is main's at `a537dae663`, the one 2297 and 2301 pin."""
        from services.intent_service.action_registry import ACTION_EXAMPLES, ACTION_REGISTRY
        from services.intent_service.inversion_router import (
            _SYSTEM_PROMPT,
            build_routing_prompt,
            derive_routing_grammar,
        )
        from services.intent_service.router_catalog_order import CATALOG_ORDER_LEDGER
        from services.intent_service.workflow_dispatcher import get_registered_workflows

        workflow_entries.register_default_workflows()
        grammar = derive_routing_grammar()
        for name in BOTH + [ptr.PROJECT_TODOS_PICK_WORKFLOW]:
            assert name in get_registered_workflows()
            assert name not in grammar.names()
            assert name not in CATALOG_ORDER_LEDGER
            assert not [k for k in ACTION_REGISTRY if k[1] == name]
            assert not [k for k in ACTION_EXAMPLES if k[1] == name]
        prompt = build_routing_prompt(
            "add a task to my Launch project: book the venue", grammar, None
        )
        request = _SYSTEM_PROMPT + "\x00" + prompt
        assert hashlib.sha256(request.encode("utf-8")).hexdigest() == (
            "0cbc4772d8cf2831a692c6239801a788034853fec897f9099aedb0c93b7a84ac"
        )

    def test_the_classifier_request_is_unchanged(self):
        """The classifier's request for ASK_1 as ``scripts/router_batch.py
        render-classifier --base neutral`` builds it (system and messages; the model
        is left out). Hashed BEFORE this change at 2f40e8dc46, whose classifier.py and
        prompts.py are byte-identical to origin/main 0517da9a36, and again after:
        the same value, with the registry populated. A different hash means the
        classifier's input moved: that is a rule-7 change and needs its screen."""
        from services.configuration.personalization_service import NEUTRAL_DEFAULT_CONTEXT
        from services.configuration.piper_config_loader import PiperConfigLoader
        from services.intent_service.action_registry import Verb
        from services.intent_service.classifier import _CLASSIFICATION_PROMPT_STATIC_HEAD
        from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT
        from services.llm.cacheable_prompt import (
            CacheablePrompt,
            anthropic_system_content,
            anthropic_user_content,
        )

        workflow_entries.register_default_workflows()
        loader = PiperConfigLoader(config_path=str(REPO / "config" / "PIPER.md"))
        system = loader._format_system_prompt(dict(NEUTRAL_DEFAULT_CONTEXT))
        head = _CLASSIFICATION_PROMPT_STATIC_HEAD
        full = INTENT_CLASSIFICATION_PROMPT.format(
            user_message=ASK_1,
            context_info="",
            file_context="",
            spatial_context="",
            verb_vocab=", ".join(v.value for v in Verb),
        )
        assert full.startswith(head)
        request = json.dumps(
            {
                "system": anthropic_system_content(system),
                "messages": [
                    {
                        "role": "user",
                        "content": anthropic_user_content(CacheablePrompt(head, full[len(head) :])),
                    }
                ],
            },
            sort_keys=True,
        )
        assert hashlib.sha256(request.encode("utf-8")).hexdigest() == (
            "550acd8ea107080ebfc4dde37e7cee5bce512261943a85d97fd7136ed38bf4b7"
        )
        for name in BOTH:
            assert name not in INTENT_CLASSIFICATION_PROMPT

    def test_the_hidden_landing_survives_router_none_stands(self, monkeypatch):
        """A router NONE on the live set leaves the legacy landing on these hidden
        entries standing (the #2132 option (b) guard in inversion_live)."""
        import services.intent_service.inversion_live as il

        workflow_entries.register_default_workflows()
        monkeypatch.setenv(
            "PIPER_INVERSION_LIVE_CATEGORIES",
            "read_floor,read_portfolio,read_referent,read_status,read_strategic,"
            "read_synthesis,read_temporal",
        )
        il.publish_live_route_provenance(
            il.LiveRouteProvenance(routed_live=False, reason="router_none", confidence=0.95)
        )
        try:
            for name in BOTH:
                assert il.router_none_stands("query", name) is None
        finally:
            il.publish_live_route_provenance(None)
