#!/usr/bin/env python3
"""verify_stored_credential_decrypt.py — READ-ONLY proof that ONE stored credential decrypts
under this process's ``ENCRYPTION_MASTER_KEY``. Prints ``ok``, or ``fail:<code>``.

#2157's restore drill, proof 4 (Arch's safe form, 2026-11-04 16:38): a restored copy of
``piper-morgan-db`` is only a backup if the secrets in it still decrypt under the key the
deployment holds. This script reads one active ``user_api_keys`` row that has an encrypted
secret, decrypts it under the row's provider context, and prints ``ok`` when the plaintext
comes back, ``fail`` otherwise. It never prints a provider, an id, a user, a value or an
error. The code beside ``fail`` says why (1 decrypt failed, 2 no row, 3 no key in this
process, 4 the database could not be read, 5 the URL names this process's own live database,
which is never the thing being proved); it is also the exit status.

Where it runs: inside alpha's container, which holds the key, pointed at the DRILL copy over
the private network (never at alpha's own database during the drill; the copy is the thing
being proved):

    fly ssh console -a piper-morgan -C "python /app/scripts/verify_stored_credential_decrypt.py \
        --database-url postgres://postgres:<drill-password>@piper-morgan-db-drill.flycast:5432/piper_morgan"

No Piper app boots against the copy (Arch's rule 2): this is one SELECT and one decrypt.
``--database-url`` is required (Arch 18:34): no default, so a dropped flag never proves alpha.

Concept: docs/internal/operations/restore-drill-2157-lead-half-fly-lines-DRAFT-2026-11-04.md
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

EXIT_OK, EXIT_DECRYPT_FAILED, EXIT_NO_ROW, EXIT_NO_KEY, EXIT_DB_UNREADABLE = 0, 1, 2, 3, 4
EXIT_SAME_HOST_AS_LIVE = 5  # the URL names the process's own live database, not a copy


def _host(url: str) -> str:
    from urllib.parse import urlsplit

    try:
        return (urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def refuses_live_database(url: str, live_url: Optional[str]) -> bool:
    """Arch 2026-11-04 18:34: inside alpha's container ``DATABASE_URL`` is alpha's live
    database; a proof pointed there would print ``ok`` about the wrong thing. The URL's
    host must differ from the live one."""
    if not live_url:
        return False
    return _host(url) != "" and _host(url) == _host(live_url)


def word(code: int) -> str:
    """``ok`` on success, else ``fail:<code>``: ``fly ssh console -C`` may not hand the
    exit status back, and a code carries no secret."""
    return "ok" if code == EXIT_OK else f"fail:{code}"


def one_encrypted_row(url: str) -> Optional[Tuple[str, str]]:
    """``(provider, encrypted_secret)`` of one active row with a secret, else None.
    The oldest row by id, so repeated proofs read the same one."""
    from prod_db import _to_sync_url
    from sqlalchemy import create_engine, text

    sql = text(
        "SELECT provider, encrypted_secret FROM user_api_keys "
        "WHERE is_active AND encrypted_secret IS NOT NULL ORDER BY id LIMIT 1"
    )
    with create_engine(_to_sync_url(url)).connect() as c:
        row = c.execute(sql).first()
    return (str(row[0]), str(row[1])) if row else None


def verdict(row: Optional[Tuple[str, str]], encryptor) -> Tuple[str, int]:
    """The one word and the exit code. Never raises, never returns the plaintext."""
    if encryptor is None:
        return "fail", EXIT_NO_KEY
    if row is None:
        return "fail", EXIT_NO_ROW
    provider, token = row
    try:
        from services.security.user_api_key_service import secret_context

        plaintext = encryptor.decrypt(token, secret_context(provider))
    except Exception:
        return "fail", EXIT_DECRYPT_FAILED
    return ("ok", EXIT_OK) if plaintext else ("fail", EXIT_DECRYPT_FAILED)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="prints ok or fail; nothing else")
    parser.add_argument(
        "--database-url",
        required=True,
        help="the COPY's URL; required, and never the process's own DATABASE_URL host",
    )
    ns = parser.parse_args(argv)
    if refuses_live_database(ns.database_url, os.environ.get("DATABASE_URL")):
        print(word(EXIT_SAME_HOST_AS_LIVE))
        return EXIT_SAME_HOST_AS_LIVE
    try:
        from services.security.field_encryption import FieldEncryptionService

        encryptor = FieldEncryptionService.from_env()
    except Exception:
        encryptor = None
    try:
        row = one_encrypted_row(ns.database_url)
    except Exception:
        print(word(EXIT_DB_UNREADABLE))
        return EXIT_DB_UNREADABLE
    _, code = verdict(row, encryptor)
    print(word(code))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
