"""#1465: execute_pattern success path must record success, not failure.

Regression: ``web/api/routes/learning.py`` had no ``datetime`` import in scope
for ``execute_pattern`` (module level has none; every other handler that needs
it imports function-locally). The success path's
``pattern.updated_at = datetime.now(timezone.utc)`` raised NameError AFTER the
ActionRegistry action ran, so the inner ``except Exception as exec_error``
recorded every successful proactive execution as a failure:
``failure_count += 1``, ``confidence *= 0.9``, and a 500-style error response.

These tests call the handler directly (same idiom as
test_learning_error_helpers_1436.py) and pin:
  - success path: success_count += 1, failure_count unchanged, confidence
    grows (x1.05), updated_at set, success payload returned
  - failure path: a genuinely failing action still records failure (semantics
    untouched by the fix)
"""

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from web.api.routes.learning import execute_pattern

PATTERN_UUID = uuid4()


def _make_pattern():
    return SimpleNamespace(
        id=PATTERN_UUID,
        user_id="user-1",
        pattern_data={"action_type": "test_action", "action_params": {"k": "v"}},
        success_count=2,
        failure_count=1,
        confidence=0.5,
        updated_at=None,
    )


def _make_session(pattern):
    session = AsyncMock()
    result = MagicMock()
    result.scalar_one_or_none.return_value = pattern
    session.execute = AsyncMock(return_value=result)
    session.commit = AsyncMock()
    return session


def _scope_returning(session):
    scope = MagicMock()
    scope.__aenter__ = AsyncMock(return_value=session)
    scope.__aexit__ = AsyncMock(return_value=None)
    return scope


@pytest.mark.asyncio
async def test_successful_execution_records_success_not_failure():
    pattern = _make_pattern()
    session = _make_session(pattern)
    current_user = SimpleNamespace(user_id="user-1")

    with (
        patch(
            "web.api.routes.learning.AsyncSessionFactory.session_scope",
            return_value=_scope_returning(session),
        ),
        patch(
            "services.actions.action_registry.ActionRegistry.execute",
            new=AsyncMock(return_value={"message": "action ran"}),
        ),
    ):
        resp = await execute_pattern(str(PATTERN_UUID), current_user=current_user)

    # Old behavior: NameError('datetime') -> failure branch -> internal_error
    # JSONResponse (status 500), failure_count 2, confidence 0.45.
    assert isinstance(resp, dict), f"expected success payload, got {resp!r}"
    assert resp["success"] is True
    assert resp["pattern"]["success_count"] == 3

    assert pattern.success_count == 3
    assert pattern.failure_count == 1  # unchanged
    assert pattern.confidence == pytest.approx(0.525)  # 0.5 * 1.05, not * 0.9
    assert isinstance(pattern.updated_at, datetime)
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_failing_execution_still_records_failure():
    pattern = _make_pattern()
    session = _make_session(pattern)
    current_user = SimpleNamespace(user_id="user-1")

    with (
        patch(
            "web.api.routes.learning.AsyncSessionFactory.session_scope",
            return_value=_scope_returning(session),
        ),
        patch(
            "services.actions.action_registry.ActionRegistry.execute",
            new=AsyncMock(side_effect=RuntimeError("action blew up")),
        ),
    ):
        resp = await execute_pattern(str(PATTERN_UUID), current_user=current_user)

    assert not isinstance(resp, dict)  # internal_error JSONResponse
    assert resp.status_code == 500
    assert pattern.success_count == 2  # unchanged
    assert pattern.failure_count == 2
    assert pattern.confidence == pytest.approx(0.45)  # 0.5 * 0.9
