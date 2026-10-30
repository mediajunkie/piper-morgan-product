"""scripts/router_batch.py: render mirrors the live Anthropic router request; replay answers it."""

import importlib.util
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
_spec = importlib.util.spec_from_file_location("router_batch", ROOT / "scripts" / "router_batch.py")
rb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rb)


def test_render_builds_the_live_request(tmp_path):
    from services.intent_service.inversion_router import (
        _SYSTEM_PROMPT,
        build_routing_prompt,
        derive_routing_grammar,
    )

    out = tmp_path / "r.jsonl"
    rb._render(
        SimpleNamespace(
            label="main", samples=2, phrase=["show my todos"], corpus=False, out=str(out)
        )
    )
    rows = [json.loads(line) for line in out.read_text().splitlines()]
    assert [r["custom_id"] for r in rows] == ["main-0-1", "main-0-2"]
    p = rows[0]["params"]
    assert p["system"] == _SYSTEM_PROMPT
    assert p["messages"] == [
        {"role": "user", "content": build_routing_prompt("show my todos", derive_routing_grammar())}
    ]
    assert p["model"].startswith("claude-") and p["max_tokens"] > 0


@pytest.mark.asyncio
async def test_replay_answers_the_router_prompt_and_its_repair(tmp_path):
    from services.intent_service.inversion_router import (
        build_routing_prompt,
        derive_routing_grammar,
    )

    reqs = tmp_path / "q.jsonl"
    res = tmp_path / "s.jsonl"
    reqs.write_text(
        json.dumps({"custom_id": "c-0-1", "phrase": "show my todos", "params": {}}) + "\n"
    )
    res.write_text(
        json.dumps(
            {
                "custom_id": "c-0-1",
                "type": "succeeded",
                "text": '{"x":1}',
                "model": "claude-haiku-4-5",
            }
        )
        + "\n"
    )
    llm = rb.ReplayLLM(str(reqs), str(res))
    prompt = build_routing_prompt("show my todos", derive_routing_grammar())
    served = {}
    assert await llm.complete(task_type="t", prompt=prompt, served=served) == '{"x":1}'
    assert served == {"provider": "anthropic", "model": "claude-haiku-4-5"}
    repair = prompt + "\n\nYour previous reply was invalid: x."
    assert await llm.complete(task_type="t", prompt=repair) == '{"x":1}'
    with pytest.raises(RuntimeError):
        await llm.complete(task_type="t", prompt="User message: 'something else'")


def test_render_model_and_no_thinking_flags(tmp_path):
    """--model renders another model id on the same tree (temperature as served
    for that id); --no-thinking adds thinking=disabled. Harness only (Arch
    2026-10-30 15:20 item 4); neither flag touches the served router."""
    import json

    out = tmp_path / "r.jsonl"
    rb._render(
        SimpleNamespace(
            label="screen",
            samples=1,
            phrase=["show my todos"],
            corpus=False,
            out=str(out),
            model="claude-opus-4-8",
            no_thinking=True,
        )
    )
    rec = json.loads(out.read_text().splitlines()[0])
    assert rec["params"]["model"] == "claude-opus-4-8"
    assert "temperature" not in rec["params"]  # opus-4-8 is in MODELS_WITHOUT_TEMPERATURE
    assert rec["params"]["thinking"] == {"type": "disabled"}
    assert rec["custom_id"] == "screen-0-1"
