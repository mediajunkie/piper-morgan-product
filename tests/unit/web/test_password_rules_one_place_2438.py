"""Issue 2438: one password rule, length only, read from one place.

xian (2026-11-26, relayed by Exec 01M8CDTHCC and 01M8CEG65R): length-only, minimum 15
characters, maximum 72 bytes. Arch (01M8CE2GFC, amended 01M8CECPDT): every path that
sets a person's chosen password asks ``PasswordValidator.failed_rule`` and answers
through ``password_rule_line``; no composition rule survives anywhere. CXO (01M8CEMET5):
a helper under every new-password field and one refusal per rule, each true for its code.

This replaces the 2026-11-25 build of the same issue (five composition rules, one
whole-rule refusal).

LAYERS: the route tests drive the real ``create_user`` body or the app's real handlers;
the page tests render the real templates through the real page routes. Nothing here is a
browser; what a person sees in one is the served check on the issue.
"""

import ast
import html
import re
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]

HELPER = (
    "At least 15 characters, and no more than 72 bytes: an English letter or digit is one byte, "
    "any other letter or an emoji is two to four."
)
TOO_SHORT = "Your password needs at least 15 characters."
TOO_LONG = (
    "Your password is too long: the most is 72 bytes. An English letter or digit is one byte, "
    "any other letter or an emoji is two to four."
)

# The composition rules' names. None may be left outside tests (Arch's condition 1).
DELETED_NAMES = (
    "RULE_NO_UPPERCASE",
    "RULE_NO_LOWERCASE",
    "RULE_NO_DIGIT",
    "RULE_NO_SPECIAL",
    "SPECIAL_CHARS",
    "_SPECIALS_AS_READ",
    "STRENGTH_RULES",
)


class TestTheRule:
    """Arch's condition 7, at the minimum xian chose (15)."""

    @staticmethod
    def _rule(password):
        from services.auth.password_validator import PasswordValidator

        return PasswordValidator.failed_rule(password)

    def test_the_two_numbers(self):
        from services.auth.password_validator import PasswordValidator

        assert PasswordValidator.MIN_LENGTH == 15
        assert PasswordValidator.MAX_PASSWORD_BYTES == 72

    def test_fifteen_lowercase_letters_pass_with_no_classes(self):
        assert self._rule("abcdefghijklmno") is None

    def test_fourteen_characters_are_refused(self):
        assert self._rule("abcdefghijklmn") == "too_short"

    def test_a_space_counts_as_typed(self):
        assert self._rule("abcdefghijklmn ") is None
        assert self._rule("              ") == "too_short"  # 14 spaces
        assert self._rule("               ") is None  # 15 spaces: no strip

    def test_exactly_72_ascii_bytes_pass_and_73_are_refused(self):
        assert self._rule("a" * 72) is None
        assert self._rule("a" * 73) == "too_long"

    def test_the_cap_counts_bytes_not_characters(self):
        assert len(("😀" * 18).encode("utf-8")) == 72
        assert self._rule("😀" * 18) is None
        assert self._rule("😀" * 19) == "too_long"
        # 37 accented letters are 74 bytes: under 72 characters, over 72 bytes.
        assert self._rule("é" * 37) == "too_long"
        assert self._rule("é" * 36) is None

    def test_the_minimum_counts_characters_not_bytes(self):
        # 14 emoji are 56 bytes but 14 characters.
        assert self._rule("😀" * 14) == "too_short"
        assert self._rule("😀" * 15) is None

    def test_empty_is_its_own_code(self):
        assert self._rule("") == "empty"

    def test_yesterdays_composition_examples_are_judged_on_length_alone(self):
        assert self._rule("password1") == "too_short"  # 9 characters
        assert self._rule("Abcdefg1!") == "too_short"  # passed the five rules; 9 characters
        assert self._rule("correct horse battery") is None  # no capital, digit or symbol

    def test_bcrypt_really_does_ignore_bytes_past_72(self):
        """The reason for the cap, measured here so an upgrade that changes it is seen:
        on our pin a long password's hash verifies against its first 72 bytes; a later
        bcrypt raises instead. Either way a password over the cap must be refused at
        set time, which is what the rule does."""
        import bcrypt

        long_password = b"a" * 72 + b"TAIL-THAT-IS-IGNORED"
        try:
            hashed = bcrypt.hashpw(long_password, bcrypt.gensalt(rounds=4))
        except ValueError:
            return  # bcrypt 5 and later: refuses outright
        assert bcrypt.checkpw(b"a" * 72, hashed)


class TestTheSentences:
    def test_cxos_words_pinned_once(self):
        from services.auth import password_validator as pv

        assert pv.PASSWORD_RULE_HELPER_LINE == HELPER
        assert pv.PASSWORD_TOO_SHORT_LINE == TOO_SHORT
        assert pv.PASSWORD_TOO_LONG_LINE == TOO_LONG

    def test_all_three_are_built_from_the_validators_own_values(self):
        """A changed minimum or cap changes the sentences: run the module's source with
        different values in a scope of its own and read them there."""
        src = (ROOT / "services/auth/password_validator.py").read_text(encoding="utf-8")
        changed = src.replace("MIN_LENGTH = 15", "MIN_LENGTH = 12").replace(
            "MAX_PASSWORD_BYTES = 72", "MAX_PASSWORD_BYTES = 64"
        )
        assert changed.count("MIN_LENGTH = 12") == 1 and changed.count("BYTES = 64") == 1
        scope: dict = {"__name__": "password_validator_changed"}
        exec(compile(changed, "password_validator_changed", "exec"), scope)
        assert scope["PASSWORD_RULE_HELPER_LINE"].startswith(
            "At least 12 characters, and no more than 64 bytes: "
        )
        assert scope["PASSWORD_TOO_SHORT_LINE"] == "Your password needs at least 12 characters."
        assert scope["PASSWORD_TOO_LONG_LINE"].startswith(
            "Your password is too long: the most is 64 bytes. "
        )

    def test_failed_rule_returns_exactly_three_codes(self):
        """A rule added to ``failed_rule`` fails here until it has a sentence."""
        tree = ast.parse((ROOT / "services/auth/password_validator.py").read_text("utf-8"))
        func = next(
            n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "failed_rule"
        )
        returned = {
            n.value.id
            for n in ast.walk(func)
            if isinstance(n, ast.Return) and isinstance(n.value, ast.Name)
        }
        assert returned == {"RULE_EMPTY", "RULE_TOO_SHORT", "RULE_TOO_LONG"}

    def test_each_code_has_its_own_true_line(self):
        from services.auth.password_validator import password_rule_line

        assert password_rule_line("empty") == "Your password can't be empty."
        assert password_rule_line("too_short") == TOO_SHORT
        assert password_rule_line("too_long") == TOO_LONG
        assert password_rule_line("mismatch") == "The passwords don't match."

    def test_a_code_with_no_line_gets_none_and_the_scripts_fallback(self):
        from services.auth import password_validator as pv

        assert pv.password_rule_line("no_uppercase") is None
        assert pv.password_refusal_line("no_uppercase") == pv.PASSWORD_CANT_BE_USED_LINE
        assert pv.password_refusal_line("too_short") == TOO_SHORT

    def test_the_composition_rules_are_gone_from_the_module(self):
        from services.auth import password_validator as pv

        for name in DELETED_NAMES + ("PASSWORD_RULE_LINE",):
            assert not hasattr(pv, name), name
        assert not hasattr(pv.PasswordValidator, "SPECIAL_CHARS")

    def test_no_file_outside_tests_names_a_composition_rule(self):
        """Arch's condition 1: ``git grep`` for each deleted name outside tests. The
        whole tracked tree is the denominator (docs and dev logs are history, left out)."""
        for name in DELETED_NAMES:
            found = subprocess.run(
                [
                    "git",
                    "grep",
                    "-l",
                    "-w",
                    name,
                    "--",
                    ".",
                    ":!tests",
                    ":!docs",
                    ":!dev",
                    ":!mailboxes",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            assert found.stdout.split() == [], (name, found.stdout)

    def test_no_sentence_a_person_reads_names_a_character_class(self):
        from services.auth import password_validator as pv

        for name in dir(pv):
            if name.endswith("_LINE"):
                line = getattr(pv, name).lower()
                for word in ("uppercase", "lowercase", "special", "a number"):
                    assert word not in line, (name, word)


class TestAccountCreationAppliesTheSameRule:
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
    async def test_too_short_is_refused_with_its_line(self):
        refusal = await self._refusal("Abcdefg1!")
        assert refusal.status_code == 400
        assert refusal.detail == TOO_SHORT

    @pytest.mark.asyncio
    async def test_too_long_is_refused_with_its_line(self):
        refusal = await self._refusal("a" * 73)
        assert refusal.status_code == 400
        assert refusal.detail == TOO_LONG

    def test_the_route_holds_no_length_check_of_its_own(self):
        src = (ROOT / "web/api/routes/setup.py").read_text(encoding="utf-8")
        assert "MIN_LENGTH" not in src
        assert "len(req.password)" not in src
        assert src.count("PasswordValidator.failed_rule(req.password)") == 1


class TestEveryPathThatSetsAChosenPasswordAsksTheValidator:
    def test_the_seat_script_makes_a_password_the_rule_accepts(self):
        """Arch's condition 6: the script's password (43 characters since the tail was
        dropped, once beta served the length-only build) passes the rule."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "seat_account_create_2438", ROOT / "scripts/seat_account_create.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        from services.auth.password_validator import PasswordValidator

        for _ in range(50):
            assert PasswordValidator.failed_rule(module.new_password()) is None

    def test_the_three_routes(self):
        auth = (ROOT / "web/api/routes/auth.py").read_text(encoding="utf-8")
        setup = (ROOT / "web/api/routes/setup.py").read_text(encoding="utf-8")
        assert auth.count("PasswordValidator.failed_rule(data.new_password)") == 2
        assert setup.count("PasswordValidator.failed_rule(req.password)") == 1

    def test_the_cli_wizard(self):
        src = (ROOT / "scripts/setup_wizard.py").read_text(encoding="utf-8")
        assert "PasswordValidator.failed_rule(password)" in src
        assert "PASSWORD_RULE_HELPER_LINE" in src and "password_refusal_line(rule)" in src
        assert "len(password) < 8" not in src
        assert "min 8 characters" not in src

    def test_the_operator_script(self):
        src = (ROOT / "scripts/setup_alpha_passwords.py").read_text(encoding="utf-8")
        assert "PasswordValidator.failed_rule(password)" in src
        assert "password_refusal_line(rule)" in src
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


class TestThePagesStateTheRule:
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

    @staticmethod
    def _password_inputs(page_text):
        return [t for t in re.findall(r"<input\b[^>]*>", page_text) if 'type="password"' in t]

    def test_the_reset_page(self):
        reply = self._page("/reset-password")
        assert reply.status_code == 200
        assert reply.text.count(html.escape(HELPER)) == 1
        assert 'aria-describedby="new-password-rule"' in reply.text

    def test_the_setup_wizard(self):
        reply = self._page("/setup")
        assert reply.status_code == 200
        assert reply.text.count(html.escape(HELPER)) == 1

    @pytest.mark.parametrize("path, fields", [("/reset-password", 2), ("/setup", 2)])
    def test_every_new_password_field_carries_the_validators_minimum(self, path, fields):
        """Arch's condition 5: minlength equals MIN_LENGTH on both fields of both pages,
        rendered from the constant; and no maxlength (the route judges bytes)."""
        from services.auth.password_validator import PasswordValidator

        inputs = [
            t
            for t in self._password_inputs(self._page(path).text)
            if re.search(r'name="(password|password_confirm|new_password|new_password_confirm)"', t)
        ]
        assert len(inputs) == fields, inputs
        for tag in inputs:
            assert f'minlength="{PasswordValidator.MIN_LENGTH}"' in tag, tag
            assert "maxlength" not in tag, tag

    @pytest.mark.parametrize("name", ["setup.html", "reset_password.html"])
    def test_no_template_carries_its_own_copy_of_the_rule(self, name):
        src = (ROOT / "templates" / name).read_text(encoding="utf-8")
        assert "{{ password_rule_helper }}" in src
        assert not re.search(r"At least \d+ characters", src)
        assert not re.search(r'minlength="\d+"[^>]*autocomplete="new-password"', src)
        assert 'minlength="8"' not in src and 'minlength="15"' not in src
        assert "uppercase letter" not in src

    def test_the_wizards_script_reads_the_fields_own_minimum(self):
        """setup.js held a literal 8. It now reads the field's minlength, which the page
        renders from the constant."""
        src = (ROOT / "web/static/js/setup.js").read_text(encoding="utf-8")
        assert "field.minLength" in src
        assert "length >= 8" not in src
        assert not re.search(r"Needs at least \d+ characters", src)
