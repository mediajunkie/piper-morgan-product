# Design Note: Wire Gemini into LLMClient (#980-adjacent hygiene)

**Date**: 2026-04-16
**Author**: Lead Dev
**Status**: In progress

## Problem

`services/llm/clients.py:_call_provider` only routes to Anthropic or OpenAI. Gemini is defined in the `LLMProvider` enum (`services/llm/config.py:13`) and validated in `LLMConfigService._validate_gemini`, but the main completion path raises `ValueError("Unsupported provider: gemini")` if the user's `default_llm_provider` is set to `"gemini"`.

Effect: "switch to Gemini for diversity / cost / resilience" is not actually available as a user option despite the enum suggesting it is. The #971 Pattern-012 adapter deletion cleaned out an old GeminiAdapter that had the SDK integration but was dead code — so the usage pattern is known from history.

## Scope

**In**: Make Gemini a real primary/fallback provider for the floor + all other `LLMClient.complete()` call sites. Same contract as Anthropic/OpenAI.

**Out**:
- Streaming (no existing provider streams)
- Response format / JSON mode (Anthropic doesn't do it either; handled via prompt engineering)
- Tuning which tasks Gemini is best for (treat as commodity replacement)
- Making Gemini the default (user choice via keychain setting stays as-is)

## Changes

1. `services/llm/config.py`:
   - Add `LLMModel.GEMINI_FLASH = "gemini-2.5-flash"` and `LLMModel.GEMINI_PRO = "gemini-2.5-pro"` (matches AAXT usage verified Apr 15)
   - Extend `PROVIDER_MODELS` with `"gemini": {"default": GEMINI_FLASH, "heavy": GEMINI_PRO}`

2. `services/llm/clients.py`:
   - Import `google.generativeai as genai` (already in requirements at `google-generativeai==0.8.6`)
   - Add `self.gemini_client` to `__init__`; initialize when `gemini` in `configured_providers`
   - Store model-per-instance pattern: genai uses `GenerativeModel(model_name)` not a stateless client, so cache models by name
   - Update `providers_initialized` property to include Gemini
   - Add `_gemini_complete(prompt, config, response_format, context, system)` matching the Anthropic signature
   - Update `_call_provider` dispatch table
   - Update fallback selection — currently hardcoded 2-way swap (Anthropic↔OpenAI). Move to ordered preference list: if primary fails, try the next configured provider in order `[ANTHROPIC, GEMINI, OPENAI]` (Anthropic first per project default, Gemini second, OpenAI last)
   - Usage logging: Gemini response has `usage_metadata.prompt_token_count` / `candidates_token_count`; match the existing log shape

3. Tests at `tests/unit/services/llm/test_clients_gemini.py`:
   - `test_gemini_client_initialized_when_configured` — mock config service, verify client exists
   - `test_gemini_client_skipped_when_not_configured` — no Gemini key → client is None
   - `test_gemini_complete_success` — mock genai model, verify completion returns expected text
   - `test_gemini_complete_with_system_prompt` — verify system passed via `system_instruction`
   - `test_gemini_complete_raises_when_not_initialized` — unconfigured → RuntimeError
   - `test_call_provider_routes_gemini` — end-to-end dispatch
   - `test_fallback_uses_gemini_when_anthropic_fails` — primary anthropic fails, gemini configured, gemini used as fallback

## Design Choices

- **Model caching in the instance**: genai creates a new `GenerativeModel` per model-name. I'll cache models by `model_name` on the instance. For this project with only 2 Gemini models (flash + pro), it's effectively O(1).
- **System prompts via `system_instruction`**: Gemini 1.5+ supports it at model-init time. Re-instantiate `GenerativeModel` per call if system differs. Trade-off: small object-creation cost vs. clean separation. Accept the cost.
- **Fallback order**: Anthropic → Gemini → OpenAI. Rationale: matches Apr 15 AAXT verification where Anthropic was primary, Gemini was judge (working when OpenAI hit quota).
- **API key source**: existing `LLMConfigService.get_api_key("gemini")` already works (validated in `_validate_gemini`). No new config surface.
- **No adapter revival**: the deleted Pattern-012 `GeminiAdapter` had the same SDK pattern. Don't resurrect it — inline the two methods into `LLMClient` following the Anthropic/OpenAI convention. Per Architect's decision on #971: "don't maintain infrastructure for a future that hasn't been designed yet."

## Risks

| Risk | Mitigation |
|------|-----------|
| `google-generativeai==0.8.6` API differs from what I implement | Run the failing test, confirm with real SDK call |
| Fallback ordering changes break existing tests that assumed hardcoded 2-way | Check `test_llm_clients*` for assumptions; update if needed |
| Gemini rate limits differ from expected | Out of scope for this change; failure becomes fallback trigger |
| Usage tracker schema doesn't accommodate Gemini token counts | Same log format; should Just Work |

## Non-goals for this session

- Changing the **default** provider (stays as user's keychain choice — Anthropic currently)
- Tuning Gemini-specific temperature/max_tokens per task type (uses same `MODEL_CONFIGS` via `resolve_model`)
- Adding a "provider preference order" config surface (current hardcoded order is fine)
