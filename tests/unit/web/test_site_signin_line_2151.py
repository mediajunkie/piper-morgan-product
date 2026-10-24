"""CXO 10-24 14:24: the Settings pages' app-credentials status is the SITE's own sign-in
app (operator config, #1485 admin-only to change), never a claim about the viewer.

- Slack and Calendar pages: "Slack/Google sign-in is set up for this site." for everyone;
  "Update Credentials" shows to admins only (page JS under Node).
- The setup wizard's two status lines read the same; nothing says "App credentials
  configured" anywhere a user reads.
- #2155: the meeting-time not-connected line has no tail promising meeting-time analysis.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


def _fn(body: str, name: str) -> str:
    start = body.index(f"function {name}(")
    i = body.index("{", start)
    depth = 0
    for j in range(i, len(body)):
        if body[j] == "{":
            depth += 1
        elif body[j] == "}":
            depth -= 1
            if depth == 0:
                return body[start : j + 1]
    raise AssertionError(name)


@needs_node
@pytest.mark.parametrize(
    "page,line",
    [
        ("settings_slack.html", "Slack sign-in is set up for this site."),
        ("settings_calendar.html", "Google sign-in is set up for this site."),
    ],
)
@pytest.mark.parametrize("is_admin,shown", [(True, "block"), (False, "none")])
def test_the_status_names_the_site_and_only_admins_get_update(page, line, is_admin, shown):
    body = (REPO / "templates" / page).read_text()
    script = (
        "const els = {};\n"
        "const document = { getElementById(id) { if (!els[id]) els[id] = { id, className: '',"
        " textContent: '', style: {} }; return els[id]; } };\n"
        f"const window = {{ currentUser: {{ is_admin: {json.dumps(is_admin)} }} }};\n"
        + _fn(body, "updateAppConfigUI")
        + "\nupdateAppConfigUI(true);\n"
        "process.stdout.write(JSON.stringify({ text: els['app-config-status-text'].textContent,"
        " update: els['app-config-configured'].style.display }));\n"
    )
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert out == {"text": line, "update": shown}


def test_no_user_facing_template_says_app_credentials_configured():
    for page in ("settings_slack.html", "settings_calendar.html", "setup.html"):
        assert "App credentials configured" not in (REPO / "templates" / page).read_text()


def test_the_meeting_time_not_connected_line_has_no_analysis_tail():
    src = (REPO / "services/intent/intent_service.py").read_text()
    assert "once it's connected I can analyze your meeting time" not in src
    assert (
        "Google Calendar isn't connected yet, so I can't see your meetings. \"\n"
        "                        'Ask me \"how do I connect Google Calendar?\" and I\\'ll walk you through it.'"
    ) in src


@needs_node
@pytest.mark.parametrize(
    "page,line",
    [
        (
            "settings_slack.html",
            "Slack sign-in isn't set up for this site yet, so you can't connect Slack. Tell us and we'll fix it.",
        ),
        (
            "settings_calendar.html",
            "Google sign-in isn't set up for this site yet, so you can't connect Google Calendar. Tell us and we'll fix it.",
        ),
    ],
)
@pytest.mark.parametrize("is_admin", [True, False])
def test_not_configured_is_a_site_line_for_non_admins_and_the_form_for_admins(page, line, is_admin):
    """CXO 10-24 14:43: a non-admin gets the site line, no form, Connect disabled; an
    admin keeps the form and today's line. Not servable on alpha (both apps configured)."""
    body = (REPO / "templates" / page).read_text()
    script = (
        "const els = {};\n"
        "const document = { getElementById(id) { if (!els[id]) els[id] = { id, className: '',"
        " textContent: '', style: {}, disabled: false }; return els[id]; } };\n"
        f"const window = {{ currentUser: {{ is_admin: {json.dumps(is_admin)} }} }};\n"
        + _fn(body, "updateAppConfigUI")
        + "\nupdateAppConfigUI(false);\n"
        "process.stdout.write(JSON.stringify({ text: els['app-config-status-text'].textContent,"
        " form: els['app-config-form'].style.display, connect: document.getElementById('connect-btn').disabled }));\n"
    )
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    if is_admin:
        assert out["form"] == "block" and out["connect"] is False
        assert out["text"].startswith("App credentials not configured")
    else:
        assert out == {"text": line, "form": "none", "connect": True}


def _async_fn(body: str, name: str) -> str:
    return "async " + _fn(body, name) if f"async function {name}(" in body else _fn(body, name)


@needs_node
@pytest.mark.parametrize(
    "page,svc", [("settings_slack.html", "Slack"), ("settings_calendar.html", "Google")]
)
@pytest.mark.parametrize("how", ["status_500", "fetch_throws"])
@pytest.mark.parametrize("is_admin", [True, False])
def test_a_failed_status_read_is_couldnt_check_and_connect_stays(page, svc, how, is_admin):
    """Arch 10-24 15:29 gap B: a failed status read said "isn't set up" and disabled
    Connect for a non-admin. It's a check that couldn't run: say so, show no form, leave
    Connect alone."""
    body = (REPO / "templates" / page).read_text()
    fetch = (
        "async function fetch() { throw new Error('fake network'); }"
        if how == "fetch_throws"
        else "async function fetch() { return { ok: false, status: 500, json: async () => ({}) }; }"
    )
    script = (
        "const els = {};\n"
        "const document = { getElementById(id) { if (!els[id]) els[id] = { id, className: '',"
        " textContent: '', style: {}, disabled: false, hidden: false }; return els[id]; } };\n"
        f"const window = {{ currentUser: {{ is_admin: {json.dumps(is_admin)} }} }};\n"
        "const console = { error() {}, log() {} };\n"
        "let appCredentialsConfigured = false;\n"
        + fetch
        + "\n"
        + _fn(body, "showAppConfigCheckFailed")
        + "\n"
        + _fn(body, "updateAppConfigUI")
        + "\n"
        + _async_fn(body, "loadAppCredentialsStatus")
        + "\n(async () => { await loadAppCredentialsStatus();\n"
        "process.stdout.write(JSON.stringify({ text: els['app-config-status-text'].textContent,"
        " form: (els['app-config-form'] || {style: {}}).style.display,"
        " connect: document.getElementById('connect-btn').disabled })); })();\n"
    )
    res = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert (
        out["text"] == f"I couldn't check whether {svc} sign-in is set up for this site just now. "
        "Reload to check again, or press Connect; if it keeps failing, tell us."
    )
    assert "isn't set up" not in out["text"]
    assert out["form"] == "none" and out["connect"] is False
