"""#2182 (#2151's show_standup row, Arch 10-27): a failed calendar or source read is said
as a failed read, never as a free day or "no observed activity".

- ``StandupCalendarProvider.read_today`` tells a read that happened from a calendar that
  isn't connected (silent) and a connected calendar whose read failed (disclosed).
- The assembler records a failed calendar read, and a failed documents read, in
  ``degraded_sources``; the chat empty branch leads with the #1889 disclosure.
- Two-account pin: user A's calendar grant never serves user B's standup.
"""

from typing import Any, List, Optional
from unittest.mock import patch

import pytest

from services.domain.models import StandupSummary, degraded_head
from services.intent_service import standup_preferences as sp
from services.radar.sources import DocumentEntitySource, EntitySourceReadFailed
from services.standup.assembler import (
    CALENDAR_NOT_CONNECTED,
    CALENDAR_READ_FAILED,
    StandupAssembler,
    StandupCalendarProvider,
)

USER_A = "11111111-1111-1111-1111-111111111111"
USER_B = "22222222-2222-2222-2222-222222222222"


class _Adapter:
    def __init__(self, events: List[dict], established: bool, err: Optional[str] = None):
        self._result = (events, established)
        self.last_read_error = err

    async def _fetch_todays_events(self, user_id=None):
        return self._result


class _Router:
    def __init__(self, adapter: Any):
        self.spatial_calendar = adapter
        self.legacy_calendar = None


def _provider(adapter: Any) -> StandupCalendarProvider:
    return StandupCalendarProvider(router_factory=lambda uid: _Router(adapter))


async def _utc(_uid):
    return "UTC"


@pytest.fixture(autouse=True)
def _tz():
    with patch("services.utils.datetime_utils.user_timezone_name", _utc):
        yield


class TestReadToday:
    async def test_a_failed_read_of_a_connected_calendar_is_failed(self):
        events, unread = await _provider(_Adapter([], False, "unauthorized")).read_today(USER_A)
        assert (events, unread) == ([], CALENDAR_READ_FAILED)

    async def test_an_unclassified_failure_is_failed_not_free(self):
        assert (await _provider(_Adapter([], False, None)).read_today(USER_A))[
            1
        ] == CALENDAR_READ_FAILED

    async def test_no_stored_credential_is_not_connected(self):
        events, unread = await _provider(_Adapter([], False, "no_credential")).read_today(USER_A)
        assert (events, unread) == ([], CALENDAR_NOT_CONNECTED)

    async def test_an_established_empty_read_is_a_free_day(self):
        assert await _provider(_Adapter([], True)).read_today(USER_A) == ([], None)

    async def test_no_calendar_integration_on_the_deploy_is_not_connected(self):
        assert (await _provider(None).read_today(USER_A))[1] == CALENDAR_NOT_CONNECTED

    async def test_a_raise_is_failed(self):
        def _boom(_uid):
            raise RuntimeError("forced")

        p = StandupCalendarProvider(router_factory=_boom)
        assert await p.read_today(USER_A) == ([], CALENDAR_READ_FAILED)

    async def test_events_today_keeps_its_list_contract(self):
        ev = {"title": "Sync", "start_time": "2026-10-27T16:00:00+00:00"}
        out = await _provider(_Adapter([ev], True)).events_today(USER_A)
        assert [e["title"] for e in out] == ["Sync"]


async def _assemble(calendar: Any, sources: Optional[list] = None) -> StandupSummary:
    return await StandupAssembler(sources or [], calendar_provider=calendar).assemble(USER_A)


class TestAssemblerRecordsTheFailure:
    async def test_a_failed_calendar_read_is_a_degraded_source_not_a_free_day(self):
        s = await _assemble(_provider(_Adapter([], False, "error")))
        assert s.degraded_sources == ["your calendar"]
        assert not s.today
        assert "couldn't reach your calendar" in s.to_prose()

    async def test_a_calendar_that_is_not_connected_stays_silent(self):
        s = await _assemble(_provider(_Adapter([], False, "no_credential")))
        assert s.degraded_sources == [] and s.degraded_details == []

    async def test_a_provider_that_raises_is_recorded(self):
        class _Raising:
            async def events_today(self, _uid):
                raise ConnectionError("forced")

        assert (await _assemble(_Raising())).degraded_sources == ["your calendar"]

    async def test_a_failed_documents_read_is_disclosed(self):
        class _Docs:
            async def list_for_user(self, _uid):
                raise OSError("forced: the documents table could not be read")

        with pytest.raises(EntitySourceReadFailed) as e:
            await DocumentEntitySource(_Docs()).fetch(USER_A)
        assert e.value.label == "your documents"
        s = await _assemble(None, [DocumentEntitySource(_Docs())])
        assert s.degraded_sources == ["your documents"]


class TestEmptyCopy:
    LINE = "I couldn't reach your calendar just now."
    TAIL = (
        "I can't pull a standup together right now. You can ask again in a bit, or we can "
        "do a quick guided one: you tell me what happened and what's ahead, and I'll write "
        "it up. Want to do that? (yes/no)"
    )

    def test_the_head_is_the_disclosure_sentence_alone(self):
        assert degraded_head(["your calendar"]) == self.LINE
        joined = degraded_head(
            [],
            [
                {"label": "your calendar", "reason": None, "connector": None},
                {"label": "x", "reason": "assignee_unresolved", "connector": "GitHub"},
            ],
        )
        assert joined == (
            "I couldn't reach your calendar just now, and I couldn't tell which GitHub "
            "issues are assigned to you."
        )
        assert degraded_head([]) == ""

    def test_no_failure_keeps_the_no_activity_copy(self):
        assert sp.empty_standup_copy(False) == (sp.INVITE_EMPTY_LEAD, sp.EMPTY_STANDALONE)

    def test_a_failure_takes_cxos_tail_not_no_observed_activity(self):
        lead, standalone = sp.empty_standup_copy(False, self.LINE)
        assert lead == f"{self.LINE} {self.TAIL}"  # CXO 10-27 19:16
        assert standalone.startswith(f"{self.LINE} I can't pull a standup together")
        for text in (lead, standalone):
            assert "no observed activity" not in text and "—" not in text

    def test_github_reconnecting_keeps_its_own_copy(self):
        assert sp.empty_standup_copy(True, self.LINE)[0] == sp.INVITE_EMPTY_LEAD_GITHUB_STALE

    def test_declining_the_degraded_lead_claims_no_report(self):
        lead, _ = sp.empty_standup_copy(False, self.LINE)
        with patch.object(sp.vi, "was_declined", lambda *_a, **_k: False):
            rec = sp.build_interview_invitation(USER_A, "s-2182", question=lead)
        assert rec["decline_message"] == sp.INVITE_DECLINE_MESSAGE_NO_REPORT


class TestGitHubStatusCheckFailed:
    """Arch 10-27: a GitHub status check that couldn't run is a failed read, not "no work
    items". Only the binding read fails (no PAT); the documents read is healthy."""

    ISS = "services.integrations.integration_status_service"

    def _status(self, binding_state, config_status):
        async def _binding(_uid):
            return binding_state

        async def _config(_iid, user_id=None):
            return config_status, None

        return (
            patch(f"{self.ISS}.github_oauth_binding_state", _binding),
            patch(f"{self.ISS}.get_config_status", _config),
        )

    async def test_a_failed_binding_check_is_disclosed_as_github(self):
        from services.integrations.integration_status_service import BINDING_CHECK_FAILED
        from services.radar.feed_factory import WorkItemProvider, WorkItemReadKind
        from services.radar.sources import WorkItemEntitySource

        class _Docs:
            async def list_for_user(self, _uid):
                return []

        a, b = self._status(BINDING_CHECK_FAILED, "not_configured")
        with a, b:
            outcome = await WorkItemProvider().gather_for_user(USER_A)
            assert outcome.kind == WorkItemReadKind.SOURCE_FAILED
            s = await _assemble(
                None, [WorkItemEntitySource(WorkItemProvider()), DocumentEntitySource(_Docs())]
            )
        assert s.degraded_sources == ["your GitHub work items"]
        lead, _ = sp.empty_standup_copy(
            False, degraded_head(s.degraded_sources, s.degraded_details)
        )
        assert lead.startswith("I couldn't reach your GitHub work items just now.")
        assert "no observed activity" not in lead

    async def test_github_not_connected_stays_verified_empty(self):
        from services.radar.feed_factory import WorkItemProvider, WorkItemReadKind

        a, b = self._status(None, "not_configured")
        with a, b:
            outcome = await WorkItemProvider().gather_for_user(USER_A)
        assert outcome.kind == WorkItemReadKind.VERIFIED_EMPTY


class TestTwoAccountPin:
    """Arch 10-27 (from #1441's DoD): A's grant never serves B's standup. Built through the
    real router and adapter; only the keychain and the token refresh are stubbed."""

    async def test_a_grant_never_serves_b(self, monkeypatch):
        monkeypatch.delenv("GOOGLE_TOKEN_FILE", raising=False)
        asked: List[str] = []
        refreshed: List[str] = []

        async def _key(_self, name, *a, **k):
            asked.append(name)
            return "rt-A" if name == f"google_calendar_{USER_A}" else None

        async def _refresh(_self, token):
            refreshed.append(token)
            return None  # A's refresh fails: a connected account's failed read

        built: List[Any] = []

        def _factory(uid):
            built.append(StandupCalendarProvider._default_router(uid))
            return built[-1]

        with (
            patch("services.infrastructure.keychain_service.KeychainService.aget_api_key", _key),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler."
                "refresh_access_token",
                _refresh,
            ),
            patch(
                "services.integrations.calendar.calendar_integration_router.FeatureFlags."
                "should_use_spatial_calendar",
                lambda: True,
            ),
        ):
            p = StandupCalendarProvider(router_factory=_factory)
            _, unread_b = await p.read_today(USER_B)
            assert asked == [f"google_calendar_{USER_B}"] and refreshed == []
            assert unread_b == CALENDAR_NOT_CONNECTED
            assert USER_B in built[0].spatial_calendar._token_file
            assert USER_A not in built[0].spatial_calendar._token_file

            _, unread_a = await p.read_today(USER_A)
            assert asked[-1] == f"google_calendar_{USER_A}" and refreshed == ["rt-A"]
            assert unread_a == CALENDAR_READ_FAILED
