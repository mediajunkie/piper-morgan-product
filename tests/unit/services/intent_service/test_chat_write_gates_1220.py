"""#1220/#1382 — chat write handlers must use the binding-aware gate + the guarded router.

The miss these tests pin (found live 2026-07-09, PM's first-real-write attempt):
``_handle_create_issue``/``_handle_update_issue`` gated on GITHUB_TOKEN/PAT only —
telling OAuth-connected users "GitHub isn't connected" — and then called the legacy
``GitHubDomainService`` directly, bypassing the #1220 connector-first router writes
and their #1322 read-back guard entirely. "Building a feature Piper can't use is
not done" (PM, 2026-07-09).

Contract pinned here:
1. The gate is ``GitHubIntegrationRouter.is_available()`` (binding OR PAT) — no
   env/keychain PAT check in the handler.
2. The write goes through ``github_router.create_issue``/``update_issue`` (the
   guarded, connector-first methods) — never ``GitHubDomainService`` directly.
3. A fired-but-unverified connector write surfaces honest uncertainty verbatim.
"""

from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


def _intent(action="create_issue", **ctx):
    defaults = {"title": "Test issue", "repository": "acme/widgets"}
    defaults.update(ctx)
    return Intent(
        original_message="create an issue",
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.95,
        context=defaults,
    )


@pytest.fixture
def svc():
    from services.intent.intent_service import IntentService

    return IntentService()


class TestCreateIssueGate:
    @pytest.mark.asyncio
    async def test_oauth_binding_passes_gate_and_write_goes_through_router(self, svc):
        """A user with ONLY an OAuth binding (no PAT anywhere) must reach the
        guarded router write — the exact case the legacy gate refused."""
        created = {"number": 7, "html_url": "https://x/7", "title": "Test issue"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            result = await svc._handle_create_issue(_intent(), "wf-1", "sess-1")
        assert result.success
        assert "#7" in result.message
        w.assert_awaited_once()
        kwargs = w.await_args.kwargs
        assert kwargs["owner"] == "acme" and kwargs["repo_name"] == "widgets"

    @pytest.mark.asyncio
    async def test_unavailable_degrades_with_settings_guidance(self, svc):
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=False)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock()) as w,
        ):
            result = await svc._handle_create_issue(_intent(), "wf-1", "sess-1")
        assert "Settings" in result.message and "Integrations" in result.message
        w.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_unverified_write_surfaces_honest_uncertainty(self, svc):
        boom = RuntimeError(
            "GitHub write could not be verified — it may or may not have landed. "
            "Check the repository directly before retrying; do not assume success."
        )
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(side_effect=boom)),
        ):
            result = await svc._handle_create_issue(_intent(), "wf-1", "sess-1")
        assert "may or may not" in result.message
        assert "duplicate" in result.message


class TestUpdateIssueGate:
    @pytest.mark.asyncio
    async def test_update_goes_through_router(self, svc):
        updated = {"number": 42, "title": "New title"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.update_issue", new=AsyncMock(return_value=updated)) as w,
        ):
            result = await svc._handle_update_issue(
                _intent(action="update_issue", issue_number=42, title="New title"),
                "wf-1",
            )
        assert result.success and "#42" in result.message
        w.assert_awaited_once()
        assert w.await_args.kwargs["owner"] == "acme"

    @pytest.mark.asyncio
    async def test_update_unavailable_degrades(self, svc):
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=False)),
        ):
            result = await svc._handle_update_issue(
                _intent(action="update_issue", issue_number=42, title="t"), "wf-1"
            )
        assert "Settings" in result.message


class TestRouterIsAvailable:
    """The gate itself: OAuth binding (BOUND) OR legacy PAT — either suffices."""

    def _router(self, user_id="694d8f4e-0000-0000-0000-000000000042"):
        from services.integrations.github.github_integration_router import (
            GitHubIntegrationRouter,
        )

        r = GitHubIntegrationRouter()
        r._user_id = user_id
        return r

    @pytest.mark.asyncio
    async def test_bound_binding_without_pat_is_available(self):
        r = self._router()
        binding = type("B", (), {"status": "bound"})()
        with (
            patch(
                "services.connectors.binding_repository.ConnectorBindingRepository.get",
                new=AsyncMock(return_value=binding),
            ),
            patch.object(r.config_service, "is_configured", return_value=False),
        ):
            assert await r.is_available() is True

    @pytest.mark.asyncio
    async def test_no_binding_no_pat_unavailable(self):
        r = self._router()
        with (
            patch(
                "services.connectors.binding_repository.ConnectorBindingRepository.get",
                new=AsyncMock(return_value=None),
            ),
            patch.object(r.config_service, "is_configured", return_value=False),
        ):
            assert await r.is_available() is False

    @pytest.mark.asyncio
    async def test_pat_only_still_available(self):
        r = self._router()
        with (
            patch(
                "services.connectors.binding_repository.ConnectorBindingRepository.get",
                new=AsyncMock(return_value=None),
            ),
            patch.object(r.config_service, "is_configured", return_value=True),
        ):
            assert await r.is_available() is True


class TestIssueRequestSlotFill:
    """2026-07-09: the classifier schema carries no entity fields and the
    extraction stage was never wired, so context.repository/title/body had no
    producer — the live first-real-write landed on the user's stale DEFAULT
    repo despite an explicitly-named target. Deterministic slot-fill from the
    message text (house #1066 pattern) is the fix; these pin it."""

    def _f(self):
        from services.intent.intent_service import IntentService

        return IntentService._slotfill_issue_request

    def test_the_live_sentence_extracts_fully(self):
        msg = ('Please create an issue in mediajunkie/test-piper-morgan repo titled '
               '"v0.8.10.3 first connector write" with body "created via the per-user '
               'OAuth rail, verified by read-back"')
        slots = self._f()(msg)
        assert slots["repository"] == "mediajunkie/test-piper-morgan"
        assert slots["title"] == "v0.8.10.3 first connector write"
        assert slots["body"] == "created via the per-user OAuth rail, verified by read-back"

    def test_url_and_git_suffix_forms(self):
        f = self._f()
        assert f("in https://github.com/acme/widgets please")["repository"] == "acme/widgets"
        assert f('github.com/acme/widgets.git titled "X"')["repository"] == "acme/widgets"

    def test_fractions_and_dates_never_match(self):
        f = self._f()
        assert "repository" not in f("what about 7/9 planning")
        # inside a real request, the real repo wins over the fraction:
        assert f("issue about the 1/2 day outage in acme/widgets")["repository"] == "acme/widgets"

    def test_no_slots_returns_empty(self):
        assert self._f()("create an issue about login bugs") == {}

    def test_colon_single_quote_title_extracts(self):
        """#1386-B2 live find: CXO's natural phrasing — no 'titled' keyword,
        colon-introduced single-quoted title — shipped a garbage fallback."""
        msg = "Let's track this. Create a GitHub issue in mediajunkie/test-piper-morgan: 'Add search functionality to navigation bar'"
        slots = self._f()(msg)
        assert slots["repository"] == "mediajunkie/test-piper-morgan"
        assert slots["title"] == "Add search functionality to navigation bar"

    def test_colon_double_quote_title_extracts(self):
        slots = self._f()('file a ticket: "Fix the login redirect"')
        assert slots["title"] == "Fix the login redirect"

    @pytest.mark.asyncio
    async def test_create_uses_slotfilled_repo_over_default(self, svc):
        """The exact live failure: explicitly-named repo must WIN over the
        stored default (which pointed at a repo with Issues disabled)."""
        intent = _intent()
        intent.context = {}  # what production actually delivers
        intent.original_message = (
            'create an issue in mediajunkie/test-piper-morgan titled "T" with body "B"'
        )
        created = {"number": 5, "html_url": "u", "title": "T"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=created)) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1")
        assert result.success
        kwargs = w.await_args.kwargs
        assert kwargs["owner"] == "mediajunkie"
        assert kwargs["repo_name"] == "test-piper-morgan"
        assert kwargs["title"] == "T"
        assert kwargs["body"] == "B"


class TestOriginalMessagePlumbing:
    """2026-07-09 root cause (#1332/#1220): NO classifier construction path set
    Intent.original_message — every downstream attribute reader (the floor's
    "came through empty", regex fallbacks, slot-fills) got "" on classifier-made
    intents. These pin the plumbing."""

    @pytest.mark.asyncio
    async def test_classifier_intents_carry_original_message(self):
        """The keyword-fallback path (cheapest deterministic construction) must
        set the attribute — representative of the five fixed sites."""
        from services.intent_service.classifier import IntentClassifier

        c = IntentClassifier(llm_service=object())  # LLM never reached on this path
        intent = c._fallback_classify("analyze the quarterly numbers please")
        assert intent.original_message == "analyze the quarterly numbers please"

    @pytest.mark.asyncio
    async def test_slotfill_falls_back_to_context_original_message(self, svc):
        """THE live 7cups case, pinned: attribute empty (pre-fix cached intents),
        context carries the message — slots must still extract and the named
        repo must win over any default."""
        intent = _intent()
        intent.original_message = ""  # what production delivered all evening
        intent.context = {
            "original_message": 'create an issue in mediajunkie/test-piper-morgan titled "T" with body "B"',
            "knowledge_used": [],
        }
        created = {"id": "1", "url": "https://github.com/mediajunkie/test-piper-morgan/issues/9"}
        full = {"number": 9, "title": "T", "html_url": "https://x/9"}
        with (
            patch(f"{ROUTER}.initialize", new=AsyncMock()),
            patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
            patch(f"{ROUTER}.create_issue", new=AsyncMock(return_value=full)) as w,
        ):
            result = await svc._handle_create_issue(intent, "wf-1", "sess-1")
        assert result.success
        kwargs = w.await_args.kwargs
        assert kwargs["owner"] == "mediajunkie"
        assert kwargs["repo_name"] == "test-piper-morgan"
