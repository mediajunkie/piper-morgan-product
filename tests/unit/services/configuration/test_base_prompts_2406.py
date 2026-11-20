"""#2406: the reply prompt states each conduct rule once; the classifier's prompt is frozen.

Arch's ruling of 2026-11-20 (mails 01M7XDBPT0 and 01M7XDJEAB), after the classifier
screen showed that any change to the classifier's system prompt moves routing (17 of 21
re-screened rows):

- The seeded or stored base (every tester's) and the fallback get CXO's behavior lines
  on the REPLY path only. The classifier's path keeps today's lines byte for byte, pinned
  here by sha256, so no run is needed.
- ``config/PIPER.md`` (xian's account and no-account calls) is one text for both calls
  and is unchanged in this unit. Its bullets wait on issue 2410.
- ``NEUTRAL_DEFAULT_CONTEXT`` itself is out of scope.

Layer: the formatted base prompts and the floor's composed reply prompt. Not a model
call.
"""

from __future__ import annotations

import asyncio
import hashlib
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from services.configuration.personalization_service import (
    NEUTRAL_DEFAULT_CONTEXT,
    personalization_service,
)
from services.configuration.piper_config_loader import (
    BEHAVIOR_GUIDELINES_HEADING,
    CLASSIFIER_BEHAVIOR_GUIDELINES_LINES,
    CLASSIFIER_FALLBACK_BEHAVIOR_GUIDELINES_LINES,
    REPLY_BEHAVIOR_GUIDELINES_LINES,
    PiperConfigLoader,
)
from services.intent_service.conduct_layer import CONDUCT_LAYER
from services.intent_service.conversational_floor import ConversationalFloor, FloorContext

REPO = Path(__file__).resolve().parents[4]

#: sha256 of the classifier's system prompt at main before this change (2026-11-20,
#: `c9097d5091`), read from ``PiperConfigLoader`` there. A change to any of these is a
#: routing change: it goes through rule 7 (issue 2410), never through an edit here.
MAIN_CLASSIFIER_SHA256 = {
    "B: the neutral default": "7756b59481ff241b94f21fcf49c0b7b25aafc6d707f6710494a4e56c02f9c003",
    "the fallback": "ae1b74ece4123f0a61a40f0e798542f51c09e046f22a462c15adf0ce7e263da1",
}

#: The behavior lines the reply no longer carries on base B and the fallback.
REMOVED_FROM_THE_REPLY = [
    "Provide evidence-based responses",
    "Reference specific projects",
    "Use the user's name (if known)",
]

#: Words that mark a rule the conduct layer owns (rule 2: evidence; rule 7: clarifying
#: questions). The reply's base B must not use them outside the layer.
RULE_MARKERS = ["evidence-based", "clarifying questions", "seeking clarification"]


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _loader() -> PiperConfigLoader:
    return PiperConfigLoader(config_path=str(REPO / "config" / "PIPER.md"))


def _base_b(lines=None) -> str:
    loader = _loader()
    if lines is None:
        return loader._format_system_prompt(dict(NEUTRAL_DEFAULT_CONTEXT))
    return loader._format_system_prompt(dict(NEUTRAL_DEFAULT_CONTEXT), lines)


def _reply_prompt(base: str, *, denial: bool = False) -> str:
    floor = ConversationalFloor(system_prompt_base=base)
    ctx = FloorContext(user_message="what's on my plate?", session_id="s-2406", denial_mode=denial)
    return str(asyncio.run(floor._get_system_prompt(ctx)))


# ── the classifier's prompt is frozen (no run, like row L) ──────────────────────


def test_classifier_system_prompt_base_b_has_mains_sha256():
    assert _sha(_base_b()) == MAIN_CLASSIFIER_SHA256["B: the neutral default"]
    assert _sha(_base_b(CLASSIFIER_BEHAVIOR_GUIDELINES_LINES)) == _sha(_base_b())


def test_classifier_system_prompt_fallback_has_mains_sha256():
    loader = _loader()
    assert _sha(loader._get_default_system_prompt()) == MAIN_CLASSIFIER_SHA256["the fallback"]
    assert (
        _sha(loader._get_default_system_prompt(for_reply=False))
        == (MAIN_CLASSIFIER_SHA256["the fallback"])
    )


def test_the_classifier_asks_for_the_classifier_lines():
    """``resolve_system_prompt_standalone`` (classifier.py) passes for_reply=False."""
    with patch.object(
        type(personalization_service), "resolve_system_prompt", new=AsyncMock(return_value="x")
    ) as resolve:

        class _Scope:
            async def __aenter__(self):
                return object()

            async def __aexit__(self, *exc):
                return False

        with patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            return_value=_Scope(),
        ):
            asyncio.run(personalization_service.resolve_system_prompt_standalone(None))
    assert resolve.await_args.kwargs == {"for_reply": False}


def test_the_floor_asks_for_the_reply_lines():
    source = (REPO / "services" / "intent_service" / "conversational_floor.py").read_text()
    assert source.count("for_reply=True") == 1
    classifier = (REPO / "services" / "intent_service" / "classifier.py").read_text()
    assert "for_reply" not in classifier


def test_piper_md_is_one_text_for_both_calls_and_unchanged_here():
    """Base A waits on issue 2410: no second copy, no reply-side filter (Arch)."""
    loader = _loader()
    assert loader.get_system_prompt(for_reply=True) == loader.get_system_prompt(for_reply=False)
    assert (
        _sha(loader.get_system_prompt())
        == "d4f08cdc2c686c42d77835b1e7bc1bcb59217bd9bcd952841dcd03fe9f454cbe"
    )


def test_neutral_default_context_is_untouched():
    """Out of scope (Arch): every existing account holds a seeded copy of this dict."""
    assert set(NEUTRAL_DEFAULT_CONTEXT) == {"User Context", "Standing Priorities"}


# ── the reply's lines are CXO's ─────────────────────────────────────────────────


def test_the_reply_lines_are_cxos_four():
    assert REPLY_BEHAVIOR_GUIDELINES_LINES == (
        "- Be direct and efficiency-focused",
        "- Maintain professional but personable tone",
        "- Suggest next steps when appropriate",
        "- Use the person's name if you know it",
    )


def test_the_reply_base_b_and_fallback_end_in_cxos_block():
    block = "\n".join([BEHAVIOR_GUIDELINES_HEADING, *REPLY_BEHAVIOR_GUIDELINES_LINES])
    assert _base_b(REPLY_BEHAVIOR_GUIDELINES_LINES).rstrip("\n").endswith(block)
    assert _loader()._get_default_system_prompt(for_reply=True).endswith(block)


def test_each_block_has_one_copy_in_the_loader_source():
    source = (REPO / "services" / "configuration" / "piper_config_loader.py").read_text()
    assert source.count('"## BEHAVIOR GUIDELINES"') == 1
    for lines in (
        REPLY_BEHAVIOR_GUIDELINES_LINES,
        CLASSIFIER_BEHAVIOR_GUIDELINES_LINES,
        CLASSIFIER_FALLBACK_BEHAVIOR_GUIDELINES_LINES,
    ):
        # A line shared by two blocks appears once per block that holds it.
        for line in lines:
            holders = sum(
                line in block
                for block in (
                    REPLY_BEHAVIOR_GUIDELINES_LINES,
                    CLASSIFIER_BEHAVIOR_GUIDELINES_LINES,
                    CLASSIFIER_FALLBACK_BEHAVIOR_GUIDELINES_LINES,
                )
            )
            assert source.count(f'"{line}"') == holders, line


@pytest.mark.parametrize("denial", [False, True])
def test_reply_prompt_states_each_rule_once_base_b(denial):
    """The acceptance row, for the reply prompt only (CXO's condition): the layer once,
    and nothing in base B's reply text restating a rule. The classifier's base keeps
    the old lines by design until issue 2410."""
    base = _base_b(REPLY_BEHAVIOR_GUIDELINES_LINES)
    prompt = _reply_prompt(base, denial=denial)
    assert prompt.count(CONDUCT_LAYER) == 1
    for line in REMOVED_FROM_THE_REPLY:
        assert line not in prompt, line
    for marker in RULE_MARKERS:
        assert marker not in base.lower(), marker


def test_reply_prompt_states_each_rule_once_fallback():
    base = _loader()._get_default_system_prompt(for_reply=True)
    prompt = _reply_prompt(base)
    assert prompt.count(CONDUCT_LAYER) == 1
    for line in REMOVED_FROM_THE_REPLY:
        assert line not in prompt, line


# ── row L: the live inversion router's request never takes the base (Arch 11-20) ──


def _router_request(phrase: str) -> str:
    from services.intent_service.inversion_router import (
        _SYSTEM_PROMPT,
        build_routing_prompt,
        derive_routing_grammar,
    )

    return _SYSTEM_PROMPT + "\x00" + build_routing_prompt(phrase, derive_routing_grammar(), None)


def test_the_router_request_is_the_same_whatever_the_base_says(monkeypatch):
    """No run for row L: its request is built from a constant system prompt and the
    catalog. Changing every base to something else leaves it byte-identical."""
    phrase = "what should I do about this bug"
    before = _sha(_router_request(phrase))
    monkeypatch.setattr(
        PiperConfigLoader, "get_system_prompt", lambda self, **kw: "A DIFFERENT BASE"
    )
    monkeypatch.setattr(
        PiperConfigLoader, "_format_system_prompt", lambda self, config, *a: "A DIFFERENT BASE"
    )
    monkeypatch.setattr(
        PiperConfigLoader, "_get_default_system_prompt", lambda self, **kw: "A DIFFERENT BASE"
    )
    assert _sha(_router_request(phrase)) == before


def test_the_router_module_reads_no_base():
    source = (REPO / "services" / "intent_service" / "inversion_router.py").read_text()
    for name in ["piper_config_loader", "personalization_service", "resolve_system_prompt"]:
        assert name not in source, name
