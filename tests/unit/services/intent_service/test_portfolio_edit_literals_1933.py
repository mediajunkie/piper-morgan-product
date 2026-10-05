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

from unittest.mock import AsyncMock, patch

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
        # CXO's 2026-10-04 ruling §2: verbatim copy, no "yet".
        assert "I can't edit a project's details from chat" in result["message"]
        # Must NOT be the generic multi-line "portfolio_help" menu.
        assert result["intent"]["action"] == "edit_project_unavailable"
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


class TestEditUpdatePrecedence:
    """CXO's #1930 §2 precedence ruling: the edit/update sniff must claim
    the turn BEFORE the list/add/search (and archive/restore/delete)
    operation sniffs below it, because a message can carry both an
    edit/update verb AND a literal that one of the later sniffs would also
    match (e.g. "add" inside "edit my project and add a note"). The sniff
    uses a leading-verb heuristic (edit/update must be the FIRST token)
    rather than a bare substring check, specifically to avoid a DIFFERENT
    false positive: "add a project to update later" is a genuine add
    request that merely mentions "update" downstream of its real verb."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message",
        [
            "edit my project description",
            "update my project name to Atlas",
        ],
    )
    async def test_true_positives_get_the_honest_reply(self, handler, message):
        result = await handler._handle_portfolio_query(_intent(message), "s1", user_id="u1")
        assert result["intent"]["action"] == "edit_project_unavailable"

    @pytest.mark.asyncio
    async def test_edit_wins_over_a_co_occurring_add_literal(self, handler):
        """The precedence case CXO's ruling is actually about: "add" is a
        literal substring of this message, but the edit verb leads it and
        must claim the turn first -- the add branch must never run."""
        result = await handler._handle_portfolio_query(
            _intent("edit my project and add a note"), "s1", user_id="u1"
        )
        assert result["intent"]["action"] == "edit_project_unavailable"

    @pytest.mark.asyncio
    async def test_plain_add_is_unaffected(self, handler):
        """No edit/update word at all -- must reach the add branch, not the
        edit_project_unavailable floor."""
        with patch.object(
            CanonicalHandlers,
            "_handle_add_project",
            AsyncMock(return_value={"intent": {"action": "_sentinel_add"}}),
        ) as mocked:
            result = await handler._handle_portfolio_query(
                _intent("add a project called Foo"), "s1", user_id="u1"
            )
        mocked.assert_awaited_once()
        assert result["intent"]["action"] == "_sentinel_add"

    @pytest.mark.asyncio
    async def test_plain_archive_is_unaffected(self, handler):
        """No edit/update word at all -- must reach the archive branch, not
        the edit_project_unavailable floor."""
        with patch.object(
            CanonicalHandlers,
            "_handle_archive_project",
            AsyncMock(return_value={"intent": {"action": "_sentinel_archive"}}),
        ) as mocked:
            result = await handler._handle_portfolio_query(
                _intent("archive my project Foo"), "s1", user_id="u1"
            )
        mocked.assert_awaited_once()
        assert result["intent"]["action"] == "_sentinel_archive"

    @pytest.mark.asyncio
    async def test_add_mentioning_update_downstream_is_not_a_false_positive(self, handler):
        """ "update" is a literal substring of this message, but it is not
        the LEADING verb -- "add" is. The leading-verb heuristic (not a
        bare substring check) must let this fall through to the add
        branch, not misclaim it as an edit/update ask."""
        with patch.object(
            CanonicalHandlers,
            "_handle_add_project",
            AsyncMock(return_value={"intent": {"action": "_sentinel_add"}}),
        ) as mocked:
            result = await handler._handle_portfolio_query(
                _intent("add a project to update later"), "s1", user_id="u1"
            )
        mocked.assert_awaited_once()
        assert result["intent"]["action"] == "_sentinel_add"


class TestPortfolioPatternsLiteralsSurvive:
    """The literals Arch's original ruling would have deleted are still
    live in the pre-classifier (PPM/CXO/Arch's agreed outcome: keep them,
    option (a))."""

    def test_update_edit_literals_still_present(self):
        from services.intent_service.pre_classifier import PreClassifier

        src = "".join(PreClassifier.PORTFOLIO_PATTERNS)
        assert "update" in src
        assert "edit" in src


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        "please edit my project description",
        "can you update my project name to Atlas",
        "hey piper, edit the project",
    ],
)
async def test_courtesy_prefixed_edit_still_gets_the_honest_reply(handler, message):
    """Lead 2026-10-04: courtesy words before the verb don't hide the edit ask
    (otherwise the PORTFOLIO literal claims the turn and the user gets the
    generic help menu, not the honest 'can't edit' reply)."""
    result = await handler._handle_portfolio_query(_intent(message), "s1", user_id="u1")
    assert result["intent"]["action"] == "edit_project_unavailable"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "message",
    [
        "I want to edit my project and add a note",
        "let me edit my project and add a description",
        "I'd like to update my project and add a repo",
    ],
)
async def test_intent_prefixed_edit_never_reaches_add(handler, message):
    """CXO 2026-10-04 residual: measured, all three reached the add sniff
    (a WRITE that creates a project) before this fix."""
    with patch.object(
        CanonicalHandlers,
        "_handle_add_project",
        AsyncMock(side_effect=AssertionError("add must not run for an edit ask")),
    ):
        result = await handler._handle_portfolio_query(_intent(message), "s1", user_id="u1")
    assert result["intent"]["action"] == "edit_project_unavailable"


@pytest.mark.asyncio
async def test_add_with_intent_prefix_still_adds(handler):
    """'I want to add a project called Foo' still reaches add (no edit verb)."""
    with patch.object(
        CanonicalHandlers,
        "_handle_add_project",
        AsyncMock(return_value={"message": "ok", "intent": {"action": "ADD"}}),
    ) as add:
        await handler._handle_portfolio_query(
            _intent("I want to add a project called Foo"), "s1", user_id="u1"
        )
    assert add.await_count == 1
