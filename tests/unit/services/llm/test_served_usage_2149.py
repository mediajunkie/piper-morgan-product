"""#2149 step 3 (Arch 2026-11-01 09:13): the live path's ``served`` dict carries the
provider's OWN token usage, never an estimate, and ``RoutingDecision.usage`` sums it over
the router's calls (the two-stage router that first consumed it was removed 2026-11-01;
the flat path keeps the counts, Arch 09:12 "like for like")."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from services.llm.clients import LLMClient
from services.llm.config import LLMProvider

pytestmark = pytest.mark.asyncio


def _anthropic_response(text="ok", usage=True):
    block = SimpleNamespace(type="text", text=text)
    resp = SimpleNamespace(content=[block])
    if usage:
        resp.usage = SimpleNamespace(input_tokens=321, output_tokens=12)
    return resp


class TestServedUsage:
    async def test_anthropic_usage_reaches_served(self, monkeypatch):
        client = LLMClient.__new__(LLMClient)
        with (
            patch("services.llm.request_key.anthropic_client_for_request"),
            patch(
                "services.llm.clients.run_provider_call",
                AsyncMock(return_value=_anthropic_response()),
            ),
            patch("services.llm.cacheable_prompt.anthropic_user_content", return_value="p"),
        ):
            served: dict = {}
            client._last_usage = None
            text = await LLMClient._call_provider(
                client,
                LLMProvider.ANTHROPIC,
                "p",
                {"model": SimpleNamespace(value="claude-x"), "max_tokens": 10, "temperature": 0},
                None,
                None,
                None,
            )
        assert text == "ok"
        assert client._last_usage == {"input_tokens": 321, "output_tokens": 12}

    async def test_no_usage_object_means_no_usage_recorded(self):
        client = LLMClient.__new__(LLMClient)
        with (
            patch("services.llm.request_key.anthropic_client_for_request"),
            patch(
                "services.llm.clients.run_provider_call",
                AsyncMock(return_value=_anthropic_response(usage=False)),
            ),
            patch("services.llm.cacheable_prompt.anthropic_user_content", return_value="p"),
        ):
            client._last_usage = {"input_tokens": 1, "output_tokens": 1}  # stale from a prior call
            await LLMClient._call_provider(
                client,
                LLMProvider.ANTHROPIC,
                "p",
                {"model": SimpleNamespace(value="claude-x"), "max_tokens": 10, "temperature": 0},
                None,
                None,
                None,
            )
        assert client._last_usage is None, "reset per call; an estimate is never recorded"


class TestFlatPathUsage:
    async def test_flat_path_records_usage(self, monkeypatch):
        from services.intent_service import inversion_router as ir

        calls = []

        class _LLM:
            async def complete(self, *, prompt, system=None, served=None, **_):
                calls.append((prompt, system))
                if served is not None:
                    served["usage"] = {"input_tokens": 5, "output_tokens": 1}
                return (
                    '{"operation": "create_todo", "args": {}, "confidence": 0.9, "rationale": "r"}'
                )

        decision = await ir.route("add a todo", None, llm_service=_LLM(), user_id=None)
        assert decision.operation == "create_todo"
        assert len(calls) == 1 and calls[0][1] == ir._SYSTEM_PROMPT
        # Arch 09:12: the flat path records the provider's own usage; never an estimate.
        assert decision.usage == {"input_tokens": 5, "output_tokens": 1}
