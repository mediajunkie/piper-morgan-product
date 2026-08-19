"""#1595 Phase 2.0 — SessionSnapshot assembly against the REAL stores.

The contract is Lead-authored (``services/intent_service/session_snapshot.py``,
five items in its docstring); this file is the review artifact for the
assembly bound to it:

1. Per-field assembly against real stores (the #1621 idioms — the real
   ``WorkflowOfferService`` in-memory store, the real ``ProcessRegistry``,
   the real ``SessionActivityRepository`` over aiosqlite as in the B3
   tests, and the ``collaboration_gate._load_preferences`` seam double as
   in the #1510 tests; the real-Postgres halves of those stores live in
   the existing integration suites).
2. IDEMPOTENCE PIN (contract item 1): assemble twice → identical world —
   the peeked offer still pops normally afterward, the process stays active.
3. Fail-open pin (contract item 3): one store raising → that field None,
   ``field_errors`` names it, everything else populated.
4. GOLDEN SERIALIZATION PIN (contract item 4): fully-populated snapshot →
   exact string. Editing ``serialize_for_prompt`` or the caps REQUIRES
   updating this pin in the same commit — that requirement is the feature.
5. Shadow wiring: the serialized block reaches the composed shadow context,
   and the LIVE turn result is byte-identical with the flag on/off
   (shadow-only proof — the #1650/#1411 real-``process_intent`` idiom,
   mocked only at the LLM boundary and the router's LLM call).
"""

import asyncio
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
from services.database.repositories import SessionActivityRepository  # noqa: E402
from services.domain.models import Intent  # noqa: E402
from services.intent_service.destructive_confirm import (  # noqa: E402
    CONFIRM_PENDING_ACTION_WORKFLOW,
)
from services.intent_service.drafted_issue import (  # noqa: E402
    build_drafted_issue_offer,
)
from services.intent_service.session_snapshot import (  # noqa: E402
    SessionSnapshot,
    serialize_for_prompt,
)
from services.intent_service.snapshot_assembly import (  # noqa: E402
    assemble_session_snapshot,
)
from services.intent_service.soft_invocation import WorkflowOfferService  # noqa: E402
from services.process.registry import (  # noqa: E402
    ProcessRegistry,
    ProcessType,
    get_process_registry,
)
from services.shared_types import IntentCategory  # noqa: E402

_USER = "3f7b8a52-1595-4b00-9e00-000000001595"
_SESSION = "sess-1595-snapshot"


# ---------------------------------------------------------------------------
# Fixtures — the #1621 store idioms
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
    """In-memory users.preferences double at the ONE persistence seam
    (the #1510 idiom — collaboration_gate._load_preferences)."""
    store: dict = {_USER: {}}

    async def _load(user_id):
        return dict(store.get(str(user_id), {}))

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    return store


@pytest.fixture(autouse=True)
def _registry_reset():
    """Real ProcessRegistry singleton, clean per test (the #427 idiom)."""
    ProcessRegistry.reset_instance()
    yield
    ProcessRegistry.reset_instance()


class _StubProcess:
    """Minimal GuidedProcess for the real registry (test_registry.py idiom)."""

    def __init__(self, process_type: ProcessType, is_active: bool = True):
        self._process_type = process_type
        self._is_active = is_active

    @property
    def process_type(self) -> ProcessType:
        return self._process_type

    async def check_active(self, user_id, session_id) -> bool:
        return self._is_active

    async def handle_message(self, user_id, session_id, message):
        raise AssertionError("snapshot assembly must never handle a message")

    async def suspend(self, user_id, session_id) -> None:
        raise AssertionError("snapshot assembly must never suspend a process")

    async def has_suspended_session(self, user_id):
        return None


@pytest.fixture
def svc():
    """The slice of IntentService the assembly reads: the REAL offer store."""
    return SimpleNamespace(workflow_offer_service=WorkflowOfferService())


def _intent(message="draft an issue about login", action="create_issue"):
    return Intent(
        original_message=message,
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=1.0,
        context={},
    )


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
# 1. Per-field assembly against the real stores
# ---------------------------------------------------------------------------


class TestPerFieldAssembly:
    async def test_empty_world_all_none(self, sm, mem_prefs, svc):
        """Contract item 3's baseline: an empty world is an EMPTY snapshot
        with EMPTY field_errors — absent state, not failed reads."""
        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap == SessionSnapshot()
        assert snap.field_errors == ()

    async def test_armed_drafted_issue_offer(self, sm, mem_prefs, svc):
        """Armed drafted-issue offer → kind + is_confirm + draft fields ride
        the ONE peek. #1665: the arm site stores its rendered ask and the
        snapshot carries it. #1664: a mid-compose draft (body still open) is
        NOT a yes/no confirm — its open question is the body ask."""
        from services.intent_service.collaboration_gate import draft_open_question

        question = draft_open_question("Fix the login flow", None)
        offer = build_drafted_issue_offer(
            _intent(),
            "Fix the login flow",
            "mediajunkie/test-piper-morgan",
            question=question,
        )
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.pending_offer_kind == "drafted_issue"
        assert snap.pending_offer_is_confirm is False  # open body ask ≠ yes/no
        assert snap.pending_offer_question == question
        assert snap.draft_in_compose is True
        assert snap.draft_title == "Fix the login flow"
        assert snap.field_errors == ()

    async def test_ready_to_file_draft_is_confirm(self, sm, mem_prefs, svc):
        """#1664: with BOTH slots shaped the draft's open ask IS the file
        confirm — the one drafted-issue state in the #1650 confirm set."""
        from services.intent_service.collaboration_gate import draft_open_question

        question = draft_open_question("Fix the login flow", "Steps: …")
        offer = build_drafted_issue_offer(
            _intent(),
            "Fix the login flow",
            "mediajunkie/test-piper-morgan",
            body="Steps: …",
            question=question,
        )
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.pending_offer_is_confirm is True
        assert snap.pending_offer_question == question

    async def test_untitled_draft_has_none_title(self, sm, mem_prefs, svc):
        """#1630 subjectless arm: draft_in_compose True, draft_title None."""
        offer = build_drafted_issue_offer(_intent(), None)
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.draft_in_compose is True
        assert snap.draft_title is None

    async def test_armed_confirm_is_confirm_true(self, sm, mem_prefs, svc):
        """The #1650 distinction: a legacy destructive confirm (the #1190
        carrier WITHOUT a kind key — the documented #1664 fallback: the only
        kindless producer ever was the destructive builder) → is_confirm
        True, kind None, no draft."""
        offer = {
            "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
            "pending_action": {
                "action": "close_issue",
                "intent": _intent("close issue #108", "close_issue"),
                "summary": "close issue #108",
            },
            "decline_message": "Okay — I won't close issue #108. Nothing has been changed.",
        }
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.pending_offer_is_confirm is True
        assert snap.pending_offer_kind is None
        assert snap.draft_in_compose is False

    async def test_non_confirm_offer_is_confirm_false(self, sm, mem_prefs, svc):
        """A non-carrier workflow offer (e.g. the standup invite) is an open
        question but NOT a strict confirm."""
        offer = {
            "workflow_type": "standup_interview",
            "pending_action": {"kind": "standup_invite", "action": "standup_interview"},
            "decline_message": "No problem.",
        }
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.pending_offer_kind == "standup_invite"
        assert snap.pending_offer_is_confirm is False

    async def test_offer_question_read_when_stored(self, sm, mem_prefs, svc):
        """The rendered ask IS read when an arm site stores one."""
        offer = {
            "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
            "question": "Close issue #108? (yes/no)",
            "pending_action": {"action": "close_issue", "summary": "close issue #108"},
            "decline_message": "Okay.",
        }
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.pending_offer_question == "Close issue #108? (yes/no)"

    async def test_active_standup_process_type(self, sm, mem_prefs, svc):
        """Real registry, active standup handler → 'standup'."""
        get_process_registry().register(_StubProcess(ProcessType.STANDUP))
        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.active_process_type == ProcessType.STANDUP.value == "standup"

    async def test_inactive_process_not_reported(self, sm, mem_prefs, svc):
        get_process_registry().register(
            _StubProcess(ProcessType.STANDUP, is_active=False)
        )
        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.active_process_type is None

    async def test_ledger_head_owner_scoped_newest_wins(self, sm, mem_prefs, svc):
        """Real repository read: newest issue_created row for THIS owner and
        session; another owner's newer row never leaks in (D1a)."""
        await _seed_issue(sm, _USER, _SESSION, "mediajunkie/test-piper-morgan#107")
        await _seed_issue(sm, _USER, _SESSION, "mediajunkie/test-piper-morgan#109")
        await _seed_issue(sm, "someone-else", _SESSION, "evil/other#999")

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.recent_issue_number == 109
        assert snap.recent_issue_repo == "mediajunkie/test-piper-morgan"

    async def test_no_principal_means_no_ledger_read_not_an_error(
        self, sm, mem_prefs, svc
    ):
        """D1a: unscopeable ≠ failed — fields None, field_errors empty."""
        await _seed_issue(sm, _USER, _SESSION, "mediajunkie/test-piper-morgan#107")
        snap = await assemble_session_snapshot(_SESSION, None, svc)
        assert snap.recent_issue_number is None
        assert snap.field_errors == ()

    async def test_stored_mode_and_verb(self, sm, mem_prefs, svc):
        """The #1510 declared mode and the #1605 per-verb default, read
        through their real read paths over the seam double."""
        from services.intent_service.reminder_clear import inference_key
        from services.intent_service.verified_inference import (
            VERIFIED_INFERENCES_PREF_KEY,
        )

        mem_prefs[_USER]["working_mode"] = "execute"
        mem_prefs[_USER][VERIFIED_INFERENCES_PREF_KEY] = {
            inference_key("clear"): {"value": "delete", "source": "user_verified"}
        }

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.declared_working_mode == "execute"
        assert snap.stored_clear_verb == "delete"

    async def test_unset_mode_is_none_not_collaborate(self, sm, mem_prefs, svc):
        """The snapshot must distinguish 'never declared' (None) from
        'declared collaborate' — get_working_mode's collaborate default
        would be a fabricated declaration here (contract item 3)."""
        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.declared_working_mode is None

        mem_prefs[_USER]["working_mode"] = "collaborate"
        snap2 = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap2.declared_working_mode == "collaborate"


# ---------------------------------------------------------------------------
# 2. IDEMPOTENCE PIN — contract item 1
# ---------------------------------------------------------------------------


class TestIdempotencePin:
    async def test_assemble_twice_world_unchanged(self, sm, mem_prefs, svc):
        """Assemble twice: identical snapshots, and the world is untouched —
        the offer still pops normally afterward (the peek consumed nothing)
        and the process is still active."""
        offer = build_drafted_issue_offer(_intent(), "Fix the login flow")
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)
        handler = _StubProcess(ProcessType.STANDUP)
        get_process_registry().register(handler)
        await _seed_issue(sm, _USER, _SESSION, "mediajunkie/test-piper-morgan#107")

        first = await assemble_session_snapshot(_SESSION, _USER, svc)
        second = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert first == second  # identical observed world
        assert first.pending_offer_kind == "drafted_issue"

        # The peek never popped: the production pop still yields THE offer.
        popped = svc.workflow_offer_service.get_and_clear_pending_offer(
            _SESSION, user_id=_USER
        )
        assert popped is offer
        # ...and pops empty only now, through the pop — not through assembly.
        assert (
            svc.workflow_offer_service.get_and_clear_pending_offer(
                _SESSION, user_id=_USER
            )
            is None
        )
        # The process probe suspended nothing.
        assert await handler.check_active(_USER, _SESSION) is True


# ---------------------------------------------------------------------------
# 3. Fail-open pin — contract item 3
# ---------------------------------------------------------------------------


class TestFailOpen:
    async def test_one_store_raising_fails_open_and_is_named(
        self, sm, mem_prefs, svc, monkeypatch
    ):
        """The process registry raises → active_process_type is None and
        field_errors names exactly it; every OTHER field still populates."""
        offer = build_drafted_issue_offer(_intent(), "Fix the login flow")
        svc.workflow_offer_service.set_pending_offer(_SESSION, offer, user_id=_USER)
        await _seed_issue(sm, _USER, _SESSION, "mediajunkie/test-piper-morgan#107")
        mem_prefs[_USER]["working_mode"] = "execute"

        import services.process.registry as registry_mod

        def _boom():
            raise RuntimeError("registry unavailable")

        monkeypatch.setattr(registry_mod, "get_process_registry", _boom)

        snap = await assemble_session_snapshot(_SESSION, _USER, svc)
        assert snap.active_process_type is None
        assert snap.field_errors == ("active_process_type",)
        # Everything else still populated — field-by-field, never all-or-nothing.
        assert snap.pending_offer_kind == "drafted_issue"
        assert snap.draft_title == "Fix the login flow"
        assert snap.recent_issue_number == 107
        assert snap.declared_working_mode == "execute"

    async def test_never_raises_even_with_broken_offer_service(
        self, sm, mem_prefs
    ):
        """A raising peek: the five offer/draft fields fail open together,
        named in dataclass declaration order (contract item 3's shape)."""

        class _BrokenStore:
            def peek_pending_offer(self, *a, **k):
                raise RuntimeError("store down")

        broken = SimpleNamespace(workflow_offer_service=_BrokenStore())
        snap = await assemble_session_snapshot(_SESSION, _USER, broken)
        assert snap.field_errors == (
            "pending_offer_kind",
            "pending_offer_question",
            "pending_offer_is_confirm",
            "draft_in_compose",
            "draft_title",
        )
        assert snap.pending_offer_kind is None
        assert snap.pending_offer_is_confirm is False


# ---------------------------------------------------------------------------
# 4. GOLDEN SERIALIZATION PIN — contract item 4
# ---------------------------------------------------------------------------

GOLDEN_FULL_SNAPSHOT = SessionSnapshot(
    pending_offer_kind="drafted_issue",
    pending_offer_question="Want me to file it, or keep shaping it?",
    pending_offer_is_confirm=True,
    active_process_type="standup",
    draft_in_compose=True,
    draft_title="Fix the login flow",
    recent_issue_number=1595,
    recent_issue_repo="mediajunkie/test-piper-morgan",
    declared_working_mode="execute",
    stored_clear_verb="delete",
)

GOLDEN_SERIALIZED = (
    "OPEN QUESTION (yes/no confirm): [drafted_issue] Want me to file it, or keep shaping it?\n"
    "RULE: a turn that plausibly ANSWERS the open question routes to that "
    "flow's handler, not to a fresh operation. Explicit unrelated commands still route normally.\n"
    "ACTIVE PROCESS: standup (mid-exchange; answers belong to it)\n"
    "DRAFT IN COMPOSE: Fix the login flow — prose likely extends the draft\n"
    "RECENT ISSUE: #1595 in mediajunkie/test-piper-morgan (bare 'it'/'that issue' likely refers here)\n"
    "DECLARED MODE: execute\n"
    "STORED CLEAR-VERB: delete"
)


class TestGoldenSerializationPin:
    def test_fully_populated_snapshot_serializes_exactly(self):
        """THE pin: any edit to serialize_for_prompt, the field order, or the
        caps must update this exact string in the same commit — that
        reviewability is the contract's stated purpose (item 4)."""
        assert serialize_for_prompt(GOLDEN_FULL_SNAPSHOT) == GOLDEN_SERIALIZED

    def test_empty_snapshot_serializes_empty(self):
        assert serialize_for_prompt(SessionSnapshot()) == ""

    def test_field_errors_never_serialized(self):
        """Assembly bookkeeping stays out of the prompt (contract dataclass
        comment: 'never serialized')."""
        snap = SessionSnapshot(field_errors=("active_process_type",))
        assert serialize_for_prompt(snap) == ""


# ---------------------------------------------------------------------------
# 5. Shadow wiring — the serialized block reaches the shadow context;
#    live routing is byte-identical with the feature on/off
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — these turns must resolve "
            "deterministically at the offer seam"
        )


def _stub_router(monkeypatch):
    """Patch the router's LLM call + grammar derivation; capture route()
    invocations. Returns the capture list."""
    from services.intent_service import inversion_router as ir

    calls = []

    async def _route(utterance, session_state=None, **kwargs):
        calls.append(SimpleNamespace(utterance=utterance, session_state=session_state))
        return ir.RoutingDecision(outcome="none", llm_calls=0)

    grammar = ir.RoutingGrammar(operations=(), alias_to_canonical={})
    monkeypatch.setattr(ir, "route", _route)
    monkeypatch.setattr(ir, "derive_routing_grammar", lambda: grammar)
    return calls


async def _drain_shadow_tasks():
    from services.intent_service import inversion_shadow as sh

    for _ in range(10):
        pending = list(sh._INFLIGHT)
        if not pending:
            return
        await asyncio.gather(*pending, return_exceptions=True)
    raise AssertionError("shadow tasks never drained")


class TestShadowWiring:
    async def test_serialized_block_reaches_shadow_context(self, monkeypatch):
        """maybe_schedule_shadow_check(snapshot=...) → the routed
        session_state carries EXACTLY serialize_for_prompt(snapshot), and
        the composed routing prompt contains it verbatim."""
        from services.intent_service import inversion_router as ir
        from services.intent_service.inversion_shadow import (
            maybe_schedule_shadow_check,
        )

        monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
        calls = _stub_router(monkeypatch)

        task = maybe_schedule_shadow_check(
            "yes, file it",
            "query:update_issue",
            session_id=_SESSION,
            user_id=_USER,
            llm_service=object(),
            snapshot=GOLDEN_FULL_SNAPSHOT,
        )
        assert task is not None
        await task

        assert len(calls) == 1
        state = calls[0].session_state
        assert state is not None
        assert state.state_block == GOLDEN_SERIALIZED
        # ...and the composed shadow context (the routing prompt) carries it.
        prompt = ir.build_routing_prompt(
            "yes, file it", ir.derive_routing_grammar(), state
        )
        assert GOLDEN_SERIALIZED in prompt
        assert "Session state:" in prompt

    async def test_no_snapshot_falls_back_to_legacy_peek(self, monkeypatch):
        """snapshot=None keeps the pre-2.0 peek path byte-compatible."""
        monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
        calls = _stub_router(monkeypatch)

        store = WorkflowOfferService()
        offer = build_drafted_issue_offer(_intent(), "Fix the login flow")
        store.set_pending_offer(_SESSION, offer, user_id=_USER)

        task = maybe_schedule_shadow_check_compat(
            "yes", session_id=_SESSION, user_id=_USER, offer_service=store
        )
        assert task is not None
        await task
        state = calls[0].session_state
        assert state.state_block is None
        assert state.pending_offer_summary == (
            f"{CONFIRM_PENDING_ACTION_WORKFLOW} (drafted_issue)"
        )

    async def test_live_result_byte_identical_shadow_on_off(
        self, sm, mem_prefs, monkeypatch
    ):
        """SHADOW-ONLY PROOF: the same deterministic turn (armed confirm +
        'no' → decline copy, never the LLM) produces a byte-identical live
        result with the feature OFF and ON — while the ON run demonstrably
        exercised the shadow lane (route() called)."""
        from services.intent.intent_service import IntentService
        from services.intent_service.classifier import IntentClassifier

        confirm_offer = {
            "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
            "pending_action": {
                "action": "close_issue",
                "intent": _intent("close issue #108", "close_issue"),
                "summary": "close issue #108",
            },
            "decline_message": (
                "Okay — I won't close issue #108. Nothing has been changed."
            ),
        }

        async def _run_turn():
            service = IntentService(
                intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM())
            )
            service.workflow_offer_service.set_pending_offer(
                _SESSION, dict(confirm_offer), user_id=_USER
            )
            result = await service.process_intent(
                message="no", session_id=_SESSION, user_id=_USER
            )
            await _drain_shadow_tasks()
            return result

        # OFF (default)
        monkeypatch.delenv("PIPER_INVERSION_SHADOW", raising=False)
        result_off = await _run_turn()

        # ON — router stubbed (no LLM); assembly runs at the call site.
        monkeypatch.setenv("PIPER_INVERSION_SHADOW", "1")
        calls = _stub_router(monkeypatch)
        result_on = await _run_turn()

        assert calls, "shadow lane never ran — the ON leg proved nothing (m-44)"
        assert result_on.message == result_off.message  # byte-identical copy
        assert result_on.intent_data == result_off.intent_data


def maybe_schedule_shadow_check_compat(message, **kwargs):
    """Legacy-path helper: schedule with production_intent label but NO
    snapshot (keyword omitted entirely, as pre-2.0 callers did)."""
    from services.intent_service.inversion_shadow import maybe_schedule_shadow_check

    return maybe_schedule_shadow_check(
        message, "query:update_issue", llm_service=object(), **kwargs
    )
