# LLM Configuration Architecture

**Component**: LLM Configuration & Provider Management
**Status**: Production
**Version**: 3.0 (Post-M1, Provider-Agnostic)
**Last Updated**: 2026-04-11

---

## Changelog

- **2026-04-11 (v3.0)**: Rewrote to reflect #940 provider-agnostic refactor
  (commits `c2bdb772`, `b6033c02`). Removed `ProviderSelector` / task-based
  provider pinning. Documented `model_tier` system, `resolve_model()`,
  setup wizard single-provider selection (#946), and floor error
  classification (#940). `provider_selector.py` still exists in the tree
  but is no longer on the `LLMClient.complete()` path.
- **2025-10-09 (v2.0)**: DDD refactor with `LLMDomainService` mediation
  and `ProviderSelector` for task-based provider choice. Superseded.

---

## Overview

Piper Morgan's LLM layer is **provider-agnostic at the task level**: task
configs (intent classification, reasoning, code generation, conversation,
etc.) declare a `model_tier` ("default" or "heavy") rather than a specific
provider. The provider is resolved at call time from the user's setup choice,
with automatic fallback to the other provider if the primary fails.

This replaced an earlier system where each task type was pinned to a
specific provider (e.g., code_generation -> OpenAI, reasoning -> Anthropic).
Pinning caused UAT failures when the pinned provider was unavailable, had a
deprecated model, or was not the one the user had configured.

---

## Core Data Shapes

### `services/llm/config.py`

```python
class LLMProvider(Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    GEMINI = "gemini"            # Defined but not wired end-to-end
    PERPLEXITY = "perplexity"    # Defined but not wired end-to-end

class LLMModel(Enum):
    CLAUDE_SONNET = "claude-sonnet-4-20250514"
    CLAUDE_OPUS   = "claude-sonnet-4-20250514"  # Alias until Opus 4 available
    GPT4          = "gpt-4o"
    GPT35         = "gpt-4o-mini"

PROVIDER_MODELS: Dict[str, Dict[str, LLMModel]] = {
    "anthropic": {
        "default": LLMModel.CLAUDE_SONNET,
        "heavy":   LLMModel.CLAUDE_OPUS,
    },
    "openai": {
        "default": LLMModel.GPT4,
        "heavy":   LLMModel.GPT4,
    },
}

MODEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "intent_classification":      {"model_tier": "default", ...},
    "reasoning":                  {"model_tier": "heavy",   ...},
    "code_generation":            {"model_tier": "default", ...},
    "github_content_generation":  {"model_tier": "heavy",   ...},
    "conversation":               {"model_tier": "default", ...},
}
```

**Key invariant**: `MODEL_CONFIGS` contains **no provider field**. The
provider is always resolved at runtime.

### `resolve_model(provider, task_type)`

```python
def resolve_model(provider: LLMProvider, task_type: str) -> LLMModel:
    config = MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])
    tier = config.get("model_tier", "default")
    provider_models = PROVIDER_MODELS.get(provider.value, PROVIDER_MODELS["openai"])
    return provider_models.get(tier, provider_models["default"])
```

This is the single resolution function. Call `resolve_model(provider, task)`
and you get the concrete model enum value for that provider/tier combo.

---

## Request Flow: `LLMClient.complete()`

**Location**: `services/llm/clients.py` line 64

Flow for a call like `await llm.complete(task_type="conversation", prompt=...)`:

```
1. Pick task_config from MODEL_CONFIGS[task_type]
      (task_config has model_tier, temperature, max_tokens; NO provider)

2. Determine primary provider (this is the new part):
   a. Read 'default_llm_provider' from the macOS keychain.
      This is the user's explicit setup choice (#946).
   b. If not set -> LLMConfigService.get_default_provider()
      which itself tries keychain again, then PIPER_DEFAULT_PROVIDER
      env var, then first-available-provider.
   c. If all else fails -> use whichever client initialized
      successfully (anthropic_client or openai_client).
   d. If neither initialized -> RuntimeError
      "No LLM providers configured. Add an API key in Settings."

3. Build runtime config:
      config = {**task_config,
                "provider": primary_provider,
                "model": resolve_model(primary_provider, task_type)}

4. Call _call_provider(primary_provider, ...)
      Dispatches to _anthropic_complete or _openai_complete.

5. On primary failure:
      Fallback provider = the other provider (Anthropic <-> OpenAI).
      If that client is initialized, retry with a fresh
      resolve_model(fallback, task_type). Otherwise raise.

6. On fallback failure:
      Raise RuntimeError with both error messages.
```

**Anthropic quirk**: Anthropic doesn't support OpenAI-style
`response_format` for JSON mode. Callers needing JSON output must handle
mode via prompt engineering (noted in `_anthropic_complete`).

---

## Provider Configuration (Setup Wizard)

**Change from v2.0**: The setup wizard no longer asks for multiple keys
or excluded providers. It asks the user to **pick one provider** (OpenAI
or Anthropic) and enter that one key.

**Storage** (`services/infrastructure/keychain_service.py`):
- `{provider}_api_key` — the API key itself, encrypted in macOS keychain
- `default_llm_provider` — the user's setup choice (`"openai"` or
  `"anthropic"`), stored as a pseudo-key

**Priority chain in `LLMConfigService.get_default_provider()`**
(line 281):

```
1. Keychain: 'default_llm_provider'                (user's setup choice, #946)
2. Env var: PIPER_DEFAULT_PROVIDER                 (if set and available)
3. First provider in get_available_providers()     (graceful fallback)
```

No provider is "required." If neither provider is configured, the floor
falls back to `FLOOR_FALLBACK_NO_PROVIDER` explaining how to add one.

---

## Client Initialization

`LLMClient.__init__()` calls `_init_clients()` which:
- Calls `LLMConfigService.get_configured_providers()` to see which
  providers have keys available (keychain first, env var fallback)
- Instantiates `Anthropic(api_key=...)` if "anthropic" is configured
- Instantiates `OpenAI(api_key=...)` if "openai" is configured
- Leaves the other client attribute as `None`

The `providers_initialized` property returns `True` if at least one
client object exists. The floor and other consumers check this before
assuming LLM calls will work.

---

## Floor Error Classification (#940)

**Location**: `services/intent_service/conversational_floor.py`
line 183 (`_classify_llm_error`)

When `ConversationalFloor.respond()` catches an exception from
`LLMClient.complete()`, it classifies the error into one of three
buckets and picks a matching user-facing fallback message:

| Classification | Triggers | Fallback Message |
|---|---|---|
| `no_provider` | "not configured" or "no llm provider" in error text | `FLOOR_FALLBACK_NO_PROVIDER` — "I don't have an LLM provider configured yet..." |
| `auth` | 401/403/unauthorized/forbidden, "invalid api key", "authentication", "not initialized", model-not-found, 404 | `FLOOR_FALLBACK_AUTH` — "I can't generate responses right now... check your LLM API key in Settings" |
| `transient` | everything else (timeouts, 500s, network errors) | `FLOOR_FALLBACK_TRANSIENT` — "I'm having trouble connecting to my reasoning engine right now... try again in a moment" |

Model-not-found and 404 are intentionally classified as `auth` rather than
`transient`: they almost always mean a config problem the user needs to fix.

---

## What Was Removed

### ProviderSelector (v2.0)

`services/llm/provider_selector.py` still exists in the tree and is still
instantiated by `LLMDomainService.initialize()` (line 94). However, it is
**not on the request path**: `LLMDomainService.complete()` delegates
directly to `LLMClient.complete()` (line 162), which uses the
keychain-first / env-fallback / first-available chain described above —
not the ProviderSelector's task-based routing.

Previously, ProviderSelector picked providers based on task type (e.g.,
coding tasks -> OpenAI, research -> Anthropic). That logic has been
superseded by:

1. The user's explicit setup choice in the keychain
2. `resolve_model(provider, task_type)` handling per-provider model choice
3. The automatic primary->fallback chain in `LLMClient.complete()`

The selector object is effectively dead code on the hot path. New code
should call `ServiceRegistry.get_llm().complete(task_type, prompt)` and
trust the resolution chain; don't pass provider hints.

### Task-type-to-provider pinning

Previous versions of `MODEL_CONFIGS` looked like:

```python
# OLD — DO NOT REINTRODUCE
MODEL_CONFIGS = {
    "reasoning": {"provider": "anthropic", "model": "claude-opus-4", ...},
    "code_generation": {"provider": "openai", "model": "gpt-4o", ...},
}
```

This caused #940: UAT sessions where a user with only an Anthropic key
would hit the `code_generation` task, which tried to call OpenAI, failed
with `not initialized`, and got a broken experience. The provider field
has been removed from every entry in `MODEL_CONFIGS`.

---

## Security Model

### Key Storage

- **Primary**: macOS Keychain (encrypted, OS-managed)
- **Migration**: Environment variables (still supported as fallback)
- **Never**: Plaintext config files

### Access Control

- Keys loaded once at `LLMClient._init_clients()` time
- Never logged or included in error messages sent to users
- `LLMConfigService` centralizes the keychain-first, env-var-fallback logic

### Rotating a Key

1. Generate new key at the provider
2. Open Settings UI and paste new key (or run
   `python scripts/migrate_keys_to_keychain.py`)
3. Restart the server so `_init_clients()` picks up the new key
4. Revoke the old key at the provider

---

## Related Documentation

- [intent-categories-reference.md](intent-categories-reference.md) —
  how the floor uses LLM calls
- [architecture.md](architecture.md) — system-wide context
- ADR-029: Domain Service Mediation (still current for the broader pattern)
- ADR-010: Configuration Management (Hybrid Access)

---

## Source Files

- `services/llm/config.py` — `MODEL_CONFIGS`, `PROVIDER_MODELS`, `resolve_model`
- `services/llm/clients.py` — `LLMClient.complete()` with fallback chain
- `services/config/llm_config_service.py` — `get_default_provider`, key retrieval
- `services/infrastructure/keychain_service.py` — secure storage
- `services/intent_service/conversational_floor.py` — `_classify_llm_error`,
  fallback constants
