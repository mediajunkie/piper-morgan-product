#!/usr/bin/env python3
"""check_autoclose_keywords.py — refuse a commit/mail message that would either
(a) auto-close an issue by accident (#1691), or (b) carry a bearer credential (#1845).

GitHub's auto-close parser treats ``close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved``
followed (within a few tokens) by ``#N`` in a commit message pushed to the default branch as a
command to close issue N — **regardless of surrounding wording**. "not yet resolved: #1278"
closed a live Beta Blocker (2026-07); "ask(ppm): close #1677/#1488 properly" closed #1677 from a
MAIL commit subject (2026-08-28) that nobody meant as a decision. The documented gotcha in
CLAUDE.md failed to prevent it twice; this is the mechanism.

Rule (a): a close-keyword within THREE tokens before ``#N`` (or ``owner/repo#N``, or a full issue
URL) is refused unless the message opts in with the trailer ``Auto-Close: intentional`` (a genuine
fix commit that means to close the issue). Rewording is the normal fix: "closed-out" → "done",
"fix for 1234" → "fix (issue 1234)" — writing the number without ``#`` never trips the parser.

Rule (b), added R5/#1845-security (2026-10-04): a commit subject sat with a tester's name and a
full invite token in plaintext on main (``7941ae4b97``) because ``mailbox_bearer_lint.py`` reads
*files*, not commit messages — a message is just as committed and just as public. This script
already extracts "the message, however it arrived" for both doorways below, so it is the natural
place to run the SAME bearer-credential scan: it imports ``scan_line``/``mask`` from
``mailbox_bearer_lint`` rather than re-deriving the credential-shape regexes. The ``Auto-Close:
intentional`` opt-in only waives rule (a); it never waives rule (b) — there is no legitimate reason
for a real credential to be in a message, masked or not.

Both doorways (same as before): mail-send.sh's commit-tree path (bypasses git hooks entirely) and
the ``autoclose-guard.sh`` PreToolUse hook on ``git commit``.

Exit 0 = safe, 1 = refused (reasons on stderr; a bearer hit is printed MASKED only, never in full).
Usage:
    scripts/check_autoclose_keywords.py "message text"      # argument
    printf '%s' "message" | scripts/check_autoclose_keywords.py -   # stdin
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Shared bearer-credential detector (#1845) — one definition of "what a real
# credential shape looks like," reused here rather than duplicated.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mailbox_bearer_lint import mask, scan_line  # noqa: E402

KEYWORDS = r"(?:close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)"
# keyword, then up to three short tokens (GitHub tolerates e.g. "fixes issue #12", "closes: #12"),
# then #N / owner/repo#N / an issue URL.
_PATTERN = re.compile(
    r"\b" + KEYWORDS + r"\b[\s:,-]*(?:\S+[\s,]+){0,3}?"
    r"(?:#\d+|[\w.-]+/[\w.-]+#\d+|https?://github\.com/[\w.-]+/[\w.-]+/issues/\d+)",
    re.IGNORECASE,
)
_OPT_IN = re.compile(r"^\s*Auto-Close:\s*intentional\s*$", re.IGNORECASE | re.MULTILINE)


def find_hits(message: str) -> list[str]:
    return [m.group(0) for m in _PATTERN.finditer(message)]


def bearer_hits_in_message(message: str) -> list[str]:
    """Bearer-credential shapes (invite tokens, API keys) found in a
    commit/mail message (#1845). Scans line-by-line with
    ``mailbox_bearer_lint.scan_line`` — the same function the file-based
    lint uses — so a credential shape is defined in exactly one place.
    Returns the credentials UNMASKED (for the caller to mask on print);
    never log or return these directly to a human-visible surface without
    calling ``mask()`` first.
    """
    hits: list[str] = []
    for line in message.splitlines():
        hits.extend(scan_line(line))
    return hits


def commit_messages_in_bash_command(cmd: str) -> list[str]:
    """The commit-message arguments of a `git commit` shell command — ONLY those.

    `-m "$(cat <<'EOF' … EOF)"` bodies, `-m "…"` (may span lines), `-m '…'`. A
    heredoc elsewhere in the command that merely mentions an incident subject is
    not a commit message; the first version of the PreToolUse doorway scanned the
    whole command and blocked exactly that.
    """
    if "git commit" not in cmd:
        return []
    out: list[str] = []
    for m in re.finditer(r"-m\s+\"\$\(cat\s+<<-?'?(\w+)'?\s*\n(.*?)\n\1\s*\)\"", cmd, re.S):
        out.append(m.group(2))
    for m in re.finditer(r"-m\s+\"((?:[^\"\\]|\\.)*)\"", cmd, re.S):
        if "$(cat" not in m.group(1):
            out.append(m.group(1))
    for m in re.finditer(r"-m\s+'([^']*)'", cmd, re.S):
        out.append(m.group(1))
    return out


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[1] == "--bash-tool-input":
        # PreToolUse doorway: the Bash tool's JSON on stdin; check only the -m messages.
        import json

        try:
            cmd = json.load(sys.stdin).get("tool_input", {}).get("command", "")
        except Exception:
            return 0
        message = "\n---MSG---\n".join(commit_messages_in_bash_command(cmd))
        if not message:
            return 0
    elif len(argv) < 2 or argv[1] == "-":
        message = sys.stdin.read()
    else:
        message = " ".join(argv[1:])
    autoclose_hits = find_hits(message)
    autoclose_blocked = bool(autoclose_hits) and not _OPT_IN.search(message)
    # #1845: bearer-credential scan runs unconditionally — the Auto-Close
    # opt-in waives the close-keyword concern only; it is not and must
    # never become a way to push a real credential through.
    bearer_hits = bearer_hits_in_message(message)

    if not autoclose_blocked and not bearer_hits:
        return 0

    if autoclose_blocked:
        sys.stderr.write(
            "auto-close guard (#1691): this message would CLOSE an issue on push — GitHub's parser "
            "ignores wording:\n"
        )
        for h in autoclose_hits:
            sys.stderr.write(f"  {h!r}\n")
        sys.stderr.write(
            "Reword (write the number without '#', or move the keyword away from it), or, if this "
            "commit genuinely closes the issue, add the trailer line exactly:\n"
            "  Auto-Close: intentional\n"
        )

    if bearer_hits:
        sys.stderr.write(
            "bearer-credential guard (#1845): this message carries what looks like a real "
            "credential (invite token / API key) — a commit or mail message is a committed, "
            "public surface, same rule as mailboxes/:\n"
        )
        for cred in bearer_hits:
            sys.stderr.write(f"  {mask(cred)}\n")
        sys.stderr.write(
            "Remove it, or replace it with the masked form (ABCD…WXYZ); rotate the credential "
            "if it was ever pushed. The Auto-Close opt-in does NOT waive this.\n"
        )

    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
