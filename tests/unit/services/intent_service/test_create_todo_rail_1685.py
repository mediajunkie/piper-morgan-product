"""#1685 [MVP] — create_todo onto the rail (#1666's exact gap, create side).

Arch's finding (2026-08-25, while checking a claim of their own rather than
trusting it): ``create_todo`` was absent from the rail dict in
``workflow_entries.py`` entirely, so ``intent.action in _action_workflows``
was FALSE at the #1124 rail check. It dispatched via the legacy
``elif mapped_action`` chain into ``todo_handlers.handle_create_todo``, which
makes ZERO ``consent_gate`` calls. So it was never "a WRITE the matrix
correctly waves through" — it was UNREGISTERED: not covered because nothing
evaluated it. That distinction is the whole issue.

The fix under test: the create-todo alias family registered
``effect=EffectClass.WRITE``, ``outwardness=PRIVATE``,
``action_triggered=True`` (the #1666 delete_todo shape, one tier down); the
legacy elif REMOVED in the same commit (#1411/#1666 migration precedent).

⚠️ THE POINT IS EVALUATION, NOT CEREMONY. The consent gate must now be
CONSULTED on a create turn (``TestConsentGateIsConsulted``) while the user
sees exactly what they saw before: one turn, todo created, no question
(``TestNoNewCeremony``). Both halves are asserted, because either one alone
is a half-truth — a silent pass and an unregistered action are indistinguish-
able from the transcript, which is the m-44 shape #1685 exists to close.

The ALIAS FAMILY is derived from ``ActionMapper.ACTION_MAPPING``, never
assumed to mirror the delete side (it does not: delete's family is
delete/remove/cancel, create's is create/add/new) — ``test_alias_family_is_
exactly_the_mapper_family`` pins the derivation so a future mapper alias
cannot silently land off-rail.

Layer honesty (m-43): the end-to-end classes drive the REAL
``IntentService.process_intent`` with an explosive LLM — mocked ONLY at the
classification boundary (no deterministic surface emits create_todo; the
#1675 note in test_canonical_conversations records that "Add a todo: …" has
no pre-classifier claim) and at the TodoManagementService boundary. The
reminder-boundary class drives the REAL pre-classifier-claimed reminder
shapes with no classification stub at all.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import consent_gate
from services.intent_service.action_mapper import ActionMapper
from services.intent_service.classifier import IntentClassifier
from services.intent_service.collaboration_gate import WORKING_MODE_PREF_KEY
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
)
from services.intent_service.todo_handlers import (
    REMINDER_TASK_QUESTION_KIND,
    REMINDER_TIME_QUESTION_KIND,
)
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory, Outwardness

_USER = "3f7b8a52-1685-4b00-9e00-000000001685"  # valid UUID: survives principal parsing

# The create-side alias family, ENUMERATED from the mapper (see the module
# docstring) — create_todo/add_todo/new_todo, NOT a mirror of delete's set.
CREATE_TODO_ALIASES = ("create_todo", "add_todo", "new_todo")

# Verb-initial imperative — what every natural create phrasing looks like, and
# what classify_framing reads as EXECUTE (→ PROCEED, no ceremony).
IMPERATIVE_CREATE = "add a todo: buy milk"
# The one shape the #1509 matrix holds: no imperative head, no compose marker.
AMBIGUOUS_CREATE = "todo: buy milk"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1685 turns must resolve "
            "deterministically"
        )


@pytest.fixture
def live_service():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


@pytest.fixture
def mem_prefs(monkeypatch):
    """In-memory users.preferences double at the ONE persistence seam (the
    #1509 fixture) — the declared working mode decides the ambiguous cell."""
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        if str(user_id) not in store:
            return False
        store[str(user_id)][key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _stub_classification(
    monkeypatch, service, message, action, category=IntentCategory.EXECUTION
):
    """Deterministic classification for the classified turn (the #1666 idiom).
    Stated per m-43: create_todo has NO deterministic emitting surface, so the
    (action, framing) pair can only come from the LLM lane in production."""
    intent = Intent(
        category=category,
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
    """TodoManagementService.create_todo boundary: records every write."""
    from services.todo.todo_management_service import TodoManagementService

    state = {"created": []}

    async def _create(self, user_id, text, priority="medium", **kwargs):
        row = SimpleNamespace(
            id=uuid4(), text=text, priority=priority, user_id=user_id
        )
        state["created"].append(row)
        return row

    monkeypatch.setattr(TodoManagementService, "create_todo", _create)
    return state


# ---------------------------------------------------------------------------
# 1. Registry: the entry exists at all (RED while create_todo was rail-invisible)
# ---------------------------------------------------------------------------


class TestCreateTodoRailEntries:
    def test_family_registered_write_private_action_triggered(self):
        register_default_workflows()
        wf = get_action_workflows()
        for alias in CREATE_TODO_ALIASES:
            assert alias in wf, f"{alias} missing from the action rail (#1685)"
            entry = wf[alias]
            assert entry.effect == EffectClass.WRITE, (
                f"{alias} must be WRITE — handle_create_todo persists a row, "
                f"but the row is deletable, so never DESTRUCTIVE (#1685)"
            )
            assert entry.outwardness == Outwardness.PRIVATE
            assert entry.action_triggered is True

    def test_family_derives_needs_consent_but_not_needs_confirm(self):
        """The registration's whole effect, in two booleans: the gate now RUNS
        (needs_consent), and it does NOT arm a #1190 yes/no confirm tier."""
        register_default_workflows()
        wf = get_action_workflows()
        for alias in CREATE_TODO_ALIASES:
            assert wf[alias].needs_consent is True
            assert wf[alias].needs_confirm is False
            assert wf[alias].destructive_hint is False

    def test_aliases_share_one_entry(self):
        register_default_workflows()
        wf = get_action_workflows()
        assert wf["add_todo"] is wf["create_todo"]
        assert wf["new_todo"] is wf["create_todo"]

    def test_alias_family_is_exactly_the_mapper_family(self):
        """Drift guard on the ENUMERATION (not an assumption that create
        mirrors delete): every ActionMapper key that canonicalizes to
        create_todo must be rail-registered, or an LLM emitting that raw name
        lands off-rail and skips the gate again — #1685's own failure mode."""
        register_default_workflows()
        wf = get_action_workflows()
        mapper_family = {
            raw
            for raw, canonical in ActionMapper.ACTION_MAPPING.items()
            if canonical == "create_todo"
        }
        assert mapper_family == set(CREATE_TODO_ALIASES), (
            f"the mapper's create-todo family changed: {sorted(mapper_family)} — "
            f"update the rail registration and this list together (#1685)"
        )
        missing = mapper_family - set(wf)
        assert not missing, f"mapper aliases off the rail: {sorted(missing)} (#1685)"

    def test_declared_effect_is_readable_through_the_lookup_seam(self):
        """#1557: consumers look the effect up, never infer it from the name.
        Before #1685 both lookups returned None for create_todo — the shape of
        'unregistered', which is what let it read as 'no consent derivation'."""
        for alias in CREATE_TODO_ALIASES:
            assert consent_gate.effect_for_action(alias) is EffectClass.WRITE
            assert consent_gate.outwardness_for_action(alias) is Outwardness.PRIVATE

    def test_legacy_elif_removed(self):
        """Migration completion (#1411/#1666 precedent): the ungated elif is
        GONE — the rail is the single dispatch surface for create_todo. Kept as
        a 'backstop' it would be reachable only when rail dispatch returned
        None (i.e. the handler RAISED), making it a silent retry of a failed
        write."""
        with open("services/intent/intent_service.py", encoding="utf-8") as fh:
            src = fh.read()
        assert 'mapped_action == "create_todo"' not in src, (
            "the legacy create_todo elif is back — it dispatches a write that "
            "consent_gate never evaluates (#1685's whole finding)"
        )


# ---------------------------------------------------------------------------
# 2. The gate is CONSULTED (the half that was missing, and is invisible)
# ---------------------------------------------------------------------------


class TestConsentGateIsConsulted:
    """The #1685 AC that no transcript can show: on a create turn the unified
    consent decision actually RUNS, with the DECLARED effect + outwardness.

    Pre-#1685 this class is RED at the assertion, not the setup: the turn
    completes identically and evaluate_consent is never called. That
    indistinguishability is exactly why the assertion is at this seam.
    """

    pytestmark = pytest.mark.asyncio

    async def test_create_turn_evaluates_consent_with_declared_effect(
        self, live_service, monkeypatch, todo_boundary
    ):
        calls = []
        real = consent_gate.evaluate_consent

        async def _spy(effect, message, user_id, outwardness=Outwardness.PRIVATE):
            calls.append((effect, message, user_id, outwardness))
            return await real(effect, message, user_id, outwardness=outwardness)

        monkeypatch.setattr(consent_gate, "evaluate_consent", _spy)

        sid = "e2e-1685-consulted"
        _stub_classification(monkeypatch, live_service, IMPERATIVE_CREATE, "create_todo")
        await live_service.process_intent(
            message=IMPERATIVE_CREATE, session_id=sid, user_id=_USER
        )

        assert len(calls) == 1, (
            "consent_gate.evaluate_consent was not consulted for a create_todo "
            "turn — the #1685 gap (unregistered, so nothing evaluates it)"
        )
        effect, message, principal, outwardness = calls[0]
        assert effect is EffectClass.WRITE
        assert outwardness is Outwardness.PRIVATE
        assert message == IMPERATIVE_CREATE
        assert str(principal) == _USER

    @pytest.mark.parametrize("alias", CREATE_TODO_ALIASES)
    async def test_every_alias_is_evaluated(
        self, live_service, monkeypatch, todo_boundary, alias
    ):
        """A raw mapper alias must reach the gate too — an alias registered on
        the mapper but not the rail is the same gap wearing another name."""
        calls = []
        real = consent_gate.evaluate_consent

        async def _spy(effect, message, user_id, outwardness=Outwardness.PRIVATE):
            calls.append(effect)
            return await real(effect, message, user_id, outwardness=outwardness)

        monkeypatch.setattr(consent_gate, "evaluate_consent", _spy)
        sid = f"e2e-1685-alias-{alias}"
        _stub_classification(monkeypatch, live_service, IMPERATIVE_CREATE, alias)
        await live_service.process_intent(
            message=IMPERATIVE_CREATE, session_id=sid, user_id=_USER
        )
        assert calls == [EffectClass.WRITE], f"{alias} skipped the consent gate"

    async def test_verdict_on_an_imperative_create_is_proceed(self):
        """The cell that makes evaluation cheap: PRIVATE x WRITE x execute
        framing is PROCEED, so consultation costs the user nothing."""
        verdict = await consent_gate.evaluate_consent(
            EffectClass.WRITE, IMPERATIVE_CREATE, _USER, outwardness=Outwardness.PRIVATE
        )
        assert verdict is consent_gate.ConsentDecision.PROCEED


# ---------------------------------------------------------------------------
# 3. NO new ceremony — the user-visible half, pinned e2e
# ---------------------------------------------------------------------------


class TestNoNewCeremony:
    """#1685 explicitly is NOT 'creating a todo starts asking'. A create turn
    still creates in ONE step: the row is written on the classified turn, the
    confirmation copy comes back, and nothing is left pending."""

    pytestmark = pytest.mark.asyncio

    async def test_imperative_create_writes_the_row_in_one_turn(
        self, live_service, monkeypatch, todo_boundary
    ):
        sid = "e2e-1685-oneturn"
        _stub_classification(monkeypatch, live_service, IMPERATIVE_CREATE, "create_todo")
        result = await live_service.process_intent(
            message=IMPERATIVE_CREATE, session_id=sid, user_id=_USER
        )
        assert [row.text for row in todo_boundary["created"]] == ["buy milk"]
        assert result.success is True
        assert "I've added that to your list." in result.message
        assert "'buy milk' is now tracked" in result.message

    async def test_imperative_create_asks_nothing_and_leaves_nothing_pending(
        self, live_service, monkeypatch, todo_boundary
    ):
        """The no-ceremony pin, stated as the three things a check turn would
        have produced: a question, a clarification flag, and a pending offer."""
        sid = "e2e-1685-noask"
        _stub_classification(monkeypatch, live_service, IMPERATIVE_CREATE, "create_todo")
        result = await live_service.process_intent(
            message=IMPERATIVE_CREATE, session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("consent_check_pending") is not True
        assert result.intent_data.get("destructive_confirmation_pending") is not True
        assert result.requires_clarification is not True
        assert "(yes/no)" not in result.message
        assert _pending_offers(live_service).get(sid) is None

    @pytest.mark.parametrize(
        "message,expected",
        [
            ("add a todo: buy milk", "buy milk"),
            ("create a todo: review the PR", "review the PR"),
            ("please add a new todo: water the plants", "water the plants"),
        ],
    )
    async def test_natural_create_phrasings_all_proceed(
        self, live_service, monkeypatch, todo_boundary, message, expected
    ):
        sid = f"e2e-1685-phrasing-{expected.replace(' ', '-')}"
        _stub_classification(monkeypatch, live_service, message, "create_todo")
        result = await live_service.process_intent(
            message=message, session_id=sid, user_id=_USER
        )
        assert [row.text for row in todo_boundary["created"]] == [expected]
        assert _pending_offers(live_service).get(sid) is None
        assert "(yes/no)" not in result.message

    async def test_category_independence(
        self, live_service, monkeypatch, todo_boundary
    ):
        """The rail dispatches by action BEFORE category routing (#1560
        rationale) — a create_todo emission under a non-EXECUTION category now
        writes the row instead of flooring into an improvised denial."""
        sid = "e2e-1685-category"
        _stub_classification(
            monkeypatch,
            live_service,
            IMPERATIVE_CREATE,
            "create_todo",
            category=IntentCategory.QUERY,
        )
        result = await live_service.process_intent(
            message=IMPERATIVE_CREATE, session_id=sid, user_id=_USER
        )
        assert [row.text for row in todo_boundary["created"]] == ["buy milk"]
        assert "I've added that to your list." in result.message

    async def test_unauthenticated_create_declines_without_writing(
        self, live_service, monkeypatch, todo_boundary
    ):
        """The removed elif's auth leg, carried verbatim by the rail entry
        point (#1466: principal coercion never raises on a Slack id)."""
        sid = "e2e-1685-noauth"
        _stub_classification(monkeypatch, live_service, IMPERATIVE_CREATE, "create_todo")
        result = await live_service.process_intent(
            message=IMPERATIVE_CREATE, session_id=sid, user_id=None
        )
        assert result.success is False
        assert "logged in to manage todos" in result.message
        assert result.error_type == "AuthenticationRequired"
        assert todo_boundary["created"] == []


# ---------------------------------------------------------------------------
# 4. The ambiguous cell — the ratified matrix, stated so it is never inferred
# ---------------------------------------------------------------------------


class TestAmbiguousFramingFollowsTheRatifiedMatrix:
    """Honest scope note (#1685): registering WRITE puts create_todo under the
    SAME #1509/#1510 matrix every other WRITE rail action already lives under,
    including the ambiguous cell. That cell holds — not because create_todo is
    special, but because ambiguity is what the gate confiscates. It is the
    identical treatment its already-registered sibling create_reminder (#1560)
    has had since #1509, and the declared execute mode still proceeds.
    """

    pytestmark = pytest.mark.asyncio

    async def test_ambiguous_create_is_held_with_a_legible_check(
        self, live_service, monkeypatch, todo_boundary, mem_prefs
    ):
        sid = "e2e-1685-ambiguous"
        _stub_classification(monkeypatch, live_service, AMBIGUOUS_CREATE, "create_todo")
        result = await live_service.process_intent(
            message=AMBIGUOUS_CREATE, session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("consent_check_pending") is True
        assert result.intent_data.get("consent_effect") == "write"
        assert todo_boundary["created"] == [], "an unchecked WRITE fired"
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert stored["pending_action"]["action"] == "create_todo"

    async def test_yes_writes_the_original_intent_unreclassified(
        self, live_service, monkeypatch, todo_boundary, mem_prefs
    ):
        sid = "e2e-1685-ambiguous-yes"
        _stub_classification(monkeypatch, live_service, AMBIGUOUS_CREATE, "create_todo")
        await live_service.process_intent(
            message=AMBIGUOUS_CREATE, session_id=sid, user_id=_USER
        )
        assert todo_boundary["created"] == []

        async def _explosive(msg, context=None, user_id=None, session_id=None):
            raise AssertionError("'yes' was re-classified")

        monkeypatch.setattr(
            live_service.intent_classifier, "classify_multiple", _explosive
        )
        result = await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        assert [row.text for row in todo_boundary["created"]] == ["buy milk"]
        assert "I've added that to your list." in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_execute_mode_user_proceeds_on_the_same_ambiguity(
        self, live_service, monkeypatch, todo_boundary, mem_prefs
    ):
        """The declared working model decides the ambiguous cell — graduation
        is a setting, not friction (CXO's decline-property inverse)."""
        mem_prefs[_USER][WORKING_MODE_PREF_KEY] = "execute"
        sid = "e2e-1685-ambiguous-execmode"
        _stub_classification(monkeypatch, live_service, AMBIGUOUS_CREATE, "create_todo")
        result = await live_service.process_intent(
            message=AMBIGUOUS_CREATE, session_id=sid, user_id=_USER
        )
        assert [row.text for row in todo_boundary["created"]] == ["buy milk"]
        assert _pending_offers(live_service).get(sid) is None
        assert "I've added that to your list." in result.message


# ---------------------------------------------------------------------------
# 5. The reminder boundary, pinned BOTH ways (#1648 / #1654 carriers)
# ---------------------------------------------------------------------------


def _mock_reminder_todo_service(svc):
    """The #1654 fixture: swap the DB-backed service for a recording mock.
    The seam under test is claim-ownership, not persistence."""
    mock = MagicMock()
    mock.create_todo = AsyncMock(
        return_value=SimpleNamespace(id=uuid4(), text="whatever")
    )
    mock.list_todos = AsyncMock(return_value=[])
    svc.todo_handlers.todo_service = mock
    return mock


class TestReminderBoundaryBothWays:
    """Reminder-creation and todo-creation share phrasing space, and #1685
    puts a NEW claimant (the create_todo rail entry) into it. Both directions
    are pinned: the reminder carriers still claim exactly the turns they
    claimed before, and a create_todo turn never reaches them.

    Layer note (m-43): direction 1 uses the REAL pre-classifier-claimed
    reminder shapes with NO classification stub — the explosive LLM proves the
    turns resolved deterministically, which is the property #1648/#1654 exist
    to protect.
    """

    pytestmark = pytest.mark.asyncio

    async def test_reminder_task_clarify_still_arms_its_carrier(self, live_service):
        """Direction 1a (#1654): the no-task clarify ask still fires and still
        arms the task-question carrier — create_todo's registration did not
        intercept the reminder turn."""
        _mock_reminder_todo_service(live_service)
        sid = "e2e-1685-reminder-arm"
        from services.intent_service import collaboration_gate as _cg

        with patch.object(_cg, "_load_preferences", new=AsyncMock(return_value={})):
            r1 = await live_service.process_intent(
                message="set a reminder: check the oven", session_id=sid, user_id=_USER
            )
        assert "I didn't catch what you'd like to be reminded about" in r1.message
        stored = next(iter(_pending_offers(live_service).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TASK_QUESTION_KIND

    async def test_bare_task_answer_still_binds_to_the_reminder_carrier(
        self, live_service
    ):
        """Direction 1b — the load-bearing one. 'buy milk' is a bare task
        phrase that a classifier would happily read as create_todo; the
        carrier must still win it at the offer seam (which runs BEFORE
        classification), or #1685 would re-open #1654's orphan by giving the
        phrase a new home."""
        mock = _mock_reminder_todo_service(live_service)
        sid = "e2e-1685-reminder-bind"
        from services.intent_service import collaboration_gate as _cg

        with patch.object(_cg, "_load_preferences", new=AsyncMock(return_value={})):
            await live_service.process_intent(
                message="set a reminder: check the oven", session_id=sid, user_id=_USER
            )
        r2 = await live_service.process_intent(
            message="buy milk", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_not_awaited()  # no time yet — the reminder flow, not a todo write
        assert "**buy milk**" in r2.message
        stored = next(iter(_pending_offers(live_service).values()))
        assert stored["pending_action"]["kind"] == REMINDER_TIME_QUESTION_KIND
        assert stored["pending_action"]["task_text"] == "buy milk"

    async def test_full_reminder_recovery_unchanged(self, live_service):
        """Direction 1c: the whole two-question #1654 recovery still ends in
        the REAL reminder save, with the reminder date bound."""
        mock = _mock_reminder_todo_service(live_service)
        sid = "e2e-1685-reminder-recovery"
        from services.intent_service import collaboration_gate as _cg

        with patch.object(_cg, "_load_preferences", new=AsyncMock(return_value={})):
            await live_service.process_intent(
                message="set a reminder: check the oven", session_id=sid, user_id=_USER
            )
        await live_service.process_intent(
            message="buy milk", session_id=sid, user_id=_USER
        )
        r3 = await live_service.process_intent(
            message="at 3pm tomorrow", session_id=sid, user_id=_USER
        )
        mock.create_todo.assert_awaited_once()
        kwargs = mock.create_todo.await_args.kwargs
        assert kwargs["text"] == "buy milk"
        assert kwargs["reminder_date"] is not None
        assert "Reminder saved" in r3.message
        assert _pending_offers(live_service) == {}

    async def test_create_reminder_still_routes_to_the_reminder_entry(self):
        """Direction 1d, at the registry: create_todo's registration did not
        take over, alias, or re-point the create_reminder family."""
        register_default_workflows()
        wf = get_action_workflows()
        assert wf["create_reminder"] is not wf["create_todo"]
        for alias in ("create_reminder", "set_reminder", "add_reminder"):
            assert wf[alias] is wf["create_reminder"]
            assert wf[alias].effect == EffectClass.WRITE

    async def test_create_todo_turn_never_touches_a_reminder_carrier(
        self, live_service, monkeypatch, todo_boundary
    ):
        """Direction 2: a create_todo turn writes a plain todo and arms NO
        reminder carrier — it must not leak into #1648/#1654's flow, whose
        whole contract is that an armed question owns the next turn."""
        sid = "e2e-1685-no-reminder-leak"
        _stub_classification(monkeypatch, live_service, IMPERATIVE_CREATE, "create_todo")
        result = await live_service.process_intent(
            message=IMPERATIVE_CREATE, session_id=sid, user_id=_USER
        )
        assert [row.text for row in todo_boundary["created"]] == ["buy milk"]
        assert result.intent_data.get("reminder_task_question_pending") is not True
        assert result.intent_data.get("reminder_time_question_pending") is not True
        assert _pending_offers(live_service) == {}
        assert "reminded about" not in result.message
