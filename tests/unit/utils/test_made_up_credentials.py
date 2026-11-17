"""Issue 2397: the made-up credential helper builds values the scan would refuse in a
file, and builds them only at run time."""

import subprocess
import sys
from pathlib import Path

import pytest

from services.security.api_key_validator import APIKeyValidator
from tests.utils import made_up_credentials as made_up

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import staged_credential_scan as scan  # noqa: E402


def test_the_same_label_gives_the_same_body_and_another_label_a_different_one():
    assert made_up.body("a", 40) == made_up.body("a", 40)
    assert made_up.body("a", 40) != made_up.body("b", 40)
    assert len(made_up.body("a", 7)) == 7 and len(made_up.body("a", 300)) == 300
    assert set(made_up.body("a", 300, made_up.CROCKFORD)) <= set(made_up.CROCKFORD)


@pytest.mark.parametrize(
    "value",
    (
        made_up.GOOD_OPENAI_KEY,
        made_up.GOOD_ANTHROPIC_KEY,
        made_up.openai_key("x", 32, project=True),
        made_up.github_pat("x"),
        made_up.invite_code("x"),
    ),
)
def test_each_built_value_is_a_shape_the_scan_refuses_in_a_file(value):
    """The point of building at run time: written into a file, each of these is a hit."""
    assert scan.find(f"key = {value!r}", "tests/x.py") == [value]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "provider,key",
    (("openai", made_up.GOOD_OPENAI_KEY), ("anthropic", made_up.GOOD_ANTHROPIC_KEY)),
)
async def test_the_two_good_keys_pass_the_real_validator(provider, key):
    report = await APIKeyValidator().validate_api_key(provider, key)
    assert report.format_valid is True and report.overall_valid is True
    assert report.leak_result.severity == "unknown"


def test_the_helper_and_the_detector_hold_no_credential_shape():
    """The two files this issue was about most: neither holds a matching run."""
    for path in ("tests/utils/made_up_credentials.py", "services/security/key_leak_detector.py"):
        lines = (ROOT / path).read_text(encoding="utf-8").splitlines()
        assert [n for n, line in enumerate(lines, 1) if scan.find(line, path)] == [], path


def test_no_tracked_test_file_holds_a_credential_shape():
    """The acceptance row: the scan with no baseline lists no path under tests/. Reads the
    working tree through git grep, as the scan's own tracked mode reads HEAD."""
    listed = subprocess.run(
        ["git", "ls-files", "tests"], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.split("\n")
    hits = []
    for path in filter(None, listed):
        file = ROOT / path
        if not file.is_file() or file.suffix.lower() in scan.bearer._SKIP_SUFFIXES:
            continue
        try:
            lines = file.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue
        hits += [f"{path}:{n}" for n, line in enumerate(lines, 1) if scan.find(line, path)]
    assert hits == []
