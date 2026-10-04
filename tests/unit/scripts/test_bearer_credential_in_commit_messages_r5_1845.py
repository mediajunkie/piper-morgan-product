"""R5/#1845-security (2026-10-04) — the bearer-credential check extended to
commit/mail MESSAGES, not just files.

`mailbox_bearer_lint.py` scans files; it never looked at the message itself,
and a full invite token sat in a commit SUBJECT on main (`7941ae4b97`,
2026-07-09) as a result. `scripts/check_autoclose_keywords.py` already
extracts "the message, however it arrived" at both doorways (mail-send.sh's
commit-tree path and the `autoclose-guard.sh` PreToolUse hook on `git
commit`), so this reuses that extraction and the EXISTING bearer-shape
detector (`mailbox_bearer_lint.scan_line`/`mask`) rather than re-deriving the
credential regexes.

Layer: the function in isolation, then both doorways by actually running
them (subprocess), per this repo's existing pattern in
test_check_autoclose_keywords_1691.py and test_mailbox_bearer_lint_1845.py.
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
from check_autoclose_keywords import bearer_hits_in_message, mask  # noqa: E402

# A synthetic 24-char Crockford token (never minted) — same fixture as
# test_mailbox_bearer_lint_1845.py, so the two suites agree on what "a real
# credential shape" means.
TOKEN = "9EA0V9VPHS9CFRTKH873EGJ6"
MASKED = mask(TOKEN)  # "9EA0…EGJ6"

CREDENTIAL_MESSAGES = (
    f"mail(ppm): invite code for the new tester is {TOKEN}",
    f"docs(lead): rotate key sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123 before merge",
    f"fix(auth): hardcode ghp_abcdefghijklmnopqrstuvwxyz0123 for local testing",
    f"chore: paste the lowercased token {TOKEN.lower()} into the roster",
)

SAFE_MESSAGES = (
    "fix(intent): render == data at 13 sites, refs 1762",
    "docs(lead): 1877 closed, 1838 traced — log",
    f"mail(lead): the invite token is masked as {MASKED} in the roster",
    "fix: dedupe commit 7941ae4b97 against main",  # a real git sha from the incident, not a token
    "chore: full sha c3d1d8b54c0f1a2b3d4e5f60718293a4b5c6d7e8 referenced",  # 40-char hex sha
    "docs: issue #1845 and #1691 both apply here",
    "feat: session id 9eA0V9VpHs9cFrTkH873EgJ6 is a base62 id, not a token",  # mixed case
)


@pytest.mark.parametrize("message", CREDENTIAL_MESSAGES)
def test_bearer_hits_in_message_detects_credential_shapes(message):
    assert bearer_hits_in_message(message), message


@pytest.mark.parametrize("message", SAFE_MESSAGES)
def test_bearer_hits_in_message_has_no_false_positives(message):
    assert bearer_hits_in_message(message) == [], message


@pytest.mark.parametrize("message", CREDENTIAL_MESSAGES)
def test_cli_refuses_and_never_prints_the_full_credential(message):
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "-"], input=message, capture_output=True, text=True
    )
    assert r.returncode == 1, (message, r.stderr)
    assert "#1845" in r.stderr
    assert TOKEN not in r.stderr and TOKEN.lower() not in r.stderr
    # every well-known key prefix in the fixtures is short enough that the
    # masked form (prefix…suffix) is what should appear, not the raw value
    assert "…" in r.stderr


@pytest.mark.parametrize("message", SAFE_MESSAGES)
def test_cli_passes_safe_messages(message):
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "-"], input=message, capture_output=True, text=True
    )
    assert r.returncode == 0, (message, r.stderr)


def test_auto_close_opt_in_does_not_waive_a_bearer_hit():
    """The escape hatch for #1691 is narrowly scoped: it must not become a
    way to push a real credential through under cover of 'intentional'."""
    message = f"fix(auth): rotates #1520\n\nAuto-Close: intentional\n\ntoken: {TOKEN}"
    r = subprocess.run(
        [sys.executable, str(SCRIPT), "-"], input=message, capture_output=True, text=True
    )
    assert r.returncode == 1, r.stderr
    assert "#1845" in r.stderr
    assert TOKEN not in r.stderr


def _hook(command: str) -> subprocess.CompletedProcess:
    payload = json.dumps({"tool_input": {"command": command}})
    return subprocess.run(
        ["bash", str(HOOK)], input=payload, capture_output=True, text=True, cwd=REPO
    )


def test_git_commit_doorway_blocks_a_credential_in_the_message():
    r = _hook(f'git commit -m "mail(ppm): invite code is {TOKEN}" -- a.md')
    assert r.returncode == 2
    # #1934: the block reason moved to STDERR — a PreToolUse hook's stdout on
    # exit 2 never reaches the committer through this harness (HOST verified
    # behaviorally: 455 bytes on stdout, 0 on stderr, before this fix).
    assert "BLOCKED" in r.stderr
    assert r.stdout == ""
    assert TOKEN not in r.stdout and TOKEN not in r.stderr


def test_git_commit_doorway_lets_a_masked_credential_through():
    r = _hook(f'git commit -m "mail(ppm): invite code for the roster is {MASKED}" -- a.md')
    assert r.returncode == 0


def test_mail_send_doorway_refuses_a_credential_in_the_subject_before_any_push():
    """The commit-tree path git hooks can't see — same doorway #1691 uses,
    and the one the 2026-07-09 incident (#1845) actually went through,
    since the credential was in a commit SUBJECT, not the memo body."""
    r = subprocess.run(
        [
            "bash",
            str(REPO / "scripts" / "mail-send.sh"),
            f"mail(x): invite code is {TOKEN} (probe)",
            "mailboxes/lead/sent/does-not-exist.md",
        ],
        capture_output=True,
        text=True,
        cwd=REPO,
    )
    assert r.returncode == 1
    assert "Nothing was sent" in r.stderr
    assert TOKEN not in r.stdout and TOKEN not in r.stderr
