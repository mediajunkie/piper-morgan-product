"""#1576 — the standup's user-visible datetime FACES (time-handling audit F2).

The audit's finding, restated for this surface: ``StandupResult.generated_at``
was built with a bare ``datetime.now()`` (``standup_orchestration_service.py:45``),
so it carried NO zone at all, and the three text formatters printed it through
``strftime('%Y-%m-%d %H:%M')``. On Fly the server runs UTC, so a PT user read a
standup header seven hours ahead of their own morning with nothing in the string
to tell them so.

Two distinct defects stacked on one value, and they need separate fixes:

* the **instant** was naive — an ISO string with no offset is not an instant at
  all, and a browser handed ``"2025-10-19T14:30:00"`` reads it as *local* time
  (``new Date()`` semantics), silently inventing an offset. Fixed at the source.
* the **face** was unlabeled — every server-rendered surface (Slack, Markdown
  export, plain text) has no browser to re-render it, so it must carry the zone
  it was rendered in.

The JSON format is the one that DOES reach a browser; per the audit's converge
target it stays machine-shaped (aware ISO) and the page renders it with
``toLocale*``, exactly as the 23 already-correct sites do.
"""

from datetime import datetime, timedelta, timezone

import pytest

from services.features.morning_standup import StandupResult
from web.api.routes.standup import (
    format_as_markdown,
    format_as_slack,
    format_as_text,
    format_standup,
)

PT = "America/Los_Angeles"

# 2025-10-19 21:30 UTC == 2:30 PM PDT. The two faces differ by seven hours, so
# "which clock is this?" is answerable from the rendered string or it isn't.
INSTANT_UTC = datetime(2025, 10, 19, 21, 30, 0, tzinfo=timezone.utc)


def _result(generated_at=INSTANT_UTC) -> StandupResult:
    return StandupResult(
        user_id="user-1",
        generated_at=generated_at,
        generation_time_ms=12,
        yesterday_accomplishments=[],
        today_priorities=[],
        blockers=[],
        context_source="assembled",
        github_activity={},
        performance_metrics={},
        time_saved_minutes=0,
    )


class TestGeneratedAtIsAnInstant:
    """The value itself, before anything renders it."""

    @pytest.mark.asyncio
    async def test_orchestration_service_generates_an_aware_timestamp(self):
        """``generated_at`` must be a real instant, not a wall-clock reading.

        ``datetime.now()`` on an instance whose TZ is UTC yields a naive value
        that *looks* like a local time and is not one. Nothing downstream can
        recover the zone, so every consumer has to guess — and they guessed
        differently (the JSON consumer guessed browser-local; the text
        formatters guessed "don't mention it").
        """
        from services.domain.models import StandupSummary
        from services.domain.standup_orchestration_service import _summary_to_result

        result = _summary_to_result(StandupSummary(), "user-1", 12)

        assert result.generated_at.tzinfo is not None, "generated_at is naive — no instant"
        # And it is actually NOW, not a stale/constructed value.
        assert abs(result.generated_at - datetime.now(timezone.utc)) < timedelta(minutes=5)

    def test_json_format_emits_an_offset_bearing_iso(self):
        """The browser-facing format keeps the audit's converge pattern.

        Aware ISO out, ``toLocale*`` in the page — NOT a server-side face. The
        assertion is on the offset because that is the whole difference between
        a string a browser can localize and one it will mis-localize in silence.

        Driven through the real production path (``_summary_to_result``), not a
        hand-built aware fixture — a fixture would assert that this formatter
        passes an offset through, which was never the broken part.
        """
        from services.domain.models import StandupSummary
        from services.domain.standup_orchestration_service import _summary_to_result

        payload = format_standup(_summary_to_result(StandupSummary(), "user-1", 12), "json")
        iso = payload["generated_at"]

        assert datetime.fromisoformat(iso).tzinfo is not None, f"naive ISO reached the API: {iso}"


class TestServerRenderedFacesAreLabeled:
    """Slack / Markdown / plain text: no browser downstream, so label the zone."""

    @pytest.mark.parametrize("formatter", [format_as_slack, format_as_markdown, format_as_text])
    def test_face_states_the_zone_it_was_rendered_in(self, formatter):
        rendered = formatter(_result(), tz_name=PT)

        assert "PDT" in rendered, f"unlabeled clock face in {formatter.__name__}: {rendered!r}"
        assert "2:30 PM" in rendered, f"not the user's clock in {formatter.__name__}: {rendered!r}"
        assert "21:30" not in rendered, "server (UTC) face leaked into the render"

    @pytest.mark.parametrize("formatter", [format_as_slack, format_as_markdown, format_as_text])
    def test_unknown_zone_renders_utc_and_says_so(self, formatter):
        """#1381's rule generalized: never an unlabeled face, even when the
        user's zone is unknown. UTC-and-say-UTC is wrong for the reader but
        *checkably* wrong, which is the property that matters."""
        rendered = formatter(_result(), tz_name=None)

        assert "UTC" in rendered, f"no zone label on the unknown-tz path: {rendered!r}"
        assert "9:30 PM" in rendered

    def test_naive_generated_at_is_read_as_utc_not_as_a_local_face(self):
        """Defence in depth for any caller still constructing a naive value:
        it is interpreted as UTC (``ensure_utc``) and labeled, never printed
        as though it were already the user's wall clock."""
        rendered = format_as_slack(_result(datetime(2025, 10, 19, 21, 30, 0)), tz_name=PT)

        assert "2:30 PM PDT" in rendered
