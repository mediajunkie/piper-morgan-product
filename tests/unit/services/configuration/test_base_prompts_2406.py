"""#2406: the bases and the conduct layer state each rule once.

CXO's words (2026-11-20) and Arch's scope: seven ``config/PIPER.md`` bullets and its
"When Queries Are Ambiguous" section are removed, the shared behavior block loses two lines and has one reworded, and the
fallback prompt takes the block from the same constant. ``NEUTRAL_DEFAULT_CONTEXT``
itself is out of scope.

Layer: the formatted base prompts and the floor's composed reply prompt. Not a
model call: whether routing moved is rule 7's run, on the issue.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from services.configuration.personalization_service import NEUTRAL_DEFAULT_CONTEXT
from services.configuration.piper_config_loader import (
    BEHAVIOR_GUIDELINES_HEADING,
    BEHAVIOR_GUIDELINES_LINES,
    PiperConfigLoader,
)
from services.intent_service.conduct_layer import CONDUCT_LAYER
from services.intent_service.conversational_floor import ConversationalFloor, FloorContext

REPO = Path(__file__).resolve().parents[4]

#: Every line the edit removed, as it stood. None may come back in any base.
REMOVED = [
    # config/PIPER.md, Interaction Principles and Key Behaviors
    "Proactive about seeking clarification when requirements are ambiguous",
    "Evidence-based responses with concrete examples",
    "Maintains high standards for accuracy and completeness",
    "Asks clarifying questions when faced with ambiguity",
    "Follows up on incomplete tasks",
    "Learns from user feedback and corrections",
    "Maintains conversation context across sessions",
    # config/PIPER.md, "When Queries Are Ambiguous" (the whole section; CXO 11-20)
    "When Queries Are Ambiguous",
    "Ask clarifying questions",
    "Offer multiple interpretations",
    "Provide examples of similar queries",
    "Learn from user clarification for future",
    # the shared block and the fallback
    "Provide evidence-based responses",
    "Reference specific projects",
    "Use the user's name (if known)",
]

#: Words that mark a rule the conduct layer now owns. Outside the layer, the
#: composed reply prompt's BASE must not use them (rule 2: evidence; rule 7:
#: clarifying questions).
RULE_MARKERS = ["evidence-based", "clarifying questions", "seeking clarification"]


def _loader() -> PiperConfigLoader:
    return PiperConfigLoader(config_path=str(REPO / "config" / "PIPER.md"))


def _bases() -> dict[str, str]:
    loader = _loader()
    return {
        "A: config/PIPER.md": loader.get_system_prompt(),
        "B: the neutral default": loader._format_system_prompt(dict(NEUTRAL_DEFAULT_CONTEXT)),
        "the fallback": loader._get_default_system_prompt(),
    }


def _reply_prompt(base: str, *, denial: bool = False) -> str:
    floor = ConversationalFloor(system_prompt_base=base)
    ctx = FloorContext(user_message="what's on my plate?", session_id="s-2406", denial_mode=denial)
    return str(asyncio.run(floor._get_system_prompt(ctx)))


@pytest.mark.parametrize("name", ["A: config/PIPER.md", "B: the neutral default", "the fallback"])
def test_no_base_carries_a_removed_line(name):
    base = _bases()[name]
    for line in REMOVED:
        assert line not in base, line


def test_piper_md_keeps_the_bullets_cxo_kept():
    text = (REPO / "config" / "PIPER.md").read_text()
    for kept in [
        "- Respects user time and preferences",
        "- Adaptive to individual communication styles",
        "- Provides actionable recommendations, not just information",
    ]:
        assert text.count(kept) == 1, kept


def test_the_block_is_cxos_four_lines():
    assert BEHAVIOR_GUIDELINES_LINES == (
        "- Be direct and efficiency-focused",
        "- Maintain professional but personable tone",
        "- Suggest next steps when appropriate",
        "- Use the person's name if you know it",
    )


@pytest.mark.parametrize("name", ["A: config/PIPER.md", "B: the neutral default", "the fallback"])
def test_every_base_ends_in_the_one_block(name):
    block = "\n".join([BEHAVIOR_GUIDELINES_HEADING, *BEHAVIOR_GUIDELINES_LINES])
    base = _bases()[name]
    assert base.count(BEHAVIOR_GUIDELINES_HEADING) == 1
    assert base.rstrip("\n").endswith(block)


def test_the_block_has_one_copy_in_the_loader_source():
    """Arch: the fallback takes the block from the constant, not a second copy."""
    source = (REPO / "services" / "configuration" / "piper_config_loader.py").read_text()
    for line in BEHAVIOR_GUIDELINES_LINES:
        assert source.count(line[2:]) == 1, line
    assert source.count('"## BEHAVIOR GUIDELINES"') == 1


def test_neutral_default_context_is_untouched():
    """Out of scope (Arch): every existing account holds a seeded copy of this dict."""
    assert set(NEUTRAL_DEFAULT_CONTEXT) == {"User Context", "Standing Priorities"}


@pytest.mark.parametrize("name", ["A: config/PIPER.md", "B: the neutral default"])
@pytest.mark.parametrize("denial", [False, True])
def test_the_reply_prompt_states_each_rule_once(name, denial):
    """The acceptance row: the layer once, and nothing outside it restating a rule."""
    base = _bases()[name]
    prompt = _reply_prompt(base, denial=denial)
    assert prompt.count(CONDUCT_LAYER) == 1
    for line in REMOVED:
        assert line not in prompt, line
    for marker in RULE_MARKERS:
        assert marker not in base.lower(), marker
