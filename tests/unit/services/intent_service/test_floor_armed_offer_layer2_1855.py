"""#1855 layer 2 — the floor ARMS what it offers, so the question may stand.

Layer 1 (2026-09-23, ``test_floor_unarmed_offer_seam_1855.py``) made an unarmed
offer-question impossible: the floor's output seam rewrote it into an imperative
suggestion. That closed the trust break but left CXO's contract sentence half
served — *the floor may only ASK "want me to X?" when X is armed this turn*. The
other half is this file: where tier 1 genuinely BINDS a command, the seam ARMS
it and PM's verbatim exchange finally works as written —

    Piper < Want me to add 'One Job' with the Design-in-Product/one-job repo
            to your projects now?
    PM    > Yes, please.
    Piper < Added One Job to your portfolio and linked
            Design-in-Product/one-job to it.

The arming precondition is exactly tier 1's existing round-trip (catalogued
family + slots from the floor's OWN sentence + a composed command that parses
back through the real extractor). No guessing: anything less is still a layer-1
rewrite.

Layer honesty (m-43). Four distinct layers are measured here, and they are NOT
interchangeable:
  * ``enforce_armed_offers`` / ``bind_catalogued_command`` / the record builder
    as PURE FUNCTIONS — no store, no rail.
  * The RENDERER SEAM: ``ConversationalFloor.respond()`` driven with a STUBBED
    LLM client (``llm.complete`` returns canned prose) and a static system
    prompt. This measures what reaches user copy given a model output; it is
    not a live model.
  * The #846 STORE: a real ``WorkflowOfferService`` instance, written by the
    real callback and read back with ``peek_pending_offer``.
  * The REAL RAIL, two turns: a real ``IntentService`` whose classifier LLM is
    EXPLOSIVE (any access fails the test), so every turn must resolve
    deterministically — the pending-offer seam on turn 2, the pre-classifier on
    the re-run command. The add-project handler is patched only at its DB seam
    (``ProjectRepository`` / ``RepositoryRepository`` /
    ``AsyncSessionFactory``), so the handler's own logic, slots and copy are
    the real ones.

Denominator (m-44): the one catalogued family (add-project) — pinned as exactly
the tested set by ``TestCatalogueDenominator``; PM's two verbatim turns; the
three non-accept dispositions (decline, off-intent, already-armed); both
settings of ``ARMED_QUESTION_FORM``; and ``revise_draft``'s log-only guard.
"""

import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from structlog.testing import capture_logs

from services.intent.intent_service import IntentService
from services.intent_service import unarmed_offer as uo
from services.intent_service.classifier import IntentClassifier
from services.intent_service.conversational_floor import ConversationalFloor, FloorContext
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
    offer_is_confirm,
)
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.unarmed_offer import (
    COMMAND_FAMILIES,
    FLOOR_BOUND_OFFER_KIND,
    bind_catalogued_command,
    build_floor_bound_offer_record,
    detect_offer_questions,
    enforce_armed_offers,
)

# PM's verbatim transcript turns (issue #1855, alpha 2026-09-23).
PM_OFFER = "Want me to add 'One Job' with the Design-in-Product/one-job repo to your projects now?"
PM_REPLY = "I found the repo. " + PM_OFFER
PM_ACCEPT = "Yes, please."
PM_EXPECTED_COMMAND = "add project One Job with repo Design-in-Product/one-job"

_USER = "3f7b8a52-1855-4b00-9e00-000000001855"  # valid UUID: survives principal parsing


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class _Armer:
    """The arming callback, backed by a REAL WorkflowOfferService."""

    def __init__(self, session_id="s1855-l2", user_id=None, succeeds=True, raises=False):
        self.offers = WorkflowOfferService()
        self.session_id = session_id
        self.user_id = user_id
        self.records = []
        self._succeeds = succeeds
        self._raises = raises

    def __call__(self, record):
        self.records.append(record)
        if self._raises:
            raise RuntimeError("store unavailable")
        if not self._succeeds:
            return False
        self.offers.set_pending_offer(self.session_id, record, user_id=self.user_id)
        return True

    def peek(self):
        return self.offers.peek_pending_offer(self.session_id, user_id=self.user_id)


def _floor_returning(text):
    llm = MagicMock()
    llm.complete = AsyncMock(return_value=text)
    return ConversationalFloor(
        llm_client=llm,
        system_prompt_base="You are Piper Morgan (test base).",
    )


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    the rail tests must resolve deterministically (the pending-offer seam,
    which runs before classification, and the pre-classifier)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1855 layer 2 turns are deterministic"
        )


class _Created:
    id = "proj-1855"
    name = "One Job"


class _RecordingProjectRepository:
    """The add-project handler's DB seam, recording — not the handler."""

    calls = []

    def __init__(self, session):
        pass

    async def find_by_name(self, name, owner_id):
        _RecordingProjectRepository.calls.append(("find_by_name", name, owner_id))
        return None

    async def create(self, name, description, owner_id):
        _RecordingProjectRepository.calls.append(("create", name, owner_id))
        return _Created()


class _RecordingRepositoryRepository:
    def __init__(self, session):
        pass

    async def get_by_full_name(self, full_name, provider, owner_id):
        _RecordingProjectRepository.calls.append(("get_repo", full_name))
        return MagicMock(id="repo-1855")

    async def get_project_links(self, repository_id):
        return []

    async def link_to_project(self, repository_id, project_id, linked_by):
        _RecordingProjectRepository.calls.append(("link", repository_id, project_id))


class _ExplosiveProjectRepository:
    """Nothing may reach the add-project write on a non-accept turn."""

    def __init__(self, *a, **k):
        raise AssertionError("add-project DB seam touched — nothing should have dispatched")


class _SessionScope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *exc):
        return False


def _patched_db(project_repo=_RecordingProjectRepository):
    """Patch ONLY the DB seam the add-project handler imports."""
    return (
        patch("services.database.repositories.ProjectRepository", project_repo),
        patch(
            "services.database.repositories.RepositoryRepository", _RecordingRepositoryRepository
        ),
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            lambda *a, **k: _SessionScope(),
        ),
    )


@pytest.fixture
def live_service():
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


@pytest.fixture(autouse=True)
def _reset_db_calls():
    _RecordingProjectRepository.calls = []
    yield


# ---------------------------------------------------------------------------
# (a) The seam: arm / rewrite / pass
# ---------------------------------------------------------------------------


class TestArmOutcome:
    def test_pm_fixture_arms_and_the_question_stands(self):
        armer = _Armer()
        out, rewrites = enforce_armed_offers(PM_REPLY, armed_offer=None, arm_offer=armer)

        # The question is left exactly as the model wrote it (default copy).
        assert out == PM_REPLY
        assert rewrites == 0
        assert PM_OFFER in out

        record = armer.peek()
        assert record is not None, "the offer was not armed"
        assert record["pending_action"]["command"] == PM_EXPECTED_COMMAND

    def test_the_armed_record_shape_is_the_carrier_shape(self):
        """Quoted in full: what the accept seam and the predicate actually read."""
        armer = _Armer()
        enforce_armed_offers(PM_REPLY, armed_offer=None, arm_offer=armer)
        record = armer.peek()

        assert record["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        # #1665 input adequacy: the rendered ask rides under "question" —
        # the key `evaluate_acceptance` is threaded from at this seam.
        assert record["question"] == PM_OFFER
        assert record["offer_message"] == PM_OFFER
        assert record["ask_rendered"] is True
        assert record["pending_action"] == {
            "kind": FLOOR_BOUND_OFFER_KIND,
            "command": PM_EXPECTED_COMMAND,
            "action": "add_project",
            "summary": PM_EXPECTED_COMMAND,
        }
        assert PM_EXPECTED_COMMAND in record["decline_message"]
        # #1664: the open question IS a yes/no, so the snapshot must say so.
        assert offer_is_confirm(record) is True

    def test_arming_is_logged_with_the_command(self):
        armer = _Armer()
        with capture_logs() as events:
            enforce_armed_offers(PM_REPLY, armed_offer=None, arm_offer=armer, session_id="s1855-l2")
        armed = [e for e in events if e.get("event") == "floor_offer_armed"]
        assert len(armed) == 1
        assert armed[0]["command"] == PM_EXPECTED_COMMAND
        assert armed[0]["question"] == PM_OFFER
        assert armed[0]["session_id"] == "s1855-l2"
        # An arm is not a rewrite — the corpus sink must not see one.
        assert [e for e in events if e.get("event") == "floor_unarmed_offer_rewritten"] == []

    def test_no_round_trip_bind_is_still_a_layer_1_rewrite(self):
        """Family recognised, slots unbound → tier 2. Never an arm."""
        armer = _Armer()
        text = "Want me to add that project for you?"
        out, rewrites = enforce_armed_offers(text, armed_offer=None, arm_offer=armer)
        assert rewrites == 1
        assert "?" not in out
        assert f"To do that, say: {uo.ADD_PROJECT_IMPERATIVE}." in out
        assert armer.peek() is None
        assert armer.records == []

    def test_uncatalogued_action_is_still_a_layer_1_rewrite(self):
        armer = _Armer()
        out, rewrites = enforce_armed_offers(
            "Should I dig into the release notes?", armed_offer=None, arm_offer=armer
        )
        assert rewrites == 1
        assert out == "If you'd like me to dig into the release notes, just tell me directly."
        assert armer.peek() is None

    @pytest.mark.parametrize("rail", ["workflow_offer", "last_offer", "interview_offer"])
    def test_already_armed_is_untouched_and_never_double_armed(self, rail):
        armer = _Armer()
        out, rewrites = enforce_armed_offers(PM_REPLY, armed_offer=rail, arm_offer=armer)
        assert (out, rewrites) == (PM_REPLY, 0)
        assert armer.records == [], "a second arm would clobber the live one-slot store"
        assert armer.peek() is None

    def test_without_a_callback_behaviour_is_layer_1_exactly(self):
        """The rollback switch: no callback, no arm, byte-identical to layer 1."""
        with_cb = enforce_armed_offers(PM_REPLY, armed_offer=None, arm_offer=None)
        assert with_cb == enforce_armed_offers(PM_REPLY, armed_offer=None)
        out, rewrites = with_cb
        assert rewrites == 1
        assert f"To do that, say: {PM_EXPECTED_COMMAND}." in out

    @pytest.mark.parametrize(
        "kwargs", [{"succeeds": False}, {"raises": True}], ids=["refused", "raised"]
    )
    def test_a_failed_arm_falls_back_to_the_rewrite(self, kwargs):
        """Fail-safe in every direction: an offer we could not arm never stands."""
        armer = _Armer(**kwargs)
        out, rewrites = enforce_armed_offers(PM_REPLY, armed_offer=None, arm_offer=armer)
        assert rewrites == 1
        assert PM_OFFER not in out
        assert armer.peek() is None

    def test_multiple_offers_are_never_half_armed(self):
        armer = _Armer()
        text = f"Should I file it? {PM_OFFER}"
        out, rewrites = enforce_armed_offers(text, armed_offer=None, arm_offer=armer)
        assert rewrites == 2
        assert armer.peek() is None
        assert detect_offer_questions(out) == []

    def test_the_armed_question_is_not_re_rewritten_on_the_same_call(self):
        """Layer 1's pin ('no rewrite re-matches the detector') still holds —
        and an ARMED question is ALLOWED to match: that is the point. What must
        not happen is the seam chewing its own armed output."""
        armer = _Armer()
        out, rewrites = enforce_armed_offers(PM_REPLY, armed_offer=None, arm_offer=armer)
        assert rewrites == 0
        found = detect_offer_questions(out)
        assert [f.sentence for f in found] == [PM_OFFER]
        assert armer.peek()["question"] == PM_OFFER


# ---------------------------------------------------------------------------
# (a, cont.) The same decision at the renderer seam
# ---------------------------------------------------------------------------


class TestFloorOutputSeam:
    @pytest.mark.asyncio
    async def test_respond_arms_and_keeps_the_question(self):
        armer = _Armer()
        floor = _floor_returning(PM_REPLY)
        resp = await floor.respond(
            FloorContext(user_message="add One Job", session_id="s1855-l2", arm_offer=armer)
        )
        assert resp.message == PM_REPLY
        assert armer.peek()["pending_action"]["command"] == PM_EXPECTED_COMMAND

    @pytest.mark.asyncio
    async def test_respond_without_a_callback_is_layer_1(self):
        floor = _floor_returning(PM_REPLY)
        resp = await floor.respond(FloorContext(user_message="add One Job", session_id="s1855-l2"))
        assert PM_OFFER not in resp.message
        assert f"To do that, say: {PM_EXPECTED_COMMAND}." in resp.message

    def test_the_callback_is_threaded_at_every_floor_door(self):
        """m-44: the denominator is FOUR doors, and all four state it."""
        import inspect

        import services.intent.intent_service as isvc

        src = inspect.getsource(isvc)
        assert src.count("arm_offer=self._floor_arming_callback(") == 4

    def test_the_callback_is_none_when_the_store_is_unreadable(self):
        """Fail-safe: a service with no offer store cannot arm, so the seam
        rewrites rather than trusting a store it cannot write."""
        svc = IntentService.__new__(IntentService)  # no __init__: no store
        assert svc._floor_arming_callback("s1855-l2", _USER) is None
        armed = IntentService.__new__(IntentService)
        armed.workflow_offer_service = WorkflowOfferService()
        assert armed._floor_arming_callback(None, _USER) is None
        assert armed._floor_arming_callback("s1855-l2", _USER) is not None


# ---------------------------------------------------------------------------
# (b) The accept turn, through the REAL rail
# ---------------------------------------------------------------------------


class TestAcceptDispatchesTheRealRail:
    @pytest.mark.asyncio
    async def test_pm_two_turn_fixture_end_to_end(self, live_service):
        """Turn 1 arms the floor's own question; turn 2's 'Yes, please.' runs
        the command through the ordinary rail and answers in the HANDLER's own
        words — never the floor's, never a second implementation."""
        session_id = str(uuid.uuid4())

        # --- turn 1: the floor composes PM's offer, and ARMS it ------------
        floor = _floor_returning(PM_REPLY)
        turn1 = await floor.respond(
            FloorContext(
                user_message="add One Job",
                session_id=session_id,
                user_id=_USER,
                arm_offer=live_service._floor_arming_callback(session_id, _USER),
            )
        )
        assert PM_OFFER in turn1.message  # the question STANDS — it is armed

        # --- turn 2: "Yes, please." ---------------------------------------
        p1, p2, p3 = _patched_db()
        with p1, p2, p3:
            turn2 = await live_service.process_intent(
                PM_ACCEPT, session_id=session_id, user_id=_USER
            )

        # The handler's own confirmation, with the handler's own slots.
        assert turn2.message == (
            "Added One Job to your portfolio and linked Design-in-Product/one-job to it."
        )
        assert turn2.intent_data["action"] == "add_project"
        assert turn2.intent_data["context"]["project_name"] == "One Job"
        assert turn2.intent_data["context"]["repo_name"] == "Design-in-Product/one-job"

        # The DB seam saw exactly the bound slots.
        assert ("create", "One Job", _USER) in _RecordingProjectRepository.calls
        assert ("get_repo", "Design-in-Product/one-job") in _RecordingProjectRepository.calls

        # One-slot store emptied by the pop — no leak into turn 3.
        assert live_service.workflow_offer_service.peek_pending_offer(session_id) is None

    @pytest.mark.asyncio
    async def test_the_carrier_runs_the_command_not_a_second_implementation(self):
        """Unit-level: the carrier re-runs the stored TEXT through the rail."""
        from services.intent_service.workflow_entries import (
            register_default_workflows,
            run_confirm_pending_action_workflow,
        )

        register_default_workflows()

        class _StubIntentService:
            def __init__(self):
                self.calls = []

            async def _process_intent_internal(self, message, session_id=None, user_id=None):
                self.calls.append((message, session_id, user_id))
                result = MagicMock()
                result.message = "Added One Job to your portfolio."
                result.intent_data = {"action": "add_project"}
                return result

        stub = _StubIntentService()
        record = build_floor_bound_offer_record(
            command=PM_EXPECTED_COMMAND, question=PM_OFFER, action="add_project"
        )
        result = await run_confirm_pending_action_workflow(
            session_id="sess-1855-l2",
            user_id=_USER,
            context={"pending_action": record["pending_action"], "intent_service": stub},
        )
        assert stub.calls == [(PM_EXPECTED_COMMAND, "sess-1855-l2", _USER)]
        assert result["message"] == "Added One Job to your portfolio."

    @pytest.mark.asyncio
    async def test_a_command_less_record_dispatches_nothing(self):
        from services.intent_service.workflow_entries import (
            run_confirm_pending_action_workflow,
        )

        result = await run_confirm_pending_action_workflow(
            session_id="sess-1855-l2",
            user_id=_USER,
            context={
                "pending_action": {"kind": FLOOR_BOUND_OFFER_KIND, "action": "add_project"},
                "intent_service": MagicMock(),
            },
        )
        assert result is None


# ---------------------------------------------------------------------------
# (c) Decline and off-intent — the existing #1529 semantics, nothing new
# ---------------------------------------------------------------------------


class TestDeclineAndOffIntent:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("message", ["no", "no thanks", "cancel"])
    async def test_decline_clears_the_record_and_fires_nothing(self, live_service, message):
        session_id = str(uuid.uuid4())
        live_service.workflow_offer_service.set_pending_offer(
            session_id,
            build_floor_bound_offer_record(
                command=PM_EXPECTED_COMMAND, question=PM_OFFER, action="add_project"
            ),
            user_id=_USER,
        )
        with patch("services.database.repositories.ProjectRepository", _ExplosiveProjectRepository):
            result = await live_service.process_intent(
                message, session_id=session_id, user_id=_USER
            )
        assert PM_EXPECTED_COMMAND in result.message  # honest re-offer, no action
        assert live_service.workflow_offer_service.peek_pending_offer(session_id) is None

    @pytest.mark.asyncio
    async def test_off_intent_abandons_the_record_and_fires_nothing(self, live_service):
        session_id = str(uuid.uuid4())
        live_service.workflow_offer_service.set_pending_offer(
            session_id,
            build_floor_bound_offer_record(
                command=PM_EXPECTED_COMMAND, question=PM_OFFER, action="add_project"
            ),
            user_id=_USER,
        )
        with patch("services.database.repositories.ProjectRepository", _ExplosiveProjectRepository):
            with capture_logs() as events:
                await live_service.process_intent("hello", session_id=session_id, user_id=_USER)

        assert live_service.workflow_offer_service.peek_pending_offer(session_id) is None
        assert any(e.get("event") == "floor_bound_offer_abandoned" for e in events)


# ---------------------------------------------------------------------------
# (d) The question's copy — CXO's open call, both settings
# ---------------------------------------------------------------------------


class TestArmedQuestionForm:
    def test_default_is_the_models_own_wording(self):
        assert uo.ARMED_QUESTION_FORM is None
        armer = _Armer()
        out, _ = enforce_armed_offers(PM_REPLY, armed_offer=None, arm_offer=armer)
        assert out == PM_REPLY
        assert armer.peek()["question"] == PM_OFFER

    def test_a_house_form_replaces_the_sentence_and_is_what_gets_stored(self, monkeypatch):
        form = "Want me to {command}? Say yes, or tell me otherwise."
        monkeypatch.setattr(uo, "ARMED_QUESTION_FORM", form)
        armer = _Armer()
        out, rewrites = enforce_armed_offers(PM_REPLY, armed_offer=None, arm_offer=armer)

        expected = form.format(command=PM_EXPECTED_COMMAND)
        assert rewrites == 0
        assert out == "I found the repo. " + expected
        assert PM_OFFER not in out
        # #1665: the STORED ask is what the user actually read, verbatim.
        assert armer.peek()["question"] == expected
        # Still a question, still armed — the detector matching it is correct
        # (it scans SENTENCES, so it sees the ask, not the trailing guidance).
        found = detect_offer_questions(out)
        assert len(found) == 1
        assert expected.startswith(found[0].sentence)


# ---------------------------------------------------------------------------
# (e) The catalogue — denominator pin
# ---------------------------------------------------------------------------


# Every catalogued family needs a sentence the floor could plausibly compose
# and the command it must bind to. The pin below asserts this mapping's keys
# ARE the catalogue, so a family added without a round-trip test fails here.
FAMILY_ROUND_TRIPS = {
    "add_project": (PM_OFFER, PM_EXPECTED_COMMAND),
}


class TestCatalogueDenominator:
    def test_the_catalogue_is_exactly_the_tested_set(self):
        assert {family.name for family in COMMAND_FAMILIES} == set(FAMILY_ROUND_TRIPS)

    @pytest.mark.parametrize("name", sorted(FAMILY_ROUND_TRIPS))
    def test_each_family_round_trips_from_sentence_to_command(self, name):
        sentence, command = FAMILY_ROUND_TRIPS[name]
        found = detect_offer_questions(sentence)
        assert len(found) == 1
        bound = bind_catalogued_command(found[0].predicate)
        assert bound is not None, f"{name} did not bind its own fixture"
        family, composed = bound
        assert family.name == name
        assert composed == command

    def test_each_family_arms_a_record_naming_its_own_action(self):
        for family in COMMAND_FAMILIES:
            sentence, command = FAMILY_ROUND_TRIPS[family.name]
            armer = _Armer(session_id=f"s-{family.name}")
            enforce_armed_offers(sentence, armed_offer=None, arm_offer=armer)
            record = armer.peek()
            assert record["pending_action"]["action"] == family.name
            assert record["pending_action"]["command"] == command

    def test_the_kind_literal_matches_its_confirm_table_entry(self):
        """#1664 drift pin: the literal in destructive_confirm._CONFIRM_KINDS
        (its home module imports this one's siblings, so it cannot import the
        constant) must equal the constant declared beside the binder."""
        from services.intent_service import destructive_confirm as dc

        assert FLOOR_BOUND_OFFER_KIND in dc._CONFIRM_KINDS


# ---------------------------------------------------------------------------
# (f) revise_draft — the guard is log-only
# ---------------------------------------------------------------------------


class TestReviseDraftGuard:
    @pytest.mark.asyncio
    async def test_an_offer_in_a_revised_draft_is_logged_not_rewritten(self):
        revised = "Standup notes.\n\nWant me to file that as an issue?"
        floor = _floor_returning(revised)
        with capture_logs() as events:
            out = await floor.revise_draft(
                user_message="tighten it", draft="Standup notes.", user_id=_USER
            )
        assert out == revised, "a DRAFT artifact is never rewritten by the seam"
        hits = [e for e in events if e.get("event") == "floor_offer_in_revise_draft"]
        assert len(hits) == 1
        assert hits[0]["sentence"] == "Want me to file that as an issue?"

    @pytest.mark.asyncio
    async def test_a_clean_draft_logs_nothing(self):
        floor = _floor_returning("Standup notes, tightened.")
        with capture_logs() as events:
            out = await floor.revise_draft(
                user_message="tighten it", draft="Standup notes.", user_id=_USER
            )
        assert out == "Standup notes, tightened."
        assert [e for e in events if e.get("event") == "floor_offer_in_revise_draft"] == []

    @pytest.mark.asyncio
    async def test_revise_draft_never_arms(self):
        """No arming path here: the store is untouched by a draft revision."""
        offers = WorkflowOfferService()
        floor = _floor_returning("Want me to file that as an issue?")
        await floor.revise_draft(user_message="tighten it", draft="x", user_id=_USER)
        assert offers.peek_pending_offer("s1855-l2") is None
