"""#1477 — the CURRENT chat must appear in the left rail from its first turn.

Alpha-tester finding (Jake, 2026-07-25): his in-progress chat had no row in the
left panel, so he avoided "+ New chat" fearing the current conversation would be
lost — a data loss that could not happen (the server auto-creates the conversation
row on the first /api/v1/intent post; persistence worked the whole time). HOST:
*a mechanism that works but cannot be seen to work is indistinguishable from a
broken one.*

Root causes pinned here:
- nav.js loaded the rail's conversation list ONCE at DOMContentLoaded and never
  refreshed, so a conversation created after page load stayed invisible until a
  full reload.
- chat.js's conversation_created hook (#787) called home.html's loadConversations,
  which renders NOTHING since #1522 step 1 (data-only) — the refresh signal
  existed but refreshed no visible surface.
- The active row was marked only from the ?conversation= URL param, so a chat
  running via the widget was never marked current.

These are source-content assertions on nav.js/chat.js (house pattern, cf.
test_home_radar_wiring_1236.py) plus a real template.render() of nav_rail.html
for the microcopy — a Jinja render doesn't execute JS, and no jest harness exists
for web/static/js (noted gap; the site-level package.json carries no jest config).
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parents[3]
TEMPLATES = ROOT / "templates"
_USER = {"username": "xian", "user_id": "u1", "is_admin": False}


@pytest.fixture
def nav_js() -> str:
    return (ROOT / "web" / "static" / "js" / "nav.js").read_text()


@pytest.fixture
def chat_js() -> str:
    return (ROOT / "web" / "static" / "js" / "chat.js").read_text()


@pytest.fixture
def rail_html() -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    return env.get_template("components/nav_rail.html").render(
        trust_stage=1, user=_USER, hide_floating_widget=True
    )


# --- nav.js: refreshable loader, not a one-shot fetch ---


def test_rail_loader_is_a_named_refreshable_function(nav_js):
    assert "function loadRailChats(" in nav_js
    # exposed so other surfaces can refresh the rail
    assert "window.NavRail" in nav_js
    assert "refreshChats" in nav_js


def test_rail_listens_for_conversation_updated_event(nav_js):
    assert "piper:conversation-updated" in nav_js


def test_rail_resolves_active_chat_beyond_url_param(nav_js):
    # URL param first, then the picker's persisted selection, then the chat
    # widget's own session id (the conversation id for widget-started chats).
    assert "piper_active_conversation_id" in nav_js
    assert "piper_chat_session_id" in nav_js


def test_rail_synthesizes_current_chat_row_when_missing(nav_js):
    # The current conversation is ALWAYS present: if it isn't in the fetched
    # list yet (brand-new, or beyond the limit), a row is synthesized and
    # marked active.
    assert "Current chat" in nav_js
    assert "aria-current" in nav_js


# --- chat.js: the first exchange announces itself ---


def test_chat_dispatches_conversation_updated_after_exchange(chat_js):
    assert "piper:conversation-updated" in chat_js


# --- nav_rail.html: honest microcopy near "+ New chat" ---


def test_rail_renders_saved_chat_microcopy(rail_html):
    assert "Your current chat is saved" in rail_html
    assert "nav-rail-new-chat-hint" in rail_html


def test_hint_styled_in_rail_css():
    css = (ROOT / "web" / "static" / "css" / "nav-rail.css").read_text()
    assert ".nav-rail-new-chat-hint" in css
