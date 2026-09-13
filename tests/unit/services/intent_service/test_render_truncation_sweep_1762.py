"""#1762: the render-truncation sweep — #1738's defect class at every OTHER
capped render over a bounded, user-owned set.

#1738 fixed the FIRST instance (the portfolio list handlers) and named the
mechanism: ``turn.response`` — the RENDERED string — is the only per-turn
record that reaches next-turn context via ``build_recent_history`` (#1122).
Re-verified this session at ``services/intent/intent_service.py:865``
(``conv_ctx.turns[-1].response = result.message``). Whatever the render drops
is, from the model's own position next turn, information it never had.

GatherOutcome contract §5b (Arch-confirmed joint invariant of epics 1+2):

    "A provenance value is a fact about the SOURCE, and it must survive
    rendering unchanged. A render cap may shorten what the user sees; it
    must never change what the system believes it has."

This suite pins the class-(a) half of the #1762 census: sites whose
underlying set is BOUNDED and USER-OWNED (the user's own PIPER.md projects
and priorities, their own todo list, their own reminders, their own
portfolio), where render == data is both correct and cheap. The class-(b)
half — genuinely long sets (GitHub issues/PRs/branches/labels/releases,
external search results, composted insights) — is deliberately NOT changed
here; it needs the epic-6 rendered-deliverable display policy (a renderer
that consumes a structured outcome it never rewrites). ``TestClassBBoundary``
below pins that boundary so a later sweep can't quietly cross it without the
design.

One site is not a ``turn.response`` render at all and is the sharpest of the
set: ``ConversationalFloor._format_domain_context`` truncates the DUE
REMINDERS block of the LLM's own system prompt — the data channel itself —
two lines under a directive ordering the model to "Briefly surface them in
your reply … do not wait to be asked". The prompt instructed surfacing of
items the same prompt had elided.

Layer honesty (m-43): pure render-layer (formatters called directly with
their real signatures), the canonical handler seam with the data source
mocked, the floor's prompt-composition layer (a real ``ConversationalFloor``
with a mocked LLM client, calling the real ``_format_domain_context``), the
reminder_clear clarify seam (real function, mocked todo service), and ONE
history-assembly pin using the in-memory ``ConversationContext`` and the REAL
``build_recent_history``. No live classifier, no DB, no delivered turn.
"""

import uuid
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.conversation_context import (
    build_recent_history,
    get_or_create_context,
)
from services.intent_service.conversational_floor import ConversationalFloor
from services.shared_types import EffectClass, IntentCategory

# ---------------------------------------------------------------------------
# Fixtures / shared data
#
# Every list below is deliberately one longer than the cap it exercises, and
# the LAST element is uniquely named — that last element is the one the
# assistant could not name in #1738's live round.
# ---------------------------------------------------------------------------

# 7 PIPER.md projects: past the [:3] embedded caps AND the [:5] standard caps.
SEVEN_PROJECTS = [
    "Klatch",
    "Piper Morgan",
    "OpenLaws",
    "Design in Product",
    "Janus",
    "Website",
    "Seventh Project",
]

# 6 PIPER.md priorities: past [1:4] (which renders items 2-4) and [:3].
SIX_PRIORITIES = [
    "Ship the MVP",
    "Fix the floor",
    "Write the ADR",
    "Review the epic",
    "Plan the sprint",
    "Sixth Priority",
]


def _todos(n: int, priority: str, prefix: str):
    """Agenda/retrospective formatters take dicts keyed title/priority."""
    return [{"title": f"{prefix} {i}", "priority": priority} for i in range(1, n + 1)]


def _user_context(projects=None, priorities=None, organization=None):
    return SimpleNamespace(
        user_id=None,
        organization=organization,
        projects=list(projects or []),
        priorities=list(priorities or []),
        preferences={},
    )


@pytest.fixture
def handler():
    return CanonicalHandlers()


def _assert_all_present(msg: str, items, where: str):
    for item in items:
        assert item in msg, (
            f"{item!r} missing from {where} — whatever the render drops, the "
            f"model next turn believes it never had (#1762, GatherOutcome §5b)"
        )


def _assert_no_elision(msg: str, where: str):
    lowered = msg.lower()
    for marker in ("and 1 more", "and 2 more", "and 3 more", "and 4 more", "more."):
        assert marker not in lowered, (
            f"uncashable elision marker {marker!r} in {where} — '…and N more' is "
            f"a claim the assistant cannot cash next turn (#1762)"
        )


# ---------------------------------------------------------------------------
# a1 — the portfolio SEARCH branch: the third branch of the very handler
#      #1738 fixed. Silent [:5] under a count claim of len(results).
# ---------------------------------------------------------------------------


class _FakeScope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


async def _run_portfolio_search(handler, message, results):
    from services.database.session_factory import AsyncSessionFactory
    from services.onboarding.portfolio_service import PortfolioService

    with patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())):
        with patch.object(PortfolioService, "search_projects", AsyncMock(return_value=results)):
            return await handler._handle_portfolio_query(
                Intent(
                    category=IntentCategory.PORTFOLIO,
                    action="manage_portfolio",
                    confidence=1.0,
                    context={"original_message": message},
                ),
                session_id="s1762",
                user_id="u1762",
            )


SIX_MATCHES = [SimpleNamespace(name=n) for n in [*SEVEN_PROJECTS[:5], "Sixth Match"]]


class TestPortfolioSearchRendersFullSet:
    """#1738 fixed `list` and `list_archived` in `_handle_portfolio_query`;
    the `search` branch in the SAME function kept its `[:5]`."""

    @pytest.mark.asyncio
    async def test_search_renders_every_match(self, handler):
        result = await _run_portfolio_search(handler, "search projects for test", SIX_MATCHES)
        _assert_all_present(
            result["message"], [m.name for m in SIX_MATCHES], "the portfolio SEARCH render"
        )

    @pytest.mark.asyncio
    async def test_search_count_claim_matches_rendered_bullets(self, handler):
        """The copy already claims `Found {len(results)} projects` — with the
        cap in place that count was a number the render itself refuted."""
        result = await _run_portfolio_search(handler, "search projects for test", SIX_MATCHES)
        msg = result["message"]
        bullets = [line for line in msg.splitlines() if line.startswith("- ")]
        assert f"Found {len(SIX_MATCHES)} projects" in msg
        assert len(bullets) == len(SIX_MATCHES), (
            f"count says {len(SIX_MATCHES)}, render shows {len(bullets)} — the gap "
            f"is exactly what the assistant cannot answer about next turn (#1762)"
        )


# ---------------------------------------------------------------------------
# The provenance layer (the #1738 idiom): what the model actually reads on
# the NEXT turn. turn.response is the one channel; this drives the real
# build_recent_history over it.
# ---------------------------------------------------------------------------


class TestProvenanceSurvivesIntoNextTurnHistory:
    @pytest.mark.asyncio
    async def test_next_turn_history_carries_the_sixth_match(self, handler):
        result = await _run_portfolio_search(handler, "search projects for test", SIX_MATCHES)

        session_id = f"hist-1762-{uuid.uuid4()}"  # isolate from the process-local registry
        conv_ctx = get_or_create_context(session_id, user_id=None)
        turn = conv_ctx.add_turn(message="search projects for test")
        turn.response = result["message"]  # what process_intent records (intent_service.py:865)

        history = build_recent_history(session_id, None, exclude_in_flight=False)
        assistant_content = " ".join(h["content"] for h in history if h["role"] == "assistant")
        assert "Sixth Match" in assistant_content, (
            "the model's next-turn context does not carry the 6th match — this is "
            "the exact state that produced 'the list I got back only showed five "
            "names clearly' in #1738's live round"
        )

    @pytest.mark.asyncio
    async def test_next_turn_history_carries_the_seventh_agenda_todo(self, handler):
        """Same channel, a different class-(a) render: the agenda's task list."""
        todos = _todos(7, "medium", "Task")
        message = handler._format_agenda_standard(None, todos, [])

        session_id = f"hist-1762-{uuid.uuid4()}"
        conv_ctx = get_or_create_context(session_id, user_id=None)
        conv_ctx.add_turn(message="what's on my agenda today?").response = message

        history = build_recent_history(session_id, None, exclude_in_flight=False)
        assistant_content = " ".join(h["content"] for h in history if h["role"] == "assistant")
        assert "Task 7" in assistant_content, (
            "the 7th todo never reaches next-turn context — asked 'what else is on "
            "my list?', the model can only describe its own render (#1762)"
        )


# ---------------------------------------------------------------------------
# a2-a4, a6 — PIPER.md project lists (hand-authored config; bounded by a
# human typing them).
# ---------------------------------------------------------------------------


class TestPiperMdProjectRendersCarryFullSet:
    def test_consolidated_status_names_every_project(self, handler):
        msg = handler._format_consolidated_status(SEVEN_PROJECTS, _user_context())
        _assert_all_present(msg, SEVEN_PROJECTS, "_format_consolidated_status")
        assert "more" not in msg, "'+ N more' survived in the EMBEDDED status render (#1762)"

    def test_standard_status_names_every_project(self, handler):
        msg = handler._format_standard_status(
            SEVEN_PROJECTS, _user_context(projects=SEVEN_PROJECTS)
        )
        _assert_all_present(msg, SEVEN_PROJECTS, "_format_standard_status")
        _assert_no_elision(msg, "_format_standard_status")

    def test_standard_status_bullet_count_matches_its_own_claim(self, handler):
        msg = handler._format_standard_status(
            SEVEN_PROJECTS, _user_context(projects=SEVEN_PROJECTS)
        )
        bullets = [line for line in msg.splitlines() if line.startswith("- ")]
        assert f"You're working on {len(SEVEN_PROJECTS)} active projects" in msg
        assert len(bullets) == len(SEVEN_PROJECTS)

    def test_project_list_embedded_names_every_project(self, handler):
        msg = handler._format_project_list_embedded(SEVEN_PROJECTS)
        _assert_all_present(msg, SEVEN_PROJECTS, "_format_project_list_embedded")
        assert "more" not in msg

    @pytest.mark.asyncio
    async def test_project_setup_request_names_every_project(self, handler):
        from services.user_context_service import user_context_service

        with patch.object(
            user_context_service,
            "get_user_context",
            AsyncMock(return_value=_user_context(projects=SEVEN_PROJECTS)),
        ):
            result = await handler._handle_project_setup_request(
                Intent(
                    category=IntentCategory.GUIDANCE,
                    action="provide_setup_guidance",
                    confidence=1.0,
                    context={"original_message": "set up my projects"},
                ),
                session_id="s1762",
                user_id="u1762",
            )
        _assert_all_present(result["message"], SEVEN_PROJECTS, "_handle_project_setup_request")
        _assert_no_elision(result["message"], "_handle_project_setup_request")


# ---------------------------------------------------------------------------
# a5, a10 — PIPER.md priority lists.
# ---------------------------------------------------------------------------


class TestPiperMdPriorityRendersCarryFullSet:
    def test_standard_priorities_names_every_priority(self, handler):
        msg = handler._format_standard_priorities(
            SIX_PRIORITIES, _user_context(priorities=SIX_PRIORITIES)
        )
        _assert_all_present(msg, SIX_PRIORITIES, "_format_standard_priorities")
        _assert_no_elision(msg, "_format_standard_priorities")

    def test_granular_agenda_names_every_priority(self, handler):
        """GRANULAR is the MOST detailed mode and it silently kept `[:3]`."""
        msg = handler._format_agenda_granular(None, [], SIX_PRIORITIES)
        _assert_all_present(msg, SIX_PRIORITIES, "_format_agenda_granular priorities")


# ---------------------------------------------------------------------------
# a7-a9, a11 — the user's own todo list.
# ---------------------------------------------------------------------------


class TestTodoRendersCarryFullSet:
    def test_agenda_standard_lists_every_todo(self, handler):
        todos = _todos(7, "medium", "Task")
        msg = handler._format_agenda_standard(None, todos, [])
        _assert_all_present(msg, [t["title"] for t in todos], "_format_agenda_standard")
        _assert_no_elision(msg, "_format_agenda_standard")

    def test_agenda_granular_lists_every_medium_and_low_todo(self, handler):
        """The `high` band already rendered in full — the medium/low caps were
        arbitrary asymmetry inside one function."""
        todos = _todos(7, "medium", "Medium") + _todos(5, "low", "Low")
        msg = handler._format_agenda_granular(None, todos, [])
        _assert_all_present(msg, [t["title"] for t in todos], "_format_agenda_granular")
        _assert_no_elision(msg, "_format_agenda_granular")

    def test_agenda_granular_total_matches_rendered_items(self, handler):
        todos = _todos(7, "medium", "Medium") + _todos(5, "low", "Low")
        msg = handler._format_agenda_granular(None, todos, [])
        rendered = [line for line in msg.splitlines() if line.strip().startswith("- ")]
        assert f"**Total**: {len(todos)} pending tasks" in msg
        assert len(rendered) == len(todos)

    def test_retrospective_standard_lists_every_completed_todo(self, handler):
        completed = _todos(11, "high", "Done")
        msg = handler._format_retrospective_standard(completed, datetime(2026, 9, 12))
        _assert_all_present(msg, [t["title"] for t in completed], "_format_retrospective_standard")
        _assert_no_elision(msg, "_format_retrospective_standard")


# ---------------------------------------------------------------------------
# a12 — the floor's DUE REMINDERS block. Not turn.response: this is the LLM's
# own system prompt, i.e. the data channel. The directive immediately above
# the cap orders the model to surface every one of them.
# ---------------------------------------------------------------------------


class TestFloorDueRemindersDataChannelCarriesFullSet:
    @pytest.fixture
    def floor(self):
        return ConversationalFloor(llm_client=MagicMock())

    def test_all_due_reminders_reach_the_prompt(self, floor):
        rems = [f"Reminder {i}" for i in range(1, 8)]
        rendered = floor._format_domain_context(
            {"due_reminders": rems, "reminder_count": len(rems)}
        )
        _assert_all_present(rendered, rems, "the floor's DUE REMINDERS prompt block")

    def test_no_elision_marker_in_the_data_channel(self, floor):
        rems = [f"Reminder {i}" for i in range(1, 8)]
        rendered = floor._format_domain_context(
            {"due_reminders": rems, "reminder_count": len(rems)}
        )
        assert "more" not in rendered.split("Vocabulary")[0], (
            "the prompt elides reminders it simultaneously orders the model to "
            "surface — the model cannot surface what it was never shown (#1762)"
        )

    def test_count_header_matches_the_items_rendered(self, floor):
        rems = [f"Reminder {i}" for i in range(1, 8)]
        rendered = floor._format_domain_context(
            {"due_reminders": rems, "reminder_count": len(rems)}
        )
        assert f"DUE REMINDERS ({len(rems)})" in rendered
        bullets = [ln for ln in rendered.splitlines() if ln.strip().startswith("• Reminder")]
        assert len(bullets) == len(rems)


# ---------------------------------------------------------------------------
# a13 — reminder_clear's ambiguity clarification. Silent [:6] under the
# definite claim "you have: …", which is simply false past six.
# ---------------------------------------------------------------------------


class TestReminderClearClarifyListsEveryCandidate:
    @pytest.mark.asyncio
    async def test_unmatched_named_target_lists_all_candidates(self):
        from services.intent_service.reminder_clear import maybe_handle_clear_family

        targets = [
            SimpleNamespace(
                id=uuid.uuid4(),
                text=f"Reminder {i}",
                completed=False,
                reminder_date=datetime(2026, 9, 12),
            )
            for i in range(1, 9)
        ]

        todo_service = MagicMock()
        todo_service.list_todos = AsyncMock(return_value=targets)
        intent_service = MagicMock()
        intent_service.todo_handlers.todo_service = todo_service

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="delete_todo",
            confidence=1.0,
            context={"original_message": 'clear the "nothing matches this" reminder'},
        )
        intent.original_message = 'clear the "nothing matches this" reminder'

        result = await maybe_handle_clear_family(
            intent_service,
            intent,
            session_id="s1762-clear",
            user_id=str(uuid.uuid4()),
            todo_user_id=uuid.uuid4(),
            candidate_effect=EffectClass.DESTRUCTIVE,
        )

        assert result is not None, "the clear-family clarify path did not run"
        assert "you have:" in result.message, f"unexpected branch: {result.message!r}"
        _assert_all_present(
            result.message, [t.text for t in targets], "the reminder_clear clarify list"
        )


# ---------------------------------------------------------------------------
# The scope boundary. These are class (b) — the underlying set is genuinely
# large, so "render the full set" is the WRONG answer and the right one is
# the epic-6 rendered-deliverable design (a renderer consuming a structured
# outcome it never rewrites). They must stay capped until that design lands;
# these are green controls, and they are also a tripwire against a future
# sweep "finishing the job" without the design work.
# ---------------------------------------------------------------------------


class TestClassBBoundaryDeliberatelyUnchanged:
    def test_search_results_still_cap_at_ten(self):
        from services.consciousness.search_consciousness import (
            format_search_results_conscious,
        )

        results = [{"title": f"Result {i}", "url": ""} for i in range(1, 16)]
        out = format_search_results_conscious("q", results, "Notion")
        assert "...and 5 more results." in out, (
            "external search results were un-capped — that is class (b) in the "
            "#1762 census and needs the epic-6 display policy, not a full render"
        )

    def test_floor_insight_bands_still_cap(self):
        floor = ConversationalFloor(llm_client=MagicMock())
        high = [
            {"expression": f"Insight {i}", "confidence": 0.9, "observation_count": 3}
            for i in range(1, 16)
        ]
        rendered = floor._format_domain_context(
            {"insights": {"is_empty": False, "total_count": 15, "high_confidence": high}}
        )
        assert "Insight 15" not in rendered, (
            "composted insights were un-capped — the set grows with every session "
            "forever; this is class (b) (#1762)"
        )
