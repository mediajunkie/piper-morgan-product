"""#1933 (Arch's 2026-10-04 ruling §2, endorsing Lead's finding) + #1932.

Arch's own "dead claims, delete" ruling on the PORTFOLIO_PATTERNS
"update project"/"edit project" literals was wrong: deleting them sends
"edit my project description" to update_document_query 10/10 on both legs
(a WRITE on the wrong object), per Lead's surface-2 probe. The literals
are protective, not dead — they hold a write-shaped ask away from a write
it doesn't belong to. Option (a): keep the literals, give
``_handle_portfolio_query``'s update/edit case an honest, non-arming
reply instead of the generic "portfolio_help" fallback it used to fall
into (inventory row 12).
"""

from __future__ import annotations

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.shared_types import IntentCategory


def _intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_portfolio",
        confidence=1.0,
        context={"original_message": message},
    )


@pytest.fixture
def handler():
    return CanonicalHandlers()


class TestUpdateEditGetsHonestReply:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message",
        [
            "update my project",
            "update the project",
            "edit my project",
            "edit the project",
        ],
    )
    async def test_honest_floor_reply_not_the_generic_fallback(self, handler, message):
        result = await handler._handle_portfolio_query(_intent(message), "s1", user_id="u1")
        assert "I can't edit projects yet" in result["message"]
        # Must NOT be the generic multi-line "portfolio_help" menu.
        assert result["intent"]["action"] == "edit_unavailable"
        assert result["intent"]["action"] != "portfolio_help"

    @pytest.mark.asyncio
    async def test_arms_nothing(self, handler):
        result = await handler._handle_portfolio_query(
            _intent("edit my project"), "s1", user_id="u1"
        )
        assert result["requires_clarification"] is False
        assert "awaiting_confirmation" not in result["intent"].get("context", {})

    @pytest.mark.asyncio
    async def test_reply_is_not_interrogative(self, handler):
        """Imperative/declarative copy only — the #1766 ratchet forbids a
        new unarmed question-emitting site."""
        result = await handler._handle_portfolio_query(
            _intent("update my project"), "s1", user_id="u1"
        )
        assert not result["message"].rstrip().endswith("?")


class TestPortfolioPatternsLiteralsSurvive:
    """The literals Arch's original ruling would have deleted are still
    live in the pre-classifier (PPM/CXO/Arch's agreed outcome: keep them,
    option (a))."""

    def test_update_edit_literals_still_present(self):
        from services.intent_service.pre_classifier import PreClassifier

        src = "".join(PreClassifier.PORTFOLIO_PATTERNS)
        assert "update" in src
        assert "edit" in src
