"""1527 (remaining scope) — named-target resolution for delete_todo.

PM live 2026-08-29 (v64): after the 1527 routing fix, 'delete my hydrate
reminder' — the phrase Piper itself taught — ROUTED correctly to the
delete_todo rail and then died on the gate's no-number passthrough:
"Which todo? Try: 'delete todo [number]'". The lane's honest scope note:
routing was fixed, resolution was not.

The fix under test: when a delete turn carries a NAMED target (no number),
``build_todo_delete_confirmation`` resolves it against the owner's todos
with complete_todo's matching — the shared pure matcher extracted to
``todo_handlers`` module level (``fuzzy_todo_match_score`` /
``match_todos_by_text`` / ``resolve_named_todo_target``), same word-overlap
score, same ``_FUZZY_MATCH_THRESHOLD``. Single match → the EXISTING #1666
title-bound DESTRUCTIVE confirm arms ('Delete todo: "hydrate"? (yes/no)'),
resolved row bound into the intent (list-shift protection intact). Several
matches → ask which, listing candidates by real list position. Zero → the
honest didn't-find copy in todo/reminder vocabulary — NEVER a project.

Ratchet note (TestExtractionPatternRatchet, PM-ratified the same day): the
named target is derived by word-SET subtraction (drop delete-command
vocabulary + stopwords), then string-matched against the DB list — no new
message-parsing regex patterns anywhere on this path.

Layer honesty (m-43): unit classes hit the pure matcher and the async
builder directly; the end-to-end classes drive the REAL
``IntentService.process_intent`` (the 1527/#1666 idiom) with the LLM
boundary explosive, classification stubbed to the surface-2 ``delete_todo``
emission, and the TodoManagementService boundary explosive-until-armed.
"""

import datetime as _dt
from types import SimpleNamespace
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    DESTRUCTIVE_CONFIRM_KIND,
    RESOLVED_TODO_CONTEXT_KEY,
    build_todo_delete_confirmation,
)
from services.intent_service.todo_handlers import (
    TodoIntentHandlers,
    fuzzy_todo_match_score,
    match_todos_by_text,
    resolve_named_todo_target,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

_USER = "3f7b8a52-1527-4b00-9e00-000000001666"  # valid UUID: survives principal parsing


def _todo(text):
    return Todo(
        id=str(uuid4()),
        text=text,
        priority="medium",
        status="pending",
        completed=False,
        reminder_date=_dt.datetime(2026, 8, 29, 9, 0, tzinfo=_dt.timezone.utc),
    )


# ---------------------------------------------------------------------------
# 1. The shared matcher — one mechanism, both callers (unit)
# ---------------------------------------------------------------------------


class TestSharedMatcher:
    def test_complete_todos_score_fn_is_the_shared_fn(self):
        """The completion path's matcher IS the module-level pure function —
        not a divergent copy (the reuse-don't-duplicate pin)."""
        assert TodoIntentHandlers._fuzzy_match_score is fuzzy_todo_match_score

    def test_find_best_matching_todo_delegates_to_shared_scorer(self, monkeypatch):
        """Both callers observe the same module-level scorer: patch it and
        the completion path's best-match reflects the patch."""
        import services.intent_service.todo_handlers as th

        todos = [_todo("alpha"), _todo("beta")]

        def _rigged(search_text, candidates):
            return [(1.0, todos[1])]

        monkeypatch.setattr(th, "match_todos_by_text", _rigged)
        handlers = TodoIntentHandlers.__new__(TodoIntentHandlers)
        assert handlers._find_best_matching_todo("anything", todos) is todos[1]

    def test_completion_best_match_behavior_unchanged(self):
        """#904 behavior, verbatim through the extracted helper: best fuzzy
        match above threshold; None below it."""
        handlers = TodoIntentHandlers.__new__(TodoIntentHandlers)
        todos = [_todo("Review the PR for auth"), _todo("deploy kubernetes cluster")]
        assert handlers._find_best_matching_todo("PR review", todos) is todos[0]
        assert handlers._find_best_matching_todo("banana shopping list", todos) is None

    def test_resolver_unique_exact_beats_fuzzy_crowd(self):
        """'call mom' against ['call mom', 'call the dentist']: both fuzzy-
        match, but the unique EXACT title wins outright — one candidate,
        no nagging ambiguity ask for a precisely-named target."""
        todos = [_todo("call mom"), _todo("call the dentist")]
        assert resolve_named_todo_target("call mom", todos) == [todos[0]]

    def test_resolver_multiple_fuzzy_no_exact_returns_all_candidates(self):
        todos = [_todo("hydrate the plants"), _todo("hydrate the cat")]
        matches = resolve_named_todo_target("hydrate", todos)
        assert set(t.id for t in matches) == {todos[0].id, todos[1].id}

    def test_resolver_zero_match_returns_empty(self):
        todos = [_todo("Review the PR"), _todo("Call the vendor")]
        assert resolve_named_todo_target("flayrod", todos) == []

    def test_resolver_uses_the_shared_threshold(self):
        """Same threshold as completion: a 1-of-3-words overlap (0.33) is a
        candidate; a 1-of-4 (0.25) is not — mirroring _FUZZY_MATCH_THRESHOLD
        = 0.3 through the shared scorer."""
        todos = [_todo("hydrate")]
        assert resolve_named_todo_target("hydrate morning evening", todos) == [todos[0]]
        assert resolve_named_todo_target("hydrate morning evening night", todos) == []

    def test_match_todos_by_text_orders_best_first(self):
        """Higher word-overlap fraction sorts first: 'water plants' scores
        1.0 against "water plants" and 0.5 against "water the garden"."""
        todos = [_todo("water the garden"), _todo("water plants")]
        scored = match_todos_by_text("water plants", todos)
        assert [t.id for _, t in scored] == [todos[1].id, todos[0].id]
        assert scored[0][0] == 1.0 and scored[1][0] == 0.5


# ---------------------------------------------------------------------------
# 2. The async builder's named-target leg (unit)
# ---------------------------------------------------------------------------


class _BuilderHandlers:
    """Minimal todo_handlers stand-in (the #1666 builder-test idiom): real
    _extract_todo_id via the real class method, list via stub."""

    def __init__(self, todos=None, raise_on_list=False):
        self._extract = TodoIntentHandlers._extract_todo_id
        self._todos = todos if todos is not None else [_todo("hydrate"), _todo("Review the PR")]
        self._raise = raise_on_list
        outer = self

        class _Svc:
            async def list_todos(self, user_id, include_completed=False):
                if outer._raise:
                    raise RuntimeError("db down")
                return list(outer._todos)

        self.todo_service = _Svc()

    def _extract_todo_id(self, message):
        return self._extract(self, message)


def _delete_intent(message, action="delete_todo"):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )


class TestBuilderNamedTargetLeg:
    pytestmark = pytest.mark.asyncio

    @pytest.mark.parametrize(
        "message", ("delete my hydrate reminder", "delete the reminder to hydrate")
    )
    async def test_pm_phrasings_arm_the_title_bound_confirm(self, message):
        handlers = _BuilderHandlers()
        intent = _delete_intent(message)
        gate = await build_todo_delete_confirmation(intent, handlers, _USER)
        assert gate.offer is not None and not gate.passthrough
        assert gate.offer.question == 'Delete todo: "hydrate"? (yes/no)'
        record = gate.offer.offer
        # #1665: the stored ask IS the said ask, byte-for-byte.
        assert record["question"] == gate.offer.question
        pa = record["pending_action"]
        assert pa["kind"] == DESTRUCTIVE_CONFIRM_KIND
        assert pa["action"] == "delete_todo"
        assert pa["intent"] is intent
        assert 'won\'t delete the todo "hydrate"' in record["decline_message"]
        assert "Nothing has been changed" in record["decline_message"]
        # WHAT-binding (#1666 list-shift protection) rides the named leg too:
        resolved = intent.context[RESOLVED_TODO_CONTEXT_KEY]
        assert resolved["todo_id"] == handlers._todos[0].id
        assert resolved["text"] == "hydrate"

    async def test_exact_title_wins_over_a_similar_sibling(self):
        """A precisely-named target arms directly even when a similar todo
        exists — the exact tier of the shared resolver."""
        handlers = _BuilderHandlers(todos=[_todo("hydrate"), _todo("hydrate the plants")])
        gate = await build_todo_delete_confirmation(
            _delete_intent("delete my hydrate reminder"), handlers, _USER
        )
        assert gate.offer is not None
        assert gate.offer.question == 'Delete todo: "hydrate"? (yes/no)'

    async def test_ambiguous_target_asks_which_with_real_positions(self):
        """Two fuzzy candidates, no exact — the gate asks which, numbering
        by REAL list position (so 'delete todo [number]' works verbatim),
        and arms nothing."""
        todos = [_todo("Review the PR"), _todo("hydrate the plants"), _todo("hydrate the cat")]
        handlers = _BuilderHandlers(todos=todos)
        intent = _delete_intent("delete my hydrate reminder")
        gate = await build_todo_delete_confirmation(intent, handlers, _USER)
        assert gate.clarification is not None
        assert gate.offer is None and not gate.passthrough
        assert '2. "hydrate the plants"' in gate.clarification
        assert '3. "hydrate the cat"' in gate.clarification
        assert "Which one should I delete?" in gate.clarification
        # nothing bound: an unarmed turn must not leave a usable binding
        assert RESOLVED_TODO_CONTEXT_KEY not in (intent.context or {})

    async def test_zero_match_is_honest_todo_vocabulary_never_projects(self):
        """The 1527 wound, pinned at the copy level: a miss answers in the
        user's domain (todos/reminders) — the word 'project' never appears."""
        handlers = _BuilderHandlers()
        gate = await build_todo_delete_confirmation(
            _delete_intent("delete the reminder to check the flayrod"), handlers, _USER
        )
        assert gate.clarification is not None
        assert "couldn't find a todo or reminder" in gate.clarification
        assert "flayrod" in gate.clarification
        assert "nothing has been deleted" in gate.clarification
        assert "project" not in gate.clarification.lower()

    async def test_numbered_path_unchanged(self):
        """A number still takes the positional leg with the #1666 shape."""
        handlers = _BuilderHandlers()
        gate = await build_todo_delete_confirmation(
            _delete_intent("delete todo 1"), handlers, _USER
        )
        assert gate.offer is not None
        assert gate.offer.question == 'Delete todo 1: "hydrate"? (yes/no)'

    async def test_lookup_failure_on_named_path_is_honest_noop(self):
        """The named leg inherits the #1666 safe default: can't see the list
        → honest no-op turn, never a passthrough of a possibly-deleting turn."""
        handlers = _BuilderHandlers(raise_on_list=True)
        gate = await build_todo_delete_confirmation(
            _delete_intent("delete my hydrate reminder"), handlers, _USER
        )
        assert gate.error_message is not None
        assert gate.offer is None and not gate.passthrough
        assert "haven't deleted anything" in gate.error_message


# ---------------------------------------------------------------------------
# 3. End-to-end through the REAL process_intent (the 1527/#1666 idiom)
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — these turns must resolve deterministically"
        )


@pytest.fixture
def live_service():
    register_default_workflows()  # idempotent; the app does this at startup
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _stub_classification(monkeypatch, service, message, action):
    """Deterministic surface-2 emission (the 1666/#1605 idiom)."""
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)
    return intent


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list deterministic (PM's hydrate
    reminder is row 1); delete EXPLOSIVE until a test arms it — nothing may
    mutate unconfirmed."""
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": [_todo("hydrate"), _todo("Review the PR")],
        "deleted": [],
        "allow_delete": False,
    }

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _delete(self, todo_id, user_id):
        if not state["allow_delete"]:
            raise AssertionError(
                "todo_service.delete_todo FIRED — a destructive mutation "
                "executed without a confirmed yes"
            )
        state["deleted"].append(str(todo_id))
        state["todos"] = [t for t in state["todos"] if t.id != str(todo_id)]
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


class TestEndToEndNamedDelete:
    pytestmark = pytest.mark.asyncio

    async def test_pm_exact_phrase_arms_then_yes_deletes_that_row(
        self, live_service, monkeypatch, todo_boundary
    ):
        """PM's exact live phrasing (the one Piper taught, then denied):
        'delete my hydrate reminder' → title-bound confirm → 'yes' deletes
        THE row resolved at ask time."""
        sid = "e2e-named-yes"
        hydrate_id = todo_boundary["todos"][0].id
        _stub_classification(monkeypatch, live_service, "delete my hydrate reminder", "delete_todo")
        result = await live_service.process_intent(
            message="delete my hydrate reminder", session_id=sid, user_id=_USER
        )
        assert result.message == 'Delete todo: "hydrate"? (yes/no)'
        assert result.intent_data.get("destructive_confirmation_pending") is True
        assert todo_boundary["deleted"] == []
        todo_boundary["allow_delete"] = True
        result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert todo_boundary["deleted"] == [hydrate_id]
        assert "hydrate" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_pm_other_phrase_arms_then_no_deletes_nothing(
        self, live_service, monkeypatch, todo_boundary
    ):
        sid = "e2e-named-no"
        _stub_classification(
            monkeypatch, live_service, "delete the reminder to hydrate", "delete_todo"
        )
        result = await live_service.process_intent(
            message="delete the reminder to hydrate", session_id=sid, user_id=_USER
        )
        assert result.message == 'Delete todo: "hydrate"? (yes/no)'
        result = await live_service.process_intent(message="no", session_id=sid, user_id=_USER)
        assert 'won\'t delete the todo "hydrate"' in result.message
        assert "Nothing has been changed" in result.message
        assert todo_boundary["deleted"] == []
        assert _pending_offers(live_service).get(sid) is None

    async def test_yes_deletes_the_bound_row_under_list_shift(
        self, live_service, monkeypatch, todo_boundary
    ):
        """#1666's list-shift protection holds on the named leg: an
        interloper lands at position 1 between ask and yes — the delete
        still takes the row the user confirmed by title."""
        sid = "e2e-named-shift"
        hydrate_id = todo_boundary["todos"][0].id
        _stub_classification(monkeypatch, live_service, "delete my hydrate reminder", "delete_todo")
        await live_service.process_intent(
            message="delete my hydrate reminder", session_id=sid, user_id=_USER
        )
        interloper = _todo("Brand new urgent thing")
        todo_boundary["todos"].insert(0, interloper)
        todo_boundary["allow_delete"] = True
        await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert todo_boundary["deleted"] == [hydrate_id]
        assert interloper.id not in todo_boundary["deleted"]

    async def test_ambiguous_target_asks_which_and_arms_nothing(
        self, live_service, monkeypatch, todo_boundary
    ):
        sid = "e2e-named-ambiguous"
        todo_boundary["todos"] = [_todo("hydrate the plants"), _todo("hydrate the cat")]
        _stub_classification(monkeypatch, live_service, "delete my hydrate reminder", "delete_todo")
        result = await live_service.process_intent(
            message="delete my hydrate reminder", session_id=sid, user_id=_USER
        )
        assert "Which one should I delete?" in result.message
        assert '1. "hydrate the plants"' in result.message
        assert '2. "hydrate the cat"' in result.message
        assert "project" not in result.message.lower()
        assert result.requires_clarification is True
        assert _pending_offers(live_service).get(sid) is None
        assert todo_boundary["deleted"] == []

    async def test_zero_match_answers_honestly_never_a_project(
        self, live_service, monkeypatch, todo_boundary
    ):
        """PM's 08-18 live miss verbatim: 'delete the reminder to check the
        flayrod' must answer in todo/reminder vocabulary — never "couldn't
        find a project called ...'."""
        sid = "e2e-named-miss"
        phrase = "delete the reminder to check the flayrod"
        _stub_classification(monkeypatch, live_service, phrase, "delete_todo")
        result = await live_service.process_intent(message=phrase, session_id=sid, user_id=_USER)
        assert "couldn't find a todo or reminder" in result.message
        assert "project" not in result.message.lower()
        assert _pending_offers(live_service).get(sid) is None
        assert todo_boundary["deleted"] == []

    async def test_numbered_path_unchanged_end_to_end(
        self, live_service, monkeypatch, todo_boundary
    ):
        sid = "e2e-named-numbered"
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        result = await live_service.process_intent(
            message="delete todo 1", session_id=sid, user_id=_USER
        )
        assert result.message == 'Delete todo 1: "hydrate"? (yes/no)'
        assert todo_boundary["deleted"] == []
