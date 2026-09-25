"""#1762 epic 6, the PORTFOLIO / floor-``domain_context`` cohort — the sites the
2026-09-13 class-(a) census could not see, plus the one real data-channel loss
left in the floor prompt.

WHAT THIS COHORT TURNED OUT TO BE, and why there is no new ``ListRemainder``
arming site in it (stated up front because the absence is the finding):

The GitHub six (``e267db8dc``) are the class-(b) cohort where a capped render
sits over a genuinely long source, so the cap has to become a CASHABLE offer.
Re-running the census on 2026-09-24 found that **every remaining site in the
portfolio / floor-``domain_context`` cohort is over a set that is either
hand-authored PIPER.md data (bounded, user-owned) or already gather-capped to
≤5 upstream.** For both shapes the ratified answer is the class-(a) one —
render the full held set — and PPM's epic-6 threshold reaches the same place
independently: a hidden tail of ≤3 is ceremony, so show them.

Composing ``compose_capped_list`` at these sites would have been strictly
WORSE than this: the formatters here are pure ``-> str`` functions with no
session id, so an offer emitted at a site whose gather cap later rises (#1776)
would be a promise with nothing armed behind it — the exact §5b defect, newly
manufactured. The threshold is doing the work the offer would have done, and
it does it without a claim to cash.

SIX SITES THE CLASS-(a) CENSUS MISSED, and the two reasons it missed them
(recorded so the next sweep doesn't re-derive them):

  1. **Five were SILENT** — a bare ``[:3]`` with no marker. The census's
     primary grep was for elision markers; its silent-cap pass covered the
     render neighborhoods it had already opened, not these.
  2. **One was MARKED, in a phrasing the grep could not match**:
     ``_format_priority_standard`` printed ``"_Plus N more projects_"`` — not
     ``"…and N more"``. An explicit, uncashable claim about the user's own
     portfolio that no pattern in the census was looking for.

Layer honesty (m-43): pure render layer — every canonical assertion calls the
real formatter directly with its real signature, and the floor assertion calls
the real ``ConversationalFloor._format_domain_context`` (the LLM's system
prompt, NOT ``turn.response``). No classifier, no DB, no LLM, no delivered
turn. Denominator (m-44): the seven sites converted in this build, named one
class per site below; the sites deliberately left are pinned in
``TestDeliberatelyLeftCapped`` with the reason attached to each.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.conversational_floor import ConversationalFloor

# Deliberately longer than every cap under test, with a uniquely-named LAST
# element — the element the model would believe it had never been shown.
SEVEN_PROJECTS = [
    "Klatch",
    "Piper Morgan",
    "OpenLaws",
    "Design in Product",
    "Janus",
    "Website",
    "Seventh Project",
]

SIX_PRIORITIES = [
    "Ship the MVP",
    "Fix the floor",
    "Write the ADR",
    "Review the epic",
    "Plan the sprint",
    "Sixth Priority",
]


def _user_context(projects=None, priorities=None, organization=None):
    return SimpleNamespace(
        user_id=None,
        organization=organization,
        projects=list(projects or []),
        priorities=list(priorities or []),
        preferences={},
    )


def _issues(n: int):
    """The shape ``priority_metadata["high_priority_issues"]`` carries."""
    return [
        {"number": 100 + i, "title": f"Urgent issue {i}", "labels": []} for i in range(1, n + 1)
    ]


@pytest.fixture
def handler():
    return CanonicalHandlers()


@pytest.fixture
def floor():
    return ConversationalFloor(llm_client=MagicMock())


def _assert_all_present(msg: str, items, where: str):
    for item in items:
        assert item in msg, (
            f"{item!r} missing from {where} — whatever the render drops is, from "
            f"the model's own position next turn, information it never had "
            f"(#1762, GatherOutcome §5b)"
        )


# ---------------------------------------------------------------------------
# The five SILENT misses. Each is the same hand-authored PIPER.md list the
# class-(a) sweep already renders whole at its sibling sites, or a held set
# whose hidden tail is under PPM's threshold.
# ---------------------------------------------------------------------------


class TestSilentPiperMdCapsRenderWhole:
    def test_project_specific_granular_names_every_priority(self, handler):
        """``_format_project_specific_status`` GRANULAR — the a10 twin, and in
        the MOST detailed mode, which is where an elision is least defensible."""
        out = handler._format_project_specific_status(
            "Klatch",
            {"has_github": False},
            _user_context(priorities=SIX_PRIORITIES),
            spatial_pattern="GRANULAR",
        )
        _assert_all_present(out, SIX_PRIORITIES, "_format_project_specific_status GRANULAR")

    def test_detailed_status_names_every_priority(self, handler):
        """``_format_detailed_status`` printed ``Current priorities: a, b, c``
        — a label that reads as a complete enumeration over a silent [:3]."""
        out = handler._format_detailed_status(
            ["Klatch"],
            _user_context(projects=["Klatch"], priorities=SIX_PRIORITIES, organization="Acme"),
            {},
        )
        _assert_all_present(out, SIX_PRIORITIES, "_format_detailed_status")

    def test_detailed_guidance_names_every_secondary_priority(self, handler):
        """The ``[1:3]`` secondary-priorities cap — the a5 twin (``[1:4]``)."""
        out = handler._format_detailed_guidance(
            current_hour=10,
            user_context=_user_context(projects=SEVEN_PROJECTS, priorities=SIX_PRIORITIES),
            focus_recommendation={"urgent_items": 0, "suggestions": []},
        )
        # priorities[0] is the PRIMARY line; [1:] are the secondaries.
        _assert_all_present(out, SIX_PRIORITIES[1:], "_format_detailed_guidance secondaries")

    def test_detailed_guidance_names_every_project(self, handler):
        out = handler._format_detailed_guidance(
            current_hour=10,
            user_context=_user_context(projects=SEVEN_PROJECTS, priorities=SIX_PRIORITIES),
            focus_recommendation={"urgent_items": 0, "suggestions": []},
        )
        _assert_all_present(out, SEVEN_PROJECTS, "_format_detailed_guidance projects")

    def test_standard_priorities_lists_every_held_urgent_issue(self, handler):
        """``high_priority_issues`` is gather-capped to 5 upstream; the render's
        ``[:3]`` dropped 2 of the 5 the handler had in hand. PPM's threshold
        rules a hidden tail of ≤3 directly: show them."""
        held = _issues(5)
        out = handler._format_standard_priorities(
            SIX_PRIORITIES,
            _user_context(priorities=SIX_PRIORITIES),
            {"high_priority_issues": held},
        )
        _assert_all_present(
            out, [i["title"] for i in held], "_format_standard_priorities urgent issues"
        )

    def test_detailed_guidance_urgent_block_matches_its_own_count(self, handler):
        """Sharpest of the five: the header states ``urgent_count`` and the
        block below it rendered three — the count and the list disagreed inside
        a single block (m-44 within one turn)."""
        held = _issues(5)
        out = handler._format_detailed_guidance(
            current_hour=10,
            user_context=_user_context(projects=SEVEN_PROJECTS, priorities=SIX_PRIORITIES),
            priority_metadata={"high_priority_issues": held},
            focus_recommendation={"urgent_items": 5, "suggestions": []},
        )
        assert "**Urgent Items (5)**" in out
        _assert_all_present(out, [i["title"] for i in held], "_format_detailed_guidance urgent")


# ---------------------------------------------------------------------------
# The MARKED miss the census grep could not see.
# ---------------------------------------------------------------------------


def _ranked(names):
    return [
        {
            "name": n,
            "score": 100 - i * 5,
            "top_reason": f"{i} open issues",
            "breakdown": {"staleness": 0, "issue_count": 0, "urgency": 0},
        }
        for i, n in enumerate(names)
    ]


class TestPriorityStandardRendersTheWholeRanking:
    def test_every_ranked_project_is_named(self, handler):
        out = handler._format_priority_standard(_ranked(SEVEN_PROJECTS))
        _assert_all_present(out, SEVEN_PROJECTS, "_format_priority_standard")

    def test_the_plus_n_more_claim_is_gone(self, handler):
        """The marker was an EXPLICIT claim the turn could not cash — the model
        asserted a 4th project existed and then had no record of which."""
        out = handler._format_priority_standard(_ranked(SEVEN_PROJECTS))
        assert "more projects" not in out, (
            "'_Plus N more projects_' is an uncashable claim about the user's own "
            "portfolio — the phrasing the 2026-09-13 census grep could not match (#1762)"
        )

    def test_rank_numbering_runs_to_the_end(self, handler):
        out = handler._format_priority_standard(_ranked(SEVEN_PROJECTS))
        assert "7. **Seventh Project**" in out

    def test_granular_mode_still_differs_by_per_item_detail(self, handler):
        """The mode distinction survives the fix: GRANULAR carries the score
        breakdown, STANDARD does not. Item COUNT was never what made STANDARD
        less detailed — that was the defect wearing a product decision's coat."""
        ranked = _ranked(SEVEN_PROJECTS)
        assert "Score Breakdown" not in handler._format_priority_standard(ranked)
        assert "Score Breakdown" in handler._format_priority_granular(ranked)


# ---------------------------------------------------------------------------
# The floor's data channel: the sibling of the already-fixed DUE REMINDERS
# block, two sections down in the same function.
# ---------------------------------------------------------------------------


class TestFloorCompletedTodosDataChannelCarriesHeldSet:
    """``_format_domain_context`` composes the LLM's SYSTEM PROMPT, not
    ``turn.response``. A cap here removes information from the model with no
    follow-up turn in which it could ask for the rest."""

    TEN_HELD = [{"text": f"Completed todo {i}"} for i in range(1, 11)]

    def test_every_held_completed_todo_reaches_the_prompt(self, floor):
        out = floor._format_domain_context(
            {"completed_todos": self.TEN_HELD, "completed_todo_count": 10}
        )
        _assert_all_present(
            out, [t["text"] for t in self.TEN_HELD], "the floor's completed-todos block"
        )

    def test_the_stated_count_matches_the_items_rendered(self, floor):
        """The prompt asserted ``(10)`` and then showed five — a count the
        render itself had made unverifiable."""
        out = floor._format_domain_context(
            {"completed_todos": self.TEN_HELD, "completed_todo_count": 10}
        )
        assert "- Recently completed todos (10):" in out
        rendered = [ln for ln in out.split("\n") if ln.strip().startswith("• Completed todo")]
        assert len(rendered) == 10, (
            f"header claims 10, prompt carries {len(rendered)} — §5b: a render cap "
            "may shorten what the user sees; it must never change what the system "
            "believes it has (#1762)"
        )

    def test_the_gather_cap_denominator_is_untouched(self, floor):
        """#1776's half is NOT this build's: when the row count exceeds the
        held set, the count stays the row-derived one and the render stays the
        held set. Neither number is derived from the other."""
        out = floor._format_domain_context(
            {"completed_todos": self.TEN_HELD, "completed_todo_count": 42}
        )
        assert "- Recently completed todos (42):" in out
        _assert_all_present(out, [t["text"] for t in self.TEN_HELD], "the held set")


# ---------------------------------------------------------------------------
# The scope boundary, restated for THIS build. Green controls: each of these
# stays capped for a reason named in the assertion, so a later sweep cannot
# cross the line without reading why.
# ---------------------------------------------------------------------------


class TestDeliberatelyLeftCapped:
    def test_floor_blocked_items_cap_is_not_a_loss(self, floor):
        """``blocked[:10]`` sits over a set the gatherer already caps at 10, so
        it drops nothing today; the count rides honestly (#1778's ``N+`` floor).
        Left alone deliberately — it is a prompt-budget belt over a repo-scale
        source, not an elision."""
        held = [{"number": i, "title": f"Blocked {i}"} for i in range(1, 11)]
        out = floor._format_domain_context({"blocked_items": held, "blocked_count": 10})
        for b in held:
            assert b["title"] in out

    def test_floor_insight_bands_still_cap(self, floor):
        """Unchanged from the class-(a) boundary: composted insights grow with
        every session forever. Genuinely class (b), and NOT this cohort."""
        high = [
            {"expression": f"Insight {i}", "confidence": 0.9, "observation_count": 3}
            for i in range(1, 16)
        ]
        out = floor._format_domain_context(
            {"insights": {"is_empty": False, "total_count": 15, "high_confidence": high}}
        )
        assert "Insight 15" not in out

    def test_integration_guidance_caps_are_structurally_dead(self):
        """``configured[:5]`` / ``not_configured[:5]`` in the integrations
        guidance sit over ``KNOWN_INTEGRATIONS``, which has FOUR members — the
        caps cannot fire. Pinned so the fact is checked, not remembered: if the
        integration set ever grows past five, this test fails and the caps get
        the same treatment as the rest of this cohort."""
        from services.integrations.integration_status_service import KNOWN_INTEGRATIONS

        assert len(KNOWN_INTEGRATIONS) <= 5, (
            "the integration set grew past the render caps in "
            "_format_integration_guidance — those [:5] slices are now live "
            "elisions and need the #1762 treatment"
        )
