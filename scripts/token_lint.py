#!/usr/bin/env python3
"""#1172 DESIGN-FLOOR-F3 — token-discipline lint gate.

Catches hardcoded color / spacing / radius / type values in CSS that should come
from `tokens.css` custom properties (the root of craft-inconsistency drift).
"Mechanism, not vigilance": run in CI so a new hardcoded value turns the build red.

Spec (CXO design-floor F3):
  CATCH (fail): hex/rgb()/hsl() color literals; raw px for spacing not from
    --space-*; border-radius literals not from --border-radius-*; font-size/
    font-weight/line-height literals not from the type scale.
  ALLOW: tokens.css itself; 0; 1px/2px hairlines; %/vh/vw/em relative units;
    unitless line-height; a line carrying a `/* token-lint-allow */` comment.

Start = grep-grade Python (no node dep); the durable upgrade is
stylelint-declaration-strict-value (tracked on #1172). Usage:
    python scripts/token_lint.py [PATH ...]          # default: web/static/css
    python scripts/token_lint.py --summary           # counts by category
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# --- patterns ---------------------------------------------------------------
_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
_FUNC_COLOR = re.compile(r"\b(?:rgb|rgba|hsl|hsla)\s*\(")
# property: value  (value terminated by ; or }) — requires a real declaration,
# so selectors / pseudo-classes (`a:hover {`) don't false-match.
_DECL = re.compile(r"(--[\w-]+|[a-zA-Z-]+)\s*:\s*([^;{}]+?)\s*(?=[;}])")
_COMMENT = re.compile(r"/\*.*?\*/")
# a length literal with an absolute-ish unit (not preceded by a word/dot char)
_LEN = re.compile(r"(?<![\w.])(\d*\.?\d+)(px|pt|em|rem)\b")
_NUMERIC_WEIGHT = re.compile(r"^\d{3}$")

SPACING_PROPS = {
    "margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
    "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
    "gap", "row-gap", "column-gap", "top", "right", "bottom", "left",
    "inset", "inset-block", "inset-inline",
}
RADIUS_PROPS = {
    "border-radius", "border-top-left-radius", "border-top-right-radius",
    "border-bottom-left-radius", "border-bottom-right-radius",
    "border-start-start-radius", "border-start-end-radius",
    "border-end-start-radius", "border-end-end-radius",
}
TYPE_PROPS = {"font-size", "font-weight", "line-height"}
TYPE_KEYWORDS = {"normal", "bold", "bolder", "lighter", "inherit", "initial", "unset", "revert"}

ALLOW_COMMENT = "token-lint-allow"


@dataclass(frozen=True)
class Violation:
    line_no: int
    category: str  # color | spacing | radius | type
    snippet: str


def find_violations(css_text: str, filename: Optional[str] = None) -> List[Violation]:
    """Return the token-discipline violations in one stylesheet's text."""
    out: List[Violation] = []
    for i, raw in enumerate(css_text.splitlines(), start=1):
        if ALLOW_COMMENT in raw:
            continue
        line = _COMMENT.sub("", raw)
        for m in _DECL.finditer(line):
            prop = m.group(1).strip().lower()
            value = m.group(2).strip()
            val_l = value.lower()
            has_var = "var(" in val_l

            # Color literals — any property (color is color).
            if _HEX.search(value) or _FUNC_COLOR.search(val_l):
                out.append(Violation(i, "color", f"{prop}: {value}"))

            if has_var:
                continue  # token-driven for the remaining (property-specific) rules

            # border-radius — one scale, via --border-radius-*.
            if prop in RADIUS_PROPS and _LEN.search(value):
                out.append(Violation(i, "radius", f"{prop}: {value}"))

            # spacing — raw px (not 0/1px/2px) not from --space-*.
            if prop in SPACING_PROPS:
                for lm in _LEN.finditer(value):
                    num, unit = lm.group(1), lm.group(2)
                    if unit == "px" and num not in ("1", "2") and float(num) != 0:
                        out.append(Violation(i, "spacing", f"{prop}: {value}"))
                        break

            # type scale — font-size/weight/line-height literals.
            if prop in TYPE_PROPS and val_l not in TYPE_KEYWORDS:
                if prop == "font-weight":
                    if _NUMERIC_WEIGHT.match(val_l):
                        out.append(Violation(i, "type", f"{prop}: {value}"))
                else:  # font-size / line-height — flag only unit-bearing literals
                    if _LEN.search(value):
                        out.append(Violation(i, "type", f"{prop}: {value}"))
    return out


def lint_paths(paths: List[Path]) -> List[tuple]:
    results = []
    for p in paths:
        if p.name == "tokens.css":
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for v in find_violations(text, str(p)):
            results.append((p, v))
    return results


def _gather(args: List[str]) -> List[Path]:
    targets = [a for a in args if not a.startswith("-")]
    roots = [Path(t) for t in targets] if targets else [Path("web/static/css")]
    files: List[Path] = []
    for r in roots:
        if r.is_dir():
            files.extend(sorted(r.rglob("*.css")))
        elif r.suffix == ".css":
            files.append(r)
    return files


def main(argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    summary = "--summary" in argv
    files = _gather(argv)
    results = lint_paths(files)

    if summary:
        by_cat: dict = {}
        for _, v in results:
            by_cat[v.category] = by_cat.get(v.category, 0) + 1
        print(f"token-lint: {len(results)} violation(s) across {len(files)} file(s)")
        for cat in sorted(by_cat):
            print(f"  {cat:8} {by_cat[cat]}")
    else:
        for p, v in results:
            print(f"{p}:{v.line_no}: [{v.category}] {v.snippet}")
        if results:
            print(f"\ntoken-lint: {len(results)} violation(s). "
                  f"Use tokens from tokens.css, or add /* {ALLOW_COMMENT} */ for a documented exception.")

    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())
