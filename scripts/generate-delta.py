#!/usr/bin/env python3
"""
generate-delta.py — MEM-975 delta-since-last-session generator.

Per #975 MEM-DELTA AC: generate a "delta since last session" injection
for an agent at session start — structured "what changed" summary that
eliminates the 5-15 min manual reconstruction agents currently perform.

Per CIO May 26 design (dev/active/mem-975-delta-generator-design.md):
- Detect cutoff via filename-encoded timestamp of newest role session log
- 24h fallback if no log found in last 7 days
- Output to dev/active/delta-{role-slug}-{date}.md
- Print one-line signal to stdout for hook consumption (~50 tokens)
- <500 token target for full delta file
- Read-only (does not mutate state)

Usage:
    python scripts/generate-delta.py --role cio
    python scripts/generate-delta.py --role lead --cutoff 2026-05-26T08:00
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

# Filename pattern (both formats supported; model dropped from filenames 2026-06-29):
#   New: YYYY-MM-DD-HHMM-{role-slug}-code-log.md
#   Old: YYYY-MM-DD-HHMM-{role-slug}-code-opus-log.md (or -sonnet-, -haiku-)
LOG_FILENAME_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})-(\d{2})(\d{2})-([a-z0-9 ()-]+)-code(?:-(?:opus|sonnet|haiku))?-log\.md$",
    re.IGNORECASE,
)


def find_last_session_cutoff(role: str, lookback_days: int = 7) -> tuple[datetime, str | None]:
    """
    Find newest session log file for {role}. Return (cutoff_datetime, source_filename).
    Falls back to (now - 24h, None) if no log found within lookback_days.
    """
    dev_root = REPO_ROOT / "dev"
    if not dev_root.exists():
        return _fallback_cutoff(), None

    candidates: list[tuple[datetime, Path]] = []
    cutoff_floor = datetime.now() - timedelta(days=lookback_days)

    for path in dev_root.rglob(f"*-{role}-code*-log.md"):
        m = LOG_FILENAME_RE.match(path.name)
        if not m:
            continue
        year, month, day, hour, minute = map(int, m.group(1, 2, 3, 4, 5))
        try:
            ts = datetime(year, month, day, hour, minute)
        except ValueError:
            continue
        if ts < cutoff_floor:
            continue
        candidates.append((ts, path))

    if not candidates:
        return _fallback_cutoff(), None

    candidates.sort(key=lambda t: t[0], reverse=True)
    newest_ts, newest_path = candidates[0]
    return newest_ts, newest_path.name


def _fallback_cutoff() -> datetime:
    return datetime.now() - timedelta(hours=24)


# Valid role-slug charset (matches the mailbox/log convention: lowercase, digits,
# spaces, parens, hyphens — e.g. "cio", "xian (ceo)"). Notably excludes ".", so a
# filename fragment like "opus-log.md" (the #1153 mis-parse) is rejected.
ROLE_SLUG_RE = re.compile(r"[a-z0-9 ()-]+$")


def prune_old_deltas(role: str, out_dir: Path, retention_days: int = 7) -> int:
    """
    Remove this role's own delta files older than retention_days (#1153 no-prune fix).
    Deltas are gitignored but accumulated one-per-role-per-day on disk forever.
    Scoped to delta-{role}-*.md so concurrent roles don't delete each other's files.
    Returns count removed. Best-effort: tolerates races/permission errors.
    """
    if not out_dir.exists():
        return 0
    cutoff_ts = (datetime.now() - timedelta(days=retention_days)).timestamp()
    removed = 0
    for p in out_dir.glob(f"delta-{role}-*.md"):
        try:
            if p.is_file() and p.stat().st_mtime < cutoff_ts:
                p.unlink()
                removed += 1
        except OSError:
            continue
    return removed


def git_commits_since(cutoff: datetime, limit: int = 20) -> list[str]:
    """Return list of commit summary lines since cutoff (oneline format)."""
    iso = cutoff.strftime("%Y-%m-%dT%H:%M:%S")
    try:
        out = subprocess.check_output(
            ["git", "-C", str(REPO_ROOT), "log", f"--since={iso}", "--oneline", f"-{limit}"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except subprocess.CalledProcessError:
        return []
    return [line.rstrip() for line in out.splitlines() if line.strip()]


def new_memos_since(role: str, cutoff: datetime) -> tuple[list[Path], list[Path]]:
    """
    Find memos in role's inbox + read dirs that landed since cutoff.
    Use file mtime as best-available signal (filename dates don't encode time).
    Returns (inbox_list, read_list).
    """
    inbox_dir = REPO_ROOT / "mailboxes" / role / "inbox"
    read_dir = REPO_ROOT / "mailboxes" / role / "read"
    inbox_new: list[Path] = []
    read_new: list[Path] = []

    cutoff_ts = cutoff.timestamp()

    for d, accumulator in ((inbox_dir, inbox_new), (read_dir, read_new)):
        if not d.exists():
            continue
        for p in d.iterdir():
            if p.name == "MANIFEST.md" or not p.is_file() or p.suffix != ".md":
                continue
            try:
                if p.stat().st_mtime >= cutoff_ts:
                    accumulator.append(p)
            except OSError:
                continue

    return inbox_new, read_new


def omnibus_refs_since(cutoff: datetime) -> list[Path]:
    """Find omnibus log files created/modified since cutoff."""
    out: list[Path] = []
    cutoff_ts = cutoff.timestamp()
    dev_root = REPO_ROOT / "dev"
    if not dev_root.exists():
        return out
    for p in dev_root.rglob("omnibus-*.md"):
        try:
            if p.stat().st_mtime >= cutoff_ts:
                out.append(p)
        except OSError:
            continue
    return out


def write_delta_file(
    role: str,
    cutoff: datetime,
    cutoff_source: str | None,
    commits: list[str],
    inbox_memos: list[Path],
    read_memos: list[Path],
    omnibus: list[Path],
    out_path: Path,
) -> None:
    """Write the delta detail file. Truncates long lists with '+N more' footer."""
    today = datetime.now().strftime("%Y-%m-%d")
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M")

    lines: list[str] = []
    lines.append(f"# Delta — {role} — {today}")
    lines.append("")
    src = (
        f"from session log `{cutoff_source}`"
        if cutoff_source
        else "24h fallback (no recent log found)"
    )
    lines.append(f"**Cutoff**: {cutoff_str} ({src})")
    lines.append("")

    # Commits
    lines.append(f"## Commits ({len(commits)})")
    if not commits:
        lines.append("- (none)")
    else:
        for c in commits[:15]:
            lines.append(f"- {c}")
        if len(commits) > 15:
            lines.append(f"- +{len(commits) - 15} more (truncated)")
    lines.append("")

    # Memos
    total_memos = len(inbox_memos) + len(read_memos)
    lines.append(f"## New memos ({total_memos})")
    if not total_memos:
        lines.append("- (none)")
    else:
        for p in inbox_memos[:10]:
            lines.append(f"- inbox: `{p.name}`")
        for p in read_memos[:10]:
            lines.append(f"- read: `{p.name}`")
        remaining = max(0, (len(inbox_memos) - 10)) + max(0, (len(read_memos) - 10))
        if remaining:
            lines.append(f"- +{remaining} more (truncated)")
    lines.append("")

    # Omnibus
    lines.append(f"## Omnibus refs ({len(omnibus)})")
    if not omnibus:
        lines.append("- (none)")
    else:
        for p in omnibus[:5]:
            rel = p.relative_to(REPO_ROOT) if p.is_absolute() else p
            lines.append(f"- `{rel}`")
        if len(omnibus) > 5:
            lines.append(f"- +{len(omnibus) - 5} more (truncated)")
    lines.append("")

    lines.append("---")
    lines.append(f"*Regenerated at session-start by `scripts/generate-delta.py --role {role}`*")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")


def emit_signal(
    role: str,
    cutoff: datetime,
    commit_count: int,
    memo_count: int,
    omnibus_count: int,
    out_path: Path,
) -> str:
    """Return one-line signal for SessionStart hook consumption."""
    cutoff_str = cutoff.strftime("%Y-%m-%d %H:%M")
    rel = out_path.relative_to(REPO_ROOT) if out_path.is_absolute() else out_path
    return (
        f"📋 Delta available: {commit_count} commits, {memo_count} new memos, "
        f"{omnibus_count} omnibus refs since {cutoff_str} — see {rel}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate delta-since-last-session for an agent role"
    )
    parser.add_argument("--role", required=True, help="Role slug (e.g., cio, lead, host)")
    parser.add_argument(
        "--cutoff", help="Override cutoff ISO timestamp (default: detect from session log)"
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress signal output (still writes file)"
    )
    args = parser.parse_args()

    role = args.role.lower()

    # Defense-in-depth (#1153): reject implausible role slugs. The hook is the
    # primary fix, but if a caller ever passes a filename fragment (e.g.
    # "opus-log.md" from a mis-parse), fail loudly instead of writing a malformed
    # delta-opus-log.md-{date}.md file.
    if not ROLE_SLUG_RE.fullmatch(role):
        print(
            f"error: implausible role slug {args.role!r} (looks like a filename fragment, not a role)",
            file=sys.stderr,
        )
        return 1

    if args.cutoff:
        try:
            cutoff = datetime.fromisoformat(args.cutoff)
            cutoff_source = "manual override"
        except ValueError:
            print(f"error: invalid --cutoff value: {args.cutoff}", file=sys.stderr)
            return 1
    else:
        cutoff, cutoff_source = find_last_session_cutoff(role)

    commits = git_commits_since(cutoff)
    inbox_memos, read_memos = new_memos_since(role, cutoff)
    omnibus = omnibus_refs_since(cutoff)

    today = datetime.now().strftime("%Y-%m-%d")
    out_path = REPO_ROOT / "dev" / "active" / f"delta-{role}-{today}.md"

    prune_old_deltas(role, out_path.parent)

    write_delta_file(
        role=role,
        cutoff=cutoff,
        cutoff_source=cutoff_source,
        commits=commits,
        inbox_memos=inbox_memos,
        read_memos=read_memos,
        omnibus=omnibus,
        out_path=out_path,
    )

    signal = emit_signal(
        role=role,
        cutoff=cutoff,
        commit_count=len(commits),
        memo_count=len(inbox_memos) + len(read_memos),
        omnibus_count=len(omnibus),
        out_path=out_path,
    )

    if not args.quiet:
        print(signal)

    return 0


if __name__ == "__main__":
    sys.exit(main())
