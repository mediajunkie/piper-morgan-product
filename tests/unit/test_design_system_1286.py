"""#1286 D2 — design-system foundation (Slice 1): required tokens + baseline + grid tokenization.

Slice 1 is the token foundation per the CXO spec (design-spec-1286-d2-design-system-2026-06-20.md):
the 9 new tokens, the 24px body baseline applied via token (not raw px → token_lint-clean), and
the shell grid tokenized (rail/radar widths from tokens, not raw 180px/320px). No behavioral
change at desktop. The responsive/mobile-nav stack is Slice 2.
"""
from pathlib import Path

_CSS = Path(__file__).resolve().parents[2] / "web" / "static" / "css"
_TOKENS = (_CSS / "tokens.css").read_text()
_APP_SHELL = (_CSS / "app-shell.css").read_text()

REQUIRED_TOKENS = [
    "--grid-rail-width:",
    "--grid-radar-width:",
    "--baseline-unit:",
    "--baseline-rhythm:",
    "--space-2xs:",
    "--border-radius-pill:",
    "--breakpoint-mobile:",
    "--breakpoint-tablet:",
    "--breakpoint-desktop:",
]


def test_required_d2_tokens_defined():
    missing = [t for t in REQUIRED_TOKENS if t not in _TOKENS]
    assert not missing, f"#1286 D2 tokens missing from tokens.css: {missing}"


def test_space_2xs_is_6px():
    assert "--space-2xs: 6px" in _TOKENS  # micro-spacing for dense entity surfaces


def test_baseline_rhythm_is_24px():
    assert "--baseline-rhythm: 24px" in _TOKENS  # 3 × 8px grid


def test_border_radius_pill_is_999px():
    assert "--border-radius-pill: 999px" in _TOKENS


def test_breakpoints_documented():
    assert "--breakpoint-tablet: 768px" in _TOKENS
    assert "--breakpoint-desktop: 1024px" in _TOKENS


def test_body_snaps_to_24px_baseline_via_token():
    # body line-height comes from the token (24px), not a raw px (which token_lint forbids).
    assert "var(--baseline-rhythm)" in _APP_SHELL


def test_shell_grid_widths_are_tokenized():
    # rail/radar widths come from tokens, not raw 180px/320px (drift-proof + lint-clean).
    assert "var(--grid-rail-width)" in _APP_SHELL
    assert "var(--grid-radar-width)" in _APP_SHELL


def test_shell_grid_no_longer_hardcodes_rail_radar_px():
    # the raw 180px / 320px column widths are gone (replaced by tokens).
    assert "180px 1fr" not in _APP_SHELL
    assert "1fr 320px" not in _APP_SHELL
