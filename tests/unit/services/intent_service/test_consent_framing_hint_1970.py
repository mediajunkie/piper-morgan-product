"""#1970 (ADR-080 D1/D6 step 1) — the framing-hint PLUMBING, behind the
existing live flag, with NO router prompt change and NO LLM call anywhere in
this suite (Arch's design comment on #1970: "(2)+(3)+(4) behind the existing
flag" — the prompt (1) and the ratchet (5) are later steps, out of scope
here).

Covers:
- the router parser accepts ONLY the gate's existing 3 framing values at the
  TOP LEVEL (single-op and plan alike), dropping anything else to None
  (``RoutingDecision.framing``, AC1);
- ``inversion_live`` carries ``decision.framing`` onto the dispatch Intent's
  context exactly like ``inversion_args`` (AC2);
- the live-flag token ``framing_hint`` gates consumption — absent, the hint
  is parsed/carried but IGNORED everywhere (AC3);
- ``consent_gate.evaluate_consent``'s D3 asymmetry: DESTRUCTIVE ignores the
  hint; PRIVATE uses it as is; OUTWARD takes the LESS PERMISSIVE of the hint
  and the regex read (AC4), including the inverted-order case the task
  briefing's own suggested order gets backwards (see
  TestFramingPermissivenessOrder below);
- the ``consent_framing_disagreement`` telemetry event (AC6);
- one rail-level test proving the hint actually reaches ``evaluate_consent``
  through ``_dispatch_action_rail`` when the flag token is on (AC7).

No LLM anywhere: the router tests use a scripted double (the house
``test_inversion_router_1595.py`` idiom); the rail/context tests use the
house explosive-LLM classifier double plus real aiosqlite-backed stores (the
``test_inversion_live_1595.py`` / ``test_consent_gate_1509.py`` idioms).
"""

import contextlib
from types import SimpleNamespace
from unittest.mock import AsyncMock

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
from services.intent.intent_service import IntentService  # noqa: E402
from services.intent_service import consent_gate as cg  # noqa: E402
from services.intent_service import inversion_live  # noqa: E402
from services.intent_service.classifier import IntentClassifier  # noqa: E402
from services.intent_service.collaboration_gate import (  # noqa: E402
    FRAMING_AMBIGUOUS,
    FRAMING_COMPOSE,
    FRAMING_EXECUTE,
    WorkingMode,
    is_valid_framing,
)
from services.intent_service.drafted_issue import is_command_shaped  # noqa: E402
from services.intent_service.inversion_live import (  # noqa: E402
    FRAMING_HINT_TOKEN,
    consult_inversion_live,
    resolve_framing_hint,
)
from services.intent_service.inversion_router import RoutingDecision, route  # noqa: E402
from services.intent_service.workflow_entries import (  # noqa: E402
    register_default_workflows,
)
from services.process.registry import ProcessRegistry  # noqa: E402
from services.shared_types import EffectClass, IntentCategory, Outwardness  # noqa: E402

_USER = "3f7b8a52-1970-4b00-9e00-000000001970"
_SESSION = "sess-1970"

# Deterministic READ route for the context-write/flag-gate tests (same
# choice as test_inversion_live_1595.py, same reasoning: a registered READ
# rail key whose real handler is deterministic within one test run).
_MSG = "are we behind upstream at all"
_OP = "local_git_status_query"

# An update-issue request with AMBIGUOUS framing (same literal the #1509
# suite pins): no verb-initial imperative, no compose marker.
AMBIGUOUS_UPDATE = "the title of issue #108 ought to say Q3 roadmap"
# A verb-initial imperative — regex reads EXECUTE.
IMPERATIVE_UPDATE = "change the title of issue #108 to Q3 roadmap"


# ---------------------------------------------------------------------------
# Shared fixtures (mirrors test_inversion_live_1595.py / test_consent_gate_1509.py)
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    """Every test starts with every live-flag env var unset (default world)."""
    monkeypatch.delenv("PIPER_INVERSION_LIVE_CATEGORIES", raising=False)
    monkeypatch.delenv("PIPER_INVERSION_LIVE_MIN_CONFIDENCE", raising=False)
    monkeypatch.delenv("PIPER_INVERSION_SHADOW", raising=False)


@pytest.fixture(autouse=True)
def _registry_reset():
    ProcessRegistry.reset_instance()
    yield
    ProcessRegistry.reset_instance()


@pytest.fixture(autouse=True)
def _rail_registered():
    register_default_workflows()  # idempotent — container-init equivalent


@pytest_asyncio.fixture
async def sm(monkeypatch):
    """Real SessionActivityRepository over aiosqlite (the B3 #1394 idiom) —
    consult_inversion_live's B3 ledger read needs a real session factory."""
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
    """In-memory users.preferences double at the ONE persistence seam
    (collaboration_gate's declared-mode store)."""
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


@pytest.fixture
def svc():
    """The IntentService slice consult_inversion_live reads (snapshot peek +
    llm seam) — the #1595 idiom."""
    from services.intent_service.soft_invocation import WorkflowOfferService

    return SimpleNamespace(workflow_offer_service=WorkflowOfferService(), intent_classifier=None)


class _ExplosiveLLM:
    """Any attribute access = an LLM boundary was consulted (house idiom)."""

    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name}) — not allowed in this suite")


def _real_service():
    return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _stub_classifier(service, intent):
    """Classification-boundary stub (the #1509 suite idiom) — used where the
    rail block itself is under test, not classification."""
    multi = SimpleNamespace(
        is_multi_intent=False,
        intents=[intent],
        primary_intent=intent,
        has_greeting=False,
        has_substantive_intent=True,
        secondary_intents=[],
    )
    service.intent_classifier.classify_multiple = AsyncMock(return_value=multi)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _decision(outcome="operation", operation=_OP, confidence=0.9, **kw):
    return RoutingDecision(
        outcome=outcome,
        operation=operation if outcome == "operation" else None,
        confidence=confidence,
        **kw,
    )


def _stub_route(monkeypatch, decision):
    """Deterministic fake for the router call (NO live LLM)."""
    from services.intent_service import inversion_router as ir

    async def _route(utterance, session_state=None, **kwargs):
        return decision

    monkeypatch.setattr(ir, "route", _route)


class ScriptedLLM:
    """LLM double for route()'s structured-output contract: queued replies."""

    def __init__(self, replies):
        self.replies = list(replies)

    async def complete(self, **kwargs):
        if not self.replies:
            raise AssertionError("ScriptedLLM exhausted — unexpected extra call")
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return reply


def _update_intent(message=AMBIGUOUS_UPDATE, framing_hint=None):
    """A PRIVATE-WRITE rail Intent (update_issue), optionally carrying the
    #1970 context hint — same shape _update_intent() uses in
    test_consent_gate_1509.py, extended with the hint."""
    context = {"original_message": message}
    if framing_hint is not None:
        context["inversion_framing"] = framing_hint
    return Intent(
        category=IntentCategory.QUERY,
        action="update_issue",
        confidence=0.85,
        original_message=message,
        context=context,
    )


# ---------------------------------------------------------------------------
# AC1 — router parser: top-level "framing", gate's 3 values only
# ---------------------------------------------------------------------------


class TestRouterFramingParse:
    async def test_valid_execute_framing_parses(self):
        llm = ScriptedLLM(
            [
                '{"operation": "create_reminder", "framing": "execute", '
                '"confidence": 0.9, "rationale": "x"}'
            ]
        )
        d = await route("remind me at 9am", llm_service=llm)
        assert d.outcome == "operation"
        assert d.framing == FRAMING_EXECUTE

    async def test_valid_compose_framing_parses(self):
        llm = ScriptedLLM(
            [
                '{"operation": "create_reminder", "framing": "compose", '
                '"confidence": 0.9, "rationale": "x"}'
            ]
        )
        d = await route("remind me at 9am", llm_service=llm)
        assert d.framing == FRAMING_COMPOSE

    async def test_valid_ambiguous_framing_parses(self):
        llm = ScriptedLLM(
            [
                '{"operation": "create_reminder", "framing": "ambiguous", '
                '"confidence": 0.9, "rationale": "x"}'
            ]
        )
        d = await route("remind me at 9am", llm_service=llm)
        assert d.framing == FRAMING_AMBIGUOUS

    async def test_invalid_framing_value_drops_to_none(self):
        """Not one of the gate's 3 values (e.g. a guessed "imperative") is
        dropped, never passed on as if valid."""
        llm = ScriptedLLM(
            [
                '{"operation": "create_reminder", "framing": "imperative", '
                '"confidence": 0.9, "rationale": "x"}'
            ]
        )
        d = await route("remind me at 9am", llm_service=llm)
        assert d.framing is None

    async def test_wrong_type_framing_drops_to_none(self):
        llm = ScriptedLLM(
            [
                '{"operation": "create_reminder", "framing": 1, '
                '"confidence": 0.9, "rationale": "x"}'
            ]
        )
        d = await route("remind me at 9am", llm_service=llm)
        assert d.framing is None

    async def test_missing_framing_defaults_to_none(self):
        """A router that doesn't emit the key at all yields None — today's
        behavior, byte-for-byte (no prompt change in this step)."""
        llm = ScriptedLLM(['{"operation": "create_reminder", "confidence": 0.9, "rationale": "x"}'])
        d = await route("remind me at 9am", llm_service=llm)
        assert d.framing is None

    async def test_plan_level_framing_is_top_level_not_per_element(self):
        """A property of the MESSAGE, not of each operation — sits beside
        "outcome", never inside operations[i]."""
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "framing": "compose", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                '{"operation": "delete_todo", "confidence": 0.9, "rationale": "y"}]}'
            ]
        )
        d = await route("two things", llm_service=llm)
        assert d.outcome == "plan"
        assert d.framing == FRAMING_COMPOSE
        for op in d.operations:
            assert "framing" not in op

    async def test_plan_with_no_framing_key_defaults_to_none(self):
        llm = ScriptedLLM(
            [
                '{"outcome": "plan", "operations": ['
                '{"operation": "list_todos_query", "confidence": 0.9, "rationale": "x"}, '
                '{"operation": "delete_todo", "confidence": 0.9, "rationale": "y"}]}'
            ]
        )
        d = await route("two things", llm_service=llm)
        assert d.outcome == "plan"
        assert d.framing is None


class TestIsValidFraming:
    """The shared validity check both the router parser and consent_gate's
    hint validation go through — one source of truth for "what counts"."""

    def test_the_three_gate_values_are_valid(self):
        assert is_valid_framing(FRAMING_EXECUTE)
        assert is_valid_framing(FRAMING_COMPOSE)
        assert is_valid_framing(FRAMING_AMBIGUOUS)

    def test_anything_else_is_invalid(self):
        assert not is_valid_framing("imperative")
        assert not is_valid_framing("declarative")
        assert not is_valid_framing(None)
        assert not is_valid_framing(1)
        assert not is_valid_framing({})


# ---------------------------------------------------------------------------
# AC2 — context write (inversion_live carries decision.framing like
# inversion_args), AC3 — flag gate at the live-dispatch layer
# ---------------------------------------------------------------------------


class TestContextWrite:
    async def test_framing_is_carried_on_the_dispatch_intent(self, sm, mem_prefs, svc, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _stub_route(monkeypatch, _decision(framing=FRAMING_EXECUTE))
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert isinstance(out, Intent)
        assert out.context["inversion_framing"] == FRAMING_EXECUTE
        # inversion_args is unaffected — framing rides alongside it, never
        # replacing it.
        assert "inversion_args" in out.context

    async def test_absent_framing_is_not_a_none_valued_key(self, sm, mem_prefs, svc, monkeypatch):
        """Today's router never emits framing, so the key is simply MISSING
        on the Intent's context, not present-and-None."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")
        _stub_route(monkeypatch, _decision())  # framing defaults to None
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert isinstance(out, Intent)
        assert "inversion_framing" not in out.context


# ---------------------------------------------------------------------------
# AC3 — the flag-and-context read (resolve_framing_hint), both halves gated
# ---------------------------------------------------------------------------


class TestFlagGate:
    def test_hint_ignored_when_token_absent_even_with_context_present(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY")  # no framing_hint token
        intent = SimpleNamespace(context={"inversion_framing": "execute"})
        assert resolve_framing_hint(intent) is None

    def test_hint_resolved_when_token_present(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", FRAMING_HINT_TOKEN)
        intent = SimpleNamespace(context={"inversion_framing": "execute"})
        assert resolve_framing_hint(intent) == "execute"

    def test_token_match_is_case_insensitive_like_every_other_token(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "FRAMING_HINT")
        intent = SimpleNamespace(context={"inversion_framing": "compose"})
        assert resolve_framing_hint(intent) == "compose"

    def test_other_tokens_alone_dont_enable_it(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "QUERY,read_status")
        intent = SimpleNamespace(context={"inversion_framing": "execute"})
        assert resolve_framing_hint(intent) is None

    def test_absent_context_key_resolves_to_none_even_with_token_on(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", FRAMING_HINT_TOKEN)
        intent = SimpleNamespace(context={})
        assert resolve_framing_hint(intent) is None

    def test_no_context_attribute_at_all_is_handled(self, monkeypatch):
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", FRAMING_HINT_TOKEN)
        intent = SimpleNamespace()
        assert resolve_framing_hint(intent) is None


# ---------------------------------------------------------------------------
# The permissiveness order itself — verified against decide_consent, not
# assumed (see consent_gate._FRAMING_PERMISSIVENESS's comment)
# ---------------------------------------------------------------------------


class TestFramingPermissivenessOrder:
    _RANK = {
        cg.ConsentDecision.COLLABORATE: 0,
        cg.ConsentDecision.PROCEED_WITH_DISCLOSURE: 1,
        cg.ConsentDecision.PROCEED: 2,
    }

    @pytest.mark.parametrize("outwardness", [Outwardness.PRIVATE, Outwardness.OUTWARD])
    @pytest.mark.parametrize("mode", [WorkingMode.COLLABORATE, WorkingMode.EXECUTE])
    def test_execute_ge_ambiguous_ge_compose_in_every_cell(self, outwardness, mode):
        """The order the module relies on, mechanically re-derived: for
        every (outwardness, mode) WRITE cell, execute's decision is never
        less permissive than ambiguous's, and ambiguous's is never less
        permissive than compose's."""
        ranks = {
            f: self._RANK[cg.decide_consent(EffectClass.WRITE, f, mode, outwardness=outwardness)]
            for f in (FRAMING_COMPOSE, FRAMING_AMBIGUOUS, FRAMING_EXECUTE)
        }
        assert ranks[FRAMING_EXECUTE] >= ranks[FRAMING_AMBIGUOUS] >= ranks[FRAMING_COMPOSE]

    def test_less_permissive_framing_matches_the_derived_order(self):
        assert cg.less_permissive_framing(FRAMING_EXECUTE, FRAMING_COMPOSE) == FRAMING_COMPOSE
        assert cg.less_permissive_framing(FRAMING_COMPOSE, FRAMING_EXECUTE) == FRAMING_COMPOSE
        assert cg.less_permissive_framing(FRAMING_EXECUTE, FRAMING_AMBIGUOUS) == FRAMING_AMBIGUOUS
        assert cg.less_permissive_framing(FRAMING_AMBIGUOUS, FRAMING_COMPOSE) == FRAMING_COMPOSE

    def test_ambiguous_is_not_less_permissive_than_compose(self):
        """Regression pin for the specific mistake this order corrects
        (callers must NOT assume "execute, then compose, then ambiguous
        least" — that gets compose and ambiguous backwards). Under a
        declared EXECUTE mode, OUTWARD ambiguous reaches the SAME decision
        as OUTWARD execute (both PROCEED_WITH_DISCLOSURE) — strictly MORE
        permissive than OUTWARD compose (COLLABORATE, mode-invariant)."""
        d_ambiguous = cg.decide_consent(
            EffectClass.WRITE,
            FRAMING_AMBIGUOUS,
            WorkingMode.EXECUTE,
            outwardness=Outwardness.OUTWARD,
        )
        d_execute = cg.decide_consent(
            EffectClass.WRITE,
            FRAMING_EXECUTE,
            WorkingMode.EXECUTE,
            outwardness=Outwardness.OUTWARD,
        )
        d_compose = cg.decide_consent(
            EffectClass.WRITE,
            FRAMING_COMPOSE,
            WorkingMode.EXECUTE,
            outwardness=Outwardness.OUTWARD,
        )
        assert d_ambiguous == d_execute == cg.ConsentDecision.PROCEED_WITH_DISCLOSURE
        assert d_compose == cg.ConsentDecision.COLLABORATE


# ---------------------------------------------------------------------------
# AC4 — evaluate_consent's D3 asymmetry
# ---------------------------------------------------------------------------


class TestEvaluateConsentFramingHint:
    async def test_destructive_confirms_regardless_of_any_hint(self):
        for hint in (FRAMING_EXECUTE, FRAMING_COMPOSE, FRAMING_AMBIGUOUS, None, "bogus"):
            for outwardness in (Outwardness.PRIVATE, Outwardness.OUTWARD):
                verdict = await cg.evaluate_consent(
                    EffectClass.DESTRUCTIVE,
                    "close issue 5",
                    _USER,
                    outwardness=outwardness,
                    framing_hint=hint,
                )
                assert verdict is cg.ConsentDecision.CONFIRM

    async def test_private_write_uses_the_hint_as_is_no_mode_consult(self, monkeypatch):
        """A valid PRIVATE hint stands in place of the regex read entirely —
        and, for an EXECUTE-framed hint, consults no stored mode at all (the
        same no-extra-DB-touch property the regex path has today)."""
        from services.intent_service import collaboration_gate as cgate

        async def _explosive_mode(*a, **k):
            raise AssertionError("get_working_mode consulted — must not be, for this cell")

        monkeypatch.setattr(cgate, "get_working_mode", _explosive_mode)

        verdict = await cg.evaluate_consent(
            EffectClass.WRITE,
            AMBIGUOUS_UPDATE,  # regex would read AMBIGUOUS
            _USER,
            outwardness=Outwardness.PRIVATE,
            framing_hint=FRAMING_EXECUTE,
        )
        assert verdict is cg.ConsentDecision.PROCEED

    async def test_private_write_hint_compose_collaborates_even_though_regex_says_execute(self):
        verdict = await cg.evaluate_consent(
            EffectClass.WRITE,
            IMPERATIVE_UPDATE,  # regex would read EXECUTE
            _USER,
            outwardness=Outwardness.PRIVATE,
            framing_hint=FRAMING_COMPOSE,
        )
        assert verdict is cg.ConsentDecision.COLLABORATE

    async def test_outward_write_hint_execute_regex_ambiguous_ambiguous_wins(self, mem_prefs):
        """THE required case: hint says execute, the deterministic regex
        says ambiguous — for an OUTWARD write the LESS permissive of the two
        wins, which is ambiguous, not execute."""
        verdict = await cg.evaluate_consent(
            EffectClass.WRITE,
            AMBIGUOUS_UPDATE,  # regex reads AMBIGUOUS
            _USER,
            outwardness=Outwardness.OUTWARD,
            framing_hint=FRAMING_EXECUTE,
        )
        # Default (collaborate) mode, ambiguous framing, OUTWARD -> COLLABORATE.
        assert verdict is cg.ConsentDecision.COLLABORATE

    async def test_outward_write_hint_compose_wins_over_regex_execute(self):
        """hint says compose, regex says execute (a verb-initial imperative)
        — compose is less permissive, so it wins: the communication act
        never loses its ask on the LLM's word alone."""
        verdict = await cg.evaluate_consent(
            EffectClass.WRITE,
            IMPERATIVE_UPDATE,  # regex reads EXECUTE
            _USER,
            outwardness=Outwardness.OUTWARD,
            framing_hint=FRAMING_COMPOSE,
        )
        assert verdict is cg.ConsentDecision.COLLABORATE

    async def test_outward_write_hint_and_regex_agree_on_execute_proceeds_with_disclosure(
        self, mem_prefs
    ):
        from services.intent_service.collaboration_gate import WORKING_MODE_PREF_KEY

        mem_prefs[_USER][WORKING_MODE_PREF_KEY] = "execute"
        verdict = await cg.evaluate_consent(
            EffectClass.WRITE,
            IMPERATIVE_UPDATE,
            _USER,
            outwardness=Outwardness.OUTWARD,
            framing_hint=FRAMING_EXECUTE,
        )
        assert verdict is cg.ConsentDecision.PROCEED_WITH_DISCLOSURE

    async def test_no_hint_falls_back_to_regex_unchanged(self):
        verdict = await cg.evaluate_consent(
            EffectClass.WRITE,
            IMPERATIVE_UPDATE,
            _USER,
            outwardness=Outwardness.PRIVATE,
            framing_hint=None,
        )
        assert verdict is cg.ConsentDecision.PROCEED

    async def test_invalid_hint_string_falls_back_to_regex(self):
        verdict = await cg.evaluate_consent(
            EffectClass.WRITE,
            IMPERATIVE_UPDATE,
            _USER,
            outwardness=Outwardness.PRIVATE,
            framing_hint="declarative",  # not one of the gate's 3 values
        )
        assert verdict is cg.ConsentDecision.PROCEED  # same as no hint at all


# ---------------------------------------------------------------------------
# AC6 — disagreement telemetry
# ---------------------------------------------------------------------------


class _LogRecorder:
    def __init__(self):
        self.events = []

    def info(self, event, **fields):
        self.events.append((event, fields))

    def __getattr__(self, name):
        def _rec(event, **fields):
            self.events.append((event, fields))

        return _rec


class TestDisagreementTelemetry:
    async def test_logs_on_disagreement(self, monkeypatch):
        rec = _LogRecorder()
        monkeypatch.setattr(cg, "logger", rec)
        await cg.evaluate_consent(
            EffectClass.WRITE,
            AMBIGUOUS_UPDATE,  # regex -> AMBIGUOUS
            _USER,
            outwardness=Outwardness.OUTWARD,
            framing_hint=FRAMING_EXECUTE,  # disagrees
            action="update_issue",
        )
        disagreements = [f for ev, f in rec.events if ev == "consent_framing_disagreement"]
        assert len(disagreements) == 1
        assert disagreements[0]["action"] == "update_issue"
        assert disagreements[0]["hint"] == FRAMING_EXECUTE
        assert disagreements[0]["regex"] == FRAMING_AMBIGUOUS
        assert disagreements[0]["outward"] is True

    async def test_silent_on_agreement(self, monkeypatch):
        rec = _LogRecorder()
        monkeypatch.setattr(cg, "logger", rec)
        await cg.evaluate_consent(
            EffectClass.WRITE,
            IMPERATIVE_UPDATE,  # regex -> EXECUTE
            _USER,
            outwardness=Outwardness.PRIVATE,
            framing_hint=FRAMING_EXECUTE,  # agrees
            action="update_issue",
        )
        disagreements = [f for ev, f in rec.events if ev == "consent_framing_disagreement"]
        assert disagreements == []

    async def test_silent_when_no_hint_at_all(self, monkeypatch):
        rec = _LogRecorder()
        monkeypatch.setattr(cg, "logger", rec)
        await cg.evaluate_consent(
            EffectClass.WRITE,
            AMBIGUOUS_UPDATE,
            _USER,
            outwardness=Outwardness.PRIVATE,
            framing_hint=None,
            action="update_issue",
        )
        disagreements = [f for ev, f in rec.events if ev == "consent_framing_disagreement"]
        assert disagreements == []


# ---------------------------------------------------------------------------
# drafted_issue.is_command_shaped — the OUTWARD less-permissive rule,
# applied directly (no caller threads a real hint yet; see its docstring)
# ---------------------------------------------------------------------------


class TestIsCommandShapedFramingHint:
    def test_no_hint_is_unchanged_behavior(self):
        assert is_command_shaped("close issue #108") is True
        assert is_command_shaped(AMBIGUOUS_UPDATE) is False

    def test_hint_compose_overrides_regex_execute_to_less_permissive(self):
        """Regex alone reads this as a command (verb-initial "update" — the
        collaborate-gate EXECUTE family, not the close/read/destructive
        supplement, which a hint deliberately never touches); a compose hint
        is LESS permissive, so the OUTWARD rule makes it win — no longer
        command-shaped."""
        text = "update the title of the issue"
        assert is_command_shaped(text) is True  # baseline
        assert is_command_shaped(text, framing_hint=FRAMING_COMPOSE) is False

    def test_hint_execute_cannot_override_regex_ambiguous(self):
        """The less-permissive rule only ever makes the read MORE cautious —
        an execute hint can never promote a non-command read to a command."""
        text = "what would make a good body?"
        assert is_command_shaped(text) is False
        assert is_command_shaped(text, framing_hint=FRAMING_EXECUTE) is False

    def test_invalid_hint_is_ignored(self):
        assert is_command_shaped(
            "close the loop with the team", framing_hint="bogus"
        ) == is_command_shaped("close the loop with the team")


# ---------------------------------------------------------------------------
# AC7 — one rail-level test: the hint reaches evaluate_consent through
# _dispatch_action_rail when the flag token is on, and is ignored when off.
# ---------------------------------------------------------------------------


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


class TestRailThreadsFramingHint:
    async def test_flag_on_hint_reaches_evaluate_consent_and_proceeds(
        self, live_service, mem_prefs, monkeypatch
    ):
        """AMBIGUOUS-phrased update_issue (PRIVATE WRITE) would normally
        hold for a consent check (see test_consent_gate_1509.py's
        test_ambiguous_write_is_held_with_a_legible_check). With the
        framing_hint token on and an EXECUTE hint in context, PRIVATE's
        "use the hint as is" rule makes it PROCEED directly instead — proof
        the hint actually reaches evaluate_consent through the rail."""
        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", FRAMING_HINT_TOKEN)
        sid = "e2e-1970-hint-on"
        intent = _update_intent(framing_hint=FRAMING_EXECUTE)
        _stub_classifier(live_service, intent)

        from services.intent.intent_service import IntentProcessingResult

        handler = AsyncMock(
            return_value=IntentProcessingResult(
                success=True, message="Updated issue #108", intent_data={}
            )
        )
        live_service._handle_update_issue = handler

        result = await live_service.process_intent(
            message=AMBIGUOUS_UPDATE, session_id=sid, user_id=_USER
        )
        handler.assert_awaited_once()
        assert "Updated issue #108" in result.message
        assert _pending_offers(live_service).get(sid) is None

    async def test_flag_off_hint_is_ignored_even_though_context_carries_one(
        self, live_service, mem_prefs, monkeypatch
    ):
        """Same Intent, same hint in context, but the live flag does NOT
        carry the framing_hint token — the rail must fall back to today's
        regex-only behavior and HOLD for a consent check."""
        sid = "e2e-1970-hint-off"
        intent = _update_intent(framing_hint=FRAMING_EXECUTE)
        _stub_classifier(live_service, intent)

        async def _explosive_handler(*a, **k):
            raise AssertionError("update handler reached — consent gate must hold")

        live_service._handle_update_issue = _explosive_handler

        result = await live_service.process_intent(
            message=AMBIGUOUS_UPDATE, session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("consent_check_pending") is True
        assert result.requires_clarification is True
