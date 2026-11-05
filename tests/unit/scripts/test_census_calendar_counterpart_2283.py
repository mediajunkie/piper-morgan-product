"""#2283 (Arch 2026-11-04 21:29): the census's Calendar counterpart classifies each stored
Calendar token by the Google account it opens, and prints counts and account ids only."""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import github_identity_census as census  # noqa: E402

A, B, C, D = "a-2283", "b-2283", "c-2283", "d-2283"
USERS = [
    SimpleNamespace(id=A, email="Alice@example.invalid"),  # opens her own (case differs)
    SimpleNamespace(id=B, email="bob@example.invalid"),  # opens ALICE's: a crossing
    SimpleNamespace(id=C, email="cat@example.invalid"),  # opens a personal account
    SimpleNamespace(id=D, email="dan@example.invalid"),  # no token stored
]
TOKENS = {f"google_calendar_{A}": "rA", f"google_calendar_{B}": "rB", f"google_calendar_{C}": "rC"}
OPENS = {
    "rA": "alice@example.invalid",
    "rB": "alice@example.invalid",
    "rC": "cat.personal@example.invalid",
}


def _run(capsys):
    session = MagicMock()
    session.execute = AsyncMock(return_value=MagicMock(all=lambda: USERS))
    keychain = MagicMock()
    keychain.aget_api_key = AsyncMock(side_effect=lambda k: TOKENS.get(k))
    with (
        patch("services.infrastructure.keychain_service.KeychainService", return_value=keychain),
        patch.object(
            census, "_google_email_for_refresh_token", AsyncMock(side_effect=lambda t: OPENS[t])
        ),
    ):
        asyncio.run(census._verify_calendar(session))
    return capsys.readouterr().out


def test_counts_and_the_one_crossing(capsys):
    out = _run(capsys)
    assert "'accounts with a stored Calendar token': 3" in out
    assert "'opens its own sign-in email': 1" in out
    assert "'opens ANOTHER Piper account email (CROSSING)': 1" in out
    assert "'opens another Google account of no Piper account (not printed)': 1" in out
    assert f"CROSSING: account {B} holds a Calendar token for account {A}'s email" in out


def test_no_address_is_ever_printed(capsys):
    out = _run(capsys)
    assert "@" not in out


def test_the_flag_exists():
    src = (Path(census.__file__)).read_text()
    assert '"--verify-calendar"' in src and "verify_calendar=args.verify_calendar" in src
