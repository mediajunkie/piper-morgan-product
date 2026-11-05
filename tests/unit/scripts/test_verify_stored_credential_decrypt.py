"""#2157 proof 4: the decrypt check prints one word (``ok`` or ``fail:<code>``) and leaks
nothing; the URL is required and never the process's own live database (Arch 18:34)."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import verify_stored_credential_decrypt as v  # noqa: E402


class _Enc:
    def __init__(self, plaintext=None, raise_=False):
        self.p, self.r = plaintext, raise_

    def decrypt(self, token, context):
        if self.r:
            raise ValueError("bad key")
        return self.p


def test_ok_when_the_secret_decrypts():
    assert v.verdict(("github", "enc"), _Enc("ghp_x")) == ("ok", v.EXIT_OK)


def test_fail_when_decrypt_raises_and_the_error_is_swallowed():
    assert v.verdict(("github", "enc"), _Enc(raise_=True)) == ("fail", v.EXIT_DECRYPT_FAILED)


def test_fail_when_no_row():
    assert v.verdict(None, _Enc("x")) == ("fail", v.EXIT_NO_ROW)


def test_fail_when_this_process_holds_no_key():
    assert v.verdict(("github", "enc"), None) == ("fail", v.EXIT_NO_KEY)


def test_main_prints_exactly_one_word(capsys, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://u:p@alpha-db.flycast/db")
    with (
        patch.object(v, "one_encrypted_row", return_value=("github", "enc")),
        patch(
            "services.security.field_encryption.FieldEncryptionService.from_env",
            return_value=_Enc("s"),
        ),
    ):
        code = v.main(["--database-url", "postgres://u:p@drill-db.flycast/db"])
    out = capsys.readouterr()
    assert out.out == "ok\n" and out.err == "" and code == 0


def test_fail_carries_its_code_and_nothing_else_when_the_db_is_unreadable(capsys, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with patch.object(v, "one_encrypted_row", side_effect=RuntimeError("secret://host")):
        code = v.main(["--database-url", "postgres://u:p@h/db"])
    out = capsys.readouterr()
    assert out.out == "fail:4\n" and "secret" not in out.err and code == v.EXIT_DB_UNREADABLE


def test_the_url_is_required():
    with pytest.raises(SystemExit):
        v.main([])


def test_the_processs_own_live_database_is_refused(capsys, monkeypatch):
    """Arch 18:34: inside alpha's container DATABASE_URL is alpha; the proof must never
    point there, whatever the credentials in the URL."""
    monkeypatch.setenv(
        "DATABASE_URL", "postgresql+asyncpg://piper:x@piper-morgan-db.flycast:5432/piper_morgan"
    )
    with patch.object(v, "one_encrypted_row", side_effect=AssertionError("must not be read")):
        code = v.main(
            ["--database-url", "postgres://postgres:y@PIPER-MORGAN-DB.flycast:5432/piper_morgan"]
        )
    out = capsys.readouterr()
    assert out.out == "fail:5\n" and code == v.EXIT_SAME_HOST_AS_LIVE


def test_a_different_host_is_not_refused():
    assert (
        v.refuses_live_database("postgres://u:p@drill.flycast/db", "postgres://u:p@live.flycast/db")
        is False
    )
    assert v.refuses_live_database("postgres://u:p@drill.flycast/db", None) is False


def test_words():
    assert v.word(0) == "ok" and v.word(2) == "fail:2"
