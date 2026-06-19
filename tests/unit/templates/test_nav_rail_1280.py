"""#1280 — the left dark-rail nav component renders the CXO-ratified content-model.

Real `template.render()` (the UI-fix discipline, not curl-200). Asserts the rail's STRUCTURE:
brand top · conversation-list region · "+ New chat" CTA · footer (nav links + trust-gated items
+ user-menu). Behavior (trust-gating visibility, dropdowns, conv-list loading) is JS, verified at
the flip (#1280 Phase 3) via the jest harness / PM UAT — a Jinja render doesn't execute JS.
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).resolve().parents[3] / "templates"
_USER = {"username": "xian", "user_id": "u1", "is_admin": False}


@pytest.fixture
def html():
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    # hide_floating_widget=True isolates the rail (skips the chat-widget include);
    # the rail's own structure is what's under test.
    return env.get_template("components/nav_rail.html").render(
        trust_stage=1, user=_USER, hide_floating_widget=True
    )


def test_rail_renders_dark_surface_container(html):
    assert 'class="nav-rail"' in html
    assert "/static/css/nav-rail.css" in html  # the dark-surface stylesheet


def test_brand_at_top(html):
    assert "nav-rail-brand" in html and "Piper Morgan" in html


def test_conversation_list_region_present(html):
    # the Slack-style conversation list (populated client-side at the flip)
    assert 'id="nav-rail-chats"' in html
    assert "Chats" in html


def test_new_chat_cta(html):
    assert 'id="nav-rail-new-chat"' in html and "New chat" in html


def test_footer_utility_links(html):
    # v2: compact footer utility links — Check in (Stage 3+), Insights, Learning, Settings.
    assert "nav-rail-utility" in html
    for label in ("Check in", "Insights", "Learning", "Settings"):
        assert label in html


def test_check_in_is_the_only_trust_gated_item(html):
    # v2: only "Check in" is gated (Stage 3+, link-level); Insights/Learning/Settings are plain.
    assert 'data-min-trust-stage="3"' in html  # Check in
    assert 'data-min-trust-stage="1"' not in html  # no Stage-1 gating in the v2 footer
    assert "nav-item-trust-gated" in html


def test_no_radar_nav_item(html):
    # v2: the "Radar" item is removed — home IS the Radar (logo links home).
    assert "nav-history-trigger" not in html


def test_your_stuff_in_avatar_menu(html):
    # v2: "Your work" moves from a footer dropdown into the user-avatar menu (the 6 user-content routes).
    assert "Your work" in html  # the avatar-menu label
    for label in ("To-dos", "Projects", "Work Items", "Files", "Documents", "Lists"):
        assert label in html


def test_avatar_menu_has_account_logout_not_settings(html):
    # v2: avatar menu = Your work / Account / Logout. Settings is a FOOTER link, not in the menu.
    assert 'id="user-menu-button"' in html and 'id="user-dropdown"' in html
    for label in ("Account", "Logout"):
        assert label in html
    assert 'id="dropdown-settings"' not in html  # the old in-menu Settings link is gone (now a footer link)


def test_is_not_the_old_top_nav(html):
    # the rail is the NEW chrome — it must not carry the top global-nav container class
    assert 'class="global-nav"' not in html


def test_home_renders_persistent_radar_aside():
    """#1280 v2 — home gets the persistent 320px Radar column (show_radar → app_shell aside)."""
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    html = env.get_template("home.html").render(trust_stage=1, user=_USER, show_radar=True)
    assert 'id="home-radar-cards"' in html  # the Radar cards container
    assert 'id="home-radar-search"' in html  # the entity-search field (reuses #1236 filter)
    assert "what I'm keeping an eye on" in html  # the Radar panel header (mock copy)
    assert "app-shell-aside" in html  # it fills the shell's 320px aside (show_radar on)
