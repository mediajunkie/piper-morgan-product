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
import shlex
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


_HEREDOC_RE = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[ \t]*\n(.*?)\n[ \t]*\2\b", re.S)
_SENTINEL_RE = re.compile(r"^__HEREDOC_\d+__$")
_CAT_SENTINEL_RE = re.compile(r"^\$\(cat\s+(\S+)\s*\)$", re.S)
_GLOBAL_OPTS_WITH_ARG = ("-C", "--git-dir", "--work-tree", "-c")
# Short-flag cluster that ENDS in 'm' and whose other characters are plain
# letters (git commit's boolean short flags: -a, -s, -v, -n, -e, -q, -p, -o,
# -i, -S, ...) — e.g. `-am`, `-sm`, `-avm`. The real `-m` (len 2) is handled
# separately, before this branch is ever checked.
_SHORT_CLUSTER_ENDING_IN_M = re.compile(r"^-[A-Za-z]+m$")
_SEGMENT_BREAKS = {"&&", "||", ";", "|", "|&"}


def _legacy_commit_messages_in_bash_command(cmd: str) -> list[str]:
    """Pre-#1934 regex extraction. Kept as the fallback when shlex can't
    parse the command at all (e.g. genuinely unbalanced quoting) — never
    crash the hook; degrade to the old (narrower) behaviour instead."""
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


def _extract_heredocs(cmd: str) -> tuple[str, dict[str, str]]:
    """Replace every heredoc body in ``cmd`` with a shlex-safe sentinel word
    (``__HEREDOC_0__``, ...) and return (protected_cmd, {sentinel: body}).

    Protecting heredocs BEFORE shlex-tokenizing is what lets `-F -
    <<'EOF'...EOF` and `-m "$(cat <<'EOF'...EOF)"` survive tokenization at
    all — the raw heredoc body can contain quotes, `#N`, anything — shlex
    has no concept of heredoc syntax and would otherwise choke on or
    mis-tokenize it.
    """
    bodies: dict[str, str] = {}

    def _sub(m: re.Match[str]) -> str:
        sentinel = f"__HEREDOC_{len(bodies)}__"
        bodies[sentinel] = m.group(3)
        return sentinel

    protected = _HEREDOC_RE.sub(_sub, cmd)
    return protected, bodies


def _resolve_value(value: str, sentinels: dict[str, str]) -> str:
    """Resolve a parsed -m/--message/-F argument value that may actually be
    a heredoc sentinel (`-F -` followed by a heredoc) or a `$(cat
    __HEREDOC_N__)` wrapper (the `-m "$(cat <<'EOF'...EOF)"` idiom) back to
    the real heredoc body. Anything else passes through unchanged."""
    if value in sentinels:
        return sentinels[value]
    m = _CAT_SENTINEL_RE.match(value)
    if m and m.group(1) in sentinels:
        return sentinels[m.group(1)]
    return value


def _split_segments(tokens: list[str]) -> list[list[str]]:
    """Split a flat shlex token list into simple-command segments on shell
    control operators (&&, ||, ;, |, |&) — segment boundaries only; each
    segment is itself just a list of words for one simple command."""
    segments: list[list[str]] = []
    current: list[str] = []
    for tok in tokens:
        if tok in _SEGMENT_BREAKS:
            if current:
                segments.append(current)
            current = []
        else:
            current.append(tok)
    if current:
        segments.append(current)
    return segments


def _commit_args(segment: list[str]) -> list[str] | None:
    """If `segment` is a `git [global-opts] commit ...` invocation, return
    the argument tokens AFTER `commit`. Otherwise return None (not a commit
    invocation — e.g. `git status`, `git add`, a non-git command)."""
    # Strip leading subshell/grouping parens, if any made it through as
    # standalone tokens.
    i = 0
    while i < len(segment) and segment[i] in ("(", ")"):
        i += 1
    if i >= len(segment) or (segment[i] != "git" and not segment[i].endswith("/git")):
        return None
    i += 1
    while i < len(segment):
        tok = segment[i]
        if tok in _GLOBAL_OPTS_WITH_ARG:
            i += 2
            continue
        if tok.startswith("--git-dir=") or tok.startswith("--work-tree="):
            i += 1
            continue
        if tok.startswith("-c") and len(tok) > 2 and "=" in tok:
            i += 1  # -cuser.name=x form
            continue
        if tok == "commit":
            return segment[i + 1 :]
        if tok.startswith("-"):
            i += 1
            continue
        # First non-flag, non-"commit" token: a different subcommand.
        return None
    return None


def commit_messages_in_bash_command(cmd: str) -> list[str]:
    """The commit-message content of every `git commit` invocation in a
    (possibly compound) shell command — robust to quoting via `shlex`,
    rather than a few hand-matched regex shapes.

    Covers: `-m "..."` / `-m '...'` (repeatable — git joins multiple as
    paragraphs), the no-space attached form `-m"..."`, `--message ...` /
    `--message=...`, combined short-flag clusters ending in `m` (`-am`,
    `-sm`, `-avm`, ...), `-F <file>` (file is read if it exists), `-F -`
    followed by an inline heredoc, the `-m "$(cat <<'EOF' ... EOF)"` idiom,
    `git -C <dir> commit ...` / `git -c k=v commit ...`, and compound
    commands joined by `&&`/`;`/`|`/`||`. A heredoc elsewhere in the command
    that merely mentions an incident subject (writing a *file*, not a commit
    message) is never picked up — only a heredoc actually reachable from
    `-F -` or `-m "$(cat ...)"` is.

    Falls back to the pre-#1934 regex extraction (never crashes) if shlex
    cannot tokenize the command at all, and says so on stderr.
    """
    # Fast path only — NOT "git commit" as a substring: `git -C <dir> commit`
    # and `git -c k=v commit` put other text between the two words, which is
    # exactly the #1934 gap this rewrite closes. "commit" alone is cheap and
    # cannot false-negative (every shape below needs the literal word).
    if "commit" not in cmd:
        return []
    try:
        protected, sentinels = _extract_heredocs(cmd)
        tokens = shlex.split(protected, posix=True)
    except ValueError as e:
        sys.stderr.write(
            f"check_autoclose_keywords: could not parse the command as shell words ({e}); "
            "falling back to regex extraction — some shapes may be missed.\n"
        )
        return _legacy_commit_messages_in_bash_command(cmd)

    out: list[str] = []
    for segment in _split_segments(tokens):
        args = _commit_args(segment)
        if args is None:
            continue
        j = 0
        while j < len(args):
            tok = args[j]
            if tok in ("-m", "--message"):
                if j + 1 < len(args):
                    out.append(_resolve_value(args[j + 1], sentinels))
                j += 2
                continue
            if tok.startswith("--message="):
                out.append(_resolve_value(tok[len("--message=") :], sentinels))
                j += 1
                continue
            if tok.startswith("-m") and len(tok) > 2:
                # Attached form: `-m"..."` / `-m'...'` — shlex has already
                # stripped the quotes and merged it into one token.
                out.append(_resolve_value(tok[2:], sentinels))
                j += 1
                continue
            if _SHORT_CLUSTER_ENDING_IN_M.match(tok):
                # `-am`, `-sm`, `-avm`, ... — the message is the next token.
                if j + 1 < len(args):
                    out.append(_resolve_value(args[j + 1], sentinels))
                j += 2
                continue
            if tok in ("-F", "--file"):
                if j + 1 >= len(args):
                    j += 1
                    continue
                val = args[j + 1]
                if val == "-":
                    if j + 2 < len(args) and _SENTINEL_RE.match(args[j + 2]):
                        out.append(sentinels[args[j + 2]])
                        j += 3
                    else:
                        sys.stderr.write(
                            "check_autoclose_keywords: '-F -' with no inline heredoc found "
                            "— cannot read actual stdin content statically; skipped.\n"
                        )
                        j += 2
                    continue
                resolved = _resolve_value(val, sentinels)
                p = Path(resolved)
                try:
                    if p.is_file():
                        out.append(p.read_text(errors="replace"))
                except OSError:
                    pass
                j += 2
                continue
            if tok.startswith("--file="):
                val = tok[len("--file=") :]
                if val == "-":
                    sys.stderr.write(
                        "check_autoclose_keywords: '--file=-' with no inline heredoc found "
                        "— cannot read actual stdin content statically; skipped.\n"
                    )
                    j += 1
                    continue
                resolved = _resolve_value(val, sentinels)
                p = Path(resolved)
                try:
                    if p.is_file():
                        out.append(p.read_text(errors="replace"))
                except OSError:
                    pass
                j += 1
                continue
            j += 1
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
