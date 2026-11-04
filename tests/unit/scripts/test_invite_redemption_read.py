"""invite_redemption_read.py: the mask rule refuses before any DB connection."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import invite_redemption_read as irr  # noqa: E402


def test_masks_are_uppercased_and_split():
    assert irr.parse_masks("4jaj8wbg, D7TFY3M9") == ["4JAJ8WBG", "D7TFY3M9"]


@pytest.mark.parametrize(
    "bad", ["", ",", "abc", "4JAJ8WBG1", "4JAJ-WBG", ",".join(["AAAAAAAA"] * 21)]
)
def test_bad_masks_refused(bad):
    with pytest.raises(SystemExit):
        irr.parse_masks(bad)


def test_full_length_token_is_refused():
    """A 24-char raw token must never be accepted as a mask (hard rule 3)."""
    with pytest.raises(SystemExit):
        irr.parse_masks("0123456789ABCDEFGHJKMNPQ")
