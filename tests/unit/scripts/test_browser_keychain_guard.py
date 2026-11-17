"""The two guards against a browser reading xian's login keychain (xian, 2026-11-17).

``.claude/hooks/guard_browser_launch.py`` refuses a Bash launch without the flag;
``scripts/browser_keychain_check.py`` finds one already running.
"""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
HOOK_SH = ROOT / ".claude" / "hooks" / "guard-browser-launch.sh"
TEST_BROWSER = "/Users/x/.claude-pm/chrome-for-testing.app/Contents/MacOS/Google Chrome for Testing"
OWN_BROWSER = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


hook = _load(ROOT / ".claude" / "hooks" / "guard_browser_launch.py", "guard_browser_launch")
check = _load(ROOT / "scripts" / "browser_keychain_check.py", "browser_keychain_check")

REFUSED = [
    f'"{TEST_BROWSER}" --headless=new --remote-debugging-port=9333',
    f'nohup "{TEST_BROWSER}" --headless=new > /tmp/x.log 2>&1 &',
    f'cd /tmp && env -u FOO BAR=1 "{TEST_BROWSER}" --user-data-dir=/tmp/p',
    f'B="{TEST_BROWSER}"; "$B" --headless=new',
    f'B="{TEST_BROWSER}"\n"${{B}}" --headless=new &',
    f"bash -c '\"{TEST_BROWSER}\" --headless=new'",
    f'echo start & "{TEST_BROWSER}" --headless=new',
    f'"{OWN_BROWSER}" --remote-debugging-port=9222',
    'open -a "Google Chrome for Testing" --args --headless=new',
    "open -na Chromium",
    "/opt/homebrew/bin/chromium --headless",
    "chrome-headless-shell --dump-dom https://example.com",
    f'bash <<EOF\n"{TEST_BROWSER}" --headless=new\nEOF',
    # HOST, 2026-11-17: wrappers outside the known list, and osascript.
    f'arch -arm64 "{TEST_BROWSER}" --headless=new',
    f'timeout 5 "{TEST_BROWSER}" --headless=new',
    "gtimeout 5 /opt/homebrew/bin/chromium",
    f'sudo -u someone "{TEST_BROWSER}"',
    f'echo --headless | xargs "{TEST_BROWSER}"',
    f'some-unknown-wrapper --opt "{TEST_BROWSER}"',
    "osascript -e 'tell application \"Google Chrome\" to activate'",
    'osascript -e \'tell application "Chromium" to open location "https://example.com"\'',
    f"cat >> log.md <<'EOF'\nquoted\nEOF\n\"{TEST_BROWSER}\" --headless=new",
]

ALLOWED = [
    f'"{TEST_BROWSER}" --use-mock-keychain --headless=new --remote-debugging-port=9333',
    f'B="{TEST_BROWSER}"; nohup "$B" --headless=new --use-mock-keychain &',
    'open -a "Google Chrome for Testing" --args --use-mock-keychain',
    f'strings "{TEST_BROWSER}" | grep -c "Safe Storage"',
    f'ls -l "{TEST_BROWSER}"',
    "/bin/ps -axww -o pid=,command= | grep 'Google Chrome for Testing'",
    "python3 scripts/seat_browser.py --check web",
    "python3 scripts/browser_keychain_check.py",
    "npx chrome-devtools-mcp@1.10.1 --isolated",
    "git commit -m 'chrome guard'",
    "cat docs/chromium-notes.md",
    f'timeout 5 "{TEST_BROWSER}" --use-mock-keychain --headless=new',
    "npx playwright install chromium",
    "grep -rn chromium scripts",
    f'codesign -dv "{TEST_BROWSER}"',
    "osascript -e 'tell application \"Finder\" to activate'",
    # PA, 2026-11-17: heredoc text going to a file is not a launch.
    "cat >> log.md <<'EOF'\n- ran:\n/nonexistent-dir/chromium --version\nEOF",
    f'cat > note.md <<-"END"\n"{TEST_BROWSER}" --headless=new\nEND\ngit status',
]


@pytest.mark.parametrize("command", REFUSED)
def test_launch_without_the_flag_is_refused(command):
    assert hook.launches(command), command


@pytest.mark.parametrize("command", ALLOWED)
def test_flagged_launch_and_plain_reads_pass(command):
    assert hook.launches(command) == [], command


def _run_hook(payload: str):
    return subprocess.run(
        ["bash", str(HOOK_SH)], input=payload, capture_output=True, text=True, check=False
    )


def test_hook_exits_2_with_the_reason_on_stderr():
    done = _run_hook(json.dumps({"tool_input": {"command": REFUSED[0]}}))
    assert done.returncode == 2
    assert "REFUSED" in done.stderr and "--use-mock-keychain" in done.stderr
    assert done.stdout == ""


def test_hook_passes_a_flagged_launch_and_unrelated_commands():
    assert _run_hook(json.dumps({"tool_input": {"command": ALLOWED[0]}})).returncode == 0
    assert _run_hook(json.dumps({"tool_input": {"command": "git status"}})).returncode == 0


def test_hook_fails_open_on_input_it_cannot_read():
    assert _run_hook("not json, but it says chrome").returncode == 0
    assert _run_hook(json.dumps({"tool_input": {"command": 'echo "chrome'}})).returncode == 0


def test_hook_is_wired_in_project_settings():
    settings = json.loads((ROOT / ".claude" / "settings.json").read_text())
    commands = [
        h["command"]
        for block in settings["hooks"]["PreToolUse"]
        if block.get("matcher") == "Bash"
        for h in block["hooks"]
        if "if" not in h
    ]
    assert "bash .claude/hooks/guard-browser-launch.sh" in commands


TABLE = "\n".join(
    [
        f"  101 {TEST_BROWSER} --headless=new --use-mock-keychain --user-data-dir=/tmp/a",
        f"  102 {TEST_BROWSER} --headless=new --user-data-dir=/tmp/b",
        f"  103 {TEST_BROWSER} Helper --type=renderer --user-data-dir=/tmp/b",
        f"  104 {OWN_BROWSER} --restore-last-session",
        f"  105 npm exec chrome-devtools-mcp@1.10.1 --executablePath={TEST_BROWSER} --isolated",
        "  106 chrome-devtools-mcp",
        "  107 /opt/homebrew/bin/chromium --headless",
        "  108 /usr/bin/grep chrome",
    ]
)


def test_check_lists_only_unflagged_main_browsers_outside_applications():
    assert check.unflagged(TABLE) == [(102, TEST_BROWSER), (107, "/opt/homebrew/bin/chromium")]


def test_check_prints_pid_and_program_only(monkeypatch, capsys):
    monkeypatch.setattr(check, "process_table", lambda: TABLE)
    assert check.main() == 1
    out = capsys.readouterr().out
    assert "pid 102" in out and "pid 107" in out
    assert "--user-data-dir" not in out and "/tmp/b" not in out


def test_check_clean_and_unreadable(monkeypatch, capsys):
    monkeypatch.setattr(check, "process_table", lambda: TABLE.splitlines()[0])
    assert check.main() == 0
    monkeypatch.setattr(check, "process_table", lambda: None)
    assert check.main() == 3
    assert "nothing was checked" in capsys.readouterr().out
