"""#2029: Settings → GitHub shows a stale grant as stale, keeps a Reconnect, and says
"Connected" only for a live binding. Copy is CXO's (2026-10-15), verbatim.

Layer: the rendered page through the app's TestClient (template render). The three
states are JS branches on the ``oauth-status`` JSON (``data.stale``,
``data.serving === 'pat'``, ``data.connected``), so this pins each branch key and the
strings inside it in the served HTML. It does NOT execute the JS in a browser; the
served judgement (Web or PA with xian) covers that.
"""

from __future__ import annotations

import re
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

REPO = Path(__file__).resolve().parents[3]
PAGE = "/settings/integrations/github"


@pytest.fixture(scope="module")
def body():
    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(REPO / "templates"))
    client = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2029@example.com", scopes=["user"]
    )
    client.cookies.set("auth_token", token)
    r = client.get(PAGE)
    assert r.status_code == 200, f"{PAGE} -> {r.status_code}"
    return r.text


def _status_fn(body: str) -> str:
    start = body.index("async function checkGitHubOAuthStatus()")
    end = body.index("async function saveGitHubToken()")
    return body[start:end]


def _branch(fn: str, key: str, until: str) -> str:
    return fn[fn.index(key) : fn.index(until, fn.index(key))]


def test_page_reads_oauth_status(body):
    assert "fetch('/api/v1/settings/integrations/github/oauth-status')" in body


def test_stale_without_a_serving_token_shows_needs_reconnecting(body):
    fn = _status_fn(body)
    stale = _branch(fn, "if (data.stale) {", "return;")
    no_pat = stale[stale.index("} else {") :]
    assert "iconEl.textContent = '⚠️'" in no_pat
    assert "titleEl.textContent = 'Needs reconnecting'" in no_pat
    assert (
        '"GitHub no longer accepts your connection, so I can\'t read your GitHub right now."'
        in no_pat
    )


def test_stale_keeps_the_connect_group_as_reconnect(body):
    fn = _status_fn(body)
    stale = _branch(fn, "if (data.stale) {", "return;")
    assert "btnEl.textContent = 'Reconnect with GitHub'" in stale
    assert "'Reconnect to give me access again. Nothing else on your account changes.'" in stale
    # Kept, not replaced: the stale branch never rewrites the group's innerHTML, and it
    # returns before the connected branch can.
    assert "group.innerHTML" not in stale
    assert fn.index("if (data.stale) {") < fn.index("if (data.connected && group)")
    # The button and hint it rewrites are on the page and the button starts the OAuth flow.
    assert 'id="oauth-connect-hint"' in body
    assert re.search(r'id="oauth-connect-btn"\s+onclick="connectGitHubOAuth\(\)"', body)


def test_stale_with_a_working_personal_token(body):
    fn = _status_fn(body)
    stale = _branch(fn, "if (data.stale) {", "return;")
    pat = _branch(stale, "if (data.serving === 'pat') {", "} else {")
    assert "titleEl.textContent = 'Connected via your personal token'" in pat
    assert '"Your GitHub connection needs re-authorizing, so I\'m not using it right now."' in pat


def test_connected_wording(body):
    fn = _status_fn(body)
    assert "'✓ Connected with GitHub.</p>'" in fn
    connected = _branch(fn, "if (data.connected) {", "} catch")
    assert "titleEl.textContent = 'Connected'" in connected
    # #2279 (CXO 2026-11-04 18:32): the subtitle claims no owner now; the login is read
    # from the grant on the Integrations card, not here.
    assert "subtitleEl.textContent = 'Connected with GitHub.'" in connected


def test_no_internal_vocabulary_on_the_page(body):
    low = body.lower()
    assert "mcp connector" not in low
    assert "mcp-connector" not in low
    assert "via OAuth (MCP" not in body


def test_stale_with_a_serving_token_is_amber_not_green(body):
    """CXO 2026-10-15 16:30: the token-serving state keeps ⚠️ (half good: reads
    work, the grant is still broken); ✅ is for a fully healthy connection only."""
    fn = _status_fn(body)
    stale = _branch(fn, "if (data.stale) {", "return;")
    pat = stale[stale.index("if (data.serving === 'pat') {") : stale.index("} else {")]
    assert "iconEl.textContent = '⚠️'" in pat
    assert "iconEl.textContent = '✅'" not in pat
    assert "status-icon disconnected" in pat
    assert "titleEl.textContent = 'Connected via your personal token'" in pat
