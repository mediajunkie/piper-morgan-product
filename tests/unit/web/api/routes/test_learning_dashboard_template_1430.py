"""#1430 (F19) — learning dashboard template: no phantom user, authed endpoints only.

House discipline (feedback_ui_fix_requires_template_render_test): UI changes are
verified by a REAL template.render() through the real shell, not file greps and
not a bare route 200.

Before: the page hardcoded `USER_ID = 'current_user'` and passed it as a
client-supplied user_id on the Export/Clear fetches (which pointed at
unregistered Sprint A5 routes → the buttons 404'd for everyone).
"""

from jinja2 import Environment, FileSystemLoader


def _render() -> str:
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template("learning-dashboard.html").render(
        request=None, user={"username": "t"}
    )


class TestLearningDashboardNoPhantomUser:
    def test_no_hardcoded_user_id_constant(self):
        html = _render()
        assert "USER_ID" not in html
        assert "'current_user'" not in html  # the phantom principal literal

    def test_no_client_supplied_user_id_on_any_fetch(self):
        html = _render()
        assert "user_id=" not in html  # identity comes from the session, never the client

    def test_export_and_clear_hit_the_authed_routes(self):
        html = _render()
        assert "/controls/export?format=json" in html
        assert "/controls/data/clear?data_type=" in html

    def test_settings_and_patterns_fetches_present_with_credentials(self):
        """The toggle/status/metrics surfaces ride the authed #300 routes."""
        html = _render()
        assert "const API_BASE = '/api/v1/learning'" in html
        assert "${API_BASE}/settings" in html
        assert "${API_BASE}/patterns" in html
        assert "credentials: 'include'" in html

    def test_dashboard_route_registered_in_ui_module(self):
        """The page is reachable: ui.py declares GET /learning."""
        import web.api.routes.ui as ui

        paths = [r.path for r in ui.router.routes]
        assert "/learning" in paths
