#!/usr/bin/env python3
"""mailbox_bearer_lint.py — no bearer credential may travel through the repo (#1845).

The rule (proposed 2026-09-22, PM to ratify; this is the mechanical backstop the
issue asked the Lead for): **invite codes and any bearer credential NEVER travel
through `mailboxes/` or any other repo-committed surface.** A memo may name a
credential by its MASKED form only — `ZVHW…8B35` (first 4, an ellipsis, last 4).
The repo is public; an invite code sat exposed for eight days before this rule.

What counts as a bearer credential here (the shapes that have actually leaked
or could):

- an **invite token**: 24 chars of Crockford Base32 (`services/auth/
  invite_token_service.py`: alphabet 0-9 A-Z minus I L O U, length 24), matched
  with or without the cosmetic dashes/spaces of a distribution copy;
- an **API key / bot token** by its well-known prefix: `sk-ant-`, `sk-`,
  `xoxb-`/`xoxp-`/`xapp-` (Slack), `ghp_`/`gho_`/`github_pat_` (GitHub),
  `AIza` (Google), `fo1_`/`FlyV1` (Fly).

Masked forms are allowed: a 4-char prefix, an ellipsis (… or ...), a 4-char
suffix. A `--baseline` file lists historical hits by `path:sha1(line)` so the
gate only blocks NEW ones (the same ratchet shape as mailbox_filename_lint.py).

Exit 1 on any unbaselined hit; the offending path and a masked excerpt are
printed — never the credential itself.

Usage:
    scripts/mailbox_bearer_lint.py                    # scan mailboxes/ (default)
    scripts/mailbox_bearer_lint.py --baseline FILE    # ratchet against baseline
    scripts/mailbox_bearer_lint.py --write-baseline FILE
    scripts/mailbox_bearer_lint.py --roots mailboxes docs dev
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

CROCKFORD = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
TOKEN_LENGTH = 24

# A 24-char Crockford run, optionally dash/space-grouped (4-4-4-4-4-4 or any
# grouping), in EITHER case (uppercase as minted, or a lowercased paste —
# mixed case is rejected in _is_token_run). Word-bounded so longer ids and
# shas don't match; a 24-char all-hex run is rejected in _is_token_run.
# Requires at least one digit AND one letter so an all-caps English word run
# can't match.
_CROCKFORD_RUN = re.compile(
    r"(?<![A-Za-z0-9])(?:[" + CROCKFORD + r"][- ]?){" + str(TOKEN_LENGTH) + r"}(?![A-Za-z0-9])",
    re.IGNORECASE,  # 1845 second review (HOST, 09-24): a lowercased paste slipped through
)
_HEX_ONLY = re.compile(r"^[0-9a-f]+$", re.IGNORECASE)
_PREFIXED_KEY = re.compile(
    r"(?<![A-Za-z0-9_])"
    r"(?:sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9_-]{20,}"
    r"|xox[bpa]-[A-Za-z0-9-]{10,}|xapp-[A-Za-z0-9-]{10,}"
    r"|ghp_[A-Za-z0-9]{20,}|gho_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}"
    r"|AIza[0-9A-Za-z_-]{30,}|fo1_[A-Za-z0-9_-]{20,}|FlyV1 [A-Za-z0-9_=+/-]{20,})"
)
# Masked form: 4 chars, an ellipsis, 4 chars — allowed, and also what we print.
_MASKED = re.compile(
    r"\b[" + CROCKFORD + r"]{4}(?:…|\.\.\.)[" + CROCKFORD + r"]{4}\b", re.IGNORECASE
)

_SKIP_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".pdf",
    ".webp",
    ".ico",
    ".svg",
    ".pptx",
    ".docx",
    ".xlsx",
    ".zip",
    ".gz",
    ".tgz",
    ".pyc",
    ".woff",
    ".woff2",
    ".ttf",
}
_SKIP_NAMES = {"MANIFEST.md"}  # regenerated; never carries body text


def _is_token_run(candidate: str) -> bool:
    core = re.sub(r"[- ]", "", candidate)
    if len(core) != TOKEN_LENGTH:
        return False
    has_digit = any(c.isdigit() for c in core)
    has_alpha = any(c.isalpha() for c in core)
    if not (has_digit and has_alpha):
        return False
    # Tokens are minted uppercase; a lowercased copy is the same credential
    # (HOST's 09-24 gap). A MIXED-case run is not — that is a base62 id
    # (session ids, object ids), and a lowercase all-hex run is a truncated
    # sha/hash, not a token (a real Crockford token is all-hex with
    # probability 2^-24). Both would otherwise become false positives the
    # moment the class went case-insensitive.
    if not (core.isupper() or core.islower()):
        return False
    # A lowercase run must be CONTIGUOUS: with grouping allowed, hyphenated
    # prose with a digit in it ("phase0-assessment-…") matched 357 times on
    # the first case-insensitive pass. Tokens are minted ungrouped, and a
    # lowercased paste keeps that shape; only the as-minted uppercase form
    # gets the display-grouping tolerance.
    if core.islower() and core != candidate:
        return False
    # An obviously-fake placeholder ("XXXX0000XXXX0000XXXX0000", the shape HOST
    # recommended for synthetic examples on 2026-09-25 — and the memo saying
    # so tripped this gate) is built from a handful of distinct characters. A
    # minted token is 24 draws from a 32-symbol alphabet: fewer than 8 distinct
    # characters has probability far below 1e-9. Below that, it is a mock.
    if len(set(core.upper())) < 8:
        return False
    return not _HEX_ONLY.match(core)


def mask(credential: str) -> str:
    core = re.sub(r"[- ]", "", credential)
    return f"{core[:4]}…{core[-4:]}" if len(core) >= 8 else "…"


def scan_line(line: str) -> list[str]:
    """Return the bearer credentials found in ``line`` (unmasked, for hashing)."""
    hits: list[str] = []
    # Strip allowed masked forms first so they can't be mistaken for anything.
    stripped = _MASKED.sub("", line)
    for m in _CROCKFORD_RUN.finditer(stripped):
        if _is_token_run(m.group(0)):
            hits.append(m.group(0))
    hits.extend(m.group(0) for m in _PREFIXED_KEY.finditer(stripped))
    return hits


def _tracked_files(roots: list[Path], repo_root: Path) -> list[Path]:
    """Only git-TRACKED files: the rule is about what the public repo carries.
    A gitignored roster (dev/alpha/invite-tokens-*.md, chmod 600) is exactly
    where a credential is allowed to live and must not trip this."""
    import subprocess

    rels = [r.relative_to(repo_root).as_posix() for r in roots if r.exists()]
    if not rels:
        return []
    out = subprocess.run(
        ["git", "-C", str(repo_root), "ls-files", "-z", "--", *rels],
        capture_output=True,
        check=False,
    ).stdout.decode("utf-8", errors="ignore")
    return [repo_root / p for p in out.split("\0") if p]


def scan(roots: list[Path], repo_root: Path) -> list[tuple[str, int, str]]:
    """(relative path, line number, credential) for every hit in the tracked
    files under ``roots``."""
    found: list[tuple[str, int, str]] = []
    for path in _tracked_files(roots, repo_root):
        if not path.is_file() or path.suffix.lower() in _SKIP_SUFFIXES:
            continue
        if path.name in _SKIP_NAMES or ".git" in path.parts:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = path.relative_to(repo_root).as_posix()
        for lineno, line in enumerate(text.splitlines(), 1):
            for cred in scan_line(line):
                found.append((rel, lineno, cred))
    return found


def _key(rel: str, cred: str) -> str:
    # Hash the credential so the baseline itself never stores one.
    return f"{rel}:{hashlib.sha1(cred.encode()).hexdigest()[:12]}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--roots", nargs="*", default=["mailboxes"], help="directories to scan")
    ap.add_argument("--baseline", type=Path, help="ratchet: ignore hits listed here")
    ap.add_argument("--write-baseline", type=Path, help="write current hits as the baseline")
    args = ap.parse_args(argv)

    repo_root = Path(__file__).resolve().parents[1]
    roots = [repo_root / r for r in args.roots]
    hits = scan(roots, repo_root)

    if args.write_baseline:
        keys = sorted({_key(rel, cred) for rel, _, cred in hits})
        args.write_baseline.write_text("\n".join(keys) + ("\n" if keys else ""))
        print(f"mailbox_bearer_lint: baseline written — {len(keys)} historical hit(s)")
        return 0

    baseline: set[str] = set()
    if args.baseline and args.baseline.exists():
        baseline = {ln.strip() for ln in args.baseline.read_text().splitlines() if ln.strip()}

    new = [(rel, ln, cred) for rel, ln, cred in hits if _key(rel, cred) not in baseline]
    scanned = ", ".join(args.roots)
    if not new:
        print(
            f"mailbox_bearer_lint: OK — no new bearer credential under {scanned} "
            f"({len(hits)} baselined historical hit(s), {len(baseline)} baseline entries)"
        )
        return 0

    print(
        f"mailbox_bearer_lint: FAIL — {len(new)} bearer credential(s) in repo-committed text (#1845):"
    )
    for rel, ln, cred in new:
        print(f"  {rel}:{ln}  {mask(cred)}")
    print(
        "\nBearer credentials (invite codes, API keys, bot tokens) never travel through "
        "mailboxes/ or any committed surface — the repo is public. Deliver them in "
        "PM's private conversation or the gitignored roster; reference them in a memo "
        "by MASKED form only (ABCD…WXYZ). Remove the credential, rotate it if it was "
        "ever pushed, then re-run.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
