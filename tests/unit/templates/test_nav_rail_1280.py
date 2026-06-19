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


def test_footer_nav_links_present(html):
    for label in ("Check in", "Your stuff", "Learning", "Insights", "Radar"):
        assert label in html


def test_trust_gating_preserved(html):
    # the JS reads data-min-trust-stage to show/hide — must survive the relocation
    assert 'data-min-trust-stage="3"' in html  # Check in / Learning
    assert 'data-min-trust-stage="1"' in html  # Insights / Radar
    assert "nav-item-trust-gated" in html


def test_your_stuff_items(html):
    for label in ("To-dos", "Projects", "Work Items", "Files", "Documents", "Lists"):
        assert label in html


def test_user_menu_in_footer(html):
    assert 'id="user-menu-button"' in html
    for label in ("Settings", "Account", "Logout"):
        assert label in html


def test_is_not_the_old_top_nav(html):
    # the rail is the NEW chrome — it must not carry the top global-nav container class
    assert 'class="global-nav"' not in html
