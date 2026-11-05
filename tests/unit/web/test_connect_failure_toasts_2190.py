"""#2190 (CXO 2026-11-05, carried from #2285): a failed connect on the Integrations page says
a sentence and never prints the query value. A decline (access_denied, the OAuth 2.0 code)
gets its own sentence; everything else gets the generic one."""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
PAGE = (ROOT / "templates/integrations.html").read_text()
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not on PATH")


def _line(name: str, code: str) -> str:
    start = PAGE.index("function connectFailedLine(name, code) {")
    end = PAGE.index("\n  }\n", start) + 4
    js = PAGE[start:end] + f"\nprocess.stdout.write(connectFailedLine({name!r}, {code!r}));\n"
    return subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout


@needs_node
@pytest.mark.parametrize("name", ["GitHub", "Calendar", "Slack"])
def test_a_decline_gets_its_own_sentence(name):
    assert _line(name, "access_denied") == (
        f"{name} isn't connected, because you didn't approve access. Press Connect to try again."
    )


@needs_node
@pytest.mark.parametrize("code", ["callback_failed", "invalid_state", "missing_params", "x<y"])
def test_everything_else_gets_the_generic_sentence_and_never_the_code(code):
    out = _line("Slack", code)
    assert out == "Slack didn't connect. Press Connect to try again."
    assert code not in out


def test_no_toast_prints_a_query_value():
    assert "Failed to connect: ${" not in PAGE
    for c in ("slack", "calendar", "github"):
        assert (
            f"connectFailedLine('{c.capitalize() if c != 'github' else 'GitHub'}', params.get('{c}_error'))"
            in PAGE
        )


def test_the_calendar_scope_toasts_keep_their_own_words():
    assert "Google is connected, but you didn't allow calendar access" in PAGE
    assert "I couldn't confirm what Google allowed" in PAGE
    assert PAGE.index("calendar_error') === 'scope_missing'") < PAGE.index(
        "connectFailedLine('Calendar'"
    )


def test_the_setup_wizard_never_prints_a_code_either():
    js = (ROOT / "web/static/js/setup.js").read_text()
    for fn in ("getSlackErrorMessage", "getCalendarErrorMessage"):
        body = js[js.index(f"function {fn}(error)") :]
        body = body[: body.index("\n    }\n")]
        assert re.search(r"return messages\[error\] \|\| '[^']+'", body), fn
