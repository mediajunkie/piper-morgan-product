"""1691 — the auto-close guard: a commit message that would close an issue by
accident is refused; a genuine fix opts in with a trailer.

Two real incidents pinned verbatim: 'not yet resolved: #1278' (2026-07, a live
Beta Blocker closed) and 'ask(ppm): close #1677/#1488 properly' (2026-08-28, a
MAIL subject closed #1677 — nobody decided anything). Layer: the checker
script's own function + its CLI exit code; the two doorways (mail-send.sh's
commit-tree path and the PreToolUse hook on `git commit`) are pinned by
running them, not by config presence.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "scripts" / "check_autoclose_keywords.py"
HOOK = REPO / ".claude" / "hooks" / "autoclose-guard.sh"

sys.path.insert(0, str(REPO / "scripts"))
from check_autoclose_keywords import find_hits  # noqa: E402

_KW = "clo" + "se"  # assembled so this file's own text never reads as an auto-close command
_FIX = "fi" + "xes"
_RES = "reso" + "lved"

REFUSED = (
    f"ask(ppm): {_KW} #1677/#1488 properly, test-sequencing discussion, #1522 dispatch read",
    f"not yet {_RES}: #1278",
    "fix: resol" + "ves mediajunkie/piper-morgan-product#12",
    f"{_FIX.capitalize()} https://github.com/mediajunkie/piper-morgan-product/issues/99",
    f"{_KW}s: #40 and #41",
    "this FI" + "XED issue #7 for real",
)

PASSES = (
    "fix(intent): render == data at 13 sites, refs 1762",
    "fix(web): the composer grows (issue 1737)",
    "docs(lead): 1877 closed, 1838 traced — log",
    "chore: 1723 disposed; 1867 census",
    f"feat: {_KW}s the loop on the standup skill",  # keyword, no #N
    f"fix(auth): expired token honesty — {_KW}s #1520\n\nAuto-Close: intentional",
)


@pytest.mark.parametrize("message", REFUSED)
def test_refused(message):
    assert find_hits(message), message
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "-"], input=message, capture_output=True, text=True
    )
    assert r.returncode == 1, (message, r.stderr)
    assert "Auto-Close: intentional" in r.stderr  # the escape hatch is named


@pytest.mark.parametrize("message", PASSES)
def test_passes(message):
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "-"], input=message, capture_output=True, text=True
    )
    assert r.returncode == 0, (message, r.stderr)


def _hook(command: str) -> subprocess.CompletedProcess:
    payload = json.dumps({"tool_input": {"command": command}})
    return subprocess.run(
        ["bash", str(HOOK)], input=payload, capture_output=True, text=True, cwd=REPO
    )


def test_git_commit_doorway_blocks_the_incident_subject():
    r = _hook(f'git commit -m "ask(ppm): {_KW} #1677 properly" -- a.md')
    assert r.returncode == 2 and "BLOCKED" in r.stdout


def test_git_commit_doorway_lets_a_reworded_subject_through():
    r = _hook('git commit -m "ask(ppm): about issue 1677, closing later" -- a.md')
    assert r.returncode == 0


def test_git_commit_doorway_reads_only_the_message_not_the_whole_command():
    """A heredoc that WRITES a file mentioning the incident subject is not a
    commit message — the first hook version blocked exactly that."""
    cmd = (
        "cat > note.md <<'EOF'\n"
        f"the subject '{_KW} #1677' was the incident\n"
        "EOF\n"
        'git commit -m "docs: note about the 1677 incident" -- note.md'
    )
    assert _hook(cmd).returncode == 0


def test_git_commit_doorway_reads_a_heredoc_message():
    cmd = "git commit -m \"$(cat <<'EOF'\n" f"feat: {_KW}s #1520 for real\n" "EOF\n" ')" -- a.md'
    assert _hook(cmd).returncode == 2


def test_mail_send_doorway_refuses_before_any_push():
    """The commit-tree path — the one the 08-28 incident used and git hooks can't see."""
    r = subprocess.run(
        [
            "bash",
            str(REPO / "scripts" / "mail-send.sh"),
            f"mail(x): {_KW} #1677 properly (probe)",
            "mailboxes/lead/sent/does-not-exist.md",
        ],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert r.returncode == 1
    assert "auto-close" in r.stderr.lower() and "Nothing was sent" in r.stderr
