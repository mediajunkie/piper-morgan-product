"""F2 #1171 — app_shell page-shell: real-render block-contract tests.

Verifies via real `template.render()` (NOT curl-200, per the UI-fix discipline) that:
- the shell renders with the global nav chrome + token CSS;
- page_title / main / scripts are page-overridable;
- header/nav are SHELL-ONLY — a page cannot override or inject chrome
  (the F2 structural guarantee — the drift-killer);
- the skip-link is shell-owned + first-focusable (a11y, #1265);
- the Radar aside is opt-in (show_radar).
(The footer was removed 2026-06-17 — apps aren't documents; util links belong in nav.)
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).resolve().parents[3] / "templates"


@pytest.fixture
def env():
    return Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)


def _render(env, child_src, **ctx):
    ctx.setdefault("trust_stage", 1)
    return env.from_string(child_src).render(**ctx)


def test_shell_renders_with_nav_chrome(env):
    html = _render(
        env,
        "{% extends 'layouts/app_shell.html' %}{% block main %}<p>HELLO_MAIN</p>{% endblock %}",
    )
    assert "HELLO_MAIN" in html  # the page's content
    assert "nav-rail" in html  # nav chrome included (shell-owned, #1280 left dark rail)
    assert "/static/css/app-shell.css" in html
    assert "/static/css/tokens.css" in html


def test_page_title_and_scripts_overridable(env):
    html = _render(
        env,
        "{% extends 'layouts/app_shell.html' %}"
        "{% block page_title %}Insights · Piper{% endblock %}"
        "{% block main %}x{% endblock %}"
        "{% block scripts %}<script>window.PAGE_JS=1</script>{% endblock %}",
    )
    assert "<title>Insights · Piper</title>" in html
    assert "window.PAGE_JS=1" in html


def test_chrome_not_page_overridable(env):
    # A page trying to override header/nav/footer has NO effect — they aren't blocks.
    html = _render(
        env,
        "{% extends 'layouts/app_shell.html' %}{% block main %}m{% endblock %}"
        "{% block header %}HIJACKED{% endblock %}"
        "{% block nav %}HIJACKED{% endblock %}"
        "{% block footer %}HIJACKED{% endblock %}",
    )
    assert "HIJACKED" not in html  # nonexistent override blocks are ignored by Jinja
    assert "nav-rail" in html  # real chrome still renders


def test_aside_is_opt_in_via_show_radar(env):
    base = (
        "{% extends 'layouts/app_shell.html' %}{% block main %}m{% endblock %}"
        "{% block aside %}RADAR_SLOT{% endblock %}"
    )
    off = _render(env, base)  # default: show_radar off → no aside
    on = _render(env, base, show_radar=True)
    assert "RADAR_SLOT" not in off and "app-shell-aside" not in off
    assert "RADAR_SLOT" in on and "app-shell-aside" in on


def test_shell_template_has_no_inline_style_attr():
    # chrome styling lives in app-shell.css (token-only); the shell template adds no inline styles.
    shell = (TEMPLATES / "layouts" / "app_shell.html").read_text()
    assert "style=" not in shell


def test_shell_provides_chrome_runtime_for_widget(env):
    # The shell owns the nav-included floating-widget runtime so migrated pages don't
    # each re-declare it (the F2 chrome-completeness fix). Mirrors home.html's set.
    html = _render(env, "{% extends 'layouts/app_shell.html' %}{% block main %}x{% endblock %}")
    assert "/static/js/chat.js" in html  # the widget toggle/send
    assert "marked" in html  # markdown rendering
    assert "/static/js/permissions.js" in html  # permission prompts


def test_shell_sets_current_user_for_nav_menu(env):
    # The nav user-menu reads window.currentUser; the shell sets it from {{ user }}.
    user = {"username": "xian", "user_id": "u1", "is_admin": False}
    html = _render(
        env, "{% extends 'layouts/app_shell.html' %}{% block main %}x{% endblock %}", user=user
    )
    assert "window.currentUser" in html and "xian" in html
    # no user → explicit null (logged-out / render without a user)
    html2 = _render(env, "{% extends 'layouts/app_shell.html' %}{% block main %}x{% endblock %}")
    assert "window.currentUser = null" in html2


def test_shell_owns_skip_link_as_first_focusable(env):
    # #1265 a11y: the shell owns the "skip to content" link as the FIRST focusable element
    # (before the nav), targeting the main region — so keyboard users bypass the nav on first Tab.
    # (Pre-#1265 the per-page skip-links targeted #main-content, which no template actually had.)
    html = _render(env, "{% extends 'layouts/app_shell.html' %}{% block main %}x{% endblock %}")
    assert 'class="skip-link"' in html  # the skip-link renders
    assert 'href="#main-content"' in html  # it targets the main region
    assert 'id="main-content"' in html  # ...which now exists on the shell <main>
    assert "/static/css/skip-link.css" in html  # styling is shell-provided
    # skip-link precedes the nav in source order = first in tab order (bypasses the nav)
    assert html.index('class="skip-link"') < html.index("nav-rail")
