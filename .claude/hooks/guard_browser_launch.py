#!/usr/bin/env python3
# Concept: docs/internal/operations/hooks-registry.md (the guard-browser-launch row).
# Logic for guard-browser-launch.sh. Any error exits 0 (fail open); only a judged launch exits 2.
import json
import re
import shlex
import sys

FLAG = "--use-mock-keychain"
# A token that IS a Chrome or Chromium program (not a folder that merely contains one).
BROWSER = re.compile(
    r"(?:^|/)(?:Contents/MacOS/(?:Google Chrome(?: for Testing| Canary| Beta| Dev)?|Chromium)"
    r"|chrome|chromium|chromium-browser|google-chrome(?:-stable)?|chrome-headless-shell)$"
)
APP = re.compile(r"chrom(e|ium)", re.IGNORECASE)
# `$(`, `(`, `)` and backticks are separators too, so a program inside them is read (Arch).
SPLIT = re.compile(r"&&|\|\||;|\n|\||\$\(|\(|\)|`|(?<![>&\d])&(?![>&])")
TELL = re.compile(r"tell\s+application\s+\\?[\"'][^\"']*chrom", re.IGNORECASE)
WRAPPERS = {"nohup", "exec", "command", "time", "caffeinate", "setsid", "nice"}
# Commands that may NAME a browser program without starting it. Any other command with a
# browser program among its words is refused (HOST, 2026-11-17: `timeout 5 <program>`,
# `arch -arm64 <program>`, `sudo -u <user> <program>` and `xargs <program>` passed a list of
# known wrappers; an unknown wrapper must fail closed).
NOT_LAUNCHERS = {
    "ls",
    "strings",
    "file",
    "stat",
    "grep",
    "egrep",
    "rg",
    "codesign",
    "echo",
    "printf",
    "cat",
    "test",
    "[",
    "[[",
    "lsof",
    "ps",
    "pgrep",
    "pkill",
    "kill",
    "md5",
    "shasum",
    "xattr",
    "which",
    "type",
    "mdls",
    "otool",
    "plutil",
    "du",
    "wc",
    "head",
    "tail",
    "sed",
    "awk",
    "git",
    "gh",
    "brew",
    "npm",
    "npx",
    "pip",
    "pip3",
    "python",
    "python3",
    "node",
    "cd",
    "export",
    "chmod",
    "cp",
    "mv",
    "rm",
    "mkdir",
    "touch",
    "diff",
    "sort",
    "uniq",
    "tee",
    "true",
    "false",
    "dirname",
    "basename",
    "realpath",
    "readlink",
}
SHELLS = {"bash", "sh", "zsh", "/bin/bash", "/bin/sh", "/bin/zsh"}
ASSIGN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", re.DOTALL)
VAR = re.compile(r"^\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?$")


HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
FEEDS_SHELL = re.compile(r"(?:^|[\s;&|(/])(?:bash|sh|zsh|osascript)(?:\s|$)")


def without_heredoc_text(cmd):
    """The command with heredoc bodies taken out: text going to a file is not a launch
    (PA, 2026-11-17: a log entry quoting a browser command was refused). A heredoc fed
    to a shell (``bash <<EOF``) is kept, because its body does run."""
    out, end, keep = [], None, False
    for line in cmd.split("\n"):
        if end is not None:
            if line.strip() == end:
                end = None
            elif keep:
                out.append(line)
            continue
        out.append(line)
        m = HEREDOC.search(line)
        if m:
            end, keep = m.group(2), bool(FEEDS_SHELL.search(line[: m.start()]))
    return "\n".join(out)


def launches(cmd, names=None, depth=0):
    """Reasons this command is refused (empty when it is fine)."""
    names = set() if names is None else names  # variables holding a browser path
    bad = []
    cmd = without_heredoc_text(cmd)
    if TELL.search(cmd):
        bad.append("tell application")
    for seg in SPLIT.split(cmd):
        seg = seg.strip().lstrip("({ ").rstrip(")} ")
        try:
            toks = shlex.split(seg, posix=True)
        except ValueError:
            toks = seg.split()
        while toks:  # leading NAME=value words, then wrappers such as nohup or env
            m = ASSIGN.match(toks[0])
            if m:
                if BROWSER.search(m.group(2)):
                    names.add(m.group(1))
                toks = toks[1:]
            elif toks[0] in WRAPPERS:
                toks = toks[1:]
            elif toks[0] == "env":
                toks = toks[1:]
                while toks and toks[0].startswith("-"):
                    toks = toks[2:] if toks[0] == "-u" else toks[1:]
            else:
                break
        if not toks:
            continue
        word, args = toks[0], toks[1:]

        def is_program(tok):
            var = VAR.match(tok)
            return bool(BROWSER.search(tok)) or bool(var and var.group(1) in names)

        if word in SHELLS and "-c" in args and depth < 3:
            i = args.index("-c")
            if i + 1 < len(args):
                bad.extend(launches(args[i + 1], names, depth + 1))
            continue
        if word in ("open", "/usr/bin/open", "osascript", "/usr/bin/osascript"):
            # `open -a` can pass the flag after --args; osascript can't pass it at all.
            if any(APP.search(a) for a in args) and (
                word.endswith("osascript") or FLAG not in args
            ):
                bad.append(word)
            continue
        if is_program(word):
            if FLAG not in args:
                bad.append(word)
            continue
        if word.rsplit("/", 1)[-1] in NOT_LAUNCHERS:
            continue
        if depth < 3:  # `eval "<program> --x"`: a quoted argument that is itself a command
            for a in args:
                if " " in a.strip() and not is_program(a):
                    bad.extend(launches(a, names, depth + 1))
        named = [a for a in args if is_program(a)]
        if named and FLAG not in args:
            bad.append(f"{word} ... {named[0]}")
    return bad


def main():
    try:
        d = json.load(sys.stdin)
        cmd = (d.get("tool_input") or {}).get("command") or ""
        bad = launches(cmd)
    except Exception:
        return 0
    if not bad:
        return 0
    print(
        "guard-browser-launch: REFUSED. This command starts a Chrome or Chromium browser without "
        f"{FLAG}, so it could read or write xian's login keychain (his rule of 2026-11-11; "
        "2026-11-17: 'ensure it doesn't recur'). Use the browser tool, or the seat browser "
        "(scripts/seat_browser.py; Pard's LaunchAgent starts it). If you must start one by hand, "
        f"put {FLAG} among its arguments. If the command only reads the program file and was "
        "refused anyway, tell CIO; do not work around this refusal.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
