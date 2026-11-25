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
