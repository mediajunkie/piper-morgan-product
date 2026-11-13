#!/usr/bin/env python3
"""Fail when a reader-facing page tells someone to put a secret on a command line.

The rule (Exec 01M796NKZZ and 01M797MV42, 2026-11-12, from xian's ruling that local running
is a supported path): no page a user, tester or developer follows tells them to put a key,
token or secret in a shell ``export`` line with a value, or in the keychain with
``security add-generic-password ... -w <value>``. Either one leaves the secret in shell
history, and the second also writes it to the keychain. The one supported way in is a
hidden prompt: ``python scripts/local_key_setup.py`` for provider keys, or ``read -rs NAME``
in a shell (``canonical-ops-recipes.md`` section 10, rule 1).

What is a site (in a tracked Markdown file outside the internal paths below):
- ``export NAME=VALUE`` where NAME contains KEY, TOKEN, SECRET or PASSWORD, and VALUE is
  non-empty and not a shell expansion (``$...``, ``"$..."``). A placeholder value counts:
  the reader replaces it with the real secret, on the same command line.
- ``security add-generic-password`` with ``-w`` followed by a value. A bare ``-w`` at the
  end of the line makes macOS prompt, and that's allowed.

Not scanned: ``docs/internal/``, ``dev/``, ``mailboxes/``, ``archive`` folders and the
omnibus logs. They record what happened, and they aren't instructions to a reader.

Ratchet: pre-existing sites live in a baseline file, keyed on path and the line's text, not
its line number, so unrelated edits don't churn it. A new site fails. The baseline only
shrinks.

Usage:
    python scripts/key_in_docs_lint.py                       # list every site, exit 1 if any
    python scripts/key_in_docs_lint.py --baseline FILE       # fail only on sites not in FILE
    python scripts/key_in_docs_lint.py --write-baseline FILE

Concept: docs/internal/operations/canonical-ops-recipes.md (section 10)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Set, Tuple

ROOT = Path(__file__).resolve().parent.parent

EXCLUDED_PREFIXES = ("docs/internal/", "dev/", "mailboxes/")
EXCLUDED_PARTS = ("/archive/", "archive/", "omnibus")

_SECRET_NAME = r"[A-Za-z_][A-Za-z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD)[A-Za-z0-9_]*"
EXPORT_WITH_VALUE = re.compile(
    r"\bexport\s+(" + _SECRET_NAME + r")=(?![\"']?\$)(?![\"']?\s*$)(\S+)", re.IGNORECASE
)
KEYCHAIN_WITH_VALUE = re.compile(r"\bsecurity\s+add-generic-password\b.*\s-w\s+(?!-)\S+")

Site = Tuple[str, int, str]


def excluded(path: str) -> bool:
    if path.startswith(EXCLUDED_PREFIXES):
        return True
    return any(part in path for part in EXCLUDED_PARTS)


def tracked_markdown(root: Path) -> List[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.md"], cwd=root, capture_output=True, text=True, check=True
    ).stdout
    return [p for p in out.splitlines() if p and not excluded(p)]


def scan_text(path: str, text: str) -> List[Site]:
    sites: List[Site] = []
    for number, line in enumerate(text.splitlines(), 1):
        if EXPORT_WITH_VALUE.search(line) or KEYCHAIN_WITH_VALUE.search(line):
            sites.append((path, number, line.strip()))
    return sites


def scan(root: Path, paths: Iterable[str]) -> List[Site]:
    sites: List[Site] = []
    for path in paths:
        try:
            text = (root / path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        sites.extend(scan_text(path, text))
    return sites


def key(site: Site) -> str:
    path, _, text = site
    return f"{path}\t{text}"


def read_baseline(path: Path) -> Set[str]:
    if not path.exists():
        return set()
    return {line for line in path.read_text().splitlines() if line and not line.startswith("#")}


def main(argv: List[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--baseline", type=Path)
    p.add_argument("--write-baseline", type=Path)
    ns = p.parse_args(argv)

    sites = scan(ROOT, tracked_markdown(ROOT))

    if ns.write_baseline:
        body = "".join(f"{key(s)}\n" for s in sites)
        header = "# key_in_docs_lint baseline: path<TAB>line text. Only ever shrinks.\n"
        ns.write_baseline.write_text(header + body)
        print(f"key-in-docs: wrote {len(sites)} site(s) to {ns.write_baseline}")
        return 0

    allowed = read_baseline(ns.baseline) if ns.baseline else set()
    new = [s for s in sites if key(s) not in allowed]
    stale = len(allowed - {key(s) for s in sites})
    for path, number, text in new:
        print(f"{path}:{number}: secret on a command line: {text}")
    print(
        f"key-in-docs: {len(sites)} site(s) in reader-facing Markdown, "
        f"{len(sites) - len(new)} baselined, {len(new)} new"
        + (f"; {stale} baseline line(s) no longer present, remove them" if stale else "")
    )
    if new:
        print(
            "Use a hidden prompt instead: `python scripts/local_key_setup.py` for a provider "
            "key, or `read -rs NAME && export NAME` in a shell (canonical-ops-recipes.md "
            "section 10)."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
