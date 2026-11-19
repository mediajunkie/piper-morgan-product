"""#2354: the conduct layer rides the floor's reply system prompt only.

Arch's ruling (issuecomment-6990069114) stands in for a rule-7 run with these checks:
(a) the classifier's system prompt and static head don't carry the layer, checked
    line by line from the layer itself, so a later edit can't pass by changing words;
(b) the classifier and router pins run whole, unchanged (the suites, not this file);
(c) the layer appears exactly once in the floor's system prompt, after the addendum
    and before the manifest, on a normal and on a denial turn;
(d) the size cap, and the 1,024-token cached-prefix minimum.

Layer measured: prompt assembly and the request the Anthropic leg builds. Not model
behaviour (that is the served question set, 2356) and not a token count (that needs
the provider's counting call; the sizes here are byte estimates, said so).
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from services.intent_service import conduct_layer as layer_module
from services.intent_service.conduct_layer import (
    CACHE_MIN_PREFIX_TOKENS,
    CAP_CHARS_PER_TOKEN,
    CONDUCT_LAYER,
    CONDUCT_LAYER_TOKEN_CAP,
    MIN_CHARS_PER_TOKEN,
    estimated_tokens,
)
from services.intent_service.conversational_floor import (
    FLOOR_DENIAL_ADDENDUM,
    FLOOR_SYSTEM_PROMPT_ADDENDUM,
    ConversationalFloor,
    FloorContext,
    capability_manifest_block,
)
from services.llm.cacheable_prompt import CacheablePrompt, anthropic_system_content

REPO = Path(__file__).resolve().parents[4]
LAYER_LINES = [line for line in CONDUCT_LAYER.splitlines() if line.strip()]


def _system(**ctx_kwargs) -> str:
    floor = ConversationalFloor(system_prompt_base="BASE-IDENTITY")
    ctx = FloorContext(user_message="what's on my plate today?", session_id="s-2354", **ctx_kwargs)
    return asyncio.run(floor._get_system_prompt(ctx))


# ── the wording ─────────────────────────────────────────────────────────────


def test_the_layer_is_the_approved_text_byte_for_byte():
    """xian approved the draft's block (11-18); CXO voiced it. The build copies it
    verbatim, so a change to either side fails here and goes back to CXO."""
    draft = (
        REPO / "docs/internal/architecture/design-records/piper-conduct-layer-draft-2026-11-12.md"
    ).read_text()
    assert draft.split("\n---\n")[1].strip() == CONDUCT_LAYER
    assert len(LAYER_LINES) == 10  # the heading and nine rules


# ── (a) not in the router's prompt ──────────────────────────────────────────


def _classifier_system_prompts() -> dict[str, str]:
    from services.configuration.personalization_service import NEUTRAL_DEFAULT_CONTEXT
    from services.configuration.piper_config_loader import piper_config_loader

    return {
        # resolve_system_prompt_standalone: no principal, or PM's own request
        "file": piper_config_loader.get_system_prompt(),
        # resolve_system_prompt_standalone: any other principal, before they customise
        "neutral": piper_config_loader._format_system_prompt(dict(NEUTRAL_DEFAULT_CONTEXT)),
    }


@pytest.mark.parametrize("name", ["file", "neutral"])
def test_the_classifier_system_prompt_has_no_line_of_the_layer(name):
    prompt = _classifier_system_prompts()[name]
    for line in LAYER_LINES:
        assert line not in prompt, f"conduct layer line in the classifier's {name} prompt"


def test_the_classifier_prompt_text_has_no_line_of_the_layer():
    from services.intent_service.classifier import _CLASSIFICATION_PROMPT_STATIC_HEAD
    from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT

    for text in (_CLASSIFICATION_PROMPT_STATIC_HEAD, INTENT_CLASSIFICATION_PROMPT):
        for line in LAYER_LINES:
            assert line not in text


def test_the_layer_is_not_written_into_piper_md():
    piper_md = (REPO / "config/PIPER.md").read_text()
    for line in LAYER_LINES:
        assert line not in piper_md


# ── (c) once, in position, on normal and denial turns ───────────────────────


@pytest.mark.parametrize(
    "denial, addendum", [(False, FLOOR_SYSTEM_PROMPT_ADDENDUM), (True, FLOOR_DENIAL_ADDENDUM)]
)
def test_the_layer_appears_once_after_the_addendum(denial, addendum):
    prompt = _system(denial_mode=denial)
    assert prompt.count(CONDUCT_LAYER) == 1
    at = prompt.index(CONDUCT_LAYER)
    assert prompt.index(addendum) + len(addendum) <= at
    assert prompt.index("BASE-IDENTITY") < prompt.index(addendum)


def test_on_a_normal_turn_the_manifest_follows_the_layer():
    prompt = _system()
    manifest = capability_manifest_block()
    assert prompt.index(CONDUCT_LAYER) + len(CONDUCT_LAYER) <= prompt.index(manifest)


def test_a_denial_turn_carries_the_layer_and_no_manifest():
    prompt = _system(denial_mode=True)
    assert CONDUCT_LAYER in prompt  # rule 9 is about declining
    assert capability_manifest_block() not in prompt


def test_the_breakpoint_ends_after_the_manifest_and_warmth_follows_it():
    prompt = _system(formality_baseline=0.9)
    assert isinstance(prompt, CacheablePrompt)
    prefix, rest = prompt[: prompt.cache_prefix_len], prompt[prompt.cache_prefix_len :]
    assert prefix.endswith(capability_manifest_block())
    assert rest.startswith("\nTone:")  # the per-person warmth line, after the breakpoint
    assert CONDUCT_LAYER in prefix


def test_with_no_warmth_the_whole_prompt_is_the_prefix():
    prompt = _system()
    assert prompt.cache_prefix_len == len(prompt)
    blocks = anthropic_system_content(prompt)
    assert len(blocks) == 1 and blocks[0]["cache_control"] == {"type": "ephemeral"}


def test_the_draft_revision_call_does_not_carry_the_layer():
    from services.intent_service.conversational_floor import FLOOR_DRAFT_REVISION_INSTRUCTION

    for line in LAYER_LINES:
        assert line not in FLOOR_DRAFT_REVISION_INSTRUCTION
    sent = {}

    class _LLM:
        async def complete(self, **kw):
            sent.update(kw)
            return "revised"

    floor = ConversationalFloor(llm_client=_LLM(), system_prompt_base="BASE")
    asyncio.run(floor.revise_draft(user_message="shorter", draft="a long draft", user_id="u"))
    assert sent["system"] == FLOOR_DRAFT_REVISION_INSTRUCTION


# ── the Anthropic leg sends the system as blocks with one breakpoint ────────


def test_system_blocks_split_at_the_prefix():
    blocks = anthropic_system_content(CacheablePrompt("FIXED", "\nTone: warm"))
    assert blocks == [
        {"type": "text", "text": "FIXED", "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": "\nTone: warm"},
    ]


@pytest.mark.parametrize("system", ["plain", CacheablePrompt("", "x")])
def test_a_plain_system_is_sent_as_a_string(system):
    assert anthropic_system_content(system) == str(system)


@pytest.mark.asyncio
async def test_the_anthropic_leg_sends_the_system_blocks():
    from services.llm.clients import LLMClient

    sent = {}

    def create(**kw):
        sent.update(kw)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text="ok")],
            usage=SimpleNamespace(
                input_tokens=10,
                output_tokens=2,
                cache_creation_input_tokens=0,
                cache_read_input_tokens=0,
            ),
        )

    client = MagicMock()
    client.messages.create = create
    client.messages.with_raw_response.create = lambda **kw: SimpleNamespace(
        parse=lambda: create(**kw), retries_taken=0, status_code=200
    )
    llm = LLMClient.__new__(LLMClient)
    config = {
        "model": SimpleNamespace(value="claude-sonnet-4-6"),
        "max_tokens": 10,
        "temperature": 0,
    }
    system = CacheablePrompt("FIXED", "\nTone: warm")
    with patch("services.llm.request_key.anthropic_client_for_request", return_value=client):
        await llm._anthropic_complete("hello", config, system=system)
    assert sent["system"][0] == {
        "type": "text",
        "text": "FIXED",
        "cache_control": {"type": "ephemeral"},
    }
    assert sent["system"][1]["text"] == "\nTone: warm"
    assert sent["messages"][0]["content"] == "hello"  # one breakpoint, in the system


# ── (d) size ────────────────────────────────────────────────────────────────


def test_the_layer_is_under_the_cap_by_an_over_estimate(capsys):
    assert estimated_tokens(CONDUCT_LAYER, chars_per_token=CAP_CHARS_PER_TOKEN) <= (
        CONDUCT_LAYER_TOKEN_CAP
    )
    assert layer_module.main() == 0
    assert "cap 1000: OK" in capsys.readouterr().out


def test_the_size_check_fails_above_the_cap(monkeypatch, capsys):
    monkeypatch.setattr(layer_module, "CONDUCT_LAYER", "x" * (3 * CONDUCT_LAYER_TOKEN_CAP + 30))
    assert layer_module.main() == 1
    assert "OVER CAP" in capsys.readouterr().out


def test_the_cached_prefix_reaches_the_cache_minimum_with_the_neutral_base():
    """CIO's build check (design record, H1): base + addendum + layer + manifest
    reaches 1,024 tokens, by an UNDER-estimate, with the shortest real base (the
    neutral default). A shorter prefix would not be cached at all."""
    from services.configuration.personalization_service import NEUTRAL_DEFAULT_CONTEXT
    from services.configuration.piper_config_loader import piper_config_loader

    base = piper_config_loader._format_system_prompt(dict(NEUTRAL_DEFAULT_CONTEXT))
    floor = ConversationalFloor(system_prompt_base=base)
    prompt = asyncio.run(floor._get_system_prompt(FloorContext(user_message="hi", session_id="s")))
    prefix = prompt[: prompt.cache_prefix_len]
    assert estimated_tokens(prefix, chars_per_token=MIN_CHARS_PER_TOKEN) >= CACHE_MIN_PREFIX_TOKENS
