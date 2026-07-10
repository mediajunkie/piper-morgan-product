"""#1150 + #1381: context_assembler's current_time is USER-timezone-aware or absent.

#1150: a bare datetime.now() was the server's local clock, unlabeled — wrong
time-of-day fed to the floor on any non-local-tz instance. #1381 found the
hosted consequence: the single-file config (or the naive fallback — a UTC
container clock) fed EVERY user the wrong local time; Piper narrated "4:30 AM —
early riser or late night" at 9:32 PM Pacific (live, 2026-07-08/09).

The contract now: the user's own personalization timezone wins → the file
config covers the single-tenant/local path → otherwise the flourish is OMITTED
("" — the floor's renderer skips absent keys). A wrong confident time is worse
than none; the server clock never wears user clothing.
"""

import re
from datetime import datetime
from unittest.mock import AsyncMock, patch
from zoneinfo import ZoneInfo

import pytest

from services.intent_service.context_assembler import _current_time_for_user

_REPO_GET = (
    "services.configuration.personalization_repository."
    "PersonalizationContextRepository.get"
)
_FILE_CFG = (
    "services.configuration.piper_config_loader.piper_config_loader.load_standup_config"
)


class TestCurrentTimeForUser:
    @pytest.mark.asyncio
    async def test_personalization_timezone_wins(self):
        """#1381 core: the USER's stored timezone beats the file config."""
        row = type("Row", (), {"context": {"timezone": "America/New_York"}})()
        with (
            patch(_REPO_GET, new=AsyncMock(return_value=row)),
            patch(_FILE_CFG, return_value={"timing": {"timezone": "America/Los_Angeles"}}),
        ):
            result = await _current_time_for_user("694d8f4e-578e-40c2-9cb8-18c8891e2d2a")
        expected_label = datetime.now(ZoneInfo("America/New_York")).strftime("%Z")
        assert result.endswith(expected_label), (result, expected_label)

    @pytest.mark.asyncio
    async def test_file_config_covers_single_tenant_path(self):
        """No personalization row (or no user) → the #1150 file-config behavior."""
        with (
            patch(_REPO_GET, new=AsyncMock(return_value=None)),
            patch(_FILE_CFG, return_value={"timing": {"timezone": "America/New_York"}}),
        ):
            result = await _current_time_for_user("694d8f4e-578e-40c2-9cb8-18c8891e2d2a")
        assert re.match(r"^\d{2}:\d{2} (AM|PM) [A-Z]{2,5}$", result), result
        assert result.endswith(datetime.now(ZoneInfo("America/New_York")).strftime("%Z"))

    @pytest.mark.asyncio
    async def test_unknown_timezone_omits_never_guesses(self):
        """#1381's core rule: no user tz + no file tz → EMPTY (the floor skips
        the line) — never the server clock presented as the user's."""
        with (
            patch(_REPO_GET, new=AsyncMock(return_value=None)),
            patch(_FILE_CFG, side_effect=RuntimeError("config unavailable")),
        ):
            result = await _current_time_for_user("694d8f4e-578e-40c2-9cb8-18c8891e2d2a")
        assert result == ""

    @pytest.mark.asyncio
    async def test_no_user_id_still_works_via_file_config(self):
        with patch(_FILE_CFG, return_value={"timing": {"timezone": "UTC"}}):
            result = await _current_time_for_user(None)
        assert result.endswith("UTC")

    @pytest.mark.asyncio
    async def test_repo_error_degrades_to_file_config_not_crash(self):
        with (
            patch(_REPO_GET, new=AsyncMock(side_effect=RuntimeError("db down"))),
            patch(_FILE_CFG, return_value={"timing": {"timezone": "UTC"}}),
        ):
            result = await _current_time_for_user("694d8f4e-578e-40c2-9cb8-18c8891e2d2a")
        assert result.endswith("UTC")

    @pytest.mark.asyncio
    async def test_bogus_timezone_name_omits(self):
        row = type("Row", (), {"context": {"timezone": "Not/AZone"}})()
        with (
            patch(_REPO_GET, new=AsyncMock(return_value=row)),
            patch(_FILE_CFG, side_effect=RuntimeError("no file")),
        ):
            result = await _current_time_for_user("694d8f4e-578e-40c2-9cb8-18c8891e2d2a")
        assert result == ""
