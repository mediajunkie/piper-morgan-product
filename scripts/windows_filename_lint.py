#!/usr/bin/env python3
"""#1457 — Windows-invalid filename gate.

A path that is legal on POSIX can make the whole repo un-checkout-able on
Windows: `dev/2025/11/10/3.` (trailing dot) broke every Windows clone from
2026-03 to 2026-07, a recurrence of #353, because nothing guarded the class.
The detector that would have caught it, `windows-test.yml`, is parked
(dispatch-only since 2026-09-13), so this check runs in lint, on Linux.

Fails if any tracked path has a component that Windows refuses:
  - ends with a dot or a space
  - contains < > : " | ? * \\ or a control character
  - is a reserved device name (CON, PRN, AUX, NUL, COM1-9, LPT1-9), with or
    without an extension

Path LENGTH is #1616's gate (mailbox_filename_lint.py), not this one.
No baseline: the 2026-07-29 sweep found one instance and it was removed.

Usage: python scripts/windows_filename_lint.py [--repo PATH]
Concept: docs/operations/regression-prevention.md
"""

import argparse
import re
import subprocess
import sys

RESERVED = (
    {"CON", "PRN", "AUX", "NUL"}
    | {f"COM{i}" for i in range(1, 10)}
    | {f"LPT{i}" for i in range(1, 10)}
)
BAD_CHARS = re.compile(r'[<>:"|?*\\\x00-\x1f]')


def problem(component: str) -> str | None:
    if component.endswith((".", " ")):
        return "ends with a dot or space"
    if BAD_CHARS.search(component):
        return "contains a character Windows forbids"
    if component.split(".")[0].upper() in RESERVED:
        return "is a reserved device name"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    out = subprocess.run(
        ["git", "-C", args.repo, "ls-files", "-z"], capture_output=True, check=True
    ).stdout
    paths = [p for p in out.decode("utf-8", "surrogateescape").split("\0") if p]
    bad = []
    for p in paths:
        for comp in p.split("/"):
            why = problem(comp)
            if why:
                bad.append((p, comp, why))
                break
    print(f"windows-filename lint: {len(paths)} tracked paths checked, {len(bad)} Windows-invalid")
    for p, comp, why in bad:
        print(f"  {p!r}: component {comp!r} {why}")
    if bad:
        print("::error::#1457 these paths cannot be checked out on Windows; rename or remove them")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
