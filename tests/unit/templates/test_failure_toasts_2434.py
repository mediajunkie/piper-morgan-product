"""Issue 2434: the pages' own failure toasts say what failed and what to do, in CXO's words.

These are fallbacks. Where a page reads the route's reply through the shared reader
(``RouteMessage.read``, issue 2431), the route's own ``message`` still wins.

LAYER: template source. A string here is what the page's script passes to ``Toast.show``;
no browser ran. DENOMINATOR: every file under ``templates/`` and ``web/static/js/``.
"""

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]

CONNECTIONS = r"I couldn\'t load your connections. Try refreshing the page."
TEST_ALL = r"I couldn\'t test your connections just now. Try again in a moment."
NOTION = r"I couldn\'t load your Notion databases. Try refreshing the page."
CALENDARS = r"I couldn\'t load your calendars. Try refreshing the page."
LOAD_TITLE = r"'Couldn\'t load'"
TEST_TITLE = r"'Couldn\'t test'"

# (page, the line, its title, how many times the page shows it)
TOASTS = [
    ("templates/settings_calendar.html", CONNECTIONS, LOAD_TITLE, 1),
    ("templates/settings_github.html", CONNECTIONS, LOAD_TITLE, 1),
    ("templates/settings_notion.html", CONNECTIONS, LOAD_TITLE, 1),
    ("templates/settings_slack.html", CONNECTIONS, LOAD_TITLE, 1),
    ("templates/settings_notion.html", NOTION, LOAD_TITLE, 1),
    ("templates/settings_calendar.html", CALENDARS, LOAD_TITLE, 1),
    # Test All: once behind the shared reader (a refused request), once in the catch.
    ("templates/integrations.html", TEST_ALL, TEST_TITLE, 2),
]

RETIRED = [
    "Failed to load connection status",
    "Failed to test connections",
    "Failed to load Notion databases",
    "Failed to load calendar list",
]

ERROR_TITLE = re.compile(r"""Toast\.show\(\s*['"](?:error|warning)['"]\s*,\s*['"`]Error['"`]""")


def _pages():
    files = sorted((ROOT / "templates").rglob("*.html"))
    files += sorted((ROOT / "web/static/js").rglob("*.js"))
    return files


@pytest.mark.parametrize("page, line, title, times", TOASTS)
def test_each_toast_carries_cxos_words_under_its_title(page, line, title, times):
    text = (ROOT / page).read_text(encoding="utf-8")
    plain = f"Toast.show('error', {title}, '{line}');"
    through_the_reader = f"Toast.show('error', {title}, RouteMessage.read(body, '{line}'));"
    assert text.count(plain) + text.count(through_the_reader) == times
    # And the line is in no toast under any other title. (The calendar page also shows
    # its line in the empty list, which is not a toast.)
    toasts_with_the_line = [
        row for row in text.splitlines() if "Toast.show(" in row and line in row
    ]
    assert len(toasts_with_the_line) == times


def test_the_words_read_as_cxo_wrote_them():
    # The page source escapes the apostrophe; this is what a person reads.
    assert CONNECTIONS.replace("\\'", "'") == (
        "I couldn't load your connections. Try refreshing the page."
    )
    assert TEST_ALL.replace("\\'", "'") == (
        "I couldn't test your connections just now. Try again in a moment."
    )
    assert NOTION.replace("\\'", "'") == (
        "I couldn't load your Notion databases. Try refreshing the page."
    )
    assert (
        CALENDARS.replace("\\'", "'") == "I couldn't load your calendars. Try refreshing the page."
    )


def test_test_all_keeps_the_routes_own_message_first():
    text = (ROOT / "templates/integrations.html").read_text(encoding="utf-8")
    assert f"RouteMessage.read(body, '{TEST_ALL}')" in text


@pytest.mark.parametrize("old", RETIRED)
def test_the_old_words_are_gone_from_every_page(old):
    holders = [p.relative_to(ROOT).as_posix() for p in _pages() if old in p.read_text("utf-8")]
    assert holders == []


def test_the_primary_calendar_check_is_unchanged():
    text = (ROOT / "templates/settings_calendar.html").read_text(encoding="utf-8")
    assert "Primary calendar must be in the selected list" in text


def test_no_new_toast_takes_the_bare_title_error():
    """One is left, kept on purpose: the GitHub repositories load failure (ruled with
    issue 2430: the line for a failure nobody could name). A new one fails here."""
    found = {}
    for path in _pages():
        count = len(ERROR_TITLE.findall(path.read_text(encoding="utf-8")))
        if count:
            found[path.relative_to(ROOT).as_posix()] = count
    assert found == {"templates/settings_github.html": 1}


# ---- the sweep row: page text that contradicted the route in fact (CXO, mail 01M89MSJ49) ----


def test_the_upload_picker_offers_exactly_the_kinds_the_route_accepts():
    from web.api.routes.files import ALLOWED_EXTENSIONS

    text = (ROOT / "templates/files.html").read_text(encoding="utf-8")
    accepts = re.findall(r'accept="([^"]*)"', text)
    assert len(accepts) == 1
    assert set(accepts[0].split(",")) == set(ALLOWED_EXTENSIONS)
    assert ".doc" not in accepts[0].split(",")  # the old Word format the route refuses


def test_the_upload_helper_names_the_word_kind_that_is_accepted():
    text = (ROOT / "templates/files.html").read_text(encoding="utf-8")
    assert "Max size: 10MB. Allowed: Text, PDF, Word (.docx), Markdown, JSON" in text
    assert "Allowed: Text, PDF, Word, Markdown" not in text


def test_the_upload_helpers_size_is_the_routes_limit():
    from web.api.routes.files import MAX_FILE_SIZE

    assert MAX_FILE_SIZE == 10 * 1024 * 1024


def test_the_setup_wizard_counts_the_password_as_typed():
    """Arch (mail 01M89MNGKX): the password field only. The shared ``minLength`` still
    trims, which is right for the username."""
    from services.auth.password_validator import PasswordValidator

    setup = (ROOT / "web/static/js/setup.js").read_text(encoding="utf-8")
    start = setup.index("password: [", setup.index("FormValidation.init('account-form'"))
    rule = setup[start : setup.index("],", start)]
    assert "Validators.minLength" not in rule
    assert ".trim()" not in rule
    assert f"(field.value || '').length >= {PasswordValidator.MIN_LENGTH}" in rule
    assert "'Needs at least 8 characters'" in rule
    assert "username: [Validators.required(), Validators.minLength(3)]" in setup

    shared = (ROOT / "web/static/js/form-validation.js").read_text(encoding="utf-8")
    block = shared[shared.index("minLength: (length)") :][:200]
    assert "field.value?.trim()" in block


def test_the_setup_email_field_cannot_send_more_than_the_route_accepts():
    """Arch (mail 01M89PD7NG): the page enforces the model's limit first, so a person cannot
    meet the generic validation sentence; the model's rule stays as the backstop for a script."""
    from web.api.routes.setup import CreateUserRequest

    limit = next(
        m.max_length
        for m in CreateUserRequest.model_fields["email"].metadata
        if getattr(m, "max_length", None) is not None
    )
    page = (ROOT / "templates/setup.html").read_text(encoding="utf-8")
    fields = re.findall(r'<input[^>]*name="email"[^>]*>', page)
    assert len(fields) == 1
    assert f'maxlength="{limit}"' in fields[0]
    assert limit == 255
