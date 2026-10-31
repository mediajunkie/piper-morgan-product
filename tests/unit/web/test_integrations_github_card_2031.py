"""#2031: the Integrations page renders the GitHub card's four resolver states in CXO's
words, with the right Test / Reconnect / Connect affordance, and no "MCP connector".

Layers:
1. the served page (``/settings/integrations`` through the app's TestClient, template
   render): the card renderer carries the new fields and no internal vocabulary;
2. the served JSON (``GET /api/v1/integrations/health`` through the same TestClient,
   the resolver stubbed per state);
3. that JSON run through the page's OWN ``renderIntegrations`` (extracted from the served
   HTML) under Node with a minimal DOM stub, so the assertions read the card markup the
   browser would insert. Skipped when ``node`` is not on PATH. Not a browser: no CSS,
   no click; the served judgement (CXO/PA) covers that.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubReposResult
from web.app import app

REPO = Path(__file__).resolve().parents[3]
PAGE = "/settings/integrations"
HEALTH = "/api/v1/integrations/health"
_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"

STATES = {
    "oauth": GitHubCredential(owner_id="u", mcp_server_ref="github", token=None, leg="oauth"),
    "pat_stale": GitHubCredential(
        owner_id="u",
        mcp_server_ref="github",
        token="tok",
        leg="pat",
        stale_oauth_reason=DegradationReason.STALE_TOKEN,
    ),
    "stale_nothing": DegradationResponse(
        reason=DegradationReason.STALE_TOKEN, user_message="needs re-authorizing"
    ),
    "nothing": DegradationResponse(
        reason=DegradationReason.CONNECT_REQUIRED, user_message="Connect GitHub to continue."
    ),
}


@pytest.fixture(scope="module")
def client():
    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(REPO / "templates"))
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2031@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    return c


@pytest.fixture(scope="module")
def body(client):
    r = client.get(PAGE)
    assert r.status_code == 200, f"{PAGE} -> {r.status_code}"
    return r.text


def _github_json(client, state: str) -> dict:
    probe = GitHubReposResult(repositories=[{"full_name": "o/r"}])
    with (
        patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=STATES[state])),
        patch(f"{_ADAPTER}.search_user_repositories", new=AsyncMock(return_value=probe)),
    ):
        r = client.get(HEALTH)
    assert r.status_code == 200, f"{HEALTH} -> {r.status_code}"
    (github,) = [i for i in r.json()["integrations"] if i["name"] == "github"]
    return github


def _renderer(body: str) -> str:
    # Anchored on the page's own comment: the command palette partial has an ICONS too.
    consts = body[
        body.index("// Integration icons mapping") : body.index(
            "// Status icons for overall health"
        )
    ]
    start = body.index("function renderIntegrations(integrations) {")
    end = body.index("async function testConnection(integrationName)")
    return consts + body[start:end]


def _render(body: str, integration: dict) -> str:
    script = (
        "const window = { __OFFERED_CONNECTORS__: ['github', 'calendar'] };\n"
        "const out = {};\n"
        "const document = { getElementById(id) {\n"
        "  if (id === 'integrations-list') return out;\n"
        "  return null; } };\n"
        + _renderer(body)
        + "\nrenderIntegrations(JSON.parse(process.argv[1]));\n"
        "process.stdout.write(out.innerHTML);\n"
    )
    res = subprocess.run(
        ["node", "-e", script, json.dumps([integration])],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert res.returncode == 0, res.stderr
    return " ".join(res.stdout.split())


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


# ── Layer 1: the served page ──────────────────────────────────────────────────


def test_page_renders_cards_from_the_health_json(body):
    assert "fetch('/api/v1/integrations/health')" in body
    renderer = _renderer(body)
    assert "integration.action === 'reconnect'" in renderer
    assert "integration.show_test === false" in renderer
    assert "integration.status_detail" in renderer
    assert "integration.status_icon" in renderer


def test_no_internal_vocabulary_on_the_page(body):
    low = body.lower()
    assert "mcp connector" not in low
    assert "mcp-connector" not in low


# ── Layer 2: the served JSON per resolver outcome ─────────────────────────────


def test_health_json_per_state(client):
    oauth = _github_json(client, "oauth")
    assert (oauth["status"], oauth["status_message"]) == (
        "connected",  # #2075: a bound grant with no recorded check claims no health
        "Connected with your GitHub account.",
    )
    pat = _github_json(client, "pat_stale")
    assert (pat["status_icon"], pat["status_message"], pat["status_detail"]) == (
        "⚠️",
        "Connected via your personal token",
        "Your GitHub connection needs re-authorizing, so I'm not using it right now.",
    )
    stale = _github_json(client, "stale_nothing")
    assert (stale["status_icon"], stale["status_message"], stale["status_detail"]) == (
        "⚠️",
        "Needs reconnecting",
        "GitHub no longer accepts your connection.",
    )
    assert stale["action"] == "reconnect" and stale["show_test"] is False
    nothing = _github_json(client, "nothing")
    assert (nothing["status"], nothing["status_message"], nothing["can_test"]) == (
        "not_configured",
        "Not configured",
        False,
    )
    for card in (oauth, pat, stale, nothing):
        assert "mcp connector" not in json.dumps(card).lower()


# ── Layer 3: the page's own renderer on that JSON ─────────────────────────────


@needs_node
def test_rendered_connected_card(client, body):
    html = _render(body, _github_json(client, "oauth"))
    assert "Connected with your GitHub account." in html
    assert 'id="test-btn-github"' in html and "disabled" not in html
    assert 'id="reconnect-btn-github"' not in html
    # #2187 (CXO 14:32 10-28): a connected card with no Test on record says so on its
    # health line; a binding alone never renders as a checked connection. No warning glyph.
    assert "status-detail" in html and "Not checked yet. Press Test." in html
    assert "⚠️" not in html


@needs_node
def test_rendered_connected_card_with_a_recorded_check_keeps_the_leg_sentence(client, body):
    """#2066: once a check is recorded the OAuth card carries last_check (CI's full suite
    records one before this file runs); the page appends the time to the leg sentence
    instead of replacing it with "Healthy." (the main-red on beb244edbc)."""
    from datetime import datetime, timezone

    github = _github_json(client, "oauth")
    # #2075: a recorded passing check is what makes the OAuth card "healthy"; the
    # unchecked card is "connected" and carries no time line.
    github["status"] = "healthy"
    github["last_check"] = datetime.now(timezone.utc).isoformat()
    html = _render(body, github)
    assert "Connected with your GitHub account." in html
    assert "Checked just now." in html
    assert "Healthy." not in html
    assert 'id="reconnect-btn-github"' not in html and "⚠️" not in html


@needs_node
def test_rendered_token_serving_card(client, body):
    html = _render(body, _github_json(client, "pat_stale"))
    assert "⚠️" in html
    assert "Connected via your personal token" in html
    assert "Your GitHub connection needs re-authorizing, so I'm not using it right now." in html
    assert 'class="status-dot degraded"' in html
    assert 'id="test-btn-github"' in html and "disabled" not in html
    assert 'id="reconnect-btn-github"' in html  # #2053 (CXO): Reconnect beside Test


@needs_node
def test_rendered_needs_reconnecting_card(client, body):
    html = _render(body, _github_json(client, "stale_nothing"))
    assert "⚠️" in html
    assert "Needs reconnecting" in html
    assert "GitHub no longer accepts your connection." in html
    assert "Not configured" not in html
    assert 'id="test-btn-github"' not in html  # Test hidden, not just disabled
    assert 'href="/settings/integrations/github"' in html
    assert 'id="reconnect-btn-github"' in html and ">Reconnect with GitHub<" in html.replace(
        " <", "<"
    ).replace("> ", ">")
    assert 'id="disconnect-btn-github"' not in html and 'id="connect-btn-github"' not in html


@needs_node
def test_rendered_not_configured_card(client, body):
    html = _render(body, _github_json(client, "nothing"))
    assert "Not configured" in html
    assert 'id="test-btn-github"' in html and "disabled" in html
    assert ">Connect<" in html.replace(" <", "<").replace("> ", ">")
    assert 'id="reconnect-btn-github"' not in html and "⚠️" not in html


@needs_node
def test_no_rendered_card_says_mcp_connector(client, body):
    for state in STATES:
        assert "mcp connector" not in _render(body, _github_json(client, state)).lower()
