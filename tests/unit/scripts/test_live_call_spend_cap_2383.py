"""#2383: a seat's paid live-call run states a dollar cap before its first call and
cannot pass it (ADR-084 D2, "one cap enforcer").

The stand-in client below is the only "provider" here. No test sends anything, and
every key is a made-up string.
"""

import asyncio
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import dev_key_binding as binder  # noqa: E402

from services.llm import spend_cap  # noqa: E402
from services.llm.clients import LLMClient  # noqa: E402
from services.llm.config import LLMModel  # noqa: E402

HAIKU = {"model": LLMModel.CLAUDE_HAIKU, "max_tokens": 1000, "temperature": 0.0}


class _StandInAnthropic:
    """Counts what is sent and answers with fixed token counts."""

    def __init__(self, input_tokens=100_000, output_tokens=1_000, usage=True, fail=False):
        self.sent = 0
        self._usage = (
            SimpleNamespace(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cache_creation_input_tokens=0,
                cache_read_input_tokens=0,
            )
            if usage
            else None
        )
        self._fail = fail
        self.messages = SimpleNamespace(create=self._create)

    def _create(self, **params):
        self.sent += 1
        if self._fail:
            raise RuntimeError("stand-in provider error")
        response = SimpleNamespace(content=[SimpleNamespace(type="text", text="ok")])
        if self._usage is not None:
            response.usage = self._usage
        return response


@pytest.fixture
def stand_in(monkeypatch):
    def _install(**kwargs):
        client = _StandInAnthropic(**kwargs)
        import services.llm.request_key as request_key

        monkeypatch.setattr(request_key, "anthropic_client_for_request", lambda: client)
        return client

    return _install


@pytest.fixture
def bound_env(monkeypatch):
    monkeypatch.setenv("PIPER_CREDENTIAL_STORE", "db")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-env-anthropic")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)


def _call(prompt="x" * 30):
    client = LLMClient.__new__(LLMClient)
    return asyncio.run(client._anthropic_complete(prompt, HAIKU))


# --- the binder refuses to start without a cap ------------------------------------


def test_no_cap_refuses_before_any_call_and_before_any_key_lookup(bound_env, stand_in):
    client = stand_in()
    with pytest.raises(SystemExit) as exc:
        with binder.developer_keys_bound(providers=("anthropic",)):
            pytest.fail("the block ran")
    assert "--max-usd" in str(exc.value) and "Refusing before the first call" in str(exc.value)
    assert client.sent == 0


@pytest.mark.parametrize("bad", (0, -1.0, True, "2"))
def test_a_cap_that_is_not_a_positive_number_refuses(bound_env, bad):
    with pytest.raises(SystemExit):
        with binder.developer_keys_bound(providers=("anthropic",), max_usd=bad):
            pytest.fail("the block ran")


def test_a_dry_run_needs_no_cap_and_binds_none(bound_env):
    with binder.developer_keys_bound(providers=(), require=False) as keys:
        assert keys == {}
        assert spend_cap.current_cap() is None


# --- the running total at the chokepoint ------------------------------------------


def test_a_run_that_reaches_its_cap_has_its_next_call_refused_and_nothing_more_sent(
    bound_env, stand_in, capsys
):
    # Each call measures 100,000 input and 1,000 output tokens on Haiku 4.5:
    # $0.10 + $0.005 = $0.105. The upper estimate of a 30-character prompt with
    # max_tokens 1000 is about $0.005. After two calls $0.21 is counted, so a $0.212 cap
    # takes two calls and refuses the third.
    client = stand_in()
    with pytest.raises(SystemExit) as exit_info:
        with binder.developer_keys_bound(providers=("anthropic",), max_usd=0.212, planned_calls=3):
            assert _call() == "ok"
            assert _call() == "ok"
            with pytest.raises(spend_cap.SpendCapReached) as exc:
                _call()
            assert "Nothing was sent" in str(exc.value)
            with pytest.raises(spend_cap.SpendCapReached):
                _call()
    assert client.sent == 2
    assert "2 calls were refused and not sent" in str(exit_info.value)
    out = capsys.readouterr().out
    assert out.index("PLANNED: 3 model calls on anthropic. Cap $0.21.") < out.index("COST:")


def test_the_cost_line_matches_the_stand_ins_token_counts(bound_env, stand_in, capsys):
    stand_in(input_tokens=200_000, output_tokens=10_000)
    with binder.developer_keys_bound(providers=("anthropic",), max_usd=5.0):
        _call()
        _call()
    line = [ln for ln in capsys.readouterr().out.splitlines() if ln.startswith("COST:")][0]
    # 2 x (200,000 x $1 + 10,000 x $5) / 1,000,000 = 2 x $0.25
    assert "COST: $0.5000 from the provider's token counts" in line
    assert "(2 calls, 400000 input and 20000 output tokens)" in line
    assert "against the $5.00 cap" in line


def test_cache_tokens_are_counted_at_their_own_rates():
    cost = spend_cap.usage_usd(
        "claude-haiku-4-5-20251001",
        {
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_creation_input_tokens": 1_000_000,
            "cache_read_input_tokens": 1_000_000,
        },
    )
    assert cost == pytest.approx(1.25 + 0.10)


def test_a_call_that_fails_keeps_its_upper_estimate_on_the_total(bound_env, stand_in, capsys):
    stand_in(fail=True)
    with binder.developer_keys_bound(providers=("anthropic",), max_usd=1.0):
        with pytest.raises(RuntimeError):
            _call()
        cap = spend_cap.current_cap()
        assert cap.reserved_usd == 0
        assert cap.estimated_usd == pytest.approx(spend_cap.upper_usd("claude-haiku-4-5", 30, 1000))
    assert "returned no token counts" in capsys.readouterr().out


def test_a_response_with_no_usage_is_counted_at_its_upper_estimate(bound_env, stand_in):
    stand_in(usage=False)
    with binder.developer_keys_bound(providers=("anthropic",), max_usd=1.0):
        _call()
        cap = spend_cap.current_cap()
        assert cap.measured_usd == 0 and cap.unmeasured_calls == 1 and cap.estimated_usd > 0


def test_a_model_with_no_price_row_is_refused_and_not_sent(bound_env, stand_in):
    client = stand_in()
    with pytest.raises(SystemExit):
        with binder.developer_keys_bound(providers=("anthropic",), max_usd=1.0):
            with pytest.raises(spend_cap.SpendCapReached) as exc:
                asyncio.run(
                    LLMClient.__new__(LLMClient)._anthropic_complete(
                        "hello", {**HAIKU, "model": LLMModel.GPT4}
                    )
                )
    assert "no price recorded" in str(exc.value)
    assert client.sent == 0


def test_calls_in_flight_are_counted_so_two_cannot_pass_the_cap_together():
    cap = spend_cap.SpendCap(0.008)
    first = cap.reserve("claude-haiku-4-5", 30, 1000)  # about $0.005 held
    with pytest.raises(spend_cap.SpendCapReached):
        cap.reserve("claude-haiku-4-5", 30, 1000)
    assert cap.refused == 1 and cap.reserved_usd == pytest.approx(first.upper)
    cap.settle(first, {"input_tokens": 10, "output_tokens": 10})
    assert cap.reserved_usd == 0


def test_embeddings_are_refused_under_a_cap_and_untouched_without_one():
    spend_cap.refuse_uncounted("an OpenAI embedding call")
    with spend_cap.spend_cap(1.0):
        with pytest.raises(spend_cap.SpendCapUncounted):
            spend_cap.refuse_uncounted("an OpenAI embedding call")


# --- a refusal ends the run (Arch's first required change, 2026-11-16) --------------


def test_a_cap_refusal_passes_through_complete_and_no_other_provider_is_tried(
    bound_env, stand_in, monkeypatch
):
    # Both providers are bound and consented, so a fallback to OpenAI is open. Without
    # the pass-through, the refused Anthropic call would be answered by the stand-in
    # below: a different model, inside a screen.
    monkeypatch.setenv("OPENAI_API_KEY", "fake-env-openai")
    client = stand_in()
    llm = LLMClient()
    tried = []

    async def _openai(*args, **kwargs):
        tried.append("openai")
        return "answered by another provider"

    monkeypatch.setattr(llm, "_openai_complete", _openai)
    monkeypatch.setattr(
        llm._config_service, "get_default_provider", lambda user_id=None: "anthropic"
    )
    monkeypatch.setattr(
        llm._config_service,
        "get_configured_providers",
        lambda user_id=None: ["anthropic", "openai"],
    )
    with pytest.raises(SystemExit) as exit_info:
        with binder.developer_keys_bound(providers=("anthropic", "openai"), max_usd=0.000001):
            with pytest.raises(spend_cap.SpendCapReached):
                asyncio.run(llm.complete(task_type="intent_classification", prompt="hello"))
    assert client.sent == 0, "the refused call was sent"
    assert tried == [], "a cap refusal was treated as a provider failure and fell back"
    assert "stopped at its $0.00 cap" in str(exit_info.value)


def test_the_binder_exits_non_zero_when_a_refusal_was_swallowed_on_the_way(bound_env, stand_in):
    stand_in()
    with pytest.raises(SystemExit) as exit_info:
        with binder.developer_keys_bound(providers=("anthropic",), max_usd=0.000001):
            try:
                _call()
            except Exception:
                pass  # a script's own row handler swallowing the refusal
    message = str(exit_info.value)
    assert exit_info.value.code not in (0, None)
    assert "1 calls were refused and not sent" in message
    assert "do not count its rows" in message


def test_after_one_refusal_every_later_call_is_refused_too():
    cap = spend_cap.SpendCap(0.006)
    cap.settle(cap.reserve("claude-haiku-4-5", 30, 1000), {"input_tokens": 1, "output_tokens": 1})
    with pytest.raises(spend_cap.SpendCapReached):
        cap.reserve("claude-haiku-4-5", 30_000, 1000)  # too big for what is left
    with pytest.raises(spend_cap.SpendCapReached) as exc:
        cap.reserve("claude-haiku-4-5", 3, 1)  # would fit, but the run is over
    assert "the run is over" in str(exc.value)


# --- the ten-dollar figure (Arch's second required change) --------------------------

RELAY_ID = "01M7JBP51M70C9GGYZT9AEGEBX"  # the shape of a mail id; no approval is implied


def test_a_cap_above_ten_dollars_refuses_without_the_relay_id(bound_env, stand_in):
    client = stand_in()
    with pytest.raises(SystemExit) as exc:
        with binder.developer_keys_bound(providers=("anthropic",), max_usd=10.01):
            pytest.fail("the block ran")
    assert "--approved-by" in str(exc.value) and "$10.00" in str(exc.value)
    assert client.sent == 0


def test_ten_dollars_exactly_needs_no_approval(bound_env, stand_in, capsys):
    stand_in()
    with binder.developer_keys_bound(providers=("anthropic",), max_usd=10.0):
        pass
    assert "on approval" not in capsys.readouterr().out


def test_a_cap_above_ten_dollars_runs_with_the_relay_id_and_prints_it(bound_env, stand_in, capsys):
    stand_in()
    with binder.developer_keys_bound(
        providers=("anthropic",), max_usd=25.0, approved_by=RELAY_ID, planned_calls=4
    ):
        pass
    planned = [ln for ln in capsys.readouterr().out.splitlines() if ln.startswith("PLANNED:")][0]
    assert f"Cap $25.00. Above $10.00 on approval {RELAY_ID}." in planned


@pytest.mark.parametrize("bad", ("yes", "xian said ok", "01M7", ""))
def test_an_approval_that_is_not_a_mail_id_refuses(bound_env, bad):
    with pytest.raises(SystemExit):
        with binder.developer_keys_bound(providers=("anthropic",), max_usd=25.0, approved_by=bad):
            pytest.fail("the block ran")


def test_pop_approved_by_flag():
    argv = ["prog", "--approved-by", RELAY_ID, "x"]
    assert binder.pop_approved_by_flag(argv) == RELAY_ID and argv == ["prog", "x"]
    argv = ["prog", f"--approved-by={RELAY_ID}"]
    assert binder.pop_approved_by_flag(argv) == RELAY_ID and argv == ["prog"]
    assert binder.pop_approved_by_flag(["prog"]) is None


def test_every_binder_user_passes_the_approval_through():
    import ast

    for path in sorted(SCRIPTS.glob("*.py")):
        if path.name == "dev_key_binding.py":
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if (
                isinstance(node, ast.Call)
                and getattr(node.func, "id", "") == "developer_keys_bound"
            ):
                names = {kw.arg for kw in node.keywords}
                assert "approved_by" in names, f"{path.name}:{node.lineno} can't carry an approval"


# --- a served request is untouched --------------------------------------------------


def test_with_no_cap_bound_the_leg_sends_as_before(monkeypatch, stand_in):
    client = stand_in()
    assert spend_cap.current_cap() is None
    assert _call() == "ok"
    assert client.sent == 1
    assert spend_cap.reserve_call("a-model-with-no-price", 10, 10) is None


# --- every script passes a cap, and nothing prints a key -------------------------


def test_pop_max_usd_flag():
    argv = ["prog", "--max-usd", "2.5", "out.md"]
    assert binder.pop_max_usd_flag(argv) == 2.5 and argv == ["prog", "out.md"]
    argv = ["prog", "--max-usd=3"]
    assert binder.pop_max_usd_flag(argv) == 3.0 and argv == ["prog"]
    assert binder.pop_max_usd_flag(["prog"]) is None
    with pytest.raises(SystemExit):
        binder.pop_max_usd_flag(["prog", "--max-usd", "lots"])


def test_every_binder_user_passes_a_cap():
    import ast

    seen = 0
    for path in sorted(SCRIPTS.glob("*.py")):
        if path.name == "dev_key_binding.py":
            continue
        for node in ast.walk(ast.parse(path.read_text())):
            if (
                isinstance(node, ast.Call)
                and getattr(node.func, "id", "") == "developer_keys_bound"
            ):
                seen += 1
                names = {kw.arg for kw in node.keywords}
                assert "max_usd" in names, f"{path.name}:{node.lineno} passes no cap"
    assert seen >= 10


def test_the_lines_never_carry_the_key(bound_env, stand_in, capsys):
    stand_in()
    with binder.developer_keys_bound(providers=("anthropic",), max_usd=1.0):
        _call()
    assert "fake-env-anthropic" not in capsys.readouterr().out
    for name in ("dev_key_binding.py",):
        src = (SCRIPTS / name).read_text()
        assert "os.environ)" not in src and "print(keys" not in src
