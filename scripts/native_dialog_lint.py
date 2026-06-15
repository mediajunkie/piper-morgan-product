#!/usr/bin/env python3
"""F1 #1170 (Part C) — native-dialog lint gate.

Catches native browser `confirm()` / `alert()` / `prompt()` reachable in app code
(`templates/` + `web/static/js/`). The design-floor F1 "Done = no native
confirm/alert reachable" gate — native dialogs are off-brand + unstyleable;
callers must use the `Dialog` component. Mirrors the F3 token-lint
(`scripts/token_lint.py`) baseline-ratchet pattern; reuses its ratchet helper.

Usage:
    python scripts/native_dialog_lint.py [PATH ...]          # default: templates + web/static/js
    python scripts/native_dialog_lint.py --baseline FILE     # fail only on NEW calls
    python scripts/native_dialog_lint.py --write-baseline FILE
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


def new_against_baseline(current: Counter, baseline: Counter) -> Counter:
    """Signatures present more often now than in baseline — the ratchet (same as
    the F3 token-lint's): pre-existing calls tolerated, NEW ones fail CI."""
    return current - baseline  # multiset difference


# window.confirm( / window.alert( / window.prompt(  — explicit native via window
_WINDOW = re.compile(r"\bwindow\s*\.\s*(confirm|alert|prompt)\s*\(")
# bare confirm( / alert( / prompt(  — not preceded by `.` (method call) or a word char
_BARE = re.compile(r"(?<![.\w])(confirm|alert|prompt)\s*\(")
_LINE_COMMENT = re.compile(r"//.*$")
_BLOCK_COMMENT = re.compile(r"/\*.*?\*/")
ALLOW = "native-dialog-allow"
# files that DEFINE the Dialog component (their `confirm`/`show` are methods, not native calls)
_EXCLUDE_NAMES = {"dialog.js"}


@dataclass(frozen=True)
class Violation:
    line_no: int
    snippet: str


def find_native_dialogs(text: str, filename: Optional[str] = None) -> List[Violation]:
    """Native `confirm`/`alert`/`prompt` *calls* in one file's text."""
    out: List[Violation] = []
    for i, raw in enumerate(text.splitlines(), start=1):
        if ALLOW in raw:
            continue
        line = _LINE_COMMENT.sub("", _BLOCK_COMMENT.sub("", raw))
        flagged = False
        if _WINDOW.search(line):
            flagged = True
        if not flagged:
            for m in _BARE.finditer(line):
                if line[: m.start()].rstrip().endswith("function"):
                    continue  # a function/method definition, not a native call
                flagged = True
                break
        if flagged:
            out.append(Violation(i, raw.strip()[:100]))
    return out


def lint_paths(paths: List[Path]) -> List[tuple]:
    results = []
    for p in paths:
        if p.name in _EXCLUDE_NAMES:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for v in find_native_dialogs(text, str(p)):
            results.append((p, v))
    return results


def _signature(path: Path, v: Violation) -> str:
    return f"{path.as_posix()}|{v.snippet}"


def _gather(targets: List[str]) -> List[Path]:
    roots = [Path(t) for t in targets] if targets else [Path("templates"), Path("web/static/js")]
    files: List[Path] = []
    for r in roots:
        if r.is_dir():
            files.extend(sorted(r.rglob("*.html")))
            files.extend(sorted(r.rglob("*.js")))
        elif r.suffix in (".html", ".js"):
            files.append(r)
    return files


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="native-dialog lint gate (#1170 F1)")
    parser.add_argument("paths", nargs="*", help="files/dirs (default: templates + web/static/js)")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument("--baseline", metavar="FILE", help="ratchet: fail only on calls NOT in FILE")
    parser.add_argument("--write-baseline", metavar="FILE", help="snapshot current calls to FILE")
    ns = parser.parse_args(argv)

    files = _gather(ns.paths)
    results = lint_paths(files)
    current = Counter(_signature(p, v) for p, v in results)

    if ns.write_baseline:
        Path(ns.write_baseline).write_text("\n".join(sorted(current.elements())) + "\n", encoding="utf-8")
        print(f"native-dialog-lint: wrote baseline ({sum(current.values())} call(s)) to {ns.write_baseline}")
        return 0

    if ns.summary:
        print(f"native-dialog-lint: {len(results)} native dialog call(s) across {len(files)} file(s)")
        return 1 if results else 0

    if ns.baseline:
        base = Counter(ln for ln in Path(ns.baseline).read_text(encoding="utf-8").splitlines() if ln.strip())
        new = new_against_baseline(current, base)
        if new:
            print(f"native-dialog-lint: {sum(new.values())} NEW native dialog call(s) (not in baseline {ns.baseline}):")
            for sig in sorted(new.elements()):
                path, snip = sig.split("|", 1)
                print(f"  {path}: {snip}")
            print("\nUse the Dialog component (Dialog.open/confirm/alert/prompt), not native confirm()/alert()/prompt().")
            return 1
        fixed = sum((base - current).values())
        msg = f"native-dialog-lint: no new native dialogs ({sum(current.values())} baselined"
        msg += f"; {fixed} migrated — rerun --write-baseline to ratchet down)." if fixed else ")."
        print(msg)
        return 0

    for p, v in results:
        print(f"{p}:{v.line_no}: {v.snippet}")
    if results:
        print(f"\nnative-dialog-lint: {len(results)} native dialog call(s). Use the Dialog component.")
    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())
