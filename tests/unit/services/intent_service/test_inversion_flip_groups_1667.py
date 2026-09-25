"""#1667 — the flip UNIT moves onto the rail entry, and the flag widens.

What flip-1 could express and what it needed to express had diverged: the
per-category flag addressed 33 of 93 rail READ keys (the decision doc says 23,
measured against ACTION_REGISTRY's direct action names; the live path also
back-maps aliases — see the --audit report's note), leaving most of wave 1
unreachable by any flag value. ``WorkflowEntry.flip_group`` makes the flip unit
the operation's own, and ``PIPER_INVERSION_LIVE_CATEGORIES`` (name kept,
semantics widened) now accepts a GROUP name, an OPERATION name, or a registry
CATEGORY.

Pinned here:

1. Declaration — the group vocabulary is closed, and a non-READ entry carrying
   a group is UNCONSTRUCTIBLE (not merely guarded downstream). The wave-1
   assignments themselves are pinned by class, not by exhaustive list, so
   adding an op to a group doesn't break the suite but removing the invariant
   does.
2. Flag resolution — group-name flip, single-op-name flip, canonical-alias
   flip, registry-category flip (flip-1's unit, unregressed), and the
   precedence REPORTED when several match.
3. Live consult — each of the three surfaces dispatches end-to-end through the
   real consult; an UNGROUPED op does NOT dispatch even when its group-mates
   are live; default-empty is still byte-identically dark.
4. Audit — the coverage report lists unassigned ops BY NAME with denominators,
   and re-measures the READ-only invariant rather than asserting it.

Idioms inherited from test_inversion_live_1595.py (deterministic router fake,
explosive LLM boundary, real stores over aiosqlite, call-time env reads).
"""

import contextlib
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import SessionActivityDB  # noqa: E402
from services.domain.models import Intent  # noqa: E402
from services.intent_service import inversion_live  # noqa: E402
from services.intent_service.inversion_live import (  # noqa: E402
    consult_inversion_live,
    live_categories,
    resolve_live_match,
    unrecognized_flag_tokens,
)
from services.intent_service.inversion_router import (  # noqa: E402
    RoutingDecision,
    derive_routing_grammar,
)
from services.intent_service.soft_invocation import WorkflowOfferService  # noqa: E402
from services.intent_service.workflow_dispatcher import (  # noqa: E402
    FLIP_GROUPS,
    WorkflowEntry,
    get_action_workflows,
)
from services.intent_service.workflow_entries import (  # noqa: E402
    register_default_workflows,
)
from services.shared_types import EffectClass, IntentCategory  # noqa: E402

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))

import inversion_phase2_gate as gate  # noqa: E402

_USER = "3f7b8a52-1667-4b00-9e00-000000002202"
_SESSION = "sess-1667-flip2"
_MSG = "what did we create this session?"

# The probe operations, chosen for what they PROVE, not for convenience:
#   - session_activity_query: read_status AND registry category QUERY — the op
#     flip-1's pins already use, so all three surfaces can be compared on it.
#   - show_standup: read_status with NO registry category — #1667's own
#     headline example; unreachable by any category flag before this change.
# strategic_planning USED to be the "unassigned stays unaddressable by a
# wave" probe; wave 3 (#1595, 2026-09-25) grouped it into read_strategic,
# so no real op is ungrouped anymore (see
# test_no_real_read_op_is_ungrouped_after_wave_3 below) — that pin now runs
# against an injected synthetic op instead, same idiom as the b-list pin
# wave 2 already converted.
_STATUS_OP = "session_activity_query"
_NO_CATEGORY_OP = "show_standup"


# ---------------------------------------------------------------------------
# Fixtures (the #1595 flip-1 set)
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def sm(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: SessionActivityDB.__table__.create(c, checkfirst=True))
    maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with maker() as s:
            yield s

    import services.database.session_factory as sf

    monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    yield maker
    await engine.dispose()


@pytest.fixture
def mem_prefs(monkeypatch):
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    return store


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    monkeypatch.delenv("PIPER_INVERSION_LIVE_CATEGORIES", raising=False)
    monkeypatch.delenv("PIPER_INVERSION_LIVE_MIN_CONFIDENCE", raising=False)
    monkeypatch.delenv("PIPER_INVERSION_SHADOW", raising=False)


@pytest.fixture(autouse=True)
def _rail_registered():
    register_default_workflows()


@pytest.fixture
def svc():
    return SimpleNamespace(workflow_offer_service=WorkflowOfferService(), intent_classifier=None)


class _LogRecorder:
    def __init__(self):
        self.events = []

    def _rec(self, level):
        def _log(event, **fields):
            self.events.append((level, event, fields))

        return _log

    def __getattr__(self, name):
        if name in ("info", "warning", "error", "debug"):
            return self._rec(name)
        raise AttributeError(name)

    def decisions(self):
        return [(lvl, f) for lvl, ev, f in self.events if ev == "inversion_live_decision"]


@pytest.fixture
def log_rec(monkeypatch):
    rec = _LogRecorder()
    monkeypatch.setattr(inversion_live, "logger", rec)
    return rec


def _stub_route(monkeypatch, decision):
    from services.intent_service import inversion_router as ir

    calls = []

    async def _route(utterance, session_state=None, **kwargs):
        calls.append(SimpleNamespace(utterance=utterance, session_state=session_state))
        return decision

    monkeypatch.setattr(ir, "route", _route)
    return calls


def _explosive_route(monkeypatch):
    from services.intent_service import inversion_router as ir

    async def _boom(*a, **k):
        raise AssertionError("inversion router consulted — must not be on this path")

    monkeypatch.setattr(ir, "route", _boom)


def _explosive_snapshot(monkeypatch):
    from services.intent_service import snapshot_assembly as sa

    async def _boom(*a, **k):
        raise AssertionError("snapshot assembled — flag-off consult must do zero work")

    monkeypatch.setattr(sa, "assemble_session_snapshot", _boom)


def _decision(operation=_STATUS_OP, confidence=0.9):
    return RoutingDecision(outcome="operation", operation=operation, confidence=confidence)


async def _consult(svc, monkeypatch, log_rec, *, cats, operation, confidence=0.9):
    monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", cats)
    calls = _stub_route(monkeypatch, _decision(operation, confidence))
    out = await consult_inversion_live(_MSG, session_id=_SESSION, user_id=_USER, intent_service=svc)
    return out, calls, log_rec.decisions()


# ---------------------------------------------------------------------------
# 1. DECLARATION — the flip unit lives on the entry, READ-only by construction
# ---------------------------------------------------------------------------


class TestFlipGroupDeclaration:
    def test_default_is_ungrouped(self):
        """The safe direction: an entry that says nothing is addressable by no
        wave. A forgotten assignment can only ever UNDER-flip."""
        entry = WorkflowEntry(entry_point=lambda **k: None, effect=EffectClass.READ)
        assert entry.flip_group is None

    @pytest.mark.parametrize("effect", [EffectClass.WRITE, EffectClass.DESTRUCTIVE])
    def test_non_read_entry_with_flip_group_is_unconstructible(self, effect):
        """THE load-bearing pin. The runtime effect guard in inversion_live is
        the belt; this is the structural guarantee — a flippable write cannot
        be brought into existence, so no flag value can produce one."""
        with pytest.raises(ValueError) as exc:
            WorkflowEntry(
                entry_point=lambda **k: None,
                effect=effect,
                flip_group="read_status",
                description="a write pretending it can flip",
            )
        msg = str(exc.value)
        assert "read_status" in msg and effect.name in msg
        assert "READ-only" in msg  # says WHY, not just "invalid"

    def test_unknown_group_name_rejected_loudly(self):
        """A typo is doubly silent otherwise: the op becomes unaddressable AND
        the flag token that names the intended group matches nothing."""
        with pytest.raises(ValueError) as exc:
            WorkflowEntry(
                entry_point=lambda **k: None,
                effect=EffectClass.READ,
                flip_group="read_stauts",
            )
        assert "read_stauts" in str(exc.value)
        assert "read_status" in str(exc.value)  # lists the known vocabulary

    def test_wave_1_vocabulary(self):
        # #1595 wave 2 (2026-09-25): read_temporal joined the closed
        # vocabulary. #1595 wave 3 (2026-09-25): read_strategic joined it
        # too — this assertion is the CLOSED-set pin, so it must grow with
        # the vocabulary, not stay wave-1-only. FLIP_GROUPS now has 5
        # members.
        assert FLIP_GROUPS == frozenset(
            {
                "read_status",
                "read_referent",
                "read_synthesis",
                "read_temporal",
                "read_strategic",
            }
        )

    def test_every_grouped_rail_entry_is_read(self):
        """The invariant re-measured over the REAL registry, not just the
        constructor: whatever registration paths exist, nothing non-READ ends
        up grouped."""
        offenders = {
            k: (e.effect.name, e.flip_group)
            for k, e in get_action_workflows().items()
            if e.flip_group is not None and e.effect != EffectClass.READ
        }
        assert offenders == {}

    def test_wave_1_assignments_by_class(self):
        """Pins the CLASSES the decision named, not an exhaustive list — a
        later wave adding members must not have to edit this test, but losing
        one of these must fail."""
        rail = get_action_workflows()
        for op in (
            "show_standup",
            "list_projects",
            "list_issues",
            "list_archived_projects",
            "get_default_repo",
            "local_git_status_query",
            "attention_query",
        ):
            assert rail[op].flip_group == "read_status", op
        for op in ("review_issue", "analyze_commits", "analyze_data", "generate_report"):
            assert rail[op].flip_group == "read_referent", op
        for op in ("summarize_document", "summarize_file"):
            assert rail[op].flip_group == "read_synthesis", op
        # There are no deliberately-ungrouped READ ops left. changes_query/
        # week_calendar moved to read_temporal in wave 2 (#1595, 2026-09-25,
        # pinned in TestWaveTwoReadTemporal below); strategic_planning/
        # learn_pattern/prioritize/generate_content (plus their aliases
        # create_plan/detect_pattern/set_priorities/create_content) moved to
        # read_strategic in wave 3 (#1595, 2026-09-25, pinned in
        # TestWaveThreeReadStrategic below). The honest "reads done" line for
        # epic 0: of the 93 READ rail keys, zero are ungrouped.
        ungrouped_reads = {
            k for k, e in rail.items() if e.effect == EffectClass.READ and e.flip_group is None
        }
        assert (
            ungrouped_reads == set()
        ), f"{len(ungrouped_reads)}/93 READ keys still ungrouped: {sorted(ungrouped_reads)}"

    def test_aliases_inherit_their_entrys_group(self):
        """Aliases share the entry object, so a wave that names a group flips
        the paraphrase emissions too — the mode-4 defense keeps working."""
        rail = get_action_workflows()
        assert rail["get_standup"].flip_group == rail["show_standup"].flip_group
        assert rail["show_issue"].flip_group == rail["review_issue"].flip_group


# ---------------------------------------------------------------------------
# 2. FLAG RESOLUTION — three naming surfaces, one flag
# ---------------------------------------------------------------------------


class TestFlagResolution:
    def test_default_empty_unchanged(self):
        assert live_categories() == frozenset()

    def test_group_and_op_tokens_normalize_like_categories(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", " read_status , show_standup ,QUERY,")
        assert live_categories() == frozenset({"READ_STATUS", "SHOW_STANDUP", "QUERY"})

    def test_match_by_group(self):
        assert (
            resolve_live_match(
                operation="show_standup",
                canonical="show_standup",
                flip_group="read_status",
                category=None,
                cats=frozenset({"READ_STATUS"}),
            )
            == "group"
        )

    def test_match_by_operation_name(self):
        assert (
            resolve_live_match(
                operation="show_standup",
                canonical="show_standup",
                flip_group=None,
                category=None,
                cats=frozenset({"SHOW_STANDUP"}),
            )
            == "operation"
        )

    def test_match_by_canonical_when_alias_emitted(self):
        assert (
            resolve_live_match(
                operation="get_standup",
                canonical="show_standup",
                flip_group=None,
                category=None,
                cats=frozenset({"SHOW_STANDUP"}),
            )
            == "operation"
        )

    def test_match_by_registry_category_still_works(self):
        """flip-1's unit, unregressed."""
        assert (
            resolve_live_match(
                operation="session_activity_query",
                canonical="session_activity_query",
                flip_group="read_status",
                category="QUERY",
                cats=frozenset({"QUERY"}),
            )
            == "category"
        )

    def test_no_match_is_none(self):
        assert (
            resolve_live_match(
                operation="show_standup",
                canonical="show_standup",
                flip_group="read_status",
                category="QUERY",
                cats=frozenset({"READ_REFERENT"}),
            )
            is None
        )

    def test_reported_precedence_is_most_specific_first(self):
        """When several surfaces match, telemetry names the most specific —
        so an operator reverting knows which token did it."""
        cats = frozenset({"SHOW_STANDUP", "READ_STATUS", "QUERY"})
        assert (
            resolve_live_match(
                operation="show_standup",
                canonical="show_standup",
                flip_group="read_status",
                category="QUERY",
                cats=cats,
            )
            == "operation"
        )
        assert (
            resolve_live_match(
                operation="show_standup",
                canonical="show_standup",
                flip_group="read_status",
                category="QUERY",
                cats=frozenset({"READ_STATUS", "QUERY"}),
            )
            == "group"
        )

    def test_unrecognized_tokens_reported(self):
        """A typo'd token would otherwise be perfectly silent."""
        grammar = derive_routing_grammar()
        cats = frozenset({"READ_STATUS", "SHOW_STANDUP", "QUERY", "READ_STAUTS"})
        assert unrecognized_flag_tokens(cats, grammar) == ["READ_STAUTS"]


# ---------------------------------------------------------------------------
# 3. LIVE CONSULT — each surface dispatches; ungrouped never does
# ---------------------------------------------------------------------------


class TestLiveConsultSurfaces:
    async def test_group_name_flips_a_no_category_op(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """#1667's headline case: show_standup has NO registry category, so no
        value of flip-1's flag could reach it. Naming its GROUP does."""
        out, calls, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="read_status", operation=_NO_CATEGORY_OP
        )
        assert isinstance(out, Intent)
        assert out.action == _NO_CATEGORY_OP
        assert len(calls) == 1
        assert f["route"] == "inversion" and f["reason"] is None
        assert f["live_match"] == "group"
        assert f["flip_group"] == "read_status"
        assert f["category"] is None

    async def test_no_category_op_gets_the_query_shape_category(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The Intent still needs a category field. With no registry row to
        read, it is QUERY — the read-only-retrieval member — chosen AFTER the
        effect guard proved the op is declared READ. The rail dispatches on
        action before category routing, so this picks no handler."""
        out, _, _ = await _consult(
            svc, monkeypatch, log_rec, cats="read_status", operation=_NO_CATEGORY_OP
        )
        assert out.category is IntentCategory.QUERY

    async def test_single_op_name_flips_exactly_that_op(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """A surgical flip needs no group at all."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats=_NO_CATEGORY_OP, operation=_NO_CATEGORY_OP
        )
        assert isinstance(out, Intent) and f["live_match"] == "operation"

    async def test_single_op_flip_does_not_flip_its_group_mates(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """Naming ONE op must not sweep its group in — otherwise the surgical
        flip is a wave flip wearing a smaller name."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats=_NO_CATEGORY_OP, operation="list_projects"
        )
        assert out is None
        assert f["live_match"] is None
        assert f["flip_group"] == "read_status"  # same group, still legacy

    async def test_registry_category_flip_still_works(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """flip-1's deploy string keeps its exact meaning."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="QUERY", operation=_STATUS_OP
        )
        assert isinstance(out, Intent)
        assert f["live_match"] == "category" and f["category"] == "QUERY"
        assert out.category is IntentCategory.QUERY

    async def test_ungrouped_op_never_dispatches_when_group_mates_are_live(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The AC's opt-in pin. Every named group live at once; an UNGROUPED
        READ op still takes legacy — unaddressable by design, not by
        accident. strategic_planning was this probe through wave 2; wave 3
        (#1595, 2026-09-25) grouped it into read_strategic (see
        TestWaveThreeReadStrategic), so — same idiom as the b-list pin
        below — this now runs against an injected synthetic op with no
        group and no registry category, so no category token can reach it
        either."""
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY

        synthetic_op = "_test_ungrouped_uncategorized_op_1667"
        monkeypatch.setitem(
            WORKFLOW_REGISTRY,
            synthetic_op,
            WorkflowEntry(
                entry_point=lambda **k: None,
                effect=EffectClass.READ,
                description="synthetic — ungrouped, uncategorized (test only)",
                action_triggered=True,
            ),
        )
        out, _, [(_, f)] = await _consult(
            svc,
            monkeypatch,
            log_rec,
            cats="read_status,read_referent,read_synthesis,read_temporal,read_strategic",
            operation=synthetic_op,
        )
        assert out is None
        assert f["live_match"] is None
        assert f["flip_group"] is None
        assert f["reason"] == "not_live_uncategorized"  # renamed #1670

    async def test_ungrouped_op_with_a_category_is_still_swept_by_that_category(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The honest converse, pinned so nobody reads 'ungrouped' as 'safe'.
        Wave 1 pinned this against week_calendar; wave 2 (#1595, 2026-09-25)
        grouped week_calendar into read_temporal, which — as designed —
        emptied the audit's b-list (0 ungrouped-but-categorized READ ops
        remain live). The property itself doesn't stop being true just
        because no PRODUCTION op currently exemplifies it, so this pins it
        against an injected synthetic op instead of a real one: an
        ungrouped READ rail entry carrying an ACTION_REGISTRY category still
        gets swept by a CATEGORY flip."""
        from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY

        synthetic_op = "_test_ungrouped_categorized_op_1667"
        monkeypatch.setitem(
            WORKFLOW_REGISTRY,
            synthetic_op,
            WorkflowEntry(
                entry_point=lambda **k: None,
                effect=EffectClass.READ,
                description="synthetic — ungrouped, categorized (test only)",
                action_triggered=True,
            ),
        )
        monkeypatch.setitem(ACTION_REGISTRY, ("QUERY", synthetic_op), ActionDisposition.WORKFLOW)

        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="QUERY", operation=synthetic_op
        )
        assert isinstance(out, Intent)
        assert f["live_match"] == "category" and f["flip_group"] is None

    def test_no_real_read_op_is_ungrouped_but_categorized_after_wave_2(self):
        """States the design outcome directly, over the real registry: after
        wave 2 the audit's b-list (ungrouped READ ops that still carry an
        ACTION_REGISTRY category) is empty — every category-carrying READ op
        was either wave-1-grouped or is now read_temporal. The strategic
        cohort (wave 3's own scope) carries no registry category at all."""
        from services.intent_service.inversion_live import _category_by_operation
        from services.intent_service.inversion_router import derive_routing_grammar

        grammar = derive_routing_grammar()
        cat_by_op = _category_by_operation(grammar)
        rail = get_action_workflows()
        b_list = [
            k
            for k, e in rail.items()
            if e.effect == EffectClass.READ and e.flip_group is None and k in cat_by_op
        ]
        assert b_list == []

    def test_no_real_read_op_is_ungrouped_after_wave_3(self):
        """States wave 3's design outcome directly, over the real registry:
        after wave 3 the ungrouped READ list — group OR category, either
        one — is empty. Denominator stated: 0 of 93 READ rail keys are
        ungrouped (`scripts/inversion_phase2_gate.py --audit` prints the
        same number). This is the a-list closing to zero, the sibling of
        test_no_real_read_op_is_ungrouped_but_categorized_after_wave_2's
        b-list closing to zero."""
        rail = get_action_workflows()
        read_keys = {k: e for k, e in rail.items() if e.effect == EffectClass.READ}
        ungrouped = [k for k, e in read_keys.items() if e.flip_group is None]
        assert (
            ungrouped == []
        ), f"{len(ungrouped)}/{len(read_keys)} READ keys still ungrouped: {sorted(ungrouped)}"

    async def test_write_never_flips_by_any_surface(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        """Belt, restated for the widened flag: naming a WRITE op directly —
        the most explicit request possible — still cannot flip it."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="create_issue", operation="create_issue"
        )
        assert out is None
        assert f["reason"] == "not_read_effect"
        assert f["live_match"] == "operation"  # named live, and STILL refused

    async def test_sub_threshold_still_blocks_a_group_flip(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        out, _, [(_, f)] = await _consult(
            svc,
            monkeypatch,
            log_rec,
            cats="read_status",
            operation=_NO_CATEGORY_OP,
            confidence=0.5,
        )
        assert out is None and f["reason"] == "sub_threshold"

    async def test_default_empty_still_byte_identically_dark(self, monkeypatch, svc, log_rec):
        """Unchanged by the widening: unset ⇒ zero work, not even a log line.
        (Explosive snapshot AND explosive router — the group lookup must not
        have introduced work before the flag check.)"""
        _explosive_snapshot(monkeypatch)
        _explosive_route(monkeypatch)
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is None
        assert log_rec.events == []

    async def test_group_flip_dispatches_through_the_real_rail_e2e(
        self, sm, mem_prefs, monkeypatch
    ):
        """End-to-end over the real process_intent: a GROUP flip routes the
        turn to the same handler the legacy chain reaches, with the classifier
        consult replaced."""
        from services.intent.intent_service import IntentService
        from services.intent_service.classifier import IntentClassifier

        class _ExplosiveLLM:
            def __getattr__(self, name):
                raise AssertionError(f"LLM boundary touched ({name})")

        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_status")
        calls = _stub_route(monkeypatch, _decision(_STATUS_OP, 0.9))
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))

        async def _boom(*a, **k):
            raise AssertionError("classify_multiple consulted — the flip must replace it")

        monkeypatch.setattr(service.intent_classifier, "classify_multiple", _boom)
        result = await service.process_intent(message=_MSG, session_id=_SESSION, user_id=_USER)
        assert len(calls) == 1
        assert result.success is True
        assert result.intent_data["action"] == _STATUS_OP
        assert result.message == "We haven't created anything in this session yet."


# ---------------------------------------------------------------------------
# 3b. WAVE 2 — read_temporal (#1595 epic-0 scope doc, 2026-09-25)
# ---------------------------------------------------------------------------

# The changes_query alias family (one shared entry) + the calendar cohort
# (three shared entries: meeting_time / recurring_meetings / week_calendar).
# 13 rail keys, not 12 — the epic-0 scope doc's dispatch prompt undercounted
# the calendar cohort by one; the real audit (run below) is the source of
# truth, not the estimate.
_READ_TEMPORAL_KEYS = frozenset(
    {
        "changes_query",
        "what_changed",
        "show_changes",
        "changes_since",
        "meeting_time",
        "how_much_time_in_meetings",
        "calendar_analysis",
        "recurring_meetings",
        "review_recurring_meetings",
        "audit_meetings",
        "week_calendar",
        "week_ahead",
        "whats_my_week_like",
    }
)


class TestWaveTwoReadTemporal:
    def test_all_thirteen_keys_carry_read_temporal(self):
        """(a) Every temporal rail key the wave-2 grouping was meant to reach
        actually carries the group — the assignment, not just the audit
        count."""
        rail = get_action_workflows()
        for op in _READ_TEMPORAL_KEYS:
            assert rail[op].flip_group == "read_temporal", op

    def test_every_read_temporal_entry_is_read(self):
        """(b) The READ-only invariant, re-asserted for the new group
        specifically (not just the whole-registry sweep in
        TestFlipGroupDeclaration.test_every_grouped_rail_entry_is_read)."""
        rail = get_action_workflows()
        offenders = {
            k: e.effect.name
            for k, e in rail.items()
            if e.flip_group == "read_temporal" and e.effect != EffectClass.READ
        }
        assert offenders == {}

    def test_read_temporal_keys_count_matches_group_membership(self):
        """No stray key outside the pinned set carries read_temporal, and
        none of the pinned set is missing — the set is exact, not a subset
        check."""
        rail = get_action_workflows()
        actual = {k for k, e in rail.items() if e.flip_group == "read_temporal"}
        assert actual == _READ_TEMPORAL_KEYS

    def test_flag_recognizes_read_temporal_token(self, monkeypatch):
        """(c) The wave's own flag token resolves live — not just declared
        in FLIP_GROUPS, but usable at the flag-parsing layer."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_temporal")
        assert live_categories() == frozenset({"READ_TEMPORAL"})
        assert (
            resolve_live_match(
                operation="changes_query",
                canonical="changes_query",
                flip_group="read_temporal",
                category="QUERY",
                cats=frozenset({"READ_TEMPORAL"}),
            )
            == "group"
        )

    def test_typo_of_read_temporal_is_reported_unrecognized(self):
        """(c) A misspelled wave name is loud, not a silent no-op — the same
        contract test_unrecognized_tokens_reported pins for wave 1."""
        grammar = derive_routing_grammar()
        cats = frozenset({"READ_TEMPORL"})
        assert unrecognized_flag_tokens(cats, grammar) == ["READ_TEMPORL"]

    async def test_group_flip_dispatches_a_calendar_op_e2e(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """End-to-end (the same shape as the wave-1 group-flip pin): naming
        read_temporal reaches a calendar-cohort op through the real consult."""
        out, calls, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="read_temporal", operation="meeting_time"
        )
        assert isinstance(out, Intent)
        assert out.action == "meeting_time"
        assert len(calls) == 1
        assert f["route"] == "inversion" and f["live_match"] == "group"
        assert f["flip_group"] == "read_temporal"


# ---------------------------------------------------------------------------
# 3c. WAVE 3 — read_strategic (#1595 epic-0 scope doc, 2026-09-25)
# ---------------------------------------------------------------------------

# The last 8 ungrouped READ rail keys: strategic_planning/create_plan
# (one shared entry), learn_pattern/detect_pattern (one shared entry),
# prioritize/set_priorities (prioritization_entry), generate_content/
# create_content (generate_content_entry). This closes the ungrouped READ
# list to zero — the honest "reads done" line for epic 0.
_READ_STRATEGIC_KEYS = frozenset(
    {
        "strategic_planning",
        "create_plan",
        "learn_pattern",
        "detect_pattern",
        "prioritize",
        "set_priorities",
        "generate_content",
        "create_content",
    }
)


class TestWaveThreeReadStrategic:
    def test_all_eight_keys_carry_read_strategic(self):
        """(a) Every strategic rail key the wave-3 grouping was meant to
        reach actually carries the group — the assignment, not just the
        audit count."""
        rail = get_action_workflows()
        for op in _READ_STRATEGIC_KEYS:
            assert rail[op].flip_group == "read_strategic", op

    def test_every_read_strategic_entry_is_read(self):
        """(b) The READ-only invariant, re-asserted for the new group
        specifically (not just the whole-registry sweep in
        TestFlipGroupDeclaration.test_every_grouped_rail_entry_is_read)."""
        rail = get_action_workflows()
        offenders = {
            k: e.effect.name
            for k, e in rail.items()
            if e.flip_group == "read_strategic" and e.effect != EffectClass.READ
        }
        assert offenders == {}

    def test_read_strategic_keys_count_matches_group_membership(self):
        """No stray key outside the pinned set carries read_strategic, and
        none of the pinned set is missing — the set is exact, not a subset
        check."""
        rail = get_action_workflows()
        actual = {k for k, e in rail.items() if e.flip_group == "read_strategic"}
        assert actual == _READ_STRATEGIC_KEYS

    def test_flag_recognizes_read_strategic_token(self, monkeypatch):
        """(c) The wave's own flag token resolves live — not just declared
        in FLIP_GROUPS, but usable at the flag-parsing layer."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "read_strategic")
        assert live_categories() == frozenset({"READ_STRATEGIC"})
        assert (
            resolve_live_match(
                operation="strategic_planning",
                canonical="strategic_planning",
                flip_group="read_strategic",
                category=None,
                cats=frozenset({"READ_STRATEGIC"}),
            )
            == "group"
        )

    def test_typo_of_read_strategic_is_reported_unrecognized(self):
        """(c) A misspelled wave name is loud, not a silent no-op — the same
        contract test_unrecognized_tokens_reported pins for wave 1."""
        grammar = derive_routing_grammar()
        cats = frozenset({"READ_STRATEGC"})
        assert unrecognized_flag_tokens(cats, grammar) == ["READ_STRATEGC"]

    async def test_group_flip_dispatches_a_strategic_op_e2e(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """End-to-end (the same shape as the wave-1/wave-2 group-flip pins):
        naming read_strategic reaches strategic_planning through the real
        consult."""
        out, calls, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="read_strategic", operation="strategic_planning"
        )
        assert isinstance(out, Intent)
        assert out.action == "strategic_planning"
        assert len(calls) == 1
        assert f["route"] == "inversion" and f["live_match"] == "group"
        assert f["flip_group"] == "read_strategic"


# ---------------------------------------------------------------------------
# 4. AUDIT — unassigned ops are visible output, never a silent remainder
# ---------------------------------------------------------------------------


class TestFlipCoverageAudit:
    @pytest.fixture(scope="class")
    def report(self):
        return gate.flip_coverage_audit()

    def test_lists_every_unassigned_read_op_by_name(self, report):
        """m-44 in the AC: the unassigned list must be OUTPUT, not a remainder
        the reader is expected to subtract. After wave 3 (#1595, 2026-09-25)
        the real registry has zero unassigned READ ops — this is the honest
        "reads done" state, and the report must SAY zero, not just omit
        names."""
        rail = get_action_workflows()
        unassigned = [
            k for k, e in rail.items() if e.effect == EffectClass.READ and e.flip_group is None
        ]
        assert unassigned == [], f"expected zero unassigned READ ops, found: {unassigned}"
        assert "UNASSIGNED — the 0 READ keys NO WAVE CAN FLIP, by name" in report
        for op in unassigned:  # vacuous while empty; guards a future regression
            assert op in report, f"unassigned op {op} missing from --audit output"

    def test_unassigned_mechanism_still_names_ops_when_present(self, monkeypatch):
        """The m-44 mechanism itself, re-pinned independent of the real
        registry's current (now-zero) unassigned count — same idiom as the
        b-list synthetic pins above: inject a synthetic ungrouped,
        uncategorized READ op and confirm the audit lists it by name rather
        than only adjusting the count."""
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY

        synthetic_op = "_test_unassigned_by_name_1667"
        monkeypatch.setitem(
            WORKFLOW_REGISTRY,
            synthetic_op,
            WorkflowEntry(
                entry_point=lambda **k: None,
                effect=EffectClass.READ,
                description="synthetic — unassigned (test only)",
                action_triggered=True,
            ),
        )
        synthetic_report = gate.flip_coverage_audit()
        assert synthetic_op in synthetic_report

    def test_states_denominators_not_bare_counts(self, report):
        rail = get_action_workflows()
        n_read = sum(1 for e in rail.values() if e.effect == EffectClass.READ)
        n_ungrouped = sum(
            1 for e in rail.values() if e.effect == EffectClass.READ and e.flip_group is None
        )
        assert f"{n_ungrouped:3d}/{n_read}" in report
        assert f"rail operation keys (action_triggered) : {len(rail):3d}" in report
        for group in FLIP_GROUPS:
            assert f"/{n_read}" in report and group in report

    def test_separates_reachable_by_category_from_truly_unreachable(self, report):
        """The honesty the flag's widening requires: 'ungrouped' does not mean
        'unreachable' for an op that carries a registry category."""
        assert "STILL SWEPT IN" in report
        assert "week_calendar" in report

    def test_reports_the_read_only_invariant_as_a_measurement(self, report):
        assert "READ-ONLY INVARIANT (re-measured, not assumed)" in report
        assert "0 of" in report and "carry a flip_group" in report

    def test_names_the_layer_it_measured(self, report):
        assert "layer measured (m-43)" in report
        assert "not what routing did" in report
