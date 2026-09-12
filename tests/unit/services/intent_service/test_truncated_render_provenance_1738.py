"""#1738: Piper reads its OWN truncated render as its data source.

PM live 2026-09-09 (v70), verbatim: "list my archived projects" → "You have
**6** archived projects: • Klatch • Test • Test1 • Test2 • Test3 …and 1
more." Then "what's the sixth one?" → "I don't have that detail in front of
me right now — the list I got back only showed five names clearly."

Mechanism (diagnosed 2026-09-12): the portfolio list handlers render
`projects[:5]` + "...and N more" — and `turn.response` (the rendered string)
is the ONLY per-turn record that reaches next-turn context via
`build_recent_history` (#1122). Whatever the render drops is, from the
model's own position next turn, information it never had. The GatherOutcome
contract §5b (docs/internal/design/gather-outcome-user-facing-contract-
2026-09-09.md, Arch-confirmed joint invariant of epics 1+2):

    "A provenance value is a fact about the SOURCE, and it must survive
    rendering unchanged. A render cap may shorten what the user sees; it
    must never change what the system believes it has."

The provenance-half fix (this epic): the deterministic portfolio list
renders carry the FULL set — render == data, so the one channel into
next-turn context carries the true set and "…and N more" never becomes a
claim the assistant cannot cash. Display treatment for pathologically long
lists (caps, deliverables, pagination) is epic-6 renderer territory and is
deliberately NOT built here — a renderer may shorten what the user sees
only when it consumes a structured outcome it never rewrites.

Also pinned here (both filed inside #1738, not separately):
  - defect 1: the restore hint used the literal placeholder `<name>`, which
    the web render swallows as an unknown HTML tag — PM saw
    'Say "restore " to bring one back.' with an empty slot.
  - defect 2: "list my archived projects" matched BOTH the PORTFOLIO list
    pattern AND STATUS_PATTERNS' broad r"\blist.*projects\b" — a phantom
    STATUS/get_project_status sibling made every archived-list turn
    multi-intent; when that sibling failed, _aggregate_messages appended
    "I wasn't able to check on project status right now…" to a SUCCESSFUL
    listing (the §2 reportability defect; same rider text as the #1431
    screenshots). Fixed by a subsumption rule (the #1084 mechanism, no new
    routing pattern — #1559 moratorium respected).

Layer honesty (m-43): handler-render layer (canonical + rail entry, data
source mocked), the pre-classifier multi-intent layer (pure function), and
the history-assembly layer (in-memory ConversationContext + the real
build_recent_history). No live classifier, no DB, no delivered turn.
"""

import re
import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.conversation_context import (
    build_recent_history,
    get_or_create_context,
)
from services.intent_service.pre_classifier import PreClassifier
from services.intent_service.workflow_dispatcher import dispatch_workflow
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory

# ---------------------------------------------------------------------------
# Shared harness (canonical handler seam — mirrors test_archived_list_1431)
# ---------------------------------------------------------------------------

# PM's live round had 6; the 6th is the one Piper could not name.
SIX_ARCHIVED = [
    SimpleNamespace(name=n) for n in ["Klatch", "Test", "Test1", "Test2", "Test3", "Sixth Project"]
]
SEVEN_ACTIVE = [
    SimpleNamespace(name=n)
    for n in ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Seventh Active"]
]

# A placeholder rendered inside <angle brackets> is swallowed by the web
# render as an unknown HTML tag (defect 1's mechanism).
ANGLE_BRACKET_TOKEN = re.compile(r"<[a-zA-Z][a-zA-Z ]*>")


def _portfolio_intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_portfolio",
        confidence=1.0,
        context={"original_message": message},
    )


class _FakeScope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


@pytest.fixture
def handler():
    return CanonicalHandlers()


async def _run_portfolio(handler, message, archived_rows, active_rows):
    archived_mock = AsyncMock(return_value=archived_rows)
    active_mock = AsyncMock(return_value=active_rows)

    from services.database.session_factory import AsyncSessionFactory
    from services.onboarding.portfolio_service import PortfolioService

    with patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())):
        with patch.object(PortfolioService, "list_archived_projects", archived_mock):
            with patch.object(PortfolioService, "list_active_projects", active_mock):
                result = await handler._handle_portfolio_query(
                    _portfolio_intent(message), session_id="s1738", user_id="u1738"
                )
    return result


# ---------------------------------------------------------------------------
# THE defect: the render must carry the full set, because the render is the
# only thing the model gets to reason over next turn.
# ---------------------------------------------------------------------------


class TestArchivedRenderCarriesFullSet:
    @pytest.mark.asyncio
    async def test_six_archived_projects_render_all_six_names(self, handler):
        """PM's live case: the 6th name must be IN the render, not elided."""
        result = await _run_portfolio(handler, "list my archived projects", SIX_ARCHIVED, [])
        msg = result["message"]
        for row in SIX_ARCHIVED:
            assert row.name in msg, (
                f"{row.name!r} missing from the archived-list render — whatever "
                f"the render drops, the model next turn believes it never had "
                f"(#1738, GatherOutcome contract §5b)"
            )

    @pytest.mark.asyncio
    async def test_no_uncashable_elision_marker(self, handler):
        """'…and N more' is a claim the assistant must be able to cash; the
        deterministic portfolio render makes no elision at all."""
        result = await _run_portfolio(handler, "list my archived projects", SIX_ARCHIVED, [])
        assert "more." not in result["message"], (
            "silent elision marker in the archived-list render — the model "
            "reads its own render as its data source (#1738)"
        )

    @pytest.mark.asyncio
    async def test_count_claim_matches_rendered_names(self, handler):
        """The count the copy claims equals the number of bullets rendered —
        the render never asserts a set it does not show."""
        result = await _run_portfolio(handler, "list my archived projects", SIX_ARCHIVED, [])
        msg = result["message"]
        bullets = [line for line in msg.splitlines() if line.startswith("- ")]
        assert f"You have {len(SIX_ARCHIVED)} archived" in msg
        assert len(bullets) == len(SIX_ARCHIVED), (
            f"count says {len(SIX_ARCHIVED)}, render shows {len(bullets)} — "
            f"the gap is exactly what the assistant cannot answer about next turn"
        )


class TestActiveRenderCarriesFullSet:
    @pytest.mark.asyncio
    async def test_seven_active_projects_render_all_seven(self, handler):
        """Same defect, same handler block, active-list branch."""
        result = await _run_portfolio(handler, "list my projects", [], SEVEN_ACTIVE)
        msg = result["message"]
        for row in SEVEN_ACTIVE:
            assert row.name in msg, f"{row.name!r} elided from the active-list render (#1738)"
        assert "more." not in msg


class TestRailArchivedRenderCarriesFullSet:
    """The #1570 rail entry renders the same list — same invariant."""

    def _patch_portfolio(self, archived):
        service = MagicMock()
        service.list_archived_projects = AsyncMock(return_value=archived)

        @asynccontextmanager
        async def fake_scope():
            yield MagicMock()

        return (
            patch(
                "services.onboarding.portfolio_service.PortfolioService",
                return_value=service,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope",
                fake_scope,
            ),
        )

    @pytest.mark.asyncio
    async def test_rail_dispatch_renders_all_six(self):
        register_default_workflows()
        p_service, p_scope = self._patch_portfolio(SIX_ARCHIVED)
        with p_service, p_scope:
            result = await dispatch_workflow(
                workflow_type="list_archived_projects",
                session_id="sess-1738",
                user_id="user-1738",
                context={},
            )
        assert result is not None and result.success
        for row in SIX_ARCHIVED:
            assert (
                row.name in result.message
            ), f"{row.name!r} elided from the RAIL archived render (#1738)"
        assert "more." not in result.message


# ---------------------------------------------------------------------------
# Defect 1: the restore hint's placeholder must survive an HTML render.
# ---------------------------------------------------------------------------


class TestRestoreHintSurvivesHtmlRender:
    @pytest.mark.asyncio
    async def test_canonical_restore_hint_has_no_angle_bracket_placeholder(self, handler):
        result = await _run_portfolio(handler, "list my archived projects", SIX_ARCHIVED, [])
        msg = result["message"]
        assert "restore" in msg.lower(), "restore hint disappeared entirely"
        m = ANGLE_BRACKET_TOKEN.search(msg)
        assert m is None, (
            f"angle-bracket placeholder {m.group(0)!r} in user-facing copy — the "
            f"web render swallows it as an HTML tag; PM saw 'Say \"restore \"' "
            f"with an empty slot (#1738 defect 1)"
        )

    @pytest.mark.asyncio
    async def test_rail_restore_hint_has_no_angle_bracket_placeholder(self):
        register_default_workflows()
        service = MagicMock()
        service.list_archived_projects = AsyncMock(return_value=SIX_ARCHIVED)

        @asynccontextmanager
        async def fake_scope():
            yield MagicMock()

        with patch("services.onboarding.portfolio_service.PortfolioService", return_value=service):
            with patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope",
                fake_scope,
            ):
                result = await dispatch_workflow(
                    workflow_type="list_archived_projects",
                    session_id="sess-1738b",
                    user_id="user-1738",
                    context={},
                )
        assert result is not None and result.success
        assert ANGLE_BRACKET_TOKEN.search(result.message) is None


# ---------------------------------------------------------------------------
# The provenance layer: what the model actually reads next turn.
# turn.response is the ONE per-turn channel into build_recent_history —
# this pins that the channel now carries the full set.
# ---------------------------------------------------------------------------


class TestProvenanceSurvivesIntoNextTurnHistory:
    @pytest.mark.asyncio
    async def test_next_turn_history_carries_the_sixth_name(self, handler):
        result = await _run_portfolio(handler, "list my archived projects", SIX_ARCHIVED, [])

        session_id = f"hist-{uuid.uuid4()}"  # isolate from the process-local registry
        conv_ctx = get_or_create_context(session_id, user_id=None)
        turn = conv_ctx.add_turn(message="list my archived projects")
        turn.response = result["message"]  # what process_intent records for the turn

        history = build_recent_history(session_id, None, exclude_in_flight=False)
        assistant_content = " ".join(h["content"] for h in history if h["role"] == "assistant")
        assert "Sixth Project" in assistant_content, (
            "the model's next-turn context does not carry the 6th name — this is "
            "the exact state that produced 'the list I got back only showed five "
            "names clearly' (#1738)"
        )
        assert "6 archived" in assistant_content


# ---------------------------------------------------------------------------
# Defect 2: the phantom STATUS sibling. PORTFOLIO's list claim subsumes
# STATUS's broad list/show overlap — mirrors pre_classify() precedence
# (PORTFOLIO is checked before STATUS on the single-intent path).
# ---------------------------------------------------------------------------


class TestPhantomStatusSiblingSubsumed:
    @pytest.mark.parametrize(
        "message",
        [
            "list my archived projects",
            "list my archived projects (show all names)",  # PM's retry, live v70
            "show my projects",
            "list my projects",
        ],
    )
    def test_portfolio_list_claim_is_single_intent(self, message):
        result = PreClassifier.detect_multiple_intents(message)
        actions = [(i.category, i.action) for i in result.intents]
        assert not result.is_multi_intent, (
            f"phantom sibling survives for {message!r}: {actions} — the failed "
            f"get_project_status sibling is what stapled 'I wasn't able to check "
            f"on project status…' onto a SUCCESSFUL listing (#1738 defect 2)"
        )
        assert len(result.intents) == 1
        assert result.intents[0].category == IntentCategory.PORTFOLIO
        assert result.intents[0].action == "manage_portfolio"

    def test_pure_status_ask_keeps_status(self):
        """Control: no PORTFOLIO claim → STATUS untouched."""
        result = PreClassifier.detect_multiple_intents("What projects are we working on?")
        assert len(result.intents) == 1
        assert result.intents[0].category == IntentCategory.STATUS

    def test_portfolio_write_beside_status_ask_keeps_both(self):
        """Control for narrowness: the rule keys on the LIST claim, not on the
        PORTFOLIO category — a genuine two-part write+status ask keeps both."""
        result = PreClassifier.detect_multiple_intents(
            "archive project Klatch and give me a status update"
        )
        categories = {i.category for i in result.intents}
        assert IntentCategory.PORTFOLIO in categories
        assert IntentCategory.STATUS in categories, (
            "over-suppression: a real status ask beside a portfolio WRITE lost "
            "its STATUS intent — the subsumption rule must key on the list claim"
        )
