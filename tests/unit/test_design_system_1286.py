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
    "--space-dense:",
    "--border-radius-pill:",
    "--breakpoint-mobile:",
    "--breakpoint-tablet:",
    "--breakpoint-desktop:",
]


def test_required_d2_tokens_defined():
    missing = [t for t in REQUIRED_TOKENS if t not in _TOKENS]
    assert not missing, f"#1286 D2 tokens missing from tokens.css: {missing}"


def test_space_dense_is_6px_and_2xs_renamed_away():
    assert (
        "--space-dense: 6px" in _TOKENS
    )  # dense-surface micro-spacing (renamed from --space-2xs per CXO)
    assert (
        "--space-2xs:" not in _TOKENS
    )  # the old token definition is gone (a comment mentioning the rename would be fine)


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


# ── Slice 2 (#1286, CXO-ruled 2026-06-21): radar tiling — pill chip + tokenized dense spacing ──
_HISTORY_SIDEBAR = (
    Path(__file__).resolve().parents[2] / "templates" / "components" / "history_sidebar.html"
).read_text()


def test_radar_etype_is_a_pill_chip():
    # CXO option (c): the entity-type label is a pill chip (badge), not plain text.
    assert ".radar-etype" in _HISTORY_SIDEBAR
    idx = _HISTORY_SIDEBAR.index(".radar-etype")
    assert "--border-radius-pill" in _HISTORY_SIDEBAR[idx : idx + 260]


def test_radar_card_dense_margins_use_token():
    # CXO: tokenize the raw 6px margins in .radar-card via --space-dense (no-visual-change cleanup).
    assert _HISTORY_SIDEBAR.count("var(--space-dense") >= 2  # radar-card-meta + radar-card-prov
