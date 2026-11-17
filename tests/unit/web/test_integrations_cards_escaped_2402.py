"""#2402 (Arch 2026-11-17): no string the route sends reaches the Integrations page's
``innerHTML`` unescaped. A Test's stored error can quote a remote service's reply.

Layer: the page's own script under node, through ``scripts/card_state_file.py``, and
the template's source. Not a browser.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import card_state_file as cards  # noqa: E402

needs_node = pytest.mark.skipif(cards.node_missing_is_a_skip(), reason="node not on PATH")
PAGE = (ROOT / "templates" / "integrations.html").read_text(encoding="utf-8")
HOSTILE = "<img src=x onerror=alert(1)>\"'&"


def _scenario(key):
    (found,) = [s for s in cards.scenarios() if s.key == key]
    return found


@pytest.fixture(scope="module")
def user_id():
    return cards._setup()


# The ids are not the bare card names: tests/conftest.py skips a test whose keyword is
# "github" when no GitHub token is set.
@needs_node
@pytest.mark.parametrize("name", cards.CARDS, ids=[f"card-{n}" for n in cards.CARDS])
def test_a_stored_error_with_markup_is_drawn_as_text(user_id, name):
    scenario = _scenario("failed-markup")
    drawn = cards.draw(cards.health_payload(user_id, scenario), scenario)
    card = cards.read_card(drawn, name)
    assert card["lines"][-1] == f"{cards.MARKUP_ERROR}. Checked just now. [error style]"
    assert "<b>" not in drawn["list"] and "&lt;b&gt;markup&lt;/b&gt; &amp;" in drawn["list"]


@needs_node
def test_the_github_error_line_is_escaped_too(user_id):
    scenario = _scenario("github-app-failed-markup")
    drawn = cards.draw(cards.health_payload(user_id, scenario), scenario)
    card = cards.read_card(drawn, "github")
    assert card["lines"][-2:] == [
        "Connected as octo-example.",
        f"{cards.MARKUP_ERROR}. Checked just now. [error style]",
    ]
    assert [c["label"] for c in card["controls"]] == ["Test", "Disconnect", "Manage repositories"]


@needs_node
@pytest.mark.parametrize(
    "field",
    (
        "display_name",
        "status_message",
        "status_detail",
        "fix_suggestion",
        "error_line",
        "status_icon",
        "configure_url",
        "status",
    ),
)
def test_every_string_field_of_a_card_is_escaped(user_id, field):
    """A payload the route would not send, to cover each field the template draws."""
    scenario = _scenario("connected-untested")
    payload = cards.health_payload(user_id, scenario)
    (slack,) = [c for c in payload["integrations"] if c["name"] == "slack"]
    slack[field] = HOSTILE
    drawn = cards.draw(payload, scenario)
    assert "<img" not in drawn["list"], field
    assert "&lt;img src=x onerror=alert(1)&gt;" in drawn["list"], field


def test_the_template_escapes_the_card_before_drawing_any_of_it():
    start = PAGE.index("function renderIntegrations(integrations) {")
    body = PAGE[start : PAGE.index("function formatCheckedAt(", start)]
    assert "integrations.map(card => {" in body
    lines = body[body.index("integrations.map(card => {") :].split("\n")[1:]
    first = next(ln.strip() for ln in lines if ln.strip() and not ln.strip().startswith("//"))
    assert first == "const integration = escapedCard(card);"
    rest = body.split("escapedCard(card);", 1)[1]
    assert "${card." not in body
    # The one later use of the raw card is the check on its name.
    assert rest.count("card.") == 1 and "test(String(card.name))) return '';" in rest


@needs_node
@pytest.mark.parametrize("name", ("x');alert(1);('", "<b>", "Slack", ""))
def test_a_card_whose_name_is_not_a_registry_key_is_not_drawn(user_id, name):
    """The name goes inside click handlers, where escaping text is not enough."""
    scenario = _scenario("connected-untested")
    payload = cards.health_payload(user_id, scenario)
    (slack,) = [c for c in payload["integrations"] if c["name"] == "slack"]
    slack["name"] = name
    drawn = cards.draw(payload, scenario)
    assert "alert" not in drawn["list"] and "<b>" not in drawn["list"]
    assert drawn["list"].count('class="integration-card') == 3


def test_the_load_failure_line_is_escaped():
    start = PAGE.index("function showError(message) {")
    assert "${escapeHtml(message)}" in PAGE[start : start + 400]
    assert "${message}" not in PAGE[start : start + 400]
