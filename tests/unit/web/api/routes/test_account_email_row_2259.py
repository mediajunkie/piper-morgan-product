"""#2259 (CXO 2026-11-02; PPM 11-03): Account Settings shows the account's email,
read-only, in the Username row's place and style; an account with no email on
record reads "No email on this account.", never blank, never a placeholder; no
change control. House discipline: a REAL template.render() through the real
shell (feedback_ui_fix_requires_template_render_test), plus the context builder.
"""

import re
from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader

from web.api.routes.ui import _extract_user_context

EMAIL_ROW = re.compile(
    r'<div class="info-label">Email</div>\s*<div class="info-value">(.*?)</div>', re.S
)


def _render(user):
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template("account.html").render(request=None, user=user)


def _email_value(html: str) -> str:
    m = EMAIL_ROW.search(html)
    assert m, "the Email row is missing from the Profile Information card"
    return " ".join(m.group(1).split())


class TestEmailRow:
    def test_the_address_shows_in_the_profile_card(self):
        html = _render(
            {
                "username": "web-pat-test",
                "user_id": "u-1",
                "is_admin": False,
                "email": "pat@example.invalid",
            }
        )
        assert _email_value(html) == "pat@example.invalid"

    def test_no_email_on_record_reads_cxos_line(self):
        for user in (
            {"username": "t", "user_id": "u-1", "is_admin": False, "email": ""},
            {"username": "t", "user_id": "u-1", "is_admin": False},
        ):
            assert _email_value(_render(user)) == "No email on this account."

    def test_the_row_sits_between_username_and_user_id(self):
        html = _render(
            {"username": "t", "user_id": "u-1", "is_admin": False, "email": "a@b.invalid"}
        )
        order = [
            html.index(f'<div class="info-label">{label}</div>')
            for label in ("Username", "Email", "User ID", "Account Type")
        ]
        assert order == sorted(order)

    def test_no_change_control_and_no_placeholder(self):
        html = _render({"username": "t", "user_id": "u-1", "is_admin": False, "email": ""})
        low = html.lower()
        assert "change email" not in low and "update email" not in low
        assert "email@example.com" not in low and "your email" not in low

    def test_signed_out_shows_a_dash_like_the_other_rows(self):
        assert _email_value(_render(None)) == "—"


class TestContextCarriesTheEmail:
    def _request(self, claims):
        return SimpleNamespace(
            state=SimpleNamespace(user_id="u-1", user_claims=claims, is_admin=False)
        )

    def test_from_object_claims(self):
        ctx = _extract_user_context(
            self._request(SimpleNamespace(user_email=" pat@example.invalid "))
        )
        assert ctx["email"] == "pat@example.invalid"

    def test_from_dict_claims(self):
        ctx = _extract_user_context(self._request({"user_email": "d@example.invalid"}))
        assert ctx["email"] == "d@example.invalid"

    def test_no_claims_or_no_email_is_empty_never_a_placeholder(self):
        assert _extract_user_context(self._request(None))["email"] == ""
        assert _extract_user_context(self._request(SimpleNamespace(user_email=None)))["email"] == ""
        assert _extract_user_context(self._request({}))["email"] == ""

    def test_the_route_is_registered(self):
        import web.api.routes.ui as ui

        assert "/account" in [r.path for r in ui.router.routes]
