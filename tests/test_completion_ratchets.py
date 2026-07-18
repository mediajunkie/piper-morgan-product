"""Completion ratchets — the Finish-the-Unfinished sprint's growth guards (#1424).

Each test compares a mechanically-detected debt count against a frozen ceiling in
scripts/ratchet_ceilings.json. Counts may only go DOWN: a fix that removes debt
MUST lower the ceiling in the same commit (the MAX_DISPATCH_SITES discipline);
new debt that raises a count fails the build immediately.

These are growth-only guards: they cannot false-positive existing code, so they
CI-gate from day one (PM-ratified 2026-07-16) while the richer lints run
warn-mode pending Arch ratification.

Detectors:
  - silent_death_core     -> scripts/check_silent_death.py   (#1423)
  - unscoped_reads        -> scripts/check_unscoped_reads.py (#1419)
  - notimplementederror   -> raise-site count in production code (Census C)
  - todo_markers          -> TODO/FIXME/XXX/HACK comment count (Census C)

Plan of record: docs/internal/operations/finish-the-unfinished-sprint-2026-07-16.md
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
CEILINGS = json.loads((REPO_ROOT / "scripts" / "ratchet_ceilings.json").read_text())

RATCHET_MSG = (
    "\n{name}: count {count} exceeds frozen ceiling {ceiling} (#1424 ratchet).\n"
    "New debt of this class may not ship. Either remove it, or (for a reviewed "
    "exception) use the detector's annotation mechanism ({fix_hint}).\n"
    "If you MIGRATED debt away, lower the ceiling in scripts/ratchet_ceilings.json "
    "in this same commit."
)

SHRINK_MSG = (
    "\n{name}: count {count} is BELOW ceiling {ceiling} — nice, debt was removed. "
    "Lower the ceiling to {count} in scripts/ratchet_ceilings.json in this same "
    "commit so the improvement is locked in."
)


def _script_count(script: str, flag: str = "--count") -> int:
    out = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / script), flag],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        timeout=120,
    )
    assert out.returncode == 0, f"{script} failed: {out.stderr[:500]}"
    return int(out.stdout.strip())


def _grep_count(pattern: str, *, flags: int = 0) -> int:
    """Canonical pure-python recipe (embedded so the ratchet can't drift from a
    shell grep's quoting): count matching LINES in production .py under
    services/ + web/, excluding tests/archive/__pycache__."""
    rx = re.compile(pattern, flags)
    count = 0
    for root in ("services", "web"):
        for f in (REPO_ROOT / root).rglob("*.py"):
            if any(p in ("tests", "archive", "__pycache__") for p in f.parts):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            count += sum(1 for line in text.splitlines() if rx.search(line))
    return count


def _assert_ratchet(name: str, count: int, fix_hint: str) -> None:
    ceiling = CEILINGS[name]
    assert count <= ceiling, RATCHET_MSG.format(
        name=name, count=count, ceiling=ceiling, fix_hint=fix_hint
    )
    # Shrinkage is success, but an un-lowered ceiling lets the next regression
    # hide inside the slack — force the lock-in.
    assert count == ceiling, SHRINK_MSG.format(name=name, count=count, ceiling=ceiling)


@pytest.mark.smoke
def test_silent_death_ratchet():
    """#1423: broad no-reraise except handlers on the core path may only decrease."""
    _assert_ratchet(
        "silent_death_core",
        _script_count("check_silent_death.py"),
        "narrow the exception type, re-raise, or '# silent-ok: <reason>'",
    )


@pytest.mark.smoke
def test_unscoped_reads_ratchet():
    """#1419: global reads of user-specific credential/config state may only decrease."""
    _assert_ratchet(
        "unscoped_reads",
        _script_count("check_unscoped_reads.py"),
        "pass the principal (username=/user_id=) or '# global-ok: <reason>'",
    )


@pytest.mark.smoke
def test_unscoped_repo_reads_ratchet():
    """ADR-079 D2b: owner-bearing repository reads without an owner predicate may
    only decrease. The model set is DERIVED (D3) — a new owner-bearing table is
    auto-covered, so genuinely-new unscoped reads raise this count and fail here.
    Legit-indirect scoping (fetch-then-check, join/subquery) gets
    '# global-ok: <how>' per the D4/D6 allowlist discipline (Arch calibrates)."""
    _assert_ratchet(
        "unscoped_repo_reads",
        _script_count("check_unscoped_reads.py", flag="--count-repo"),
        "add the owner predicate to the WHERE, or '# global-ok: <how it is scoped>'",
    )


@pytest.mark.smoke
def test_notimplementederror_ratchet():
    """Census C: NotImplementedError raise sites in production code may only decrease."""
    # Lines carrying '# nie-ok: <reason>' are reviewed LOUD stubs (e.g. the
    # Arch-ruled security raise in token_blacklist, #1436 F4) — the ratchet
    # hunts silent stubs, and converting a silent no-op into a loud raise is an
    # improvement the raw count would misread as regression.
    count = _grep_count(r"raise NotImplementedError") - _grep_count(
        r"raise NotImplementedError\(.*# nie-ok:"
    )
    _assert_ratchet(
        "notimplementederror",
        count,
        "implement it, annotate '# nie-ok: <reason>' for a reviewed loud stub, "
        "or route through a documented-legit abstract/guard shape",
    )


@pytest.mark.smoke
def test_todo_marker_ratchet():
    """Census C: TODO/FIXME/XXX/HACK comment markers may only decrease."""
    _assert_ratchet(
        "todo_markers",
        _grep_count(r"#\s*(TODO|FIXME|XXX|HACK)\b", flags=re.IGNORECASE),
        "do the work, file an issue and reference it, or delete the stale marker",
    )
