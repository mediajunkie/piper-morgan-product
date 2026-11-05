"""#2287 (CXO 2026-11-05, from Web's window): the GitHub Disconnect dialog says Piper
removes its access at GitHub only when there is an OAuth grant to revoke (connected or
stale); a PAT-only account gets the shorter form. After a Disconnect the page never keeps
a "Connected" line: the Connect group is put back before the status refresh.

The page's own JavaScript runs under node with stubbed browser objects."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
PAGE = (ROOT / "templates/settings_github.html").read_text()
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")

OAUTH_LINE = (
    "Piper will stop reading your GitHub and remove its access from your GitHub account. "
    "You can connect again anytime."
)
PAT_LINE = "Piper will stop reading your GitHub. You can connect again anytime."
ORIGINAL_GROUP = "<button id='oauth-connect-btn'>Connect with GitHub</button>"


def _block(start: str, end: str) -> str:
    i = PAGE.index(start)
    return PAGE[i : PAGE.index(end, i)]


HARNESS = r"""
const els = {};
function el(id) {
  if (!els[id]) els[id] = { id, innerHTML: '', textContent: '', className: '', disabled: false };
  return els[id];
}
el('oauth-connect-group').innerHTML = ORIGINAL;
const document = { getElementById: (id) => el(id) };
let dialogMessage = null;
const Dialog = { confirm: async (o) => { dialogMessage = o.message; return true; } };
const Toast = { show: () => {} };
let groupAtRefresh = null;
function loadGitHubStatus() { groupAtRefresh = el('oauth-connect-group').innerHTML; }
function parseApiDetail(d, f) { return f; }
async function fetch(url) {
  if (url.endsWith('/oauth-status')) return { ok: true, json: async () => STATUS };
  return { ok: true, json: async () => ({ success: true }) };
}
"""


def _run(status: dict) -> dict:
    js = (
        f"const ORIGINAL = {json.dumps(ORIGINAL_GROUP)};\nconst STATUS = {json.dumps(status)};\n"
        + HARNESS
        + _block("      // #2287 (CXO 2026-11-05)", "      async function saveGitHubToken")
        + _block("      const DISCONNECT_LINE_OAUTH", "      // Repository Selection Functions")
        + """
(async () => {
  await checkGitHubOAuthStatus();
  const shownBefore = el('oauth-connect-group').innerHTML;
  await disconnectGitHub();
  process.stdout.write(JSON.stringify({ dialogMessage, shownBefore, groupAtRefresh }));
})();
"""
    )
    out = subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


@needs_node
def test_a_connected_grant_gets_the_revoke_sentence():
    assert _run({"connected": True, "stale": False})["dialogMessage"] == OAUTH_LINE


@needs_node
def test_a_stale_grant_gets_the_revoke_sentence():
    assert _run({"connected": False, "stale": True})["dialogMessage"] == OAUTH_LINE


@needs_node
def test_a_pat_only_account_gets_the_short_form():
    out = _run({"connected": False, "stale": False})
    assert out["dialogMessage"] == PAT_LINE
    assert "remove its access" not in out["dialogMessage"]


@needs_node
def test_after_disconnect_no_connected_line_is_left():
    out = _run({"connected": True, "stale": False})
    assert "Connected with GitHub" in out["shownBefore"]
    assert out["groupAtRefresh"] == ORIGINAL_GROUP


def test_the_old_dialog_line_is_gone():
    assert "I'll disconnect your GitHub account" not in PAGE
