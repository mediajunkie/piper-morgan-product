"""#1588 — the conversation handler's principal reads: threaded param wins, context fills in.

The #1588 audit of services/conversation/conversation_handler.py found exactly two principal
reads (respond and _respond_to_greeting — the pair #1536 fixed) and no siblings. Both used
``context OR param``, which stops DROPPING the param (the #1536 bug) but still lets a derived
context value OVERRIDE the caller's authenticated principal when the two differ. The threaded
param comes from the auth dependency; intent.context is derived state. Precedence is now
``param OR context``.

LAYER (m-43): the handler's own entry with the greeting body patched at its seam — what's under
test is which principal reaches it. DENOMINATOR: both reads in the file (2 of 2 found by
`grep -n '.get("user_id"'`); the persist helper takes user_id directly and is not a read.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.conversation.conversation_handler import ConversationHandler
from services.domain.models import Intent
from services.shared_types import IntentCategory

pytestmark = pytest.mark.asyncio


def _greeting(ctx_user):
    return Intent(
        category=IntentCategory.QUERY,
        action="greeting",
        confidence=1.0,
        context={"user_id": ctx_user} if ctx_user else {},
    )


class TestThreadedPrincipalWins:
    async def test_param_beats_a_differing_context_principal(self):
        """THE #1588 pin: authenticated param 'p' vs derived context 'c' → 'p' reaches the body."""
        h = ConversationHandler()
        with patch.object(h, "_respond_to_greeting", AsyncMock(return_value={})) as body:
            await h.respond(_greeting("c-derived"), "sess", user_id="p-authenticated")
        body.assert_awaited_once()
        assert body.await_args.kwargs["user_id"] == "p-authenticated"

    async def test_context_fills_in_when_no_param(self):
        """#1536's guarantee kept: a missing param falls back to context, never to None."""
        h = ConversationHandler()
        with patch.object(h, "_respond_to_greeting", AsyncMock(return_value={})) as body:
            await h.respond(_greeting("c-derived"), "sess", user_id=None)
        assert body.await_args.kwargs["user_id"] == "c-derived"

    async def test_neither_yields_none_not_a_crash(self):
        h = ConversationHandler()
        with patch.object(h, "_respond_to_greeting", AsyncMock(return_value={})) as body:
            await h.respond(_greeting(None), "sess", user_id=None)
        assert body.await_args.kwargs["user_id"] is None
