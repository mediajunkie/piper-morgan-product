"""MODEL_ALIASES (PA proposal, Lead-approved 2026-06-12): deprecated model IDs
resolve to current equivalents at the request choke points; resolution warns."""

from services.llm.config import MODEL_ALIASES, resolve_model_alias


def test_deprecated_ids_resolve():
    for old, new in MODEL_ALIASES.items():
        assert resolve_model_alias(old) == new


def test_current_ids_pass_through():
    assert resolve_model_alias("claude-opus-4-8") == "claude-opus-4-8"
    assert resolve_model_alias("totally-unknown-model") == "totally-unknown-model"


def test_clients_wired_through_alias_resolver():
    # The three request-construction sites must route model IDs through the
    # alias resolver (anthropic + openai request_params, gemini model_name).
    src = open("services/llm/clients.py").read()
    assert src.count('resolve_model_alias(config["model"].value)') == 3
