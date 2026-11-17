#!/usr/bin/env python3
"""ADR-084 D2 (issue 2392): refuse a credential shape before it reaches this public repo.

Two modes, one set of shapes (``mailbox_bearer_lint.scan_line`` plus the GitHub app-token
and bare Fly macaroon prefixes below):

- ``--staged`` (the commit hook): reads the lines the staged change ADDS, from
  ``git diff --cached``, in every folder. A moved file adds no lines, so a memo with an old
  hit can still be moved. With ``--baseline`` a line already listed there (an existing test
  fixture, edited around or re-indented) passes; any other added line with a shape is refused.
- ``--tracked`` (the push gate and CI): reads every tracked text file at HEAD outside
  ``mailboxes/``, ``docs/`` and ``dev/``. Those three are ``mailbox_bearer_lint.py``'s, with
  its own baseline, on the line above this one in ``lint.yml``.

A hit prints the path, the line number and the shape's name. It never prints the value, a
part of it, or the line. The baseline holds ``path:hash`` where the hash is of the line with
every hit replaced by a fixed word, so it carries nothing derived from a value.

A masked form (``ABCD…WXYZ``) has no run long enough to match and passes.

Usage:
    scripts/staged_credential_scan.py --staged --baseline .staged-credential-scan-baseline.txt
    scripts/staged_credential_scan.py --tracked --baseline .staged-credential-scan-baseline.txt
    scripts/staged_credential_scan.py --tracked --write-baseline .staged-credential-scan-baseline.txt

Exit 0 clean, 1 on a hit, 3 if git could not be read (the hook treats 3 as a refusal too).

Concept: docs/internal/operations/adr-084-one-time-steps.md (staged_credential_scan.py)
"""

from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))

import mailbox_bearer_lint as bearer  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# Shapes the bearer lint doesn't name: GitHub app tokens (server, user, refresh) and a Fly
# macaroon written without its "FlyV1 " scheme word.
_EXTRA = re.compile(r"(?<![A-Za-z0-9_])(?:gh[sur]_[A-Za-z0-9]{20,}|fm[12]_[A-Za-z0-9_=+/-]{20,})")

# First match wins; the name is all a report says about what was found.
_NAMES = (
    ("sk-ant-", "Anthropic key"),
    ("sk-", "OpenAI-style key"),
    ("xox", "Slack token"),
    ("xapp-", "Slack token"),
    ("gh", "GitHub token"),
    ("github_pat_", "GitHub token"),
    ("AIza", "Google key"),
    ("fo1_", "Fly token"),
    ("fm", "Fly token"),
    ("FlyV1 ", "Fly token"),
)

# What git grep pre-filters on before Python decides. Looser than the real shapes on purpose.
_PREFILTER = (
    r"(sk-|xox[bpa]-|xapp-|gh[pousr]_|github_pat_|AIza|fo1_|fm[12]_|FlyV1 )"
    r"[A-Za-z0-9_=+/-]{10,}|[0-9A-Za-z-]{24}"
)
BEARER_ROOTS = ("mailboxes", "docs", "dev")
PLACEHOLDER = "<credential>"

Hit = Tuple[str, int, str, str]  # path, line number, shape name, baseline key


class GitError(Exception):
    pass


def shape_name(credential: str) -> str:
    for prefix, name in _NAMES:
        if credential.startswith(prefix):
            return name
    return "invite code"


def _is_placeholder(credential: str) -> bool:
    """``ghp_xxxxxxxxxxxxxxxxxxxx`` in a form's placeholder text: a run built from a handful
    of characters. A minted key draws from 32 or more symbols; fewer than 6 distinct
    characters in 20 or more has a probability far below 1e-9."""
    return len(set(credential[-20:])) < 6


def _is_identifier(credential: str) -> bool:
    """``github_pat_at_rest_clear_failed`` is a log event name, not a token: no digit and no
    upper-case letter anywhere. A minted key of 20 or more characters has one or the other
    (base62 without either: under 1e-8). Invite codes are judged by the bearer lint's own
    rule and never reach this."""
    return not any(ch.isdigit() or ch.isupper() for ch in credential)


def find(line: str, path: str = "") -> List[str]:
    """The credentials in one line. Callers must not print what this returns.

    Outside the bearer lint's three roots an invite code counts only as minted, 24
    characters with no dashes: the dash-grouped form matched upper-case log event names in
    ``services/`` on the first run (5 of 5 hits there were event names)."""
    in_bearer_roots = path.split("/", 1)[0] in BEARER_ROOTS
    found = []
    for credential in bearer.scan_line(line) + [m.group(0) for m in _EXTRA.finditer(line)]:
        if _is_placeholder(credential) or _is_identifier(credential):
            continue
        if shape_name(credential) == "invite code" and "-" in credential and not in_bearer_roots:
            continue
        found.append(credential)
    return found


def baseline_key(path: str, line: str, credentials: Iterable[str]) -> str:
    for credential in credentials:
        line = line.replace(credential, PLACEHOLDER)
    digest = hashlib.sha1(line.strip().encode("utf-8", errors="replace")).hexdigest()[:12]
    return f"{path}:{digest}"


def hits_in(path: str, numbered_lines: Iterable[Tuple[int, str]]) -> List[Hit]:
    if Path(path).suffix.lower() in bearer._SKIP_SUFFIXES:
        return []
    found: List[Hit] = []
    for number, line in numbered_lines:
        credentials = find(line, path)
        if credentials:
            key = baseline_key(path, line, credentials)
            found.extend((path, number, shape_name(c), key) for c in credentials)
    return found


def _git(args: List[str], ok_codes: Tuple[int, ...] = (0,)) -> str:
    try:
        done = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, check=False)
    except OSError:
        raise GitError("git could not be run") from None
    if done.returncode not in ok_codes:
        raise GitError(f"git {args[0]} exited {done.returncode}")
    return done.stdout.decode("utf-8", errors="replace")


_HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


def added_lines(diff: str) -> List[Tuple[str, int, str]]:
    """(path, line number, text) for each line a unified diff adds."""
    out: List[Tuple[str, int, str]] = []
    path: Optional[str] = None
    number = 0
    for raw in diff.splitlines():
        if raw.startswith("+++ "):
            target = raw[4:].rstrip("\t")
            path = None if target == "/dev/null" else target[2:] if target[:2] == "b/" else target
            continue
        if raw.startswith("--- ") or raw.startswith("diff --git "):
            continue
        hunk = _HUNK.match(raw)
        if hunk:
            number = int(hunk.group(1))
            continue
        if path is not None and raw.startswith("+"):
            out.append((path, number, raw[1:]))
            number += 1
    return out


def scan_staged() -> List[Hit]:
    diff = _git(
        ["diff", "--cached", "-M", "-U0", "--no-color", "--no-ext-diff", "--diff-filter=ACMR"]
    )
    by_path: dict = {}
    for path, number, text in added_lines(diff):
        by_path.setdefault(path, []).append((number, text))
    return [hit for path, lines in by_path.items() for hit in hits_in(path, lines)]


def scan_tracked() -> List[Hit]:
    excludes = [f":(exclude){root}" for root in BEARER_ROOTS]
    out = _git(
        ["grep", "-I", "-n", "-z", "-E", _PREFILTER, "HEAD", "--", ".", *excludes],
        ok_codes=(0, 1),  # 1 is "no line matched"
    )
    by_path: dict = {}
    for record in out.split("\n"):
        parts = record.split("\0", 2)
        if len(parts) != 3:
            continue
        ref_path, number, text = parts
        path = ref_path.split(":", 1)[1] if ":" in ref_path else ref_path
        by_path.setdefault(path, []).append((int(number), text))
    return [hit for path, lines in by_path.items() for hit in hits_in(path, lines)]


def read_baseline(path: Optional[Path]) -> Set[str]:
    if not path or not path.exists():
        return set()
    return {line.strip() for line in path.read_text().splitlines() if line.strip()}


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Refuse credential shapes in staged or tracked files."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--staged", action="store_true", help="lines the staged change adds")
    mode.add_argument("--tracked", action="store_true", help="tracked files at HEAD")
    parser.add_argument("--baseline", type=Path, help="ignore the lines listed here")
    parser.add_argument("--write-baseline", type=Path, help="with --tracked: write current hits")
    args = parser.parse_args(argv)
    if args.staged and args.write_baseline:
        parser.error("the baseline is written from --tracked")

    try:
        hits = scan_staged() if args.staged else scan_tracked()
    except GitError as error:
        print(
            f"staged_credential_scan: could not read git ({error}); nothing was checked",
            file=sys.stderr,
        )
        return 3

    if args.write_baseline:
        keys = sorted({key for _, _, _, key in hits})
        args.write_baseline.write_text("\n".join(keys) + ("\n" if keys else ""))
        print(f"staged_credential_scan: baseline written, {len(keys)} line(s)")
        return 0

    baseline = read_baseline(args.baseline)
    new = [hit for hit in hits if hit[3] not in baseline]
    what = (
        "lines the staged change adds"
        if args.staged
        else "tracked files outside mailboxes/, docs/ and dev/"
    )
    if not new:
        print(
            f"staged_credential_scan: OK, no new credential shape in {what} "
            f"({len(hits) - len(new)} baselined)"
        )
        return 0

    print(
        f"staged_credential_scan: FAIL, {len(new)} credential shape(s) in {what} (issue 2392):",
        file=sys.stderr,
    )
    for path, number, name, _ in new:
        print(f"  {path}:{number}  {name}", file=sys.stderr)
    print(
        "\nThis repo is public. Take the value out and refer to it in the masked form "
        "ABCD…WXYZ. If it is a real credential and it was ever pushed, it must be rotated: "
        "tell Exec. If it is a made-up test value, build it at run time from parts so the "
        "file holds no matching run.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
