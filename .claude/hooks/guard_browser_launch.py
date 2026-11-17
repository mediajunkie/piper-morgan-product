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
SPLIT = re.compile(r"&&|\|\||;|\n|\||(?<![>&\d])&(?![>&])")
WRAPPERS = {"nohup", "exec", "command", "time", "caffeinate", "setsid", "nice"}
SHELLS = {"bash", "sh", "zsh", "/bin/bash", "/bin/sh", "/bin/zsh"}
ASSIGN = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)=(.*)$", re.DOTALL)
VAR = re.compile(r"^\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?$")


def launches(cmd, names=None, depth=0):
    """Reasons this command is refused (empty when it is fine)."""
    names = set() if names is None else names  # variables holding a browser path
    bad = []
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
        var = VAR.match(word)
        is_browser = bool(BROWSER.search(word)) or bool(var and var.group(1) in names)
        if word in ("open", "/usr/bin/open") and any(APP.search(a) for a in args):
            is_browser = True
        if is_browser and FLAG not in args:
            bad.append(word if not var else "$" + var.group(1))
        elif word in SHELLS and "-c" in args and depth < 3:
            i = args.index("-c")
            if i + 1 < len(args):
                bad.extend(launches(args[i + 1], names, depth + 1))
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
        f"put {FLAG} among its arguments. Do not work around this refusal.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
