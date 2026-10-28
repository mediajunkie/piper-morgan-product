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

from services.domain.models import StandupSummary
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
    LINE = "I couldn't reach your calendar just now. I can't put together a standup right now — try again in a bit."

    def test_no_failure_keeps_the_no_activity_copy(self):
        assert sp.empty_standup_copy(False) == (sp.INVITE_EMPTY_LEAD, sp.EMPTY_STANDALONE)

    def test_a_failure_replaces_no_observed_activity(self):
        lead, standalone = sp.empty_standup_copy(False, self.LINE)
        for text in (lead, standalone):
            assert text.startswith(self.LINE)
            assert "no observed activity" not in text
        assert lead.endswith("(yes/no)")

    def test_github_reconnecting_keeps_its_own_copy(self):
        assert sp.empty_standup_copy(True, self.LINE)[0] == sp.INVITE_EMPTY_LEAD_GITHUB_STALE

    def test_declining_the_degraded_lead_claims_no_report(self):
        lead, _ = sp.empty_standup_copy(False, self.LINE)
        with patch.object(sp.vi, "was_declined", lambda *_a, **_k: False):
            rec = sp.build_interview_invitation(USER_A, "s-2182", question=lead)
        assert rec["decline_message"] == sp.INVITE_DECLINE_MESSAGE_NO_REPORT


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
