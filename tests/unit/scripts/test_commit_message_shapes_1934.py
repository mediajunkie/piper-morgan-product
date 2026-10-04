"""#1934 — the commit-message guard (#1691 auto-close + #1845 bearer-credential) missed
several ordinary ways of writing a commit message. HOST's gap table (issue #1934), each
row pinned here as a parametrized case:

    -am "..."                       (combined short-flag cluster)        -> was PASSING, now BLOCKED
    -m"..."                         (no-space attached form)             -> was PASSING, now BLOCKED
    --message "..." / --message=... (long option, space and =)          -> was PASSING, now BLOCKED
    -F <file> / -F - <<EOF          (message from a file / heredoc)      -> was PASSING, now BLOCKED
    git -C <dir> commit / git -c k=v commit (global options before the subcommand) -> was PASSING, now BLOCKED
    compound command (&&)           (sanity: already worked, must still) -> stays BLOCKED

Plus the output-channel fix: a block's reason must land on STDERR, never stdout — the harness
shows only stderr for a PreToolUse hook's exit-2 feedback, so a stdout-only reason never reached
the committer (verified behaviorally by HOST: 455 bytes on stdout, 0 on stderr, before this fix).

Layer: the extractor function in isolation (`commit_messages_in_bash_command`), then the live
PreToolUse hook by actually running it (subprocess), matching this repo's existing pattern in
test_check_autoclose_keywords_1691.py and test_bearer_credential_in_commit_messages_r5_1845.py.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
SCRIPT = REPO / "scripts" / "check_autoclose_keywords.py"
HOOK = REPO / ".claude" / "hooks" / "autoclose-guard.sh"
COMMIT_MSG_HOOK = REPO / "scripts" / "git-hooks" / "commit-msg"

sys.path.insert(0, str(REPO / "scripts"))
from check_autoclose_keywords import commit_messages_in_bash_command, mask  # noqa: E402

# Same synthetic fixture as the R5/#1845 suite — never a minted token.
TOKEN = "9EA0V9VPHS9CFRTKH873EGJ6"
MASKED = mask(TOKEN)  # "9EA0…EGJ6"
_FIX_FILE = REPO / "tests" / "unit" / "scripts" / "_fixture_commit_msg_1934.txt"

_KW = "clo" + "se"  # assembled so this file's own text never reads as an auto-close command


def setup_module(module):
    _FIX_FILE.write_text(f"mail(ppm): invite code is {TOKEN}\n")


def teardown_module(module):
    _FIX_FILE.unlink(missing_ok=True)


# --- shape -> command, each carrying the credential --------------------------------------------
CREDENTIAL_SHAPES = {
    "combined short cluster -am (space)": f'git commit -am "mail(ppm): invite code is {TOKEN}" -- a.md',
    "combined short cluster -sm (space)": f'git commit -sm "mail(ppm): invite code is {TOKEN}" -- a.md',
    'attached -m"..." (no space)': f'git commit -m"mail(ppm): invite code is {TOKEN}" -- a.md',
    "attached -m'...' (no space)": f"git commit -m'mail(ppm): invite code is {TOKEN}' -- a.md",
    "--message with space": f'git commit --message "mail(ppm): invite code is {TOKEN}" -- a.md',
    "--message=... attached": f'git commit --message="mail(ppm): invite code is {TOKEN}" -- a.md',
    "-F <file>": f"git commit -F {_FIX_FILE}",
    "--file=<file>": f"git commit --file={_FIX_FILE}",
    "-F - <<heredoc>": ("git commit -F - <<'EOF'\n" f"mail(ppm): invite code is {TOKEN}\n" "EOF"),
    "git -C <dir> commit -m": f'git -C /tmp commit -m "mail(ppm): invite code is {TOKEN}"',
    "git -c k=v commit -m": f'git -c user.name=x commit -m "mail(ppm): invite code is {TOKEN}"',
    "compound (git status && git commit -am)": (
        f'git status && git commit -am "mail(ppm): invite code is {TOKEN}" -- a.md'
    ),
    "second -m (multi-paragraph)": (f'git commit -m "first paragraph" -m "second with {TOKEN}"'),
    'existing -m "..." still works': f'git commit -m "mail(ppm): invite code is {TOKEN}"',
}

# --- shapes/commands that must NOT be flagged (false-positive guard) ---------------------------
SAFE_SHAPES = {
    "git tag -a -m (out of scope, no 'commit')": f'git tag -a -m "invite code {TOKEN}" v1.0',
    "git status (not a commit)": "git status",
    "git add (not a commit)": "git add -A",
    "masked credential via -am": f'git commit -am "roster has {MASKED}" -- a.md',
    "heredoc writes a FILE, not the message (-m is separate)": (
        "cat > note.md <<'EOF'\n"
        f"the subject {_KW} #1677 was the incident\n"
        "EOF\n"
        'git commit -m "docs: note about the 1677 incident" -- note.md'
    ),
    "unrelated -am without credential": 'git commit -am "chore: bump version" -- a.md',
}

# --- #1691 auto-close shapes in the new forms ---------------------------------------------------
AUTOCLOSE_SHAPES = {
    "-am closes #N": f'git commit -am "{_KW.capitalize()}s #123" -- a.md',
    "--message closes #N": f'git commit --message "{_KW}s #456"',
    "git -C ... closes #N": f'git -C /tmp commit -m "resolved: #789"',
}


@pytest.mark.parametrize("shape", CREDENTIAL_SHAPES)
def test_extractor_captures_credential_shape(shape):
    cmd = CREDENTIAL_SHAPES[shape]
    msgs = commit_messages_in_bash_command(cmd)
    assert any(TOKEN in m for m in msgs), (shape, cmd, msgs)


@pytest.mark.parametrize("shape", SAFE_SHAPES)
def test_extractor_has_no_false_positive(shape):
    cmd = SAFE_SHAPES[shape]
    msgs = commit_messages_in_bash_command(cmd)
    assert not any(TOKEN in m for m in msgs), (shape, cmd, msgs)
    assert not any(_KW in m and "#1677" in m for m in msgs), (shape, cmd, msgs)


def _hook(command: str) -> subprocess.CompletedProcess:
    payload = json.dumps({"tool_input": {"command": command}})
    return subprocess.run(
        ["bash", str(HOOK)], input=payload, capture_output=True, text=True, cwd=REPO
    )


@pytest.mark.parametrize("shape", CREDENTIAL_SHAPES)
def test_live_hook_blocks_credential_shape_with_reason_on_stderr(shape):
    cmd = CREDENTIAL_SHAPES[shape]
    r = _hook(cmd)
    assert r.returncode == 2, (shape, cmd, r.stdout, r.stderr)
    # #1934: the reason must be on stderr, and stdout must carry nothing —
    # a stdout-only reason is invisible to the committer through this harness.
    assert r.stdout == "", (shape, "stdout should be empty", r.stdout)
    assert "BLOCKED" in r.stderr, (shape, r.stderr)
    assert TOKEN not in r.stdout and TOKEN not in r.stderr, (shape, "credential leaked")


@pytest.mark.parametrize("shape", SAFE_SHAPES)
def test_live_hook_passes_safe_shape(shape):
    cmd = SAFE_SHAPES[shape]
    r = _hook(cmd)
    assert r.returncode == 0, (shape, cmd, r.stdout, r.stderr)


@pytest.mark.parametrize("shape", AUTOCLOSE_SHAPES)
def test_live_hook_blocks_autoclose_in_new_shapes(shape):
    cmd = AUTOCLOSE_SHAPES[shape]
    r = _hook(cmd)
    assert r.returncode == 2, (shape, cmd, r.stdout, r.stderr)
    assert r.stdout == "", (shape, "stdout should be empty", r.stdout)
    assert "BLOCKED" in r.stderr, (shape, r.stderr)


def test_live_hook_autoclose_opt_in_waives_in_the_am_shape():
    cmd = f'git commit -am "{_KW.capitalize()}s #123\n\nAuto-Close: intentional" -- a.md'
    r = _hook(cmd)
    assert r.returncode == 0, (cmd, r.stdout, r.stderr)


def test_output_channel_stdout_is_always_empty_on_block():
    """The specific regression HOST found: BLOCKED text used to land on
    stdout (455 bytes observed), which this harness never shows."""
    r = _hook(f'git commit -am "mail(ppm): invite code is {TOKEN}" -- a.md')
    assert r.returncode == 2
    assert r.stdout == "", f"stdout leaked {len(r.stdout)} bytes: {r.stdout!r}"
    assert len(r.stderr) > 0


# --- the proposed (NOT installed) commit-msg hook layer -----------------------------------------


def _run_commit_msg_hook(message: str) -> subprocess.CompletedProcess:
    msgfile = REPO / "tests" / "unit" / "scripts" / "_fixture_commit_msg_hook_input.txt"
    msgfile.write_text(message)
    try:
        return subprocess.run(
            ["sh", str(COMMIT_MSG_HOOK), str(msgfile)],
            capture_output=True,
            text=True,
            cwd=REPO,
        )
    finally:
        msgfile.unlink(missing_ok=True)


def test_proposed_commit_msg_hook_blocks_a_credential_shape_independently():
    """This layer takes the FINAL message git assembled — it never has to
    know -m vs -am vs -F vs an editor. One representative case is enough to
    show the mechanism; the shape coverage above is the extractor's job."""
    r = _run_commit_msg_hook(f"mail(ppm): invite code is {TOKEN}")
    assert r.returncode == 1, (r.stdout, r.stderr)
    assert TOKEN not in r.stdout and TOKEN not in r.stderr


def test_proposed_commit_msg_hook_passes_a_safe_message():
    r = _run_commit_msg_hook("fix(intent): render == data at 13 sites, refs 1762")
    assert r.returncode == 0, (r.stdout, r.stderr)


def test_proposed_commit_msg_hook_is_not_installed():
    """Hard rule from the task: this is a candidate for CIO co-sign, not a
    live hook. Assert it isn't wired into .claude/settings.json or copied
    into any git-hooks directory this checkout can see."""
    settings = (REPO / ".claude" / "settings.json").read_text()
    assert "git-hooks/commit-msg" not in settings
    common_dir = subprocess.run(
        ["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True, cwd=REPO
    ).stdout.strip()
    installed = Path(REPO / common_dir / "hooks" / "commit-msg")
    if installed.exists():
        # If something is installed, it must not be THIS proposal verbatim —
        # i.e. installation is a deliberate separate act, not a side effect
        # of this test suite or this task.
        assert installed.read_text() != COMMIT_MSG_HOOK.read_text()
