#!/usr/bin/env python3
"""After-the-fact check: is a Chrome or Chromium browser running without --use-mock-keychain?

xian's rule (2026-11-11): nothing a seat runs reads his login keychain without his permission.
A browser started without ``--use-mock-keychain`` makes or reads a "Safe Storage" item there
(CIO's hand launch, 2026-11-15; xian 2026-11-17: "ensure it doesn't recur"). The Bash hook
``.claude/hooks/guard-browser-launch.sh`` refuses such a launch typed into the Bash tool. This
script is for what the hook can't see: a launch from inside a script or another program.

It reads the process table of this user and prints, for each browser main process that
lacks the flag, its pid and program path. It never prints the rest of a command line.

Limits, so nobody reads it as covering more:
- It sees only what is running when it runs. A browser that started and exited in between
  is not seen.
- A browser under ``/Applications`` is taken to be xian's own and is not judged. A seat
  starting that one from a script would not be flagged here.
- It does not look at the keychain. No seat does.

Exit 0 clean, 1 if any is found, 3 if the process table could not be read.

Concept: docs/internal/operations/hooks-registry.md (the guard-browser-launch row)
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from typing import List, Optional, Tuple

FLAG = "--use-mock-keychain"
PROGRAM = re.compile(
    r"^(/(?:(?! -)[^=])*?/Contents/MacOS/(?:Google Chrome(?: for Testing| Canary| Beta| Dev)?|Chromium)"
    r"|/\S*/(?:chrome|chromium|chromium-browser|google-chrome(?:-stable)?|chrome-headless-shell))"
    r"(?= |$)"
)
OWN = ("/Applications/",)


def unflagged(table: str) -> List[Tuple[int, str]]:
    """(pid, program path) for each browser main process without the flag."""
    found = []
    for row in table.splitlines():
        parts = row.strip().split(None, 1)
        if len(parts) != 2 or not parts[0].isdigit():
            continue
        pid, command = int(parts[0]), parts[1]
        match = PROGRAM.match(command)
        if not match or "--type=" in command:  # helpers carry --type and inherit the choice
            continue
        program = match.group(1)
        if program.startswith(OWN) or f" {FLAG}" in command:
            continue
        found.append((pid, program))
    return found


def process_table() -> Optional[str]:
    try:
        done = subprocess.run(
            ["/bin/ps", "-axww", "-U", str(os.getuid()), "-o", "pid=,command="],
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    if done.returncode != 0:
        return None
    return done.stdout.decode("utf-8", errors="replace")


def main() -> int:
    table = process_table()
    if table is None:
        print("browser_keychain_check: could not read the process table; nothing was checked")
        return 3
    found = unflagged(table)
    if not found:
        print(f"browser_keychain_check: OK, no browser running without {FLAG}")
        return 0
    print(f"browser_keychain_check: FAIL, {len(found)} browser(s) running without {FLAG}:")
    for pid, program in found:
        print(f"  pid {pid}  {program}")
    print("Tell HOST and Exec. Do not look in the keychain; that is xian's call.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
