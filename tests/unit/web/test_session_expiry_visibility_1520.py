"""#1520 — session expiry must be VISIBLE, and refresh must fire during ACTIVE use.

PM's live failure (2026-08-08): no banner or redirect on expiry; a typed chat
message was accepted and answered with wrong-blame key copy. Two client-side
defects pinned here (server-side copy is pinned in
tests/unit/web/api/routes/test_intent_session_expired_1520.py):

1. chat.js had no handling for an expired session beyond the never-firing #840
   branch: on `error_type: "session_expired"` it must (a) attempt ONE silent
   refresh via the #857 endpoint and retry the send, (b) on refresh failure make
   the expiry visible with honest copy, preserve the drafted message, and offer
   re-login.

2. session-timeout.js's ONLY refresh caller was the idle-modal's "Continue
   Working" button — i.e. refresh could fire only when the user was AWAY.
   Active use suppressed the modal, so the 30-min access token died mid-use
   (the #1520 "expires too frequently" report). A proactive, activity-aware
   refresh must run on a cadence safely inside the access-token lifetime.

House discipline: template assertions run through a REAL Jinja render
(curl-200 / source-grep of rendered claims is not a render test).
"""

import re

from jinja2 import Environment, FileSystemLoader


def _render_component(name: str) -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template(name).render()


def _chat_js() -> str:
    return open("web/static/js/chat.js").read()


def _timeout_js() -> str:
    return open("web/static/js/session-timeout.js").read()


class TestChatExpiryHandling:
    def test_chat_recognizes_session_expired_error_type(self):
        assert "session_expired" in _chat_js()

    def test_chat_attempts_silent_refresh_before_surfacing_expiry(self):
        js = _chat_js()
        assert "/api/v1/auth/refresh" in js

    def test_expiry_copy_is_honest_no_key_blame(self):
        """The chat-side expiry copy talks about signing in, never API keys."""
        js = _chat_js()
        m = re.search(r"function handleSessionExpired[\s\S]*?\n  \}", js)
        assert m, "chat.js must define handleSessionExpired(...)"
        body = m.group(0).lower()
        assert "expired" in body
        assert "api key" not in body

    def test_draft_message_is_preserved_on_expiry(self):
        """Re-login affordance preserves the drafted message: restored into the
        input AND stashed under a storage key survivable across the redirect."""
        js = _chat_js()
        assert "DRAFT_MESSAGE" in js
        assert "piper_chat_draft" in js

    def test_draft_is_restored_at_init(self):
        assert "restoreDraftMessage" in _chat_js()


class TestProactiveRefresh:
    def test_refresh_interval_configured_inside_token_lifetime(self):
        """Access token is 30 min (JWTService default); the proactive refresh
        cadence must sit safely inside it."""
        js = _timeout_js()
        m = re.search(r"refreshIntervalMinutes:\s*(\d+)", js)
        assert m, "session-timeout.js must define refreshIntervalMinutes"
        assert int(m.group(1)) < 30

    def test_proactive_refresh_wired_into_periodic_check(self):
        """Refresh must be reachable WITHOUT the idle modal: the periodic check
        loop calls maybeRefreshToken(), not only the extend() button."""
        js = _timeout_js()
        assert "maybeRefreshToken" in js
        check_loop = re.search(r"startIdleCheck\(\)\s*\{[\s\S]*?\n  \}", js)
        assert check_loop, "startIdleCheck not found"
        assert "maybeRefreshToken" in check_loop.group(0)

    def test_refresh_gated_on_recent_activity(self):
        """Idle users must NOT be kept alive forever — proactive refresh only
        fires when the user has been recently active."""
        js = _timeout_js()
        m = re.search(r"async maybeRefreshToken[\s\S]*?\n  \},", js)
        assert m, "async maybeRefreshToken definition not found"
        assert "lastActivityTime" in m.group(0)


class TestExpiredModalRender:
    def test_modal_component_still_renders_with_binding_ids(self):
        html = _render_component("components/session-timeout-modal.html")
        for el_id in (
            "session-timeout-modal",
            "session-timeout-extend",
            "session-timeout-logout",
            "session-timeout-close",
        ):
            assert f'id="{el_id}"' in html

    def test_chat_input_target_for_draft_restore_renders(self):
        """chat.js restores the draft into `.chat-input` — the rendered
        chat-inline component must actually carry that class."""
        html = _render_component("components/chat-inline.html")
        assert "chat-input" in html
