"""#1829 — provider-agnosticism is load-bearing for BYOC but was enforced
only by a source comment ("Task configurations — provider-agnostic",
services/llm/config.py:74) — a comment is not a mechanism (m-41).

Arch's finding (2026-09-19, from CXO's #1823 branch-two trace): the
invariant holds today (CXO measured 8/8 MODEL_CONFIGS task types x 3/3
PROVIDER_MODELS providers, all resolve) but nothing in the repo would fail,
flag, or even notice if a future task type became provider-constrained, or
a fourth provider were added without a full tier set. Two distinct gaps:

1. No RATCHET asserting the enumeration — a future regression would be
   silent, same as the invariant was before this test.
2. `resolve_model`'s totality is by SILENT FALLBACK, not exhaustive
   coverage: an unknown task_type quietly bought the heavy tier; an
   unknown provider quietly returned OpenAI's models. Neither failed nor
   logged.

Decision on (2), stated at the enforcement site (services/llm/config.py's
resolve_model docstring, #1829 lane, 2026-09-24): KEEP both fallbacks
(raising would take down live request paths for an axis that's unreached
today), but make them LOUD — a structured warning naming which axis fell
through. This file enforces both halves: the strong-form enumeration (not
`resolve_model(...) is not None`, which passes vacuously given the
fallbacks — the #1642 `test_standup_data_sources` shape) plus a positive
check that the now-logged fallback still fires under a deliberately-unknown
pair (so it isn't vestigial dead code that never actually triggers).
"""

import types

import structlog

from services.llm.config import (
    MODEL_CONFIGS,
    PROVIDER_MODELS,
    LLMModel,
    LLMProvider,
    resolve_model,
)


class TestProviderAgnosticismEnumeration1829:
    """AC: every task type x every provider the config knows, enumerated
    from the config module itself — never a hand-written list, so a new
    task type or provider is automatically covered on the next run."""

    def _task_types(self):
        return sorted(MODEL_CONFIGS.keys())

    def _providers(self):
        return sorted(PROVIDER_MODELS.keys())

    def test_enumeration_is_non_empty_and_denominator_is_stated(self, capsys):
        task_types = self._task_types()
        providers = self._providers()
        assert (
            task_types
        ), "MODEL_CONFIGS is empty — nothing to enumerate (#1829 requires a non-empty domain)"
        assert (
            providers
        ), "PROVIDER_MODELS is empty — nothing to enumerate (#1829 requires a non-empty domain)"
        print(
            f"#1829 denominator: {len(task_types)} task types "
            f"({task_types}) x {len(providers)} providers ({providers}) "
            f"= {len(task_types) * len(providers)} pairs"
        )

    def test_every_task_type_x_provider_resolves_to_a_real_model(self):
        """The weak form, kept because it's still a real assertion (a
        raise would fail this) — but see the next test for the STRONG
        form this issue actually asked for."""
        task_types = self._task_types()
        providers = [LLMProvider(p) for p in self._providers()]
        assert task_types and providers

        failures = []
        checked = 0
        for task_type in task_types:
            for provider in providers:
                checked += 1
                try:
                    model = resolve_model(provider, task_type)
                except Exception as e:  # pragma: no cover - failure path, asserted below
                    failures.append(f"{provider.value}/{task_type}: raised {e!r}")
                    continue
                if not isinstance(model, LLMModel):
                    failures.append(
                        f"{provider.value}/{task_type}: resolved to non-LLMModel {model!r}"
                    )

        assert checked == len(task_types) * len(providers), (
            f"expected to check {len(task_types)} x {len(providers)} = "
            f"{len(task_types) * len(providers)} pairs, actually checked {checked}"
        )
        assert not failures, (
            f"{len(failures)} of {checked} (task_type, provider) pairs failed to "
            f"resolve to a real LLMModel:\n" + "\n".join(failures)
        )

    def test_no_known_pair_silently_falls_through_to_a_default(self):
        """The STRONG form #1829 asked for explicitly: not
        ``resolve_model(...) is not None`` (passes vacuously — both
        fallback branches also return a non-None LLMModel), but that NONE
        of the config's own declared pairs actually trip the fallback
        path. This is the test that would have caught #1829's own defect
        class: a task type silently dropped from MODEL_CONFIGS coverage,
        or a provider silently missing a tier, now fails loudly here
        instead of degrading to the heavy tier / OpenAI's models."""
        task_types = self._task_types()
        providers = [LLMProvider(p) for p in self._providers()]

        with structlog.testing.capture_logs() as cap:
            for task_type in task_types:
                for provider in providers:
                    resolve_model(provider, task_type)

        fallback_events = {
            "resolve_model_unknown_task_type_fallback",
            "resolve_model_unknown_provider_fallback",
        }
        fired = [e for e in cap if e.get("event") in fallback_events]
        assert not fired, (
            f"{len(fired)} of {len(task_types) * len(providers)} known-good "
            f"(task_type, provider) pairs silently hit the fallback path "
            f"(should never happen for a config-declared pair): {fired}"
        )


class TestSilentFallbackIsNowLogged1829:
    """AC: the fallback stays a fallback — KEEP, not RAISE (the decision is
    stated at services/llm/config.py's resolve_model docstring) — but a
    deliberately-unknown (task_type, provider) pair must be LOUD, not
    silent. Both halves proven independently: an unknown task_type, and an
    unknown provider."""

    def test_unknown_task_type_fires_a_structured_warning_and_still_resolves(self):
        unknown = "totally-unknown-task-type-1829"
        with structlog.testing.capture_logs() as cap:
            model = resolve_model(LLMProvider.ANTHROPIC, unknown)

        # Fallback KEPT (not raised) — a caller with a typo'd task_type
        # still gets served, per the stated decision.
        assert isinstance(model, LLMModel)

        events = [e for e in cap if e.get("event") == "resolve_model_unknown_task_type_fallback"]
        assert events, (
            f"expected a resolve_model_unknown_task_type_fallback warning; "
            f"captured events: {[e.get('event') for e in cap]}"
        )
        assert events[0]["task_type"] == unknown
        assert events[0]["fallback_task_type"] == "reasoning"
        assert events[0]["log_level"] == "warning"

    def test_unknown_provider_fires_a_structured_warning_and_still_resolves(self):
        # A bare object carrying `.value` — resolve_model's only real
        # runtime contract on `provider` (it is not enforced by the type
        # hint at runtime). Stands in for "a 4th provider the config
        # doesn't know about yet" without touching the real LLMProvider
        # enum or monkeypatching PROVIDER_MODELS.
        fake_provider = types.SimpleNamespace(value="cohere-not-a-real-provider-1829")

        with structlog.testing.capture_logs() as cap:
            model = resolve_model(fake_provider, "reasoning")

        assert isinstance(model, LLMModel)

        events = [e for e in cap if e.get("event") == "resolve_model_unknown_provider_fallback"]
        assert events, (
            f"expected a resolve_model_unknown_provider_fallback warning; "
            f"captured events: {[e.get('event') for e in cap]}"
        )
        assert events[0]["provider"] == "cohere-not-a-real-provider-1829"
        assert events[0]["fallback_provider"] == "openai"
        assert events[0]["log_level"] == "warning"
