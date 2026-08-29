"""#1543 — create_issue titles the SUBJECT, never the raw command.

Live evidence (PM retest, 2026-08-09): created issue #108's title was
``Issue: create an issue in mediajunkie/test-piper-morgan a`` — the raw command
captured by the fallback ``f"Issue: {original_message[:50]}"`` and truncated
mid-word.

Verify-first finding: an "about X" extraction NEVER existed. Git history of
``_slotfill_issue_request`` (042cee411 introduced it, ff9febf01 added the
quoted to-form; ``git log -S/-G`` over services/intent/intent_service.py shows
no other versions) contains titled/colon/quoted-to forms only — while the
#1212 no-repo degrade copy has been TEACHING the about-form the whole time
('… tell me which one — e.g. "create an issue in owner/repo about testing."').

Contract pinned here:
1. "create an issue [in owner/repo] about X" → title X (the promised form).
2. Unquoted to-form: "change the title of issue #N to X" → title X (the quoted
   to-form #1386-B3' required quotes; PM's natural phrasing has none).
3. No extractable subject → ASK (the #1490 honest-ask shape: ask rather than
   guess), never ship a garbage raw-command title.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"

# PM's verbatim command shape (2026-08-09; #108's fallback title is byte-exact
# for this prefix: 'Issue: create an issue in mediajunkie/test-piper-morgan a').
PM_CREATE = "create an issue in mediajunkie/test-piper-morgan about testing regressions"
PM_UPDATE = "change the title of issue #108 to test new regressions"


def _slotfill():
    from services.intent.intent_service import IntentService

    return IntentService._slotfill_issue_request


def _create_intent(message):
    return Intent(
        original_message=message,
        category=IntentCategory.EXECUTION,
        action="create_issue",
        confidence=0.95,
        context={},  # what production actually delivers (#1220)
    )


@pytest.fixture
def svc():
    from services.intent.intent_service import IntentService

    return IntentService()


class TestAboutFormExtraction:
    def test_pm_verbatim_extracts_subject_and_repo(self):
        slots = _slotfill()(PM_CREATE)
        assert slots["repository"] == "mediajunkie/test-piper-morgan"
        assert slots["title"] == "testing regressions"

    def test_bare_about_form(self):
        assert _slotfill()("create an issue about login bugs")["title"] == "login bugs"

    def test_trailing_repo_clause_is_routing_not_subject(self):
        slots = _slotfill()("create an issue about flaky login tests in acme/widgets")
        assert slots["repository"] == "acme/widgets"
        assert slots["title"] == "flaky login tests"

    def test_quoted_titled_form_still_wins_over_about(self):
        slots = _slotfill()('create an issue about performance titled "P1: slow dashboards"')
        assert slots["title"] == "P1: slow dashboards"

    def test_no_issue_word_no_about_capture(self):
        # "what about 7/9 planning" must not grow a title (no issue/ticket word)
        assert "title" not in _slotfill()("what about 7/9 planning")


class TestUnquotedToFormExtraction:
    def test_pm_verbatim_update_title(self):
        assert _slotfill()(PM_UPDATE)["title"] == "test new regressions"

    def test_quoted_to_form_still_extracts_exactly(self):
        # 1386-B3' regression pin: quotes still win, quote marks stripped
        msg = "change the title of issue #107 to 'Implement full-text search'"
        assert _slotfill()(msg)["title"] == "Implement full-text search"


class TestCreateHandlerHonestAsk:
    pytestmark = pytest.mark.asyncio

    async def test_no_subject_asks_instead_of_garbage_title(self, svc):
        """The #1490 shape: no extractable subject → ask, never title the
        issue with the raw command. No write may fire."""
        intent = _create_intent("create an issue in mediajunkie/test-piper-morgan")
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1")
        w.assert_not_awaited()
        assert result.requires_clarification is True
        assert "Issue:" not in result.message
        assert "about" in result.message  # the ask teaches the working form

    async def test_pm_verbatim_creates_with_subject_title(self, svc):
        created = {"number": 109, "html_url": "https://x/109", "title": "testing regressions"}
        intent = _create_intent(PM_CREATE)
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1")
        assert result.success
        w.assert_awaited_once()
        kwargs = w.await_args.kwargs
        assert kwargs["title"] == "testing regressions"
        assert not kwargs["title"].startswith("Issue:")
        assert kwargs["owner"] == "mediajunkie"
        assert kwargs["repo_name"] == "test-piper-morgan"

    async def test_explicit_context_title_still_wins(self, svc):
        intent = _create_intent(PM_CREATE)
        intent.context = {"title": "Explicit title", "repository": "acme/widgets"}
        created = {"number": 5, "html_url": "u", "title": "Explicit title"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1")
        assert result.success
        assert w.await_args.kwargs["title"] == "Explicit title"


class TestRawCaptureKilledEverywhere:
    """#1543 REWORK (PM live round 2026-08-29, v64): the raw-capture MOVED.

    PM's verbatim 'create an issue about the login timeout in
    test-piper-morgan' produced test-piper-morgan#111 with title
    'the login timeout in test-piper-morgan' (the bare repo-routing phrase
    leaked in — no slash, no "repository" word, so extraction-time
    stripping could not know it was a repo) and body = the raw command
    verbatim (the `or intent.original_message` description fallback).

    Contract pinned here:
    1. Once the routed repo is known, a trailing phrase NAMING it is
       stripped from the title (named-resolved OR default-coinciding).
    2. The body is NEVER the raw command: no described content → empty.
    3. A trailing phrase naming anything else is honest content — kept.
    """

    pytestmark = pytest.mark.asyncio

    PM_V64 = "create an issue about the login timeout in test-piper-morgan"
    DEFAULT_REPO = "mediajunkie/test-piper-morgan"
    RESOLVER = "services.integrations.github.repo_resolver.get_user_default_repo"
    USER = "3f7b8a52-1543-4b00-9e00-000000001543"

    async def _create(self, svc, message):
        created = {"number": 111, "html_url": "https://x/111", "title": "t"}
        intent = _create_intent(message)
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
            patch(self.RESOLVER, new=AsyncMock(return_value=self.DEFAULT_REPO)),
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1", user_id=self.USER)
        return result, w

    async def test_pm_verbatim_v64_title_clean_body_empty(self, svc):
        """PM's exact v64 command: the repo phrase is routing (it names the
        routed repo), so the title is 'the login timeout' — and the body is
        empty, never the command echoed back."""
        result, w = await self._create(svc, self.PM_V64)
        assert result.success
        w.assert_awaited_once()
        kwargs = w.await_args.kwargs
        assert kwargs["title"] == "the login timeout"
        assert kwargs["body"] == ""
        assert self.PM_V64 not in kwargs["body"]
        assert kwargs["owner"] == "mediajunkie"
        assert kwargs["repo_name"] == "test-piper-morgan"

    async def test_repo_phrase_mid_sentence_stays_clean(self, svc):
        result, w = await self._create(
            svc, "create an issue in test-piper-morgan about the login timeout"
        )
        kwargs = w.await_args.kwargs
        assert kwargs["title"] == "the login timeout"
        assert kwargs["body"] == ""

    async def test_no_repo_phrase(self, svc):
        result, w = await self._create(svc, "create an issue about the login timeout")
        kwargs = w.await_args.kwargs
        assert kwargs["title"] == "the login timeout"
        assert kwargs["body"] == ""

    async def test_actual_description_after_comma_lands_in_body(self, svc):
        """Real described content IS the body — the raw-command ban never
        swallows a description the user actually gave."""
        result, w = await self._create(
            svc,
            "create an issue about the login timeout in test-piper-morgan, "
            "and the description is sessions expire after 5 min",
        )
        kwargs = w.await_args.kwargs
        assert kwargs["title"] == "the login timeout"
        assert kwargs["body"] == "sessions expire after 5 min"

    async def test_phrase_naming_a_non_repo_is_kept(self, svc):
        """'in production' names no repo we route to — it is content, and
        guessing it away would mangle honest titles."""
        result, w = await self._create(svc, "create an issue about the login timeout in production")
        kwargs = w.await_args.kwargs
        assert kwargs["title"] == "the login timeout in production"
        assert kwargs["body"] == ""

    async def test_owner_qualified_trailing_phrase_also_stripped(self, svc):
        result, w = await self._create(
            svc,
            "create an issue about the login timeout in mediajunkie/test-piper-morgan",
        )
        kwargs = w.await_args.kwargs
        assert kwargs["title"] == "the login timeout"
        assert kwargs["body"] == ""


class TestStripRepoPhraseForHelper:
    """The pure helper (SUPERSESSION note: extraction stays pure so it
    lifts into the SessionSnapshot draft-state consumers)."""

    def _strip(self):
        from services.intent_service.repo_clarification import (
            strip_repo_phrase_for,
        )

        return strip_repo_phrase_for

    def test_bare_name_match_stripped(self):
        assert (
            self._strip()("the login timeout in test-piper-morgan", "mediajunkie/test-piper-morgan")
            == "the login timeout"
        )

    def test_case_insensitive(self):
        assert (
            self._strip()("the login timeout in Test-Piper-Morgan", "mediajunkie/test-piper-morgan")
            == "the login timeout"
        )

    def test_non_matching_name_untouched(self):
        title = "the login timeout in production"
        assert self._strip()(title, "mediajunkie/test-piper-morgan") == title

    def test_phrase_only_title_never_emptied(self):
        title = "in test-piper-morgan"
        assert self._strip()(title, "mediajunkie/test-piper-morgan") == title

    def test_no_repository_is_a_passthrough(self):
        assert self._strip()("the login timeout", None) == "the login timeout"
        assert self._strip()("the login timeout", "notaslashrepo") == ("the login timeout")

    def test_mid_title_mention_is_not_stripped(self):
        # Only a TRAILING clause is routing; a mid-title mention is content.
        title = "the test-piper-morgan deploy fails on login"
        assert self._strip()(title, "mediajunkie/test-piper-morgan") == title


class TestUpdateHandlerEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_b3_resolved_update_carries_unquoted_title(self, svc):
        """The #1411 emit + #1543 extraction together: a B3-resolved intent for
        PM's verbatim update must reach github_router.update_issue with the
        unquoted new title — not fail 'no fields to update'."""
        intent = Intent(
            original_message=PM_UPDATE,
            category=IntentCategory.QUERY,
            action="update_issue",
            confidence=1.0,
            context={
                "original_message": PM_UPDATE,
                "repository": "mediajunkie/test-piper-morgan",
                "issue_number": 108,
                "b3_resolved": True,
            },
        )
        updated = {"number": 108, "title": "test new regressions", "state": "open"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=updated)) as w,
        ):
            result = await svc._handle_update_issue(intent, "wf-1", user_id="u-1")
        assert result.success
        w.assert_awaited_once()
        kwargs = w.await_args.kwargs
        assert kwargs["issue_number"] == 108
        assert kwargs["title"] == "test new regressions"
        assert kwargs["owner"] == "mediajunkie"
        assert kwargs["repo_name"] == "test-piper-morgan"
