"""Issue 2432, CXO's follow-up row (mail 01M87SH7F2, 2026-11-24): the reset page and the
setup wizard check the two password fields in the browser and show their own sentence,
sending nothing. Those sentences are now CXO's lines, the same words the routes use.

LAYER: source text of the page and the script (the render is on the issue). DENOMINATOR:
every file under ``templates/`` and ``web/static/js/`` is scanned for the old wording."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_the_reset_page_says_the_routes_line():
    from web.api.routes.auth import NEW_PASSWORDS_DONT_MATCH_LINE

    assert NEW_PASSWORDS_DONT_MATCH_LINE == "The new passwords don't match."
    text = (ROOT / "templates/reset_password.html").read_text(encoding="utf-8")
    assert text.count('"The new passwords don\'t match."') == 1


def test_the_setup_wizard_says_the_passwords_dont_match_in_both_places():
    from services.auth.password_validator import PASSWORDS_DONT_MATCH_LINE

    assert PASSWORDS_DONT_MATCH_LINE == "The passwords don't match."
    text = (ROOT / "web/static/js/setup.js").read_text(encoding="utf-8")
    assert text.count('"The passwords don\'t match."') == 2


def test_no_page_or_script_keeps_the_old_wording():
    found = []
    for folder in ("templates", "web/static/js"):
        for path in sorted((ROOT / folder).rglob("*")):
            if path.suffix not in (".html", ".js"):
                continue
            if "do not match" in path.read_text(encoding="utf-8", errors="ignore").lower():
                found.append(path.relative_to(ROOT).as_posix())
    assert found == []


def test_the_wizards_match_rule_is_keyed_by_the_fields_name():
    """Found by render 2026-11-24: the rule was keyed 'password-confirm' (the id), which
    ``FormValidation.validateField`` looks up as ``[name="password-confirm"]`` and never
    finds, so the check never ran. The field's name is ``password_confirm``."""
    import re

    script = (ROOT / "web/static/js/setup.js").read_text(encoding="utf-8")
    page = (ROOT / "templates/setup.html").read_text(encoding="utf-8")
    assert "'password-confirm': [" not in script
    assert re.search(r"^\s+password_confirm: \[$", script, re.M)
    assert 'name="password_confirm"' in page
    start = script.index("FormValidation.init('account-form'")
    # To the end of the init call (issue 2434 made the password rule longer than the
    # fixed 900-character window this used to read).
    block = script[start : script.index("});", start)]
    keys = re.findall(r"^\s{12}'?([a-z_-]+)'?: \[", block, re.M)
    assert keys == ["username", "email", "password", "password_confirm"]
    for key in keys:
        assert f'name="{key}"' in page, key
