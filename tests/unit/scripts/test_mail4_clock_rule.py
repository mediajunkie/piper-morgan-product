"""mail4.py's clock rule (xian's yes 2026-11-18, CIO's 11-13 proposal): an estimated minute
(`HH:Mx`) in a body or an ack note is refused; backticks are the escape for a quoted time."""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture(scope="module")
def mail4():
    spec = importlib.util.spec_from_file_location("mail4", ROOT / "scripts" / "mail4.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize(
    "text, found",
    [
        ("Lead replied at 17:4x.", ["17:4x"]),
        ("Both at 9:0X and 22:1x", ["9:0X", "22:1x"]),
        ("Lead wrote `17:4x` in the memo.", []),
        ("```\nlog line 17:4x\n```\nafter", []),
        ("STOP fires at 22:07; it ran at 14:46:39.", []),
        ("", []),
        (None, []),
    ],
)
def test_estimated_minutes(mail4, text, found):
    assert mail4.estimated_minutes(text) == found


def test_refusal_names_the_form_and_the_escape(mail4):
    msg = mail4.clock_refusal("send", "done 10:2x")
    assert "10:2x" in msg and "backticks" in msg and msg.startswith("send: refused")
    assert mail4.clock_refusal("ack", "done 10:24") is None
    assert mail4.clock_refusal("ack", None) is None
