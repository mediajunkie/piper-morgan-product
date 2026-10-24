"""#2154 (#2151 route group 2; Arch 10-24 09:09, CXO 10-24 09:32): a failed preferences
read must never become a save of defaults over the user's stored values.

Layers:
1. the server: ``_load_prefs_db`` / ``_load_github_prefs_db`` raise on a DB error (they
   returned {}), and every preferences GET answers 503 with CXO's line, through the app;
   every preferences read in the routes file goes through the 503 path;
2. each page's OWN load and save functions (extracted from the template) under Node with
   a stubbed DOM and fetch: after a failed load the line replaces the form, Save is
   disabled, and the save function sends no POST. Skipped when ``node`` isn't on PATH.
   Not a browser: no CSS or click; Web's served rows cover the healthy path.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import uuid
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

REPO = Path(__file__).resolve().parents[3]
ROUTES = REPO / "web/api/routes/settings_integrations.py"
LINE = (
    "I couldn't load {thing} just now, so Saving is turned off to keep your saved "
    "settings as they are. Reload to try again; if it keeps failing, tell us."
)
_CONFIG = "services.connectors.config_service.ConnectorConfigService.get_config"


@pytest.fixture(scope="module")
def client():
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2154@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    return c


# ── Layer 1: the server ──────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "connector,thing",
    [
        ("slack", "your Slack preferences"),
        ("calendar", "your Google Calendar preferences"),
        ("notion", "your Notion preferences"),
        ("github", "your GitHub preferences"),
    ],
)
def test_a_failed_preferences_read_is_a_503_with_cxos_line(client, connector, thing):
    with patch(_CONFIG, new=AsyncMock(side_effect=OSError("fake db down"))):
        r = client.get(f"/api/v1/settings/integrations/{connector}/preferences")
    assert r.status_code == 503, r.text
    assert r.json()["detail"] == LINE.format(thing=thing)


def test_a_verified_miss_still_answers_defaults(client):
    with (
        patch(_CONFIG, new=AsyncMock(return_value={})),
        patch("web.api.routes.settings_integrations._read_legacy_pref_file", return_value={}),
    ):
        r = client.get("/api/v1/settings/integrations/slack/preferences")
    assert r.status_code == 200
    assert r.json()["monitored_channels"] == []


@pytest.mark.asyncio
async def test_the_loaders_raise_on_a_db_error():
    from web.api.routes import settings_integrations as si

    with patch(_CONFIG, new=AsyncMock(side_effect=OSError("fake"))):
        with pytest.raises(si.PreferencesReadFailed):
            await si._load_prefs_db("u", "slack")
        with pytest.raises(si.PreferencesReadFailed):
            await si._load_github_prefs_db("u")


def test_every_route_read_of_preferences_goes_through_the_503():
    src = ROUTES.read_text()
    bare = re.findall(r"user_prefs = await _load_prefs_db\(", src)
    assert bare == [], "a route reads _load_prefs_db directly (no 503 on failure)"
    github_reads = [m.start() for m in re.finditer(r"await _load_github_prefs_db\(", src)]
    for at in github_reads:
        window = src[at : at + 300]
        assert "except PreferencesReadFailed" in window, "a GitHub prefs read without the 503"
    for thing in ("your saved calendar choices", "your saved database choices"):
        assert f'"{thing}"' in src


# ── Layer 2: the pages under Node ────────────────────────────────────────────

needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


def _fn(body: str, name: str) -> str:
    """The source of ``async function name(...) { ... }`` by brace matching."""
    start = body.index(f"async function {name}(")
    i = body.index("{", start)
    depth = 0
    for j in range(i, len(body)):
        if body[j] == "{":
            depth += 1
        elif body[j] == "}":
            depth -= 1
            if depth == 0:
                return body[start : j + 1]
    raise AssertionError(f"unbalanced {name}")


def _helpers(body: str) -> str:
    a = body.index("let prefsLoadFailed = false;")
    b = body.index("function showPrefsLoadFailed(")
    end = _fn(
        body.replace("function showPrefsLoadFailed(", "async function showPrefsLoadFailed(", 1),
        "showPrefsLoadFailed",
    )
    return body[a:b] + end.replace("async function", "function", 1)


_STUB = r"""
const els = {};
function el(id) {
  if (!els[id]) els[id] = { id, innerHTML: '', textContent: '', disabled: false, value: '',
    style: {}, children: [], className: '', attrs: {},
    appendChild(c) { this.children.push(c); }, setAttribute(k, v) { this.attrs[k] = v; } };
  return els[id];
}
const document = {
  getElementById: (id) => el(id),
  createElement: (t) => ({ tag: t, textContent: '', className: '', attrs: {},
    setAttribute(k, v) { this.attrs[k] = v; } }),
  querySelectorAll: () => [],
};
const Toast = { show() {} };
const posts = [];
let responses = {};
async function fetch(url, opts) {
  if (opts && opts.method === 'POST') { posts.push(url); return { ok: true, status: 200, json: async () => ({}) }; }
  const r = responses[url] || { status: 200, body: {} };
  return { ok: r.status < 400, status: r.status, json: async () => r.body };
}
function parseApiDetail(d, f) { return d || f; }
function escapeHtml(s) { return String(s); }
"""


def _run(body: str, load: str, save: str, responses: dict, after_load: str = "") -> dict:
    script = (
        _STUB
        + _helpers(body)
        + "\n"
        + _fn(body, load)
        + "\n"
        + _fn(body, save)
        + "\n(async () => {\n"
        + f"  responses = {json.dumps(responses)};\n"
        + f"  await {load}();\n"
        + after_load
        + f"  await {save}();\n"
        + "  const notes = Object.values(els).flatMap(e => e.children.filter(c => c.className === 'prefs-load-failed').map(c => c.textContent));\n"
        + "  const disabled = Object.values(els).filter(e => e.disabled).map(e => e.id);\n"
        + "  process.stdout.write(JSON.stringify({ posts, notes, disabled, flag: prefsLoadFailed }));\n"
        + "})().catch(e => { console.error(e); process.exit(1); });\n"
    )
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


def _page(name: str) -> str:
    return (REPO / "templates" / f"settings_{name}.html").read_text()


def _detail(thing: str) -> dict:
    return {"status": 503, "body": {"detail": LINE.format(thing=thing)}}


@needs_node
def test_slack_a_failed_preferences_load_locks_the_form():
    out = _run(
        _page("slack"),
        "loadChannelSettings",
        "saveSlackPreferences",
        {
            "/api/v1/settings/integrations/slack/channels": {
                "status": 200,
                "body": {"channels": []},
            },
            "/api/v1/settings/integrations/slack/preferences": _detail("your Slack preferences"),
        },
    )
    assert out["posts"] == []
    assert out["notes"] == [LINE.format(thing="your Slack preferences")]
    assert "save-preferences-btn" in out["disabled"] and out["flag"] is True


@needs_node
def test_calendar_a_failed_selection_read_locks_the_form():
    out = _run(
        _page("calendar"),
        "loadCalendarList",
        "saveCalendarPreferences",
        {
            "/api/v1/settings/integrations/calendar/calendars": _detail(
                "your saved calendar choices"
            )
        },
    )
    assert out["posts"] == []
    assert out["notes"] == [LINE.format(thing="your saved calendar choices")]
    assert "save-calendar-prefs-btn" in out["disabled"]


@needs_node
@pytest.mark.parametrize(
    "name,load,save,url,thing,btn",
    [
        (
            "github",
            "loadRepositoryList",
            "saveGitHubPreferences",
            "github/repositories",
            "your saved repository choices",
            "save-github-prefs-btn",
        ),
        (
            "notion",
            "loadDatabaseList",
            "saveNotionPreferences",
            "notion/databases",
            "your saved database choices",
            "save-notion-prefs-btn",
        ),
    ],
)
def test_a_failed_list_read_locks_the_form(name, load, save, url, thing, btn):
    out = _run(_page(name), load, save, {f"/api/v1/settings/integrations/{url}": _detail(thing)})
    assert out["posts"] == []
    assert out["notes"] == [LINE.format(thing=thing)]
    assert btn in out["disabled"]


@needs_node
@pytest.mark.parametrize(
    "name,prefs_fn,save,thing,btn",
    [
        (
            "github",
            "loadGitHubPreferences",
            "saveGitHubPreferences",
            "your GitHub preferences",
            "save-github-prefs-btn",
        ),
        (
            "notion",
            "loadNotionPreferences",
            "saveNotionPreferences",
            "your Notion preferences",
            "save-notion-prefs-btn",
        ),
    ],
)
def test_a_failed_default_read_locks_the_form(name, prefs_fn, save, thing, btn):
    out = _run(
        _page(name),
        prefs_fn,
        save,
        {f"/api/v1/settings/integrations/{name}/preferences": _detail(thing)},
    )
    assert out["posts"] == []
    assert out["notes"] == [LINE.format(thing=thing)]
    assert btn in out["disabled"]


@needs_node
def test_a_healthy_slack_load_still_saves():
    """The guard costs nothing on the healthy path: preferences load, Save POSTs."""
    body = _page("slack")
    page_helpers = (
        "function populateChannelDropdowns() {}\n"
        "function populateMonitoredCheckboxes() {}\n"
        "function setSelectedPreferences() {}\n"
        "function getSelectedMonitoredChannels() { return []; }\n"
    )
    responses = {
        "/api/v1/settings/integrations/slack/channels": {"status": 200, "body": {"channels": []}},
        "/api/v1/settings/integrations/slack/preferences": {"status": 200, "body": {}},
    }
    script = (
        _STUB
        + page_helpers
        + _helpers(body)
        + "\n"
        + _fn(body, "loadChannelSettings")
        + "\n"
        + _fn(body, "saveSlackPreferences")
        + "\n(async () => {\n"
        + f"  responses = {json.dumps(responses)};\n"
        + "  await loadChannelSettings();\n  await saveSlackPreferences();\n"
        + "  process.stdout.write(JSON.stringify({ posts, flag: prefsLoadFailed }));\n"
        + "})().catch(e => { console.error(e); process.exit(1); });\n"
    )
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout) == {
        "posts": ["/api/v1/settings/integrations/slack/preferences"],
        "flag": False,
    }
