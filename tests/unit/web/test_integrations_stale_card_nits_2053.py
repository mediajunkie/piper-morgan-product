"""#2053 (CXO's three rulings on the stale GitHub card): the warning toast's title, a
Reconnect link in every stale state, and the re-authorize sentence shown once after a Test.

Runs the page's OWN ``testConnection`` and ``renderIntegrations`` under Node with minimal
DOM/fetch stubs (no browser: no CSS, no click). Skipped when ``node`` is absent.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

REPO = Path(__file__).resolve().parents[3]
PAGE = "/settings/integrations"
SENTENCE = "Your GitHub connection needs re-authorizing, so I'm not using it right now."
STALE_MSG = f"GitHub is working, using your personal token. {SENTENCE}"

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


@pytest.fixture(scope="module")
def body():
    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(REPO / "templates"))
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2053@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    r = c.get(PAGE)
    assert r.status_code == 200
    return r.text


def _slice(body: str, start: str, end: str) -> str:
    return body[body.index(start) : body.index(end)]


def _consts_and_renderer(body: str) -> str:
    consts = _slice(body, "// Integration icons mapping", "// Status icons for overall health")
    return consts + _slice(
        body, "function renderIntegrations(", "async function testConnection(integrationName)"
    )


def _handler(body: str) -> str:
    return _slice(
        body, "// #2037: a Test result is stale when", "async function testAllConnections()"
    )


PAT_CARD = {
    "name": "github",
    "display_name": "GitHub",
    "status": "degraded",
    "status_icon": "⚠️",
    "status_message": "Connected via your personal token",
    "status_detail": SENTENCE,
    "configure_url": "/settings/integrations/github",
    "can_test": True,
    "show_test": True,
    "action": "reconnect",
}
NO_TOKEN_CARD = {
    **PAT_CARD,
    "status_message": "Needs reconnecting",
    "status_detail": "GitHub no longer accepts your connection.",
    "can_test": False,
    "show_test": False,
}


def _render(body: str, card: dict, owns_line=None) -> str:
    script = (
        "const window = { __OFFERED_CONNECTORS__: ['github', 'calendar'] };\n"
        "const out = {};\n"
        "const document = { getElementById(id) { return id === 'integrations-list' ? out : null; } };\n"
        + _consts_and_renderer(body)
        + "\nresultOwnsLine = JSON.parse(process.argv[2]);\nrenderIntegrations(JSON.parse(process.argv[1]));\n"
        "process.stdout.write(out.innerHTML);\n"
    )
    res = subprocess.run(
        ["node", "-e", script, json.dumps([card]), json.dumps(owns_line)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert res.returncode == 0, res.stderr
    return " ".join(res.stdout.split())


def _run_test(body: str, reply: dict) -> dict:
    """Run testConnection; record the toast and what the redraw was asked to own."""
    script = (
        "const calls = []; const redraws = []; let resultOwnsLine = null;\n"
        "const el = { disabled: false, textContent: '', classList: {add(){}, remove(){}, toggle(){}} };\n"
        "const dot = { className: '' };\n"
        "const card = { querySelector(s) { return s === '.status-dot' ? dot : { appendChild(){} }; } };\n"
        "const document = { getElementById(id) { return id.startsWith('card-') ? card : id.startsWith('fix-') ? null : el; },\n"
        "  createElement() { return {}; } };\n"
        "const fetch = async () => ({ json: async () => JSON.parse(process.argv[1]) });\n"
        "const Toast = { show(type, title, message) { calls.push({type, message, title}); } };\n"
        "function loadIntegrationsHealth() { redraws.push(resultOwnsLine); }\n"
        + _handler(body)
        + "\n(async () => { await testConnection('github');\n"
        "process.stdout.write(JSON.stringify({toast: calls, redraws})); })();\n"
    )
    res = subprocess.run(
        ["node", "-e", script, json.dumps(reply)], capture_output=True, text=True, timeout=30
    )
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


def _reply(success=True, message=STALE_MSG, stale_reason="stale_token") -> dict:
    return {
        "integration": "github",
        "success": success,
        "message": message,
        "stale_reason": stale_reason,
    }


# ── 1. toast titles ───────────────────────────────────────────────────────────


@needs_node
def test_warning_toast_title(body):
    out = _run_test(body, _reply())
    assert out["toast"] == [
        {"type": "warning", "message": STALE_MSG, "title": "Works, needs attention"}
    ]


@needs_node
def test_plain_success_and_failure_titles_unchanged(body):
    ok = _run_test(body, _reply(message="GitHub is working.", stale_reason=None))
    assert ok["toast"][0]["title"] == "Test Passed" and ok["toast"][0]["type"] == "success"
    bad = _run_test(body, _reply(success=False, message="Rejected.", stale_reason=None))
    assert bad["toast"] == [{"type": "error", "message": "Rejected.", "title": "Test Failed"}]


# ── 2. Reconnect in every stale state ─────────────────────────────────────────


@needs_node
def test_stale_plus_pat_card_has_reconnect_and_test(body):
    html = _render(body, PAT_CARD)
    assert 'id="reconnect-btn-github"' in html
    assert 'href="/settings/integrations/github"' in html
    assert ">Reconnect with GitHub<" in html.replace(" <", "<").replace("> ", ">")
    assert 'id="test-btn-github"' in html and "disabled" not in html


@needs_node
def test_stale_no_token_card_still_has_reconnect_and_no_test(body):
    html = _render(body, NO_TOKEN_CARD)
    assert 'id="reconnect-btn-github"' in html
    assert 'id="test-btn-github"' not in html


# ── 3. the re-authorize sentence once after a Test ────────────────────────────


@needs_node
def test_warning_test_asks_the_redraw_to_drop_the_detail(body):
    assert _run_test(body, _reply())["redraws"] == ["github"]
    assert _run_test(body, _reply(message="ok", stale_reason=None))["redraws"] == [None]


@needs_node
def test_sentence_appears_once_with_the_result_on_screen(body):
    # No Test yet: the card's own subtitle carries it, once.
    assert _render(body, PAT_CARD).count(SENTENCE) == 1
    # After a warning Test: the result (toast + status line) owns it; the card does not.
    redrawn = _render(body, PAT_CARD, owns_line="github")
    assert SENTENCE not in redrawn
    assert "Connected via your personal token" in redrawn
    shown = _run_test(body, _reply())["toast"][0]["message"] + " " + redrawn
    assert shown.count(SENTENCE) == 1
