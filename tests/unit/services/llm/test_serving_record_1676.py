"""#1676 — the SERVING provider/model is recorded, so a silent cross-provider
fallback can never change the instrument's identity without a trace.

SERVING_MODEL_RECORD (services/llm/clients.py) increments ONLY at a successful
_call_provider return — it records which provider+model actually answered, not
config-at-rest. The canonical-retest harness reads the per-run delta
(tests/e2e/test_canonical_conversations.py serving_llm_report fixture) and the
history CSV gets it as serving_provider/serving_model columns.

Test harness style mirrors test_provider_selection_1415.py (same file, same
_complete_raw layer).
"""

from collections import Counter
from unittest.mock import AsyncMock, patch

import pytest

from services.llm import clients as llm_clients
from services.llm.clients import SERVING_MODEL_RECORD, _record_serving


class _StubConfigService:
    def __init__(self):
        self.default_by_user = {"user-a": "anthropic", "user-b": "openai"}
        self.authorized_by_user = {"user-b": ["openai", "anthropic"]}

    def get_default_provider(self, user_id=None):
        return self.default_by_user.get(user_id, "openai")

    def get_configured_providers(self, user_id=None):
        return self.authorized_by_user.get(user_id, ["openai", "anthropic", "gemini"])


def _make_client(config_service):
    from services.llm.clients import LLMClient

    client = LLMClient.__new__(LLMClient)  # skip heavyweight __init__ (builds SDKs)
    client._config_service = config_service
    client._output_filter = None
    client.anthropic_client = object()
    client.openai_client = object()
    client.gemini_client = None
    return client


@pytest.fixture(autouse=True)
def _snapshot_record():
    """Isolate each test's view of the module-level Counter (delta-based, like
    the e2e harness reads it — never clear it, other code may be mid-run)."""
    before = Counter(SERVING_MODEL_RECORD)
    yield before
    # no cleanup: the record is append-only by design


def _delta(before):
    return Counter(SERVING_MODEL_RECORD) - before


def test_record_serving_increments_by_provider_model_key(_snapshot_record):
    _record_serving("anthropic", "claude-haiku-4-5")
    _record_serving("anthropic", "claude-haiku-4-5")
    _record_serving("openai", "gpt-4o")
    d = _delta(_snapshot_record)
    assert d["anthropic:claude-haiku-4-5"] == 2
    assert d["openai:gpt-4o"] == 1


@pytest.mark.asyncio
async def test_primary_success_records_serving_model(_snapshot_record):
    """A successful primary call records THAT provider+the resolved model id."""
    client = _make_client(_StubConfigService())

    with patch.object(type(client), "_call_provider", new=AsyncMock(return_value="ok")):
        await client._complete_raw("conversation", "hi", user_id="user-a")

    d = _delta(_snapshot_record)
    assert sum(d.values()) == 1
    (key,) = d.keys()
    provider, model = key.split(":", 1)
    assert provider == "anthropic"
    assert model, "model id must be non-empty"
    # the recorded id is the resolved wire id (resolve_model_alias), not the enum repr
    assert not model.startswith("LLMModel."), f"enum repr leaked into record: {model}"


@pytest.mark.asyncio
async def test_cross_provider_fallback_records_the_FALLBACK_model(_snapshot_record):
    """THE #1676 CONFOUND: primary (openai) fails, anthropic serves — the record
    must show anthropic's model, and no openai entry (openai never answered)."""
    client = _make_client(_StubConfigService())

    async def fake_call(provider, *a, **k):
        if provider.value == "openai":
            raise RuntimeError("credit_balance_exhausted")
        return "served-by-fallback"

    with patch.object(type(client), "_call_provider", new=AsyncMock(side_effect=fake_call)):
        out = await client._complete_raw("conversation", "hi", user_id="user-b")

    assert out == "served-by-fallback"
    d = _delta(_snapshot_record)
    assert sum(d.values()) == 1
    (key,) = d.keys()
    assert key.startswith("anthropic:"), f"fallback serve must be recorded as anthropic, got {key}"
    assert not any(k.startswith("openai:") for k in d), "failed primary must NOT be recorded"


@pytest.mark.asyncio
async def test_total_failure_records_nothing(_snapshot_record):
    """No successful serve -> no record (the record is serves, not attempts)."""
    client = _make_client(_StubConfigService())

    with patch.object(
        type(client), "_call_provider", new=AsyncMock(side_effect=RuntimeError("down"))
    ):
        with pytest.raises(RuntimeError, match="All configured LLM providers failed"):
            await client._complete_raw("conversation", "hi", user_id="user-b")

    assert sum(_delta(_snapshot_record).values()) == 0


def test_record_serving_never_raises():
    # observability must not break the call path, whatever it's handed
    _record_serving(None, None)  # type: ignore[arg-type]
