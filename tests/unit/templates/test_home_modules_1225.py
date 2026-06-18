"""
#1225 — home ambient modules collapse + dismiss affordances.

PM flagged (M3 UAT 2026-06-14): the home "what i'm seeing" / "recently" modules
take real-estate with no way to minimize or dismiss. CXO disposition (D1 punch-list
2026-06-17): collapsible + dismissable; dismiss = "not now" (re-surface on new
content), the permanent "don't show again" is a separate future opt-out.

Verified via real `template.render()` (NOT curl-200, per the UI-fix discipline):
- the controls render inside each ambient module's header at Stage 3+,
- the trust-gating still hides the whole capability surface (controls included) below
  Stage 3 — collapse/dismiss are for the user's *view*, they don't ungate a Piper
  capability surface,
- the CSS state rules + JS controller + async wiring are actually present (not just
  markup that nothing drives).
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
    return env.get_template("home.html").render(**ctx)


class TestControlsRenderAtStage3:
    """At Stage 3+ the ambient modules show, each with collapse + dismiss controls."""

    def test_both_modules_marked_as_ambient(self, env):
        html = _render(env, trust_stage=3)
        assert html.count("data-ambient-module") >= 2
        assert 'data-module-id="places"' in html
        assert 'data-module-id="recently"' in html

    def test_each_module_has_collapse_and_dismiss(self, env):
        html = _render(env, trust_stage=3)
        # two modules × {collapse, dismiss}
        assert html.count("module-collapse") == 2
        assert html.count("module-dismiss") == 2

    def test_places_is_async_recently_is_not(self, env):
        """places fills in via /api/v1/places (async) → its dismiss signature is
        evaluated after render; recently is server-rendered (sync)."""
        html = _render(env, trust_stage=3)
        # exactly one async marker, and it sits on the places section
        assert html.count('data-module-async="true"') == 1
        places_open_tag = html.split('id="places-section"', 1)[1][:300]
        assert 'data-module-async="true"' in places_open_tag

    def test_controls_are_accessible(self, env):
        html = _render(env, trust_stage=3)
        # collapse button announces collapsed state (default-collapsed, #3) + controls
        # the body it hides
        assert 'aria-expanded="false"' in html
        assert 'aria-controls="places-container"' in html
        assert 'aria-controls="recently-cards"' in html
        # both actions carry a label (icon-only buttons)
        assert 'aria-label="Collapse what i\'m seeing"' in html
        assert 'aria-label="Dismiss what i\'m seeing for now"' in html

    def test_modules_default_collapsed_so_chat_is_not_occluded(self, env):
        """#3 (PM 2026-06-18): ambient modules server-render COLLAPSED by default so
        the full-height chat (#1173) is never buried. Both module sections carry
        is-collapsed in the template (no collapse-flash); home-modules.js expands only
        if the user explicitly did. Interim — CXO owns the fuller composition."""
        html = _render(env, trust_stage=3)
        # both ambient sections render collapsed in the markup
        assert 'class="card places-section is-collapsed"' in html
        assert 'class="card is-collapsed" id="recently-section"' in html
        # the JS default is collapsed-unless-explicitly-expanded ("0")
        js = Path("web/static/js/home-modules.js").read_text()
        assert 'lsGet(COLLAPSE_KEY + id) !== "0"' in js


class TestTrustGatingPreserved:
    """Collapse/dismiss is a per-user *view* control — it must NOT ungate the
    capability surface. Below Stage 3 the modules (and their controls) stay hidden."""

    def test_modules_and_controls_absent_below_stage_3(self, env):
        html = _render(env, trust_stage=1)
        assert 'id="places-section"' not in html
        assert 'id="recently-section"' not in html
        assert "module-collapse" not in html
        assert "data-ambient-module" not in html


class TestWiringExists:
    """The markup must be backed by real CSS state rules + a JS controller +
    the async hook — otherwise the buttons would be inert."""

    def test_css_has_state_rules(self):
        css = Path("web/static/css/home-modules.css").read_text()
        assert ".card__header-controls" in css
        assert ".module-control" in css
        # collapsed hides the body; dismissed hides the whole module
        assert "[data-ambient-module].is-collapsed .card__body" in css
        assert "[data-ambient-module].is-dismissed" in css

    def test_js_controller_exposes_api_and_logic(self):
        js = Path("web/static/js/home-modules.js").read_text()
        assert "window.HomeModules" in js
        assert "refreshAsync" in js
        assert "computeSignature" in js  # content-signature → re-surface on new content
        assert "piper_module_collapsed_" in js
        assert "piper_module_dismissed_" in js

    def test_home_loads_controller_and_hooks_async(self):
        home = Path("templates/home.html").read_text()
        assert '/static/js/home-modules.js' in home
        assert '/static/css/home-modules.css' in home
        # loadPlaces re-evaluates dismiss after rendering its (async) content
        assert "window.HomeModules.refreshAsync('places')" in home
