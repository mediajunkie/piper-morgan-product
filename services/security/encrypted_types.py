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
