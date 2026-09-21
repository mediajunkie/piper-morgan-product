"""
LLM Client implementations
Handles connections to Anthropic, OpenAI, and Gemini.

Uses LLMConfigService for secure key management and validation.
"""

from collections import Counter
from typing import Any, Dict, Optional

import structlog
from openai import OpenAI

from services.config.llm_config_service import LLMConfigService
from services.llm.request_key import LLMKeyRequiredError

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
    except (
        Exception
    ):  # silent-ok: observability-only record; must never break the serving call path (#1676)
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
        # #1812 steps 5–6 (2026-09-21): the server's own long-lived clients
        # (`self.anthropic_client` / `self.openai_client` / `self.gemini_client`)
        # and `_init_clients` are AMPUTATED, not made lazy. Their last consumer was
        # the designated-operator seam (#1807), deleted with the seam itself: every
        # leg now builds a fresh per-request client from the acting user's bound key
        # via `request_spend_key`, or refuses (`UnboundLLMKeyError`). Constructing
        # this class therefore reads NO credential from any store — which also
        # discharges the import-time-singleton hazard (`llm_client` below) at the
        # root: there is no key state left to construct eagerly.
        self._config_service = LLMConfigService()
        # #1017 Phase 2.2: output filter wrapping. None-safe — existing
        # callers and tests that construct LLMClient() without arguments
        # continue to work; the filter applies only when an instance is
        # injected at construction.
        self._output_filter = output_filter
        # Note: per-call usage tracking lives in services/domain/llm_domain_service.py
        # (Issue #271). Earlier scaffolding here was never wired (no DB session in
        # synchronous context); removed Apr 28 per #1012 sweep.

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
        served: Optional[Dict[str, str]] = None,
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
            served: (#1620) optional caller-owned dict; on a successful call
                it is populated with {"provider": ..., "model": ...} — the
                RESOLVED provider/model that actually answered THIS call,
                after fallback. Per-call and task-safe (unlike the module's
                aggregate SERVING_MODEL_RECORD counter, which is unsafe to
                attribute to one call under concurrent traffic). None (the
                default) skips this — no behavior change for existing callers.

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
            served=served,
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
            served=served,
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
        served: Optional[Dict[str, str]] = None,
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
            served=served,  # #1620: the retry's serving overwrites the first attempt's
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
        served: Optional[Dict[str, str]] = None,
    ) -> str:
        """Underlying provider-call path (extracted from complete() in #1017
        Phase 2.2 so that the output-filter wrap can call the raw path
        twice during the regenerate-on-violation retry flow).

        Returns the raw LLM response text before filtering. ``served``
        (#1620), when given, is populated on success with this call's own
        resolved provider+model — the same values recorded into the module's
        aggregate SERVING_MODEL_RECORD, but scoped to this one call so a
        caller can attribute it correctly under concurrent traffic.
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
        except LLMKeyRequiredError:
            # #1815 Gap 2 / #1816: a REFUSAL is not a selection failure. The
            # blanket handler below degrades to "whichever client is initialized"
            # — i.e. the SERVER's own long-lived client — which for a consent-read
            # failure would be precisely the outcome Arch's ruling forbids:
            # fail-closed quietly reassigned to the operator's key. Measured
            # 2026-09-15 before this line existed: a consent-read failure was
            # swallowed here and the turn was served by the operator's Anthropic
            # client. Closed means closed; let it out.
            raise
        except (ValueError, Exception):
            # #1812 step 6: selection failed for a non-refusal reason. The old
            # fallback here was "whichever SERVER client is initialized" — those
            # clients no longer exist, so fall back to whichever provider THIS
            # REQUEST is entitled to spend (same read the fallback loop's gate
            # uses; the gate and this fallback cannot disagree).
            from services.llm.request_key import provider_spend_entitled

            for candidate in _FALLBACK_ORDER:
                if provider_spend_entitled(candidate.value):
                    primary_provider = candidate
                    break
            else:
                raise RuntimeError("No LLM providers configured. Add an API key in Settings.")

        # Build runtime config with correct model for this provider
        config = {
            **task_config,
            "provider": primary_provider,
            "model": resolve_model(primary_provider, task_type),
        }

        # Try primary provider first
        primary_exc: Exception
        primary_refused: bool
        try:
            result = await self._call_provider(
                primary_provider, prompt, config, response_format, context, system
            )
            # #1676: record the SERVING provider+model (success only).
            # resolve_model_alias(...) is the exact id the provider call sends.
            served_model = resolve_model_alias(config["model"].value)
            _record_serving(primary_provider.value, served_model)
            if served is not None:  # #1620: per-call resolved provider+model
                served["provider"] = primary_provider.value
                served["model"] = served_model
            return result
        except LLMKeyRequiredError as e:
            # #1809: a key refusal from the provider leg (the inverted chokepoint —
            # unbound is now an ERROR, never a server-key fallback) is a correct
            # ANSWER, not a provider failure to relabel as "All configured LLM
            # providers failed" (try-again copy for a condition retrying cannot fix;
            # #1815 Gap 2 at the call layer).
            # #1819 refinement: with the binding PER-PROVIDER, "not entitled on the
            # primary" no longer implies "not entitled at all" — a user whose
            # instance defaults to OpenAI may hold only their own Anthropic key
            # (#1815's exact scenario). So the refusal falls through to the loop
            # below, whose availability gate is entitlement-aware: only providers
            # this REQUEST can spend are tried. If none exists, the refusal — not a
            # fabricated outage — is what surfaces (the #1809 pin, preserved).
            logger.info(
                "llm_primary_not_entitled",
                provider=primary_provider.value,
                task_type=task_type,
            )
            primary_exc = e
            primary_refused = True
        except Exception as e:  # silent-ok: DEFERRED, not swallowed — captured as primary_exc; every path below either returns a successful fallback or re-raises (the refusal, or the aggregate RuntimeError) (#1819)
            logger.warning(
                "llm_primary_failed",
                provider=primary_provider.value,
                task_type=task_type,
                error=str(e),
            )
            primary_exc = e
            primary_refused = False

        # Try each other configured provider in the fallback order (Apr 16: Gemini added)
        # #1415: the fallback set respects the acting user's consent list —
        # resilience never overrides #946 (a de-authorized provider must not
        # process the user's message even when everything else is down).
        try:
            user_authorized = set(self._config_service.get_configured_providers(user_id))
        except Exception as consent_err:  # silent-ok: consent unknown -> no cross-provider fallback (fail closed); the primary error below still surfaces honestly (#1415). #1816: a ConsentUnreadableError landing here is ALSO fail-closed — an empty authorized set means every fallback candidate is skipped; the primary provider's own error is the honest thing to report, since the primary had already been selected from a consent read that succeeded.
            logger.warning(f"fallback_consent_check_failed: {consent_err}")
            user_authorized = set()
        fallback_errors: list[str] = [f"{primary_provider.value}: {primary_exc}"]
        attempted_fallback = False
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
            attempted_fallback = True

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
                fallback_served_model = resolve_model_alias(fallback_config["model"].value)
                _record_serving(fallback_provider.value, fallback_served_model)
                if served is not None:  # #1620: per-call resolved provider+model
                    served["provider"] = fallback_provider.value
                    served["model"] = fallback_served_model
                return result
            except LLMKeyRequiredError:
                # #1809/#1819: the gate above (`_is_provider_configured`) is
                # entitlement-aware, so a refusal HERE means the gate and the
                # consumer disagreed about this request's spend entitlement — the
                # #1814/#1815 agreement property broke. Surface it; papering over
                # it with the next candidate would hide the disagreement.
                raise
            except Exception as fallback_error:
                logger.warning(
                    f"Fallback provider {fallback_provider.value} failed: {fallback_error}"
                )
                fallback_errors.append(f"{fallback_provider.value}: {fallback_error}")
                continue

        if primary_refused and not attempted_fallback:
            # #1809: the request held no spendable key for ANY consented provider —
            # the refusal is the honest answer, never "all providers failed".
            raise primary_exc
        # No fallback succeeded
        logger.error(f"All LLM providers failed: {fallback_errors}")
        raise RuntimeError(
            f"All configured LLM providers failed. Details: {'; '.join(fallback_errors)}"
        )

    def _is_provider_configured(self, provider: LLMProvider) -> bool:
        """Return True if `provider` can be called ON THIS REQUEST.

        #1815 Gap 1. This used to mean "the SERVER has a live client for it", which is the
        same server-singleton-as-availability-proxy shape #1814 removed from the primary
        path — surviving one frame lower, in `_complete_raw`'s cross-provider fallback
        loop (this method's only caller). Post-#1810 the server owns no Anthropic key on a
        BYOC deployment, so `self.anthropic_client` is None and a user's own working key
        satisfied the gate above `_call_provider` but was skipped in silence as a
        *fallback*. Primary=openai is the default (`PIPER_DEFAULT_PROVIDER`), so this bit
        any mixed instance the moment OpenAI had a bad minute.

        The fix reuses #1814's shape rather than inventing a parallel one: read the SAME
        ContextVar the consumers read, so the gate and the consumers cannot disagree.
        Every leg resolves its spend entitlement through `request_spend_key` (#1819), so
        that read — surfaced non-raising as `provider_spend_entitled` — and only that
        read, is what "available" has to mean here.

        #1819 (superseding the #1815-era "Anthropic only" carve): the per-request
        binding is provider-keyed now, and EVERY leg refuses unbound. So a server
        client's mere existence is no longer availability — an unbound request that
        reached `_openai_complete` would refuse, and reporting True here would route
        the fallback loop into that guaranteed refusal (the exact trap the #1815
        docstring named).

        #1812 step 5: with the operator seam deleted there are no server clients
        left to consult, so this collapses to the entitlement read itself: True
        exactly when a key is bound for this provider AND the leg can build a
        per-request client from it (`PER_REQUEST_CLIENT_PROVIDERS` — a bound Gemini
        key has no safe consumer and reads False). The gate and the consumers read
        the SAME ContextVar, so they cannot disagree (#1814's shape).

        **Nothing is constructed or stored.** This is a pure read; the key reaches
        the provider only via the leg's own chokepoint read.
        """
        from services.llm.request_key import provider_spend_entitled

        return provider_spend_entitled(provider.value)

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
        # #1162 BYOC / #1809 inversion: use the request's user-supplied key (bound by
        # the entry point via `request_api_key`). UNBOUND raises `UnboundLLMKeyError`
        # — there is no server-key fallback (PM ruling, #1812; the operator seam is
        # gone since step 5). Always a fresh per-request client, billed to the acting
        # user. The key is never logged here.
        from services.llm.request_key import anthropic_client_for_request

        client = anthropic_client_for_request()

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
        """Get completion from OpenAI.

        #1819: same inversion as `_anthropic_complete` (#1809). `request_spend_key`
        decides WHOSE credential this call spends: the bound per-request OpenAI key
        (the user's own, from `user_api_keys`) builds a FRESH client for this call
        — never stored on `self` (#1814 containment). UNBOUND raises
        `UnboundLLMKeyError`; there is no server-key fallback (PM ruling, #1812;
        the operator seam is gone since step 5). The key is never logged here.
        """
        from services.llm.request_key import request_spend_key

        client = OpenAI(api_key=request_spend_key("openai"))

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

        response = client.chat.completions.create(**request_params)

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

        #1819: same inversion as the other legs — with one deliberate asymmetry.
        `google.generativeai` configures credentials PROCESS-GLOBALLY
        (`genai.configure`), so there is no safe per-request client path: honoring
        a bound per-request Gemini key would risk serving request A under request
        B's credential in concurrent traffic.

        #1812 step 5: the leg's ONLY spend path was the designated-operator binding
        (the process-global configuration as the operator's own credential), and
        that seam is deleted — so Gemini currently has NO spend path at all and
        this leg is a pure, honest refusal. `_is_provider_configured` already
        reads False for Gemini on every binding (not in
        `PER_REQUEST_CLIENT_PROVIDERS`), so the fallback loop never routes here;
        only an explicit primary selection can. The serving code was removed with
        the seam (git has it) — resurrect it only alongside a SAFE per-request
        credential path, which the SDK does not offer today (#1819).
        """
        from services.llm.request_key import UnboundLLMKeyError, request_spend_key

        # Raises UnboundLLMKeyError unless a Gemini key is bound for this request…
        request_spend_key("gemini")
        # …and a bound Gemini key still has no safe per-request client path:
        raise UnboundLLMKeyError(
            "A per-request Gemini key was bound, but Gemini has no per-request "
            "client path (google.generativeai credentials are process-global) — "
            "refusing rather than risking a cross-request credential mix-up "
            "(#1819). Use Anthropic or OpenAI for per-user keys."
        )


# Global client instance
llm_client = LLMClient()
