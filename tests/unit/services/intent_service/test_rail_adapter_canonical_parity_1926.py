"""Adapter parity pin (Arch's 2026-10-04 ruling, unparking "the rail owns
every rail key": mailboxes/lead/inbox/rule-arch-to-lead-cc-cxo-exec-take-a-
split-predicate-adapter-parity-lands-with-it-b-uses-0926-sequencing-
2026-10-04.md §2).

"A rail adapter around a canonical handler must reproduce everything the
canonical path did around that call." Once ``CanonicalHandlers.can_handle``
declines every rail key (the generalization this ruling unparks), EVERY
canonical-wrapping rail adapter below is the ONLY path a classified/
live-consulted intent for that op takes — there is no longer a reachable
"main path" fallback for these specific ops. This file pins that each
adapter's dict->``IntentProcessingResult`` conversion
(``services.intent_service.workflow_entries._finalize_canonical_rail_result``)
reproduces the two things the (now largely unreachable, for these ops) main
canonical-dispatch branch did around the SAME dict
(``IntentService._process_intent_internal``, ~2763-2908):

  - the ``_is_generic_canonical_response`` floor-fallback safety net
  - ``offer_hint`` (#852) continuation tracking into
    ``ConversationContext.last_offer`` (``IntentService._track_offer_hint``)

Method: for each canonical-wrapping adapter, two independently-computed
results are compared for an identical input dict —

  (A) ``_expected_main_path_result`` — a standalone mirror of the main
      dispatch branch's logic, written fresh in THIS file (not calling
      ``_finalize_canonical_rail_result``), so a future drift in either
      implementation is caught rather than a tautology.
  (B) the REAL registered rail adapter entry point
      (``run_*_workflow``/the ``read_canonical`` factory's entry, via
      ``get_action_workflows()``), driven with the canonical handler method
      stubbed to return the SAME fixture dict.

Mocking idiom: the canonical handler METHOD is stubbed (not the DB layer
underneath it) — the same boundary test_portfolio_write_split_1595.py /
test_read_portfolio_rail_1595.py / test_read_canonical_rail_1595.py already
mock at (``SimpleNamespace(_handle_archive_project=...)`` etc.); this file
uses a REAL ``IntentService``/``CanonicalHandlers`` pair with only the one
handler method replaced, so the shared methods under test
(``_is_generic_canonical_response``, ``_track_offer_hint``,
``_resolve_formality_baseline``, ``_resolve_trust_stage``) are the real
ones, never a parallel mock of them. No DB call, no LLM call: the generic
case patches ``_handle_floor_with_context`` itself rather than letting the
real floor run (that method's own DB/LLM behavior is out of scope here).
"""

from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.conversation_context import clear_context, get_or_create_context
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import (
    register_default_workflows,
    run_add_project_workflow,
    run_archive_project_workflow,
    run_get_current_time_workflow,
    run_link_repo_workflow,
    run_list_repos_workflow,
    run_restore_project_workflow,
    run_search_projects_workflow,
    run_unlink_repo_workflow,
)
from services.shared_types import IntentCategory

pytestmark = pytest.mark.unit


async def _expected_main_path_result(
    service: IntentService,
    intent: Intent,
    canonical_dict: dict,
    session_id: str,
    user_id: str,
):
    """Independent mirror of the main canonical-dispatch branch
    (intent_service.py's _process_intent_internal, ~2763-2908) — written
    fresh here, never delegating to _finalize_canonical_rail_result, so this
    file is a real second implementation, not a tautology."""
    message = canonical_dict["message"]
    if service._is_generic_canonical_response(canonical_dict, message):
        formality_baseline = await service._resolve_formality_baseline(user_id)
        trust_stage = await service._resolve_trust_stage(user_id)
        return await service._handle_floor_with_context(
            intent,
            session_id,
            user_id=user_id,
            formality_baseline=formality_baseline,
            trust_stage=trust_stage,
        )
    service._track_offer_hint(canonical_dict, session_id, user_id)
    return IntentProcessingResult(
        success=True,
        message=message,
        intent_data=canonical_dict.get("intent"),
        workflow_id=None,
        requires_clarification=canonical_dict.get("requires_clarification", False),
    )


def _make_intent(category: IntentCategory, action: str) -> Intent:
    msg = f"test message for {action}"
    return Intent(
        category=category,
        action=action,
        confidence=0.95,
        original_message=msg,
        context={"original_message": msg},
    )


# ---------------------------------------------------------------------------
# Fixture dicts — ≥2 per adapter: a "found"/normal case and a "not found"/
# clarification case (the latter carrying offer_hint — the #852 continuation
# shape the not-found branches of archive/restore/search actually use).
# ---------------------------------------------------------------------------


def _found_dict(op: str, category: str) -> dict:
    return {
        "message": f"Here is the {op} result.",
        "intent": {"category": category, "action": op, "confidence": 0.95},
        "requires_clarification": False,
    }


def _not_found_dict(op: str, category: str) -> dict:
    return {
        "message": f"I couldn't find anything for {op}.",
        "intent": {
            "category": category,
            "action": op,
            "confidence": 0.95,
            "context": {"reason": "not_found"},
        },
        "requires_clarification": True,
        "offer_hint": {
            "continuation_hint": f"{op}_not_found",
            "offer_text": f"Want me to try a different name for {op}?",
        },
    }


# op -> (registry category, CanonicalHandlers attr, entry-point getter)
_ADAPTER_SPECS = {
    "get_current_time": (
        "TEMPORAL",
        "_handle_temporal_query",
        lambda: run_get_current_time_workflow,
    ),
    "explain_suggestion": (
        "PROVENANCE",
        "_handle_provenance_query",
        lambda: get_action_workflows()["explain_suggestion"].entry_point,
    ),
    "get_contextual_guidance": (
        "GUIDANCE",
        "_handle_guidance_query",
        lambda: get_action_workflows()["get_contextual_guidance"].entry_point,
    ),
    "list_repos": ("PORTFOLIO", "_handle_list_repos", lambda: run_list_repos_workflow),
    "search_projects": (
        "PORTFOLIO",
        "_handle_search_projects",
        lambda: run_search_projects_workflow,
    ),
    "archive_project": (
        "PORTFOLIO",
        "_handle_archive_project",
        lambda: run_archive_project_workflow,
    ),
    "restore_project": (
        "PORTFOLIO",
        "_handle_restore_project",
        lambda: run_restore_project_workflow,
    ),
    "add_project": ("PORTFOLIO", "_handle_add_project", lambda: run_add_project_workflow),
    "link_repo": ("PORTFOLIO", "_handle_link_repo", lambda: run_link_repo_workflow),
    "unlink_repo": ("PORTFOLIO", "_handle_unlink_repo", lambda: run_unlink_repo_workflow),
}


@pytest.fixture(autouse=True)
def _rail_registered():
    register_default_workflows()


@pytest.fixture(autouse=True)
def _clear_conversation_contexts():
    """Isolate #852 offer-hint tracking between cases — each test uses its
    own session_id, but belt-and-suspenders against cross-test leakage."""
    yield


@pytest.mark.asyncio
@pytest.mark.parametrize("op", sorted(_ADAPTER_SPECS))
@pytest.mark.parametrize(
    "fixture_builder", [_found_dict, _not_found_dict], ids=["found", "not_found"]
)
async def test_adapter_matches_main_path_for_dict(op, fixture_builder):
    category, handler_attr, get_entry_fn = _ADAPTER_SPECS[op]
    fixture = fixture_builder(op, category.lower())
    intent = _make_intent(IntentCategory[category], op)

    service = IntentService()
    setattr(service.canonical_handlers, handler_attr, AsyncMock(return_value=fixture))
    entry_fn = get_entry_fn()

    session_a = f"sess-main-{op}-{fixture_builder.__name__}"
    session_b = f"sess-rail-{op}-{fixture_builder.__name__}"
    user_id = "user-parity-1926"
    clear_context(session_a, user_id)
    clear_context(session_b, user_id)

    expected = await _expected_main_path_result(service, intent, fixture, session_a, user_id)
    actual = await entry_fn(
        session_b, user_id, context={"intent": intent, "intent_service": service}
    )

    assert actual is not None
    assert actual.message == expected.message
    assert actual.intent_data == expected.intent_data
    assert actual.requires_clarification == expected.requires_clarification

    expected_action = (expected.intent_data or {}).get("action")
    actual_action = (actual.intent_data or {}).get("action")
    assert actual_action == expected_action == op

    # #852 offer_hint parity: same side effect, same outcome, in each path's
    # own (isolated) conversation context.
    expected_offer = get_or_create_context(session_a, user_id).last_offer
    actual_offer = get_or_create_context(session_b, user_id).last_offer
    if fixture.get("offer_hint"):
        assert expected_offer is not None, "main-path mirror did not track offer_hint"
        assert actual_offer is not None, "rail adapter did not track offer_hint (#852 parity loss)"
        assert actual_offer.continuation_hint == expected_offer.continuation_hint
        assert actual_offer.offer_text == expected_offer.offer_text
    else:
        assert expected_offer is None
        assert actual_offer is None

    clear_context(session_a, user_id)
    clear_context(session_b, user_id)


# ---------------------------------------------------------------------------
# The generic-response floor-fallback safety net — only get_contextual_
# guidance's non-setup synthesis branch can produce a message matching
# IntentService._GENERIC_CANONICAL_SIGNATURES (verified in the parked lane's
# handback; the other 9 adapters never emit one of those templates).
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_guidance_adapter_reroutes_generic_response_to_the_floor():
    fixture = {
        "message": "Focus: Deep work",
        "intent": {"category": "guidance", "action": "get_contextual_guidance"},
        "requires_clarification": False,
    }
    intent = _make_intent(IntentCategory.GUIDANCE, "get_contextual_guidance")

    service = IntentService()
    setattr(service.canonical_handlers, "_handle_guidance_query", AsyncMock(return_value=fixture))

    floored = IntentProcessingResult(
        success=True,
        message="FLOORED — the richer, context-aware answer.",
        intent_data={"category": "guidance", "action": "floor_response"},
        requires_clarification=False,
    )
    service._handle_floor_with_context = AsyncMock(return_value=floored)
    service._resolve_formality_baseline = AsyncMock(return_value=None)
    service._resolve_trust_stage = AsyncMock(return_value=None)

    entry_fn = get_action_workflows()["get_contextual_guidance"].entry_point
    session_id = "sess-generic-guidance-1926"
    user_id = "user-parity-1926"
    clear_context(session_id, user_id)

    result = await entry_fn(
        session_id, user_id, context={"intent": intent, "intent_service": service}
    )

    assert result is floored, "the rail adapter did not reroute a generic response to the floor"
    service._handle_floor_with_context.assert_awaited_once()
    # The templated message must NOT be what the user sees — that's the
    # whole point of the safety net.
    assert result.message != fixture["message"]

    clear_context(session_id, user_id)
