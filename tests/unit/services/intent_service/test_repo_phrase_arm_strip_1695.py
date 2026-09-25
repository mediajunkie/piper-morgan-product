"""#1695 — compose-framed draft's armed subject still carries the bare
repo-routing phrase ("...in test-piper-morgan").

Repro (PM's live shape, driven through the real #1510 collaborate-gate ARM
path — ``IntentService._handle_create_issue``, `tests/unit/services/
intent_service/test_collaboration_gate_1510.py`'s harness):

    "draft an issue about the login bug in test-piper-morgan"

armed a pending ``drafted_issue`` offer whose subject was still "the login
bug **in test-piper-morgan**" — the #1543/#1649 rework's
``strip_repo_phrase_for`` only runs on the FINALIZED execute/file path (once
``repository`` resolves, deep in ``_handle_create_issue``'s non-gated
branch), which is AFTER the draft has already been echoed to the user in the
collaboration response and stored in the offer.

Scope note from the issue (2026-08-29): "strip_repo_phrase_for applies
where the target repo is FINALIZED... The collaborate-gate ARM path doesn't
resolve bare repo names." Fix direction chosen here: **resolve-or-strip at
arm time**, using the SAME resolver the execute path falls back to when no
repo is named — ``get_user_default_repo`` (a DB read via
``ConnectorConfigService``, not a GitHub connector/network call, so this
holds the gate's own "drafting together needs no connector" invariant). An
already-extracted slash-form repo (from ``_slotfill_issue_request``,
zero-cost) is tried first; the default-repo DB read only runs when that
comes back empty. No new regex: reuses ``strip_repo_phrase_for`` verbatim,
the same function the execute path already calls (#1543/#1649).

A bare name that ISN'T the resolved target (no default configured, or the
default doesn't match the phrase) is left untouched — never guessed at,
same "never guess" discipline ``strip_repo_phrase_for`` already documents.
"""

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory

GATE = "services.intent_service.collaboration_gate"
ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
DEFAULT_REPO = "services.integrations.github.repo_resolver.get_user_default_repo"


def _intent(message, action="create_ticket"):
    return Intent(
        original_message=message,
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.95,
        context={},
    )


@pytest.fixture
def svc():
    return IntentService()


async def _arm(svc, message, *, default_repo, user_id=None):
    """Drive the real #1510 ARM path and return (result, armed offer)."""
    user_id = user_id or str(uuid4())
    intent = _intent(message)
    with (
        patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        patch(DEFAULT_REPO, new=AsyncMock(return_value=default_repo)),
    ):
        result = await svc._handle_create_issue(intent, "wf-1", "sess-1", user_id=user_id)
    w.assert_not_awaited()  # still a draft, never a write
    offer = svc.workflow_offer_service.peek_pending_offer("sess-1", user_id=user_id)
    return result, offer


@pytest.mark.asyncio
class TestArmTimeRepoPhraseStrip:
    async def test_bare_repo_phrase_stripped_when_it_matches_default(self, svc):
        """The live #1695 repro: bare 'in test-piper-morgan' matches the
        user's configured default repo — the armed subject must NOT carry
        the routing phrase, in the message copy OR the stored draft."""
        result, offer = await _arm(
            svc,
            "draft an issue about the login bug in test-piper-morgan",
            default_repo="mediajunkie/test-piper-morgan",
        )
        assert offer is not None
        assert offer["pending_action"]["draft"]["title"] == "the login bug"
        assert offer["pending_action"]["intent"].context["title"] == "the login bug"
        assert "in test-piper-morgan" not in result.message
        assert "the login bug" in result.message

    async def test_compose_framed_subject_with_no_repo_phrase_stays_clean(self, svc):
        """Pin: a subject with nothing to strip is untouched (no over-eager
        stripping of ordinary trailing words)."""
        result, offer = await _arm(
            svc,
            "draft an issue about the login bug",
            default_repo="mediajunkie/test-piper-morgan",
        )
        assert offer["pending_action"]["draft"]["title"] == "the login bug"
        assert "the login bug" in result.message

    async def test_in_x_that_is_not_the_target_repo_is_untouched(self, svc):
        """Red-first pin: 'in production' is prose, not repo routing, when
        it doesn't match the resolved default — never guessed at."""
        result, offer = await _arm(
            svc,
            "draft an issue about the bug in production",
            default_repo="mediajunkie/test-piper-morgan",
        )
        assert offer["pending_action"]["draft"]["title"] == "the bug in production"
        assert "the bug in production" in result.message

    async def test_no_default_repo_configured_leaves_phrase_untouched(self, svc):
        """No resolver signal at all (no default set) means no strip — the
        gate's 'never guess' discipline, same failure mode file-time already
        has for an unresolvable name (#1695 doesn't widen that gap)."""
        result, offer = await _arm(
            svc,
            "draft an issue about the login bug in test-piper-morgan",
            default_repo=None,
        )
        assert offer["pending_action"]["draft"]["title"] == "the login bug in test-piper-morgan"
        assert "in test-piper-morgan" in result.message

    async def test_explicit_slash_form_never_calls_default_resolver(self, svc):
        """An explicit owner/repo in the message is already extracted by
        _slotfill_issue_request (zero-cost) — the default-repo DB read must
        not even be consulted in that case."""
        user_id = str(uuid4())
        intent = _intent("draft an issue about the login bug in mediajunkie/test-piper-morgan")
        with (
            patch(f"{GATE}._load_preferences", new=AsyncMock(return_value={})),
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()),
            patch(DEFAULT_REPO, new=AsyncMock()) as default_mock,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1", user_id=user_id)
        default_mock.assert_not_awaited()
        offer = svc.workflow_offer_service.peek_pending_offer("sess-1", user_id=user_id)
        assert offer["pending_action"]["draft"]["title"] == "the login bug"
        # The repo is legitimately echoed elsewhere in the response (it's
        # the explicit target, not a routing-phrase leak) — only the TITLE
        # line must be clean of the routing phrase.
        assert "**Title**: the login bug\n" in result.message
