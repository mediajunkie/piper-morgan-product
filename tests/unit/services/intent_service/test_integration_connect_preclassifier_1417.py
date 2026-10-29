"""#1417 (Arch-ratified 2026-07-16): "connect my github" reaches the guidance lane.

Before: integration-connect utterances were mode-4 category-luck — the LLM
usually emitted EXECUTION + a free-form action, landing on the generic
unwired-write decline ("still on the way") while the OAuth flow, the settings
page, AND a purpose-built chat answer (_format_integration_setup_guidance) all
existed. Now surface 1 routes them deterministically to the EXISTING registry
canonical GUIDANCE/get_contextual_guidance (no new action; pure reachability).

Coverage shape per Arch's ruling: positive rows, the COLLISION guard (repo
slug / "repo" word stays in the #862 repo-link lane), and the REGRESSION row
("help me set up github" unchanged via the older #487 patterns).

#1595 Phase 3, thirty-first deletion (2026-10-29, issue 2195):
INTEGRATION_CONNECT_PATTERNS is now `[]` (tombstoned). Surface 1 no longer
claims any connect phrasing; the Inversion router answers them (the gate's 8
claimed corpus rows all route get_contextual_guidance, live via
read_canonical). Every positive pin below is converted to the decline +
inversion-routes idiom, not deleted: (a) surface 1 declines, (b) the
Inversion (stubbed, deterministic, no live LLM) routes the phrase to
get_contextual_guidance. `setup_target` is no longer asserted: it was a
surface-1-only context key with no reader in services/ or web/. The
collision-guard and negative rows still hold (an empty list can never hijack).
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)


def _classify(msg: str):
    return PreClassifier.pre_classify(msg)


async def _declines_and_routes_to_guidance(monkeypatch, message: str):
    """The thirty-first deletion's two-part pin (see module docstring)."""
    intent = _classify(message)
    assert intent is None, (
        "INTEGRATION_CONNECT_PATTERNS is deleted — pre-classifier should no "
        f"longer claim {message!r} (got {intent!r})"
    )
    routed = await assert_inversion_routes(
        monkeypatch,
        message,
        live_categories="read_canonical",
        expected_action="get_contextual_guidance",
    )
    assert routed.category == IntentCategory.GUIDANCE
    return routed


# ---------------------------------------------------------------------------
# Positive: natural connect phrasings route deterministically
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        "can we connect my github?",
        "connect my github",
        "Connect GitHub",
        "connect my slack",
        "set up notion",
        "setup notion for me",
        "hook up google calendar",
        "can you integrate slack with this?",
        "link my github account",
        "enable the calendar integration",
    ],
)
async def test_integration_connect_routes_to_guidance(message, monkeypatch):
    """#1595 Phase 3 thirty-first deletion: decline + inversion-routes."""
    await _declines_and_routes_to_guidance(monkeypatch, message)


# ---------------------------------------------------------------------------
# Collision guard (the load-bearing one): repo-slug / "repo" stays link_repo
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "connect the mediajunkie/piper-morgan-product repo",
        "connect my repo to the project",
        "link mediajunkie/test-piper-morgan",
        "add my github repo to the portfolio",
        "connect repository acme/widgets",
    ],
)
def test_repo_phrasings_never_hijacked(message):
    intent = _classify(message)
    if intent is not None:
        assert not (
            intent.action == "get_contextual_guidance" and intent.context.get("setup_target")
        ), f"repo-lane message hijacked into integration setup: {message!r}"


def test_slug_link_still_reaches_repo_management():
    """#1595 Phase 3, rule-10-licensed deletion (2026-10-09): this exact
    phrase is REPO_MANAGEMENT_PATTERNS' own corpus row "link mediajunkie/
    test-piper-morgan to the project" -- the owner/repo-form link literal
    is now deleted (one of the 5 of 9 non-survivors). The row passes via
    the mis-serve escape (the pattern's own claim, manage_repos, disagreed
    with the ruled destination, link_repo; a frozen N=10 surface-2 probe
    shows no WRITE/DESTRUCTIVE op in any sample) -- link_repo has no
    flip_group/live token in the current flag, so there is no live
    Inversion route to assert; declining cleanly is the whole proof."""
    intent = _classify("link mediajunkie/test-piper-morgan to the project")
    assert intent is None, (
        "REPO_MANAGEMENT_PATTERNS' owner/repo-form link literal is deleted — "
        f"surface 1 should decline (got {intent!r})"
    )


# ---------------------------------------------------------------------------
# Regression: the older #487 setup phrasings are unchanged
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_help_me_set_up_github_unchanged(monkeypatch):
    """#1595 Phase 3 thirty-first deletion: this phrase's last surface-1
    claim was INTEGRATION_CONNECT_PATTERNS (GUIDANCE_PATTERNS is `[]` since
    2026-10-09). Its corpus row scores MATCH get_contextual_guidance @0.95
    (inversion-week-calendar-description-full-score-2026-10-10-anthropic.md)."""
    await _declines_and_routes_to_guidance(monkeypatch, "help me set up github")


# ---------------------------------------------------------------------------
# Negative: no integration noun, no hijack
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    ["connect the dots for me", "add a todo to buy milk", "can you connect?"],
)
def test_no_integration_noun_no_match(message):
    intent = _classify(message)
    if intent is not None:
        assert intent.context.get("setup_target") is None


# ---------------------------------------------------------------------------
# #1471: temporal-calendar collision — connect verbs OUT-RANK the temporal
# calendar-noun patterns. "connect my calendar" matched `\bmy calendar\b` in
# TEMPORAL_PATTERNS (checked earlier than the #1417 lane) and answered with
# the current time; only pattern-avoiding phrasings ("link my google
# calendar") reached setup guidance. Fixed by precedence (pre_classify) and —
# originally — a TEMPORAL-collision substitution in detect_multiple_intents,
# replaced by #1505 with a general INTEGRATION_CONNECT pattern group (same
# shared _integration_connect_match, same behavior on this family; see
# test_multi_intent_connect_1505.py).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        "connect my calendar",
        "can you connect my calendar?",
        "link my calendar",
        "set up my calendar",
        "add my google calendar",
    ],
)
async def test_connect_calendar_beats_temporal_1471(message, monkeypatch):
    """#1595 Phase 3 thirty-first deletion: neither the temporal calendar
    patterns (`[]` since the fourth deletion) nor the connect lane claims
    now; the #1471 property (never a current-time answer) is held by the
    router, which routes the ask to get_contextual_guidance."""
    await _declines_and_routes_to_guidance(monkeypatch, message)


@pytest.mark.asyncio
async def test_connect_calendar_multi_intent_path_1471(monkeypatch):
    """The dominant chat path is classify_multiple → detect_multiple_intents,
    where TEMPORAL_PATTERNS matched before any connect handling existed —
    the #1471 misroute lived here even after pre_classify was fixed.

    #1595 Phase 3 thirty-first deletion: the multi path claims nothing for
    this phrase now (no TEMPORAL phantom, no surface-1 guidance), and the
    routed intent still carries the #1460 original_message FIELD."""
    result = PreClassifier.detect_multiple_intents("connect my calendar")
    resolved = [(i.category, i.action) for i in result.intents]
    assert resolved == [], f"multi-intent path resolved {resolved} (#1471)"
    routed = await _declines_and_routes_to_guidance(monkeypatch, "connect my calendar")
    assert routed.original_message == "connect my calendar"  # #1460 field


@pytest.mark.asyncio
async def test_multi_intent_substitution_keeps_other_parts_1471(monkeypatch):
    """Substitution, not suppression: the temporal phantom never appears.

    #1595 Phase 3 thirty-first deletion: the greeting declines with
    substantive residue (#1416/#1924) and the connect lane is `[]`, so the
    multi path claims nothing and the whole message reaches the router, which
    routes it to guidance (corpus: 'hi piper, connect my github' REVIEW-agrees
    get_contextual_guidance @0.8)."""
    result = PreClassifier.detect_multiple_intents("hi piper, connect my calendar")
    categories = {i.category for i in result.intents}
    assert IntentCategory.TEMPORAL not in categories
    assert result.intents == []
    await assert_inversion_routes(
        monkeypatch,
        "hi piper, connect my calendar",
        live_categories="read_canonical",
        expected_action="get_contextual_guidance",
    )


@pytest.mark.asyncio
async def test_no_duplicate_guidance_when_both_lanes_match_1471(monkeypatch):
    """'help me set up my calendar' once matched the #487 GUIDANCE patterns
    AND the connect substitution — exactly one guidance intent had to come
    out. #1595 Phase 3 thirty-first deletion: both lists are `[]`, so surface
    1 produces none (no duplicate is possible) and the router answers."""
    result = PreClassifier.detect_multiple_intents("help me set up my calendar")
    guidance = [
        i
        for i in result.intents
        if i.category == IntentCategory.GUIDANCE and i.action == "get_contextual_guidance"
    ]
    assert guidance == [], f"expected no surface-1 guidance intent, got {len(guidance)}"
    await _declines_and_routes_to_guidance(monkeypatch, "help me set up my calendar")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message,expected_action",
    [
        # #1595 Phase 3 fourth deletion (2026-10-01): TEMPORAL_PATTERNS is
        # now `[]` (tombstoned) — these three phrases no longer claim at
        # surface 1 at all (the #1471 property this test originally pinned,
        # "the connect blocker doesn't suppress a standalone temporal
        # query", has nothing left to not-suppress: none of these messages
        # even mentions a connect verb). Converted to the decline+
        # inversion-routes idiom, not deleted — surface 1 declines, and the
        # Inversion (stubbed, deterministic, no live LLM call) still routes
        # each to its correct destination when read_temporal is live.
        ("show my calendar", "week_calendar"),
        ("what time is it", "get_current_time"),
        ("my appointments", "week_calendar"),
    ],
)
async def test_temporal_queries_unchanged_1471(message, expected_action, monkeypatch):
    assert _classify(message) is None, f"surface 1 still claims: {message}"
    await assert_inversion_routes(
        monkeypatch,
        message,
        live_categories="read_temporal",
        expected_action=expected_action,
    )


@pytest.mark.parametrize(
    "message",
    [
        "add a meeting to my calendar",
        "add an event to my calendar",
        "set up a meeting on my calendar",
    ],
)
def test_calendar_event_writes_stay_out_of_connect_lane_1471(message):
    """Event-write nouns are blocked from the connect lane (#1471 blocker):
    these keep their pre-#1471 routing instead of flipping to setup guidance."""
    intent = _classify(message)
    if intent is not None:
        assert not (
            intent.action == "get_contextual_guidance" and intent.context.get("setup_target")
        ), f"event-write ask hijacked into integration setup: {message!r}"


# ---------------------------------------------------------------------------
# The handoff bug found via this issue: the classifier's Stage-1 return left
# Intent.original_message EMPTY (only context carried it), so the GUIDANCE
# canonical gate (_detect_setup_request reads the FIELD) never fired for ANY
# pre-classified setup request — they all floored (#1332/#1220 completion).
# ---------------------------------------------------------------------------


# #1595 Phase 3 thirty-first deletion (2026-10-29): the classifier's Stage-1
# (pre-classifier) return no longer claims "can we connect my github?", so
# IntentClassifier().classify would reach the LLM (none in unit tests). The
# served path is now the Inversion consult; both properties are pinned on the
# intent IT returns: the original_message FIELD is populated, and the GUIDANCE
# canonical setup gate fires on it.


@pytest.mark.asyncio
async def test_classifier_handoff_populates_original_message_field(monkeypatch):
    msg = "can we connect my github?"
    intent = await _declines_and_routes_to_guidance(monkeypatch, msg)
    assert intent.action == "get_contextual_guidance"
    assert intent.original_message == msg  # the FIELD, not just context


@pytest.mark.asyncio
async def test_setup_gate_fires_end_to_end_on_the_classified_intent(monkeypatch):
    from services.intent_service.canonical_handlers import CanonicalHandlers

    intent = await _declines_and_routes_to_guidance(monkeypatch, "can we connect my github?")
    assert CanonicalHandlers()._detect_setup_request(intent) == "integrations"
