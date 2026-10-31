"""#2237 (page half): connectors outside ``BETA_OFFERED_CONNECTORS`` render greyed as
"coming" on the Integrations page and the setup wizard, with no active connect control.

The page builds its cards client-side, so the render test extracts the page's own
``renderIntegrations`` from the served HTML and runs it under Node (as the 2031 test
does). Skipped when ``node`` is not on PATH.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from services.integrations import integration_status_service as svc
from web.app import app

REPO = Path(__file__).resolve().parents[3]
PAGE = "/settings/integrations"
LABEL = "Not in this beta"
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")

HEALTH_NAMES = {"slack": "Slack", "notion": "Notion"}
HEALTH = [
    {
        "name": n,
        "display_name": d,
        "status": "not_configured",
        "can_test": False,
        "configure_url": f"/settings/integrations/{n}",
        "status_icon": "",
        "message": "Not configured",
    }
    for n, d in [
        ("github", "GitHub"),
        ("slack", "Slack"),
        ("calendar", "Google Calendar"),
        ("notion", "Notion"),
    ]
]


@pytest.fixture(scope="module")
def client():
    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(REPO / "templates"))
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2237p@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    return c


def _page(client) -> str:
    r = client.get(PAGE)
    assert r.status_code == 200
    return r.text


def _cards(body: str, health: list) -> dict[str, str]:
    consts = body[
        body.index("// Integration icons mapping") : body.index(
            "// Status icons for overall health"
        )
    ]
    offered = re.search(r"window.__OFFERED_CONNECTORS__ = .*?;\n", body).group(0)
    start = body.index("function renderIntegrations(integrations) {")
    end = body.index("async function testConnection(integrationName)")
    script = (
        "const window = {}; " + offered + "\n"
        "const out = {};\n"
        "const document = { getElementById(id) { return id === 'integrations-list' ? out : null; } };\n"
        + consts
        + body[start:end]
        + "\nrenderIntegrations(JSON.parse(process.argv[1]));\n"
        "process.stdout.write(out.innerHTML);\n"
    )
    res = subprocess.run(
        ["node", "-e", script, json.dumps(health)], capture_output=True, text=True, timeout=30
    )
    assert res.returncode == 0, res.stderr
    parts = re.split(r'(?=<div class="integration-card)', res.stdout)
    return {re.search(r'id="card-(\w+)"', p).group(1): p for p in parts if 'id="card-' in p}


@needs_node
def test_slack_and_notion_render_greyed_with_no_connect_control(client):
    cards = _cards(_page(client), HEALTH)
    assert set(cards) == {"github", "slack", "calendar", "notion"}
    for name in ("slack", "notion"):
        card = cards[name]
        assert "not-in-beta" in card and LABEL in card
        assert f"{HEALTH_NAMES[name]} isn't available in this beta yet." in card
        assert "oming soon" not in card
        for control in (
            "connect-btn",
            "Connect",
            "Reconnect",
            "Settings",
            "test-btn",
            "<a ",
            "<button",
            "<input",
        ):
            assert control not in card, (name, control)
        assert "disconnect-btn" not in card  # not connected: nothing to clear


@needs_node
def test_github_and_calendar_keep_their_controls(client):
    cards = _cards(_page(client), HEALTH)
    for name in ("github", "calendar"):
        assert "not-in-beta" not in cards[name]
        assert LABEL not in cards[name]
        assert "connect-btn" in cards[name]
        assert "test-btn" in cards[name]


@needs_node
def test_connected_but_not_offered_still_shows_disconnect(client):
    health = [dict(h, status="healthy") if h["name"] == "slack" else h for h in HEALTH]
    slack = _cards(_page(client), health)["slack"]
    assert "disconnect-btn-slack" in slack and LABEL in slack
    for control in (" connect-btn", "Reconnect", "Settings", "configure-btn"):
        assert control not in slack


@needs_node
def test_the_greyed_set_follows_the_constant(client, monkeypatch):
    monkeypatch.setattr(svc, "BETA_OFFERED_CONNECTORS", {"github": "GitHub", "notion": "Notion"})
    body = _page(client)
    assert 'window.__OFFERED_CONNECTORS__ = ["github", "notion"];' in body
    cards = _cards(body, HEALTH)
    assert "not-in-beta" not in cards["notion"]
    for name in ("calendar", "slack"):
        assert "not-in-beta" in cards[name]


def test_the_page_lists_exactly_the_constant(client):
    body = _page(client)
    assert (
        f"window.__OFFERED_CONNECTORS__ = {json.dumps(list(svc.BETA_OFFERED_CONNECTORS))};" in body
    )


def _wizard(client_or_none, offered) -> str:
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader(str(REPO / "templates")))
    return env.get_template("setup.html").render(
        asset_v="t", hosted=False, offered_connectors=offered
    )


def test_wizard_no_longer_offers_notion_or_slack():
    html = _wizard(None, list(svc.BETA_OFFERED_CONNECTORS))
    for gone in (
        'id="notion-key"',
        'data-provider="notion"',
        "Notion API Key",
        'id="connect-slack-btn"',
        'id="save-slack-credentials-btn"',
        "Slack Integration",
        "oming soon",
    ):
        assert gone not in html, gone
    assert 'id="connect-calendar-btn"' in html  # Calendar unchanged
    assert 'id="validate-llm-btn"' in html  # the step still has its skip/continue path


def test_wizard_follows_the_offered_set():
    html = _wizard(None, ["github", "calendar", "notion", "slack"])
    assert 'id="notion-key"' in html and 'id="connect-slack-btn"' in html


def test_wizard_route_passes_the_constant(client):
    r = client.get("/setup")
    assert r.status_code == 200
    assert 'id="notion-key"' not in r.text
