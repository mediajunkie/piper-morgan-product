"""#1286 D2 Slice 3 — app_shell mobile nav (responsive shell + hamburger drawer).

Real template.render() (per the UI-fix discipline): the shell renders a mobile top-bar
whose hamburger controls the rail (an off-canvas drawer on mobile), plus a backdrop and the
toggle JS. Desktop is unchanged — CSS media queries do the responsive switch; the top-bar is
display:none until the mobile breakpoint. The rail width is tokenized (single source of truth
with the grid).
"""
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

_ROOT = Path(__file__).resolve().parents[3]
TEMPLATES = _ROOT / "templates"
CSS = _ROOT / "web" / "static" / "css"


@pytest.fixture
def env():
    return Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)


def _render(env, **ctx):
    ctx.setdefault("trust_stage", 1)
    src = "{% extends 'layouts/app_shell.html' %}{% block main %}m{% endblock %}"
    return env.from_string(src).render(**ctx)


def test_shell_renders_mobile_topbar_with_hamburger(env):
    html = _render(env)
    assert "app-shell-topbar" in html
    assert 'id="app-shell-hamburger"' in html
    assert 'aria-controls="nav-rail"' in html  # a11y: the hamburger controls the rail
    assert 'aria-expanded="false"' in html  # starts collapsed


def test_rail_has_id_for_drawer_toggle(env):
    assert 'id="nav-rail"' in _render(env)  # the drawer target


def test_shell_has_backdrop_for_open_drawer(env):
    assert 'id="app-shell-backdrop"' in _render(env)


def test_mobile_nav_toggle_js_included(env):
    assert "/static/js/mobile-nav.js" in _render(env)


def test_topbar_precedes_rail_in_source_order(env):
    # top-bar (with the hamburger) comes before the rail → sane tab order
    html = _render(env)
    assert html.index("app-shell-topbar") < html.index('id="nav-rail"')


def test_shell_template_still_has_no_inline_style_attr():
    # Slice 3 keeps the token-only / no-inline-style discipline (chrome styles in app-shell.css).
    assert "style=" not in (TEMPLATES / "layouts" / "app_shell.html").read_text()


def test_responsive_grid_is_mobile_first():
    css = (CSS / "app-shell.css").read_text()
    assert "@media" in css and "min-width" in css and "768px" in css


def test_topbar_styled_in_app_shell_css():
    assert "app-shell-topbar" in (CSS / "app-shell.css").read_text()


def test_rail_width_tokenized_not_raw():
    css = (CSS / "nav-rail.css").read_text()
    assert "var(--grid-rail-width)" in css
    assert "width: 180px" not in css  # the raw rail width is gone (single source = the token)
