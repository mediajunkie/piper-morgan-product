"""The card-state file (Arch 2026-11-15; CXO reads it at each promotion).

Layer: unit. The health route function with its inputs stubbed, the page's own script
under node. Not a browser and not the served app. Skipped without ``node``.
"""

import shutil
import socket
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import card_state_file as cards  # noqa: E402

# Skipped on a seat without node; in CI a missing node fails these (Arch 2026-11-17).
needs_node = pytest.mark.skipif(cards.node_missing_is_a_skip(), reason="node not on PATH")


@pytest.fixture(scope="module")
def text():
    return cards.build()


@needs_node
def test_the_tracked_file_is_what_the_code_draws_now(text):
    """A change to a card's words or controls shows as a diff on the tracked file, in the
    commit that makes it. If this fails: ``venv/bin/python scripts/card_state_file.py``,
    read the diff, and commit the file with your change."""
    assert cards.DEFAULT_OUT.read_text(encoding="utf-8") == text


@needs_node
def test_every_state_has_a_section_and_every_card_is_drawn(text):
    for scenario in cards.scenarios():
        assert f"State key: `{scenario.key}`" in text
    assert "No card is drawn." not in text
    assert len({s.key for s in cards.scenarios()}) == len(cards.scenarios())


def _section(text, key):
    start = text.index(f"State key: `{key}`")
    end = text.find("\n## ", start)
    return text[start:] if end == -1 else text[start:end]


@needs_node
@pytest.mark.parametrize(
    "key,label,style",
    (
        ("github-app-none", "Install the GitHub app", "connect-btn"),
        ("github-app-some", "Manage repositories", "configure-btn"),
        ("github-app-unknown", "Repositories", "configure-btn"),
    ),
)
def test_the_github_link_carries_the_label_the_page_ends_with(text, key, label, style):
    """The 2375 defect: the link was in a branch that never drew GitHub's card. Here the
    drawn card holds it, with the label set after the install-state answer."""
    row = f"| link | {label} | {style} | `/settings/integrations/github#repositories` |"
    assert row in _section(text, key)


@needs_node
def test_a_card_outside_the_beta_list_offers_no_connect(text):
    section = _section(text, "not-offered")
    assert "| link | Connect |" not in section and "Not in this beta" in section
    assert "| link | Connect |" in _section(text, "not-connected")


@needs_node
def test_the_file_is_the_same_on_a_second_run(text):
    assert cards.build() == text


@pytest.mark.parametrize(
    "node,ci,skip",
    (
        (None, "", True),
        (None, "true", False),
        ("/usr/bin/node", "", False),
        ("/usr/bin/node", "true", False),
    ),
)
def test_a_missing_node_is_a_skip_on_a_seat_and_never_in_ci(monkeypatch, node, ci, skip):
    monkeypatch.setattr(shutil, "which", lambda name: node)
    monkeypatch.setenv("CI", ci)
    assert cards.node_missing_is_a_skip() is skip


def test_without_node_the_build_stops_rather_than_writing_anything(monkeypatch):
    """What CI sees if its image loses node: a failure with a plain reason."""
    monkeypatch.setattr(shutil, "which", lambda name: None)
    with pytest.raises(cards.Stopped, match="node is not on PATH"):
        cards.build()


def test_a_state_that_reaches_for_the_network_stops_the_run(monkeypatch):
    """The route turns a failure into a "couldn't check" card, so an unstubbed input
    would draw wrong words quietly. The run stops instead."""
    user_id = cards._setup()
    from web.api.routes import integrations as routes

    def reaches_out(integrations):
        socket.getaddrinfo("example.invalid", 443)

    monkeypatch.setattr(routes, "summarize_integrations", reaches_out)
    with pytest.raises(cards.Stopped):
        cards.health_payload(user_id, cards.scenarios()[0])


def test_reading_a_card_lists_lines_and_controls_and_marks_an_error_line():
    listing = (
        '<div class="integration-card" id="card-a"><h3>Alpha</h3>'
        '<span class="status-message error" id="status-a">It broke</span>'
        '<button class="action-btn test-btn" onclick="testConnection(\'a\')" disabled>Test</button>'
        '<a href="/x" class="action-btn connect-btn">Connect</a></div>'
        '<div class="integration-card" id="card-b"><h3>Beta</h3></div>'
    )
    card = cards.read_card({"list": listing, "link": None}, "a")
    assert card["lines"] == ["Alpha", "It broke [error style]"]
    assert [(c["kind"], c["label"], c["goes"], c["disabled"]) for c in card["controls"]] == [
        ("button", "Test", "testConnection()", "yes"),
        ("link", "Connect", "/x", ""),
    ]
    assert cards.read_card({"list": listing, "link": None}, "b")["lines"] == ["Beta"]
    assert cards.read_card({"list": listing, "link": None}, "c") is None


def test_building_the_file_in_process_leaves_the_store_variable_alone(monkeypatch):
    """The script chooses the database store for its own process in main(). Called from a
    test, _setup() must not write it into os.environ, where it would stay for every
    later test in the run (found 2026-11-17)."""
    import os

    monkeypatch.delenv("PIPER_CREDENTIAL_STORE", raising=False)
    cards._setup()
    assert "PIPER_CREDENTIAL_STORE" not in os.environ
    source = (ROOT / "scripts" / "card_state_file.py").read_text(encoding="utf-8")
    setup_body = source[source.index("def _setup()") : source.index("def _github_outcome")]
    assert "PIPER_CREDENTIAL_STORE" not in setup_body


@needs_node
def test_every_test_click_state_has_a_section(text):
    keys = [c.key for c in cards.clicks()]
    assert len(set(keys)) == len(keys)
    assert not set(keys) & {s.key for s in cards.scenarios()}
    for key in keys:
        assert f"State key: `{key}`" in text


@needs_node
def test_no_click_row_is_the_pages_own_error_branch(text):
    """The page's ``catch`` shows "Test Error" / "Failed to test github" when its own script
    throws. In this file that means the harness, not the app, broke (it did once, on a
    lookup a browser answers with null); a row like that is never a reading of the page."""
    clicked = text[text.index("# After pressing Test") :]
    assert "**Test Error**" not in clicked and "Failed to test" not in clicked


@needs_node
def test_a_passing_test_shows_the_routes_own_line_in_the_toast_and_at_the_click(text):
    row = _section(text, "test-own-token")
    assert (
        "- Toast (success): **Test Passed**. GitHub is working, using your personal token." in row
    )
    assert "- At the click, the card's line: GitHub is working, using your personal token." in row


# CXO 2026-11-18: any fact the click names that still holds is on the redrawn card, in
# the same words, and one fact has one name.
FACTS_ON_THE_CARD = {
    "test-own-token": "Connected via your personal token.",
    "test-token-serving-stale": "GitHub no longer accepts your connection, so I'm not using it right now.",
    "test-needs-reconnecting": "GitHub no longer accepts your connection.",
    "test-not-connected": "Not connected",
    "test-lookup-failed": "Couldn't check this just now. Press Test to try again.",
    "test-github-did-not-answer": "Couldn't check this just now. Press Test to try again.",
}


@needs_node
@pytest.mark.parametrize("key,fact", sorted(FACTS_ON_THE_CARD.items()))
def test_the_fact_the_click_names_is_on_the_redrawn_card(text, key, fact):
    row = _section(text, key)
    after = row[row.index("- The card after the page redraws it:") :]
    assert fact in after


@needs_node
def test_re_authorizing_is_retired_from_the_github_test_rows(text):
    clicked = text[text.index("# After pressing Test") :]
    rows = "\n".join(ln for ln in clicked.splitlines() if not ln.startswith("## "))
    assert "re-authoriz" not in rows


# --- the Notion, Slack and Calendar Tests, and Test All (Lead 2026-11-18) ----------------


@needs_node
def test_every_connector_test_and_test_all_state_has_a_section(text):
    keys = [c.key for c in cards.connector_clicks()] + [c.key for c in cards.test_all_clicks()]
    others = {s.key for s in cards.scenarios()} | {c.key for c in cards.clicks()}
    assert len(set(keys)) == len(keys) and not set(keys) & others
    for key in keys:
        assert f"State key: `{key}`" in text
    for card, outcomes in cards._CONNECTOR_OUTCOMES.items():
        assert len([c for c in cards.connector_clicks() if c.show == (card,)]) == len(outcomes)


@needs_node
def test_a_connector_test_reaches_the_apps_own_check(text):
    """The words come from the app's ``_test_*`` checks and routes, not from this script:
    a refused Slack token shows the route's own constant, at the click and on the card."""
    from web.api.routes.integrations import CHECK_FAILED_MESSAGE, SLACK_TOKEN_REFUSED_LINE

    row = _section(text, "test-slack-refused")
    assert f"- At the click, the card's line: {SLACK_TOKEN_REFUSED_LINE} [error style]" in row
    assert f"  - {SLACK_TOKEN_REFUSED_LINE} Checked just now. [error style]" in row
    for key in ("test-notion-no-answer", "test-calendar-store-failed", "test-slack-raised"):
        assert f"- At the click, the card's line: {CHECK_FAILED_MESSAGE}" in _section(text, key)


@needs_node
def test_test_all_shows_one_toast_and_every_cards_line(text):
    row = _section(text, "test-all-pass")
    assert "- Toast (success): **All Tests Passed**. 4 of 4 connections successful" in row
    for card in cards.CARDS:
        assert f"### {card}" in row
    # CXO 2026-11-18: a card with nothing connected wasn't tested, so it isn't counted.
    mixed = _section(text, "test-all-mixed")
    assert "**Some Tests Failed**. 1 of 3 connections successful, 1 not connected" in mixed
    nothing = _section(text, "test-all-nothing")
    assert "- Toast (info): **Nothing to test yet**. Connect an integration first." in nothing
    assert "Some Tests Failed" not in nothing


# CXO 2026-11-18: no code word on screen, at the click or on a card. The list is the codes
# the Test checks and the registry can produce, not a regex of words.
CODES = sorted(
    {"not_configured", "token_invalid", "api_key_invalid", "connect_required", "check_failed"}
    | {outcome for outcomes in cards._CONNECTOR_OUTCOMES.values() for outcome, _ in outcomes}
    - {"ok", "raised", "no_answer", "refused", "store_failed", "not_connected", "revoked", "error"}
)


@needs_node
def test_no_code_word_reaches_a_click_or_a_card(text):
    pressed = text[text.index("# After pressing Test: the Notion") :]
    lines = [ln for ln in pressed.splitlines() if ln.startswith(("- ", "  - "))]
    for line in lines:
        assert "Error:" not in line, line
        for code in CODES:
            assert code not in line, (code, line)


# CXO 2026-11-18: the fact the click names is on the redrawn card, in the same words.
CONNECTOR_FACTS = {
    "test-notion-refused": "Notion didn't accept your key.",
    "test-calendar-revoked": "Google Calendar no longer accepts your connection.",
    "test-calendar-insufficient-scope": "the connection doesn't include calendar access.",
    "test-calendar-api-not-enabled": "the Calendar service isn't switched on for this app yet.",
    "test-calendar-error": "Google refused the calendar read, and I couldn't tell why.",
    "test-calendar-not-found": "Google couldn't find your calendar. Reconnect and try again.",
    "test-notion-not-connected": "Not connected",
    "test-slack-not-connected": "Not connected",
    "test-calendar-not-connected": "Not connected",
}


@needs_node
@pytest.mark.parametrize("key,fact", sorted(CONNECTOR_FACTS.items()))
def test_a_connector_click_and_its_redrawn_card_share_the_fact(text, key, fact):
    start = text.index(f"State key: `{key}`")
    ends = [text.find(h, start) for h in ("\n### ", "\n## ", "\n# ")]
    row = text[start : min([e for e in ends if e != -1] or [len(text)])]
    at, after = row.split("- The card after the page redraws it:")
    assert fact in after
    if fact != "Not connected":
        assert "- At the click, the card's line: " in at and fact in at


def test_the_connector_stand_in_refuses_any_other_address():
    """A Test that reached past the stood-in replies would stop, not draw a reply."""
    session = cards._connector_session({"notion": "ok"})()
    with pytest.raises(OSError):
        session.get("https://example.invalid/")
    with pytest.raises(OSError):
        session.post("https://api.other.example/v1/users/me")


# --- the confirm dialogs before a disconnect (Lead 2026-11-18, CXO's next surface) ------


@needs_node
def test_every_connected_card_and_disconnect_all_show_a_dialog_and_cancel_sends_nothing(text):
    section = text[text.index("# Before a disconnect") :]
    connected = _section(text, "dialogs-connected")
    for card in cards.CARDS:
        assert f"### Disconnect on {card} (`" in connected
    assert connected.count("- Title: **") == len(cards.CARDS) + 1  # each card, then All
    assert "No dialog." not in connected
    assert section.count("Sent to a disconnect route after Cancel: nothing") == len(
        cards.dialog_pages()
    )


@needs_node
def test_disconnect_all_lists_the_cards_by_their_drawn_names(text):
    row = _section(text, "dialogs-connected")
    for name in ("Notion", "Slack", "GitHub", "Google Calendar"):
        assert f"  > • {name}" in row


@needs_node
def test_every_confirmed_disconnect_has_a_section_and_no_row_is_a_harness_error(text):
    section = text[text.index("# After a confirmed disconnect") :]
    for key, *_ in cards.disconnect_clicks():
        assert f"State key: `{key}`" in section
    # A page script that can't find a shared helper throws into the toast; that is the
    # harness, not the app (parseApiDetail was missing once, 2026-11-18). Every press ends
    # in a toast, or in Disconnect All's dialog (CXO 2026-11-18 D).
    assert "is not defined" not in section
    assert section.count("- No toast.") == section.count("- No toast.\n- A dialog:")
    # Arch 2026-11-18: the raised clear's text reaches no toast, dialog or card.
    assert cards.SAMPLE_ERROR not in section


@needs_node
def test_a_cleared_disconnect_redraws_the_card_not_connected(text):
    """CXO 2026-11-18 C: a cleared card's toast is its words from the one map, in warning
    style where something stays valid at the provider (the GitHub token, Notion)."""
    from services.connectors.disconnect_words import disconnect_words

    legs = {"github": "token"}
    for card in cards.CARDS:
        row = _section(text, f"disconnect-{card}-cleared")
        words = disconnect_words(card, legs.get(card))
        kind = "warning" if words.stays else "success"
        assert f"- Toast ({kind}): **Disconnected**. {words.cleared}" in row
        assert row.rstrip().endswith("- Not connected")
    for leg in ("app", "oauth", "unknown"):
        row = _section(text, f"disconnect-github-{leg}-cleared")
        words = disconnect_words("github", leg)
        kind = "warning" if words.stays else "success"
        assert f"- Toast ({kind}): **Disconnected**. {words.cleared}" in row


@needs_node
def test_a_failed_revoke_is_a_warning_and_names_a_place_a_person_can_find(text):
    for card in ("slack", "calendar", "github"):
        row = _section(text, f"disconnect-{card}-revoke-failed")
        assert "- Toast (warning): **Disconnected**." in row
    assert "remove Piper in your Google account's settings." in _section(
        text, "disconnect-calendar-revoke-failed"
    )


@needs_node
def test_an_incomplete_disconnect_holds_its_line_on_the_still_connected_card(text):
    from web.api.routes.settings_integrations import DISCONNECT_INCOMPLETE_LINE

    for card, name in (("slack", "Slack"), ("calendar", "Google Calendar")):
        for outcome in ("incomplete", "raised"):
            row = _section(text, f"disconnect-{card}-{outcome}")
            after = row.split(f"- {card} after the redraw:")[1]
            assert "  - Connected\n" in after
            assert DISCONNECT_INCOMPLETE_LINE.format(service=name) in after
            assert "Not checked yet" not in after


@needs_node
def test_disconnect_all_keeps_each_cards_own_outcome_in_a_dialog(text):
    """CXO 2026-11-18 D: anything but "all cleared, nothing stays" is a dialog with OK, the
    count as its heading, one line per card with something to say, then the closing line."""
    from services.connectors.disconnect_words import (
        all_incomplete_line,
        all_revoke_failed_line,
    )

    row = _section(text, "disconnect-all-mixed")
    assert "- No toast.\n- A dialog:" in row
    assert "  - Title: **3 of 4 disconnected.**" in row
    assert f"    > {all_revoke_failed_line('Slack')}" in row
    assert f"    > {all_incomplete_line('Google Calendar')}" in row
    assert "    > GitHub and Notion also need you to remove Piper in their own settings." in row
    assert "  - Buttons: OK (only)" in row
    quiet = _section(text, "disconnect-all-cleared-nothing-stays")
    assert "- Toast (success): **All Disconnected**. 3 of 3 disconnected." in quiet
    assert "A dialog" not in quiet


@needs_node
def test_nothing_connected_keeps_its_title_case_title(text):
    row = _section(text, "dialogs-nothing")
    assert "- Toast (info): **Nothing to Do**. Nothing is connected." in row


def test_the_disconnect_stand_in_replaces_only_the_clearing_call():
    """The route's own words: the stub is the one call under it, nothing above."""
    user_id = cards._setup()
    replies = cards.run_disconnect(user_id, {"slack": "incomplete"})
    from web.api.routes.settings_integrations import DISCONNECT_INCOMPLETE_LINE

    assert replies["slack"]["status"] == 503
    assert replies["slack"]["body"]["detail"] == DISCONNECT_INCOMPLETE_LINE.format(service="Slack")


@needs_node
def test_each_dialog_names_its_card_as_the_card_draws_it(text):
    """CXO 2026-11-18: the dialog's name is the card's own drawn name, not one built from
    the id; and no dialog says "integration" except the Disconnect All title."""
    from services.connectors.disconnect_words import disconnect_words

    pages = {
        "dialogs-connected": "token",
        "dialogs-github-app": "app",
        "dialogs-github-classic": "oauth",
        "dialogs-github-unknown": "unknown",
    }
    for key, leg in pages.items():
        row = _section(text, key)
        for block in row.split("### Disconnect on ")[1:-1]:
            card = block.split(" ", 1)[0]
            drawn = (
                _section(text, "connected-untested").split(f"### {card}\n", 1)[1].split("\n- ")[2]
            )
            assert f"- Title: **Disconnect {drawn}?**" in block, (card, drawn)
            # CXO 2026-11-18 B: the message is the card's own sentence from the one map.
            dialog = disconnect_words(card, leg if card == "github" else None).dialog
            assert f"  > {dialog}" in block, (key, card)
    dialogs = text[text.index("# Before a disconnect") : text.index("# After a confirmed")]
    lines = [ln for ln in dialogs.splitlines() if ln.startswith(("- Title", "  >"))]
    # "integration" only in the All title and in Notion's own sentence (CXO's words: a
    # Notion key lives in a Notion "integration").
    assert {ln for ln in lines if "integration" in ln and "Notion" not in ln} == {
        "- Title: **Disconnect all integrations?**"
    }


@needs_node
@pytest.mark.parametrize(
    "key,closing",
    [
        ("dialogs-connected", "GitHub and Notion also need you to remove Piper in their own settings."),
        ("dialogs-github-app", "GitHub and Notion also need you to remove Piper in their own settings."),
        ("dialogs-github-classic", "Notion also needs you to remove Piper in its settings."),
        (
            "dialogs-github-unknown",
            "Notion also needs you to remove Piper in its settings, and GitHub may too if you "
            "connected it with the app or a token.",
        ),
        ("dialogs-github-classic-no-notion", None),
        (
            "dialogs-github-unknown-no-notion",
            "GitHub may need you to remove Piper in its settings if you connected it with the "
            "app or a token.",
        ),
    ],
)  # fmt: skip
def test_disconnect_all_names_who_else_needs_piper_removed(text, key, closing):
    all_block = _section(text, key).split("### Disconnect All", 1)[1]
    if closing is None:
        assert "remove Piper" not in all_block
    else:
        assert f"  > {closing}\n  >\n  > You can connect them again anytime." in all_block
