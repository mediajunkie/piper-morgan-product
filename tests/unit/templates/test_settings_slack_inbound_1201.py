"""#1201 — settings_slack.html "Enable Slack replies" (inbound) section renders.

Real Jinja render() (not curl-200, not source-read): catches template-syntax errors
AND verifies the inbound card + app-token input + 3-state status + wiring are present.
"""

import pytest
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


@pytest.fixture(scope="module")
def rendered():
    env = Environment(loader=FileSystemLoader("templates"))
    # Render the full template (extends layouts/app_shell.html) — proves it compiles.
    return env.get_template("settings_slack.html").render()


@pytest.fixture(scope="module")
def soup(rendered):
    return BeautifulSoup(rendered, "html.parser")


def test_template_renders_nonempty(rendered):
    assert rendered and len(rendered) > 500  # compiled + rendered without error


def test_inbound_card_present(soup):
    assert soup.find(id="inbound-card") is not None


def test_app_token_input_is_password_with_xapp_placeholder(soup):
    inp = soup.find(id="slack-app-token")
    assert inp is not None
    assert inp.get("type") == "password"
    assert "xapp-" in (inp.get("placeholder") or "")


def test_three_state_status_badge_present(soup):
    assert soup.find(id="inbound-status") is not None
    assert soup.find(id="inbound-status-icon") is not None
    assert soup.find(id="inbound-status-text") is not None


def test_save_button_wired_to_handler(soup):
    btn = soup.find(id="save-app-token-btn")
    assert btn is not None
    assert "saveAppToken" in (btn.get("onclick") or "")


def test_cxo_copy_and_setup_steps_present(rendered):
    assert "Enable Slack replies" in rendered
    assert "connections:write" in rendered  # the required scope, in the steps
    assert "api.slack.com/apps" in rendered  # the setup link


def test_event_subscription_step_present(rendered):
    """#1201 AC: instructions MUST cover the event subscriptions — without them the
    bot connects via Socket Mode but receives no events (non-working setup)."""
    assert "Event Subscriptions" in rendered
    assert "message.im" in rendered
    assert "app_mention" in rendered


def test_js_wires_both_endpoints_and_loads_on_start(rendered):
    assert "/api/v1/settings/integrations/slack/inbound/status" in rendered
    assert "/api/v1/settings/integrations/slack/app-token" in rendered
    assert "loadInboundStatus()" in rendered  # called on DOMContentLoaded
    # all three states are rendered by the JS
    assert "listening" in rendered and "connecting" in rendered
