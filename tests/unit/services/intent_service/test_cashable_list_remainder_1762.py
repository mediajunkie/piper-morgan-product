"""#1762 epic 6, first build — the "…and N more" claim becomes CASHABLE for the
GitHub six (issues, PRs, milestones, releases, labels, branches).

THE RULING under test (three memos, 2026-09-13, all in mailboxes/lead/read/):

- **Arch**: ``GatherOutcome`` is the remainder's home. Three ratified pieces
  compose to it — CXO's contract §5b ("'…and N more' is a claim the assistant
  must be able to CASH"), the #1738 joint invariant (the renderer CONSUMES
  provenance and never writes it; the model's context gets the OUTCOME, not
  the rendered string), and the acceptance contract giving the follow-up its
  consume path ("show me the rest" = an armed offer over the stored
  remainder). *"RETURNS them, from the outcome, not a re-fetch that might
  disagree with the claim."*
- **PPM**: GitHub-six-first. Threshold — **skip the offer when the hidden
  remainder is 3 or fewer**; just render them all. An offer to reveal 1-3
  items is ceremony.
- **CXO** (§5b-i): the copy is *"That's 5 of 340 — say the word and I'll pull
  the rest."* — what they're HOLDING, not what's missing; the affordance, never
  the syntax; the source's own denominator, never a fabricated exact number.

THE HINGE, and why this suite's headline test looks the way it does — CXO's
constraint, which nobody had named:

> ⚠️ arms live exactly ONE turn, **but a capped-list offer is precisely the
> kind users answer LATE**. An acceptance test of "…and 335 more" → immediate
> next turn asks → returns them **passes without exercising the property that
> actually fails.**

So the acceptance test here is
``test_the_late_follow_up_still_cashes_after_an_intervening_turn`` — offer,
then an unrelated turn in between, THEN the ask. The immediate-follow-up test
is kept as its weaker sibling, explicitly labelled as insufficient on its own,
so nobody mistakes it for the acceptance criterion.

LAYER HONESTY (m-43). Three layers, named per class:
- ``TestTheRenderer`` is the pure composition unit — no service, no session.
- ``TestTheSixHandlers`` drives the REAL handler methods with the GitHub
  routers/adapters mocked at the network boundary, then reads the session
  store. It measures render AND arm, which is what the six actually own.
- ``TestTheLateFollowUp`` / ``TestStaleRemainder`` / ``TestPrecedence`` drive
  the REAL ``IntentService.process_intent`` with the LLM boundary explosive —
  the turn pipeline is the layer where "arms live one turn" actually bites, so
  a unit test of the consume method alone could not have caught it.

DENOMINATOR (m-44): the six handlers named above, which is the whole of
#1762's class-(b) GitHub cohort (census e8f6128cf). The other class-(b) sites
(portfolio/floor domain_context) are NOT covered here — PPM's ordering call
puts them after this build.
"""

from datetime import datetime, timedelta
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.conversation_context import get_or_create_context
from services.intent_service.list_remainder import (
    REMAINDER_MAX_AGE_MINUTES,
    REMAINDER_OFFER_THRESHOLD,
    ListRemainder,
    compose_capped_list,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

_USER = "5a2c9d10-1762-4b00-9e00-000000001762"  # valid UUID: survives principal parsing

# The INTERVENING turn. Deliberately neither an accept nor a decline nor a
# question (verdict PASS), so the late-follow-up test measures survival across
# an ordinary aside rather than across the §5a state-question path.
_ASIDE = "i was reading about vector databases earlier"
_ASIDE_REPLY = "Noted — nothing pending on my side."


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    these tests must resolve deterministically."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1762 turns must resolve deterministically"
        )


@pytest.fixture
def live_service():
    register_default_workflows()
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _store(sid, user_id=_USER):
    return get_or_create_context(sid, user_id=user_id).pending_list_remainder


def _clear(sid, user_id=_USER):
    get_or_create_context(sid, user_id=user_id).pending_list_remainder = None


def _intent(message="show me my issues"):
    return Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        confidence=0.95,
        original_message=message,
        context={"original_message": message, "user_id": _USER},
    )


def _issue(n):
    return {"number": n, "title": f"Issue number {n}", "labels": []}


# ---------------------------------------------------------------------------
# 1. THE RENDERER — pure composition (no service, no session)
# ---------------------------------------------------------------------------


class TestTheRenderer:
    """Layer: ``compose_capped_list`` alone. Measures the copy and the split
    between what is shown and what is stored."""

    def test_offer_reads_as_what_you_are_holding_not_what_is_missing(self):
        """CXO §5b-i decision 1: "5 of 340", NOT "…and 335 more"."""
        lines = [f"\n- item {i}" for i in range(340)]
        rendered = compose_capped_list(lines=lines, cap=5, kind="open issues", source_total=340)
        assert "That's 5 of 340 — say the word and I'll pull the rest." in rendered.body
        assert "335 more" not in rendered.body
        assert "...and" not in rendered.body

    def test_the_shown_half_stops_at_the_cap_and_the_stored_half_is_the_tail(self):
        lines = [f"\n- item {i}" for i in range(340)]
        rendered = compose_capped_list(lines=lines, cap=5, kind="open issues", source_total=340)
        assert rendered.body.count("\n- item ") == 5
        assert rendered.remainder is not None
        # Render == the data it claims: the stored tail is exactly the set the
        # copy says is still available.
        assert len(rendered.remainder.lines) == 335
        assert rendered.remainder.lines[0] == "\n- item 5"
        assert rendered.remainder.lines[-1] == "\n- item 339"

    def test_a_remainder_of_three_or_fewer_gets_shown_instead_of_offered(self):
        """PPM's threshold: an offer to reveal 1-3 items is ceremony."""
        for hidden in range(REMAINDER_OFFER_THRESHOLD + 1):
            lines = [f"\n- item {i}" for i in range(5 + hidden)]
            rendered = compose_capped_list(
                lines=lines, cap=5, kind="labels", source_total=5 + hidden
            )
            assert rendered.remainder is None, f"{hidden} hidden should not arm an offer"
            assert "say the word" not in rendered.body
            assert (
                rendered.body.count("\n- item ") == 5 + hidden
            ), f"{hidden} hidden items must be RENDERED, not silently dropped"

    def test_one_past_the_threshold_earns_the_offer(self):
        lines = [f"\n- item {i}" for i in range(5 + REMAINDER_OFFER_THRESHOLD + 1)]
        rendered = compose_capped_list(lines=lines, cap=5, kind="labels", source_total=len(lines))
        assert rendered.remainder is not None
        assert "say the word" in rendered.body

    def test_a_paged_source_offers_only_what_it_can_actually_cash(self):
        """The issues case: the SOURCE says 179, we hold a 50-item page. CXO's
        stale-remainder rule generalized — promising "the rest" here would be
        a promise only a re-fetch could keep, and a re-fetch is the fabricated
        continuity §5b-i forbids."""
        lines = [f"\n- item {i}" for i in range(50)]
        rendered = compose_capped_list(lines=lines, cap=5, kind="open issues", source_total=179)
        assert "That's 5 of 179" in rendered.body
        assert "I have 50 of them in front of me" in rendered.body
        assert "pull the rest" not in rendered.body
        assert rendered.remainder is not None
        assert len(rendered.remainder.lines) == 45

    def test_the_denominator_is_the_sources_own_count_never_a_fabricated_one(self):
        """CXO §5b-i decision 3: if the source says ``1000+``, we say
        ``1000+`` — a cap rendered as an exact number is a fabricated
        denominator."""
        lines = [f"\n- item {i}" for i in range(50)]
        rendered = compose_capped_list(
            lines=lines,
            cap=5,
            kind="open issues",
            source_total=1000,
            source_total_display="1000+",
        )
        assert "That's 5 of 1000+" in rendered.body
        assert "of 1000 " not in rendered.body
        assert rendered.remainder.source_total_display == "1000+"

    def test_holding_everything_but_less_than_the_source_says_makes_no_offer(self):
        """held <= cap but the source has more: nothing is cashable, so
        nothing is offered — and the turn says what is in hand rather than
        letting the header's total imply we showed it."""
        lines = [f"\n- item {i}" for i in range(4)]
        rendered = compose_capped_list(lines=lines, cap=5, kind="open issues", source_total=179)
        assert rendered.remainder is None
        assert "say the word" not in rendered.body
        assert "That's all 4 I have in front of me, out of 179." in rendered.body

    def test_an_incoherent_source_total_never_prints_below_what_we_hold(self):
        lines = [f"\n- item {i}" for i in range(10)]
        rendered = compose_capped_list(lines=lines, cap=5, kind="labels", source_total=2)
        assert "That's 5 of 10" in rendered.body


# ---------------------------------------------------------------------------
# 2. THE SIX HANDLERS — render + arm, at the real handler methods
# ---------------------------------------------------------------------------


def _router_stub(**payloads):
    router = MagicMock()
    router.initialize = AsyncMock(return_value=None)
    router.is_available = AsyncMock(return_value=True)
    for name, value in payloads.items():
        setattr(router, name, AsyncMock(return_value=value))
    return router


def _connector_not_connected():
    """Force the native-PAT path (CONNECT_REQUIRED) so the GitHub six run
    their router branch deterministically."""
    from services.mcp.consumer.connector import DegradationReason

    return SimpleNamespace(
        issues=None,
        total=None,
        degradation=SimpleNamespace(
            reason=DegradationReason.CONNECT_REQUIRED, user_message="connect github"
        ),
    )


class TestTheSixHandlers:
    """Layer: the real handler methods, GitHub mocked at the network boundary.
    Denominator: all six of #1762's class-(b) GitHub cohort."""

    pytestmark = pytest.mark.asyncio

    async def test_issues_render_offers_and_arms(self, live_service):
        sid = "1762-handler-issues"
        _clear(sid)
        router = _router_stub(get_open_issues=[_issue(n) for n in range(100, 150)])
        adapter = MagicMock()
        adapter.list_open_issues = AsyncMock(return_value=_connector_not_connected())
        with (
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter",
                return_value=adapter,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
        ):
            result = await live_service._handle_list_issues_query(_intent(), "wf", sid)
        assert "say the word" in result.message
        assert result.intent_data["list_remainder_offer_pending"] is True
        stored = _store(sid)
        assert stored is not None and len(stored.lines) == 45
        assert stored.kind == "open issues"

    async def test_prs_render_offers_and_arms(self, live_service):
        sid = "1762-handler-prs"
        _clear(sid)
        prs = [
            {
                "number": n,
                "title": f"PR {n}",
                "html_url": f"u/{n}",
                "pull_request": {"url": f"u/{n}"},
            }
            for n in range(20)
        ]
        router = _router_stub(get_open_issues=prs)
        adapter = MagicMock()
        adapter.list_open_prs = AsyncMock(return_value=_connector_not_connected())
        with (
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter",
                return_value=adapter,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
        ):
            result = await live_service._handle_list_prs_query(_intent(), "wf", sid)
        assert "That's 5 of 20 — say the word and I'll pull the rest." in result.message
        assert _store(sid) is not None and len(_store(sid).lines) == 15

    async def test_milestones_render_offers_and_arms(self, live_service):
        sid = "1762-handler-milestones"
        _clear(sid)
        ms = [{"title": f"M{n}", "due_on": None, "open_issues": n} for n in range(12)]
        router = _router_stub(list_milestones_via_mcp=ms)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await live_service._handle_list_milestones_query(_intent(), "wf", sid)
        assert "That's 5 of 12" in result.message
        assert _store(sid) is not None and len(_store(sid).lines) == 7

    async def test_releases_render_offers_and_arms(self, live_service):
        sid = "1762-handler-releases"
        _clear(sid)
        rels = [
            {"tag_name": f"v{n}", "name": f"rel {n}", "published_at": None, "prerelease": False}
            for n in range(11)
        ]
        router = _router_stub(list_releases_via_mcp=rels)
        adapter = MagicMock()
        adapter.list_releases_connector = AsyncMock(
            return_value=SimpleNamespace(
                items=None,
                degradation=_connector_not_connected().degradation,
            )
        )
        with (
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter",
                return_value=adapter,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
        ):
            result = await live_service._handle_list_releases_query(_intent(), "wf", sid)
        assert "That's 5 of 11" in result.message
        assert _store(sid) is not None and len(_store(sid).lines) == 6

    async def test_labels_render_offers_and_arms(self, live_service):
        sid = "1762-handler-labels"
        _clear(sid)
        labels = [{"name": f"label-{n:03d}", "description": ""} for n in range(40)]
        router = _router_stub(list_labels_via_mcp=labels)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await live_service._handle_list_labels_query(_intent(), "wf", sid)
        assert "That's 20 of 40" in result.message
        assert _store(sid) is not None and len(_store(sid).lines) == 20

    async def test_branches_render_offers_and_arms(self, live_service):
        sid = "1762-handler-branches"
        _clear(sid)
        payload = {
            "branches": [{"name": f"branch-{n:03d}", "protected": False} for n in range(30)],
            "default_branch": "main",
        }
        router = _router_stub(list_branches_via_mcp=payload)
        adapter = MagicMock()
        adapter.list_branches_connector = AsyncMock(
            return_value=SimpleNamespace(
                items=None, degradation=_connector_not_connected().degradation
            )
        )
        with (
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter",
                return_value=adapter,
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
        ):
            result = await live_service._handle_list_branches_query(_intent(), "wf", sid)
        assert "That's 20 of 30" in result.message
        assert _store(sid) is not None and len(_store(sid).lines) == 10

    async def test_no_site_still_makes_the_uncashable_and_n_more_claim(self, live_service):
        """The #1762 class-(b) defect itself: none of the six may emit a bare
        '…and N more' any more — the claim it made was one it could not cash."""
        import inspect

        import services.intent.intent_service as mod

        source = inspect.getsource(mod)
        for handler in (
            "_handle_list_issues_query",
            "_handle_list_prs_query",
            "_handle_list_milestones_query",
            "_handle_list_releases_query",
            "_handle_list_labels_query",
            "_handle_list_branches_query",
        ):
            body = source.split(f"async def {handler}(")[1].split("\n    async def ")[0]
            assert "...and " not in body, f"{handler} still makes an uncashable claim"

    async def test_a_small_list_is_rendered_whole_with_no_offer(self, live_service):
        """PPM's threshold at the handler layer: 22 labels, cap 20, 2 hidden —
        render all 22, no ceremony."""
        sid = "1762-handler-labels-small"
        _clear(sid)
        labels = [{"name": f"label-{n:03d}", "description": ""} for n in range(22)]
        router = _router_stub(list_labels_via_mcp=labels)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            result = await live_service._handle_list_labels_query(_intent(), "wf", sid)
        assert "say the word" not in result.message
        assert result.message.count("\n- **label-") == 22
        assert _store(sid) is None
        assert "list_remainder_offer_pending" not in result.intent_data


# ---------------------------------------------------------------------------
# 3. THE ACCEPTANCE TEST — the LATE follow-up (CXO's hinge)
# ---------------------------------------------------------------------------


def _stub_fallthrough_routing(service, message):
    """An intervening turn whose own routing is not under test (the #1753
    idiom): classification returns low-confidence UNKNOWN, the floor door is
    patched, and the patched result carries no arm flag."""
    from services.intent_service.pre_classifier import MultiIntentResult

    fallback = Intent(
        category=IntentCategory.UNKNOWN,
        action="unknown",
        confidence=0.2,
        original_message=message,
        context={"original_message": message},
    )
    return (
        patch.object(
            service.intent_classifier,
            "classify_multiple",
            new=AsyncMock(
                return_value=MultiIntentResult(intents=[fallback], original_message=message)
            ),
        ),
        patch.object(
            service,
            "_handle_unknown_intent",
            new=AsyncMock(
                return_value=IntentProcessingResult(
                    success=True, message=_ASIDE_REPLY, intent_data={}
                )
            ),
        ),
        patch.object(
            service,
            "_handle_floor_with_context",
            new=AsyncMock(
                return_value=IntentProcessingResult(
                    success=True, message=_ASIDE_REPLY, intent_data={}
                )
            ),
        ),
    )


def _inert_registry():
    mock_registry = MagicMock()
    mock_registry.check_suspended_processes = AsyncMock(return_value=None)
    mock_registry.check_active_processes = AsyncMock(
        return_value=SimpleNamespace(
            handled=False, escaped=False, response_message=None, process_type=None
        )
    )
    return patch("services.intent.intent_service.get_process_registry"), mock_registry


def _arm_a_capped_list(sid, *, held=50, source_total=179, cap=5, kind="open issues"):
    """Arm the store the way a handler's render does — through the SAME
    composer, so the test can never drift from the production split."""
    lines = [f"\n- **#{100 + i}**: Issue number {100 + i}" for i in range(held)]
    rendered = compose_capped_list(lines=lines, cap=cap, kind=kind, source_total=source_total)
    ctx = get_or_create_context(sid, user_id=_USER)
    ctx.pending_list_remainder = rendered.remainder
    ctx.last_offer = None
    return rendered


class TestTheLateFollowUp:
    """⭐ THE acceptance test. Layer: the REAL ``process_intent`` turn
    pipeline, which is where "arms live exactly one turn" actually bites."""

    pytestmark = pytest.mark.asyncio

    async def test_the_late_follow_up_still_cashes_after_an_intervening_turn(self, live_service):
        """CXO's hinge, stated in her words: *a capped-list offer is exactly
        the kind a user answers LATE — they read the five, think, come back.*
        Offer → an unrelated turn about the weather → THEN "show me the rest".

        RED pre-fix in two distinct ways, and the second is the point: with no
        store at all the ask falls to the classifier; with the offer on the
        one-turn ``last_offer`` rail the intervening turn's unconditional pop
        destroys it and the later ask lands on nothing (#1694's felt shape).
        """
        sid = "1762-e2e-late-follow-up"
        armed = _arm_a_capped_list(sid)
        assert armed.remainder is not None

        # --- the INTERVENING turn: something else entirely -----------------
        aside = _ASIDE
        p_registry, mock_registry = _inert_registry()
        p_classify, p_floor, p_floor2 = _stub_fallthrough_routing(live_service, aside)
        with p_registry as registry_fn, p_classify, p_floor, p_floor2:
            registry_fn.return_value = mock_registry
            interim = await live_service.process_intent(
                message=aside, session_id=sid, user_id=_USER
            )
        assert _ASIDE_REPLY in interim.message, "the intervening turn must be answered normally"
        assert _store(sid) is not None, (
            "the arm must SURVIVE the intervening turn — this is the property a "
            "next-turn-only acceptance test cannot see"
        )

        # --- the LATE ask ---------------------------------------------------
        p_registry, mock_registry = _inert_registry()
        with p_registry as registry_fn:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message="show me the rest", session_id=sid, user_id=_USER
            )

        assert result.success
        assert result.intent_data["action"] == "list_remainder_cash"
        assert result.intent_data["context"]["returned"] == 45
        assert result.intent_data["context"]["refetched"] is False
        # The items themselves, not a description of them.
        assert "**#105**" in result.message
        assert "**#149**" in result.message
        assert "**#100**" not in result.message, "already shown; the cash is the TAIL"
        # Spent: the offer cannot be cashed twice.
        assert _store(sid) is None

    async def test_the_immediate_follow_up_also_cashes_but_proves_less(self, live_service):
        """The weaker sibling, kept and labelled. CXO: an acceptance test of
        '…and 335 more' → immediate next turn asks → returns them **passes
        without exercising the property that actually fails**. It is here as a
        no-regression pin, NOT as the acceptance criterion."""
        sid = "1762-e2e-immediate-follow-up"
        _arm_a_capped_list(sid)
        p_registry, mock_registry = _inert_registry()
        with p_registry as registry_fn:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.intent_data["action"] == "list_remainder_cash"

    @pytest.mark.parametrize(
        "phrasing",
        [
            "yes",  # the shared vocabulary — the affordance, not a syntax
            "yes please",
            "sure",
            "go ahead",
            "show me the rest",  # taught by the offer's own copy
            "the rest",
            "show them all",
            "say the word",
        ],
    )
    async def test_more_than_one_phrasing_cashes_the_offer(self, live_service, phrasing):
        """CXO §5b-i decision 2: offer the affordance, never the syntax — *if
        only one phrasing works, that's an acceptance-contract defect*. The
        taught list is ADDITIVE over the shared vocabulary, never a
        substitute, so a plain "yes" still works."""
        sid = f"1762-e2e-phrasing-{phrasing.replace(' ', '-')}"
        _arm_a_capped_list(sid)
        p_registry, mock_registry = _inert_registry()
        with p_registry as registry_fn:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message=phrasing, session_id=sid, user_id=_USER
            )
        assert result.intent_data.get("action") == "list_remainder_cash", phrasing

    async def test_a_decline_clears_the_offer_and_never_composes_a_reply(self, live_service):
        sid = "1762-e2e-decline"
        _arm_a_capped_list(sid)
        p_registry, mock_registry = _inert_registry()
        p_classify, p_floor, p_floor2 = _stub_fallthrough_routing(live_service, "no thanks")
        with p_registry as registry_fn, p_classify, p_floor, p_floor2:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message="no thanks", session_id=sid, user_id=_USER
            )
        assert result.intent_data.get("action") != "list_remainder_cash"
        assert _store(sid) is None, "a decline spends the offer"

    async def test_a_state_question_leaves_the_arm_standing(self, live_service):
        """The stated survival form is PERSISTING, which subsumes §5a: contract
        axis (a) says a question-form never accepts, and at this seam it also
        never costs the user the pending offer."""
        sid = "1762-e2e-state-question"
        _arm_a_capped_list(sid)
        q = "how many did you say there were?"
        p_registry, mock_registry = _inert_registry()
        p_classify, p_floor, p_floor2 = _stub_fallthrough_routing(live_service, q)
        with p_registry as registry_fn, p_classify, p_floor, p_floor2:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(message=q, session_id=sid, user_id=_USER)
        assert result.intent_data.get("action") != "list_remainder_cash"
        assert _store(sid) is not None


# ---------------------------------------------------------------------------
# 4. STALE / ABSENT REMAINDER — the honest turn, never a silent re-fetch
# ---------------------------------------------------------------------------


class TestStaleRemainder:
    """CXO §5b-i: *if the stored remainder is gone or stale, the honest turn
    says the list moved and offers a fresh read. A silent re-fetch presented
    as "the rest" is a fabrication of continuity* — the user believes they are
    holding items 6-340 of the list they saw, and they aren't."""

    pytestmark = pytest.mark.asyncio

    async def test_a_stale_remainder_says_the_list_moved(self, live_service):
        sid = "1762-e2e-stale"
        _arm_a_capped_list(sid)
        stored = _store(sid)
        stored.armed_at = datetime.now() - timedelta(minutes=REMAINDER_MAX_AGE_MINUTES + 1)
        p_registry, mock_registry = _inert_registry()
        with p_registry as registry_fn:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message="show me the rest", session_id=sid, user_id=_USER
            )
        assert result.intent_data["action"] == "list_remainder_moved"
        assert "moved on" in result.message
        assert "ask me for them again" in result.message.lower()
        # NOT the items: presenting a stale set as "the rest" is the failure.
        assert "**#105**" not in result.message
        assert _store(sid) is None

    async def test_the_stale_turn_does_not_re_fetch(self, live_service):
        """The guarantee is structural, not a policy this branch happens to
        follow: nothing on the consume path calls a GitHub surface at all."""
        sid = "1762-e2e-stale-no-refetch"
        _arm_a_capped_list(sid)
        _store(sid).armed_at = datetime.now() - timedelta(minutes=REMAINDER_MAX_AGE_MINUTES + 1)
        adapter = MagicMock()
        adapter.list_open_issues = AsyncMock(
            side_effect=AssertionError("re-fetched a list it promised from the outcome")
        )
        router_cls = MagicMock(
            side_effect=AssertionError("re-fetched a list it promised from the outcome")
        )
        p_registry, mock_registry = _inert_registry()
        with (
            p_registry as registry_fn,
            patch(
                "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter", return_value=adapter
            ),
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                router_cls,
            ),
        ):
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message="show me the rest", session_id=sid, user_id=_USER
            )
        assert result.intent_data["action"] == "list_remainder_moved"
        assert result.intent_data["context"]["refetched"] is False

    async def test_a_cash_does_not_re_fetch_either(self, live_service):
        """Arch: *RETURNS them, from the outcome, not a re-fetch that might
        disagree with the claim.* The fresh path carries the same guarantee."""
        sid = "1762-e2e-cash-no-refetch"
        _arm_a_capped_list(sid)
        router_cls = MagicMock(side_effect=AssertionError("cash re-fetched"))
        p_registry, mock_registry = _inert_registry()
        with (
            p_registry as registry_fn,
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                router_cls,
            ),
        ):
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message="show me the rest", session_id=sid, user_id=_USER
            )
        assert result.intent_data["action"] == "list_remainder_cash"
        assert result.intent_data["context"]["refetched"] is False

    async def test_an_emptied_remainder_says_the_list_moved_rather_than_nothing(self, live_service):
        """The "gone" half of "gone or stale": a remainder whose items did not
        survive still owes the user an honest turn, not silence."""
        sid = "1762-e2e-emptied"
        ctx = get_or_create_context(sid, user_id=_USER)
        ctx.last_offer = None
        ctx.pending_list_remainder = ListRemainder(
            kind="open issues",
            shown=5,
            held_total=50,
            source_total_display="179",
            lines=(),
            offer_text="That's 5 of 179 — say the word and I'll show you those.",
        )
        p_registry, mock_registry = _inert_registry()
        with p_registry as registry_fn:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message="show me the rest", session_id=sid, user_id=_USER
            )
        assert result.intent_data["action"] == "list_remainder_moved"

    async def test_with_no_remainder_at_all_the_seam_is_silent(self, live_service):
        """A list we have NO record of cannot honestly be called "moved" — the
        turn falls through to normal processing instead."""
        sid = "1762-e2e-no-remainder"
        _clear(sid)
        get_or_create_context(sid, user_id=_USER).last_offer = None
        p_registry, mock_registry = _inert_registry()
        p_classify, p_floor, p_floor2 = _stub_fallthrough_routing(live_service, "show me the rest")
        with p_registry as registry_fn, p_classify, p_floor, p_floor2:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(
                message="show me the rest", session_id=sid, user_id=_USER
            )
        assert result.intent_data.get("action") not in (
            "list_remainder_cash",
            "list_remainder_moved",
        )


# ---------------------------------------------------------------------------
# 5. PRECEDENCE AND NON-INTERFERENCE — the surviving arm must not take over
# ---------------------------------------------------------------------------


class TestPrecedence:
    """A persisting arm is a new kind of thing in this pipeline. These pin
    that it yields to fresher arms and does not suppress soft offers."""

    pytestmark = pytest.mark.asyncio

    async def test_a_fresher_one_turn_offer_wins_the_yes(self, live_service):
        """A "yes" answering the offer Piper made LAST TURN must not be stolen
        by a list offer from five turns ago."""
        from services.intent_service.conversation_context import LastOffer

        sid = "1762-e2e-precedence"
        _arm_a_capped_list(sid)
        ctx = get_or_create_context(sid, user_id=_USER)
        ctx.last_offer = LastOffer(
            offer_type="contextual",
            continuation_hint="explain how project context works",
            offer_text="Want me to explain how project context works?",
        )
        p_registry, mock_registry = _inert_registry()
        p_classify, p_floor, p_floor2 = _stub_fallthrough_routing(live_service, "yes")
        with p_registry as registry_fn, p_classify, p_floor, p_floor2:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.intent_data.get("action") != "list_remainder_cash"
        assert _store(sid) is not None, "the unspent list offer survives for a later ask"

    def test_the_persisting_store_is_not_in_the_soft_offer_no_clobber_peek(self, live_service):
        """Deliberate asymmetry with the two one-slot rails (#1753/#1770):
        peeking a store that lives for 30 minutes would suppress every soft
        offer for that whole window. The arm TURN is covered by the
        ``list_remainder_offer_pending`` flag instead."""
        sid = "1762-peek-asymmetry"
        _arm_a_capped_list(sid)
        assert live_service._peek_last_offer(sid, _USER) is None

    def test_the_arm_turn_carries_the_flag_that_blocks_a_competing_soft_offer(self, live_service):
        armed = IntentProcessingResult(
            success=True,
            message="…That's 5 of 179 — say the word and I'll show you those.",
            intent_data={"list_remainder_offer_pending": True},
        )
        import inspect

        from services.intent.intent_service import IntentService as _IS

        source = inspect.getsource(_IS._apply_soft_offer)
        assert "list_remainder_offer_pending" in source
        assert armed.intent_data["list_remainder_offer_pending"] is True

    async def test_a_newer_capped_list_replaces_the_stored_one(self, live_service):
        """Last list wins: the live offer always refers to what the user most
        recently saw, never to a list two topics ago."""
        sid = "1762-handler-replace"
        _arm_a_capped_list(sid, held=50, source_total=179, kind="open issues")
        labels = [{"name": f"label-{n:03d}", "description": ""} for n in range(40)]
        router = _router_stub(list_labels_via_mcp=labels)
        with patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
            return_value=router,
        ):
            await live_service._handle_list_labels_query(_intent(), "wf", sid)
        assert _store(sid).kind == "labels"


# ---------------------------------------------------------------------------
# 6. DELIBERATE BOUNDARIES — pinned so they can't drift silently
# ---------------------------------------------------------------------------


class TestDeliberateBoundariesPinned:
    """Each of these is a CHOICE, not an accident. Pinned so a later change
    has to argue with a failing test rather than slide past a comment."""

    pytestmark = pytest.mark.asyncio

    async def test_an_interrogative_request_does_not_cash_it_asks(self, live_service):
        """PINNED, and filed as discovered work: contract axis (a) —
        *question-forms NEVER accept* — means "can I see the rest?" is a
        STATE_QUESTION, not an ACCEPT, even though a colleague would read it
        as a request. The arm survives and normal processing answers, so
        nothing is lost; but it is the #1579 shape CXO warns about and the
        contract, not this seam, is where it would be changed."""
        sid = "1762-e2e-interrogative"
        _arm_a_capped_list(sid)
        q = "can I see the rest?"
        p_registry, mock_registry = _inert_registry()
        p_classify, p_floor, p_floor2 = _stub_fallthrough_routing(live_service, q)
        with p_registry as registry_fn, p_classify, p_floor, p_floor2:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(message=q, session_id=sid, user_id=_USER)
        assert result.intent_data.get("action") != "list_remainder_cash"
        assert _store(sid) is not None, "the arm survives; the ask costs nothing"

    async def test_a_bare_yes_long_after_the_offer_still_cashes(self, live_service):
        """PINNED as deliberate: within the age window a bare "yes" cashes
        even with turns in between. The alternative — requiring a referent
        late — reintroduces the syntax CXO's decision 2 forbids. Safe because
        cashing FIRES NOTHING: it prints lines already gathered, so a mistaken
        accept costs one turn and no state."""
        sid = "1762-e2e-late-bare-yes"
        _arm_a_capped_list(sid)
        aside = _ASIDE
        p_registry, mock_registry = _inert_registry()
        p_classify, p_floor, p_floor2 = _stub_fallthrough_routing(live_service, aside)
        with p_registry as registry_fn, p_classify, p_floor, p_floor2:
            registry_fn.return_value = mock_registry
            await live_service.process_intent(message=aside, session_id=sid, user_id=_USER)
        p_registry, mock_registry = _inert_registry()
        with p_registry as registry_fn:
            registry_fn.return_value = mock_registry
            result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.intent_data["action"] == "list_remainder_cash"

    def test_the_remainder_window_is_the_conversations_own_staleness_number(self):
        """Not a fresh arbitrary constant: a remainder older than the
        conversation that produced it has no claim to be "the list you saw"."""
        from services.intent_service.conversation_context import ConversationContext

        assert REMAINDER_MAX_AGE_MINUTES == ConversationContext().max_age_minutes
