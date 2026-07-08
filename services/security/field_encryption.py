"""#358 SEC-ENCRYPT-ATREST — field-level encryption (AES-256-GCM, HKDF per-field).

One reusable primitive for the per-user secret store (#1185 floor) and, later, the
content/PII fields. AES-256-GCM gives **authenticated** encryption (confidentiality +
tamper-detection via the GCM tag). A per-field subkey is derived from the master key via
HKDF-SHA256 keyed by a context label, so a compromise/rotation of one field's subkey does
not cross-contaminate others. The master key comes from ``ENCRYPTION_MASTER_KEY``
(KEK-from-env now; AWS-KMS is the later path, #482).

Security properties (load-bearing — keep them):
- the master key, derived subkeys, nonce, and plaintext are **never logged** (repr is key-safe);
- a **unique random nonce** per encryption (never reuse under one key);
- a wrong key / wrong context / tampered token **raises** ``DecryptionError`` — never
  returns garbage plaintext.
"""

from __future__ import annotations

import base64
import os
from typing import Optional

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

_KEY_LEN = 32  # AES-256
_NONCE_LEN = 12  # AES-GCM standard nonce length

ENV_MASTER_KEY = "ENCRYPTION_MASTER_KEY"


class DecryptionError(Exception):
    """Raised when a token can't be decrypted (wrong key/context, or tampered)."""


class FieldEncryptionService:
    """AES-256-GCM field encryptor with HKDF per-field subkeys.

    Token format = ``base64(nonce ‖ ciphertext+tag)``. The ``context`` label
    (e.g. ``"user_api_keys.secret"``) selects an HKDF-derived subkey, so one master
    key safely protects many independent fields.
    """

    def __init__(self, master_key: bytes):
        if not isinstance(master_key, (bytes, bytearray)) or len(master_key) != _KEY_LEN:
            got = (
                f"{len(master_key)} bytes"
                if isinstance(master_key, (bytes, bytearray))
                else type(master_key).__name__
            )
            raise ValueError(f"master_key must be {_KEY_LEN} bytes (AES-256); got {got}")
        self._master_key = bytes(master_key)

    @classmethod
    def from_env(cls, env_var: str = ENV_MASTER_KEY) -> Optional["FieldEncryptionService"]:
        """Build from a base64 master key in the environment, or ``None`` if unset.

        ``None`` lets callers fall back gracefully (e.g. local dev without the env
        var → the OS keychain), rather than hard-failing.
        """
        raw = os.getenv(env_var)
        if not raw:
            return None
        try:
            key = base64.b64decode(raw)
        except Exception as e:  # a malformed env value is a hard config error
            raise ValueError(f"{env_var} is not valid base64") from e
        return cls(key)

    def _subkey(self, context: str) -> bytes:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=_KEY_LEN,
            salt=None,
            info=context.encode("utf-8"),
        )
        return hkdf.derive(self._master_key)

    def encrypt(self, plaintext: str, context: str) -> str:
        aes = AESGCM(self._subkey(context))
        nonce = os.urandom(_NONCE_LEN)
        ct = aes.encrypt(nonce, plaintext.encode("utf-8"), None)
        return base64.b64encode(nonce + ct).decode("ascii")

    def encrypt_bytes(self, plaintext: bytes, context: str) -> bytes:
        """#1306: bytes-native sibling of encrypt() for file content — same
        AES-256-GCM + per-context HKDF subkey; raw binary out (nonce + ct),
        no base64 (files are stored as bytes, not text columns)."""
        aes = AESGCM(self._subkey(context))
        nonce = os.urandom(_NONCE_LEN)
        return nonce + aes.encrypt(nonce, plaintext, None)

    def decrypt_bytes(self, blob: bytes, context: str) -> bytes:
        """#1306: bytes-native sibling of decrypt(). Raises DecryptionError on
        tamper/wrong-key/short input, mirroring decrypt()'s contract."""
        try:
            nonce, ct = blob[:_NONCE_LEN], blob[_NONCE_LEN:]
            aes = AESGCM(self._subkey(context))
            return aes.decrypt(nonce, ct, None)
        except (InvalidTag, ValueError) as e:
            raise DecryptionError(f"file-content decryption failed: {type(e).__name__}") from e

    def decrypt(self, token: str, context: str) -> str:
        try:
            raw = base64.b64decode(token)
            nonce, ct = raw[:_NONCE_LEN], raw[_NONCE_LEN:]
            aes = AESGCM(self._subkey(context))
            return aes.decrypt(nonce, ct, None).decode("utf-8")
        except (InvalidTag, ValueError) as e:
            raise DecryptionError("decryption failed (wrong key/context or tampered token)") from e

    def __repr__(self) -> str:  # never expose key material
        return f"<FieldEncryptionService key=***{_KEY_LEN}B>"
