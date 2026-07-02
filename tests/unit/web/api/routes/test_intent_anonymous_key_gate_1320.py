"""#1320: POST /api/v1/intent must refuse a fully anonymous (no login, no
X-User-Api-Key) request BEFORE touching IntentService/the LLM at all — never
silently bill the server's own Anthropic key. BYOC (anonymous + own key) must
still work unchanged (#1162's whole point).
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from web.api.routes.intent import process_intent


def _mock_request(message="hello", header_key=None, has_intent_service=True):
    req = MagicMock()
    req.json = AsyncMock(return_value={"message": message, "session_id": "s1"})
    req.headers = MagicMock()
    req.headers.get = MagicMock(
        side_effect=lambda k, default=None: (
            header_key if k == "X-User-Api-Key" else default
        )
    )
    req.cookies = {}
    req.app.state.intent_service = MagicMock() if has_intent_service else None
    return req


@pytest.mark.asyncio
async def test_anonymous_no_header_key_refused_before_touching_intent_service():
    req = _mock_request(header_key=None)

    result = await process_intent(req, current_user=None)

    assert result["error_type"] == "anonymous_key_required"
    assert result["requires_clarification"] is True
    assert "sign in" in result["message"].lower()
    # never reached the LLM/intent-service layer — refused up front
    req.app.state.intent_service.process_intent.assert_not_called()


@pytest.mark.asyncio
async def test_anonymous_blank_header_key_also_refused():
    req = _mock_request(header_key="")

    result = await process_intent(req, current_user=None)

    assert result["error_type"] == "anonymous_key_required"
    req.app.state.intent_service.process_intent.assert_not_called()


@pytest.mark.asyncio
async def test_anonymous_with_byoc_header_key_still_reaches_intent_service():
    """The whole point of #1162 (BYOC needs no login) must be UNCHANGED."""
    req = _mock_request(header_key="sk-byoc-key")
    mock_result = MagicMock(
        message="hi there",
        intent_data={},
        workflow_id=None,
        requires_clarification=False,
        clarification_type=None,
        suggestions=[],
        preferences={},
        error=None,
        error_type=None,
        async_work_started=False,
    )
    req.app.state.intent_service.process_intent = AsyncMock(return_value=mock_result)

    result = await process_intent(req, current_user=None)

    req.app.state.intent_service.process_intent.assert_awaited_once()
    assert result.get("error_type") != "anonymous_key_required"
    assert result["message"] == "hi there"
