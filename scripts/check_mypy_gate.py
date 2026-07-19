#!/usr/bin/env python3
"""check_mypy_gate.py — the signature-drift gate (#1436 Part 2, Arch-ratified).

Runs mypy (pinned config: mypy-gate.ini — the plugins are load-bearing, see the
ini header) over services/ + web/, filters to the four census-proven defect
codes, and enforces PER-CODE shrink-only ratchets against
scripts/ratchet_ceilings.json:

    mypy_call_arg · mypy_arg_type · mypy_attr_defined · mypy_union_attr

Per-code (not a single total) so shrinkage in one code can't hide regression in
another (Arch's ruling). Same semantics as tests/test_completion_ratchets.py:
count > ceiling fails (new drift may not ship); count < ceiling ALSO fails
until the ceiling is lowered in the same commit (improvements get locked in).

Exit codes: 0 = all four at ceiling · 1 = violation (message says which way).
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
CODES = {
    "call-arg": "mypy_call_arg",
    "arg-type": "mypy_arg_type",
    "attr-defined": "mypy_attr_defined",
    "union-attr": "mypy_union_attr",
}
_LINE = re.compile(r"error:.*\[([a-z-]+)\]\s*$")


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
        if m and m.group(1) in CODES:
            counts[m.group(1)] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--measure", action="store_true", help="print counts, exit 0")
    args = parser.parse_args()

    counts = run_mypy()
    if args.measure:
        for code, key in CODES.items():
            print(f"{key}={counts[code]}")
        return 0

    ceilings = json.loads(CEILINGS_FILE.read_text())
    failures = []
    for code, key in CODES.items():
        ceiling = ceilings.get(key)
        if ceiling is None:
            failures.append(f"{key}: no ceiling in {CEILINGS_FILE.name} — freeze one")
            continue
        n = counts[code]
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
        "mypy gate: all four codes at ceiling "
        f"({', '.join(f'{k}={counts[c]}' for c, k in CODES.items())})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
