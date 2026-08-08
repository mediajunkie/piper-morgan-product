"""#1520: an EXPIRED session must not be blamed on the user's missing API key.

PM's live failure (2026-08-08): session expired silently mid-use; the chat
accepted a typed message and answered "I can't process this without you being
signed in or supplying your own Anthropic API key" — wrong-blame copy served to
a signed-in user of the hosted app whose token had simply expired.

Mechanism: `get_current_user_optional` catches TokenExpired and sets
`request.state.auth_expired = True` (#840), but the #1320 anonymous-key gate
returns `_create_anonymous_key_required_response` EARLY — before the normal
response dict that carries `auth_expired` is built. So the #840 signal was
dropped on exactly the path it was built for.

The contract pinned here:
- token-present-but-expired → `error_type: "session_expired"`, honest
  "your session expired, sign in again" copy, `auth_expired: True` so the
  frontend can act — and NO key-talk.
- genuinely anonymous (no token at all) → the #1320 key copy, unchanged.
Both refuse BEFORE touching IntentService/the LLM.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from web.api.routes.intent import process_intent


def _mock_request(message="hello", header_key=None, auth_expired=False):
    req = MagicMock()
    req.json = AsyncMock(return_value={"message": message, "session_id": "s1"})
    req.headers = MagicMock()
    req.headers.get = MagicMock(
        side_effect=lambda k, default=None: (
            header_key if k == "X-User-Api-Key" else default
        )
    )
    req.cookies = {}
    # Real attribute semantics for request.state — a bare MagicMock would make
    # getattr(state, "auth_expired", False) truthy and poison the assertions.
    req.state = SimpleNamespace(**({"auth_expired": True} if auth_expired else {}))
    req.app.state.intent_service = MagicMock()
    return req


@pytest.mark.asyncio
async def test_expired_session_gets_session_expired_not_key_blame():
    """The #1520 fix itself: expired token → honest session-expired response."""
    req = _mock_request(auth_expired=True)

    result = await process_intent(req, current_user=None)

    assert result["error_type"] == "session_expired"
    assert "session" in result["message"].lower()
    assert "expired" in result["message"].lower()
    assert "sign in" in result["message"].lower()
    # The wrong-blame copy must be gone from this path entirely.
    assert "api key" not in result["message"].lower()
    assert all("api key" not in s.lower() for s in result["suggestions"])
    # Frontend signal (#840) survives the early return now.
    assert result["auth_expired"] is True
    # Refused before touching the LLM layer.
    req.app.state.intent_service.process_intent.assert_not_called()


@pytest.mark.asyncio
async def test_genuinely_anonymous_caller_still_gets_key_copy():
    """#1320 unchanged: no token at all → the sign-in-or-bring-a-key copy."""
    req = _mock_request(auth_expired=False)

    result = await process_intent(req, current_user=None)

    assert result["error_type"] == "anonymous_key_required"
    req.app.state.intent_service.process_intent.assert_not_called()


@pytest.mark.asyncio
async def test_expired_session_with_byoc_header_still_processes():
    """BYOC (own key in header) works even with an expired cookie — the key
    wins per #1162; expiry is signaled via auth_expired on the response."""
    req = _mock_request(header_key="sk-byoc-key", auth_expired=True)
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
    assert result["message"] == "hi there"
    assert result["auth_expired"] is True
