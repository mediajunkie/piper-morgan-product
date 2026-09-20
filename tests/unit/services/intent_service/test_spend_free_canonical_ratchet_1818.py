"""#1818 — the spend-free ratchet: THE definition of the spends-nothing set.

Why this test is the definition and not a check of one (Arch's 2026-09-20 correction):
``ActionDisposition.CANONICAL`` does NOT mean "spends nothing" — it means "the LLM cannot
do this alone," which for EXECUTION/PORTFOLIO is true BECAUSE they have side effects, not
because they're free. Gating #1818's keyless door on CANONICAL would have opened keyless
issue-creation. The property the gate needs — "this turn spends nothing" — had no owner in
the codebase. This file creates it, empirically: every pre-classifier pair the registry
calls CANONICAL is driven through the REAL ``process_intent`` with the spend chokepoint
instrumented, and the pairs measured clean ARE the set. Nothing else defines it.

Measurement point: ``services.llm.request_key.request_spend_key`` — every provider leg
(all three completions AND embeddings) resolves its spend entitlement through this one
function (#1815 Gap 1 / #1819). A turn that never calls it cannot spend; a turn that calls
it would spend when keyed. We record calls AND raise the real ``UnboundLLMKeyError``, so
the drive is production-faithful-keyless and can never bill anything regardless of what
keys the host machine holds (#1821's property). Known limit, stated: a handler that
bypassed LLMClient and constructed a vendor SDK client directly would not cross this
chokepoint — no such path exists today (that bypass audit is #1829's first task), and one
appearing would be its own architecture violation.

TWO-SIDED (the #1452 burn-down shape):
- A pair in ``SPEND_FREE`` that starts spending FAILS — the #1818 gate consumes this
  predicate, so that regression would open a billed path behind a keyless door.
- A pair in ``SPENDS`` that stops spending FAILS TOO — deliberately loud, because that's
  an improvement someone should PROMOTE to ``SPEND_FREE`` (and thereby through the gate),
  not an accident that drifts silently.

The mapping assertions exist so pattern drift surfaces as "this message no longer reaches
that pair" instead of silently measuring the wrong path.

CXO's coherence findings (2026-09-20) live one layer up: THIS file measures what IS
spend-free; whether that set is coherent as a first-contact experience (compound
greetings, farewell/thanks) is #1818's design surface, fed by these measurements.
"""

from unittest.mock import AsyncMock

import pytest

from services.intent_service.pre_classifier import PreClassifier

# (category, action) -> a message the pre-classifier VERIFIABLY maps to that pair
# (probed live 2026-09-20; the test re-asserts each mapping on every run).
PAIR_MESSAGES = {
    ("CONVERSATION", "greeting"): "hi",
    ("CONVERSATION", "farewell"): "bye",
    ("CONVERSATION", "thanks"): "thanks",
    ("IDENTITY", "get_identity"): "what's your name?",
    ("DISCOVERY", "get_capabilities"): "what can you do?",
    ("TRUST", "explain_trust"): "why can't you do that?",
    ("MEMORY", "get_memory"): "what do you remember?",
    ("TEMPORAL", "get_current_time"): "what time is it?",
    ("STATUS", "get_project_status"): "project status",
    ("PRIORITY", "get_top_priority"): "what's the top priority?",
    ("GUIDANCE", "get_contextual_guidance"): "any guidance?",
    ("PORTFOLIO", "manage_portfolio"): "archive project X in my portfolio",
    ("PORTFOLIO", "manage_repos"): "link mediajunkie/test to project X",
    ("PROVENANCE", "explain_suggestion"): "why did you suggest that?",
}

# THE SETS — measured 2026-09-20, first instrumented drive. Membership changes are
# deliberate acts reviewed against #1818's gate, never side effects.
#
# The measurement, for the record: only 5 of the 14 registry-CANONICAL pairs are
# actually spend-free. NINE cross the chokepoint — including `thanks` and `farewell`
# (traced: intent_service dispatch -> conversational_floor.py:1533 -> LLMClient
# openai leg — the floor COMPOSES the pleasantry, which is #1773's registry-vs-runtime
# drift caught billing), and the "deterministic fast-path" poster children (identity,
# capabilities, trust, memory, status, priority, guidance), whose real handler flows
# reach the LLM. "Canonical" was never a cost claim; here is the cost, measured.
SPEND_FREE = {
    ("CONVERSATION", "greeting"),
    ("TEMPORAL", "get_current_time"),
    ("PORTFOLIO", "manage_portfolio"),
    ("PORTFOLIO", "manage_repos"),
    ("PROVENANCE", "explain_suggestion"),
}
SPENDS = set(PAIR_MESSAGES) - SPEND_FREE


@pytest.fixture
def spend_chokepoint(monkeypatch):
    """Instrument request_spend_key: count every crossing, refuse like keyless prod."""
    from services.llm import request_key as rk

    calls: list = []

    def _recording_refusal(provider: str):
        calls.append(provider)
        raise rk.UnboundLLMKeyError(
            f"spend attempted for '{provider}' during the #1818 spend-free drive "
            "(recorded by the ratchet; refused so nothing can ever bill)"
        )

    monkeypatch.setattr(rk, "request_spend_key", _recording_refusal)
    # clients.py imports the name at call sites via module attribute lookups in some
    # legs and direct import in others — patch the consumer module's binding too.
    from services.llm import clients as clients_mod

    if hasattr(clients_mod, "request_spend_key"):
        monkeypatch.setattr(clients_mod, "request_spend_key", _recording_refusal)
    return calls


@pytest.fixture
def real_intent_service():
    """The REAL service — real pre-classifier, real canonical handlers, real dispatch.

    (Unlike this directory's offer suites, nothing is mocked: the whole point is
    measuring what the true handler paths do.)
    """
    from services.intent.intent_service import IntentService
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
    from services.intent_service.workflow_entries import register_default_workflows

    WORKFLOW_REGISTRY.clear()
    register_default_workflows()
    service = IntentService()
    yield service
    WORKFLOW_REGISTRY.clear()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "pair,message",
    [(p, m) for p, m in PAIR_MESSAGES.items()],
    ids=[f"{c}-{a}" for (c, a) in PAIR_MESSAGES],
)
async def test_canonical_pair_spend_reach(pair, message, spend_chokepoint, real_intent_service):
    # 1. The message still maps to the pair it claims to exercise.
    intent = PreClassifier.pre_classify(message)
    assert intent is not None and (intent.category.name, intent.action) == pair, (
        f"pattern drift: {message!r} no longer pre-classifies to {pair} "
        f"(got {(intent.category.name, intent.action) if intent else None}) — "
        "fix the message here, don't let the ratchet measure the wrong path"
    )

    # 2. Drive the REAL turn, keyless. A spend-refusal ESCAPING here is itself part of
    # the measurement: process_intent deliberately does not catch UnboundLLMKeyError
    # (#1809 — a refusal surfaces; the ROUTE layer converts it to honest copy), so for
    # spending pairs the drive ends in the refusal. The chokepoint counter has already
    # recorded the crossing by then.
    from services.llm.request_key import UnboundLLMKeyError

    refused = False
    try:
        result = await real_intent_service.process_intent(
            message=message, session_id=f"spendfree-{pair[1]}", user_id=None
        )
        assert result is not None, f"{pair}: process_intent returned nothing"
    except UnboundLLMKeyError:
        refused = True
    assert (
        refused == (len(spend_chokepoint) > 0) or not refused
    ), f"{pair}: refusal escaped with zero recorded crossings — harness inconsistency"

    # 3. The two-sided ratchet on the chokepoint count.
    crossings = len(spend_chokepoint)
    if pair in SPEND_FREE:
        assert crossings == 0, (
            f"{pair} is in SPEND_FREE but crossed the spend chokepoint {crossings}x "
            f"(providers: {spend_chokepoint}). The #1818 gate consumes this predicate — "
            "a keyless user would have been served a turn that bills when keyed. Either "
            "fix the regression or, if the spend is a deliberate design change, move the "
            "pair to SPENDS *and* re-review the gate's exempt set in the same commit."
        )
    else:
        assert crossings > 0, (
            f"{pair} is in SPENDS but crossed the chokepoint 0x — it became spend-free. "
            "That's an improvement: PROMOTE it to SPEND_FREE deliberately (and consider "
            "whether #1818's gate should now admit it) instead of letting it drift."
        )
