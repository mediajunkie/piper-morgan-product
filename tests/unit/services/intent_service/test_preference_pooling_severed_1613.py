"""1613: preference confirmation works WITHOUT the cross-user pooled store.

PM ruled option (a) 2026-08-31: the live pooling write path — every confirmed
preference handed to ``QueryLearningLoop._apply_user_preference_pattern`` (a
store keyed by ``source_feature``, not by user) — contradicted published
privacy claims and was severed. Confirmed preferences now land ONLY in the
user-scoped ``UserPreferenceManager``.

These pins are the inverse of the retired ``test_preference_pattern_type_1436``
(which asserted the pooled hand-off DID happen — correct then, a violation now):

1. Confirm-a-preference end-to-end still succeeds and writes the user-scoped
   preference.
2. NO write (or construction) reaches the pooled store during handler init +
   the full confirm flow — spy-asserted while the pooling module still exists;
   once the module is disposed (Phase 2 of 1613), asserted by its absence from
   the import graph, which is the strictly stronger guarantee.
"""

import importlib.util
from datetime import datetime
from unittest.mock import AsyncMock, patch

from services.intent_service import preference_handler as ph_module
from services.intent_service.preference_handler import PreferenceDetectionHandler

POOLING_MODULE = "services.learning.query_learning_loop"

_HINT_ID = "hint-1613"
_SESSION_ID = "session-1613"
_USER_ID = "8b7df143-6135-4a0e-9d9f-9f0d3a3d3a3d"


def _seed_session_hint():
    """Place a valid, unexpired hint where confirm_preference retrieves it."""
    ph_module._SESSION_HINTS[_SESSION_ID] = {
        _HINT_ID: {
            "id": _HINT_ID,
            "dimension": "technical_depth",
            "current_value": "medium",
            "detected_value": "high",
            "confidence_score": 0.9,
            "detection_method": "explicit_feedback",
            "stored_at": datetime.now().isoformat(),
            "ttl_minutes": 30,
        }
    }


def _build_handler() -> PreferenceDetectionHandler:
    handler = PreferenceDetectionHandler()
    # Seam-level mock: the user-scoped persistence layer, not the flow under test.
    handler.preference_manager.set_preference = AsyncMock(return_value=True)
    return handler


async def _confirm(handler: PreferenceDetectionHandler):
    _seed_session_hint()
    try:
        return await handler.confirm_preference(
            user_id=_USER_ID,
            session_id=_SESSION_ID,
            hint_id=_HINT_ID,
            accepted=True,
        )
    finally:
        ph_module._SESSION_HINTS.pop(_SESSION_ID, None)


async def test_confirm_preference_e2e_succeeds_user_scoped():
    """The confirm flow works minus the pooled write: success + user-scoped store."""
    handler = _build_handler()

    result = await _confirm(handler)

    assert result["success"] is True
    assert result["action"] == "accepted"
    assert result["dimension"] == "technical_depth"
    assert result["new_value"] == "high"
    handler.preference_manager.set_preference.assert_awaited_once()
    kwargs = handler.preference_manager.set_preference.await_args.kwargs
    assert kwargs["key"] == "personality_technical_depth"
    assert kwargs["value"] == "high"
    assert str(kwargs["user_id"]) == _USER_ID  # user-scoped, never pooled


async def test_no_write_reaches_the_pooled_store():
    """Spy on every pooled-store entry point across init + confirm: zero calls.

    Layer named (m-43): while the pooling module exists this measures actual
    call traffic via spies; after Phase-2 disposal it measures the import
    graph — the module's absence makes a pooled write structurally impossible.
    """
    if importlib.util.find_spec(POOLING_MODULE) is None:
        # Phase 2 landed: pooled store is gone from the codebase entirely.
        handler = _build_handler()
        result = await _confirm(handler)
        assert result["success"] is True
        assert not hasattr(handler, "learning_loop")
        return

    from services.learning.query_learning_loop import QueryLearningLoop

    with (
        patch.object(QueryLearningLoop, "__init__", autospec=True, return_value=None) as spy_init,
        patch.object(QueryLearningLoop, "learn_pattern", new_callable=AsyncMock) as spy_learn,
        patch.object(
            QueryLearningLoop, "_apply_user_preference_pattern", new_callable=AsyncMock
        ) as spy_apply,
    ):
        handler = _build_handler()
        result = await _confirm(handler)

    assert result["success"] is True
    assert not hasattr(handler, "learning_loop")
    spy_init.assert_not_called()  # pooled store never even constructed
    spy_learn.assert_not_awaited()
    spy_apply.assert_not_awaited()
