"""#1466 — settings_slack.html "Link your Slack account" section renders.

Real Jinja render() per the house rule (not curl-200, not source-read):
catches template-syntax errors AND verifies the link section, the mint
button, the deep-link pre-mint mode (CXO §2), and unlink wiring are present.
"""

import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


@pytest.fixture(scope="module")
def rendered():
    env = Environment(loader=FileSystemLoader("templates"))
    return env.get_template("settings_slack.html").render()


@pytest.fixture(scope="module")
def soup(rendered):
    return BeautifulSoup(rendered, "html.parser")


def test_template_renders_nonempty(rendered):
    assert rendered and len(rendered) > 500


def test_link_slack_section_present_with_anchor_id(soup):
    """The deep link targets #link-slack — the section id IS the contract."""
    assert soup.find(id="link-slack") is not None


def test_mint_button_wired_to_handler(soup):
    btn = soup.find(id="mint-link-code-btn")
    assert btn is not None
    assert "mintSlackLinkCode" in (btn.get("onclick") or "")


def test_code_display_panel_present(soup):
    assert soup.find(id="link-slack-code") is not None
    assert soup.find(id="link-slack-expiry") is not None


def test_deep_link_params_premint_mode_present(rendered):
    """CXO §2: arriving via the decline's deep link (opaque slack params) must
    render 'Link this Slack account' with the code pre-minted."""
    assert "slack_user_id" in rendered  # param read in the page script
    assert "slack_team_id" in rendered
    assert "Link this Slack account" in rendered


def test_slash_link_instruction_present(rendered):
    """The handshake's Slack-side half is `/link <code>` — the page must say so."""
    assert "/link" in rendered


def test_unlink_wiring_present(rendered):
    assert "unlinkSlack" in rendered
    assert "linked-accounts-list" in rendered
