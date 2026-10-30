"""#2101 — a provider completion never holds the event loop.

PA's watchdog read on alpha 987dd10ed7 (2026-10-20): 26 of 26 `event_loop_blocked` stacks
ended in `clients.py` calling the synchronous Anthropic SDK (`client.messages.create`) on the
loop, down through sync httpx to `ssl.read`; 91 s of a 155 s canonical run were blocked. The
three provider round trips now run in `asyncio.to_thread`.

LAYER: `LLMClient`'s provider legs with the per-request client builder replaced by a fake that
records the calling thread (no network). DENOMINATOR: the Anthropic and OpenAI legs (the Gemini leg has no
per-request client path and raises before any network call); a source pin over the module
for a bare provider call inside a coroutine.
"""

from __future__ import annotations

import ast
import threading
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.llm import clients as mod


class _Recorder:
    def __init__(self, response):
        self.thread = None
        self.kwargs = None
        self._response = response

    def __call__(self, **kwargs):
        self.thread = threading.current_thread()
        self.kwargs = kwargs
        return self._response


def _anthropic_fake():
    response = SimpleNamespace(
        usage=SimpleNamespace(input_tokens=3, output_tokens=2),
        content=[SimpleNamespace(type="text", text="hi")],
    )
    rec = _Recorder(response)
    client = SimpleNamespace(messages=SimpleNamespace(create=rec))
    return client, rec


def _openai_fake():
    response = SimpleNamespace(
        usage=SimpleNamespace(prompt_tokens=3, completion_tokens=2),
        choices=[SimpleNamespace(message=SimpleNamespace(content="hi"))],
    )
    rec = _Recorder(response)
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=rec)))
    return client, rec


def _config(model):
    return {"model": model, "max_tokens": 16, "temperature": 0.0}


def _llm():
    return mod.LLMClient.__new__(mod.LLMClient)


@pytest.mark.asyncio
async def test_anthropic_round_trip_runs_on_a_worker_thread():
    client, rec = _anthropic_fake()
    model = next(m for m in mod.LLMModel if "claude" in m.value.lower())
    with patch("services.llm.request_key.anthropic_client_for_request", return_value=client):
        text = await _llm()._anthropic_complete("hello", _config(model))
    assert text == "hi"
    assert rec.thread is not None and rec.thread is not threading.current_thread()
    assert rec.kwargs["messages"] == [{"role": "user", "content": "hello"}]


@pytest.mark.asyncio
async def test_openai_round_trip_runs_on_a_worker_thread():
    client, rec = _openai_fake()
    model = next(m for m in mod.LLMModel if "gpt" in m.value.lower())
    with (
        patch("services.llm.request_key.request_spend_key", return_value="k-2101"),
        patch("services.llm.clients.OpenAI", return_value=client),
    ):
        text = await _llm()._openai_complete("hello", _config(model))
    assert text == "hi"
    assert rec.thread is not None and rec.thread is not threading.current_thread()


def _provider_calls(tree):
    """Every Call whose attribute chain ends in a provider round-trip method."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            chain = []
            cur = node.func
            while isinstance(cur, ast.Attribute):
                chain.append(cur.attr)
                cur = cur.value
            dotted = ".".join(reversed(chain))
            if dotted.endswith(("messages.create", "chat.completions.create", "generate_content")):
                found.append((node.lineno, dotted))
    return found


def _wrapped_calls(tree):
    """Provider methods passed BY REFERENCE to run_provider_call / to_thread / run_in_executor."""
    wrapped = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        fn = node.func
        name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", "")
        if name not in {"run_provider_call", "to_thread", "run_in_executor"}:
            continue
        for arg in node.args:
            if isinstance(arg, ast.Attribute):
                wrapped.add(arg.lineno)
    return wrapped


def test_no_provider_round_trip_is_called_inside_a_coroutine():
    """Arch's condition 3 (2026-10-20): an AST walk, not a regex. A provider method may only
    appear as a reference handed to the executor, never as a call inside clients.py."""
    tree = ast.parse(Path(mod.__file__).read_text())
    calls = _provider_calls(tree)
    assert calls == [], f"provider round trip called directly: {calls}"
    # and the two legs do hand their methods to the executor
    src = Path(mod.__file__).read_text()
    assert "run_provider_call(client.messages.create" in src
    assert "run_provider_call(client.chat.completions.create" in src


def _ctor_kwargs(tree, ctor_name):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and getattr(node.func, "id", None) == ctor_name:
            return {kw.arg for kw in node.keywords}
    return None


def test_both_sdk_clients_carry_explicit_timeout_and_retries():
    """Arch's condition 1: the SDK defaults (600 s read, 2 retries) would let a hung call hold
    a worker for half an hour, and a thread cannot be cancelled from the loop."""
    from services.llm import request_key

    anthropic_kwargs = _ctor_kwargs(ast.parse(Path(request_key.__file__).read_text()), "Anthropic")
    openai_kwargs = _ctor_kwargs(ast.parse(Path(mod.__file__).read_text()), "OpenAI")
    assert anthropic_kwargs is not None and {"timeout", "max_retries"} <= anthropic_kwargs
    assert openai_kwargs is not None and {"timeout", "max_retries"} <= openai_kwargs


def test_round_trips_use_the_dedicated_executor_not_the_default_pool():
    """Arch's condition 2: the default pool is 5 workers on shared-cpu-1x and now also
    carries credential reads and the calendar's HTTP."""
    from services.llm import provider_bounds as pb

    assert pb.PROVIDER_EXECUTOR._max_workers >= 8
    assert pb.PROVIDER_EXECUTOR._thread_name_prefix == "llm-provider"
    assert 0 < pb.PROVIDER_TIMEOUT_SECONDS <= 120
    assert pb.PROVIDER_MAX_RETRIES <= 1


@pytest.mark.asyncio
async def test_anthropic_round_trip_runs_on_the_provider_executor_thread():
    client, rec = _anthropic_fake()
    model = next(m for m in mod.LLMModel if "claude" in m.value.lower())
    with patch("services.llm.request_key.anthropic_client_for_request", return_value=client):
        await _llm()._anthropic_complete("hello", _config(model))
    assert rec.thread is not None and rec.thread.name.startswith("llm-provider")
