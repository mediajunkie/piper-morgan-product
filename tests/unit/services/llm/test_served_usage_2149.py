"""#2149 step 3 (Arch 2026-11-01 09:13): the live path's ``served`` dict carries the
provider's OWN token usage, never an estimate; the two-stage router's ``stage_metrics``
carry it per stage when present and omit it when not."""

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


class TestStageMetricsCarryTokens:
    async def test_tokens_present_when_the_provider_reported_them(self, monkeypatch):
        from services.intent_service import inversion_router as ir

        monkeypatch.setenv("PIPER_INVERSION_TWO_STAGE", "1")
        replies = iter(
            [
                '{"group": "todos_and_reminders", "confidence": 0.9}',
                '{"operation": "create_todo", "args": {}, "confidence": 0.9, "rationale": "r"}',
            ]
        )

        class _LLM:
            async def complete(self, *, served=None, **_):
                if served is not None:
                    served["provider"] = "anthropic"
                    served["model"] = "m"
                    served["usage"] = {"input_tokens": 100, "output_tokens": 7}
                return next(replies)

        decision = await ir.route("add a todo", None, llm_service=_LLM(), user_id=None)
        assert decision.operation == "create_todo"
        assert [m["stage"] for m in decision.stage_metrics] == [1, 2]
        assert all(
            m["input_tokens"] == 100 and m["output_tokens"] == 7 for m in decision.stage_metrics
        )
        assert decision.usage == {
            "input_tokens": 200,
            "output_tokens": 14,
        }, "the decision sums its stages"

    async def test_tokens_absent_when_the_provider_reported_none(self, monkeypatch):
        from services.intent_service import inversion_router as ir

        monkeypatch.setenv("PIPER_INVERSION_TWO_STAGE", "1")
        replies = iter(
            [
                '{"group": "todos_and_reminders", "confidence": 0.9}',
                '{"operation": "create_todo", "args": {}, "confidence": 0.9, "rationale": "r"}',
            ]
        )

        class _LLM:
            async def complete(self, *, served=None, **_):
                if served is not None:
                    served["provider"] = "anthropic"
                    served["model"] = "m"
                return next(replies)

        decision = await ir.route("add a todo", None, llm_service=_LLM(), user_id=None)
        assert decision.operation == "create_todo"
        assert all("input_tokens" not in m for m in decision.stage_metrics), "never estimated"
        assert decision.usage is None

    async def test_flag_off_path_is_unchanged(self, monkeypatch):
        from services.intent_service import inversion_router as ir

        monkeypatch.delenv("PIPER_INVERSION_TWO_STAGE", raising=False)
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
        assert decision.operation == "create_todo" and decision.stage_metrics is None
        assert len(calls) == 1 and calls[0][1] == ir._SYSTEM_PROMPT
        # Arch 09:12: the flat path records usage too, like for like.
        assert decision.usage == {"input_tokens": 5, "output_tokens": 1}
