"""#1236: home.html Radar surface wiring (content assertions).

home.html loads the Layer-2 Radar surface as the DEFAULT panel (#1090 swap,
PM-authorized 2026-06-18); ?radar=0 is the escape hatch back to the plain
conversation list, and it falls back to that list if /api/v1/radar fails. The JS render
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


def test_radar_is_the_default_panel_with_escape_hatch(home_html):
    # #1090 swap (PM-authorized 2026-06-18; Radar design approved, no real users):
    # Radar is now the DEFAULT Layer-2 panel. ?radar=0 is the escape hatch back to
    # the plain conversation list (loadRadar also falls back to it on fetch error).
    assert "new URLSearchParams(window.location.search).get('radar') === '0'" in home_html
    assert "radarDisabled" in home_html
    assert "if (radarDisabled) {" in home_html
    # The default (no flag / not '0') path loads Radar.
    assert "loadRadar();" in home_html
