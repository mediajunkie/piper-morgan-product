#!/usr/bin/env python3
"""Verify VERSION and pyproject.toml agree (docs/versioning.md: "must match").

Found 2026-07-02 (v0.8.9.1 release): VERSION had drifted 4 releases behind
pyproject.toml, silently, because nothing checked this mechanically -- the release
runbook's "Version Bump" step didn't even list VERSION as a file to update, so the
manual checklist had no chance to catch it either. This closes that gap: run this
after any version bump (the release runbook now calls it explicitly), or as a
pre-commit/CI check, so the two files can't silently diverge again.

Exit 0 = match. Exit 1 = mismatch (prints both values).
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def read_version_file() -> str:
    return (ROOT / "VERSION").read_text().strip()


def read_pyproject_version() -> str:
    text = (ROOT / "pyproject.toml").read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise SystemExit("Could not find a version = \"...\" line in pyproject.toml")
    return match.group(1)


def main() -> int:
    version_file = read_version_file()
    pyproject_version = read_pyproject_version()

    if version_file == pyproject_version:
        print(f"OK: VERSION and pyproject.toml agree ({version_file})")
        return 0

    print(
        f"MISMATCH: VERSION={version_file!r} but pyproject.toml={pyproject_version!r}\n"
        "docs/versioning.md: 'pyproject.toml ... must match VERSION file'. Update whichever "
        "is stale, or run the release runbook's Version Bump step, which updates both."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
