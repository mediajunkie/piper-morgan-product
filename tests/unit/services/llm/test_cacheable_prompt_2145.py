"""#2145: the classifier's static prefix is marked cacheable; the text sent is unchanged.

Measured live 2026-10-23 on Haiku 4.5: call 1 wrote 4,153 cached tokens, calls
2..6 read 4,153 each (uncached remainder ~1,376). The router's 3.3k prompt is
under the model's cache minimum (cache_write 0), so it is not marked.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from services.llm.cacheable_prompt import CacheablePrompt, anthropic_user_content


def test_a_cacheable_prompt_is_the_same_string():
    p = CacheablePrompt("static head ", "the message")
    assert p == "static head the message"
    assert isinstance(p, str) and p.cache_prefix_len == len("static head ")


def test_anthropic_content_puts_one_breakpoint_after_the_prefix():
    blocks = anthropic_user_content(CacheablePrompt("HEAD", "tail"))
    assert blocks == [
        {"type": "text", "text": "HEAD", "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": "tail"},
    ]
    assert "".join(b["text"] for b in blocks) == "HEADtail"


@pytest.mark.parametrize(
    "prompt", ["plain text", CacheablePrompt("", "x"), CacheablePrompt("x", "")]
)
def test_a_plain_or_degenerate_prompt_is_sent_as_a_string(prompt):
    assert anthropic_user_content(prompt) == str(prompt)


def test_the_classifier_prompt_is_cacheable_up_to_the_user_message():
    import importlib

    clf = importlib.import_module("services.intent_service.classifier")
    from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT

    head = clf._CLASSIFICATION_PROMPT_STATIC_HEAD
    rendered = INTENT_CLASSIFICATION_PROMPT.format(
        user_message="MSG-2145",
        context_info="",
        file_context="",
        spatial_context="",
        verb_vocab="get",
    )
    assert rendered.startswith(head)
    assert rendered[len(head) :].startswith("MSG-2145")
    assert "MSG-2145" not in head


@pytest.mark.asyncio
async def test_the_anthropic_leg_sends_the_blocks():
    from services.llm.clients import LLMClient

    sent = {}

    def create(**kw):
        sent.update(kw)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text="{}")],
            usage=SimpleNamespace(
                input_tokens=10,
                output_tokens=2,
                cache_creation_input_tokens=0,
                cache_read_input_tokens=4153,
            ),
        )

    client = MagicMock()
    client.messages.create = create
    llm = LLMClient.__new__(LLMClient)
    config = {
        "model": SimpleNamespace(value="claude-haiku-4-5"),
        "max_tokens": 10,
        "temperature": 0,
    }
    with patch("services.llm.request_key.anthropic_client_for_request", return_value=client):
        out = await llm._anthropic_complete(CacheablePrompt("H", "T"), config, system="SYS")
    assert out == "{}"
    assert sent["system"] == "SYS"
    assert sent["messages"][0]["content"][0]["cache_control"] == {"type": "ephemeral"}
    assert sent["messages"][0]["content"][1]["text"] == "T"
