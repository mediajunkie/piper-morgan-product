"""#2333: a Slack room, territory or path keeps its spatial position across processes.

Arch's pins (2026-11-12): one crc32 helper, an int in 0-999, an integer passes through,
the room_id fallback applies only when room_position is falsy, and the builtin hash()
never returns to the Slack spatial modules.
"""

import os
import re
import subprocess
import sys
import zlib
from pathlib import Path

import pytest

from services.integrations.slack.spatial_adapter import SlackSpatialAdapter, stable_position

ROOT = Path(__file__).resolve().parents[5]

# crc32 of the UTF-8 bytes, mod 1000, worked out once and written down.
KNOWN = {"C789012": 785, "T123456": 392, "thread_abc": 945}


def test_the_known_values_are_pinned_exactly():
    for value, position in KNOWN.items():
        assert zlib.crc32(value.encode("utf-8")) % 1000 == position
        assert stable_position(value) == position


def test_a_position_is_an_int_in_range_and_the_modulus_is_honoured():
    for value in ("", "C1", "a much longer identifier with spaces", "日本語"):
        assert 0 <= stable_position(value) < 1000
    assert 0 <= stable_position("C789012", 10) < 10


@pytest.mark.parametrize("seed", ["0", "1", "4242"])
def test_another_process_with_another_hash_seed_gives_the_same_position(seed):
    code = (
        "from services.integrations.slack.spatial_adapter import stable_position;"
        "print(stable_position('C789012'), stable_position('T123456'), hash('C789012') % 1000)"
    )
    env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONPATH=str(ROOT))
    done = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, env=env, cwd=str(ROOT)
    )
    assert done.returncode == 0, done.stderr[-500:]
    room, territory, _salted = done.stdout.split()
    assert (int(room), int(territory)) == (KNOWN["C789012"], KNOWN["T123456"])


def test_the_builtin_hash_really_does_differ_between_seeds():
    """The control: without the helper, two processes disagree, which is the defect."""
    seen = set()
    for seed in ("1", "2", "3", "4"):
        done = subprocess.run(
            [sys.executable, "-c", "print(hash('C789012') % 1000)"],
            capture_output=True,
            text=True,
            env=dict(os.environ, PYTHONHASHSEED=seed),
        )
        seen.add(done.stdout.strip())
    assert len(seen) > 1


@pytest.mark.asyncio
async def test_all_four_sites_use_the_helper_and_integers_pass_through():
    adapter = SlackSpatialAdapter()
    event = await adapter.create_spatial_event_from_slack(
        "1234567890.000001",
        "message_posted",
        {
            "territory_position": "T123456",
            "room_position": "C789012",
            "path_position": "thread_abc",
        },
    )
    assert event.territory_position == KNOWN["T123456"]
    assert event.room_position == KNOWN["C789012"]
    assert event.path_position == KNOWN["thread_abc"]

    event = await adapter.create_spatial_event_from_slack(
        "1234567890.000002",
        "message_posted",
        {"territory_position": 7, "room_position": 12, "path_position": 3, "room_id": "C789012"},
    )
    assert (event.territory_position, event.room_position, event.path_position) == (7, 12, 3)


@pytest.mark.asyncio
async def test_the_room_id_fallback_applies_only_when_room_position_is_falsy():
    adapter = SlackSpatialAdapter()
    event = await adapter.create_spatial_event_from_slack(
        "1234567890.000003", "message_posted", {"room_id": "C789012"}
    )
    assert event.room_position == KNOWN["C789012"]
    # 0 is falsy, so the fallback still applies; that precedence is unchanged on purpose.
    event = await adapter.create_spatial_event_from_slack(
        "1234567890.000004", "message_posted", {"room_position": 0, "room_id": "C789012"}
    )
    assert event.room_position == KNOWN["C789012"]


def test_the_builtin_hash_never_returns_to_the_slack_spatial_modules():
    """A ratchet at 0 (Arch): no call to builtin hash( in services/integrations/slack/spatial*.py."""
    call = re.compile(r"(?<![\w.])hash\(")
    offenders = []
    for path in sorted((ROOT / "services" / "integrations" / "slack").glob("spatial*.py")):
        for number, line in enumerate(path.read_text().splitlines(), 1):
            code = line.split("#", 1)[0]
            if call.search(code):
                offenders.append(f"{path.name}:{number}")
    assert offenders == []
