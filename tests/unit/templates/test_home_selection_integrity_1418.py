"""#1418 — conversation-picker selection integrity: real-render contract tests.

The bug: clicking a conversation flashed it, then the chat landed back on the
most recent one — a late implicit default (racing init auto-select) stomped the
user's explicit selection, and out-of-order turn fetches could render the loser
last. The fix lives in home.html's inline script: an explicit-selection latch +
a last-call-wins sequence token in switchConversation.

Browser-verified 2026-07-17 (localhost, seeded two-conversation account):
URL-param render, late-default BLOCKED, explicit switches both ways, two-switch
race (last wins), rail-click navigation. These render()-level tests pin the
guard's presence in the template so a refactor can't silently drop it
(per the UI-fix template.render() discipline — curl-200 proves nothing here).
"""

from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).resolve().parents[3] / "templates"


def _home_html() -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    return env.get_template("home.html").render(
        trust_stage=1, show_radar=True, user_name="tester"
    )


def test_selection_latch_and_sequence_token_present():
    html = _home_html()
    # The latch state + the guard inside switchConversation
    assert "explicitSelectionMade" in html
    assert "switchSeq" in html
    assert "implicit switch ignored" in html  # the latch's guard branch
    assert "stale turns response discarded" in html  # last-call-wins branch


def test_init_autoselect_marks_default_as_implicit():
    html = _home_html()
    # initSidebar must pass explicit only when the user (URL/localStorage) chose;
    # the most-recent fallback rides explicit: false via !!conversationId.
    assert "switchConversation(targetConversationId, { explicit: !!conversationId })" in html


def test_explicit_paths_do_not_opt_out():
    """User-click paths (sidebar onclick, history-select) must stay explicit —
    only the init default derives its explicitness from whether the user chose."""
    html = _home_html()
    assert html.count("{ explicit: !!conversationId }") == 1  # exactly the init call
    assert html.count("explicit: false") == 0  # no caller hardcodes implicit
