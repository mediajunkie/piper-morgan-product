"""#1384 — the session-timeout modal's buttons must actually work.

PM's live report (2026-07-09, alpha): the "Still there?" modal appeared and
neither Continue Working nor the [x] close responded. Harness reproduction of
the rendered page surfaced a cluster of real defects in the component, pinned
here:

1. Inline ``onclick`` handlers (CSP-hostile, single-point-of-failure) — buttons
   are now wired by session-timeout.js at init via addEventListener, bound to
   stable ids.
2. ``transition: all`` animated visibility+pointer-events, leaving a
   pointer-DEAD window during the fade-in — clicks fell through to the page
   under the modal. Only opacity transitions now.
3. The modal copy promises "Move your mouse ... to stay signed in" but
   ``mousemove`` was never tracked; and ``'touch'`` is not a DOM event (that
   listener never fired once). Both fixed.
4. "Continue Working" was a placebo: it reset the CLIENT timer while the 30-min
   JWT marched on. ``extendUrl`` now defaults to the #857 refresh endpoint.

House discipline: template assertions run through a REAL Jinja render.
"""

from jinja2 import Environment, FileSystemLoader


def _render_component() -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template("components/session-timeout-modal.html").render()


def _js() -> str:
    return open("web/static/js/session-timeout.js").read()


def _css() -> str:
    return open("web/static/css/session-timeout.css").read()


class TestModalTemplate:
    def test_no_inline_onclick_handlers(self):
        html = _render_component()
        assert "onclick=" not in html

    def test_buttons_carry_binding_ids(self):
        html = _render_component()
        for el_id in (
            "session-timeout-extend",
            "session-timeout-logout",
            "session-timeout-close",
        ):
            assert f'id="{el_id}"' in html

    def test_home_still_includes_component_and_script(self):
        env = Environment(loader=FileSystemLoader("templates"))
        src = env.loader.get_source(env, "home.html")[0]
        assert "components/session-timeout-modal.html" in src
        assert "session-timeout.js" in src


class TestComponentScript:
    def test_binds_all_three_buttons(self):
        js = _js()
        for el_id in (
            "session-timeout-extend",
            "session-timeout-logout",
            "session-timeout-close",
        ):
            assert el_id in js

    def test_extend_url_defaults_to_real_refresh_endpoint(self):
        """#857's cookie-based refresh — Continue Working is no longer a placebo."""
        assert "extendUrl: '/api/v1/auth/refresh'" in _js()

    def test_promised_activity_signals_are_tracked(self):
        js = _js()
        assert "'mousemove'" in js  # the copy promises it
        assert "'touchstart'" in js  # 'touch' is not a DOM event
        assert "addEventListener('touch'," not in js

    def test_extend_sends_cookies(self):
        assert "credentials: 'same-origin'" in _js()


class TestComponentStyle:
    def test_no_pointer_dead_transition_window(self):
        """`transition: all` animated pointer-events/visibility — the fade-in
        ate clicks. Interactivity must be instant: only opacity transitions.
        Comments are stripped so prose explaining the rule can't trip it."""
        import re

        css = re.sub(r"/\*.*?\*/", "", _css(), flags=re.S)
        assert "transition: opacity" in css
        assert "transition: var(--transition-all)" not in css
        assert "transition: all" not in css
