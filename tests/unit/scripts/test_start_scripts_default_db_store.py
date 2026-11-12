"""xian, 2026-11-12: the two local start scripts default to the database credential
store, so neither reads his login keychain unless PIPER_CREDENTIAL_STORE is set to
keychain on purpose.

Each script is run under bash with its real work cut off: only the lines up to and
including the default are evaluated, then the variable is printed.
"""

import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_LINE = 'PIPER_CREDENTIAL_STORE="${PIPER_CREDENTIAL_STORE:-db}"'


def _value_after_default(script: str, preset):
    line = next(
        raw for raw in (ROOT / "scripts" / script).read_text().splitlines() if DEFAULT_LINE in raw
    )
    env = {"PATH": "/usr/bin:/bin"}
    if preset is not None:
        env["PIPER_CREDENTIAL_STORE"] = preset
    done = subprocess.run(
        ["bash", "-c", f'{line}\nprintf "%s" "$PIPER_CREDENTIAL_STORE"'],
        capture_output=True,
        text=True,
        env=env,
    )
    assert done.returncode == 0, done.stderr
    return done.stdout


@pytest.mark.parametrize("script", ["restart-server.sh", "start-piper.sh"])
def test_unset_means_the_database_store(script):
    assert _value_after_default(script, None) == "db"


@pytest.mark.parametrize("script", ["restart-server.sh", "start-piper.sh"])
def test_an_explicit_choice_is_kept(script):
    assert _value_after_default(script, "keychain") == "keychain"


def test_restart_server_hands_the_store_to_the_server_process():
    text = (ROOT / "scripts" / "restart-server.sh").read_text()
    start = text.index("env -u ANTHROPIC_API_KEY")
    command = text[start : text.index("SERVER_PID=$!", start)]
    assert 'PIPER_CREDENTIAL_STORE="$PIPER_CREDENTIAL_STORE"' in command
    assert "main.py" in command


def test_start_piper_exports_it_before_either_process_starts():
    text = (ROOT / "scripts" / "start-piper.sh").read_text()
    assert f"export {DEFAULT_LINE}" in text
    assert text.index(f"export {DEFAULT_LINE}") < text.index("nohup python main.py")
