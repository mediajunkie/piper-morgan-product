#!/usr/bin/env python3
"""
merge-keeper-sweep — Docs's daily merge-keeper protocol, automated.

Per PA Apr 27 scoping ask + Lead Dev Apr 28 sizing reply: simple-heuristic
version. Auto-merges wrapped + clean fast-forwardable feature branches to
main; escalates everything else to Docs via a structured log entry.

Heuristic: a branch is "wrapped" if its last commit is older than --age-hours
(default 24). A branch is "clean" if no large blobs, .env files, or .DS_Store
files appear in its diff against main, AND a no-conflict merge is possible.

Always escalates (never auto-merges):
  - Branches younger than the age threshold (likely active)
  - Branches with merge conflicts against main
  - Branches whose diff contains files larger than --max-blob-size (default 1MB)
  - Branches whose diff contains .env, .DS_Store, or other ignore-pattern files

Always reports its actions to dev/active/merge-keeper-{YYYY-MM-DD}.md so
Docs can review. Read-only by default (--dry-run is implicit unless
--apply is passed).

Usage:
    python scripts/merge-keeper-sweep.py             # dry-run (default)
    python scripts/merge-keeper-sweep.py --apply     # actually merge
    python scripts/merge-keeper-sweep.py --age-hours 12  # tighter age window
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Tuple


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_AGE_HOURS = 24
DEFAULT_MAX_BLOB_SIZE = 1_000_000  # 1MB
ESCALATION_PATTERNS = (
    re.compile(r"\.env(\.|$)"),
    re.compile(r"\.DS_Store$"),
    re.compile(r"\.pem$"),
    re.compile(r"\.key$"),
    re.compile(r"id_rsa"),
    re.compile(r"credentials\.json$"),
)


@dataclass
class BranchAction:
    """One branch's evaluation result + the action taken (or proposed)."""

    branch: str
    last_commit_age_hours: float
    files_changed: int
    insertions: int
    deletions: int
    action: str  # "merged" | "escalate" | "skip-active" | "no-changes"
    reason: str
    conflicts: bool = False
    blob_warnings: List[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.blob_warnings is None:
            self.blob_warnings = []


def run_git(*args: str, cwd: Path = PROJECT_ROOT) -> Tuple[int, str, str]:
    """Run git with args, return (returncode, stdout, stderr). No raises."""
    result = subprocess.run(
        ["git"] + list(args),
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def fetch_origin() -> bool:
    rc, _, err = run_git("fetch", "origin", "--prune")
    if rc != 0:
        print(f"[merge-keeper] git fetch failed: {err}", file=sys.stderr)
        return False
    return True


def list_claude_branches() -> List[str]:
    """Return list of remote claude/* branches that have at least one commit
    not on origin/main."""
    rc, out, _ = run_git(
        "for-each-ref",
        "--format=%(refname:short)",
        "refs/remotes/origin/claude/",
    )
    if rc != 0:
        return []

    branches = [b.strip().removeprefix("origin/") for b in out.splitlines() if b.strip()]
    branches = [b for b in branches if b.startswith("claude/")]

    # Filter to those with commits ahead of origin/main
    ahead: List[str] = []
    for branch in branches:
        rc, out, _ = run_git("rev-list", "--count", f"origin/main..origin/{branch}")
        if rc == 0:
            try:
                count = int(out.strip())
                if count > 0:
                    ahead.append(branch)
            except ValueError:
                continue
    return ahead


def branch_last_commit_age(branch: str) -> Optional[float]:
    """Hours since last commit on the branch (decimal). None on error."""
    rc, out, _ = run_git("log", "-1", "--format=%cI", f"origin/{branch}")
    if rc != 0 or not out.strip():
        return None
    try:
        committed_at = datetime.fromisoformat(out.strip())
    except ValueError:
        return None
    if committed_at.tzinfo is None:
        committed_at = committed_at.replace(tzinfo=timezone.utc)
    delta = datetime.now(timezone.utc) - committed_at
    return delta.total_seconds() / 3600.0


def branch_diff_summary(
    branch: str,
    max_blob_size: int = DEFAULT_MAX_BLOB_SIZE,
) -> Tuple[int, int, int, List[str]]:
    """Return (files_changed, insertions, deletions, blob_warnings)."""
    rc, out, _ = run_git("diff", "--numstat", f"origin/main...origin/{branch}")
    if rc != 0:
        return 0, 0, 0, []

    files_changed = 0
    insertions = 0
    deletions = 0
    warnings: List[str] = []

    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        ins_s, del_s, path = parts[0], parts[1], parts[2]
        files_changed += 1
        if ins_s != "-":
            try:
                insertions += int(ins_s)
            except ValueError:
                pass
        if del_s != "-":
            try:
                deletions += int(del_s)
            except ValueError:
                pass
        for pat in ESCALATION_PATTERNS:
            if pat.search(path):
                warnings.append(f"escalation pattern matched: {path}")

    # Check for large blobs via ls-tree on the branch tip vs main
    rc2, blob_out, _ = run_git(
        "diff",
        "--diff-filter=AM",
        "--no-renames",
        "--raw",
        f"origin/main...origin/{branch}",
    )
    if rc2 == 0:
        for line in blob_out.splitlines():
            # raw format: :100644 100644 oldsha newsha M    path
            parts = line.split()
            if len(parts) < 6:
                continue
            new_sha = parts[3]
            path = " ".join(parts[5:])
            rc3, size_out, _ = run_git("cat-file", "-s", new_sha)
            if rc3 == 0:
                try:
                    size = int(size_out.strip())
                    if size > max_blob_size:
                        warnings.append(f"large blob: {path} ({size:,} bytes)")
                except ValueError:
                    continue

    return files_changed, insertions, deletions, warnings


def branch_has_conflicts(branch: str) -> bool:
    """Use merge-tree to check whether merging origin/{branch} into main
    would produce conflicts. Read-only check; doesn't modify worktree."""
    rc, base_out, _ = run_git("merge-base", "origin/main", f"origin/{branch}")
    if rc != 0 or not base_out.strip():
        return True  # safer to escalate on uncertainty
    base = base_out.strip()
    rc2, mt_out, _ = run_git("merge-tree", base, "origin/main", f"origin/{branch}")
    if rc2 != 0:
        return True
    # merge-tree prints conflict markers (<<<<<<<) when conflicts exist.
    return "<<<<<<<" in mt_out


def evaluate_branch(
    branch: str,
    age_hours_threshold: float,
    max_blob_size: int,
) -> BranchAction:
    """Assess one branch and decide what action to take."""
    age = branch_last_commit_age(branch)
    if age is None:
        return BranchAction(
            branch=branch,
            last_commit_age_hours=0.0,
            files_changed=0,
            insertions=0,
            deletions=0,
            action="escalate",
            reason="could not read last-commit timestamp",
        )

    if age < age_hours_threshold:
        return BranchAction(
            branch=branch,
            last_commit_age_hours=age,
            files_changed=0,
            insertions=0,
            deletions=0,
            action="skip-active",
            reason=(
                f"last commit {age:.1f}h ago (< {age_hours_threshold}h "
                f"threshold) — likely active session"
            ),
        )

    files_changed, insertions, deletions, warnings = branch_diff_summary(
        branch, max_blob_size=max_blob_size
    )
    if files_changed == 0:
        return BranchAction(
            branch=branch,
            last_commit_age_hours=age,
            files_changed=0,
            insertions=0,
            deletions=0,
            action="no-changes",
            reason="no file diff against main (already merged?)",
        )

    if warnings:
        return BranchAction(
            branch=branch,
            last_commit_age_hours=age,
            files_changed=files_changed,
            insertions=insertions,
            deletions=deletions,
            action="escalate",
            reason="diff contains files matching escalation patterns",
            blob_warnings=warnings,
        )

    if branch_has_conflicts(branch):
        return BranchAction(
            branch=branch,
            last_commit_age_hours=age,
            files_changed=files_changed,
            insertions=insertions,
            deletions=deletions,
            action="escalate",
            reason="merge would conflict against main",
            conflicts=True,
        )

    # Eligible for auto-merge.
    return BranchAction(
        branch=branch,
        last_commit_age_hours=age,
        files_changed=files_changed,
        insertions=insertions,
        deletions=deletions,
        action="merged",
        reason=(
            f"wrapped ({age:.1f}h since last commit), {files_changed} "
            f"files / +{insertions} -{deletions}, no escalation patterns, "
            f"no conflicts"
        ),
    )


def perform_merge(branch: str) -> Tuple[bool, str]:
    """Execute the merge + push for an auto-mergeable branch. Returns
    (success, output_message). Caller has already verified the branch
    is safe to merge."""
    rc, out, err = run_git(
        "merge",
        "--no-ff",
        f"origin/{branch}",
        "-m",
        f"merge: {branch} — auto-merged via merge-keeper-sweep",
    )
    if rc != 0:
        return False, f"merge failed: {err.strip() or out.strip()}"

    rc, out, err = run_git("push", "origin", "main")
    if rc != 0:
        return False, f"push failed (merge succeeded locally): {err.strip()}"

    return True, "merged + pushed to origin/main"


def render_log(actions: List[BranchAction], applied: bool) -> str:
    """Build the dev/active/merge-keeper-{date}.md report content."""
    timestamp = datetime.now(timezone.utc).astimezone()
    mode = "APPLIED" if applied else "DRY-RUN"
    lines: List[str] = [
        f"# Merge-Keeper Sweep — {timestamp.strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        f"**Mode**: {mode}",
        f"**Branches considered**: {len(actions)}",
        "",
        "## Summary",
        "",
        f"| Action | Count |",
        f"|---|---|",
    ]
    counts: dict = {}
    for a in actions:
        counts[a.action] = counts.get(a.action, 0) + 1
    for action, count in sorted(counts.items()):
        lines.append(f"| {action} | {count} |")

    lines.append("")
    lines.append("## Per-branch detail")
    lines.append("")

    for a in actions:
        lines.append(f"### {a.branch}")
        lines.append("")
        lines.append(f"- **Action**: {a.action}")
        lines.append(f"- **Reason**: {a.reason}")
        lines.append(f"- **Last commit**: {a.last_commit_age_hours:.1f}h ago")
        if a.files_changed:
            lines.append(f"- **Diff**: {a.files_changed} files, " f"+{a.insertions} -{a.deletions}")
        if a.conflicts:
            lines.append("- **Conflict**: merge-tree reports conflicts against main")
        if a.blob_warnings:
            lines.append("- **Blob/pattern warnings**:")
            for w in a.blob_warnings:
                lines.append(f"  - {w}")
        lines.append("")

    if any(a.action == "escalate" for a in actions):
        lines.append("## Escalation queue (Docs to review)")
        lines.append("")
        for a in actions:
            if a.action == "escalate":
                lines.append(f"- `{a.branch}` — {a.reason}")
        lines.append("")

    return "\n".join(lines)


def write_log(content: str) -> Path:
    """Write the sweep log under dev/active/. Returns path."""
    today = datetime.now().date().isoformat()
    log_dir = PROJECT_ROOT / "dev" / "active"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"merge-keeper-{today}.md"
    log_path.write_text(content, encoding="utf-8")
    return log_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually perform merges. Default is dry-run.",
    )
    parser.add_argument(
        "--age-hours",
        type=float,
        default=DEFAULT_AGE_HOURS,
        help=f"Min hours since last commit to consider wrapped (default {DEFAULT_AGE_HOURS})",
    )
    parser.add_argument(
        "--max-blob-size",
        type=int,
        default=DEFAULT_MAX_BLOB_SIZE,
        help=f"Max bytes per blob before escalation (default {DEFAULT_MAX_BLOB_SIZE})",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Skip git fetch (testing aid)",
    )
    args = parser.parse_args()

    if not args.no_fetch:
        if not fetch_origin():
            print("[merge-keeper] aborting (fetch failed)", file=sys.stderr)
            return 2

    branches = list_claude_branches()
    if not branches:
        print("[merge-keeper] no claude/* branches with commits ahead of main")
        return 0

    print(f"[merge-keeper] evaluating {len(branches)} branches...")
    actions: List[BranchAction] = []
    for branch in branches:
        action = evaluate_branch(
            branch,
            age_hours_threshold=args.age_hours,
            max_blob_size=args.max_blob_size,
        )
        actions.append(action)
        print(f"  {action.branch}: {action.action} — {action.reason}")

    # Apply merges if requested.
    if args.apply:
        for action in actions:
            if action.action != "merged":
                continue
            print(f"[merge-keeper] merging {action.branch}...")
            success, msg = perform_merge(action.branch)
            if success:
                action.reason += f"; {msg}"
            else:
                action.action = "escalate"
                action.reason = f"auto-merge attempted but failed: {msg}"
                print(f"  [merge-keeper] {action.branch}: {msg}", file=sys.stderr)

    # Always write the log.
    log_content = render_log(actions, applied=args.apply)
    log_path = write_log(log_content)
    print(f"[merge-keeper] log: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
