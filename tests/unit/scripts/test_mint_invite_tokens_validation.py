"""mint_invite_tokens.py validates its own arguments (CIO option 3, 2026-10-09):
as deployed in /app it is the permission boundary, so the bounds live here."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

import mint_invite_tokens as mt  # noqa: E402


def _ns(count=0, burn=None, apply=False):
    return SimpleNamespace(count=count, burn_unused=burn, apply=apply)


@pytest.mark.parametrize("count", [1, 3, 20])
def test_counts_in_range_pass(count):
    mt._validate(_ns(count=count))


@pytest.mark.parametrize("count", [0, -1, 21, 500])
def test_counts_out_of_range_refused(count):
    with pytest.raises(SystemExit):
        mt._validate(_ns(count=count))


@pytest.mark.parametrize("burn", ["ZVHW8B35", "zvhw8b35", "ZVHW8B35,QGQPKJGP"])
def test_good_masks_pass(burn):
    mt._validate(_ns(burn=burn))


@pytest.mark.parametrize(
    "burn", ["", "SHORT", "ZVHW8B3$", "ZVHW8B35;DROP", "ZVHW 8B35", ",".join(["ZVHW8B35"] * 21)]
)
def test_bad_masks_refused(burn):
    with pytest.raises(SystemExit):
        mt._validate(_ns(burn=burn))


def test_burn_with_a_count_is_refused():
    with pytest.raises(SystemExit):
        mt._validate(_ns(count=2, burn="ZVHW8B35"))
