"""#1236: home.html Radar surface wiring (content assertions).

home.html loads the Layer-2 Radar surface behind a ?radar=1 feature flag
(default off → no regression for the existing conversation-list sidebar), and
falls back to the conversation list if /api/v1/radar fails. The JS render
behavior is exercised by the route tests (tests/unit/web/api/routes/test_radar.py)
+ the component render functions (test_history_sidebar.py::TestRadarSurface);
these guard the home.html wiring that ties the two together.
"""

from pathlib import Path

import pytest


@pytest.fixture
def home_html() -> str:
    return (Path(__file__).resolve().parents[3] / "templates" / "home.html").read_text()


def test_load_radar_function_defined(home_html):
    assert "async function loadRadar()" in home_html


def test_load_radar_fetches_radar_endpoint(home_html):
    # Must hit the versioned API surface with credentials (auth cookie).
    assert "fetch('/api/v1/radar'" in home_html
    assert "credentials: 'include'" in home_html


def test_load_radar_feeds_the_sidebar_render(home_html):
    # loadRadar() hands the RadarView to the component's updateRadar() entry point.
    assert "window.HistorySidebar.updateRadar(view)" in home_html


def test_load_radar_falls_back_to_history_on_error(home_html):
    # Graceful degradation: a failed radar fetch must not blank the sidebar —
    # it falls back to the existing conversation list (no regression).
    assert "loadHistoryData();" in home_html
    assert "falling back to history list" in home_html


def test_radar_is_feature_flagged_default_off(home_html):
    # ?radar=1 gates the new surface; absent the flag, the existing history
    # list loads unchanged (the default-off no-regression guarantee for PM UAT).
    assert "new URLSearchParams(window.location.search).get('radar') === '1'" in home_html
    assert "radarEnabled" in home_html
    # The else-branch keeps the legacy loader as the default path.
    assert "if (radarEnabled) {" in home_html
