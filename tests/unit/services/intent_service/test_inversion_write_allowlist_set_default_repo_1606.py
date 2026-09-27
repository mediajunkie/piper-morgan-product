"""#1595 unit 3c — the FOURTH named write flips through the Inversion:
``set_default_repo``, via the same #1677 allowlist mechanism
``create_todo``/``create_reminder``/``delete_todo`` used (never a relaxed
effect check, never a ``flip_group``).

This closes #1606's SET-DEFAULT-REPO half (its clear/delete half —
``delete_todo`` — was closed by #1595 unit 3b, ``70f7dd5159``). Verbatim
corpus phrasing from #1606: "set my default repo to
mediajunkie/piper-morgan-product".

This file is a SIBLING of ``test_inversion_write_allowlist_1677.py``,
``test_inversion_write_allowlist_create_reminder_1559.py``, and
``test_inversion_write_allowlist_delete_todo_1606.py``, not an extension of
any of them — the SHARED constant (``FLIP_WRITE_ALLOWLIST``) and its
closed-set/denominator assertions live in the 1677 file, updated in the
same commit as this one; all four files must agree on the closed set and
are run together.

⚠️ UNLIKE its three siblings, ``set_default_repo``'s ACTION_REGISTRY
category is ``QUERY`` (action_registry.py:150), not ``EXECUTION`` — so
naming the raw category token ``QUERY`` (flip-1's own original, and by far
the broadest category on the rail) sweeps this write in too, not only the
``EXECUTION`` token the other three writes answer to. Exercised directly in
``TestDispatchGuard.test_query_category_surface_reaches_the_allowlisted_
write_too`` and its negative twin
``test_execution_category_does_not_sweep_set_default_repo_in``.

⚠️ DISCOVERED WORK (filed #1898, not fixed here — out of this unit's
scope): ``_handle_set_default_repo`` extracts its repo argument from
``intent.context.get("original_message", "")`` ONLY — it does not fall
back to ``intent.original_message`` the way ``handle_create_reminder`` /
``handle_delete_todo`` do. ``consult_inversion_live`` sets
``original_message`` on the TOP-LEVEL Intent field only (context carries
just ``inversion_live``/``inversion_args``), so a flipped
``set_default_repo`` turn reaches the handler and the consent gate fires
correctly (Arch's condition 3, proven below independent of this gap), but
the handler itself cannot see the repo the user named — it answers the
graceful bad-shape nudge and never calls
``ConnectorConfigService.set_default_repo``. ``TestFlippedTurnReachesThe
Rail`` below asserts the ACTUAL current behavior (consent evaluated, no
write), not the aspirational one, and names #1898 at the assertion so this
is never mistaken for the write actually landing. The allowlist entry
itself is still correct per Arch's three conditions — registration,
declared-effect-by-behavior, and consent-gate reachability are properties
of the ENTRY and the RAIL, not of whether this one handler happens to read
its argument from the right place — but #1898 must land before flipping
this token actually closes #1606's corpus row live.

⚠️ LAYER HONESTY (m-43), same caveat as the sibling files': the unit layer
uses a DETERMINISTIC router fake, so these tests prove *the flip routes a
set-default-repo operation to set_default_repo, and consent is evaluated
before the handler runs* — they do NOT prove the live constrained router
draws set_default_repo more reliably than the classifier did for the #1606
phrasing. That is observable only live, in the ``inversion_live_decision``
telemetry, once the flag is actually set (out of scope for this unit —
declaration + pins only, same as the sibling files).
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
from services.domain.models import Intent  # noqa: E402
from services.intent_service import consent_gate, inversion_live  # noqa: E402
from services.intent_service.inversion_live import (  # noqa: E402
    consult_inversion_live,
)
from services.intent_service.inversion_router import (  # noqa: E402
    RoutingDecision,
    derive_routing_grammar,
)
from services.intent_service.soft_invocation import WorkflowOfferService  # noqa: E402
from services.intent_service.workflow_dispatcher import (  # noqa: E402
    FLIP_WRITE_ALLOWLIST,
    get_action_workflows,
)
from services.intent_service.workflow_entries import (  # noqa: E402
    register_default_workflows,
)
from services.shared_types import (  # noqa: E402
    EffectClass,
    IntentCategory,
    Outwardness,
)

_USER = "3f7b8a52-1606-4b00-9e00-000000001606"  # valid UUID: survives principal parsing
_SESSION = "sess-1606-write-flip"

# The #1606 corpus phrasing, verbatim as given for this unit.
_MSG = "set my default repo to mediajunkie/piper-morgan-product"


# ---------------------------------------------------------------------------
# Fixtures (inherited wholesale from the #1677/#1559/#1606-delete flip set,
# same shape)
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


@pytest.fixture
def repo_boundary(monkeypatch):
    """``ConnectorConfigService.set_default_repo`` boundary: records every
    write. ``_handle_set_default_repo`` (via ``ConnectorConfigService(session)
    .set_default_repo(...)``) calls this exact method — replacing it here
    means the session it was constructed with is never actually queried, so
    the DB-shape question (JSONB-on-sqlite dialect, the ``ConnectorConfig``
    FK to ``users.id``) is fully out of scope for this unit layer — same
    isolation discipline the create_todo/create_reminder ``todo_boundary``
    fixture applies to ``TodoManagementService.create_todo``."""
    from services.connectors.config_service import ConnectorConfigService

    state = {"set": []}

    async def _set_default_repo(self, owner_id, value):
        state["set"].append((owner_id, value))

    monkeypatch.setattr(ConnectorConfigService, "set_default_repo", _set_default_repo)
    return state


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


def _decision(operation, confidence=0.9):
    return RoutingDecision(outcome="operation", operation=operation, confidence=confidence)


async def _consult(svc, monkeypatch, log_rec, *, cats, operation, message=_MSG, confidence=0.9):
    monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", cats)
    calls = _stub_route(monkeypatch, _decision(operation, confidence))
    out = await consult_inversion_live(
        message, session_id=_SESSION, user_id=_USER, intent_service=svc
    )
    return out, calls, log_rec.decisions()


# ---------------------------------------------------------------------------
# 1. THE ENTRY — allowlisted, no flip_group, no alias family
# ---------------------------------------------------------------------------


class TestEntryDeclaration:
    def test_allowlist_includes_set_default_repo(self):
        assert "set_default_repo" in FLIP_WRITE_ALLOWLIST

    def test_real_rail_set_default_repo_declares_the_key_and_no_group(self):
        """set_default_repo flips by NAME (or its registry category), never by
        a wave — the same shape as its three siblings: no flip_group, so no
        group token sweeps a write in."""
        wf = get_action_workflows()
        entry = wf["set_default_repo"]
        assert entry.flip_write_allowlist_key == "set_default_repo"
        assert entry.flip_group is None
        assert entry.effect == EffectClass.WRITE
        assert entry.outwardness == Outwardness.PRIVATE
        assert entry.action_triggered is True

    def test_no_alias_family_only_one_key_shares_this_entry_object(self):
        """Unlike create_todo/create_reminder/delete_todo, set_default_repo
        has no ActionMapper alias family — it is reached deterministically
        by the pre-classifier's SET_DEFAULT_REPO_PATTERNS (which emits the
        literal action string) and by the LLM/inversion routers targeting
        the same registry canonical. Exactly one rail key maps to this
        entry object."""
        wf = get_action_workflows()
        ids = [k for k, e in wf.items() if id(e) == id(wf["set_default_repo"])]
        assert ids == ["set_default_repo"]


# ---------------------------------------------------------------------------
# 2. THE DISPATCH GUARD — mirrors the sibling files' TestDispatchGuard,
#    plus the QUERY-category-sweep pair that is set_default_repo's own
#    consequence to state (its category differs from its siblings').
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestDispatchGuard:
    async def test_named_set_default_repo_flips(self, sm, mem_prefs, svc, monkeypatch, log_rec):
        out, calls, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="set_default_repo", operation="set_default_repo"
        )
        assert isinstance(out, Intent)
        assert out.action == "set_default_repo"
        # QUERY from ACTION_REGISTRY (action_registry.py:150) — set_default_repo's
        # GENUINE registered category, unlike its three EXECUTION siblings; not the
        # "allowlisted_write_uncategorized" fallback (which fires only when an
        # allowlisted write carries NO registry category at all — not this op's case).
        assert out.category is IntentCategory.QUERY
        assert out.original_message == _MSG
        assert f["reason"] is None and f["live_match"] == "operation"
        assert len(calls) == 1

    async def test_query_category_surface_reaches_the_allowlisted_write_too(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The same honest consequence create_todo/create_reminder/delete_todo
        carry for EXECUTION, restated for set_default_repo's OWN registry
        category: it carries QUERY, so flipping the raw category token
        `QUERY` sweeps it in too — the allowlist bounds WHICH writes, never
        WHICH surface names them. Worth its own test because QUERY is
        flip-1's own original, and by far the BROADEST, category on the
        rail (most READ query ops live there) — an operator flipping QUERY
        is flipping a write, same as flipping EXECUTION is for the other
        three named writes."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="QUERY", operation="set_default_repo"
        )
        assert isinstance(out, Intent)
        assert f["live_match"] == "category"

    async def test_execution_category_does_not_sweep_set_default_repo_in(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """The negative twin, proving set_default_repo's category really is
        QUERY and not EXECUTION: naming EXECUTION (the token that sweeps in
        create_todo/create_reminder/delete_todo) leaves set_default_repo
        unnamed."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="EXECUTION", operation="set_default_repo"
        )
        assert out is None
        assert f["live_match"] is None and f["reason"] == "not_live_categorized"

    async def test_sub_threshold_still_blocks_the_named_write(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        out, _, [(_, f)] = await _consult(
            svc,
            monkeypatch,
            log_rec,
            cats="set_default_repo",
            operation="set_default_repo",
            confidence=0.5,
        )
        assert out is None and f["reason"] == "sub_threshold"

    async def test_unnamed_set_default_repo_does_not_flip(
        self, sm, mem_prefs, svc, monkeypatch, log_rec
    ):
        """Allowlisted != live. A flag naming a READ wave (e.g. read_status)
        must never sweep set_default_repo in — no wave carries a write; the
        allowlist says only 'may flip when named' (op or its own registry
        category)."""
        out, _, [(_, f)] = await _consult(
            svc, monkeypatch, log_rec, cats="read_status", operation="set_default_repo"
        )
        assert out is None
        assert f["live_match"] is None and f["reason"] == "not_live_categorized"

    async def test_default_empty_is_still_byte_identically_dark(self, monkeypatch, svc, log_rec):
        """Unchanged by the fourth write flip: unset => zero work, not even a
        log line. Explosive snapshot AND explosive router — the allowlist
        lookup must not have introduced work before the flag check."""
        _explosive_snapshot(monkeypatch)
        _explosive_route(monkeypatch)
        out = await consult_inversion_live(
            _MSG, session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is None
        assert log_rec.events == []


# ---------------------------------------------------------------------------
# 3. THE RAIL, END TO END — consent still evaluated (Arch's condition 3,
#    proven live and independent of #1898's handler-side gap)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestFlippedTurnReachesTheRail:
    async def _run(self, monkeypatch, message, *, spy_calls):
        from services.intent.intent_service import IntentService
        from services.intent_service.classifier import IntentClassifier

        class _ExplosiveLLM:
            def __getattr__(self, name):
                raise AssertionError(f"LLM boundary touched ({name})")

        monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", "set_default_repo")
        calls = _stub_route(monkeypatch, _decision("set_default_repo", 0.95))
        service = IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))

        async def _boom(*a, **k):
            raise AssertionError(
                "classify_multiple consulted — the flip must REPLACE the "
                "classifier draw that #1606 is about"
            )

        monkeypatch.setattr(service.intent_classifier, "classify_multiple", _boom)

        real = consent_gate.evaluate_consent

        async def _spy(effect, msg, user_id, outwardness=Outwardness.PRIVATE):
            spy_calls.append((effect, msg, user_id, outwardness))
            return await real(effect, msg, user_id, outwardness=outwardness)

        monkeypatch.setattr(consent_gate, "evaluate_consent", _spy)

        result = await service.process_intent(
            message=message,
            session_id=f"{_SESSION}-{abs(hash(message))}",
            user_id=_USER,
        )
        return result, calls

    async def test_flipped_turn_reaches_the_handler_and_consent_is_evaluated(
        self, mem_prefs, repo_boundary, monkeypatch
    ):
        """What #1898 leaves TRUE today: the router is consulted exactly
        once, the SAME rail dispatch that would run create_todo/
        create_reminder/delete_todo runs here too, and consent_gate.
        evaluate_consent fires with this entry's declared effect +
        outwardness BEFORE the handler's internal extraction ever runs —
        the consent evaluation is a property of the rail, not of whether
        the handler subsequently manages to parse its argument. This is
        Arch's third allowlist condition, held live rather than cited, and
        it holds independent of #1898."""
        spy: list = []
        result, calls = await self._run(monkeypatch, _MSG, spy_calls=spy)
        assert len(calls) == 1, "the inversion router was not consulted"
        assert result.intent_data["action"] == "set_default_repo"
        assert len(spy) == 1, (
            "consent_gate.evaluate_consent was not consulted on a flipped "
            "set_default_repo turn — the flip must not bypass the shared "
            "rail's gate"
        )
        effect, msg, principal, outwardness = spy[0]
        assert effect is EffectClass.WRITE
        assert outwardness is Outwardness.PRIVATE
        assert msg == _MSG and str(principal) == _USER

    async def test_flipped_turn_writes_the_row_1898(self, mem_prefs, repo_boundary, monkeypatch):
        """#1898, FIXED the same morning it was found (Lead, 2026-09-27): the
        handler used to read ``intent.context.get("original_message", "")``
        only, while ``consult_inversion_live`` sets the Intent's TOP-LEVEL
        ``original_message`` — so a flipped turn saw an empty string and
        answered the bad-shape nudge instead of writing. The handler now
        falls back the way ``handle_create_reminder``/``handle_delete_todo``
        already did. This is the positive assertion the sibling suites make:
        the flipped turn reaches the same handler AND the row is written for
        the token's owner."""
        result, _ = await self._run(monkeypatch, _MSG, spy_calls=[])
        assert result.success is True
        assert not result.requires_clarification
        assert len(repo_boundary["set"]) == 1
        owner_id, value = repo_boundary["set"][0]
        assert value == "mediajunkie/piper-morgan-product"
        assert owner_id  # never an empty/None principal


# ---------------------------------------------------------------------------
# 4. Structural fact underneath the claim — same class as the sibling files'
#    grammar pin
# ---------------------------------------------------------------------------


class TestRouterChoiceSet:
    def test_set_default_repo_is_a_grammar_name(self):
        """set_default_repo must actually be a name the router can choose —
        not merely allowlisted in the abstract."""
        grammar = derive_routing_grammar()
        assert "set_default_repo" in set(grammar.names())
