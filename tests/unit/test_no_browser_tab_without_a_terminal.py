"""``main.py`` opens a browser tab only for a person at a terminal (HOST and Arch,
decisions.log 2026-11-24 07:40).

Twice (11-11, 11-24) a server started from a seat's shell opened a tab in xian's own
browser. A remembered ``--no-browser`` flag is not a mechanism; this is.

LAYER: ``main.should_open_browser`` run in a child process (``main.py`` parses arguments and
configures logging when imported, so it is not imported into the test process), with the
two streams' ``isatty`` replaced; and an ``ast`` read of shipped code for ``webbrowser``.
DENOMINATOR: the four terminal combinations, the flag, a command, a broken stream; every
Python file under services/, web/, cli/ and scripts/, plus main.py and main_mcp.py.
NOT COVERED: a real terminal (a person's own start is the test of that).
"""

import ast
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

PROBE = r"""
import json, sys
argv = json.loads(sys.argv[1])
real_out = sys.stdout
sys.argv = ["main.py"] + argv
import main

class Stream:
    def __init__(self, tty): self.tty = tty
    def isatty(self):
        if self.tty == "broken": raise ValueError("I/O operation on closed file")
        return self.tty

results = {}
for name, (i, o) in {
    "both": (True, True), "stdin_only": (True, False), "stdout_only": (False, True),
    "neither": (False, False), "broken": ("broken", True),
}.items():
    main.sys.stdin, main.sys.stdout = Stream(i), Stream(o)
    try:
        results[name] = main.should_open_browser()
    finally:
        main.sys.stdin, main.sys.stdout = sys.__stdin__, real_out
main.sys.stdin, main.sys.stdout = None, None
try:
    results["missing"] = main.should_open_browser()
finally:
    main.sys.stdin, main.sys.stdout = sys.__stdin__, real_out
real_out.write("\nRESULT " + json.dumps(results) + "\n")
"""


def _probe(*argv):
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(Path.home()),
        "PYTHON_DOTENV_DISABLED": "1",
        "DISPLAY": ":0",  # so the no-display branch never decides the answer on Linux
    }
    done = subprocess.run(
        [sys.executable, "-c", PROBE, json.dumps(list(argv))],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    lines = [line for line in done.stdout.splitlines() if line.startswith("RESULT ")]
    assert lines, (done.returncode, done.stderr[-800:])
    return json.loads(lines[-1][len("RESULT ") :])


@pytest.fixture(scope="module")
def plain_start():
    return _probe()


def test_a_person_at_a_terminal_on_both_ends_keeps_the_tab(plain_start):
    assert plain_start["both"] is True


@pytest.mark.parametrize("case", ["stdin_only", "stdout_only", "neither"])
def test_without_a_terminal_on_both_ends_no_tab_opens(plain_start, case):
    """A seat's shell reads False for both; nohup with a log file has no terminal on
    stdout; a pipe into the process has none on stdin."""
    assert plain_start[case] is False


@pytest.mark.parametrize("case", ["broken", "missing"])
def test_a_stream_that_cannot_answer_counts_as_no_terminal(plain_start, case):
    assert plain_start[case] is False


def test_the_flag_still_refuses_even_at_a_terminal():
    assert _probe("--no-browser")["both"] is False


def test_a_command_still_opens_nothing_even_at_a_terminal():
    assert _probe("status")["both"] is False


# --- Arch's pin: no other code path in shipped code can open a browser from Python ---


def _shipped_files():
    for folder in ("services", "web", "cli", "scripts"):
        yield from sorted((ROOT / folder).rglob("*.py"))
    yield ROOT / "main.py"
    yield ROOT / "main_mcp.py"


def _webbrowser_uses(path):
    """Line numbers where the file calls into ``webbrowser`` or imports a name from it."""
    text = path.read_text(encoding="utf-8")
    if "webbrowser" not in text:
        return []
    uses = []
    for node in ast.walk(ast.parse(text)):
        if isinstance(node, ast.ImportFrom) and node.module == "webbrowser":
            uses.append(node.lineno)
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "webbrowser"
        ):
            uses.append(node.lineno)
    return uses


def test_only_main_py_uses_webbrowser_and_only_at_its_two_sites():
    """``guard-browser-launch.sh`` reads command lines and cannot see a launch made from
    inside Python, so this pin is what keeps a new one from slipping in. A bare
    ``import webbrowser`` that is never used opens nothing and is not counted."""
    users = {}
    for path in _shipped_files():
        uses = _webbrowser_uses(path)
        if uses:
            users[path.relative_to(ROOT).as_posix()] = len(uses)
    assert users == {"main.py": 2}


def test_both_sites_sit_behind_the_one_gate():
    tree = ast.parse((ROOT / "main.py").read_text(encoding="utf-8"))
    opener = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "open_browser_delayed"
    )
    inside = [
        node
        for node in ast.walk(opener)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "webbrowser"
    ]
    assert len(inside) == 2  # so no call to webbrowser exists outside this function

    # The opener is called in exactly one place, and that place is the body of
    # ``if should_open_browser():``.
    def _is_opener_call(node):
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "open_browser_delayed"
        )

    calls = [node for node in ast.walk(tree) if _is_opener_call(node)]
    assert len(calls) == 1
    guarded = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.If)
        and isinstance(node.test, ast.Call)
        and isinstance(node.test.func, ast.Name)
        and node.test.func.id == "should_open_browser"
        and any(_is_opener_call(inner) for stmt in node.body for inner in ast.walk(stmt))
    ]
    assert len(guarded) == 1


def test_the_gate_asks_both_streams():
    source = (ROOT / "main.py").read_text(encoding="utf-8")
    assert "if not (_is_terminal(sys.stdin) and _is_terminal(sys.stdout)):" in source
