"""#1489 — history reload renders only user bubbles: template-layer regression pins.

ROOT CAUSE (2026-08-07): an unescaped apostrophe in a single-quoted JS string
(`'It'll stop appearing…'`, delete-dialog copy shipped by #1482 in ce31b09d6)
was a SyntaxError that killed home.html's ENTIRE inline conversation script at
parse time — loadConversations / switchConversation / initSidebar all became
undefined, so the server-side `/turns` reload never ran. The only thing left
rendering on a return visit was chat.js's localStorage restore, which persists
USER messages only (live bot replies are appended empty and filled by
handleDirectResponse, so they are never saved client-side) → every assistant
reply vanished from the reloaded view while live sessions looked fine.

Layer note (#1487): the history renderer lives INSIDE the Jinja template, so the
jest/jsdom harness (tests/frontend/, standalone web/static/js/ files only)
structurally cannot execute it. Per the #1489 AC these pins therefore sit at the
API-contract layer (tests/unit/web/api/routes/test_conversations.py, issue #583
suite, already green) and the template-content layer (this file). If the inline
script is ever extracted per #1487, move the render pins into the jest harness.

The parse pin below is deliberately broader than the one bad string: ANY
unescaped quote inside any inline-script string literal of home.html re-creates
this exact failure class (one typo → whole conversation UI dead), and no other
gate catches it — the frontend workflow doesn't watch templates/, and pytest
content assertions match substrings whether or not the script parses.
"""

import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

TEMPLATES = Path(__file__).resolve().parents[3] / "templates"

# Keyword-operators that may legitimately follow a string literal on the same
# line ("'x' in obj", "'x' instanceof C" — the latter is nonsense but harmless).
_ALLOWED_AFTER_STRING = {"in", "instanceof"}

_IDENT_START = re.compile(r"[A-Za-z_$]")
_IDENT = re.compile(r"[A-Za-z0-9_$]*")


def _home_html() -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES)), autoescape=True)
    return env.get_template("home.html").render(trust_stage=1, show_radar=True, user_name="tester")


def _inline_scripts(html: str) -> list[str]:
    """All inline <script> bodies (no src=) from rendered HTML."""
    out = []
    for m in re.finditer(r"<script\b([^>]*)>(.*?)</script>", html, re.DOTALL | re.IGNORECASE):
        attrs, body = m.group(1), m.group(2)
        if "src=" in attrs:
            continue
        if body.strip():
            out.append(body)
    return out


def _string_breakages(src: str) -> list[str]:
    """Lex a JS source just enough to catch the #1489 failure class.

    Reports two things, both of which are SyntaxErrors in real JS:
      * a string literal immediately followed (same line, only blanks between)
        by an identifier that is not a keyword-operator — the signature of an
        unescaped quote chopping a string in half ('It'll …' → STRING `'It'`
        then identifier `ll`);
      * a string literal never terminated before EOF.

    Handles //-comments, /* */-comments, escape sequences, and template
    literals (including ${…} interpolation holes). Regex literals are not
    modeled; they are quote-free in this template and flagged strings are
    reported with context so a false positive would be obvious and fixable.
    """
    problems = []
    i, n = 0, len(src)
    line = 1

    def scan_after_string(j: int, opener_pos: int) -> None:
        """After a closed string at src[j:], flag same-line trailing identifier."""
        while j < n and src[j] in " \t":
            j += 1
        if j < n and _IDENT_START.match(src[j]):
            word = src[j] + _IDENT.match(src, j + 1).group(0)
            if word not in _ALLOWED_AFTER_STRING:
                snippet = src[max(0, opener_pos - 40) : j + len(word)]
                problems.append(
                    f"line {line}: string literal followed by identifier "
                    f"{word!r} — unescaped quote inside the string? …{snippet}"
                )

    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            i += 1
        elif c == "/" and i + 1 < n and src[i + 1] == "/":
            while i < n and src[i] != "\n":
                i += 1
        elif c == "/" and i + 1 < n and src[i + 1] == "*":
            i += 2
            while i + 1 < n and not (src[i] == "*" and src[i + 1] == "/"):
                if src[i] == "\n":
                    line += 1
                i += 1
            i += 2
        elif c in "'\"":
            opener, start = c, i
            i += 1
            closed = False
            while i < n:
                if src[i] == "\\":
                    i += 2
                    continue
                if src[i] == "\n":  # plain strings cannot span raw newlines
                    break
                if src[i] == opener:
                    closed = True
                    i += 1
                    break
                i += 1
            if not closed:
                problems.append(
                    f"line {line}: unterminated {opener} string starting at "
                    f"…{src[start:start + 60]!r}"
                )
            else:
                scan_after_string(i, start)
        elif c == "`":
            start = i
            i += 1
            depth = 0  # ${…} nesting inside the template literal
            closed = False
            while i < n:
                if src[i] == "\\":
                    i += 2
                    continue
                if src[i] == "\n":
                    line += 1
                    i += 1
                    continue
                if src[i] == "$" and i + 1 < n and src[i + 1] == "{":
                    depth += 1
                    i += 2
                    continue
                if depth and src[i] == "}":
                    depth -= 1
                    i += 1
                    continue
                if src[i] == "`" and depth == 0:
                    closed = True
                    i += 1
                    break
                i += 1
            if not closed:
                problems.append(
                    f"line {line}: unterminated template literal starting at "
                    f"…{src[start:start + 60]!r}"
                )
            else:
                scan_after_string(i, start)
        else:
            i += 1
    return problems


def test_home_inline_scripts_have_no_broken_string_literals():
    """The #1489 root cause, pinned: every inline-script string literal in
    home.html must lex cleanly. One unescaped apostrophe here disables the
    entire conversation-history reload path (only user bubbles survive)."""
    html = _home_html()
    scripts = _inline_scripts(html)
    assert scripts, "home.html should contain inline scripts (extraction broke?)"
    problems = [p for s in scripts for p in _string_breakages(s)]
    assert not problems, (
        "Inline <script> string breakage in home.html — this is the #1489 "
        "regression class (SyntaxError kills the whole conversation script; "
        "history reload renders user bubbles only):\n" + "\n".join(problems)
    )


# test_delete_dialog_copy_apostrophe_is_escaped was removed in #1522 step 1
# (2026-08-08): the specific #1482 string it pinned lived in home.html's dead
# legacy sidebar renderer, which is now excised (the copy had shipped dark into
# the hidden twin — #1516). The regression CLASS stays covered by the broader
# parse pin above (test_home_inline_scripts_have_no_broken_string_literals);
# the #1482 copy itself stays pinned on its live surfaces by
# test_delete_copy_honesty_1482.py.


def test_history_reload_renders_both_sides_of_each_turn():
    """Template-content pin for the render contract (#1487: the renderer is
    template-embedded, so this cannot be a jest test yet): the turns loop in
    switchConversation must append BOTH the user message and the assistant
    response for every turn."""
    html = _home_html()
    assert "ChatWidget.appendMessage(turn.user_message, true" in html
    assert "ChatWidget.appendMessage(turn.assistant_response, false" in html
    # And the fetch it depends on must still target the pinned turns API.
    assert "/turns" in html and "/api/v1/conversations/" in html
