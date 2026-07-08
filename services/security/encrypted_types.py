"""#358-B: EncryptedString — SQLAlchemy TypeDecorator for transparent at-rest field encryption.

Wraps ``FieldEncryptionService`` (AES-256-GCM, dimension A) at the ORM boundary: plaintext
in the application, ciphertext in the database. A version **marker prefix** (``PMENC1:``)
distinguishes encrypted values from legacy plaintext, so a target column is safe to read
during a backfill (mixed plaintext + ciphertext) and becomes effectively *strict* once every
row is encrypted (an unmarked value is then simply legacy; a marked-but-undecryptable value
is a real error, never silently returned).

Key resolution:
- inject an encryptor (tests, or a custom service) via ``encryptor=``;
- otherwise resolve from ``ENCRYPTION_MASTER_KEY`` via ``FieldEncryptionService.from_env()`` per
  call (env changes take effect immediately; the DB round-trip dominates a read, so per-call
  resolution is negligible).

No master key configured → values pass through as plaintext on write (logged once) so local
dev / pre-key environments keep working. The Phase-3 backfill refuses to run without the key,
so production never silently stores plaintext *under* the encryption marker.

Security: this layer logs no values — never the master key, the plaintext, or the ciphertext.
"""

from __future__ import annotations

import logging
from typing import Optional

from sqlalchemy import Text
from sqlalchemy.types import TypeDecorator

from services.security.field_encryption import DecryptionError, FieldEncryptionService

logger = logging.getLogger(__name__)

# Version-tagged so a future encryption scheme can coexist with v1 ciphertext.
MARKER = "PMENC1:"

# Sentinel: distinguishes "no encryptor injected" (→ resolve from env) from an
# explicit ``encryptor=None`` (→ deliberately keyless, e.g. a no-key test).
_UNSET = object()

_warned_no_key = False


class EncryptedString(TypeDecorator):
    """Transparent at-rest encryption for a ``Text`` column.

    - bind (save):   ``plaintext`` → ``MARKER + service.encrypt(value, context)``
    - result (load): ``MARKER``-prefixed → ``service.decrypt(...)`` (``DecryptionError``
      propagates on tamper / wrong key); unmarked → plaintext passthrough (legacy row)

    ``None`` passes through untouched. The ``context`` label selects a per-field HKDF
    subkey, so ciphertext from one column can't be decrypted as another.
    """

    impl = Text
    cache_ok = True  # encryption is invisible to SQL compilation (always Text)

    def __init__(self, context: str, *args, encryptor=_UNSET, **kwargs):
        if not context:
            raise ValueError("EncryptedString requires a non-empty context label")
        self._context = context
        self._injected = encryptor
        super().__init__(*args, **kwargs)

    @property
    def _service(self) -> Optional[FieldEncryptionService]:
        if self._injected is not _UNSET:
            return self._injected
        return FieldEncryptionService.from_env()

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        svc = self._service
        if svc is None:
            global _warned_no_key
            if not _warned_no_key:
                logger.warning(
                    "ENCRYPTION_MASTER_KEY unset — EncryptedString storing plaintext "
                    "(non-prod fallback; the #358-B backfill refuses to run without the key)"
                )
                _warned_no_key = True
            return value
        return MARKER + svc.encrypt(value, self._context)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if not value.startswith(MARKER):
            return value  # legacy plaintext (pre-backfill row)
        svc = self._service
        if svc is None:
            # Marked ciphertext but no key: do NOT silently return the raw token.
            raise DecryptionError("encrypted value present but ENCRYPTION_MASTER_KEY is unset")
        token = value[len(MARKER) :]
        return svc.decrypt(token, self._context)  # DecryptionError propagates


class EncryptedJSON(TypeDecorator):
    """#1305: transparent at-rest encryption for a JSON/JSONB column.

    Two modes, one default-safe design (Arch's ratified condition, 2026-07-07):

    - **Full-value mode** (no whitelist): the whole JSON value is serialized and
      encrypted; the column stores a single JSON *string* — ``"PMENC1:<token>"``
      — which is valid JSON, so the column type (JSONB/JSON) is untouched.
    - **Leaf-split mode** (``plaintext_whitelist=(...)``): for dict values, the
      whitelisted keys stay as plaintext JSON leaves (server-side SQL on them —
      e.g. ``pattern_data -> 'action_type'`` — keeps working) and **everything
      else** is encrypted under a single ``_enc`` leaf. The split is
      DEFAULT-ENCRYPT: a key not on the whitelist is encrypted *by construction*
      — a future PII field added to the payload lands encrypted without anyone
      remembering to update anything (encrypt-a-named-blacklist is the drift
      class this design exists to prevent).

    Read side mirrors ``EncryptedString``'s contract exactly: an unmarked value
    (a plain dict/list without ``_enc``, or a non-marker string) is legacy
    plaintext and passes through (pre-backfill compatibility); a marked value
    without a key raises ``DecryptionError`` (fail closed, never return the raw
    token); ``None`` passes through.
    """

    impl = Text  # overridden per-column via load_dialect_impl of the declared type
    cache_ok = True

    _ENC_KEY = "_enc"

    def __init__(
        self,
        context: str,
        *args,
        plaintext_whitelist: tuple = (),
        encryptor=_UNSET,
        **kwargs,
    ):
        if not context:
            raise ValueError("EncryptedJSON requires a non-empty context label")
        self._context = context
        self._whitelist = tuple(plaintext_whitelist)
        self._injected = encryptor
        super().__init__(*args, **kwargs)

    def load_dialect_impl(self, dialect):
        # Keep the underlying column type JSONB on Postgres / JSON elsewhere —
        # ciphertext is stored as a JSON string (or an object with an ``_enc``
        # string leaf), both valid JSON, so no column-type migration is needed.
        from sqlalchemy import JSON as _JSON
        from sqlalchemy.dialects import postgresql as _pg

        if dialect.name == "postgresql":
            return dialect.type_descriptor(_pg.JSONB())
        return dialect.type_descriptor(_JSON())

    def compare_against_backend(self, dialect, conn_type):
        # #1312: alembic autogenerate reflects the DB column as plain JSON or JSONB
        # and would flag every EncryptedJSON column as a type change forever
        # (learned_patterns.pattern_data is `json` in the DB while the dialect impl
        # is JSONB). Ciphertext is valid JSON under either — the whole JSON family
        # is equivalent for comparison purposes.
        from sqlalchemy import JSON as _JSON

        return isinstance(conn_type, _JSON)

    def coerce_compared_value(self, op, value):
        # Without this, SQLAlchemy runs comparison/index operands through THIS
        # type's bind processor — so the literal key in
        # ``pattern_data.op("->")("action_type")`` would itself get ENCRYPTED
        # and typed JSONB (`json -> jsonb`: no such operator), breaking the one
        # server-side query the leaf-split whitelist exists to preserve
        # (learning_handler.py:396). Delegating to the plain JSON type binds
        # path/index operands as text/int, exactly as before encryption — the
        # SQLAlchemy-documented recipe for TypeDecorator-around-JSON. Caught by
        # the real-Postgres proof test, not the unit tests.
        from sqlalchemy import JSON as _JSON

        return _JSON().coerce_compared_value(op, value)

    @property
    def _service(self) -> Optional[FieldEncryptionService]:
        if self._injected is not _UNSET:
            return self._injected
        return FieldEncryptionService.from_env()

    # -- write ---------------------------------------------------------------
    def process_bind_param(self, value, dialect):
        import json as _json

        if value is None:
            return None
        svc = self._service
        if svc is None:
            global _warned_no_key
            if not _warned_no_key:
                logger.warning(
                    "ENCRYPTION_MASTER_KEY unset — EncryptedJSON storing plaintext "
                    "(non-prod fallback; the #1305 backfill refuses to run without the key)"
                )
                _warned_no_key = True
            return value

        if self._whitelist and isinstance(value, dict):
            # Leaf-split: whitelisted keys plaintext, EVERYTHING ELSE encrypted.
            plain = {k: v for k, v in value.items() if k in self._whitelist}
            rest = {k: v for k, v in value.items() if k not in self._whitelist}
            plain[self._ENC_KEY] = MARKER + svc.encrypt(
                _json.dumps(rest, default=str), self._context
            )
            return plain
        # Full-value: the whole payload becomes one encrypted JSON string.
        return MARKER + svc.encrypt(_json.dumps(value, default=str), self._context)

    # -- read ----------------------------------------------------------------
    def process_result_value(self, value, dialect):
        import json as _json

        if value is None:
            return None

        # Leaf-split shape: dict carrying our _enc leaf.
        if isinstance(value, dict) and self._ENC_KEY in value:
            token_str = value[self._ENC_KEY]
            if not isinstance(token_str, str) or not token_str.startswith(MARKER):
                return value  # not ours — legacy dict that happens to have _enc
            svc = self._service
            if svc is None:
                raise DecryptionError(
                    "encrypted JSON leaf present but ENCRYPTION_MASTER_KEY is unset"
                )
            rest = _json.loads(svc.decrypt(token_str[len(MARKER) :], self._context))
            merged = {k: v for k, v in value.items() if k != self._ENC_KEY}
            merged.update(rest)
            return merged

        # Full-value shape: a marker-prefixed JSON string.
        if isinstance(value, str) and value.startswith(MARKER):
            svc = self._service
            if svc is None:
                raise DecryptionError(
                    "encrypted JSON value present but ENCRYPTION_MASTER_KEY is unset"
                )
            return _json.loads(svc.decrypt(value[len(MARKER) :], self._context))

        return value  # legacy plaintext (pre-backfill row)
