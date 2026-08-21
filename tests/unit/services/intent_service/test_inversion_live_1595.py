"""#1595 Phase 2.2 flip-1 — LIVE inversion routing behind a DEFAULT-EMPTY flag.

Pins the contract addendum (Arch #1663 ruling, kickoff plan §2.2):

1. DEFAULT-EMPTY pin — flag unset ⇒ the consult does ZERO work (no snapshot
   assembly, no router call) and the full legacy chain answers the turn
   byte-identically (e2e over the real ``process_intent``).
2. LIVE DISPATCH — with a test category set live, an in-category turn routes
   via the inversion to the SAME handler result the legacy chain produces
   (e2e, real rail + real handler over aiosqlite, LLM boundary explosive).
3. ARMED-TURN GUARD — a turn with a popped pending offer, a bound contextual
   offer, or snapshot-armed state (pending offer / active process / draft)
   NEVER reaches the router; armed + in-set category still takes legacy (e2e).
4. Fallback honesty — REFUSED / error / NONE / CLARIFY / sub-threshold /
   off-set category / non-rail / non-READ operations all fall through to the
   legacy chain, each with its own telemetry reason. The non-READ pin is
   load-bearing: ACTION_REGISTRY files create_issue (WRITE) under QUERY, so a
   category flag alone must never flip a write.
5. Error path — a raising consult never breaks the turn (call-site belt).
6. Disagreement telemetry — every consult decision logs one
   ``inversion_live_decision`` line; the flip-1 legacy comparison is the
   deterministic pre-classifier (no extra LLM), divergence asserted present.

Test idioms are the #1621/#1595-Phase-2.0 set (test_snapshot_assembly_1595):
real WorkflowOfferService store, real ProcessRegistry, real
SessionActivityRepository over aiosqlite, explosive LLM boundaries,
deterministic fakes for the router decision — NO live LLM anywhere.
"""

import contextlib
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
from services.database.repositories import SessionActivityRepository  # noqa: E402
from services.domain.models import Intent  # noqa: E402
from services.intent_service import inversion_live  # noqa: E402
from services.intent_service.destructive_confirm import (  # noqa: E402
    CONFIRM_PENDING_ACTION_WORKFLOW,
)
from services.intent_service.drafted_issue import (  # noqa: E402
    build_drafted_issue_offer,
)
from services.intent_service.inversion_live import (  # noqa: E402
    consult_inversion_live,
    live_categories,
    live_min_confidence,
)
from services.intent_service.inversion_router import RoutingDecision  # noqa: E402
from services.intent_service.soft_invocation import WorkflowOfferService  # noqa: E402
from services.intent_service.workflow_entries import (  # noqa: E402
    register_default_workflows,
)
from services.process.registry import (  # noqa: E402
    ProcessRegistry,
    ProcessType,
    get_process_registry,
)
from services.shared_types import IntentCategory  # noqa: E402

_USER = "3f7b8a52-1595-4b00-9e00-000000002202"
_SESSION = "sess-1595-flip1"
# Deterministically claimed by the legacy pre-classifier (surface 1:
# QUERY/session_activity_query) so BOTH legs of the same-handler e2e resolve
# without any live LLM, and the flip-1 divergence comparison has a concrete
# legacy label to compare against.
_MSG = "what did we create this session?"
_OP = "session_activity_query"
_EMPTY_LEDGER_ANSWER = "We haven't created anything in this session yet."


# ---------------------------------------------------------------------------
# Fixtures — the #1621 store idioms (mirrors test_snapshot_assembly_1595)
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def sm(monkeypatch):
    """Real SessionActivityRepository over aiosqlite (the B3 #1394 idiom)."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda c: SessionActivityDB.__table__.create(c, checkfirst=True)
        )
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
    """In-memory users.preferences double at the ONE persistence seam."""
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    return store


@pytest.fixture(autouse=True)
def _registry_reset():
    ProcessRegistry.reset_instance()
    yield
    ProcessRegistry.reset_instance()


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """Every test starts with the flip OFF and the shadow OFF (default world)."""
    monkeypatch.delenv("PIPER_INVERSION_LIVE_CATEGORIES", raising=False)
    monkeypatch.delenv("PIPER_INVERSION_LIVE_MIN_CONFIDENCE", raising=False)
    monkeypatch.delenv("PIPER_INVERSION_SHADOW", raising=False)


@pytest.fixture(autouse=True)
def _rail_registered():
    register_default_workflows()  # idempotent — container-init equivalent


@pytest.fixture
def svc():
    """The IntentService slice the CONSULT reads (snapshot peek + llm seam)."""
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(), intent_classifier=None
    )


class _LogRecorder:
    def __init__(self):
        self.events = []  # (level, event, fields)

    def _rec(self, level):
        def _log(event, **fields):
            self.events.append((level, event, fields))

        return _log

    def __getattr__(self, name):
        if name in ("info", "warning", "error", "debug"):
            return self._rec(name)
        raise AttributeError(name)

    def decisions(self):
        return [
            (lvl, f) for lvl, ev, f in self.events if ev == "inversion_live_decision"
        ]


@pytest.fixture
def log_rec(monkeypatch):
    rec = _LogRecorder()
    monkeypatch.setattr(inversion_live, "logger", rec)
    return rec


def _decision(operation=_OP, confidence=0.9, outcome="operation", **kw):
    return RoutingDecision(
        outcome=outcome,
        operation=operation if outcome == "operation" else None,
        confidence=confidence,
        **kw,
    )


def _stub_route(monkeypatch, decision):
    """Deterministic fake for the router call (NO live LLM). Records calls."""
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


class _ExplosiveLLM:
    """Any attribute access = an LLM boundary was consulted."""

    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name}) — not allowed here")


def _real_service():
    from services.intent.intent_service import IntentService
    from services.intent_service.classifier import IntentClassifier

    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


async def _seed_issue(maker, owner, conv, ref, title="Seeded"):
    async with maker() as s:
        await SessionActivityRepository(s).record(
            owner_id=owner,
            conversation_id=conv,
            action_type="issue_created",
            target_ref=ref,
            target_title=title,
        )


# ---------------------------------------------------------------------------
# Flag resolution (mirrors shadow_enabled: call-time env reads)
# ---------------------------------------------------------------------------


class TestFlagResolution:
    def test_default_empty(self):
        assert live_categories() == frozenset()

    def test_parse_and_normalize(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", " query, Status ,")
        assert live_categories() == frozenset({"QUERY", "STATUS"})

    def test_min_confidence_default(self):
        assert live_min_confidence() == inversion_live.DEFAULT_MIN_CONFIDENCE == 0.8

    def test_min_confidence_override_clamped_and_fallback(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_MIN_CONFIDENCE", "0.5")
        assert live_min_confidence() == 0.5
        monkeypatch.setenv("PIPER_INVERSION_LIVE_MIN_CONFIDENCE", "7")
        assert live_min_confidence() == 1.0
        monkeypatch.setenv("PIPER_INVERSION_LIVE_MIN_CONFIDENCE", "not-a-number")
        assert live_min_confidence() == inversion_live.DEFAULT_MIN_CONFIDENCE


# ---------------------------------------------------------------------------
# 1. DEFAULT-EMPTY pin
# ---------------------------------------------------------------------------


class TestDefaultEmptyPin:
    async def test_unset_flag_zero_work(self, monkeypatch, svc, log_rec):
        """Flag unset ⇒ None with ZERO work: no snapshot assembly, no router
        call, not even a telemetry line — the module is inert."""
        _explosive_snapshot(monkeypatch)
        _explosive_route(monkeypatch)
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is None
        assert log_rec.events == []

    async def test_unset_flag_e2e_legacy_chain_answers(self, sm, mem_prefs, monkeypatch):
        """E2E byte-identical pin: with the set unset, the real process_intent
        resolves the turn through the legacy chain (pre-classifier → rail →
        real handler) with the router provably untouched."""
        _explosive_route(monkeypatch)
        service = _real_service()
        result = await service.process_intent(
            message=_MSG, session_id=_SESSION, user_id=_USER
        )
        assert result.success is True
        assert result.message == _EMPTY_LEDGER_ANSWER
        assert result.intent_data["action"] == _OP


# ---------------------------------------------------------------------------
# 2. LIVE DISPATCH — in-category turn routes via the inversion to the SAME
#    handler result
# ---------------------------------------------------------------------------


class TestLiveDispatch:
    async def test_consult_returns_dispatch_ready_intent(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        calls = _stub_route(monkeypatch, _decision(confidence=0.9))
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert isinstance(out, Intent)
        assert out.category is IntentCategory.QUERY
        assert out.action == _OP
        assert out.confidence == 0.9
        assert out.original_message == _MSG
        assert out.context["inversion_live"] is True
        assert len(calls) == 1

    async def test_in_category_turn_same_handler_result_e2e(
        self, sm, mem_prefs, monkeypatch
    ):
        """The AC pin: leg A = legacy chain (flag unset); leg B = flip live
        (flag=QUERY, router chooses the key, classifier consult REPLACED —
        classify_multiple explosive). Same rail, same handler, same answer."""
        # Leg A — legacy (flag unset), router explosive.
        _explosive_route(monkeypatch)
        service_a = _real_service()
        result_a = await service_a.process_intent(
            message=_MSG, session_id=f"{_SESSION}-a", user_id=_USER
        )
        assert result_a.message == _EMPTY_LEDGER_ANSWER

        # Leg B — flip live; the router decision is the ONLY route chooser.
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        calls = _stub_route(monkeypatch, _decision(confidence=0.9))
        service_b = _real_service()

        async def _classifier_boom(*a, **k):
            raise AssertionError(
                "classify_multiple consulted — flip-1 must REPLACE the "
                "classifier consult for an in-set dispatch"
            )

        monkeypatch.setattr(
            service_b.intent_classifier, "classify_multiple", _classifier_boom
        )
        result_b = await service_b.process_intent(
            message=_MSG, session_id=f"{_SESSION}-b", user_id=_USER
        )

        assert len(calls) == 1, "the inversion routed this turn exactly once"
        assert result_b.success is True
        assert result_b.message == result_a.message  # SAME handler result
        assert result_b.intent_data["action"] == result_a.intent_data["action"] == _OP
        assert result_b.intent_data["category"] == result_a.intent_data["category"]

    async def test_pre_classification_snapshot_threads_into_router(
        self, sm, mem_prefs, svc, monkeypatch
    ):
        """The Phase-2.0 point, live: the router call carries the
        PRE-classification snapshot (ledger head + declared mode) as its
        serialized state block."""
        await _seed_issue(sm, _USER, _SESSION, "mediajunkie/test-piper-morgan#107")
        mem_prefs[_USER]["working_mode"] = "execute"
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        calls = _stub_route(monkeypatch, RoutingDecision(outcome="none"))

        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is None  # NONE → legacy
        assert len(calls) == 1
        block = calls[0].session_state.state_block
        assert "RECENT ISSUE: #107" in block
        assert "DECLARED MODE: execute" in block


# ---------------------------------------------------------------------------
# 3. ARMED-TURN GUARD (flip-1: armed turns NEVER take the inversion path)
# ---------------------------------------------------------------------------


class TestArmedGuard:
    async def test_popped_offer_skips_before_any_work(
        self, svc, monkeypatch, log_rec
    ):
        """Guard part 1: the pop seam found an offer this turn — no snapshot,
        no router, reason logged."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _explosive_snapshot(monkeypatch)
        _explosive_route(monkeypatch)
        out = await consult_inversion_live(
            _MSG,
            session_id=_SESSION,
            user_id=_USER,
            intent_service=svc,
            turn_had_pending_offer=True,
        )
        assert out is None
        [(lvl, fields)] = log_rec.decisions()
        assert fields["reason"] == "armed_pending_offer_popped"
        assert fields["route"] == "legacy"

    async def test_bound_contextual_offer_skips(self, svc, monkeypatch, log_rec):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _explosive_snapshot(monkeypatch)
        _explosive_route(monkeypatch)
        out = await consult_inversion_live(
            _MSG,
            session_id=_SESSION,
            user_id=_USER,
            intent_service=svc,
            turn_bound_contextual_offer=True,
        )
        assert out is None
        [(_, fields)] = log_rec.decisions()
        assert fields["reason"] == "armed_contextual_offer_bound"

    async def test_snapshot_armed_offer_skips_router(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """Guard part 2 (belt): the snapshot sees an armed offer → legacy."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _explosive_route(monkeypatch)
        offer = build_drafted_issue_offer(
            Intent(
                category=IntentCategory.EXECUTION,
                action="create_issue",
                original_message="draft an issue about login",
                confidence=1.0,
                context={},
            ),
            "Fix the login flow",
        )
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is None
        [(_, fields)] = log_rec.decisions()
        assert fields["reason"] == "armed_snapshot"

    async def test_active_process_skips_router(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _explosive_route(monkeypatch)

        class _StubProcess:
            """Minimal GuidedProcess (the snapshot suite's stub idiom)."""

            @property
            def process_type(self):
                return ProcessType.STANDUP

            async def check_active(self, user_id, session_id):
                return True

            async def handle_message(self, user_id, session_id, message):
                raise AssertionError("the consult must never handle a message")

            async def suspend(self, user_id, session_id):
                raise AssertionError("the consult must never suspend a process")

            async def has_suspended_session(self, user_id):
                return None

        get_process_registry().register(_StubProcess())
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is None
        [(_, fields)] = log_rec.decisions()
        assert fields["reason"] == "armed_snapshot"

    async def test_armed_turn_in_set_category_takes_legacy_e2e(
        self, sm, mem_prefs, monkeypatch
    ):
        """AC pin, e2e: an ARMED turn (pending destructive confirm) carrying
        an in-set-category command abandons via the pop and takes the LEGACY
        chain — the router is provably never consulted."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _explosive_route(monkeypatch)
        service = _real_service()
        service.workflow_offer_service.set_pending_offer(
            _SESSION,
            {
                "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
                "pending_action": {
                    "action": "close_issue",
                    "intent": Intent(
                        category=IntentCategory.QUERY,
                        action="close_issue",
                        original_message="close issue #108",
                        confidence=1.0,
                        context={},
                    ),
                    "summary": "close issue #108",
                },
                "decline_message": "Okay — I won't close issue #108.",
            },
            user_id=_USER,
        )
        # The unrelated in-set command abandons the confirm via the pop and
        # must resolve through the LEGACY chain (pre-classifier → rail).
        result = await service.process_intent(
            message=_MSG, session_id=_SESSION, user_id=_USER
        )
        assert result.success is True
        assert result.message == _EMPTY_LEDGER_ANSWER  # legacy handler answered


# ---------------------------------------------------------------------------
# 4. Fallback honesty — every non-dispatch reason falls to legacy, telemetered
# ---------------------------------------------------------------------------


class TestFallthroughReasons:
    async def _consult(self, svc, monkeypatch, log_rec, decision, cats="QUERY"):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", cats)
        calls = _stub_route(monkeypatch, decision)
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        return out, calls, log_rec.decisions()

    async def test_router_none(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        out, _, [(lvl, f)] = await self._consult(
            svc, monkeypatch, log_rec, RoutingDecision(outcome="none")
        )
        assert out is None and f["reason"] == "router_none" and lvl == "info"

    async def test_router_clarify(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        out, _, [(_, f)] = await self._consult(
            svc, monkeypatch, log_rec, RoutingDecision(outcome="clarify")
        )
        assert out is None and f["reason"] == "router_clarify"

    async def test_router_refused_pinned(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        out, _, [(_, f)] = await self._consult(
            svc,
            monkeypatch,
            log_rec,
            RoutingDecision(outcome="refused", error="twice invalid"),
        )
        assert out is None and f["reason"] == "router_refused"

    async def test_router_error_pinned_and_loud(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """Transport error → legacy, logged at WARNING (loud, never silent)."""
        out, _, [(lvl, f)] = await self._consult(
            svc,
            monkeypatch,
            log_rec,
            RoutingDecision(outcome="error", error="ConnectionError: boom"),
        )
        assert out is None and f["reason"] == "router_error"
        assert lvl == "warning"
        assert f["error"] == "ConnectionError: boom"

    async def test_sub_threshold_pinned(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        out, _, [(_, f)] = await self._consult(
            svc, monkeypatch, log_rec, _decision(confidence=0.79)
        )
        assert out is None and f["reason"] == "sub_threshold"
        assert f["threshold"] == 0.8

    async def test_threshold_env_override_dispatches(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_MIN_CONFIDENCE", "0.5")
        out, _, [(_, f)] = await self._consult(
            svc, monkeypatch, log_rec, _decision(confidence=0.6)
        )
        assert isinstance(out, Intent) and f["route"] == "inversion"

    async def test_not_live_categorized(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        """Bucket renamed from its flip-1 name by the #1670 corpus migration
        (the sanctioned change to this byte-for-byte pin; old→new mapping
        note in inversion-phase2-gate-2026-08-19.md)."""
        out, _, [(_, f)] = await self._consult(
            svc, monkeypatch, log_rec, _decision(), cats="STATUS"
        )
        assert out is None and f["reason"] == "not_live_categorized"
        assert f["category"] == "QUERY"

    async def test_registry_only_operation_not_rail_dispatchable(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """get_identity is ACTION_REGISTRY-only (CANONICAL, no rail key) —
        flip-1 honestly falls to legacy rather than inventing a dispatch."""
        out, _, [(_, f)] = await self._consult(
            svc,
            monkeypatch,
            log_rec,
            _decision(operation="get_identity"),
            cats="IDENTITY",
        )
        assert out is None and f["reason"] == "not_rail_dispatchable"

    async def test_write_effect_never_flips_even_in_live_category(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """LOAD-BEARING pin: create_issue rides ACTION_REGISTRY under QUERY
        but declares WRITE on the rail — the effect guard, not the category
        flag, is what keeps flip-1 READ-only."""
        out, _, [(_, f)] = await self._consult(
            svc, monkeypatch, log_rec, _decision(operation="create_issue")
        )
        assert out is None and f["reason"] == "not_read_effect"

    async def test_not_live_uncategorized_falls_through(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """A rail READ op with no ACTION_REGISTRY category (show_standup) is
        outside the category flag's addressable space — honest legacy, with
        the gap visible in telemetry (the coverage note in the report).
        Bucket renamed from its flip-1 name by the #1670 corpus migration
        (the sanctioned change to this byte-for-byte pin; old→new mapping
        note in inversion-phase2-gate-2026-08-19.md)."""
        out, _, [(_, f)] = await self._consult(
            svc, monkeypatch, log_rec, _decision(operation="show_standup")
        )
        assert out is None and f["reason"] == "not_live_uncategorized"


# ---------------------------------------------------------------------------
# 5. Error path — a raising consult never breaks the turn (call-site belt)
# ---------------------------------------------------------------------------


class TestErrorPathNeverBreaksTurn:
    async def test_raising_router_falls_to_legacy_e2e(
        self, sm, mem_prefs, monkeypatch
    ):
        from services.intent_service import inversion_router as ir

        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")

        async def _transport_down(*a, **k):
            raise RuntimeError("transport down")

        monkeypatch.setattr(ir, "route", _transport_down)
        service = _real_service()
        result = await service.process_intent(
            message=_MSG, session_id=_SESSION, user_id=_USER
        )
        assert result.success is True
        assert result.message == _EMPTY_LEDGER_ANSWER  # legacy chain answered


# ---------------------------------------------------------------------------
# 6. Disagreement telemetry (flip-1: deterministic pre-classifier comparison)
# ---------------------------------------------------------------------------


class TestDisagreementTelemetry:
    async def test_dispatch_line_carries_legacy_agreement(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _stub_route(monkeypatch, _decision(confidence=0.9))
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert isinstance(out, Intent)
        [(lvl, f)] = log_rec.decisions()
        assert f["route"] == "inversion" and f["reason"] is None
        assert f["operation"] == _OP
        assert f["confidence"] == 0.9 and f["threshold"] == 0.8
        assert f["snapshot_present"] is False  # empty world → no state block
        # The legacy pre-classifier claims this phrase — agreement recorded.
        assert f["legacy_preclassifier"] == "query:session_activity_query"
        assert f["legacy_divergence"] is False
        assert "utterance_sha256" in f

    async def test_divergence_true_when_router_overrides_preclassifier(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The flip's telemetry: the router picks a DIFFERENT in-set READ op
        than the deterministic legacy chain would have — dispatched (the flip
        is live) with the disagreement recorded on the corpus line."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _stub_route(monkeypatch, _decision(operation="list_reminders_query"))
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert isinstance(out, Intent)
        assert out.action == "list_reminders_query"
        [(_, f)] = log_rec.decisions()
        assert f["legacy_preclassifier"] == "query:session_activity_query"
        assert f["legacy_divergence"] is True

    async def test_incomparable_when_preclassifier_would_defer(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """A phrase surface 1 never claims → legacy label None, divergence
        None (the legacy counterfactual would be the LLM classifier, which
        flip-1 deliberately does not spend a second call on)."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _stub_route(monkeypatch, _decision(confidence=0.9))
        out = await consult_inversion_live(
            "hmm can you pull together the things we shipped",
            session_id=_SESSION,
            user_id=_USER,
            intent_service=svc,
        )
        assert isinstance(out, Intent)
        [(_, f)] = log_rec.decisions()
        assert f["legacy_preclassifier"] is None
        assert f["legacy_divergence"] is None
