"""prod_user_lookup.py — the boundary is the payload (CIO 2026-10-09, option 3):
argument refusal, masking, and READ ONLY before any query, all pinned here."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))

import prod_user_lookup as lk  # noqa: E402


@pytest.mark.parametrize(
    "argv",
    [
        [],
        ["a", "b"],
        ["x; rm -rf /"],
        ["$(whoami)"],
        ["a b"],
        ["--drop"],
        ["'or'1'='1"],
        ["x" * 255],
    ],
)
def test_refuses_anything_but_one_safe_identifier_or_all(argv):
    with pytest.raises(SystemExit):
        lk.parse_args(argv)


@pytest.mark.parametrize(
    "arg", ["sachio222", "janne@example.com", "web-agent", "a.b+c@d.io", "--all"]
)
def test_accepts_safe_identifiers(arg):
    assert lk.parse_args([arg]) == arg


def test_masks_the_email_to_one_character_and_the_domain():
    assert lk.mask_email("janne@example.com") == "j…@example.com"
    assert lk.mask_email("") == "(none)"
    assert lk.mask_email("no-at-sign") == "(none)"


def test_read_only_is_set_before_any_select_and_only_masked_columns_print(capsys):
    calls = []
    conn = MagicMock()

    def _exec(stmt, params=None):
        calls.append(str(stmt))
        res = MagicMock()
        res.fetchall.return_value = [
            ("janne", "janne@example.com", True, False, "2026-09-01", None)
        ]
        return res

    conn.execute.side_effect = _exec
    engine = MagicMock()
    engine.connect.return_value.__enter__.return_value = conn
    fake_mint = MagicMock(
        _database_url=lambda: ("postgresql://h/db", "test"), _redacted=lambda u: "h/db"
    )
    with (
        patch.dict(sys.modules, {"mint_invite_tokens": fake_mint}),
        patch("sqlalchemy.create_engine", return_value=engine),
    ):
        assert lk.main(["janne"]) == 0
    assert calls[0] == "SET TRANSACTION READ ONLY"
    assert (
        "SELECT username, email, is_active, setup_complete, created_at, last_login_at" in calls[1]
    )
    assert "password" not in calls[1] and " id" not in calls[1]
    out = capsys.readouterr().out
    assert "j…@example.com" in out and "janne@example.com" not in out
