"""A script named as a bare command in an exact allow rule must be committed executable.

An exact allow such as `Bash(scripts/seat_account_create.py --account seat-github-1)` only
matches the bare command, so a `python3` prefix falls outside it, and a file without its execute
bit refuses the bare command ("permission denied"). That stopped Step F0 on 2026-11-20 (Exec,
2389): the file was committed 100644. This reads every tracked rule text outside logs and mail and
checks the git mode of each script it names that exists.
"""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ALLOW = re.compile(r"Bash\((scripts/[A-Za-z0-9_.\-/]+)")
SKIP_PREFIXES = ("dev/", "mailboxes/")


def git(*args):
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout


def named_scripts():
    found = {}
    for path in git("ls-files", "*.md", "*.json").splitlines():
        if path.startswith(SKIP_PREFIXES):
            continue
        try:
            text = (ROOT / path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for m in ALLOW.finditer(text):
            found.setdefault(m.group(1), path)
    return found


def test_allow_named_scripts_are_executable():
    named = named_scripts()
    modes = {}
    for line in git("ls-files", "-s", "--", *named).splitlines():
        meta, path = line.split("\t", 1)
        modes[path] = meta.split()[0]
    assert modes, "no allow-named script found; the pattern or the rule texts moved"
    bad = {p: f"{modes[p]} (named in {named[p]})" for p in modes if modes[p] != "100755"}
    assert not bad, f"named in an exact allow but not executable in git: {bad}"
