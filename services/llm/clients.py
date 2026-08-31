"""
LLM Client implementations
Handles connections to Anthropic, OpenAI, and Gemini.

Uses LLMConfigService for secure key management and validation.
"""

from collections import Counter
from typing import Any, Dict, Optional

import structlog
from anthropic import Anthropic
from openai import OpenAI

from services.config.llm_config_service import LLMConfigService

from .config import (
    MODEL_CONFIGS,
    MODELS_WITHOUT_TEMPERATURE,
    PROVIDER_MODELS,
    LLMModel,
    LLMProvider,
    resolve_model,
    resolve_model_alias,
)


def _build_temperature_kwarg(model_value: str, configured_temperature: float) -> Dict[str, float]:
    """Issue #1126: return `{}` if the model doesn't accept temperature.

    Anthropic deprecated `temperature` for extended-thinking models (e.g. the
    retired claude-opus-4-7; see MODEL_ALIASES in config.py). Returning an empty dict (instead of including the
    param) means the API gets a clean payload without the deprecated key.

    Returns:
        {"temperature": <value>} for models that support it; {} otherwise.
    """
    if model_value in MODELS_WITHOUT_TEMPERATURE:
        return {}
    return {"temperature": configured_temperature}


logger = structlog.get_logger()

# Fallback preference order — tried in sequence if the primary provider fails.
# Anthropic first (project default), Gemini second (added Apr 16), OpenAI last.
_FALLBACK_ORDER = [LLMProvider.ANTHROPIC, LLMProvider.GEMINI, LLMProvider.OPENAI]

# #1676 (the #1620 record-the-model discipline): per-process record of which
# provider+model ACTUALLY answered — incremented only at a SUCCESSFUL
# _call_provider return, so a silent cross-provider fallback is visible here,
# where config-at-rest is not. Keyed "provider:model" (e.g.
# "anthropic:claude-haiku-4-5"). In-process observability for harnesses that
# must report the serving LLM per run (canonical retest boots the app in-process
# via ASGITransport and reads the delta); NOT persisted, NOT per-user state.
SERVING_MODEL_RECORD: Counter = Counter()


def _record_serving(provider_value: str, model: str) -> None:
    """Record one successfully-served LLM call. Never raises (observability
    must not break the call path)."""
    try:
        SERVING_MODEL_RECORD[f"{provider_value}:{model}"] += 1
    except Exception:  # silent-ok: observability-only record; must never break the serving call path (#1676)
        pass


class LLMClient:
    """Base LLM client with common interface"""

    def __init__(self, output_filter: Optional[Any] = None):
        """
        Args:
            output_filter: optional OutputFilter for #1017 post-generation
                content filtering. If None (current default — Phase 2.2
                scaffold), complete() behaves as before. Container wiring
                will pass a configured OutputFilter once Phase 2.3 lands
                the durable audit envelope.
        """
        self.anthropic_client = None
        self.openai_client = None
        self.gemini_client = (
            None  # Gemini uses a per-call GenerativeModel; this flag tracks "configured"
        )
        self._config_service = LLMConfigService()
        # #1017 Phase 2.2: output filter wrapping. None-safe — existing
        # callers and tests that construct LLMClient() without arguments
        # continue to work; the filter applies only when an instance is
        # injected at construction.
        self._output_filter = output_filter
        # Note: per-call usage tracking lives in services/domain/llm_domain_service.py
        # (Issue #271). Earlier scaffolding here was never wired (no DB session in
        # synchronous context); removed Apr 28 per #1012 sweep.
        self._init_clients()

    @property
    def providers_initialized(self) -> bool:
        """Check if at least one LLM provider is initialized and available"""
        return (
            self.anthropic_client is not None
            or self.openai_client is not None
            or self.gemini_client is not None
        )

    def _init_clients(self):
        """Initialize API clients using LLMConfigService"""
        # Get configured providers from config service
        configured_providers = self._config_service.get_configured_providers()

        # Anthropic
        if "anthropic" in configured_providers:
            try:
                anthropic_key = self._config_service.get_api_key("anthropic")
                self.anthropic_client = Anthropic(api_key=anthropic_key)
                logger.info("Anthropic client initialized")
            except ValueError as e:
                logger.warning(f"Anthropic client initialization skipped: {e}")
        else:
            logger.warning("No ANTHROPIC_API_KEY configured")

        # OpenAI
        if "openai" in configured_providers:
            try:
                openai_key = self._config_service.get_api_key("openai")
                self.openai_client = OpenAI(api_key=openai_key)
                logger.info("OpenAI client initialized")
            except ValueError as e:
                logger.warning(f"OpenAI client initialization skipped: {e}")
        else:
            logger.warning("No OPENAI_API_KEY configured")

        # Gemini (added Apr 16, #950-adjacent)
        if "gemini" in configured_providers:
            try:
                import google.generativeai as genai

                gemini_key = self._config_service.get_api_key("gemini")
                genai.configure(api_key=gemini_key)
                # Gemini uses a per-call GenerativeModel rather than a stateless client.
                # We set this flag to True to signal "configured"; actual model instances
                # are constructed inside _gemini_complete as needed (cheap, supports
                # per-call system_instruction).
                self.gemini_client = True
                logger.info("Gemini client initialized")
            except (ValueError, ImportError) as e:
                logger.warning(f"Gemini client initialization skipped: {e}")
        else:
            logger.warning("No GEMINI_API_KEY configured")

    def set_output_filter(self, output_filter: Optional[Any]) -> None:
        """Attach (or replace) the OutputFilter post-construction.

        #1017 Phase 2.3: lets application startup wire the filter into
        the module-level `llm_client` singleton after BoundaryEnforcer
        and other dependencies are ready, without forcing eager
        construction at module-import time (which would break test
        contexts that import this module without a live DB/config).
        """
        self._output_filter = output_filter

    async def complete(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
        *,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        regenerate_on_violation: bool = True,
    ) -> str:
        """
        Get completion for a specific task type with automatic fallback.

        Issue #1017 Phase 2.2: when an `output_filter` was injected at
        construction, the LLM response passes through it. PII matches
        get redacted in place; secret-format matches get redacted with
        high severity; BoundaryEnforcer category violations trigger
        regenerate-then-canned-substitute (one retry max) when
        `regenerate_on_violation` is True.

        Args:
            task_type: Type of task (intent_classification, reasoning, etc)
            prompt: The prompt to send
            context: Optional context to include
            response_format: Optional response format (for JSON mode)
            system: Optional system prompt
            user_id, session_id: optional context for the OutputFilter
                audit envelope (#1017). Passed through to filter; ignored
                when no filter is configured.
            regenerate_on_violation: if True (default) and a Tier 2
                BoundaryEnforcer category violation fires, the LLM call
                retries once before surfacing the canned substitute to
                the user. Set False for semantically single-shot calls
                (audit log entries, idempotent operations).

        Returns:
            The LLM's response, post-filter.
        """
        raw_response = await self._complete_raw(
            task_type=task_type,
            prompt=prompt,
            context=context,
            response_format=response_format,
            system=system,
            # #1415: identity reaches provider SELECTION, not just the filter.
            user_id=user_id,
        )

        # #1017 Phase 2.2: filter wrap. Skips entirely when no filter injected
        # (backward compat for existing tests + standalone uses).
        if self._output_filter is None:
            return raw_response

        return await self._apply_output_filter(
            raw_response=raw_response,
            task_type=task_type,
            prompt=prompt,
            context=context,
            response_format=response_format,
            system=system,
            user_id=user_id,
            session_id=session_id,
            regenerate_on_violation=regenerate_on_violation,
        )

    async def _apply_output_filter(
        self,
        raw_response: str,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]],
        response_format: Optional[Dict[str, Any]],
        system: Optional[str],
        user_id: Optional[str],
        session_id: Optional[str],
        regenerate_on_violation: bool,
    ) -> str:
        """Run the output filter; handle regenerate-on-violation retry."""
        first = await self._output_filter.filter(
            content=raw_response,
            task_type=task_type,
            user_id=user_id,
            session_id=session_id,
            attempt_number=1,
            prior_attempt_decision_id=None,
        )

        await self._log_output_filter_decision(first.decision)

        if not first.is_violation:
            return first.filtered_content

        # Boundary-category violation. Try to regenerate before surfacing
        # the canned response — most LLM-output filter trips are
        # non-deterministic; same input regenerated often passes cleanly.
        if not regenerate_on_violation:
            return first.filtered_content  # canned substitute

        retry_response = await self._complete_raw(
            task_type=task_type,
            prompt=prompt,
            context=context,
            response_format=response_format,
            system=system,
            user_id=user_id,  # #1415: retry uses the same per-user selection
        )
        second = await self._output_filter.filter(
            content=retry_response,
            task_type=task_type,
            user_id=user_id,
            session_id=session_id,
            attempt_number=2,
            prior_attempt_decision_id=first.decision.decision_id,
        )
        await self._log_output_filter_decision(second.decision)

        if not second.is_violation:
            return second.filtered_content

        # Retry also failed — surface the canned substitute.
        return second.filtered_content

    async def _log_output_filter_decision(self, decision) -> None:
        """Persist an OutputFilterDecision via the audit envelope.

        #1017 Phase 2.3: durable audit envelope. Wraps
        `audit_transparency.log_output_filter_decision` in a try/except so
        audit-write failure can't break the LLM call (matches the
        per-call session_scope transaction-boundary semantic of the
        underlying function).
        """
        try:
            from services.ethics.audit_transparency import audit_transparency

            await audit_transparency.log_output_filter_decision(decision)
        except Exception as exc:  # pragma: no cover — defensive
            logger.warning(
                "output_filter_audit_log_failed",
                error=str(exc),
                decision_id=getattr(decision, "decision_id", "unknown"),
            )

    async def _complete_raw(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None,
        response_format: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> str:
        """Underlying provider-call path (extracted from complete() in #1017
        Phase 2.2 so that the output-filter wrap can call the raw path
        twice during the regenerate-on-violation retry flow).

        Returns the raw LLM response text before filtering.
        """
        task_config = MODEL_CONFIGS.get(task_type, MODEL_CONFIGS["reasoning"])

        # Resolve primary provider for the ACTING PRINCIPAL (#1415). The old
        # code read the GLOBAL default_llm_provider keychain slot right here —
        # one user's setup pinned every user's provider, and a second user's
        # per-user key (#1185) was un-selectable (2026-07-16 incident). The
        # config service now resolves per-user choice -> server choice -> env
        # default, consent-filtered (#946) and fail-closed (F1).
        try:
            default_provider_name = self._config_service.get_default_provider(user_id)
            primary_provider = LLMProvider(default_provider_name)
        except (ValueError, Exception):
            # Fall back to whichever client is initialized
            if self.anthropic_client:
                primary_provider = LLMProvider.ANTHROPIC
            elif self.gemini_client:
                primary_provider = LLMProvider.GEMINI
            elif self.openai_client:
                primary_provider = LLMProvider.OPENAI
            else:
                raise RuntimeError("No LLM providers configured. Add an API key in Settings.")

        # Build runtime config with correct model for this provider
        config = {
            **task_config,
            "provider": primary_provider,
            "model": resolve_model(primary_provider, task_type),
        }

        # Try primary provider first
        try:
            result = await self._call_provider(
                primary_provider, prompt, config, response_format, context, system
            )
            # #1676: record the SERVING provider+model (success only).
            # resolve_model_alias(...) is the exact id the provider call sends.
            _record_serving(primary_provider.value, resolve_model_alias(config["model"].value))
            return result
        except Exception as e:
            logger.warning(
                "llm_primary_failed",
                provider=primary_provider.value,
                task_type=task_type,
                error=str(e),
            )

            # Try each other configured provider in the fallback order (Apr 16: Gemini added)
            # #1415: the fallback set respects the acting user's consent list —
            # resilience never overrides #946 (a de-authorized provider must not
            # process the user's message even when everything else is down).
            try:
                user_authorized = set(self._config_service.get_configured_providers(user_id))
            except Exception as consent_err:  # silent-ok: consent unknown -> no cross-provider fallback (fail closed); the primary error below still surfaces honestly (#1415)
                logger.warning(f"fallback_consent_check_failed: {consent_err}")
                user_authorized = set()
            fallback_errors: list[str] = [f"{primary_provider.value}: {e}"]
            for fallback_provider in _FALLBACK_ORDER:
                if fallback_provider == primary_provider:
                    continue
                if not self._is_provider_configured(fallback_provider):
                    continue
                if fallback_provider.value not in user_authorized:
                    continue

                fallback_config = {
                    **task_config,
                    "provider": fallback_provider,
                    "model": resolve_model(fallback_provider, task_type),
                }

                logger.info(f"Falling back to {fallback_provider.value}")

                try:
                    result = await self._call_provider(
                        fallback_provider,
                        prompt,
                        fallback_config,
                        response_format,
                        context,
                        system,
                    )
                    # #1676: a cross-provider fallback CHANGES the serving model —
                    # record it so the instrument's identity is never silent.
                    _record_serving(
                        fallback_provider.value,
                        resolve_model_alias(fallback_config["model"].value),
                    )
                    return result
                except Exception as fallback_error:
                    logger.warning(
                        f"Fallback provider {fallback_provider.value} failed: {fallback_error}"
                    )
                    fallback_errors.append(f"{fallback_provider.value}: {fallback_error}")
                    continue

            # No fallback succeeded
            logger.error(f"All LLM providers failed: {fallback_errors}")
            raise RuntimeError(
                f"All configured LLM providers failed. Details: {'; '.join(fallback_errors)}"
            )

    def _is_provider_configured(self, provider: LLMProvider) -> bool:
        """Return True if the given provider has a live client / configured flag."""
        if provider == LLMProvider.ANTHROPIC:
            return self.anthropic_client is not None
        if provider == LLMProvider.OPENAI:
            return self.openai_client is not None
        if provider == LLMProvider.GEMINI:
            return bool(self.gemini_client)
        return False

    async def _call_provider(
        self,
        provider: LLMProvider,
        prompt: str,
        config: Dict[str, Any],
        response_format=None,
        context=None,
        system=None,
    ) -> str:
        """Route to the appropriate provider's completion method."""
        if provider == LLMProvider.ANTHROPIC:
            return await self._anthropic_complete(prompt, config, response_format, context, system)
        elif provider == LLMProvider.OPENAI:
            return await self._openai_complete(prompt, config, response_format, context, system)
        elif provider == LLMProvider.GEMINI:
            return await self._gemini_complete(prompt, config, response_format, context, system)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    async def _anthropic_complete(
        self,
        prompt: str,
        config: Dict[str, Any],
        response_format: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
    ) -> str:
        """Get completion from Anthropic"""
        # #1162 BYOC: use the request's user-supplied key (if one was bound at the
        # /api/v1/intent route) instead of the server's configured client; falls back
        # to the server client when absent. The key is never logged here.
        from services.llm.request_key import anthropic_client_for_request

        client = anthropic_client_for_request(self.anthropic_client)
        if not client:
            raise RuntimeError("Anthropic client not initialized")

        # Build request parameters
        # Issue #1126: temperature is conditional — some Anthropic extended-thinking
        # models reject it as deprecated (model IDs alias-resolved via MODEL_ALIASES).
        request_params = {
            "model": resolve_model_alias(config["model"].value),
            "max_tokens": config["max_tokens"],
            **_build_temperature_kwarg(config["model"].value, config["temperature"]),
            "messages": [{"role": "user", "content": prompt}],
        }

        # Add system prompt if provided
        if system:
            request_params["system"] = system

        # Note: Anthropic doesn't support response_format like OpenAI
        # JSON mode must be handled via prompt engineering
        response = client.messages.create(**request_params)

        # Extract actual token counts from response
        prompt_tokens = (
            response.usage.input_tokens if hasattr(response, "usage") else len(prompt) // 4
        )
        completion_tokens = (
            response.usage.output_tokens
            if hasattr(response, "usage")
            else len(response.content[0].text) // 4
        )

        # Log usage - non-blocking
        try:
            # Note: We don't have DB session here in synchronous context
            # Usage tracking will need to be handled at a higher level with DB session
            logger.info(
                "llm_usage",
                provider="anthropic",
                model=config["model"].value,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception as e:
            logger.warning(f"Failed to log usage: {e}")

        return response.content[0].text

    async def _openai_complete(
        self,
        prompt: str,
        config: Dict[str, Any],
        response_format: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
    ) -> str:
        """Get completion from OpenAI"""
        if not self.openai_client:
            raise RuntimeError("OpenAI client not initialized")

        # Build messages list
        messages = []

        # Add system message if provided
        if system:
            messages.append({"role": "system", "content": system})

        # Add user message
        messages.append({"role": "user", "content": prompt})

        # Prepare request parameters
        # Issue #1126: defensive — apply same temperature-deprecation guard
        # across providers (OpenAI doesn't currently have this issue but the
        # guard is cheap and provider-agnostic).
        request_params = {
            "model": resolve_model_alias(config["model"].value),
            "max_tokens": config["max_tokens"],
            **_build_temperature_kwarg(config["model"].value, config["temperature"]),
            "messages": messages,
        }

        # Add response_format if provided (for JSON mode)
        if response_format:
            request_params["response_format"] = response_format

        response = self.openai_client.chat.completions.create(**request_params)

        # Extract actual token counts from response
        prompt_tokens = (
            response.usage.prompt_tokens if hasattr(response, "usage") else len(prompt) // 4
        )
        completion_tokens = (
            response.usage.completion_tokens
            if hasattr(response, "usage")
            else len(response.choices[0].message.content) // 4
        )

        # Log usage - non-blocking
        try:
            # Note: We don't have DB session here in synchronous context
            # Usage tracking will need to be handled at a higher level with DB session
            logger.info(
                "llm_usage",
                provider="openai",
                model=config["model"].value,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception as e:
            logger.warning(f"Failed to log usage: {e}")

        return response.choices[0].message.content

    async def _gemini_complete(
        self,
        prompt: str,
        config: Dict[str, Any],
        response_format: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
        system: Optional[str] = None,
    ) -> str:
        """Get completion from Google Gemini.

        Constructs a per-call GenerativeModel so that system_instruction can vary
        per request (Gemini 1.5+ sets system_instruction at model-init time rather
        than per-call). Object creation is cheap relative to the HTTP round trip.

        response_format handling (#988): when the caller passes
        {"type": "json_object"} (matching OpenAI's convention), Gemini's
        response_mime_type is set to 'application/json' so the model returns
        structured JSON rather than prose. Without this, Gemini often returns
        natural-language text where the classifier expects JSON, causing
        downstream ValueError on parse.
        """
        if not self.gemini_client:
            raise RuntimeError("Gemini client not initialized")

        import google.generativeai as genai

        model_name = resolve_model_alias(config["model"].value)
        model_kwargs: Dict[str, Any] = {"model_name": model_name}
        if system:
            model_kwargs["system_instruction"] = system

        model = genai.GenerativeModel(**model_kwargs)

        # #988: translate OpenAI-convention response_format to Gemini's native flag
        # Issue #1126: defensive — apply same temperature-deprecation guard
        # across providers. Gemini currently accepts temperature universally
        # but the guard is cheap to apply.
        gen_config_kwargs: Dict[str, Any] = {
            "max_output_tokens": config["max_tokens"],
            **_build_temperature_kwarg(config["model"].value, config["temperature"]),
        }
        if response_format and response_format.get("type") == "json_object":
            gen_config_kwargs["response_mime_type"] = "application/json"

        generation_config = genai.types.GenerationConfig(**gen_config_kwargs)

        response = await model.generate_content_async(
            prompt,
            generation_config=generation_config,
        )

        # Extract token counts from usage_metadata if available
        try:
            prompt_tokens = response.usage_metadata.prompt_token_count
            completion_tokens = response.usage_metadata.candidates_token_count
        except AttributeError:
            prompt_tokens = len(prompt) // 4
            completion_tokens = len(response.text) // 4 if hasattr(response, "text") else 0

        try:
            logger.info(
                "llm_usage",
                provider="gemini",
                model=model_name,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
        except Exception as e:
            logger.warning(f"Failed to log usage: {e}")

        return response.text


# Global client instance
llm_client = LLMClient()
