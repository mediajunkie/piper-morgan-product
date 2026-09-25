"""#1498 — the "Good afternoon" header must not claim liveness over a
historical conversation.

Before: the greeting line ("Good afternoon, dinp · Friday, August 7 at
2:30 PM") was computed once from `new Date()` at page load and never
touched again. Selecting an OLD conversation from history (switchConversation
in home.html) replaced the chat turns but left the header alone, so a thread
whose turns were from 8:33 AM rendered under a header timestamped 2:30 PM —
"NOW", not the conversation on screen.

Fix (templates/home.html + web/api/routes/ui.py's home() route context):
- `web/api/routes/ui.py::home()` resolves the user's configured zone via
  `services.utils.datetime_utils.user_timezone_name` (the #1576 getter — the
  SAME one every other face on this account is rendered against) and passes
  it as `user_timezone` into home.html's render context.
- home.html turns that into `const USER_TIMEZONE` and a shared `faceOptions()`
  formatter used by both states:
  - LIVE: `initializeGreeting()` — "Good afternoon, <name> · <today's face>".
    Called on page load and again from `createNewConversation()` (a fresh
    conversation has no turns — the one state where "now" is honest).
  - HISTORICAL: `renderConversationFace(firstTurnCreatedAt)` — "Conversation
    from <that conversation's own face>". Called from `switchConversation()`
    whenever the loaded conversation has turns (turns[0] = earliest, per
    GET /api/v1/conversations/{id}/turns which orders by turn_number).

LAYER (m-43, named honestly): this is a template-render pin, not a browser
test — this repo has no JS harness (confirmed absent; see
tests/unit/web/test_static_cache_policy_1859.py for the same source-pin
precedent). A Jinja render proves the server→client wiring (user_timezone
flows into USER_TIMEZONE correctly, safely JSON-encoded) and that BOTH
code paths — the live branch and the historical branch — exist, are wired
into the right call sites, and are reachable from the rendered page's own
script text. It does NOT execute the JS or prove the DOM updates at runtime;
that would need a browser. "One historical, one live" below means: two
render passes (matching the pattern already used for direct-template pins
elsewhere in this repo, e.g. test_learning_dashboard_template_1430.py) each
asserting the code for its own state, against the one template that serves
both (the branch is 100% client-side — there is no separate server-rendered
"historical" page).

Denominator (m-44): this file covers home.html's greeting/conversation-face
header only. It does not cover the adjacent "your calendar isn't connected
yet" reply text noted in #1498 (out of scope for this fix — the issue asked
only to report whether the header fix makes the thread read as clearly
historical, not to fix that reply).
"""

import re

from jinja2 import Environment, FileSystemLoader

_ENV = Environment(loader=FileSystemLoader("templates"))
_ENV.globals["asset_v"] = "test"

_BASE_CONTEXT = {
    "request": None,
    "user": {"username": "pm", "user_id": "u1498", "is_admin": False},
    "trust_stage": 3,
    "trust_stage_name": "ESTABLISHED",
    "setup_complete": True,
    "orientation_seen": True,
    "hide_floating_widget": True,
    "show_radar": True,
    "surfaced_insights": [],
}


def _render(user_timezone) -> str:
    ctx = dict(_BASE_CONTEXT, user_timezone=user_timezone)
    return _ENV.get_template("home.html").render(**ctx)


class TestServerSideTimezoneWiring:
    """The zone resolved server-side by ui.py's home() route must reach the
    client verbatim and safely — this is the part a browser test can't
    distinguish from a coincidence, so it's pinned explicitly here."""

    def test_resolved_timezone_flows_into_js_constant(self):
        html = _render("America/New_York")
        m = re.search(r"const USER_TIMEZONE = (.*?);", html)
        assert m is not None, "USER_TIMEZONE constant not found in rendered page"
        assert m.group(1) == '"America/New_York"'

    def test_missing_timezone_degrades_to_null_not_a_crash(self):
        """user_timezone_name is documented total/never-raising, but the
        template's own handling of an absent value must degrade safely too
        (falls back to the browser's ambient zone at runtime, per faceOptions())."""
        html = _render(None)
        m = re.search(r"const USER_TIMEZONE = (.*?);", html)
        assert m is not None
        assert m.group(1) == "null"

    def test_timezone_value_is_not_html_escaped_into_garbage(self):
        """|tojson must produce a valid JS string literal, not HTML-entity-escaped
        quotes that would break the JS parse."""
        html = _render("America/New_York")
        assert "&quot;" not in html.split("const USER_TIMEZONE")[1][:40]


class TestLiveState:
    """The live/new-chat state: greeting word + today's face, computed in
    USER_TIMEZONE, restored explicitly when a brand-new (turn-less)
    conversation is created."""

    def test_initialize_greeting_function_defined(self):
        html = _render("America/Los_Angeles")
        assert "function initializeGreeting()" in html

    def test_greeting_uses_shared_face_options_helper(self):
        html = _render("America/Los_Angeles")
        assert "function faceOptions()" in html
        assert 'timeElement.textContent = now.toLocaleDateString("en-US", faceOptions());' in html

    def test_greeting_word_respects_user_timezone_not_just_browser_clock(self):
        html = _render("America/Los_Angeles")
        assert "function greetingWordFor(date)" in html
        assert "timeZone: USER_TIMEZONE" in html

    def test_dom_content_loaded_calls_initialize_greeting(self):
        html = _render("America/Los_Angeles")
        assert 'document.addEventListener("DOMContentLoaded", function () {' in html
        # initializeGreeting() must be called from within that same handler.
        block = html.split('document.addEventListener("DOMContentLoaded", function () {', 1)[1]
        block = block[: block.index("});")]
        assert "initializeGreeting();" in block

    def test_new_conversation_restores_the_greeting(self):
        """A freshly created conversation has zero turns — the one honestly-live
        state — so createNewConversation() must put the greeting back (in case
        the header was showing a previous conversation's own face)."""
        html = _render("America/Los_Angeles")
        assert "async function createNewConversation()" in html
        block = html.split("async function createNewConversation()", 1)[1]
        block = block[: block.index("\n      }\n")]
        assert "initializeGreeting();" in block


class TestHistoricalState:
    """The historical state: any loaded conversation WITH turns gets its own
    face — "Conversation from <its earliest turn's date/time>" — never the
    live greeting. This is the actual #1498 fix."""

    def test_render_conversation_face_function_defined(self):
        html = _render("America/Los_Angeles")
        assert "function renderConversationFace(firstTurnCreatedAt)" in html

    def test_conversation_face_label_is_honest_not_a_greeting(self):
        html = _render("America/Los_Angeles")
        assert '"Conversation from"' in html
        # The old always-live copy must not still be reachable from this path.
        fn_body = html.split("function renderConversationFace(firstTurnCreatedAt) {", 1)[1]
        fn_body = fn_body[: fn_body.index("\n      }\n")]
        assert "Good afternoon" not in fn_body
        assert "Good morning" not in fn_body
        assert "Good evening" not in fn_body

    def test_conversation_face_uses_the_conversations_own_timestamp(self):
        """It must format `firstTurnCreatedAt` (the conversation's own turn),
        not `new Date()` (now) — that's the entire bug."""
        html = _render("America/Los_Angeles")
        fn_body = html.split("function renderConversationFace(firstTurnCreatedAt) {", 1)[1]
        fn_body = fn_body[: fn_body.index("\n      }\n")]
        assert "new Date(firstTurnCreatedAt)" in fn_body
        assert "new Date()" not in fn_body

    def test_switch_conversation_calls_historical_face_when_turns_exist(self):
        html = _render("America/Los_Angeles")
        assert "async function switchConversation(conversationId, opts)" in html
        block = html.split("async function switchConversation(conversationId, opts)", 1)[1]
        block = block[: block.index("\n      // Create a new conversation")]
        assert "if (turns.length > 0) {" in block
        assert "renderConversationFace(turns[0].created_at);" in block
        # The no-turns branch (a resumed-but-blank conversation) stays live.
        assert "} else {\n            initializeGreeting();" in block

    def test_first_turn_is_earliest_not_latest(self):
        """turns[0], not turns[turns.length - 1] — matches the API's documented
        turn_number ordering (GET /api/v1/conversations/{id}/turns), so the face
        is the conversation's START, not its most recent activity."""
        html = _render("America/Los_Angeles")
        assert "renderConversationFace(turns[0].created_at)" in html
        assert "renderConversationFace(turns[turns.length - 1]" not in html
