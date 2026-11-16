"""scripts/run_tests.sh never starts services (issue 2386).

The script used to run `docker-compose up -d postgres redis` in its `full` and `coverage` modes
whenever `pgrep postgres` found nothing. On a host where Postgres runs in a container, `pgrep`
always finds nothing, so those modes always ran compose, and on a shared host that re-creates
containers other work is using. The check is now the database port, and a closed port ends the
run with a message.
"""

import re
import socket
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[3] / "scripts" / "run_tests.sh"


def _code_lines():
    """The script's lines with comments removed."""
    return [line.split("#", 1)[0] for line in SCRIPT.read_text().splitlines()]


def _helper_source():
    match = re.search(r"^postgres_port_open\(\) \{.*?^\}", SCRIPT.read_text(), re.S | re.M)
    assert match, "postgres_port_open() is missing from scripts/run_tests.sh"
    return match.group(0)


def _port_open(port):
    result = subprocess.run(
        ["bash", "-c", _helper_source() + "\npostgres_port_open"],
        env={"PATH": "/usr/bin:/bin", "POSTGRES_HOST": "127.0.0.1", "POSTGRES_PORT": str(port)},
        capture_output=True,
        timeout=20,
    )
    return result.returncode == 0


@pytest.mark.smoke
def test_no_line_runs_compose_or_starts_a_container():
    offenders = [
        line.strip()
        for line in _code_lines()
        if re.search(r"docker[- ]compose|docker\s+(start|run|compose)\b", line)
    ]
    assert offenders == [], f"run_tests.sh must not start services: {offenders}"


@pytest.mark.smoke
def test_no_line_checks_for_postgres_with_pgrep():
    offenders = [line.strip() for line in _code_lines() if "pgrep" in line]
    assert offenders == [], f"pgrep cannot see a container's Postgres: {offenders}"


def test_full_mode_stops_with_a_message_when_the_port_is_closed():
    body = re.search(r"^run_full_tests\(\) \{.*?^\}", SCRIPT.read_text(), re.S | re.M).group(0)
    guard = body.index("if ! postgres_port_open; then")
    pytest_call = body.index("python -m pytest")
    assert guard < pytest_call
    block = body[guard:pytest_call]
    assert "return 1" in block
    assert "does not start services" in block


def test_the_helper_sees_a_listening_port_and_a_closed_one():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(1)
        port = listener.getsockname()[1]
        assert _port_open(port) is True
    assert _port_open(port) is False
