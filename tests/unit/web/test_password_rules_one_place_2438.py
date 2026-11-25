"""Issue 2438: one password rule set, stated whole, read from one place.

Arch (mails 01M8A7N4F1, 01M8A7PQQ6): every path that sets a person's chosen password asks
``PasswordValidator.failed_rule`` and answers through ``password_rule_line``. CXO (mail
01M8A7MG8Q): the page states the whole rule before submit, and a refusal states the whole
rule, not the part that failed.

LAYERS: the route tests drive the real ``create_user`` body or the app's real handlers;
the page tests render the real templates through the real page routes. Nothing here is a
browser; what a person sees in one is the served check on the issue.
"""

import ast
import html
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]

HELPER = (
    "At least 8 characters, with an uppercase letter, a lowercase letter, a number and "
    "one of ! @ # $ % ^ & * ( )."
)
RULE = (
    "Your password needs at least 8 characters, an uppercase letter, a lowercase letter, "
    "a number and one of ! @ # $ % ^ & * ( )."
)

# One password per strength rule, each breaking only that rule.
BREAKS_ONE_RULE = [
    ("Ab1!xyz", "too_short"),
    ("abcdefg1!", "no_uppercase"),
    ("ABCDEFG1!", "no_lowercase"),
    ("Abcdefgh!", "no_digit"),
    ("Abcdefg12", "no_special"),
]


class TestTheTwoSentences:
    def test_cxos_words_pinned_once(self):
        from services.auth import password_validator as pv

        assert pv.PASSWORD_RULE_HELPER_LINE == HELPER
        assert pv.PASSWORD_RULE_LINE == RULE

    def test_both_are_built_from_the_validators_own_values(self):
        """A changed minimum or special set changes both sentences: run the module's
        source with different values in a scope of its own and read them there."""
        src = (ROOT / "services/auth/password_validator.py").read_text(encoding="utf-8")
        changed = src.replace("MIN_LENGTH = 8", "MIN_LENGTH = 12").replace(
            'SPECIAL_CHARS = "!@#$%^&*()"', 'SPECIAL_CHARS = "!?"'
        )
        assert changed != src
        scope: dict = {"__name__": "password_validator_changed"}
        exec(compile(changed, "password_validator_changed", "exec"), scope)
        assert scope["PASSWORD_RULE_HELPER_LINE"].startswith("At least 12 characters, ")
        assert scope["PASSWORD_RULE_HELPER_LINE"].endswith("one of ! ?.")
        assert "at least 12 characters" in scope["PASSWORD_RULE_LINE"]
        assert scope["PASSWORD_RULE_LINE"].endswith("one of ! ?.")

    def test_the_sentences_name_every_rule_the_validator_checks(self):
        """A sixth rule added to ``failed_rule`` fails here until the sentences and
        ``STRENGTH_RULES`` are read again."""
        from services.auth import password_validator as pv

        tree = ast.parse((ROOT / "services/auth/password_validator.py").read_text("utf-8"))
        func = next(
            n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "failed_rule"
        )
        returned = {
            n.value.id
            for n in ast.walk(func)
            if isinstance(n, ast.Return) and isinstance(n.value, ast.Name)
        }
        assert returned == {
            "RULE_EMPTY",
            "RULE_TOO_SHORT",
            "RULE_NO_UPPERCASE",
            "RULE_NO_LOWERCASE",
            "RULE_NO_DIGIT",
            "RULE_NO_SPECIAL",
        }
        assert set(pv.STRENGTH_RULES) == {getattr(pv, n) for n in returned} - {pv.RULE_EMPTY}

    @pytest.mark.parametrize("password, code", BREAKS_ONE_RULE)
    def test_each_strength_rule_answers_the_one_line(self, password, code):
        from services.auth.password_validator import PasswordValidator, password_rule_line

        assert PasswordValidator.failed_rule(password) == code
        assert password_rule_line(code) == RULE

    def test_empty_and_mismatch_keep_their_own_lines(self):
        from services.auth.password_validator import password_rule_line

        assert password_rule_line("empty") == "Your password can't be empty."
        assert password_rule_line("mismatch") == "The passwords don't match."

    def test_the_per_rule_lines_are_gone(self):
        from services.auth import password_validator as pv

        for name in (
            "PASSWORD_TOO_SHORT_LINE",
            "PASSWORD_NEEDS_UPPERCASE_LINE",
            "PASSWORD_NEEDS_LOWERCASE_LINE",
            "PASSWORD_NEEDS_NUMBER_LINE",
            "PASSWORD_NEEDS_SPECIAL_LINE",
        ):
            assert not hasattr(pv, name)


class TestAccountCreationAppliesTheSameRules:
    """The real ``create_user`` body. The checks run before anything is read or written,
    so a refused password never reaches the invite code."""

    @staticmethod
    async def _refusal(password):
        from web.api.routes import setup as setup_routes

        req = setup_routes.CreateUserRequest(
            username="rule-check",
            email="rule-check@example.com",
            password=password,
            password_confirm=password,
            invite_token="never-read",
        )
        with pytest.raises(setup_routes.UserFacingHTTPException) as caught:
            await setup_routes.create_user(req)
        return caught.value

    @pytest.mark.asyncio
    @pytest.mark.parametrize("password, code", BREAKS_ONE_RULE)
    async def test_each_broken_rule_is_refused_with_the_whole_rule(self, password, code):
        refusal = await self._refusal(password)
        assert refusal.status_code == 400
        assert refusal.detail == RULE

    @pytest.mark.asyncio
    async def test_the_password_creation_once_accepted_is_now_refused(self):
        refusal = await self._refusal("password1")
        assert refusal.detail == RULE

    def test_the_route_holds_no_length_check_of_its_own(self):
        src = (ROOT / "web/api/routes/setup.py").read_text(encoding="utf-8")
        assert "MIN_LENGTH" not in src
        assert "len(req.password)" not in src
        assert src.count("PasswordValidator.failed_rule(req.password)") == 1


class TestEveryPathThatSetsAChosenPasswordAsksTheValidator:
    def test_the_three_routes(self):
        auth = (ROOT / "web/api/routes/auth.py").read_text(encoding="utf-8")
        setup = (ROOT / "web/api/routes/setup.py").read_text(encoding="utf-8")
        assert auth.count("PasswordValidator.failed_rule(data.new_password)") == 2
        assert setup.count("PasswordValidator.failed_rule(req.password)") == 1

    def test_the_cli_wizard(self):
        src = (ROOT / "scripts/setup_wizard.py").read_text(encoding="utf-8")
        assert "PasswordValidator.failed_rule(password)" in src
        assert "PASSWORD_RULE_HELPER_LINE" in src and "PASSWORD_RULE_LINE" in src
        assert "len(password) < 8" not in src
        assert "min 8 characters" not in src

    def test_the_operator_script(self):
        src = (ROOT / "scripts/setup_alpha_passwords.py").read_text(encoding="utf-8")
        assert "PasswordValidator.failed_rule(password)" in src
        assert "len(password) < 8" not in src

    def test_no_other_file_hashes_a_typed_password_without_the_validator(self):
        """The denominator: every file under web/, services/ and scripts/ that calls
        ``hash_password``. Each is on this list with its reason, so a new write path
        fails here until someone decides whether it takes a person's choice."""
        callers = set()
        for top in ("web", "services", "scripts", "cli"):
            for path in (ROOT / top).rglob("*.py"):
                if "hash_password(" in path.read_text(encoding="utf-8", errors="ignore"):
                    callers.add(str(path.relative_to(ROOT)))
        assert callers == KNOWN_HASH_CALLERS


# Six files call ``hash_password`` (scan run for issue 2438). What each does with a rule:
KNOWN_HASH_CALLERS = {
    "services/auth/password_service.py",  # defines it; also hashes its own generated temp password
    "web/api/routes/auth.py",  # change and reset: the validator (pinned above)
    "web/api/routes/setup.py",  # account creation: the validator (pinned above)
    "scripts/setup_wizard.py",  # the CLI wizard: the validator (pinned above)
    "scripts/setup_alpha_passwords.py",  # operator sets one: the validator (pinned below)
    # A dev and staging test-account tool: ``--password`` or a generated one, written
    # straight to the row. Not a person choosing their own password; reported to Arch
    # with issue 2438 rather than changed here.
    "scripts/create_test_alpha_user.py",
}


class TestThePagesStateTheWholeRule:
    @staticmethod
    def _page(path):
        from fastapi.testclient import TestClient

        from web.app import app

        # Startup sets the templates; a test client without startup sets them the same
        # way (as tests/unit/web/test_signed_out_modal_2067.py does).
        if getattr(app.state, "templates", None) is None:
            from fastapi.templating import Jinja2Templates

            app.state.templates = Jinja2Templates(directory=str(ROOT / "templates"))
        return TestClient(app, follow_redirects=False).get(path)

    def test_the_reset_page(self):
        reply = self._page("/reset-password")
        assert reply.status_code == 200
        # The page escapes the ampersand; a browser shows it as written.
        assert reply.text.count(html.escape(HELPER)) == 1
        assert 'aria-describedby="new-password-rule"' in reply.text
        assert 'At least 8 characters"' not in reply.text  # the old placeholder

    def test_the_setup_wizard(self):
        reply = self._page("/setup")
        assert reply.status_code == 200
        # The page escapes the ampersand; a browser shows it as written.
        assert reply.text.count(html.escape(HELPER)) == 1
        assert "<small>At least 8 characters</small>" not in reply.text

    @pytest.mark.parametrize("name", ["setup.html", "reset_password.html"])
    def test_no_template_carries_its_own_copy_of_the_rule(self, name):
        src = (ROOT / "templates" / name).read_text(encoding="utf-8")
        assert "{{ password_rule_helper }}" in src
        assert not re.search(r"At least \d+ characters", src)
        assert "uppercase letter" not in src
