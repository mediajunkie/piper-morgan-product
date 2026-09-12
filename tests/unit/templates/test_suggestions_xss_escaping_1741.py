"""#1741 [SECURITY] — pattern-suggestions UI XSS (renderSuggestions/renderSuggestionCard).

web/assets/bot-message-renderer.js handleDirectResponse appends
renderSuggestions(result.suggestions) HTML to element.innerHTML.
renderSuggestionCard interpolated suggestion.pattern_id, pattern_type, and a
reasoning string (derived from pattern_data.reasoning / description /
action_params.title — plausibly user-authored content) unescaped into HTML and
into onclick JS-string context. Deliberately OUTSIDE the #1732 DOMPurify
chokepoint: this markup carries inline onclick handlers by design, and
DOMPurify would strip them. Fix is the #1578 treatment — escapeHtml/escapeAttr
per interpolation, numeric coercion for count/confidence, and user-adjacent
text never in onclick context (only the server-generated pattern id crosses,
escapeAttr'd for the HTML-attribute layer).

LAYER (named honestly): these are SOURCE pins on the shipped JS file — string/
regex ratchets that fail if a future edit reintroduces a bare interpolation in
the suggestions render path. The runtime-DOM half (hostile suggestion objects
through the real renderer into a real jsdom container, asserting inert OUTPUT)
lives in the jsdom harness: tests/frontend/unit/suggestions-xss-1741.test.js.
"""

import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
RENDERER = REPO / "web" / "assets" / "bot-message-renderer.js"


@pytest.fixture(scope="module")
def src():
    return RENDERER.read_text(encoding="utf-8")


def _fn_body(src: str, name: str) -> str:
    """Extract a top-level `function name(...) {...}` body (4-space indent style,
    closes at the first column-0 brace)."""
    m = re.search(rf"function {re.escape(name)}\(.*?\n\}}", src, re.DOTALL)
    assert m, f"{name}() not found in {RENDERER}"
    return m.group(0)


# --- the helpers exist and cover the metacharacters ----------------------------


def test_escape_helpers_exist_and_cover_the_metacharacters(src):
    body = _fn_body(src, "_escapeHtml")
    for ch, entity in [
        ("&", "&amp;"),
        ("<", "&lt;"),
        (">", "&gt;"),
        ('"', "&quot;"),
        ("'", "&#39;"),
    ]:
        assert entity in body, f"_escapeHtml() does not escape {ch!r} -> {entity}"
    assert "function _escapeAttr" in src, "_escapeAttr() (attribute-context variant) went missing"


# --- the headline holes: bare interpolations are gone --------------------------


def test_bare_pattern_id_interpolation_is_gone(src):
    """pattern_id crossed both the data-attribute and onclick boundaries bare."""
    assert "${suggestion.pattern_id}" not in src, (
        "suggestion.pattern_id is interpolated unescaped — an attribute-breakout "
        "payload in pattern data materializes live event handlers when a "
        "suggestion renders"
    )


def test_bare_reasoning_interpolation_is_gone(src):
    """reasoning derives from pattern_data.reasoning/description/action_params.title
    — plausibly user-authored (e.g. an issue title in a learned pattern)."""
    assert "${reasoning}" not in src, (
        "reasoning is interpolated unescaped — a stored payload in pattern data "
        "executes when the suggestion renders (the #1578 threat model)"
    )


def test_bare_pattern_type_interpolation_is_gone_from_returned_html(src):
    """Scoped to the returned template: ``${patternType}`` legitimately appears
    in the reasoning string-building fallback above the return (escaped later
    at the HTML boundary); bare in the HTML itself is the hole."""
    body = _fn_body(src, "renderSuggestionCard")
    template = body.split("return `", 1)[1]
    assert "${patternType}" not in template, "patternType reaches the HTML unescaped"


# --- ratchet: the card template's dynamic fields stay escaped/coerced ----------


def test_card_render_path_has_no_bare_suggestion_field_interpolation(src):
    """Sweep ratchet (the 1578 pattern): in renderSuggestionCard's RETURNED
    template (the HTML that reaches innerHTML — string-building above it is
    covered by the escape-at-interpolation pins), every ``${...}`` is an escape
    call, a numeric/app-constant local, or the pre-escaped safePatternId —
    never a bare suggestion.* field."""
    body = _fn_body(src, "renderSuggestionCard")
    parts = body.split("return `", 1)
    assert len(parts) == 2, "renderSuggestionCard no longer returns a template literal"
    template = parts[1]
    allowed = re.compile(
        r"^(_escapeHtml\(|_escapeAttr\(|safePatternId$|icon$|cardClass$|badgeClass$"
        r"|badgeText$|confidence$|usageText$|isAutoTriggered\b)"
    )
    for m in re.finditer(r"\$\{([^}]*)\}", template):
        expr = m.group(1).strip()
        assert allowed.match(expr), (
            f"renderSuggestionCard interpolates {expr!r} outside the escaped/"
            "coerced allowlist — route it through _escapeHtml/_escapeAttr or "
            "coerce it to a number first (#1741)"
        )


def test_numeric_fields_are_coerced_not_trusted(src):
    body = _fn_body(src, "renderSuggestionCard")
    assert re.search(r"Number\(suggestion\.confidence\)", body), (
        "confidence must be Number()-coerced — a hostile string otherwise "
        "reaches a style attribute"
    )
    assert re.search(
        r"Number\(suggestion\.usage_count\)", body
    ), "usage_count must be Number()-coerced — it lands in HTML text context"


# --- the onclick boundary rule --------------------------------------------------


def test_user_adjacent_text_never_in_onclick(src):
    """HTML-escaping CANNOT protect a JS string inside onclick (the parser
    decodes entities before the JS engine runs) — so the pin is absence: the
    only interpolation inside any onclick in the suggestions markup is the
    escaped server-generated id."""
    body = _fn_body(src, "renderSuggestionCard")
    for m in re.finditer(r'onclick="[^"]*?\$\{([^}]*)\}[^"]*?"', body):
        expr = m.group(1).strip()
        assert expr == "safePatternId", (
            f"onclick interpolates {expr!r} — only the escaped server-generated "
            "pattern id may cross the onclick boundary (#1578/#1741)"
        )
