"""#1763: a multi-intent plan containing a floor-routed sibling must never
produce the false "ask me again and I'll retry" rider.

THE MECHANISM (verified 2026-09-24, reproduced by ``TestOrchestratorCannotExecuteFloorRoutedSiblings``):

``IntentOrchestrator._execute_single`` gates on ``CanonicalHandlers.can_handle``
(orchestrator.py:196). The real ``can_handle`` set is TEMPORAL / GUIDANCE /
PORTFOLIO / CONVERSATION / PROVENANCE only (canonical_handlers.py:141-157 —
STATUS and PRIORITY were removed by #925 Phase 3 when they were floor-routed,
and #1877 corrected the registry to match). So every floor-routed sibling in a
≥2-substantive plan returns ``success=False,
error="No handler for category: …"`` DETERMINISTICALLY — no exception, no
handler invocation, no data touched — and ``_aggregate_messages`` renders it as

    "I wasn't able to check on project status right now — ask me again and I'll retry."

which is the exact false-retry-promise shape #1198 forbids: retrying reproduces
it byte-for-byte. When EVERY sibling is floor-routed there are zero successes
and the whole turn becomes "I'm having trouble processing that right now."

THE FIX: ``process_intent``'s multi-intent branch orchestrates only when EVERY
substantive sibling is canonical-handleable by the SAME predicate pair the
single-intent path uses (``_is_orchestratable_sibling`` ==
``not _should_route_to_floor(i) and canonical_handlers.can_handle(i)``), and
there are ≥2 of them. Otherwise it skips orchestration and falls into the
single-intent path with a floor-routed sibling as the intent — the floor is a
whole-message surface, so both topics reach the layer that can answer them, and
no failed ``IntentExecutionResult`` is ever produced, which makes the rider
structurally unreachable rather than merely unlikely.
"""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.conversation_context import clear_context, get_or_create_context
from services.intent_service.orchestrator import (
    IntentExecutionResult,
    IntentOrchestrator,
    OrchestratedResponse,
)
from services.intent_service.pre_classifier import MultiIntentResult
from services.shared_types import IntentCategory

TWO_TOPIC_MESSAGE = "what time is it and what's the status of my projects?"

RETRY_RIDER_FRAGMENT = "ask me again and I'll retry"
ALL_FAILED_COPY = "I'm having trouble processing that right now"


def _make_intent(category: IntentCategory, action: str, message: str = TWO_TOPIC_MESSAGE) -> Intent:
    """An intent as a classification surface mints it — carrying the WHOLE message.

    The pre-classifier's multi-intent path binds the full message into
    ``context["original_message"]`` (pre_classifier.py), which is what the floor
    reads for ``FloorContext.user_message``.
    """
    return Intent(
        category=category,
        action=action,
        confidence=1.0,
        original_message=message,
        context={"original_message": message},
    )


# ---------------------------------------------------------------------------
# (1) The probe, as a pin: the orchestrator cannot execute a floor-routed sibling
# ---------------------------------------------------------------------------


class TestOrchestratorCannotExecuteFloorRoutedSiblings:
    """The mechanism, against the REAL CanonicalHandlers — no mocks.

    A blanket ``can_handle`` mock is exactly what hid this bug from the #764
    suite for months (m-43: that measured the branch's plumbing, not the
    registry it dispatches against). These assertions read the real registry.
    """

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "category,action",
        [
            (IntentCategory.STATUS, "get_project_status"),
            (IntentCategory.PRIORITY, "get_top_priority"),
        ],
    )
    async def test_floor_routed_sibling_fails_deterministically(self, category, action):
        orchestrator = IntentOrchestrator(canonical_handlers=CanonicalHandlers())

        result = await orchestrator._execute_single(
            _make_intent(category, action), "sess-1763", None
        )

        assert result.success is False
        assert result.error == f"No handler for category: {category.value}"

    def test_canonical_categories_are_the_only_handleable_ones(self):
        """The contrast that gives the failure above its denominator.

        Registry-level only — deliberately does NOT invoke the TEMPORAL handler,
        which would reach the calendar adapter and the keychain.
        """
        handlers = CanonicalHandlers()

        assert handlers.can_handle(_make_intent(IntentCategory.TEMPORAL, "get_current_time"))
        assert handlers.can_handle(_make_intent(IntentCategory.PORTFOLIO, "manage_portfolio"))
        assert not handlers.can_handle(_make_intent(IntentCategory.STATUS, "get_project_status"))
        assert not handlers.can_handle(_make_intent(IntentCategory.PRIORITY, "get_top_priority"))

    def test_a_failed_result_renders_the_forbidden_retry_rider(self):
        """Why a failed sibling is not survivable: the aggregator promises a retry.

        This is the #1198 violation, pinned at the renderer so the fix cannot be
        mistaken for "the copy is fine now".
        """
        orchestrator = IntentOrchestrator(canonical_handlers=CanonicalHandlers())
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.TEMPORAL, "get_current_time"),
                    response="It's 5:36 PM.",
                    success=True,
                ),
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.STATUS, "get_project_status"),
                    success=False,
                    error="No handler for category: status",
                ),
            ]
        )

        rendered = orchestrator._aggregate_messages(response)

        assert RETRY_RIDER_FRAGMENT in rendered

    def test_all_failed_renders_the_blanket_trouble_copy(self):
        orchestrator = IntentOrchestrator(canonical_handlers=CanonicalHandlers())
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.STATUS, "get_project_status"),
                    success=False,
                    error="No handler for category: status",
                ),
                IntentExecutionResult(
                    intent=_make_intent(IntentCategory.PRIORITY, "get_top_priority"),
                    success=False,
                    error="No handler for category: priority",
                ),
            ]
        )

        assert ALL_FAILED_COPY in orchestrator._aggregate_messages(response)


# ---------------------------------------------------------------------------
# The branch under test
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_classifier():
    classifier = MagicMock()
    classifier.classify_multiple = AsyncMock()
    classifier.classify = AsyncMock()
    return classifier


@pytest.fixture
def intent_service(mock_classifier):
    """IntentService with the REAL CanonicalHandlers registry.

    The registry is the object #1763 turns on, so it is deliberately not
    mocked; only ``handle``/``execute_plan``/the floor are stubbed, so nothing
    reaches a database, a calendar, or an LLM.
    """
    service = IntentService(intent_classifier=mock_classifier)
    handlers = CanonicalHandlers()
    handlers.handle = AsyncMock(
        return_value={
            "message": "Canonical response.",
            "intent": {"category": "temporal", "action": "get_current_time"},
            "requires_clarification": False,
        }
    )
    service.canonical_handlers = handlers
    service.intent_orchestrator = IntentOrchestrator(canonical_handlers=handlers)
    return service


@pytest.fixture
def floor_spy(intent_service):
    """Stub the floor door and hand back the recording mock.

    ``_handle_floor_with_context`` is the narrowest real seam downstream of the
    multi-intent branch on the single-intent path; stubbing it keeps the LLM out
    while still proving WHICH intent the branch handed to the single path.
    """
    spy = AsyncMock(
        return_value=IntentProcessingResult(
            success=True,
            message="Floor answered both topics.",
            intent_data={"category": "status", "action": "get_project_status"},
        )
    )
    with patch.object(intent_service, "_handle_floor_with_context", spy):
        yield spy


def _multi(*intents: Intent) -> MultiIntentResult:
    return MultiIntentResult(
        intents=list(intents),
        original_message=TWO_TOPIC_MESSAGE,
        is_multi_intent=True,
    )


# ---------------------------------------------------------------------------
# (2) A floor-routed sibling: skip orchestration, run the single path
# ---------------------------------------------------------------------------


class TestFloorRoutedSiblingSkipsOrchestration:
    @pytest.mark.asyncio
    async def test_temporal_plus_status_never_produces_the_retry_rider(
        self, intent_service, mock_classifier, floor_spy
    ):
        temporal = _make_intent(IntentCategory.TEMPORAL, "get_current_time")
        status = _make_intent(IntentCategory.STATUS, "get_project_status")
        mock_classifier.classify_multiple.return_value = _multi(temporal, status)

        with (
            patch.object(
                intent_service.intent_orchestrator, "execute_plan", new_callable=AsyncMock
            ) as execute_plan,
            patch.object(intent_service.intent_orchestrator, "create_plan") as create_plan,
        ):
            result = await intent_service.process_intent(
                message=TWO_TOPIC_MESSAGE, session_id="sess-1763-a", user_id=None
            )

            # The orchestrator is never entered — so no failed
            # IntentExecutionResult can exist, so the rider cannot be rendered.
            create_plan.assert_not_called()
            execute_plan.assert_not_called()

        assert not result.multi_intent_orchestrated
        assert RETRY_RIDER_FRAGMENT not in result.message
        assert ALL_FAILED_COPY not in result.message

        # The single path ran, with the FLOOR-ROUTED sibling as the intent.
        floor_spy.assert_called_once()
        routed_intent = floor_spy.call_args.args[0]
        assert routed_intent.category == IntentCategory.STATUS
        assert routed_intent.action == "get_project_status"

    @pytest.mark.asyncio
    async def test_the_floor_receives_the_whole_message_not_a_fragment(
        self, intent_service, mock_classifier, floor_spy
    ):
        """Both topics must reach the floor, or the fix trades one silent loss for another.

        ``_handle_floor_with_context`` builds ``FloorContext.user_message`` from
        ``intent.original_message or intent.context["original_message"]``, so a
        sibling minted without either would floor with an EMPTY message.
        """
        temporal = _make_intent(IntentCategory.TEMPORAL, "get_current_time")
        # A sibling that carries NEITHER — the branch must backfill it.
        bare_status = Intent(
            category=IntentCategory.STATUS, action="get_project_status", confidence=1.0
        )
        mock_classifier.classify_multiple.return_value = _multi(temporal, bare_status)

        await intent_service.process_intent(
            message=TWO_TOPIC_MESSAGE, session_id="sess-1763-b", user_id=None
        )

        routed_intent = floor_spy.call_args.args[0]
        whole_message = routed_intent.original_message or routed_intent.context.get(
            "original_message", ""
        )
        assert whole_message == TWO_TOPIC_MESSAGE

    @pytest.mark.asyncio
    async def test_a_bound_original_message_is_never_overwritten(
        self, intent_service, mock_classifier, floor_spy
    ):
        """Backfill only fills an absence; a surface's own binding wins."""
        temporal = _make_intent(IntentCategory.TEMPORAL, "get_current_time")
        status = _make_intent(
            IntentCategory.STATUS, "get_project_status", message="a surface bound this"
        )
        mock_classifier.classify_multiple.return_value = _multi(temporal, status)

        await intent_service.process_intent(
            message=TWO_TOPIC_MESSAGE, session_id="sess-1763-c", user_id=None
        )

        assert floor_spy.call_args.args[0].original_message == "a surface bound this"


# ---------------------------------------------------------------------------
# (3) All-canonical plans still orchestrate — the fix is a narrowing, not a kill
# ---------------------------------------------------------------------------


class TestAllCanonicalPlanStillOrchestrates:
    @pytest.mark.asyncio
    async def test_temporal_plus_portfolio_orchestrates(self, intent_service, mock_classifier):
        temporal = _make_intent(IntentCategory.TEMPORAL, "get_current_time")
        portfolio = _make_intent(IntentCategory.PORTFOLIO, "manage_portfolio")
        mock_classifier.classify_multiple.return_value = _multi(temporal, portfolio)

        with patch.object(
            intent_service.intent_orchestrator, "execute_plan", new_callable=AsyncMock
        ) as execute_plan:
            execute_plan.return_value = OrchestratedResponse(
                results=[
                    IntentExecutionResult(intent=temporal, response="It's 5:36 PM.", success=True),
                    IntentExecutionResult(
                        intent=portfolio, response="Three active projects.", success=True
                    ),
                ],
                aggregated_message="It's 5:36 PM. As for your portfolio, three active projects.",
            )

            result = await intent_service.process_intent(
                message="what time is it and what's in my portfolio?",
                session_id="sess-1763-d",
                user_id=None,
            )

            execute_plan.assert_called_once()

        assert result.multi_intent_orchestrated
        assert RETRY_RIDER_FRAGMENT not in result.message

    def test_the_predicate_agrees_with_the_single_path(self, intent_service):
        """The predicate IS the single path's pair — including for PROVENANCE.

        ``_requires_canonical_handler`` alone would be the wrong predicate: it
        returns False for PROVENANCE, while the single path still routes
        PROVENANCE canonically because PROVENANCE is absent from
        ``_FLOOR_ROUTED_CATEGORIES``. Pinned so a later "simplification" to the
        single gate cannot silently strand a canonical category on the floor.
        """
        provenance = _make_intent(IntentCategory.PROVENANCE, "explain_suggestion")

        assert intent_service._requires_canonical_handler(provenance) is False
        assert intent_service._should_route_to_floor(provenance) is False
        assert intent_service._is_orchestratable_sibling(provenance) is True

    def test_predicate_failure_defaults_to_skipping_orchestration(self, intent_service):
        """A raising predicate must not break the turn — the floor is the safe default."""
        intent_service.canonical_handlers.can_handle = MagicMock(
            side_effect=RuntimeError("registry exploded")
        )

        assert (
            intent_service._is_orchestratable_sibling(
                _make_intent(IntentCategory.PORTFOLIO, "manage_portfolio")
            )
            is False
        )


# ---------------------------------------------------------------------------
# The skip must never drop a side effect — found by the #1818 ratchet, not by
# inspection, so it is pinned here where a reader of #1763 will see it
# ---------------------------------------------------------------------------


class TestSkipPreservesSideEffectingSiblings:
    """A PORTFOLIO / EXECUTION sibling wins the skip over a floor-routed one.

    THE LIVE SHAPE, probed 2026-09-24: the plain command
    ``"archive project X in my portfolio"`` is split by the pre-classifier into
    PORTFOLIO/manage_portfolio + a PHANTOM STATUS/get_project_status sibling —
    the same phantom class #1738 narrowed, whose ``_apply_subsumption_filter``
    rule covers only the LIST claim, not archive/add/delete phrasings. So this
    is not a contrived plan: it is what a one-topic archive command actually
    produces today, and at HEAD it earned the user a successful archive with
    the false retry rider stapled on.

    Naively choosing "the first floor-routed sibling" would hand that turn to
    the floor, which would stop performing the archive (a WRITE silently
    becoming a conversation) and start billing a keyless turn — caught by
    ``test_spend_free_canonical_ratchet_1818.py``'s PORTFOLIO case going red.
    """

    def test_the_archive_command_no_longer_produces_a_phantom_status_sibling(self):
        """The premise, measured — not assumed. When this class was written
        (2026-09-24, morning) the pre-classifier DID split this message into
        PORTFOLIO + a phantom STATUS sibling — the live occasion the gate below
        exists for. #1884 (same day, evening) widened #1738's subsumption to the
        whole PORTFOLIO write family, so the split is gone at surface 1. Pin the
        new truth (m-44): the archive command is single-intent PORTFOLIO. The
        gate itself is still exercised by the mocked two-intent plan in the next
        test, which is the shape a future phantom would take."""
        from services.intent_service.pre_classifier import PreClassifier

        detected = PreClassifier.detect_multiple_intents("archive project X in my portfolio")

        assert not detected.is_multi_intent
        assert [(i.category.name, i.action) for i in detected.intents] == [
            ("PORTFOLIO", "manage_portfolio"),
        ]

    @pytest.mark.asyncio
    async def test_portfolio_sibling_wins_over_a_floor_routed_one(
        self, intent_service, mock_classifier, floor_spy
    ):
        message = "archive project X in my portfolio"
        portfolio = _make_intent(IntentCategory.PORTFOLIO, "manage_portfolio", message=message)
        phantom_status = _make_intent(IntentCategory.STATUS, "get_project_status", message=message)
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[portfolio, phantom_status],
            original_message=message,
            is_multi_intent=True,
        )

        with patch.object(
            intent_service.intent_orchestrator, "execute_plan", new_callable=AsyncMock
        ) as execute_plan:
            result = await intent_service.process_intent(
                message=message, session_id="sess-1763-h", user_id=None
            )

            execute_plan.assert_not_called()

        # The canonical PORTFOLIO handler ran — the side effect survives.
        intent_service.canonical_handlers.handle.assert_awaited_once()
        handled_intent = intent_service.canonical_handlers.handle.await_args.args[0]
        assert handled_intent.category == IntentCategory.PORTFOLIO

        # ...and the turn never reached the floor, so it spends nothing.
        floor_spy.assert_not_called()
        assert RETRY_RIDER_FRAGMENT not in result.message

    @pytest.mark.asyncio
    async def test_the_choice_is_logged_as_side_effect_preservation(
        self, intent_service, mock_classifier
    ):
        message = "archive project X in my portfolio"
        mock_classifier.classify_multiple.return_value = MultiIntentResult(
            intents=[
                _make_intent(IntentCategory.PORTFOLIO, "manage_portfolio", message=message),
                _make_intent(IntentCategory.STATUS, "get_project_status", message=message),
            ],
            original_message=message,
            is_multi_intent=True,
        )

        with patch.object(intent_service, "logger", MagicMock()) as logger:
            await intent_service.process_intent(
                message=message, session_id="sess-1763-i", user_id=None
            )

        skips = [
            call
            for call in logger.info.call_args_list
            if call.args and call.args[0] == "multi_intent_orchestration_skipped"
        ]
        assert len(skips) == 1
        assert skips[0].kwargs["chosen_because"] == "side_effecting_sibling_preserved"
        assert skips[0].kwargs["chosen_category"] == "portfolio"


# ---------------------------------------------------------------------------
# (4) Every sibling floor-routed — the "I'm having trouble" case
# ---------------------------------------------------------------------------


class TestAllSiblingsFloorRouted:
    @pytest.mark.asyncio
    async def test_status_plus_priority_never_produces_the_blanket_trouble_copy(
        self, intent_service, mock_classifier, floor_spy
    ):
        status = _make_intent(IntentCategory.STATUS, "get_project_status")
        priority = _make_intent(IntentCategory.PRIORITY, "get_top_priority")
        mock_classifier.classify_multiple.return_value = _multi(status, priority)

        with patch.object(
            intent_service.intent_orchestrator, "execute_plan", new_callable=AsyncMock
        ) as execute_plan:
            result = await intent_service.process_intent(
                message="what's my project status and my top priority?",
                session_id="sess-1763-e",
                user_id=None,
            )

            execute_plan.assert_not_called()

        assert ALL_FAILED_COPY not in result.message
        assert RETRY_RIDER_FRAGMENT not in result.message
        assert result.success

        # The FIRST floor-routed sibling in plan order is chosen — deterministic.
        assert floor_spy.call_args.args[0].category == IntentCategory.STATUS

    @pytest.mark.asyncio
    async def test_the_skip_decision_is_logged_with_reason_and_categories(
        self, intent_service, mock_classifier, floor_spy
    ):
        """A live transcript has to be readable against the decision (#1763 AC).

        Without the log, "why did this turn not orchestrate?" is unanswerable
        from production output alone.
        """
        temporal = _make_intent(IntentCategory.TEMPORAL, "get_current_time")
        status = _make_intent(IntentCategory.STATUS, "get_project_status")
        mock_classifier.classify_multiple.return_value = _multi(temporal, status)

        with patch.object(intent_service, "logger", MagicMock()) as logger:
            await intent_service.process_intent(
                message=TWO_TOPIC_MESSAGE, session_id="sess-1763-f", user_id=None
            )

        skips = [
            call
            for call in logger.info.call_args_list
            if call.args and call.args[0] == "multi_intent_orchestration_skipped"
        ]
        assert len(skips) == 1
        fields = skips[0].kwargs
        assert fields["reason"] == "floor_routed_sibling"
        assert fields["floor_routed_categories"] == ["status"]
        assert fields["orchestratable_categories"] == ["temporal"]
        assert fields["chosen_category"] == "status"
        assert fields["chosen_action"] == "get_project_status"
        assert fields["chosen_because"] == "first_floor_routed_sibling"

    @pytest.mark.asyncio
    async def test_no_canonical_sibling_reason_when_every_sibling_is_floor_routed(
        self, intent_service, mock_classifier, floor_spy
    ):
        status = _make_intent(IntentCategory.STATUS, "get_project_status")
        priority = _make_intent(IntentCategory.PRIORITY, "get_top_priority")
        mock_classifier.classify_multiple.return_value = _multi(status, priority)

        with patch.object(intent_service, "logger", MagicMock()) as logger:
            await intent_service.process_intent(
                message="what's my project status and my top priority?",
                session_id="sess-1763-g",
                user_id=None,
            )

        skips = [
            call
            for call in logger.info.call_args_list
            if call.args and call.args[0] == "multi_intent_orchestration_skipped"
        ]
        assert len(skips) == 1
        assert skips[0].kwargs["reason"] == "no_canonical_sibling"
        assert skips[0].kwargs["orchestratable_categories"] == []


# ---------------------------------------------------------------------------
# #1533 principal-keyed sibling — the skip path threads the real user_id
# ---------------------------------------------------------------------------


class TestFloorSiblingSkipAuthenticated:
    """#1533 (principal-dropping audit) — every call above passes user_id=None.

    The #1763 skip path re-enters the single-intent path mid-turn, which still
    runs through ``process_intent``'s outer turn-recording seam
    (``get_or_create_context``). If the skip ever dropped user_id, two
    authenticated users sharing one session_id would collapse onto the same
    context and nothing above would see it (m-44: a probe where the anonymous
    and authenticated keys coincide is a config check, not a verification).
    """

    @pytest.mark.asyncio
    async def test_skip_path_does_not_leak_turns_across_authenticated_users(
        self, intent_service, mock_classifier, floor_spy
    ):
        session_id = str(uuid4())
        user_a = str(uuid4())
        user_b = str(uuid4())

        mock_classifier.classify_multiple.return_value = _multi(
            _make_intent(IntentCategory.TEMPORAL, "get_current_time"),
            _make_intent(IntentCategory.STATUS, "get_project_status"),
        )

        try:
            await intent_service.process_intent(
                message=TWO_TOPIC_MESSAGE, session_id=session_id, user_id=user_a
            )
            await intent_service.process_intent(
                message=TWO_TOPIC_MESSAGE, session_id=session_id, user_id=user_b
            )

            ctx_a = get_or_create_context(session_id, user_id=user_a)
            ctx_b = get_or_create_context(session_id, user_id=user_b)

            assert ctx_a is not ctx_b, (
                "two distinct authenticated users sharing a session_id collapsed "
                "onto the same context on the #1763 orchestration-skip path — "
                "user_id was dropped"
            )
            assert len(ctx_a.turns) == 1 and len(ctx_b.turns) == 1

            # The principal also reaches the floor door the skip hands off to.
            assert floor_spy.call_args.kwargs.get("user_id") == user_b
        finally:
            clear_context(session_id, user_a)
            clear_context(session_id, user_b)
