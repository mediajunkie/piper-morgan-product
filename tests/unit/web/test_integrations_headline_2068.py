"""#2068: the Integrations headline counts only connected integrations (CXO's ruling).

Layers: (1) ``summarize_integrations`` rule; (2) the served health JSON
(``_check_integration_health`` stubbed per card) through the app's TestClient;
(3) that JSON run through the page's OWN ``renderOverallStatus`` under Node.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.api.routes.integrations import IntegrationStatus, summarize_integrations
from web.app import app

REPO = Path(__file__).resolve().parents[3]
HEALTH = "/api/v1/integrations/health"
NAMES = ["notion", "slack", "github", "calendar"]


def _card(name, status):
    return IntegrationStatus(
        name=name, display_name=name.title(), status=status, status_message=status
    )


def _cards(**states):
    return [_card(n, states.get(n, "not_configured")) for n in NAMES]


CASES = {
    "none": (_cards(), "Nothing connected yet", "none"),
    "github_degraded": (
        _cards(github="degraded"),
        "Needs attention",
        "degraded",
    ),
    "all_healthy": (_cards(github="healthy", calendar="healthy"), "All Systems Healthy", "healthy"),
    "two_failing": (_cards(github="failed", calendar="failed"), "Multiple Issues", "unhealthy"),
    "one_failing": (_cards(github="failed", calendar="healthy"), "Needs attention", "degraded"),
    "two_amber_not_multiple": (
        _cards(github="degraded", calendar="degraded"),
        "Needs attention",
        "degraded",
    ),
}


@pytest.mark.parametrize("case", CASES)
def test_rule(case):
    cards, headline, overall = CASES[case]
    got_overall, got_headline, summary, working, connected = summarize_integrations(cards)
    assert (got_overall, got_headline) == (overall, headline)
    assert "0 of 4" not in summary


def test_count_line_uses_connected_only():
    _, _, summary, working, connected = summarize_integrations(_cards(github="degraded"))
    assert summary == "0 of 1 checked integrations working"
    _, _, summary, _, _ = summarize_integrations(_cards(github="healthy", calendar="degraded"))
    assert summary == "1 of 2 checked integrations working"


def test_untested_connected_is_not_an_alarm():
    overall, headline, *_ = summarize_integrations(_cards(github="connected"))
    assert headline not in ("Needs attention", "Multiple Issues")
    assert overall == "unknown"


@pytest.fixture(scope="module")
def client():
    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(REPO / "templates"))
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2068@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    return c


def _health(client, cards):
    by_name = {c.name: c for c in cards}

    async def fake(integration_id, metadata, user_id=None):
        return by_name[integration_id]

    with patch("web.api.routes.integrations._check_integration_health", new=fake):
        r = client.get(HEALTH)
    assert r.status_code == 200
    return r.json()


def _headline_text(client, data):
    body = client.get("/settings/integrations").text
    start = body.index("function renderOverallStatus(data) {")
    end = body.index("function renderIntegrations(integrations) {")
    consts = body[
        body.index("// Status icons for overall health") : body.index("// Load health status")
    ]
    script = (
        "const els = {};\n"
        "const document = { getElementById(id) { return els[id] = els[id] || {}; } };\n"
        + consts
        + body[start:end]
        + "\nrenderOverallStatus(JSON.parse(process.argv[1]));\n"
        "process.stdout.write(els['overall-title'].textContent + '|' + "
        "els['overall-subtitle'].textContent);\n"
    )
    res = subprocess.run(
        ["node", "-e", script, json.dumps(data)], capture_output=True, text=True, timeout=30
    )
    assert res.returncode == 0, res.stderr
    return res.stdout


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


@needs_node
@pytest.mark.parametrize("case", CASES)
def test_page_renders_the_served_headline(client, case):
    cards, headline, _ = CASES[case]
    data = _health(client, cards)
    assert data["headline"] == headline
    title, subtitle = _headline_text(client, data).split("|")
    assert title == headline
    assert "0 of 4" not in subtitle
    if case == "none":
        assert subtitle == ""
    if case == "github_degraded":
        assert subtitle == "0 of 1 checked integrations working"
