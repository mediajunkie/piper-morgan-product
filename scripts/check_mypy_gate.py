#!/usr/bin/env python3
"""check_mypy_gate.py — the signature-drift gate (#1436 Part 2, Arch-ratified).

Runs mypy (pinned config: mypy-gate.ini — the plugins are load-bearing, see the
ini header) over services/ + web/ and enforces PER-CODE shrink-only ratchets
against scripts/ratchet_ceilings.json (`mypy_*` keys).

Coverage history:
- v1 (2026-07-17): four census-proven codes only (call-arg, arg-type,
  attr-defined, union-attr). Everything else was silently discarded — which is
  how #1469 happened: [name-defined] errors are GUARANTEED runtime NameErrors
  (the #1465 class: a live one in google_calendar_adapter returned [] on every
  recurring-events query, swallowed by a broad except), and the gate could not
  see them.
- v2 (#1436 slice, closes #1469's blindness): EVERY error code mypy emits is
  ratcheted. Each observed code needs a `mypy_<code>` ceiling (dashes →
  underscores); an error code with no ceiling FAILS the gate ("freeze one") —
  so a brand-new drift class can never ship invisibly again. name-defined's
  ceiling is 0: that class is extinct and stays extinct.

Per-code (not a single total) so shrinkage in one code can't hide regression
in another (Arch's ruling). Same semantics as tests/test_completion_ratchets.py:
count > ceiling fails (new drift may not ship); count < ceiling ALSO fails
until the ceiling is lowered in the same commit (improvements get locked in).

Exit codes: 0 = every code at ceiling · 1 = violation (message says which way).
Requires mypy importable (CI installs mypy==2.3.0 + sqlalchemy/pydantic/fastapi
pins; locally use any venv with them). --measure prints counts and exits 0.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CEILINGS_FILE = REPO_ROOT / "scripts" / "ratchet_ceilings.json"
CEILING_PREFIX = "mypy_"
_LINE = re.compile(r"error:.*\[([a-z-]+)\]\s*$")


def _key(code: str) -> str:
    """[error-code] → ratchet_ceilings.json key (call-arg → mypy_call_arg)."""
    return CEILING_PREFIX + code.replace("-", "_")


def _code(key: str) -> str:
    """Inverse of _key (best-effort: mypy codes use dashes, never underscores)."""
    return key[len(CEILING_PREFIX) :].replace("_", "-")


def run_mypy() -> Counter:
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "mypy",
            "services/",
            "web/",
            "--config-file",
            "mypy-gate.ini",
            "--no-error-summary",
            "--show-error-codes",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=900,
    )
    if proc.returncode not in (0, 1):  # 2 = usage/crash — surface it
        print(proc.stderr[-2000:], file=sys.stderr)
        raise SystemExit(f"mypy did not run cleanly (exit {proc.returncode})")
    # mypy exits 1 only when it found errors, so exit 1 + EMPTY stdout means it
    # never actually ran (e.g. `python -m mypy` with mypy not installed also
    # exits 1, error on stderr). Without this guard that state parses as
    # "zero errors" — a gate blind to its own absence.
    if proc.returncode == 1 and not proc.stdout.strip():
        print(proc.stderr[-2000:], file=sys.stderr)
        raise SystemExit("mypy produced no output on exit 1 — it did not run; refusing to report 0")
    counts: Counter = Counter()
    for line in proc.stdout.splitlines():
        m = _LINE.search(line)
        if m:
            counts[m.group(1)] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--measure", action="store_true", help="print counts, exit 0")
    args = parser.parse_args()

    counts = run_mypy()
    if args.measure:
        for code in sorted(counts):
            print(f"{_key(code)}={counts[code]}")
        return 0

    ceilings = json.loads(CEILINGS_FILE.read_text())
    mypy_ceilings = {k: v for k, v in ceilings.items() if k.startswith(CEILING_PREFIX)}

    failures = []
    # Direction 1: every OBSERVED code must have a ceiling and sit at it.
    for code in sorted(counts):
        key = _key(code)
        if key not in mypy_ceilings:
            failures.append(
                f"{key}: {counts[code]} [{code}] errors observed but NO ceiling exists — "
                f"a new drift class may not ship invisibly (#1469). Fix the errors or "
                f"freeze an explicitly-reviewed ceiling in {CEILINGS_FILE.name}."
            )
    # Direction 2: every RATCHETED code must sit exactly at its ceiling
    # (this also covers observed-with-ceiling codes; zero-count codes like
    # name-defined are asserted extinct by their ceiling of 0).
    for key, ceiling in sorted(mypy_ceilings.items()):
        code = _code(key)
        n = counts.get(code, 0)
        if n > ceiling:
            failures.append(
                f"{key}: {n} > ceiling {ceiling} — new [{code}] drift may not ship "
                f"(#1436 gate). Fix the call site; the masks (#1423) don't save you here."
            )
        elif n < ceiling:
            failures.append(
                f"{key}: {n} < ceiling {ceiling} — drift was removed; lower the "
                f"ceiling to {n} in this same commit to lock it in."
            )
    if failures:
        print("\n".join(failures))
        return 1
    print(
        f"mypy gate: all {len(mypy_ceilings)} ratcheted codes at ceiling "
        f"(total={sum(counts.values())}; "
        f"{', '.join(f'{c}={counts[c]}' for c in sorted(counts) if counts[c])})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
