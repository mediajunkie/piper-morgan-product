"""#2037: the Integrations Test button shows the API's own message (toast and card
status line), verbatim, with no latency; a stale OAuth grant gets the warning style.

The stale state is keyed on the API's structured ``stale_reason`` field (Arch's ruling,
ADR-070 B4/B5), never on the message copy: a reworded line with the flag still warns, and
the "needs re-authorizing" sentence without the flag does not.

Runs the served page's OWN ``testConnection`` / ``testAllConnections`` under Node with a minimal DOM/fetch stub
(not a browser: no CSS, no click). Node-dependent tests skip when ``node`` is absent.
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

OAUTH = "GitHub is working, using your GitHub connection."
PAT = "GitHub is working, using your personal token."
STALE = (
    "GitHub is working, using your personal token. "
    "GitHub no longer accepts your connection, so I'm not using it right now."
)
FAILURE = "GitHub rejected the token."


@pytest.fixture(scope="module")
def body():
    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(REPO / "templates"))
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2037@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    r = c.get(PAGE)
    assert r.status_code == 200
    return r.text


def _handler(body: str) -> str:
    start = body.index("// #2037: a Test result is stale when the API sets its structured")
    end = body.index("async function testAllConnections()")
    return body[start:end]


def _test_all(body: str) -> str:
    start = body.index("async function testAllConnections()")
    end = body.index("function updateLastUpdated(")
    return body[start:end]


def _run(body: str, reply: dict) -> dict:
    script = (
        "const calls = []; const status = {cls: new Set(), text: ''};\n"
        "const btn = { disabled: false, textContent: '', classList: {add(){}, remove(){}} };\n"
        "const statusEl = { get textContent() { return status.text; },\n"
        "  set textContent(v) { status.text = v; },\n"
        "  classList: { add(c) { status.cls.add(c); }, remove(c) { status.cls.delete(c); },\n"
        "    toggle(c, on) { on ? status.cls.add(c) : status.cls.delete(c); } } };\n"
        "const dot = { className: '' };\n"
        "const card = { querySelector(s) { return s === '.status-dot' ? dot : { appendChild(){} }; } };\n"
        "const document = { getElementById(id) {\n"
        "  if (id.startsWith('test-btn-')) return btn;\n"
        "  if (id.startsWith('status-')) return statusEl;\n"
        "  if (id.startsWith('card-')) return card;\n"
        "  return null; },\n"
        "  createElement() { return {}; } };\n"
        "const fetch = async () => ({ json: async () => JSON.parse(process.argv[1]) });\n"
        "const Toast = { show(type, title, message) { calls.push({type, message, title}); } };\n"
        "function loadIntegrationsHealth() {}\n"
        "const couldNotCheckLine = {};\n"  # the page's couldn't-check memory (CXO, Arch 11-18)  # #2045: the page redraws after a Test
        + _handler(body)
        + "\n(async () => { await testConnection('github');\n"
        "process.stdout.write(JSON.stringify({toast: calls, status: status.text,\n"
        "  cls: [...status.cls], dot: dot.className})); })();\n"
    )
    res = subprocess.run(
        ["node", "-e", script, json.dumps(reply)], capture_output=True, text=True, timeout=30
    )
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


def _ok(message: str, leg: str = "oauth", stale_reason=None) -> dict:
    return {
        "integration": "github",
        "success": True,
        "message": message,
        "latency_ms": 368.81,
        "leg": leg,
        "stale_reason": stale_reason,
    }


def test_page_no_longer_builds_the_generic_toast_or_shows_latency(body):
    handler = _handler(body)
    assert "connection successful`" not in handler
    assert "latency_ms" not in handler
    assert "Connected (" not in body
    # The stale state is the structured field, never a copy match (Arch, 2026-10-15).
    assert "needs re-authorizing" not in handler
    assert "needs re-authorizing" not in _test_all(body)
    assert "isStaleOAuthMessage" not in body
    assert "result.stale_reason" in handler
    assert "result.stale_reason" in _test_all(body)


@needs_node
@pytest.mark.parametrize("message,leg", [(OAUTH, "oauth"), (PAT, "pat")])
def test_working_legs_show_the_message_verbatim(body, message, leg):
    out = _run(body, _ok(message, leg=leg))
    assert out["toast"] == [{"type": "success", "message": message, "title": "Test Passed"}]
    assert out["status"] == message
    assert "warning" not in out["cls"] and "error" not in out["cls"]
    assert out["dot"] == "status-dot healthy"
    assert "368" not in out["status"]


@needs_node
def test_stale_oauth_line_gets_the_warning_style(body):
    out = _run(body, _ok(STALE, leg="pat", stale_reason="stale_token"))
    assert out["toast"] == [
        {"type": "warning", "message": STALE, "title": "Works, needs attention"}
    ]
    assert out["status"] == STALE
    assert "warning" in out["cls"] and "error" not in out["cls"]
    assert out["dot"] == "status-dot degraded"
    assert "368" not in out["status"]


@needs_node
def test_generic_failure_keeps_the_error_style(body):
    reply = {
        "integration": "github",
        "success": False,
        "message": FAILURE,
        "latency_ms": 12.0,
        "fix_suggestion": "Check your token.",
        "leg": None,
        "stale_reason": None,
    }
    out = _run(body, reply)
    assert out["toast"] == [{"type": "error", "message": FAILURE, "title": "Test Failed"}]
    assert out["status"] == FAILURE
    assert "error" in out["cls"] and "warning" not in out["cls"]
    assert out["dot"] == "status-dot failed"


@needs_node
def test_warning_keys_on_the_flag_not_the_sentence(body):
    # A CXO reword of the stale line must not turn a stale connection green.
    reworded = "GitHub works through your personal token; reconnect GitHub to use your account."
    out = _run(body, _ok(reworded, leg="pat", stale_reason="stale_token"))
    assert out["toast"] == [
        {"type": "warning", "message": reworded, "title": "Works, needs attention"}
    ]
    assert out["status"] == reworded
    assert "warning" in out["cls"]
    assert out["dot"] == "status-dot degraded"

    # And the old sentence WITHOUT the flag is a plain success: copy carries no state.
    out = _run(body, _ok(STALE, leg="pat", stale_reason=None))
    assert out["toast"] == [{"type": "success", "message": STALE, "title": "Test Passed"}]
    assert "warning" not in out["cls"]
    assert out["dot"] == "status-dot healthy"


def _run_all(body: str, replies: list) -> dict:
    script = (
        "const toasts = []; const cards = {};\n"
        "function mk(name) { const st = {cls: new Set(), text: ''}; const dot = {className: ''};\n"
        "  cards[name] = {st, dot};\n"
        "  return { dot, statusEl: { get textContent() { return st.text; },\n"
        "    set textContent(v) { st.text = v; },\n"
        "    classList: { add(c) { st.cls.add(c); }, remove(c) { st.cls.delete(c); },\n"
        "      toggle(c, on) { on ? st.cls.add(c) : st.cls.delete(c); } } } }; }\n"
        "const els = {};\n"
        "const btn = { disabled: false, textContent: '', classList: {add(){}, remove(){}} };\n"
        "const document = { getElementById(id) {\n"
        "  if (id === 'test-all-btn') return btn;\n"
        "  const m = id.match(/^(card|status)-(.*)$/); if (!m) return null;\n"
        "  const name = m[2]; if (!els[name]) els[name] = mk(name);\n"
        "  if (m[1] === 'status') return els[name].statusEl;\n"
        "  return { querySelector() { return els[name].dot; } }; } };\n"
        "const fetch = async () => ({ json: async () => JSON.parse(process.argv[1]) });\n"
        "const Toast = { show(type, title, message) { toasts.push({type, message, title}); } };\n"
        "function loadIntegrationsHealth() {}\n"
        "const couldNotCheckLine = {};\n"  # the page's couldn't-check memory (CXO, Arch 11-18)
        + _test_all(body)
        + "\n(async () => { await testAllConnections();\n"
        "const out = {}; for (const [k, v] of Object.entries(cards))\n"
        "  out[k] = {status: v.st.text, cls: [...v.st.cls], dot: v.dot.className};\n"
        "process.stdout.write(JSON.stringify({toasts, cards: out})); })();\n"
    )
    res = subprocess.run(
        ["node", "-e", script, json.dumps(replies)], capture_output=True, text=True, timeout=30
    )
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


@needs_node
def test_test_all_keys_the_degraded_dot_on_the_flag(body):
    reworded = "GitHub works through your personal token; reconnect GitHub to use your account."
    gh = _ok(reworded, leg="pat", stale_reason="stale_token")
    notion = {
        "integration": "notion",
        "success": True,
        "message": STALE,
        "leg": None,
        "stale_reason": None,
    }
    cal = {
        "integration": "calendar",
        "success": False,
        "message": FAILURE,
        "leg": None,
        "stale_reason": None,
    }
    out = _run_all(body, [gh, notion, cal])
    assert out["cards"]["github"] == {
        "status": reworded,
        "cls": ["warning"],
        "dot": "status-dot degraded",
    }
    # The stale sentence without the flag is not a warning (copy carries no state).
    assert out["cards"]["notion"] == {"status": STALE, "cls": [], "dot": "status-dot healthy"}
    assert out["cards"]["calendar"]["dot"] == "status-dot failed"
    assert "error" in out["cards"]["calendar"]["cls"]
    assert "warning" not in out["cards"]["calendar"]["cls"]
    assert out["toasts"] == [
        {
            "type": "warning",
            "message": "2 of 3 connections successful",
            "title": "Some Tests Failed",
        }
    ]
