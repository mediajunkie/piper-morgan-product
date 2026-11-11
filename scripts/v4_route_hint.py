#!/usr/bin/env python3
"""Advisory for mail-send.sh: name a v3 memo that could have gone on mail v4.

Usage: v4_route_hint.py <mailbox path> [...]   (run from the repo root; prints nothing when clean)

A memo qualifies when its from: and every to:/cc: role are `pilot: true` in the mail repo's
roles.yaml (read from that repo's origin/main ref, no fetch). Each memo is named once, however many
recipient copies and sent mirrors are passed. Only files under mailboxes/<role>/inbox/ or sent/ are
read. Never blocks: exit 0 always. A missing mail repo or an unreadable roles.yaml prints nothing.

Why: 11-09 to 11-10, after v4 widened to 11 seats, 49 of 53 v3 memos had only pilot roles on both
ends and v4 carried 3. The send rule lived in prose (check-mailbox Step 1, the v4 ops doc), and
mail-send.sh, the tool every seat already reaches for, said nothing. CIO 2026-11-11.
Concept: docs/internal/operations/mail-v4-pilot.md
"""

import os
import re
import subprocess
import sys
from pathlib import Path

MAIL_REPO = Path(
    os.environ.get("PIPER_MAIL4_REPO", str(Path.home() / "Development/piper-morgan-mail"))
)
FALLBACK_END = "2026-11-23"


def pilots():
    try:
        out = subprocess.run(
            ["git", "-C", str(MAIL_REPO), "show", "origin/main:roles.yaml"],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return set()
    if out.returncode != 0:
        return set()
    return set(re.findall(r"^\s+([a-z]+):\s*\{[^}]*pilot:\s*true", out.stdout, re.M))


def roles(fm, key):
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    return set(re.findall(r"[a-z]+", m.group(1).lower())) if m else set()


def main(paths):
    p = pilots()
    if not p:
        return 0
    seen = set()
    for path in paths:
        if not re.match(r"mailboxes/[^/]+/(inbox|sent)/[^/]+\.md$", path) or path.endswith(
            "MANIFEST.md"
        ):
            continue
        name = path.rsplit("/", 1)[1]
        if name in seen:
            continue
        seen.add(name)
        try:
            text = Path(path).read_text()
        except OSError:
            continue
        m = re.match(r"---\n(.*?)\n---", text, re.S)
        if not m:
            continue
        fm = m.group(1)
        sender = roles(fm, "from")
        rcpts = roles(fm, "to") | roles(fm, "cc")
        if sender and rcpts and sender <= p and rcpts <= p:
            print(
                f"mail-send: ⚠ v4: every party to '{name}' is a mail v4 seat. Send it with "
                f"scripts/mail4.py send (docs/internal/operations/mail-v4-pilot.md); v3 is the fallback "
                f"until {FALLBACK_END}. Sending on v3 anyway; say why in your log.",
                file=sys.stderr,
            )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
