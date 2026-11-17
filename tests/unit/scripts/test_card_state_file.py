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
