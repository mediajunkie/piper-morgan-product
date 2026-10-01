"""The Inversion router must work through the LLM object the APP injects.

Found 2026-09-30 by the first end-to-end probe through the real app (#1897
live proof): ``services/container/initialization.py`` builds the classifier
with ``LLMDomainService`` (``registry.get("llm")``), and the router's
``route()`` passes ``served=`` (#1620) to ``llm_service.complete`` — which
``LLMDomainService.complete`` did not accept. Every live consult raised
``TypeError`` inside the router, which caught it and reported
``outcome="error"`` → ``route: legacy, reason: router_error``. The flag read
"live" for five days while no production turn was routed by the Inversion;
the scorer never saw it because it calls ``LLMClient`` directly.

This pin drives ``route()`` through a real ``LLMDomainService`` wrapping a
stub client, so the app's actual call path is what is tested — the shape
m-43 asks for. No network.
"""

from __future__ import annotations

import inspect

import pytest

from services.domain.llm_domain_service import LLMDomainService
from services.intent_service import inversion_router as ir


class _StubClient:
    def __init__(self, reply: str):
        self.reply = reply
        self.calls = []

    async def complete(self, *, served=None, **kwargs):
        self.calls.append(kwargs)
        if served is not None:
            served["provider"] = "stub"
            served["model"] = "stub-model"
        return self.reply


def _domain_service(reply: str) -> LLMDomainService:
    svc = LLMDomainService()
    svc._llm_client = _StubClient(reply)
    svc._initialized = True
    return svc


def test_domain_service_complete_accepts_served():
    """The signature itself: the kwarg the router passes exists here."""
    assert "served" in inspect.signature(LLMDomainService.complete).parameters


@pytest.mark.asyncio
async def test_router_routes_through_the_apps_llm_object():
    grammar = ir.derive_routing_grammar()
    op = grammar.operations[0].name
    svc = _domain_service(
        f'{{"operation": "{op}", "args": {{}}, "confidence": 0.9, "rationale": "stub"}}'
    )
    decision = await ir.route("hello", None, llm_service=svc, grammar=grammar, user_id=None)
    assert decision.outcome == "operation", decision
    assert decision.operation == op
    # #1620: the resolved provider/model flow back through the domain service.
    assert decision.served_provider == "stub"
    assert decision.served_model == "stub-model"
    assert len(svc._llm_client.calls) == 1


@pytest.mark.asyncio
async def test_router_error_is_the_old_failure_shape_and_must_not_recur():
    """Documents the exact failure: a wrapper whose complete() lacks ``served``
    turns every consult into outcome="error" with a TypeError — the router
    survives it (by design) and the Inversion silently goes dark."""

    class _NoServed:
        async def complete(  # the pre-fix LLMDomainService shape: no ``served``
            self,
            task_type,
            prompt,
            context=None,
            response_format=None,
            session=None,
            system=None,
            user_id=None,
        ):
            return "{}"

    grammar = ir.derive_routing_grammar()
    decision = await ir.route("hello", None, llm_service=_NoServed(), grammar=grammar, user_id=None)
    assert decision.outcome == "error"
    assert "served" in (decision.error or "")
    # And the real wrapper does NOT have that shape any more:
    svc = _domain_service('{"operation": "NONE", "args": {}, "confidence": 1.0, "rationale": "x"}')
    ok = await ir.route("hello", None, llm_service=svc, grammar=grammar, user_id=None)
    assert ok.outcome != "error"


@pytest.mark.asyncio
async def test_initialization_injects_a_domain_service_not_a_client():
    """The wiring fact this pin exists for: the classifier's LLM in the app is
    LLMDomainService. If that ever changes, this test should be updated with
    the new object's call shape, not deleted."""
    from services.container import initialization

    src = inspect.getsource(initialization.ServiceInitializer._initialize_intent_service)
    assert 'self.registry.get("llm")' in src
    assert "IntentClassifier(llm_service=llm_service)" in src
    # And registry "llm" is an LLMDomainService — the type the app registers.
    llm_src = inspect.getsource(initialization.ServiceInitializer._initialize_llm_service)
    assert "LLMDomainService" in llm_src
