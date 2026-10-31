"""#2237 (CXO 2026-10-30 20:5x): the general "connect my integrations" listing follows
BETA_OFFERED_CONNECTORS. Slack and Notion are never listed under "Not connected yet"
(that invites a connect the page and the server refuse); the list equals the offered
set minus what is connected. One source of truth with the page's cards and the
capability block."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest

from services.integrations import integration_status_service as iss
from services.intent_service.canonical_handlers import CanonicalHandlers
from tests.unit.services.intent_service.test_integration_status_answer_2093 import (
    SEAM,
    _off,
    _ok,
)

GENERAL = "connect my integrations"


async def _listing(statuses):
    handlers = CanonicalHandlers()
    with patch(SEAM, new=AsyncMock(return_value=statuses)):
        return await handlers._format_integration_setup_guidance("u1", original_message=GENERAL)


def _block(out) -> str:
    text = out["message"] if isinstance(out, dict) else str(out)
    assert "Not connected yet" in text, text
    return text.split("Not connected yet", 1)[1]


@pytest.mark.asyncio
async def test_not_connected_list_names_only_the_offered_set():
    text = await _listing({"github": _off(), "slack": _off(), "calendar": _off(), "notion": _off()})
    block = _block(text)
    assert "GitHub" in block and "Google Calendar" in block
    assert "Slack" not in block and "Notion" not in block


@pytest.mark.asyncio
async def test_not_connected_list_is_the_offered_set_minus_connected():
    text = await _listing(
        {"github": _ok("oauth_binding"), "slack": _off(), "calendar": _off(), "notion": _off()}
    )
    block = _block(text)
    assert "Google Calendar" in block
    assert "GitHub" not in block
    assert "Slack" not in block and "Notion" not in block


@pytest.mark.asyncio
async def test_listing_follows_the_constant(monkeypatch):
    monkeypatch.setattr(iss, "BETA_OFFERED_CONNECTORS", {"github": "GitHub"})
    text = await _listing({"github": _off(), "slack": _off(), "calendar": _off(), "notion": _off()})
    block = _block(text)
    assert "GitHub" in block
    assert "Google Calendar" not in block
