"""#1236 — the home center is a clean chat (CXO consolidation, 2026-06-19).

The home "what i'm seeing" (Places) and "recently" (insights) ambient modules were
retired: Places now render as Radar ``work_item`` entities (PlaceEntitySource); insights
are out of the Radar entirely (accessible via /insights, chat, and the standup surface).
The home center is just the greeting + the inline chat. These guard the removal — modules
and their orphaned JS/asset loads must not silently creep back.

Replaces test_home_modules_1225.py / test_home_recently_module_1194.py / test_home_places.py
(all tested the now-removed modules). Verified via real template.render() (NOT curl-200).
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path("templates")


@pytest.fixture
def env():
    return Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)


def _render(env, **ctx):
    ctx.setdefault("current_user", {"username": "xian", "display_name": "Xian"})
    ctx.setdefault("trust_stage", 3)
    return env.get_template("home.html").render(**ctx)


def test_ambient_modules_removed_even_at_stage_3(env):
    # the modules used to render at Stage 3+; they must be gone now at every stage
    html = _render(env, trust_stage=3)
    assert "data-ambient-module" not in html
    assert 'id="places-section"' not in html
    assert 'id="recently-section"' not in html
    # heading elements gone (id-based, so the #1236 doc comment naming the old modules
    # doesn't trip the check)
    assert 'id="places-heading"' not in html
    assert 'id="recently-heading"' not in html


def test_orphaned_places_module_js_and_assets_gone():
    home = Path("templates/home.html").read_text()
    assert "home-modules.js" not in home
    assert "home-modules.css" not in home
    assert "loadPlaces" not in home
    assert "places-container" not in home
    assert "place_window.html" not in home


def test_chat_inline_center_preserved():
    home = Path("templates/home.html").read_text()
    assert "components/chat-inline.html" in home  # the center chat survives the cleanup


def test_consolidation_is_documented():
    home = Path("templates/home.html").read_text()
    assert "#1236" in home  # a future reader sees why the modules are gone
