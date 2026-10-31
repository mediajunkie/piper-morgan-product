"""#2044 (CXO, 2026-10-15): an integration with a connection but no test result reads
"Connected" with the health line "Not checked yet. Press Test." on its card, for every
provider; "unknown" never reaches a configured card; the healthy summary does not count
an unchecked connection.

Cause pinned: the health monitor registered every component as UNKNOWN with a real
``last_check`` at startup, so a just-connected integration took the "tested" branch and
rendered "Status: unknown" (xian, row E, 2026-10-15 18:43). Since #2071 the card reads
the viewer's own Test result from the per-principal store, so "never tested" is "no
record for this principal", including when another account has tested.

Layers: the route function per provider (another account's record only, and an empty
store); the served JSON through the app's TestClient; the page's own
``renderIntegrations`` under Node (skipped without ``node``). Not a browser.
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
from services.integrations.principal_test_results import PrincipalTestResultStore
from web.api.routes import integrations
from web.app import app

REPO = Path(__file__).resolve().parents[3]
PAGE = "/settings/integrations"
HEALTH = "/api/v1/integrations/health"
PROVIDERS = [k for k in integrations.INTEGRATION_REGISTRY if k != "github"]


def _store_tested_by(principal: str, provider: str, ok: bool = True) -> PrincipalTestResultStore:
    store = PrincipalTestResultStore()
    store.record_test_result(principal, provider, ok=ok, error=None if ok else "boom")
    return store


async def _card(provider: str, store: PrincipalTestResultStore):
    meta = integrations.INTEGRATION_REGISTRY[provider]
    with (
        patch.object(
            integrations, "_get_integration_config_status", new=AsyncMock(return_value="configured")
        ),
        patch.object(integrations, "_get_test_result_store", return_value=store),
    ):
        return await integrations._check_integration_health(provider, meta, user_id="u1")


def _assert_unchecked(status, provider: str):
    assert status.status == "connected", (provider, status.status)
    assert status.status_message == "Connected", (provider, status.status_message)
    assert status.status_detail == "Not checked yet. Press Test.", (provider, status.status_detail)
    assert status.can_test is True
    assert "unknown" not in json.dumps(status.model_dump()).lower(), (provider, status)


@pytest.mark.asyncio
@pytest.mark.parametrize("provider", PROVIDERS)
async def test_another_accounts_test_is_still_the_unchecked_card(provider):
    """#2071: another account's Test result (pass or fail) is 'never tested' for u1."""
    for ok in (True, False):
        _assert_unchecked(
            await _card(provider, _store_tested_by("u-other", provider, ok)), provider
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("provider", PROVIDERS)
async def test_no_record_at_all_is_the_unchecked_card(provider):
    _assert_unchecked(await _card(provider, PrincipalTestResultStore()), provider)


@pytest.mark.asyncio
async def test_a_recorded_healthy_check_still_reads_healthy():
    status = await _card("calendar", _store_tested_by("u1", "calendar"))
    assert status.status == "healthy"
    assert status.status_message.startswith("Healthy")


@pytest.mark.asyncio
async def test_a_health_check_that_throws_says_so_and_keeps_the_error_off_the_card():
    """CXO 19:01: "Couldn't check this just now. Press Test to try again."; the raw
    error goes to the log, not the card (``error`` unset so the page does not redden)."""
    meta = integrations.INTEGRATION_REGISTRY["calendar"]
    with patch.object(
        integrations,
        "_get_integration_config_status",
        new=AsyncMock(side_effect=RuntimeError("keychain exploded: secret-ish detail")),
    ):
        status = await integrations._check_integration_health("calendar", meta, user_id="u1")
    assert status.status_message == "Couldn't check this just now. Press Test to try again."
    assert status.error is None
    assert status.can_test is True
    assert "exploded" not in json.dumps(status.model_dump())
    assert "Status unknown" not in json.dumps(status.model_dump())


def test_the_route_module_has_no_status_unknown_line_for_a_configured_card():
    src = (REPO / "web/api/routes/integrations.py").read_text()
    assert "Click 'Test' to check connection" not in src
    assert '"Status unknown"' not in src
    assert 'status="unknown",\n            status_message="Status: ' not in src
    assert src.count("UNCHECKED_DETAIL") >= 2  # the constant and its one use


@pytest.fixture(scope="module")
def client():
    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(REPO / "templates"))
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2044@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    return c


def test_served_json_unchecked_calendar_is_not_counted_healthy(client):
    """Through the real route: every provider configured, only another account tested."""
    store = PrincipalTestResultStore()
    for name in integrations.INTEGRATION_REGISTRY:
        store.record_test_result("u-other", name, ok=True)
    with (
        patch.object(
            integrations, "_get_integration_config_status", new=AsyncMock(return_value="configured")
        ),
        patch.object(integrations, "_get_test_result_store", return_value=store),
        patch.object(integrations, "_github_card", new=AsyncMock(return_value=None)),
    ):
        r = client.get(HEALTH)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["healthy_count"] == 0
    assert body["total_count"] == len(integrations.INTEGRATION_REGISTRY)
    for card in body["integrations"]:
        assert card["status"] == "connected", card
        assert card["status_message"] == "Connected", card
        assert card["status_detail"] == "Not checked yet. Press Test.", card
    assert "unknown" not in json.dumps(body["integrations"]).lower()


def test_a_test_result_redraws_the_page_from_the_health_route(client):
    """#2045: after a Test (pass, fail or error) ``testConnection`` re-fetches the health
    route once, after the button reset, so the unchecked line goes and the summary
    recounts; a redraw failure never reaches the toast (it is guarded, not in the try)."""
    body = client.get(PAGE).text
    start = body.index("async function testConnection(integrationName)")
    end = body.index("async function testAllConnections()")
    fn = body[start:end]
    assert fn.count("await loadIntegrationsHealth();") == 1, fn
    tail = fn[fn.index("'Test Error'") :]
    assert "await loadIntegrationsHealth();" in tail  # after the result handling
    assert "Failed to redraw integrations after Test" in tail  # its own catch


needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


def _renderer(body: str) -> str:
    consts = body[
        body.index("// Integration icons mapping") : body.index(
            "// Status icons for overall health"
        )
    ]
    start = body.index("function renderIntegrations(integrations) {")
    end = body.index("async function testConnection(integrationName)")
    return consts + body[start:end]


@needs_node
def test_page_renders_connected_and_the_not_checked_line(client):
    page = client.get(PAGE)
    assert page.status_code == 200
    body = page.text
    assert ".status-dot.connected" in body  # the dot has a colour for the new state
    card = {
        "name": "calendar",
        "display_name": "Google Calendar",
        "status": "connected",
        "status_message": "Connected",
        "status_detail": "Not checked yet. Press Test.",
        "can_test": True,
        "configure_url": "/settings/integrations/calendar",
        "show_test": True,
    }
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
        ["node", "-e", script, json.dumps([card])], capture_output=True, text=True, timeout=30
    )
    assert res.returncode == 0, res.stderr
    html = " ".join(res.stdout.split())
    assert 'class="status-dot connected"' in html
    assert ">Connected<" in html.replace("> Connected <", ">Connected<")
    assert "Not checked yet. Press Test." in html
    assert "unknown" not in html.lower()
    assert (
        'id="test-btn-calendar"' in html
        and "disabled" not in html.split('id="test-btn-calendar"')[1].split(">")[0]
    )
