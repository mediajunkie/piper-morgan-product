"""Arch 2026-11-18 (the card-state file's disconnect slice): a disconnect that raises
answers with the incomplete line from the one helper, never the exception's text; and
every disconnect reply carries a stable outcome code (cleared, revoke_failed, incomplete)
for Disconnect All to count on.

Layer: the four route functions, with the one clearing call under them stubbed.
"""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.connectors.disconnect import DisconnectResult
from web.api.routes import settings_integrations as routes

SENTINEL = "postgres://u:SENTINEL-TOKEN-FRAGMENT@db.internal/x"
ROUTES = {
    "slack": ("disconnect_slack", "Slack"),
    "calendar": ("disconnect_calendar", "Google Calendar"),
    "notion": ("disconnect_notion", "Notion"),
    "github": ("disconnect_github", "GitHub"),
}
WHO = SimpleNamespace(sub="user-1")


async def _reply(card, clearing):
    fn = getattr(routes, ROUTES[card][0])
    with patch("services.connectors.disconnect.disconnect_connector", new=clearing):
        reply = await fn(current_user=WHO)
    if hasattr(reply, "status_code") and hasattr(reply, "body"):
        return reply.status_code, json.loads(reply.body)
    return 200, reply


@pytest.mark.asyncio
@pytest.mark.parametrize("card", sorted(ROUTES))
async def test_a_raised_disconnect_answers_the_incomplete_line_and_no_error_text(card):
    async def clearing(user, connector):
        raise RuntimeError(SENTINEL)

    status, body = await _reply(card, clearing)
    line = routes.DISCONNECT_INCOMPLETE_LINE.format(service=ROUTES[card][1])
    assert status == 503 and body["success"] is False
    assert body["detail"] == line and body["outcome"] == "incomplete"
    assert "SENTINEL" not in json.dumps(body)


@pytest.mark.asyncio
@pytest.mark.parametrize("card", sorted(ROUTES))
@pytest.mark.parametrize(
    "remaining,revoke_failed,status,outcome",
    [
        ((), False, 200, "cleared"),
        (("a stored copy",), False, 503, "incomplete"),
    ],
)
async def test_every_reply_carries_its_outcome_code(
    card, remaining, revoke_failed, status, outcome
):
    async def clearing(user, connector):
        return DisconnectResult(connector, remaining, revoke_failed)

    got_status, body = await _reply(card, clearing)
    assert got_status == status and body["outcome"] == outcome


@pytest.mark.asyncio
@pytest.mark.parametrize("card", ["slack", "calendar", "github"])
async def test_a_failed_provider_revoke_is_its_own_outcome(card):
    async def clearing(user, connector):
        return DisconnectResult(connector, (), True)

    status, body = await _reply(card, clearing)
    assert status == 200 and body["success"] is True and body["outcome"] == "revoke_failed"
