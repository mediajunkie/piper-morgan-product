#!/usr/bin/env python3
"""
deliver-mail (b1) — regenerate MANIFEST.md from filesystem state.

Per PA Apr 27 scoping memo: the manifest-append race in the legacy
deliver-mail skill (two agents simultaneously writing → conflict) is solved
structurally by treating MANIFEST.md as a derived artifact regenerated
from the filesystem. Files in inbox/read/sent are the authoritative state;
the manifest just describes them.

This script walks `mailboxes/{role}/{inbox,read,sent}/` for any role, parses
the YAML frontmatter of each `.md` file (skipping `MANIFEST.md`), and writes
out a fresh `MANIFEST.md` per directory matching the existing 4-column
format (`Delivered | From | Filename | Summary`).

Frontmatter schema parsed:
  - `from`: maps to "From" column (slug or full role name)
  - `date`: maps to "Delivered" column (used for sort ordering)
  - `subject`: maps to "Summary" column (truncated to ~80 chars)

Filename convention `memo-YYYY-MM-DD-from-{slug}-...` is the fallback
when frontmatter is missing or malformed (some legacy memos don't carry
full frontmatter).

Usage:
    python scripts/regenerate-mailbox-manifests.py            # all roles
    python scripts/regenerate-mailbox-manifests.py --role lead # one role
    python scripts/regenerate-mailbox-manifests.py --dry-run   # show diff,
                                                                no writes
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MAILBOXES_ROOT = PROJECT_ROOT / "mailboxes"

# Subdirectories per role that carry memos with their own MANIFEST.md.
# `sent/` historically uses `sent.log` (append-only), not MANIFEST.md, so
# we leave it alone unless a `MANIFEST.md` is already present.
MANIFEST_SUBDIRS = ("inbox", "read")
SUMMARY_TRUNCATE = 80
MANIFEST_FILENAME = "MANIFEST.md"

# Curated-content preservation (#1106): everything from this marker line to
# EOF in an existing MANIFEST is the recipient's curated register — carried
# over VERBATIM on every regen. The derived register (header + entry table)
# above the marker is regenerated from filesystem state; the curated register
# below it belongs to the recipient alone. This is the m-41 register-
# separation cure applied to MANIFESTs: two registers, explicit delimiter,
# no path-of-least-resistance that silently drops one.
CURATED_MARKER = "<!-- curated -->"


@dataclass
class MemoEntry:
    """Parsed metadata from one memo file."""

    filename: str
    delivered: str  # YYYY-MM-DD HH:MM
    sender: str
    summary: str
    sort_key: str  # date, used to order rows


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------


_FILENAME_FROM_RE = re.compile(r"^memo-(?:\d{4}-\d{2}-\d{2}-)?(?:from-)?([a-z0-9-]+?)-to-")
_FILENAME_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")


def parse_frontmatter(path: Path) -> dict:
    """Read the first ~30 lines of a memo file, extract YAML frontmatter
    delimited by `---` lines. Returns a dict of fields. Robust to malformed
    or absent frontmatter (returns {} rather than raising)."""
    try:
        with path.open("r", encoding="utf-8") as f:
            lines: List[str] = []
            for i, line in enumerate(f):
                if i >= 60:
                    break
                lines.append(line.rstrip("\n"))
    except (OSError, UnicodeDecodeError):
        return {}

    if not lines or lines[0].strip() != "---":
        return {}

    fields: dict = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        # Simple `key: value` parser. Multi-line values not supported
        # (unnecessary for these memos in practice).
        match = re.match(r"^([a-zA-Z][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if match:
            key, value = match.group(1), match.group(2).strip()
            # Strip surrounding quotes if present.
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            fields[key] = value

    return fields


def _extract_date(frontmatter: dict, filename: str) -> str:
    """Choose the best date string for the manifest. Prefers frontmatter
    `date`; falls back to the first YYYY-MM-DD in the filename; last resort
    is empty string."""
    raw = frontmatter.get("date", "")
    if raw:
        # Accept either YYYY-MM-DD or YYYY-MM-DD HH:MM forms; preserve as-is.
        return raw
    match = _FILENAME_DATE_RE.search(filename)
    return match.group(1) if match else ""


def _extract_sender(frontmatter: dict, filename: str) -> str:
    """Choose the best sender for the manifest. Prefers frontmatter `from`;
    falls back to filename slug pattern `memo-YYYY-MM-DD-from-{slug}-...`
    or `memo-{slug}-to-{...}`."""
    raw = frontmatter.get("from", "")
    if raw:
        return raw
    match = _FILENAME_FROM_RE.match(filename)
    return match.group(1) if match else "?"


def _extract_first_h1(path: Path) -> str:
    """Fallback summary source (#1106 AC): the file's first `# ` heading
    after any frontmatter block. Returns "" if none found in the first
    ~80 lines."""
    try:
        with path.open("r", encoding="utf-8") as f:
            in_frontmatter = False
            for i, line in enumerate(f):
                if i >= 80:
                    break
                stripped = line.strip()
                if i == 0 and stripped == "---":
                    in_frontmatter = True
                    continue
                if in_frontmatter:
                    if stripped == "---":
                        in_frontmatter = False
                    continue
                if stripped.startswith("# "):
                    return stripped[2:].strip()
    except (OSError, UnicodeDecodeError):
        pass
    return ""


def _extract_summary(frontmatter: dict, path: Path) -> str:
    """Summary precedence (#1106 AC): frontmatter `subject:` → file's first
    H1 → "(no subject)" — and the last is WARNED to stderr, never silent
    (the 2026-05-19 destructive sync wrote 32 silent `(no subject)` markers;
    the warning makes the parse gap visible at regen time)."""
    subject = frontmatter.get("subject", "").strip()
    if not subject:
        subject = _extract_first_h1(path)
    if not subject:
        print(
            f"[regen-mailbox] WARNING: no subject or H1 found in {path.name}"
            " — writing '(no subject)'",
            file=sys.stderr,
        )
        return "(no subject)"
    if len(subject) > SUMMARY_TRUNCATE:
        return subject[: SUMMARY_TRUNCATE - 1].rstrip() + "…"
    return subject


def collect_memos(directory: Path) -> List[MemoEntry]:
    """Walk a single mailbox subdirectory (inbox/read), return one MemoEntry
    per `.md` file (skipping MANIFEST.md and any non-memo files)."""
    if not directory.is_dir():
        return []

    entries: List[MemoEntry] = []
    for path in sorted(directory.iterdir()):
        if path.name == MANIFEST_FILENAME:
            continue
        if path.suffix != ".md":
            continue

        frontmatter = parse_frontmatter(path)
        delivered = _extract_date(frontmatter, path.name)
        sender = _extract_sender(frontmatter, path.name)
        summary = _extract_summary(frontmatter, path)

        # Sort key: prefer ISO date for stable ordering. If no parseable date,
        # fall back to filename sort.
        sort_key = delivered or path.name

        entries.append(
            MemoEntry(
                filename=path.name,
                delivered=delivered,
                sender=sender,
                summary=summary,
                sort_key=sort_key,
            )
        )

    # Sort descending — newest first.
    entries.sort(key=lambda e: e.sort_key, reverse=True)
    return entries


# ---------------------------------------------------------------------------
# Manifest rendering
# ---------------------------------------------------------------------------


def extract_curated_tail(existing_content: str) -> str:
    """Return the curated register of an existing MANIFEST: everything from
    the CURATED_MARKER line to EOF (marker included). Returns "" when the
    marker is absent. The curated tail is preserved verbatim across regens —
    the recipient is its sole writer (#1106 recipient-owns semantics)."""
    if not existing_content:
        return ""
    idx = existing_content.find(CURATED_MARKER)
    if idx == -1:
        return ""
    return existing_content[idx:].rstrip("\n") + "\n"


def render_manifest(
    role: str,
    subdir: str,
    entries: List[MemoEntry],
    curated_tail: str = "",
) -> str:
    """Render the MANIFEST.md content for one role/subdir combination.
    The derived register (header + table) is regenerated; the curated
    register (`curated_tail`, everything at/below the CURATED_MARKER in the
    prior content) is re-emitted verbatim after it."""
    lines: List[str] = [
        f"# {subdir.capitalize()} Manifest — {role}",
        "",
        "| Delivered | From | Filename | Summary |",
        "|-----------|------|----------|---------|",
    ]
    if not entries:
        lines.append("| _(empty)_ | | | |")
    else:
        for e in entries:
            # Escape any pipe chars in summary to avoid breaking the table.
            safe_summary = e.summary.replace("|", "\\|")
            lines.append(f"| {e.delivered} | {e.sender} | {e.filename} | {safe_summary} |")
    lines.append("")  # blank line after table
    if curated_tail:
        lines.append(curated_tail.rstrip("\n"))
        lines.append("")
    return "\n".join(lines)


def regenerate_for_role(
    role: str,
    dry_run: bool = False,
    quiet: bool = False,
) -> int:
    """Regenerate manifests for one role. Returns count of manifest files
    written (or that would be written in --dry-run)."""
    role_dir = MAILBOXES_ROOT / role
    if not role_dir.is_dir():
        if not quiet:
            print(f"[regen-mailbox] skip {role}: not a directory", file=sys.stderr)
        return 0

    # #1454 self-heal: an inbox file whose read/ twin exists is a merge-resurrected
    # duplicate of an already-triaged memo (add/delete merge semantics keep re-adding
    # it after the inbox->read move lands on origin). The read/ copy is the
    # authoritative triage state; drop the inbox ghost so it can't round-trip again.
    inbox_dir, read_dir = role_dir / "inbox", role_dir / "read"
    if inbox_dir.is_dir() and read_dir.is_dir():
        for ghost in inbox_dir.glob("*.md"):
            if ghost.name != MANIFEST_FILENAME and (read_dir / ghost.name).is_file():
                if dry_run:
                    print(f"[regen-mailbox] would drop inbox ghost: {ghost.name}", file=sys.stderr)
                else:
                    ghost.unlink()
                    print(
                        f"[regen-mailbox] dropped inbox ghost (read/ twin exists): {ghost.name}",
                        file=sys.stderr,
                    )

    written = 0
    for subdir in MANIFEST_SUBDIRS:
        target_dir = role_dir / subdir
        if not target_dir.is_dir():
            continue

        entries = collect_memos(target_dir)
        manifest_path = target_dir / MANIFEST_FILENAME

        old_content = ""
        if manifest_path.exists():
            try:
                old_content = manifest_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                old_content = ""

        curated_tail = extract_curated_tail(old_content)
        new_content = render_manifest(role, subdir, entries, curated_tail)

        if old_content == new_content:
            if not quiet:
                print(f"[regen-mailbox] {role}/{subdir} unchanged ({len(entries)} entries)")
            continue

        if dry_run:
            if not quiet:
                print(
                    f"[regen-mailbox] DRY-RUN would update "
                    f"{role}/{subdir}/MANIFEST.md ({len(entries)} entries)"
                )
        else:
            # Atomic write via temp + rename.
            tmp_path = manifest_path.with_suffix(".md.tmp")
            tmp_path.write_text(new_content, encoding="utf-8")
            tmp_path.replace(manifest_path)
            if not quiet:
                print(
                    f"[regen-mailbox] wrote {role}/{subdir}/MANIFEST.md "
                    f"({len(entries)} entries)"
                )
        written += 1

    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def discover_roles() -> List[str]:
    """Return sorted list of subdirs of mailboxes/ that look like role
    directories (have an `inbox/` or `read/`)."""
    if not MAILBOXES_ROOT.is_dir():
        return []
    roles: List[str] = []
    for entry in sorted(MAILBOXES_ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name in ("incoming",):
            continue
        if (entry / "inbox").is_dir() or (entry / "read").is_dir():
            roles.append(entry.name)
    return roles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--role",
        help="Regenerate manifests for one specific role (default: all roles)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't write; report what would change",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file output (still reports summary)",
    )
    args = parser.parse_args()

    if args.role:
        roles = [args.role]
    else:
        roles = discover_roles()

    total_written = 0
    for role in roles:
        total_written += regenerate_for_role(role, dry_run=args.dry_run, quiet=args.quiet)

    action = "would update" if args.dry_run else "updated"
    print(f"[regen-mailbox] {action} {total_written} manifest(s) " f"across {len(roles)} role(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
