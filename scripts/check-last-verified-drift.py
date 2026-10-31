#!/usr/bin/env python3
"""check-last-verified-drift.py: surface un-bumped edits and bare frontmatter bumps (#1726).

check-staleness.py (#972) says how OLD a doc's last_verified is. It cannot see two failure modes
the weekly audits kept naming (five weeks running, #1475 to #1724):

  EDITED-UNBUMPED  the body changed after last_verified, so the stamp no longer vouches for
                   the text that is there now.
  BARE-BUMP        last_verified was moved forward in a commit that changed no body text.
                   That is legitimate when someone re-read the doc and found it right, and it
                   is the drive-by stamp when no one did. The script cannot tell, so it lists
                   them with the commit so a human can ask "who read it?".

Same doc set as check-staleness.py. Warn-only: always exits 0 (per #972 and #1726).

Usage:
  scripts/check-last-verified-drift.py              # default doc set
  scripts/check-last-verified-drift.py path ...     # explicit files or globs
  DRIFT_MARGIN_DAYS=2 scripts/check-last-verified-drift.py
"""

import datetime
import importlib.util
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("check_staleness", os.path.join(HERE, "check-staleness.py"))
cs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cs)

MARGIN = int(os.environ.get("DRIFT_MARGIN_DAYS", "2"))
DEPTH = 25  # most recent commits per file to examine


def git(*args):
    r = subprocess.run(["git", "-C", cs.REPO, *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def split(text):
    """(frontmatter dict-ish lines, body) of a document's text."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4 :]
    return "", text


def fm_value(fm_text, key):
    for line in fm_text.splitlines():
        k, _, v = line.partition(":")
        if k.strip() == key:
            return v.strip().strip('"').strip("'")
    return ""


def history(rel):
    """[(sha, date)] newest first for the file."""
    out = git("log", f"-n{DEPTH}", "--format=%h\t%cs", "--follow", "--", rel)
    return [tuple(l.split("\t")) for l in out.splitlines() if "\t" in l]


def analyse(rel):
    commits = history(rel)
    last_body_edit = None  # (sha, date) newest commit that changed the body
    last_bare_bump = None  # (sha, date) newest commit that changed last_verified but not the body
    for i, (sha, date) in enumerate(commits):
        new = git("show", f"{sha}:{rel}")
        old = git("show", f"{commits[i + 1][0]}:{rel}") if i + 1 < len(commits) else ""
        nfm, nbody = split(new)
        ofm, obody = split(old)
        body_changed = nbody.strip() != obody.strip()
        lv_changed = fm_value(nfm, "last_verified") != fm_value(ofm, "last_verified")
        if body_changed and last_body_edit is None:
            last_body_edit = (sha, date)
        if lv_changed and not body_changed and last_bare_bump is None and old:
            last_bare_bump = (sha, date)
        if last_body_edit and last_bare_bump:
            break
    return last_body_edit, last_bare_bump


def main():
    paths = cs.collect(sys.argv[1:] or cs.DEFAULT_GLOBS)
    unbumped, bare = [], []
    for p in paths:
        rel = os.path.relpath(p, cs.REPO)
        fm = cs.frontmatter(p)
        lv = cs.parse_date(fm.get("last_verified"))
        if not lv:
            continue
        edit, bump = analyse(rel)
        lu = cs.parse_date(fm.get("last_updated"))
        newest_stamp = max(d for d in (lv, lu) if d)  # a fresh last_updated also dates the edit
        if edit:
            ed = datetime.date.fromisoformat(edit[1])
            if (ed - newest_stamp).days > MARGIN:
                unbumped.append((rel, f"body edited {edit[1]} ({edit[0]}), newest stamp {newest_stamp}"))
        if bump:
            bare.append((rel, f"last_verified moved with no body change on {bump[1]} ({bump[0]}), now {lv}"))

    print(f"check-last-verified-drift: {len(paths)} doc(s), margin {MARGIN}d, {cs.datetime.date.today()}")
    for title, items in (
        ("EDITED-UNBUMPED: body changed after last_verified, the stamp no longer covers the text", unbumped),
        ("BARE-BUMP: stamp moved with no edit, ask who re-read it (fine if someone did)", bare),
    ):
        if items:
            print(f"\n{title} ({len(items)}):")
            for rel, why in items:
                print(f"  - {rel}: {why}")
    if not unbumped and not bare:
        print("\nNo drift found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
