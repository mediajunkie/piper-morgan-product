"""Anthropic reply parse picks the first `type == "text"` block (Arch 10-30 15:20 item 3, 2227).

`content[0].text` assumed the first block is text. A reply from an extended-thinking
model can lead with a thinking block (AttributeError), and an empty content list
raised IndexError. The pick returns the first text block's text; with none it
raises, and the raise lands in the existing provider-failure path
(`_complete_raw` -> `AllProvidersFailed`), never an empty string.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from services.llm.clients import AllProvidersFailed, LLMClient
from services.llm.request_key import request_api_key

_USAGE = SimpleNamespace(
    input_tokens=10,
    output_tokens=2,
    cache_creation_input_tokens=0,
    cache_read_input_tokens=0,
)
_CONFIG = {
    "model": SimpleNamespace(value="claude-haiku-4-5"),
    "max_tokens": 10,
    "temperature": 0,
}
THINKING = SimpleNamespace(type="thinking", thinking="hmm")
TEXT = SimpleNamespace(type="text", text='{"action": "x"}')


def _llm_returning(content):
    client = MagicMock()
    client.messages.create = lambda **kw: SimpleNamespace(content=content, usage=_USAGE)
    llm = LLMClient.__new__(LLMClient)
    return llm, client


@pytest.mark.asyncio
async def test_text_block_after_a_thinking_block_is_returned():
    llm, client = _llm_returning([THINKING, TEXT])
    with patch("services.llm.request_key.anthropic_client_for_request", return_value=client):
        assert await llm._anthropic_complete("p", _CONFIG) == '{"action": "x"}'


@pytest.mark.asyncio
async def test_text_first_reply_is_the_same_string_as_before():
    llm, client = _llm_returning([TEXT])
    with patch("services.llm.request_key.anthropic_client_for_request", return_value=client):
        assert await llm._anthropic_complete("p", _CONFIG) == TEXT.text


@pytest.mark.asyncio
@pytest.mark.parametrize("content", [[THINKING], []], ids=["thinking-only", "empty-list"])
async def test_no_text_block_is_a_provider_failure_not_an_empty_reply(content):
    class _Cfg:
        def get_default_provider(self, user_id=None):
            return "anthropic"

        def get_configured_providers(self, user_id=None):
            return ["anthropic"]

    llm, client = _llm_returning(content)
    llm._config_service = _Cfg()
    llm._output_filter = None
    llm.anthropic_client = object()
    llm.openai_client = None
    llm.gemini_client = None
    with patch("services.llm.request_key.anthropic_client_for_request", return_value=client):
        with patch.object(LLMClient, "_is_provider_configured", return_value=True):
            with request_api_key({"anthropic": "sk-ant-test"}):
                with pytest.raises(AllProvidersFailed) as excinfo:
                    await llm._complete_raw("conversation", "hi", user_id="u1")
    assert excinfo.value.attempts[0][0] == "anthropic"
    assert "no text block" in excinfo.value.primary_reason
