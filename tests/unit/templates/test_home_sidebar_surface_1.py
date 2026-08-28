"""home.html conversation-list surface — post-excision contract (#1522 step 1).

History: this file originally pinned the #1097 Round-2 Surface-1 contract on
home's OWN left sidebar (aside#sidebar, "Recent" header, 5-active fetch). #1280
hid that sidebar (the app_shell nav rail took over the conversation list) but
left the markup + renderer in place, and the hidden twin became a fix-magnet —
a #1482 copy fix shipped dark into it (#1516). #1522 step 1 excised it.

These are REAL template.render() tests (house rule: curl-200 is not a render
test). They gate the excision:
  1. home.html still renders cleanly without the excised block;
  2. the live rail include (components/nav_rail.html via layouts/app_shell.html)
     survives in the rendered page, as does the history_sidebar include;
  3. the dead surface stays dead — no aside#sidebar, no .conversation-item
     renderer may return to home.html (regression pin against rebuilding the
     fix-magnet);
  4. the auto-select data fetch (Surface-1's surviving piece: most-recent
     ACTIVE conversation id for #583 auto-select) is still present.
"""

from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).resolve().parents[3] / "templates"


@pytest.fixture
def rendered() -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    return env.get_template("home.html").render(trust_stage=1, show_radar=True, user_name="tester")


@pytest.fixture
def source() -> str:
    return (TEMPLATES / "home.html").read_text()


def test_home_renders_without_excised_sidebar(rendered: str) -> None:
    """The excision gate: a full jinja2 render must succeed and produce the
    live page skeleton (rendering at all is the assertion that matters —
    a stranded include/endblock would raise TemplateError here)."""
    assert '<div class="app-layout">' in rendered
    assert '<div class="main-content">' in rendered
    assert "chat" in rendered.lower()


def test_live_rail_include_survives(rendered: str) -> None:
    """The conversation list users actually see: the left dark rail
    (components/nav_rail.html, included by layouts/app_shell.html and
    populated by static/js/nav.js)."""
    assert 'id="nav-rail"' in rendered
    assert 'id="nav-rail-chats"' in rendered, (
        "nav rail's conversation-list region must be in the rendered page — "
        "it is the ONLY visible conversation list (#1280 conv-list-everywhere)"
    )


def test_history_sidebar_include_survives(rendered: str) -> None:
    """Right slide-out (full archive) — its own renderer, untouched by the
    excision."""
    assert 'class="history-sidebar"' in rendered


def test_dead_sidebar_stays_dead(source: str) -> None:
    """Cauterization pin: the legacy surface must not be rebuilt in home.html.
    It shipped a fix dark once (#1516) — if you need conversation-list UI,
    it belongs in components/nav_rail.html (+ static/js/nav.js) or
    components/history_sidebar.html, never here."""
    assert 'id="sidebar"' not in source
    assert 'class="conversation-item' not in source
    assert "renderConversationItem" not in source
    assert "renderConversationList" not in source
    assert "archiveConversation" not in source
    assert "deleteConversation" not in source
    assert "toggleSidebar" not in source


def test_autoselect_fetch_survives(source: str) -> None:
    """Surface-1's surviving piece: loadConversations still fetches recent
    ACTIVE conversations to return the most-recent id for auto-select (#583) —
    data only, no rendering."""
    assert "/api/v1/conversations?state=active&limit=5" in source
