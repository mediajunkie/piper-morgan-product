"""#1382 tier-2 — encrypted-at-rest DB credential store (the hosted keychain).

Hosted Linux containers have no OS keyring backend (python-keyring resolves to
``keyring.backends.fail.Keyring``, whose every operation raises — found live on
alpha 2026-07-08, where it broke OAuth token storage and all keychain reads).
This store is the drop-in fallback BEHIND the ``KeychainService`` seam: same
composed key names, values encrypted with ``FieldEncryptionService`` under a
per-name HKDF context (``secure_credentials.{name}``) into the
``secure_credentials`` table (migration g1382creds). No plaintext is ever
written; with no master key the store REFUSES to construct (fail closed) —
``keyrings.alt``-style plaintext fallbacks are explicitly rejected.

Sync by design: ``KeychainService`` is a sync interface called from sync and
async contexts alike. Credential ops are settings/connect-time rare, so a
small dedicated sync engine (NOT the app's async pool) is the honest trade —
flagged in the 2026-07-09 design memo to Arch.

Relationship to the connector-binding rail (ADR-070): this is the general
hosted store; each connector's #1232-contract port migrates its grant onto the
binding rail as it lands, shrinking this store's connector share naturally.
"""

from __future__ import annotations

import threading
from typing import List, Optional

import structlog
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

logger = structlog.get_logger(__name__)

_CONTEXT_PREFIX = "secure_credentials."


class EncryptedDBCredentialStore:
    """Encrypted credential storage in Postgres, keyed by composed name."""

    def __init__(self, encryptor=None, engine=None):
        if encryptor is None:
            from services.security.field_encryption import FieldEncryptionService

            encryptor = FieldEncryptionService.from_env()
        if encryptor is None:
            # Fail closed: no master key means no secure place to put a secret.
            raise RuntimeError(
                "EncryptedDBCredentialStore requires ENCRYPTION_MASTER_KEY — "
                "refusing to store credentials without encryption (#1382)."
            )
        self._encryptor = encryptor
        self._engine = engine
        self._engine_lock = threading.Lock()

    def _get_engine(self):
        if self._engine is None:
            with self._engine_lock:
                if self._engine is None:
                    from services.database.session_factory import get_sync_migration_url

                    # NullPool per the Arch concur's build-note (2026-07-09):
                    # "short-lived = actually short-lived." Ops are rare
                    # (connect/settings-time), so every op opens and truly
                    # closes its connection — no idle sync connection parked
                    # against Postgres for the process lifetime.
                    self._engine = create_engine(
                        get_sync_migration_url(), poolclass=NullPool
                    )
        return self._engine

    def store(self, name: str, value: str) -> None:
        encrypted = self._encryptor.encrypt(value, _CONTEXT_PREFIX + name)
        with self._get_engine().begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO secure_credentials (name, encrypted_value) "
                    "VALUES (:name, :val) "
                    "ON CONFLICT (name) DO UPDATE SET "
                    "encrypted_value = EXCLUDED.encrypted_value, updated_at = now()"
                ),
                {"name": name, "val": encrypted},
            )
        logger.info("credential_stored_db", name=name)

    def get(self, name: str) -> Optional[str]:
        with self._get_engine().connect() as conn:
            row = conn.execute(
                text("SELECT encrypted_value FROM secure_credentials WHERE name = :name"),
                {"name": name},
            ).first()
        if row is None:
            return None
        return self._encryptor.decrypt(row[0], _CONTEXT_PREFIX + name)

    def delete(self, name: str) -> bool:
        with self._get_engine().begin() as conn:
            result = conn.execute(
                text("DELETE FROM secure_credentials WHERE name = :name"), {"name": name}
            )
        deleted = result.rowcount > 0
        if deleted:
            logger.info("credential_deleted_db", name=name)
        return deleted

    def list_names(self) -> List[str]:
        with self._get_engine().connect() as conn:
            rows = conn.execute(text("SELECT name FROM secure_credentials ORDER BY name")).all()
        return [r[0] for r in rows]
