"""#1868 — the GUIDANCE handler's clock face is the USER's, not the server's.

Before: `_handle_guidance_query` computed `current_hour` from the SERVER's
naive `datetime.now().hour` (whatever wall-clock zone the process happens to
run on — UTC on Fly) and labeled the printed face from the CONFIG FILE's
standup timezone (same value for every user on the instance). Two independent
defects in one line: the day-part bucket (`_get_immediate_focus`, and the
three `_format_*_guidance` callers that feed it) could bucket a user into the
wrong part of their day, and the label on `time_context` described the
deployment, never the person reading it — the #1576-audit "labeled but
wrong" category (F2), the hardest kind to notice because the string looks
careful.

After: one `now_user = now_in_zone(await user_timezone_name(user_id))`
computed at the top drives both `current_hour` and the printed face.

LAYER (m-43): `_handle_guidance_query` itself, with its data collaborators
(`_get_calendar_context`, `_get_priority_metadata`, `user_context_service`)
stubbed out — irrelevant to what's under test — and the clock seam
(`user_timezone_name` / `now_in_zone`) controlled precisely. DENOMINATOR:
this pins the GUIDANCE handler's own clock derivation; it does not re-verify
`_zone`'s None-degrades-to-UTC behavior (already covered in
`services/utils/datetime_utils.py`'s own suite) beyond confirming this
handler's wiring reaches that real code path.
"""

from __future__ import annotations

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from zoneinfo import ZoneInfo

import pytest

from services.intent_service.canonical_handlers import CanonicalHandlers
from services.utils.datetime_utils import now_in_zone

pytestmark = pytest.mark.asyncio

TOKYO = ZoneInfo("Asia/Tokyo")
# 10:00 in Tokyo on 2026-09-23 is 01:00 UTC the SAME day (JST = UTC+9).
NOW_TOKYO = datetime(2026, 9, 23, 10, 0, tzinfo=TOKYO)


@pytest.fixture
def handlers():
    return CanonicalHandlers()


def _guidance_intent():
    intent = MagicMock()
    intent.spatial_context = None  # -> _format_standard_guidance path
    intent.context = {}
    return intent


def _stub_collaborators(handlers):
    """Patch the data collaborators this test has no stake in, so the only
    thing driving the result is the clock seam under test."""
    return (
        patch.object(handlers, "_detect_setup_request", return_value=None),
        patch(
            "services.intent_service.canonical_handlers.user_context_service.get_user_context",
            new=AsyncMock(return_value=None),
        ),
        patch.object(handlers, "_get_calendar_context", new=AsyncMock(return_value=None)),
        patch.object(handlers, "_get_priority_metadata", new=AsyncMock(return_value={})),
    )


class TestGuidanceUsesTheUsersClockNotTheServers:
    async def test_tokyo_user_buckets_and_labels_on_their_own_clock(self, handlers):
        """A Tokyo user at 10:00 local (01:00 UTC) gets the CORRECT day-part
        bucket for 10:00 ("Collaboration time" — 9<=hour<14 in
        `_get_immediate_focus`) and a face labeled JST.

        The bug this catches is concrete: bucketing off the raw UTC hour (1)
        would land in `_get_immediate_focus`'s trailing `else` branch
        ("Flexible time... strategic planning") instead — a materially
        different, wrong recommendation. Both assertions below are needed to
        show the fix, not just the label.
        """
        stubs = _stub_collaborators(handlers)
        with (
            stubs[0],
            stubs[1],
            stubs[2],
            stubs[3],
            patch(
                "services.intent_service.canonical_handlers.user_timezone_name",
                new=AsyncMock(return_value="Asia/Tokyo"),
            ),
            patch(
                "services.intent_service.canonical_handlers.now_in_zone",
                new=MagicMock(return_value=NOW_TOKYO),
            ) as mock_now_in_zone,
        ):
            result = await handlers._handle_guidance_query(
                _guidance_intent(),
                session_id="s-1868",
                user_id="11111111-2222-3333-4444-555555555555",
            )

        # Wiring: the resolved user zone reached now_in_zone, not a hardcoded one.
        mock_now_in_zone.assert_called_once_with("Asia/Tokyo")

        ctx = result["intent"]["context"]
        # The face: labeled JST, in the user's local 12-hour clock, never bare.
        assert ctx["time_context"] == "10:00 AM JST"

        # The bucket: correct-for-10:00 text present, wrong-for-1:00-UTC text absent.
        assert "Collaboration time" in ctx["immediate_focus"]
        assert "team coordination" in ctx["immediate_focus"]
        assert "Flexible time" not in ctx["immediate_focus"]
        assert "Flexible time" not in result["message"]
        assert "strategic planning" not in result["message"]

    async def test_unknown_user_degrades_to_a_labeled_utc_face_never_a_bare_hour(self, handlers):
        """When the zone can't be resolved for this user, the face still
        carries an honest zone label (UTC) — never a bare digit. Exercises
        the REAL `now_in_zone` (only the async preference lookup is faked),
        so this also pins that this handler's `None` really reaches the
        `_zone(None) -> UTC` degrade path rather than crashing or silently
        defaulting to some other zone.
        """
        stubs = _stub_collaborators(handlers)
        with (
            stubs[0],
            stubs[1],
            stubs[2],
            stubs[3],
            patch(
                "services.intent_service.canonical_handlers.user_timezone_name",
                new=AsyncMock(return_value=None),
            ),
            patch(
                "services.intent_service.canonical_handlers.now_in_zone",
                wraps=now_in_zone,
            ) as spy_now_in_zone,
        ):
            result = await handlers._handle_guidance_query(
                _guidance_intent(), session_id="s-1868", user_id=None
            )

        spy_now_in_zone.assert_called_once_with(None)

        ctx = result["intent"]["context"]
        assert ctx["time_context"].endswith(" UTC"), ctx["time_context"]
        # Never a bare hour: the face must carry AM/PM and the zone label,
        # not just a digit (the pre-#1868 shape was f"{current_hour}:00 {label}").
        import re

        assert re.match(r"^\d{1,2}:\d{2} (AM|PM) UTC$", ctx["time_context"]), ctx["time_context"]

        # And the day-part bucket derived from that same UTC hour is a real,
        # non-empty recommendation — not a crash, not an unresolved token.
        assert isinstance(ctx["immediate_focus"], str) and len(ctx["immediate_focus"]) > 10
