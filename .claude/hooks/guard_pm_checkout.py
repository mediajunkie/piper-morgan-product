#!/usr/bin/env python3
# Logic for guard-pm-checkout.sh (kept in its own file: embedding Python in a shell string broke on
# quotes, and a crashed hook exits 2, which would block EVERY git call; caught in testing 2026-10-04).
import json
import os
import re
import shlex
import sys

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # unparseable input: not ours to judge (fail open)
cmd = (d.get("tool_input") or {}).get("command") or ""
cwd = d.get("cwd") or os.getcwd()
pm = os.path.realpath(os.environ["PM_CHECKOUT"])


def real(p, base):
    p = os.path.expanduser(p.strip("\"'"))
    return os.path.realpath(p if os.path.isabs(p) else os.path.join(base, p))


def is_pm(p):
    return p == pm or p.startswith(pm + os.sep)


target_base = cwd
bad = []
for seg in re.split(r"&&|\|\||;|\n|\|", cmd):
    try:
        toks = shlex.split(seg, posix=True)
    except ValueError:
        toks = seg.split()
    if not toks:
        continue
    if toks[0] == "cd" and len(toks) > 1:
        target_base = real(toks[1], target_base)
        continue
    if "git" not in toks:
        continue
    i = toks.index("git")
    rest = toks[i + 1 :]
    tgt = target_base
    while rest and rest[0].startswith("-"):  # global options before the subcommand
        if rest[0] == "-C" and len(rest) > 1:
            tgt = real(rest[1], tgt)
            rest = rest[2:]
            continue
        if rest[0] == "-c" and len(rest) > 1:
            rest = rest[2:]
            continue
        rest = rest[1:]
    if not rest or not is_pm(tgt):
        continue
    sub, args = rest[0], rest[1:]
    why = None
    if sub == "checkout" and ("--" in args or "." in args):
        why = "checkout overwrites working-tree files"
    elif sub == "restore" and "--staged" not in args and "-S" not in args:
        why = "restore (without --staged) overwrites working-tree files"
    elif sub == "reset" and "--hard" in args:
        why = "reset --hard discards working-tree changes"
    elif sub == "clean" and any(a.startswith("-") and ("f" in a or "x" in a) for a in args):
        why = "clean deletes untracked files"
    elif sub == "stash" and not (args and args[0] in ("list", "show")):
        why = "stash removes working-tree changes (and the stack is shared)"
    if why:
        bad.append((seg.strip(), why))
if bad:
    for s, why in bad:
        print(
            f"BLOCKED by guard-pm-checkout (R6 step 1): `{s}` targets PM's main checkout ({pm}): {why}.",
            file=sys.stderr,
        )
    print(
        "PM edits there without committing; discarded changes are unrecoverable (CLAUDE.md HARD RULE).",
        file=sys.stderr,
    )
    print(
        "Do the work from your own worktree instead. If PM explicitly asked for this, PM runs it.",
        file=sys.stderr,
    )
    sys.exit(2)
sys.exit(0)
