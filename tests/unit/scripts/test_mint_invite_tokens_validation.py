"""Invite-token payloads validate their own arguments (CIO option 3, 2026-10-09):
as deployed in /app each payload is its own permission boundary, and each carries
ONE effect class (Arch): the mint creates rows, the burn deletes them."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))

import burn_invite_tokens as bt  # noqa: E402
import mint_invite_tokens as mt  # noqa: E402


@pytest.mark.parametrize("count", [1, 3, 20])
def test_mint_counts_in_range_pass(count):
    mt._validate(SimpleNamespace(count=count))


@pytest.mark.parametrize("count", [0, -1, 21, 500])
def test_mint_counts_out_of_range_refused(count):
    with pytest.raises(SystemExit):
        mt._validate(SimpleNamespace(count=count))


def test_the_mint_payload_cannot_burn(monkeypatch):
    """One effect class per payload: the mint has no delete path, and the old
    --burn-unused flag is now an unknown argument (argparse exits)."""
    assert "DELETE FROM" not in Path(mt.__file__).read_text()
    monkeypatch.setattr(sys, "argv", ["mint_invite_tokens.py", "--burn-unused", "ZVHW8B35"])
    with pytest.raises(SystemExit):
        mt.main()


@pytest.mark.parametrize("masks", ["ZVHW8B35", "zvhw8b35", "ZVHW8B35,QGQPKJGP"])
def test_burn_good_masks_pass(masks):
    assert all(len(m) == 8 for m in bt.parse_masks(masks))


@pytest.mark.parametrize(
    "masks",
    ["", "SHORT", "ZVHW8B3$", "ZVHW8B35;DROP", "ZVHW 8B35", ",".join(["ZVHW8B35"] * 21)],
)
def test_burn_bad_masks_refused(masks):
    with pytest.raises(SystemExit):
        bt.parse_masks(masks)


def test_burn_refuses_extra_arguments_before_any_connection():
    with pytest.raises(SystemExit):
        bt.main(["ZVHW8B35", "--count", "3"])


# --- mint_mcp_token.py: same shape (CIO yes, 2026-10-09) ---

import mint_mcp_token as mm  # noqa: E402


def _mm(email="a@b.com", user_id=None, label="alpha-tester", days=None):
    return SimpleNamespace(user_email=email, user_id=user_id, label=label, expires_days=days)


@pytest.mark.parametrize(
    "ns",
    [
        _mm(),
        _mm(email=None, user_id="12345678-1234-5678-1234-567812345678"),
        _mm(days=30),
        _mm(label="x.y:z-1"),
    ],
)
def test_mcp_mint_good_args_pass(ns):
    mm._validate(ns)


@pytest.mark.parametrize(
    "ns",
    [
        _mm(email="a@b.com; rm x"),
        _mm(email="-a@b.com"),
        _mm(email=None, user_id="not-a-uuid"),
        _mm(label="alpha tester"),
        _mm(label="--apply"),
        _mm(label=""),
        _mm(days=0),
        _mm(days=366),
    ],
)
def test_mcp_mint_bad_args_refused(ns):
    with pytest.raises(SystemExit):
        mm._validate(ns)
