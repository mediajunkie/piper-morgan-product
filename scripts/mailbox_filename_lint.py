#!/usr/bin/env python3
"""#1616 — mailbox filename-length lint gate.

Windows' effective MAX_PATH is 260 characters, INCLUDING the clone-path
prefix (e.g. ``C:\\Users\\alexandra\\Documents\\GitHub\\piper-morgan-product\\``,
commonly 50-90 characters for a real machine). Cohort agents have written
`mailboxes/` memo filenames whose repo-relative path alone exceeds 250
characters — see e.g.
``mailboxes/xian (ceo)/inbox/CORRECTION-pa-to-arch-host-cio-comms-...md``
(258 chars). Combined with a clone prefix, that's well past 260: a Windows
user cannot `git clone` this repo at all (confirmed by the `windows-clone-test`
job in `.github/workflows/windows-test.yml`, currently red for exactly this
reason).

Per issue #1616's explicit recommendation (option 1, not option 2): this
lint caps the length of `mailboxes/` paths GOING FORWARD only. It does NOT
rename or otherwise touch existing offenders — those stay as historical
record. "Mirrors the F3 token-lint (`scripts/token_lint.py`) baseline-ratchet
pattern, same as `scripts/native_dialog_lint.py` / `scripts/principal_threading_lint.py`:
pre-existing violations are snapshotted into a baseline file and tolerated
forever; only a NEW violation (a path not already in the baseline) fails CI.

Length cap: 180 characters, measured on the full repo-relative POSIX path
(e.g. `mailboxes/cio/read/some-file.md`) — not just the basename, since the
full relative path is what actually consumes the Windows path budget once
prepended with a real clone-path prefix. Rationale for 180: 260 (Windows
MAX_PATH) minus ~80 (a realistic worst-case clone-path prefix such as
`C:\\Users\\<name>\\Documents\\GitHub\\piper-morgan-product\\`) leaves 180
with a bit of headroom. This matches issue #1616's own suggested starting
point.

Why CI, not a pre-commit hook: real mailbox writes go through
`scripts/mail-send.sh`, which builds the commit via `git commit-tree`
directly (see its own comment: "commit-tree is NOT `git commit`, so
check-branch.sh (PreToolUse on git commit) [doesn't fire]") — deliberately,
so cross-agent mail delivery isn't blocked by local hook state. A
pre-commit hook would never see the commits this lint needs to catch. CI
(`lint.yml`, triggered on push to `main` including path `mailboxes/**`) is
the one mechanism that actually observes every mailbox-touching push,
regardless of how the commit was built.

Usage:
    python scripts/mailbox_filename_lint.py                    # list violations
    python scripts/mailbox_filename_lint.py --summary          # count only
    python scripts/mailbox_filename_lint.py --baseline FILE    # fail only on NEW long paths
    python scripts/mailbox_filename_lint.py --write-baseline FILE
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from typing import List, Optional

MAILBOX_ROOT = Path("mailboxes")
MAX_PATH_LENGTH = 180


def find_violations(root: Path = MAILBOX_ROOT) -> List[str]:
    """Repo-relative POSIX paths under `mailboxes/` longer than MAX_PATH_LENGTH."""
    if not root.is_dir():
        return []
    violations = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.as_posix()
        if len(rel) > MAX_PATH_LENGTH:
            violations.append(rel)
    return violations


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="mailbox filename-length lint gate (#1616)")
    parser.add_argument("--summary", action="store_true", help="count only")
    parser.add_argument(
        "--baseline", metavar="FILE", help="ratchet: fail only on paths NOT already in FILE"
    )
    parser.add_argument(
        "--write-baseline",
        metavar="FILE",
        help="snapshot current over-length paths to FILE (grandfathers existing history)",
    )
    ns = parser.parse_args(argv)

    current = Counter(find_violations())

    if ns.write_baseline:
        Path(ns.write_baseline).write_text(
            "\n".join(sorted(current.elements())) + "\n", encoding="utf-8"
        )
        print(
            f"mailbox-filename-lint: wrote baseline ({sum(current.values())} "
            f"path(s) over {MAX_PATH_LENGTH} chars) to {ns.write_baseline}"
        )
        return 0

    if ns.summary:
        print(f"mailbox-filename-lint: {len(current)} path(s) over {MAX_PATH_LENGTH} chars")
        return 1 if current else 0

    if ns.baseline:
        base = Counter(
            ln for ln in Path(ns.baseline).read_text(encoding="utf-8").splitlines() if ln.strip()
        )
        new = current - base  # multiset difference — same ratchet as token_lint.py
        if new:
            print(
                f"mailbox-filename-lint: {sum(new.values())} NEW mailboxes/ path(s) over "
                f"{MAX_PATH_LENGTH} characters (not in baseline {ns.baseline}):"
            )
            for path in sorted(new.elements()):
                print(f"  {path}  ({len(path)} chars)")
            print(
                f"\nWindows' effective MAX_PATH is 260 characters including the clone-path "
                f"prefix (commonly 50-90 chars on a real machine). A path this long makes the "
                f"repo un-cloneable on Windows — see issue #1616.\n"
                f"Shorten the filename so the full 'mailboxes/...' path is {MAX_PATH_LENGTH} "
                f"characters or fewer.\n"
                f"(Existing long paths are grandfathered in the baseline — this only catches "
                f"NEW ones. Do not rename existing mailbox files to fix this.)"
            )
            return 1
        fixed = sum((base - current).values())
        msg = (
            f"mailbox-filename-lint: no new over-length paths "
            f"({sum(current.values())} baselined"
        )
        msg += f"; {fixed} no longer present)." if fixed else ")."
        print(msg)
        return 0

    for path in sorted(current.elements()):
        print(f"{path}  ({len(path)} chars)")
    if current:
        print(f"\nmailbox-filename-lint: {len(current)} path(s) over {MAX_PATH_LENGTH} chars.")
    return 1 if current else 0


if __name__ == "__main__":
    raise SystemExit(main())
