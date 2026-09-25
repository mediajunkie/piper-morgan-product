"""#1879 — chat-widget.html and chat-inline.html both carried id="chatForm" /
id="chat-window" / id="chat-container"; on home BOTH templates are included
(`components/nav_rail.html:81` includes chat-widget.html on every shell page;
`home.html:728` includes chat-inline.html) so a naive render produced a
duplicate-id DOM, and any `getElementById`/`#id` CSS selector on those three
ids picked one instance by document order, not by intent.

Fix: the inline component's three ids are suffixed `-inline`
(chat-container-inline / chat-window-inline / chatForm-inline); the widget's
ids are unchanged. `home.html`'s own helpers (the module-scope `chatWindow`
const, `switchConversation`'s scroll-to-bottom, `clearChat`) now target
`chat-window-inline` explicitly. `chat.js` no longer looks up either id at
all — it queries the shared `.chat-window` / `.chat-form` CLASSES, so it
binds to whichever single instance is actually on the page regardless of id.

LAYER (m-43): real Jinja `Environment.get_template('home.html').render()` —
NOT a grep of the two component files in isolation, which would miss that
they're both actually included together (that's exactly how the original bug
was invisible to a per-file read).

Two render scenarios are pinned, both required to be duplicate-id-free:
  - the ACTUAL production context (`hide_floating_widget=True`, set by
    `web/api/routes/ui.py`'s `home()` route since #1266 — "home renders the
    INLINE chat -> suppress the shell floating widget"). Verified at HEAD:
    under this context the floating widget is NOT included at all, so this
    scenario alone would not have caught #1879 pre-fix.
  - the DEFENSIVE worst case (`hide_floating_widget` unset/False), i.e. the
    floating widget renders alongside the inline chat. This is the scenario
    that actually reproduced the duplicate ids pre-fix (verified: chatForm,
    chat-window, chat-container each appeared twice before this change) and
    is what the id rename is a structural guard against, independent of
    whether the render-time flag is always set correctly.

DENOMINATOR: the three ids named in #1879 (chatForm, chat-window,
chat-container) across the two chat components on home.html. This does not
assert home.html carries zero duplicate ids of ANY kind — only that these
chat-surface ids, and the DOM as a whole under either scenario, are
collision-free.
"""

import re
from collections import Counter
from pathlib import Path

import pytest
from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path("templates")


@pytest.fixture
def env():
    return Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)


def _base_ctx():
    return dict(
        current_user={"username": "xian", "display_name": "Xian"},
        user={"username": "xian"},
        trust_stage=3,
    )


def _render(env, **extra):
    ctx = _base_ctx()
    ctx.update(extra)
    return env.get_template("home.html").render(**ctx)


def _duplicate_ids(html):
    ids = re.findall(r'id="([^"]+)"', html)
    return {id_: count for id_, count in Counter(ids).items() if count > 1}


def test_no_duplicate_ids_under_production_context(env):
    """The actual route context (hide_floating_widget=True): no duplicate ids
    anywhere in the rendered page."""
    html = _render(env, hide_floating_widget=True)
    dupes = _duplicate_ids(html)
    assert not dupes, f"duplicate id= values found: {dupes}"


def test_no_duplicate_ids_when_floating_widget_not_suppressed(env):
    """Defensive worst case: hide_floating_widget unset, so both chat
    components render together (this is the exact scenario that reproduced
    #1879 pre-fix — the fix must hold even if this flag is ever dropped)."""
    html = _render(env)  # hide_floating_widget omitted -> falsy in Jinja
    dupes = _duplicate_ids(html)
    assert not dupes, f"duplicate id= values found: {dupes}"


def test_both_chat_components_present_in_worst_case(env):
    """Sanity check on the worst-case fixture itself: both components really
    are in the DOM together (otherwise the previous test would trivially
    pass without exercising the collision at all)."""
    html = _render(env)
    assert html.count('id="chat-widget-container"') == 1
    assert html.count('id="chat-container-inline"') == 1


def test_widget_ids_unchanged(env):
    """The floating widget keeps its original ids — chat.js's non-home pages
    (which only ever render the widget) depend on nothing else changing.
    Rendered WITHOUT hide_floating_widget (production home suppresses the
    widget entirely, so this has to use the worst-case context to see it at
    all — see test_both_chat_components_present_in_worst_case)."""
    html = _render(env)
    assert 'id="chatForm"' in html
    assert 'id="chat-window"' in html
    assert 'id="chat-container"' in html


def test_inline_ids_are_suffixed(env):
    """The inline component's three ids are the -inline variants."""
    html = _render(env, hide_floating_widget=True)
    assert 'id="chatForm-inline"' in html
    assert 'id="chat-window-inline"' in html
    assert 'id="chat-container-inline"' in html


def test_home_helpers_target_inline_explicitly():
    """home.html's own chatWindow references (module scope, switchConversation
    scroll-to-bottom, clearChat) all target chat-window-inline explicitly —
    not the bare id that used to collide."""
    home = Path("templates/home.html").read_text()
    assert (
        home.count('getElementById("chat-window-inline")')
        + home.count("getElementById('chat-window-inline')")
        == 3
    )
    # and no leftover un-suffixed references that would now resolve to nothing
    # on home (the widget isn't rendered there) or ambiguously elsewhere.
    assert "getElementById('chat-window')" not in home
    assert 'getElementById("chat-window")' not in home


def test_chat_js_no_longer_keys_off_either_id():
    """chat.js binds by the shared .chat-window / .chat-form CLASSES, not
    either component's id — so it works regardless of which one component is
    actually present on a given page."""
    chat_js = Path("web/static/js/chat.js").read_text()
    assert 'document.getElementById("chat-window")' not in chat_js
    assert 'document.getElementById("chatForm")' not in chat_js
    assert 'document.querySelector(".chat-window")' in chat_js
    assert 'document.querySelector(".chat-form")' in chat_js
