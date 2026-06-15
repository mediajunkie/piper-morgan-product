"""#1172 DESIGN-FLOOR-F3 — token-discipline lint gate.

Tests the linter that catches hardcoded color/spacing/radius/type values in CSS
(everything should come from tokens.css custom properties). The grep/stylelint
spec (CXO design-floor F3) defines the catch/allow rules these tests encode.
"""
from __future__ import annotations

from collections import Counter

from scripts.token_lint import find_violations, new_against_baseline


def _cats(text):
    return sorted({v.category for v in find_violations(text)})


# --- Color literals (catch) -------------------------------------------------

def test_hex_color_is_violation():
    assert "color" in _cats("a { color: #ff0000; }")


def test_rgb_and_hsl_are_violations():
    assert "color" in _cats("a { color: rgb(1,2,3); }")
    assert "color" in _cats("a { background: hsl(0, 50%, 50%); }")


def test_color_via_token_is_clean():
    assert find_violations("a { color: var(--color-text); }") == []


def test_hex_inside_mixed_value_is_caught():
    # `1px solid #ccc` — the hairline px is allowed, but the hex is flagged.
    cats = _cats("a { border: 1px solid #ccc; }")
    assert "color" in cats


def test_var_fallback_hex_is_allowed():
    # token-primary graceful degradation — the token is the source of truth.
    # (Interim default pending CXO #1172 ruling.)
    assert find_violations("a { color: var(--color-text, #fff); }") == []
    assert find_violations("a { color: var(--c, rgb(0,0,0)); }") == []


def test_bare_hex_alongside_a_var_is_still_caught():
    # A var() elsewhere doesn't excuse a bare literal in the same value.
    assert "color" in _cats("a { background: var(--a, #fff), #000; }")


# --- border-radius (catch; one scale) ---------------------------------------

def test_radius_literal_is_violation():
    assert "radius" in _cats("a { border-radius: 4px; }")


def test_radius_via_token_is_clean():
    assert find_violations("a { border-radius: var(--border-radius-sm); }") == []


def test_radius_percent_and_zero_are_clean():
    assert find_violations("a { border-radius: 50%; }") == []
    assert find_violations("a { border-radius: 0; }") == []


# --- spacing px (catch) -----------------------------------------------------

def test_spacing_px_is_violation():
    assert "spacing" in _cats("a { padding: 16px; }")
    assert "spacing" in _cats("a { margin-top: 24px; }")


def test_spacing_via_token_is_clean():
    assert find_violations("a { padding: var(--space-md); }") == []


def test_hairline_and_zero_and_relative_spacing_are_clean():
    assert find_violations("a { margin: 0; }") == []
    assert find_violations("a { border-bottom-width: 1px; }") == []
    assert find_violations("a { gap: 2px; }") == []
    assert find_violations("a { width: 100%; }") == []
    assert find_violations("a { padding: 1em; }") == []


# --- type scale (catch) -----------------------------------------------------

def test_font_size_literal_is_violation():
    assert "type" in _cats("a { font-size: 14px; }")


def test_font_weight_numeric_literal_is_violation():
    assert "type" in _cats("a { font-weight: 600; }")


def test_type_via_token_or_keyword_is_clean():
    assert find_violations("a { font-size: var(--font-size-sm); }") == []
    assert find_violations("a { font-weight: normal; }") == []
    assert find_violations("a { line-height: 1.5; }") == []  # unitless allowed


def test_line_height_with_unit_is_violation():
    assert "type" in _cats("a { line-height: 20px; }")


# --- allow-list comment -----------------------------------------------------

def test_inline_allow_comment_suppresses():
    assert find_violations("a { color: #fff; /* token-lint-allow */ }") == []


# --- clean stylesheet -------------------------------------------------------

def test_baseline_ratchet_tolerates_existing_flags_new():
    baseline = Counter(["a.css|color|color: #fff", "a.css|spacing|padding: 10px"])
    # same set → nothing new
    assert new_against_baseline(Counter(baseline), baseline) == Counter()
    # one new violation added
    current = Counter(["a.css|color|color: #fff", "a.css|spacing|padding: 10px",
                       "b.css|radius|border-radius: 18px"])
    new = new_against_baseline(current, baseline)
    assert list(new.elements()) == ["b.css|radius|border-radius: 18px"]
    # a fixed violation is not "new" (ratchet only fails on additions)
    fewer = Counter(["a.css|color|color: #fff"])
    assert new_against_baseline(fewer, baseline) == Counter()


def test_fully_tokenized_block_is_clean():
    css = """
    .card {
      color: var(--color-text);
      background: var(--color-surface);
      padding: var(--space-md);
      border-radius: var(--border-radius-lg);
      font-size: var(--font-size-base);
      gap: 0;
      width: 100%;
      border: 1px solid var(--color-border);
    }
    """
    assert find_violations(css) == []
