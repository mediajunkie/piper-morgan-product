"""#2366 (CXO's ruling, 2026-11-13): the keys page doesn't offer what the build can't serve.

No reply can be served on a Gemini key (`LLMClient._gemini_complete` always refuses,
#1819), so the "Add or replace a key" select offers Anthropic and OpenAI only. A Gemini
key stored earlier stays listed and removable: a grey "not used yet" badge replaces
validated/unvalidated (which would read as "this works"), and one line under the table
says so, shown only when such a row exists.

Layers: the source pins always run. The behaviour test runs the page's own script in
Node against a small DOM stand-in and skips where Node is absent; it is not a browser
render (CXO's served check is the rendered read).
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
TEMPLATE = ROOT / "templates/settings_llm_keys.html"

NOTE = (
    "Piper doesn't use Google (Gemini) keys yet, so this one isn't doing anything. "
    "It stays saved until you remove it. Anthropic and OpenAI keys work."
)


def _src() -> str:
    return TEMPLATE.read_text()


def test_the_select_offers_anthropic_and_openai_only():
    select = re.search(r'<select id="llm-provider".*?</select>', _src(), re.S).group(0)
    assert re.findall(r'<option value="([^"]+)"', select) == ["anthropic", "openai"]
    assert "emini" not in select


def test_the_note_carries_cxos_words_and_starts_hidden():
    src = _src()
    assert src.count(NOTE) == 1
    tag = re.search(r'<p [^>]*id="llm-keys-unused-note"[^>]*>', src).group(0)
    assert " hidden" in tag


def test_copy_rules_hold():
    """CXO's copy check: no "alpha", no issue numbers, no internals in what a person reads."""
    visible = re.sub(r"<script>.*?</script>", "", _src(), flags=re.S)
    visible = re.sub(r"\{#.*?#\}", "", visible, flags=re.S)
    assert NOTE in visible
    assert "per-request" not in visible
    assert not re.search(r"#\d{3,}", NOTE)
    assert "alpha" not in NOTE.lower()


def test_a_stored_gemini_row_keeps_its_name_and_its_remove_button():
    src = _src()
    line = next(ln for ln in src.splitlines() if "const PROVIDER_NAMES" in ln)
    assert 'gemini: "Google Gemini"' in line
    assert 'data-del="' in src


_HARNESS = r"""
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const keys = JSON.parse(process.argv[3]);
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
function el() {
  return { innerHTML: "", textContent: "", className: "", hidden: true, value: "",
           disabled: false, addEventListener() {} };
}
const els = {};
const document = {
  getElementById(id) { return (els[id] = els[id] || el()); },
  createElement() {
    const d = { _t: "" };
    Object.defineProperty(d, "textContent", { set(v) { d._t = String(v); }, get() { return d._t; } });
    Object.defineProperty(d, "innerHTML", { get() {
      return d._t.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    } });
    return d;
  },
};
const fetch = async () => ({ ok: true, json: async () => keys });
const Dialog = { confirm: async () => false };
new Function("document", "fetch", "Dialog", script)(document, fetch, Dialog);
setTimeout(() => {
  console.log(JSON.stringify({
    rows: els["llm-keys-tbody"].innerHTML,
    noteHidden: els["llm-keys-unused-note"].hidden,
  }));
}, 50);
"""


def _run_page_script(tmp_path, keys):
    node = shutil.which("node")
    if node is None:
        pytest.skip("node is not installed; the source pins above still ran")
    harness = tmp_path / "harness.js"
    harness.write_text(_HARNESS)
    out = subprocess.run(
        [node, str(harness), str(TEMPLATE), json.dumps(keys)],
        capture_output=True,
        text=True,
        timeout=30,
        check=True,
    )
    return json.loads(out.stdout.strip().splitlines()[-1])


def test_a_stored_gemini_key_reads_not_used_yet_and_shows_the_note(tmp_path):
    result = _run_page_script(
        tmp_path,
        [
            {"provider": "gemini", "is_validated": True, "created_at": "2026-10-01T00:00:00Z"},
            {"provider": "openai", "is_validated": True, "created_at": "2026-10-02T00:00:00Z"},
        ],
    )
    gemini_row, openai_row = result["rows"].split("</tr>")[:2]
    assert "Google Gemini" in gemini_row
    assert '<span class="llmkeys-badge unused">not used yet</span>' in gemini_row
    assert "validated" not in gemini_row  # neither "validated" nor "unvalidated"
    assert 'data-del="gemini"' in gemini_row and ">Remove<" in gemini_row
    assert '<span class="llmkeys-badge ok">validated</span>' in openai_row
    assert result["noteHidden"] is False


def test_without_a_gemini_key_the_note_stays_hidden(tmp_path):
    result = _run_page_script(
        tmp_path,
        [{"provider": "anthropic", "is_validated": False, "created_at": None}],
    )
    assert '<span class="llmkeys-badge warn">unvalidated</span>' in result["rows"]
    assert "not used yet" not in result["rows"]
    assert result["noteHidden"] is True


def test_with_no_keys_the_note_stays_hidden(tmp_path):
    result = _run_page_script(tmp_path, [])
    assert "No keys stored yet." in result["rows"]
    assert result["noteHidden"] is True


def test_the_save_line_names_the_provider_as_the_table_does():
    """CXO 2026-11-13: "Key saved for Anthropic.", not "Key saved for anthropic."."""
    src = _src()
    assert "const savedName = PROVIDER_NAMES[provider] || provider;" in src
    assert 'setStatus("Key saved for " + savedName + ".", true);' in src
    assert '"Key saved for " + provider' not in src
    assert '"Saved, but " + provider' not in src
