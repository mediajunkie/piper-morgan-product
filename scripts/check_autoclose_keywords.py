#!/usr/bin/env python3
"""check_autoclose_keywords.py — refuse a commit message that would close an issue by accident (#1691).

GitHub's auto-close parser treats ``close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved``
followed (within a few tokens) by ``#N`` in a commit message pushed to the default branch as a
command to close issue N — **regardless of surrounding wording**. "not yet resolved: #1278"
closed a live Beta Blocker (2026-07); "ask(ppm): close #1677/#1488 properly" closed #1677 from a
MAIL commit subject (2026-08-28) that nobody meant as a decision. The documented gotcha in
CLAUDE.md failed to prevent it twice; this is the mechanism.

Rule: a close-keyword within THREE tokens before ``#N`` (or ``owner/repo#N``, or a full issue
URL) is refused unless the message opts in with the trailer ``Auto-Close: intentional`` (a genuine
fix commit that means to close the issue). Rewording is the normal fix: "closed-out" → "done",
"fix for 1234" → "fix (issue 1234)" — writing the number without ``#`` never trips the parser.

Exit 0 = safe, 1 = refused (reasons on stderr). Usage:
    scripts/check_autoclose_keywords.py "message text"      # argument
    printf '%s' "message" | scripts/check_autoclose_keywords.py -   # stdin
"""

from __future__ import annotations

import re
import sys

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
    hits = find_hits(message)
    if not hits:
        return 0
    if _OPT_IN.search(message):
        return 0
    sys.stderr.write(
        "auto-close guard (#1691): this message would CLOSE an issue on push — GitHub's parser "
        "ignores wording:\n"
    )
    for h in hits:
        sys.stderr.write(f"  {h!r}\n")
    sys.stderr.write(
        "Reword (write the number without '#', or move the keyword away from it), or, if this "
        "commit genuinely closes the issue, add the trailer line exactly:\n"
        "  Auto-Close: intentional\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
