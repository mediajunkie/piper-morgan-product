"""#2157 proof 4: the decrypt check prints one word and leaks nothing."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

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


def test_main_prints_exactly_one_word(capsys):
    with (
        patch.object(v, "one_encrypted_row", return_value=("github", "enc")),
        patch(
            "services.security.field_encryption.FieldEncryptionService.from_env",
            return_value=_Enc("s"),
        ),
    ):
        code = v.main(["--database-url", "postgres://u:p@h/db"])
    out = capsys.readouterr()
    assert out.out == "ok\n" and out.err == "" and code == 0


def test_main_prints_fail_and_nothing_else_when_the_db_is_unreadable(capsys):
    with patch.object(v, "one_encrypted_row", side_effect=RuntimeError("secret://host")):
        code = v.main(["--database-url", "postgres://u:p@h/db"])
    out = capsys.readouterr()
    assert out.out == "fail\n" and "secret" not in out.err and code == v.EXIT_DB_UNREADABLE


def test_no_url_is_fail():
    with patch.dict("os.environ", {}, clear=False):
        import os

        os.environ.pop("DATABASE_URL", None)
        assert v.main([]) == v.EXIT_DB_UNREADABLE
