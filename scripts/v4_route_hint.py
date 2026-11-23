#!/usr/bin/env python3
"""mail-send.sh's route check: refuse a v3 memo whose every party is a mail v4 seat.

Usage: v4_route_hint.py <mailbox path> [...]   (run from the repo root; prints nothing when clean)

A memo qualifies when its from: and every to:/cc: role are `pilot: true` in the mail repo's
roles.yaml (read from that repo's origin/main ref, no fetch). Each memo is named once, however many
recipient copies and sent mirrors are passed. Only files under mailboxes/<role>/inbox/ or sent/ are
read. Exit 2 refuses the send. Exit 0 otherwise, and a missing mail repo or an unreadable roles.yaml
prints nothing and lets the send through (fail open, so a broken mail repo can't stop the fallback).

Refuses since 2026-11-23 (the v4 review, dev/2026/11/23/mail-v4-review-2026-11-23.md: the v3
fallback ended for mail between seats in this repo, and Exec moved the Ship kickoff to v4 in
8d0b8a1fb2). Before that it only warned. When v4 itself is broken, set PIPER_V3_FALLBACK to the
reason: the send goes through with the reason printed, and the sender writes it in their log.

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
FALLBACK_ENV = "PIPER_V3_FALLBACK"


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
    hits = []
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
            hits.append(name)
    if not hits:
        return 0
    reason = os.environ.get(FALLBACK_ENV, "").strip()
    for name in hits:
        if reason:
            print(
                f"mail-send: v4: every party to '{name}' is a mail v4 seat. Sending on v3 because "
                f"{FALLBACK_ENV} is set ({reason!r}). Write that reason in your log.",
                file=sys.stderr,
            )
        else:
            print(
                f"mail-send: REFUSED: every party to '{name}' is a mail v4 seat, and the v3 fallback "
                f"ended 2026-11-23. Send it with scripts/mail4.py send "
                f"(docs/internal/operations/mail-v4-pilot.md). If v4 itself is broken, set "
                f"{FALLBACK_ENV}='<why>' and say why in your log.",
                file=sys.stderr,
            )
    return 0 if reason else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
